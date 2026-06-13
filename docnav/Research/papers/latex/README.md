# LaTeX exports (Pandoc)

These `.tex` files were generated from Markdown with [Pandoc](https://pandoc.org/). Source files:

| LaTeX | Source |
|-------|--------|
| `2_supply-chain-transparency-tvpci.tex` | `../2_supply-chain-transparency-tvpci.md` |
| `6_qualitative-nature-integers-triadic-roles.tex` | `../6_qualitative-nature-integers-triadic-roles.md` (canonical `.tex` lives in the paper folder, see below) |
| `tvpci-r_recycling_integration_plan.tex` | `.cursor/plans/tvpci-r_recycling_integration_950c5fee.plan.md` (repo copy may differ; regenerate from your plan file if needed) |

## Paper 6 canonical path

The qualitative-integers paper is maintained as:

- `../6_qualitative-nature-integers-triadic-roles/6_qualitative-nature-integers-triadic-roles.tex`

Regenerate it with Pandoc plus `scripts/pandoc_paper_postprocess.py` using the **`research-paper-latex`** skill (`.cursor/skills/research-paper-latex/SKILL.md`).

Build the PDF like papers 1 to 5: from the **repository root**, run `./scripts/research_paper_pdflatex.sh docnav/Research/papers/6_qualitative-nature-integers-triadic-roles` (two-pass `pdflatex`). Or run `pdflatex` twice by hand in the paper folder.

## Build

From this directory (`docnav/Research/papers/latex/`):

```bash
pdflatex -interaction=nonstopmode 2_supply-chain-transparency-tvpci.tex
pdflatex -interaction=nonstopmode tvpci-r_recycling_integration_plan.tex
```

From the paper 6 folder (`docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/`):

```bash
pdflatex -interaction=nonstopmode 6_qualitative-nature-integers-triadic-roles.tex
```

Paper 2 figures: `\graphicspath{{../figures/}}` expects PNG assets under `docnav/Research/papers/figures/` (same layout as the Markdown figure checklist). Missing files produce compile warnings but the document still builds.

## Regenerate from Markdown

```bash
cd docnav/Research/papers
pandoc 2_supply-chain-transparency-tvpci.md -o latex/2_supply-chain-transparency-tvpci.tex --standalone \
  -V documentclass=article -V papersize=letter -V geometry=margin=1in -V fontsize=11pt
```

Re-apply post-processing if needed: section numbering (`\setcounter{secnumdepth}{5}`), `\graphicspath`, and figure paths without the redundant `figures/` prefix for paper 2.

The integration plan in `.cursor/plans/` may be outside the git tree; copy it into the repo or point Pandoc at its path when regenerating.
