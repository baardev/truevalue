# Phase Discovery Instrument (PDI) — Gold Supply Chain
### Worked Example: Primary Gold — Geological Origin to Exchange-Registered Bullion

**Version 1.0 — Completed Example**
**Project: True Value Analytics — Supply Chain Intelligence**
**Based on:** PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md v1.0

> **How to read this document:** This is a fully completed example of the PDI applied to the gold supply chain. All fields are filled in. Checkbox states are shown as `[x]` (selected) or `[ ]` (not selected). Analyst notes explain any non-obvious scoring decisions. Use this as a reference when completing the blank instrument for a new material.

---

## How to Use This Document

Work through the four modules **in strict sequence**. Do not skip ahead. Each module depends on the outputs of the one before it.

| Module | Name | What you do | What you get |
|--------|------|-------------|--------------|
| **1** | Anchor the Chain | Answer seven questions once, about the whole chain | Two fixed endpoints; a list of candidate events |
| **2** | Event Inventory | For each candidate event, answer twelve questions | A scored record for every change event |
| **3** | Boundary Scoring | Apply the scoring rule to each event record | A confirmed, numbered phase map |
| **4** | Opacity Tagging | Answer four questions per confirmed phase | A transparency classification for each phase |

**Time required:** 2–4 hours for a well-documented chain. Longer for opaque or informal chains where events must be reconstructed from secondary sources.

**Who should complete it:** At minimum one person with domain knowledge of the material (to complete Module 2, Question B5). All other questions can be answered by any analyst with access to supply chain documentation.

---

---

# MODULE 1 — Anchor the Chain

> **When to use:** Once, at the start. Before listing any events.
>
> **What it does:** Establishes the two fixed endpoints of the chain (origin and market), identifies what units of measurement apply at each end, and produces a first-pass list of all change events and actors to investigate.
>
> **How to complete it:** Answer each question in writing. Be precise. Resist the temptation to describe processes here — that happens in Module 2. This module is only about naming states and actors.

---

**Material being analyzed:** Gold (Au) — primary and secondary (recycled) supply chain

**Analyst name(s):** True Value Analytics — Supply Chain Intelligence Team

**Date completed:** April 2026

**Sources consulted for this module:** World Gold Council Annual Demand Trends; LBMA Good Delivery Rules; USGS Minerals Yearbook (Gold); COMEX Daily Reports; WGC Gold Supply and Demand Statistics; Metals Focus Global Gold Mine Production Database

---

**A1. What is the material in its pre-commercial state — before any human intervention?**

Describe the physical form, location, and condition of the material as it exists in nature or at its origin point, before any extraction, harvest, or collection has occurred.

> *Answer:* Gold-bearing rock formations within the earth's crust — mineralised zones in which gold occurs as native metal, electrum (gold-silver alloy), or in association with sulphide minerals (e.g. pyrite, arsenopyrite). The gold is physically immobile, undifferentiated from its host rock, and economically undefined. It exists as part of a geological formation that may span from surface-accessible to several kilometres depth. No discrete quantity of gold can be assigned at this stage; the material has neither mass nor grade as a matter of record. Typical occurrence: disseminated low-grade deposits (0.5–2 g/t Au), high-grade veins (5–50 g/t Au), and placer deposits (alluvial or eluvial). Global distribution includes Nevada (USA), South Africa (Witwatersrand), Western Australia, Ghana, Peru, Russia, and China.

---

**A2. What is the material at the point of final market delivery — what does the end buyer or end market actually receive?**

Describe the physical form, specification, and condition of the material as it is transferred to the final purchaser or registered for market use.

> *Answer:* Exchange-registered Good Delivery gold bars — solid, rectangular bars cast to a defined specification, each bearing a unique serial number, refinery brand stamp, assay certificate, and fineness mark. Standard form for international wholesale trade: London Good Delivery bar (350–430 troy oz, 995+ fineness) or COMEX-registered bar (100 troy oz, 995+ fineness). Bars are physically held in an exchange-approved vault and represented by a warrant (legal document of title). The buyer receives either physical delivery against the warrant or the warrant itself as title to allocated metal. The material at this point is fully specified, independently assayed, legally titled, and publicly registered.

---

**A3. What unit of measurement applies at the origin state (A1)?**

> *Unit:* No unit is applicable at the pre-discovery state. Post-discovery (Phase 0 output): tonnes of mineralised rock at grade expressed as grams per tonne (g/t Au). The underlying gold quantity is expressed as contained ounces or tonnes Au within the identified resource.

---

**A4. What unit of measurement applies at the final market state (A2)?**

> *Unit:* Troy ounces (troy oz) of fine gold at stated fineness (parts per thousand, ppt). Exchange contracts and vault warrants are denominated in troy ounces. One troy ounce = 31.1035 grams.

---

**A5. Are the units in A3 and A4 the same?**

- [ ] Yes — the unit does not change across the chain
- [x] No — the unit changes at least once

> *Preliminary note on unit change location:* The unit changes at least twice across the gold supply chain. The first major change occurs at ore processing (Phase 2), where tonnes of ore at g/t grade are converted to kilogram quantities of gold in solution or concentrate. The second occurs at refining (Phase 4), where kilogram quantities of doré (expressed as kg at % purity) are converted to troy ounces of fine gold at fineness. These unit changes are strong predictors of phase boundaries and are confirmed in Module 2 Events 5 and 8.

---

**A6. List every distinct physical form the material passes through, between origin (A1) and market (A2).**

| # | Physical form | Approximate location in chain |
|---|---------------|-------------------------------|
| 1 | In-situ mineralised rock (undiscovered/unbounded) | Geological formation, pre-survey |
| 2 | Identified ore body — bounded, graded resource (in-situ) | Post-exploration survey; geological model |
| 3 | Run-of-mine (ROM) ore — broken rock, above surface | Mine site; post-extraction |
| 4 | Ground ore slurry — uniform fine particle size, suspended in water | Processing mill; pre-leach circuit |
| 5 | Pregnant leach solution / gold concentrate — gold in chemical solution or gravity concentrate | Leach circuit / CIL tanks; processing plant |
| 6 | Doré bars — solid semi-pure gold-silver alloy (60–95% Au), cast bars | Mine site smelter |
| 7 | Fine gold — chemically pure, 995+ fineness, granules or ingot | LBMA refinery |
| 8 | Good Delivery bars — cast, stamped, serially numbered, assay-certified | Refinery casting/assay facility |
| 9 | Registered bullion — bars in exchange-approved vault, warrant issued | Exchange-approved vault; COMEX/LBMA system |
| 10 | Scrap / secondary feed — used jewellery, electronics, dental, industrial scrap | Post-consumer; recycler intake |

> *Note: Form 10 (scrap) re-enters the chain at Form 6 or 7, creating a recovery loop (Phase 8).*

---

**A7. List every distinct actor class that holds or handles the material at any point in the chain.**

| # | Actor class | Approximate point in chain |
|---|-------------|---------------------------|
| 1 | Exploration company / geological surveyor | Phase 0 — resource identification |
| 2 | Mining company / mine operator | Phase 1 — extraction; may also hold through Phase 3 |
| 3 | On-site processing facility / mill operator | Phase 2 — concentration (often same entity as mine operator) |
| 4 | Mine-site smelter operator | Phase 3 — doré production (often same entity as mine operator) |
| 5 | Bullion bank / streaming company / offtake partner | Phase 3→4 transition — doré purchase |
| 6 | LBMA-accredited refinery | Phase 4 — refining; Phase 5 — bar casting and assay |
| 7 | Secure transport / logistics provider (e.g. Brinks, G4S) | Phase 6 — transport |
| 8 | Vault operator / bullion bank custodian | Phase 6 — storage |
| 9 | Exchange / exchange warehouse operator | Phase 7 — registration and delivery |
| 10 | End buyer (investor, central bank, jewellery manufacturer, industrial user) | Phase 7 exit / post-chain |
| 11 | Scrap collector / recycler / secondary refiner | Phase 8 — recovery and re-entry |

---

### Module 1 — Completion Check

Before proceeding to Module 2, confirm:

- [x] A1 and A2 are filled in with specific physical descriptions (not general statements)
- [x] A3 and A4 have explicit units of measurement
- [x] A6 has at least three distinct physical forms listed
- [x] A7 has at least three distinct actor classes listed

---

---

# MODULE 2 — Event Inventory

> **When to use:** After Module 1 is complete. Repeat this module once for every candidate event.
>
> **What is an event?** An event is anything that changes any of the following: the physical form of the material, who holds it, where it is, what process is being applied to it, or who owns it. When in doubt, record it as an event — Module 3 will determine whether it rises to phase-boundary level.
>
> **How to identify events:** Use the physical forms listed in A6 and the actor classes listed in A7 as your starting point. Each transition between forms is an event. Each transition between actor classes is an event. Add any additional events you identify through research.
>
> **How to complete it:** Copy or reproduce this module for each event. Fill in every field. Where an answer is genuinely unknown, mark it `UNKNOWN` and note the reason. Do not leave fields blank.

