---
doc_id: frontend_project_aubeb_data_pdi_aubeb_status
title: "PDI AUBEB — Schema Updates and Missing Data Report"
type: status_report
status: active
domain: pdi
layer: methodology
projects:
  - aubeb
tags:
  - aubeb
  - methodology
  - pdi
related_docs:
  []
key_claims:
  []
---

# PDI AUBEB — Schema Updates and Missing Data Report

**Instrument:** Phase Discovery Instrument (PDI) v1.0
**Instance:** Africa Blue Economy Bond (AUBEB) — African Mangrove Ecosystem Services Supply Chain
**Completed file:** `PDI_AUBEB_2026-04-21.yaml`
**Report date:** 2026-04-21
**Analyst:** AI (Claude Sonnet 4.6)

---

## 1. New Fields Added to `PDI_TEMPLATE.yaml`

The following fields were added to the master template because the AUBEB document contained data that the original schema did not accommodate. All fields are present in the completed instance and in the updated template.

---

### 1.1 `geographic_scope` — Header level

**Why added:** Multi-country programmes require site names, country-level carbon stock values, and spatial extent data that do not fit into the material description field. This field is optional for single-geography or conventional commodity chains.

```yaml
geographic_scope:
  programme_envelope_ha: 150000
  countries:
    - country: Nigeria
      sites: ["Niger Delta", "Burutu LGA", "Forcados Estuary"]
      carbon_stock_intact_MgCO2e_ha: ">2500"
      sediment_organic_carbon_MgC_ha_top1m: "622–640"
    # ... one entry per country
```

---

### 1.2 `programme_scale` — Header level

**Why added:** Large programmes have defined total budgets, implementation timelines, phase dates, gross and net output volumes, and beneficiary counts that contextualise all module answers and are needed for investor and NDC reporting.

```yaml
programme_scale:
  total_budget_USD: "1,000,000,000"
  implementation_years: 10
  phase_1: "March 2026 – March 2031"
  phase_2: "April 2031 – April 2036"
  baseline_emissions_MtCO2e_yr: "6.5–10.4"
  gross_sequestration_tCO2e_yr: 7050000
  net_sequestration_tCO2e_yr: 5640000
  crediting_period_years: 30
  coastal_dwellers_benefiting: 1500000
```

---

### 1.3 `financial_mechanism` — Header level

**Why added:** When a bond, fund, or credit facility is the commercialisation vehicle embedded in the supply chain, its instrument type, counterparties, coupon structure, and market eligibility must be captured alongside the supply chain logic. This is not needed for conventional commodity chains where the commercial phase is a standard sales transaction.

```yaml
financial_mechanism:
  instrument_name: "African Union Blue Economy Bond (AUBEB)"
  instrument_type: "DFI-issued conservation milestone-linked bond"
  coupon_serviced_from: "Sovereign general revenues"
  derisking_reserve: "Blue carbon revenues as reserve layer above coverage floor"
  dfi_issuer: "AfDB or AFC"
  political_risk_insurer: "DFC or equivalent"
  arranging_bank: "MUFG or equivalent"
  legal_counterparty: "AUC and host governments"
  co_developer: "GUD — not a bond counterparty"
  carbon_standards_eligible: [Verra VM0007/VM0033, Gold Standard, Plan Vivo, ICR, ACR]
  article_6_2_eligible: true
  corsia_eligible: true
```

---

### 1.4 `teeb_category` — Under `A7_actor_classes`

**Why added:** Ecosystem services and nature-based solutions (NbS) supply chains classify actors by TEEB category (The Economics of Ecosystems and Biodiversity): Provisioning, Regulating, Cultural, Biodiversity. This is standard practice for blue carbon and NbS instruments. The field is optional and can be left blank for conventional commodity chains.

```yaml
A7_actor_classes:
  - sequence: 1
    actor: "Coastal communities"
    point_in_chain: "Origin, Phase 0, Phase 8–10"
    teeb_category: "Provisioning / Cultural"
    notes: "Primary custodians; women and youth as stewardship leaders"
```

