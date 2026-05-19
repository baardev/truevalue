# TrueValue Analytics Platform: User Manual

**Version 1.0 — May 2026**

This manual has two parts. Part A is for analysts and researchers using the
platform to evaluate supply chains. Part B is for developers and contributors
adding data, new projects, or extending the model.

---

# Part A: Analyst Guide

## What this platform does

TrueValue Analytics scores commodity supply chains using a structural model
based on five irreducible mathematical constants. The central question it
answers is: **how close to its structural ideal is this supply chain operating,
and where is the gap?**

The output is not a price or a financial rating. It is a transparency and
coherence score that identifies which phases of a chain are structurally sound,
which are bottlenecks, and where ecological or custody accountability breaks
down.

---

## The scoring model in plain terms

Every supply chain phase is scored on three dimensions:

| Role | Symbol | What it measures |
|------|--------|-----------------|
| Negotiation state | N | Declared position: mass balance coherence, identifier continuity, document completeness |
| Definition / limitation | D | Bounding evidence: audit scope, counterparty documentation, policy existence |
| Contribution / corroboration | C | Independent evidence depth: third-party assays, geospatial attestation, physical touchpoints |

A **balance score B** penalizes one-sided evidence. High D with no C (detailed
policy, no independent test) scores low. High C with no D (test result,
no governing policy) also scores low. Both directions of imbalance degrade the
score identically.

The five constants anchor what "balanced" means at each structural level:

| Constant | Value | Role in scoring |
|---------|-------|----------------|
| $\varphi$ (phi) | 1.618 | Coherence: phase-to-phase amplification ratio. A chain where each phase amplifies value by ~1.618 is self-similar. |
| $e$ | 2.718 | Decay: rate at which imbalance propagates to adjacent phases. |
| $\ln 2$ | 0.693 | Doubling: unit of value capture. Measures which phases capture which logarithmic growth steps. |
| $\sqrt{2}$ | 1.414 | Threshold: marks the structural crossing from physically-constrained to institutionally-constrained phases. |
| $\pi/4$ | 0.785 | Equilibrium: whether the value and material cycles close (the ecological return question). |

The overall **TVPCI score** (Transparency via Phase-resolved Classification and
Indexing) is a weighted aggregate on 0-100. Higher scores mean the chain
operates closer to its structural ideal. Opaque phases incur a transparency
penalty rather than a false score.

---

## The recycling model (TVPCI-R and B_chain)

A supply chain does not only flow forward. Every phase generates waste: tailings,
emissions, process water, scrap. The **TVPCI-R** score measures how visible and
managed those ecological return flows are, using the same N-D-C scoring logic
but applied to waste streams rather than custody claims.

TVPCI-R is not a Phase 8 appended to the forward chain. It is a parallel
structure, scored at each of the primary chain's phases, weighted by the waste
intensity of each phase (extraction phases carry much higher weight than
vaulting phases).

The **B_chain** score combines the two:

$$B_\text{chain} = 100 \cdot \exp\!\left(-2 \cdot \frac{|\text{TVPCI} - \text{TVPCI-R}|}{\max(\text{TVPCI},\,\text{TVPCI-R})}\right)$$

| Score | Meaning |
|-------|---------|
| 80-100 | Coherent: custody and ecological accountability are in proportion |
| 61.8-79 | Stressed: chain is accountable for what it takes more than what it gives back |
| 38.2-61.8 | Failure: ecological accountability substantially lags custody transparency |
| 0-38.2 | Breakdown: chain's ecological debt is effectively invisible |

For the current gold benchmark (TVPCI = 82.5, TVPCI-R = 41.2), B_chain ≈ 45.4,
placing the gold supply chain in the Failure zone. This is the expected structural
condition under current voluntary disclosure norms.

---

## Navigating the platform

### Homepage

Open `http://localhost:8000/` (or the production URL). The homepage shows a
grid of all active projects. Current projects include:

