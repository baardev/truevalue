#!/usr/bin/env python3
"""Generate the figures for Research paper 10 (tholonic neural architecture).

All data figures use only the numbers reported in the paper's Section 13 tables.
Schematic figures are illustrative diagrams and are labeled as such in captions.

Output: docnav/Research/papers/figures/10_*.png
"""

import math
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

OUT = "docnav/Research/papers/figures"

D_COLOR = "#1f5fa8"   # Definition: blue
C_COLOR = "#c2542b"   # Contribution: orange-red
N_COLOR = "#3c8a4e"   # Negotiation: green
GREY = "#666666"

plt.rcParams.update({
    "font.size": 10,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 160,
})


def save(fig, name):
    fig.savefig(f"{OUT}/{name}", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT}/{name}")


# ----------------------------------------------------------------------------
# Figure 1: paradigm plane (schematic)
# ----------------------------------------------------------------------------
def fig_paradigm_plane():
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    ax.plot([0, 10.5], [0, 10.5], "--", color=N_COLOR, lw=1.5, zorder=1)
    ax.text(3.05, 3.55, "balance diagonal (D ~ C)", color=N_COLOR, fontsize=9,
            ha="center", style="italic", rotation=42)

    pts = {
        "Symbolic AI": (8.5, 2.6, D_COLOR, 0.85),
        "Connectionist AI": (2.0, 8.0, C_COLOR, -0.95),
        "Neurosymbolic\nhybrids": (5.4, 7.2, "#8a5fa8", -0.95),
        "Tholonic\narchitecture": (8.3, 8.3, N_COLOR, -0.95),
    }
    for label, (x, y, color, dy) in pts.items():
        ax.scatter([x], [y], s=190, color=color, zorder=3,
                   edgecolor="black", linewidth=0.6)
        ax.text(x, y + dy, label, ha="center",
                va="top" if dy < 0 else "bottom", fontsize=10, color=color,
                fontweight="bold")

    ax.annotate("", xy=(8.0, 8.2), xytext=(5.7, 7.35),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2,
                                linestyle=":"))
    ax.text(6.8, 8.25, "modular to\nconstitutive", fontsize=8, color=GREY,
            ha="center")

    ax.text(8.5, 4.05, "brittle,\nnon-generalizing", ha="center", fontsize=8,
            color=GREY, style="italic")
    ax.text(2.0, 9.0, "specification gaming,\nreward hacking", ha="center",
            fontsize=8, color=GREY, style="italic")

    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 10.8)
    ax.set_xlabel("D strength (structural constraint, definition)")
    ax.set_ylabel("C strength (integration, learning)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("The four paradigms on the D-C plane")
    save(fig, "10_paradigm-plane.png")


# ----------------------------------------------------------------------------
# Figure 2: N-D-C mapping at four scales (schematic)
# ----------------------------------------------------------------------------
def fig_ndc_mapping():
    fig, axes = plt.subplots(1, 4, figsize=(13, 4.4))
    panels = [
        ("Node", "weights +\nactivation threshold", "weighted\ninput sum",
         "activated\noutput"),
        ("Layer", "normalization\n(LayerNorm)", "collective\nactivations",
         "representational\noutput"),
        ("Transformer block", "residual +\nlayer norm", "attention +\nMLP",
         "block\noutput"),
        ("Full model", "embedding +\npositional encoding", "stack of\nblocks",
         "output\ndistribution"),
    ]
    for ax, (title, d, c, n) in zip(axes, panels):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")
        ax.set_title(title, fontsize=11, fontweight="bold")
        # triangle vertices: D bottom-left, C bottom-right, N top
        coords = {"D": (2.2, 2.6), "C": (7.8, 2.6), "N": (5.0, 8.0)}
        ax.add_patch(Polygon([coords["D"], coords["C"], coords["N"]],
                             closed=True, fill=False, edgecolor=GREY, lw=1.1))
        for role, (x, y), color, text in [
            ("D", coords["D"], D_COLOR, d),
            ("C", coords["C"], C_COLOR, c),
            ("N", coords["N"], N_COLOR, n),
        ]:
            ax.scatter([x], [y], s=420, color=color, zorder=3,
                       edgecolor="black", linewidth=0.6)
            ax.text(x, y, role, ha="center", va="center", color="white",
                    fontsize=12, fontweight="bold", zorder=4)
            dy = -1.0 if role != "N" else 1.05
            ax.text(x, y + dy, text, ha="center",
                    va="top" if dy < 0 else "bottom", fontsize=8.5,
                    color=color)
    # arrows between panels: N of one scale feeds C of the next
    for i in range(3):
        fig.text(0.255 + i * 0.245, 0.5, r"$\rightarrow$", fontsize=20,
                 ha="center", va="center", color=N_COLOR)
    fig.suptitle("The same N-D-C operation at four scales; "
                 "each level's N becomes a C-input above", y=1.02, fontsize=12)
    save(fig, "10_ndc-neural-mapping.png")


# ----------------------------------------------------------------------------
# Figure 3: entropy funnel / supply chain framing (schematic)
# ----------------------------------------------------------------------------
def fig_entropy_funnel():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

    chain = ["raw\nmaterial", "extraction", "refining", "certification",
             "registered\nproduct"]
    widths = [9, 7, 5, 3.2, 1.8]
    for i, (label, w) in enumerate(zip(chain, widths)):
        y = 9 - i * 2
        ax1.add_patch(FancyBboxPatch(((10 - w) / 2, y - 0.75), w, 1.5,
                                     boxstyle="round,pad=0.08",
                                     facecolor="#e8d9a0", edgecolor=GREY))
        ax1.text(5, y, label, ha="center", va="center", fontsize=9)
        if i < len(chain) - 1:
            ax1.annotate("", xy=(5, y - 1.32), xytext=(5, y - 0.85),
                         arrowprops=dict(arrowstyle="->", color=GREY))
    ax1.set_xlim(0, 10)
    ax1.set_ylim(-0.2, 10.4)
    ax1.axis("off")
    ax1.set_title("Commodity supply chain:\nsuccessive D-C closures")

    layers = ["input tokens", "early layers", "middle layers", "late layers",
              "output distribution"]
    widths = [9, 7, 5, 3.2, 1.8]
    for i, (label, w) in enumerate(zip(layers, widths)):
        y = 9 - i * 2
        ax2.add_patch(FancyBboxPatch(((10 - w) / 2, y - 0.75), w, 1.5,
                                     boxstyle="round,pad=0.08",
                                     facecolor="#cfe0f0", edgecolor=GREY))
        ax2.text(5, y, label, ha="center", va="center", fontsize=9)
        if i < len(layers) - 1:
            ax2.annotate("", xy=(5, y - 1.32), xytext=(5, y - 0.85),
                         arrowprops=dict(arrowstyle="->", color=GREY))
    ax2.annotate(r"$H_\ell$ decreases with depth", xy=(9.0, 5),
                 fontsize=10, rotation=-90, ha="center", va="center",
                 color=D_COLOR)
    ax2.annotate("", xy=(9.6, 1.4), xytext=(9.6, 8.6),
                 arrowprops=dict(arrowstyle="->", color=D_COLOR, lw=1.4))
    ax2.set_xlim(0, 10.6)
    ax2.set_ylim(-0.2, 10.4)
    ax2.axis("off")
    ax2.set_title("Neural network inference:\nprogressive entropy reduction")

    fig.suptitle("Inference as a supply chain: diffuse to committed", y=1.02)
    save(fig, "10_entropy-funnel.png")


# ----------------------------------------------------------------------------
# Figure 4: annotated transformer block (schematic)
# ----------------------------------------------------------------------------
def fig_transformer_annotated():
    fig, ax = plt.subplots(figsize=(7.2, 8.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    ax.axis("off")

    def box(y, label, color, w=4.6, x=2.7, h=0.95, fs=9.5):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor="black",
                                    linewidth=0.6, alpha=0.85))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color="white", fontweight="bold")
        return y + h

    def arrow(y0, y1, x=5.0):
        ax.annotate("", xy=(x, y1), xytext=(x, y0),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.1))

    items = [
        ("token embedding", C_COLOR, "C"),
        ("positional encoding   [pi]", D_COLOR, "D"),
        ("LayerNorm / RMSNorm", D_COLOR, "D"),
        ("masked self-attention\nsoftmax(QK$^T$/sqrt(d$_k$))V   [e, sqrt(2)]",
         C_COLOR, "C"),
        ("residual add", C_COLOR, "C"),
        ("LayerNorm / RMSNorm", D_COLOR, "D"),
        ("MLP / FFN   [sqrt(2) init]", C_COLOR, "C"),
        ("residual add", C_COLOR, "C"),
        ("output projection (lm_head)", C_COLOR, "C"),
        ("cross-entropy objective   [ln 2]", D_COLOR, "D"),
    ]
    y = 0.6
    for label, color, role in items:
        h = 1.35 if "\n" in label else 0.95
        ax.add_patch(FancyBboxPatch((2.7, y), 4.6, h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor="black",
                                    linewidth=0.6, alpha=0.88))
        ax.text(5.0, y + h / 2, label, ha="center", va="center", fontsize=9,
                color="white", fontweight="bold")
        ax.text(7.75, y + h / 2, role, ha="center", va="center", fontsize=11,
                color=color, fontweight="bold")
        y_top = y + h
        y = y_top + 0.42
        if (label, color, role) != items[-1]:
            arrow(y_top, y)

    ax.text(1.15, 7.4, "vocabulary boundary, causal mask,\ncontext window: "
            "structural D limits", rotation=90, fontsize=8.5, color=D_COLOR,
            ha="center", va="center", style="italic")

    handles = [
        plt.Line2D([0], [0], marker="s", linestyle="", markersize=11,
                   markerfacecolor=D_COLOR, label="D: constrain / bound"),
        plt.Line2D([0], [0], marker="s", linestyle="", markersize=11,
                   markerfacecolor=C_COLOR, label="C: integrate / enrich"),
    ]
    ax.legend(handles=handles, loc="upper right", frameon=False, fontsize=9)
    ax.set_title("Transformer components by tholonic role\n"
                 "(constants in brackets; D is sparse, C is deep)", fontsize=11)
    save(fig, "10_transformer-annotated.png")


