---
doc_id: frontend_docs_pdi_pdi_water_newwater_status
title: "PDI Status Report — water_newwater (Singapore PUB NEWater)"
type: status_report
status: active
domain: pdi
layer: methodology
projects:
  - water_newwater
tags:
  - methodology
  - pdi
  - water
  - water_newwater
related_docs:
  []
key_claims:
  []
---

# PDI Status Report — water_newwater (Singapore PUB NEWater)
# Generated: 2026-04-22
# Analyst: AI (Claude Sonnet 4.6)

## 1. New Fields Added to PDI_TEMPLATE.yaml

| Field name | Location | YAML syntax | Reason added | Chain types |
|---|---|---|---|---|
| `tvpci_notes` | `module_3.phase_map[n]` | `tvpci_notes: ""` | Captures TVPCI and Tholonic integration notes per confirmed phase; enables direct generation of comparative analysis content without re-parsing event records | All chain types with TVPCI modelling |

**SYNC PENDING**: `tvpci_notes` field not yet added to `PDI_TEMPLATE.yaml`, `frontend/PDI.html`, or `PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md`.

---

## 2. Missing Data — High Priority

| ID | Missing item | YAML field affected | Impact if absent |
|---|---|---|---|
| M01 | Individual waterworks intake volumes (daily ML/day per plant) | `module_2_events[2].B11_approximate_volume` | Phase 1 volume is aggregate only; per-plant breakdown unavailable from public sources. Impact: minor — aggregate is sufficient for D/C/N derivation. |
| M02 | Individual service reservoir capacities (ML per reservoir) | `module_2_events[5].B11_approximate_volume` | Phase 3 volume flagged as UNKNOWN at reservoir level. PUB publishes distribution input but not per-reservoir storage. Impact: moderate for Phase 3 N calculation; workaround: use aggregate distribution input. |
| M03 | NEWater treatment cost breakdown (disaggregated: MF, RO, UV separately) | `summary.analyst_notes` | Total treatment cost ~SGD 1.18/m³ estimated from OECD (2012) and PUB tariff structure; not directly published by PUB as a per-process cost. Source quality: medium. |
| M04 | DTSS flow metering data at individual junction points | `module_2_events[7].B11_approximate_volume` | Phase 5 volume uses aggregate WRP inlet data; DTSS intermediate flow points not published. Impact: low. |

---

## 3. Missing Data — Medium / Low Priority

| ID | Missing item | YAML field affected | Notes |
|---|---|---|---|
| L01 | NEWater factory-level production volumes (Bedok, Kranji, Seletar, Ulu Pandan, Changi individually) | `module_2_events[10].B11_approximate_volume` | PUB publishes total 900 ML/day; per-factory split not published. Low impact. |
| L02 | Blending ratio of NEWater in Bedok and Kranji reservoirs (% NEWater vs. conventional treated water) | `module_2_events[13].B11_approximate_volume` | PUB publishes total volumes but not blending ratios per reservoir. Low impact for supply chain modelling. |
| L03 | Singapore NEWater capital expenditure (total and per-factory) | `programme_scale.total_budget_USD` | PUB does not publish disaggregated capex for NEWater factories. Industry estimates ~SGD 3–5B total across 5 factories; not verified. |
| L04 | Percentage of NEWater used for industrial non-potable vs. reservoir blending (split) | Phase 11 distribution | Annual Report gives broad range; precise split not published at phase level. |

---

## 4. Analyst Observations

**Loop closure structural note:** This is the first PDI instance in this project to describe a fully closed-loop supply chain (Phase 11 → Phase 0 via reservoir replenishment). The `tvpci_notes` field was added specifically to capture the Tholonic loop-closure significance. Future PDI completions for circular or recycling chains should use this field.

**Single-actor dominance:** The absence of inter-institutional handoffs in this chain (all phases: PUB) creates an unusual PDI profile. All B9 flags in Events 3–12 are false except Events 6–7 (consumer delivery and wastewater collection handoffs). This results in lower average C_flags in the D/C/N derivation for the recycling phases (5–11), which may understate the actual integration benefit of single-actor operation. The `generate_project_data.py` script should apply a coherence bonus to chains with zero inter-institutional handoffs in the recycling loop — this is not currently in the pipeline formula and should be considered for the template.

**SYNC PENDING items:** `tvpci_notes` field synchronisation to template, HTML form, and protocol document has been flagged above (M01) and must be completed before this PDI instance is used as a reference for the Abstract Supply Chain Phase Template.

**Comparison validity:** This PDI instance is designed to be compared against `PDI_water_ocwd_2026.yaml`. The two PDIs use identical phase numbering, event numbering scheme, and B-flag conventions. Any change to one should be reviewed for impact on the other.

**Treatment cost source quality note (M03):** The NEWater treatment cost of ~USD 0.88/m³ is derived from OECD (2012) benchmarks and PUB tariff structure analysis, not directly published by PUB as a per-m³ operational cost. Treat as a medium-quality estimate. PUB's cost recovery tariff (SGD 2.74/m³ retail) includes infrastructure, treatment, distribution, and profit margin; the ~USD 0.88/m³ represents an operational treatment-only estimate consistent with published academic benchmarks.