---

**Total events identified for this chain: 12**

*(Events 3, 4, and 7 scored as sub-processes. All others confirmed as phase boundaries. See Module 3.)*

---

### Event Record — Event 1 of 12

**Event name / short description:** Geological survey and ore body delineation

**Sources consulted for this event:** USGS Mineral Resources Program; S&P Global Market Intelligence Reserves Database; JORC Code / NI 43-101 resource classification standards; company exploration reports (public filings)

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Undifferentiated, unmapped mineralised rock formations within the earth's crust. Gold exists in trace quantities distributed through host rock. No boundary, no grade measurement, no quantity assigned. Material is physically indistinguishable from non-mineralised rock without chemical analysis.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Geologically delineated ore body — a bounded volume of mineralised rock with a measured or estimated gold grade (g/t Au), classified under a recognised resource standard (JORC/NI 43-101) as Measured, Indicated, or Inferred resource. The material remains physically in-situ (unmoved), but is now quantified, bounded, and legally defined within an exploration or mining licence area.

---

**B3. Are B1 and B2 the same physical form?**

- [x] Yes — physical state is unchanged across this event (material remains in-situ rock)
- [ ] No — physical state changes across this event

> *Note: The rock itself does not move or transform. However, its status changes from unquantified to quantified and bounded — a definitional transformation. Physical form: unchanged. Definitional state: fundamentally changed.*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* None — material has no assigned unit before survey
>
> *Unit leaving this event:* Million tonnes (Mt) of ore at grade (g/t Au); contained gold expressed as Moz (million troy ounces) or tonnes Au

- [x] Yes — unit changes *(flag: +1 toward boundary score)*
- [ ] No — same unit throughout

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [x] **Aggregative** — geological survey gathers and synthesises data about the ore body without physically extracting or transforming it
- [ ] Chemical / Thermal
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [ ] Commercial

> *Notes:* Geological surveying is classified as Aggregative because it assembles information about a physical resource without altering the material. The output is a data product (resource model) that defines the material, not a transformed physical product. This is the closest available classification.

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* None — this is the first event in the chain.

- [x] Yes — process class changes (no prior class → Aggregative) *(flag: +1 toward boundary score)*
- [ ] No — same process class continues

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* No holder — material is in-situ geological formation. Nominal sovereign ownership in most jurisdictions rests with the national government or landowner.
>
> *Specific name (if known):* State/Crown (mineral rights holder); specific national jurisdiction varies.

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Exploration company / mining licence holder
>
> *Specific name (if known):* Named in exploration licence filing; examples include Barrick Gold, Newmont, AngloGold Ashanti at project level.

---

**B9. Are B7 and B8 the same entity?**

- [ ] Yes — physical custody is unchanged
- [x] No — an exploration licence is granted; legal rights over the defined resource are formally assigned to the mining company *(flag: +1 toward boundary score)*

> *Note:* The physical material does not move. However, legal rights over a now-defined, bounded resource are transferred from the state/landowner to the licensed exploration/mining company. This constitutes a custody change at the definitional level: the resource is now formally held by a named legal entity.

---

**B10. Does legal ownership of the material change across this event?**

- [x] Yes — exploration/mining licence grants legal rights to extract the resource to the licence holder *(flag: +1 toward boundary score)*
- [ ] No — same owner before and after
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Measured + Indicated + Inferred resource in million tonnes at g/t Au grade; total contained gold in Moz Au
>
> *Approximate volume (per year, per season, or per cycle):* Varies by deposit. Global new resource additions: approximately 80–120 Moz new resources defined per year across all projects (WGC / S&P Global). Individual deposit examples: Carlin Trend (Nevada) ~40 Moz; Mponeng (South Africa) ~60 Moz defined resource.
>
> *Named recipient (actor class or specific entity):* Exploration/mining company named in exploration licence; geological resource classified under JORC/NI 43-101 and disclosed in public filings.

- [ ] No

---

### Event 1 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | No — physical form unchanged | 0 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | Yes — first event | 1 |
| Physical custody changed (B9 = No) | Yes — legal rights assigned to licence holder | 1 |
| Legal ownership changed (B10 = Yes) | Yes | 1 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 5**

---

### Event Record — Event 2 of 12

**Event name / short description:** Primary mine extraction — ore separated from host rock

**Sources consulted for this event:** USGS Minerals Yearbook (Gold); WGC Gold Supply and Demand Statistics; company Annual Reports (mine production tables); SNL Metals & Mining Database

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* In-situ ore body — gold-bearing rock, still in the ground, identified and bounded from Event 1. The material is physically immobile within the geological formation.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Run-of-mine (ROM) ore — physically broken, excavated rock extracted from the pit or underground workings and stockpiled above surface at the mine site. Gold remains distributed throughout the rock matrix at mill-head grade. The material is now mobile, above ground, and under active physical custody.

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes
- [x] No — fundamental physical state change: material transitions from immobile, in-ground geological formation to mobile, above-ground broken ore *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Tonnes in-situ resource at g/t Au (resource estimate)
>
> *Unit leaving this event:* Tonnes run-of-mine ore at mill head grade (g/t Au) — operationally measured at the crushing circuit

- [x] Yes — unit changes from resource estimate to operational mill feed measurement *(flag: +1 toward boundary score)*
- [ ] No

---

**B5. What class of process is applied during this event?**

- [x] **Extractive** — ore is physically separated from its geological origin by drilling, blasting, loading, and hauling
- [ ] Aggregative
- [ ] Chemical / Thermal
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Aggregative (Event 1)

- [x] Yes — Aggregative → Extractive *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* Mining company (holds mineral rights and exploration licence; material is in-ground)
>
> *Specific name (if known):* Mine operator named in mining lease — e.g. Newmont Mining Corp (Carlin, Nevada); Gold Fields (South Deep, South Africa)

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Mine operator (now with active physical custody of above-ground broken ore)
>
> *Specific name (if known):* Same mine operator; material held at ROM pad / primary crusher stockpile on mine site.

---

**B9. Are B7 and B8 the same entity?**

- [ ] Yes
- [x] No — before extraction, the mine operator held legal rights to in-situ material but not physical custody of a discrete, movable mass. After extraction, active physical custody of a defined, weighed quantity of broken ore is established for the first time. *(flag: +1 toward boundary score)*

> *Note:* Same legal entity, but the nature of custody changes categorically: rights over immobile in-ground resource → active physical custody of a movable, quantified stockpile. This is treated as a custody establishment event.

---

**B10. Does legal ownership of the material change across this event?**

- [x] Yes — upon legal extraction, ROM ore becomes the property of the mine operator under the terms of the mining lease *(flag: +1 toward boundary score)*
- [ ] No
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Tonnes ROM ore at mill head grade (g/t Au)
>
> *Approximate volume (per year, per season, or per cycle):* Global primary mine production approximately 3,300–3,600 tonnes Au contained per year (WGC). ROM ore volumes typically 50–500 Mt/year across all operations. Individual mine example: Muruntau (Uzbekistan) ~80 Mt ROM ore/year; Grasberg (Indonesia) ~200,000 t/day.
>
> *Named recipient (actor class or specific entity):* Mine operator (self-held); ROM ore stockpile at mine site under mine operator's direct control.

- [ ] No

---

### Event 2 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | Yes | 1 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | Yes — active custody established | 1 |
| Legal ownership changed (B10 = Yes) | Yes | 1 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 6**

---

### Event Record — Event 3 of 12

**Event name / short description:** Ore stockpile management and transport to processing mill

**Sources consulted for this event:** Mine operational reports; internal logistics documentation (not publicly available); industry process engineering references

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* ROM ore — broken rock at mine stockpile, awaiting processing.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* ROM ore — same broken rock, now delivered to the primary crusher intake at the processing mill. Physical form is identical.

---

**B3. Are B1 and B2 the same physical form?**

- [x] Yes — no physical or chemical change; material is transported, not transformed
- [ ] No

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Tonnes ROM ore
>
> *Unit leaving this event:* Tonnes ROM ore (same unit)

- [ ] Yes
- [x] No — same unit throughout

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [ ] Chemical / Thermal
- [ ] Specification
- [ ] Certification
- [x] **Custodial** — haul truck transport and stockpile management; no material transformation
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Extractive (Event 2)

- [x] Yes — Extractive → Custodial *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* Mine operator
>
> *Specific name (if known):* Same mine operator as Event 2

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Mine operator / processing facility (typically same legal entity; different physical location on site)
>
> *Specific name (if known):* Same entity; material is now at mill intake

---

**B9. Are B7 and B8 the same entity?**

- [x] Yes — same organisation holds material throughout; transport is internal
- [ ] No

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes
- [x] No — same owner throughout
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [ ] Yes

- [x] **No** — mill feed tonnage is measured internally by the mine operator using belt weighers and truck tallies, but this data is not independently verifiable from outside the operation. The quantity delivered to the crusher is proprietary operational data.

---

**B12. What is the reason the output cannot be measured?**

