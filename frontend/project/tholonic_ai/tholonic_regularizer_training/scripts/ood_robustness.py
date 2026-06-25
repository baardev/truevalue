#!/usr/bin/env python3
"""
EXPERIMENT 1.3 — OUT-OF-DISTRIBUTION ROBUSTNESS (revised protocol)

Tests whether tholonically-trained models generalise better to out-of-distribution
inputs than matched standard (baseline) models.

Protocol:
  Load the 6 Row 2 checkpoints (3 baseline, 3 tholonic seeds) from Experiment 1.1.
  Evaluate each on:
    - WikiText-103 validation  (in-distribution, ID)
    - AG News test set         (medium-OOD: news domain, ~1M tokens of English prose)
    - Prose fallback corpus    (hardcoded ~4K tokens of news/history prose;
                                used only if AG News download fails)

  Previous attempt used WikiText-2 (same domain as ID, ratio ~1.0) and a 1,661-token
  corpus containing Python code and SQL (categorically wrong domain — not a prose shift).
  Both were uninformative. This revised protocol uses a proper medium-shift prose domain.

  Metric: perplexity ratio = OOD_ppl / ID_ppl  (lower = more robust)

  Pass criterion: tholonic models have lower mean perplexity ratio than baseline
  for >= 2 of 3 seeds (matched-pair comparison, same random seed).

Output: ood_robustness_results.json
"""

import json, math, sys
from pathlib import Path
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import GPT2TokenizerFast

try:
    from datasets import load_dataset
    HAS_DATASETS = True
except ImportError:
    HAS_DATASETS = False
    print("WARNING: datasets not installed. Run: pip install datasets")

# ── paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
BASE_DIR    = SCRIPT_DIR.parent
CKPT_DIR    = BASE_DIR / "checkpoints"
OUT_DIR     = BASE_DIR / "results"
RESULTS_FILE = OUT_DIR / "ood_robustness_results.json"
DATA_CACHE  = OUT_DIR / "wikitext103_tokens.pt"

# ── constants matching the training script ─────────────────────────────────────
DEVICE    = "cpu"  # force CPU: inference only, models are small; avoids VRAM contention
VOCAB_SIZE = 50257
ROW2_D      = 768
ROW2_HEADS  = 12
ROW2_LAYERS = 12
SEQ_LEN     = 256
SEEDS       = [42, 7, 13]
# eval up to this many tokens per domain (keeps runtime predictable)
MAX_TOKENS  = 256_000

# ── model (identical to train_experiments_full.py) ─────────────────────────────

