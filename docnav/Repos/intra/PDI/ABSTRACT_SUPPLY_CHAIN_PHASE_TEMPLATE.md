---
doc_id: abstract_supply_chain_phase_template
title: Abstract Supply Chain Phase Template
type: template
status: active
domain: pdi
layer: supply_chain
projects:
  - gold
  - shea
tags:
  - pdi
  - template
  - supply_chain
  - phase_mapping
  - ndc
related_docs:
  - abstract_value_chain_phase_template
  - gold_supply_chain_phase_instance
  - shea_supply_chain_phase_instance
key_claims:
  - phase_must_have_physical_state_transformation_output
source_role: phase_template
---

# Abstract Supply Chain Phase Template

Product-agnostic supply chain phase model (phases 0–8) and information categories per phase, with **N-D-C tagging** and example metric types. Use this template to build instances for specific commodities (e.g. [shea butter](SHEA_VALUE_CHAIN_PHASE_INSTANCE.md), [gold](ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE_GOLD_INSTANCE.md)). The **value chain** (profit, pricing, margins) has a separate [Abstract Value Chain Phase Template](ABSTRACT_VALUE_CHAIN_PHASE_TEMPLATE.md) and instances ([gold](GOLD_VALUE_CHAIN_PHASE_INSTANCE.md), [shea](SHEA_VALUE_CHAIN_PHASE_INSTANCE.md)); phases align by id only.

**N-D-C:** **D** = Definition (constraints, boundaries, specs). **C** = Contribution (connections, flow, integration). **N** = Negotiation (emergent outcome: throughput, yield, price). Each phase is the locus where D and C interact to produce N.

---

## Phase 0 — Origin / resource identification
*Role:* Resource exists in place; no commercial flow yet.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state (resource in situ) | D | e.g. description; grade/spec if applicable |
| Location / geography | D | e.g. region, country, site list; km² or ha |
| Identification / boundary | D | e.g. reserve boundary; harvest area; map reference |
| Typical time scale | context | e.g. years; seasonal (months); cycle |
| Transparency level | D | e.g. High / Medium / Low |
| D-parameters (constraints) | D | e.g. threshold; regulatory; cost limit (index or score) |
| C-parameters (integration) | C | e.g. survey/tech access; partnerships; data sharing (index or score) |

---

## Phase 1 — Primary extraction / harvest
*Role:* Raw material first leaves origin and enters the chain.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state in | D | e.g. as Phase 0 |
| Physical state out | D | e.g. first tradeable form (ore, nuts, raw material) |
| Primary transformation | D | e.g. harvest; mechanical extraction (type) |
| Actors / custodians | C | e.g. count; names; % women / workforce |
| Throughput / volume | N | e.g. t/year; kg/actor/season; units/month |
| Time scale | context | e.g. continuous; seasonal (months) |
| D-parameters | D | e.g. extraction specs; safety; capacity (index) |
| C-parameters | C | e.g. equipment suppliers; labour flexibility (index) |
| Custody (who holds after) | C | e.g. custodian name; ownership change Y/N |

---

## Phase 2 — First aggregation / bulking
*Role:* First custody change; material gathered or traded.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state in | D | e.g. output of Phase 1 |
| Physical state out | D | e.g. aggregated/bulk form |
| Primary transformation | D | e.g. custody transfer; storage; sorting |
| Actors | C | e.g. sellers; traders; aggregators (count or list) |
| Price / value flow | N | e.g. US$/MT; local currency/kg; margin % |
| Volume | N | e.g. MT/year; bags/month |
| D-parameters | D | e.g. quality/grade; contract terms (index) |
| C-parameters | C | e.g. buyer/seller count; routes (index) |
| Custody (from → to) | C | e.g. custodian_from; custodian_to; ownership_change |

---