---

### 1.5 `pricing_reference` — Under `module_2_events`

**Why added:** Commercial-phase events with publicly documentable floor or ceiling pricing need this captured explicitly so that transparency scoring (Module 4, C3/C4) can be anchored to verifiable public benchmarks rather than undisclosed bilateral contract terms. Particularly important for carbon markets and sovereign instruments.

```yaml
# On Event 5 (Commercialisation):
pricing_reference:
  vcm_floor_usd_per_tCO2e: 15
  corsia_floor_usd_per_tCO2e: 20
  current_market_signal: "Supply of biodiversity-linked blue carbon credits structurally below demand"
  annual_reserve_capacity_usd_min: 84600000
```

---

### 1.6 `multi_value_outputs` — Under `module_2_events`

**Why added:** Some phases simultaneously produce multiple verified output streams that cannot be reduced to a single `child_n_output` unit. Phase 10 of this chain produces carbon credits, fisheries recovery indicators, community livelihood metrics, and NDC contributions all at once. The standard `child_n_output` field assumes a single primary output unit and is insufficient for co-benefit chains.

```yaml
# On Event 10 (Verified Restoration):
multi_value_outputs:
  - stream: "carbon"
    unit: "tCO2e/year"
    volume: "5.64M net (after 20% buffer)"
    recipient: "Standards registry; carbon buyers"
  - stream: "fisheries"
    unit: "fisheries productivity index"
    volume: "UNKNOWN — index methodology not specified"
    recipient: "Coastal communities; fisheries value chain"
  - stream: "livelihoods"
    unit: "households and employment figures"
    volume: "1.5M+ coastal dwellers; employment figures not specified"
    recipient: "Community governance bodies"
  - stream: "ndc_fulfilment"
    unit: "tCO2e attributed to national NDC"
    volume: "Country-allocated per AUC programme"
    recipient: "7 host governments for UNFCCC NDC reporting"
```

---

### 1.7 `tvpci_notes` — Under `module_3` phase map entries

**Why added:** The TrueValue Analytics TVPCI (True Value Pricing Convergence Index) is computed at specific phases of the supply chain and tracks the relationship between structural quality (established at Phase 4) and commercial terms (realised at Phase 5). Every chain in the TrueValue Analytics portfolio should record which phases produce or consume TVPCI scores.

```yaml
# On Phase 4 entry:
tvpci_notes: "TVPCI baseline structural quality score is computed at this phase.
              TrueValue Analytics and MSCI are custodians of the index computation."

# On Phase 5 entry:
tvpci_notes: "TVPCI index tracks Phase 5 commercial terms against the Phase 4 baseline."

# On Phase 10 entry:
tvpci_notes: "TVPCI convergence milestone achieved. Score published in annual investor report."
```

---

## 2. Missing Data

The following information was needed to complete the instrument but was not present in the source document (`DRAFT_AUBEB_PDI_v1 response.docx`).

---

### Priority 1 — High (blocks full instrument completion)

| ID | Missing item | Where needed in the YAML | Impact if absent |
|----|-------------|--------------------------|-----------------|
| M1 | AUBEB total bond principal (USD amount) | Phase 5 and Phase 6 `B11_approximate_volume` | Phase 6 capital return volume cannot be specified; investor reporting incomplete |
| M2 | Fisheries productivity index methodology | Phase 10 `multi_value_outputs`; Module 4 C3 and C4 for Phase 10 | Fisheries output stream cannot be independently confirmed; Phase 10 opacity scoring is provisional |
| M3 | Per-country carbon credit allocation split | Phase 4/5 `B11_quantity_and_unit`; Phase 4 opacity `C1_source` | Registry issuance by country registry cannot be specified; NDC attribution per country is undefined |
| M4 | Conservation Trust Fund disbursement schedule | Phase 6 `B11_approximate_volume` (currently marked UNKNOWN) | Phase 6 child-N output is incomplete; capital deployment cannot be verified by country |
| M5 | Analyst name(s) | Header `analyst` field | Audit trail and instrument provenance are absent |
| M6 | Source document version date | Header `date_completed` field | Instrument version control cannot be established; draft status is unresolved |