**Commodity chains:** Gold, Shea, Lighter, Blue Carbon

**Water systems:** Singapore NEWater, Orange County GWRS, Jackson MS Water,
Water Recycling Comparison

**Ecosystem / energy:** Danube Basin, Photosynthesis, ERCOT Winter Storm Uri

**Other:** AUBEB, CUNY EPHS PhD, History of Economic Thought

Below the project grid, hub sections link to: Research Papers, PDI instruments,
modeling documents, and TVPCI resources.

### Gold hub: the primary worked example

From the homepage, open **Gold**. The hub page has four main sections:

**Supply Chain.** The physical forward chain, Phases 0 through 7. Start here.

**System Lifecycle.** N-D-C lifecycle view of the system as a whole.

**Value Chain.** Margin and pricing analysis. Only meaningful after the supply
chain layer is understood.

**Ecological Return (TVPCI-R).** The recycling parallel chain. Scores each
primary phase for waste-stream visibility and aggregates into TVPCI-R and B_chain.

### Gold supply chain dashboard

The main dashboard shows:

- **Phase flow diagram.** Each of the eight phases (0-7) with its N-D-C balance
  scores and transparency classification. Click any phase to see detail.
- **TVPCI score.** Overall chain score, decomposed by phase contribution.
- **Five-constant panels.** One panel per constant showing how each dimension
  scores across the chain.
- **TVPCI-R and B_chain KPI cards.** Chain-level recycling accountability score.
- **Phase 6 bottleneck.** The logistics and vaulting phase consistently shows the
  largest D-C gap. The dashboard identifies the correctable lever (expanding C
  via custody reporting reform, not by reducing D security requirements).

### What-If simulator

The what-if simulator lets you adjust phase-level parameters and observe
downstream effects on the TVPCI score. Use it to model scenarios such as:

- Mandatory ecological disclosure at all phases (narrows TVPCI-TVPCI-R gap)
- Improved logistics transparency (closes the Phase 6 bottleneck)
- New LBMA-accredited secondary smelters (improves TVPCI-R Phase 2 score)

All scenario data is in `frontend/project/gold/supply_chain/scenarios.json`.

### TVPCI-R recycling analysis page

Open via **Ecological Return** on the gold hub or via the nav card on the supply
chain index. Shows:

- 8-spoke spider chart: one spoke per primary phase, spoke length = R_p score
  weighted by omega_p
- Per-phase collapsible cards: waste streams, N/D/C scores, B_r and delta_r
- Interactive worksheet: adjust indicator values and live-recalculate TVPCI-R
  and B_chain
- All data marked PROVISIONAL until replaced with empirical measurements

### Reading a PDI

The Phase Discovery Instrument (PDI) is how each supply chain's phase structure
was determined from first principles. You can view any completed PDI YAML
alongside the HTML form at `docnav/Repos/intra/PDI/PDI.html`.

The gold forward chain PDI is documented in
`docnav/Repos/intra/PDI/PDI_WORKED_EXAMPLE_GOLD_SUPPLY_CHAIN.md`.

The gold recycling chain PDI is at
`frontend/project/gold/data/PDI_gold_recycling_2026.yaml`.

---

## Interpreting scores

### Phase transparency classifications

| Classification | Opacity score (C1-C4) | Meaning |
|---------------|----------------------|---------|
| High | 4 | All four measurability tests pass. Volume, custodians, process, and output are all independently verifiable. |
| Medium | 2-3 | Partial traceability. Some structural gaps. |
| Low | 0-1 | Phase is structurally opaque. The N-state transition cannot be independently confirmed. |

For recycling chain phases (C1-C5): High = 5, Medium = 3-4, Low = 0-2.

### TVPCI zone thresholds (phi-derived)

| Score | Zone |
|-------|------|
| 80-100 | Coherent |
| 61.8-79 | Stressed (phi-reciprocal boundary) |
| 38.2-61.8 | Failure |
| 0-38.2 | Breakdown |

