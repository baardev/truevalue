# The True Value Pricing Convergence Index (TVPCI)
### *An Introduction with Mechanics, Mathematics, and Interpretation*

---

## Preface

This document explains the **True Value Pricing Convergence Index (TVPCI)**: what it measures, how it is calculated, and what it means for price interpretation. It assumes familiarity with the True Value Framework (TVF) and the N-D-C phase analysis that underpins it. If you haven't read the TVF college-level introduction, start there: the TVPCI is the index that sits on top of the TVF's phase analysis.

The TVPCI is a composite index from 0 to 100. **It is not a price.** It is a structural integrity score, a quantitative measure of how much friction, imbalance, and incoherence exists within a supply chain such that the observed market price diverges from True Value. A TVPCI of 100 means the chain is structurally coherent: value flows proportionally through every phase, all phases are internally balanced, and the market price is structurally trustworthy. As the score falls, the gap between market price and True Value is *structurally explained*, not by intent or speculation, but by measurable conditions at each phase.

---

## 1. Where the TVPCI Sits in the Analytical Stack

The TVF separates analysis into five layers:

```
Layer 1: Physical Supply Chain     (Phase mapping, N-D-C metrics per phase)
Layer 2: Value Chain               (Phase-aligned costs, margins, prices)
Layer 3: TVPCI                     (Composite structural integrity score)  <- HERE
Layer 4: True Value Pricing        (Price convergence interpretation)
Layer 5: Financial Abstraction     (Paper claims, derivatives, out of scope)
```

The TVPCI is computed entirely from Layer 1 and Layer 2 inputs. It feeds forward into Layer 4 (price interpretation) but is never derived from Layer 5 data. This sequencing is methodologically non-negotiable: if you allow financial derivatives or exchange positioning to influence a structural supply chain score, you collapse the analytical independence that makes the score meaningful.

---

## 2. The Three Structural Sub-Scores

The TVPCI is a weighted composite of three independent sub-scores. Each captures a distinct structural property of the supply chain.

---

### 2.1 Phase Balance Score ( B̄ ), Weight: 0.40

This is the most direct sub-score. For each phase *i*, the balance score is:

$$B_i = 100 \cdot \exp\!\left(-2 \cdot \frac{|D_i - C_i|}{\max(D_i, C_i)}\right)$$

Where D_i is the sum of constraint parameters and C_i is the sum of connection parameters, each on a 0-100 scale. The balance score peaks at 100 when D = C and decays exponentially as imbalance grows.

The chain-level mean balance score is:

$$\bar{B} = \frac{1}{P} \sum_{i=0}^{P-1} B_i$$

**Worked example: shea collection phase (Phase 0)**

```
D1: buyer quality specifications     = 45
D2: cooperative membership rules     = 50
D3: seasonal harvest calendar        = 70
D4: transport packaging standards    = 40
D_total = 205

C1: alternative buyers               = 20
C2: price information access         = 15
C3: cooperative network strength     = 40
C4: processing alternatives          = 35
C_total = 110

Imbalance = |205 - 110| = 95
B0 = 100 x exp(-2 x 95 / 205)
   = 100 x exp(-0.927)
   = 100 x 0.396
   = 39.6  <-  CRITICAL range
```

The collection phase has a balance score of approximately 40, indicating severe structural imbalance. The collector is heavily constrained (D = 205) with very few alternatives or market connections (C = 110). This one phase will substantially drag down the chain-wide B̄.

**Interpretation scale:**

| B̄ | Condition |
|---|---|
| 95-100 | Near-perfect: all phases operating at structural optimum |
| 80-94 | Good: minor phase-level imbalances |
| 60-79 | Fair: one or more phases with meaningful D-C friction |
| 40-59 | Poor: multiple phases underperforming |
| 0-39 | Critical: chain-wide structural failure |

---

### 2.2 Boundary Coherence Score ( Φ̄ ), Weight: 0.40

This is the most mathematically interesting sub-score and the most diagnostically powerful.

At every boundary between adjacent phases, the TVF computes the ratio of their N-states:

$$r_{i \to i+1} = \frac{N_{i+1}}{N_i}$$

It then compares this ratio to **φ, the golden ratio (approximately 1.61803)**, using the same exponential decay function:

$$\Phi_{i \to i+1} = 100 \cdot \exp\!\left(-2 \cdot \frac{|r_{i \to i+1} - \varphi|}{\varphi}\right)$$

The chain-level mean boundary coherence is:

$$\bar{\Phi} = \frac{1}{P-1} \sum_{i=0}^{P-2} \Phi_{i \to i+1}$$