- [ ] (a) Informal practice
- [x] **(b) Commercial secrecy** — mill feed rates and ROM delivery tonnages are internal operational metrics not disclosed publicly. Mine production reports show annual totals but not event-level throughput.
- [ ] (c) Physical inaccessibility

---

### Event 3 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | No | 0 |
| Unit of measurement changed (B4 = Yes) | No | 0 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | No | 0 |
| Legal ownership changed (B10 = Yes) | No | 0 |
| Measurable output exists (B11 = Yes) | No | 0 |

**Raw boundary score: 1**

> *Score 1 = Sub-process. Confirmed sub-process within Phase 1 (mine extraction zone). The ore has not transformed; custody has not transferred; output is not independently measurable.*

---

### Event Record — Event 4 of 12

**Event name / short description:** Crushing, grinding, and slurry preparation

**Sources consulted for this event:** Comminution and mineral processing engineering references; mine environmental impact assessments (public); plant design documentation (private)

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* ROM ore — irregular, variable-size broken rock (fragments up to 1–2 metres diameter), delivered to primary crusher intake.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Fine ground ore slurry — uniform particle size (typically 75–150 microns), suspended in water to form a pumpable slurry. The rock matrix is physically disaggregated; gold particles are now liberated from host rock and accessible to chemical leaching agents.

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes
- [x] No — significant physical transformation: irregular rock → fine uniform slurry *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Tonnes ROM ore
>
> *Unit leaving this event:* Tonnes ore (solids) per unit volume of slurry — still measured in tonnes, but expressed as slurry density. Unit class is the same.

- [ ] Yes
- [x] No — measurement remains in mass units (tonnes); the form of expression changes but the fundamental unit does not

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [x] **Chemical / Thermal** — mechanical comminution (crushing and grinding) followed by water addition to form slurry; classified as Chemical/Thermal due to the energy-intensive mechanical and water-chemistry process
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Custodial (Event 3)

- [x] Yes — Custodial → Chemical/Thermal *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* Mine operator / processing facility
>
> *Specific name (if known):* Same mine operator; material at crusher intake

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Processing facility (mill operator — same entity as mine operator in most integrated operations)
>
> *Specific name (if known):* Same entity; material now in grinding circuit / thickener.

---

**B9. Are B7 and B8 the same entity?**

- [x] Yes — same entity throughout grinding circuit
- [ ] No

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes
- [x] No — same owner
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [ ] Yes

- [x] **No** — the slurry output of the grinding circuit is an internal intermediate product. It is not independently measured or reported. It proceeds directly into the leach circuit without a defined handoff point.

---

**B12. What is the reason the output cannot be measured?**

- [ ] (a) Informal practice
- [ ] (b) Commercial secrecy
- [x] **(c) Physical inaccessibility** — the slurry is a continuous flowing intermediate within a closed processing plant. There is no structural point at which a third party could independently verify the quantity or gold content of the material at this stage.

---

### Event 4 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | Yes | 1 |
| Unit of measurement changed (B4 = Yes) | No | 0 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | No | 0 |
| Legal ownership changed (B10 = Yes) | No | 0 |
| Measurable output exists (B11 = Yes) | No | 0 |

**Raw boundary score: 2**

> *Score 2 = Candidate boundary. B11 = No → Sub-process. Despite the physical form change, the absence of a measurable output means this event cannot constitute a phase boundary. It is a sub-process within Phase 2 (ore processing and concentration). This is the scoring rule in action: a physical state change alone is insufficient without a definable child-N output.*

---

### Event Record — Event 5 of 12

**Event name / short description:** Chemical leaching and gold concentration

**Sources consulted for this event:** WGC Gold Mine Production methodology notes; USGS mineral processing references; CIL/CIP technology references; mine environmental permits (public); company sustainability reports (recovery rate disclosures)

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Fine ground ore slurry — gold particles liberated from host rock matrix, suspended in water, entering the leach circuit (Carbon-in-Leach or Carbon-in-Pulp circuit, or heap leach pad).

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Pregnant leach solution (PLS) or loaded carbon — a gold-bearing aqueous cyanide solution in which gold has been chemically dissolved from the slurry, or gold adsorbed onto activated carbon granules. Gold is now chemically separated from the rock matrix and exists as a discrete, recoverable quantity in solution or on carbon. The host rock remains as barren tailings.

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes
- [x] No — fundamental chemical separation: gold is now isolated from host rock as a discrete chemical species in solution *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Tonnes ore slurry (gold content expressed as g/t)
>
> *Unit leaving this event:* Grams per litre (g/L) gold in solution, or kg Au on loaded carbon — a concentration unit rather than a bulk mass unit

- [x] Yes — unit changes from bulk ore mass (g/t) to gold-specific concentration (g/L or kg Au) *(flag: +1 toward boundary score)*
- [ ] No

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [x] **Chemical / Thermal** — cyanide leaching (chemical dissolution of gold from rock matrix); carbon adsorption; counter-current decantation
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Chemical/Thermal (Event 4)

- [ ] Yes
- [x] No — both Events 4 and 5 are Chemical/Thermal processes; the class does not change

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* Processing facility / mine operator
>
> *Specific name (if known):* Same mine operator; material in leach feed thickener

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Processing facility / mine operator
>
> *Specific name (if known):* Same mine operator; loaded carbon or PLS held in elution circuit or electrowinning cell

---

**B9. Are B7 and B8 the same entity?**

- [x] Yes — same entity throughout
- [ ] No

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes
- [x] No — same owner
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Kilograms of gold recovered in solution or on loaded carbon, expressed as kg Au at estimated concentration (derived from feed grade and metallurgical recovery rate)
>
> *Approximate volume (per year, per season, or per cycle):* Recovery rates typically 85–93% of mill head grade. At global production of ~3,300 t Au/year from primary mines, approximately 2,800–3,100 t Au enters solution annually. Individual mine example: Goldstrike (Nevada) approximately 25–30 t Au/year recovered in leach circuit.
>
> *Named recipient (actor class or specific entity):* Mine operator / processing facility (self-held; material proceeds directly to electrowinning or carbon stripping circuit).

- [ ] No

---

### Event 5 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | Yes | 1 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | No | 0 |
| Physical custody changed (B9 = No) | No | 0 |
| Legal ownership changed (B10 = Yes) | No | 0 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 3**

> *Score 3 = Candidate boundary. B11 = Yes → CONFIRMED PHASE BOUNDARY. Phase 2 is confirmed. Note: the process class did not change (both Events 4 and 5 are Chemical/Thermal), which kept the score at 3. However, the combination of physical state change, unit change, and a measurable output is sufficient to confirm this as a phase boundary per Rule 2.*

---

### Event Record — Event 6 of 12

**Event name / short description:** On-site smelting — production of doré bars

**Sources consulted for this event:** Mine site process flow diagrams (public); company sustainability reports; LBMA doré trade flow analysis; Metals Focus Gold Mines Database

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Gold-bearing cathode (electrowinning product) — a spongy gold-silver precipitate produced by passing electric current through the pregnant leach solution. Typically 50–90% Au with silver, base metal impurities, and moisture. Physically resembles a grey-brown metallic sponge or powder.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Doré bars — solid, rectangular cast bars of semi-pure gold-silver alloy. Typically 60–95% gold content with 5–40% silver and trace impurities. Each bar weighs approximately 25–35 kg. The bars are discrete, countable physical objects that can be individually weighed, labelled, and inventoried for the first time in the supply chain.

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes
- [x] No — transformation from metallic sponge/precipitate to solid cast bar: a discrete, countable physical object is produced for the first time *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Kg Au in precipitate (gold content, not total mass)
>
> *Unit leaving this event:* Kg doré (total bar mass) at stated purity (% Au by assay)

- [x] Yes — unit shifts from gold-content measurement (kg Au) to total-mass-at-purity (kg doré at % Au) *(flag: +1 toward boundary score)*
- [ ] No

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [x] **Chemical / Thermal** — high-temperature furnace smelting: precipitate is dried, fluxed, and melted; impurities are oxidised and removed as slag; molten alloy is poured into bar moulds and allowed to solidify
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Chemical/Thermal (Event 5)

- [ ] Yes
- [x] No — both Events 5 and 6 are Chemical/Thermal; process class is continuous

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* Mine operator / processing facility (electrowinning cell)
>
> *Specific name (if known):* Same mine operator; cathode deposit in electrowinning cell

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Mine operator / mine-site smelter (secure storage facility)
>
> *Specific name (if known):* Same entity in most integrated mines; doré bars held in mine's secure vault or bullion room pending dispatch.

---

**B9. Are B7 and B8 the same entity?**

- [x] Yes — typically the same mine operator controls the smelter; in toll-smelting arrangements a third party may hold the bars temporarily
- [ ] No

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes
- [x] No — mine operator retains ownership of the doré bars until a commercial sale or toll-refining agreement is executed (typically at Event 7)
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Kg doré bars at % Au purity; number of bars; total contained Au (kg)
>
> *Approximate volume (per year, per season, or per cycle):* Global doré production approximately 3,300–3,500 t Au-equivalent per year (primary only). Individual mine example: Kibali (DRC, Barrick/AngloGold) approximately 15–17 t Au per year in doré.
>
> *Named recipient (actor class or specific entity):* Mine operator (self-held in mine vault); pending commercial dispatch to LBMA refinery.

