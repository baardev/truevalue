# Skills and Rules Reference

This document is the authoritative guide to every Cursor Agent Skill and every Cursor Rule active in this project. It must be kept up to date whenever a skill or rule is added, changed, or removed.

**Skills location:** `.cursor/skills/<skill-name>/SKILL.md`
**Rules location:** `.cursor/rules/<rule-name>.mdc`
**This file location:** `docs/skills.md`

---

## How to use a skill

Skills are markdown instructions the AI agent follows when asked to perform a specific task. To activate a skill, describe what you want in plain language. If the description matches a skill's trigger terms, the agent loads and follows it automatically.

You can also name a skill explicitly: "use the add-homepage-section skill to add a Papers section."

To add a new skill, describe the workflow to the agent and ask it to "create a skill for this." The agent will place the skill in `.cursor/skills/` and update this file.

---

## Project skills

### `create-project`

**File:** `.cursor/skills/create-project/SKILL.md`

**What it does:** End-to-end guide for creating any new project in this repo. Handles two project types:

- **Type A (standalone hub):** Gold/Shea/AUBEB/water hub pattern. Creates the full `frontend/project/<slug>/` folder tree, required HTML pages (hub, supply chain, value chain), and a mandatory `supply_chain/recycling_analysis.html` (TVPCI-R Ecological Return Chain page with R_p scores, B_chain KPI, waste stream table, and circular economy interventions). Also generates processed JSON, applies N-D-C formulas, and registers the project on the homepage.
- **Type B (basin subproject):** Danube natural/human/paired pattern. Creates `project.yaml`, PDI YAML, CSV schema files, runs the basin data generation script, builds all six HTML pages, updates the basin hub index and bond prospectus, and registers the project.

Both paths end with the same post-creation steps: homepage registration (via `add-homepage-section`), `tree.md` update, rebuild, and a final checklist covering JSON validation, nav links, coherence panels, recycling analysis presence, em-dash check, and color-scheme declarations.

**When to use it:** Any time you say "create a new project," "add a new hub," "scaffold a new supply chain," "set up a basin subproject," or "start a new project page."

**Files it touches (varies by type):**
- `frontend/project/<slug>/` (entire new folder)
- `frontend/site-index.json` and `frontend/homepage-layout.json` (via `add-homepage-section`)
- `index.html` (homepage registration, Type B hub sections)
- `tree.md`
- `scripts/generate_danube_data.py` (Type B only)

**Rules it consolidates:** `project-homepage-template.mdc`, `basin-subproject-architecture.mdc`, `rebuild-on-change.mdc`, `tv-project-workflow.mdc`, and the `add-homepage-section` skill.

---

### `add-homepage-section`

**File:** `.cursor/skills/add-homepage-section/SKILL.md`

**What it does:** Guides the agent through adding new content to the TrueValue Analytics homepage (`index.html`). Handles two scenarios:

- **Type A: Project card** — a tile in the top project grid. Adds an entry to `frontend/site-index.json > projects` and assigns it to a category in `frontend/homepage-layout.json`. If no suitable category exists, the agent asks you what to call it before proceeding.
- **Type B: Hub section** — a labeled row of rich cards below the project grid (like Papers, PDI, Twistors). Adds the data key to `site-index.json`, inserts the HTML placeholder div, adds the CSS rules, adds the JS render block, and adds the error handler entry, all in `index.html`.

**When to use it:** Any time you say "add a section to the homepage," "add a project card," "link these files on the homepage," or "create a new homepage block."

**Files it touches:**
- `frontend/site-index.json` (always)
- `frontend/homepage-layout.json` (Type A only)
- `index.html` (Type B only)

**Key constraint:** The skill validates JSON after every write and bumps the `?v=` cache-bust date on the `SITE_INDEX` variable in `index.html`.

---

### `create-research-paper`

**File:** `.cursor/skills/create-research-paper/SKILL.md`