**Why φ: The Fibonacci Derivation**

This is not a cosmetic choice. The mathematical justification runs as follows.

The Clarity TrueValue  propagation rule states that when D and C parameters are *inherited naturally* between phases (specifically, when each new phase's D receives the value of the prior phase's N-state, and each new phase's C receives the value of the prior phase's D), the sequences of D and C values follow the Fibonacci recursion:

$$D_{n+1} = N_n = \sqrt{D_n \cdot C_n}, \qquad C_{n+1} = D_n$$

When D and C follow Fibonacci-type growth (each D_n = F_{n+1} and C_n = F_n, where F_n is the nth Fibonacci number), the N-states are:

$$N_n = \sqrt{D_n \cdot C_n} \cdot \frac{B_n}{100} \approx \sqrt{F_{n+1} \cdot F_n}$$

The ratio of consecutive N-states then becomes:

$$\frac{N_{n+1}}{N_n} = \frac{\sqrt{F_{n+2} \cdot F_{n+1}}}{\sqrt{F_{n+1} \cdot F_n}} = \sqrt{\frac{F_{n+2}}{F_n}}$$

Using the Fibonacci identity F_{n+2} = F_{n+1} + F_n:

$$\frac{F_{n+2}}{F_n} = \frac{F_{n+1}}{F_n} + 1 \;\xrightarrow{n \to \infty}\; \varphi + 1 = \varphi^2$$

Therefore:

$$\frac{N_{n+1}}{N_n} \;\to\; \sqrt{\varphi^2} = \varphi$$

**The φ benchmark is not an assumption.** It is the convergent limit of the natural proportional inheritance of D and C parameters between phases. A boundary ratio at φ means that phase is inheriting capacity from the prior phase in exactly the proportion the Tholonic framework generates from first principles. A ratio below φ (say, 0.5) means capacity has been suppressed: something is extracting or retaining value at that boundary that the structural logic does not account for.

**Worked example: gold, Phase 5 to Phase 6 boundary**

```
N5 (bar casting) = 237
N6 (vaulting)    = 118

r(5->6) = 118 / 237 = 0.498

Phi(5->6) = 100 x exp(-2 x |0.498 - 1.618| / 1.618)
          = 100 x exp(-2 x 1.120 / 1.618)
          = 100 x exp(-1.385)
          = 100 x 0.250
          = 25.0  <-  SEVERE suppression
```

The Phase 5 to Phase 6 boundary in the gold supply chain, the transition from refiner to vault, scores 25/100 on boundary coherence. The N-state is being cut roughly in half (0.498) when the natural, proportional value would be to increase it by 1.618. This is quantitative evidence of the structural bottleneck at the custody and vaulting interface: the small number of approved vault operators, the opaque custody arrangements, and the institutional D-constraints on logistics all suppress capacity precisely at this junction.

**Worked example: shea, farmgate to retail amplification**

From Phase 1 (first farmgate sale: \$150/MT) to Phase 6 (retail equivalent: \$47,500/MT), the value multiplies **317 times** across 5 phase boundaries.

In a structurally coherent chain where each boundary ratio equals φ:
$$317 \approx \varphi^{12.0}$$

So a 317x value amplification distributed equally across 12 φ-steps would require 12 boundaries, which is more than the 5 actual boundaries. In practice, the amplification is highly concentrated: approximately 16x at Phase 3 (processing/refining, \$250 to \$4,000/MT) and a disproportionate accumulation at the EU manufacturing and retail stages. The Phase 4 (export) boundary shows N4 = 158 vs N3 = 241, a ratio of 0.66, which is below φ and consistent with intermediary extraction at the export stage.

**Boundary coherence interpretation:**

| Φ̄ | Status | Interpretation |
|---|---|---|
| 80-100 | r approximately φ across most boundaries | Value flows proportionally, with no structural extraction |
| 55-79 | Mild deviation | Localised boundary failures |
| 35-54 | Moderate deviation | Systematic value capture by intermediaries |
| 0-34 | Severe deviation | Market price structurally divorced from True Value |

---

### 2.3 Phase Sustainability Score ( S̄_norm ), Weight: 0.20

The sustainability index for each phase measures the *energy cost* of imbalance, capturing the friction, coercion, and inefficiency consumed by maintaining an unbalanced phase. It is defined as:

$$S_i = \frac{100}{|D_i - C_i|^2 + 10}$$

This is a decreasing function of imbalance: when D = C (imbalance = 0), S reaches its maximum of 100/10 = 10 (arbitrary units). As imbalance grows, the squared term in the denominator causes S to fall rapidly; the energy cost of imbalance grows quadratically, not linearly.

