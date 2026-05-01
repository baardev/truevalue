---
doc_id: phi_threshold_project_reanalysis
title: "Adopting 0.618 as the Sustainability Floor: Reclassification of All Active Projects and Danube Basin Reanalysis"
type: analytical_report
status: active
domain: tholonic_framework
layer: applied_analysis
projects:
  - gold
  - shea
  - lighter
  - aubeb
  - danube
tags:
  - phi
  - sustainability_threshold
  - reclassification
  - danube
  - ndc
  - rating_system
related_docs:
  - phi_sustainability_threshold
  - tvpci_explained_math
  - tvpci_foundation
key_claims:
  - current_70pct_floor_conflates_stressed_and_failure_zones
  - no_danube_phase_falls_below_phi_threshold
  - lighter_phase8_is_only_failure_zone_phase_in_active_projects
  - policy_intervention_type_differs_by_zone
---

# Adopting 0.618 as the Sustainability Floor

### Reclassification of All Active Projects and Danube Basin Reanalysis

---

## 1. The Problem with the Current Rating System

The current N-D-C grading system uses round-number thresholds:

```
Green  (Coherent):    ≥ 80%
Amber  (Stressed):    70–80%
Red    (Bottleneck):  < 70%
```

These thresholds were chosen as reasonable engineering benchmarks. They are not derived from the structure of the N-D-C model. The consequence is that phases at 68% and phases at 55% are both labelled "red bottleneck," even though they occupy fundamentally different structural conditions: one is over-constrained but self-sustaining; the other has crossed a structural threshold and cannot sustain itself without external subsidy.

The derivation in `PHI_SUSTAINABILITY_THRESHOLD.md` establishes that the balance formula $B = \frac{2\min(D,C)}{D+C}$ produces a structural threshold at exactly $B = \frac{1}{\varphi} \approx 0.6180$ when $D/C = \sqrt{5} \approx 2.236$. Below this threshold, the constraint apparatus exceeds the contribution apparatus by more than $\sqrt{5}$:1. The system exports costs to its environment rather than sustaining itself.

This document applies the revised four-zone framework to every active project and conducts a full reanalysis of the Danube Basin.

---

## 2. The Revised Four-Zone Framework

| Zone | Balance Range | D/C Ratio | Structural Meaning | Color |
|---|---|---|---|---|
| **Coherent** | $\geq$ 80% | $\leq$ 1.50 | Self-sustaining and healthy. Improvements are optional optimizations, not structural repairs. | Green |
| **Stressed** | 61.8–80% | 1.50–2.24 | Self-sustaining but over-constrained. The phase can be improved from within the existing system by reducing D or growing C. External intervention is helpful but not required. | Amber |
| **Failure** | 38.2–61.8% | 2.24–4.24 | Cannot self-sustain. The phase exports costs to external parties (society, environment, future generations). Internal actors have no economic incentive to close the gap. External policy, regulation, or infrastructure investment is required. | Red |
| **Breakdown** | $<$ 38.2% | $>$ 4.24 | Structural collapse. The constraint apparatus is more than $\varphi^3$:1 against contributions. The phase is a regulatory shell without a functioning core. | Dark Red |

The critical shift is the split of the old "red zone" (below 70%) into two meaningfully different categories: **stressed but self-sustaining** (61.8–70%) and **failure** (below 61.8%). This is not cosmetic. It determines whether the intervention required is internal (investment, process improvement, better data) or external (legislation, EPR regulation, public infrastructure, bond mechanism).

---

## 3. Cross-Project Reclassification Summary

### 3.1 Gold Supply Chain

| Phase | Name | Balance | Old Label | New Label | Change? |
|---|---|---|---|---|---|
| 0 | Geological Occurrence | 83.9% | Green | Coherent | No |
| 1 | Mine Extraction | 94.6% | Green | Coherent | No |
| 2 | Ore Processing | 96.0% | Green | Coherent | No |
| 3 | Doré Production | 89.3% | Green | Coherent | No |
| 4 | Refining | 95.1% | Green | Coherent | No |
| 5 | Bar Casting & Assay | 95.0% | Green | Coherent | No |
| **6** | **Logistics & Vaulting** | **65.5%** | Red (Bottleneck) | **Amber (Stressed)** | **YES** |
| 7 | Exchange Registration | 92.2% | Green | Coherent | No |
| 8 | Recycling & Recovery | 80.0% | Green | Coherent | No |
| **Mining Co. B, Phase 1** | **Mine Extraction** | **45.3%** | Red (Bottleneck) | **Red (Failure zone)** | **YES** |

