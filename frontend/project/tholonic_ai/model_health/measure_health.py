#!/usr/bin/env python3
"""
THOLONIC MODEL HEALTH ASSESSMENT

For each of 14 cached models, measures health on 5 axes:
  1. Boundary fidelity  — overall % of detected phase boundaries matching a
                          tholonic constant within ±8%
  2. Role consistency   — among passing boundaries, % where the constant matches
                          its tholonic role (e→expansion, √2→scaling,
                          φ→equilibrium, ln2→compression)
  3. Compression quality— quality of ln2 governance in the final 20% of layers
  4. Equilibrium quality— quality of φ  governance in the mid 45-80% of layers
  5. Virial balance     — how close the mean D/C activation ratio is to 0.5

Outputs: model_health_results.json  (embedded in the HTML page)
"""

import math, re, json, torch, numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

# ── constants ─────────────────────────────────────────────────────────────────
PHI   = (1 + math.sqrt(5)) / 2
LOG2  = math.log(2)
E     = math.e
SQRT2 = math.sqrt(2)
CONSTS = [("φ", PHI), ("ln2", LOG2), ("e", E), ("√2", SQRT2)]
TOL = 0.08

ROLE_ZONES = {          # expected constant → layer fraction (start, end)
    "e":   (0.00, 0.20),
    "√2":  (0.20, 0.55),
    "φ":   (0.45, 0.80),
    "ln2": (0.80, 1.00),
}

TEXTS = [
    "The study of neural networks reveals deep structural patterns.",
    "Artificial intelligence is transforming how we understand cognition.",
    "Language models learn statistical patterns from vast corpora.",
    "The golden ratio appears throughout nature in spirals and seeds.",
    "A transformer processes tokens in parallel using self-attention.",
    "Gradient descent optimizes weights by propagating error signals.",
    "The alignment problem asks how AI systems remain beneficial.",
    "Recursive systems exhibit self-similar structure across levels.",
    "Information bottleneck theory explains deep learning compression.",
    "Scale laws show performance improves predictably with compute.",
]

MODELS = [
    ("openai-community/openai-gpt",         "GPT-1",         "GPT-1",   12),
    ("distilgpt2",                           "distilGPT-2",   "GPT-2",    6),
    ("gpt2",                                 "GPT-2 small",   "GPT-2",   12),
    ("gpt2-medium",                          "GPT-2 medium",  "GPT-2",   24),
    ("gpt2-large",                           "GPT-2 large",   "GPT-2",   36),
    ("gpt2-xl",                              "GPT-2 XL",      "GPT-2",   48),
    ("EleutherAI/gpt-neo-125m",              "GPT-Neo 125m",  "GPT-Neo", 12),
    ("EleutherAI/gpt-neo-1.3B",              "GPT-Neo 1.3B",  "GPT-Neo", 24),
    ("EleutherAI/pythia-160m",               "Pythia 160m",   "Pythia",  12),
    ("EleutherAI/pythia-410m",               "Pythia 410m",   "Pythia",  24),
    ("facebook/opt-125m",                    "OPT 125m",      "OPT",     12),
    ("Qwen/Qwen2.5-0.5B",                    "Qwen2.5-0.5B",  "Qwen",    24),
    ("Qwen/Qwen3-0.6B",                      "Qwen3-0.6B",    "Qwen",    28),
    ("TinyLlama/TinyLlama-1.1B-Chat-v1.0",  "TinyLlama 1.1B","LLaMA",   22),
]

# ── helpers ───────────────────────────────────────────────────────────────────
def eff_rank(mat):
    try:
        sv = torch.linalg.svdvals(mat.float())
        sv = sv[sv > 1e-10]
        p  = sv**2 / (sv**2).sum()
        return math.exp(-(p * torch.log(p + 1e-12)).sum().item())
    except:
        return float('nan')

def attn_entropy(aw):
    w = aw.float().clamp(min=1e-12)
    return (-(w * torch.log(w)).sum(dim=-1)).mean().item()

