---
name: create-research-paper
description: Create a new research paper in docnav/Research/papers/ with the correct canonical format: title, author, version, date, keywords, abstract, and numbered sections. Use when the user says "create a paper", "write a paper", "make this a paper", "add a new paper", or asks to turn a notes file or discovery into a formal research paper.
---

# Create Research Paper

All papers live as `docnav/Research/papers/<N>_<slug>.md` where `<N>` is the next available integer.

## Step 1: Determine the next paper number

```bash
ls docnav/Research/papers/*.md | grep -oP '^\d+' | sort -n | tail -1
```

Increment by 1 to get the new paper number.

## Step 2: Choose a slug

Lowercase, hyphen-separated, descriptive. Examples:
- `tholonic-constant-sweep-discoveries`
- `supply-chain-phase-transitions`

File name: `docnav/Research/papers/<N>_<slug>.md`

## Step 3: Apply the canonical header

Every paper must open with exactly this block (fill in the bracketed fields):

```markdown
# [Full descriptive title of the paper]

**Author:** J. W. Milton, Clarity Coalition

**Version:** 1.0

**Date:** [D Month YYYY — e.g., "8 June 2026"]

**Keywords:** term1; term2; term3
```

**Keywords** are required. Use semicolon-separated topical terms suitable for any preprint repository (SSRN, Zenodo, institutional archive, etc.). Do not name a specific repository or use repository-specific subject-classification codes.

Close the header block with a `---` divider.

## Step 4: Write the Abstract

```markdown
## Abstract

[Paragraph prose. State: what the paper does, the core result or contribution, what the paper does NOT claim, and any explicit scope limits. One to three paragraphs. No section number on Abstract.]

---
```

Close with another `---` divider.

## Step 5: Number every section

Sections use `## N. Title` format:

```markdown
## 1. Introduction

## 2. Background

## 3. ...
```

Subsections: `### N.M Title`

Sub-subsections: `#### N.M.K Title`

**No unnumbered body sections.** The only unnumbered headings allowed are `## Abstract`, `## References`, and `## Appendix [Letter]. Title`.

## Step 6: Introduction structure

The Introduction should include clearly labelled paragraphs (bold inline, not sub-headings) for:

- **What this paper provides.** (concrete deliverables)
- **What this paper does not provide.** (explicit scope exclusions)
- **Organization.** (§N covers X, §M covers Y, ...)

## Step 7: References

End with an unnumbered references section using inline citation keys in `[AuthYY]` format:

```markdown
## References

[AuthYY] Author, A. *Title.* Publisher, Year.
```

**In-series paper URLs:** `docnav/Research/papers/github_pdf_urls.md` holds the canonical GitHub URLs for every paper PDF. When citing another paper in this series (in the References section or in prose), link citation keys and plain `paper N` / `Paper N` text to the **Direct download** URL from that file:

```markdown
[Mil26a](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) Milton, J. W. ...

Prior work in [paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) establishes ...
```

Use `github.com/.../raw/main/...` only. Do not use `raw.githubusercontent.com`. When adding a new paper, add its URLs to `github_pdf_urls.md` first. See `.cursor/rules/research-paper-references.mdc` for the full convention.

## Step 8: Cross-references to other papers in the series

Cite other papers in the series as `paper N` or `[Mil26N]` in the text. **Both forms must link to the PDF** using URLs from `github_pdf_urls.md` (see Step 7). Citation keys are not global: `[Mil26a]` may denote different paper numbers in different files; always match the URL to that file's References mapping.

## Step 9: Generate figures when helpful or necessary

Figures are expected whenever the paper:

- Maps N, D, or C roles onto a system (generate a triangle diagram with the canonical layout: N blue top, C red lower-left, D green lower-right)
- Shows quantitative relationships, balance scores, or time series
- Compares multiple phases, domains, or conditions side by side
- Has an appendix with computed results (bar charts, scatter plots, heatmaps)

**When to generate (required):** any paper that makes a quantitative claim without a supporting figure is incomplete. Generate the figure before writing the caption, not after.

**Figure naming convention:** `<N>_<short-descriptor>.png`, stored in `docnav/Research/papers/<N>_<slug>/figures/`. For example: `14_ndc-cancer-triangle.png`, `14_d-collapse-grades.png`.

**Embed in Markdown** immediately after the relevant paragraph using an **absolute path**:

```markdown
![Caption text.](/home/jw/src/tv/docnav/Research/papers/14_cancer-d-collapse/figures/14_ndc-cancer-triangle.png)
```

