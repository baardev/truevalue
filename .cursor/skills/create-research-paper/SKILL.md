---
name: create-research-paper
description: Create a new research paper in docnav/Research/papers/ with the correct canonical format: title, author, version, date, arXiv subjects, optional keywords, abstract, and numbered sections. Use when the user says "create a paper", "write a paper", "make this a paper", "add a new paper", or asks to turn a notes file or discovery into a formal research paper.
---

# Create Research Paper

All papers live as `docnav/Research/papers/<N>_<slug>.md` where `<N>` is the next available integer.

## Step 1: Determine the next paper number

```bash
ls docnav/Research/papers/*.md | grep -oP '^\d+' | sort -n | tail -1
```

Increment by 1 to get the new paper number. (Currently papers 1-6 and 8-10 exist; 7 is the next free slot as of June 2026.)

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

**[arXiv label]:** [primary subject]; [secondary subject] (secondary: [tertiary])
```

**arXiv label** varies slightly across the series; match context:
- `Proposed arXiv subjects:` (math-primary papers)
- `Provisional arXiv subjects:` (applied/interdisciplinary)
- `arXiv subject classifications:` (cs-primary papers)

**Keywords** line is optional. Include it when the paper has strong domain-specific terms worth indexing:

```markdown
**Keywords:** term1, term2, term3
```

Add keywords for physics, AI, or applied papers. Omit for pure-math papers where the arXiv subject line is sufficient (see papers 1, 3, 4, 6).

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

## Step 8: Cross-references to other papers in the series

Cite other papers in the series as `paper N` or `[Mil26N]` in the text. The series now includes papers 1 through 10 (with 7 open). Common back-references:

| Shorthand | Content |
|-----------|---------|
| Paper 1 | Five constants from tholonic recursion |
| Paper 2 | TVPCI supply-chain transparency scoring |
| Paper 3 | Minimal recursive triadic framework (irreducibility lemma) |
| Paper 4 | Game-theoretic triadic balance |
| Paper 5 | Tholonic-twistor connection |
| Paper 6 | Qualitative nature of integers in triadic roles |
| Paper 8 | Atom as measurable tholon |
| Paper 9 | Tholonic model vs Standard Model |
| Paper 10 | Neural networks as tholonic systems |

## Step 9: Build LaTeX and PDF

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
- arXiv label and subjects appear as a bold `\noindent` line immediately after `\maketitle`

Do not manually edit `\date{}`, `\author{}`, or the arXiv line in the `.tex` — regenerate from `--md` instead.

## Canonical header example

```markdown
# Seed-Space Convergence Hierarchy of Classical Constants Under Tholonic Recursion

**Author:** J. W. Milton, Clarity Coalition

**Version:** 1.0

**Date:** 8 June 2026

**Proposed arXiv subjects:** math.CA; math.NT (secondary: math.CO)

---

## Abstract

...

---

## 1. Introduction
```

## Checklist before handing off to research-paper-latex

- [ ] File saved as `docnav/Research/papers/<N>_<slug>.md`
- [ ] Header has Author, Version, Date, arXiv line
- [ ] `---` divider after header block and after Abstract
- [ ] All body sections numbered (`## 1.`, `## 2.`, ...)
- [ ] Introduction contains "What this paper provides / does not provide / Organization"
- [ ] References section present (even if minimal)
- [ ] No em dashes anywhere (use colons, commas, or new sentences)
- [ ] Inline math uses `$...$`, display math uses `$$...$$`