- [ ] No

---

### Event 6 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | Yes | 1 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | No | 0 |
| Physical custody changed (B9 = No) | No | 0 |
| Legal ownership changed (B10 = Yes) | No | 0 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 3**

> *Score 3 = Candidate boundary. B11 = Yes → CONFIRMED PHASE BOUNDARY. Phase 3 is confirmed. The same reasoning as Event 5 applies: the combination of physical state change, unit change, and measurable output confirms the boundary despite the process class being continuous. A countable, weighable, inventoriable physical object (doré bar) now exists for the first time — this is a structurally significant N-state.*

---

### Event Record — Event 7 of 12

**Event name / short description:** Doré packaging, assay, and transport to LBMA-accredited refinery

**Sources consulted for this event:** LBMA doré trade documentation guidelines; secure transport provider operational procedures (Brinks, G4S — partial public); commercial doré purchase agreement structures (industry standard terms)

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Doré bars at mine vault — solid, cast, individually labelled bars of gold-silver alloy, accompanied by mine assay certificate.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Doré bars at refinery intake dock — physically identical bars, now in the possession of the refinery, accompanied by transport manifest and updated assay documentation.

---

**B3. Are B1 and B2 the same physical form?**

- [x] Yes — bars are physically unchanged during transport
- [ ] No

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Kg doré at % Au purity
>
> *Unit leaving this event:* Kg doré at % Au purity (same)

- [ ] Yes
- [x] No — same unit

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [ ] Chemical / Thermal
- [ ] Specification
- [ ] Certification
- [x] **Custodial** — secure transport of physical bars from mine site to refinery; no material transformation occurs
- [ ] Commercial

> *Note:* A commercial transaction (doré sale or toll-refining agreement) typically accompanies this transfer, but the physical process is custodial. The commercial element is noted but does not change the process class.

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Chemical/Thermal (Event 6)

- [x] Yes — Chemical/Thermal → Custodial *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* Mine operator (secure vault)
>
> *Specific name (if known):* Mine operator; examples: Barrick, Newmont, Gold Fields

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* LBMA-accredited refinery (intake custody)
>
> *Specific name (if known):* Examples: Rand Refinery (South Africa), Metalor (Switzerland), Umicore (Belgium), Asahi Refining (USA/Japan)

---

**B9. Are B7 and B8 the same entity?**

- [ ] Yes
- [x] No — custody transfers from mine operator to independent LBMA refinery *(flag: +1 toward boundary score)*

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes
- [ ] No
- [x] Unknown / unverifiable — ownership transfer depends on commercial arrangement. In outright doré sale: ownership transfers to refinery on intake. In toll refining: mine operator retains ownership; refinery holds as bailee. Arrangement is commercially confidential and varies by counterparty.

> *Note:* UNKNOWN classification does not score a point, but is noted as a structural opacity in the chain. The question of who legally owns the gold between mine and refinery is not publicly determinable.

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [ ] Yes

- [x] **No** — the quantity of doré received at the refinery is not publicly disclosed. Transport manifests and refinery intake receipts are commercially confidential documents. The mine may disclose aggregate annual doré production, but the specific shipment quantities are not publicly verifiable.

---

**B12. What is the reason the output cannot be measured?**

- [ ] (a) Informal practice
- [x] **(b) Commercial secrecy** — doré shipment quantities, refinery intake receipts, and commercial terms are confidential between mine operator and refinery. No public reporting requirement exists for individual shipment volumes.
- [ ] (c) Physical inaccessibility

---

### Event 7 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | No | 0 |
| Unit of measurement changed (B4 = Yes) | No | 0 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | Yes | 1 |
| Legal ownership changed (B10 = Yes) | Unknown — 0 | 0 |
| Measurable output exists (B11 = Yes) | No | 0 |

**Raw boundary score: 2**

> *Score 2 = Candidate boundary. B11 = No → Sub-process. Despite the custody transfer to an independent refinery, the absence of a measurable output and the unverifiable ownership status means this event cannot confirm a new phase. It is classified as a sub-process or transitional step within Phase 3 (doré production / custody zone). The Phase 4 boundary will be established when the refining transformation is completed and a measurable output exists.*

---

### Event Record — Event 8 of 12

**Event name / short description:** Electrolytic and/or acid refining to fine gold

**Sources consulted for this event:** LBMA Good Delivery Rules; WGC Gold Supply and Demand — Refinery Production; Metals Focus Refinery Output Database; LBMA Annual Report (global refinery capacity)

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Doré bars at LBMA refinery — semi-pure gold-silver alloy, 60–95% Au, in custody of the refinery.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Fine gold — chemically pure gold at 995+ fineness (99.5% minimum purity), produced via electrolytic refining (Wohlwill process) or acid refining (Miller chlorination process). At this point, gold is chemically separated from silver and base metal impurities. The material exists as granules, anodes, or ingots of high-purity gold, ready for bar casting.

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes
- [x] No — fundamental chemical transformation: semi-pure alloy (60–95% Au) → fine gold (995+ purity); silver and base metals chemically removed *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Kg doré at % Au purity
>
> *Unit leaving this event:* Troy ounces (troy oz) of fine gold at stated fineness (ppt)

- [x] Yes — shift from mass-at-purity (kg doré at %) to standard precious metal unit (troy oz at fineness) *(flag: +1 toward boundary score)*
- [ ] No

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [x] **Chemical / Thermal** — Miller process: chlorine gas passed through molten doré to oxidise and remove impurities; or Wohlwill process: electrolytic dissolution and re-deposition of pure gold
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Custodial (Event 7)

- [x] Yes — Custodial → Chemical/Thermal *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* LBMA-accredited refinery
>
> *Specific name (if known):* Refinery named in doré intake documentation (e.g. Rand Refinery, Metalor, Umicore)

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* LBMA-accredited refinery (same entity; now holds fine gold product)
>
> *Specific name (if known):* Same refinery

---

**B9. Are B7 and B8 the same entity?**

- [x] Yes — refinery retains physical custody throughout the refining process
- [ ] No

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes
- [x] No — in toll refining, ownership returns to mine operator/client upon production of fine gold; in outright purchase, refinery owns throughout. In either case, no additional ownership transfer event occurs within this event itself.
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Troy ounces of fine gold at stated fineness; refinery production record
>
> *Approximate volume (per year, per season, or per cycle):* Global refinery throughput approximately 4,500–5,000 t Au per year (including recycled feed). Primary mine-sourced fine gold: approximately 3,300–3,600 t Au/year. LBMA member refineries collectively report total output; individual refinery volumes from Metals Focus / LBMA reporting.
>
> *Named recipient (actor class or specific entity):* Client (mine operator or bullion bank) receives fine gold credit against refinery account; physical metal held by refinery pending bar casting.

- [ ] No

---

### Event 8 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | Yes | 1 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | No | 0 |
| Legal ownership changed (B10 = Yes) | No | 0 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 4**

> *CONFIRMED PHASE BOUNDARY. Phase 4 is confirmed. The combination of physical state change, unit change, process class change, and measurable output clears the confirmed-boundary threshold. Note: Event 7 (transport) scored as a sub-process, meaning Phase 4 begins definitionally at the refining transformation, with the transport/custody event considered preparatory.*

---

### Event Record — Event 9 of 12

**Event name / short description:** Bar casting, formal assay, and LBMA Good Delivery certification

**Sources consulted for this event:** LBMA Good Delivery Rules (current edition); LBMA Good Delivery List (public); LBMA Bar Specifications; independent assayer accreditation lists

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Fine gold — 995+ fineness, in granule, anode, or ingot form, held at LBMA refinery.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* LBMA Good Delivery gold bars — cast rectangular bars meeting full specification: 350–430 troy oz weight, 995+ fineness, refinery brand stamp, unique serial number, year of manufacture, assay certificate issued by an independent LBMA-accredited assayer. Each bar is individually identified and legally traceable.

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes
- [x] No — fine gold (unformed, no serial identity) → standardised, serialised, legally specified bar *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Troy ounces of fine gold (quantity measurement)
>
> *Unit leaving this event:* Good Delivery bars (individually identified physical objects, each with a specific troy oz weight and fineness)

- [x] Yes — shift from fungible quantity (troy oz) to discrete, identified physical units (individual bars with serial numbers) *(flag: +1 toward boundary score)*
- [ ] No

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [ ] Chemical / Thermal
- [ ] Specification
- [x] **Certification** — the defining activity of this event is the independent assay and LBMA Good Delivery certification; bar casting is preparatory to certification
- [ ] Custodial
- [ ] Commercial

