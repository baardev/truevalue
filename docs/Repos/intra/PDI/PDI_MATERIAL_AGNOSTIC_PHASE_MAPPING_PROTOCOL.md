# Phase Discovery Instrument (PDI)
### A Material-Agnostic Supply Chain Phase Mapping Protocol

**Version 1.0**
**Project: True Value Analytics — Supply Chain Intelligence**

---

## Purpose

This instrument is used to determine the phase structure of any material supply chain from first principles. It does not assume any prior knowledge of the industry or commodity. The phases are not inputs to this process — they are **outputs** of it.

You bring:
- Knowledge of what the material is
- Willingness to trace its journey from origin to market, step by step

The instrument produces:
- A numbered, confirmed phase map
- A transparency rating for each phase
- A documented basis for every phase boundary decision

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

**Material being analyzed:** _______________________________________________

**Analyst name(s):** _____________________________________________________

**Date completed:** ______________________________________________________

**Sources consulted for this module:** _______________________________________

---

**A1. What is the material in its pre-commercial state — before any human intervention?**

Describe the physical form, location, and condition of the material as it exists in nature or at its origin point, before any extraction, harvest, or collection has occurred.

> *Answer:*

---

**A2. What is the material at the point of final market delivery — what does the end buyer or end market actually receive?**

Describe the physical form, specification, and condition of the material as it is transferred to the final purchaser or registered for market use.

> *Answer:*

---

**A3. What unit of measurement applies at the origin state (A1)?**

Examples: tonnes of ore, hectares of crop area, cubic metres, number of animals, kilograms of raw material.

> *Unit:*

---

**A4. What unit of measurement applies at the final market state (A2)?**

Examples: troy ounces of refined metal, kilograms of certified butter, litres of processed oil, standardised units.

> *Unit:*

---

**A5. Are the units in A3 and A4 the same?**

- [ ] Yes — the unit does not change across the chain
- [ ] No — the unit changes at least once

> *If No: note that at least one unit-change event exists somewhere in the chain. This is a strong signal of a phase boundary. Record where you believe it occurs — you will confirm it in Module 2.*
>
> *Preliminary note on unit change location:*

---

**A6. List every distinct physical form the material passes through, between origin (A1) and market (A2).**

Work from memory, documentation, or industry knowledge. Do not worry about completeness — this list will be refined in Module 2. Number each form.

| # | Physical form | Approximate location in chain |
|---|---------------|-------------------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |

> *Add rows as needed.*

---

**A7. List every distinct actor class that holds or handles the material at any point in the chain.**

Examples: miner, farmer, collector, trader, processor, refiner, certifier, logistics company, exchange, end buyer.

| # | Actor class | Approximate point in chain |
|---|-------------|---------------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |

> *Add rows as needed.*

---

### Module 1 — Completion Check

Before proceeding to Module 2, confirm:

- [ ] A1 and A2 are filled in with specific physical descriptions (not general statements)
- [ ] A3 and A4 have explicit units of measurement
- [ ] A6 has at least three distinct physical forms listed
- [ ] A7 has at least three distinct actor classes listed

> *If any box is unchecked, return to the relevant question before proceeding.*

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

### Event Record

**Event number:** _______ of _______ total events identified

**Event name / short description:** ___________________________________________

**Sources consulted for this event:** ___________________________________________

---

**B1. What is the physical form of the material entering this event?**

> *Answer:*

---

**B2. What is the physical form of the material leaving this event?**

> *Answer:*

---

**B3. Are B1 and B2 the same physical form?**

- [ ] Yes — physical state is unchanged across this event
- [ ] No — physical state changes across this event *(flag: +1 toward boundary score)*

---

**B4. Does the unit of measurement change across this event?**

> *Unit entering this event:*
>
> *Unit leaving this event:*

- [ ] Yes — unit changes *(flag: +1 toward boundary score)*
- [ ] No — same unit throughout

---

**B5. What class of process is applied during this event?**

Select one:

- [ ] **Extractive** — material is separated from its origin (mining, harvesting, collection)
- [ ] **Aggregative** — material is gathered, sorted, bulked, or first-traded without chemical change
- [ ] **Chemical / Thermal** — material undergoes chemical or thermal transformation (smelting, pressing, cracking, refining)
- [ ] **Specification** — material is brought to a defined standard or grade without changing its fundamental form
- [ ] **Certification** — material is tested, assayed, audited, or formally approved against a standard
- [ ] **Custodial** — material is stored or transported; no change in form, specification, or ownership
- [ ] **Commercial** — material is sold, registered, or delivered; change in legal status or market access

