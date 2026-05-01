---
doc_id: tvpci_specification
title: TVPCI True Value Pricing Convergence Index
type: methodology
status: active
domain: tvpci
layer: methodology
projects:
  - gold
  - shea
  - aubeb
tags:
  - tvpci
  - "true_value"
  - pricing
  - convergence
  - ndc
related_docs:
  - tvpci_foundation
  - tvpci_explained_math
key_claims:
  - pricing_convergence_can_be_evaluated_against_tholonic_balance
source_role: tvpci_methodology
---

# True Value Pricing Convergence Index (TVPCI)
## Technical Specification and Methodology

**Version**: 1.0  
**Status**: Specification  
**Applies to**: Gold supply chain (Phase 0–7), Shea supply chain (Phase 0–6)  
**Framework**: TrueValue Analytics — C-G-N TrueValue model  

---

## 1. Purpose

The **True Value Pricing Convergence Index (TVPCI)** is a dimensionless composite index, ranging from 0 to 100, that measures how closely the structural condition of a supply chain would allow an observed market price to converge toward its True Value.

It does **not** produce a price. It produces a structural reading — a quantitative measure of how much friction, imbalance, and incoherence exists *within* the physical chain that would cause market price to diverge from True Value. When TVPCI = 100, the chain is operating at maximum structural integrity: value flows proportionally through every phase, all phases are internally balanced, and the chain imposes no structural distortion on price. As TVPCI falls, the gap between market price and True Value is *structurally explained* — not by speculation or intent, but by measurable phase-level C-G-N conditions.

This index is the primary quantitative output of the TrueValue Analytics platform. It precedes financial analysis; it does not replace it.

---

## 2. Position in the Analytical Stack

```
Layer 1 — Physical Supply Chain        (Phases 0–N, C-G-N metrics per phase)
Layer 2 — Value Chain                  (Phase-aligned costs, margins, prices)
Layer 3 — TVPCI                        (Composite structural integrity score)
Layer 4 — True Value Pricing           (Price convergence interpretation)
Layer 5 — Financial Abstraction        (Paper claims, leverage — OUT OF SCOPE here)
```

The TVPCI sits at Layer 3. It is computed entirely from Layers 1–2 inputs and feeds forward into Layer 4. It must never be computed from Layer 5 data (paper gold, financial derivatives, exchange positioning).

---

## 3. Mathematical Foundation

### 3.1 C-G-N Phase State

Each supply chain phase \(i\) is characterised by three quantities computed by the Tholonic engine:

**Definition total** (sum of constraint parameters, 0–100 each):

$$D_i = \sum_{k} d_{i,k}$$

**Contribution total** (sum of integration parameters, 0–100 each):

$$C_i = \sum_{k} c_{i,k}$$

**Balance score** (0–100, maximum when \(D_i = C_i\)):

$$B_i = 100 \cdot \exp\!\left(-2 \cdot \frac{|D_i - C_i|}{\max(D_i, C_i)}\right)$$

**Sustainability index** (higher is more efficient):

$$S_i = \frac{100}{|D_i - C_i|^2 + E_{\text{base}}} \qquad E_{\text{base}} = 10$$

**N-state** (emergent operational capacity):

$$N_i = \sqrt{D_i \cdot C_i} \cdot \frac{B_i}{100}$$

### 3.2 Phase Boundary Coherence (φ-model)

Between adjacent phases, the ratio of N-states is compared to the golden ratio \(\varphi = 1.61803\ldots\):

$$r_{i \to i+1} = \frac{N_{i+1}}{N_i}$$

**Boundary φ-score** (100 when \(r = \varphi\), decaying exponentially away from it):

$$\Phi_{i \to i+1} = 100 \cdot \exp\!\left(-2 \cdot \frac{|r_{i \to i+1} - \varphi|}{\varphi}\right)$$

