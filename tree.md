---
doc_id: tree
title: HTML Page Tree
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

# HTML Page Tree

All HTML pages in the project, organised by the new commodity-first hierarchy.
Arrows (→) show outbound navigation links. `/index.html` is the root landing page.

---

## Structure overview

```
index.html                          Root — project grid, Papers (DocNav drafts), PDI/PCI/Twistors/Game theory hubs
├── frontend/project/gold/index.html        Gold commodity hub
│   ├── supply_chain/index.html     Gold Supply Chain hub
│   │   ├── project_context.html
│   │   ├── system_lifecycle.html
│   │   ├── dashboard.html
│   │   └── what_if_simulator.html
│   └── value_chain/index.html      Gold Value Chain hub
│       ├── dashboard.html
│       └── what_if_simulator.html
├── frontend/project/west_african_shea/index.html        **West African Shea** commodity hub
│   ├── supply_chain/index.html     **West African Shea** Supply Chain hub
│   │   ├── project_context.html
│   │   ├── system_lifecycle.html
│   │   ├── dashboard.html
│   │   └── what_if_simulator.html
│   └── value_chain/index.html      **West African Shea** Value Chain hub
│       ├── dashboard.html
│       └── what_if_simulator.html
├── frontend/project/marina_alta/index.html  Marina Alta Mountain Ecosystem — Multi-commodity climate adaptation hub
│   ├── project.yaml                Marina Alta project metadata, key metrics, EU Horizon funding context
│   ├── research_notes.md           Comprehensive data: email, PPTX 19-slide plan, YouTube transcripts, web research
│   ├── supply_chain/index.html     Supply Chain hub — 8-phase analysis
│   │   ├── dashboard.html          Dark-theme N-D-C dashboard; bottleneck Phases 2 and 6
│   │   ├── project_context.html    Context, actor network, 10-year cherry trend, bond opportunity analysis
│   │   └── recycling_analysis.html TVPCI-R ecological return chain (alperujo, cherry marc, almond shells)
│   ├── value_chain/index.html      Value Chain — investment model, EUR 10-25M SLB, Los Grobos scaling
│   └── data/
│       └── processed/marina_alta_supply_chain_ui.json
├── frontend/docs/PDI/PDI_marina_alta_20260606.yaml   Marina Alta Physical Disclosure Index YAML (8 phases)
├── frontend/docs/PDI/PDI_andalucia_olive_20260606.yaml  Andalucia olive ecosystem PDI (8 phases, paired with Marina Alta)
├── frontend/project/spain_olive_oil/index.html   Spain Olive Oil — Spanish supply and value chain hub
│   ├── project.yaml                Olive oil project metadata, key metrics, bond relevance
│   ├── supply_chain/index.html     Supply Chain hub — 8-phase analysis
│   │   ├── dashboard.html          Dark-theme dashboard with NDC bars and coherence scores
│   │   ├── recycling_analysis.html TVPCI-R ecological return chain (alperujo, alpechin, packaging)
│   │   └── project_context.html    Context, key actors, bond opportunity analysis, 16 sources
│   ├── value_chain/index.html      Value Chain — price structure, EUR 1.20/kg premium gap
│   └── data/
│       ├── schema/spain_olive_oil_supply_chain_phases.csv
│       ├── schema/spain_olive_oil_supply_chain_metrics.csv
│       └── processed/spain_olive_oil_supply_chain_ui.json
├── frontend/project/cocoa_international/index.html  Cocoa International — Global Supply and Value Chain hub
│   ├── project.yaml                Cocoa project metadata, 7-phase structure, bond relevance, key metrics
│   ├── supply_chain/index.html     Supply Chain hub — 7-phase analysis, Phase 1 bottleneck
│   │   ├── dashboard.html          Dark-theme dashboard with NDC bars and five-model coherence
│   │   ├── recycling_analysis.html TVPCI-R ecological return chain (pod husks, shell, packaging)
│   │   └── project_context.html    Context, country breakdown, bond structures, risk factors, 10 sources
│   ├── value_chain/index.html      Value Chain — farm-to-retail 1:6 ratio, certification premium analysis
│   └── data/
│       ├── schema/cocoa_international_supply_chain_phases.csv
│       ├── schema/cocoa_international_supply_chain_metrics.csv
│       └── processed/cocoa_international_supply_chain_ui.json
├── frontend/project/cocoa_netherlands/index.html  Cocoa Netherlands — Industrial Processing and Value Hub (6 phases, shea composite at Phase 3, data quality H)
│   ├── project.yaml                Cocoa Netherlands project metadata, 6-phase structure, shea integration, bond relevance
│   ├── supply_chain/index.html     Supply Chain hub — 6-phase analysis, Phase 4 bottleneck (85.1%), shea composite at Phase 3
│   │   ├── dashboard.html          Dark-theme dashboard with NDC bars, Five-Model coherence, Phase Detail Table
│   │   ├── project_context.html    Context, shea composite calculation, Tony's vs conventional, bond structures, 15 sources
│   │   └── recycling_analysis.html TVPCI-R ecological return chain — TVPCI-R 65.0 vs global 46.0; shell-to-energy; EPR
│   ├── value_chain/index.html      Value Chain — Tony's Chocolonely Living Income model, CBE economics, bond structures
│   └── data/
│       ├── schema/cocoa_netherlands_supply_chain_phases.csv
│       ├── schema/cocoa_netherlands_supply_chain_metrics.csv
│       └── processed/cocoa_netherlands_supply_chain_ui.json
├── frontend/project/gran_chaco/index.html  Gran Chaco — Soy, Beef & Forest Ecosystem Services hub
│   ├── project.yaml                Gran Chaco project metadata and bond relevance
│   ├── supply_chain/index.html     Soy Supply Chain — 5-phase analysis
│   │   ├── dashboard.html          Dark-theme dashboard with NDC bars and coherence pentagon
│   │   └── project_context.html    Context, bond opportunity analysis, risk factors
│   ├── value_chain/index.html      Value Chain (deferred — pending beef and ecosystem PDIs)
│   └── data/
│       ├── PDI_soy_gran_chaco_2026.yaml
│       ├── schema/gran_chaco_supply_chain_phases.csv
│       ├── schema/gran_chaco_supply_chain_metrics.csv
│       └── processed/gran_chaco_supply_chain_ui.json
├── frontend/project/burkino_faso_shea/index.html  Burkina Faso Shea — BAU vs. Serious Shea Dual-Scenario Supply Chain Hub
│   ├── supply_chain/index.html     Supply Chain — 8-phase dual-scenario phase flow table (BAU vs. Serious Shea)
│   │   ├── dashboard.html          Dark amber N-D-C dashboard with grouped BAU/SS bar charts and coherence pentagon
│   │   ├── project_context.html    Women's economics, buyer landscape, carbon data, DD 2022 inventory, actor map
│   │   └── recycling_analysis.html TVPCI-R, B_chain, per-phase R_p cards, waste stream table (biogas/syngas/compost), interventions
│   ├── value_chain/index.html      Value Chain — kernel pricing, butter grades, EBITDA projections, carbon revenue, BAU vs SS gap
│   └── data/processed/burkino_faso_shea_supply_chain_ui.json
├── frontend/project/senegal_agroforestry/index.html  Senegal Agroforestry — Ecosystem Carbon and Agroforestry Hub
│   ├── supply_chain/index.html     Supply Chain — 8-phase agroforestry chain overview
│   │   ├── dashboard.html          Dark-theme N-D-C dashboard with phase bars and coherence pentagon
│   │   ├── project_context.html    PDI data, land cover, carbon projections, actor map, sovereign risk
│   │   └── recycling_analysis.html TVPCI-R, B_chain, per-phase R_p cards, waste stream table, interventions
│   ├── value_chain/index.html      Value Chain (deferred — carbon revenue context from Mirova shown)
│   └── data/processed/senegal_agroforestry_supply_chain_ui.json
├── frontend/project/aubeb/index.html       AUBEB commodity hub
│   ├── supply_chain/index.html     AUBEB Supply Chain hub
│   │   ├── project_context.html
│   │   ├── system_lifecycle.html
│   │   ├── dashboard.html
│   │   └── what_if_simulator.html
│   └── value_chain/index.html      AUBEB Value Chain hub
│       ├── dashboard.html
│       ├── what_if_simulator.html
│       └── financial_report.html
├── frontend/project/water_newwater/index.html   Singapore NEWater hub
│   ├── supply_chain/index.html     NEWater Supply Chain hub
│   │   ├── project_context.html
│   │   ├── dashboard.html
│   │   └── what_if_simulator.html
│   └── value_chain/index.html      NEWater Value Chain hub
│       ├── dashboard.html
│       ├── what_if_simulator.html
│       └── financial_report.html
├── frontend/project/water_ocwd/index.html   Orange County GWRS hub
│   ├── supply_chain/index.html     OCWD Supply Chain hub
│   │   ├── project_context.html
│   │   ├── dashboard.html
│   │   └── what_if_simulator.html
│   └── value_chain/index.html      OCWD Value Chain hub
│       ├── dashboard.html
│       ├── what_if_simulator.html
│       └── financial_report.html
├── frontend/project/water_jackson_ms/index.html   Jackson MS Water broken-system hub
│   ├── supply_chain/index.html     Jackson Water Supply Chain hub
│   │   ├── project_context.html
│   │   ├── system_lifecycle.html
│   │   └── dashboard.html
│   └── value_chain/index.html      Jackson Water deferred value layer
├── frontend/project/grid_ercot_uri/index.html     ERCOT Uri broken-grid hub
│   ├── supply_chain/index.html     ERCOT Uri Supply Chain hub
│   │   ├── project_context.html
│   │   ├── system_lifecycle.html
│   │   └── dashboard.html
│   └── value_chain/index.html      ERCOT Uri deferred value layer
├── frontend/project/water_compare/index.html   NEWater vs. OCWD comparative analysis
├── frontend/project/olive_compare/index.html   Marina Alta vs. Andalucia olive ecosystem comparison
│   └── data/andalucia_olive_supply_chain_ui.json  Andalucia 8-phase supply chain N-D-C data (phases.synthetic format)
```

