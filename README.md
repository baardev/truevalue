---
doc_id: readme
title: TrueValue Analytics Platform
type: readme
status: active
domain: meta
tags: [meta, site-management, gold, supply-chain, tvpci, pdi]
related_docs: [skills_ref, document_registry, content_sync_log, tree]
key_claims: []
---

# TrueValue Analytics Platform

Site management reference. Start here when you need to know how the repo is
organized, what a config or management file does, how to add content, or how
to propagate a model change across documents.

---

## Project overview

A quantitative, phase-resolved, physically grounded platform for commodity
supply chain analysis. The primary instance is gold (Phases 0 through 7,
geological origin to COMEX-registered bullion). Parallel instances include
shea, blue carbon, Danube basin, and others.

The Tholonic N-D-C framework and five irreducible constants ($\varphi$, $e$,
$\ln 2$, $\sqrt 2$, $\pi/4$) provide the scoring backbone via the TVPCI
(Transparency via Phase-resolved Classification and Indexing) model. The
recycling chain is modeled as a parallel inverse chain (TVPCI-R) rather than
a Phase 8 appended to the forward chain.

Three analytical layers: supply chain (physical flow, custody, constraints)
then value chain (margins, pricing) then financial abstraction (paper claims).
Do not mix layers prematurely.

---

## Quick start

```bash
# Dev server (repo root = site root)
python3 -m http.server 8000 --bind 127.0.0.1
```

| URL | Page |
|-----|------|
| `http://localhost:8000/` | Homepage |
| `http://localhost:8000/frontend/project/gold/index.html` | Gold hub |
| `http://localhost:8000/frontend/project/gold/supply_chain/index.html` | Gold supply chain |
| `http://localhost:8000/frontend/project/shea/index.html` | Shea hub |

```bash
# Regenerate frontend JSON after schema or code changes
python3 src/api/generate_frontend_data.py
python3 src/api/generate_ui_data.py

# COMEX scrape (Phase 7 anchor)
python3 src/ingest/comex_scraper.py

# Health check
python3 scripts/health_check.py

# MkDocs wiki (optional)
pip install -r requirements-docs.txt
mkdocs serve -f scripts/mkdocs.yml
```

---

## Repo structure

```
tv/
├── README.md                     ← this file (site management reference)
├── index.html                    ← homepage (project grid + hub sections)
├── site-index.json               ← data source for homepage rendering
├── tree.md                       ← HTML page tree (all pages + nav links)
│
├── docs/                         ← all project documentation and management files
│   ├── skills.md                 ← AI skills and rules reference (human-readable)
│   ├── document-registry.yaml    ← curated registry of official/support documents
│   ├── content-sync-log.json     ← audit trail of every content sync run
│   └── notes.md                  ← operational notes (Cognee, tooling)
│
├── .cursor/
│   ├── rules/                    ← AI rule files (.mdc); always-applied or glob-triggered
│   └── skills/                   ← AI skill directories (each has a SKILL.md)
├── .cursorrules                  ← master AI operating rules for this project
│
├── docnav/
│   ├── Repos/intra/
│   │   ├── TVPCI/                ← TVPCI specification documents (Tier 1 source of truth)
│   │   └── PDI/                  ← Phase Discovery Instrument template + protocol + HTML form
│   ├── Research/
│   │   ├── papers/               ← numbered research papers (MD + TEX + PDF)
│   │   └── modeling/             ← modeling and analysis documents
│   └── .ai_notes/                ← AI-generated concept and document summary notes
│
├── frontend/
│   ├── site-index.json           ← site-wide config: project grid + hub section data
│   ├── homepage-layout.json      ← site-wide config: homepage category definitions
│   ├── js/
│   │   └── tv-hub.js             ← shared JavaScript reused across hub pages
│   └── project/
│       ├── shared/               ← shared code and test pages (not a real project)
│       │   ├── phi_balance_radar.js
│       │   └── model_engine_test.html
│       │
│       ├── gold/                 ← standard project layout (see below)
│       ├── shea/
│       ├── danube/               ← basin project: sub-projects one level deeper (see below)
│       └── ...
│
│       │
│       │   Standard project layout (gold, shea, lighter, water_*, etc.):
│       │   <name>/
│       │   ├── index.html            hub page (presentation)
│       │   ├── supply_chain/         HTML analysis pages (presentation)
│       │   ├── value_chain/          HTML analysis pages (presentation)
│       │   └── data/
│       │       ├── schema/           CSV schemas — source of truth for field definitions
│       │       ├── processed/        generated JSON — output of pipeline scripts
│       │       ├── PDI_*.yaml        PDI instances for this project
│       │       └── *_SOURCE_NOTE.md  source documents and analyst notes
│       │
│       │   Basin sub-project layout (danube only, one level deeper):
│       │   danube/
│       │   ├── index.html
│       │   ├── data/
│       │   └── <chain_name>/         e.g. human_commercial_fishing, natural_reed_bed
│       │       ├── supply_chain/
│       │       ├── value_chain/
│       │       └── data/
│
├── src/
│   ├── api/                      ← data generation scripts (generate_frontend_data.py etc.)
│   ├── simulation/               ← Tholonic engines: phi, ln2, sqrt2, e, pi, balance
│   ├── ingest/                   ← data collection (comex_scraper.py, data_importer.py)
│   └── analysis/                 ← Jupyter notebooks
│
├── schema/                       ← CSV schema definitions (project-level source of truth)
├── scripts/                      ← build helpers (pdflatex, pandoc, serve.py, health_check.py)
├── deploy/                       ← systemd service files and install script
└── data/                         ← raw and processed data
```

