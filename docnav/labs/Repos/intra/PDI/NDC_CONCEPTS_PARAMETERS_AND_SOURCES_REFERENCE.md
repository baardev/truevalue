---
doc_id: ndc_concepts_parameters_sources_reference
title: N-D-C Definitions Reference Guide
type: documentation
status: active
domain: pdi
layer: methodology
projects:
  []
tags:
  - methodology
  - ndc
  - pdi
related_docs:
  []
key_claims:
  []
---

# N-D-C Definitions Reference Guide

**How the D (Definition) and C (Contribution) values are defined, where they come from, and how to research them further.**

This document is written for someone who wants to understand the intellectual and data sources behind the N-D-C model in this project, audit the current values, or extend the model with real empirical data.

---

## The Short Version

| What | Where |
|---|---|
| What D and C *mean* conceptually for each phase | `docs/Research/NDC_QUALITATIVE_D_AND_C_MAPPING_BY_PHASE.md` |
| The named D and C parameters per phase (structured) | `schema/supply_chain_phases_ndc.csv` |
| The D-natural vs D-institutional distinction | `docs/Research/NDC_QUALITATIVE_D_AND_C_MAPPING_BY_PHASE.md` (Part 1) |
| The math (how D, C → N, balance score) | `docs/PDI/NDC_D_C_N_METRICS_CALCULATION_REFERENCE.md` |
| Where the current numeric D/C values come from | `schema/gold_supply_chain_metrics_ndc.csv` (synthetic) |
| Real-world evidence grounding Phases 1–2 | `src/frontend/project/gold/data/processed/phase1_summary.json`, `phase2_summary.json` |
| The tholonic framework behind the model | `docs/Research/../Research/THOLONIC_FRAMEWORK_SUPPLY_AND_VALUE_CHAIN_APPLICATION.md` |
| The template for any new phase instance | `docs/PDI/ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE.md` |
| The gold supply chain as a filled-in instance | `docs/PDI/ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE_GOLD_INSTANCE.md` |

---

## Part 1 — The Conceptual Framework

### What is D?

**D (Definition)** represents all constraints, boundaries, specifications, and requirements that define what a supply chain phase *is*. D parameters are internally focused — they govern structure, identity, and what is permissible or possible within the phase.

D is not a single number in the real world. It is the sum of multiple constraint parameters, each scored 0–100:

```
D_total = D1 + D2 + D3 + D4 + ... + Dn
```

Typical total range: **150–350** (dimensionless index)

### What is C?

**C (Contribution)** represents all connections, outputs, integrations, and flows that define what a supply chain phase *does* — how it connects to the world outside itself. C parameters are externally focused — they govern production, relationships, and what the phase delivers forward.

```
C_total = C1 + C2 + C3 + C4 + ... + Cn
```

Typical total range: **150–350** (dimensionless index)

### What is N?

**N (Negotiation)** is not directly measured — it *emerges* from the interaction of D and C. It represents the operational coherence of the phase: its actual throughput, stability, and sustainable capacity.

```
balance_score = 100 × e^(−2 × |D − C| / max(D, C))

N = √(D × C) × (balance_score / 100)
```

N is highest when D ≈ C (balanced). When D far exceeds C, or C far exceeds D, the balance score collapses and N follows.

**Full derivation:** `docs/PDI/NDC_D_C_N_METRICS_CALCULATION_REFERENCE.md`

---

## Part 2 — The D-Natural vs D-Institutional Distinction

This is the most important conceptual refinement in the project. Not all constraints are the same kind of thing.

| Class | Origin | Can be changed? | Example |
|---|---|---|---|
| **D-natural** | Physics, chemistry, geology, biology | No — governed by natural law | Minimum ore grade for economic extraction |
| **D-institutional** | States, law, financial institutions, industry bodies | Yes — contingent on politics and negotiation | LBMA purity standard (99.99%), royalty rates, export licences |

**D-natural parameters** would exist in a world with no governments, no laws, and no institutions. They arise from the physical nature of what is being done.

**D-institutional parameters** are the encoded outcomes of negotiations between states, corporations, and market bodies. They are imported into the supply chain phase from the political and legal context that surrounds it. They *feel* natural — they are treated as fixed constraints — but they were constructed and can, in principle, be changed.

This distinction matters for two reasons:

