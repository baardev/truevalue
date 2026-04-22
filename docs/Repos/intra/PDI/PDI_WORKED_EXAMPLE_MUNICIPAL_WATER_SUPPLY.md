# Phase Discovery Instrument (PDI) — Municipal Drinking Water
### Worked Example: Simplest Possible Supply Chain

**Version 1.0 — Completed Example**
**Project: True Value Analytics — Supply Chain Intelligence**
**Based on:** PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md v1.0

> **Purpose of this document:** This is the simplest possible completed example of the PDI. It uses municipal drinking water — a chain every person on earth interacts with daily — to demonstrate how the instrument works before applying it to a complex commodity. Compare with the gold example (PDI_WORKED_EXAMPLE_GOLD_SUPPLY_CHAIN.md) to see how the same questions scale across complexity levels.

---

## How to Use This Document

Work through the four modules **in strict sequence**. Do not skip ahead. Each module depends on the outputs of the one before it.

| Module | Name | What you do | What you get |
|--------|------|-------------|--------------|
| **1** | Anchor the Chain | Answer seven questions once, about the whole chain | Two fixed endpoints; a list of candidate events |
| **2** | Event Inventory | For each candidate event, answer twelve questions | A scored record for every change event |
| **3** | Boundary Scoring | Apply the scoring rule to each event record | A confirmed, numbered phase map |
| **4** | Opacity Tagging | Answer four questions per confirmed phase | A transparency classification for each phase |

---

---

# MODULE 1 — Anchor the Chain

> **When to use:** Once, at the start. Before listing any events.
>
> **What it does:** Establishes the two fixed endpoints of the chain, identifies what units apply at each end, and produces a first-pass list of all change events and actors.
>
> **How to complete it:** Answer each question in writing. Be precise. This module is only about naming states and actors — not describing processes.

---

**Material being analyzed:** Drinking water (municipal tap water supply)

**Analyst name(s):** True Value Analytics — worked example

**Date completed:** April 2026

**Sources consulted for this module:** UK Water Industry Act 1991; Drinking Water Inspectorate (DWI) annual reports; Water Services Regulation Authority (Ofwat) published standards; WHO Guidelines for Drinking-water Quality; general municipal water utility operational documentation

---

**A1. What is the material in its pre-commercial state — before any human intervention?**

> *Answer:* Rainwater and surface water naturally accumulated in a river, lake, or underground aquifer. The water exists in its natural hydrological state — untreated, unquantified in terms of licensed allocation, and not yet connected to any supply infrastructure. It is chemically and biologically variable: it contains dissolved minerals, organic matter, sediment, and microorganisms at concentrations determined by the natural catchment environment. No specific quantity has been assigned; no abstraction right exists yet.

---

**A2. What is the material at the point of final market delivery — what does the end buyer or end market actually receive?**

> *Answer:* Treated potable water delivered under pressure at the consumer's tap — water that meets the legal drinking water standard for the jurisdiction (e.g. UK Drinking Water Standards: residual chlorine ≥0.1 mg/L; turbidity <1 NTU; pH 6.5–9.5; coliform bacteria = 0 per 100 mL). The water is metered, billed, and delivered continuously through a pressurised network. The consumer receives a measured volume of a legally specified product.

---

**A3. What unit of measurement applies at the origin state (A1)?**

> *Unit:* No unit applicable before abstraction licence. Post-identification: megalitres (ML) or cubic metres (m³) of available flow in the source water body, expressed as mean annual flow or available yield.

---

**A4. What unit of measurement applies at the final market state (A2)?**

> *Unit:* Cubic metres (m³) of potable water meeting specified water quality parameters, metered at the consumer connection point. Billing unit is typically m³ or litres.

---

**A5. Are the units in A3 and A4 the same?**

- [ ] Yes
- [x] No — the unit changes from "raw water volume in a natural body" to "treated water volume meeting a quality specification." The underlying volume unit (m³) is the same, but the specification dimension is added at the treatment phase, representing a real change in what is being measured.

> *Preliminary note on unit change location:* The specification change occurs at the chemical treatment event — when raw water is transformed into water meeting the legal drinking water standard. Confirmed in Module 2, Event 4.