---

## Site management files

### Config and AI tooling

| File / Path | What it does |
|-------------|--------------|
| `.cursorrules` | Master AI operating rules: methodology, layer separation, schema-first, COMEX anchor, Tholonic N-D-C framework. Non-negotiable for every session. |
| `.cursor/rules/*.mdc` | Individual AI rules. Some always-apply (punctuation, project workflow, skills maintenance). Others trigger on file globs (PDI files, frontend simulators, basin architecture). |
| `.cursor/skills/*/SKILL.md` | AI skill playbooks. Each is a multi-step procedure the agent follows when triggered. See `docs/skills.md` for the full list. |

### Document management files

| File | What it does |
|------|--------------|
| `docs/document-registry.yaml` | Curated registry of all official and support documents. Each entry has a `doc_id`, `path`, `type`, `status`, `tags`, and `derived` list. Used by the `content-sync` skill to build work lists. **Add an entry here whenever a new official or support document is created.** |
| `docs/content-sync-log.json` | Append-only audit trail. Every time the `content-sync` skill runs, it adds one entry: date, change type, files updated, PDFs rebuilt, notes. Never delete entries. |
| `docs/skills.md` | Human-readable reference for every AI skill and rule. Updated automatically by the agent whenever a skill or rule is added, changed, or removed. |
| `tree.md` | All HTML pages in the project organized by commodity hierarchy, with navigation link maps. Update when pages are added or renamed. |
| `site-index.json` | Data source for the homepage. Lists all projects (for the project card grid) and hub sections (Papers, PDI, etc.). The `add-homepage-section` skill manages this file. |

### TVPCI specification documents

All live under `docnav/Repos/intra/TVPCI/`. These are the Tier 1 source of
truth for the TVPCI model. Update these first when any TVPCI parameter,
formula, or phase definition changes. Downstream documents (research papers,
frontend HTML, generated JSON) are updated afterward via `content-sync`.

| File | Role |
|------|------|
| `TVPCI_FOUNDATION.md` | Full first-principles derivation; canonical phase map; R_p parallel recycling structure |
| `TVPCI_FOUNDATION_INTRO.md` | Accessible introduction; five-constant rationale; stakeholder questions |
| `TVPCI_FOUNDATION_SIMPLE.md` | Simplified version for non-technical audiences |
| `TVPCI_EXPLAINED_MATH.md` | Mathematical walkthrough of the five constants |
| `TVPCI_TRUE_VALUE_PRICING_CONVERGENCE_INDEX.md` | High-level overview; formula; synthetic benchmarks |

### PDI instrument files

All live under `docnav/Repos/intra/PDI/`. The PDI (Phase Discovery Instrument)
maps any supply chain from first principles.