### What a low TVPCI does and does not mean

A low TVPCI does not mean the chain is fraudulent or badly managed. It means
the chain produces insufficient independently verifiable information to confirm
structural coherence. Opacity at Phase 6 (vaulting) is a structural property
of that phase, not a finding about misconduct. The score measures what is
knowable, not what is intended.

---

# Part B: Developer and Contributor Guide

## Frontend file taxonomy

Everything under `frontend/` falls into exactly one of these categories. There
are no other types.

### Site-wide config (frontend root)

| File | Purpose |
|------|---------|
| `frontend/site-index.json` | Project grid entries and hub section data for the homepage. Managed by the `add-homepage-section` skill. |
| `frontend/homepage-layout.json` | Category definitions that group projects on the homepage. |

### Shared code (not a project)

`frontend/js/tv-hub.js` is shared JavaScript reused across hub pages.
`frontend/project/shared/` contains shared charting components (`phi_balance_radar.js`)
and test pages. Neither is a commodity project and neither has a `data/` folder
with real data.

### Standard project layout

Every commodity project (`gold`, `shea`, `lighter`, `water_*`, etc.) follows
this structure:

```
frontend/project/<name>/
├── index.html                  presentation — hub page
├── supply_chain/               presentation — HTML analysis pages
│   ├── index.html
│   ├── dashboard.html
│   ├── what_if_simulator.html
│   └── ...
├── value_chain/                presentation — HTML analysis pages
└── data/
    ├── schema/                 data — CSV schemas (source of truth for field definitions)
    ├── processed/              data — generated JSON (output of pipeline scripts, not edited by hand)
    ├── PDI_<material>_<date>.yaml   project content — PDI phase map instances
    └── *_SOURCE_NOTE.md        project content — source documents and analyst notes
```

Rules that follow from this structure:

- **Schema CSVs are edited directly** when field definitions change.
- **Processed JSON is never edited by hand.** Re-run the pipeline scripts.
- **PDI YAMLs are completed by the analyst or AI** using the template.
- **Source notes are input material**, not outputs. They are what the analyst
  reads to fill in a PDI or schema.

### Basin sub-project layout (Danube only)

The Danube project has an extra layer because each service chain is a
sub-project:

```
frontend/project/danube/
├── index.html
├── data/
└── <chain_name>/               e.g. human_commercial_fishing, natural_reed_bed
    ├── supply_chain/
    ├── value_chain/
    └── data/
        ├── schema/
        ├── processed/
        └── PDI_*.yaml
```

The pattern at each chain level is identical to the standard layout. Only the
depth changes.

---

## Adding a new commodity project

1. **Run the PDI.** Open `docnav/Repos/intra/PDI/PDI.html` or copy
   `docnav/Repos/intra/PDI/PDI_TEMPLATE.yaml`. Work through all four modules
   to produce the phase map, transparency ratings, and child-N outputs.
   Save the completed instance as `frontend/project/<name>/data/PDI_<material>_<date>.yaml`.

2. **Create the schema CSVs.** Based on the PDI phase map, create the supply
   chain phase schema at `frontend/project/<name>/data/schema/supply_chain_phases.csv`
   (and associated metrics CSVs). Use the gold schemas as reference.

3. **Generate the frontend JSON.** Add the new project to `src/api/generate_frontend_data.py`
   and run it. Output goes to `frontend/project/<name>/data/processed/`.

4. **Build the hub page.** Copy the gold hub structure
   (`frontend/project/gold/index.html`) and adapt. Use the `add-homepage-section`
   skill to add the project card to the homepage.

5. **Register the documents.** Add entries to `docs/document-registry.yaml`
   for the PDI YAML, the schema CSVs, the hub HTML, and any supply chain
   HTML pages.