# ----------------------------------------------------------------------------
# Figure 5: decision pathways (schematic)
# ----------------------------------------------------------------------------
def fig_decision_pathways():
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.4))
    flows = {
        "C-dominant AI": (
            C_COLOR,
            ["objective:\nmaximize engagement",
             "early layers:\noutrage and novelty produce clicks",
             "middle layers:\naddictive patterns retain users",
             "late layers:\nfilter bubbles maximize per-user engagement",
             "output:\noutrage-inducing, addictive,\npolarizing content"],
            "no structural D during inference;\nhighest-C path is free"),
        "Tholonically-balanced AI": (
            N_COLOR,
            ["objective:\nmaximize engagement",
             "early layers:\nD-sublayer flags trust degradation",
             "middle layers:\nbalance regularizer penalizes\nhigh-C / low-D paths",
             "late layers:\nscope narrows to sustainable engagement",
             "output:\ngenuine interest, discovery,\nstable engagement"],
            "high-C/low-D configurations\nare structurally expensive"),
    }
    for ax, (title, (color, steps, note)) in zip(axes, flows.items()):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 16)
        ax.axis("off")
        ax.set_title(title, fontsize=12, fontweight="bold", color=color)
        y = 15.0
        for i, step in enumerate(steps):
            h = 1.5 + 0.55 * step.count("\n")
            face = "#f2f2f2" if i == 0 else color
            tcol = "black" if i == 0 else "white"
            ax.add_patch(FancyBboxPatch((1.2, y - h), 7.6, h,
                                        boxstyle="round,pad=0.12",
                                        facecolor=face, alpha=0.9,
                                        edgecolor="black", linewidth=0.6))
            ax.text(5.0, y - h / 2, step, ha="center", va="center",
                    fontsize=8.8, color=tcol)
            if i < len(steps) - 1:
                ax.annotate("", xy=(5, y - h - 0.62), xytext=(5, y - h - 0.08),
                            arrowprops=dict(arrowstyle="->", color=GREY))
            y = y - h - 0.7
        ax.text(5, y - 0.1, note, ha="center", va="top", fontsize=8.6,
                style="italic", color=GREY)
    fig.suptitle("The decision supply chain under the same objective "
                 "(schematic; Section 10.6)", y=0.99)
    save(fig, "10_decision-pathways.png")


