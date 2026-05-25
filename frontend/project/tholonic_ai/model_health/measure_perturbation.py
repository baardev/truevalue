#!/usr/bin/env python3
"""
THOLONIC CONTEXT-LENGTH PERTURBATION TEST

For each model, runs the same prompts at three context lengths (128, 64, 32
tokens) and measures per-layer hidden-state sensitivity:

    sensitivity_l = mean_over_texts( ||h_l(full) - h_l(short)|| / ||h_l(full)|| )

The falsifiable tholonic prediction: layers in the φ-equilibrium zone (45–80%
of network depth) should show *lower* sensitivity than early or late layers,
because the φ checkpoint represents a self-stabilising structural attractor.
This would produce a U-shaped or dip-shaped sensitivity profile across layers.

A flat profile would indicate D is uniformly sparse, reinforcing the virial=0
finding.  Either outcome is informative.

Output: perturbation_results.json
"""

import math, json, torch, numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path

# ── models ────────────────────────────────────────────────────────────────────
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

CONTEXT_LENGTHS = [128, 64, 32]   # tokens: full, half, quarter
PHI_ZONE = (0.45, 0.80)           # expected φ-equilibrium fraction

# ── core measurement ──────────────────────────────────────────────────────────
@torch.no_grad()
def hidden_states_last_token(mdl, input_ids):
    """Return hidden states at the LAST token position for each layer.
    Shape: (n_layers+1, hidden_size)
    """
    out = mdl(input_ids, output_hidden_states=True)
    return torch.stack([h[0, -1, :] for h in out.hidden_states])   # (L+1, H)