1. **Transparency and opacity:** Opacity arising from D-natural is genuinely irreducible. No reform can make an ore body more visible. Opacity from D-institutional is contingent — it was constructed and can be reformed.

2. **Value capture:** D-institutional parameters are the primary levers through which value is redirected away from producers. Royalty rates, accreditation requirements, and purity standards all determine who may participate in the chain and on what terms.

In the parameter tables below, each D parameter is tagged `[natural]` or `[institutional]` where known.

**Primary source:** `docs/Research/NDC_QUALITATIVE_D_AND_C_MAPPING_BY_PHASE.md`, section "The Two Classes of D"

---

## Part 3 — The Named Parameters for Each Phase

These are the canonical D and C parameters defined in `schema/supply_chain_phases_ndc.csv`. Each parameter is a named index variable (0–100 scale) that represents the intensity or degree of that constraint or integration at the phase level.

---

### Phase 0 — Geological Occurrence & Prospecting

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: ore_grade_threshold | D | natural | Minimum grade below which deposit is uneconomic |
| D2: geological_certainty | D | natural | Confidence level in resource classification (measured/indicated/inferred) |
| D3: exploration_cost_limit | D | institutional | Capital budget ceiling for exploration activities |
| D4: regulatory_constraints | D | institutional | Permitting, environmental assessment, indigenous rights requirements |
| C1: survey_technology | C | — | Availability and quality of seismic, drilling, remote sensing capability |
| C2: data_sharing | C | — | Access to public geological databases, historical surveys |
| C3: exploration_partnerships | C | — | Joint venture partners, co-investment agreements |
| C4: market_information | C | — | Gold price signals, demand outlook — informs exploration priority |

**Balance target:** 0.75 | **Transparency:** Medium

---

### Phase 1 — Mine Extraction

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: ore_grade_actual | D | natural | Actual grade of ore being extracted (g/t) — set by geology |
| D2: extraction_method_spec | D | natural | Physical constraints of open-pit vs underground vs heap leach |
| D3: safety_standards | D | institutional | National and international safety regulations |
| D4: environmental_regulations | D | institutional | Tailings, air quality, water discharge standards |
| D5: production_capacity | D | mixed | Physical throughput ceiling (natural); royalty/tax obligations (institutional) |
| C1: equipment_suppliers | C | — | Availability and diversity of mining equipment supply chain |
| C2: labor_flexibility | C | — | Workforce availability, skills, union constraints |
| C3: energy_sources | C | — | Access to grid electricity, diesel, renewable — type and reliability |
| C4: transportation_options | C | — | Road, rail, air options for ore and personnel |
| C5: market_access | C | — | Offtake agreements, refinery relationships, export routes |

**Balance target:** 0.85 | **Transparency:** High

**Real-world evidence in project data (`src/frontend/project/gold/data/processed/phase1_summary.json`):**
- D-institutional confirmed: LBMA Responsible Gold Guidance — verified by Newmont customer audits at Ahafo South, Lihir, Yanacocha
- D-natural evidence: 192 ha land reclamation (2024) — confirms irreducible physical closure obligations
- C-fragility flag: 24% of supplier base carries elevated human rights risk (194/812 screened)
- Economic scale: Newmont contributed USD 16.0B direct economic value and USD 69M community investment (2024)

---

### Phase 2 — Ore Processing & Concentration

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: recovery_rate_target | D | natural | Chemistry-constrained maximum extraction efficiency |
| D2: process_specifications | D | natural | Leaching, flotation, CIL protocol requirements |
| D3: purity_standards | D | institutional | Downstream buyer specifications for concentrate grade |
| D4: throughput_capacity | D | natural | Physical mill and leach pad capacity ceiling |
| D5: waste_management | D | institutional | Tailings dam regulations, cyanide handling standards |
| C1: chemical_suppliers | C | — | Cyanide, lime, flocculant supply chain |
| C2: technology_integration | C | — | Process control systems, automation level |
| C3: water_sources | C | — | Water availability — most intensive water phase in the chain |
| C4: byproduct_markets | C | — | Silver, copper, and other metals recovered alongside gold |
| C5: information_systems | C | — | Assay data, production reporting, metallurgical accounting |

**Balance target:** 0.90 | **Transparency:** High

