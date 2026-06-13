---
name: create-project
description: >
  End-to-end guide for creating a new project in this repo. Covers standalone
  supply-chain project hubs (gold/shea pattern) and basin ecosystem subprojects
  (Danube pattern). Consolidates rules from project-homepage-template,
  basin-subproject-architecture, rebuild-on-change, and add-homepage-section.
  Use when the user says "create a new project", "add a new hub", "scaffold a
  new supply chain", "set up a basin subproject", or "start a new project page".
---

# Create Project — End-to-End Skill

## Step 0 — Determine project type before doing anything else

Ask (or infer from context) which type applies:

| Type | Pattern | Rule that governs it |
|---|---|---|
| **A — Standalone hub** | Gold, Shea, AUBEB, Singapore NEWater, OCWD, Jackson Water, ERCOT Uri | `project-homepage-template.mdc` |
| **B — Basin subproject** | Danube natural/human/paired, any future basin | `basin-subproject-architecture.mdc` |

If the user mentions a basin (river, watershed, estuary) or an ecological service, use Type B.
Everything else is Type A.

For basin subprojects also determine: **natural**, **human**, or **paired** (see Type prefix table below).

---

## TYPE A — Standalone Hub

### A1. Folder structure

Create the following under `frontend/project/<slug>/`:

```
frontend/project/<slug>/
  index.html
  supply_chain/
    index.html
    dashboard.html
    project_context.html
    recycling_analysis.html      (required for ALL new projects — see A1a below)
    system_lifecycle.html        (only when maintenance/resilience is part of the case)
  value_chain/
    index.html                   (create even if value layer is deferred)
  data/
    processed/
      <slug>_supply_chain_ui.json     (generated)
      <slug>_system_lifecycle_ndc.json (generated, when lifecycle page exists)
```

### A1a. Recycling / Ecological Return Chain (required for all new projects)

Every new standalone project must include `supply_chain/recycling_analysis.html`. This page models the **TVPCI-R** (Ecological Return Chain): waste streams, byproduct recovery, and circular economy flows alongside the primary custody chain.

**Required elements:**
- **Concept panel:** explain TVPCI (D role), TVPCI-R (C role), and B_chain (N role) in project-specific terms
- **Three KPI cards:** TVPCI (primary chain balance), TVPCI-R (return chain score), B_chain (holon balance)
- **Delta bar:** visualises `Delta_chain = TVPCI - TVPCI_R` with signed imbalance label
- **Per-phase R_p cards:** one card per phase showing the recycling/return score, omega weight, zone label, and dominant waste stream description
- **Waste stream table:** phase, primary waste, volume/intensity, current disposal, recovery potential, R_p
- **Priority circular economy interventions table:** top 3-4 interventions with phase, intervention description, expected R_p impact, and bond/finance link

**R_p score derivation:**
```
R_p  = recycling/return score for phase p (0-100)
     = how observable and accountable the phase's ecological return is
omega_p = phase weight (proportional to waste volume and environmental impact; must sum to 1.0)
TVPCI_R = sum(omega_p * R_p) for all phases
B_chain = 100 * exp(-2 * |TVPCI - TVPCI_R| / max(TVPCI, TVPCI_R))
```

**Zone thresholds (phi-derived, same as N-D-C):**
- Coherent: R_p >= 80
- Stressed: 61.8 <= R_p < 80
- Failure: 38.2 <= R_p < 61.8
- Breakdown: R_p < 38.2

**What to include per commodity:**
- Identify the 2-3 highest-volume waste streams at the milling/processing phase (these carry highest omega_p)
- Identify the end-of-life packaging stream (consumer return)
- Identify the agricultural residue stream (cultivation phase)
- Note any existing circular economy infrastructure the project already uses (e.g. alperujo for olive oil, tailings for gold)
- Flag the weakest return phase (lowest R_p) as a bond intervention candidate

All R_p scores and omega weights on new projects may be labelled **PROVISIONAL** if no phase-resolved LCA data is available. The worksheet still must be populated with reasoned synthetic baselines derived from public sources.

