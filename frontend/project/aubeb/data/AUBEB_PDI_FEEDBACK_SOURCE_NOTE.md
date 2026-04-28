---
doc_id: aubeb_pdi_feedback_source_note
title: AUBEB PDI Feedback Source Note
type: source_note
status: active
domain: methodology
layer: methodology
projects:
  - aubeb
  - water_newwater
tags:
  - aubeb
  - pdi
  - ctvf
  - ecosystem_services
  - ai_costs
  - tvpci
related_docs:
  - frontend_docs_pdi_pdi_water_newwater_status
  - tholonic_framework_supply_value_chain
  - tvpci_specification
key_claims:
  - aubeb_pdi_requires_ecosystem_services_gap_mapping
  - financial_mechanism_parameter_is_needed_for_bond_kpis
  - expert_curated_documents_reduce_early_ai_cost_and_risk
source_file: NEW/260422_For Jeff, message to Janine and Michael re PDI feedback.docx
source_type: private
created: 2026-04-26
---

# AUBEB PDI Feedback Source Note

## Source Context

This note extracts project-relevant information from a message from Sarah Jones to Michael and Janine, dated 2026-04-26. The message discusses early feedback on AUBEB PDI work, ecosystem services, cTVF characteristics, AI costs, and required PDI parameters.

## Extracted Information

- The commodities supply-chain structure model has accepted ecosystem services as a holistic whole for an AU Blue Economy Bond (AUBEB) KPI.
- Sarah describes this as a significant step for the cTVF model and connects it to prior collaboration with Janine.
- The current PDI site work is described as unstable and undergoing rewrite to include ecosystem services redefinition and gap handling.
- Preliminary AUBEB system-integrity signals include lower Phi and other cTVF characteristics for investors.
- The identified gaps include detailed fisheries data, number of women livelihoods, and lack of clarity on KPI formalization.
- A complete gap analysis is being run across the whole cTVF model.
- The message emphasizes that connecting the cTVF front end to a growing database increases AI costs substantially.
- Expert manual document input, expert summaries, and expert baseline gap checks are described as fundamental and cheaper at the present stage.
- Jeff identifies the report as critical because it shows what data was extracted from Draft AUBCI PDI v1 JC 20.4.26, what was needed but not extracted, and what new critical parameters were discovered.
- A new `financial_mechanism` header-level parameter is identified for cases where a bond, fund, or credit facility is the commercialization vehicle embedded in the supply chain.
- The `financial_mechanism` parameter should capture instrument type, counterparties, coupon structure, and market eligibility alongside the supply-chain logic.
- The parameter is described as unnecessary for conventional commodity chains where the commercial phase is a standard sales transaction.
- The note flags a terminology issue: the current Tholonic N-D-C language may cause confusion with nationally determined contributions. The suggested alternative terms are N as Net Performance, C as Constraints, and G as Growth.

## Extracted Links

- AUBEB PDI Status: `https://claritycoalition.net/knowledge-base/6456/`
- AUBEB front-end screen shots: `https://claritycoalition.net/knowledge-base/aubeb-front-end/`
- TVPCI foundation intro: `https://claritycoalition.net/knowledge-base/tvpci_foundation_intro/`

## Structured Data Candidates

| field | extracted value | layer | note |
| --- | --- | --- | --- |
| project | AUBEB | methodology | Blue Economy bond KPI context |
| missing_data | fisheries detail | supply_chain | Phase assignment still needed |
| missing_data | number of women livelihoods | supply_chain | Social/livelihood metric, phase assignment still needed |
| missing_data | KPI formalization | methodology | Definition gap for the KPI itself |
| new_parameter | financial_mechanism | financial_abstraction | Applies when bond, fund, or credit facility is embedded |
| financial_mechanism_detail | instrument type | financial_abstraction | Needed for bond or fund structures |
| financial_mechanism_detail | counterparties | financial_abstraction | Needed for custody/control and contractual mapping |
| financial_mechanism_detail | coupon structure | financial_abstraction | Financial layer only |
| financial_mechanism_detail | market eligibility | financial_abstraction | Financial layer only |

## Handling Notes

Do not treat the financial mechanism parameter as a normal physical supply-chain field. It belongs to the financial-abstraction layer unless the analysis is explicitly modeling the bond, fund, or credit facility as an embedded commercialization vehicle.