**Real-world evidence in project data (`src/frontend/project/gold/data/processed/phase2_summary.json`):**
- C-parameter water: 71% water recycling rate (Newmont 2024) vs 65% baseline (2018) — positive C trend
- D-natural cyanide: 30 cyanide spills in 2024 (-33% YoY) — irreducible D-natural constraint, cannot be eliminated, only reduced
- Data gap: throughput volumes, recovery rates, treatment costs remain MISSING in current schema

---

### Phase 3 — Doré Production

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: dore_purity_range | D | mixed | Physical chemistry of smelting (natural); buyer purity spec (institutional) |
| D2: smelting_protocols | D | natural | Furnace temperature, flux requirements, pour specifications |
| D3: bar_weight_specs | D | institutional | Weight tolerances set by refinery acceptance standards |
| D4: quality_control | D | institutional | Assay and sampling protocols required by downstream |
| C1: refinery_network | C | — | Number and proximity of accredited refineries |
| C2: transport_providers | C | — | Secure transport options for doré shipment |
| C3: assay_services | C | — | Independent assay houses for dispute resolution |
| C4: trade_relationships | C | — | Refinery offtake agreements, hedging relationships |

**Balance target:** 0.70 | **Transparency:** Medium

---

### Phase 4 — Refining

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: fineness_standard | D | institutional | 99.99% (four nines) purity — LBMA Good Delivery standard |
| D2: accreditation_requirements | D | institutional | LBMA, COMEX, and national bank approval — barrier to entry |
| D3: refining_capacity | D | natural | Physical throughput ceiling of electrolytic/Miller/Wohlwill plant |
| D4: process_control | D | natural | Chemical precision requirements of acid and electrolytic processes |
| D5: waste_recovery | D | institutional | Environmental compliance for acid, chlorine, and slag waste |
| C1: client_base | C | — | Mine operators, central banks, bullion dealers as customers |
| C2: equipment_vendors | C | — | Specialist refinery equipment supply chain |
| C3: certification_bodies | C | — | LBMA, national assay offices |
| C4: market_integration | C | — | Spot market access, bullion bank relationships |
| C5: technology_adoption | C | — | Continuous casting, inline assay, digital traceability |

**Balance target:** 0.75 | **Transparency:** Medium

**Note:** Phase 4 carries the heaviest D-institutional burden in the chain. The LBMA Good Delivery List is a private accreditation system maintained by a London-based industry association. Access to global bullion markets depends on appearing on this list — a requirement that did not arise from the physics of refining.

---

### Phase 5 — Bar Casting & Assay

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: bar_specifications | D | institutional | LBMA Good Delivery bar: 350–430 troy oz, 99.5% minimum fineness |
| D2: assay_precision | D | natural | Measurement precision limits of fire assay and XRF |
| D3: serial_protocols | D | institutional | Hallmarking, serial numbering, tamper-evidence requirements |
| D4: storage_standards | D | institutional | Vault acceptance standards for bar condition |
| D5: quality_rejection_limits | D | institutional | Defect tolerances before bar is rejected from Good Delivery |
| C1: exchange_relationships | C | — | COMEX, LBMA, and other exchange approval pathways |
| C2: vault_network | C | — | Approved vaults accepting newly cast bars |
| C3: transport_logistics | C | — | Secure logistics providers certified for bullion |
| C4: documentation_systems | C | — | Chain of custody documentation, digital provenance records |

**Balance target:** 0.80 | **Transparency:** Medium-High

---

### Phase 6 — Logistics & Vaulting

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: vault_capacity | D | natural | Physical storage capacity ceiling |
| D2: security_protocols | D | institutional | Insurance and regulatory minimum security specifications |
| D3: insurance_requirements | D | institutional | Lloyd's of London and specialist bullion insurer requirements |
| D4: custody_standards | D | institutional | Legal custody transfer requirements; allocated vs unallocated |
| D5: jurisdictional_compliance | D | institutional | AML, KYC, sanctions compliance in each vault jurisdiction |
| C1: vault_network_size | C | — | Number of interconnected vaults globally |
| C2: transport_flexibility | C | — | Air, road, sea options and frequency |
| C3: insurance_access | C | — | Availability of specialist bullion insurance |
| C4: client_access | C | — | Counterparty relationships permitting gold withdrawal |
| C5: information_opacity | C | — | (Note: this is a *negative* C parameter — opacity reduces integration) |