> *Notes on classification if ambiguous:*

---

**B6. Does the process class selected in B5 differ from the process class of the immediately preceding event?**

> *Process class of preceding event:*

- [ ] Yes — process class changes *(flag: +1 toward boundary score)*
- [ ] No — same process class continues

---

**B7. Who physically holds the material immediately before this event begins?**

Name the actor class, and the specific organisation or individual if known.

> *Actor class:*
>
> *Specific name (if known):*

---

**B8. Who physically holds the material immediately after this event ends?**

> *Actor class:*
>
> *Specific name (if known):*

---

**B9. Are B7 and B8 the same entity?**

- [ ] Yes — physical custody is unchanged
- [ ] No — physical custody transfers *(flag: +1 toward boundary score)*

---

**B10. Does legal ownership of the material change across this event?**

- [ ] Yes — ownership transfers *(flag: +1 toward boundary score)*
- [ ] No — same owner before and after
- [ ] Unknown / unverifiable — note reason:

---

**B11. Can you name a specific, measurable quantity that leaves this event — with a unit, a volume, and a named recipient?**

This is the output test. The output must be definable, not estimated. "Approximately X tonnes" is acceptable. "It varies informally" is not.

- [ ] **Yes** *(flag: +1 toward boundary score)* — complete the fields below:

> *Quantity and unit:*
>
> *Approximate volume (per year, per season, or per cycle):*
>
> *Named recipient (actor class or specific entity):*

- [ ] **No** — the output cannot be defined. Proceed to B12.

---

**B12. If B11 is No: what is the reason the output cannot be measured?**

Select one:

- [ ] **(a) Informal practice** — transactions occur but are not recorded in any accessible form
- [ ] **(b) Commercial secrecy** — data exists but is withheld by actors for competitive or legal reasons
- [ ] **(c) Physical inaccessibility** — the material or transaction is structurally unobservable (e.g. sub-surface, off-market, cross-border informal)

> *This classification is used in Module 4. Record it here for later use.*

---

### Event Record — Boundary Score Calculation

Transfer your flags from B3–B11 to the scoring table:

| Criterion | Flag | Score |
|-----------|------|-------|
| Physical state changed (B3 = No) | [ ] Yes / [ ] No | |
| Unit of measurement changed (B4 = Yes) | [ ] Yes / [ ] No | |
| Process class changed (B6 = Yes) | [ ] Yes / [ ] No | |
| Physical custody changed (B9 = No) | [ ] Yes / [ ] No | |
| Legal ownership changed (B10 = Yes) | [ ] Yes / [ ] No | |
| Measurable output exists (B11 = Yes) | [ ] Yes / [ ] No | |

**Raw boundary score (0–6):** _______

> *Do not interpret this score yet. Interpretation occurs in Module 3, where all event scores are reviewed together.*

---

> **Repeat this module for every event before proceeding to Module 3.**

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

Transfer all events and their boundary scores here, in the order they occur in the chain:

| Event # | Event name | Score (0–6) | B11 output defined? | Preliminary interpretation |
|---------|------------|-------------|---------------------|---------------------------|
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |
| | | | [ ] Yes / [ ] No | |

> *Add rows as needed.*

---

### Step 3.2 — Apply Interpretation Rules

For each event, assign one of three interpretations using the following rules:

**Rule 1 — Sub-process:**
Score 0–1, regardless of output status → this event belongs *inside* an existing phase, not at a boundary between phases. Record which phase it belongs to.

**Rule 2 — Candidate boundary:**
Score 2–3 → review the B11 output field.
- If B11 = Yes (output is measurable): **confirm as phase boundary.**
- If B11 = No (output not measurable): **classify as sub-process.** A boundary without a definable output is structurally incomplete; the phase has not yet resolved into a stable N-state.

**Rule 3 — Confirmed boundary:**
Score 4–6 → phase boundary confirmed regardless of B11, but B11 must be noted. If B11 = No at score 4+, the boundary is real but the transition point is opaque — record this explicitly.

---

### Step 3.3 — Confirmed Phase Map

List only the confirmed phase boundaries below, in sequence. Number them starting from Phase 0 (origin/pre-commercial state) through the final phase.