# ----------------------------------------------------------------------------
# Figure 6: phase detection method (schematic, synthetic traces)
# ----------------------------------------------------------------------------
def fig_phase_detection():
    rng = np.random.default_rng(7)
    L = 24
    x = np.arange(L)
    boundaries = [5, 12, 19]

    def trace(base, jumps, noise=0.04):
        y = np.full(L, base, dtype=float)
        for b, j in zip(boundaries, jumps):
            y[b:] += j
        y += np.cumsum(rng.normal(0, noise, L)) * 0.3
        return y

    metrics = [
        ("effective rank", trace(0.8, [0.5, -0.3, -0.6]), "#1f5fa8"),
        ("attention entropy", trace(0.6, [-0.25, 0.45, -0.5]), "#c2542b"),
        ("gradient sensitivity", trace(0.5, [0.4, -0.5, 0.35]), "#3c8a4e"),
        ("delta norm", trace(0.4, [0.45, 0.4, -0.55]), "#8a5fa8"),
    ]
    fig, axes = plt.subplots(4, 1, figsize=(8.2, 6.8), sharex=True)
    for ax, (name, y, color) in zip(axes, metrics):
        ax.plot(x, y, color=color, lw=1.6)
        ax.set_ylabel(name, fontsize=8.5)
        ax.set_yticks([])
        for b in boundaries:
            ax.axvline(b - 0.5, color="black", lw=0.9, linestyle="--",
                       alpha=0.55)
    labels = [r"$e^{1}$ (expansion)", r"$\sqrt{2}^{\,2}$ (scaling)",
              r"$\ln 2^{\,1}$ (compression)"]
    for b, lab in zip(boundaries, labels):
        axes[0].text(b - 0.5, axes[0].get_ylim()[1] * 1.02, lab, ha="center",
                     fontsize=8.5, va="bottom")
    axes[-1].set_xlabel("layer index")
    fig.suptitle("Four-metric phase boundary detection (schematic traces)\n"
                 "dashed lines: detected transitions; annotations: "
                 "constant matched by the norm ratio", y=1.01, fontsize=10.5)
    fig.tight_layout()
    save(fig, "10_phase-detection-traces.png")