### A2. Required homepage elements (`index.html`)

Every standalone hub page must include:

- Hero: kicker label, title, concise subtitle with phase count and analytical layer
- Four KPI cards using physical or N-D-C metrics (balance, avg N, bottleneck count, transparency gap, energy intensity, volume, hectares, etc.)
- Alert/insight panel explaining the defining structural issue (handoffs, loop closure, winterization failure, opacity, lifecycle bottleneck)
- Layer cards for Supply Chain, System Lifecycle, and Value Chain (use a "deferred" card if value analysis is not ready)
- Phase strip or explicit phase map (required when phase count > 5 or the system is a broken/infrastructure case)
- Phase-level N-D-C radar or spider chart for supply-chain phases
- Five-model coherence panel using the Gold/Shea/AUBEB pattern with π, φ, √2, ln(2), and e axes. If scenario data is not available, derive an explicit baseline from N-D-C data and label it as a baseline.
- Navigation back to main homepage and to related comparison projects

### A3. Processed JSON shape

The `_supply_chain_ui.json` file must include:

```json
{
  "_meta": {},
  "entities": { "synthetic": {} },
  "phase_meta": [
    { "name": "...", "transparency": "...", "transformation": "..." }
  ],
  "phases": { "synthetic": [] },
  "system": {
    "balance": 0,
    "average_N": 0,
    "bottleneck_phase_ids": [],
    "interpretation": "..."
  }
}
```

Each phase object inside `phases.synthetic` must include: `D`, `C`, `balance`, `N`, `sustainability`, `notes`, `data_quality`, and any key `metrics`.

### A4. N-D-C formulas (apply consistently)

```
balance       = 100 - (|D - C| / max(D, C)) * 100
N             = sqrt(D * C) * (balance / 100)
sustainability = 100 / ((|D - C|^2) + 10)
```

Status labels: 95–100 = Excellent (green), 80–94 = Good (teal), 60–79 = Fair (orange), < 60 = Poor (red).

### A5. Generate JSON

```bash
python3 src/api/generate_frontend_data.py
python3 src/api/generate_ui_data.py
```

Outputs land under `frontend/project/*/data/processed/`.

---

## TYPE B — Basin Ecosystem Subproject

### B1. Type prefix and naming

| Type | Prefix | Meaning |
|---|---|---|
| Natural | `natural_` | Ecological service cascade, no human infrastructure |
| Human | `human_` | Engineered supply chain from intake to delivery |
| Paired | `paired_` | Composite hub linking one natural and one human subproject |

Slug: lowercase, underscore-separated, must match folder name exactly.
Examples: `natural_freshwater_availability`, `human_irrigation_infrastructure`, `paired_agricultural_water`.

### B2. Folder structure (natural or human)

```
frontend/project/<basin>/<type_slug>/
  project.yaml
  index.html
  data/
    PDI_<material>_<basin>_<year>.yaml
    schema/
      <slug>_supply_chain_phases.csv
      <slug>_supply_chain_metrics.csv
    processed/
      <slug>_supply_chain_ui.json       (generated)
      <slug>_system_lifecycle_ndc.json  (generated)
  supply_chain/
    index.html
    dashboard.html
    project_context.html
    system_lifecycle.html
    scenarios.json                      (generated)
  value_chain/
    index.html
```

Paired hubs only need `index.html`. No PDI, no supply chain or value chain pages.

### B3. `project.yaml` — required fields

```yaml
id: <slug>
name: <Human-readable name>
basin: <basin_id>
type: natural | human
service_category: provisioning | regulating | habitat | cultural
teeb_class: <same as above>
description: >
  One-paragraph description with key volumes, countries, and bond relevance.
paired_with:
  natural: <natural_slug>   # for human subprojects
  hub: <paired_slug>
data_availability: H | M | L
primary_sources:
  - name: "Source name"
    url: "https://..."
    metrics: "what this source provides"
key_metrics:
  <metric_slug>: <value>
ndc_colors:
  primary: "#xxxxxx"
  dark: "#xxxxxx"
  light: "#xxxxxx"
created: "<ISO date>"
```