**Balance target:** 0.50 | **Transparency:** Low (structural bottleneck)

**Note:** Phase 6 is the **known bottleneck** in the current model (D=204, C=161, balance≈65). The D-institutional burden (insurance, custody law, jurisdictional compliance) significantly exceeds the C integration capacity. This is not a data artifact — it reflects the structural reality that vault custody is controlled by a small number of approved operators, entry is restricted, and information about holdings is commercially and legally protected.

---

### Phase 7 — Exchange Registration

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: exchange_standards | D | institutional | COMEX and LBMA delivery specifications |
| D2: registration_requirements | D | institutional | Warrant issuance, bar inspection, weighing protocols |
| D3: warehouse_specifications | D | institutional | Approved warehouse location and security standards |
| D4: delivery_protocols | D | institutional | Last trading day, delivery notice procedures |
| D5: contract_terms | D | institutional | Contract size (100 oz), grade, fineness, brand requirements |
| C1: market_participants | C | — | Number and diversity of registered trading participants |
| C2: clearing_systems | C | — | CME Clearing, LCH Clearnet integration |
| C3: information_transparency | C | — | Daily inventory reporting — highest transparency in the chain |
| C4: settlement_flexibility | C | — | EFP, EFS, and block trade mechanisms |
| C5: global_integration | C | — | Cross-listing, arbitrage mechanisms connecting COMEX/LBMA/SGE |

**Balance target:** 0.85 | **Transparency:** High

---

### Phase 8 — Recycling & Recovery

| Parameter | Role | Type | Description |
|---|---|---|---|
| D1: collection_standards | D | institutional | AML requirements for scrap gold dealers |
| D2: sorting_protocols | D | natural | Minimum purity levels viable for secondary smelting |
| D3: refining_specifications | D | natural | Chemistry of secondary refining (same as Phase 4) |
| D4: purity_requirements | D | institutional | Final product must meet same LBMA standard as virgin gold |
| D5: throughput_capacity | D | natural | Physical capacity of secondary refining infrastructure |
| C1: waste_supplier_network | C | — | Jewellery scrap, electronics, industrial gold waste collectors |
| C2: refinery_relationships | C | — | Access to Phase 4 refineries willing to accept secondary feed |
| C3: technology_providers | C | — | Urban mining technology, electrochemical recovery |
| C4: market_integration | C | — | Certified recycled gold premium, ESG buyer demand |
| C5: regulatory_compliance | C | — | Responsible recycling certification (RJC, LBMA) |

**Balance target:** 0.80 | **Transparency:** Low-Medium

**Note:** Phase 8 feeds back into Phase 4 (Refining), creating the only circular loop in the supply chain. It currently supplies approximately 28% of annual gold demand. The D-institutional burden is significantly lower than Phase 4 for the same chemistry because secondary feed does not require LBMA accreditation to enter the refining step — but the *output* must still meet LBMA Good Delivery standard.

---

## Part 4 — Where the Numeric D/C Values Come From

### Current Status: Synthetic Baseline

The numeric D and C values currently used in the simulator (e.g., Phase 1: D=270, C=277) are **synthetically generated**, not measured from real-world data.

**Source file:** `schema/gold_supply_chain_metrics_ndc.csv`

Every record in this file carries:
```
source_type = "simulated"
source_name = "Synthetic Generator - Baseline"
notes = "Baseline balanced scenario - healthy supply chain"
```

**How they were generated:** `src/data/synthetic_data_generator.py`

The generator uses phase-specific D and C base values with added Gaussian noise to simulate daily variation over a 365-day period. The base values were chosen to produce balance scores consistent with each phase's expected transparency level and operational stability:

| Phase | D base | C base | Design intent |
|---|---|---|---|
| 0 — Prospecting | 220 | 210 | Moderately balanced, medium transparency |
| 1 — Mining | 260 | 250 | Near-balanced, high transparency |
| 2 — Ore Processing | 280 | 275 | Near-balanced, high transparency, high energy |
| 3 — Doré Production | 240 | 235 | Slightly D-dominant, medium transparency |
| 4 — Refining | 270 | 260 | Slightly D-dominant, institutional burden |
| 5 — Bar Casting | 260 | 255 | Near-balanced, standard protocol |
| 6 — Logistics/Vaulting | 200 | 195 | **Intentionally bottlenecked** in some scenarios |
| 7 — Exchange | 280 | 275 | Near-balanced, high transparency |