When \(r \ll \varphi\): value is suppressed at the boundary (retained upstream or extracted by an intermediary).  
When \(r \gg \varphi\): disproportionate recovery — structurally unstable, typically precedes a collapse.  
When \(r \approx \varphi\): value passes through in natural proportion — no structural distortion at this boundary.

**Why φ? — Mathematical justification**

The N-state is a geometric mean (\(N_i = \sqrt{D_i \cdot C_i}\)), so the question arises: why should the ratio of consecutive N-states converge to φ, a constant that classically emerges from additive (Fibonacci-type) recursion, not from geometric means?

The answer lies in the Tholonic propagation rule. When the D and C parameters of successive phases follow the Fibonacci inheritance pattern — each phase's D receiving the prior phase's N-value, and each phase's C receiving the prior phase's D-value — the D and C sequences become consecutive Fibonacci numbers. Substituting \(D_n = F_{n+1}\) and \(C_n = F_n\):

$$\frac{N_{n+1}}{N_n} = \frac{\sqrt{F_{n+2} \cdot F_{n+1}}}{\sqrt{F_{n+1} \cdot F_n}} = \sqrt{\frac{F_{n+2}}{F_n}}$$

Using the Fibonacci identity \(F_{n+2} = F_{n+1} + F_n\):

$$\frac{F_{n+2}}{F_n} = \frac{F_{n+1}}{F_n} + 1 \;\xrightarrow{n \to \infty}\; \varphi + 1 = \varphi^2$$

Therefore:

$$\frac{N_{n+1}}{N_n} \;\to\; \sqrt{\varphi^2} = \varphi$$

The φ-benchmark is not arbitrary. It measures the structural fidelity of the underlying D and C parameters to the Fibonacci propagation pattern that the Tholonic framework generates from first principles. A boundary ratio at φ indicates that the phase's D and C parameters are inheriting value from the prior phase in the natural Tholonic proportion. Deviation from φ is a quantitative signal that this proportional inheritance has been disrupted — by extraction, suppression, or imbalance.

### 3.3 Chain-Level Aggregates

**Mean phase balance** across \(P\) phases:

$$\bar{B} = \frac{1}{P} \sum_{i=0}^{P-1} B_i$$

**Mean phase sustainability**:

$$\bar{S}_{\text{norm}} = \frac{\bar{S} - S_{\min}}{S_{\max} - S_{\min}} \cdot 100 \qquad \text{(normalised to 0–100)}$$

**System φ-coherence** across \(P-1\) boundaries:

$$\bar{\Phi} = \frac{1}{P-1} \sum_{i=0}^{P-2} \Phi_{i \to i+1}$$

---

## 4. TVPCI Composite Formula

The TVPCI is a weighted composite of three structural sub-scores:

$$\text{TVPCI} = w_B \cdot \bar{B} + w_\Phi \cdot \bar{\Phi} + w_S \cdot \bar{S}_{\text{norm}}$$

### 4.1 Default Weights

| Sub-score | Symbol | Default Weight | Rationale |
|---|---|---|---|
| Phase Balance | \(\bar{B}\) | 0.40 | D-C balance is the primary sustainability condition |
| Boundary Coherence | \(\bar{\Phi}\) | 0.40 | φ-proportionality determines value flow integrity |
| Phase Sustainability | \(\bar{S}_{\text{norm}}\) | 0.20 | Energy cost of imbalance; partially captured by \(\bar{B}\) |

Weights must sum to 1.0. Commodity-specific weight profiles may be defined (see Section 7).

### 4.2 Opacity Correction Factor

Phases with `data_quality: "OPAQUE"` introduce structural uncertainty. For each opaque phase \(j\), the sub-scores contributed by phase \(j\) are replaced by the chain mean of the transparent phases, and a **transparency penalty** is applied:

$$\text{TVPCI}_{\text{adjusted}} = \text{TVPCI} \cdot \left(1 - \alpha \cdot \frac{N_{\text{opaque}}}{P}\right)$$

