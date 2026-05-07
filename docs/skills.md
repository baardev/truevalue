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

## Cursor rules (always-applied and context-triggered)

Rules live in `.cursor/rules/`. Rules with `alwaysApply: true` are active in every chat. Rules with `globs` activate when you open or edit a matching file.

### `tv-project-workflow` (always applied)

**File:** `.cursor/rules/tv-project-workflow.mdc`

The master workflow reference for this repo. Covers:

- Dev server startup (`python3 -m http.server 8000`)
- Frontend entry URLs for gold, shea, and other hubs
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

### `skills-maintenance` (always applied)

**File:** `.cursor/rules/skills-maintenance.mdc`

Enforces that `docs/skills.md` is updated whenever any skill under `.cursor/skills/` is added, changed, or deleted. See the rule file for exact obligations.

---

## Maintenance

When you add, change, or delete a skill or rule:

1. Update the relevant section in this file.
2. If adding a skill: add a new `###` subsection under "Project skills" with the name, file path, what it does, when to use it, and files it touches.
3. If adding a rule: add a new `###` subsection under "Cursor rules" with the name, file path, trigger condition, and a plain-language description.
4. If deleting: remove the section entirely and note the removal with a one-line comment in git.

This file is the single source of truth for "what AI tools does this project have?"