class CausalMHA(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.h, self.dh = h, d // h
        self.qkv      = nn.Linear(d, 3 * d, bias=False)
        self.out_proj = nn.Linear(d, d,     bias=False)

    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.qkv(x).split(C, -1)
        def sp(t): return t.reshape(B, T, self.h, self.dh).transpose(1, 2)
        q, k, v = sp(q), sp(k), sp(v)
        mask = torch.triu(torch.full((T, T), float("-inf"), device=x.device), 1)
        attn = F.softmax(q @ k.transpose(-2, -1) / math.sqrt(self.dh) + mask, -1)
        return self.out_proj((attn @ v).transpose(1, 2).reshape(B, T, C))


class MLP(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.fc1    = nn.Linear(d, 4 * d, bias=False)
        self.c_proj = nn.Linear(4 * d, d, bias=False)

    def forward(self, x):
        return self.c_proj(F.gelu(self.fc1(x)))


class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.ln_1 = nn.LayerNorm(d)
        self.attn = CausalMHA(d, h)
        self.ln_2 = nn.LayerNorm(d)
        self.mlp  = MLP(d)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class GPTModel(nn.Module):
    def __init__(self, vocab=VOCAB_SIZE, d=ROW2_D, n_layers=ROW2_LAYERS,
                 n_heads=ROW2_HEADS, seq=SEQ_LEN):
        super().__init__()
        self.wte    = nn.Embedding(vocab, d)
        self.wpe    = nn.Embedding(seq, d)
        self.blocks = nn.ModuleList([Block(d, n_heads) for _ in range(n_layers)])
        self.ln_f   = nn.LayerNorm(d)
        self.head   = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.wte.weight

    def forward(self, x):
        B, T = x.shape
        h = self.wte(x) + self.wpe(torch.arange(T, device=x.device))
        for blk in self.blocks:
            h = blk(h)
        return self.head(self.ln_f(h))


# ── checkpoint loader ─────────────────────────────────────────────────────────

def load_model(ckpt_path):
    model = GPTModel().to(DEVICE)
    ckpt  = torch.load(ckpt_path, map_location=DEVICE, weights_only=False)
    model.load_state_dict(ckpt["model"])
    model.eval()
    return model


# ── perplexity evaluation ─────────────────────────────────────────────────────

@torch.no_grad()
def compute_perplexity(model, token_ids, seq_len=SEQ_LEN, max_tokens=MAX_TOKENS):
    """
    Compute perplexity over token_ids using non-overlapping windows of seq_len.
    Stops after max_tokens tokens to keep runtime bounded.
    """
    token_ids = token_ids[:max_tokens]
    n = len(token_ids)
    total_loss = 0.0
    total_tokens = 0
    stride = seq_len

    for start in range(0, n - stride, stride):
        x = token_ids[start : start + stride].unsqueeze(0).to(DEVICE)
        y = token_ids[start + 1 : start + stride + 1].unsqueeze(0).to(DEVICE)
        with torch.amp.autocast("cuda", enabled=torch.cuda.is_available()):
            logits = model(x)
        loss = F.cross_entropy(logits.view(-1, VOCAB_SIZE), y.view(-1), reduction="sum")
        total_loss   += loss.item()
        total_tokens += y.numel()

    if total_tokens == 0:
        return float("nan")
    nll = total_loss / total_tokens
    return math.exp(nll)


# ── data loading ──────────────────────────────────────────────────────────────

def load_id_data(tok):
    """WikiText-103 validation tokens (in-distribution)."""
    if DATA_CACHE.exists():
        d = torch.load(DATA_CACHE, weights_only=True)
        return d["val"]

    if not HAS_DATASETS:
        raise RuntimeError("datasets library required; pip install datasets")

    print("  Downloading WikiText-103 ...", flush=True)
    ds  = load_dataset("wikitext", "wikitext-103-raw-v1")
    texts = [t for t in ds["validation"]["text"] if t.strip()]
    joined = tok.eos_token.join(texts)
    val_ids = torch.tensor(tok.encode(joined), dtype=torch.long)
    # Save for later (don't overwrite full cache if train split isn't here)
    if not DATA_CACHE.exists():
        torch.save({"val": val_ids}, DATA_CACHE)
    return val_ids


def tokenize_dataset(dataset_name, config_name, split, text_key, tok, max_chars=4_000_000):
    """Download and tokenize any text dataset."""
    label = config_name or dataset_name
    print(f"  Loading {dataset_name}/{label} ({split}) ...", flush=True)
    kwargs = dict(split=split)
    if config_name is not None:
        ds = load_dataset(dataset_name, config_name, **kwargs)
    else:
        ds = load_dataset(dataset_name, **kwargs)
    texts = [t for t in ds[text_key] if t and t.strip()]
    joined = tok.eos_token.join(texts)[:max_chars]
    ids    = torch.tensor(tok.encode(joined), dtype=torch.long)
    print(f"    Tokens: {len(ids):,}", flush=True)
    return ids


# Prose-only fallback OOD corpus used when AG News download is unavailable.
# All natural English prose: news, history, and science writing.
# No code, SQL, or symbolic notation. Target: ~4,000 tokens.
PROSE_FALLBACK_CORPUS = """
The city council voted unanimously on Tuesday to approve a new transit plan that
would extend the subway network by fourteen miles over the next decade, connecting
three underserved neighbourhoods to the downtown core for the first time. The
project, estimated at four point two billion dollars, will be funded through a
combination of federal grants, municipal bonds, and a small increase in the
regional sales tax. Supporters said the expansion would reduce car traffic on
the main arterial roads by as much as eighteen percent and cut average commute
times for residents in the affected areas by half an hour each day. Critics
argued that the timeline was too ambitious and that cost overruns on similar
projects in other cities warranted more cautious planning. The mayor responded
that delays would only make construction more expensive and that the city had
already waited too long to address its chronic transit deficit.

Relations between the two neighbouring countries reached a new low this week
after a series of diplomatic incidents involving disputed fishing rights in the
strait separating their coastlines. Officials from both governments exchanged
sharp public statements, and the foreign ministry of the northern country
recalled its ambassador for consultations. Fishing vessels from both nations
have been operating in contested waters for decades, but an agreement signed
in the nineteen eighties that had previously managed the tension was allowed to
lapse three years ago when negotiations over a renewal collapsed. Analysts said
the current standoff was unlikely to escalate into open conflict but could
seriously damage trade relations that have grown substantially since the two
countries entered a bilateral free trade agreement in the early two thousands.

The new treatment showed remarkable results in the second phase of clinical
trials, reducing tumour size in seventy three percent of patients with advanced
stages of the disease. Researchers at the university hospital presented the
findings at the annual oncology conference, drawing immediate attention from
specialists who had struggled for years to improve outcomes for this category
of patients. The therapy works by training the immune system to recognise
proteins on the surface of cancer cells that had previously evaded detection.
Unlike earlier immunotherapy approaches, the new method does not require
patients to undergo genetic screening before treatment, which the researchers
said would make it substantially easier to administer in community hospitals
rather than only in major research centres. A third phase trial enrolling
twelve hundred patients across eleven countries was expected to begin within
six months, pending regulatory approval.

Global grain markets responded nervously on Friday to reports that prolonged
dry conditions across major wheat-producing regions of central Asia had damaged
a significant portion of this season's expected harvest. Futures prices rose by
more than four percent in early trading before settling back slightly as analysts
cautioned that final harvest figures would not be available for several weeks.
The United Nations food programme warned that any sustained increase in staple
grain prices would disproportionately affect lower-income countries that depend
heavily on imports and have limited reserves. Officials from the agricultural
ministry of the affected region said that irrigation had offset some of the
losses but acknowledged that output would be meaningfully below the levels
of the previous two years. Several food aid organisations said they were
monitoring the situation closely and would adjust their procurement plans if
prices remained elevated through the autumn.

The ancient city was first settled more than three thousand years ago on a
low promontory overlooking a natural harbour that offered shelter from the
prevailing winds. Its founders, seafarers who had migrated along the coast
from their original homeland to the north, established the settlement as a
trading post and gradually transformed it into a regional centre of commerce.
At its height, the city controlled a network of smaller outposts stretching
along several hundred miles of coastline, extracting raw materials from the
interior and exchanging finished goods with merchants from distant civilisations.
The ruins uncovered by excavations over the past thirty years have revealed
a sophisticated urban layout with paved streets, a central market square, and
a large administrative building whose inscribed stone walls have provided
historians with some of their richest evidence for the legal and commercial
practices of the period. The city declined gradually after a series of poor
harvests and an outbreak of disease weakened its population, and it was
eventually abandoned rather than conquered.

The review panel concluded that the safety protocols in place at the facility
were inadequate and had contributed directly to the severity of the incident.
Investigators found that pressure gauges in the primary containment system had
not been calibrated for more than two years, that three mandatory inspections
had been skipped due to staff shortages, and that the emergency shutdown
procedure had been modified informally without proper documentation or approval.
The facility operator disputed several of the panel's technical findings but
accepted the recommendation that a full audit of maintenance practices be
conducted before operations resumed. Regulatory officials said they would
consider whether additional enforcement action was warranted once the audit
results were available. Independent safety engineers who reviewed the panel's
report said the findings were consistent with a broader pattern of under-investment
in maintenance infrastructure across the sector that had been flagged in previous
inspection cycles without prompting sufficient corrective action.

The film opened to strong reviews and a better than expected performance at the
box office during its opening weekend, earning more than sixty million dollars
domestically and an additional forty million in international markets. Critics
praised the lead performances and the script, which was widely described as the
most tightly structured work the director had produced in more than a decade.
Some reviewers noted that the film's third act felt rushed relative to the
careful pacing of its first two hours, but the consensus was that this was a
minor flaw in an otherwise accomplished work. The studio expressed confidence
that word of mouth would sustain ticket sales through the traditionally slower
weeks following a major holiday weekend. Award season observers began
speculating about which categories the film might compete in, with most
attention focused on the acting and writing categories rather than technical
achievements, though the cinematography was also mentioned by several commentators.

Rising energy costs continued to weigh on household budgets across the region,
with the latest government survey showing that the average family was spending
nearly a fifth of its monthly income on heating, electricity, and transportation
combined. The increase represented a thirty percent rise over the comparable
figure from three years earlier and was concentrated most heavily among
lower-income households, for whom energy costs now consumed a larger share of
total spending than food. Consumer advocates called on the government to
expand its utility assistance programme, which currently reaches only a small
fraction of eligible families due to administrative barriers and limited outreach.
Energy companies pointed to higher wholesale prices driven by global commodity
markets as the primary cause of retail price increases and resisted calls for
a windfall profits tax, arguing that profits were being reinvested in grid
upgrades and renewable generation capacity. Economists said the structural
transition to cleaner energy sources was likely to keep costs elevated for
several more years before efficiency gains and falling technology prices began
to provide relief.
"""


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    tok = GPT2TokenizerFast.from_pretrained("gpt2")

    print("=" * 70)
    print("  EXPERIMENT 1.3 — OUT-OF-DISTRIBUTION ROBUSTNESS (revised protocol)")
    print("  ID:   WikiText-103 validation")
    print("  OOD1: AG News test (news domain, medium shift)")
    print("  OOD2: Prose fallback corpus (news/history prose, used if OOD1 fails)")
    print("=" * 70)

    # ── load datasets once ────────────────────────────────────────────────────
    print("\n  Loading datasets ...", flush=True)

    id_tokens = load_id_data(tok)
    print(f"  ID (WikiText-103 val): {len(id_tokens):,} tokens", flush=True)

    # OOD1: AG News test set — medium-shift (news domain vs Wikipedia prose)
    # Provides ~1M tokens of short English news articles across four categories.
    ood1_tokens = None
    ood1_name   = None
    try:
        ood1_tokens = tokenize_dataset(
            "ag_news", None, "test", "text", tok, max_chars=8_000_000
        )
        ood1_name = "AG News test (news domain)"
        print(f"  OOD1 ({ood1_name}): {len(ood1_tokens):,} tokens", flush=True)
    except Exception as e:
        print(f"  WARNING: AG News load failed ({e}); falling back to prose corpus",
              flush=True)

    # OOD2: prose-only fallback — used when AG News is unavailable.
    # All natural English prose (news, history, science writing); no code or SQL.
    ood2_ids    = tok.encode(PROSE_FALLBACK_CORPUS)
    ood2_tokens = torch.tensor(ood2_ids, dtype=torch.long)
    ood2_name   = "Prose fallback corpus (news/history)"
    print(f"  OOD2 (prose fallback): {len(ood2_tokens):,} tokens", flush=True)

    # If AG News failed use the prose fallback as the primary OOD signal.
    if ood1_tokens is None:
        ood1_tokens, ood1_name = ood2_tokens, ood2_name
        ood2_tokens, ood2_name = None, None

    # ── evaluate each checkpoint ──────────────────────────────────────────────
    results = []
    summary_rows = []

    for seed in SEEDS:
        for cond in ("baseline", "tholonic"):
            ckpt_name = f"row2_{cond}_seed{seed}.pt"
            ckpt_path = CKPT_DIR / ckpt_name
            if not ckpt_path.exists():
                print(f"\n  SKIP {ckpt_name} (checkpoint not found)")
                continue

            print(f"\n  Evaluating {ckpt_name} ...", flush=True)
            model = load_model(ckpt_path)

            id_ppl = compute_perplexity(model, id_tokens)
            print(f"    ID  perplexity: {id_ppl:.2f}", flush=True)

            row = {
                "checkpoint":  ckpt_name,
                "condition":   cond,
                "seed":        seed,
                "id_ppl":      round(id_ppl, 3),
            }

            if ood1_tokens is not None:
                ood1_ppl   = compute_perplexity(model, ood1_tokens)
                ratio1     = ood1_ppl / id_ppl if id_ppl > 0 else float("nan")
                print(f"    OOD1 ({ood1_name}) perplexity: {ood1_ppl:.2f}  ratio: {ratio1:.3f}",
                      flush=True)
                row["ood1_name"]  = ood1_name
                row["ood1_ppl"]   = round(ood1_ppl, 3)
                row["ood1_ratio"] = round(ratio1, 4)

            if ood2_tokens is not None:
                ood2_ppl   = compute_perplexity(model, ood2_tokens)
                ratio2     = ood2_ppl / id_ppl if id_ppl > 0 else float("nan")
                print(f"    OOD2 ({ood2_name}) perplexity: {ood2_ppl:.2f}  ratio: {ratio2:.3f}",
                      flush=True)
                row["ood2_name"]  = ood2_name
                row["ood2_ppl"]   = round(ood2_ppl, 3)
                row["ood2_ratio"] = round(ratio2, 4)

            # mean ratio (kept for reference; confounded when ID ppls differ)
            ratios = [v for k, v in row.items() if k.endswith("_ratio")]
            row["mean_ood_ratio"] = round(sum(ratios) / len(ratios), 4) if ratios else None

            # Primary comparison metric: OOD1 absolute perplexity only.
            # OOD2 is a ~4K-token fallback corpus: too small for a reliable estimate
            # and only intended for use when OOD1 (AG News) is unavailable.
            # OOD2 is recorded for reference but excluded from the pass criterion.
            row["mean_ood_abs_ppl"] = row.get("ood1_ppl")

            results.append(row)
            del model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    # ── paired comparison ─────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  SUMMARY — OOD Robustness (Experiment 1.3)")
    print("  Primary metric: mean absolute OOD perplexity (lower = better)")
    print("  Ratio shown for reference only (confounded by unequal ID perplexity)")
    print(f"  {'Checkpoint':<30} {'ID ppl':>8} {'OOD1 ppl':>10} {'OOD2 ppl':>10} {'mean OOD ppl':>13} {'mean ratio':>11}")
    print(f"  {'-' * 76}")
    for r in results:
        ood1_s  = f"{r['ood1_ppl']:>10.1f}"   if 'ood1_ppl'       in r else f"{'n/a':>10}"
        ood2_s  = f"{r['ood2_ppl']:>10.1f}"   if 'ood2_ppl'       in r else f"{'n/a':>10}"
        mean_s  = f"{r['mean_ood_abs_ppl']:>13.1f}" if r.get('mean_ood_abs_ppl') else f"{'n/a':>13}"
        ratio_s = f"{r['mean_ood_ratio']:>11.3f}"   if r.get('mean_ood_ratio')   else f"{'n/a':>11}"
        print(f"  {r['checkpoint']:<30} {r['id_ppl']:>8.2f} {ood1_s} {ood2_s} {mean_s} {ratio_s}")

    print()
    # Paired comparison per seed — criterion: lower absolute OOD perplexity
    n_pass = 0
    n_seeds_tested = 0
    pair_details = []
    for seed in SEEDS:
        b = next((r for r in results if r["condition"] == "baseline" and r["seed"] == seed), None)
        t = next((r for r in results if r["condition"] == "tholonic"  and r["seed"] == seed), None)
        if b is None or t is None or b.get("mean_ood_abs_ppl") is None or t.get("mean_ood_abs_ppl") is None:
            continue
        n_seeds_tested += 1
        tholonic_better = t["mean_ood_abs_ppl"] < b["mean_ood_abs_ppl"]
        if tholonic_better:
            n_pass += 1
        diff = b["mean_ood_abs_ppl"] - t["mean_ood_abs_ppl"]
        pct  = 100 * diff / b["mean_ood_abs_ppl"]
        pair_details.append({
            "seed": seed,
            "baseline_abs_ppl":   b["mean_ood_abs_ppl"],
            "tholonic_abs_ppl":   t["mean_ood_abs_ppl"],
            "tholonic_advantage_abs": round(diff, 3),
            "tholonic_advantage_pct": round(pct, 2),
            "tholonic_better": tholonic_better,
            "baseline_ratio":  b.get("mean_ood_ratio"),
            "tholonic_ratio":  t.get("mean_ood_ratio"),
        })
        sign = "✓" if tholonic_better else "✗"
        print(f"  Seed {seed}: baseline={b['mean_ood_abs_ppl']:.1f}  "
              f"tholonic={t['mean_ood_abs_ppl']:.1f}  "
              f"advantage={diff:+.1f} ({pct:+.1f}%)  {sign}")

    verdict = "PASS" if n_pass >= 2 else "FAIL"
    print()
    print(f"  Tholonic better for {n_pass}/{n_seeds_tested} seeds  → VERDICT: {verdict}")
    print(f"  (PASS if tholonic has lower mean absolute OOD perplexity for >= 2/3 seeds)")

    output = {
        "experiment":        "1.3 — OOD Robustness (revised protocol)",
        "id_domain":         "WikiText-103 validation",
        "ood_domains":       [n for n in [ood1_name, ood2_name] if n is not None],
        "primary_metric":    "mean_ood_abs_ppl (absolute OOD perplexity, lower = better)",
        "note":              "OOD/ID ratio kept for reference; confounded when ID perplexities differ",
        "results":           results,
        "paired_comparison": pair_details,
        "n_seeds_tested":    n_seeds_tested,
        "n_pass":            n_pass,
        "verdict":           verdict,
    }

    with open(RESULTS_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved → {RESULTS_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