---

**A6. List every distinct physical form the material passes through, between origin (A1) and market (A2).**

| # | Physical form | Approximate location in chain |
|---|---------------|-------------------------------|
| 1 | Natural source water — river, lake, or aquifer; untreated, unallocated | In situ; natural environment |
| 2 | Abstracted raw water — physically removed from source, in intake channel or raw water main | Water intake structure; start of treatment works |
| 3 | Pre-treated water — coarsely filtered, sedimented; still raw, not potable | Within treatment works; pre-chemical stage |
| 4 | Treated potable water — chemically dosed, microbiologically safe, meeting drinking water standard | Treatment works output; service reservoir |
| 5 | Pressurised distribution water — potable water held at pressure in the distribution network | Service reservoir; trunk mains; local distribution pipes |
| 6 | Delivered tap water — water at consumer connection, metered | Consumer premises |

---

**A7. List every distinct actor class that holds or handles the material at any point in the chain.**

| # | Actor class | Approximate point in chain |
|---|-------------|---------------------------|
| 1 | Environment agency / regulator (issues abstraction licence) | Phase 0 — licensing |
| 2 | Water utility / water company (abstracts, treats, distributes) | Phases 1–4 — all operational phases |
| 3 | Distribution network operator (may be same as water utility) | Phase 3 — distribution |
| 4 | Consumer / end user | Phase 4 — consumption |

> *Note: This is the simplest actor map of any supply chain presented in this project. In many municipal systems, a single water utility performs all roles from abstraction to billing.*

---

### Module 1 — Completion Check

- [x] A1 and A2 are filled in with specific physical descriptions
- [x] A3 and A4 have explicit units of measurement
- [x] A6 has at least three distinct physical forms listed
- [x] A7 has at least three distinct actor classes listed

---

---

# MODULE 2 — Event Inventory

> **Total events identified for this chain: 6**
>
> *(Event 3 scored as sub-process. Events 1, 2, 4, 5, 6 confirmed as phase boundaries.)*

---

### Event Record — Event 1 of 6

**Event name / short description:** Source identification and abstraction licence grant

**Sources consulted for this event:** Environment Agency abstraction licence register (public); Catchment Abstraction Management Strategy (CAMS) documents; water company Water Resource Management Plans (public)

---

**B1.** Undifferentiated natural water body — river, lake, or aquifer — with no assigned allocation or abstraction right.

**B2.** Named, measured water source with a legally defined abstraction licence: permitted volume (ML/year or ML/day), intake point location, and licence holder identified. Water remains physically in the source; the licence defines the quantity and conditions under which it may be taken.

**B3. Are B1 and B2 the same physical form?**
- [x] Yes — water remains in natural source; physical form is unchanged

**B4. Does the unit of measurement change?**
> Unit in: None (no assigned quantity)
> Unit out: ML/year licensed abstraction volume; river flow in ML/day

- [x] Yes — unit changes from undefined to licensed volume allocation *(+1)*

**B5. Process class:**
- [x] **Aggregative** — survey, assessment, and licensing; information and legal process, not material transformation

**B6. Process class change from preceding?**
> Prior: None (first event)
- [x] Yes — first event in chain *(+1)*

**B7.** Before: Environment / no holder. The water body is a natural commons.
**B8.** After: Water utility (holds abstraction licence; named as licence holder in Environment Agency register)

**B9. Same entity?**
- [x] No — abstraction licence formally assigns the right to take this water to a named water utility *(+1)*

**B10. Legal ownership changes?**
- [x] Yes — abstraction licence is a legal right to property (the water); granted by regulator to water utility *(+1)*

**B11. Measurable output?**
- [x] Yes *(+1)*
> Quantity: Licensed abstraction volume — e.g. 50 ML/day from [River X] at [Grid Reference]
> Volume: Stated in licence; publicly registered
> Recipient: Named water utility (licence holder)

### Event 1 — Boundary Score