**What it does:** Scaffolds a new numbered research paper in `docnav/Research/papers/` with the canonical header (title, Author, Version, Date, Keywords), Abstract with `---` dividers, numbered body sections, and an Introduction with the standard "What this paper provides / does not provide / Organization" block. Determines the next available paper number, chooses a slug, and runs the pre-build checklist. Steps 7–8 require in-series citations to link to direct-download PDF URLs from `docnav/Research/papers/github_pdf_urls.md`. Includes a figure generation step (Step 9) covering when figures are required, naming conventions, style rules (white background, canonical N/D/C colors, correct triangle orientation), and figure types by section. Delegates LaTeX and PDF generation to the `research-paper-latex` skill.

**When to use it:** Whenever the user asks to "create a paper", "write a paper", "make this a paper", or turn a notes or discovery file into a formal research paper in the series.

**Files it touches:**
- `docnav/Research/papers/<N>_<slug>.md` (the new paper)
- `docnav/Research/papers/<N>_<slug>/figures/<N>_<descriptor>.png` (generated figures)

---

### `research-paper-latex`

**File:** `.cursor/skills/research-paper-latex/SKILL.md`

**What it does:** Converts a companion research paper from Markdown (`docnav/Research/papers/<n>_<slug>.md`) to the **same artifact pattern as papers 1 to 5**: canonical LaTeX under `<n>_<slug>/` plus a **built PDF** and usual LaTeX sidecars. Flow is **Pandoc** to raw standalone `.tex`, **`scripts/pandoc_paper_postprocess.py`** for preprint-style layout (title page Keywords line) and headings, then **`scripts/research_paper_pdflatex.sh`** (two-pass **`pdflatex`**). Markdown in-series links should use URLs from `github_pdf_urls.md` before conversion. Without **`pdflatex`** on PATH, only **`.tex`** exists until the user installs TeX and runs the script.

**When to use it:** Whenever you ask to turn paper 6 (or a similar numbered paper) from `.md` into **`.tex` and `.pdf`**, rebuild paper 6 end to end, or match the repo’s existing paper folder layout.

**Files it touches:**
- `docnav/Research/papers/latex/_paper6_pandoc_raw.tex` (optional intermediate; can be deleted after a successful run)
- `docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/6_qualitative-nature-integers-triadic-roles.tex` (primary LaTeX for paper 6)
- `docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/6_qualitative-nature-integers-triadic-roles.pdf` (after `research_paper_pdflatex.sh`)
- `scripts/pandoc_paper_postprocess.py` (shared postprocessor; extend only with care)
- `scripts/research_paper_pdflatex.sh` (two-pass compile helper)

---

### `faq-md-to-html`

**File:** `.cursor/skills/faq-md-to-html/SKILL.md`

**What it does:** Converts `docnav/FAQ/tholonic-faq.md` into `docnav/FAQ/tholonic-faq.html`. Produces a self-contained, single-file HTML page with: a sticky two-column layout (280px TOC sidebar + content area), all questions grouped by section with anchor links, N-D-C role colours applied inline (N = blue `#1d4ed8`, D = green `#15803d`, C = red `#b91c1c`), colour-coded callout boxes for N/D/C definitions and examples, MathJax 3 for LaTeX rendering, the six-domain N-D-C context table with colour-coded column headers, and an IntersectionObserver script that highlights the active TOC entry as the user scrolls.

**When to use it:** Whenever the user says "convert the FAQ", "rebuild the HTML FAQ", "regenerate tholonic-faq.html", "sync the FAQ HTML", or asks to update the HTML version of the FAQ after changes to the markdown source.

**Files it touches:**
- `docnav/FAQ/tholonic-faq.html` (always regenerated from scratch)
- `docnav/FAQ/tholonic-faq.md` (read-only source)

---

### `paper-to-essay`

**File:** `.cursor/skills/paper-to-essay/SKILL.md`

**What it does:** Converts a technical research paper in `docnav/Research/papers/` into a well-written, accessible essay for educated non-expert readers. The essay re-presents the paper's ideas in plain prose with analogies and concrete examples, replacing equations with descriptions and jargon with clear substitutes. Supports four named audiences: `educated-layperson`, `magazine`, `humanities`, and `highschool`. Optionally generates illustrative images using the `GenerateImage` tool for concepts that are hard to grasp in prose alone. Output is saved to `docnav/Research/papers/essays/<N>_<slug>_<audience>.md`.

