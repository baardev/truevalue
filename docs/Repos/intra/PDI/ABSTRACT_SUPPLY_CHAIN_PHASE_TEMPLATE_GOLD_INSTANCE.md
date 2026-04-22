# Abstract Supply Chain Phase Template — Gold Instance

This document provides the **gold supply chain instance** of the same abstract phase template. The full abstract template (phases 0–8, categories, N-D-C tagging, example metric types) is in **[Abstract Supply Chain Phase Template](ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE.md)**. **Value chain** (revenue, cost, margin, fees): [Gold value chain instance](GOLD_VALUE_CHAIN_PHASE_INSTANCE.md).

**N-D-C:** **D** = Definition (constraints, boundaries, specs). **C** = Contribution (connections, flow, integration). **N** = Negotiation (emergent outcome: throughput, yield, volume). Each phase is where D and C interact to produce N.

**Gold data sources (current):** `schema/supply_chain_phases.csv`, `schema/supply_chain_phases_ndc.csv`, `schema/phase_interactions_ndc.csv`, `schema/gold_supply_chain_metrics_ndc.csv` (synthetic D/C/N indices), `schema/custody_and_flow.csv` (structure only, no rows), `schema/data_sources.csv`, `docs/Reports/WATER_WASTE_METHODOLOGY.md` (benchmark ranges, not populated records). **Physical metrics** (tonnes, oz, recovery rates, custody names) are not yet populated in project data; gold_metrics CSV is empty. Exchange data (e.g. COMEX) is reference/anchor only per project rules.

---

# Gold instance (phases 0–8)

Gold phases in this project map 1:1 to the abstract phases (0–8). Below: **Value (current)** from schema and any project data; **Status** = POPULATED / PARTIAL / MISSING; **Example metrics** for measurement.

---

## Gold Phase 0 — Geological Occurrence & Prospecting (Origin)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state (resource in situ) | D | In situ | POPULATED | e.g. ore in place; resource class (measured/indicated/inferred) |
| Location / geography | D | — | MISSING | e.g. country; region; deposit list; km² or ha |
| Identification / boundary | D | — | MISSING | e.g. reserve boundary; licence area; map reference |
| Typical time scale | context | Years | POPULATED | e.g. years; exploration cycle |
| Transparency level | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters (constraints) | D | D1:ore_grade_threshold \| D2:geological_certainty \| D3:exploration_cost_limit \| D4:regulatory_constraints | POPULATED | e.g. g/t threshold; regulatory index; cost cap (index) |
| C-parameters (integration) | C | C1:survey_technology \| C2:data_sharing \| C3:exploration_partnerships \| C4:market_information | POPULATED | e.g. survey coverage; partnership count (index) |
| Balance / N (synthetic) | N | balance_target 0.75; synthetic d/c/n indices in metrics_ndc | PARTIAL | e.g. balance score 0–100; N-index (simulated) |

---

## Gold Phase 1 — Mine Extraction (Primary extraction)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | In situ (from Phase 0) | POPULATED | e.g. resource in place |
| Physical state out | D | Ore | POPULATED | e.g. ore (t/year); grade g/t |
| Primary transformation | D | Mechanical | POPULATED | e.g. open-pit; underground; heap leach |
| Actors / custodians | C | — | MISSING | e.g. operator name; country; workforce count |
| Throughput / volume | N | — | MISSING | e.g. t ore/year; oz Au/year; t/worker/year |
| Time scale | context | Continuous | POPULATED | e.g. continuous; campaign |
| D-parameters | D | D1:ore_grade_actual \| D2:extraction_method_spec \| D3:safety_standards \| D4:environmental_regulations \| D5:production_capacity | POPULATED | e.g. grade g/t; capacity t/day (index) |
| C-parameters | C | C1:equipment_suppliers \| C2:labor_flexibility \| C3:energy_sources \| C4:transportation_options \| C5:market_access | POPULATED | e.g. supplier count; transport options (index) |
| Custody (who holds after) | C | — | MISSING | e.g. mine operator; ownership change Y/N |
| Water / energy (methodology) | D/N | WATER_WASTE_METHODOLOGY: 0.5–4M litres/day range; recycling 10–30% | PARTIAL | e.g. litres/day; litres/t ore; % recycled |