Absolute paths are required so the IDE Markdown preview renders the figure regardless of where the `.md` file sits relative to the figures folder. The postprocessor (`scripts/pandoc_paper_postprocess.py`) automatically converts absolute paths to the correct relative path inside the output `.tex` before running `pdflatex`. Never use relative paths like `figures/14_foo.png` or `14_cancer-d-collapse/figures/14_foo.png` in the Markdown source.

**Style rules (non-negotiable):**
- White background. Papers print on white; transparent or dark backgrounds render as black rectangles in PDF.
- N role: blue (`#1d4ed8` dark, `#3b82f6` medium). D role: green (`#15803d` dark, `#22c55e` medium). C role: red (`#b91c1c` dark, `#ef4444` medium).
- In all triangle diagrams: N at top, C lower-left, D lower-right. Do not rotate or mirror.
- Labels match role colors (blue text for N labels, green for D, red for C).
- Axis titles and tick labels in black or dark gray for readability.
- Figures must be self-explanatory: title, axis labels, and legend (if needed) included in the image.

**Figure types by paper section:**

| Section content | Recommended figure type |
|---|---|
| N-D-C role mapping for a new domain | Triangle diagram with domain labels at each vertex |
| Balance scores across phases or conditions | Horizontal bar chart, color-coded by role or health |
| D-collapse or C-runaway trajectory | Line plot showing D, C, and N over time or progression |
| Comparison across multiple domains or datasets | Grouped bar chart or heatmap |
| Quantitative proxy data (e.g. soil carbon vs. microbial biomass) | Scatter plot with B-score contour overlay |

**Before building the PDF:** ensure every `figures/` reference in the Markdown resolves. The build script creates `<paper-dir>/figures -> ../figures` automatically when figures are in the shared pool; place paper-specific figures in `<N>_<slug>/figures/` directly.

## Step 10: Build LaTeX and PDF

After the Markdown is complete, run the full build pipeline (Pandoc → postprocessor → pdflatex). Always pass `--md` to the postprocessor so it reads the header fields automatically:

```bash
cd docnav/Research/papers
pandoc <N>_<slug>.md -o latex/_paper<N>_pandoc_raw.tex \
  --standalone -V documentclass=article -V papersize=letter \
  -V geometry=margin=1in -V fontsize=11pt

cd /path/to/repo/root
python3 scripts/pandoc_paper_postprocess.py \
  docnav/Research/papers/latex/_paper<N>_pandoc_raw.tex \
  docnav/Research/papers/<N>_<slug>/<N>_<slug>.tex \
  --md docnav/Research/papers/<N>_<slug>.md

./scripts/research_paper_pdflatex.sh docnav/Research/papers/<N>_<slug>
```

**Title page format (enforced by the postprocessor when `--md` is used):**
- Author: `Name` on one line, affiliation in small type below (split on the first `, ` in the Author field)
- Date: small font
- Version: small font, on a separate line below the date (e.g. `8 June 2026` / `v1.1`)
- Keywords appear as a bold `\noindent` line immediately after `\maketitle` when present in the Markdown header

Do not manually edit `\date{}`, `\author{}`, or the Keywords line in the `.tex` — regenerate from `--md` instead.

## Canonical header example

```markdown
# Seed-Space Convergence Hierarchy of Classical Constants Under Tholonic Recursion

**Author:** J. W. Milton, Clarity Coalition

**Version:** 1.0

**Date:** 8 June 2026

**Keywords:** tholonic model; classical constants; seed-space sweep; convergence hierarchy; golden ratio; power of two

---

## Abstract

...

---

## 1. Introduction
```

## Checklist before handing off to research-paper-latex

- [ ] File saved as `docnav/Research/papers/<N>_<slug>.md`
- [ ] Header has Author, Version, Date, Keywords
- [ ] `---` divider after header block and after Abstract
- [ ] All body sections numbered (`## 1.`, `## 2.`, ...)
- [ ] Introduction contains "What this paper provides / does not provide / Organization"
- [ ] References section present (even if minimal)
- [ ] In-series citations (`[Mil…]`, `paper N`, `Paper N`) link to direct-download URLs from `github_pdf_urls.md`
- [ ] No em dashes anywhere (use colons, commas, or new sentences)
- [ ] Inline math uses `$...$`, display math uses `$$...$$`
- [ ] Every quantitative claim has a supporting figure
- [ ] Every N-D-C role mapping has a triangle diagram
- [ ] All figures use white background, canonical N/D/C colors, and correct triangle orientation
- [ ] All figure paths in the Markdown use **absolute paths** (`/home/jw/src/tv/docnav/...`), not relative paths
