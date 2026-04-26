---
doc_id: claude
title: CLAUDE.md
type: documentation
status: active
domain: project_documentation
layer: methodology
projects:
  []
tags:
  - methodology
  - project_documentation
related_docs:
  []
key_claims:
  []
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A quantitative, phase-resolved, physically-grounded model of the gold supply chain (geological origin to COMEX exchange registration), with a parallel shea butter supply chain instance. The system is a data pipeline + static web simulator, not a traditional web application.

## Writing Style

- Do not use em-dashes (--) anywhere in output, documentation, or generated content. Use colons, commas, or rephrase instead.

## Common Commands

### Start the dev environment
```bash
cd /home/jw/src/tv
python3 -m http.server 8000 --bind 127.0.0.1 # static backend behind Nginx
./scripts/start_mkdocs_from_site.sh # docs wiki (pre-built site/)
```

**Frontend entry points:**
- Gold supply chain: `http://localhost:8000/frontend/project/gold/supply_chain/Supplychain.html`
- Shea supply chain: `http://localhost:8000/frontend/project/shea/index.html`

### Systemd (preferred for production)
```bash
sudo cp deploy/tv-web.service /etc/systemd/system/
sudo cp deploy/tv-docs.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now tv-web.service tv-docs.service
```

### AUBEB password gate

Use Nginx in front of the Python static server when AUBEB pages need password
protection. See `deploy/README-aubeb-nginx.md`. The Python server should bind
to `127.0.0.1:8000` so browsers cannot bypass Nginx and request protected files
directly.

### Generate frontend data from schema CSVs
```bash
python3 src/api/generate_frontend_data.py   # outputs to data/processed/
python3 src/api/generate_ui_data.py
```

### Scrape live COMEX data (Phase 7 anchor)
```bash
python3 src/ingest/comex_scraper.py         # saves XLS to data/raw/
```

### Health check
```bash
python scripts/health_check.py
```

### Documentation wiki (live reload)
```bash
pip install -r requirements-docs.txt
mkdocs serve -f scripts/mkdocs.yml
```

### Install dependencies
```bash
pip install -r requirements.txt
```

There is no test suite. Validation is embedded in `src/ingest/data_importer.py` using pydantic models.

## Architecture

### Data flow
```
schema/ (CSV schemas)
    -> src/api/generate_frontend_data.py
        -> data/processed/ (JSON)
            -> frontend/ (HTML/JS reads JSON)

src/ingest/comex_scraper.py -> data/raw/ -> data/processed/
```

### Three strict analytical layers (never mix them)

1. **Supply chain**: physical flow, custody, constraints (phases 0-7)
2. **Value chain**: profit, pricing, margins
3. **Financial abstraction**: paper claims, leverage

No pricing, margins, or value discussion during supply chain modeling. No economic inference without a completed physical mapping. If gold cannot be weighed, moved, or stored in a step, it does not belong in the supply chain layer.

### Phase structure

Everything maps to one of 8 discrete phases (phase_id 0-7). Phase 7 (COMEX registration) is the highest-transparency anchor point. Phase 6 (vaulting) has a structural opacity gap; document it, never speculate about it.

Required structure per phase: `Phase -> Metric -> Unit -> Source -> Custodian`

Reject any concept that spans multiple phases without explicit linkage, or that cannot be assigned a phase_id.

### Schema-first rule

All data must be representable as CSV/SQL/dataframes. `schema/` is the single source of truth for field definitions. Narrative is secondary and must map to schema elements. If it cannot be tabulated, it does not exist.

### Simulation engines (`src/simulation/`)

- `tholonic_engine.py`: N-D-C (Negotiation, Definition, Contribution) recursive triadic model
- `phi_engine.py`: golden ratio optimization
- `ln2_engine.py`: balance calculations
- `balance_optimizer.py`: bottleneck detection

### Frontend (`frontend/`)

Static HTML+JS, no build step required. Pages read JSON from `data/processed/` directly.

## Operating Rules

### Rule 1: Separation of Concerns (non-negotiable)

Never mix the supply chain, value chain, and financial abstraction layers. No pricing or value discussion during supply chain modeling. No economic inference before the physical chain is fully mapped.