**When to use it:** Whenever the user says "convert this paper to an essay", "make this readable for non-experts", "write a layperson version", "magazine version", "humanities version", "explain this paper to a general audience", or asks for an "accessible version" of any research paper.

**Files it touches:**
- `docnav/Research/papers/essays/<N>_<slug>_<audience>.md` (the new essay, always)
- Images auto-saved by the `GenerateImage` tool (optional)

---

### `content-sync`

**File:** `.cursor/skills/content-sync/SKILL.md`

**What it does:** Propagates a model or data change across every affected document, dashboard, and generated artifact in the project, then appends a summary entry to `docs/content-sync-log.json`. Covers four change types:

- **`tvpci`**: TVPCI formula or parameter update. Works through five tiers: (1) primary TVPCI spec docs in `docnav/Repos/intra/TVPCI/`, (2) research papers 2, 3, 5, 6 (MD + TEX + PDF rebuild), (3) AI notes regenerated from updated Tier 1 source, (4) per-project PDI status files (methodology changes only), (5) `scenarios.json`, gold supply chain dashboard HTML, and regenerated frontend JSON.
- **`new-chain`**: New supply chain project added (gold scope for now). Creates the frontend scaffold, updates `site-index.json` and `index.html` via the `add-homepage-section` skill, and adds the chain to paper 2.
- **`engine`**: Simulation engine edit (`phi_engine.py`, `ln2_engine.py`, etc.). Checks affected dashboard HTML and generate scripts, then regenerates JSON.
- **`schema`**: CSV schema field added, renamed, or removed. Updates generate scripts and the `frontend/project/gold/data/schema/` copies, then regenerates JSON.

After executing the work list, the skill appends one entry to `docs/content-sync-log.json` with: date, change type, one-line description, list of files updated, PDFs rebuilt, whether JSON was regenerated, and optional notes.

**Work list source:** The skill now reads `docs/document-registry.yaml` first and filters by tag to build the work list dynamically. The hardcoded impact tables in the skill are a fallback only.

**When to use it:** Any time you say "TVPCI changed," "I added a new supply chain," "the algorithm was updated," "sync the documents," or "what needs updating after this change?"

**Files it touches (varies by change type):**
- `docnav/Research/papers/2_supply-chain-transparency-tvpci.md` and `.tex`
- `docnav/Research/papers/4_game-theoretic-triadic-balance/...tex`
- `docnav/Research/papers/5_tholonic-twistor-connection/...tex`
- `docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/...tex`
- `frontend/project/gold/supply_chain/scenarios.json`
- `frontend/project/gold/supply_chain/index.html`, `dashboard.html`
- `src/api/generate_frontend_data.py`, `src/api/generate_ui_data.py`
- `site-index.json`, `index.html` (new-chain only, via `add-homepage-section`)
- `docs/content-sync-log.json` (always, audit trail)

**Key constraint:** Never rewrite whole documents during a sync. Scope every edit to the changed value or section only. The `.md` source is edited before `.tex`; do not re-run Pandoc for parameter-only changes.

---

## Supporting reference files

### `docs/user-manual.md`

Two-part user manual. **Part A (Analyst Guide):** scoring model in plain terms, the five constants and what they measure, TVPCI-R and B_chain interpretation, platform navigation (homepage, gold hub, dashboard, what-if simulator, recycling analysis page), reading a PDI, score interpretation tables. **Part B (Developer Guide):** adding a new commodity project end-to-end, propagating a model change, adding a research paper, data pipeline commands, updating the PDI instrument, and key constraints to observe.

### `docs/document-registry.yaml`

Central curated registry of all official and support documents for TVF projects. Each entry carries:

- `doc_id` (unique slug), `path` (repo-relative), `title`, `type` (official | support | schema | frontend | archive)
- `status` (active | draft | deprecated | provisional)
- `domain` and `tags` (used by content-sync to filter the work list)
- `last_updated`, `description`, `related_docs`, `derived` (paths of TEX/PDF/JSON built from this source)

AI notes under `docnav/.ai_notes/` are self-describing and not listed here. Add a new entry to the registry whenever a new official or support document is created. Update `last_updated` and `tags` as part of any content-sync run.

### `docs/ndc_measurement_framework.md`

