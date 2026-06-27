---
name: research-paper-latex
description: Convert a research Markdown paper under docnav/Research/papers/ to the same artifact pattern as papers 1 to 5, canonical LaTeX plus a built PDF. Uses Pandoc, scripts/pandoc_paper_postprocess.py, then scripts/research_paper_pdflatex.sh (pdflatex). Use when the user wants a companion .md turned into .tex and .pdf, or paper 6 rebuilt end to end.
---

# Research paper Markdown to LaTeX and PDF

The **intended outcome** matches papers **1 to 5**: under `<N>_<slug>/` you have **`<N>_<slug>.tex`** and, after compilation, **`<N>_<slug>.pdf`** plus the usual LaTeX sidecars (`.aux`, `.log`, `.out`, `.toc`, and with `natbib` also `.bbl`, `.blg`).

**Pandoc only produces `.tex`.** A PDF appears only after **`pdflatex`** runs. The skill is not complete for “like the other papers” until that compile step succeeds (or you clearly report that no TeX engine is available and the user must install one or compile locally).

Companion papers live as `docnav/Research/papers/<N>_<slug>.md`. The canonical build lives in `<N>_<slug>/<N>_<slug>.tex`.

**In-series citation URLs:** Markdown sources should link cross-references to PDFs using direct-download URLs from `docnav/Research/papers/github_pdf_urls.md` (see `.cursor/rules/research-paper-references.mdc`). Pandoc converts body hyperlinks to `\href{...}{...}` in the output `.tex`.

**PDF References rule (mandatory):** Before building, every in-series References entry must include the full direct-download URL as **visible plain text** on its own line (angle-bracket form). Hyperlink-only References (`[Mil26a](url) ... [paper 1](url)`) are not acceptable: they vanish in print. See `.cursor/rules/research-paper-pdf.mdc`. Do not run `research_paper_pdflatex.sh` until the pre-build gate passes.

## Steps

0. **Pre-build gate** (mandatory). Open the source `.md` References section and verify every in-series entry follows the print-safe format in `.cursor/rules/research-paper-pdf.mdc`. Fix the Markdown before Pandoc if any entry uses hyperlink-only URLs.

1. **Pandoc** (standalone) from the `docnav/Research/papers` directory:
   ```bash
   pandoc 6_qualitative-nature-integers-triadic-roles.md \
     -o latex/_paper6_pandoc_raw.tex \
     --standalone \
     -V documentclass=article \
     -V papersize=letter \
     -V geometry=margin=1in \
     -V fontsize=11pt
   ```

2. **Post-process** (fixes `\maketitle`, `abstract` environment, section numbering, References/Appendix):
   ```bash
   python3 scripts/pandoc_paper_postprocess.py \
     docnav/Research/papers/latex/_paper6_pandoc_raw.tex \
     docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/6_qualitative-nature-integers-triadic-roles.tex
   ```

3. **Build PDF** (required for parity with papers 1 to 5). From the **repository root**:
   ```bash
   ./scripts/research_paper_pdflatex.sh docnav/Research/papers/6_qualitative-nature-integers-triadic-roles
   ```
   This runs **two** `pdflatex` passes (cross-references and TOC). If `pdflatex` is missing, install a TeX distribution first (for example `texlive-most` on Manjaro).

   **BibTeX:** papers that use **`natbib`** and a **`.bib`** file need **`bibtex <basename>`** between the first and second `pdflatex` pass (extend the script or run by hand for those papers). Paper 6 as converted from Markdown uses **inline / Pandoc-style references**, so two **`pdflatex`** passes alone are enough unless you add **`natbib`** and a **`.bib`** later.

4. **Post-build check.** Open the generated PDF References section. Confirm each in-series entry shows the full URL as readable text, not only a hyperlink label. If URLs overflow the margin, ensure `xurl` is loaded (already in `pandoc_paper_postprocess.py`) and URLs are on separate lines in the `.md`.

## Requirements

- Markdown must use `## Abstract` then `## 1. Introduction` (Pandoc pattern the script expects).
- In-series References must use visible URLs on separate lines (`.cursor/rules/research-paper-pdf.mdc`). Hyperlink-only References block PDF completion.
- Postprocessor is tuned for paper 6’s heading style; generalizing to other `.md` files may need regex updates in `scripts/pandoc_paper_postprocess.py`.

## Files touched

| File | Role |
|------|------|
| `scripts/pandoc_paper_postprocess.py` | Section promotion, abstract extraction |
| `scripts/research_paper_pdflatex.sh` | Two-pass `pdflatex` for a paper folder |
| `docnav/Research/papers/latex/_paper6_pandoc_raw.tex` | Optional Pandoc scratch (gitignored or delete after use) |
| `docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/6_qualitative-nature-integers-triadic-roles.tex` | Output LaTeX |
| `docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/6_qualitative-nature-integers-triadic-roles.pdf` | Output PDF (after step 3) |

Do not rename the postprocessor’s expected `## 1. Introduction` anchor without updating the script.