# ----------------------------------------------------------------------------
# Data from Section 13.3 / 13.4 tables
# ----------------------------------------------------------------------------
MODELS = [
    # name, family, passes, total, fidelity, phi, ln2, virial, overall
    ("GPT-1", "GPT-1", 2, 3, 67, 40, 25, 0, 26),
    ("distilGPT-2", "GPT-2", 2, 3, 67, 25, 40, 0, 26),
    ("GPT-2 small", "GPT-2", 2, 4, 50, 40, 25, 0, 33),
    ("GPT-2 medium", "GPT-2", 4, 6, 67, 40, 25, 0, 31),
    ("GPT-2 large", "GPT-2", 3, 4, 75, 40, 87, 0, 47),
    ("GPT-2 XL", "GPT-2", 4, 4, 100, 40, 25, 0, 33),
    ("GPT-Neo 125m", "GPT-Neo", 4, 4, 100, 40, 97, 4, 55),
    ("GPT-Neo 1.3B", "GPT-Neo", 5, 7, 71, 40, 25, 23, 36),
    ("Pythia 160m", "Pythia", 4, 4, 100, 18, 25, 0, 34),
    ("Pythia 410m", "Pythia", 5, 6, 83, 40, 62, 0, 44),
    ("OPT 125m", "OPT", 3, 3, 100, 40, 97, 0, 52),
    ("Qwen2.5-0.5B", "Qwen", 6, 7, 86, 97, 75, 0, 57),
    ("Qwen3-0.6B", "Qwen", 5, 6, 83, 40, 25, 0, 35),
    ("TinyLlama-1.1B", "LLaMA", 2, 4, 50, 40, 79, 0, 44),
]

FAMILY_COLORS = {
    "GPT-1": "#7f7f7f", "GPT-2": "#1f5fa8", "GPT-Neo": "#c2542b",
    "Pythia": "#3c8a4e", "OPT": "#8a5fa8", "Qwen": "#b8860b",
    "LLaMA": "#a83232",
}


# ----------------------------------------------------------------------------
# Figure 7: pass rates by model (data)
# ----------------------------------------------------------------------------
def fig_pass_rates():
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    names = [m[0] for m in MODELS]
    rates = [100.0 * m[2] / m[3] for m in MODELS]
    colors = [FAMILY_COLORS[m[1]] for m in MODELS]
    bars = ax.bar(range(len(MODELS)), rates, color=colors,
                  edgecolor="black", linewidth=0.4)
    for bar, m in zip(bars, MODELS):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{m[2]}/{m[3]}", ha="center", fontsize=7.6)
    ax.axhline(67, color="black", linestyle="--", lw=1.1)
    ax.text(13.45, 68.5, "67% threshold", fontsize=8.5, ha="right")
    ax.axhline(78, color=N_COLOR, linestyle="-", lw=1.1, alpha=0.7)
    ax.text(13.45, 79.5, "combined 78% (51/65)", fontsize=8.5, ha="right",
            color=N_COLOR)
    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels(names, rotation=40, ha="right", fontsize=8.2)
    ax.set_ylabel("pass rate at detected boundaries (%)")
    ax.set_ylim(0, 112)
    handles = [plt.Line2D([0], [0], marker="s", linestyle="", markersize=8,
                          markerfacecolor=c, label=f)
               for f, c in FAMILY_COLORS.items()]
    ax.legend(handles=handles, ncol=4, frameon=False, fontsize=8,
              loc="upper left")
    ax.set_title("Tholonic constant matches at data-driven phase boundaries "
                 "(Section 13.3)")
    save(fig, "10_pass-rates-by-model.png")


