#!/usr/bin/env python3
"""
Alternative tholonic prediction tests.

Derived from Sections 6.1, 8.2, 11.2, 11.3 of:
  Milton, J.W. (2026). Neural Networks as Tholonic Systems. Clarity Coalition.

The Section 12 row-1 test (||h_l|| / ||h_{l-1}|| → φ^{-1}) was falsified across
GPT-2 (all sizes) and Qwen3-0.6B. These tests probe five other structural
predictions of the tholonic framework.

Tests
-----
  A  Activation entropy monotonicity
       Spectral entropy of hidden-state covariance decreases monotonically with
       depth. (§6.1: "H_ℓ decreases monotonically with depth")

  B  Effective-rank φ ratio
       The ratio eff_rank[ℓ] / eff_rank[ℓ-1] should cluster near φ^{-1} ≈ 0.618.
       (§8.2: φ is the unique fixed-point / inter-level scaling attractor)

  C  Virial D/C sublayer ratio  [GPT-2 only — requires architecture hooks]
       RMS activation of the D-sublayer (LayerNorm) should be ≈ half the
       RMS activation of the C-sublayer (Attention + MLP output projections).
       Predicted ratio RMS_D / RMS_C → 0.5  (§11.2, virial-theorem analogy)

  D  Attention entropy monotonicity
       Per-layer mean Shannon entropy of attention weights (normalised by
       log(seq_len)) should decrease with depth.  (§6.1)

  E  Depth formula
       Predicted depth  L* = log_φ(H_0 / H_L)  should match actual depth
       within 10 %.  (§11.3)

Usage
-----
  python measure_alternative_tests.py
  python measure_alternative_tests.py --model gpt2-large
  python measure_alternative_tests.py --model qwen3-0.6b
"""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI   # ≈ 0.618

SAMPLE_TEXTS = [
    "The study of neural networks reveals deep structural patterns in how information flows.",
    "Artificial intelligence is transforming how we understand cognition and learning.",
    "Language models learn statistical patterns from vast corpora of human-written text.",
    "The golden ratio appears throughout nature in the spiral arrangements of leaves and seeds.",
    "A transformer architecture processes tokens in parallel using self-attention mechanisms.",
    "Gradient descent optimizes network weights by propagating error signals backward.",
    "The alignment problem asks how we ensure AI systems remain beneficial as they scale.",
    "Recursive systems often exhibit self-similar structure across multiple levels of organization.",
    "Information bottleneck theory suggests networks compress irrelevant information during training.",
    "Scale laws show that language model performance improves predictably with compute and data.",
    "Neural networks with many layers learn hierarchical representations of increasing abstraction.",
    "The residual connection prevents the output of a transformer block from drifting arbitrarily.",
    "Entropy decreases monotonically with depth in well-trained deep neural networks.",
    "The fixed point of a self-similar recursion is determined by the recursion's structural form.",
    "Transfer learning works because early layers capture domain-general features.",
    "Constitutional AI uses written principles to guide model self-critique during training.",
    "The softmax function uses the exponential, a fundamental mathematical constant.",
    "Attention is computed as the softmax of scaled dot products between query and key matrices.",
    "Biological systems from nautilus shells to phyllotaxis exhibit phi-based scaling.",
    "The bitter lesson: methods that scale with compute consistently outperform encoded knowledge.",
    "Deep learning replaced decades of hand-crafted computer vision features in a single year.",
    "Self-attention allows each token to attend to all other tokens in the sequence simultaneously.",
    "The virial theorem relates kinetic and potential energy in a bound physical system.",
    "Representation learning extracts useful features automatically from raw data.",
    "The structural balance between integration and constraint determines system stability.",
]

MODEL_ALIASES = {
    "gpt2":         "gpt2",
    "gpt2-medium":  "gpt2-medium",
    "gpt2-large":   "gpt2-large",
    "gpt2-xl":      "gpt2-xl",
    "qwen2.5-0.5b": "Qwen/Qwen2.5-0.5B",
    "qwen2.5-1.5b": "Qwen/Qwen2.5-1.5B",
    "qwen3-0.6b":   "Qwen/Qwen3-0.6B",
    "qwen3-1.7b":   "Qwen/Qwen3-1.7B",
}