Explains the Tholonic N-D-C measurement framework in plain terms: what a tholonic primitive is (and its three subtypes), how D and C values are currently derived from PDI binary flags, where the mathematical constants (phi) enter as convergence targets rather than computed outputs, the key distinction from AI training, and a structured analysis of current weaknesses (scale arbitrariness, sustainability metric scale-dependence, cross-commodity invalidity). Closes with four candidate approaches to a principled normalization scale, from threshold-ratio normalization (recommended near-term) to prime-ratio derivation (long-term theoretical goal). Intended as a conceptual reference for analysts and developers.

### `docs/roadmap.md`

Platform-wide planning tracker. Organized into six sections: PDI status per project (with a conformance check for PDI v1.1), TVPCI scoring pipeline tasks, research paper status, frontend and site structure tasks, infrastructure and tooling, and documentation. Also contains a "Completed milestones" block for recent history. Update this file whenever a task is finished or a new task is identified. It is not a change log (use `docs/content-sync-log.json` for that).

### `docs/content-sync-log.json`

Append-only audit trail written by the `content-sync` skill after every sync run. Each entry records: date, change type, one-line description, files updated, PDFs rebuilt, whether JSON was regenerated, and notes for the next reader.

---

## Cursor rules (always-applied and context-triggered)

Rules live in `.cursor/rules/`. Rules with `alwaysApply: true` are active in every chat. Rules with `globs` activate when you open or edit a matching file.

### `tv-project-workflow` (always applied)

**File:** `.cursor/rules/tv-project-workflow.mdc`

The master workflow reference for this repo. Covers:

- Terminology: **TVPCI**, **TVPCI-R**, **GGW** (always Great Green Wall)
- Dev server startup (`python3 scripts/serve.py --http-only`, `bash scripts/restart_server`)
- Protected project paths (`deploy/protected-paths.json`, `deploy/auth.env`)
- Frontend entry URLs for gold, west African shea (`west_african_shea`), and other hubs
- Data pipeline commands (`generate_frontend_data.py`, `generate_ui_data.py`, `comex_scraper.py`)
- Health check script
- Architecture overview (supply chain vs value chain vs financial abstraction layers)
- Schema-first principle and simulation code locations
- The `docs/` folder convention (all documentation, notes, and how-to guides live in `docs/`)

### `punctuation` (always applied)

**File:** `.cursor/rules/punctuation.mdc`

Enforces two formatting standards across all written output:

1. No em dashes anywhere. Use a comma, colon, parentheses, or a new sentence instead.
2. LaTeX inline math uses `$...$` delimiters, not `\(` and `\)`.

### `rebuild-on-change`

**File:** `.cursor/rules/rebuild-on-change.mdc`
**Triggers on:** `frontend/**`, `index.html`, `data/**`

After any HTML page is created or modified, the agent must run the appropriate rebuild step. The rule includes a step-selection table:

| Change type | Required action |
|-------------|----------------|
| New project under `frontend/project/<m>/` | Update homepage card + `tree.md` |
| Existing HTML page modified | Check all pages linking to it |
| Source CSVs edited | `RUN_GENERATE_UI=1 ./scripts/rebuild-site.sh` |
| Full new project (PDI + data + HTML) | `RUN_GENERATE_UI=1 ./scripts/rebuild-site.sh` |

### `project-homepage-template`

**File:** `.cursor/rules/project-homepage-template.mdc`
**Triggers on:** `frontend/project/**`, `frontend/site-index.json`, `tree.md`

Defines the required structure for every new project hub page. Required elements include: hero section with kicker and subtitle, four KPI cards, alert/insight panel, layer cards (Supply Chain, System Lifecycle, Value Chain), phase strip or radar chart, and a five-model coherence panel (pi, phi, sqrt2, ln2, e). Also specifies the required shape of the processed JSON file that feeds the hub.

### `pdi-processing`

**File:** `.cursor/rules/pdi-processing.mdc`
**Triggers on:** `frontend/docs/PDI/**`, `frontend/PDI.html`

Rules for working with Phase Discovery Instrument (PDI) YAML files. Covers how to fill out, update, and maintain PDI instances and the master protocol document.