| Criterion | Score |
|-----------|-------|
| Physical state changed | 0 |
| Unit changed | 1 |
| Process class changed | 1 |
| Custody changed | 1 |
| Ownership changed | 1 |
| Measurable output | 1 |

**Raw boundary score: 5 → CONFIRMED. Phase 0.**

---

### Event Record — Event 2 of 6

**Event name / short description:** Water abstraction — raw water enters the supply system

**Sources consulted for this event:** Water company operational reports; Drinking Water Inspectorate (DWI) reports; water utility annual performance reviews (Ofwat)

---

**B1.** Natural water in river / lake / aquifer — in its natural environment.

**B2.** Raw water — same water, now physically pumped or gravity-fed through the intake structure into the raw water main. The water has left the natural environment and is now confined within an engineered system under the water utility's direct control.

**B3. Same physical form?**
- [ ] Yes
- [x] No — water transitions from free-flowing natural body to confined, controlled flow within engineered infrastructure *(+1)*

**B4. Unit change?**
> Unit in: ML available in source water body
> Unit out: ML/day abstracted flow at intake meter

- [x] Yes — shift from natural body volume to metered intake flow rate *(+1)*

**B5. Process class:**
- [x] **Extractive** — water is physically separated from its natural source by pumping or gravity intake

**B6. Process class change?**
> Prior: Aggregative (Event 1)
- [x] Yes — Aggregative → Extractive *(+1)*

**B7.** Natural water body / environment.
**B8.** Water utility (intake infrastructure; raw water main)

**B9. Same entity?**
- [x] No — active physical custody of a defined, flowing, metered quantity is established for the first time *(+1)*

**B10. Ownership change?**
- [x] Yes — water utility exercises its licensed right; abstracted water becomes the utility's property *(+1)*

**B11. Measurable output?**
- [x] Yes *(+1)*
> Quantity: ML/day raw water at intake meter
> Volume: e.g. 50 ML/day (continuous metered measurement at intake)
> Recipient: Water utility (self-held; raw water main)

### Event 2 — Boundary Score

| Criterion | Score |
|-----------|-------|
| Physical state changed | 1 |
| Unit changed | 1 |
| Process class changed | 1 |
| Custody changed | 1 |
| Ownership changed | 1 |
| Measurable output | 1 |

**Raw boundary score: 6 → CONFIRMED. Phase 1.**

---

### Event Record — Event 3 of 6

**Event name / short description:** Primary filtration — screens, sedimentation, coarse sand filters

**Sources consulted for this event:** Water treatment plant engineering manuals; DWI inspection records; water utility environmental permits

---

**B1.** Raw water — abstracted, in raw water main. Untreated; contains suspended solids, biological material, dissolved organics.

**B2.** Pre-treated raw water — same water, with coarse particles removed by screens and sedimentation. Still not potable; still classified as "raw water" under drinking water regulations. The water has not yet been chemically treated or certified as safe.

**B3. Same physical form?**
- [x] Yes — still classified as raw untreated water; the filtration removes gross solids but does not change the fundamental state of the material (still non-potable)

**B4. Unit change?**
- [x] No — same unit (m³ raw water flow); turbidity decreases but the measurement unit does not change

**B5. Process class:**
- [x] **Chemical / Thermal** — physical and mechanical filtration (screens, sedimentation tanks, gravity sand filters); classified as Chemical/Thermal as the closest available category for a physical separation process

**B6. Process class change?**
> Prior: Extractive (Event 2)
- [x] Yes — Extractive → Chemical/Thermal *(+1)*

**B7.** Water utility (raw water main / intake works)
**B8.** Water utility (treatment works — same entity, same location)

**B9. Same entity?**
- [x] Yes — same water utility operates the entire treatment process

**B10. Ownership change?**
- [x] No — same owner throughout

**B11. Measurable output?**
- [x] No — pre-filtered water is an internal intermediate. Flow is metered within the treatment works but the specific output of the sedimentation/filtration stage is not independently reported or publicly verifiable. It is a continuous internal process step.

**B12. Reason output cannot be measured:**
- [x] **(c) Physical inaccessibility** — the pre-treatment stage is a continuous, closed process within the treatment works. There is no structural point at which a third party can independently sample or verify the volume and condition of water between sedimentation and chlorination.

