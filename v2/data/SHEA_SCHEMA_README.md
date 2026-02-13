# Shea Supply Chain – Phase-Resolved, Custody-Aware, Schema-First Template

This folder contains a **template** for the shea (shea butter) supply chain in a phase-resolved, custody-aware, schema-first form. Cells are **populated only where information is present** in the source (Clarity Coalition Cleo Shea True Value page and cited references); **missing areas are left blank** or marked **OPAQUE**.

## Conventions

| Convention | Meaning |
|------------|--------|
| **Blank cell** | No value; information not in source. |
| **OPAQUE** (in `data_status` or in a cell) | Explicitly marked as unknown or not disclosed; structural gap. |
| **POPULATED** | Value or classification filled from source. |
| **PARTIAL** | Some fields filled; others missing for that row/phase. |

## Files

| File | Purpose |
|------|--------|
| **shea_supply_chain_phases.csv** | Phase definitions: phase_id, physical_state in/out, transformation, time_scale, transparency, measurable_output. Blank where not stated. |
| **shea_phase_metrics.csv** | Metrics per phase: metric_name, value, unit, source, custodian, data_status. Rows with values = POPULATED; missing metrics use OPAQUE or blank value. |
| **shea_custody_and_flow.csv** | Flows between phases: from_phase, to_phase, custodian_from/to, ownership_change, custody_change, physical_move, volume. Most custody/ownership cells blank; data_status indicates OPAQUE where applicable. |
| **shea_data_sources.csv** | Source registry: source_name, source_type, phase_coverage, url. Includes Clarity public and internal (password-protected) sources. |
| **shea_fund_and_project_context.csv** | Fund/project figures: BF 2021; Senegal (€25M, €50M Y10, 35M trees, 3774 T p.a., 40/60 equity/debt); Acorn pilot 50, 100k potential, 1 ha, PAPSEN 400 ha; George Comments (area, pop, GGW ha); SDG baseline/target; additionality. |
| **shea_plantation_sites_senegal.csv** | Plantation site list from EP Carbon (site_id, site_name, region); 31+ sites; Primary/Secondary Area (Ha) in source. |
| **EXTRACTED_SHEA_DATA_SUMMARY.md** | Summary of data extracted from Mirova, Acorn Onboarding, Serious Shea BPlan V8 PDFs. |
| **UNINTEGRATED_FILES_QUICK_VIEW.md** | Quick view of unintegrated files and suggested actions. |

## Phases (summary)

| phase_id | Phase name | Populated from source | Gaps (blank/OPAQUE) |
|----------|------------|------------------------|----------------------|
| 0 | Collection | Geography (BF, West Africa); 94% women; 3M employed; season May–Oct 5 months | Transparency; D/C parameters; volume per collector |
| 1 | First sale / aggregation | Sellers; 150 US$/MT; 425 US$/MT nuts; 250 CFA/kg | Custodian chain; volume |
| 2 | Trading / bulking | Traders 250, large exporters 250–800 US$/MT | Custody; volume; transparency |
| 3 | Processing (to butter) | 7 bags→187 kg; 0.53 MT/woman/month; 925 kg/woman/season; BAU vs 100% renewable | D/C parameters; exact custodian at each step |
| 4 | Export | 265k–445k t/year region; 90–200M US$ BF; ~50% consumed in region | Route; custodian; ownership change |
| 5 | Manufacturing | 95% shea; 100% renewable (Cleo) | Location; custodian; throughput |
| 6 | Retail | SKU sizes; 30 US$/30g; 4k vs 47.5k US$/MT to women | Transparency tag |

## Custody and flow

- **shea_custody_and_flow.csv** has one row per flow (0→1, 1→2, … 5→6). Columns **custodian_from**, **custodian_to**, **ownership_change**, **custody_change**, **physical_move**, **typical_volume** are left **blank** unless inferable from the source; **data_status** or notes use **OPAQUE** where the gap is explicit.
- Only flow 6 (manufacturer → consumer) has partial population (custody and physical move to consumer implied).

## Use

- **Add data**: Fill blank cells or new rows when new sources provide phase-level, custody-level, or metric-level data.
- **Keep separation**: Price/income are in metrics for traceability but supply chain focus remains physical flow, custody, and constraints; value chain stays in a separate layer.
- **Mark gaps**: When a field cannot be filled, leave it blank and set `data_status = OPAQUE` (or add a note) so the gap is auditable.

## Source of populated data

All populated values are traceable to the Clarity Coalition page **True Value Carbon – Cleo Shea Value Chain (Updated 2020)** and the references it cites (FAO 2017, US AID 2013, Rousseau et al. 2015, Yinug & Fetzer 2008, Lovett, US Aid). See **docs/Clarity_Cleo_Shea_Value_Chain_Outline.md** for the extracted narrative and tables.