---

## Gold Phase 2 — Ore Processing & Concentration (First aggregation → primary transformation)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Ore | POPULATED | e.g. ore t |
| Physical state out | D | Concentrate | POPULATED | e.g. concentrate t; grade g/t |
| Primary transformation | D | Chemical | POPULATED | e.g. leaching; flotation; CIL |
| Conversion / yield | N | — | MISSING | e.g. recovery rate %; t ore → t concentrate; oz Au recovered |
| Actors | C | — | MISSING | e.g. processor name; site; custodian |
| Throughput | N | — | MISSING | e.g. t ore/year; t concentrate/year; oz Au/year |
| Time scale | context | Hours–Days | POPULATED | e.g. hours; days |
| D-parameters | D | D1:recovery_rate_target \| D2:process_specifications \| D3:purity_standards \| D4:throughput_capacity \| D5:waste_management | POPULATED | e.g. recovery %; throughput t/day (index) |
| C-parameters | C | C1:chemical_suppliers \| C2:technology_integration \| C3:water_sources \| C4:byproduct_markets \| C5:information_systems | POPULATED | e.g. supplier base; water source (index) |
| Custody | C | — | MISSING | e.g. processor; ownership change |
| Water (methodology) | D/N | 5–12M litres/day; 1000–2500 L/t ore; recycling 60–85% | PARTIAL | e.g. litres/t ore; litres/day; % recycled |

---

## Gold Phase 3 — Doré Production (Primary transformation)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Concentrate | POPULATED | e.g. concentrate |
| Physical state out | D | Doré bars | POPULATED | e.g. doré bars; kg or oz |
| Primary transformation | D | Thermal | POPULATED | e.g. smelting; furnace type |
| Conversion / yield | N | — | MISSING | e.g. kg doré/t concentrate; recovery % |
| Actors | C | — | MISSING | e.g. smelter; custodian |
| Throughput | N | — | MISSING | e.g. t doré/year; oz Au/year |
| Time scale | context | Days | POPULATED | e.g. days |
| Transparency | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters | D | D1:dore_purity_range \| D2:smelting_protocols \| D3:bar_weight_specs \| D4:quality_control | POPULATED | e.g. purity %; bar weight kg (index) |
| C-parameters | C | C1:refinery_network \| C2:transport_providers \| C3:assay_services \| C4:trade_relationships | POPULATED | e.g. refinery count; transport options (index) |
| Custody | C | — | MISSING | e.g. smelter → refinery; ownership change |
| Flow from Phase 2 | C | interaction_type: concentrate_production; d_coupling 0.80, c_coupling 0.65 | POPULATED | e.g. coupling indices; visibility High |

---

## Gold Phase 4 — Refining (Secondary transformation / specification)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Doré bars | POPULATED | e.g. doré |
| Physical state out | D | Fine gold | POPULATED | e.g. fine gold; 995+ fineness |
| Primary transformation | D | Chemical | POPULATED | e.g. electrolytic; aqua regia |
| Specification | D | — | PARTIAL | e.g. fineness (995, 999.9); LBMA standard |
| Actors | C | — | MISSING | e.g. refiner name; LBMA list; country |
| Throughput | N | — | MISSING | e.g. t/year; oz/year refined |
| Time scale | context | Days–Weeks | POPULATED | e.g. days; weeks |
| Transparency | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters | D | D1:fineness_standard \| D2:accreditation_requirements \| D3:refining_capacity \| D4:process_control \| D5:waste_recovery | POPULATED | e.g. fineness; accreditation (index) |
| C-parameters | C | C1:client_base \| C2:equipment_vendors \| C3:certification_bodies \| C4:market_integration \| C5:technology_adoption | POPULATED | e.g. client count; LBMA status (index) |
| Custody | C | — | MISSING | e.g. refiner; ownership change |
| Water (methodology) | D/N | 500k–2M litres/day; 200–500 L/kg refined | PARTIAL | e.g. litres/kg refined; litres/day |

---