### Event 3 — Boundary Score

| Criterion | Score |
|-----------|-------|
| Physical state changed | 0 |
| Unit changed | 0 |
| Process class changed | 1 |
| Custody changed | 0 |
| Ownership changed | 0 |
| Measurable output | 0 |

**Raw boundary score: 1 → Sub-process. Belongs inside Phase 2 (water treatment).**

> *This is the clearest example of a sub-process in this chain. The filtration step changes the process class but produces no distinct measurable output and does not alter the legal or physical status of the water. It is a preparatory step before the chemical treatment that defines Phase 2.*

---

### Event Record — Event 4 of 6

**Event name / short description:** Chemical treatment — chlorination, pH correction, fluoridation

**Sources consulted for this event:** DWI Annual Report on Drinking Water Quality; water company compliance reports; UK Water Supply (Water Quality) Regulations 2016; WHO Guidelines for Drinking-water Quality

---

**B1.** Pre-treated raw water — filtered, clarified, but not yet potable. Does not meet drinking water standards. Cannot lawfully be supplied to consumers.

**B2.** Treated potable water — water that has been chemically dosed to achieve residual disinfection (chlorine ≥0.1 mg/L), pH correction (6.5–9.5), and fluoridation where required. Water now meets the legal drinking water standard and can lawfully be supplied to consumers. A qualitatively different product has been produced.

**B3. Same physical form?**
- [ ] Yes
- [x] No — the water changes status from non-potable (legally prohibited from supply) to potable (legally permitted for supply). This is a genuine state change: the same molecules, but now a different legal and physical product. *(+1)*

**B4. Unit change?**
> Unit in: m³ raw water
> Unit out: m³ potable water meeting Drinking Water Standard (DWS) — the standard adds a specification dimension to the volume unit

- [x] Yes — unit shifts from simple volume to specified volume (volume × quality standard) *(+1)*

**B5. Process class:**
- [x] **Chemical / Thermal** — chlorine dosing, pH adjustment chemicals (lime, CO₂), fluoride dosing; chemical transformation of the water's biological safety profile

**B6. Process class change?**
> Prior: Chemical/Thermal (Event 3)
- [x] No — same class; filtration (Event 3) and chemical treatment (Event 4) are both Chemical/Thermal

**B7.** Water utility (treatment works; pre-treatment zone)
**B8.** Water utility (treatment works; treated water contact tank / service reservoir inlet)

**B9. Same entity?**
- [x] Yes — same water utility

**B10. Ownership change?**
- [x] No — same owner

**B11. Measurable output?**
- [x] Yes *(+1)*
> Quantity: m³/day treated potable water at stated residual chlorine, pH, turbidity
> Volume: e.g. 48 ML/day treated water (treatment losses ~4%)
> Recipient: Water utility (self-held; service reservoir)

> *Note: DWI requires water companies to monitor and report treated water quality at the treatment works outlet. This is a legally mandated, independently audited measurement point — one of only two in the entire chain.*

### Event 4 — Boundary Score

| Criterion | Score |
|-----------|-------|
| Physical state changed | 1 |
| Unit changed | 1 |
| Process class changed | 0 |
| Custody changed | 0 |
| Ownership changed | 0 |
| Measurable output | 1 |

**Raw boundary score: 3 → Candidate. B11 = Yes → CONFIRMED. Phase 2.**

---

### Event Record — Event 5 of 6

**Event name / short description:** Transfer to service reservoir and pressurised storage

**Sources consulted for this event:** Water utility asset registers (partial public); Ofwat service reservoir monitoring requirements; DWI reservoir inspection guidelines

---

**B1.** Treated potable water at treatment works outlet — meeting drinking water standard; ready for distribution.

**B2.** Treated potable water held in a service reservoir — same water, now physically stored in an elevated or underground covered reservoir that maintains hydraulic pressure in the distribution network. The water is now a pressurised, instantly-available supply rather than a flowing process stream.

**B3. Same physical form?**
- [x] Yes — same potable water; physical form unchanged by storage