**Key reclassification — Gold Phase 6 (Logistics and Vaulting, 65.5%):** This phase is currently flagged red, alongside Mining Co. B's mine extraction at 45.3%. Under the phi framework they are separated. Phase 6 is stressed but self-sustaining: the vaulting industry operates commercially, the constraints (LBMA chain of integrity, customs bonding, allocated vs unallocated accounting) are high but the custody-and-storage contribution does function. The opacity of vaulting economics is a transparency problem, not a structural failure.

**Key reclassification — Mining Co. B Phase 1 (Mine Extraction, 45.3%):** This is the only gold phase in the **failure zone**. D/C ratio of approximately 3.5:1 means the regulatory, environmental, and geological constraint apparatus exceeds operational contribution by more than $\sqrt{5}$. This mine cannot sustain itself without one of: a commodity price rise that improves C, regulatory relaxation that reduces D, or external capital subsidy. Under current conditions it is a structurally subsidized operation.

**Gold system-level finding:** The gold supply chain has no systemic failure. One entity-specific phase (Co. B mine extraction) is in the failure zone; the chain-level Phase 6 is stressed but intact. The chain's primary analytical challenge remains the opacity gap at vaulting, not structural failure.

---

### 3.2 Shea Supply Chain

| Phase | Name | Balance | Old Label | New Label | Change? |
|---|---|---|---|---|---|
| **0** | **Collection** | **68.2%** | Red (Bottleneck) | **Amber (Stressed)** | **YES** |
| **1** | **First Sale / Aggregation** | **78.5%** | Amber | Amber (Stressed) | No (already amber) |
| 2 | Trading / Bulking | 88.0% | Green | Coherent | No |
| 3 | Processing (nuts to butter) | 92.5% | Green | Coherent | No |
| **4** | **Export** | **64.0%** | Red (Bottleneck) | **Amber (Stressed — near threshold)** | **YES** |
| 5 | Manufacturing (cosmetic) | 90.2% | Green | Coherent | No |
| 6 | Retail | 91.8% | Green | Coherent | No |

**Key reclassification — Collection (68.2%):** Currently flagged red, implying structural failure. Under the phi framework it is stressed but self-sustaining. The 200,000+ women collectors in the shea belt do sustain their livelihoods; the constraint (seasonal availability, informal market access, physical collection burden) is high but the contribution (consistent nut delivery to aggregators) functions. The problem is efficiency, equity, and data visibility, not structural collapse.

**Key reclassification — Export (64.0%):** This phase is stressed and close to the phi threshold (only 2.2 percentage points above 61.8%). It is self-sustaining, but a modest deterioration in market access conditions, certification burden, or currency pressure could push it below the threshold. It is the highest-risk phase in the shea chain under the phi criterion. It warrants monitoring as a near-threshold phase.

**Shea system-level finding:** No shea phase is in the failure zone. The chain's two historically red phases are both reclassified as stressed-but-functional. The most important metric to track is the Export phase margin against the 61.8% floor.

---

### 3.3 Lighter Supply Chain

| Phase | Name | Balance | Old Label | New Label | Change? |
|---|---|---|---|---|---|
| 0 | Raw Material Extraction | 83.0% | Green | Coherent | No |
| **1** | **Component Manufacturing** | **70.0%** | Red (Bottleneck) | **Amber (Stressed)** | **YES** |
| **2** | **Lighter Assembly** | **72.0%** | Red (Bottleneck) | **Amber (Stressed)** | **YES** |
| 3 | QA Testing & Certification | 85.0% | Green | Coherent | No |
| 4 | Packaging & Containerization | 82.0% | Green | Coherent | No |
| 5 | Ocean Freight & Import | 91.0% | Green | Coherent | No |
| 6 | Wholesale Distribution | 80.0% | Green | Coherent | No |
| 7 | Retail | 92.0% | Green | Coherent | No |
| **8** | **End-of-Life & Waste Mgmt** | **56.7%** | Red (Bottleneck) | **Red (Failure zone)** | **YES (confirmed failure)** |

