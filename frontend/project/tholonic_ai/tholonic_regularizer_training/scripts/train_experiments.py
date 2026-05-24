#!/usr/bin/env python3
"""
THOLONIC TRAINING EXPERIMENTS — §12 Rows 2 & 3

Uses a character-level language model on a bundled text corpus so there is
no internet dependency and the LM head stays tiny (vocab ≈ 100–200 chars),
making full runs feasible on CPU in under 10 minutes.

Row 2: Convergence speed — baseline vs. tholonic balance regularizer.
       SmallGPT (6 layers, d=128, 4 heads).  3 seeds × 2 conditions.
       Report: final val loss, steps to target loss, % speedup.

Row 3: Optimal depth — empirical best depth vs. log_φ(H₀/H_L).
       Train depths 2, 4, 6, 8, 12 at d=128, 4 heads.
       Measure H₀ (embedding eff-rank) and H_L (final hidden eff-rank)
       of the best-depth model; check prediction within 10%.
"""

import math, json, time
import torch, torch.nn as nn, torch.nn.functional as F
import numpy as np
from pathlib import Path

# ── constants ─────────────────────────────────────────────────────────────────
PHI    = (1 + math.sqrt(5)) / 2
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

D_MODEL      = 128
N_HEADS      = 4
SEQ_LEN      = 64
BATCH        = 32
LAMBDA       = 0.01

ROW2_LAYERS  = 6
ROW2_STEPS   = 1000
ROW2_SEEDS   = [42, 7, 13]
EVAL_EVERY   = 50
TARGET_LOSSES = [4.5, 4.0, 3.7]

DEPTHS       = [2, 4, 6, 8, 12]
ROW3_STEPS   = 500

