# Abstract Value Chain Phase Template

Product-agnostic **value chain** phase model (phases 0–8) aligned with the [Abstract Supply Chain Phase Template](ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE.md). Each **value_phase_id** corresponds to the same logical stage as supply **phase_id**; linkage is by identifier only—no mixing of physical and value datasets.

This template defines **value** categories per phase (revenue, cost, margin, fees, realized price) with **N-D-C tagging** and example value metric types. Instances: [Gold value instance](GOLD_VALUE_CHAIN_PHASE_INSTANCE.md), [Shea value instance](SHEA_VALUE_CHAIN_PHASE_INSTANCE.md).

**N-D-C (value interpretation):** **D** = Definition (cost constraints, contract terms, regulatory/tax). **C** = Contribution (counterparty options, flexibility, market access). **N** = Negotiation (revenue, margin, realized price, value capture). Time resolution: **quarterly** and/or **annual** (period end date).

---

## Phase 0 — Origin (value context)

*Role:* Project economics pre-production; no revenue from product flow yet.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. project economics; exploration budget; reserve confidence |
| Capital / risk | D | e.g. capital at risk; permit uncertainty; timeline rigidity (index) |
| Revenue / income | N | e.g. none or pre-revenue (USD) |
| Typical time scale | context | e.g. Annual |
| Transparency level | D | e.g. High / Medium / Low |
| D-parameters (value) | D | e.g. capital_risk; permit_uncertainty; exploration_budget (index) |
| C-parameters (value) | C | e.g. capital_access; partner_network; regulatory_navigation (index) |

---

## Phase 1 — Primary extraction (value context)

*Role:* Operating cost structure at extraction stage; revenue and cost per unit.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. operating cost structure; AISC; cash cost |
| Revenue / income | N | e.g. USD; USD/oz; USD/MT |
| Opex | N | e.g. USD; USD/unit |
| Capex | N | e.g. USD (period) |
| Margin / cost per unit | N | e.g. USD/oz (AISC); USD/MT; percent |
| Royalty / tax | D or N | e.g. royalty_rate %; effective_tax_rate % |
| Typical time scale | context | e.g. Quarterly; Annual |
| Transparency level | D | e.g. High / Medium / Low |
| D-parameters (value) | D | e.g. fixed_cost_burden; tax_royalty_constraints (index) |
| C-parameters (value) | C | e.g. supplier_diversity; operational_flexibility (index) |

---

## Phase 2 — First aggregation / processing (value context)

*Role:* Treatment/processing economics; charges and margins.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. treatment economics; processing charges |
| Revenue / income | N | e.g. USD; USD/MT |
| Treatment / processing charge | N | e.g. USD/tonne; USD/MT |
| Opex / cost | N | e.g. USD |
| Margin | N | e.g. percent |
| Typical time scale | context | e.g. Quarterly |
| Transparency level | D | e.g. High / Medium / Low (often opaque) |
| D-parameters (value) | D | e.g. reagent_cost_constraints; quality_spec_penalties (index) |
| C-parameters (value) | C | e.g. processing_optionality; byproduct_monetization (index) |

---

## Phase 3 — Intermediate product (value context)

*Role:* Intermediate product economics; financing and terms.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. intermediate product economics; assay/trade terms |
| Revenue / value flow | N | e.g. USD; USD/unit |
| Fees / financing | N | e.g. USD; percent |
| Security / documentation cost | D or N | e.g. USD |
| Typical time scale | context | e.g. Quarterly |
| Transparency level | D | e.g. High / Medium / Low |
| D-parameters (value) | D | e.g. assay_dispute_risk; financing_terms (index) |
| C-parameters (value) | C | e.g. refinery_counterparties; trade_terms_flex (index) |

---

## Phase 4 — Refining / specification (value context)

*Role:* Refining fee stack and throughput economics.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. refining fee stack; accreditation costs |
| Revenue / income | N | e.g. USD |
| Refining fee | N | e.g. USD/oz; USD/kg; USD/MT |
| Opex / compliance cost | N | e.g. USD |
| Margin | N | e.g. percent |
| Typical time scale | context | e.g. Quarterly |
| Transparency level | D | e.g. High / Medium / Low (fees often opaque) |
| D-parameters (value) | D | e.g. fee_schedule_rigidity; capacity_constraints (index) |
| C-parameters (value) | C | e.g. refinery_network; client_diversity (index) |

---

## Phase 5 — Certification / casting (value context)

*Role:* Certification/casting economics; service fees.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. certification/casting economics |
| Revenue / fee | N | e.g. USD; USD/unit |
| Rejection / quality cost | N | e.g. USD; percent |
| Typical time scale | context | e.g. Quarterly |
| Transparency level | D | e.g. Medium–High |
| D-parameters (value) | D | e.g. assay_precision_requirements; rejection_costs (index) |
| C-parameters (value) | C | e.g. certification_paths; exchange_relationships (index) |

---

## Phase 6 — Logistics / vaulting (value context)

*Role:* Transport, security, insurance economics.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. transport/security/insurance economics |
| Transport cost | N | e.g. USD/kg; USD/unit |
| Insurance cost | N | e.g. USD |
| Revenue / fee | N | e.g. USD |
| Typical time scale | context | e.g. Quarterly |
| Transparency level | D | e.g. Low (structurally opaque) |
| D-parameters (value) | D | e.g. security_protocol_costs; insurance_requirements (index) |
| C-parameters (value) | C | e.g. route_diversity; provider_options (index) |

---

## Phase 7 — Market interface / exchange (value context)

*Role:* Exchange-related value; realized price and settlement.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. exchange-related value frictions |
| Realized price | N | e.g. USD/oz; USD/unit; USD/MT |
| Revenue / turnover | N | e.g. USD/annum |
| Warehouse / settlement cost | N | e.g. USD; USD/unit |
| Typical time scale | context | e.g. Daily–Quarterly |
| Transparency level | D | e.g. High |
| D-parameters (value) | D | e.g. exchange_rules; delivery_terms (index) |
| C-parameters (value) | C | e.g. participant_diversity; market_access (index) |

---

## Phase 8 — Recycling (value context)

*Role:* Recycling economics and fee stack.

| Category | N-D-C | Example metric type |
|----------|-------|---------------------|
| Definition scope | D | e.g. recycling economics; collection/processing cost |
| Revenue / value from scrap | N | e.g. USD; USD/unit |
| Collection / processing cost | N | e.g. USD; USD/unit |
| Typical time scale | context | e.g. Quarterly |
| Transparency level | D | e.g. Medium |
| D-parameters (value) | D | e.g. collection_costs; feedstock_variability (index) |
| C-parameters (value) | C | e.g. collection_network; refinery_relationships (index) |