The "day 1" values from this generator (the baseline scenario, record_ids 1–8 in the CSV) become the canonical simulator baseline values stored in `data/frontend/gold_supply_chain_ui.json`.

### The Data Pipeline

```
schema/supply_chain_phases_ndc.csv       ← parameter definitions (what D and C mean)
schema/gold_supply_chain_metrics_ndc.csv ← synthetic numeric D/C/N values
        ↓
src/api/generate_ui_data.py              ← reads CSVs, merges with real data, writes JSON
        ↓
data/frontend/gold_supply_chain_ui.json  ← authoritative runtime data store
        ↓
frontend/project/gold/supply_chain/what_if_simulator.html  ← reads JSON, renders only
```

---

## Part 5 — Real-World Data That Has Been Integrated

Only two phases currently have real, cited data grounding their D and C sub-parameters. All others are synthetic pending further data collection.

### Phase 1 — Mine Extraction (Partial real data)

| Evidence | NDC role | Source |
|---|---|---|
| LBMA Responsible Gold Guidance compliance, verified at Ahafo South, Lihir, Yanacocha | D-institutional confirmed | Newmont 2024 Sustainability Report |
| 192 ha land reclamation (2024) | D-natural confirmed | Newmont 2024 Sustainability Report |
| 24% of supplier base carries elevated human rights risk (194/812 screened) | C-fragility flag | Newmont 2024 Sustainability Report |
| USD 16.0B direct economic value contributed | N-scale reference | Newmont 2024 Sustainability Report |
| GHG source split: 13% direct, 44% electricity | Scope 1/2 basis | Foran et al. 2005 *Balancing Act* Vol. 2 |
| GHG intensity 35% below economy-wide average per $1 demand | Scope 1/2 quality | Foran et al. 2005 *Balancing Act* Vol. 2 |

**Stored in:** `src/frontend/project/gold/data/processed/phase1_summary.json`

### Phase 2 — Ore Processing (Partial real data)

| Evidence | NDC role | Source |
|---|---|---|
| 71% water recycling (2024) vs 65% baseline (2018) | C-parameter positive trend | Newmont 2024 Sustainability Report |
| 30 cyanide spills in 2024, -33% YoY | D-natural constraint evidence | Newmont 2024 Sustainability Report |
| GHG source split: 44% electricity dominant | Scope 2 basis | Foran et al. 2005 *Balancing Act* Vol. 2 |
| Water intensity 85% below economy-wide average | Water D/N basis | Foran et al. 2005 *Balancing Act* Vol. 2 |

**Stored in:** `src/frontend/project/gold/data/processed/phase2_summary.json`

### What remains MISSING (and must be treated as OPAQUE)

Per the project's transparency classification rules, the following are explicitly absent from current data for Phase 2 and most other phases:
- Throughput volumes (t ore/year, oz Au/year)
- Recovery rates (%)
- Treatment costs
- Reagent consumption
- Custody transfer records

These are the *primary N-state metrics* for most phases. Until they are populated, the numeric D/C values remain synthetic estimates.

---

## Part 6 — How to Research and Replace the Synthetic Values

### Step 1: Identify the parameter you want to ground

Use `schema/supply_chain_phases_ndc.csv` to find the specific parameter name (e.g., `D1:ore_grade_actual` for Phase 1).

### Step 2: Find a real-world source

Recommended public sources by phase:

| Phase | Best public sources |
|---|---|
| 0 — Prospecting | S&P Global Market Intelligence, National geological surveys (USGS, Geoscience Australia) |
| 1 — Mining | Newmont, Barrick, AngloGold annual/sustainability reports; World Gold Council production statistics |
| 2 — Ore Processing | Same major company reports; ICMM (International Council on Mining and Metals) |
| 3 — Doré Production | Largely opaque; doré assay reports are commercially confidential |
| 4 — Refining | LBMA Good Delivery list (public); individual refinery sustainability reports (Rand, Argor-Heraeus, etc.) |
| 5 — Bar Casting | LBMA Good Delivery rules (public document); COMEX delivery specifications |
| 6 — Logistics | LBMA vault list (partially public); Insurance market data (Lloyd's) — largely opaque |
| 7 — Exchange | COMEX daily inventory reports (public, free); LBMA clearing statistics (public) |
| 8 — Recycling | World Gold Council *Gold Demand Trends* (quarterly, free); IPMI (precious metals recyclers) |

**For Scope 1/2 emissions specifically:**
- World Gold Council "Gold and Climate" report (annual, free)
- Foran et al. 2005 *Balancing Act* Volumes 1 and 2 (available in `docs/`)
- Company Scope 1/2 disclosures in sustainability reports (CDP database, free)
- ICCT transport emissions benchmarks (for Phase 6)

### Step 3: Score the parameter (0–100 scale)

Each D and C parameter is scored as an intensity index:
- **0** = no constraint / no connection
- **50** = moderate, typical industry level
- **100** = maximum constraint / fully integrated

A regulatory burden of 100 means the highest level of regulatory friction observed anywhere in the global industry. A supplier network of 100 means maximum diversity and resilience. These are relative, comparative scores — not physical measurements.

### Step 4: Update the data store

Add the real value to `schema/gold_supply_chain_metrics.csv` with:
- `phase_id` = the phase number
- `entity` = the company or sector name
- `metric_name` = the parameter ID (e.g., `D1_ore_grade_actual`)
- `metric_value` = your score (0–100)
- `source_type` = `public` / `paid` / `private` / `inferred`
- `source_name` = citation

Then run `python3 src/api/generate_ui_data.py --gold-only` to propagate the update into the JSON and simulator.

---

## Part 7 — Document Map

```
docs/
├── Research/
│   ├── NDC_QUALITATIVE_D_AND_C_MAPPING_BY_PHASE.md     ← Primary: what D/C mean, per phase
│   ├── NDC_D_C_N_METRICS_CALCULATION_REFERENCE.md      ← The math: D+C → balance → N
│   ├── ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE_GOLD_INSTANCE.md  ← Gold-specific fill
│   ├── ../Research/THOLONIC_FRAMEWORK_SUPPLY_AND_VALUE_CHAIN_APPLICATION.md  ← Theory: N-D-C in supply chains
│   └── NDC_CONCEPTS_PARAMETERS_AND_SOURCES_REFERENCE.md        ← This document
├── PDI/ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE.md   ← Generic template (phases 0–8)
├── Guidelines/SUPPLY_CHAIN_RULES.md                    ← Project rules governing analysis
└── PDI/THOLONIC_INTEGRATION.md               ← Integration guide + formula reference

schema/
├── supply_chain_phases_ndc.csv                 ← Canonical parameter names per phase
├── gold_supply_chain_metrics_ndc.csv           ← Synthetic D/C/N numeric time series
└── gold_supply_chain_metrics.csv               ← Real-world metrics (partial)

src/data/
├── synthetic_data_generator.py                 ← Generates the synthetic baseline
└── processed/
    ├── phase1_summary.json                     ← Real evidence: Phase 1
    └── phase2_summary.json                     ← Real evidence: Phase 2

data/frontend/
└── gold_supply_chain_ui.json                   ← Runtime data store (generated)

src/api/
└── generate_ui_data.py                         ← Builds the runtime JSON from all sources
```

---

## Part 8 — A Note on the Tholonic Mathematical Grounding

The N-D-C framework is not an arbitrary analytical convenience. It has a formal mathematical foundation documented in `docs/Research/../Research/THOLONIC_FRAMEWORK_SUPPLY_AND_VALUE_CHAIN_APPLICATION.md`.

When the first three prime numbers are assigned to the N, D, and C roles (2, 3, and 5 respectively) and the recursive model is applied, the fundamental mathematical constants emerge naturally: π, φ (the golden ratio), √2, and Euler's number *e*. This is structural, not coincidental — the constants are emergent properties of the recursive self-similar iteration of the trigram, in the same way that φ emerges from the Fibonacci sequence.

**Practical implication for this document:** When you see the balance formula `100 × e^(−2 × |D − C| / max(D, C))`, the choice of *e* as the base is not arbitrary. It arises naturally from the Tholonic recursive structure and produces the correct scale-invariant decay behaviour for the balance score across all phase types.

---

*Last updated: April 2026. To regenerate the runtime data after any schema change: `python3 src/api/generate_ui_data.py`*