6. **Update tree.md.** Add the new pages to the HTML page tree.

---

## Propagating a model change

When TVPCI parameters, phase definitions, or algorithms change, use the
**content-sync skill**. Tell the AI: "TVPCI phase 3 weight changed from X to Y,
sync the documents."

The skill reads `docs/document-registry.yaml`, filters by the relevant tags
(e.g. `tvpci`), and works through five tiers:

1. TVPCI specification documents in `docnav/Repos/intra/TVPCI/`
2. Research papers (MD then TEX; rebuild PDF)
3. AI notes (regenerated from Tier 1 sources)
4. PDI status files (only if phase methodology changed)
5. Frontend dashboards and generated JSON

Every sync run appends to `docs/content-sync-log.json`.

---

## Adding a research paper

1. Write the paper as a Markdown file at
   `docnav/Research/papers/<N>_<slug>.md` following the abstract + numbered
   sections pattern.

2. Use the **research-paper-latex skill** to convert it. The skill runs Pandoc,
   post-processes the LaTeX, and compiles to PDF via `pdflatex`.

3. Register the paper in `docs/document-registry.yaml` with its tags and
   `derived` paths for the TEX and PDF.

---

## Data pipeline

```bash
# After changing a schema CSV:
python3 src/api/generate_frontend_data.py
python3 src/api/generate_ui_data.py

# COMEX Phase 7 anchor data:
python3 src/ingest/comex_scraper.py

# Health check (validates data integrity):
python3 scripts/health_check.py
```

Schema CSVs are the source of truth for field definitions. If you cannot
represent a claim in a CSV row, it does not exist for this project.

---

## Updating the PDI instrument

When any PDI instance requires a new field that does not exist in the template,
the `pdi-processing` rule requires three files to be updated in the same
session:

| File | What to do |
|------|-----------|
| `docnav/Repos/intra/PDI/PDI_TEMPLATE.yaml` | Add the field with a blank default and a `# [NEW FIELD]` comment |
| `docnav/Repos/intra/PDI/PDI.html` | Add the corresponding form input |
| `docnav/Repos/intra/PDI/PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md` | Document the field in the relevant module section |

---

## Key constraints to observe

- **Never mix analytical layers.** Supply chain (physical) before value chain
  (margins) before financial abstraction. The dashboard pages enforce this
  visually; the methodology enforces it structurally.
- **Phase 8 does not exist.** Recycling is modeled as a parallel TVPCI-R
  structure, not as an extension of the forward phase sequence.
- **Schema first.** Every new metric needs a CSV schema entry before a frontend
  card. If it cannot be tabulated, it does not enter the model.
- **Opacity is structural, not editorial.** Never describe an opaque phase as
  suspicious or as a failure of the operator. Record it as a measurability
  finding.
- **All provisional data must be labelled.** Any value derived from schematic
  estimates (rather than empirical sources) carries `data_status: PROVISIONAL`
  in its schema and a visible banner in the frontend.
- **Document registry hygiene.** Add every new official or support document to
  `docs/document-registry.yaml` before ending the session. This is how the
  content-sync skill finds files to update in future runs.

---

## Reference links

| Resource | Location |
|---------|----------|
| Site management reference | `README.md` |
| All AI skills and rules | `docs/skills.md` |
| Document registry | `docs/document-registry.yaml` |
| Sync audit trail | `docs/content-sync-log.json` |
| HTML page tree | `tree.md` |
| TVPCI foundation spec | `docnav/Repos/intra/TVPCI/TVPCI_FOUNDATION.md` |
| PDI template | `docnav/Repos/intra/PDI/PDI_TEMPLATE.yaml` |
| PDI HTML form | `docnav/Repos/intra/PDI/PDI.html` |
| Gold supply chain hub | `frontend/project/gold/index.html` |
| Gold recycling PDI | `frontend/project/gold/data/PDI_gold_recycling_2026.yaml` |