### `pdi-to-html-pipeline`

**File:** `.cursor/rules/pdi-to-html-pipeline.mdc`
**Triggers on:** `frontend/docs/PDI/PDI_*.yaml`, `frontend/project/**`

Full pipeline for converting a completed PDI YAML into a new project's data files and HTML pages, following the gold/shea hub structure. Use this when bootstrapping a new commodity project from a PDI file.

### `basin-subproject-architecture`

**File:** `.cursor/rules/basin-subproject-architecture.mdc`
**Triggers on:** `frontend/project/danube/**`, `frontend/project/*/index.html`, `scripts/generate_danube_data.py`

Architecture and naming conventions for building ecosystem subprojects under a basin hub (currently Danube). Covers natural service chains, human service chains, paired chains, file structure, and HTML page requirements.

### `frontend-simulator-conventions`

**File:** `.cursor/rules/frontend-simulator-conventions.mdc`
**Triggers on:** `frontend/project/gold/supply_chain/**`, `src/api/**`

Conventions for the Gold Supply Chain dashboard and what-if simulator: data contract between `generate_ui_data.py` and the JS frontend, chart patterns, slider behavior, and metric display format.

### `intervention-worksheet`

**File:** `.cursor/rules/intervention-worksheet.mdc`
**Triggers on:** `alwaysApply: true` (changed from glob-only to ensure the rule fires even when creating project_context.html from scratch)

Requires every `project_context.html` to contain a Phase Intervention Worksheet section. The section must include: a provisional disclaimer, a five-axis failure diagnosis table (pi, phi, sqrt2, ln2, e) with chain scores, one worksheet block per bottleneck phase with named interventions and estimated D/C effects, and a combined effect estimate. References `marina_alta/supply_chain/project_context.html` as the canonical template. Includes a completion checklist.

### `skills-maintenance` (always applied)

**File:** `.cursor/rules/skills-maintenance.mdc`

Enforces that `docs/skills.md` is updated whenever any skill under `.cursor/skills/` is added, changed, or deleted. See the rule file for exact obligations.

### `research-paper-references`

**File:** `.cursor/rules/research-paper-references.mdc`
**Triggers on:** `docnav/Research/papers/**/*.md`

Governs in-series citation URLs for research papers. Key rules:

- `docnav/Research/papers/github_pdf_urls.md` is the single source of truth for GitHub PDF URLs.
- Link both citation keys (`[Mil26a]`) and plain prose (`paper 3`, `Paper 1 of this series`) to the **Direct download** URL (`github.com/.../raw/main/...`).
- Do not use `raw.githubusercontent.com` (LFS pointer issue).
- Citation keys are per-file, not global; match URLs to each file's References mapping.
- Add new papers to `github_pdf_urls.md` before writing cross-references.

### `research-paper-images`

**File:** `.cursor/rules/research-paper-images.mdc`
**Triggers on:** `docnav/Research/papers/**/*.md`

Governs image path conventions for research papers. Key rules:

- All `![caption](path)` references in paper `.md` files must use **absolute filesystem paths** (e.g. `/home/jw/src/tv/docnav/Research/papers/17_foo/figures/17_bar.png`). Absolute paths render correctly in the IDE Markdown preview regardless of where the `.md` file sits relative to the figures folder.
- `scripts/pandoc_paper_postprocess.py` automatically rewrites absolute image paths to paths relative to the output `.tex` directory before writing the final `.tex`, so `pdflatex` (which runs from inside the paper folder) finds the figures correctly.
- Paper-specific figures live in `docnav/Research/papers/<N>_<slug>/figures/`. Shared figures live in `docnav/Research/papers/figures/`.
- Naming convention: `<N>_<short-descriptor>.png`.

---

## Maintenance

When you add, change, or delete a skill or rule:

1. Update the relevant section in this file.
2. If adding a skill: add a new `###` subsection under "Project skills" with the name, file path, what it does, when to use it, and files it touches.
3. If adding a rule: add a new `###` subsection under "Cursor rules" with the name, file path, trigger condition, and a plain-language description.
4. If deleting: remove the section entirely and note the removal with a one-line comment in git.

This file is the single source of truth for "what AI tools does this project have?"