Every page follows a uniform depth: **Root → Commodity hub → Layer hub → View**.

---

## Root

```
index.html  ·  TV Project Home — True Value Analytics
├── → frontend/project/gold/supply_chain/index.html
├── → frontend/project/gold/value_chain/index.html
├── → frontend/project/west_african_shea/supply_chain/index.html
├── → frontend/project/west_african_shea/value_chain/index.html
├── → frontend/project/aubeb/index.html
├── → frontend/project/water_jackson_ms/index.html
├── → frontend/project/grid_ercot_uri/index.html
├── → frontend/project/gold/index.html     (Gold Hub shortcut)
├── → frontend/project/west_african_shea/index.html     (**West African Shea** Hub shortcut)
└── → frontend/csv/index.html
```

---

## frontend/gold/

Gold commodity hub and its supply, lifecycle, and value layers.

```
index.html  ·  Gold – Supply & Value Chain Hub
├── → supply_chain/index.html
├── → supply_chain/project_context.html
├── → supply_chain/system_lifecycle.html
├── → supply_chain/dashboard.html
├── → supply_chain/what_if_simulator.html
├── → value_chain/index.html
├── → value_chain/dashboard.html
├── → value_chain/what_if_simulator.html
├── → ../west_african_shea/index.html
└── → /index.html
```

