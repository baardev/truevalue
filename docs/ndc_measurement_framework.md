# NDC Measurement Framework: Primitives, Scales, and Open Problems

## Overview

This document explains what the Tholonic N-D-C model is measuring, how measurements are derived, where the implementation is sound, and where further work is needed. It covers the original flag-count model, the threshold-ratio normalized implementation (gold_v2), and the complex number extension (gold_v3). It is intended as a reference for analysts and developers working with this project.

---

## 1. The Tholonic N-D-C Framework

The Tholonic model describes any coherent system as a triadic structure of three interacting components:

- **N (Negotiation):** The emergent operational state of the system. N is not measured directly. It arises from the balance between D and C. It is simultaneously the product of D and C at one level and the source that differentiates into D and C at the next level down.

- **D (Definition):** The constraints, boundaries, requirements, and specifications that define what a phase IS. Internally focused. Governs structure, identity, and operating envelope.

- **C (Contribution):** The outputs, flows, connections, and integrations that define what a phase DOES. Externally focused. Governs production, relationships, and downstream effects.

The system is most stable and efficient when D and C are in balance (D ≈ C). Imbalance in either direction increases energy cost and degrades the N state. The phi-derived thresholds mark the boundaries between structural health zones.

The framework has a mathematical grounding: when the first three prime numbers (2, 3, 5) are assigned to N, D, and C respectively, and the recursive triadic structure is iterated, the fundamental mathematical constants (phi, pi, sqrt(2), e) emerge as natural consequences. This is not coincidental. It means the N-D-C structure has mathematical validity independent of its descriptive utility.

---

## 2. Tholonic Primitives

### Definition

A **tholonic primitive** is a value that is fixed from the perspective of the phase being modeled and therefore serves as a non-negotiable input to either D or C. It cannot be changed by operations within the phase. It defines the phase's operating context.

### Three types of tholonic primitives

**Physically irreducible:** Fixed by the material world. The ore grade of a mineral deposit is what the geology made it. No operational decision inside the mining phase changes it. Example: `ore_grade_actual` in Phase 1 (Mine Extraction).

**Scope-relative (exogenous):** Fixed from the phase's perspective because the setting agent is outside the phase's scope of control. Safety regulations are set by governments, not mine operators. Exchange registration standards are set by COMEX, not refiners. These are reducible in principle (a legislature could change a law) but irreducible from within the phase. Example: `safety_standards`, `environmental_regulations`, `exchange_standards`.

**Crystallized structural choices:** Originally a decision made by the phase operator, but now a fixed structural fact that defines what the operation IS. Once a mine is built to a certain production capacity, that capacity defines the mine's identity for the duration of the phase, even though it was a choice at construction time. Example: `production_capacity`, `extraction_method_spec`.

### Why the term "tholonic primitives"

The term connects to the mathematical foundation of the framework. Prime numbers are primitives in number theory: they cannot be factored into simpler components. Tholonic primitives are analogous: they cannot be decomposed or changed from within the phase's scope. The label also distinguishes them from "parameters," which implies tunability, and from "variables," which implies freedom to change.

---

## 3. PDI (Phase Discovery Instrument) Boundary Flags: What They Are and How They Work

### What a flag is

A **flag** is a binary (true/false) question answered by an analyst about a single event in a supply chain. An event is any moment where the material being tracked changes in some observable way: its physical form, the unit it is measured in, who holds custody of it, who owns it, what kind of process is being applied to it, or whether its output is defined and measurable.

Flags are recorded in Module 2 of the PDI (Phase Discovery Instrument) YAML file, one block per event. They are the primary instrument by which an analyst encodes structural information about a phase boundary into a form the pipeline can compute with.

There are six scoring flags, each contributing +1 to the boundary score if true:

| Flag | Question answered | Contributes to |
|---|---|---|
| **B3** `physical_state_changes` | Does the material change physical state at this event? (e.g. ore to concentrate, wastewater to effluent) | D |
| **B4** `unit_changes` | Does the unit of measurement change? (e.g. kg/ha to tonnes/season, ML/day to m³ billed) | D |
| **B6** `process_class_changes` | Does the process class change from the preceding event? (extractive, chemical_thermal, specification, certification, custodial, commercial) | D |
| **B9** `custody_changes` | Does physical custody pass to a different actor? | C |
| **B10** `ownership_changes` | Does legal ownership change? (true / false / unknown) | C (indirectly via boundary_score) |
| **B11** `output_defined` | Is the output of this event measurable with a defined quantity and unit? | C |

B3, B4, and B6 are Definition flags: they describe changes to what the material IS and what kind of process is being applied to it. B9, B10, and B11 are Contribution flags: they describe changes to who controls the material and whether what it produces can be observed and handed forward.

There are also two non-scoring descriptive flags used for context:

- **B5** `process_class`: the process class label for this specific event (not a score; used to determine whether B6 is true by comparing to the preceding event's class).
- **B12** `opacity_reason`: if B11 is false (output is not defined), this records why: informal practice, commercial secrecy, or physical inaccessibility.

### How the boundary score is calculated

The boundary score for an event is the count of true flags across B3, B4, B6, B9, B10, and B11. Maximum is 6. It is calculated by the analyst and recorded in the YAML; it is not auto-computed.

```
boundary_score = B3 + B4 + B6 + B9 + B10 + B11    (each 1 if true, 0 if false)
```

### How the boundary score determines phase boundaries

Module 3 of the PDI uses the boundary score plus the B11 flag to decide whether an event marks a genuine phase boundary or is merely a sub-process within an existing phase:

| Score | B11 | Classification |
|---|---|---|
| 0-1 | either | Sub-process: belongs inside a phase, not a boundary |
| 2-3 | true | Confirmed boundary |
| 2-3 | false | Sub-process: no measurable output, so not a phase boundary |
| 4-6 | either | Confirmed boundary (analyst should note if B11 is false) |

This rule is intentional. A phase boundary requires that something genuinely changes AND that the result is observable. An event that scores high on structural change but produces no measurable output (B11 = false) is a transformation without a handoff point. The model cannot compute a C value for it and it does not qualify as a phase boundary.

### A real example: water treatment (Singapore NEWater)

At the event where secondary effluent enters the advanced purification plant:

```yaml
B3_physical_state_changes: true    # wastewater → purified water (physical change)
B4_unit_changes: true              # ML/day secondary effluent → ML/day WHO+ standard water (unit + quality spec)
B6_process_class_changes: false    # same process class as preceding step
B9_custody_changes: false          # PUB retains custody
B10_ownership_changes: false       # no ownership change
B11_output_defined: true           # ML/day NEWater at WHO+ standard — measurable
boundary_score: 3                  # B3 + B4 + B11 = 3
```

Score 3 with B11 = true: confirmed phase boundary. This event marks where Phase 8 (advanced treatment) begins.

### How flags feed into D and C

After phase boundaries are confirmed in Module 3, the pipeline aggregates the flags for the event that opens each phase:

```
d_flags       = B3 + B4 + B6     (the three Definition flags)
c_flags       = B9 + B11          (two of the three Contribution flags)
boundary_score = B3+B4+B6+B9+B10+B11   (all six flags)
opacity        = phase opacity score from Module 4 (0-4)

D = 200 + (d_flags × 20) + (boundary_score × 4)
C = 200 + (c_flags × 20) + (opacity × 8)
```

The Definition flags (B3, B4, B6) each contribute 20 points to D, and the Contribution flags (B9, B11) each contribute 20 points to C. Every true flag also adds 4 points to D via the boundary score. The net effect per flag is therefore: a true D-flag adds 24 points to D total (20 + 4); a true C-flag adds 20 points to C and 4 points to D. B10 is the only flag with no ×20 path: it does not appear in D_flags or C_flags, so when true it adds only 4 points to D via the boundary score. It affects whether the event qualifies as a phase boundary, but contributes almost no weight to D or C compared to the other flags. The opacity score raises C because an opaque phase is one where contributions are harder to trace, which the model represents as higher (more complex, less well-defined) contribution load.

### Step-by-step worked example: wheat farm to flour mill

This example walks through every calculation from a single supply chain event, using a deliberately simple case so the arithmetic is easy to follow.

**The event:** Harvested wheat grain is weighed, loaded onto a truck, and shipped from the farm to the flour mill.

---

**Step 1: Answer each flag question**

Read each question and answer true or false based on what physically and legally happens at this event.

| Flag | Question | Answer | Score |
|---|---|---|---|
| B3 `physical_state_changes` | Does the material change physical state? Wheat grain goes on a truck. It is still wheat grain. | false | 0 |
| B4 `unit_changes` | Does the unit of measurement change? On the farm, sacks were counted in kg. At the mill gate, the full load is weighed on a truck scale in tonnes. | true | 1 |
| B6 `process_class_changes` | Does the process class change from the preceding step? The previous step was agricultural (growing, harvesting). This step is custodial (transporting). | true | 1 |
| B9 `custody_changes` | Does physical custody pass to a different actor? The transport driver takes responsibility for the load while in transit. | true | 1 |
| B10 `ownership_changes` | Does legal ownership change? The farmer still owns the grain during transit; ownership transfers only when the mill weighs and accepts delivery. | false | 0 |
| B11 `output_defined` | Is the output measurable with a defined quantity and unit? Yes: the delivery note records X tonnes at Y% moisture content. | true | 1 |

---

**Step 2: Calculate the boundary score**

Add up all six flag values:

```
boundary_score = B3 + B4 + B6 + B9 + B10 + B11
               = 0 + 1 + 1 + 1 + 0 + 1
               = 4
```

---

**Step 3: Decide whether this event marks a phase boundary**

Using the classification table from earlier in this section:

- Score is 4 and B11 is true.
- Score 4-6 with any B11 value = confirmed boundary.

This event marks a genuine phase boundary. The pipeline will treat it as the opening event of a new phase.

---

**Step 4: Separate the flags into D-flags and C-flags**

The three Definition flags (B3, B4, B6) capture what changes about the material's identity and the process being applied to it. The two Contribution flags (B9, B11) capture what the phase produces and hands forward to the next phase.

```
D_flags = B3 + B4 + B6 = 0 + 1 + 1 = 2
C_flags = B9 + B11      = 1 + 1     = 2
```

---

**Step 5: Assign the opacity score**

The analyst assigns an opacity score of 1 (out of 4). Delivery documents exist, the mill issues a weight ticket, and the transaction follows standard commercial practice. This is a low-opacity phase: what happens is visible and recorded. If no documents existed and the weighing was informal, opacity would be 3 or 4.

---

**Step 6: Calculate D and C**

```
D = 200 + (D_flags × 20) + (boundary_score × 4)
  = 200 + (2 × 20)       + (4 × 4)
  = 200 + 40             + 16
  = 256

C = 200 + (C_flags × 20) + (opacity × 8)
  = 200 + (2 × 20)       + (1 × 8)
  = 200 + 40             + 8
  = 248
```

The 200 floor is a common base applied to every phase. It ensures D and C are always positive and in a comparable range, regardless of how many flags fire. It has no physical meaning on its own: it is a scaffolding number. The meaningful signal sits in the flag contributions (20 points each) and the boundary score contribution (4 points per flag), which sit on top of it.

D (256) is slightly larger than C (248). The transport phase has slightly more structural constraint than contribution capacity: two things changed about what the material IS (unit, process class) and two things changed about what it DOES (custody, output defined), but the constraints carry more weight in the formula. This is typical of a custodial handoff: the phase is imposing more structure than it is integrating.

---

**Step 7: Calculate the balance score**

The balance score measures how close D and C are to each other, expressed as a number from 0 to 100. A score of 100 means perfect balance (D = C exactly). A score of 0 means one side has completely collapsed.

```
balance = 100 × e^(−2 × |D − C| / max(D, C))
        = 100 × e^(−2 × |256 − 248| / 256)
        = 100 × e^(−2 × 8 / 256)
        = 100 × e^(−0.0625)
        = 100 × 0.939
        ≈ 93.9
```

The formula uses exponential decay: when D and C are equal, e^0 = 1 and balance = 100. As D and C diverge, the balance score falls toward zero. A result of 93.9 means D and C differ by less than 7%, which is a well-balanced phase.

---

**Step 8: Determine the health zone**

Apply the phi-derived zone thresholds:

| Zone | Threshold | This phase (93.9) |
|---|---|---|
| Coherent | balance >= 80 | yes |
| Stressed | balance >= 61.8 | — |
| Failure | balance >= 38.2 | — |
| Breakdown | balance < 38.2 | — |

This phase is in the Coherent zone. D and C are close to equilibrium. The transport handoff is functioning as it should.

---

**Step 9: Calculate N**

N is the operational output of the phase: the capacity available to the next phase, weighted by how well this phase is balanced.

```
N = round((D + C) / 2 × (balance / 100))
  = round((256 + 248) / 2 × (93.9 / 100))
  = round(252 × 0.939)
  = round(236.6)
  = 237
```

A perfectly balanced phase (balance = 100) with D = C = 252 would produce N = 252. This phase produces N = 237, slightly reduced from the maximum because D and C are not perfectly equal. The reduction (252 - 237 = 15 points) represents the operational cost of the imbalance.

---

**What changes if the phase is opaque?**

Suppose no delivery documents exist: informal weighing, no paper trail, the transaction is not recorded. The analyst assigns opacity = 4 (maximum).

C changes but D does not. The reason is rooted in what D and C each represent. D is about what the phase IS: its constraints, boundaries, and structural identity exist whether or not anyone documents them. A phase's regulatory requirements, process class, and operating specifications are real regardless of whether there is a paper trail. Opacity does not make a phase more constrained. C, by contrast, is about what the phase DOES and hands forward. Opacity directly impairs this: when a phase produces no documentation, its output cannot be cleanly verified or integrated by the next phase. The model represents that interpretive burden as an inflated C. The contribution exists physically, but it is murky and harder to build on. Raising C rather than D also has diagnostic meaning: when opacity is high, C ends up above D, which points toward documentation and governance interventions rather than physical or structural ones.

```
C = 200 + (2 × 20) + (4 × 8)
  = 200 + 40 + 32
  = 272
```

Now C = 272 and D = 256.

```
balance = 100 × e^(−2 × |256 − 272| / 272)
        = 100 × e^(−0.1176)
        = 100 × 0.889
        ≈ 88.9
```

The balance score falls from 93.9 to 88.9. The phase is still Coherent (above 80) but the margin above the Stressed threshold has narrowed. High opacity has pushed C above D: the contributions of the phase are harder to trace than its structural constraints. This is a different kind of imbalance from the low-opacity case, and it points toward a different category of intervention (documentation, governance, custody tracking) rather than a structural or physical one.

---

### What flags capture and what they do not

Flags capture **structural boundary characteristics**: whether and how the material, the process, and the custody arrangement change at a phase transition. They are a well-defined, reproducible analytical instrument.

What they do not capture is the **magnitude** of those changes. A phase where the physical state changes from low-grade ore to concentrate (massive chemical transformation, high energy input) scores B3 = true (1 point), exactly the same as a phase where state changes from tagged bar to bonded bar (minor administrative change). The flag is a binary presence/absence indicator, not a measurement of the significance or scale of the change.

This is the fundamental limitation that connects to the broader normalization problem discussed in Section 7: flags tell you that a change happened, not how large or consequential that change was.

---

### What binary flags are sufficient to conclude, and what they are not

Binary change-of-state flags are sufficient for **structural topology analysis** and insufficient for **magnitude analysis**. Understanding this distinction clarifies both what the model can claim and where it stops short.

**What flags are sufficient to conclude:**

- Where genuine phase boundaries lie versus internal sub-processes. A high boundary score is evidence that enough distinct categorical transformations occurred to constitute a qualitative transition. Two events with identical throughput volumes can have completely different topological meaning: one is a sub-process, the other is a handoff point.

- Whether a phase is constraint-led or contribution-led. The ratio of D-flags to C-flags encodes which side dominates structurally. A phase where three definition-type changes occur and zero contribution-type changes is structurally different from the reverse, regardless of how much material passes through it. The balance score is scale-invariant by design: if D and C are both multiplied by any constant, the balance score is unchanged. Volume does not enter this calculation.

- Which phases are structural bottlenecks, as a relative ranking within a project. The flag model and the physically-grounded normalized model (which uses actual industry benchmarks for ore grade, energy intensity, LBMA fineness, and so on) reach the same structural conclusions. Vaulting is the bottleneck in both. The coherent cluster of phases 1-5 and 7-8 appears in both. The flags did not accidentally identify these properties. They tracked real structural conditions that the normalized model later confirmed independently.

- What kind of intervention is needed. If D exceeds C (argument below 45 degrees in the complex plane), the phase is constraint-dominated and the intervention target is the D side: reduce custody fragmentation, simplify certification, reduce opacity. This diagnostic is structural and does not require volumetric data, just as an ECG does not require cardiac output in liters per minute to identify an abnormal signal pattern.

- Whether a phase is legible to the rest of the chain. B11 (output defined) and the opacity score capture whether a phase produces documentable output at all. A phase that processes large volume but produces no documentable output is opaque regardless of its scale. That is a structural fact with governance consequences independent of throughput.

**What flags cannot conclude:**

- How much material crosses each phase boundary.
- How large the constraints or contributions are in absolute terms.
- The absolute operational load per phase (available only from the modulus in the normalized complex representation).
- Why opacity exists at a physical level, only that it exists.
- How costly an intervention will be.

The framework is scoped to the former category by design. Operational throughput data requires proprietary reporting from companies running each phase, which is often inconsistent across the chain and subject to the exact opacity problem the model is measuring. Introducing unverifiable throughput estimates would undermine the auditability that is one of the framework's core requirements. Throughput is treated as a scalar multiplier to be added once reliable, auditable flow data is available for a given supply chain, not as a prerequisite for structural analysis.

---

## 4. How D and C Values Are Currently Determined

### The PDI pipeline formula

When a new project is created from a PDI (Phase Discovery Instrument) YAML file, D and C values are derived from structural binary flags attached to each phase boundary event:

```
D_flags       = B3 + B4 + B6   (physical state change, unit change, process class change)
C_flags       = B9 + B11        (custody change, output defined)
boundary_score = B3+B4+B6+B9+B10+B11   (all boundary flags summed)
opacity        = module_4_opacity score, range 0-4

D = 200 + (D_flags × 20) + (boundary_score × 4)
C = 200 + (C_flags × 20) + (opacity × 8)
balance = assigned by transparency tier: high=90±4, medium=83±4, low=70±4
N = round((D + C) / 2 × (balance / 100))
```

The resulting D and C values land in approximately the 200-284 range. N is capped at 290.

### The simulation engine defaults

When the simulation engine loads phases from a schema CSV, each individual D and C parameter defaults to `50.0` (the midpoint of a 0-100 scale). This is a neutral starting assumption: unknown parameters are placed at the center of the available range, giving equal initial weight to all constraints and contributions.

---

## 5. Where the Mathematical Constants Enter

The phi-derived constants appear not as outputs of the calculation but as reference thresholds applied to the balance score:

```
PHI = (1 + sqrt(5)) / 2 ≈ 1.618

Zone thresholds on the balance score B (0-100):
  Coherent:   B >= 80
  Stressed:   B >= 100/phi  ≈ 61.8
  Failure:    B >= 100×(1 - 1/phi)  ≈ 38.2
  Breakdown:  B < 38.2
```

The balance score B is a pure function of the D/C ratio:

$$B = 100 \times e^{-2|D-C| / \max(D,C)}$$

This is important: B depends only on the ratio D/C, not on the absolute values of D and C. If both D and C are multiplied by any constant, B is unchanged. The phi thresholds are therefore fixed rulers applied to a ratio-based measurement. They do not emerge from the data. They are asserted as the structural attractors that coherent systems converge toward.

### The key distinction from AI training

In machine learning, a model is trained toward a target defined by human-labeled data. The ground truth is contingent on human judgment. In the NDC model, the convergence target is a mathematical constant that exists independently of any observation or labeling. Phi is not an opinion. The NDC model's validity claim is therefore of a different and stronger kind: not "does this match what experts said is good?" but "does this phase sit near the mathematically necessary equilibrium ratio?"

---

## 6. Current Strengths of the Implementation

**Balance score is scale-invariant.** Because B = f(D/C), not f(D, C) independently, the arbitrary 200 floor and the flag-count ceiling do not distort the primary convergence measurement. Comparing phase balance scores across phases within a project is valid as long as the same flag-counting formula is applied consistently.

**The framework architecture is correct.** The recursive triadic structure (parent N differentiates into D and C, which negotiate to produce child N) is properly implemented. Constraint propagation between phases is modeled. The phi zone classification is correctly applied to the exponential balance score.

**The opacity-to-C mapping is principled.** Higher opacity raises C in the formula, reflecting that an opaque phase is one where contributions and outputs are less traceable. This is structurally sound.

---

## 7. Current Weaknesses and Open Problems

### 7.1 Physical primitives do not feed directly into D and C

The most significant gap. Tholonic primitives such as ore grade, energy consumption, water use, and regulatory compliance counts are not currently used to compute D and C. Instead, binary structural flags (did the physical state change? was custody transferred?) serve as proxies. The measurement instrument describes the schema structure, not the physical supply chain.

The mathematical architecture is in place. The empirical grounding is not yet built.

### 7.2 The scale is arbitrary and instrument-dependent

The D and C values (roughly 200-284) are determined by how many binary flags are in the PDI schema. Adding or removing a flag shifts the ceiling. This means:

- The absolute values of D and C have no physical meaning.
- The 290 cap on N is not derived from any physical or mathematical principle. It is a safety rail set slightly above the formula's arithmetic maximum.
- The default value of 50.0 per parameter in the simulation engine is the midpoint of an arbitrary 0-100 range.

None of these numbers derive from phi, the primes, or any supply chain reality.

### 7.3 The sustainability metric is scale-dependent

Unlike the balance score, the sustainability metric is NOT ratio-based:

```
energy_cost   = |D - C|² + energy_base
sustainability = 100 / energy_cost
```

The absolute magnitude of `|D - C|` matters here. Two phases with identical D/C ratios (identical balance scores, identical convergence behavior) will report different sustainability scores if their absolute D and C values differ. This is a measurement artifact introduced by the arbitrary scale.

### 7.4 Cross-commodity comparison is not yet valid

Because different projects may accumulate different numbers of flags in their PDI schemas, a balance score of 65 in a gold mining phase does not necessarily represent the same structural condition as a balance score of 65 in a water treatment phase. The measurement instrument is not yet standardized across projects.

---

## 8. Approaches to a Principled Scale

Four candidates for grounding the scale more rigorously, listed in recommended implementation order:

### 8.1 Threshold-ratio normalization (completed: gold_v2)

Normalize each tholonic primitive as a ratio to its minimum viable threshold:

```
normalized = actual_value / threshold_value
```

Ore grade 1.5 g/t against a minimum economic threshold of 1.0 g/t scores 1.5. A phase at exactly its definitional threshold scores 1.0 on every primitive. D and C aggregates then live on a scale where 1.0 means "at the boundary of viability."

This is scale-invariant by construction (all inputs are dimensionless ratios), makes the sustainability metric comparable across projects, and grounds each measurement in a physical or institutional fact rather than a schema artifact. The threshold values themselves must be sourced from industry standards or domain knowledge and documented in the PDI schema.

**Status: implemented in `frontend/project/gold_v2/`.** The gold supply chain now carries a `normalized` entity alongside the original `synthetic` entity. D and C for each of the 9 phases are computed as averages of 2-4 threshold-ratio primitives per side, sourced from WGC 2023, LBMA Good Delivery Rules 2024, COMEX delivery specifications, Newmont 2024 Sustainability Report, and ICMM benchmarks. All primitive definitions and threshold values are documented in `_meta._normalization_thresholds` within `gold_v2/data/processed/gold_supply_chain_ui.json`.

The normalized D and C values land in the 1.1-2.2 range (compared to 200-280 for the flag-count model). Key results:

| Phase | D (norm) | C (norm) | Balance | Zone | vs flag-count balance |
|---|---|---|---|---|---|
| 0 Geological | 1.506 | 1.385 | 85.1% | Coherent | +1.2 pp |
| 1 Mining | 1.280 | 1.339 | 91.6% | Coherent | -3.0 pp |
| 2 Processing | 1.196 | 1.239 | 93.3% | Coherent | -2.7 pp |
| 3 Doré | 1.409 | 1.262 | 81.1% | Coherent | -8.2 pp |
| 4 Refining | 1.295 | 1.226 | 89.8% | Coherent | -5.3 pp |
| 5 Bar Casting | 1.750 | 1.629 | 87.1% | Coherent | -7.9 pp |
| 6 Vaulting | 2.208 | 1.704 | 63.4% | Stressed | -2.1 pp |
| 7 Exchange | 1.111 | 1.072 | 93.2% | Coherent | +1.0 pp |
| 8 Recycling | 1.661 | 1.495 | 81.9% | Coherent | +1.9 pp |

All balance zones are identical between the flag-count and normalized models. The normalized model generally reduces balance scores by 3-8 percentage points for the thermal and precision-intensive phases (Doré, Refining, Bar Casting), because real energy intensity and specification overhead add genuine D load that binary flag presence/absence could not capture. Phase 6 (Vaulting) remains the single Stressed bottleneck in both models, confirming the flag-count model's structural conclusion.

### What the normalized primitives measure and what they do not

The primitives used in gold_v2 fall into three types:

**Industry standards and specifications.** Fixed by external bodies and publicly documented: LBMA fineness requirement (999.5/1000), COMEX delivery overhead ratio, NI 43-101 maximum inferred resource fraction, LBMA assay precision tolerance. These are knowable from desk research and stable over multi-year periods.

**Physical and engineering characteristics.** Intrinsic to the process type, not the specific run: energy intensity per ounce produced, recovery rate percentage, tailings generation ratio, reagent consumption per tonne. These describe *how* a phase operates, not *how much* it processed in a given period.

**Governance and transparency indicators.** Structural conditions of the operating environment: custody fragmentation count, opacity score, number of certification steps, regulatory reporting burden. These capture institutional load, not material flow.

What these primitives collectively describe is **how intensely each phase operates relative to its minimum viable threshold**. A phase with D = 1.75 is pressing against its definition constraints at 1.75 times the minimum level required to function. A phase with C = 1.50 is producing contributions at 1.50 times the minimum level. Neither number says anything about how many tonnes of material flowed through the phase in a given year.

**What is not measured: throughput volumes.** Actual flow quantities (tonnes mined, ounces refined, contracts settled, kilograms recycled) are absent from the current model. A small high-specification refinery and a large high-specification refinery operating under identical LBMA standards produce identical D/C values. This is a documented gap. The Phase 2 (Processing) notes in the JSON explicitly flag it: "No throughput volumes, recovery rates, treatment costs, or reagent consumption data in current schema. These are the primary N-state metrics for Phase 2 and remain MISSING."

This architecture is deliberate for the current stage. The structural primitives used are **available and auditable**: they come from industry reports, regulatory standards, and engineering benchmarks that any analyst can verify independently. Operational throughput data requires actual reporting from the companies running each phase, which is often proprietary, inconsistent across the chain, and subject to the exact opacity problem the model is measuring. Introducing unverifiable throughput estimates would undermine the auditability that is one of the framework's core design requirements.

Throughput as a scalar multiplier on the modulus (or as a third axis) is the natural next addition once reliable, auditable flow data becomes available for a given supply chain.

### 8.2 Information-entropy normalization / Confidence Accounting (priority 2: pilot when data available)

Treat each primitive as a probability distribution over its possible states. High uncertainty (unstable regulations, opaque custody) = high entropy. Low uncertainty (precisely measured ore grade, fully documented process) = low entropy. Entropy is naturally dimensionless and handles heterogeneous units: physical quantities, institutional facts, and relational properties all reduce to the same scale once expressed as uncertainty distributions.

The connection to **Confidence Accounting** is the strongest argument for this approach. Confidence Accounting treats reported values as probability distributions rather than point estimates, and entropy is the natural measure of how wide that distribution is. The PDI already captures informal entropy through opacity scoring (B12 opacity reasons, opacity scores 0-4). If each primitive's uncertainty is expressed as a distribution, the entropy contribution to D or C is directly comparable across commodities regardless of physical units, and connects to an established accounting framework that regulators and auditors already understand.

Practical implementation path:
1. Use the existing PDI opacity score as a proxy entropy contribution (already in the data).
2. Define a simple mapping from opacity score to an entropy weight on each D and C parameter.
3. Test on a pilot dataset where probability estimates are available.
4. Refine toward full probability distributions as data quality improves.

This approach has the broadest applicability across commodity types and ecosystem services and is likely the most defensible to external audiences. It is elevated above percentile normalization in priority because it does not require a large reference population to be useful.

### 8.3 Percentile normalization against a reference population (priority 3: deferred)

Normalize each primitive to its rank within a reference population (all gold mines, all water treatment plants of comparable type). Valid for within-commodity benchmarking. Does not generalize across commodity types.

This approach requires a minimum of two commodities and two ecosystem service chains with enough data points per class for stable percentiles. The current project does not yet have that volume. It becomes useful later, once many more projects are in the system, as a cross-instance benchmarking layer on top of whichever primary scale is adopted. Implementing it prematurely would produce unstable rankings that shift significantly as new instances are added.

### 8.4 Prime-ratio derivation (priority 4: theoretical experiment on gold)

The most internally consistent approach. If N, D, C are assigned primes 2, 3, 5, the natural reference ratio is D/C = 3/5 = 0.6, which approximates 1/phi (0.618). A scale derived from these prime ratios would make the phi threshold a direct consequence of the framework's own mathematical foundation rather than an externally imposed constant.

Gold is the right testbed because it has the most complete supply chain data and the clearest tholonic primitive candidates. The specific empirical test: for gold mining phases that are known to be functioning well, compute the actual D/C ratio and check whether it approximates 0.6. If it does, that is evidence the prime assignment is not arbitrary. If it does not, the result sharpens either the phase boundary definitions or the prime assignment logic.

This experiment is low-cost relative to its theoretical payoff: it does not require building a new normalization pipeline. It requires taking existing D and C values for gold phases, computing D/C, and comparing against the prime-derived target. It should be run alongside the threshold-ratio normalization work on gold rather than deferred indefinitely.

### Recommended implementation sequence

| Step | Approach | Status |
|---|---|---|
| 1 | 8.1 on gold | **Done.** Normalized entity in `gold_v2`. Complex extension in `gold_v3` (Section 11). |
| 2 | 8.4 experiment on gold | Pending. Low-cost test: compute D/C ratios from normalized values, compare against 3/5 = 0.6. |
| 3 | 8.2 pilot on available dataset | Pending. Waiting for probability/confidence data. |
| 4 | 8.3 across project library | Deferred. Requires enough instances per commodity class for stable percentiles. |

---

## 9. Summary of What the Model Currently Measures

The table below covers both the original flag-count implementation and the normalized implementation (gold_v2 / gold_v3). Validity assessments reflect the state of each implementation.

| What is measured | Flag-count model | Normalized model (gold_v2/v3) |
|---|---|---|
| D/C balance per phase | Valid for relative comparison within a project | Valid for within-project and (when thresholds are standardized) cross-project comparison |
| Convergence toward phi | Architecturally correct; input quality is the limitation | Same architecture; inputs are now physically grounded |
| Phase bottleneck identification | Valid as a relative ranking within a project | Valid; confirmed consistent with flag-count results for gold |
| Cross-project comparison | Not yet valid: different flag counts per schema | Potentially valid once threshold sources are standardized across projects |
| Sustainability per phase | Scale-dependent; not comparable across projects | Scale-invariant: D and C are dimensionless ratios; sustainability is now comparable |
| N (operational capacity) | Valid as a relative within-project metric | Same; now also interpretable as an absolute: N near 1.0 means near-threshold operational output |
| Operational load (modulus) | Not available: scale is arbitrary | Available in gold_v3: \|z\| = sqrt(D²+C²) is a genuine load measure (Section 11) |
| Balance angle (argument) | Not available: absolute scale meaningless | Available in gold_v3: θ = arctan(C/D) encodes zone position in angular form |

---

## 10. Roadmap Implication

**Step 1 of the implementation sequence is complete.** The gold supply chain now has a physically grounded normalized entity (gold_v2) and a complex number extension on top of it (gold_v3). This has achieved the following outcomes from the original roadmap:

1. The sustainability metric is now scale-invariant for gold. D and C are dimensionless ratios; |D-C|² is a ratio quantity comparable across phases and (in principle) across projects with normalized D/C values.
2. The phi thresholds are now connected to physical viability boundaries rather than flag-count ceilings. A phase with D = 1.5 is constrained at 1.5 times the minimum viable threshold on the D side, not at an abstract flag-count score.
3. The complex extension (Section 11) has added the modulus as a second, orthogonal health dimension. The balance score continues to measure ratio health; the modulus measures operational load. These are genuinely independent: a phase can be coherent but heavy (Bar Casting: balance 87.1%, |z| = 2.391) or stressed but not the heaviest (Vaulting: balance 63.4%, |z| = 2.789).

**What Step 1 confirmed about the gold model:** The balance zone assignments are stable across both methods (flag-count and normalized). Phase 6 (Vaulting) is the bottleneck in both. This is important: it means the structural conclusions drawn from the original flag-count model are not artifacts of the counting instrument. They reflect real structural properties of the gold supply chain.

**Remaining steps:** Step 2 (prime-ratio experiment: check whether normalized D/C ratios for healthy gold phases approximate 3/5 = 0.6) is now directly executable because physically grounded D and C values exist in gold_v2. This is the next low-cost theoretical test. Step 3 (information-entropy / Confidence Accounting pilot) remains the highest-value next investment for cross-commodity comparability. The existing PDI opacity scoring provides a starting proxy that can be refined incrementally as more structured uncertainty data becomes available.

---

## 11. Complex Number Extension: Capturing Magnitude Alongside Ratio

### The current limitation

The balance score is purely ratio-based:

$$B = 100 \times e^{-2|D-C| / \max(D,C)}$$

Two phases with D=256, C=248 and D=56, C=48 produce identical balance scores because the D/C ratio is the same. The absolute scale is invisible. This means the model currently cannot distinguish a large, heavily loaded phase from a small, lightly loaded one if their constraint-to-contribution ratios happen to be equal.

### Representing a phase as a complex number

If D and C are treated as the real and imaginary components of a complex number:

```
z = D + iC
```

the complex plane immediately provides two independent quantities:

```
argument  θ = arctan(C / D)     — captures the D/C ratio (same information as the balance score)
modulus  |z| = sqrt(D² + C²)    — captures the absolute scale (new information)
```

These two quantities are mathematically independent. Knowing one tells you nothing about the other. Together they fully locate a phase in the operational space.

### The π/4 connection

When D = C (perfect balance), the argument of z = D + iD is exactly π/4. This is the same π/4 that serves as the operational constant in the cTVF engine: the constant that injects new information per iteration. In the complex plane, the ideal N-D-C balance maps geometrically to the 45-degree line, and movement along that line represents increasing operational scale at constant balance. The π/4 constant therefore emerges from the geometry of the complex plane rather than being imposed externally.

A second constant appears immediately: a unit-balanced phase with D = C = 1 has modulus |z| = sqrt(1² + 1²) = **√2**. The structural constant of the cTVF is the natural unit of a perfectly balanced phase in the complex representation.

### What the modulus measures

The modulus |z| = sqrt(D² + C²) is the Euclidean distance from the origin to the phase's position in the D-C plane. Phases far from the origin carry a larger total operational load: more constraints and more contribution activity simultaneously. Phases close to the origin are lighter, simpler transitions.

This gives the model a second dimension of health assessment:

| Quantity | What it measures | Formula |
|---|---|---|
| Balance score B | How close D and C are to each other (ratio health) | $100 \times e^{-2\|D-C\| / \max(D,C)}$ |
| Argument θ | The D/C angle; ideal at π/4 | arctan(C / D) |
| Modulus \|z\| | Total operational load of the phase (scale) | sqrt(D² + C²) |

### A worked comparison

Using the wheat farm to flour mill example from Section 3:

```
Low-opacity case:   D = 256, C = 248
  |z| = sqrt(256² + 248²) = sqrt(65536 + 61504) = sqrt(127040) ≈ 356.4
  θ   = arctan(248 / 256) ≈ 44.1°  (close to the ideal 45°)

High-opacity case:  D = 256, C = 272
  |z| = sqrt(256² + 272²) = sqrt(65536 + 73984) = sqrt(139520) ≈ 373.5
  θ   = arctan(272 / 256) ≈ 46.7°  (tilted past 45° — C exceeds D)
```

Both phases have similar balance scores (93.9 vs 88.9). The modulus reveals that the high-opacity phase carries a larger total operational load (373.5 vs 356.4): opacity has added weight to the system, not just shifted its ratio.

### Phi zone thresholds in the complex plane

The existing phi-derived thresholds apply to the balance score, which is a function of the argument θ. In the complex plane, each threshold defines a cone: the region between two rays from the origin at angles corresponding to the coherent, stressed, failure, and breakdown zones. A phase's modulus determines how far along its zone cone it sits — its operational intensity within that health zone.

This means the phi thresholds do not need to change. The complex extension adds an orthogonal axis (scale) without replacing the existing ratio axis (balance).

### Status: implemented in gold_v3

The prerequisite (Section 8.1 threshold-ratio normalization) is complete in gold_v2. The complex extension is built on top of it in `frontend/project/gold_v3/`. Each normalized phase in gold_v3 carries two additional fields in the JSON:

```json
"modulus":      2.789,
"argument_deg": 37.66
```

These are computed directly from the normalized D and C values: `modulus = sqrt(D^2 + C^2)`, `argument_deg = atan2(C, D) * 180 / pi`. The complex plane is visualized at `gold_v3/supply_chain/complex_plane.html`.

---

### How to read the D-C complex plane

The visualization plots each supply chain phase as a point (D, C) in the first quadrant of the Cartesian plane, where the horizontal axis is D (real component, constraint load) and the vertical axis is C (imaginary component, contribution load).

**Angular zones.** Because the balance score is a function only of the D/C ratio, each health zone corresponds to an angular wedge in the complex plane rather than a rectangular region. A phase anywhere inside the coherent wedge has a coherent balance score regardless of its distance from the origin. The zone boundaries (derived from the phi thresholds) are:

| Angle θ | Balance score | Zone boundary |
|---|---|---|
| 45.0° | 100% | Perfect balance (D = C) |
| 37.3° to 52.7° | ≥ 61.8% | Coherent zone |
| 27.4° to 37.3° and 52.7° to 62.6° | 38.2%–61.8% | Stressed zone |
| < 27.4° or > 62.6° | < 38.2% | Failure zone |

A phase at θ below 45° has D > C (constraint-led). A phase at θ above 45° has C > D (contribution-led).

**Modulus as distance from origin.** Concentric circles at equal modulus values represent equal operational load. Phases on the same circle carry the same total load but may have different balance angles. Phases on the 45° line at different distances from the origin are both perfectly balanced but at different operational scales.

**The √2 reference point.** The point (1, 1) represents a phase at exactly the minimum viable threshold on both D and C sides. Its modulus is sqrt(1² + 1²) = √2 = 1.414. This is the structural constant of the cTVF: the minimum modulus of a perfectly balanced viable phase. Phases with modulus above √2 are operationally above-threshold; phases below √2 would be below threshold on at least one side.

---

### Gold supply chain results

The normalized gold supply chain (gold_v3) produces the following complex values:

| Phase | D | C | Modulus \|z\| | Argument θ | Zone |
|---|---|---|---|---|---|
| 0 Geological | 1.506 | 1.385 | 2.046 | 42.60° | Coherent |
| 1 Mining | 1.280 | 1.339 | 1.852 | 46.29° | Coherent |
| 2 Processing | 1.196 | 1.239 | 1.722 | 46.01° | Coherent |
| 3 Doré | 1.409 | 1.262 | 1.892 | 41.85° | Coherent |
| 4 Refining | 1.295 | 1.226 | 1.783 | 43.43° | Coherent |
| 5 Bar Casting | 1.750 | 1.629 | 2.391 | 42.95° | Coherent |
| 6 Vaulting | 2.208 | 1.704 | 2.789 | 37.66° | Stressed |
| 7 Exchange | 1.111 | 1.072 | 1.544 | 43.98° | Coherent |
| 8 Recycling | 1.661 | 1.495 | 2.235 | 41.99° | Coherent |

Key observations:

**Phase 7 (Exchange Registration) is the lightest phase.** Modulus = 1.544, argument = 43.98° (closest to 45°). Exchange is the most rule-standardized phase in the chain: both D and C are close to 1.0 (near minimum viable threshold on both sides), and the D/C ratio is nearly perfect. This confirms that the exchange registration process is structurally efficient: it imposes just enough constraint to function and integrates just enough contribution to qualify as a phase.

**Phase 6 (Vaulting) is both the heaviest and the most stressed.** Modulus = 2.789 (highest in the chain), argument = 37.66° (below the Coherent boundary of 37.3°). Custody fragmentation (D primitive ratio = 3.0) and opacity (normalized to 1.75) drive D well above C. The vaulting phase is not just ratio-imbalanced: it also carries the largest total operational load in the chain. Interventions should target the D side (reduce custody fragmentation, reduce opacity) rather than the C side.

**Phases 1-5 and 7-8 cluster tightly at 42°-47°.** All coherent phases sit within a 5° band around the ideal 45° line. This is a strong structural signal: the gold supply chain is well-calibrated in ratio terms across its entire length except for the custodial bottleneck at Phase 6.

**Bar Casting (Phase 5) has the highest modulus among coherent phases.** Modulus = 2.391. The LBMA assay precision requirement (D primitive ratio = 2.000, the highest single D sub-score in the chain) adds substantial D load that is nearly matched by fast turnaround and large brand recognition on the C side. The phase is coherent but operationally heavy, which is not visible from the balance score alone.

**The modulus spread is 1.245 (from 1.544 to 2.789).** The chain is not uniform in operational load. Exchange is 45% lighter than Vaulting despite comparable balance scores. This spread is diagnostic: a narrow spread would indicate a chain where all phases carry similar loads, while a wide spread (as here) points to structural asymmetry in operational complexity.

---

### What the complex representation adds beyond the balance score

The balance score answers one question: how close are D and C to each other? The complex representation answers two:

1. How close are D and C to each other? (the argument, θ: same answer as the balance score)
2. How large is the combined operational load? (the modulus, |z|: new information)

These are independent. Two phases with identical balance scores (identical angles) can have very different moduli: one phase may be a lightweight transition, the other a heavy industrial process, and the balance score cannot distinguish them. The modulus makes this distinction explicit and measurable.

Consider Mining (Phase 1) and Exchange (Phase 7): balance scores 91.6% and 93.2% (very similar). Moduli 1.852 and 1.544 (20% difference). Mining carries 20% more combined operational load than Exchange. If an analyst is allocating monitoring resources or designing bond performance triggers, the balance score alone suggests these phases are nearly equivalent. The modulus reveals they are not.

---

### Intervention guidance from the complex plane

A phase's position in the complex plane tells an analyst not just whether there is a problem but what kind of intervention would address it.

**Phase in the Stressed zone with D > C (argument below 45°):** The phase is constraint-dominated. Intervention should reduce D: remove unnecessary regulatory overhead, consolidate custody chains, reduce opacity, simplify certification requirements. This moves the point left (lower D), rotating the argument up toward 45° while also reducing the modulus (lighter phase). Example: Phase 6 Vaulting.

**Phase in the Stressed zone with C > D (argument above 45°):** The phase is contribution-dominated. Intervention should increase D (add structural definition and documentation) or reduce C by improving output quality so each contribution unit does more. Example: would be a phase with opacity = 4 inflating C far above D.

**Phase in the Coherent zone with high modulus:** The phase is healthy in ratio terms but operationally heavy. This is not an emergency but it is a cost signal. Reducing both D and C proportionally (moving toward the origin along the same angle) would reduce operational load without changing the balance score. Example: Phase 5 Bar Casting.

**Phase in the Coherent zone with modulus near √2:** The phase is healthy and light. This is the target state: barely above the viability threshold on both sides, well-balanced, minimal operational overhead. Example: Phase 7 Exchange Registration.

---

### Connection to the cTVF mathematical constants

The complex representation makes two of the framework's five mathematical constants emerge geometrically rather than being imposed:

**π/4:** The ideal balance line (D = C) is the 45° ray, which is the angle π/4 radians. The same π/4 appears as the operational constant in the cTVF engine (the constant injecting new information per iteration). In the complex plane, π/4 is not a parameter chosen by the model — it is the geometric consequence of D = C, which is the model's own definition of perfect balance.

**√2:** The minimum modulus of a perfectly balanced viable phase is |z| at (1, 1) = sqrt(1² + 1²) = √2. The √2 structural constant of the cTVF is the natural unit of the complex plane at threshold, not an externally imposed constant.

Pi (π), phi (φ), and e enter separately: phi through the zone angle boundaries, pi through the π/4 balance line (and as the chain-average balance score in the cTVF notation), and e through the balance score formula itself (the exponential decay function).