Color conventions: natural systems = greens, human freshwater = blues, human agriculture = dark greens, human energy/industrial = ambers, paired hubs = orange accent.

### B4. PDI YAML structure

File: `data/PDI_<material>_<basin>_<year>.yaml`

Must contain: `pdi` block with `material`, `analyst`, `date_completed`, `service_type`, `basin`, `paired_with`, `hub`; `sources_overview`; `geographic_scope`; `supply_chain_phases` (standard is 5 phases, each with `id`, `name`, `phase_category`, `physical_state_in/out`, `primary_transformation`, `typical_time_scale`, `transparency_level`, `measurable_output`, `output_unit`, `data_status`, `primary_sources`, `opacity_score`, `key_values`, `notes`); `ndc_derivation` (D, C, balance, N, sustainability per phase); `coherence_scores` (pi, phi, sqrt2, ln2, e); `analyst_notes`.

NDC derivation formulas:
```
D = 200 + (D_flags × 20) + (boundary_score × 4)
C = 200 + (C_flags × 20) + (opacity × 8)
N = round((D + C) / 2 × (balance / 100))
```

Balance by transparency: High = 88–97%, Medium = 78–87%, Low = 65–77%.

### B5. CSV schema files

**`<slug>_supply_chain_phases.csv`** columns (in order):
`phase_id, phase_name, phase_category, physical_state_in, physical_state_out, primary_transformation, typical_time_scale, transparency_level, measurable_output, output_unit, D_parameters, C_parameters, data_status, notes`

**`<slug>_supply_chain_metrics.csv`** columns (in order):
`record_id, phase_id, entity, country, date, metric_name, metric_value, unit, source_type, source_name, url, notes`

`source_type` values: `public`, `paid`, `private`, `inferred`. One row per quantitative claim in the PDI.

### B6. Generate JSON for a basin subproject

Add an entry to `NDC_DATA` and `PHASE_NOTES` in `scripts/generate_danube_data.py`, then:

```bash
python3 scripts/generate_danube_data.py --subproject <slug>
# or to regenerate all:
python3 scripts/generate_danube_data.py --all
```

Outputs: `data/processed/<slug>_supply_chain_ui.json`, `data/processed/<slug>_system_lifecycle_ndc.json`, `supply_chain/scenarios.json`.

### B7. Required HTML pages (basin subproject)

Six pages for natural/human subprojects:
1. `index.html` — kicker, title with type badge, KPI strip, alert panel, paired panel, three layer cards, navigation
2. `supply_chain/index.html` — chain average balance and bottleneck phase in subtitle
3. `supply_chain/dashboard.html` — dark theme, KPIs, bottleneck alert, phase D-C-N bars, coherence pentagon, phase table
4. `supply_chain/project_context.html` — light theme, KPI strip, phases table, country breakdown, bond opportunity analysis, risk factors, data sources
5. `supply_chain/system_lifecycle.html` — dark theme, lifecycle KPI grid, phase bars from JSON, three-paragraph infrastructure interpretation
6. `value_chain/index.html` — light theme, e-layer score, revenue/cost table, bond structure table, five-model value context table

Paired hub: `index.html` only, with composite index, interactive weighting slider, bond grade, two component cards, links to both subprojects.

### B8. After adding a basin subproject, update the basin hub

1. Add a new "Active Pilot" section to `frontend/project/<basin>/index.html`
2. In the "Full System Map" section, change the card from `class="coming-card"` to `class="coming-card active"` (natural/human) or `class="coming-card active-paired"` (paired)
3. Update the composite index card to show the new default score and bond grade
4. If a bond page exists (`<basin>_basin_bond.html`), update it following the Bond Prospectus Update Rule in `basin-subproject-architecture.mdc`

