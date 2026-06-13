#!/usr/bin/env python3
"""Regenerate figures/1_traversal-classes.png with full right margin.

The original asset clipped the rightmost ln2 branch at the canvas edge.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse

OUT = Path("docnav/Research/papers/figures/1_traversal-classes.png")

CLASS_A = "#c2542b"
CLASS_B = "#1f5fa8"
CLASS_C = "#3c8a4e"
ROOT = "#2b3a55"
GREY = "#888888"


def rounded_box(ax, xy, w, h, text, face, text_color="white", fontsize=11, bold=True):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08,rounding_size=0.08",
        facecolor=face, edgecolor="black", linewidth=0.8,
    )
    ax.add_patch(patch)
    weight = "bold" if bold else "normal"
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=text_color, fontweight=weight, zorder=3)


def branch_oval(ax, xy, w, h, title, lines, edge, face):
    x, y = xy
    ell = Ellipse((x + w / 2, y + h / 2), w, h,
                  facecolor=face, edgecolor=edge, linewidth=1.6, zorder=2)
    ax.add_patch(ell)
    ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=edge, zorder=3)
    ax.text(x + w / 2, y + h * 0.28, "\n".join(lines), ha="center", va="center",
            fontsize=8.6, color="#333333", linespacing=1.35, zorder=3)


def main():
    fig, ax = plt.subplots(figsize=(13.5, 5.8))
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 5.8)
    ax.axis("off")

    # Root
    rounded_box(ax, (5.35, 4.85), 2.8, 0.55, "Tholonic Ladder", ROOT, fontsize=12)

    # Class row
    classes = [
        (0.55, 3.75, 3.6, 0.55, "Class A\nAdvancing", CLASS_A),
        (4.95, 3.75, 3.6, 0.55, "Class B\nSelf-redefined", CLASS_B),
        (9.35, 3.75, 3.6, 0.55, "Class C\nFixed", CLASS_C),
    ]
    for x, y, w, h, label, color in classes:
        rounded_box(ax, (x, y), w, h, label, color)

    # Connectors root -> classes
    for cx in [2.35, 6.75, 11.15]:
        ax.plot([6.75, cx], [4.85, 4.4], color=GREY, lw=1.2, zorder=1)
        ax.plot([cx, cx], [4.4, 4.3], color=GREY, lw=1.2, zorder=1)

    # Branches (five ovals, spaced to fit)
    branches = [
        ((0.35, 1.55), 2.15, 1.55, r"$\pi/4$",
         ["Seeds: {1, 3, 5}", "Step +4 each iteration", "(external)"],
         CLASS_A, "#f7e0d8"),
        ((2.35, 1.55), 2.15, 1.55, r"$\varphi$ (golden ratio)",
         ["Seeds: {1, 2}", "Fibonacci swap of D, C"],
         CLASS_B, "#d8e4f7"),
        ((4.85, 1.55), 2.15, 1.55, r"$e$ (Euler)",
         ["Seeds: {0, 1}", "Factorial growth of D"],
         CLASS_B, "#d8e4f7"),
        ((7.35, 1.55), 2.15, 1.55, r"$\sqrt{2}$",
         ["Seeds: {1, 2}", r"$D = C = 2$ fixed"],
         CLASS_C, "#d8f0dc"),
        ((9.85, 1.55), 2.15, 1.55, r"$\ln 2$",
         ["Seeds: {0, 1}", r"$D = C = 1$ fixed"],
         CLASS_C, "#d8f0dc"),
    ]
    for args in branches:
        branch_oval(ax, *args)

    # Class -> branch connectors
    ax.plot([2.35, 2.35], [3.75, 3.1], color=GREY, lw=1.0)
    ax.plot([6.75, 3.4], [3.75, 3.1], color=GREY, lw=1.0)
    ax.plot([6.75, 5.9], [3.75, 3.1], color=GREY, lw=1.0)
    ax.plot([11.15, 8.4], [3.75, 3.1], color=GREY, lw=1.0)
    ax.plot([11.15, 10.9], [3.75, 3.1], color=GREY, lw=1.0)

    # Bottom descriptor bars (non-overlapping)
    desc = [
        (0.35, 0.55, 2.15, 0.42, "Injects new information\neach iteration", CLASS_A),
        (2.35, 0.55, 2.15, 0.42, "Parameters transform\nthrough internal rules", CLASS_B),
        (4.85, 0.55, 2.15, 0.42, "Factorial growth\n(endogenous)", CLASS_B),
        (7.35, 0.55, 2.15, 0.42, "Parameters held\nconstant throughout", CLASS_C),
        (9.85, 0.55, 2.15, 0.42, "Iteration index drives\nconvergence", CLASS_C),
    ]
    for x, y, w, h, text, color in desc:
        rounded_box(ax, (x, y), w, h, text, color, fontsize=8.2, bold=False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight", pad_inches=0.35, facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