### frontend/project/gold/supply_chain/

```
index.html  ·  Gold Supply Chain – Intelligence Platform
├── → project_context.html
├── → system_lifecycle.html
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (Gold Hub)
├── → ../../west_african_shea/supply_chain/index.html
└── → /index.html

project_context.html  ·  Gold – Project Context & Supply Chain
├── → index.html
├── → system_lifecycle.html
├── → dashboard.html
├── → what_if_simulator.html
└── → /index.html

system_lifecycle.html  ·  Gold System Lifecycle N-D-C
├── → index.html
├── → project_context.html
├── → ../index.html            (Gold Hub)
└── → /index.html

dashboard.html  ·  Gold Supply Chain Intelligence – Main Dashboard
├── → ../../west_african_shea/index.html
└── → /index.html

what_if_simulator.html  ·  What-If Simulator – Gold Supply Chain
├── → dashboard.html
├── → ../../west_african_shea/index.html
└── → /index.html
```

### frontend/project/gold/value_chain/

```
index.html  ·  Gold Value Chain – Intelligence Platform
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (Gold Hub)
├── → ../../west_african_shea/value_chain/index.html
└── → /index.html

dashboard.html  ·  Value Chain Dashboard
├── → what_if_simulator.html
├── → ../../west_african_shea/value_chain/dashboard.html
└── → /index.html

what_if_simulator.html  ·  Value Chain What-If Simulator
├── → dashboard.html
└── → /index.html
```

---

## frontend/project/west_african_shea/

**West African Shea** commodity hub and its supply, lifecycle, and value layers.

```
index.html  ·  **West African Shea** – Supply & Value Chain Hub
├── → supply_chain/index.html
├── → supply_chain/project_context.html
├── → supply_chain/system_lifecycle.html
├── → supply_chain/dashboard.html
├── → supply_chain/what_if_simulator.html
├── → value_chain/index.html
├── → value_chain/dashboard.html
├── → value_chain/what_if_simulator.html
├── → ../gold/index.html
└── → /index.html
```

