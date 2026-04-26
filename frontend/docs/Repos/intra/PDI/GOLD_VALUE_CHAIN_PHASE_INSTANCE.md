---
doc_id: gold_value_chain_phase_instance
title: "Gold — Value Chain Phase Instance"
type: documentation
status: active
domain: pdi
layer: value_chain
projects:
  - gold
tags:
  - gold
  - pdi
  - phase_mapping
  - value_chain
related_docs:
  []
key_claims:
  []
---

# Gold — Value Chain Phase Instance

**Template reference:** This instance follows the [Abstract Value Chain Phase Template](ABSTRACT_VALUE_CHAIN_PHASE_TEMPLATE.md). Value phases align with supply chain phases via `value_phase_id` = `phase_id`; only identifiers link the two layers.

Current project data: schema (`value_chain_phases_ndc.csv`, `value_chain_metric_definitions.csv`, `value_chain_data_sources.csv`) and synthetic N-D-C indices in `value_chain_metrics_ndc.csv`. **Actual value metrics** (revenue_usd, aisc_usd_per_oz, refining_fee_usd_per_oz, etc.) are not yet populated—marked MISSING with example metrics.

---

## Gold Value Phase 0 — Geological occurrence (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Project economics pre-production | POPULATED | e.g. description |
| Typical time scale | context | Annual | POPULATED | e.g. period_type annual |
| Transparency level | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters (value) | D | D1:capital_risk \| D2:permit_uncertainty \| D3:timeline_rigidity \| D4:exploration_budget_constraints \| D5:reserve_confidence | POPULATED | e.g. index 0–100 |
| C-parameters (value) | C | C1:capital_access \| C2:partner_network \| C3:information_quality \| C4:portfolio_diversification \| C5:regulatory_navigation | POPULATED | e.g. index 0–100 |
| Revenue / capital at risk | N | — | MISSING | e.g. USD; exploration spend USD |
| Balance (synthetic) | N | balance_target 0.75; synthetic d/c/n in value_metrics_ndc | PARTIAL | e.g. balance_score (simulated) |

---

## Gold Value Phase 1 — Mining (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Operating cost structure at mine stage | POPULATED | e.g. AISC; cash cost |
| Typical time scale | context | Quarterly | POPULATED | e.g. quarterly; period end |
| Transparency level | D | High | POPULATED | e.g. High / Medium / Low |
| D-parameters (value) | D | D1:fixed_cost_burden \| D2:cost_inflation_exposure \| D3:contract_rigidity \| D4:tax_royalty_constraints \| D5:capex_commitments | POPULATED | e.g. index |
| C-parameters (value) | C | C1:supplier_diversity \| C2:operational_flexibility \| C3:energy_optionality \| C4:workforce_flexibility \| C5:market_access | POPULATED | e.g. index |
| Revenue / income | N | — | MISSING | e.g. revenue_usd |
| Opex / AISC / cash cost | N | — | MISSING | e.g. opex_usd; aisc_usd_per_oz; cash_cost_usd_per_oz |
| Royalty / tax | N | — | MISSING | e.g. royalty_rate_pct; tax_rate_effective_pct |
| Margin | N | — | MISSING | e.g. margin_gross_pct |

---

## Gold Value Phase 2 — Processing (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Treatment/processing economics | POPULATED | e.g. treatment charges |
| Typical time scale | context | Quarterly | POPULATED | e.g. quarterly |
| Transparency level | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters (value) | D | D1:reagent_cost_constraints \| D2:throughput_contracts \| D3:quality_spec_penalties \| D4:waste_compliance_costs \| D5:capacity_limits | POPULATED | e.g. index |
| C-parameters (value) | C | C1:processing_optionality \| C2:technology_alternatives \| C3:water_access_flex \| C4:byproduct_monetization \| C5:information_systems | POPULATED | e.g. index |
| Treatment charge | N | — | MISSING | e.g. treatment_charge_usd_per_tonne |
| Revenue / opex | N | — | MISSING | e.g. revenue_usd; opex_usd |

---

## Gold Value Phase 3 — Doré / intermediate (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Intermediate product economics | POPULATED | e.g. assay; financing terms |
| Typical time scale | context | Quarterly | POPULATED | e.g. quarterly |
| Transparency level | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters (value) | D | D1:assay_dispute_risk \| D2:financing_terms \| D3:security_costs \| D4:documentation_burden \| D5:timing_constraints | POPULATED | e.g. index |
| C-parameters (value) | C | C1:refinery_counterparties \| C2:assay_services \| C3:transport_provider_options \| C4:trade_terms_flex \| C5:traceability_systems | POPULATED | e.g. index |
| Revenue / value flow | N | — | MISSING | e.g. revenue_usd; value flow USD |
| Fees / financing | N | — | MISSING | e.g. USD; percent |

---

