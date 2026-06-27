#!/usr/bin/env python3
"""Generate figures for paper 17: Ostrom governance and the tholonic model."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUTDIR = Path("docnav/Research/papers/17_ostrom-tholonic-governance/figures")
OUTDIR.mkdir(parents=True, exist_ok=True)

# Canonical colors
N_DARK  = "#1d4ed8"; N_MED = "#3b82f6"; N_LIGHT = "#dbeafe"
D_DARK  = "#15803d"; D_MED = "#22c55e"; D_LIGHT = "#dcfce7"
C_DARK  = "#b91c1c"; C_MED = "#ef4444"; C_LIGHT = "#fee2e2"

# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: CPR governance tholon triangle
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 8), facecolor="white")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor("white")

N = np.array([0.5,  0.90])
C = np.array([0.05, 0.10])
D = np.array([0.95, 0.10])

tri = plt.Polygon([N, C, D], closed=True,
                  facecolor="#f8fafc", edgecolor="#94a3b8", linewidth=2)
ax.add_patch(tri)

# Vertex circles
for pt, letter, color in [(N, "N", N_MED), (C, "C", C_MED), (D, "D", D_MED)]:
    ax.add_patch(plt.Circle(pt, 0.048, color=color, zorder=5))
    ax.text(pt[0], pt[1], letter, ha="center", va="center",
            fontsize=13, fontweight="bold", color="white", zorder=6)

# Vertex labels
ax.text(N[0], N[1]+0.055,
        "Stable Governance Configuration\n(Sustainable Resource State)\nEmergent N-state",
        ha="center", va="bottom", fontsize=8.5, color=N_DARK, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=N_LIGHT, edgecolor=N_MED, lw=1))

ax.text(C[0]-0.04, C[1]-0.055,
        "Collective Participation\n& Integration\nPrinciples 3, 7, 8",
        ha="center", va="top", fontsize=8.5, color=C_DARK, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=C_LIGHT, edgecolor=C_MED, lw=1))

ax.text(D[0]+0.04, D[1]-0.055,
        "Institutional Constraints\n& Boundary Rules\nPrinciples 1, 2, 4, 5, 6",
        ha="center", va="top", fontsize=8.5, color=D_DARK, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=D_LIGHT, edgecolor=D_MED, lw=1))

# Edge annotations
center = (N + C + D) / 3

# Left edge (N-C): conatus / participation drives N
mid_NC = (N + C) / 2
ax.text(mid_NC[0]-0.14, mid_NC[1]+0.04,
        "Collective choice\nfeeds rule quality",
        ha="center", va="center", fontsize=7.5, color=C_DARK, style="italic",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9))

# Right edge (N-D): rules constrain N
mid_ND = (N + D) / 2
ax.text(mid_ND[0]+0.14, mid_ND[1]+0.04,
        "Constraints define\nwho, what, when",
        ha="center", va="center", fontsize=7.5, color=D_DARK, style="italic",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9))

# Bottom edge (C-D): tragedy / balance
mid_CD = (C + D) / 2
ax.text(mid_CD[0], mid_CD[1]-0.09,
        "D ≈ C  →  Sustainability\nD ≪ C  →  Tragedy of the Commons\nD ≫ C  →  Regulatory Collapse",
        ha="center", va="top", fontsize=7.5, color="#374151",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#f9fafb", edgecolor="#94a3b8", lw=1))

# Center label
ax.text(center[0], center[1]+0.04,
        "CPR Governance\nTholon\nB = 2·min(D,C)/(D+C)·100",
        ha="center", va="center", fontsize=8, fontweight="bold", color="#374151",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#f1f5f9", edgecolor="#94a3b8", lw=1))

ax.set_title("CPR Governance as a Tholonic System\n"
             "Ostrom's Eight Design Principles Mapped onto N, D, and C",
             fontsize=11, fontweight="bold", pad=10)

fig.savefig(OUTDIR / "17_cpr-tholon-triangle.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 17_cpr-tholon-triangle.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Design principles classification with case study scores
# ─────────────────────────────────────────────────────────────────────────────
principles = [
    "P1: Defined\nboundaries",
    "P2: Rules match\nconditions",
    "P4: Monitoring",
    "P5: Graduated\nsanctions",
    "P6: Conflict\nresolution",
    "P3: Collective\nchoice",
    "P7: External\nrecognition",
    "P8: Nested\nenterprises",
]
roles = ["D","D","D","D","D","C","C","C"]
role_colors = [D_MED]*5 + [C_MED]*3
role_dark   = [D_DARK]*5 + [C_DARK]*3

# Case study scores (0, 0.5, 1.0)
cases = {
    "Törbel, CH\n(B=100)":           [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    "Alanya, TR\n(B=71)":            [1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.5, 0.0],
    "Atlantic Groundfish\n(B=35)":   [1.0, 0.5, 1.0, 1.0, 0.5, 0.0, 0.5, 0.0],
    "Open Access\n(B≈0)":            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
}

case_names = list(cases.keys())
case_colors = [N_MED, "#0891b2", "#7c3aed", "#ef4444"]

fig, ax = plt.subplots(figsize=(13, 6), facecolor="white")
ax.set_facecolor("white")

x = np.arange(len(principles))
n_cases = len(cases)
bar_width = 0.18
offsets = np.linspace(-(n_cases-1)/2, (n_cases-1)/2, n_cases) * bar_width

for i, (case_name, scores) in enumerate(cases.items()):
    bars = ax.bar(x + offsets[i], scores, width=bar_width,
                  label=case_name, color=case_colors[i], alpha=0.85,
                  edgecolor="white", linewidth=0.5)

# Role color band behind principles
for j, (color, dark) in enumerate(zip(role_colors, role_dark)):
    ax.axvspan(j - 0.45, j + 0.45, alpha=0.08, color=color, zorder=0)

# D/C role divider
ax.axvline(4.5, color="#94a3b8", linewidth=1.5, linestyle="--")
ax.text(2.0, 1.09, "D-type Principles\n(Constraining Apparatus)",
        ha="center", va="bottom", fontsize=9, color=D_DARK, fontweight="bold")
ax.text(6.0, 1.09, "C-type Principles\n(Participatory Apparatus)",
        ha="center", va="bottom", fontsize=9, color=C_DARK, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(principles, fontsize=8.5)
ax.set_yticks([0, 0.5, 1.0])
ax.set_yticklabels(["Absent", "Partial", "Present"], fontsize=9)
ax.set_ylim(0, 1.22)
ax.set_title("Ostrom's Eight Design Principles by Tholonic Role\n"
             "Presence Scores for Four Documented Case Studies",
             fontsize=11, fontweight="bold")
ax.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
ax.spines[["top","right"]].set_visible(False)

fig.tight_layout()
fig.savefig(OUTDIR / "17_principles-classification.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 17_principles-classification.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: B-score comparison for the four case studies
# ─────────────────────────────────────────────────────────────────────────────
def bscore(d_scores, c_scores):
    d_norm = (sum(d_scores) / 5.0) * 100
    c_norm = (sum(c_scores) / 3.0) * 100
    if d_norm + c_norm == 0:
        return 0, d_norm, c_norm
    b = 2 * min(d_norm, c_norm) / (d_norm + c_norm) * 100
    return b, d_norm, c_norm

case_data = {
    "Törbel\nSwitzerland": {
        "d": [1.0, 1.0, 1.0, 1.0, 1.0],
        "c": [1.0, 1.0, 1.0],
        "color": N_MED,
        "label": "Long-run success\n(5+ centuries)",
    },
    "Alanya\nTurkey": {
        "d": [1.0, 1.0, 1.0, 0.5, 1.0],
        "c": [1.0, 0.5, 0.0],
        "color": "#0891b2",
        "label": "Functioning success\nC-deficit: weak\nexternal recognition",
    },
    "Atlantic\nGroundfish": {
        "d": [1.0, 0.5, 1.0, 1.0, 0.5],
        "c": [0.0, 0.5, 0.0],
        "color": "#7c3aed",
        "label": "D-dominant collapse\nStrong rules,\nno participation",
    },
    "Open-Access\nFishery": {
        "d": [0.0, 0.0, 0.0, 0.0, 0.0],
        "c": [0.0, 0.0, 0.0],
        "color": C_MED,
        "label": "C-dominant collapse\nTragedy of\nthe commons",
    },
}

fig, axes = plt.subplots(1, 2, figsize=(13, 6), facecolor="white",
                          gridspec_kw={"width_ratios": [1.8, 1]})

# Left: main B-score bars with D and C overlaid
ax = axes[0]
ax.set_facecolor("white")
names  = list(case_data.keys())
bs, ds, cs = [], [], []
colors = []
for name, dat in case_data.items():
    b, d, c = bscore(dat["d"], dat["c"])
    bs.append(b); ds.append(d); cs.append(c)
    colors.append(dat["color"])

x = np.arange(len(names))
ax.barh(x, bs, color=colors, alpha=0.85, edgecolor="white", height=0.5)
ax.axvline(61.8, color="#dc2626", linewidth=2, linestyle="--", label="Stability threshold (61.8)")

for i, (b, d, c, name) in enumerate(zip(bs, ds, cs, names)):
    ax.text(max(b, 3) + 1.5, i, f"B={b:.0f}  (D={d:.0f}, C={c:.0f})",
            va="center", ha="left", fontsize=8.5, color="#374151")

ax.set_yticks(x)
ax.set_yticklabels(names, fontsize=9)
ax.set_xlim(0, 130)
ax.set_xlabel("Balance Score B", fontsize=10)
ax.set_title("Tholonic Balance Score B\nfor Four CPR Governance Cases", fontsize=11, fontweight="bold")
ax.legend(loc="lower right", fontsize=8.5)
ax.spines[["top","right"]].set_visible(False)

# Right: failure mode diagram
ax2 = axes[1]
ax2.set_facecolor("white")
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10)
ax2.axis("off")
ax2.set_title("Failure Mode\nClassification", fontsize=11, fontweight="bold")

boxes = [
    (5, 8.2, "C-dominant\nPartial Tholon",
     "Tragedy of the Commons\nD≈0, C>0\nResource depletes gradually",
     C_DARK, C_LIGHT, C_MED),
    (5, 5.0, "Balanced Tholon\nB ≥ 61.8",
     "Sustainable Governance\nD ≈ C\nResource maintained",
     N_DARK, N_LIGHT, N_MED),
    (5, 1.8, "D-dominant\nPartial Tholon",
     "Regulatory Brittleness\nD>0, C≈0\nSudden collapse",
     D_DARK, D_LIGHT, D_MED),
]

for x0, y0, title, desc, ec, fc, mc in boxes:
    rect = mpatches.FancyBboxPatch((x0-4.3, y0-1.0), 8.6, 2.0,
                                   boxstyle="round,pad=0.15",
                                   facecolor=fc, edgecolor=ec, linewidth=2)
    ax2.add_patch(rect)
    ax2.text(x0, y0+0.35, title, ha="center", va="center",
             fontsize=9, fontweight="bold", color=ec)
    ax2.text(x0, y0-0.35, desc, ha="center", va="center",
             fontsize=7.5, color="#374151")

# Arrows between boxes
for y1, y2 in [(7.2, 6.0), (4.0, 2.8)]:
    ax2.annotate("", xy=(5, y2), xytext=(5, y1),
                 arrowprops=dict(arrowstyle="<->", color="#6b7280", lw=1.5))

ax2.text(5, 6.6, "D-construction →", ha="center", va="center",
         fontsize=7.5, color=D_DARK, style="italic")
ax2.text(5, 3.4, "← C-construction", ha="center", va="center",
         fontsize=7.5, color=C_DARK, style="italic")

fig.tight_layout()
fig.savefig(OUTDIR / "17_bscore-cases.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 17_bscore-cases.png")

print("All figures complete.")