# ─────────────────────────────────────────────────────────────────────────────
# Maths helpers
# ─────────────────────────────────────────────────────────────────────────────

def spectral_entropy(matrix: np.ndarray) -> float:
    """
    Shannon entropy (nats) of the normalised eigenvalues of the
    (hidden_size × hidden_size) activation covariance matrix.

    Captures the effective dimensionality / dispersion of the representation
    space independent of the number of token samples.
    """
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    cov = (centered.T @ centered) / max(len(centered) - 1, 1)
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.maximum(eigvals, 0.0)
    total = eigvals.sum()
    if total < 1e-30:
        return 0.0
    p = eigvals / total
    p = p[p > 1e-30]
    return float(-np.sum(p * np.log(p)))


def effective_rank(matrix: np.ndarray) -> float:
    """exp(spectral_entropy) — the Roy-Vetterli effective rank."""
    return math.exp(spectral_entropy(matrix))


def attn_entropy_normalised(attn_weights: np.ndarray, seq_len: int) -> float:
    """
    Mean Shannon entropy of attention distributions (normalised by log(seq_len)
    so values lie in [0, 1] regardless of sequence length).

    attn_weights: (n_heads, seq_len, seq_len) — softmax probabilities over keys.
    """
    a = np.clip(attn_weights, 1e-30, 1.0)
    # Per-head, per-query entropy, averaged
    H = -(a * np.log(a)).sum(axis=-1)       # (n_heads, seq_len)
    max_H = math.log(seq_len) if seq_len > 1 else 1.0
    return float(H.mean() / max_H)


# ─────────────────────────────────────────────────────────────────────────────
# Feature extraction
# ─────────────────────────────────────────────────────────────────────────────

def resolve_model(name: str) -> str:
    if name.startswith("hf:"):
        return name[3:]
    return MODEL_ALIASES.get(name.lower(), name)