For chain-level comparison, S is normalised to 0-100 across all phases:

$$\bar{S}_{\text{norm}} = \frac{\bar{S} - S_{\min}}{S_{\max} - S_{\min}} \cdot 100$$

This sub-score is weighted at 0.20 because it is partially captured by the balance score (B̄ already reflects D-C disparity). Its additional value is diagnostic: phases with catastrophically low S values (very large imbalances) stand out even when the balance score alone might obscure the scale of the energy waste.

---

## 3. The Composite TVPCI Formula

$$\text{TVPCI} = w_B \cdot \bar{B} + w_\Phi \cdot \bar{\Phi} + w_S \cdot \bar{S}_{\text{norm}}$$

With default weights w_B = 0.40, w_Phi = 0.40, w_S = 0.20.

**Commodity-specific weight profiles are permitted.** The gold chain weights more heavily on balance (w_B = 0.45) because Phase 6 (vaulting) is the dominant structural weakness and shows up most clearly in balance scores. The shea chain weights more heavily on boundary coherence (w_Phi = 0.45) because the diagnostic signal in shea is the disproportionate value amplification between phases, not the balance of any single phase.

---

## 4. The Opacity Correction

Not all phases are observable. When a phase is flagged as `OPAQUE` (no reliable data exists), it cannot contribute its actual scores. The opaque phase receives the chain mean of the transparent phases as a placeholder, and a **transparency penalty** is applied to the final index:

$$\text{TVPCI}_{\text{adjusted}} = \text{TVPCI} \cdot \left(1 - \alpha \cdot \frac{N_{\text{opaque}}}{P}\right)$$

Where α = 0.15 (15% maximum per-phase penalty), N_opaque is the count of opaque phases, and P is total phases.

**Example:** A chain with 8 phases, one of which is opaque (e.g., Phase 3, informal cross-border trade in the shea chain):

```
TVPCI (raw) = 68.4
Penalty = 1 - (0.15 x 1/8) = 1 - 0.01875 = 0.981
TVPCI_adjusted = 68.4 x 0.981 = 67.1
```

This penalty is not punitive in the moral sense. It is an epistemic adjustment: a chain we cannot fully observe cannot be given the same trust score as one we can. **Opacity is a finding, not a data gap.** The identity and count of opaque phases are always reported alongside the TVPCI score.

---

## 5. A Complete Worked Calculation

Here is the full TVPCI calculation for the gold supply chain using the reference N-values from the φ-engine:

### Step 1: Phase N-values and Balance Scores

| Phase | Name | D | C | B_i |
|---|---|---|---|---|
| 0 | Prospecting | 220 | 210 | 95.2 |
| 1 | Mining | 260 | 250 | 96.1 |
| 2 | Processing | 280 | 275 | 98.2 |
| 3 | Dore | 240 | 235 | 97.9 |
| 4 | Refining | 270 | 260 | 96.4 |
| 5 | Casting | 255 | 250 | 98.0 |
| 6 | Vaulting | 420 | 180 | **31.9** (bottleneck) |
| 7 | Exchange | 280 | 275 | 98.2 |

B̄ = (95.2 + 96.1 + 98.2 + 97.9 + 96.4 + 98.0 + 31.9 + 98.2) / 8 = **76.5**

### Step 2: N-states and Boundary Ratios

| Phase | N | Boundary | Ratio r | Phi score |
|---|---|---|---|---|
| 0 | 183 | P0 to P1 | 259/183 = 1.415 | exp(-2 x |1.415-1.618|/1.618) x 100 = 78.1 |
| 1 | 259 | P1 to P2 | 263/259 = 1.015 | exp(-2 x |1.015-1.618|/1.618) x 100 = 47.6 |
| 2 | 263 | P2 to P3 | 229/263 = 0.871 | exp(-2 x |0.871-1.618|/1.618) x 100 = 39.5 |
| 3 | 229 | P3 to P4 | 253/229 = 1.105 | exp(-2 x |1.105-1.618|/1.618) x 100 = 53.4 |
| 4 | 253 | P4 to P5 | 237/253 = 0.937 | exp(-2 x |0.937-1.618|/1.618) x 100 = 43.5 |
| 5 | 237 | P5 to P6 | 118/237 = **0.498** | exp(-2 x |0.498-1.618|/1.618) x 100 = **25.0** (worst) |
| 6 | 118 | P6 to P7 | 239/118 = 2.025 | exp(-2 x |2.025-1.618|/1.618) x 100 = 60.4 |
| 7 | 239 | n/a | n/a | n/a |

