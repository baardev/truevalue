# NDC Measurement Framework: Primitives, Scales, and Open Problems

## Overview

This document explains what the Tholonic N-D-C model is measuring, how measurements
are currently derived, where the current implementation is sound, and where it requires
further grounding. It is intended as a reference for analysts and developers working
with this project.

---

## 1. The Tholonic N-D-C Framework

The Tholonic model describes any coherent system as a triadic structure of three
interacting components:

- **N (Negotiation):** The emergent operational state of the system. N is not measured
  directly. It arises from the balance between D and C. It is simultaneously the
  product of D and C at one level and the source that differentiates into D and C at
  the next level down.

- **D (Definition):** The constraints, boundaries, requirements, and specifications that
  define what a phase IS. Internally focused. Governs structure, identity, and operating
  envelope.

- **C (Contribution):** The outputs, flows, connections, and integrations that define
  what a phase DOES. Externally focused. Governs production, relationships, and downstream
  effects.

The system is most stable and efficient when D and C are in balance (D ≈ C). Imbalance
in either direction increases energy cost and degrades the N state. The phi-derived
thresholds mark the boundaries between structural health zones.

The framework has a mathematical grounding: when the first three prime numbers (2, 3, 5)
are assigned to N, D, and C respectively, and the recursive triadic structure is iterated,
the fundamental mathematical constants (phi, pi, sqrt(2), e) emerge as natural consequences.
This is not coincidental. It means the N-D-C structure has mathematical validity independent
of its descriptive utility.

---

## 2. Tholonic Primitives

### Definition

A **tholonic primitive** is a value that is fixed from the perspective of the phase being
modeled and therefore serves as a non-negotiable input to either D or C. It cannot be
changed by operations within the phase. It defines the phase's operating context.

### Three types of tholonic primitives

**Physically irreducible:** Fixed by the material world. The ore grade of a mineral
deposit is what the geology made it. No operational decision inside the mining phase
changes it. Example: `ore_grade_actual` in Phase 1 (Mine Extraction).

**Scope-relative (exogenous):** Fixed from the phase's perspective because the setting
agent is outside the phase's scope of control. Safety regulations are set by governments,
not mine operators. Exchange registration standards are set by COMEX, not refiners. These
are reducible in principle (a legislature could change a law) but irreducible from within
the phase. Example: `safety_standards`, `environmental_regulations`, `exchange_standards`.

**Crystallized structural choices:** Originally a decision made by the phase operator,
but now a fixed structural fact that defines what the operation IS. Once a mine is built
to a certain production capacity, that capacity defines the mine's identity for the
duration of the phase, even though it was a choice at construction time. Example:
`production_capacity`, `extraction_method_spec`.

### Why the term "tholonic primitives"

The term connects to the mathematical foundation of the framework. Prime numbers are
primitives in number theory: they cannot be factored into simpler components. Tholonic
primitives are analogous: they cannot be decomposed or changed from within the phase's
scope. The label also distinguishes them from "parameters," which implies tunability,
and from "variables," which implies freedom to change.

---

## 3. PDI (Phase Discovery Instrument) Boundary Flags: What They Are and How They Work

### What a flag is

A **flag** is a binary (true/false) question answered by an analyst about a single
event in a supply chain. An event is any moment where the material being tracked
changes in some observable way: its physical form, the unit it is measured in, who
holds custody of it, who owns it, what kind of process is being applied to it, or
whether its output is defined and measurable.

Flags are recorded in Module 2 of the PDI (Phase Discovery Instrument) YAML file, one
block per event. They are the primary instrument by which an analyst encodes
structural information about a phase boundary into a form the pipeline can compute with.

There are six scoring flags, each contributing +1 to the boundary score if true:

| Flag | Question answered | Contributes to |
|---|---|---|
| **B3** `physical_state_changes` | Does the material change physical state at this event? (e.g. ore to concentrate, wastewater to effluent) | D |
| **B4** `unit_changes` | Does the unit of measurement change? (e.g. kg/ha to tonnes/season, ML/day to m³ billed) | D |
| **B6** `process_class_changes` | Does the process class change from the preceding event? (extractive, chemical_thermal, specification, certification, custodial, commercial) | D |
| **B9** `custody_changes` | Does physical custody pass to a different actor? | C |
| **B10** `ownership_changes` | Does legal ownership change? (true / false / unknown) | C (indirectly via boundary_score) |
| **B11** `output_defined` | Is the output of this event measurable with a defined quantity and unit? | C |