> *Note:* Bar casting is a Specification sub-process (bringing gold to bar form and weight). The Certification activity (independent assay, serial registration, Good Delivery stamp) is the phase-defining transformation.

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Chemical/Thermal (Event 8)

- [x] Yes — Chemical/Thermal → Certification *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* LBMA-accredited refinery
>
> *Specific name (if known):* Same refinery as Event 8

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* LBMA-accredited refinery / vault operator (bars may be placed in vault immediately after certification)
>
> *Specific name (if known):* Refinery vault or client-nominated vault

---

**B9. Are B7 and B8 the same entity?**

- [x] Yes — refinery retains physical custody; bars may be held in refinery vault
- [ ] No

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes
- [x] No — ownership does not change at certification; title is already established
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Individual Good Delivery bars, each with serial number, weight (troy oz), and fineness (ppt) — independently verifiable via LBMA bar integrity programme
>
> *Approximate volume (per year, per season, or per cycle):* Approximately 100,000–120,000 new Good Delivery bars produced annually from primary supply (estimate; LBMA does not publish bar production totals). LBMA Approved Weighers and Assayers list is public.
>
> *Named recipient (actor class or specific entity):* Client (mine operator, bullion bank) credited with specific bar serial numbers in refinery account.

- [ ] No

---

### Event 9 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | Yes | 1 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | No | 0 |
| Legal ownership changed (B10 = Yes) | No | 0 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 4**

> *CONFIRMED PHASE BOUNDARY. Phase 5 is confirmed.*

---

### Event Record — Event 10 of 12

**Event name / short description:** Secure transport to bullion vault and formal custody transfer

**Sources consulted for this event:** Brinks / G4S / Malca-Amit logistics (partial public); LBMA Vaulting Provider list (public); bullion bank vault operator disclosures (partial); Bank of England vault list (public)

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Good Delivery bars — certified, serialised gold bars at refinery or refinery vault.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Good Delivery bars — physically identical; now held in a third-party bullion bank vault or exchange-approved warehouse under formal custodial agreement.

---

**B3. Are B1 and B2 the same physical form?**

- [x] Yes — bars are physically unchanged
- [ ] No

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Individual Good Delivery bars (serial numbers and troy oz)
>
> *Unit leaving this event:* Same — bars remain individually identified

- [ ] Yes
- [x] No — same unit

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [ ] Chemical / Thermal
- [ ] Specification
- [ ] Certification
- [x] **Custodial** — secure physical transport and formal vault intake; no material transformation
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Certification (Event 9)

- [x] Yes — Certification → Custodial *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* LBMA-accredited refinery
>
> *Specific name (if known):* Refinery (e.g. Rand Refinery, Metalor)

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Bullion bank vault operator / LBMA vault provider (independent third party)
>
> *Specific name (if known):* Bank of England; HSBC Vault (London); JPMorgan Chase Vault; Brinks Vault (various); G4S Logistics; ICBC Standard Bank Vault

---

**B9. Are B7 and B8 the same entity?**

- [ ] Yes
- [x] No — custody transfers from refinery to independent third-party vault operator *(flag: +1 toward boundary score)*

---

**B10. Does legal ownership of the material change across this event?**

- [x] Yes — in most cases, bars are sold to a bullion bank or client at this point; ownership passes at vault intake *(flag: +1 toward boundary score)*
- [ ] No
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Named Good Delivery bars (serial numbers recorded at vault intake); troy oz on vault receipt
>
> *Approximate volume (per year, per season, or per cycle):* LBMA vault holdings in London alone: approximately 9,000 t Au (~290 Moz) held in aggregate across LBMA member vaults (Bank of England + commercial vaults). Annual flows not publicly disclosed at individual vault level.
>
> *Named recipient (actor class or specific entity):* Named bullion bank or investor client; bars held in allocated account at vault operator. Vault operator issues vault receipt or holding statement.

- [ ] No

---

### Event 10 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | No | 0 |
| Unit of measurement changed (B4 = Yes) | No | 0 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | Yes | 1 |
| Legal ownership changed (B10 = Yes) | Yes | 1 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 4**

> *CONFIRMED PHASE BOUNDARY. Phase 6 is confirmed. Note: despite no physical transformation or unit change (scores of 0 for those criteria), the combination of custody transfer to an independent vault operator, ownership transfer, and measurable output is sufficient to confirm a new phase. The nature of the activity changes categorically from certification to custody management.*

---

### Event Record — Event 11 of 12

**Event name / short description:** Exchange warrant registration and market delivery

**Sources consulted for this event:** COMEX Daily Warehouse Reports (public, daily); LBMA Clearing Statistics (public, monthly); COMEX Rulebook; NYMEX delivery procedures; LBMA Global OTC Market documentation

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Good Delivery bars in vaulted custody — bars physically held in vault under bullion bank or investor ownership; not yet exchange-registered.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Exchange-registered deliverable bullion — same physical bars, now formally registered in an exchange system (COMEX or LBMA clearing), with a warrant (legal instrument of title) issued and recorded. The bar is now a deliverable unit within an exchange contract. Ownership can be transferred by warrant transfer without physical movement of the bar.

---

**B3. Are B1 and B2 the same physical form?**

- [x] Yes — bars are physically unchanged; the transformation is legal/commercial
- [ ] No

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* Individual bars (troy oz, serial number)
>
> *Unit leaving this event:* Exchange contract units (COMEX: 100 troy oz contracts; LBMA: clearing lots of 5,000-6,000 troy oz)

- [x] Yes — bars are aggregated or divided into standardised exchange contract units *(flag: +1 toward boundary score)*
- [ ] No

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [ ] Aggregative
- [ ] Chemical / Thermal
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [x] **Commercial** — registration with exchange, warrant issuance, legal delivery mechanism established; change in legal status and market access

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Custodial (Event 10)

- [x] Yes — Custodial → Commercial *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* Vault operator / bullion bank (on behalf of owner)
>
> *Specific name (if known):* LBMA vault operator or COMEX-approved warehouse (e.g. Brinks, Malca-Amit, Loomis, HSBC)

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Exchange-approved warehouse operator (bars remain in same physical vault but are now under exchange jurisdiction)
>
> *Specific name (if known):* COMEX-approved warehouses in New York/Delaware; LBMA clearing members in London

---

**B9. Are B7 and B8 the same entity?**

- [ ] Yes
- [x] No — registration with exchange changes the custodial regime; bars are now held under exchange rules and subject to exchange delivery obligations *(flag: +1 toward boundary score)*

---

**B10. Does legal ownership of the material change across this event?**

- [x] Yes — warrant holder can sell the warrant (and thus the gold) without physical movement; ownership transfer is now a paperless exchange transaction *(flag: +1 toward boundary score)*
- [ ] No
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Troy ounces registered in exchange warehouse; number of warrants issued; open interest in exchange delivery
>
> *Approximate volume (per year, per season, or per cycle):* COMEX registered gold inventory: typically 8–30 Moz (varies widely with market conditions); COMEX eligible inventory: additional 15–35 Moz. Daily changes publicly reported. LBMA clearing: approximately 18–25 Moz cleared daily (LBMA statistics).
>
> *Named recipient (actor class or specific entity):* Warrant holder (investor, bullion bank, central bank, industrial buyer); publicly registered in exchange system.

- [ ] No

---

### Event 11 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | No | 0 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | Yes | 1 |
| Legal ownership changed (B10 = Yes) | Yes | 1 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 5**

> *CONFIRMED PHASE BOUNDARY. Phase 7 is confirmed. Highest-transparency phase in the chain: COMEX publishes daily registered and eligible inventory; warrants are a legal instrument of record.*

---

### Event Record — Event 12 of 12

**Event name / short description:** Post-consumer scrap collection, sorting, and re-entry to refining

**Sources consulted for this event:** WGC Gold Supply and Demand Statistics (recycling data); Metals Focus Gold Focus (recycling chapter); LBMA recycling flow data; United Nations Comtrade (scrap gold trade codes HS 7112)

---

**B1. What is the physical form of the material entering this event?**

> *Answer:* Post-consumer gold-bearing material — used jewellery (broken, damaged, or unwanted), electronic scrap (circuit boards, connectors), dental gold (crowns, bridges), and industrial scrap. Gold content ranges from <1% (electronics) to ~75% (18-carat jewellery). Material is physically heterogeneous, mixed with other metals, plastics, and non-metallic materials.

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:* Sorted, assessed gold-bearing feed material — scrap categorised by type and approximate gold content, physically sorted by class, awaiting delivery to secondary refinery or LBMA-accredited refinery for processing. Material is no longer mixed with end-use items; it is industrial feed.

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes
- [x] No — post-consumer items → categorised industrial feed; physical transformation through sorting and de-manufacturing *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:* No standard unit (heterogeneous consumer items)
>
> *Unit leaving this event:* Kg feed material at estimated % Au content; or kg Au equivalent (assay-estimated)

- [x] Yes — shift from unquantified consumer material to industrial feed with estimated gold content *(flag: +1 toward boundary score)*
- [ ] No

---

**B5. What class of process is applied during this event?**