## Gold Phase 5 — Bar Casting & Assay (Certification / standardisation)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Fine gold | POPULATED | e.g. fine gold |
| Physical state out | D | Standard bars | POPULATED | e.g. Good Delivery bar; weight; serial |
| Primary transformation | D | Certification | POPULATED | e.g. assay; casting; stamping |
| Standard / regime | D | — | PARTIAL | e.g. LBMA Good Delivery; COMEX spec; assay precision |
| Actors | C | — | MISSING | e.g. assayers; bar casters; exchange-accepted list |
| Throughput | N | — | MISSING | e.g. bars/year; oz/year; bars/assay batch |
| Time scale | context | Hours–Days | POPULATED | e.g. hours; days |
| Transparency | D | Medium–High | POPULATED | e.g. High / Medium / Low |
| D-parameters | D | D1:bar_specifications \| D2:assay_precision \| D3:serial_protocols \| D4:storage_standards \| D5:quality_rejection_limits | POPULATED | e.g. bar weight; assay ppm (index) |
| C-parameters | C | C1:exchange_relationships \| C2:vault_network \| C3:transport_logistics \| C4:documentation_systems | POPULATED | e.g. exchange list; vault count (index) |
| Custody | C | — | MISSING | e.g. who holds bars after assay |
| Flow from Phase 4 | C | interaction_type: fineness_certification; d 0.90, c 0.85 | POPULATED | e.g. coupling; visibility Medium–High |

---

## Gold Phase 6 — Logistics & Vaulting (Logistics / custody)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state | D | Bullion | POPULATED | e.g. standard bars; unchanged form |
| Primary transformation | D | Custodial | POPULATED | e.g. storage; transport; insurance |
| Actors | C | — | MISSING | e.g. vault operator; carrier; jurisdiction |
| Routes / nodes | C | — | MISSING | e.g. refiner → vault; vault → exchange |
| Volume | N | — | MISSING | e.g. oz in vault; oz in transit; t/year |
| Transparency | D | Low | POPULATED | e.g. High / Medium / Low (vault opacity per rules) |
| D-parameters | D | D1:vault_capacity \| D2:security_protocols \| D3:insurance_requirements \| D4:custody_standards \| D5:jurisdictional_compliance | POPULATED | e.g. capacity; security level (index) |
| C-parameters | C | C1:vault_network_size \| C2:transport_flexibility \| C3:insurance_access \| C4:client_access \| C5:information_opacity | POPULATED | e.g. network size; opacity (index) |
| Custody (from → to) | C | — | MISSING | e.g. custodian_from; custodian_to; ownership_change; physical_move |
| Flow from Phase 5 | C | interaction_type: custody_transfer; d 0.75, c 0.45; visibility Low | POPULATED | e.g. coupling; balance_transfer buffered |

---

## Gold Phase 7 — Exchange Registration (Market interface / delivery)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Bullion | POPULATED | e.g. bars in custody |
| Physical state out | D | Deliverable bullion | POPULATED | e.g. registered; warrant; settlement |
| Primary transformation | D | Legal | POPULATED | e.g. registration; warrant; delivery |
| Actors | C | COMEX (reference); exchange; warehouse | PARTIAL | e.g. exchange name; warehouse list (anchor, not truth) |
| Volume / turnover | N | — | MISSING | e.g. oz registered; oz delivered; contracts (reconciliation use only) |
| Time scale | context | Daily | POPULATED | e.g. daily |
| Transparency | D | High | POPULATED | e.g. High (exchange reporting) |
| D-parameters | D | D1:exchange_standards \| D2:registration_requirements \| D3:warehouse_specifications \| D4:delivery_protocols \| D5:contract_terms | POPULATED | e.g. bar list; warehouse spec (index) |
| C-parameters | C | C1:market_participants \| C2:clearing_systems \| C3:information_transparency \| C4:settlement_flexibility \| C5:global_integration | POPULATED | e.g. participant count; transparency (index) |
| Custody | C | — | MISSING | e.g. exchange warehouse; final buyer; ownership transfer |
| Flow from Phase 6 | C | interaction_type: registration_delivery; d 0.85, c 0.90; visibility High | POPULATED | e.g. coupling; balance_transfer direct |
| Data source | context | COMEX Daily Reports (phase 7); public; daily | POPULATED | e.g. source_name; update_frequency (reconciliation anchor) |