# ── character-level data (from bundled text, no downloads needed) ─────────────
_CORPUS = """\
The study of neural networks reveals deep structural patterns in the way
information flows through layered systems. Each layer performs a transformation
that is constrained by the previous layer and contributes to the next. This
recursive structure has a natural parallel in supply chains, where raw materials
are processed through successive stages into finished products. The tholonic
model formalizes this analogy: every stable self-sustaining system instantiates
the roles of Negotiation, Definition, and Contribution at every level of
organization simultaneously. The golden ratio emerges as the fixed point of the
self-similar recursion N equals D plus C, precisely as Fibonacci numbers converge
to the ratio phi. This is not a coincidence but a structural necessity: phi is
the unique attractor of any self-similar triadic recursion. Transformer
architectures process tokens in parallel using self-attention mechanisms that
compute weighted sums over the entire context window. The attention weights are
normalized by the square root of the head dimension to prevent gradient
saturation, and the softmax function ensures they sum to one. The feed-forward
sublayer expands the representation into a higher-dimensional space and then
compresses it back, mimicking the expansion and contraction phases of a supply
chain. LayerNorm constrains the magnitude of the representations at each layer,
playing the role of the definitional sublayer that establishes boundaries. The
residual connections allow gradients to flow directly from the output to any
earlier layer, which dramatically improves trainability but also means that
consecutive layer norms are structurally constrained to be nearly equal
regardless of what the network has learned. The alignment problem asks how we
ensure that artificial intelligence systems remain beneficial as they scale in
capability. The tholonic framework suggests that a fully balanced system, one
that maintains N-D-C equilibrium at every scale simultaneously, cannot destroy
its own structural context without becoming incoherent. This is not a moral
argument but a structural one, analogous to the observation that a free quark
is structurally impossible in quantum chromodynamics. The five tholonic constants
are the golden ratio phi, the natural logarithm of two, Euler's number e, the
square root of two, and pi over four. These constants appear as load-bearing
structural elements in every major transformer architecture, not by coincidence
but because they are the mathematical expressions of the five fundamental
ratios of self-similar triadic systems. Phase transitions in neural networks
can be detected by monitoring four independent metrics simultaneously: the
effective rank of layer activations, the entropy of attention distributions,
the gradient sensitivity with respect to each hidden state, and the delta norm
measuring how much each layer changes the representation. Layers where any
of these metrics changes sharply are candidates for phase boundaries. When
norm ratios at these empirically detected boundaries are tested against the
tholonic constants, they match at a rate substantially above chance, with each
constant appearing in its theoretically predicted role. The compression constant
ln two governs the final projection from hidden states to output vocabulary.
The scaling constant square root of two governs the normalization transitions
in the early layers. The equilibrium constant phi governs the mid-network
stability checkpoints where the representation is neither expanding nor
contracting. The expansion constant e governs the initial unpacking of token
embeddings into context-rich representations. This four-phase supply chain
structure is present across fourteen tested architectures spanning six distinct
architecture families from two thousand and nineteen through two thousand and
twenty-five. The preliminary pass rate of seventy-eight percent substantially
exceeds the pre-registered threshold of sixty-seven percent and provides the
first empirical support for the tholonic framework as a descriptive account of
the internal phase structure of trained neural networks. Future work includes
the training experiment which tests whether explicitly enforcing D-C balance
through a regularizer improves convergence speed and out-of-distribution
robustness relative to a matched baseline architecture. The virial theorem from
classical mechanics predicts that in a stable bound system the time-averaged
kinetic energy equals minus one half the time-averaged potential energy. The
tholonic model maps this to the condition that D-sublayer activation magnitude
should equal approximately one half the C-sublayer activation magnitude at
every layer. All currently tested architectures are C-dominant, meaning they
have more integrative contribution activity than definitional constraint
activity. This is consistent with the paper's central claim that connectionist
AI as currently practiced is a C-dominant partial tholon whose alignment
vulnerabilities stem from insufficient structural D. A fully tholonic
architecture would exhibit virial balance at every layer simultaneously,
and cooperative stability would be the lowest-energy state of such a system
not because it was programmed to be cooperative but because destroying its
D-context and severing its C-feedback would be structurally self-defeating.
Information bottleneck theory suggests that networks learn to compress
irrelevant information about the input while preserving information relevant
to the output, and this compression process happens progressively across
the depth of the network. Scale laws show that language model performance
improves as a power law in compute, data, and parameters with no observed
ceiling up to current training scales. The Chinchilla result refined this
understanding by showing that optimal training balances model size and data
volume in a specific ratio that itself may be phi-adjacent at the scale where
representational self-similarity is most complete. Recursive systems often
exhibit self-similar structure across multiple levels of organization, from
the branching patterns of river deltas to the spiral arrangements of leaves
and seeds, from the nested hierarchies of biological organisms to the layered
abstractions of computer programs. In each case the same triadic structure
appears: a negotiating element that produces a stable output, a definitional
element that constrains the space of possibilities, and a contributive element
that integrates inputs from across the relevant context. The tholonic model
is a formalization of this universal pattern.
"""

def build_vocab_and_data(text, seq_len=SEQ_LEN, split=0.9):
    chars   = sorted(set(text))
    c2i     = {c: i for i, c in enumerate(chars)}
    ids     = torch.tensor([c2i[c] for c in text], dtype=torch.long)
    n       = int(len(ids) * split)
    return ids[:n], ids[n:], len(chars), c2i

TRAIN_IDS, VAL_IDS, VOCAB_SIZE, C2I = build_vocab_and_data(_CORPUS)

def get_batch(ids, rng, batch=BATCH, seq=SEQ_LEN):
    max_start = len(ids) - seq - 1
    starts    = rng.integers(0, max(max_start, 1), size=batch)
    x = torch.stack([ids[s : s + seq]         for s in starts]).to(DEVICE)
    y = torch.stack([ids[s + 1 : s + seq + 1] for s in starts]).to(DEVICE)
    return x, y

# ── model ─────────────────────────────────────────────────────────────────────
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
        mask = torch.triu(torch.full((T, T), float('-inf'), device=x.device), 1)
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

