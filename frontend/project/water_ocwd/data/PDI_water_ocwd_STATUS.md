---
doc_id: frontend_docs_pdi_pdi_water_ocwd_status
title: "PDI Status Report — water_ocwd (Orange County Water District GWRS)"
type: status_report
status: active
domain: pdi
layer: methodology
projects:
  - water_ocwd
tags:
  - methodology
  - pdi
  - water
  - water_ocwd
related_docs:
  []
key_claims:
  []
---

# PDI Status Report — water_ocwd (Orange County Water District GWRS)
# Generated: 2026-04-22
# Analyst: AI (Claude Sonnet 4.6)

## 1. New Fields Added to PDI_TEMPLATE.yaml

| Field name | Location | YAML syntax | Reason added | Chain types |
|---|---|---|---|---|
| `tvpci_notes` | `module_3.phase_map[n]` | `tvpci_notes: ""` | Captures TVPCI and Tholonic integration notes per confirmed phase | All chain types with TVPCI modelling |

**SYNC PENDING**: `tvpci_notes` field not yet added to `PDI_TEMPLATE.yaml`, `frontend/PDI.html`, or `PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md`. (Same pending item as `PDI_water_newwater_STATUS.md`.)

---

## 2. Missing Data — High Priority

| ID | Missing item | YAML field affected | Impact if absent |
|---|---|---|---|
| M01 | OCWD GWRS disaggregated treatment cost (MF, RO, UV/H₂O₂ separately) | `summary.analyst_notes` | Total cost ~USD 1.25/m³ from OCWD operational data; breakdown by process component not published. Impact: moderate for value chain modelling. |
| M02 | OC San / OCWD secondary effluent supply agreement (volume, price, quality terms) | `module_2_events[10]` (Event 10 handoff) | Supply agreement exists but financial terms not public. Volume (130 MGD feed to GWRS) is published; price per unit not published. Impact: high for value chain D-C cost attribution. |
| M03 | Individual municipal agency groundwater pumping volumes from OCWD basin (agency-level breakdown) | `module_2_events[13].B11_approximate_volume` | Aggregate basin extraction published (280,000 AF/yr); per-agency breakdown requires CDWR annual reports with 12–18 month lag. Impact: moderate for Phase 11 loop closure verification. |
| M04 | Service reservoir storage aggregate for Orange County (across ~30 agencies) | `module_2_events[5].B11_approximate_volume` | No single source aggregates Phase 3 storage across all agencies; Phase 3 opacity score correctly set to 1 (low transparency). Impact: high for Phase 3 N calculation; confirmed by low-transparency classification. |

---

## 3. Missing Data — Medium / Low Priority

| ID | Missing item | YAML field affected | Notes |
|---|---|---|---|
| L01 | OCWD GWRS capital expenditure by phase (Phase 1 2008, Phase 2 2015, Phase 3 2023) | `programme_scale.total_budget_USD` | Industry estimate ~USD 480M total; OCWD has not published disaggregated capex per expansion phase. |
| L02 | OC San annual energy consumption at Plant No. 1 and Plant No. 2 (separately) | Phase 6–7 energy data | OC San publishes total energy; plant-level breakdown not in public reports. |
| L03 | Per-agency non-revenue water rates across ~30 Orange County water agencies | Phase 3–4 leakage data | Aggregate ~8–10% NRW estimated from CDWR benchmarks; agency-level variation not compiled. |
| L04 | Groundwater travel time from GWRS injection to municipal pump (residence time in basin) | Phase 11 loop closure notes | Estimated 2–6 months from published OCWD studies; precise per-well data not available publicly. |

---

## 4. Analyst Observations

**Key structural anomaly — Phase 3 low transparency:** This PDI produces one low-transparency phase (Phase 3: service reservoir), which is unusual for a US regulated utility chain. The low rating is structurally correct: fragmentation across ~30 municipal water agencies means no single source can confirm aggregate storage or distribution input. This is an institutional opacity, not a physical one. It correctly flags the D-C cost of actor fragmentation at a phase that is high-transparency in the NEWater instance (Phase 3: medium).

**Two inter-institutional handoffs confirmed:**
1. Event 10 (Phase 7/8 boundary): OC San → OCWD. B9=true, B10=true. This is the largest D-C discontinuity in the chain. The D/C/N derivation formula should produce noticeably lower balance at this phase than in water_newwater Phase 8 (B9=false, B10=false).
2. Event 13 (Phase 11): OCWD → multiple municipal agencies via shared groundwater commons. B9=true, B10=true. Second discontinuity; structurally different from NEWater loop closure.

**Broken tholonic recursion at Phase 11:** The Phase 11 child-N cannot cleanly become the Phase 0 parent-N because the loop passes through a shared groundwater commons and ~30 independent agencies. The `generate_project_data.py` script should implement a loop-closure integrity flag: `loop_closure_intact: false` for water_ocwd (vs. `true` for water_newwater). This flag should be readable by the comparative analysis page.

**Supply agreement opacity (M02):** The financial terms of the OC San / OCWD secondary effluent supply agreement are not publicly available. This means the cost attribution between Phase 7 (OC San secondary treatment) and Phase 8 (OCWD advanced treatment) cannot be independently verified from public sources. The ~USD 1.25/m³ total OCWD treatment cost likely subsumes the OC San supply cost; the split is OPAQUE. This is correctly reflected in Phase 7 `tvpci_notes`.

**SYNC PENDING items:** `tvpci_notes` field synchronisation (same as water_newwater — one sync action covers both instances).

**Cross-reference with water_newwater:** All phase numbers, event numbering, and B-flag conventions are identical between this instance and `PDI_water_newwater_2026.yaml`. The two instances are designed to be directly comparable row-for-row through the `generate_project_data.py` derivation pipeline. Any change to phase numbering in one instance must be mirrored in the other.
