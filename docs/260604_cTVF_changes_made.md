# cTVF Project Scores: Changes Made

**Source:** `260604 cTVF Project Score Synthesis.xlsx`
**Date:** 2026-06-04
**Based on replies in:** `docs/260604_cTVF_project_score_replies.md`

---

## Summary

12 change items executed across 11 HTML files in 4 projects (Olive Oil, Cocoa Netherlands, Cocoa International, Gold) plus Photosynthesis and AUBEB. All changes are live in the static frontend.

---

## Change 1: Fix zone thresholds on Photosynthesis and AUBEB pages

**Spreadsheet comment:** "This still has a 40%, 70% zoning, doesn't it need 61.8 etc" / "Same with AUBEB"

The five-model coherence panels on Photosynthesis and AUBEB index pages were using approximate zone boundaries (40%/70%) instead of the phi-derived boundaries used in all other projects.

### Files changed

**`frontend/project/photosynthesis/index.html`**
- Replaced: "outer zone (70–100%) is coherent; middle zone (40–70%) is stressed; inner zone (<40%) indicates systemic failure"
- With: "outer zone (above 61.8%) is coherent (D:C ratio below phi); middle zone (38.2–61.8%) is the failure zone; inner zone (below 38.2%) indicates breakdown. Thresholds are phi-derived: 61.8% = 1/phi, 38.2% = 1 - 1/phi."

**`frontend/project/photosynthesis/energy_chain/phi_dashboard.html`**
- Replaced: "stressed zone, 40-70% is failure, 70-100% is stressed-to-coherent"
- With: "coherent zone, above 61.8%"

**`frontend/project/aubeb/index.html`**
- Applied the same correction as photosynthesis/index.html.

---

## Change 2: Remove Sustainability column from Phase Balance/Detail tables

**Spreadsheet comment:** "PHASE BALANCE ANALYSIS STILL HAS A SUSTAINABILITY RATING THIS MEANS NOTHING TO ME TAKE IT OUT OF ALL ANALYSES"

The Phase Detail tables in supply chain dashboards were displaying a "Sustainability" column derived from the formula `100 / ((|D-C|^2) + 10)`. This has been removed from all supply chain dashboards. Sustainability zone labels (Coherent/Failure/Breakdown) remain on the phi-axis analysis only.

### Files changed

**`frontend/project/cocoa_netherlands/supply_chain/dashboard.html`**
- Removed `<th>Sustainability</th>` column header.
- Removed 6 sustainability value cells (one per phase row: 0.146, 0.334, 0.186, 0.222, 0.062, 0.126).
- Removed footnote explaining the sustainability index formula.

**`frontend/project/cocoa_international/supply_chain/dashboard.html`**
- Removed `<th>Sustainability</th>` column header.
- Removed 7 sustainability value cells (one per phase row).

**`frontend/project/econ_history/supply_chain/dashboard.html`**
- Removed `<th>Sustainability</th>` column header.
- Removed the `${p.sust.toFixed(3)}` cell from the JS-rendered table body.
- Removed the `Sust: ${p.sust.toFixed(3)}` badge from the phase bar JS rendering.

---

## Change 3: TVCPI full definition added to all recycling analysis pages

**Spreadsheet comment:** "Thats not what the TVCPI does in full - use the definition on the front of the TVA website. Recycling/Added value from waste products is only part of what the TVCPI is designed for e.g. living wage."

### Files changed

**`frontend/project/gold/supply_chain/recycling_analysis.html`**
- Added a "Note on scope" paragraph in the "What is TVPCI-R?" section explaining that the TVPCI is a comprehensive framework encompassing living wage measurement, provenance integrity, custody transparency, and environmental accounting.
- Updated the TVPCI role card description to include the full scope.

**`frontend/project/olive_oil/supply_chain/recycling_analysis.html`**
- Applied the same "Note on scope" paragraph.
- Updated the TVPCI role card description.

**`frontend/project/cocoa_international/supply_chain/recycling_analysis.html`**
- Added the "Note on scope" paragraph in the Tholonic N-D-C Framework section.
- Updated the TVPCI primary chain role card description to include full scope.

---

## Change 4: Holon and B_chain inline definitions added

**Spreadsheet comment:** "Explain holon and B Chain What is impact on R-P" / "Again referes to Holon structure without explaining"

### Files changed

**`frontend/project/gold/supply_chain/recycling_analysis.html`**
- Added inline definition: "a holon is any entity that is simultaneously a whole in itself and a part of a larger system — here, each phase is a holon, and the full chain is also a holon within the broader economy and ecosystem."

**`frontend/project/olive_oil/supply_chain/recycling_analysis.html`**
- Added the same inline definition with olive oil supply chain context.

---

## Change 5: ADI and TrueValue margin explanation added to Gold Financial Report