Where:
- \(\alpha = 0.15\): maximum per-opaque-phase penalty (15%)
- \(N_{\text{opaque}}\): number of phases flagged OPAQUE
- \(P\): total phases

This penalty is not punitive. It is the structural consequence of incomplete information: a chain with opaque phases cannot be verified as operating at its stated TVPCI.

---

## 5. Sub-Score Interpretation

### 5.1 Phase Balance (\(\bar{B}\))

| Score | Condition | Interpretation |
|---|---|---|
| 95–100 | Near-perfect D-C balance | All phases operating near structural optimum |
| 80–94 | Good balance | Minor phase-level imbalances; chain broadly healthy |
| 60–79 | Fair balance | One or more phases with meaningful D-C friction |
| 40–59 | Poor balance | Multiple phases under-performing; value loss visible |
| 0–39 | Critical imbalance | Chain-wide structural failure; pricing signal unreliable |

### 5.2 Boundary Coherence (\(\bar{\Phi}\))

| Score | Ratio Profile | Interpretation |
|---|---|---|
| 80–100 | \(r \approx \varphi\) across most boundaries | Value passes proportionally — no structural extraction |
| 55–79 | Mild deviation | Localised boundary failures; monitor identified phases |
| 35–54 | Moderate deviation | Systematic proportionality breakdown; value capture likely |
| 0–34 | Severe deviation | Chain-wide incoherence; market price structurally divorced from True Value |

### 5.3 Composite TVPCI

| TVPCI | Label | Pricing Interpretation |
|---|---|---|
| 90–100 | **Structurally Coherent** | Market price and True Value structurally aligned; convergence expected |
| 75–89 | **Near Convergence** | Minor structural friction; small but measurable price divergence |
| 55–74 | **Moderate Divergence** | Identifiable phases distorting price; True Value partially obscured |
| 35–54 | **Significant Divergence** | Structural price distortion; financial analysis will overstate or understate value |
| 0–34 | **Critical Divergence** | Market price does not reflect physical chain conditions; True Value inaccessible from price alone |

---

## 6. Phase-Level TVPCI Contribution

Each phase's contribution to the overall TVPCI can be decomposed to identify which phases are suppressing chain-wide convergence. The **phase TVPCI contribution** is:

$$\text{TVPCI}_i = \frac{w_B \cdot B_i + w_S \cdot S_{i,\text{norm}}}{P} + \frac{w_\Phi \cdot (\Phi_{i-1 \to i} + \Phi_{i \to i+1})}{2(P-1)}$$

(Boundary terms use single-side values for terminal phases.)

This decomposition supports the **bottleneck identification** use case: the phase with the lowest \(\text{TVPCI}_i\) is the point where structural intervention would produce the largest gain in chain-wide convergence.

---

## 7. Commodity Profiles

### 7.1 Gold (Phases 0–7)

**Known structural characteristics:**

- Phase 6 (Vaulting) is the system's weakest phase: high D (security, compliance), low C (vault network, transport flexibility), balance target 0.50.
- Phase 7 (COMEX registration) is the most transparent: regulatory framework enforces balance, balance target 0.85.
- The Phase 5→6 and Phase 6→7 boundaries are the most likely to show sub-φ ratios, indicating value suppression at the custody/exchange interface.

**Gold weight profile (proposed):**

| Sub-score | Weight | Justification |
|---|---|---|
| \(\bar{B}\) | 0.45 | Phase 6 bottleneck dominates gold chain health |
| \(\bar{\Phi}\) | 0.35 | Boundary distortion is measurable but secondary to balance |
| \(\bar{S}_{\text{norm}}\) | 0.20 | Standard |

**Reference N-values (from `phi_engine.py`):**