# ----------------------------------------------------------------------------
# Figure 8: constant role scorecard (data)
# ----------------------------------------------------------------------------
def fig_constant_roles():
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    consts = [r"$\phi$", r"$\sqrt{2}$", r"$\ln 2$", r"$e$"]
    counts = [20, 16, 13, 2]
    roles = ["equilibrium\n(mid-network)",
             "scaling\n(entry / exit)",
             "compression\n(toward output)",
             "expansion\n(embedding)"]
    colors = [N_COLOR, D_COLOR, "#8a5fa8", C_COLOR]
    bars = ax.bar(consts, counts, color=colors, edgecolor="black",
                  linewidth=0.5, width=0.62)
    for bar, count, role in zip(bars, counts, roles):
        ax.text(bar.get_x() + bar.get_width() / 2, count + 0.4, str(count),
                ha="center", fontsize=11, fontweight="bold")
        ax.text(bar.get_x() + bar.get_width() / 2, -2.6, role, ha="center",
                va="top", fontsize=8.3, color=GREY)
    ax.set_ylabel("appearances among 51 passing transitions")
    ax.set_ylim(0, 24)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelsize=13, pad=2)
    ax.set_title("Constant role scorecard: each constant appears in its "
                 "theoretically assigned role\n($e$: too rare to evaluate)",
                 fontsize=10.5)
    fig.subplots_adjust(bottom=0.24)
    save(fig, "10_constant-roles.png")


# ----------------------------------------------------------------------------
# Figure 9: five-axis health heatmap (data; sqrt2 axis not reported)
# ----------------------------------------------------------------------------
def fig_health_heatmap():
    axes_labels = ["boundary\nfidelity", r"$\phi$" "\nequilibrium",
                   "ln2\ncompression", "virial\nbalance", "overall"]
    data = np.array([[m[4], m[5], m[6], m[7], m[8]] for m in MODELS],
                    dtype=float)
    fig, ax = plt.subplots(figsize=(7.4, 6.6))
    im = ax.imshow(data, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(len(axes_labels)))
    ax.set_xticklabels(axes_labels, fontsize=9)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels([m[0] for m in MODELS], fontsize=8.6)
    for i in range(len(MODELS)):
        for j in range(len(axes_labels)):
            v = data[i, j]
            ax.text(j, i, f"{int(v)}", ha="center", va="center", fontsize=8,
                    color="black" if 25 < v < 80 else
                    ("white" if v <= 25 else "black"))
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("axis score (0-100)", fontsize=9)
    ax.set_title("Structural health grading across 14 models (Section 13.4)\n"
                 r"$\sqrt{2}$ scaling axis omitted from source table; "
                 "overall is the five-axis composite", fontsize=10)
    save(fig, "10_health-heatmap.png")


# ----------------------------------------------------------------------------
# Figure 10: virial gap (data)
# ----------------------------------------------------------------------------
def fig_virial_gap():
    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    names = [m[0] for m in MODELS]
    virial = [m[7] for m in MODELS]
    colors = [FAMILY_COLORS[m[1]] for m in MODELS]
    y = np.arange(len(MODELS))
    ax.barh(y, virial, color=colors, edgecolor="black", linewidth=0.4,
            height=0.62)
    for yi, v in zip(y, virial):
        ax.text(max(v, 0) + 1.2, yi, str(v), va="center", fontsize=8.2)
    ax.axvline(100, color=N_COLOR, linestyle="--", lw=1.3)
    ax.text(97.5, 0.0, "virial equilibrium\n(D/C = 0.5)",
            ha="right", fontsize=8.6, color=N_COLOR, va="center")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8.6)
    ax.invert_yaxis()
    ax.set_xlim(0, 108)
    ax.set_xlabel("virial balance axis score (0-100)")
    ax.set_title("The universal C-dominance gap: virial balance scores\n"
                 "measured D/C ratios fall between 0.08 and 0.32 against the "
                 "0.5 target", fontsize=10.5)
    save(fig, "10_virial-gap.png")


if __name__ == "__main__":
    fig_paradigm_plane()
    fig_ndc_mapping()
    fig_entropy_funnel()
    fig_transformer_annotated()
    fig_decision_pathways()
    fig_phase_detection()
    fig_pass_rates()
    fig_constant_roles()
    fig_health_heatmap()
    fig_virial_gap()
    print("done")