- [ ] Extractive
- [x] **Aggregative** — collection, sorting, assessment, and bulking of scrap material prior to refining; no chemical transformation
- [ ] Chemical / Thermal
- [ ] Specification
- [ ] Certification
- [ ] Custodial
- [ ] Commercial

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:* Commercial (Event 11)

- [x] Yes — Commercial → Aggregative *(flag: +1 toward boundary score)*
- [ ] No

---

**B7. Who physically holds the material immediately before this event begins?**

> *Actor class:* End consumer / retail holder (jewellery owner, electronics recycler, dental practice)
>
> *Specific name (if known):* Dispersed individual and institutional holders; no named custodian class

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:* Scrap dealer / secondary gold recycler / refinery intake
>
> *Specific name (if known):* Commercial scrap dealers (e.g. CJ Environmental, Metallix Refining), electronics recyclers (e.g. Umicore), jewellery trade buy-back programmes

---

**B9. Are B7 and B8 the same entity?**

- [ ] Yes
- [x] No — custody transfers from dispersed end consumers to specialist scrap handlers *(flag: +1 toward boundary score)*

---

**B10. Does legal ownership of the material change across this event?**

- [x] Yes — scrap is sold by end consumers to dealers or recyclers; ownership transfers on sale *(flag: +1 toward boundary score)*
- [ ] No
- [ ] Unknown / unverifiable

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

- [x] **Yes** *(flag: +1 toward boundary score)*

> *Quantity and unit:* Tonnes Au equivalent recovered from recycling per year
>
> *Approximate volume (per year, per season, or per cycle):* Global gold recycling approximately 1,100–1,300 t Au/year (WGC, 2022–2024 range). Jewellery recycling approximately 700–900 t/year; electronics approximately 200–300 t/year; other approximately 50–100 t/year. Re-enters chain at Phase 4 (LBMA refinery intake) or Phase 5 (re-casting).
>
> *Named recipient (actor class or specific entity):* Secondary refinery or LBMA-accredited refinery scrap intake (e.g. Umicore, Heraeus, Italpreziosi).

- [ ] No

---

### Event 12 — Boundary Score Calculation

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | Yes | 1 |
| Unit of measurement changed (B4 = Yes) | Yes | 1 |
| Process class changed (B6 = Yes) | Yes | 1 |
| Physical custody changed (B9 = No) | Yes | 1 |
| Legal ownership changed (B10 = Yes) | Yes | 1 |
| Measurable output exists (B11 = Yes) | Yes | 1 |

**Raw boundary score: 6**

> *CONFIRMED PHASE BOUNDARY. Phase 8 is confirmed. Recovery and recycling constitutes a distinct phase re-entering the chain at Phase 4 or 5.*

---

---

# MODULE 3 — Boundary Scoring and Phase Map

> **When to use:** After all Event Records (Module 2) are complete.
>
> **What it does:** Applies a consistent scoring rule to every event, determines which events are confirmed phase boundaries, and produces the numbered phase map.
>
> **How to complete it:** Transfer the boundary scores from all Event Records into the master table below. Then apply the interpretation rules. Phase numbers are assigned in sequence from origin to market.

---

### Step 3.1 — Master Event Score Table

| Event # | Event name | Score (0–6) | B11 output defined? | Preliminary interpretation |
|---------|------------|-------------|---------------------|---------------------------|
| 1 | Geological survey and resource delineation | 5 | [x] Yes | Confirmed boundary |
| 2 | Primary mine extraction | 6 | [x] Yes | Confirmed boundary |
| 3 | Ore stockpile and transport to mill | 1 | [ ] No | Sub-process |
| 4 | Crushing, grinding, and slurry preparation | 2 | [ ] No | Sub-process (B11=No overrides score 2) |
| 5 | Chemical leaching and gold concentration | 3 | [x] Yes | Confirmed boundary (score 3, B11=Yes) |
| 6 | On-site smelting to doré bars | 3 | [x] Yes | Confirmed boundary (score 3, B11=Yes) |
| 7 | Doré transport and custody transfer to refinery | 2 | [ ] No | Sub-process (B11=No overrides score 2) |
| 8 | Electrolytic / acid refining to fine gold | 4 | [x] Yes | Confirmed boundary |
| 9 | Bar casting, assay, and Good Delivery certification | 4 | [x] Yes | Confirmed boundary |
| 10 | Secure transport to vault and custody transfer | 4 | [x] Yes | Confirmed boundary |
| 11 | Exchange warrant registration | 5 | [x] Yes | Confirmed boundary |
| 12 | Post-consumer scrap collection and re-entry | 6 | [x] Yes | Confirmed boundary |

---

### Step 3.2 — Apply Interpretation Rules

**Rule 1 — Sub-process:** Score 0–1 → sub-process regardless of B11.
*Applied to: Event 3 (score 1).*

**Rule 2 — Candidate boundary:** Score 2–3 → confirm if B11=Yes; sub-process if B11=No.
*Applied to: Event 4 (score 2, B11=No → sub-process); Event 5 (score 3, B11=Yes → confirmed); Event 6 (score 3, B11=Yes → confirmed); Event 7 (score 2, B11=No → sub-process).*

**Rule 3 — Confirmed boundary:** Score 4–6 → confirmed regardless of B11.
*Applied to: Events 1, 2, 8, 9, 10, 11, 12.*

**Analyst note on Events 3 and 4:** Both are custodial/mechanical sub-processes that occur between Phases 1 and 2. They have been assigned to Phase 1 (post-extraction, pre-concentration zone). The phase boundary is drawn at Event 5 (chemical leaching), where the first measurable gold-specific output is produced.

**Analyst note on Event 7:** This custody transfer (doré to refinery) scores only 2 with B11=No. The ownership arrangement is commercially opaque. This is the most structurally significant opacity in the gold supply chain: at the point where gold leaves the mine operator and enters the refinery, the specific quantity, terms, and legal ownership status are not publicly verifiable. This is noted as the primary opacity gap between Phase 3 and Phase 4.

---

### Step 3.3 — Confirmed Phase Map

| Phase # | Phase name | Begins at (event #) | Ends at / transitions to (event #) | Child N output (from B11) |
|---------|------------|--------------------|------------------------------------|--------------------------|
| 0 | Geological occurrence and resource delineation | Event 1 | → Event 2 | Identified ore body: Mt at g/t Au, contained Moz Au |
| 1 | Primary mine extraction | Event 2 | → Event 5 (via sub-processes 3, 4) | ROM ore: tonnes/year at mill head grade (g/t Au) |
| 2 | Ore processing and gold concentration | Event 5 | → Event 6 | Gold in solution/concentrate: kg Au/year at g/L or % grade |
| 3 | Doré production | Event 6 | → Event 8 (via sub-process 7) | Doré bars: kg/year at % Au purity |
| 4 | Refining to fine gold | Event 8 | → Event 9 | Fine gold: troy oz/year at fineness (ppt) |
| 5 | Bar casting and Good Delivery certification | Event 9 | → Event 10 | Certified Good Delivery bars: count and troy oz, serial-numbered |
| 6 | Logistics and vaulted custody | Event 10 | → Event 11 | Bars in named vault: troy oz under formal custodial agreement |
| 7 | Exchange registration and market delivery | Event 11 | → end of primary chain | Registered warrants: troy oz in exchange system |
| 8 | Post-consumer recovery and recycling | Event 12 | → re-enters at Phase 4 or 5 | Scrap feed: tonnes Au equivalent/year entering secondary refining |

---

### Step 3.4 — Sub-process Register

| Event # | Event name | Belongs to Phase # | Reason for sub-process classification |
|---------|------------|--------------------|-----------------------------------------|
| 3 | Ore stockpile and transport to mill | 1 | Score 1; no physical transformation, no custody change, no measurable output |
| 4 | Crushing, grinding, and slurry preparation | 2 | Score 2, B11=No; physical form changes but no measurable gold-specific output; internal closed process |
| 7 | Doré transport and custody transfer to refinery | 3 | Score 2, B11=No; custody changes but quantity is commercially confidential and ownership arrangement is unverifiable |

---

---

# MODULE 4 — Opacity Tagging

> **When to use:** After the Phase Map (Module 3, Step 3.3) is confirmed.
>
> **What it does:** Assigns a transparency classification to each confirmed phase based on four measurability tests.
>
> **How to complete it:** For each confirmed phase, answer the four questions below.

---

### Opacity Record — Phase 0: Geological Occurrence and Resource Delineation

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [x] Yes — source: S&P Global Market Intelligence Reserves Database; JORC/NI 43-101 public disclosure filings; USGS Mineral Resources Program; WGC Mine Production Statistics. Global total resource base approximately 50,000–60,000 t Au in identified resources.
- [ ] No

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [x] Yes — source: Mining company exploration licence filings (public in most jurisdictions); ASX/NYSE/TSX listed company annual resource statements. Major operators (Newmont, Barrick, AngloGold Ashanti, Gold Fields, Kinross) publish JORC/NI 43-101 resource reports.
- [ ] No

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [ ] Yes
- [x] No — reason: geological survey data and resource models are produced by the mining company's technical team. Independent verification (QP sign-off under NI 43-101; Competent Person under JORC) is required for public reporting, but the underlying drill data, assay results, and geological interpretation are held by the company and not subject to third-party audit in real time. The in-situ material cannot be independently accessed.

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [ ] Yes
- [x] No — reason: the transition from Phase 0 (identified resource) to Phase 1 (extraction) is determined by the mine operator's production decision. The quantity of resource that begins to be extracted in any given period is not independently verifiable; production rates are self-reported.