**Key reclassification — Phases 1 and 2 (70.0% and 72.0%):** The Wenzhou manufacturing cluster is stressed and opaque, but it does sustain itself commercially. It operates on sub-cent margins under extreme ISO and EN constraints. It is not failing: 10 billion units per year are assembled and shipped. It is a stressed, information-poor system that could be improved by supply chain transparency investment. External structural intervention is not required.

**Confirmed failure — Phase 8 (56.7%):** This is the only phase in the entire lighter chain that is in the failure zone, and it is the only phase in all active projects that crosses the phi threshold as a systemic supply chain phase (rather than a specific entity's operational phase, as with Gold Mining Co. B). D/C = 215/85 = 2.53, exceeding $\sqrt{5}$ = 2.236. The regulatory constraint apparatus (CPSC hazardous classification, no recycling stream, no EPR obligation) exceeds the circularity contribution (0.3% recycling rate, France CITEO only) by a factor that the system cannot close from within.

**Why this distinction matters for the lighter:** Under the old system, Phases 1, 2, and 8 were all red, implying the same type of problem. In fact they are completely different problems requiring completely different interventions:

- Phases 1 and 2: better supply chain data, factory certification programs, supplier transparency investment. These are internal improvements.
- Phase 8: EPR legislation, device-level producer responsibility mandates, public infrastructure for decontamination and material recovery. These require external regulatory action. No actor in the existing chain has an incentive to fund Phase 8 improvement without legislation, because the cost of failure is borne by society, not by the supply chain.

---

### 3.4 AUBEB (Africa Union Blue Economy Bond — Mangrove Restoration)

| Phase | Name | Balance | Old Label | New Label | Change? |
|---|---|---|---|---|---|
| **0** | **Pre-commercial: degraded ecosystem** | **71.1%** | Red (Bottleneck) | **Amber (Stressed)** | **YES** |
| 1 | Custodial formalisation | 88.2% | Green | Coherent | No |
| 2 | Data extraction (remote sensing) | 91.9% | Green | Coherent | No |
| 3 | Specification (carbon quantification) | 93.1% | Green | Coherent | No |
| 4 | Certification (verification & registration) | 89.4% | Green | Coherent | No |
| 5 | Commercialisation outward | 87.8% | Green | Coherent | No |
| 6 | Capital return (Conservation Fund) | 86.2% | Green | Coherent | No |
| 7 | Restoration specification (CBEMR design) | 91.2% | Green | Coherent | No |
| **8** | **Community custodial co-management** | **79.8%** | Amber | Amber (Stressed) | No |
| 9 | Physical recovery (active regeneration) | 92.5% | Green | Coherent | No |
| 10 | Verified restoration (sustained asset) | 92.5% | Green | Coherent | No |

**Key reclassification — Phase 0 (Pre-commercial degraded ecosystem, 71.1%):** Currently flagged red. Under the phi framework it is stressed but self-sustaining. This is a meaningful restatement for bond structuring: the degraded ecosystem is not in structural collapse; it is over-constrained (D: degraded hydrology, sedimentation pressure, community tenure insecurity) relative to its contribution (C: residual ecosystem services from degraded mangrove). It is a stressed, recoverable system, not a failed one. This supports the bond's restoration thesis: intervention is needed to reduce D and grow C, not to rescue a collapsed system.

**AUBEB system-level finding:** No AUBEB phase is in the failure zone. The bond's underlying asset (mangrove ecosystem) is in the stressed zone at Phase 0, which is precisely the condition that makes restoration investable: the system is not so far degraded that external rescue is required. It has an internal recovery capacity that the bond mechanism is designed to activate.

---

## 4. Danube Basin Full Reanalysis

The Danube Basin project contains 13 parallel chains across 6 natural ecosystem chains and 7 human operation chains. This section analyzes all 65 phases (13 chains × 5 phases each) against the phi threshold.

### 4.1 Natural Ecosystem Chains

#### Natural River Channel (System average: 79.2%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | Precipitation, Snowmelt, and Catchment Recharge | 85.0% | Coherent |
| 1 | Tributary Confluence and Flow Accumulation | 85.0% | Coherent |
| **2** | **Channel Morphology and Substrate Function** | **72.0%** | **Stressed** |
| **3** | **Sediment Transport and Geomorphic Work** | **72.0%** | **Stressed** |
| 4 | Flow Delivery to Delta and Black Sea | 82.0% | Coherent |

System: 79.2% — Stressed overall. The two stressed phases reflect the consequence of upstream channelization and dam infrastructure: the Iron Gates dam complex has fundamentally altered sediment load and channel morphology throughout the middle and lower Danube. D is high (regulated flow regime, reduced bedload, altered flood pulse) while C (geomorphic work, natural channel function, substrate renewal) is suppressed. The system is stressed but functional: the river still conveys water and delivers a diminished sediment load to the delta. It is not in failure.

#### Natural Freshwater Availability (System average: 88.2%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | Atmospheric Moisture | 91.0% | Coherent |
| 1 | Precipitation over Basin | 89.0% | Coherent |
| 2 | Catchment Runoff and River Flow | 92.0% | Coherent |
| 3 | Groundwater Recharge | 83.0% | Coherent |
| 4 | Available Flow to Beneficiaries | 86.0% | Coherent |

System: 88.2% — Fully coherent. The hydrological cycle across the Danube basin is functioning well as a natural system. All phases are in the coherent zone. This is the strongest natural chain in the Danube portfolio and provides the foundational argument for the basin's resilience: the water resource itself is not at risk.

#### Natural Fish Population (System average: 78.0%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | Water Quality and Habitat Suitability | 83.0% | Coherent |
| **1** | **Habitat and Migration Corridor** | **71.0%** | **Stressed** |
| **2** | **Recruitment and Juvenile Development** | **79.0%** | **Stressed** |
| 3 | Adult Biomass and Population Dynamics | 80.0% | Coherent |
| **4** | **Harvest-Ready Population Stock** | **77.0%** | **Stressed** |

System: 78.0% — Stressed. Three of five phases are in the stressed zone. The Habitat and Migration Corridor phase at 71.0% reflects the primary ecological constraint: the Iron Gates dam blocks migration for anadromous species (beluga sturgeon, shad, asp), fragmenting the reproductive corridor. D (dam infrastructure, habitat fragmentation, pollution load) is persistently high; C (spawning success, juvenile recruitment, population replenishment) is suppressed. The system sustains some fish population, but below its natural equilibrium. Crucially: at 71.0%, the migration corridor phase remains above the phi threshold. The basin's fish population is stressed but not collapsed. Recovery is biologically possible if constraints are reduced (dam fish passes, water quality improvement).

#### Natural Reed Bed (System average: 81.4%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | Hydrological Regime and Nutrient Supply | 81.0% | Coherent |
| 1 | Reed Establishment and Colonisation | 84.0% | Coherent |
| 2 | Biomass Accumulation and Stand Maturation | 85.0% | Coherent |
| 3 | Standing Stock and Harvest-Ready Biomass | 83.0% | Coherent |
| **4** | **Ecosystem Service Delivery** | **74.0%** | **Stressed** |
| | | | |

System: 81.4% — Broadly coherent with one stressed delivery phase. The reed bed ecosystem sustains itself well through growth and maturation. The stress at Ecosystem Service Delivery (74.0%) reflects the conversion and drainage pressure on reed bed extent: D (drainage for agriculture, fire management, navigation channel maintenance) reduces the area available for service delivery. The reed bed is biologically healthy; the constraint is human land use pressure at the delivery boundary.

#### Natural Floodplain Forest Biomass (System average: 81.0%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| **0** | **Hydrological Connectivity and Flood Pulse** | **79.0%** | **Stressed** |
| 1 | Soil Formation and Nutrient Cycling | 84.0% | Coherent |
| 2 | Tree Establishment and Canopy Formation | 86.0% | Coherent |
| 3 | Biomass Accumulation and Carbon Sequestration | 82.0% | Coherent |
| **4** | **Ecosystem Service Delivery** | **74.0%** | **Stressed** |

System: 81.0% — Broadly coherent. The forest biomass accumulation process (Phases 1-3) is fully coherent. The stressed phases are at the hydrological input (Phase 0: flood pulse suppression by dams reduces annual inundation frequency and duration) and the delivery boundary (Phase 4: land use pressure reduces the area that can deliver ecosystem services). The forest itself is healthy; the constraints are at the hydrological and land boundary interfaces.

#### Natural Delta Biodiversity (System average: 82.6%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| **0** | **Basin Sediment and Nutrient Supply** | **78.0%** | **Stressed** |
| 1 | Hydrological Pulse and Connectivity | 85.0% | Coherent |
| 2 | Habitat Formation and Heterogeneity | 88.0% | Coherent |
| 3 | Species Population Dynamics | 82.0% | Coherent |
| 4 | Biodiversity Service Delivery | 80.0% | Coherent |

System: 82.6% — Coherent overall. The Danube Delta's biodiversity is broadly functional. The one stressed phase (Sediment and Nutrient Supply, 78.0%) reflects the upstream sediment deficit caused by dam trapping: reduced sediment load is constraining delta land formation and nutrient cycling. The delta is not subsiding acutely, but the supply deficit, if sustained, will eventually push Phase 0 below the phi threshold. This is the most important leading indicator of delta degradation.

---

### 4.2 Human Operation Chains

#### Human Freshwater Supply Infrastructure (System average: 88.6%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | River and Groundwater Intake | 91.0% | Coherent |
| 1 | Raw Water Conveyance | 88.0% | Coherent |
| 2 | Water Treatment | 93.0% | Coherent |
| 3 | Pressurized Distribution Network | 81.0% | Coherent |
| 4 | Consumer Delivery and Metering | 90.0% | Coherent |

System: 88.6% — Fully coherent. The human freshwater supply infrastructure across the Danube basin is the best-functioning human chain in the portfolio. All phases are in the coherent zone. This reflects decades of EU infrastructure investment, EU Drinking Water Directive compliance pressure, and the high transparency of public utility operations. This chain provides the strongest argument for the Danube basin's investability from a water security perspective.

#### Human Irrigation Infrastructure (System average: 82.0%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | River and Canal Intake | 91.0% | Coherent |
| **1** | **Primary Canal Conveyance** | **79.0%** | **Stressed** |
| **2** | **Secondary Distribution Network** | **77.0%** | **Stressed** |
| 3 | Field Application | 84.0% | Coherent |
| **4** | **Drainage and Return Flow** | **79.0%** | **Stressed** |

System: 82.0% — Coherent overall. Three phases are stressed. The pattern is consistent: intake and field application (the directly productive phases) are coherent; conveyance, distribution, and return flow (the infrastructure-intensive intermediary phases) are stressed. This reflects aging canal infrastructure, inadequate maintenance funding, and leakage losses in the secondary network. The system delivers irrigation water but at lower efficiency than its design capacity. None of these phases are in the failure zone; the improvement path (canal lining, metering, return-flow treatment) is available from within the existing system and investment programs.

#### Human Commercial Fishing (System average: 76.2%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| **0** | **Licencing, Quota Setting, and Effort Planning** | **78.0%** | **Stressed** |
| 1 | Fishing Operations and Active Harvest | 80.0% | Coherent |
| **2** | **Processing, Cold Chain, and Preservation** | **72.0%** | **Stressed** |
| **3** | **Market Access and Distribution** | **77.0%** | **Stressed** |
| **4** | **Revenue Capture and Sector Reinvestment** | **74.0%** | **Stressed** |

System: 76.2% — Stressed. Four of five phases are in the stressed zone. Commercial fishing is the most broadly stressed human chain in the Danube portfolio. The pattern reveals a sector that sustains itself (no phase below 61.8%) but operates well below its potential across the entire value chain. Regulatory overhead (quota systems across 19 countries), infrastructure underinvestment (cold chain), market fragmentation, and low reinvestment rates all contribute to sustained D-C imbalance. Under the phi framework, this is a system that can recover from within, but requires coordinated reinvestment and regulatory harmonization across the riparian countries.

#### Human Commercial Navigation (System average: 79.2%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | Governance, Regulation, and Route Planning | 83.0% | Coherent |
| **1** | **Port Infrastructure and Cargo Handling** | **78.0%** | **Stressed** |
| **2** | **Fairway Maintenance and Dredging** | **72.0%** | **Stressed** |
| 3 | Transit Operations and Lock Passage | 85.0% | Coherent |
| **4** | **Revenue Capture and Economic Impact** | **78.0%** | **Stressed** |

System: 79.2% — Stressed. Fairway Maintenance and Dredging (72.0%) is the most constrained phase: D (low-water events increasingly frequent due to climate change, regulatory restrictions on dredging in protected areas, transboundary coordination requirements) is high while C (actual maintained navigable depth, cargo volume throughput) is suppressed by recurrent low-water events. This phase is 10.2 percentage points above the phi threshold: stress is real but the system is self-sustaining. The recurring low-water events of 2017-2019 and 2022 pushed this phase operationally close to its limits but did not cross the structural threshold.

#### Human Floodplain Forestry Operations (System average: 76.2%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| **0** | **Forest Inventory and Management Planning** | **79.0%** | **Stressed** |
| 1 | Timber Harvesting and Extraction | 82.0% | Coherent |
| **2** | **Timber Processing and Value Addition** | **77.0%** | **Stressed** |
| **3** | **Market Access and Certification** | **73.0%** | **Stressed** |
| **4** | **Revenue Capture and Ecosystem Service Payments** | **70.0%** | **Stressed — lowest phase in Danube portfolio** |

System: 76.2% — Stressed. This is the lowest-scoring human chain in the Danube portfolio, and Phase 4 (Revenue Capture and Ecosystem Service Payments, 70.0%) is the lowest-scoring single phase across the entire Danube basin dataset. It is 8.2 percentage points above the phi threshold, placing it in the stressed zone — but closer to the sustainability boundary than any other Danube phase.

The structural interpretation: the forestry sector has a functioning harvesting and processing operation (Phases 1-2 are operational) but fails to capture adequate revenue and receives minimal ecosystem service payments for the carbon sequestration, flood regulation, and biodiversity services the floodplain forest provides. D is high (access restrictions in Natura 2000 zones, FSC certification requirements, competition from cheaper non-certified timber, transboundary regulatory complexity); C is suppressed (low timber prices, near-zero ecosystem service payment flows, fragmented market). The ecosystem service payment gap is a near-threshold failure: if carbon markets and nature credits do not develop to increase C, this phase risks crossing 61.8% within the decade.

#### Human Reed Industry (System average: 78.2%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | Harvest Permitting and Zone Planning | 84.0% | Coherent |
| 1 | Reed Harvesting Operations | 81.0% | Coherent |
| **2** | **Processing, Grading, and Bundling** | **77.0%** | **Stressed** |
| **3** | **Market Access and Certification** | **72.0%** | **Stressed** |
| **4** | **Revenue Capture and Sector Reinvestment** | **77.0%** | **Stressed** |

System: 78.2% — Stressed. The reed industry has coherent upstream operations (permitting and harvesting) but stressed midstream and downstream phases. The Market Access and Certification phase at 72.0% reflects the sector's challenge: Danube Delta reed must compete with cheaper imports while carrying certification overhead (ecological compliance, origin documentation). The system sustains itself, but the market-facing phases operate close to minimum viable margins.

#### Human Cultural Heritage Management (System average: 80.6%)

| Phase | Name | Balance | Zone |
|---|---|---|---|
| 0 | Heritage Inventory and Documentation | 82.0% | Coherent |
| **1** | **Site Preservation and Conservation** | **76.0%** | **Stressed** |
| 2 | Visitor Access Infrastructure | 86.0% | Coherent |
| 3 | Cultural Programming and Guided Services | 81.0% | Coherent |
| **4** | **Tourism Revenue and Sustainable Management** | **78.0%** | **Stressed** |

System: 80.6% — Coherent. The best-performing human operational chain in the Danube portfolio. Heritage management benefits from EU Cultural Heritage programs, UNESCO recognition of the Danube Delta, and relatively high visitor revenue. The two stressed phases (site preservation and tourism revenue management) reflect chronic underfunding of conservation relative to visitor load: D (conservation standards, site condition requirements, visitor safety regulations) is high while C (funding for maintenance, conservation spending) is constrained by low earmarked revenue.

---

### 4.3 Danube Basin Summary: The Phi-Threshold View

**Primary finding: No Danube phase is in the failure zone.**

Across 13 chains and 65 phases, every single Danube phase sits above the phi threshold of 61.8%. The lowest-scoring phase in the entire basin (Floodplain Forestry Revenue Capture, 70.0%) is 8.2 percentage points above the boundary. This is not marginal comfort: it means that the Danube basin, despite pervasive stress across its human operational chains, retains the structural capacity for internal recovery.

This finding is significant for investment and policy reasoning:

- Systems above the phi threshold can be improved from within by reducing constraint load or increasing contribution capacity. No Danube sub-chain requires external structural rescue.
- The interventions required (dam fish passes, canal maintenance, ecosystem service payment mechanisms, carbon market access for forestry) are all interventions that can be executed within the existing governance framework and do not require the kind of systemic policy restructuring that a failure-zone phase demands.
- Compare with the lighter's Phase 8 (56.7%): that phase requires EPR legislation, device-level producer responsibility mandates, and public decontamination infrastructure. None of the Danube phases require equivalent external structural change.

**Danube basin phase distribution:**

| Zone | Phase Count | Phase % |
|---|---|---|
| Coherent ($\geq$ 80%) | 28 phases | 43% |
| Stressed (61.8–80%) | 37 phases | 57% |
| Failure ($<$ 61.8%) | 0 phases | 0% |
| Breakdown ($<$ 38.2%) | 0 phases | 0% |

**Natural chains vs human chains:**

| Chain Type | Coherent Phases | Stressed Phases | Avg System Balance |
|---|---|---|---|
| Natural ecosystem chains (6 chains) | 19 / 30 (63%) | 11 / 30 (37%) | 82.4% |
| Human operational chains (7 chains) | 9 / 35 (26%) | 26 / 35 (74%) | 80.1% |

Natural ecosystem chains are predominantly coherent. Human operational chains are predominantly stressed. This is the phi-threshold view of a familiar observation: the Danube's natural systems are more balanced than the human systems that exploit them. The gap is 82.4% vs 80.1% at the system average level, but much more pronounced at the phase level: 63% of natural phases are fully coherent vs only 26% of human phases.

**Threshold proximity watch list:**

The following Danube phases warrant monitoring as near-threshold candidates — phases that would cross 61.8% under moderate deterioration:

| Phase | Chain | Current Balance | Distance to Threshold | Primary Risk Factor |
|---|---|---|---|---|
| Revenue Capture / Ecosystem Service Payments | Floodplain Forestry | 70.0% | 8.2 pp | Ecosystem service payment gap; certified timber price pressure |
| Market Access / Certification | Commercial Fishing | 72.0% | 10.2 pp | Multi-country quota fragmentation; cold chain underinvestment |
| Fairway Maintenance / Dredging | Commercial Navigation | 72.0% | 10.2 pp | Low-water frequency under climate change; dredging restrictions |
| Market Access / Certification | Reed Industry | 72.0% | 10.2 pp | Import competition; certification overhead |
| Habitat / Migration Corridor | Natural Fish Population | 71.0% | 9.2 pp | Iron Gates dam obstruction; spawning habitat loss |
| Sediment / Nutrient Supply | Natural Delta Biodiversity | 78.0% | 16.2 pp | Upstream dam sediment trapping; long-term delta deficit |

The floodplain forestry revenue phase is the most critical: it is the closest to the threshold, the trend is weakening (ecosystem service markets are underdeveloped), and crossing the threshold would mean the sector can no longer sustain itself without public subsidy.

---

## 5. Policy Implications of the Revised Framework

### 5.1 The Threshold Separates Two Different Types of Problem

The phi threshold is not just an analytical refinement. It reframes the intervention question:

**For stressed phases (61.8–80%):** The system can improve itself. The right interventions are: transparency investment, operational efficiency improvement, reduced regulatory complexity, market access improvement. Private capital can drive this improvement because the actor doing the investing will capture the return.

**For failure phases (below 61.8%):** The system cannot improve itself. The actors inside the chain have no incentive to close the gap because the cost of failure is externalized. The right interventions are: EPR legislation, mandatory take-back schemes, public infrastructure for missing C-side components, bond mechanisms that monetize currently unpaid externalities. Private capital will not flow here without regulatory mandate, because there is no internal return to capture.

This is the most important practical consequence of adopting the phi threshold. Policymakers, investors, and bond structurers need to know which zone they are operating in before choosing an intervention mechanism.

### 5.2 Implications for Bond Structuring (AUBEB and Danube)

Under the phi framework:

- **AUBEB:** No failure-zone phases. The bond's underlying asset is stressed but structurally recoverable. The bond mechanism (capital return that funds restoration) is the correct intervention type for a stressed-zone system.
- **Danube (potential bond):** No failure-zone phases. A Danube ecosystem bond could appropriately target the near-threshold phases (floodplain forestry revenue, commercial fishing reinvestment, fish migration corridor) with grant or blended finance structures that reduce D (regulatory complexity) or grow C (ecosystem service payment flows, carbon market access).

A bond targeting a failure-zone system (like the lighter's Phase 8) would need a different structure: it could not rely on the supply chain's internal economics to service the bond. It would require legislative mandate (EPR), fee-for-service models (producer responsibility fees), or regulatory credit markets (plastic credits) to generate the cash flow needed for debt service.

### 5.3 Recommended Changes to the Rating System

The current three-zone system should be replaced with a four-zone system using the phi-derived thresholds:

| Old Label | Old Range | New Label | New Range | Color |
|---|---|---|---|---|
| Coherent | $\geq$ 80% | **Coherent** | $\geq$ 80% | Green |
| Stressed | 70–80% | **Stressed** | 61.8–80% | Amber |
| Bottleneck | $<$ 70% | **Failure** | 38.2–61.8% | Red |
| (none) | (none) | **Breakdown** | $<$ 38.2% | Dark Red |

The change is:
1. The amber zone is extended downward from 70% to 61.8%. Phases that were previously red due to the round-number 70% cutoff but are above 61.8% are reclassified as stressed.
2. The red zone now specifically means "failure zone": the phase cannot self-sustain without external structural change.
3. A new dark red zone (below 38.2%) is reserved for breakdown-level structural collapse, which does not currently occur in any active project but provides the model with the full phi-cascade structure.

The 70% line is not discarded. It is retained as an amber-zone threshold between "stressed" and "moderately stressed," serving as the internal early-warning level within the stressed zone. It no longer determines color.

---

## 6. Summary: Active Projects Under the Phi Threshold

| Project | Total Phases Analyzed | Coherent ($\geq$ 80%) | Stressed (61.8–80%) | Failure ($<$ 61.8%) |
|---|---|---|---|---|
| Gold (chain) | 9 | 7 | 1 (Phase 6: 65.5%) | 0 |
| Gold (Mining Co. B entity) | 1 | 0 | 0 | 1 (Mine extraction: 45.3%) |
| Shea | 7 | 4 | 3 | 0 |
| Lighter | 9 | 6 | 2 | **1 (Phase 8: 56.7%)** |
| AUBEB | 11 | 9 | 2 | 0 |
| Danube (all 13 chains) | 65 | 28 | 37 | **0** |
| **Total** | **102** | **54 (53%)** | **45 (44%)** | **2 (2%)** |

Two phases across all active projects are in the failure zone:

1. **Lighter Phase 8 (End-of-Life and Waste Management, 56.7%):** A systemic supply chain phase. The entire global lighter disposal system is in structural failure. Requires: EPR legislation, device-level producer responsibility, public decontamination infrastructure. Internal chain actors cannot and will not fix this without external mandate.

2. **Gold Mining Co. B Phase 1 (Mine Extraction, 45.3%):** An entity-specific phase. One specific mining operation is in financial/operational failure. Requires: commodity price recovery, or external capital, or regulatory accommodation, or closure. The chain-level Phase 1 for gold mining as a whole remains coherent.

The other 100 phases are stressed or coherent. The Danube basin, with 65 phases and zero in the failure zone, stands as the strongest structural argument in the portfolio that ecosystem-linked investment is viable.

---

*Document prepared: April 2026. All balance scores from project JSON data files (`data/processed/*_supply_chain_ui.json`). Phi threshold derivation: `PHI_SUSTAINABILITY_THRESHOLD.md`. Mathematical basis: `023-C1-Tholonic_Math.md`. The four-zone framework described here is a proposed revision; current dashboards use the three-zone 70/80% system.*
