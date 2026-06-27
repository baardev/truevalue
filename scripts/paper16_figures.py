#!/usr/bin/env python3
"""Generate figures for paper 16: Tholonic model vs. Spinoza and Leibniz."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
from pathlib import Path

OUTDIR = Path("docnav/Research/papers/16_tholonic-spinoza-leibniz/figures")
OUTDIR.mkdir(parents=True, exist_ok=True)

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

# Triangle vertices: N top, C lower-left, D lower-right
def triangle_vertices():
    N = np.array([0.5,  0.90])
    C = np.array([0.05, 0.10])
    D = np.array([0.95, 0.10])
    return N, C, D


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: Two-panel triangle — Spinoza and Leibniz mappings
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor="white")
fig.suptitle(
    "Tholonic N-D-C Framework: Spinoza and Leibniz Structural Mappings",
    fontsize=13, fontweight="bold", y=1.01
)

panel_data = [
    {
        "title": "Spinoza's Ethics\nMapped onto N-D-C",
        "N_label": "Substance\n(Deus sive Natura)\nSelf-subsisting ground",
        "D_label": "Attribute of Thought\n(Cogitatio)\nDefinition / constraint\nNatura naturans",
        "C_label": "Attribute of Extension\n(Extensio)\nContribution / expression\nNatura naturata",
        "edge_NC": "Conatus: each mode\nstrives to persevere\nin N",
        "edge_ND": "Mode depends on\nsubstance for existence\nand intelligibility",
        "edge_DC": "Parallelism: same\nordre in Thought\nand Extension",
        "center": "Finite Mode\n(Child N)\ninstantiated",
    },
    {
        "title": "Leibniz's Monadology\nMapped onto N-D-C",
        "N_label": "Dominant Monad\n(Entelechy / N-state)\nSelf-sustaining unit",
        "D_label": "Monad's Internal Law\n(confining structure)\nDefinition / constraint\nof perception",
        "C_label": "Mirroring / Expression\n(perceptio)\nContribution: monad\nreflects universe",
        "edge_NC": "Entelechy: internal\nprinciple drives\nN coherence",
        "edge_ND": "Hierarchy: dominant\nmonad organises\nsubordinate monads",
        "edge_DC": "Pre-established\nharmony: D and C\ncoordinated structurally",
        "center": "Child Monad\n(Child N)\ncoherent unit",
    },
]

for ax, pd in zip(axes, panel_data):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("white")

    N, C, D = triangle_vertices()

    # Draw filled triangle
    tri = plt.Polygon([N, C, D], closed=True,
                      facecolor="#f8fafc", edgecolor="#94a3b8", linewidth=2)
    ax.add_patch(tri)

    # Edge midpoints for annotations
    mid_NC = (N + C) / 2
    mid_ND = (N + D) / 2
    mid_CD = (C + D) / 2

    # Edge labels
    for midpt, txt, offset, color in [
        (mid_NC, pd["edge_NC"], (-0.22, 0.0),  N_DARK),
        (mid_ND, pd["edge_ND"], ( 0.09, 0.0),  D_DARK),
        (mid_CD, pd["edge_DC"], ( 0.0, -0.13), "#4b5563"),
    ]:
        ax.text(midpt[0] + offset[0], midpt[1] + offset[1], txt,
                ha="center", va="center", fontsize=7,
                color=color, style="italic",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="none", alpha=0.85))

    # Center label (Child N)
    center = (N + C + D) / 3
    center_y = center[1] + 0.04
    ax.text(center[0], center_y, pd["center"],
            ha="center", va="center", fontsize=8, fontweight="bold",
            color="#374151",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f1f5f9",
                      edgecolor="#94a3b8", linewidth=1))

    # Vertex circles and labels
    for pt, label, color, lcolor, va, ha, offset in [
        (N, pd["N_label"], N_MED, N_DARK, "bottom", "center", (0, 0.04)),
        (C, pd["C_label"], C_MED, C_DARK, "top",    "right",  (-0.03, -0.03)),
        (D, pd["D_label"], D_MED, D_DARK, "top",    "left",   (0.03, -0.03)),
    ]:
        circle = plt.Circle(pt, 0.045, color=color, zorder=5)
        ax.add_patch(circle)
        rname = label.split("\n")[0]
        ax.text(pt[0], pt[1], rname[0],  # N / C / D single letter
                ha="center", va="center", fontsize=12, fontweight="bold",
                color="white", zorder=6)
        ax.text(pt[0] + offset[0], pt[1] + offset[1], label,
                ha=ha, va=va, fontsize=7.5, color=lcolor,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=color, linewidth=1, alpha=0.92))

    ax.set_title(pd["title"], fontsize=10, fontweight="bold",
                 color="#111827", pad=8)

plt.tight_layout()
fig.savefig(OUTDIR / "16_philosopher-ndc-triangles.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 16_philosopher-ndc-triangles.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Hierarchical nesting — monad hierarchy vs. tholonic hierarchy
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 8), facecolor="white")
fig.suptitle(
    "Monad Hierarchy (Leibniz) vs. Tholonic N-D-C Hierarchy",
    fontsize=13, fontweight="bold"
)

# ── left panel: Leibniz monad hierarchy ──────────────────────────────────────
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis("off")
ax.set_facecolor("white")
ax.set_title("Leibniz: Monad Hierarchy", fontsize=11, fontweight="bold")

levels_l = [
    (5.0, 10.5, "God (Supreme Monad)\nInfinite, all perceptions distinct",
     "#7c3aed", "#ede9fe", 3.0),
    (5.0,  8.0, "Rational Soul (Spirit)\nApperception, reason, distinct perception",
     N_DARK,  N_LIGHT, 2.5),
    (5.0,  5.5, "Soul (Animal Monad)\nSentience, memory, partial clarity",
     "#0891b2", "#e0f2fe", 2.5),
    (5.0,  3.0, "Bare Monad (Entelechy)\nConfused, indistinct perception",
     "#64748b", "#f1f5f9", 2.5),
]

for (x, y, lbl, ec, fc, w) in levels_l:
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - 0.55), w, 1.1,
        boxstyle="round,pad=0.1",
        facecolor=fc, edgecolor=ec, linewidth=2, zorder=3
    )
    ax.add_patch(rect)
    ax.text(x, y, lbl, ha="center", va="center",
            fontsize=8, color=ec, fontweight="bold", zorder=4)

# Arrows
for (_, y1, *_), (_, y2, *_) in zip(levels_l[:-1], levels_l[1:]):
    ax.annotate("", xy=(5.0, y2 + 0.56), xytext=(5.0, y1 - 0.56),
                arrowprops=dict(arrowstyle="-|>", color="#6b7280", lw=1.5))

ax.text(5.0, 1.2,
        "Pre-established harmony:\nall levels coordinated\nby divine design",
        ha="center", va="center", fontsize=8, color="#6b7280",
        style="italic",
        bbox=dict(boxstyle="round", facecolor="#f9fafb", edgecolor="#d1d5db"))

# ── right panel: tholonic hierarchy ──────────────────────────────────────────
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis("off")
ax.set_facecolor("white")
ax.set_title("Tholonic Model: N-D-C Recursive Hierarchy", fontsize=11, fontweight="bold")

levels_t = [
    (5.0, 10.5, "Parent N\n(Level k+1)\nHighest coherence at this scope",
     N_DARK, N_LIGHT, 3.2),
    (3.0,  7.8, "D Component\n(Definition)\nConstraint, boundary,\nspecification",
     D_DARK, D_LIGHT, 2.6),
    (7.0,  7.8, "C Component\n(Contribution)\nExpression, output,\nconnection",
     C_DARK, C_LIGHT, 2.6),
    (5.0,  5.0, "Child N\n(Level k)\nEmergent equilibrium\nof D and C",
     N_DARK, N_LIGHT, 3.2),
    (5.0,  2.2, "Child N becomes\nnext Parent N\n(Level k-1, recursion continues)",
     "#7c3aed", "#ede9fe", 3.5),
]

for (x, y, lbl, ec, fc, w) in levels_t:
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - 0.62), w, 1.24,
        boxstyle="round,pad=0.1",
        facecolor=fc, edgecolor=ec, linewidth=2, zorder=3
    )
    ax.add_patch(rect)
    ax.text(x, y, lbl, ha="center", va="center",
            fontsize=8, color=ec, fontweight="bold", zorder=4)

# Arrows: parent N -> D and C
for tx, ty in [(3.0, 7.8), (7.0, 7.8)]:
    ax.annotate("", xy=(tx, ty + 0.63), xytext=(5.0, 10.5 - 0.63),
                arrowprops=dict(arrowstyle="-|>", color="#6b7280", lw=1.5))

# D+C -> child N
for tx, ty in [(3.0, 7.8), (7.0, 7.8)]:
    ax.annotate("", xy=(5.0, 5.0 + 0.63), xytext=(tx, ty - 0.63),
                arrowprops=dict(arrowstyle="-|>", color="#6b7280", lw=1.5))

# Child N -> next level
ax.annotate("", xy=(5.0, 2.2 + 0.63), xytext=(5.0, 5.0 - 0.63),
            arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2,
                            linestyle="dashed"))

# Balance label
ax.text(5.0, 6.4, "$D \\approx C$\n$B \\geq 61.8$",
        ha="center", va="center", fontsize=9, color="#374151",
        bbox=dict(boxstyle="round", facecolor="#f9fafb", edgecolor="#94a3b8"))

plt.tight_layout()
fig.savefig(OUTDIR / "16_monad-tholon-hierarchy.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 16_monad-tholon-hierarchy.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: Concept alignment heatmap
# ─────────────────────────────────────────────────────────────────────────────
philosophers = ["Spinoza", "Leibniz"]

tholonic_primitives = [
    "N-state\n(emergent\nequilibrium)",
    "D\n(constraint)",
    "C\n(expression)",
    "Tholon\n(self-contained\nunit)",
    "Parent-N\nrecursion",
    "D-C balance\ncondition",
    "Self-similarity\nacross levels",
    "Structural\nself-maintenance",
    "Failure mode\n(N dissolves)",
    "Mathematical\ngrounding",
]

# Alignment scores 0-3: 0=none, 1=partial, 2=close, 3=precise
spinoza_scores = [2, 2, 2, 1, 3, 2, 1, 3, 2, 1]
leibniz_scores = [3, 2, 2, 3, 2, 3, 3, 2, 2, 3]

data = np.array([spinoza_scores, leibniz_scores], dtype=float)

fig, ax = plt.subplots(figsize=(13, 5), facecolor="white")
ax.set_facecolor("white")

cmap = plt.cm.RdYlGn
im = ax.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=3)

ax.set_xticks(range(len(tholonic_primitives)))
ax.set_xticklabels(tholonic_primitives, fontsize=8.5, ha="center")
ax.set_yticks(range(len(philosophers)))
ax.set_yticklabels(philosophers, fontsize=11, fontweight="bold")

# Annotate cells
labels = ["None", "Partial", "Close", "Precise"]
for i in range(len(philosophers)):
    for j in range(len(tholonic_primitives)):
        score = int(data[i, j])
        ax.text(j, i, labels[score],
                ha="center", va="center", fontsize=8.5, fontweight="bold",
                color="white" if score >= 2 else "#374151")

ax.set_title(
    "Structural Alignment: Spinoza and Leibniz with Tholonic Primitives",
    fontsize=12, fontweight="bold", pad=12
)

# Color bar
cbar = fig.colorbar(im, ax=ax, orientation="vertical", fraction=0.02, pad=0.02)
cbar.set_ticks([0, 1, 2, 3])
cbar.set_ticklabels(["None", "Partial", "Close", "Precise"])
cbar.ax.tick_params(labelsize=8)

plt.tight_layout()
fig.savefig(OUTDIR / "16_concept-alignment-heatmap.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 16_concept-alignment-heatmap.png")

print("All figures complete.")