B3, B4, and B6 are Definition flags: they describe changes to what the material IS
and what kind of process is being applied to it. B9, B10, and B11 are Contribution
flags: they describe changes to who controls the material and whether what it produces
can be observed and handed forward.

There are also two non-scoring descriptive flags used for context:

- **B5** `process_class`: the process class label for this specific event (not a score;
  used to determine whether B6 is true by comparing to the preceding event's class).
- **B12** `opacity_reason`: if B11 is false (output is not defined), this records why:
  informal practice, commercial secrecy, or physical inaccessibility.

### How the boundary score is calculated

The boundary score for an event is the count of true flags across B3, B4, B6, B9,
B10, and B11. Maximum is 6. It is calculated by the analyst and recorded in the YAML;
it is not auto-computed.

```
boundary_score = B3 + B4 + B6 + B9 + B10 + B11    (each 1 if true, 0 if false)
```

### How the boundary score determines phase boundaries

Module 3 of the PDI uses the boundary score plus the B11 flag to decide whether an
event marks a genuine phase boundary or is merely a sub-process within an existing phase:

| Score | B11 | Classification |
|---|---|---|
| 0-1 | either | Sub-process: belongs inside a phase, not a boundary |
| 2-3 | true | Confirmed boundary |
| 2-3 | false | Sub-process: no measurable output, so not a phase boundary |
| 4-6 | either | Confirmed boundary (analyst should note if B11 is false) |

This rule is intentional. A phase boundary requires that something genuinely changes
AND that the result is observable. An event that scores high on structural change but
produces no measurable output (B11 = false) is a transformation without a handoff point.
The model cannot compute a C value for it and it does not qualify as a phase boundary.

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

Score 3 with B11 = true: confirmed phase boundary. This event marks where Phase 8
(advanced treatment) begins.

### How flags feed into D and C

After phase boundaries are confirmed in Module 3, the pipeline aggregates the flags
for the event that opens each phase:

```
d_flags       = B3 + B4 + B6     (the three Definition flags)
c_flags       = B9 + B11          (two of the three Contribution flags)
boundary_score = B3+B4+B6+B9+B10+B11   (all six flags)
opacity        = phase opacity score from Module 4 (0-4)

D = 200 + (d_flags × 20) + (boundary_score × 4)
C = 200 + (c_flags × 20) + (opacity × 8)
```

The three Definition flags (B3, B4, B6) contribute more weight per flag (20 points)
than the boundary score contribution (4 points per flag) because they directly describe
what is structurally changing about the phase's identity. The opacity score raises C
because an opaque phase is one where contributions are harder to trace, which the model
represents as higher (more complex, less well-defined) contribution load.

### What flags capture and what they do not

Flags capture **structural boundary characteristics**: whether and how the material,
the process, and the custody arrangement change at a phase transition. They are a
well-defined, reproducible analytical instrument.

What they do not capture is the **magnitude** of those changes. A phase where the
physical state changes from low-grade ore to concentrate (massive chemical transformation,
high energy input) scores B3 = true (1 point), exactly the same as a phase where
state changes from tagged bar to bonded bar (minor administrative change). The flag
is a binary presence/absence indicator, not a measurement of the significance or
scale of the change.

This is the fundamental limitation that connects to the broader normalization problem
discussed in Section 7: flags tell you that a change happened, not how large or
consequential that change was.

---

## 4. How D and C Values Are Currently Determined

### The PDI pipeline formula

When a new project is created from a PDI (Phase Discovery Instrument) YAML file, D and C
values are derived from structural binary flags attached to each phase boundary event:

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

When the simulation engine loads phases from a schema CSV, each individual D and C
parameter defaults to `50.0` (the midpoint of a 0-100 scale). This is a neutral starting
assumption: unknown parameters are placed at the center of the available range, giving
equal initial weight to all constraints and contributions.

---

## 5. Where the Mathematical Constants Enter

The phi-derived constants appear not as outputs of the calculation but as reference
thresholds applied to the balance score:

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

This is important: B depends only on the ratio D/C, not on the absolute values of D and C.
If both D and C are multiplied by any constant, B is unchanged. The phi thresholds are
therefore fixed rulers applied to a ratio-based measurement. They do not emerge from the
data. They are asserted as the structural attractors that coherent systems converge toward.

### The key distinction from AI training

In machine learning, a model is trained toward a target defined by human-labeled data.
The ground truth is contingent on human judgment. In the NDC model, the convergence
target is a mathematical constant that exists independently of any observation or
labeling. Phi is not an opinion. The NDC model's validity claim is therefore of a
different and stronger kind: not "does this match what experts said is good?" but "does
this phase sit near the mathematically necessary equilibrium ratio?"

---

## 6. Current Strengths of the Implementation

**Balance score is scale-invariant.** Because B = f(D/C), not f(D, C) independently,
the arbitrary 200 floor and the flag-count ceiling do not distort the primary convergence
measurement. Comparing phase balance scores across phases within a project is valid as
long as the same flag-counting formula is applied consistently.

**The framework architecture is correct.** The recursive triadic structure (parent N
differentiates into D and C, which negotiate to produce child N) is properly implemented.
Constraint propagation between phases is modeled. The phi zone classification is correctly
applied to the exponential balance score.

**The opacity-to-C mapping is principled.** Higher opacity raises C in the formula,
reflecting that an opaque phase is one where contributions and outputs are less traceable.
This is structurally sound.

---

## 7. Current Weaknesses and Open Problems

### 7.1 Physical primitives do not feed directly into D and C

The most significant gap. Tholonic primitives such as ore grade, energy consumption,
water use, and regulatory compliance counts are not currently used to compute D and C.
Instead, binary structural flags (did the physical state change? was custody transferred?)
serve as proxies. The measurement instrument describes the schema structure, not the
physical supply chain.

The mathematical architecture is in place. The empirical grounding is not yet built.

### 7.2 The scale is arbitrary and instrument-dependent

The D and C values (roughly 200-284) are determined by how many binary flags are in the
PDI schema. Adding or removing a flag shifts the ceiling. This means:

- The absolute values of D and C have no physical meaning.
- The 290 cap on N is not derived from any physical or mathematical principle. It is a
  safety rail set slightly above the formula's arithmetic maximum.
- The default value of 50.0 per parameter in the simulation engine is the midpoint of an
  arbitrary 0-100 range.

None of these numbers derive from phi, the primes, or any supply chain reality.

### 7.3 The sustainability metric is scale-dependent

Unlike the balance score, the sustainability metric is NOT ratio-based:

```
energy_cost   = |D - C|² + energy_base
sustainability = 100 / energy_cost
```

The absolute magnitude of `|D - C|` matters here. Two phases with identical D/C ratios
(identical balance scores, identical convergence behavior) will report different
sustainability scores if their absolute D and C values differ. This is a measurement
artifact introduced by the arbitrary scale.

### 7.4 Cross-commodity comparison is not yet valid

Because different projects may accumulate different numbers of flags in their PDI schemas,
a balance score of 65 in a gold mining phase does not necessarily represent the same
structural condition as a balance score of 65 in a water treatment phase. The measurement
instrument is not yet standardized across projects.

---

## 8. Approaches to a Principled Scale

Four candidates for grounding the scale more rigorously, listed in recommended
implementation order:

### 8.1 Threshold-ratio normalization (priority 1: implement now on gold)

Normalize each tholonic primitive as a ratio to its minimum viable threshold:

```
normalized = actual_value / threshold_value
```

Ore grade 1.5 g/t against a minimum economic threshold of 1.0 g/t scores 1.5.
A phase at exactly its definitional threshold scores 1.0 on every primitive.
D and C aggregates then live on a scale where 1.0 means "at the boundary of viability."

This is scale-invariant by construction (all inputs are dimensionless ratios), makes the
sustainability metric comparable across projects, and grounds each measurement in a
physical or institutional fact rather than a schema artifact. The threshold values
themselves must be sourced from industry standards or domain knowledge and documented
in the PDI schema.

Gold is the right starting point: minimum economic ore grade, LBMA fineness standards,
and COMEX delivery specifications are all publicly documented. The main open question is
institutional primitives (regulatory compliance, opacity): what constitutes a "minimum
viable threshold" for these requires domain judgment rather than industry standards, but
this is an acceptable approximation at the current stage of the project.

### 8.2 Information-entropy normalization / Confidence Accounting (priority 2: pilot when data available)

Treat each primitive as a probability distribution over its possible states. High
uncertainty (unstable regulations, opaque custody) = high entropy. Low uncertainty
(precisely measured ore grade, fully documented process) = low entropy. Entropy is
naturally dimensionless and handles heterogeneous units: physical quantities, institutional
facts, and relational properties all reduce to the same scale once expressed as
uncertainty distributions.

The connection to **Confidence Accounting** is the strongest argument for this approach.
Confidence Accounting treats reported values as probability distributions rather than
point estimates, and entropy is the natural measure of how wide that distribution is.
The PDI already captures informal entropy through opacity scoring (B12 opacity reasons,
opacity scores 0-4). If each primitive's uncertainty is expressed as a distribution, the
entropy contribution to D or C is directly comparable across commodities regardless of
physical units, and connects to an established accounting framework that regulators and
auditors already understand.

Practical implementation path:
1. Use the existing PDI opacity score as a proxy entropy contribution (already in the data).
2. Define a simple mapping from opacity score to an entropy weight on each D and C parameter.
3. Test on a pilot dataset where probability estimates are available.
4. Refine toward full probability distributions as data quality improves.

This approach has the broadest applicability across commodity types and ecosystem services
and is likely the most defensible to external audiences. It is elevated above percentile
normalization in priority because it does not require a large reference population to be
useful.

### 8.3 Percentile normalization against a reference population (priority 3: deferred)

Normalize each primitive to its rank within a reference population (all gold mines, all
water treatment plants of comparable type). Valid for within-commodity benchmarking.
Does not generalize across commodity types.

This approach requires a minimum of two commodities and two ecosystem service chains
with enough data points per class for stable percentiles. The current project does not
yet have that volume. It becomes useful later, once many more projects are in the system,
as a cross-instance benchmarking layer on top of whichever primary scale is adopted.
Implementing it prematurely would produce unstable rankings that shift significantly
as new instances are added.

### 8.4 Prime-ratio derivation (priority 4: theoretical experiment on gold)

The most internally consistent approach. If N, D, C are assigned primes 2, 3, 5, the
natural reference ratio is D/C = 3/5 = 0.6, which approximates 1/phi (0.618). A scale
derived from these prime ratios would make the phi threshold a direct consequence of
the framework's own mathematical foundation rather than an externally imposed constant.

Gold is the right testbed because it has the most complete supply chain data and the
clearest tholonic primitive candidates. The specific empirical test: for gold mining
phases that are known to be functioning well, compute the actual D/C ratio and check
whether it approximates 0.6. If it does, that is evidence the prime assignment is not
arbitrary. If it does not, the result sharpens either the phase boundary definitions or
the prime assignment logic.

This experiment is low-cost relative to its theoretical payoff: it does not require
building a new normalization pipeline. It requires taking existing D and C values for
gold phases, computing D/C, and comparing against the prime-derived target. It should
be run alongside the threshold-ratio normalization work on gold rather than deferred
indefinitely.

### Recommended implementation sequence

| Step | Approach | Trigger |
|---|---|---|
| 1 | 8.1 on gold | Now: threshold data exists for gold primitives |
| 2 | 8.4 experiment on gold | Alongside step 1: low cost, tests mathematical grounding claim |
| 3 | 8.2 pilot on available dataset | When probability/confidence data is ready |
| 4 | 8.3 across project library | When enough instances per commodity class exist for stable percentiles |

---

## 9. Summary of What the Model Currently Measures

| What is measured | How | Valid? |
|---|---|---|
| D/C balance per phase | Ratio of flag-count aggregates | Valid for relative comparison within a project |
| Convergence toward phi | Balance score vs phi-derived zone cuts | Architecturally correct; input quality is the limitation |
| Phase bottleneck identification | Which phases fall below 61.8% balance | Valid as a relative ranking within a project |
| Cross-project comparison | Same formula applied to different flag sets | Not yet valid without a standardized scale |
| Sustainability per phase | Absolute imbalance squared | Scale-dependent; not comparable across projects |
| N (operational capacity) | Geometric mean of D and C, weighted by balance | Valid as a relative within-project metric |

---

## 10. Roadmap Implication

The current implementation is a valid structural scaffold. The balance score convergence
measurement is sound for within-project analysis. The implementation sequence in Section 8
defines the path to empirical grounding. Completing steps 1 and 2 on the gold supply chain
would:

1. Make the sustainability metric scale-invariant (threshold-ratio normalization).
2. Test whether the mathematical grounding claim is empirically supported (prime-ratio experiment).
3. Connect the phi thresholds directly to physical viability boundaries rather than
   to flag-count ceilings.
4. Give the model falsifiable empirical predictions rather than structurally plausible
   outputs.

Step 3 (information-entropy / Confidence Accounting pilot) is the highest-value next
investment after gold, because it addresses cross-commodity comparability without
requiring a large reference population. It is also the approach most likely to be
understood and accepted by external audiences familiar with accounting and auditing
frameworks. The existing PDI opacity scoring provides a starting proxy that can be
refined incrementally as more structured uncertainty data becomes available.