### frontend/project/west_african_shea/supply_chain/

```
index.html  ·  **West African Shea** Supply Chain – True Value (Real-World Example)
├── → project_context.html
├── → system_lifecycle.html
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (**West African Shea** Hub)
├── → ../../gold/supply_chain/index.html
└── → /index.html

project_context.html  ·  **West African Shea** – Project Context & Impact
├── → index.html
├── → system_lifecycle.html
├── → dashboard.html
├── → what_if_simulator.html
├── → ../../gold/supply_chain/index.html
└── → /index.html

system_lifecycle.html  ·  **West African Shea** System Lifecycle N-D-C
├── → index.html
├── → project_context.html
├── → ../index.html            (**West African Shea** Hub)
└── → /index.html

dashboard.html  ·  **West African Shea** Supply Chain – Dashboard
├── → index.html
├── → project_context.html
├── → what_if_simulator.html
├── → ../../gold/supply_chain/index.html
└── → /index.html

what_if_simulator.html  ·  What-If Simulator – **West African Shea** Supply Chain
├── → dashboard.html
├── → index.html
├── → project_context.html
├── → ../../gold/supply_chain/index.html
└── → /index.html
```

### frontend/project/west_african_shea/value_chain/

```
index.html  ·  **West African Shea** Value Chain – Intelligence Platform
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (**West African Shea** Hub)
└── → /index.html

dashboard.html  ·  **West African Shea** Value Chain Dashboard
├── → what_if_simulator.html
└── → /index.html

what_if_simulator.html  ·  **West African Shea** Value What-If Simulator
├── → dashboard.html
└── → /index.html
```

---

## frontend/project/aubeb/

AUBEB commodity hub and its supply, lifecycle, and value layers.

```
index.html  ·  AUBEB – Supply & Value Chain Hub
├── → supply_chain/index.html
├── → supply_chain/project_context.html
├── → supply_chain/system_lifecycle.html
├── → supply_chain/dashboard.html
├── → supply_chain/what_if_simulator.html
├── → value_chain/index.html
├── → value_chain/dashboard.html
├── → value_chain/what_if_simulator.html
└── → /index.html
```

### frontend/project/aubeb/supply_chain/

```
index.html  ·  AUBEB Supply Chain – Intelligence Platform
├── → project_context.html
├── → system_lifecycle.html
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (AUBEB Hub)
└── → /index.html

project_context.html  ·  AUBEB – Project Context & Supply Chain
├── → index.html
├── → system_lifecycle.html
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html
└── → /index.html

system_lifecycle.html  ·  AUBEB System Lifecycle N-D-C
├── → index.html
├── → project_context.html
├── → ../index.html            (AUBEB Hub)
└── → /index.html
```

### frontend/project/aubeb/value_chain/

```
index.html  ·  AUBEB Value Chain – Intelligence Platform
├── → dashboard.html
├── → what_if_simulator.html
├── → financial_report.html
├── → ../index.html            (AUBEB Hub)
└── → /index.html
```

---

## frontend/project/water_jackson_ms/

Jackson, Mississippi municipal water broken-system case, with physical supply-chain and lifecycle maintenance layers.

```
index.html  ·  Jackson MS Water System - Broken System Case
├── → supply_chain/index.html
├── → supply_chain/project_context.html
├── → supply_chain/system_lifecycle.html
├── → supply_chain/dashboard.html
├── → value_chain/index.html
└── → /index.html
```

### frontend/project/water_jackson_ms/supply_chain/

```
index.html  ·  Jackson MS Water Supply Chain
├── → project_context.html
├── → system_lifecycle.html
├── → dashboard.html
├── → ../index.html            (Jackson Hub)
└── → /index.html

project_context.html  ·  Jackson Water Project Context
├── → index.html
├── → system_lifecycle.html
├── → dashboard.html
├── → ../index.html
└── → /index.html

system_lifecycle.html  ·  Jackson Water Lifecycle
├── → index.html
├── → dashboard.html
├── → ../index.html            (Jackson Hub)
└── → /index.html

dashboard.html  ·  Jackson Water Dashboard
├── → index.html
├── → system_lifecycle.html
├── → ../index.html
└── → /index.html
```

### frontend/project/water_jackson_ms/value_chain/

```
index.html  ·  Jackson Water Value Chain Placeholder
├── → ../index.html            (Jackson Hub)
└── → /index.html
```

---

## frontend/project/grid_ercot_uri/

