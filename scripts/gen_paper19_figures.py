#!/usr/bin/env python3
"""
Generate all six figures for Paper 19:
Phase-Resolved Sustainable Supply Chain Analysis Using a Triadic Balance
Framework: Structural Alignment with Planetary Boundaries

Run from repo root:
    python3 scripts/gen_paper19_figures.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap

FIGURES_DIR = "docnav/Research/papers/19_ndc-planetary-boundaries-supply-chain/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Canonical N-D-C colors
N_DARK  = "#1d4ed8"
N_MED   = "#3b82f6"
N_LIGHT = "#dbeafe"
D_DARK  = "#15803d"
D_MED   = "#22c55e"
D_LIGHT = "#dcfce7"
C_DARK  = "#b91c1c"
C_MED   = "#ef4444"
C_LIGHT = "#fee2e2"

FONT_BODY  = 10
FONT_SMALL = 8
FONT_TITLE = 12

# ---------------------------------------------------------------------------
# Figure 1: N-D-C triangle with Planetary Boundaries mapped to vertices
# ---------------------------------------------------------------------------
def fig1_pb_ndc_triangle():
    fig, ax = plt.subplots(figsize=(8, 7), facecolor="white")
    ax.set_facecolor("white")
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.35, 1.1)
    ax.axis("off")

    # Triangle vertices: N top, C lower-left, D lower-right
    N = np.array([0.5, 0.92])
    C = np.array([0.05, 0.08])
    D = np.array([0.95, 0.08])

    tri = plt.Polygon([N, C, D], fill=True, facecolor="#f8fafc",
                      edgecolor="#334155", linewidth=2.5, zorder=2)
    ax.add_patch(tri)

    # Vertex circles
    for pt, col, label, ha, va in [
        (N, N_DARK, "N\nNegotiation\n(Sustainable State)", "center", "bottom"),
        (C, C_DARK, "C\nContribution\n(Outputs / Flows)", "right", "top"),
        (D, D_DARK, "D\nDefinition\n(Constraints / Limits)", "left", "top"),
    ]:
        circ = plt.Circle(pt, 0.045, color=col, zorder=4)
        ax.add_patch(circ)
        offset = {"N": (0, 0.07), "C": (-0.06, -0.07), "D": (0.06, -0.07)}
        first_char = label[0]
        ox, oy = offset[first_char]
        ax.text(pt[0]+ox, pt[1]+oy, label, ha=ha, va=va,
                fontsize=FONT_BODY, fontweight="bold", color=col, zorder=5,
                linespacing=1.4)

    # D-type PB labels (green, right side of triangle near D)
    d_boundaries = [
        "Climate change\n(CO$_2$ concentration)",
        "Freshwater use\n(consumptive runoff)",
        "Land-system change\n(cropland fraction)",
        "Stratospheric ozone\n(Dobson unit floor)",
        "Novel entities\n(chemical pollution load)",
    ]
    d_x = 0.97
    d_y_start = 0.72
    ax.text(d_x, d_y_start + 0.06, "D-type boundaries\n(constraint violations)", ha="left",
            va="center", fontsize=FONT_SMALL, color=D_DARK, fontweight="bold")
    for i, b in enumerate(d_boundaries):
        ax.text(d_x, d_y_start - 0.11*i, f"• {b}", ha="left", va="center",
                fontsize=7, color=D_DARK)

    # C-type PB labels (red, left side near C)
    c_boundaries = [
        "Biosphere integrity\n(extinction rate)",
        "Biogeochemical flows\n(N and P cycle loads)",
        "Ocean acidification\n(aragonite saturation)",
        "Atmospheric aerosols\n(loading index)",
    ]
    c_x = 0.03
    c_y_start = 0.72
    ax.text(c_x, c_y_start + 0.06, "C-type boundaries\n(output violations)", ha="right",
            va="center", fontsize=FONT_SMALL, color=C_DARK, fontweight="bold")
    for i, b in enumerate(c_boundaries):
        ax.text(c_x, c_y_start - 0.12*i, f"• {b}", ha="right", va="center",
                fontsize=7, color=C_DARK)

    # Balance score label at centroid
    cx, cy = (N + C + D) / 3
    ax.text(cx, cy + 0.04, "B(D,C)", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#334155", zorder=5)
    ax.text(cx, cy - 0.05,
            r"$B = \frac{2 \cdot \min(D,C)}{D+C} \times 100$",
            ha="center", va="center", fontsize=10, color="#334155", zorder=5)
    ax.text(cx, cy - 0.16, "Stable when $B \geq 61.8$", ha="center", va="center",
            fontsize=8.5, color="#64748b", style="italic", zorder=5)

    # Edge labels
    mid_DC = (D + C) / 2
    ax.text(mid_DC[0], mid_DC[1] - 0.06, "Balance threshold ($100/\\varphi \\approx 61.8$)",
            ha="center", va="top", fontsize=7.5, color="#64748b", style="italic")

    ax.set_title("Figure 1. N-D-C Triadic Framework and Planetary Boundary Role Assignment\n"
                 "D-type boundaries constrain extraction; C-type boundaries govern output externalities.\n"
                 "The N vertex represents the sustainable operational state when $D \\approx C$.",
                 fontsize=9, pad=12, color="#1e293b", linespacing=1.5)

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "19_pb-ndc-triangle.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 2: Heat map of phase balance scores (5 chains x 8 phases)
# ---------------------------------------------------------------------------
def fig2_phase_balance_heatmap():
    chains = ["Gold", "W. African\nShea", "Cocoa\nInternational", "Spain\nOlive Oil", "Blue Carbon"]
    phases = [
        "Ph.0\nExtraction",
        "Ph.1\nAggregation",
        "Ph.2\nProcessing",
        "Ph.3\nRefining",
        "Ph.4\nFabrication",
        "Ph.5\nDistribution",
        "Ph.6\nVaulting/\nStorage",
        "Ph.7\nExchange/\nMarket",
    ]

    # Schematic balance scores (0-100); based on domain knowledge
    # Stability threshold 61.8 (= 100/phi)
    data = np.array([
        # Ph0  Ph1   Ph2   Ph3   Ph4   Ph5   Ph6   Ph7
        [28,   35,   62,   74,   70,   66,   44,   82],   # Gold
        [40,   36,   54,   61,   65,   68,   66,   70],   # Shea
        [26,   30,   56,   60,   68,   72,   70,   73],   # Cocoa
        [55,   58,   64,   70,   73,   76,   74,   78],   # Olive oil
        [44,   42,   60,   66,   70,   72,   68,   62],   # Blue carbon
    ])

    # Color map: red (low) -> yellow -> green (high)
    # Use 61.8 as mid-point
    cmap = LinearSegmentedColormap.from_list(
        "balance",
        [(0, "#ef4444"), (0.35, "#f97316"), (0.618, "#facc15"), (0.80, "#86efac"), (1.0, "#15803d")]
    )

    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor="white")
    ax.set_facecolor("white")

    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=100, aspect="auto")

    ax.set_xticks(range(len(phases)))
    ax.set_xticklabels(phases, fontsize=7.5, color="#1e293b")
    ax.set_yticks(range(len(chains)))
    ax.set_yticklabels(chains, fontsize=9, color="#1e293b")

    # Annotate cells
    for i in range(len(chains)):
        for j in range(len(phases)):
            val = data[i, j]
            txt_color = "white" if val < 45 or val > 80 else "#1e293b"
            ax.text(j, i, f"{val}", ha="center", va="center",
                    fontsize=9, fontweight="bold", color=txt_color)

    # Threshold line annotation
    cbar = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.03)
    cbar.set_label("Balance score B(D,C)", fontsize=9)
    cbar.ax.axhline(y=61.8, color="#1d4ed8", linewidth=2, linestyle="--")
    cbar.ax.text(3.5, 61.8, " 61.8\n (stability\n threshold)",
                 fontsize=7, color="#1d4ed8", va="center")

    ax.set_title(
        "Figure 2. Phase-Resolved Balance Scores Across Five Supply Chains (Schematic)\n"
        "Scores below 61.8 (blue dashed line in colorbar) indicate structurally unstable phases.\n"
        "Extraction and aggregation phases (Ph.0, Ph.1) exhibit systematic D/C imbalance across extractive commodities.",
        fontsize=9, pad=10, color="#1e293b", linespacing=1.5
    )

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "19_phase-balance-heatmap.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 3: Scatter plot - chain average balance vs. PB transgression class
# ---------------------------------------------------------------------------
def fig3_balance_vs_pb_scatter():
    # Supply chain corpus: (name, avg_balance, primary_PB_category, marker_color, imbalance_type)
    chains_data = [
        # name, avg_B, PB_x (jitter), color, imbalance
        ("Gold",               58,  0.15, C_DARK,  "D-heavy"),
        ("Gold v2",            55,  0.08, C_DARK,  "D-heavy"),
        ("Gold v3",            60,  0.22, C_DARK,  "D-heavy"),
        ("W. African Shea",    57,  1.12, D_DARK,  "D-heavy"),
        ("Burkina Faso Shea",  54,  1.08, D_DARK,  "D-heavy"),
        ("Cocoa International",52,  1.18, D_DARK,  "D-heavy"),
        ("Cocoa Netherlands",  62,  1.05, D_DARK,  "Balanced"),
        ("Senegal Agroforestry",65, 1.25, D_DARK,  "Balanced"),
        ("Spain Olive Oil",    68,  1.15, D_DARK,  "Balanced"),
        ("Gran Chaco",         50,  1.32, D_DARK,  "D-heavy"),
        ("Blue Carbon",        61,  2.10, N_DARK,  "Balanced"),
        ("Marina Alta",        67,  2.05, N_DARK,  "Balanced"),
        ("AUBEB",              63,  2.15, N_DARK,  "Balanced"),
        ("Bristol One City",   70,  2.20, N_DARK,  "C-heavy"),
        ("Grid ERCOT URI",     56,  0.42, C_DARK,  "D-heavy"),
        ("Water Jackson MS",   48,  3.12, "#7c3aed","D-heavy"),
        ("Water NewWater",     72,  3.05, "#7c3aed","Balanced"),
        ("Water OCWD",         74,  3.18, "#7c3aed","C-heavy"),
    ]

    fig, ax = plt.subplots(figsize=(9, 6), facecolor="white")
    ax.set_facecolor("white")

    # PB category positions on x-axis
    pb_categories = ["Mining /\nEnergy", "Land Use /\nAgriculture", "Ecosystem\nServices", "Freshwater\nUse"]
    ax.set_xticks([0.15, 1.15, 2.12, 3.12])
    ax.set_xticklabels(pb_categories, fontsize=9)

    # Color by imbalance type
    imbalance_colors = {"D-heavy": C_DARK, "Balanced": D_DARK, "C-heavy": N_DARK}
    imbalance_markers = {"D-heavy": "v", "Balanced": "o", "C-heavy": "^"}

    plotted = set()
    for name, avg_b, x, col, imbal in chains_data:
        marker = imbalance_markers[imbal]
        scatter_col = imbalance_colors[imbal]
        ax.scatter(x, avg_b, s=90, color=scatter_col, marker=marker,
                   alpha=0.85, zorder=4, edgecolors="white", linewidths=0.5)
        if name not in {"Gold v2", "Gold v3", "Burkina Faso Shea"}:
            ax.annotate(name, (x, avg_b), textcoords="offset points",
                        xytext=(6, 2), fontsize=6.5, color="#334155", zorder=5)
        if imbal not in plotted:
            plotted.add(imbal)

    # Threshold line
    ax.axhline(61.8, color=N_DARK, linewidth=1.5, linestyle="--", alpha=0.7, zorder=3)
    ax.text(3.35, 62.5, "Stability\nthreshold\n(61.8)", fontsize=7.5,
            color=N_DARK, va="bottom", ha="right")

    # Legend
    legend_elems = [
        mpatches.Patch(color=C_DARK, label="D-heavy imbalance (over-extraction)"),
        mpatches.Patch(color=D_DARK, label="Near-balanced (D $\\approx$ C)"),
        mpatches.Patch(color=N_DARK, label="C-heavy tendency (output-driven)"),
    ]
    ax.legend(handles=legend_elems, fontsize=8, loc="lower right", framealpha=0.9)

    ax.set_ylabel("Chain average balance score B(D,C)", fontsize=9)
    ax.set_xlabel("Primary Planetary Boundary pressure category", fontsize=9)
    ax.set_xlim(-0.3, 3.6)
    ax.set_ylim(40, 82)
    ax.grid(axis="y", alpha=0.3, linestyle=":")

    ax.set_title(
        "Figure 3. Chain Average Balance Score vs. Primary Planetary Boundary Pressure Category\n"
        "Supply chains below the 61.8 stability threshold show structural D/C imbalance\n"
        "corresponding to their primary mode of planetary boundary transgression.",
        fontsize=9, pad=10, color="#1e293b", linespacing=1.5
    )

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "19_balance-vs-pb-scatter.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 4: Five-constant axis diagnostic bar chart for 5 representative chains
# ---------------------------------------------------------------------------
def fig4_five_constant_bars():
    import math

    constants = [
        ("$\\pi$",   "Operational\nbalance",      78.5),
        ("$\\varphi$", "Value\ndistribution",      61.8),
        ("$\\sqrt{2}$","Structural\noverhead",     70.7),
        ("$\\ln 2$", "Transformation\nefficiency", 69.3),
        ("$e$",      "Financial\nalignment",       63.2),
    ]
    const_labels = [c[0] for c in constants]
    thresholds   = [c[2] for c in constants]

    # Schematic axis scores (0-100) for 5 chains
    # Higher = healthier (closer to threshold or above)
    chain_scores = {
        "Gold":            [44, 38, 52, 46, 70],
        "W. African Shea": [56, 52, 48, 55, 34],
        "Cocoa Intl.":     [50, 44, 62, 44, 40],
        "Spain Olive Oil": [67, 64, 71, 66, 44],
        "Blue Carbon":     [58, 54, 60, 64, 58],
    }

    chain_colors = [C_DARK, D_DARK, "#b45309", "#0e7490", N_DARK]
    n_chains = len(chain_scores)
    n_const  = len(constants)
    x        = np.arange(n_const)
    width    = 0.14
    offsets  = np.linspace(-(n_chains-1)/2, (n_chains-1)/2, n_chains) * width

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor="white")
    ax.set_facecolor("white")

    for i, (chain, scores) in enumerate(chain_scores.items()):
        bars = ax.bar(x + offsets[i], scores, width,
                      label=chain, color=chain_colors[i], alpha=0.85,
                      edgecolor="white", linewidth=0.5, zorder=3)

    # Threshold markers
    for j, (_, _, thresh) in enumerate(constants):
        ax.plot([j - 0.45, j + 0.45], [thresh, thresh],
                color="#1e293b", linewidth=1.5, linestyle="--", zorder=5)
        ax.text(j + 0.47, thresh, f"{thresh:.1f}", fontsize=7,
                color="#1e293b", va="center")

    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"{c[0]}\n{c[1]}" for c in constants],
        fontsize=9
    )
    ax.set_ylabel("Axis score (0-100, higher = healthier)", fontsize=9)
    ax.set_ylim(0, 95)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.9)
    ax.grid(axis="y", alpha=0.3, linestyle=":")

    ax.set_title(
        "Figure 4. Five-Constant Diagnostic Axis Scores for Five Representative Supply Chains\n"
        "Dashed lines show sustainability thresholds derived from each mathematical constant.\n"
        "All chains fall below $\\pi$-threshold for operational balance; gold and cocoa show severe $\\varphi$ failure (trapped value).",
        fontsize=9, pad=10, color="#1e293b", linespacing=1.5
    )

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "19_five-constant-bars.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 5: Supply chain phase DAG with PB pressure annotations
# ---------------------------------------------------------------------------
def fig5_supply_chain_dag():
    fig, ax = plt.subplots(figsize=(13, 4.8), facecolor="white")
    ax.set_facecolor("white")
    ax.axis("off")

    phases = [
        (0, "Phase 0\nExtraction /\nOrigin",      "D-heavy",  ["Climate", "Land use", "Biodiversity"]),
        (1, "Phase 1\nAggregation /\nCollection",  "D-heavy",  ["Land use", "Freshwater"]),
        (2, "Phase 2\nProcessing /\nTransform.",   "Moderate", ["Freshwater", "N/P cycles"]),
        (3, "Phase 3\nRefining /\nPurification",   "Moderate", ["Chemical", "pollution"]),
        (4, "Phase 4\nFabrication /\nValue-add",   "Balanced", ["Chemical", "pollution"]),
        (5, "Phase 5\nDistribution /\nLogistics",  "Balanced", ["Climate", "(transport)"]),
        (6, "Phase 6\nVaulting /\nStorage",        "Low-vis",  ["(Opaque)"]),
        (7, "Phase 7\nExchange /\nMarket",          "C-heavy",  ["Financial", "entities"]),
    ]

    health_color = {
        "D-heavy":  C_LIGHT,
        "Moderate": "#fef9c3",
        "Balanced": D_LIGHT,
        "Low-vis":  "#f1f5f9",
        "C-heavy":  N_LIGHT,
    }
    border_color = {
        "D-heavy":  C_DARK,
        "Moderate": "#b45309",
        "Balanced": D_DARK,
        "Low-vis":  "#94a3b8",
        "C-heavy":  N_DARK,
    }

    n = len(phases)
    # Normalised x positions 0..1
    xs = np.linspace(0.04, 0.96, n)
    box_w_norm = 0.09   # in axes fraction
    box_h_norm = 0.42   # in axes fraction
    box_y      = 0.32   # bottom of box in axes fraction
    arrow_y    = box_y + box_h_norm / 2
    pb_y       = box_y - 0.04  # top of PB text block

    for i, (_, label, health, pbs) in enumerate(phases):
        x = xs[i]
        fc = health_color[health]
        ec = border_color[health]

        # Box using axes fraction coordinates via transAxes
        rect = mpatches.FancyBboxPatch(
            (x - box_w_norm/2, box_y), box_w_norm, box_h_norm,
            boxstyle="round,pad=0.01",
            facecolor=fc, edgecolor=ec, linewidth=2.0, zorder=3,
            transform=ax.transAxes, clip_on=False
        )
        ax.add_patch(rect)

        # Phase label inside box
        ax.text(x, box_y + box_h_norm/2, label,
                ha="center", va="center", fontsize=7.2,
                color="#1e293b", fontweight="bold", linespacing=1.35,
                transform=ax.transAxes, zorder=4)

        # PB annotations below box
        pb_str = "\n".join(pbs)
        ax.text(x, pb_y, pb_str,
                ha="center", va="top", fontsize=6.5, color=ec,
                linespacing=1.3, transform=ax.transAxes, zorder=4)

        # Arrow to next phase
        if i < n - 1:
            x_right = x + box_w_norm/2
            x_next_left = xs[i+1] - box_w_norm/2
            ax.annotate("",
                xy=(x_next_left, arrow_y), xytext=(x_right, arrow_y),
                xycoords=ax.transAxes, textcoords=ax.transAxes,
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.4),
                zorder=5)

    # Section header at top of figure
    ax.text(0.5, 0.97, "PRIMARY PLANETARY BOUNDARY PRESSURE ZONES",
            ha="center", va="top", fontsize=9, fontweight="bold",
            color="#334155", transform=ax.transAxes)

    # Legend inside the axes
    legend_items = [
        mpatches.Patch(facecolor=C_LIGHT, edgecolor=C_DARK, label="D-heavy (extraction stress)"),
        mpatches.Patch(facecolor="#fef9c3", edgecolor="#b45309", label="Moderate imbalance"),
        mpatches.Patch(facecolor=D_LIGHT, edgecolor=D_DARK, label="Balanced (D \u2248 C)"),
        mpatches.Patch(facecolor="#f1f5f9", edgecolor="#94a3b8", label="Low visibility"),
        mpatches.Patch(facecolor=N_LIGHT, edgecolor=N_DARK, label="C-heavy (output stress)"),
    ]
    ax.legend(handles=legend_items, fontsize=7.5, loc="upper right",
              bbox_to_anchor=(1.0, 0.96), framealpha=0.95)

    ax.set_title(
        "Figure 5. Eight-Phase Supply Chain DAG with Planetary Boundary Pressure Annotations\n"
        "Phase coloring reflects N-D-C structural balance. PB annotations indicate which boundaries are primarily stressed at each phase.\n"
        "Extraction and aggregation phases carry the heaviest D-heavy imbalance and are responsible for the majority of boundary transgressions.",
        fontsize=9, pad=8, color="#1e293b", linespacing=1.5
    )

    path = os.path.join(FIGURES_DIR, "19_supply-chain-dag.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 6: Research timeline 2016-2026 (supply chains added per period)
# ---------------------------------------------------------------------------
def fig6_research_timeline():
    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor="white")
    ax.set_facecolor("white")

    # Timeline milestones
    events = [
        (2016.0, "Conceptual\nframework\ndeveloped", N_DARK,   0.85),
        (2017.5, "Gold supply\nchain\n(prototype)", C_DARK,   0.55),
        (2019.0, "W. African\nShea; Cocoa\nInternational", D_DARK, 0.85),
        (2020.5, "TVPCI\nformalized;\nOlive Oil", D_DARK,    0.55),
        (2021.5, "Gran Chaco;\nSenegal\nAgroforestry", D_DARK, 0.85),
        (2022.5, "Water\ncorpus (3);\nBlue Carbon", N_DARK,   0.55),
        (2023.5, "Grid ERCOT;\nBristol;\nMarina Alta", N_DARK, 0.85),
        (2024.5, "AUBEB;\nGold v2/v3\nrefinements", C_DARK,   0.55),
        (2025.5, "N-D-C / PB\nintegration\ntheory", N_DARK,   0.85),
        (2026.5, "Paper 19\nfirst draft\n(this work)", "#7c3aed", 0.55),
    ]

    # Cumulative supply chain count
    cumulative = [1, 2, 4, 6, 8, 11, 14, 16, 18, 18]
    years_c    = [e[0] for e in events]

    # Background timeline bar
    ax.barh(0.0, 12, left=2015.5, height=0.08, color="#e2e8f0", zorder=1)
    ax.axhline(0.0, color="#94a3b8", linewidth=1.5, xmin=0, xmax=1, zorder=2)

    # Cumulative count line (right axis)
    ax2 = ax.twinx()
    ax2.plot(years_c, cumulative, color="#94a3b8", linewidth=1.5,
             linestyle=":", zorder=2, marker="s", markersize=4)
    ax2.set_ylabel("Cumulative supply chains analyzed", fontsize=8.5, color="#64748b")
    ax2.set_ylim(0, 22)
    ax2.tick_params(axis="y", labelcolor="#64748b", labelsize=8)

    # Event markers
    for (yr, label, col, ypos) in events:
        ax.plot([yr, yr], [0, ypos - 0.05], color=col, linewidth=1.2,
                linestyle="-", alpha=0.6, zorder=3)
        ax.scatter(yr, 0, s=60, color=col, zorder=5, edgecolors="white", linewidths=0.8)
        ax.text(yr, ypos, label, ha="center", va="bottom",
                fontsize=7, color=col, linespacing=1.35)

    ax.set_xlim(2015, 2027.5)
    ax.set_ylim(-0.3, 1.3)
    ax.set_xticks(range(2016, 2027))
    ax.set_xticklabels([str(y) for y in range(2016, 2027)], fontsize=8.5)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.set_title(
        "Figure 6. Research Trajectory 2016-2026: Supply Chain Corpus Development\n"
        "Dotted line (right axis) shows cumulative supply chains analyzed. Color coding matches N-D-C framework roles\n"
        "(blue = structural/theory milestones; green = land-use chains; red = extractive chains; purple = synthesis work).",
        fontsize=9, pad=10, color="#1e293b", linespacing=1.5
    )

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "19_research-timeline.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {path}")


if __name__ == "__main__":
    print("Generating Paper 19 figures...")
    fig1_pb_ndc_triangle()
    fig2_phase_balance_heatmap()
    fig3_balance_vs_pb_scatter()
    fig4_five_constant_bars()
    fig5_supply_chain_dag()
    fig6_research_timeline()
    print("Done. All figures saved to:", FIGURES_DIR)