---

**Opacity score: 2** (C1=Yes, C2=Yes, C3=No, C4=No)

**Transparency classification:** [ ] High [x] Medium [ ] Low

**Primary reason for opacity:** Commercial secrecy — geological detail, drill data, and mine planning decisions are proprietary.

---

### Opacity Record — Phase 1: Primary Mine Extraction

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [x] Yes — source: WGC Gold Supply and Demand Statistics (quarterly, by country); USGS Minerals Yearbook; company Annual Reports (mine-level production tables); SNL Metals & Mining Database. Global production approximately 3,300–3,600 t Au/year.
- [ ] No

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [x] Yes — source: Listed mining companies disclose operating mines, production by mine, and operator details. WGC and Metals Focus maintain mine-level production databases. Major mine operators are publicly known.
- [ ] No

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [ ] Yes
- [x] No — reason: underground and open-pit mine operations are physically accessible only to authorised personnel. Ore grade, extraction rate, and ROM stockpile tonnage are measured internally. Environmental impact assessments provide some external data points, but day-to-day extraction rates are not independently verifiable.

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [ ] Yes
- [x] No — reason: mill feed tonnage delivered to the processing plant is an internal measurement. The handoff between extraction and processing is not independently verifiable; ROM ore stockpile quantities are not externally audited.

---

**Opacity score: 2** (C1=Yes, C2=Yes, C3=No, C4=No)

**Transparency classification:** [ ] High [x] Medium [ ] Low

**Primary reason for opacity:** Physical inaccessibility — extraction operations are not open to independent observation; internal tonnage measurements are proprietary.

---

### Opacity Record — Phase 2: Ore Processing and Gold Concentration

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [ ] Yes
- [x] No — reason: processing plant throughput (tonnes ore milled, recovery rates, leach circuit performance) is operational data disclosed only at an annual aggregate level in company reports. Quarterly or event-level data is not publicly available. WGC global production statistics capture the output (gold produced) but not the processing stage volume specifically.

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [x] Yes — source: Processing plants are operated by the mine operator (usually the same legal entity as Phase 1). Operator identity is publicly known from licence and company disclosures.
- [ ] No

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [ ] Yes
- [x] No — reason: leach circuits and processing plants are closed industrial facilities. Reagent use, recovery rates, and gold content in solution are internal measurements not subject to third-party verification during operation.

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [ ] Yes
- [x] No — reason: the gold content of the pregnant leach solution entering the smelter circuit is an internal measurement. There is no external audit or published record of the gold quantity at this intermediate stage.

---

**Opacity score: 1** (C1=No, C2=Yes, C3=No, C4=No)

**Transparency classification:** [ ] High [ ] Medium [x] Low

**Primary reason for opacity:** Physical inaccessibility — closed processing plant; internal intermediate measurements not externally verifiable.

---

### Opacity Record — Phase 3: Doré Production

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [ ] Yes
- [x] No — reason: doré production volumes are disclosed annually per mine in company reports, but at the phase level (i.e. kg doré at % purity), the data is aggregated into gold-equivalent ounce production figures. Individual doré batch production data is not publicly available.

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [x] Yes — source: Mine operators holding doré are publicly known from company disclosures. Major doré producers include Barrick, Newmont, AngloGold Ashanti, Gold Fields, Kinross — all publicly listed with named operating mines.
- [ ] No

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [ ] Yes
- [x] No — reason: smelter operations are within the mine site perimeter. Doré bar production, purity, and weight are determined by the mine operator's assay team or an invited third-party assayer. Independent verification of production volumes is not structurally possible.

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [x] Yes — mechanism: doré bars are accompanied by an assay certificate (mine assay or agreed third-party assay). Transport manifest and refinery intake documentation provide a paper trail. In dispute cases, a "umpire assay" by an independent LBMA-approved assayer is used to confirm content.
- [ ] No

---

**Opacity score: 2** (C1=No, C2=Yes, C3=No, C4=Yes)

**Transparency classification:** [ ] High [x] Medium [ ] Low

**Primary reason for opacity:** Commercial secrecy — doré shipment quantities and commercial terms between mine operators and refineries are not publicly reported.

---

### Opacity Record — Phase 4: Refining to Fine Gold

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [x] Yes — source: WGC Gold Supply and Demand Statistics include a refinery output estimate; LBMA Annual Report includes aggregate member refinery throughput; Metals Focus Gold Focus provides refinery output by country. Global refinery throughput approximately 4,500–5,000 t Au/year.
- [ ] No

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [x] Yes — source: LBMA Good Delivery Refiner List is public and updated; lists approximately 68 accredited refineries globally with name, country, and annual capacity. Refineries include Rand Refinery, Metalor, Umicore, Heraeus, Asahi, Tanaka, and others.
- [ ] No

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [ ] Yes
- [x] No — reason: refinery processes (electrolytic cells, acid treatment circuits) are closed industrial facilities. Input quantities (doré intake) and output quantities (fine gold) are measured internally by the refinery. LBMA accreditation requires an audit of processes, but specific throughput at any given time is not externally verifiable.

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [ ] Yes
- [x] No — reason: fine gold output quantities at individual refineries are not publicly reported. LBMA aggregate figures exist, but they do not allow confirmation of a specific refinery's output in a given period.

---

**Opacity score: 2** (C1=Yes, C2=Yes, C3=No, C4=No)

**Transparency classification:** [ ] High [x] Medium [ ] Low

**Primary reason for opacity:** Commercial secrecy — individual refinery throughput is proprietary; refinery production records are not disclosed.

---

### Opacity Record — Phase 5: Bar Casting and Good Delivery Certification

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [x] Yes — source: LBMA Good Delivery bar production is partially inferable from LBMA Approved Weighers and Assayers records; WGC production statistics; bar serial number registries (LBMA Bar Integrity Programme). Total bars in LBMA system partially trackable.
- [ ] No

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [x] Yes — source: LBMA Good Delivery Refiner List (public); LBMA Approved Assayer List (public); LBMA Approved Weigher List (public). All bars produced under LBMA Good Delivery rules carry a refinery brand stamp that identifies the producer.
- [ ] No

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [x] Yes — mechanism: LBMA Good Delivery accreditation requires independent assay of bars by an LBMA Approved Assayer. Each bar is independently weighed and assayed before receiving Good Delivery status. The assay certificate is a third-party verified document. LBMA proactive monitoring programme conducts random assay checks on bars in the system.
- [ ] No

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [x] Yes — mechanism: LBMA Bar Integrity Programme tracks bar serial numbers; each Good Delivery bar has a unique serial number recorded at production. Bar lists in vault systems are reconciled. The output (a specific, serialised, assayed bar) is independently verifiable from bar documentation.
- [ ] No

---

**Opacity score: 4** (C1=Yes, C2=Yes, C3=Yes, C4=Yes)

**Transparency classification:** [x] High [ ] Medium [ ] Low

> *Phase 5 is the highest-transparency phase in the primary production chain. The Good Delivery system is specifically designed to create an independently verifiable, serialised physical product. This is the point at which the chain transitions from opaque industrial production to a publicly auditable physical asset.*

---

### Opacity Record — Phase 6: Logistics and Vaulted Custody

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [ ] Yes
- [x] No — reason: the volume of gold in private vault custody is not publicly disclosed. The Bank of England publishes aggregate London vault holdings (approximately 400,000 bars / ~5,000 t Au as of 2024), but commercial vault holdings by individual banks or logistics operators are not publicly reported. LBMA published vault holding statistics aggregated from member reporting, but these do not constitute independent verification.

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [ ] Yes
- [x] No — reason: while the names of vault operators and bullion banks are publicly known (Bank of England, HSBC, JPMorgan, Brinks, G4S), the specific bars held by any given vault at any given time are not publicly disclosed. There is no registry of which specific bars are in which vault. The LBMA vault list identifies approved operators but not holdings.

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [ ] Yes
- [x] No — reason: vault interiors are physically inaccessible to third parties. Storage and transport operations are not subject to independent observation. Audits of vault contents (e.g. Bank of England NAO audit) are rare, periodic, and do not constitute continuous external verification.

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [ ] Yes
- [x] No — reason: the transfer of specific bars from vault custody to exchange registration is not publicly reported at the individual transaction level. COMEX daily reports show changes in registered/eligible inventory, but the specific bars moved and the parties involved are not disclosed.

---

**Opacity score: 0** (C1=No, C2=No, C3=No, C4=No)