Bond grade thresholds: ≥95% = AAA, ≥90% = AA+, ≥86% = AA, ≥82% = AA-, ≥78% = A+, ≥74% = A, ≥70% = A-, ≥65% = BBB+, ≥60% = BBB, <60% = BBB-.

---

## Step 3 — Add project to the homepage (all types)

Use the **`add-homepage-section` skill** for this step. Two paths:

- The new project needs a card in the top project grid: follow **Type A** in that skill (update `frontend/site-index.json > projects` and `frontend/homepage-layout.json`).
- The project is a new hub section below the grid: follow **Type B** in that skill (update `site-index.json`, `index.html` CSS/HTML/JS).

Also update `tree.md` to record the new folder in the repo tree.

---

## Step 4 — Post-creation rebuild

| What was created | Required action |
|---|---|
| New standalone project hub | Update `index.html` project card + update `tree.md` |
| Full new project with PDI + data + HTML | `RUN_GENERATE_UI=1 ./scripts/rebuild-site.sh` |
| Existing HTML page modified during creation | Check all pages that link to it; update stale hrefs |

Every new page must link back to its hub and to the main homepage. Every hub page that should link to the new page must be updated.

---

## Step 5 — Final checklist (required before marking complete)

- [ ] All required HTML pages exist and load without errors
- [ ] `supply_chain/recycling_analysis.html` exists with TVPCI-R scores, B_chain, waste stream table, and intervention table
- [ ] TVPCI-R is labelled PROVISIONAL if no phase-resolved LCA data is available
- [ ] JSON data files generated successfully (no "Loading..." states in browser)
- [ ] `project.yaml` exists with all required fields (basin subprojects)
- [ ] PDI YAML exists with all phases populated; no OPAQUE phases without explanation (basin subprojects)
- [ ] NDC derivation values in PDI match values in the data generation script (basin subprojects)
- [ ] Both CSV schema files exist with at least one row per phase in the metrics CSV (basin subprojects)
- [ ] Homepage card or hub section added and JSON validates: `python3 -m json.tool frontend/site-index.json > /dev/null`
- [ ] `tree.md` updated
- [ ] Bottleneck alert text explains structural cause, not just phase name
- [ ] Five-model coherence panel present on hub page
- [ ] `supply_chain/project_context.html` contains a **Phase Intervention Worksheet** section per `intervention-worksheet.mdc`: provisional disclaimer, five-axis failure diagnosis table with chain scores, one worksheet block per bottleneck phase (balance below 61.8%), per-intervention D/C effect estimates, and combined effect estimate. This is mandatory — the page is incomplete without it.
- [ ] All pages have nav links back to hub and to main homepage
- [ ] No em-dashes anywhere in any file (use commas, colons, or separate sentences)
- [ ] `color-scheme: light` declared in all light-themed pages to prevent browser dark-mode override
- [ ] Rebuild step run and no broken links remain

---

## Key files at a glance

| File | Purpose |
|---|---|
| `frontend/site-index.json` | Homepage card data (single source of truth for project grid) |
| `frontend/homepage-layout.json` | Category groupings for project grid |
| `index.html` (repo root) | Main homepage HTML/JS renderer |
| `tree.md` | Repo file tree record |
| `src/api/generate_frontend_data.py` | Generates standalone project JSON |
| `src/api/generate_ui_data.py` | Generates UI JSON |
| `scripts/generate_danube_data.py` | Generates basin subproject JSON |
| `scripts/rebuild-site.sh` | Full rebuild (run with `RUN_GENERATE_UI=1` when CSVs change) |

## Rules this skill consolidates

- `.cursor/rules/project-homepage-template.mdc` — standalone hub page structure and JSON shape
- `.cursor/rules/basin-subproject-architecture.mdc` — basin subproject folder, PDI, CSV, HTML, and bond page requirements
- `.cursor/rules/rebuild-on-change.mdc` — post-creation rebuild steps and cross-reference obligations
- `.cursor/rules/tv-project-workflow.mdc` — schema-first principle, data flow, and dev server commands
- `.cursor/skills/add-homepage-section/SKILL.md` — homepage registration for new projects