---

### Priority 2 — Medium (needed for formal instrument completeness)

| ID | Missing item | Where needed in the YAML | Impact if absent |
|----|-------------|--------------------------|-----------------|
| M7 | Individual B-score breakdowns for 5 sub-processes | Module 2 — separate event records for: Article 6.2 authorisation, FPIC formalisation, seed provenance mapping, African Seed Bank establishment, TVPCI index computation | Sub-process classifications rest on narrative justification rather than formal scoring; not reproducible by a third party |
| M8 | Per-event source citations | Module 2 `sources` field on each of the 10 event records | Reproducibility of individual boundary decisions cannot be confirmed; references are currently programme-level only |
| M9 | Women and youth employment numerical targets | Phase 8 and Phase 10 `child_n_output`; Phase 10 `multi_value_outputs` livelihood stream | SDG livelihood reporting and TVPCI livelihood metric cannot be quantified |
| M10 | African Seed Bank governance specification and inventory protocol | Sub-process register; potential Phase 8b definition | Cannot evaluate whether Seed Bank meets the threshold for elevation to confirmed Phase status |

---

### Priority 3 — Low (desirable but not blocking)

| ID | Missing item | Where needed | Notes |
|----|-------------|-------------|-------|
| M11 | SPO provider confirmed identity | A7 actor sequence 10; Phase 4 custodian | Named as "recognised SPO provider (e.g., Sustainalytics, ISS, Vigeo Eiris, Moody's ESG)" — selection not yet made |
| M12 | S&P Dow Jones Indices integration pathway and timeline | A7 actor sequence 9; Phase 10 notes | Described as "potential future" convergence index — no conditionality or timeline specified |
| M13 | Fisheries royalty rate and payment structure | Phase 5 `pricing_reference`; Phase 6 disbursement | Fisheries royalties are activated at Phase 5 but the rate and payment mechanism are not specified in the source |

---

## 3. Structural Observations Requiring Review

The following are not missing data items but anomalies in the completed instrument that should be reviewed by a domain expert before the PDI is used as source material for the Abstract Supply Chain Phase Template.

**S1 — 11-phase chain (above normal range):**
The instrument guidance states that more than 10 phases may indicate sub-processes have been elevated to phase status. All 10 confirmed boundaries meet the formal scoring criteria (scores 3–5, all B11 outputs defined). The 11-phase structure is provisionally justified by the chain's genuine complexity spanning financial, ecological, and governance transformations. Recommend independent review by a PDI-trained analyst.

**S2 — Dual consecutive Commercial phases (5 and 6):**
Phases 5 and 6 are both classified as Commercial with no process class change at their shared boundary (B6=false for Event 6). This is structurally unusual. The distinction — Phase 5 delivers value out to market; Phase 6 returns capital to the ecosystem — is real and justified, but should be noted as a precedent-setting decision for future NbS and blended finance supply chains.

**S3 — Extractive classification for active restoration (Phase 9):**
Phase 9 (active ecosystem recovery) is classified as Extractive on the basis that degradation pressure is being "extracted" from the system. This is the most counterintuitive process class assignment in the chain. An alternative classification of Custodial (with facilitated natural process) may be more consistent when the PDI protocol is applied to other restoration supply chains. The classification should be reviewed and a formal ruling issued for the protocol.

**S4 — African Seed Bank sub-process elevation criteria:**
The African Seed Bank is currently a sub-process spanning Phases 7 and 8. The analyst notes recommend elevation to Phase status (new Phase 8b) if formal establishment occurs with defined governance, species inventory, and output protocols. Recommend establishing explicit elevation criteria in the PDI protocol so this decision can be made consistently.

---

*Phase Discovery Instrument v1.0 — True Value Analytics*
*Aligned with: Abstract Supply Chain Phase Template | N-D-C Tholonic Framework*