| File | Role |
|------|------|
| `PDI_TEMPLATE.yaml` | Master template v1.1. Supports `chain_type: forward \| recycling \| ecosystem`. Copy this for every new PDI instance; never fill in the template itself. |
| `PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md` | Narrative protocol document. Authoritative description of all four modules and every field. |
| `PDI.html` | Interactive HTML form for PDI completion. Supports chain_type selector and recycling-specific fields. |
| `PDI_WORKED_EXAMPLE_GOLD_SUPPLY_CHAIN.md` | Fully completed forward-chain example (gold, Phases 0-7). Reference for new instances. |

Completed PDI instances live alongside their project data:
`frontend/project/<name>/data/PDI_<material>_<date>.yaml`

---

## Content workflows

### Add a new frontend page

1. Create the HTML file in the appropriate `frontend/project/<name>/` location.
2. Add it to `tree.md`.
3. If it needs a homepage card or hub section, run the `add-homepage-section` skill.
4. Add an entry to `docs/document-registry.yaml`.

### Add a new official document

1. Create the file.
2. Add an entry to `docs/document-registry.yaml` with correct `type`, `status`, `tags`, and `derived` paths.
3. If it is a research paper (MD source), use the `research-paper-latex` skill to generate the TEX and PDF.

### Propagate a model change (TVPCI, algorithm, schema)

Use the `content-sync` skill. It reads `docs/document-registry.yaml`, filters
by the relevant tags, builds a work list, executes targeted edits in document
tier order, and appends to `docs/content-sync-log.json`.

Trigger phrase examples: "TVPCI phase 3 weight changed," "I added a new supply
chain," "the phi engine was updated, sync the documents."

### Update the PDI instrument

When a new field is needed in any PDI instance, the `pdi-processing` rule
requires syncing all three files in the same session:
`PDI_TEMPLATE.yaml`, `PDI.html`, and
`PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md`.

---

## Deployment

### Development (local)

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Bind to `127.0.0.1` so that browsers cannot bypass any Nginx gate that may
sit in front.

### Production (systemd)

```bash
sudo bash deploy/install-service.sh
```

This copies `deploy/tv-web.service` to `/etc/systemd/system/`, reloads
the daemon, and enables and starts the `tv-web` unit. The service runs
`scripts/serve.py` (HTTP on 8000, HTTPS on 8443, bound to `127.0.0.1`).

Useful service commands:

```bash
systemctl status  tv-web
journalctl -u tv-web -f
systemctl restart tv-web
systemctl stop    tv-web
```

### AUBEB password gate

Put Nginx on `tvf.tholonia.com:80` in front of the Python server. Config
template is in `deploy/nginx-tv-aubeb.conf.template`; install notes in
`deploy/README-aubeb-nginx.md`.

---

## Operating principles

1. **Layer separation.** Supply chain (physical) before value chain (margins)
   before financial abstraction. Never mix layers in the same analysis.
2. **Phase-based modeling.** Every metric maps to a phase_id. The gold primary
   chain is Phases 0-7. The gold recycling chain (TVPCI-R) is a parallel
   inverse chain documented in its own PDI instance, not a Phase 8.
3. **Schema first.** If a claim cannot be tabulated in a CSV schema, it does
   not exist for this project.
4. **Data-first discipline.** Mark opacity explicitly. Missing data is a
   structural finding, not a failure.
5. **COMEX as anchor.** Phase 7 (exchange registration) is the highest-
   transparency reference point. Work backwards from it.
6. **Custody awareness.** Ownership, custody, and control are distinct.
   Never conflate them.
7. **Auditability.** Every claim must be traceable to: phase, metric, unit,
   source, custodian.
8. **Reproducibility.** Every document change is logged in
   `docs/content-sync-log.json`. Every schema change propagates through
   the generate scripts before frontend files are considered current.

---

## Dependencies

```bash
pip install -r requirements.txt          # core pipeline
pip install -r requirements-docs.txt     # MkDocs wiki (optional)
```

Core: Python 3.11+, pandas, numpy, requests, beautifulsoup4.
LaTeX (pdflatex): required to build research paper PDFs. Install
`texlive-most` on Manjaro or equivalent on other distros.