### Rule 2: Phase-Based Modeling

All analysis must map to a discrete supply chain phase. Each phase must be defined by a physical state of gold, a transformation or custody change, and a measurable output. Do not use narrative descriptions without metrics or aggregates that obscure phase boundaries.

### Rule 3: Data-First Discipline

Prefer quantitative metrics, units, time series, and source attribution. Every dataset must include: `phase_id`, `measurement_unit`, `source_type` (public / paid / private / inferred). If data is missing, mark it explicitly as `OPAQUE`. Do not interpolate or speculate. Missing data is a finding, not a failure.

### Rule 4: Transparency Classification

Every phase must be tagged: high transparency, medium transparency, or low transparency. Explain opacity using structural reasons only (private custody, commercial secrecy, jurisdictional limits). Never attribute opacity to conspiracy, bad actors, or malice; those belong only in later interpretive layers, if at all.

### Rule 5: Custody and Control Awareness

Distinguish between who owns the gold, who physically holds it, and who can legally mobilize it. Every transfer must specify whether ownership changes, whether custody changes, and whether gold remains physically stationary. Rehypothecation, leasing, and paper claims are out of scope until the supply chain is complete.

### Rule 6: Exchange Data as Anchor, Not Truth

COMEX inventories are highly transparent and legally constrained, but limited to registered bars. Do not extrapolate upstream supply from exchange data alone. Exchange data is used for reconciliation, not inference.

### Rule 7: Schema-First Development

All insights must be representable in CSV, SQL, or dataframes. Prioritize tables, schemas, and field definitions. Narrative explanation is secondary and must map to schema elements.

### Rule 8: Deferred Interpretation

Explicitly defer price formation, profit capture, market manipulation, and financial leverage until all supply chain phases are mapped and data visibility gaps are documented. Map the terrain first, then ask who benefits from it.

### Rule 9: Reproducibility and Auditability

Every claim must be traceable to a phase, a dataset, and a source category. Favor public data where possible; flag clearly where paywalled data is required.

### Rule 10: Tholonic N-D-C Framework

The gold supply chain is modeled using the Tholonic triadic structure of Negotiation (N), Definition (D), and Contribution (C).

Core principle: N is simultaneously the emergent product of D and C AND the source that differentiates into D and C. The relationship is recursive and bidirectional.

Full cycle: Parent N -> differentiates into D and C -> D and C negotiate -> Child N instantiates -> Child N becomes the next Parent N.

- **N (Negotiation)**: The stable, coherent instantiation at a given level. Emerges from the balance of D and C. Not directly measured.
- **D (Definition)**: Constraints, limitations, requirements, and boundaries. Internally focused; governs structure, specification, and identity.
- **C (Contribution)**: Outputs, applications, connections, and integrations. Externally focused; governs flow, production, and relationships.

Sustainability principle: systems are most stable and efficient when D ~ C. Imbalance increases energy cost and degrades the N state.

Hierarchical structure of the gold supply chain:

- Level 1 (supply chain as a whole): Parent N = refined gold; D = all constraints governing the refining/production process; C = outputs of the various phases; Child N = the 8-phase map.
- Level 2 (each individual phase): Parent N = the phase as bounded by the phase map; D = specific constraints of that phase; C = what that phase produces and passes forward; Child N = the actual operational instantiation.

A phase where the parent-N-to-child-N transition cannot be traced represents a structural break in the tholonic hierarchy. This is the analytical basis for transparency classification.

Apply this framework when analyzing phase health or sustainability, explaining why a phase is opaque or constrained, modeling how a change in one phase propagates to adjacent phases, and evaluating whether a proposed metric belongs to D (constraint) or C (output/flow).

**Mathematical grounding**: When the first three primes (2, 3, 5) are assigned to N, D, and C respectively and the recursive model is applied, fundamental mathematical constants emerge naturally (pi, phi, sqrt(2), e). This is structural, not coincidental. The N-D-C framework has mathematical validity independent of its descriptive utility. When quantitative tholonic metrics converge on or approximate these constants, treat this as significant.