## Gold Value Phase 4 — Refining (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Refining fee stack & throughput economics | POPULATED | e.g. refining fees |
| Typical time scale | context | Quarterly | POPULATED | e.g. quarterly |
| Transparency level | D | Medium | POPULATED | e.g. High / Medium / Low (fees often opaque) |
| D-parameters (value) | D | D1:accreditation_requirements \| D2:fee_schedule_rigidity \| D3:capacity_constraints \| D4:compliance_costs \| D5:working_capital_lockup | POPULATED | e.g. index |
| C-parameters (value) | C | C1:refinery_network \| C2:client_diversity \| C3:technology_adoption \| C4:logistics_integration \| C5:documentation_systems | POPULATED | e.g. index |
| Refining fee | N | — | MISSING | e.g. refining_fee_usd_per_oz |
| Revenue / opex | N | — | MISSING | e.g. revenue_usd; opex_usd |

---

## Gold Value Phase 5 — Casting & assay (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Certification/casting economics | POPULATED | e.g. service/fee economics |
| Typical time scale | context | Quarterly | POPULATED | e.g. quarterly |
| Transparency level | D | Medium–High | POPULATED | e.g. High / Medium / Low |
| D-parameters (value) | D | D1:assay_precision_requirements \| D2:rejection_costs \| D3:documentation_requirements \| D4:storage_costs \| D5:standard_compliance | POPULATED | e.g. index |
| C-parameters (value) | C | C1:certification_paths \| C2:exchange_relationships \| C3:workflow_integration \| C4:quality_systems \| C5:traceability_integration | POPULATED | e.g. index |
| Revenue / fee | N | — | MISSING | e.g. revenue_usd; fee USD/unit |

---

## Gold Value Phase 6 — Logistics & vaulting (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Transport/security/insurance economics | POPULATED | e.g. route/security costs |
| Typical time scale | context | Quarterly | POPULATED | e.g. quarterly |
| Transparency level | D | Low | POPULATED | e.g. structurally opaque |
| D-parameters (value) | D | D1:security_protocol_costs \| D2:insurance_requirements \| D3:jurisdictional_limits \| D4:route_constraints \| D5:time_sensitivity | POPULATED | e.g. index |
| C-parameters (value) | C | C1:route_diversity \| C2:provider_options \| C3:insurance_access \| C4:client_access \| C5:information_opacity | POPULATED | e.g. index |
| Transport cost | N | — | MISSING | e.g. transport_cost_usd_per_kg |
| Insurance cost | N | — | MISSING | e.g. insurance_cost_usd |

---

## Gold Value Phase 7 — Exchange / market interface (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Exchange-related value frictions | POPULATED | e.g. delivery terms; warehouse fees |
| Typical time scale | context | Daily–Quarterly | POPULATED | e.g. daily; quarterly |
| Transparency level | D | High | POPULATED | e.g. High |
| D-parameters (value) | D | D1:exchange_rules \| D2:delivery_terms \| D3:warehouse_fees \| D4:settlement_constraints \| D5:regulatory_costs | POPULATED | e.g. index |
| C-parameters (value) | C | C1:participant_diversity \| C2:clearing_integration \| C3:market_access \| C4:information_transparency \| C5:settlement_flexibility | POPULATED | e.g. index |
| Realized price | N | — | MISSING | e.g. realized_price_usd_per_oz |
| Revenue / turnover | N | — | MISSING | e.g. revenue_usd; USD/annum |

---

## Gold Value Phase 8 — Recycling (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Recycling economics and fee stack | POPULATED | e.g. collection/processing cost |
| Typical time scale | context | Quarterly | POPULATED | e.g. quarterly |
| Transparency level | D | Medium | POPULATED | e.g. High / Medium / Low |
| D-parameters (value) | D | D1:collection_costs \| D2:feedstock_variability \| D3:processing_constraints \| D4:compliance_costs \| D5:throughput_limits | POPULATED | e.g. index |
| C-parameters (value) | C | C1:collection_network \| C2:sorting_integration \| C3:refinery_relationships \| C4:technology_providers \| C5:market_integration | POPULATED | e.g. index |
| Revenue / refining fee | N | — | MISSING | e.g. revenue_usd; refining_fee_usd_per_oz (phase 8) |

---

## Summary: Gold value data status

- **D (Definition):** definition_scope, time scale, transparency, and D/C parameter lists are **POPULATED** from schema. Cost/contract details (numeric) are **MISSING**.
- **C (Contribution):** C-parameter names from schema **POPULATED**. Counterparty lists and flexibility metrics **MISSING**.
- **N (Negotiation):** Synthetic N-D-C balance indices exist in value_chain_metrics_ndc. **Actual value metrics** (revenue_usd, opex_usd, aisc_usd_per_oz, refining_fee_usd_per_oz, realized_price_usd_per_oz, etc.) are **MISSING**; metric definitions exist in value_chain_metric_definitions.csv.

*Supply chain instance (physical):* [Gold supply chain instance](ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE_GOLD_INSTANCE.md).  
*Schema:* schema/value_chain_phases_ndc.csv, value_chain_metric_definitions.csv, value_chain_data_sources.csv, value_chain_metrics_ndc.csv.
