# Gold Supply Chain Intelligence Platform

## Project Objective

Build a quantitative, phase-resolved, physically grounded model of the gold supply chain, from geological origin to exchange-registered bullion, before introducing price, value, or financial interpretation.

## End Goal

An interactive web-based simulation platform that allows users to:
- Manipulate variables across the supply chain
- Observe transient effects and cascading impacts
- Analyze profit/loss implications
- Evaluate sustainability constraints
- Reconcile physical flow against exchange inventories

## Architecture

```
tv/
├── data/              # Raw and processed data
├── schema/            # CSV schema definitions (single source of truth)
├── src/
│   ├── ingest/       # Data collection and ingestion tools
│   ├── analysis/     # Jupyter notebooks for phase analysis
│   ├── validation/   # Data quality and reconciliation
│   └── api/          # Future: API layer for frontend
├── docs/             # Documentation and methodology
└── frontend/         # Future: Interactive visualization layer
```

## Operating Principles

### 1. Separation of Concerns
- **Supply chain** (physical flow, custody, constraints) ← We start here
- **Value chain** (profit, pricing, margins) ← Added after physical mapping
- **Financial abstraction** (paper claims, leverage) ← Final layer

### 2. Phase-Based Modeling
All analysis maps to discrete supply chain phases (0-7):
- Phase 0: Geological Occurrence & Prospecting
- Phase 1: Mine Extraction
- Phase 2: Ore Processing & Concentration
- Phase 3: Doré Production
- Phase 4: Refining
- Phase 5: Bar Casting & Assay
- Phase 6: Logistics & Vaulting
- Phase 7: Exchange Registration

Each phase defined by:
- Physical state of gold
- Transformation or custody change
- Measurable output

### 3. Data-First Discipline
- No speculation - mark opacity explicitly
- Every dataset includes: phase_id, unit, source_type
- Missing data is a finding, not a failure

### 4. Transparency Classification
Every phase tagged:
- **High transparency**: Mine extraction, Exchange registration
- **Medium transparency**: Doré production, Refining, Bar casting
- **Low transparency**: Logistics & Vaulting (structural opacity)

### 5. Custody Awareness
Distinguish: ownership ≠ custody ≠ control

### 6. Exchange Data as Anchor
COMEX inventory = reconciliation target, not inference source

### 7. Schema-First Development
If it can't be tabulated, it doesn't exist.

### 8. Deferred Interpretation
Map the terrain before asking who benefits.

### 9. Reproducibility
Every claim traceable to: phase → dataset → source category

## Data Collection Strategy

### High Priority (Public Data)
- Phase 7: COMEX daily inventories (anchor point)
- Phase 1: Mine production by country/company
- Phase 2: Recovery rates from technical filings

### Medium Priority (Mixed Availability)
- Phase 4: Refinery capacity and throughput
- Phase 5: Bar specifications and standards
- Phase 0: Geological reserves (NI 43-101, JORC)

### Low Priority (Structural Opacity)
- Phase 6: Vault flows (mark as OPAQUE)
- Phase 3: Doré trade flows (aggregate only)

## Getting Started

### Prerequisites
```bash
python 3.11+
jupyter
pandas, numpy
requests, beautifulsoup4 (for scraping)
```

### Initial Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize schema
python src/ingest/init_schema.py

# Run COMEX scraper
python src/ingest/comex_scraper.py

# Launch analysis notebook
jupyter notebook src/analysis/
```

### Documentation wiki (MkDocs)
The `docs/` folder is built as a searchable wiki. To serve it locally:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Then open **http://127.0.0.1:8000**. To build a static site: `mkdocs build` (output in `site/`).

## Development Rules

### For AI Agents (Cursor)
1. **Never mix layers prematurely** - No pricing during supply chain modeling
2. **Everything must map to a phase_id** - Reject unstructured narratives
3. **Quantitative only** - Metrics, units, time series, source attribution
4. **Opacity is structural** - Never attribute to conspiracy
5. **Schema first** - All insights must be representable in CSV/SQL
6. **Work backwards from COMEX** - Highest transparency first

## Project Status

**Current Phase**: Foundation & Data Collection
- ✅ Conceptual framework defined
- ✅ Schema design complete
- 🔄 Infrastructure setup in progress
- ⏳ Phase 7 (COMEX) data collection next
- ⏳ Analysis framework pending

## License

[To be determined]

## Contact

[To be determined]