**B4. Unit change?**
- [x] No — same unit (m³ potable water)

**B5. Process class:**
- [x] **Custodial** — storage in service reservoir; no material transformation; function is pressure management and supply buffer

**B6. Process class change?**
> Prior: Chemical/Thermal (Event 4)
- [x] Yes — Chemical/Thermal → Custodial *(+1)*

**B7.** Water utility (treatment works outlet)
**B8.** Water utility / distribution network operator (service reservoir — may be same or different operational division)

**B9. Same entity?**
- [x] Yes — typically same water utility manages both treatment and distribution

**B10. Ownership change?**
- [x] No — same owner

**B11. Measurable output?**
- [x] Yes *(+1)*
> Quantity: m³ potable water in service reservoir (volume at stated date/time); measured by level sensor
> Volume: e.g. 12 ML storage capacity; inflow/outflow metered daily
> Recipient: Distribution network (self-held by water utility; immediately downstream)

### Event 5 — Boundary Score

| Criterion | Score |
|-----------|-------|
| Physical state changed | 0 |
| Unit changed | 0 |
| Process class changed | 1 |
| Custody changed | 0 |
| Ownership changed | 0 |
| Measurable output | 1 |

**Raw boundary score: 2 → Candidate. B11 = Yes → CONFIRMED. Phase 3.**

> *This is the minimum-score confirmed boundary in this chain: score 2 with B11=Yes. It is confirmed because the process class changes categorically (from chemical treatment to pure custody/storage) and a measurable output exists. The service reservoir is a structurally distinct phase: it is the buffer and pressure-management node that separates production from distribution.*

---

### Event Record — Event 6 of 6

**Event name / short description:** Distribution through pipe network and delivery to consumer tap

**Sources consulted for this event:** Water company billing systems; Ofwat metering guidelines; DWI zonal compliance monitoring; water company consumer meter reading data

---

**B1.** Potable water held in service reservoir under hydraulic pressure — stored, ready-to-distribute supply.

**B2.** Potable water delivered at consumer tap — same water, now physically received at the consumer's premises via the pressurised distribution network. The consumer opens the tap and receives a metered quantity of water that is billed to their account.

**B3. Same physical form?**
- [x] Yes — same treated potable water; physical and chemical form unchanged by distribution

**B4. Unit change?**
> Unit in: m³ in service reservoir (bulk supply)
> Unit out: m³ metered to individual consumer (individual consumption units)

- [x] Yes — shift from bulk reservoir volume to individually metered consumer consumption *(+1)*

**B5. Process class:**
- [x] **Commercial** — metered delivery to consumer; billing event; legal transfer of the water as a commercial product; consumer becomes the owner on receipt

**B6. Process class change?**
> Prior: Custodial (Event 5)
- [x] Yes — Custodial → Commercial *(+1)*

**B7.** Water utility / distribution network operator (service reservoir)
**B8.** Consumer (water received at premises; metered and billed)

**B9. Same entity?**
- [ ] Yes
- [x] No — water passes from the water utility's network into the consumer's plumbing; physical custody transfers to the consumer *(+1)*

**B10. Ownership change?**
- [x] Yes — upon metered delivery, the consumer takes legal ownership of the water (it is purchased through the utility billing system) *(+1)*

**B11. Measurable output?**
- [x] Yes *(+1)*
> Quantity: m³ metered to consumer premises
> Volume: Individual meter readings; aggregate zonal consumption (e.g. 45 ML/day delivered across distribution zone)
> Recipient: Named consumer at metered address; billing account holder

### Event 6 — Boundary Score

| Criterion | Score |
|-----------|-------|
| Physical state changed | 0 |
| Unit changed | 1 |
| Process class changed | 1 |
| Custody changed | 1 |
| Ownership changed | 1 |
| Measurable output | 1 |

**Raw boundary score: 5 → CONFIRMED. Phase 4.**

---

---

# MODULE 3 — Boundary Scoring and Phase Map

---

### Step 3.1 — Master Event Score Table

