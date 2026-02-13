# Quick Start Guide

## Gold Supply Chain Intelligence Platform - Initial Setup

### What Has Been Built

A complete data pipeline foundation for modeling the gold supply chain from geological origin to COMEX exchange registration.

---

## Project Structure

```
tv/
├── schema/                          # CSV schemas (single source of truth)
│   ├── supply_chain_phases.csv     # 8 phases (0-7)
│   ├── gold_supply_chain_metrics.csv
│   ├── custody_and_flow.csv
│   └── data_sources.csv
│
├── data/
│   ├── raw/                         # Raw scraped data
│   ├── processed/                   # Cleaned, validated data
│   │   ├── phases.json             # Frontend: Phase definitions
│   │   ├── phase0_summary.json     # Frontend: Per-phase summaries
│   │   ├── ...
│   │   ├── phase7_summary.json
│   │   ├── simulation_defaults.json # Frontend: Default variables
│   │   └── transparency_report.json # Frontend: Data quality
│   └── archive/                     # Historical backups
│
├── src/
│   ├── ingest/
│   │   ├── comex_scraper.py        # Phase 7: COMEX daily inventory
│   │   └── data_importer.py        # Generic CSV importer with validation
│   │
│   ├── analysis/
│   │   └── phase7_comex_analysis.ipynb  # Jupyter notebook for Phase 7
│   │
│   └── api/
│       └── generate_frontend_data.py    # Generate JSON for frontend
│
├── docs/
│   ├── SUPPLY_CHAIN_RULES.md         # AI operating principles (supply chain layer)
│   └── FRONTEND_API.md              # API spec for interactive simulator
│
└── README.md                        # Project overview
```

---

## Installation

```bash
cd /home/jw/src/tv

# Install dependencies
pip install -r requirements.txt

# Verify schema
ls -l schema/

# Generate frontend data
python3 src/api/generate_frontend_data.py
```

---

## Phase-by-Phase Status

| Phase | Name | Transparency | Scraper | Analysis | Status |
|-------|------|--------------|---------|----------|--------|
| 0 | Geological Prospecting | Medium | ⏳ Manual | ⏳ | Ready for data |
| 1 | Mine Extraction | High | ⏳ Manual | ⏳ | Ready for data |
| 2 | Ore Processing | High | ⏳ Manual | ⏳ | Ready for data |
| 3 | Doré Production | Medium | ⏳ Manual | ⏳ | Ready for data |
| 4 | Refining | Medium | ⏳ Manual | ⏳ | Ready for data |
| 5 | Bar Casting & Assay | Medium-High | ⏳ Manual | ⏳ | Ready for data |
| 6 | Logistics & Vaulting | **Low (OPAQUE)** | N/A | ⏳ | Structural opacity |
| 7 | Exchange Registration | **High** | ✅ Ready | ✅ Notebook | **Anchor point** |

---

## Usage Workflows

### 1. Collect COMEX Data (Phase 7)

```bash
cd /home/jw/src/tv

# Run COMEX scraper
python3 src/ingest/comex_scraper.py

# Analyze in Jupyter
jupyter notebook src/analysis/phase7_comex_analysis.ipynb
```

### 2. Import Manual Data

```python
from src.ingest.data_importer import GoldDataImporter

importer = GoldDataImporter()

# Import metrics from external CSV
importer.import_metrics('path/to/mine_production.csv', validate=True)

# Mark something as explicitly opaque
importer.mark_opaque(
    phase_id=6,
    entity="Private Vault Network",
    reason="Custodial secrecy"
)

# Generate transparency report
report = importer.get_transparency_report()
print(report)
```

### 3. Generate Frontend Data

```bash
# Regenerate all JSON files for frontend
python3 src/api/generate_frontend_data.py
```

Output files in `data/processed/`:
- `phases.json` - Complete phase definitions
- `phase{N}_summary.json` - Per-phase metrics
- `simulation_defaults.json` - Variable configurations
- `transparency_report.json` - Data quality assessment

---

## Data Collection Priority

### Immediate (Public Data Available)

1. **Phase 7 (COMEX)**: Daily inventory scraping ✅ Ready
2. **Phase 1 (Mining)**: Annual production by company/country
   - Source: World Gold Council, USGS, company reports
3. **Phase 2 (Processing)**: Recovery rates
   - Source: NI 43-101 technical reports

### Short-Term (Semi-Public)