---

## Gold Phase 8 — Recycling & Recovery (Circular)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Scrap/waste | POPULATED | e.g. scrap; jewellery; electronics; tailings |
| Physical state out | D | — | PARTIAL | e.g. refined gold re-entering Phase 4 or 5 |
| Primary transformation | D | Thermal/Chemical | POPULATED | e.g. recycling; refining |
| Re-entry point | C | — | MISSING | e.g. phase_id (4 or 5) receiving recovered gold |
| Actors | C | — | MISSING | e.g. recyclers; refineries (scrap intake) |
| Volume | N | — | MISSING | e.g. t/year recycled; % of total supply |
| Time scale | context | Days–Weeks | POPULATED | e.g. days; weeks |
| Transparency | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters | D | D1:collection_standards \| D2:sorting_protocols \| D3:refining_specifications \| D4:purity_requirements \| D5:throughput_capacity | POPULATED | e.g. collection rate; purity (index) |
| C-parameters | C | C1:waste_supplier_network \| C2:refinery_relationships \| C3:technology_providers \| C4:market_integration \| C5:regulatory_compliance | POPULATED | e.g. supplier count; refinery links (index) |
| Custody | C | — | MISSING | e.g. collector → refiner; ownership change |

---

## Cross-phase: Gold custody and flow

| Flow | interaction_type | custodian_from | custodian_to | ownership_change | typical_volume | Status | Example metrics |
|------|------------------|----------------|--------------|------------------|----------------|--------|------------------|
| 0→1 | resource_discovery | — | — | — | — | MISSING | e.g. explorer → operator; volume t resource |
| 1→2 | material_extraction | — | — | — | — | MISSING | e.g. mine → processor; t ore/year |
| 2→3 | concentrate_production | — | — | — | — | MISSING | e.g. processor → smelter; t concentrate/year |
| 3→4 | refinement_preparation | — | — | — | — | MISSING | e.g. smelter → refiner; kg doré/year |
| 4→5 | fineness_certification | — | — | — | — | MISSING | e.g. refiner → assayer; bars/year |
| 5→6 | custody_transfer | — | — | — | — | MISSING | e.g. caster → vault; oz; ownership Y/N |
| 6→7 | registration_delivery | — | — | — | — | MISSING | e.g. vault → exchange warehouse; oz registered |
| 8→4 or 5 | (re-entry) | — | — | — | — | MISSING | e.g. recycler → refiner; t/year recovered |

*Schema: `custody_and_flow.csv` has columns flow_id, from_phase, to_phase, custodian, ownership_change, typical_volume, volume_unit, visibility, notes — no data rows.*

---

## Summary: Gold data status by category type

- **D (Definition):** Phase names, physical states, transformation types, time scales, transparency, and D/C parameter lists (schema) are **POPULATED**. Location, boundary, bar specs (numeric), and some standards are **PARTIAL** or **MISSING**.
- **C (Contribution):** Phase interaction types and coupling indices are **POPULATED**. Custody (custodian_from, custodian_to), routes, and actor names are **MISSING** (no rows in custody_and_flow; no entity list per phase).
- **N (Negotiation):** Synthetic D/C/N balance and sustainability indices exist in **gold_supply_chain_metrics_ndc** (simulated). **Physical N-metrics** (tonnes ore, recovery %, oz refined, oz in vault, oz registered) are **MISSING**; COMEX is reference only for reconciliation.
- **Methodology:** Water/waste/energy benchmark ranges in `WATER_WASTE_METHODOLOGY.md` provide **example metric types** and typical ranges; they are not yet populated as phase-specific records in the gold schema.

*Document ties to: schema/supply_chain_phases.csv, supply_chain_phases_ndc.csv, phase_interactions_ndc.csv, gold_supply_chain_metrics_ndc.csv, custody_and_flow.csv, data_sources.csv, docs/Reports/WATER_WASTE_METHODOLOGY.md.*