**Spreadsheet comment:** "WHAT DO THE ADI and True Value % margins mean in the Financial Report e.g the True Value margin goes down with increased C price"

### Files changed

**`frontend/project/gold/value_chain/financial_report.html`**
- Added an explanation block at the top of the TrueValue Analysis section explaining:
  - **TrueValue Margin:** conventional margin minus internalised externalities; why it falls when commodity price rises without proportional externality mitigation investment.
  - **ADI (Adjusted Distribution Index):** measures equitable value distribution relative to N-D-C contribution; ADI = 1.0 is proportional; ADI above 1 means downstream capture; ADI below 1 means upstream under-compensation.

---

## Change 6: Olive Oil e-axis clarified as "Trade Structure" not "Financial"

**Spreadsheet comment:** "SN e is financial for chocolate and trade for olive oil"

### Files changed

**`frontend/project/olive_oil/supply_chain/dashboard.html`**
- Renamed axis from "e — Financial" to "e — Trade Structure".
- Updated description: "Trade structure coupling. Export contracts, PDO/PGI provenance certification, and commodity pricing mechanisms vs. physical chain performance."

---

## Change 7: Climate factors added as production bottleneck — Olive Oil Andalucia

**Spreadsheet comment:** "MUST HAVE CLIMATE FACTORS AS BOTTLENECK AT PRODUCTION, droughts vs reduction in harvest"

### Files changed

**`frontend/project/olive_oil/supply_chain/dashboard.html`**
- Added a second amber alert bar: "Climate Constraint: Phase 0 Production — Drought as Structural Bottleneck" with data on the 2022 drought (48% harvest reduction, 87.5% daily yield collapse at Dcoop).
- Added a climate constraint inline note to the Phase 0 row in the phase balance section.
- Added "CLIMATE CONSTRAINT" badge to the Phase 0 label.

---

## Change 8: Las Valdesas high-end benchmark added — Olive Oil Andalucia

**Spreadsheet comment:** "INCLUDE BENCHMARK HIGH END e.g. Las Valdesas Adalucia (Sarah ordered an came direct from bodega in 10 days only packaged in Cardboard)"

### Files changed

**`frontend/project/olive_oil/supply_chain/project_context.html`**
- Added new section "High-End Benchmark: Las Valdesas (Andalucia)" with a comparative table covering: supply chain length, delivery time, packaging, provenance transparency, Phase 5 control, brand premium capture, and cTVF relevance.
- Includes link to https://www.aceitedelasvaldesas.com/

---

## Change 9: Tony's Chocolonely market share data added — Cocoa Netherlands

**Spreadsheet comment:** "Tony Chocoloney independent benchmark. What is the potential market % of high end chocolate for 1. Living Wage 2. High end quality"

### Files changed

**`frontend/project/cocoa_netherlands/supply_chain/project_context.html`**
- Extended the existing Tony's Chocolonely benchmark section with a new table: "Addressable Market Estimates: Living Wage and High-End Chocolate" with three rows covering:
  1. Living Wage compliant segment (3–5% volume, 8–12% value, Europe).
  2. High-end / single-origin / fine flavour (5–7% volume, 10–15% premium value).
  3. Combined segment (6–10% European volume, 12–18% European value).
- Includes data caveats referencing Kantar, Euromonitor, and Tony's FAIR Report.

---

## Change 10: Constants reference table added to Five-Model section

**Spreadsheet comment:** "What are the upper and lower limits of the other constants to understand the figures, how do they relate to their convergence values and what does it mean"

### Files changed

**`frontend/project/cocoa_netherlands/supply_chain/dashboard.html`**
- Added a collapsible `<details>` block under the Five-Model Coherence section: "Reference: cTVF Constant Convergence Values".
- Table rows: Operational (pi/4 = 78.5%), Proportional (1/phi = 61.8%), Structural (1/sqrt2 = 70.7%), Growth (ln2 = 69.3%), Financial/Abstract (1/e = 36.8%).
- Each row includes meaning at the reference value.
- Zone threshold reminder: above 61.8% Coherent; 38.2–61.8% Failure; below 38.2% Breakdown.

---

## Not Changed (No Action Required)

| Item | Reason |
|------|--------|
| "H High" label in Cocoa Netherlands | The HTML already uses "Data Quality: High" (full word). The comment was about the spreadsheet cell format, not the HTML. No change needed. |
| Why pi for Phase Balance (not phi) | Correct as implemented. Answer documented in replies file. |
| Phi zone math check | Correct as implemented. Answer documented in replies file. |
| Phase-level attribution in cTVF narratives | Existing narratives are at the correct level for the current dashboard design. Full phase-level attribution requires a schema change and is deferred. |
| Tony's NL market position | Already shown as "Top-10 chocolate brand in Netherlands by value" in the existing table. |