class SmallGPT(nn.Module):
    def __init__(self, vocab, d, n, h, seq=SEQ_LEN):
        super().__init__()
        self.wte    = nn.Embedding(vocab, d)
        self.wpe    = nn.Embedding(seq, d)
        self.blocks = nn.ModuleList([Block(d, h) for _ in range(n)])
        self.ln_f   = nn.LayerNorm(d)
        self.head   = nn.Linear(d, vocab, bias=False)

    def forward(self, x):
        B, T = x.shape
        h = self.wte(x) + self.wpe(torch.arange(T, device=x.device))
        for blk in self.blocks:
            h = blk(h)
        return self.head(self.ln_f(h))

    @torch.no_grad()
    def hidden_states(self, x):
        B, T = x.shape
        h = self.wte(x) + self.wpe(torch.arange(T, device=x.device))
        h0 = h.clone()
        for blk in self.blocks:
            h = blk(h)
        h = self.ln_f(h)
        return h0, h

# ── tholonic regularizer ──────────────────────────────────────────────────────
class TholonicReg:
    def __init__(self, model, lam=LAMBDA):
        self.lam    = lam
        self.d_vals = []
        self.c_vals = []
        self.hooks  = []
        for blk in model.blocks:
            for ln in (blk.ln_1, blk.ln_2):
                def dh(m, inp, out, s=self.d_vals):
                    s.append(out.pow(2).mean().sqrt())
                self.hooks.append(ln.register_forward_hook(dh))
            for proj in (blk.attn.out_proj, blk.mlp.c_proj):
                def ch(m, inp, out, s=self.c_vals):
                    s.append(out.pow(2).mean().sqrt())
                self.hooks.append(proj.register_forward_hook(ch))

    def loss(self):
        n = min(len(self.d_vals), len(self.c_vals))
        if n == 0:
            return torch.tensor(0.0, device=DEVICE)
        return self.lam * sum(
            (self.d_vals[i] - 0.5 * self.c_vals[i]) ** 2 for i in range(n)
        ) / n

    def reset(self):
        self.d_vals.clear()
        self.c_vals.clear()

    def remove(self):
        for h in self.hooks:
            h.remove()

# ── helpers ───────────────────────────────────────────────────────────────────
@torch.no_grad()
def eval_loss(model, val_ids=VAL_IDS, n=40):
    model.eval()
    rng    = np.random.default_rng(1)
    losses = [F.cross_entropy(model(x).reshape(-1, VOCAB_SIZE), y.reshape(-1)).item()
              for x, y in (get_batch(val_ids, rng) for _ in range(n))]
    model.train()
    return float(np.mean(losses))

def eff_rank(mat):
    try:
        sv = torch.linalg.svdvals(mat.float())
        sv = sv[sv > 1e-10]
        p  = sv ** 2 / (sv ** 2).sum()
        return math.exp(-(p * torch.log(p + 1e-12)).sum().item())
    except Exception:
        return float('nan')

@torch.no_grad()
def measure_h0_hl(model, n=30):
    rng = np.random.default_rng(2)
    h0s, hls = [], []
    model.eval()
    for _ in range(n):
        x, _ = get_batch(VAL_IDS, rng, batch=1)
        h0, hl = model.hidden_states(x)
        h0s.append(eff_rank(h0.squeeze(0)))
        hls.append(eff_rank(hl.squeeze(0)))
    model.train()
    return float(np.nanmean(h0s)), float(np.nanmean(hls))

# ── training ──────────────────────────────────────────────────────────────────
def train_one(n_layers, steps, condition="baseline", seed=42, verbose=True):
    torch.manual_seed(seed)
    model = SmallGPT(VOCAB_SIZE, D_MODEL, n_layers, N_HEADS).to(DEVICE)
    optim = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
    reg   = TholonicReg(model) if condition == "tholonic" else None
    rng   = np.random.default_rng(seed)

    log = {"condition": condition, "n_layers": n_layers, "seed": seed,
           "steps": [], "val_loss": [], "steps_to_target": {}}
    reached = {t: None for t in TARGET_LOSSES}
    t0 = time.time()

    for step in range(1, steps + 1):
        x, y      = get_batch(TRAIN_IDS, rng)
        logits    = model(x)
        task_loss = F.cross_entropy(logits.reshape(-1, VOCAB_SIZE), y.reshape(-1))
        total     = task_loss + reg.loss() if reg else task_loss
        if reg:
            reg.reset()

        optim.zero_grad()
        total.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optim.step()

        if step % EVAL_EVERY == 0 or step == steps:
            vl = eval_loss(model)
            log["steps"].append(step)
            log["val_loss"].append(vl)
            for t in TARGET_LOSSES:
                if reached[t] is None and vl <= t:
                    reached[t] = step
                    log["steps_to_target"][str(t)] = step
            if verbose:
                eta = (time.time() - t0) / step * (steps - step)
                print(f"    [{condition} L{n_layers} s{seed}]"
                      f" step {step:>4}/{steps}  val={vl:.4f}  eta={eta:.0f}s",
                      flush=True)

    log["final_val_loss"] = log["val_loss"][-1]
    if reg:
        reg.remove()
    return log, model