def nearest_const(x):
    best_name, best_k, best_err = None, None, float('inf')
    for name, base in CONSTS:
        if x <= 0: continue
        try:
            k   = round(math.log(x) / math.log(base))
            err = abs(x - base**k) / base**k
            if err < best_err:
                best_err, best_name, best_k = err, name, k
        except: pass
    return best_name, best_k, best_err

def detect_transitions(series):
    arr = np.array([x for x in series if not math.isnan(x)])
    if len(arr) < 3: return []
    diffs = np.abs(np.diff(arr))
    thr   = np.mean(diffs) + 1.5 * np.std(diffs)
    return [i for i, d in enumerate(diffs) if d > thr]

def layer_idx_from_name(name):
    m = re.search(r'(?:^|\.)(?:h|layers|blocks)\.(\d+)\.', name)
    return int(m.group(1)) if m else None

# ── phase detection (same method as main test) ────────────────────────────────
def run_phase_detection(mdl, tok, n_layers):
    er = [[] for _ in range(n_layers + 1)]
    ae = [[] for _ in range(n_layers)]
    gn = [[] for _ in range(n_layers + 1)]
    ln = [[] for _ in range(n_layers + 1)]
    dn = [[] for _ in range(n_layers)]

    for text in TEXTS:
        inp = tok(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.enable_grad():
            out   = mdl(**inp, labels=inp["input_ids"].clone())
            grads = torch.autograd.grad(out.loss, out.hidden_states,
                                        retain_graph=False, create_graph=False,
                                        allow_unused=True)
        for i, h in enumerate(out.hidden_states):
            hm = h.squeeze(0).detach()
            ln[i].append(hm.norm(dim=-1).mean().item())
            er[i].append(eff_rank(hm))
            gn[i].append(grads[i].squeeze(0).norm(dim=-1).mean().item()
                         if grads[i] is not None else float('nan'))
        for i in range(n_layers):
            dn[i].append((out.hidden_states[i+1] - out.hidden_states[i])
                         .squeeze(0).detach().norm(dim=-1).mean().item())
        if out.attentions:
            for i, aw in enumerate(out.attentions):
                ae[i].append(attn_entropy(aw.detach()))

    avg = lambda lst: [float(np.nanmean(x)) if x else float('nan') for x in lst]
    avg_er = avg(er); avg_ae = avg(ae)
    avg_gn = avg(gn); avg_ln = avg(ln); avg_dn = avg(dn)

    all_t = sorted(set(
        detect_transitions(avg_er) + detect_transitions(avg_ae) +
        detect_transitions(avg_gn) + detect_transitions(avg_dn)
    ))

    boundaries = []
    for t in all_t:
        if t + 1 < len(avg_ln) and avg_ln[t] > 0 and not math.isnan(avg_ln[t+1]):
            ratio = avg_ln[t+1] / avg_ln[t]
            cname, ck, cerr = nearest_const(ratio)
            passes = cerr <= TOL
            frac   = t / n_layers        # relative position 0-1
            boundaries.append({
                "layer": t, "ratio": ratio,
                "constant": cname, "k": ck, "error": cerr,
                "passes": passes, "frac": frac,
            })
    return boundaries

# ── virial balance (D/C per layer) ────────────────────────────────────────────
D_TYPES    = ('LayerNorm', 'RMSNorm')
C_NAMES    = {'c_proj', 'out_proj', 'o_proj', 'down_proj', 'fc2',
              'dense_4h_to_h', 'dense', 'proj'}
C_EXCLUDE  = {'c_attn', 'q_proj', 'k_proj', 'v_proj', 'gate_proj',
              'up_proj', 'fc1', 'dense_h_to_4h', 'query_key_value',
              'qkv_proj', 'wqkv'}

def run_virial(mdl, tok, n_layers):
    d_store = {}; c_store = {}; hooks = []

    for name, mod in mdl.named_modules():
        idx  = layer_idx_from_name(name)
        if idx is None: continue
        last = name.split('.')[-1].lower()
        is_d = any(t in type(mod).__name__ for t in D_TYPES)
        is_c = (isinstance(mod, torch.nn.Linear) and
                last in C_NAMES and last not in C_EXCLUDE)
        if is_d:
            def dh(m, inp, out, i=idx, s=d_store):
                s.setdefault(i, []).append(out.detach().float().pow(2).mean().sqrt().item())
            hooks.append(mod.register_forward_hook(dh))
        if is_c:
            def ch(m, inp, out, i=idx, s=c_store):
                s.setdefault(i, []).append(out.detach().float().pow(2).mean().sqrt().item())
            hooks.append(mod.register_forward_hook(ch))

    if not hooks:
        return None

    with torch.no_grad():
        for text in TEXTS:
            inp = tok(text, return_tensors="pt", truncation=True, max_length=128)
            mdl(**inp)

    for h in hooks: h.remove()

    layers = sorted(set(d_store) & set(c_store))
    if not layers: return None

    per_layer = []
    for i in layers:
        d = float(np.mean(d_store[i]))
        c = float(np.mean(c_store[i]))
        r = d / c if c > 0 else float('nan')
        per_layer.append({"layer": i, "d_rms": d, "c_rms": c,
                          "ratio": r, "frac": i / n_layers})
    return per_layer

# ── scoring ───────────────────────────────────────────────────────────────────
def zone_for_frac(frac):
    """Return the expected tholonic constant for a given fractional depth."""
    for cname, (lo, hi) in ROLE_ZONES.items():
        if lo <= frac < hi:
            return cname
    return "ln2"  # final layer

def score_boundaries(boundaries, n_layers):
    """Compute axis 1 (fidelity), axis 2 (role), axis 3 (compression), axis 4 (equilibrium)."""
    if not boundaries:
        return 50, 50, 50, 50, []

    passing   = [b for b in boundaries if b["passes"]]
    n_pass    = len(passing)
    n_total   = len(boundaries)

    # Axis 1: boundary fidelity
    ax1 = round(n_pass / n_total * 100) if n_total else 50

    # Axis 2: role consistency among passing boundaries
    if passing:
        correct = sum(1 for b in passing
                      if zone_for_frac(b["frac"]) == b["constant"])
        ax2 = round(correct / len(passing) * 100)
    else:
        ax2 = 0

    # Axis 3: compression quality (ln2 in final 20%)
    comp_bounds = [b for b in boundaries if b["frac"] >= 0.80]
    if comp_bounds:
        best = min(comp_bounds, key=lambda b: b["error"])
        if best["constant"] == "ln2":
            ax3 = round(max(0, (1 - best["error"] / TOL) * 100))
        else:
            # wrong constant but something is there
            ax3 = 25
    else:
        ax3 = 40  # no transition detected in compression zone

    # Axis 4: equilibrium quality (φ in 45-80%)
    equil_bounds = [b for b in boundaries if 0.45 <= b["frac"] < 0.80]
    if equil_bounds:
        best = min(equil_bounds, key=lambda b: b["error"])
        if best["constant"] == "φ":
            ax4 = round(max(0, (1 - best["error"] / TOL) * 100))
        else:
            ax4 = 25
    else:
        ax4 = 40

    # annotate each boundary with its zone and role-correctness
    annotated = []
    for b in boundaries:
        expected = zone_for_frac(b["frac"])
        fidelity_score = round(max(0, (1 - b["error"] / TOL) * 100)) if b["passes"] else 0
        annotated.append({**b, "expected_role": expected,
                          "role_correct": (b["constant"] == expected),
                          "fidelity_score": fidelity_score})
    return ax1, ax2, ax3, ax4, annotated

def score_virial(per_layer):
    """Axis 5: virial balance score."""
    if not per_layer:
        return 0, float('nan')
    ratios = [l["ratio"] for l in per_layer if not math.isnan(l["ratio"])]
    if not ratios:
        return 0, float('nan')
    mean_ratio = float(np.mean(ratios))
    # score = 100 × (1 − |mean_ratio − 0.5| / 0.5), capped 0-100
    score = max(0, 100 * (1 - abs(mean_ratio - 0.5) / 0.5))
    return round(score), mean_ratio

# ── main assessment ───────────────────────────────────────────────────────────
def assess(hf_name, display_name, family, n_layers_expected):
    tok = AutoTokenizer.from_pretrained(hf_name, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    mdl = AutoModelForCausalLM.from_pretrained(
        hf_name, output_hidden_states=True, output_attentions=True,
        trust_remote_code=True, dtype=torch.float32,
    )
    mdl.eval()
    n = mdl.config.num_hidden_layers

    # Phase detection
    boundaries = run_phase_detection(mdl, tok, n)
    ax1, ax2, ax3, ax4, annotated = score_boundaries(boundaries, n)

    # Virial balance (run without gradients — separate pass for speed)
    mdl2 = AutoModelForCausalLM.from_pretrained(
        hf_name, trust_remote_code=True, dtype=torch.float32,
    )
    mdl2.eval()
    per_layer = run_virial(mdl2, tok, n)
    ax5, mean_dc = score_virial(per_layer)
    del mdl2

    overall = round((ax1 + ax2 + ax3 + ax4 + ax5) / 5)

    # Identify bottleneck (lowest axis)
    axes     = {"fidelity": ax1, "role_consistency": ax2,
                "compression": ax3, "equilibrium": ax4, "virial": ax5}
    bottleneck = min(axes, key=axes.get)
    bottleneck_labels = {
        "fidelity":        "Boundary fidelity — many detected transitions miss tholonic constants",
        "role_consistency":"Role consistency — constants appearing in wrong phase zones",
        "compression":     "Compression stage — output projection not clearly ln2-governed",
        "equilibrium":     "Equilibrium stage — mid-network lacks stable φ checkpoint",
        "virial":          f"Structural balance — C-dominant (D/C ≈ {mean_dc:.2f} vs target 0.5)",
    }

    return {
        "hf_name":      hf_name,
        "display_name": display_name,
        "family":       family,
        "n_layers":     n,
        "scores": {
            "fidelity":        ax1,
            "role_consistency": ax2,
            "compression":     ax3,
            "equilibrium":     ax4,
            "virial":          ax5,
            "overall":         overall,
        },
        "mean_dc_ratio": round(mean_dc, 3) if not math.isnan(mean_dc) else None,
        "bottleneck":    bottleneck,
        "bottleneck_label": bottleneck_labels[bottleneck],
        "boundaries":   annotated,
        "virial_layers": per_layer if per_layer else [],
    }

# ── run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from pathlib import Path

    print("=" * 68)
    print("  THOLONIC MODEL HEALTH ASSESSMENT")
    print("  5 axes: fidelity · role · compression · equilibrium · virial")
    print("=" * 68)

    results = []
    for hf_name, display_name, family, n_exp in MODELS:
        print(f"\n  Assessing {display_name} ...", flush=True)
        try:
            r = assess(hf_name, display_name, family, n_exp)
            s = r["scores"]
            results.append(r)
            print(f"    fidelity={s['fidelity']:3d}  role={s['role_consistency']:3d}  "
                  f"compress={s['compression']:3d}  equil={s['equilibrium']:3d}  "
                  f"virial={s['virial']:3d}  → overall={s['overall']:3d}  "
                  f"bottleneck={r['bottleneck']}")
        except Exception as ex:
            import traceback
            print(f"    ERROR: {ex}")
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 68)
    print("  RANKING (by overall health score)")
    print(f"  {'Rank':<5} {'Model':<16} {'Overall':>8}  "
          f"{'Fid':>5} {'Role':>5} {'Comp':>5} {'Equil':>5} {'Viral':>5}  Bottleneck")
    print(f"  {'-'*72}")
    ranked = sorted(results, key=lambda r: -r["scores"]["overall"])
    for i, r in enumerate(ranked):
        s = r["scores"]
        print(f"  {i+1:<5} {r['display_name']:<16} {s['overall']:>8}  "
              f"{s['fidelity']:>5} {s['role_consistency']:>5} "
              f"{s['compression']:>5} {s['equilibrium']:>5} {s['virial']:>5}  "
              f"{r['bottleneck']}")

    out = Path(__file__).parent / "model_health_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved → {out}")
    print("=" * 68)