| Event # | Event name | Score (0–6) | B11 output defined? | Interpretation |
|---------|------------|-------------|---------------------|----------------|
| 1 | Source identification and abstraction licence | 5 | [x] Yes | Confirmed boundary |
| 2 | Water abstraction | 6 | [x] Yes | Confirmed boundary |
| 3 | Primary filtration (sedimentation, screens) | 1 | [ ] No | Sub-process |
| 4 | Chemical treatment (chlorination, pH, fluoride) | 3 | [x] Yes | Confirmed boundary (score 3, B11=Yes) |
| 5 | Transfer to service reservoir | 2 | [x] Yes | Confirmed boundary (score 2, B11=Yes) |
| 6 | Distribution and delivery to consumer | 5 | [x] Yes | Confirmed boundary |

---

### Step 3.2 — Apply Interpretation Rules

**Rule 1:** Score 0–1 = Sub-process regardless of B11.
*Applied to: Event 3 (score 1).*

**Rule 2:** Score 2–3 = Candidate. B11=Yes → confirm. B11=No → sub-process.
*Applied to: Event 4 (score 3, B11=Yes → confirmed); Event 5 (score 2, B11=Yes → confirmed).*

**Rule 3:** Score 4–6 = Confirmed boundary regardless of B11.
*Applied to: Events 1, 2, 6.*

**Analyst note on Event 3:** Primary filtration scores 1 because it produces no independently measurable output and does not change the legal status, custody, or ownership of the water. It is correctly identified as a sub-process — a preparatory step within Phase 2 (water treatment). This is the instrument working as intended: a process step that changes the process class but produces no distinct child-N output is not a phase boundary.

**Analyst note on Event 5 (score 2, minimum confirmed boundary):** The service reservoir event is the lowest-scoring confirmed boundary in this chain. It passes because the process class changes (Chemical/Thermal → Custodial) and a measurable output exists. This reflects a real structural reality: the service reservoir is a distinct functional node in the water supply system — it is not merely a pipe segment. Its function (pressure buffering and demand management) is categorically different from both treatment and distribution.

---

### Step 3.3 — Confirmed Phase Map

| Phase # | Phase name | Begins at (event #) | Ends at / transitions to (event #) | Child N output (from B11) |
|---------|------------|--------------------|------------------------------------|--------------------------|
| 0 | Source identification and licensing | Event 1 | → Event 2 | Licensed abstraction: ML/day from [named source], assigned to [water utility] |
| 1 | Raw water abstraction | Event 2 | → Event 4 (via sub-process Event 3) | Raw water intake: ML/day at intake meter |
| 2 | Water treatment | Event 4 | → Event 5 | Potable water: ML/day meeting Drinking Water Standard at treatment works outlet |
| 3 | Service reservoir and pressurised storage | Event 5 | → Event 6 | Stored potable water: ML in reservoir; inflow/outflow metered daily |
| 4 | Distribution and consumer delivery | Event 6 | → end of chain | Delivered water: m³ metered to consumer at billing address |

---

### Step 3.4 — Sub-process Register

| Event # | Event name | Belongs to Phase # | Reason for sub-process classification |
|---------|------------|--------------------|-----------------------------------------|
| 3 | Primary filtration (sedimentation, screens) | 2 (Water treatment) | Score 1; no physical state change, no measurable output, no custody or ownership change; internal preparatory step within the treatment works |

---

---

# MODULE 4 — Opacity Tagging

---

### Opacity Record — Phase 0: Source Identification and Licensing

**C1. Can the volume throughput be measured from public sources?**
- [x] Yes — Environment Agency abstraction licence register is public; licensed volumes are published per licence holder.

**C2. Can the identity of custodians be publicly established?**
- [x] Yes — Abstraction licences name the licence holder; water utilities are publicly registered companies.

**C3. Can the transformation process be physically verified by an outside party?**
- [x] Yes — the abstraction licence is a public legal document; the source water body is geographically accessible and measurable by an independent hydrologist.

**C4. Can the child-N output be independently confirmed?**
- [x] Yes — Environment Agency publishes abstraction licence data including permitted volumes; river flow gauges provide independent source-flow data.

**Opacity score: 4 → High**