| Phase # | Phase name | Begins at (event #) | Ends at / transitions to (event #) | Child N output (from B11) |
|---------|------------|--------------------|------------------------------------|--------------------------|
| 0 | | — | | |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |

> *Most supply chains resolve to 6–9 phases. Fewer than 5 suggests events have been grouped prematurely. More than 10 suggests sub-processes have been elevated to phase status.*

---

### Step 3.4 — Sub-process Register

For events scored as sub-processes, record which phase they belong to:

| Event # | Event name | Belongs to Phase # | Reason for sub-process classification |
|---------|------------|--------------------|-----------------------------------------|
| | | | |
| | | | |
| | | | |

---

---

# MODULE 4 — Opacity Tagging

> **When to use:** After the Phase Map (Module 3, Step 3.3) is confirmed.
>
> **What it does:** Assigns a transparency classification to each confirmed phase based on four measurability tests. This is not a qualitative judgment about the industry's trustworthiness — it is a structural assessment of whether each phase produces information that can be independently verified.
>
> **How to complete it:** For each confirmed phase, answer the four questions below. Record the score and assign the classification. If data is genuinely unavailable to answer a question, answer No and note the reason — that itself is an opacity finding.

---

For each confirmed phase, complete one Opacity Record:

---

### Opacity Record

**Phase number:** _______ **Phase name:** _______________________________________

---

**C1. Can the volume throughput of this phase be measured from public sources?**

Is there a publicly accessible data source (government statistics, exchange reports, industry association data, academic research) that gives an approximate quantity of material passing through this phase per year?

- [ ] Yes — source: ___________________________________________________________
- [ ] No — reason: ____________________________________________________________

---

**C2. Can the identity of custodians in this phase be publicly established?**

Can you name, or access a public list of, the specific organisations or actor classes that physically hold the material during this phase?

- [ ] Yes — source: ___________________________________________________________
- [ ] No — reason: ____________________________________________________________

---

**C3. Can the transformation process in this phase be physically verified by an outside party?**

Could an independent analyst, auditor, or regulator observe or confirm that the stated transformation is actually occurring and producing the stated output?

- [ ] Yes — mechanism: _______________________________________________________
- [ ] No — reason: ____________________________________________________________

---

**C4. Can the child-N output of this phase — the handoff to the next phase — be independently confirmed?**

Is there a way to verify, from outside this phase, that the output stated in Step 3.3 is the actual quantity and form being transferred to the next phase?

- [ ] Yes — mechanism: _______________________________________________________
- [ ] No — reason: ____________________________________________________________

---

### Opacity Score and Classification

Count the Yes answers for this phase:

| Yes count | Transparency classification | Meaning |
|-----------|----------------------------|---------|
| 4 | **High** | All four measurability tests pass. Phase is fully traceable. |
| 2–3 | **Medium** | Partial traceability. Some structural gaps exist. |
| 0–1 | **Low** | Phase is structurally opaque. The child-N transition cannot be independently traced. |

**Opacity score (Yes count):** _______

**Transparency classification:** [ ] High [ ] Medium [ ] Low

**Primary reason for opacity (if Medium or Low) — select from B12 categories recorded in Module 2:**
- [ ] Informal practice
- [ ] Commercial secrecy
- [ ] Physical inaccessibility
- [ ] Multiple factors — describe: _______________________________________________

---

> **Repeat this Opacity Record for every confirmed phase before completing the Summary.**

---

---

# SUMMARY — Completed Phase Map

> Complete this table after all four modules are finished. This is the deliverable.

**Material:** ___________________________________

**Date completed:** _____________________________

**Analysts:** ___________________________________

| Phase # | Phase name | Physical state (in → out) | Child N output | Custodian class | Transparency |
|---------|------------|--------------------------|---------------|-----------------|--------------|
| 0 | | | | | |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |

---

**Total confirmed phases:** _______

**High transparency phases:** _______ (Phase numbers: _______)

**Medium transparency phases:** _______ (Phase numbers: _______)

**Low transparency phases:** _______ (Phase numbers: _______)

**Sub-processes identified and assigned:** _______

**Events where B11 output could not be defined:** _______ (Opacity flags for further investigation)

---

### Analyst Notes

> Use this space to record any anomalies, contradictions between sources, events that could not be confidently classified, or areas requiring further research.

---

---

*Phase Discovery Instrument v1.0 — True Value Analytics*
*Aligned with: Abstract Supply Chain Phase Template | N-D-C Tholonic Framework*