Texas ERCOT Winter Storm Uri broken-grid case, with physical grid chain and lifecycle winterization layers.

```
index.html  ·  ERCOT Winter Storm Uri Grid - Broken System Case
├── → supply_chain/index.html
├── → supply_chain/project_context.html
├── → supply_chain/system_lifecycle.html
├── → supply_chain/dashboard.html
├── → value_chain/index.html
└── → /index.html
```

### frontend/project/grid_ercot_uri/supply_chain/

```
index.html  ·  ERCOT Uri Supply Chain
├── → project_context.html
├── → system_lifecycle.html
├── → dashboard.html
├── → ../index.html            (ERCOT Hub)
└── → /index.html

project_context.html  ·  ERCOT Uri Project Context
├── → index.html
├── → system_lifecycle.html
├── → dashboard.html
├── → ../index.html
└── → /index.html

system_lifecycle.html  ·  ERCOT Uri Lifecycle
├── → index.html
├── → dashboard.html
├── → ../index.html            (ERCOT Hub)
└── → /index.html

dashboard.html  ·  ERCOT Uri Dashboard
├── → index.html
├── → system_lifecycle.html
├── → ../index.html
└── → /index.html
```

### frontend/project/grid_ercot_uri/value_chain/

```
index.html  ·  ERCOT Uri Value Chain Placeholder
├── → ../index.html            (ERCOT Hub)
└── → /index.html
```

---

## frontend/report/

Static report pages — no outbound navigation links.

```
investor_report.html            ·  The TrueValue Framework — Investor Report
gap_analysis_report.html        ·  TrueValue Framework — Gap Analysis & Research Agenda
implementation_cost_report.html ·  TrueValue Framework — Implementation Cost & Deployment Analysis
```

---

## frontend/csv/

CSV data catalogue viewer — no outbound navigation links.

```
index.html  ·  TV — CSV Catalog
```

---

## Redirect stubs (old URLs → new URLs)

All old paths now auto-redirect. Existing bookmarks and links continue to work.

| Old URL | Redirects to |
|---|---|
| `frontend/supply_chain/Supplychain.html` | `frontend/project/gold/supply_chain/index.html` |
| `frontend/supply_chain/dashboard.html` | `frontend/project/gold/supply_chain/dashboard.html` |
| `frontend/supply_chain/what_if_simulator.html` | `frontend/project/gold/supply_chain/what_if_simulator.html` |
| `frontend/value_chain/index.html` | `frontend/project/gold/value_chain/index.html` |
| `frontend/value_chain/dashboard.html` | `frontend/project/gold/value_chain/dashboard.html` |
| `frontend/value_chain/what_if_simulator.html` | `frontend/project/gold/value_chain/what_if_simulator.html` |
| `frontend/project/west_african_shea/supply_chain/dashboard.html` | `frontend/project/west_african_shea/supply_chain/dashboard.html` |
| `frontend/project/west_african_shea/supply_chain/what_if_simulator.html` | `frontend/project/west_african_shea/supply_chain/what_if_simulator.html` |
| `frontend/project/west_african_shea/supply_chain/project_context.html` | `frontend/project/west_african_shea/supply_chain/project_context.html` |
| `frontend/shea_value_chain/index.html` | `frontend/project/west_african_shea/value_chain/index.html` |
| `frontend/shea_value_chain/dashboard.html` | `frontend/project/west_african_shea/value_chain/dashboard.html` |
| `frontend/shea_value_chain/what_if_simulator.html` | `frontend/project/west_african_shea/value_chain/what_if_simulator.html` |

---

## Standalone tools

```
gametheory/gametheory_tholonic_sliders.html  ·  Tholonic Game Theory Simulator
frontend/docs/next_weeks_news.html            ·  Next Week's News
frontend/docs/next_weeks_poly.html            ·  Next Week's News (alternate)
```

---

## Navigation symmetry summary

Every commodity has the same page set at the same depth:

| | Supply Chain | Value Chain |
|---|---|---|
| **Gold** | `gold/supply_chain/` (index, dashboard, what_if) | `gold/value_chain/` (index, dashboard, what_if) |
| **West African Shea** | `west_african_shea/supply_chain/` (index, project_context, dashboard, what_if) | `west_african_shea/value_chain/` (index, dashboard, what_if) |

Cross-commodity navigation is always available in every page header.
Each commodity hub (`gold/index.html`, `shea/index.html`) links to both its layers.
The root `index.html` exposes all four entry points directly via the 2×2 grid.