> *The licensing phase is entirely transparent because it is a regulated legal process with mandatory public disclosure. No material exists yet — only legal instruments, all of which are in the public record.*

---

### Opacity Record — Phase 1: Raw Water Abstraction

**C1. Can the volume throughput be measured from public sources?**
- [x] Yes — water companies publish total abstraction volumes in their Annual Reports and Water Resource Management Plans; Ofwat publishes per-company data.

**C2. Can the identity of custodians be publicly established?**
- [x] Yes — water utility operating in each area is a matter of public record; regulated monopoly suppliers are publicly identified.

**C3. Can the transformation process be physically verified by an outside party?**
- [ ] Yes
- [x] No — intake infrastructure is within the water utility's secure operational site. Daily intake metering is the utility's own instrument. Independent verification of real-time abstraction rate is not possible without regulatory access.

**C4. Can the child-N output be independently confirmed?**
- [ ] Yes
- [x] No — raw water intake flow is self-reported by the utility. The Environment Agency monitors river flows and can cross-check against licensed volumes over time, but real-time independent verification of what enters the treatment works is not available.

**Opacity score: 2 → Medium**

---

### Opacity Record — Phase 2: Water Treatment

**C1. Can the volume throughput be measured from public sources?**
- [x] Yes — water companies report treated water output in compliance reports; DWI publishes treatment works compliance data annually.

**C2. Can the identity of custodians be publicly established?**
- [x] Yes — water utility operates all treatment works; sites are publicly registered.

**C3. Can the transformation process be physically verified by an outside party?**
- [x] Yes — DWI inspectors have statutory right of access to all treatment works; DWI publishes treatment works compliance reports annually; the chemical dosing process is externally audited. This is one of the most closely regulated industrial processes in the country.

**C4. Can the child-N output be independently confirmed?**
- [x] Yes — treated water quality at the treatment works outlet is a legally mandated monitoring point; results are published in DWI annual reports; independent sampling is conducted by DWI inspectors.

**Opacity score: 4 → High**

> *Water treatment is highly transparent because of statutory regulatory oversight. The DWI's sole function is to independently verify that this phase produces water meeting the legal standard. Phase 2 has the most external oversight of any phase in this chain.*

---

### Opacity Record — Phase 3: Service Reservoir and Pressurised Storage

**C1. Can the volume throughput be measured from public sources?**
- [x] Yes — Ofwat requires water companies to report reservoir storage levels and daily distribution input; published in regulatory returns.

**C2. Can the identity of custodians be publicly established?**
- [x] Yes — service reservoirs are listed assets of regulated water companies; asset locations are publicly registered.

**C3. Can the transformation process be physically verified by an outside party?**
- [ ] Yes
- [x] No — reservoir interiors are closed, covered structures for public health reasons. DWI can inspect but public third-party access is not possible. Water quality in the reservoir can deteriorate (chlorine decay, biofilm formation) without immediate external detection.

**C4. Can the child-N output be independently confirmed?**
- [ ] Yes
- [x] No — the flow from service reservoir into the distribution network is metered by the utility but not independently verified at the individual reservoir outlet level. DWI monitors distribution zone compliance at consumer taps, not at reservoir outlets.

**Opacity score: 2 → Medium**

---

### Opacity Record — Phase 4: Distribution and Consumer Delivery

**C1. Can the volume throughput be measured from public sources?**
- [x] Yes — Ofwat publishes per-company leakage data, metered consumption, and total distribution input; water companies publish annual reports with zone-level consumption data.

**C2. Can the identity of custodians be publicly established?**
- [x] Yes — regulated water utility distributes in each area; consumer is the recipient at their metered address.

**C3. Can the transformation process be physically verified by an outside party?**
- [ ] Yes
- [x] No — the distribution pipe network is underground infrastructure spanning thousands of kilometres. Water quality can change between the reservoir and the tap (chlorine decay, pipe condition, re-contamination events). DWI samples at consumer taps (the end of the phase) but cannot monitor the distribution process in real time.