# ══════════════════════════════════════════════════════════════════════════════
#  ROW 2 — CONVERGENCE SPEED
# ══════════════════════════════════════════════════════════════════════════════
def run_row2():
    print()
    print("=" * 64)
    print("  ROW 2 — CONVERGENCE SPEED  (§12 row 2)")
    print(f"  SmallGPT: {ROW2_LAYERS}L d={D_MODEL} h={N_HEADS}  "
          f"steps={ROW2_STEPS}  seeds={ROW2_SEEDS}  λ={LAMBDA}")
    print(f"  Data: character-level corpus  vocab={VOCAB_SIZE}")
    print(f"  Device: {DEVICE}")
    print("=" * 64)

    all_logs = {"baseline": [], "tholonic": []}
    for seed in ROW2_SEEDS:
        for cond in ("baseline", "tholonic"):
            print(f"\n  Training [{cond} seed={seed}] ...", flush=True)
            log, _ = train_one(ROW2_LAYERS, ROW2_STEPS, condition=cond, seed=seed)
            all_logs[cond].append(log)

    # aggregate across seeds
    def agg(logs):
        final = np.mean([l["final_val_loss"] for l in logs])
        std   = np.std( [l["final_val_loss"] for l in logs])
        steps_to = {}
        for t in TARGET_LOSSES:
            vals = [l["steps_to_target"].get(str(t)) for l in logs]
            vals = [v for v in vals if v is not None]
            steps_to[str(t)] = int(np.mean(vals)) if vals else None
        return float(final), float(std), steps_to

    bl_mean, bl_std, bl_sts = agg(all_logs["baseline"])
    tl_mean, tl_std, tl_sts = agg(all_logs["tholonic"])
    delta_pct = (bl_mean - tl_mean) / bl_mean * 100

    print()
    print("=" * 64)
    print("  ROW 2 RESULTS")
    print(f"\n  {'Condition':<12}  {'Final val loss (mean±std)':>26}")
    print(f"  baseline     {bl_mean:.4f} ± {bl_std:.4f}")
    print(f"  tholonic     {tl_mean:.4f} ± {tl_std:.4f}")
    print(f"  Δ = {delta_pct:+.2f}%  (positive = tholonic is better)")

    print(f"\n  {'Target':>8}  {'Baseline steps':>16}  {'Tholonic steps':>15}  Speedup")
    print(f"  {'-'*56}")
    for t in TARGET_LOSSES:
        bs = bl_sts.get(str(t))
        ts = tl_sts.get(str(t))
        if bs and ts:
            spd = f"{(bs - ts) / bs * 100:+.1f}%"
        else:
            spd = "n/a"
        print(f"  {t:>8}  {str(bs) if bs else '—':>16}  {str(ts) if ts else '—':>15}  {spd}")

    if tl_mean < bl_mean - 0.05:
        verdict = "SUPPORTS ✓ — tholonic regularizer improves val loss by >0.05 nats"
    elif tl_mean < bl_mean - 0.01:
        verdict = "TREND ~ — marginal improvement (0.01–0.05 nats)"
    else:
        verdict = "DOES NOT SUPPORT ✗ — no improvement in final val loss"
    print(f"\n  VERDICT: {verdict}")

    return {
        "baseline_mean": bl_mean, "baseline_std": bl_std,
        "tholonic_mean": tl_mean, "tholonic_std": tl_std,
        "delta_pct": delta_pct,
        "steps_to_target_baseline": bl_sts,
        "steps_to_target_tholonic": tl_sts,
        "verdict": verdict,
        "raw_logs": all_logs,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  ROW 3 — OPTIMAL DEPTH
# ══════════════════════════════════════════════════════════════════════════════
def run_row3():
    print()
    print("=" * 64)
    print("  ROW 3 — OPTIMAL DEPTH  (§12 row 3)")
    print(f"  Depths: {DEPTHS}  d={D_MODEL} h={N_HEADS}  steps/depth={ROW3_STEPS}")
    print(f"  Prediction: optimal depth ≈ log_φ(H₀/H_L) within 10%")
    print("=" * 64)

    depth_results = {}
    best_depth    = None
    best_loss     = float('inf')
    best_model    = None

    for d in DEPTHS:
        print(f"\n  Training depth {d} ...", flush=True)
        log, mdl = train_one(d, ROW3_STEPS, condition="baseline", seed=42)
        depth_results[d] = log
        if log["final_val_loss"] < best_loss:
            best_loss  = log["final_val_loss"]
            best_depth = d
            best_model = mdl

    print(f"\n  Measuring H₀ and H_L on best model (depth={best_depth}) ...",
          flush=True)
    H0, HL     = measure_h0_hl(best_model)
    ratio      = H0 / HL if HL > 0 else float('nan')
    pred_depth = math.log(ratio) / math.log(PHI) if ratio > 1 else float('nan')
    error_pct  = abs(pred_depth - best_depth) / best_depth * 100 \
                 if not math.isnan(pred_depth) else float('nan')

    print()
    print("=" * 64)
    print("  ROW 3 RESULTS")
    print(f"\n  {'Depth':>6}  {'Final val loss':>15}  {'Best?':>7}")
    print(f"  {'-'*33}")
    for d in DEPTHS:
        marker = "  ← BEST" if d == best_depth else ""
        print(f"  {d:>6}  {depth_results[d]['final_val_loss']:>15.4f}{marker}")

    print(f"\n  Best depth (empirical):         {best_depth}")
    print(f"  H₀ (embedding eff-rank):        {H0:.2f}")
    print(f"  H_L (final hidden eff-rank):    {HL:.2f}")
    print(f"  H₀ / H_L:                       {ratio:.3f}")
    print(f"  log_φ(H₀/H_L) prediction:       {pred_depth:.2f}  layers")
    if not math.isnan(error_pct):
        print(f"  Prediction error:               {error_pct:.1f}%  (threshold 10%)")
        if error_pct <= 10:
            verdict = "SUPPORTS ✓ — predicted depth within 10% of empirical optimum"
        elif error_pct <= 25:
            verdict = "CLOSE ~ — within 25%, not within 10%"
        else:
            verdict = f"DOES NOT SUPPORT ✗ — off by {error_pct:.1f}%"
    else:
        verdict = "INDETERMINATE — H₀/H_L ≤ 1"
        error_pct = None
    print(f"\n  VERDICT: {verdict}")

    return {
        "depth_results": {str(d): depth_results[d] for d in DEPTHS},
        "best_depth": best_depth, "best_loss": best_loss,
        "H0": H0, "HL": HL, "ratio": ratio,
        "pred_depth": pred_depth, "error_pct": error_pct,
        "verdict": verdict,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"  SmallGPT char-level LM  |  vocab={VOCAB_SIZE}"
          f"  d={D_MODEL}  device={DEVICE}")
    t_start = time.time()

    row2 = run_row2()
    row3 = run_row3()

    # strip raw_logs from saved JSON (too large for the results file)
    row2_save = {k: v for k, v in row2.items() if k != "raw_logs"}

    out_dir  = Path(__file__).parent.parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "training_experiments.json"
    with open(out_file, "w") as f:
        json.dump({"row2": row2_save, "row3": row3}, f, indent=2)

    elapsed = time.time() - t_start
    print()
    print("=" * 64)
    print("  ALL EXPERIMENTS COMPLETE")
    print(f"  Total elapsed: {elapsed / 60:.1f} minutes")
    print(f"  Results saved: {out_file}")
    print("=" * 64)