**Transparency classification:** [ ] High [ ] Medium [x] Low

**Primary reason for opacity:** Physical inaccessibility combined with commercial secrecy — vault contents are structurally unobservable; no public disclosure requirements exist for private vault holdings.

> *This is the lowest-transparency phase in the gold supply chain. It represents the structural opacity gap between certified production (Phase 5) and exchange registration (Phase 7). The quantity of gold held in private vault custody at any given time is not independently verifiable. This opacity is structural, not intentional — it reflects the nature of secure vault operations rather than any specific actor's behaviour.*

---

### Opacity Record — Phase 7: Exchange Registration and Market Delivery

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [x] Yes — source: COMEX Daily Warehouse Reports (registered and eligible gold, daily); LBMA Clearing Statistics (monthly); LBMA Vault Statistics (monthly aggregate). COMEX registered inventory: publicly available, updated daily.
- [ ] No

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [x] Yes — source: COMEX Approved Warehouse list is public; LBMA vault operator list is public; exchange-approved depository operators are named in exchange rules. Examples: Brinks (New York), Malca-Amit (New York), Manfra Tordella & Brookes, HSBC (London).
- [ ] No

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [x] Yes — mechanism: exchange registration is a legal/administrative process governed by published exchange rules (COMEX Rulebook, LBMA documentation). Warrant issuance is a formal legal act subject to exchange oversight. Exchange auditors have access to warehouse records. The registration process itself is verifiable.
- [ ] No

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [x] Yes — mechanism: COMEX daily reports show bar-level changes in registered inventory; warrant transfers are recorded in exchange systems; LBMA clearing confirmations are reported. Delivery against contract is a publicly reported event at the contract level.
- [ ] No

---

**Opacity score: 4** (C1=Yes, C2=Yes, C3=Yes, C4=Yes)

**Transparency classification:** [x] High [ ] Medium [ ] Low

> *Phase 7 is the highest-transparency phase in the entire chain — the only phase where daily, public, bar-level data is available. This is a consequence of exchange reporting requirements, not of industry practice. The contrast with Phase 6 (score 0) immediately preceding it is the sharpest transparency discontinuity in the gold supply chain.*

---

### Opacity Record — Phase 8: Post-Consumer Recovery and Recycling

---

**C1. Can the volume throughput of this phase be measured from public sources?**

- [x] Yes — source: WGC Gold Supply and Demand Statistics (annual recycling totals by category); Metals Focus Gold Focus (recycling chapter); UN Comtrade HS 7112 (precious metal waste and scrap trade flows). Global recycling approximately 1,100–1,300 t Au/year.
- [ ] No

---

**C2. Can the identity of custodians in this phase be publicly established?**

- [ ] Yes
- [x] No — reason: the scrap collection chain is highly fragmented. It involves millions of individual transactions between consumers, retail jewellers, pawnshops, scrap dealers, and secondary refiners. While major secondary refiners (Umicore, Heraeus, Italpreziosi) are publicly known, the intermediate scrap collection network is informal and not mapped.

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

- [ ] Yes
- [x] No — reason: scrap sorting, assessment, and aggregation occurs across a dispersed informal network. There is no central point at which a third party can observe or verify the process. Consumer-to-dealer transactions are almost entirely undocumented.

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

- [x] Yes — mechanism: secondary refineries (LBMA-accredited) receive scrap feed under commercial intake agreements. Intake records at the refinery level exist and are auditable. LBMA reporting captures recycled gold entering the formal system. The re-entry point (Phase 4 or 5) is verifiable at the refinery intake level.
- [ ] No

---

**Opacity score: 2** (C1=Yes, C2=No, C3=No, C4=Yes)

**Transparency classification:** [ ] High [x] Medium [ ] Low

**Primary reason for opacity:** Informal practice — the consumer-to-dealer segment of the scrap collection chain is structurally undocumented; collection volumes are estimated, not measured at the transaction level.

---

---

# SUMMARY — Completed Phase Map

**Material:** Gold (Au) — primary mine production and secondary recovery

**Date completed:** April 2026

**Analysts:** True Value Analytics — Supply Chain Intelligence Team

| Phase # | Phase name | Physical state (in → out) | Child N output | Custodian class | Transparency |
|---------|------------|--------------------------|---------------|-----------------|--------------|
| 0 | Geological occurrence and resource delineation | Undifferentiated mineral formation → bounded, graded ore body (in-situ) | Identified resource: Mt at g/t Au (contained Moz Au) | Exploration/mining company | Medium |
| 1 | Primary mine extraction | In-situ ore body → run-of-mine (ROM) ore, above surface | ROM ore: tonnes/year at mill head grade (g/t Au) | Mine operator | Medium |
| 2 | Ore processing and gold concentration | ROM ore slurry → pregnant leach solution / gold concentrate | Gold in solution: kg Au/year at g/L concentration | Mine operator / processing facility | Low |
| 3 | Doré production | Gold concentrate / cathode → solid doré bars | Doré bars: kg/year at % Au purity; bar count | Mine operator (mine vault) | Medium |
| 4 | Refining to fine gold | Doré bars → fine gold (995+ fineness) | Fine gold: troy oz/year at stated fineness (ppt) | LBMA-accredited refinery | Medium |
| 5 | Bar casting and Good Delivery certification | Fine gold → serialised, assay-certified Good Delivery bars | Certified bars: count; troy oz; serial-numbered and assay-certified | LBMA refinery / approved assayer | High |
| 6 | Logistics and vaulted custody | Good Delivery bars (at refinery) → bars held in third-party bullion vault | Bars in vault: troy oz under formal custodial agreement | Vault operator / bullion bank | Low |
| 7 | Exchange registration and market delivery | Bars in vault → exchange-registered deliverable bullion (warrant) | Registered warrants: troy oz in COMEX / LBMA exchange system | Exchange-approved warehouse | High |
| 8 | Post-consumer recovery and recycling | Post-consumer gold-bearing scrap → sorted industrial feed → re-enters at Phase 4 or 5 | Scrap feed: tonnes Au equivalent/year entering secondary refining | Scrap dealer / secondary refinery | Medium |

---

**Total confirmed phases:** 9 (Phases 0–8)

**High transparency phases:** 2 (Phase numbers: 5, 7)

**Medium transparency phases:** 5 (Phase numbers: 0, 1, 3, 4, 8)

**Low transparency phases:** 2 (Phase numbers: 2, 6)

**Sub-processes identified and assigned:** 3 (Events 3, 4, 7)

**Events where B11 output could not be defined:** 3 (Events 3, 4, 7 — all classified as sub-processes; none were overridden by score ≥ 4)

---

### Analyst Notes

**On the Phase 2 Low transparency rating:** Phase 2 (ore processing) is the least visible phase in primary gold production. The chemical leaching and concentration process occurs entirely within a closed industrial plant. No external party can independently verify the gold content at this stage. This is a structural opacity, not a commercial choice: the material is dissolved in solution and physically inaccessible. The WGC production figures that appear in public reporting represent the output of Phase 3 (doré), not Phase 2. Phase 2's transparency rating of Low reflects that the concentration step — where the largest volumetric transformation occurs — is effectively unobservable from outside the plant.

**On the Phase 6 zero-score opacity:** The vault custody phase (Phase 6) receives an opacity score of zero — all four measurability tests fail. This is the single most analytically significant finding from this instrument. It means that the segment of the gold supply chain between Good Delivery certification (Phase 5, High transparency) and exchange registration (Phase 7, High transparency) is structurally unobservable. What volume of gold is held in private vault custody, by whom, and under what terms, cannot be determined from public sources. This is the primary basis for the project's structural opacity classification of this phase.

**On Event 7 as sub-process (doré to refinery):** The scoring instrument correctly identified the doré-to-refinery transfer as a sub-process rather than a phase boundary, because the output (specific doré quantity at refinery intake) is commercially confidential. This reflects a genuine structural gap: the handoff between mine operators and LBMA refineries is the least well-documented transition in the formal chain. It is the point where the quantity of gold "disappears" into a commercially confidential bilateral relationship.

**On Phase 8 re-entry point:** Phase 8 (recycling) is the only non-linear phase. Its child-N output re-enters at Phase 4 (refinery) or Phase 5 (casting) depending on the quality of the scrap feed. This means the physical chain is not a single linear sequence but contains a recovery loop. The instrument handles this correctly by noting the re-entry phase_id rather than forcing a linear continuation.

**Sources not available that would improve this analysis:** Individual mine-level doré production at batch/shipment level (Phase 3 output); refinery intake volumes by counterparty (Phase 3→4 transition); individual vault holdings by operator and bar serial number (Phase 6); specific warrant-to-owner mapping in COMEX/LBMA systems (Phase 7 internal).

---

---

*Phase Discovery Instrument v1.0 — Gold Supply Chain Worked Example*
*Aligned with: Abstract Supply Chain Phase Template | N-D-C Tholonic Framework*
*Cross-reference: ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE_GOLD_INSTANCE.md | PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md*
