#!/usr/bin/env python3
"""
Retry the two models that failed in measure_health.py due to legacy remote code:
  - Phi-3-mini: rope_scaling["type"] KeyError from cached modeling_phi3.py
  - Falcon-7B:  get_head_mask AttributeError from cached modeling_falcon.py

Fix: trust_remote_code=False forces the native transformers implementations for
both models, which use the current API and do not have these issues.

Merges results into the existing model_health_results.json and reprints the ranking.
"""

import json, math
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ── import shared helpers from measure_health ─────────────────────────────────
import sys
sys.path.insert(0, str(Path(__file__).parent))
from measure_health import (
    DTYPE, run_phase_detection, run_virial,
    score_boundaries, score_virial,
)

FAILED_MODELS = [
    ("microsoft/Phi-3-mini-4k-instruct", "Phi-3-mini", "Phi",    32),
    ("tiiuae/falcon-7b",                 "Falcon-7B",   "Falcon", 32),
]

def assess(hf_name, display_name, family, n_layers_expected):
    tok = AutoTokenizer.from_pretrained(hf_name, trust_remote_code=False)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    mdl = AutoModelForCausalLM.from_pretrained(
        hf_name,
        output_hidden_states=True,
        output_attentions=True,
        trust_remote_code=False,   # use native transformers implementation
        torch_dtype=DTYPE,
        low_cpu_mem_usage=True,
    )
    mdl.eval()
    n = mdl.config.num_hidden_layers

    boundaries = run_phase_detection(mdl, tok, n)
    ax1, ax2, ax3, ax4, annotated = score_boundaries(boundaries, n)

    per_layer = run_virial(mdl, tok, n)
    ax5, mean_dc = score_virial(per_layer)

    del mdl
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    overall = round((ax1 + ax2 + ax3 + ax4 + ax5) / 5)
    axes = {"fidelity": ax1, "role_consistency": ax2,
            "compression": ax3, "equilibrium": ax4, "virial": ax5}
    bottleneck = min(axes, key=axes.get)
    bottleneck_labels = {
        "fidelity":         "Boundary fidelity",
        "role_consistency": "Role consistency",
        "compression":      "Compression stage",
        "equilibrium":      "Equilibrium stage",
        "virial":           f"Structural balance (D/C ≈ {mean_dc:.2f} vs target 0.5)",
    }
    return {
        "hf_name": hf_name, "display_name": display_name,
        "family": family, "n_layers": n,
        "scores": {
            "fidelity": ax1, "role_consistency": ax2,
            "compression": ax3, "equilibrium": ax4,
            "virial": ax5, "overall": overall,
        },
        "mean_dc_ratio": round(mean_dc, 3) if not math.isnan(mean_dc) else None,
        "bottleneck": bottleneck,
        "bottleneck_label": bottleneck_labels[bottleneck],
        "boundaries": annotated,
        "virial_layers": per_layer if per_layer else [],
    }


if __name__ == "__main__":
    results_path = Path(__file__).parent / "model_health_results.json"

    # Load existing results
    existing = []
    if results_path.exists():
        with open(results_path) as f:
            existing = json.load(f)
    existing_names = {r["hf_name"] for r in existing}

    print("=" * 68)
    print("  RETRY: Phi-3-mini and Falcon-7B (trust_remote_code=False)")
    print("=" * 68)

    new_results = []
    for hf_name, display_name, family, n_exp in FAILED_MODELS:
        print(f"\n  Assessing {display_name} ...", flush=True)
        try:
            r = assess(hf_name, display_name, family, n_exp)
            s = r["scores"]
            new_results.append(r)
            print(f"    fidelity={s['fidelity']:3d}  role={s['role_consistency']:3d}  "
                  f"compress={s['compression']:3d}  equil={s['equilibrium']:3d}  "
                  f"virial={s['virial']:3d}  → overall={s['overall']:3d}  "
                  f"bottleneck={r['bottleneck']}")
        except Exception as ex:
            import traceback
            print(f"    ERROR: {ex}")
            traceback.print_exc()

    # Merge: replace any existing entry for the same model, append new ones
    merged = [r for r in existing if r["hf_name"] not in {x["hf_name"] for x in new_results}]
    merged.extend(new_results)

    with open(results_path, "w") as f:
        json.dump(merged, f, indent=2)

    # Reprint full ranking
    print("\n" + "=" * 68)
    print("  UPDATED RANKING (by overall health score)")
    print(f"  {'Rank':<5} {'Model':<16} {'Overall':>8}  "
          f"{'Fid':>5} {'Role':>5} {'Comp':>5} {'Equil':>5} {'Viral':>5}  Bottleneck")
    print(f"  {'-'*72}")
    ranked = sorted(merged, key=lambda r: -r["scores"]["overall"])
    for i, r in enumerate(ranked):
        s = r["scores"]
        print(f"  {i+1:<5} {r['display_name']:<16} {s['overall']:>8}  "
              f"{s['fidelity']:>5} {s['role_consistency']:>5} "
              f"{s['compression']:>5} {s['equilibrium']:>5} {s['virial']:>5}  "
              f"{r['bottleneck']}")

    print(f"\n  Results saved → {results_path}")
    print("=" * 68)
