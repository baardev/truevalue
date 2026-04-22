# HTML Page Tree

All HTML pages in the project, organised by the new commodity-first hierarchy.
Arrows (→) show outbound navigation links. `/index.html` is the root landing page.

---

## Structure overview

```
index.html                          Root — 2×2 grid
├── frontend/project/gold/index.html        Gold commodity hub
│   ├── supply_chain/index.html     Gold Supply Chain hub
│   │   ├── dashboard.html
│   │   └── what_if_simulator.html
│   └── value_chain/index.html      Gold Value Chain hub
│       ├── dashboard.html
│       └── what_if_simulator.html
└── frontend/project/shea/index.html        Shea commodity hub
    ├── supply_chain/index.html     Shea Supply Chain hub
    │   ├── project_context.html
    │   ├── dashboard.html
    │   └── what_if_simulator.html
    └── value_chain/index.html      Shea Value Chain hub
        ├── dashboard.html
        └── what_if_simulator.html
```

Every page follows a uniform depth: **Root → Commodity hub → Layer hub → View**.

---

## Root

```
index.html  ·  TV Project Home — True Value Analytics
├── → frontend/project/gold/supply_chain/index.html
├── → frontend/project/gold/value_chain/index.html
├── → frontend/project/shea/supply_chain/index.html
├── → frontend/project/shea/value_chain/index.html
├── → frontend/project/gold/index.html     (Gold Hub shortcut)
├── → frontend/project/shea/index.html     (Shea Hub shortcut)
└── → frontend/csv/index.html
```

---

## frontend/gold/

Gold commodity hub and its two layers.

```
index.html  ·  Gold – Supply & Value Chain Hub
├── → supply_chain/index.html
├── → supply_chain/dashboard.html
├── → supply_chain/what_if_simulator.html
├── → value_chain/index.html
├── → value_chain/dashboard.html
├── → value_chain/what_if_simulator.html
├── → ../shea/index.html
└── → /index.html
```

### frontend/project/gold/supply_chain/

```
index.html  ·  Gold Supply Chain – Intelligence Platform
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (Gold Hub)
├── → ../../shea/supply_chain/index.html
└── → /index.html

dashboard.html  ·  Gold Supply Chain Intelligence – Main Dashboard
├── → ../../shea/index.html
└── → /index.html

what_if_simulator.html  ·  What-If Simulator – Gold Supply Chain
├── → dashboard.html
├── → ../../shea/index.html
└── → /index.html
```

### frontend/project/gold/value_chain/

```
index.html  ·  Gold Value Chain – Intelligence Platform
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (Gold Hub)
├── → ../../shea/value_chain/index.html
└── → /index.html

dashboard.html  ·  Value Chain Dashboard
├── → what_if_simulator.html
├── → ../../shea/value_chain/dashboard.html
└── → /index.html

what_if_simulator.html  ·  Value Chain What-If Simulator
├── → dashboard.html
└── → /index.html
```

---

## frontend/shea/

Shea commodity hub and its two layers.

```
index.html  ·  Shea – Supply & Value Chain Hub
├── → supply_chain/index.html
├── → supply_chain/project_context.html
├── → supply_chain/dashboard.html
├── → supply_chain/what_if_simulator.html
├── → value_chain/index.html
├── → value_chain/dashboard.html
├── → value_chain/what_if_simulator.html
├── → ../gold/index.html
└── → /index.html
```

### frontend/project/shea/supply_chain/

```
index.html  ·  Shea Supply Chain – True Value (Real-World Example)
├── → project_context.html
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (Shea Hub)
├── → ../../gold/supply_chain/index.html
└── → /index.html

project_context.html  ·  Shea – Project Context & Impact
├── → index.html
├── → dashboard.html
├── → what_if_simulator.html
├── → ../../gold/supply_chain/index.html
└── → /index.html

dashboard.html  ·  Shea Supply Chain – Dashboard
├── → index.html
├── → project_context.html
├── → what_if_simulator.html
├── → ../../gold/supply_chain/index.html
└── → /index.html

what_if_simulator.html  ·  What-If Simulator – Shea Supply Chain
├── → dashboard.html
├── → index.html
├── → project_context.html
├── → ../../gold/supply_chain/index.html
└── → /index.html
```

### frontend/project/shea/value_chain/

```
index.html  ·  Shea Value Chain – Intelligence Platform
├── → dashboard.html
├── → what_if_simulator.html
├── → ../index.html            (Shea Hub)
└── → /index.html

dashboard.html  ·  Shea Value Chain Dashboard
├── → what_if_simulator.html
└── → /index.html

what_if_simulator.html  ·  Shea Value What-If Simulator
├── → dashboard.html
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
| `frontend/shea/dashboard.html` | `frontend/project/shea/supply_chain/dashboard.html` |
| `frontend/shea/what_if_simulator.html` | `frontend/project/shea/supply_chain/what_if_simulator.html` |
| `frontend/shea/project_context.html` | `frontend/project/shea/supply_chain/project_context.html` |
| `frontend/shea_value_chain/index.html` | `frontend/project/shea/value_chain/index.html` |
| `frontend/shea_value_chain/dashboard.html` | `frontend/project/shea/value_chain/dashboard.html` |
| `frontend/shea_value_chain/what_if_simulator.html` | `frontend/project/shea/value_chain/what_if_simulator.html` |

---

## Standalone tools

```
gametheory/gametheory_tholonic_sliders.html  ·  Tholonic Game Theory Simulator
docs/next_weeks_news.html                    ·  Next Week's News
docs/next_weeks_poly.html                    ·  Next Week's News (alternate)
```

---

## Navigation symmetry summary

Every commodity has the same page set at the same depth:

| | Supply Chain | Value Chain |
|---|---|---|
| **Gold** | `gold/supply_chain/` (index, dashboard, what_if) | `gold/value_chain/` (index, dashboard, what_if) |
| **Shea** | `shea/supply_chain/` (index, project_context, dashboard, what_if) | `shea/value_chain/` (index, dashboard, what_if) |

Cross-commodity navigation is always available in every page header.
Each commodity hub (`gold/index.html`, `shea/index.html`) links to both its layers.
The root `index.html` exposes all four entry points directly via the 2×2 grid.