| Phase | Name | N |
|---|---|---|
| 0 | Prospecting | 183 |
| 1 | Mining | 259 |
| 2 | Processing | 263 |
| 3 | Doré | 229 |
| 4 | Refining | 253 |
| 5 | Casting | 237 |
| 6 | Vaulting | **118** |
| 7 | Exchange | 239 |

The Phase 5→6 boundary ratio is \(118/237 = 0.498\) — far below \(\varphi\), confirming structural suppression at the vaulting interface. This is the primary driver of gold TVPCI deviation.

### 7.2 Shea Butter (Phases 0–6)

**Known structural characteristics:**

- Phase 0 (Collection by women's cooperatives) is characterised by very low C (market access, price information, organisational capacity) relative to D (quality standards, buyer specifications).
- Phase 3 (Processing/Refining) represents a 16× value amplification (\$250/mt → \$4,000/mt), which is approximately \(\varphi^{6.6}\) steps — far above proportional.
- Phase 4 (Export) shows an N-value collapse (158), creating a boundary ratio of \(158/241 = 0.66\) — suppressed, consistent with export intermediary extraction.
- The CLEO retail mechanism (1 EUR/100g returned to cooperatives) is a direct structural intervention to correct Phase 0 C-parameters. Its effect should be measurable as an increase in \(B_0\) and a corresponding improvement in the Phase 0→1 boundary φ-score.

**Shea weight profile (proposed):**

| Sub-score | Weight | Justification |
|---|---|---|
| \(\bar{B}\) | 0.35 | Balance is structurally important but Phase 0 is a known weak point |
| \(\bar{\Phi}\) | 0.45 | Value amplification ratios are the key diagnostic in shea |
| \(\bar{S}_{\text{norm}}\) | 0.20 | Standard |

**Reference N-values and value data (from `phi_engine.py`):**

| Phase | Name | N | Value (USD/mt) |
|---|---|---|---|
| 0 | Collection | 178 | — |
| 1 | First Sale | 192 | 150 |
| 2 | Trading/Bulking | 218 | 250 |
| 3 | Processing | 241 | 4,000 |
| 4 | Export | **158** | — |
| 5 | Manufacturing | 234 | — |
| 6 | Retail | 237 | 47,500 |

The overall retail-to-farmgate value ratio is \(47,500/150 = 317\times\), equivalent to \(\approx 12\) φ-steps. A structurally coherent chain would distribute this amplification proportionally across phases. The TVPCI measures how far the actual distribution deviates from that ideal.

---

## 8. Relationship to True Value Price

The TVPCI does not produce a price. It produces the structural condition under which a price can be interpreted. The relationship is:

$$P_{\text{market}} = P_{\text{true}} \cdot \left(1 + \delta_{\text{structural}}\right)$$

Where \(\delta_{\text{structural}}\) is a signed divergence term. The TVPCI provides the magnitude of \(|\delta_{\text{structural}}|\) in structural terms:

$$|\delta_{\text{structural}}| \propto \left(1 - \frac{\text{TVPCI}}{100}\right)$$

**A TVPCI of 80 does not mean the market price is 20% wrong.** It means that 20 structural index points of friction, imbalance, and incoherence exist within the chain — and that any price formed in that chain carries a structurally unexplained component of that magnitude. Whether that component manifests as overpricing, underpricing, or redistribution between chain participants is a question for Layer 4 (True Value Pricing) and Layer 5 analysis.

---

## 9. Data Requirements

### 9.1 Minimum Required Inputs (per phase)

| Field | Source | Notes |
|---|---|---|
| `phase_id` | Schema | Integer, matches supply chain phase |
| `D_total` | CGN engine | Sum of constraint parameters (0–100 each) |
| `C_total` | CGN engine | Sum of integration parameters (0–100 each) |
| `N` | CGN engine | Calculated: \(\sqrt{D \cdot C} \cdot B/100\) |
| `balance_score` | CGN engine | 0–100 |
| `sustainability_index` | CGN engine | \(100 / (|D-C|^2 + 10)\) |
| `data_quality` | Manual flag | `"HIGH"`, `"MEDIUM"`, `"LOW"`, or `"OPAQUE"` |

### 9.2 Optional Enrichment Inputs

| Field | Source | Effect on TVPCI |
|---|---|---|
| `value_usd_per_mt` | Value chain data | Enables value amplification cross-check against φ-expectation |
| `transparency_class` | Phase assessment | Refines opacity correction factor |
| `period_type` | Time series | Enables TVPCI trend analysis (quarterly / annual) |

### 9.3 Opacity Handling

Missing or opaque phase data is **never interpolated**. Opaque phases contribute the chain mean to sub-score aggregation, subject to the opacity correction factor in Section 4.2. The count and identity of opaque phases are always reported alongside the TVPCI score. Opacity is a finding — a structurally informative result, not an error to be suppressed.

---

## 10. Output Schema

```json
{
  "commodity": "gold | shea",
  "period": "YYYY-QN | YYYY",
  "tvpci": 72.4,
  "tvpci_adjusted": 68.1,
  "label": "Moderate Divergence",
  "sub_scores": {
    "phase_balance": 74.2,
    "boundary_coherence": 68.6,
    "phase_sustainability_norm": 76.1
  },
  "weights": {
    "phase_balance": 0.45,
    "boundary_coherence": 0.35,
    "phase_sustainability_norm": 0.20
  },
  "opacity": {
    "opaque_phases": [0],
    "opaque_count": 1,
    "total_phases": 8,
    "correction_factor": 0.944
  },
  "bottleneck": {
    "phase_id": 6,
    "phase_name": "Vaulting",
    "phase_tvpci_contribution": 31.2,
    "diagnosis": "D-dominant: security/compliance constraints far exceed vault network integration"
  },
  "boundary_worst": {
    "boundary": "P5→P6",
    "ratio": 0.498,
    "phi_score": 12.4,
    "status": "suppressed"
  },
  "metadata": {
    "framework_version": "1.0",
    "generated_at": "ISO 8601 timestamp",
    "phi_constant": 1.61803,
    "e_base": 10.0
  }
}
```

---

## 11. Implementation Notes

### 11.1 Existing Code Mapping

| TVPCI Component | Implemented in |
|---|---|
| D/C/N/B/S per phase | `src/simulation/tholonic_engine.py` — `Tholon._calculate_n_state()` |
| Boundary φ-scores | `src/simulation/phi_engine.py` — `compute_phi_boundaries()` |
| System φ-coherence | `src/simulation/phi_engine.py` — `system_phi_coherence()` |
| Phase CGN data (gold) | `data/value_chain/processed/value_ndc_phase{0-8}_summary.json` |
| Phase CGN metrics | `data/value_chain/processed/value_ndc_metrics.json` |

The TVPCI composite formula (Section 4) requires a thin aggregation layer over the existing engines. The sub-scores are already computed; only the weighted combination and opacity correction are new.

### 11.2 Balance Score Formula

The balance score uses the **exponential form** throughout the codebase:

$$B = 100 \cdot \exp\!\left(-2 \cdot \frac{|D-C|}{\max(D,C)}\right)$$

This is consistent with the φ-score decay function in `src/simulation/phi_engine.py` and implemented in both `src/simulation/tholonic_engine.py` and `src/simulation/balance_optimizer.py`.

---

## 12. Revision History

| Version | Date | Notes |
|---|---|---|
| 1.0 | 2026-04-14 | Initial specification — grounded in existing C-G-N and φ engines |
| 1.1 | 2026-04-16 | Section 3.2 — added mathematical justification for φ-benchmark via Fibonacci propagation of D and C parameters |

---

*This document is a technical specification. It describes a structural index that precedes financial analysis. All pricing interpretation derived from the TVPCI belongs to the Value Chain (Layer 4) analytical layer and must not be introduced into supply chain phase analysis.*