**C4. Can the child-N output be independently confirmed?**
- [x] Yes — consumer meters are independently verified through Ofwat billing dispute processes; DWI conducts regulatory sampling at consumer taps (the output point of this phase) and publishes compliance rates annually.

**Opacity score: 2 → Medium**

> *Note: While the output is verifiable (tap water quality is independently tested), the process (pipe network) is not observable. Distribution is the longest and most physically dispersed phase, and the one most vulnerable to quality degradation between measurement points.*

---

---

# SUMMARY — Completed Phase Map

**Material:** Drinking water (municipal tap water supply)

**Date completed:** April 2026

**Analysts:** True Value Analytics — worked example

| Phase # | Phase name | Physical state (in → out) | Child N output | Custodian class | Transparency |
|---------|------------|--------------------------|---------------|-----------------|--------------|
| 0 | Source identification and licensing | Unallocated natural water → licensed abstraction right (water remains in source) | Licensed volume: ML/day assigned to named water utility | Regulator (Environment Agency) → Water utility (licence holder) | High |
| 1 | Raw water abstraction | Natural source water → abstracted raw water in intake infrastructure | Raw water intake: ML/day at intake meter | Water utility | Medium |
| 2 | Water treatment | Raw water → treated potable water meeting Drinking Water Standard | Potable water: ML/day at treatment works outlet (DWI-audited measurement point) | Water utility | High |
| 3 | Service reservoir and pressurised storage | Potable water (flowing) → potable water held at pressure in service reservoir | Stored supply: ML in reservoir; daily inflow/outflow metered | Water utility / distribution operator | Medium |
| 4 | Distribution and consumer delivery | Pressurised water in reservoir → metered water delivered at consumer tap | Delivered water: m³ metered to consumer; billed; DWI tap-sample compliance published | Water utility → Consumer | Medium |

---

**Total confirmed phases:** 5 (Phases 0–4)

**High transparency phases:** 2 (Phase numbers: 0, 2)

**Medium transparency phases:** 3 (Phase numbers: 1, 3, 4)

**Low transparency phases:** 0

**Sub-processes identified and assigned:** 1 (Event 3 — primary filtration, assigned to Phase 2)

**Events where B11 output could not be defined:** 1 (Event 3 — sub-process; B11=No was the deciding factor that prevented it from becoming a phase boundary despite a score of 1)

---

### Analyst Notes

**Why this chain has no Low transparency phases:** Drinking water is one of the most heavily regulated commodities in any jurisdiction. Statutory monitoring, mandatory public reporting, and independent regulatory inspection (DWI) create a transparency floor that does not exist in most commodity supply chains. Compare with the gold chain, which has two Low transparency phases (Phase 2 ore processing, Phase 6 vault custody) precisely because no equivalent regulatory monitoring exists at those points.

**The most instructive event in this chain is Event 3 (sub-process):** It scores 1 — the minimum possible score — and has no measurable output. It demonstrates the rule clearly: a process step that changes something about how the material is handled, but produces no distinct, independently verifiable output, is not a phase boundary. It belongs inside an existing phase. The water going through a sedimentation tank is not a new phase — it is a preparation step for the chemical treatment that actually defines Phase 2.

**Comparison with the gold chain:** The drinking water chain has 6 events (vs. 12 in gold), 5 phases (vs. 9), 1 sub-process (vs. 3), and 0 Low transparency phases (vs. 2). The instrument produces shorter, cleaner output for simpler chains. The module structure, scoring rules, and interpretation logic are identical — only the answers differ.

**What this chain demonstrates about the instrument:** The Phase Discovery Instrument does not need to know in advance how many phases a chain has. It discovered 5 phases from 6 events by applying the same scoring rules used to discover 9 phases from 12 events in the gold chain. The phases emerged from the answers; they were not assumed.

---

---

*Phase Discovery Instrument v1.0 — Drinking Water Worked Example*
*Aligned with: Abstract Supply Chain Phase Template | N-D-C Tholonic Framework*
*Cross-reference: PDI_MATERIAL_AGNOSTIC_PHASE_MAPPING_PROTOCOL.md | PDI_WORKED_EXAMPLE_GOLD_SUPPLY_CHAIN.md*