4. **Phase 4 (Refining)**: LBMA accredited refiner list + capacity estimates
5. **Phase 0 (Reserves)**: Geological survey data (JORC, NI 43-101)

### Long-Term (Paid/Estimated)

6. **Phases 3, 5**: Industry reports (Metals Focus, CPM Group)
7. **Phase 6**: Mark as OPAQUE, use aggregate estimates only

---

## Next Steps

### A. Data Collection Phase

1. **Run COMEX scraper weekly** to build time series
2. **Manually import mine production** (Phase 1)
   - Download World Gold Council data
   - Convert to CSV matching schema
   - Import using `data_importer.py`
3. **Add recovery rates** (Phase 2)
   - Extract from technical filings
   - Populate metrics table

### B. Analysis Phase

4. **Create Phase 1 analysis notebook** (mining production)
5. **Create Phase 2 analysis notebook** (ore processing)
6. **Flow reconciliation**: Compare Phase 1 → 2 → ... → 7
   - Does mining output match COMEX arrivals after losses?

### C. Simulation Engine

7. **Build simulation backend**
   - Take variable inputs (ore grade, recovery rate, etc.)
   - Propagate through phases
   - Calculate bottlenecks
   - Compare to actual COMEX data
8. **Create REST API** (FastAPI)
   - Implement endpoints from FRONTEND_API.md
9. **Build frontend** (React/Svelte + D3.js)
   - Phase flow visualization
   - Variable sliders
   - Real-time impact preview

---

## Working with the Frontend

### Current State

Static JSON files in `data/processed/` are ready for frontend development:

```javascript
// Example: Load phase data
fetch('/data/processed/phases.json')
  .then(res => res.json())
  .then(data => {
    console.log(data.phases);  // Array of 8 phases
  });

// Example: Load simulation variables
fetch('/data/processed/simulation_defaults.json')
  .then(res => res.json())
  .then(config => {
    console.log(config.variables);  // Adjustable parameters
  });
```

### Future: Live API

Once FastAPI is implemented:

```javascript
// GET all phases
fetch('http://localhost:8000/api/v1/phases')

// GET Phase 7 metrics
fetch('http://localhost:8000/api/v1/phase/7/metrics?date_from=2025-01-01')

// POST simulation run
fetch('http://localhost:8000/api/v1/simulation/run', {
  method: 'POST',
  body: JSON.stringify({
    scenario_name: "High ore grade",
    variables: { ore_grade: 5.0 }
  })
})
```

---

## Key Design Principles (From SUPPLY_CHAIN_RULES.md)

1. **Separation of Concerns**: Supply chain (physical) → Value chain (economic) → Financial (leverage)
2. **Phase-Based**: Everything maps to phases 0-7
3. **Data-First**: No speculation, mark opacity explicitly
4. **Schema-First**: If it can't be tabulated, it doesn't exist
5. **Deferred Interpretation**: Map terrain before asking who benefits

---

## Troubleshooting

### "No Phase 7 data in notebook"

Run COMEX scraper first:
```bash
python3 src/ingest/comex_scraper.py
```

### "Validation failed"

Check that CSV has required fields:
- `phase_id`, `entity`, `country`, `date`
- `metric_name`, `metric_value`, `unit`
- `source_type`

### "Module not found"

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## View the frontend in a browser

Serve the project from the repo root so both Gold and Shea pages (and their cross-links) work:

```bash
cd /home/jw/src/tv
python -m http.server 8000
```

Then open:

| Page | URL |
|------|-----|
| Gold supply chain (landing) | http://localhost:8000/frontend/supply_chain/Supplychain.html |
| Gold dashboard | http://localhost:8000/frontend/supply_chain/dashboard.html |
| Gold what-if simulator | http://localhost:8000/frontend/supply_chain/what_if_simulator.html |
| **Shea supply chain (landing)** | http://localhost:8000/frontend/shea/index.html |
| Shea dashboard | http://localhost:8000/frontend/shea/dashboard.html |
| Shea what-if simulator | http://localhost:8000/frontend/shea/what_if_simulator.html |

Stop the server with `Ctrl+C`. No install needed beyond Python.

---

## Questions?

- Review `docs/SUPPLY_CHAIN_RULES.md` for methodology
- Review `docs/FRONTEND_API.md` for API spec
- Check `README.md` for project overview

---

**Status**: Foundation Complete ✅  
**Next**: Data Collection Phase  
**Goal**: Interactive supply chain simulator with real-time reconciliation against COMEX