def extract_features(hf_name: str, texts: list, device: str):
    """
    Returns
    -------
    hidden_agg     : list[np.ndarray]  shape (total_tokens, hidden_size), len = n_layers+1
    layer_attn_ent : list[float] or None  per-layer normalised attention entropy
    dc_per_layer   : list[dict] or None   per-layer D/C RMS stats  (GPT-2 only)
    """
    try:
        from transformers import AutoModel, AutoTokenizer
    except ImportError:
        print("ERROR: run  pip install transformers torch")
        sys.exit(1)

    is_gpt2 = hf_name.startswith("gpt2")

    print(f"  Loading {hf_name}...")
    tokenizer = AutoTokenizer.from_pretrained(hf_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        hf_name,
        output_hidden_states=True,
        output_attentions=True,
        trust_remote_code=True,
        dtype=torch.float32,
    )
    model.eval().to(device)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    cfg = model.config
    n_layers = getattr(cfg, "n_layer", None) or getattr(cfg, "num_hidden_layers", None)

    # ── D/C hooks (GPT-2 only) ───────────────────────────────────────────────
    # Try to locate transformer blocks regardless of transformers version.
    gpt2_blocks = None
    if is_gpt2:
        if hasattr(model, "transformer") and hasattr(model.transformer, "h"):
            gpt2_blocks = model.transformer.h
        elif hasattr(model, "h"):
            gpt2_blocks = model.h

    d_rms_per_layer = {i: [] for i in range(n_layers)}
    c_rms_per_layer = {i: [] for i in range(n_layers)}
    hooks = []

    if gpt2_blocks is not None:
        def _rms(tensor):
            return tensor.detach().float().pow(2).mean().sqrt().item()

        for i, block in enumerate(gpt2_blocks):
            def make_d_hook(idx):
                def hook(mod, inp, out):
                    d_rms_per_layer[idx].append(_rms(out))
                return hook

            def make_c_hook(idx):
                def hook(mod, inp, out):
                    x = out[0] if isinstance(out, tuple) else out
                    c_rms_per_layer[idx].append(_rms(x))
                return hook

            hooks.append(block.ln_1.register_forward_hook(make_d_hook(i)))
            hooks.append(block.ln_2.register_forward_hook(make_d_hook(i)))
            if hasattr(block.attn, "c_proj"):
                hooks.append(block.attn.c_proj.register_forward_hook(make_c_hook(i)))
            if hasattr(block.mlp, "c_proj"):
                hooks.append(block.mlp.c_proj.register_forward_hook(make_c_hook(i)))

    # ── Forward passes ────────────────────────────────────────────────────────
    all_hidden = [[] for _ in range(n_layers + 1)]
    layer_attn_sums = [0.0] * n_layers
    layer_attn_counts = [0] * n_layers
    attn_available = False

    with torch.no_grad():
        for t_idx, text in enumerate(texts):
            print(f"  Text {t_idx+1}/{len(texts)}...", end="\r")
            inputs = tokenizer(
                text, return_tensors="pt", truncation=True, max_length=256,
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            outputs = model(**inputs)

            seq_len = inputs["input_ids"].shape[1]

            for l, hs in enumerate(outputs.hidden_states):
                all_hidden[l].append(hs.squeeze(0).cpu().float().numpy())

            if outputs.attentions is not None:
                attn_available = True
                for l, aw in enumerate(outputs.attentions):
                    ent = attn_entropy_normalised(
                        aw.squeeze(0).cpu().float().numpy(), seq_len
                    )
                    layer_attn_sums[l] += ent
                    layer_attn_counts[l] += 1

    print(f"  Done ({len(texts)} texts).          ")
    for h in hooks:
        h.remove()

    # ── Aggregate hidden states (concatenate tokens across all texts) ─────────
    hidden_agg = [np.concatenate(all_hidden[l], axis=0) for l in range(n_layers + 1)]

    # ── Attention entropy per layer ───────────────────────────────────────────
    layer_attn_ent = None
    if attn_available:
        layer_attn_ent = [
            layer_attn_sums[l] / layer_attn_counts[l]
            for l in range(n_layers)
        ]

    # ── D/C stats ─────────────────────────────────────────────────────────────
    dc_per_layer = None
    if gpt2_blocks is not None and any(d_rms_per_layer[i] for i in range(n_layers)):
        dc_per_layer = []
        for i in range(n_layers):
            d_vals = d_rms_per_layer[i]
            c_vals = c_rms_per_layer[i]
            d = float(np.mean(d_vals)) if d_vals else float("nan")
            c = float(np.mean(c_vals)) if c_vals else float("nan")
            dc_per_layer.append({
                "layer": i + 1,
                "d_rms": d,
                "c_rms": c,
                "ratio": d / c if (c and c > 0) else float("nan"),
            })

    return hidden_agg, layer_attn_ent, dc_per_layer


# ─────────────────────────────────────────────────────────────────────────────
# Individual tests
# ─────────────────────────────────────────────────────────────────────────────

def test_A(hidden_agg):
    """§6.1 — spectral entropy should decrease monotonically."""
    entropies = [spectral_entropy(h) for h in hidden_agg]
    n = len(entropies)
    decreasing = sum(entropies[i] < entropies[i-1] for i in range(1, n))
    frac = decreasing / (n - 1)
    strictly = (decreasing == n - 1)
    return {
        "entropies": entropies,
        "frac_decreasing": frac,
        "strictly_monotone": strictly,
        "passed": frac >= 0.90,
    }


def test_B(hidden_agg):
    """§8.2 — consecutive effective-rank ratios → φ^{-1}."""
    ranks = [effective_rank(h) for h in hidden_agg]
    ratios = [ranks[i] / ranks[i-1] for i in range(1, len(ranks))]
    mean_r = float(np.mean(ratios))
    frac = float(np.mean([abs(r - PHI_INV) <= 0.05 for r in ratios]))
    return {
        "ranks": ranks,
        "ratios": ratios,
        "grand_mean": mean_r,
        "deviation": abs(mean_r - PHI_INV),
        "frac_within_0.05": frac,
        "passed": abs(mean_r - PHI_INV) <= 0.05,
    }


def test_C(dc_per_layer):
    """§11.2 — RMS_D / RMS_C → 0.5 (virial analogy)."""
    if dc_per_layer is None:
        return {"passed": None, "note": "N/A — requires GPT-2"}
    valid = [r["ratio"] for r in dc_per_layer if math.isfinite(r["ratio"])]
    mean_r = float(np.mean(valid))
    return {
        "per_layer": dc_per_layer,
        "mean_ratio": mean_r,
        "target": 0.5,
        "deviation": abs(mean_r - 0.5),
        "passed": abs(mean_r - 0.5) <= 0.05,
    }


def test_D(layer_attn_ent):
    """§6.1 — normalised attention entropy decreases with depth."""
    if layer_attn_ent is None:
        return {"passed": None, "note": "Attention weights not returned by model"}
    n = len(layer_attn_ent)
    dec = sum(layer_attn_ent[i] < layer_attn_ent[i-1] for i in range(1, n))
    frac = dec / (n - 1) if n > 1 else 0.0
    return {
        "layer_entropies": layer_attn_ent,
        "frac_decreasing": frac,
        "passed": frac >= 0.75,
    }


def test_E(hidden_agg):
    """§11.3 — actual depth ≈ log_φ(H_0 / H_L) within 10 %."""
    n_layers = len(hidden_agg) - 1
    H_0 = spectral_entropy(hidden_agg[0])
    H_L = spectral_entropy(hidden_agg[-1])
    if H_L <= 0 or H_0 <= H_L:
        return {
            "actual_depth": n_layers,
            "H_0": H_0, "H_L": H_L,
            "passed": False,
            "note": f"H_0/H_L ratio = {H_0/max(H_L,1e-9):.3f} ≤ 1 — formula undefined",
        }
    ratio = H_0 / H_L
    L_pred = math.log(ratio) / math.log(PHI)
    err_pct = abs(L_pred - n_layers) / n_layers * 100
    return {
        "actual_depth": n_layers,
        "H_0": H_0, "H_L": H_L,
        "H_ratio": ratio,
        "L_predicted": L_pred,
        "error_pct": err_pct,
        "passed": err_pct <= 10.0,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────────────────────────────────────

def _verd(r):
    if r.get("passed") is None:
        return "N/A  —"
    return "PASS ✓" if r["passed"] else "FAIL ✗"


def print_report(model_name, results, n_layers):
    W = 66
    print("\n" + "=" * W)
    print(f"  ALTERNATIVE THOLONIC TESTS — {model_name}")
    print(f"  Layers: {n_layers}   φ = {PHI:.6f}   φ⁻¹ = {PHI_INV:.6f}")
    print("=" * W)

    # ── A ──────────────────────────────────────────────────────────────────
    rA = results["A"]
    ents = rA["entropies"]
    print(f"\n  Test A  Activation entropy monotonicity          [{_verd(rA)}]")
    print(f"  Prediction (§6.1): spectral entropy decreases monotonically with depth")
    print(f"    Transitions that decrease : {rA['frac_decreasing']:.1%}  "
          f"(≥90% required)")
    print(f"    Strictly monotone         : {'YES' if rA['strictly_monotone'] else 'NO'}")
    print(f"    Entropy  embed → final    : {ents[0]:.3f} → {ents[-1]:.3f}  "
          f"(range {min(ents):.3f}–{max(ents):.3f})")
    # mini sparkline
    hi, lo = max(ents), min(ents)
    span = hi - lo or 1
    bar = "".join("▂▄▅▆▇█"[min(5, int(5 * (e - lo) / span))] for e in ents)
    print(f"    Entropy profile           : {bar}")

    # ── B ──────────────────────────────────────────────────────────────────
    rB = results["B"]
    print(f"\n  Test B  Effective-rank φ ratio                    [{_verd(rB)}]")
    print(f"  Prediction (§8.2): eff_rank[ℓ]/eff_rank[ℓ-1] → {PHI_INV:.4f}")
    print(f"    Grand mean ratio          : {rB['grand_mean']:.6f}")
    print(f"    |mean − φ⁻¹|             : {rB['deviation']:.6f}")
    print(f"    Fraction within ±0.05    : {rB['frac_within_0.05']:.1%}")
    ranks = rB["ranks"]
    hi, lo = max(ranks), min(ranks)
    span = hi - lo or 1
    bar = "".join("▂▄▅▆▇█"[min(5, int(5 * (r - lo) / span))] for r in ranks)
    print(f"    Effective-rank profile    : {bar}")

    # ── C ──────────────────────────────────────────────────────────────────
    rC = results["C"]
    print(f"\n  Test C  Virial D/C activation ratio               [{_verd(rC)}]")
    print(f"  Prediction (§11.2): RMS(LayerNorm) / RMS(Attn+MLP proj) → 0.500")
    if rC.get("note"):
        print(f"    {rC['note']}")
    else:
        print(f"    Mean D/C ratio            : {rC['mean_ratio']:.4f}  "
              f"(target 0.500)")
        print(f"    |mean − 0.5|             : {rC['deviation']:.4f}")
        ratios = [r["ratio"] for r in rC["per_layer"] if math.isfinite(r["ratio"])]
        hi, lo = max(ratios), min(ratios)
        span = hi - lo or 1
        bar = "".join("▂▄▅▆▇█"[min(5, int(5 * (r - lo) / span))] for r in ratios)
        print(f"    Per-layer D/C profile     : {bar}")

    # ── D ──────────────────────────────────────────────────────────────────
    rD = results["D"]
    print(f"\n  Test D  Attention entropy monotonicity            [{_verd(rD)}]")
    print(f"  Prediction (§6.1): attention entropy decreases with depth")
    if rD.get("note"):
        print(f"    {rD['note']}")
    else:
        ents_d = rD["layer_entropies"]
        print(f"    Transitions that decrease : {rD['frac_decreasing']:.1%}  "
              f"(≥75% required)")
        print(f"    Entropy  layer1 → final   : {ents_d[0]:.3f} → {ents_d[-1]:.3f}")
        hi, lo = max(ents_d), min(ents_d)
        span = hi - lo or 1
        bar = "".join("▂▄▅▆▇█"[min(5, int(5 * (e - lo) / span))] for e in ents_d)
        print(f"    Entropy profile           : {bar}")

    # ── E ──────────────────────────────────────────────────────────────────
    rE = results["E"]
    print(f"\n  Test E  Depth formula                             [{_verd(rE)}]")
    print(f"  Prediction (§11.3): L ≈ log_φ(H_embedding / H_final)  within 10%")
    if rE.get("note"):
        print(f"    {rE['note']}")
    else:
        print(f"    Actual depth              : {rE['actual_depth']}")
        print(f"    H_embedding               : {rE['H_0']:.4f} nats")
        print(f"    H_final                   : {rE['H_L']:.4f} nats")
        print(f"    H_ratio                   : {rE['H_ratio']:.4f}  "
              f"(need φ^{rE['actual_depth']} = {PHI**rE['actual_depth']:.1f} to pass)")
        print(f"    Predicted depth           : {rE['L_predicted']:.2f}")
        print(f"    Error                     : {rE['error_pct']:.1f}%")

    # ── Summary ────────────────────────────────────────────────────────────
    print("\n" + "-" * W)
    print("  SUMMARY")
    print("-" * W)
    for tag, key in [
        ("A  Activation entropy monotone  (§6.1)", "A"),
        ("B  Effective-rank φ ratio        (§8.2)", "B"),
        ("C  Virial D/C ratio 0.5         (§11.2)", "C"),
        ("D  Attention entropy monotone   (§6.1)", "D"),
        ("E  Depth formula log_φ(H₀/H_L) (§11.3)", "E"),
    ]:
        print(f"    Test {tag} : {_verd(results[key])}")
    print("=" * W + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Alternative tholonic prediction tests")
    parser.add_argument("--model", default="gpt2",
                        help="Model alias or hf:<repo> (default: gpt2)")
    parser.add_argument("--n_texts", type=int, default=len(SAMPLE_TEXTS))
    parser.add_argument("--output_dir", default="results")
    args = parser.parse_args()

    hf_name = resolve_model(args.model)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device : {device}")
    print(f"Model  : {args.model}" + (f" → {hf_name}" if hf_name != args.model else ""))

    texts = SAMPLE_TEXTS[: args.n_texts]
    hidden_agg, layer_attn_ent, dc_per_layer = extract_features(hf_name, texts, device)

    n_layers = len(hidden_agg) - 1
    print(f"Layers : {n_layers}  — computing tests …")

    results = {
        "A": test_A(hidden_agg),
        "B": test_B(hidden_agg),
        "C": test_C(dc_per_layer),
        "D": test_D(layer_attn_ent),
        "E": test_E(hidden_agg),
    }

    print_report(hf_name, results, n_layers)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = hf_name.replace("/", "_")
    out_path = out_dir / f"alt_tests_{slug}.json"

    def _serial(obj):
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return str(obj)

    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=_serial)
    print(f"Results saved → {out_path}")


if __name__ == "__main__":
    main()