def make_long_passages(tok, n_passages=10):
    """
    Concatenate TEXTS into long passages of ~128 tokens each.
    Returns a list of token-id tensors, each at least 32 tokens long.
    """
    # Concatenate all texts into one big string, then slide a window
    big = " ".join(TEXTS * 3)  # repeat to ensure enough tokens
    ids = tok(big, return_tensors="pt", add_special_tokens=True)["input_ids"][0]

    passages = []
    step = max(1, (len(ids) - CONTEXT_LENGTHS[0]) // n_passages)
    for i in range(n_passages):
        start = i * step
        chunk = ids[start : start + CONTEXT_LENGTHS[0]]
        if len(chunk) >= CONTEXT_LENGTHS[2]:  # need at least 32 tokens
            passages.append(chunk.unsqueeze(0))  # (1, seq_len)
    return passages


def measure_sensitivity(mdl, tok, n_layers):
    """
    For each passage, run at full length (128), half (64), and quarter (32) by
    truncating to the first N tokens. Compare the last-token hidden state at
    each shorter length against the full-context baseline.

        sensitivity_l = ||h_l(full) - h_l(short)|| / ||h_l(full)||

    Returns:
        sens_64[l]  — mean normalised shift (128 → 64) at layer l
        sens_32[l]  — mean normalised shift (128 → 32) at layer l
    """
    all_64 = [[] for _ in range(n_layers + 1)]
    all_32 = [[] for _ in range(n_layers + 1)]

    passages = make_long_passages(tok)
    if not passages:
        avg = lambda lst: [float('nan')] * (n_layers + 1)
        return avg(None), avg(None)

    for ids_full in passages:
        h_full = hidden_states_last_token(mdl, ids_full)   # (L+1, H)

        for ctx, store in [(CONTEXT_LENGTHS[1], all_64),
                           (CONTEXT_LENGTHS[2], all_32)]:
            if ids_full.shape[1] < ctx:
                continue
            ids_short = ids_full[:, :ctx]   # first `ctx` tokens
            h_short   = hidden_states_last_token(mdl, ids_short)

            for l in range(n_layers + 1):
                base_norm = h_full[l].norm().item()
                if base_norm < 1e-8:
                    continue
                shift = (h_full[l] - h_short[l]).norm().item()
                store[l].append(shift / base_norm)

    avg = lambda lst: [float(np.mean(x)) if x else float('nan') for x in lst]
    return avg(all_64), avg(all_32)


# ── analysis helpers ──────────────────────────────────────────────────────────
def classify_profile(sens, n_layers):
    """
    Classify the sensitivity profile shape.
    Returns: 'dip' | 'flat' | 'rising' | 'falling' | 'noisy'
    """
    arr = np.array([x for x in sens if not math.isnan(x)])
    if len(arr) < 4:
        return "insufficient"
    # split into thirds
    t = len(arr) // 3
    early = arr[:t].mean()
    mid   = arr[t:2*t].mean()
    late  = arr[2*t:].mean()
    spread = arr.std()
    if spread < 0.01:
        return "flat"
    if mid < early * 0.85 and mid < late * 0.85:
        return "dip"         # U-shaped — consistent with tholonic prediction
    if mid > early * 1.15 and mid > late * 1.15:
        return "peak"        # inverse U
    if arr[-1] > arr[0] * 1.2:
        return "rising"
    if arr[-1] < arr[0] * 0.8:
        return "falling"
    return "noisy"


def phi_zone_dip(sens, n_layers):
    """
    Check whether the minimum sensitivity falls within the φ-equilibrium zone.
    Returns (min_frac, in_phi_zone, mean_phi_sens, mean_outside_sens)
    """
    valid = [(i, v) for i, v in enumerate(sens) if not math.isnan(v)]
    if not valid:
        return float('nan'), False, float('nan'), float('nan')
    min_idx = min(valid, key=lambda x: x[1])[0]
    min_frac = min_idx / n_layers

    phi_vals     = [v for i, v in valid if PHI_ZONE[0] <= i/n_layers <= PHI_ZONE[1]]
    outside_vals = [v for i, v in valid if not (PHI_ZONE[0] <= i/n_layers <= PHI_ZONE[1])]

    mean_phi     = float(np.mean(phi_vals))     if phi_vals     else float('nan')
    mean_outside = float(np.mean(outside_vals)) if outside_vals else float('nan')
    in_zone = PHI_ZONE[0] <= min_frac <= PHI_ZONE[1]

    return round(min_frac, 3), in_zone, round(mean_phi, 4), round(mean_outside, 4)


# ── main ──────────────────────────────────────────────────────────────────────
def assess(hf_name, display_name, family, n_exp):
    tok = AutoTokenizer.from_pretrained(hf_name, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    mdl = AutoModelForCausalLM.from_pretrained(
        hf_name, output_hidden_states=True,
        trust_remote_code=True, dtype=torch.float32,
    )
    mdl.eval()
    n = mdl.config.num_hidden_layers

    sens_64, sens_32 = measure_sensitivity(mdl, tok, n)

    shape_64 = classify_profile(sens_64, n)
    shape_32 = classify_profile(sens_32, n)

    min_frac_64, in_phi_64, phi_64, out_64 = phi_zone_dip(sens_64, n)
    min_frac_32, in_phi_32, phi_32, out_32 = phi_zone_dip(sens_32, n)

    # phi_advantage: negative means phi zone IS lower sensitivity (predicted)
    phi_adv_64 = round(phi_64 - out_64, 4) if not math.isnan(phi_64) and not math.isnan(out_64) else float('nan')
    phi_adv_32 = round(phi_32 - out_32, 4) if not math.isnan(phi_32) and not math.isnan(out_32) else float('nan')

    # Tholonic prediction passed if phi zone shows lower sensitivity than outside
    prediction_64 = "PASS" if not math.isnan(phi_adv_64) and phi_adv_64 < 0 else "FAIL"
    prediction_32 = "PASS" if not math.isnan(phi_adv_32) and phi_adv_32 < 0 else "FAIL"

    return {
        "hf_name":      hf_name,
        "display_name": display_name,
        "family":       family,
        "n_layers":     n,
        # per-layer sensitivity arrays (normalised shift)
        "sensitivity_64": [round(v, 5) if not math.isnan(v) else None for v in sens_64],
        "sensitivity_32": [round(v, 5) if not math.isnan(v) else None for v in sens_32],
        # profile shape
        "shape_64": shape_64,
        "shape_32": shape_32,
        # phi-zone analysis
        "min_frac_64":   min_frac_64,
        "min_frac_32":   min_frac_32,
        "in_phi_zone_64": in_phi_64,
        "in_phi_zone_32": in_phi_32,
        "phi_advantage_64": phi_adv_64,   # negative = phi zone is quieter (predicted)
        "phi_advantage_32": phi_adv_32,
        "prediction_64": prediction_64,
        "prediction_32": prediction_32,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("  THOLONIC CONTEXT-LENGTH PERTURBATION TEST")
    print("  Prediction: φ-equilibrium zone (45–80%) shows lower sensitivity")
    print("=" * 70)

    results = []
    pass_64 = pass_32 = 0

    for hf_name, display_name, family, n_exp in MODELS:
        print(f"\n  Testing {display_name} ...", flush=True)
        try:
            r = assess(hf_name, display_name, family, n_exp)
            results.append(r)
            if r["prediction_64"] == "PASS": pass_64 += 1
            if r["prediction_32"] == "PASS": pass_32 += 1
            print(f"    shape(64)={r['shape_64']:8s}  φ-adv(64)={r['phi_advantage_64']:+.4f}  "
                  f"→ {r['prediction_64']}   |   "
                  f"shape(32)={r['shape_32']:8s}  φ-adv(32)={r['phi_advantage_32']:+.4f}  "
                  f"→ {r['prediction_32']}")
        except Exception as ex:
            import traceback
            print(f"    ERROR: {ex}")
            traceback.print_exc()

    n = len(results)
    print("\n" + "=" * 70)
    print(f"  SUMMARY")
    print(f"  {'Model':<16} {'Shape(64)':>10} {'φ-adv(64)':>10} {'Pass?':>6}  "
          f"{'Shape(32)':>10} {'φ-adv(32)':>10} {'Pass?':>6}")
    print(f"  {'-'*68}")
    for r in results:
        print(f"  {r['display_name']:<16} {r['shape_64']:>10} "
              f"{r['phi_advantage_64']:>+10.4f} {r['prediction_64']:>6}  "
              f"{r['shape_32']:>10} {r['phi_advantage_32']:>+10.4f} {r['prediction_32']:>6}")
    print(f"\n  Pass rate (128→64): {pass_64}/{n} = {pass_64/n*100:.0f}%")
    print(f"  Pass rate (128→32): {pass_32}/{n} = {pass_32/n*100:.0f}%")
    print(f"\n  Tholonic prediction: φ-zone sensitivity < surrounding layers")
    print(f"  (negative φ-advantage = prediction supported)")

    out = Path(__file__).parent / "perturbation_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved → {out}")
    print("=" * 70)
