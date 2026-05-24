#!/usr/bin/env python3
"""
Tholonic phi-ratio measurement script.

Tests the falsifiable prediction from Section 12, row 1 of:
  Milton, J.W. (2026). Neural Networks as Tholonic Systems.
  Clarity Coalition.

Prediction: well-trained networks exhibit phi-adjacent inter-level activation
ratios. Specifically, ||h_l|| / ||h_{l-1}|| clusters near phi^(-1) ≈ 0.618 ± 0.05
across all layers and across model scales.

Usage:
  pip install torch transformers numpy matplotlib scipy
  python measure_phi_ratios.py
  python measure_phi_ratios.py --model gpt2-medium
  python measure_phi_ratios.py --model gpt2-large --n_texts 200
  python measure_phi_ratios.py --model qwen2.5-0.5b
  python measure_phi_ratios.py --model qwen2.5-1.5b
  python measure_phi_ratios.py --model hf:Qwen/Qwen3-0.6B

GPT-2 family runs fully locally via transformers (no extra setup).
Qwen shortcuts automatically resolve to the matching HuggingFace repo.
Any HuggingFace model can be specified directly with the hf: prefix.

Note: Ollama is great for chat, but does NOT expose per-layer hidden states.
      This script always uses the transformers library for activation access.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI  # ≈ 0.618 — the tholonic prediction

# Short names → HuggingFace repo IDs
MODEL_ALIASES = {
    "gpt2":          "gpt2",
    "gpt2-medium":   "gpt2-medium",
    "gpt2-large":    "gpt2-large",
    "gpt2-xl":       "gpt2-xl",
    "qwen2.5-0.5b":  "Qwen/Qwen2.5-0.5B",
    "qwen2.5-1.5b":  "Qwen/Qwen2.5-1.5B",
    "qwen2.5-3b":    "Qwen/Qwen2.5-3B",
    "qwen2.5-7b":    "Qwen/Qwen2.5-7B",
    "qwen3-0.6b":    "Qwen/Qwen3-0.6B",
    "qwen3-1.7b":    "Qwen/Qwen3-1.7B",
    "qwen3-4b":      "Qwen/Qwen3-4B",
}

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
    "The bitter lesson: methods that scale with compute consistently outperform those that encode knowledge.",
    "Deep learning replaced decades of hand-crafted computer vision features in a single year.",
    "Self-attention allows each token to attend to all other tokens in the sequence simultaneously.",
    "The virial theorem relates kinetic and potential energy in a bound physical system.",
    "Representation learning extracts useful features automatically from raw data.",
    "The structural balance between integration and constraint determines system stability.",
]


def resolve_model_name(name: str) -> str:
    """Resolve a short alias or hf: prefix to a HuggingFace repo ID."""
    if name.startswith("hf:"):
        return name[3:]
    return MODEL_ALIASES.get(name.lower(), name)


def get_hidden_state_norms(model_name: str, texts: list[str], device: str) -> dict:
    """
    Extract per-layer hidden state norms from any HuggingFace causal LM.

    Uses AutoModel / AutoTokenizer so it works with GPT-2, Qwen, Llama, etc.

    Returns a dict with:
      - 'norms': list of lists — norms[text_idx][layer_idx]
      - 'ratios': list of lists — ratios[text_idx][ratio_idx]
      - 'n_layers': int
      - 'model_name': str
    """
    try:
        from transformers import AutoModel, AutoTokenizer
    except ImportError:
        print("ERROR: transformers not installed. Run: pip install transformers torch")
        sys.exit(1)

    hf_name = resolve_model_name(model_name)
    display_name = model_name if model_name == hf_name else f"{model_name} ({hf_name})"
    print(f"Loading {display_name}...")

    tokenizer = AutoTokenizer.from_pretrained(hf_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        hf_name,
        output_hidden_states=True,
        trust_remote_code=True,
        torch_dtype=torch.float32,
    )
    model.eval()
    model.to(device)

    # Some tokenizers (e.g. Qwen) have no explicit pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    all_norms = []
    all_ratios = []

    with torch.no_grad():
        for i, text in enumerate(texts):
            print(f"  Processing text {i+1}/{len(texts)}...", end='\r')
            inputs = tokenizer(
                text, return_tensors="pt", truncation=True, max_length=512,
                padding=False,
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            outputs = model(**inputs)

            # hidden_states: tuple of (n_layers+1) tensors, each (batch=1, seq_len, hidden_size)
            # Index 0 = embedding layer, 1..N = transformer blocks
            hidden_states = outputs.hidden_states

            norms = []
            for hs in hidden_states:
                mean_hs = hs.squeeze(0).mean(dim=0)  # (hidden_size,)
                norm = mean_hs.norm().item()
                norms.append(norm)

            ratios = [norms[j] / norms[j - 1] for j in range(1, len(norms))]

            all_norms.append(norms)
            all_ratios.append(ratios)

    print(f"  Done processing {len(texts)} texts.          ")
    return {
        'model_name': hf_name,
        'n_layers': len(all_norms[0]) - 1,
        'norms': all_norms,
        'ratios': all_ratios,
    }


def compute_statistics(data: dict) -> dict:
    ratios_arr = np.array(data['ratios'])  # (n_texts, n_layers)
    mean_ratios = ratios_arr.mean(axis=0)
    std_ratios = ratios_arr.std(axis=0)
    all_flat = ratios_arr.flatten()

    grand_mean = float(all_flat.mean())
    grand_std = float(all_flat.std())
    deviation_from_phi = float(abs(grand_mean - PHI_INV))
    within_tolerance = bool(deviation_from_phi <= 0.05)

    # Fraction of individual ratios within 0.05 of phi_inv
    frac_within_tol = float(np.mean(np.abs(all_flat - PHI_INV) <= 0.05))

    return {
        'model_name': data['model_name'],
        'n_texts': len(data['ratios']),
        'n_layers': data['n_layers'],
        'grand_mean': grand_mean,
        'grand_std': grand_std,
        'phi_inv': PHI_INV,
        'deviation_from_phi_inv': deviation_from_phi,
        'within_0.05_tolerance': within_tolerance,
        'fraction_within_tolerance': frac_within_tol,
        'per_layer_mean': mean_ratios.tolist(),
        'per_layer_std': std_ratios.tolist(),
    }


def print_report(stats: dict):
    print("\n" + "=" * 60)
    print(f"  RESULTS: {stats['model_name']}")
    print("=" * 60)
    print(f"  Texts processed   : {stats['n_texts']}")
    print(f"  Transformer layers: {stats['n_layers']}")
    print(f"  phi^(-1) (predict): {stats['phi_inv']:.6f}")
    print(f"  Grand mean ratio  : {stats['grand_mean']:.6f}")
    print(f"  Grand std         : {stats['grand_std']:.6f}")
    print(f"  |mean - phi^(-1)| : {stats['deviation_from_phi_inv']:.6f}")
    print(f"  Within ±0.05 tol  : {'YES ✓' if stats['within_0.05_tolerance'] else 'NO ✗'}")
    print(f"  Frac within ±0.05 : {stats['fraction_within_tolerance']:.1%}")
    print()
    print("  Per-layer means:")
    for i, (m, s) in enumerate(zip(stats['per_layer_mean'], stats['per_layer_std'])):
        bar_len = int(m * 40)
        bar = '█' * bar_len
        marker = ' ← phi^(-1)' if abs(m - PHI_INV) < 0.03 else ''
        print(f"    Layer {i+1:2d}: {m:.4f} ± {s:.4f}  |{bar}{marker}")
    print("=" * 60)

    verdict = (
        "SUPPORTS tholonic prediction (mean within ±0.05 of phi^(-1))"
        if stats['within_0.05_tolerance']
        else "DOES NOT SUPPORT tholonic prediction (mean outside ±0.05 of phi^(-1))"
    )
    print(f"\n  Verdict: {verdict}\n")


def save_results(stats: dict, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    model_slug = stats['model_name'].replace('/', '_')
    out_path = output_dir / f"results_{model_slug}.json"
    with open(out_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Results saved to: {out_path}")


def plot_results(stats: dict, output_dir: Path):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("matplotlib not installed — skipping plots. Run: pip install matplotlib")
        return

    model_slug = stats['model_name'].replace('/', '_')
    layers = list(range(1, stats['n_layers'] + 1))
    means = stats['per_layer_mean']
    stds = stats['per_layer_std']

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(
        f"Tholonic φ-ratio Prediction Test — {stats['model_name']}",
        fontsize=14, fontweight='bold', color='#311b92'
    )

    # Left: ratio per layer with error bars
    ax = axes[0]
    ax.errorbar(layers, means, yerr=stds, fmt='o-', color='#4527a0',
                ecolor='#7e57c2', capsize=4, linewidth=2, markersize=7, label='Mean ± std')
    ax.axhline(PHI_INV, color='#c62828', linestyle='--', linewidth=2,
               label=f'φ⁻¹ ≈ {PHI_INV:.4f} (prediction)')
    ax.axhline(PHI_INV + 0.05, color='#c62828', linestyle=':', linewidth=1, alpha=0.5)
    ax.axhline(PHI_INV - 0.05, color='#c62828', linestyle=':', linewidth=1, alpha=0.5,
               label='±0.05 tolerance band')
    ax.fill_between([min(layers) - 0.5, max(layers) + 0.5],
                    PHI_INV - 0.05, PHI_INV + 0.05,
                    alpha=0.08, color='#c62828')
    ax.axhline(1.0, color='gray', linestyle=':', linewidth=1, alpha=0.4, label='ratio = 1.0')
    ax.set_xlabel('Layer index', fontsize=12)
    ax.set_ylabel('||h_ℓ|| / ||h_{ℓ-1}||', fontsize=12)
    ax.set_title(f'Inter-layer activation norm ratios', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(min(layers) - 0.5, max(layers) + 0.5)

    # Right: histogram of all ratios
    ax2 = axes[1]
    import itertools
    # Reload flat ratios from means/stds approximation isn't possible here cleanly
    # Just use means as representative
    ax2.bar(layers, means, color='#7e57c2', alpha=0.7, edgecolor='white', width=0.7)
    ax2.axhline(PHI_INV, color='#c62828', linestyle='--', linewidth=2.5,
                label=f'φ⁻¹ ≈ {PHI_INV:.4f}')
    ax2.axhline(stats['grand_mean'], color='#4527a0', linestyle='-', linewidth=2,
                label=f"Grand mean = {stats['grand_mean']:.4f}")
    ax2.fill_between([0.5, stats['n_layers'] + 0.5], PHI_INV - 0.05, PHI_INV + 0.05,
                     alpha=0.1, color='#c62828', label='±0.05 tolerance')
    ax2.set_xlabel('Layer index', fontsize=12)
    ax2.set_ylabel('Mean ratio', fontsize=12)
    ax2.set_title('Per-layer mean ratios vs. φ⁻¹ prediction', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.25, axis='y')

    plt.tight_layout()
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_path = output_dir / f"phi_ratios_{model_slug}.png"
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    plt.show()


def main():
    alias_list = ", ".join(MODEL_ALIASES.keys())
    parser = argparse.ArgumentParser(
        description='Tholonic phi-ratio measurement',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Known aliases: {alias_list}\nOr use hf:<org/repo> for any HuggingFace model.",
    )
    parser.add_argument('--model', default='gpt2',
                        help='Model alias or hf:<repo> (default: gpt2)')
    parser.add_argument('--n_texts', type=int, default=len(SAMPLE_TEXTS),
                        help='Number of texts to process')
    parser.add_argument('--output_dir', default='results',
                        help='Directory for output files')
    parser.add_argument('--no_plot', action='store_true', help='Skip matplotlib plots')
    args = parser.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    hf_name = resolve_model_name(args.model)
    print(f"Device: {device}")
    print(f"Model: {args.model}" + (f" → {hf_name}" if hf_name != args.model else ""))
    print(f"Texts: {args.n_texts}")
    print(f"phi^(-1) prediction: {PHI_INV:.6f}")
    print()

    texts = SAMPLE_TEXTS[:args.n_texts]
    data = get_hidden_state_norms(args.model, texts, device)
    stats = compute_statistics(data)
    print_report(stats)

    output_dir = Path(args.output_dir)
    save_results(stats, output_dir)
    if not args.no_plot:
        plot_results(stats, output_dir)


if __name__ == '__main__':
    main()