Phī = (78.1 + 47.6 + 39.5 + 53.4 + 43.5 + 25.0 + 60.4) / 7 = **49.6**

### Step 3: Composite TVPCI

Using gold weight profile (w_B = 0.45, w_Phi = 0.35, w_S = 0.20) and assuming normalised sustainability score of approximately 72:

```
TVPCI = (0.45 x 76.5) + (0.35 x 49.6) + (0.20 x 72.0)
      = 34.4 + 17.4 + 14.4
      = 66.2
```

With opacity correction (Phase 0 partially opaque, α = 0.15, 1 of 8 phases):

```
TVPCI_adjusted = 66.2 x (1 - 0.15 x 1/8)
               = 66.2 x 0.981
               = 65.0  (Moderate Divergence)
```

**Diagnosis:** The gold supply chain scores 65/100 (moderate divergence). The Phase 6 (vaulting) balance score of 31.9 is the primary drag on B̄. The Phase 5 to Phase 6 boundary coherence score of 25.0 is the primary drag on Phī. The bottleneck is unambiguously the custody and logistics interface: the structural point where a small number of approved vault operators, opaque holdings, and high institutional D-constraints compress the chain's operational capacity by more than half.

---

## 6. The Relationship to True Value Price

The TVPCI is explicitly a *structural* index, not a pricing model. The formal relationship is:

$$P_{\text{market}} = P_{\text{true}} \cdot \left(1 + \delta_{\text{structural}}\right)$$

Where the magnitude of the structural divergence term is proportional to:

$$|\delta_{\text{structural}}| \propto \left(1 - \frac{\text{TVPCI}}{100}\right)$$

**A TVPCI of 65 does not mean the market price is 35% wrong.** It means that 35 structural index points of friction, imbalance, and incoherence exist within the chain, and that any price formed in that chain carries a structurally unexplained component of that magnitude. How that component manifests (as overpricing at retail, underpricing at farmgate, or redistribution between intermediaries) is a Layer 4 (True Value Pricing) question, not a Layer 3 question.

This distinction is important for responsible use of the index. The TVPCI quantifies the *existence and scale* of structural distortion. It does not assign direction, intent, or mechanism to that distortion. Those require the full value chain layer analysis.

---

## 7. Bottleneck Identification

Because the TVPCI is fully decomposable by phase, it identifies which phase is most suppressing the chain-wide score. The **phase TVPCI contribution** formula is:

$$\text{TVPCI}_i = \frac{w_B \cdot B_i + w_S \cdot S_{i,\text{norm}}}{P} + \frac{w_\Phi \cdot (\Phi_{i-1 \to i} + \Phi_{i \to i+1})}{2(P-1)}$$

The phase with the lowest TVPCI_i is the structural bottleneck, the point where a targeted intervention would produce the largest gain in chain-wide convergence. In the gold chain, Phase 6 produces by far the lowest phase contribution. In the shea chain, Phase 0 (collection) and the Phase 3 to Phase 4 (processing-to-export) boundary produce the lowest contributions.

This bottleneck identification is the primary policy-actionable output of the TVPCI. It transforms a single headline number into a directed, phase-specific prescription.

---

## 8. Summary: What the TVPCI Is and Is Not

| Property | Value |
|---|---|
| Scale | 0-100 (dimensionless) |
| Produces a price? | **No**: produces a structural trust score |
| Three inputs | Phase Balance (40%), Boundary Coherence (40%), Phase Sustainability (20%) |
| Mathematical constants used | e (balance and boundary decay functions), φ (boundary coherence benchmark) |
| Source of φ-benchmark | Fibonacci propagation limit; not an assumption |
| Source of e in decay functions | Tholonic recursive structure; structurally required, not chosen |
| Opacity handling | Penalty per opaque phase; opacity always reported alongside score |
| Bottleneck output | Phase with lowest individual TVPCI contribution |
| Policy relevance | Identifies *where* and *how much* to intervene, not *whether* the price is right |

### Score Interpretation

| TVPCI | Label | Meaning |
|---|---|---|
| 90-100 | Structurally Coherent | Market price and True Value are structurally aligned |
| 75-89 | Near Convergence | Minor structural friction; small measurable divergence |
| 55-74 | Moderate Divergence | Identifiable phases distorting price |
| 35-54 | Significant Divergence | Structural price distortion; financial analysis will mislead |
| 0-34 | Critical Divergence | Market price does not reflect physical chain conditions |

---

*Document: TVPCI, True Value Pricing Convergence Index, College-Level Explanation*
*Version: 1.0, April 2026*
*Part of the True Value Analytics framework documentation*