## Phase 3 — Primary transformation
*Role:* Material is materially changed (processed, refined) into an intermediate product.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state in | D | e.g. output of Phase 2 |
| Physical state out | D | e.g. intermediate product (concentrate, butter, component) |
| Primary transformation | D | e.g. chemical; thermal; mechanical (type) |
| Conversion / yield | N | e.g. recovery rate; kg_in → kg_out; bags → kg |
| Actors | C | e.g. processors; refiners (count; custodian) |
| Throughput | N | e.g. MT/year; kg/worker/season |
| Energy / inputs | D or N | e.g. kWh/unit; kg fuel/kg product; % renewable |
| D-parameters | D | e.g. process specs; purity; capacity; waste rules (index) |
| C-parameters | C | e.g. supplier base; technology (index) |
| Custody | C | e.g. who holds before/after; ownership change |

---

## Phase 4 — Secondary transformation / specification
*Role:* Product brought to a defined specification (grade, standard, configuration).

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state in | D | e.g. output of Phase 3 |
| Physical state out | D | e.g. specified product (refined; packaged; configured) |
| Primary transformation | D | e.g. refining; formulation; packaging |
| Specification | D | e.g. fineness; recipe %; standard name |
| Actors | C | e.g. refiners; formulators (count or list) |
| Throughput | N | e.g. MT/year; units/year |
| D-parameters | D | e.g. spec standard; accreditation (index) |
| C-parameters | C | e.g. client base; certification paths (index) |
| Custody | C | e.g. custodian; ownership change |

---

## Phase 5 — Certification / standardisation
*Role:* Product certified or standardised for a market (exchange, regulation, brand).

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state in | D | e.g. output of Phase 4 |
| Physical state out | D | e.g. certified/standardised product |
| Primary transformation | D | e.g. certification; assay; type-approval |
| Standard / regime | D | e.g. exchange name; organic; regulatory ref |
| Actors | C | e.g. assayers; certifiers (count or list) |
| D-parameters | D | e.g. bar/spec; assay precision (index) |
| C-parameters | C | e.g. exchange/market relationships (index) |
| Custody | C | e.g. who holds certified product |

---

## Phase 6 — Logistics / custody
*Role:* Product stored, transported; custody transferred without changing form.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state | D | e.g. unchanged (same certified product) |
| Primary transformation | D | e.g. custodial (storage; transport) |
| Actors | C | e.g. carriers; vaults; warehouses |
| Routes / nodes | C | e.g. origin–destination; hub list |
| Volume | N | e.g. t/year; units in transit |
| D-parameters | D | e.g. capacity; security; insurance (index) |
| C-parameters | C | e.g. network size; transport options (index) |
| Custody (from → to) | C | e.g. custodian_from; custodian_to; physical_move Y/N |

---

## Phase 7 — Market interface / delivery
*Role:* Product sold, registered, or delivered to end buyer or market.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state in | D | e.g. product in custody (Phase 6) |
| Physical state out | D | e.g. delivered to buyer/consumer |
| Primary transformation | D | e.g. sale; registration; delivery |
| Actors | C | e.g. exchange; dealers; retailers; consumers |
| Volume / turnover | N | e.g. units sold/year; US$/annum |
| Price / value | N | e.g. US$/unit; retail price |
| D-parameters | D | e.g. exchange/market rules (index) |
| C-parameters | C | e.g. participants; transparency (index) |
| Custody | C | e.g. final custodian; ownership transfer Y/N |

---

## Phase 8 — Circular / recovery (optional)
*Role:* Post-use or waste re-enters the chain.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Physical state in | D | e.g. scrap; waste; end-of-life product |
| Physical state out | D | e.g. recovered material re-entering a phase |
| Primary transformation | D | e.g. collection; sorting; recycling |
| Re-entry point | C | e.g. phase_id that receives recovered flow |
| Actors | C | e.g. collectors; recyclers |
| Volume | N | e.g. t/year recovered; % of total supply |
| D-parameters | D | e.g. collection/sorting standards (index) |
| C-parameters | C | e.g. waste network; refinery links (index) |
| Custody | C | e.g. who holds scrap; who receives recovered |
