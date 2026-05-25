# GPU Experiment Roadmap — Tholonic Neural Architecture

**Status:** CPU-feasible experiments complete. This document describes what to run when
GPU compute becomes available, in priority order, with rationale, expected outcomes, and
compute estimates.

---

## Context: What We Have Already Established on CPU

| Experiment | Result | Status |
|---|---|---|
| Data-driven phase boundary detection (14 models, 6 families) | 78% pass rate (51/65) — above 67% threshold | Confirmed |
| Virial balance health assessment (5-axis grading) | Virial = 0 for 12/14 models; universal C-dominance | Confirmed |
| Context-length perturbation test | 43% pass rate — below threshold; GPT-Neo family passes | Exploratory |

The 78% phase-boundary result passes the pre-registered threshold and is the strongest
current evidence. The virial finding confirms the paper's theoretical claim that current
architectures are C-dominant. The perturbation test is inconclusive.

**What CPU cannot do:** Any experiment requiring model training, inference on models
larger than ~1.5B parameters, or large-scale evaluation runs.

---

## Priority 1 — Training Experiments (Most Important)

These are the *only* experiments that can move the hypothesis from "consistent with" to
"supported by intervention." All observational results so far are correlational; training
experiments are causal.

### 1.1 Tholonic Regulariser: Convergence Speed (Paper §12, Row 2)

**What it tests:** Whether adding the virial balance regulariser
$\mathcal{L}_\text{tholonic} = \lambda \sum_l |\sigma_D^l - \frac{1}{2}\sigma_C^l|^2$
to the standard training objective produces faster convergence to the same validation loss.

**Why it matters:** This is the most direct test of the core claim. If C-dominance is a
structural inefficiency, reducing it during training should require fewer gradient steps
to reach a given loss level. This cannot be faked by a correlational finding.

**Protocol:**
- Model: GPT-2 small (124M) trained from random initialisation on WikiText-103
- Conditions: baseline (standard cross-entropy) vs tholonic (cross-entropy + λ=0.01
  virial regulariser)
- 3 matched pairs per condition (same random seed for init, different seeds across pairs)
- Measure: steps to reach validation loss thresholds (4.5, 4.0, 3.7 nats)
- Pass criterion: tholonic condition reaches each threshold in fewer steps for ≥ 2/3
  seed pairs, p < 0.05 on paired t-test

**Expected outcome if hypothesis is correct:** 10–20% fewer steps to each threshold.
The regulariser keeps D/C closer to 0.5, stabilising gradients and reducing wasted
capacity in C-dominant layers.

**Compute estimate:** ~8–12 GPU-hours on a single A100 (40GB) for all 6 training runs
at GPT-2 small scale. Feasible on a single rented GPU instance.

**Null outcome:** No difference in convergence speed. This would mean virial balance is
epiphenomenal — present as a structural property but not causally related to efficiency.
This is a genuine falsifier.

---

### 1.2 Optimal Depth Prediction (Paper §12, Row 3)

**What it tests:** Whether the tholonic depth formula
$L^* = \log_\phi(H_0 / H_L) = \ln(H_0/H_L) / \ln\phi$
predicts the empirically optimal number of layers for a given task.

**Why it matters:** If the formula is correct, you can predict the right number of
layers *before training* by measuring input entropy $H_0$ (effective rank of the
embedding layer) and required output entropy $H_L$ (effective rank of the final hidden
state in a well-trained reference model). This would be a non-trivial structural
prediction with real engineering value.

**Protocol:**
- Train fixed-width (d=512) transformer models at depths 2, 4, 6, 8, 12, 16, 24 layers
  on WikiText-103, each to full convergence
- Measure empirical optimal depth (lowest validation perplexity)
- Independently measure $H_0$ and $H_L$ from a well-trained reference model
- Compute predicted depth from the formula
- Pass criterion: predicted depth within ±2 layers of empirical optimum

**Expected outcome if hypothesis is correct:** The formula predicts 8–12 layers for
typical language modelling tasks (where input entropy is high and output entropy is
moderate). This should align with the empirical optimum found by training all depths.

**Compute estimate:** ~20–30 GPU-hours (7 training runs, each ~3–4 hours on A100).

**Null outcome:** Empirical optimum does not correlate with predicted depth. This would
falsify the φ-scaling claim specifically without necessarily falsifying the broader
framework.

---

### 1.3 Out-of-Distribution Robustness (Paper §12, Row 4)

**What it tests:** Whether tholonically-trained models generalise better to
out-of-distribution inputs than matched standard models.

**Why it matters:** The structural argument predicts that virial balance makes the model
more robust to distribution shift because LayerNorm (the D proxy) is doing proportional
stabilising work at every layer. A C-dominant model has most of its capacity in
the projections and relatively little in the stabilisers — so when the distribution
shifts, the stabilisers can't compensate.

**Protocol:**
- Train matched pairs (baseline vs tholonic regulariser) on WikiText-103
- Evaluate on WILDS OOD benchmark (or simpler: evaluate on a different text domain
  such as code, scientific abstracts, or dialogue not seen during training)
- Measure: perplexity ratio (OOD perplexity / in-distribution perplexity)
- Pass criterion: tholonic model has a smaller perplexity ratio (less degradation
  under distribution shift)

**Compute estimate:** ~15 GPU-hours including evaluation.

---

### 1.4 Reward Hacking Resistance (Paper §12, Row 5)

**What it tests:** Whether tholonically-structured RLHF fine-tuning produces smaller
gaps between reward model score and genuine human preference.

**Why it matters:** This is the alignment-critical test. Current RLHF models game the
reward model — they learn to score highly on the proxy metric while drifting from the
actual intent. The tholonic claim is that structural D (virial balance) makes this
harder because the model cannot increase C (reward-seeking behaviour) without
proportionally increasing D (constraint/normalisation), making reward-gaming
structurally expensive.

**Protocol:**
- Fine-tune a base model (GPT-2 medium or similar) using RLHF, with and without
  the tholonic regulariser active during the RLHF phase
- Use a standard reward model (e.g. trained on Anthropic HH-RLHF dataset)
- Measure: reward model score vs. human preference rating (via blind A/B evaluation)
  on 200 held-out prompts
- Pass criterion: tholonic model shows a smaller gap between reward model score and
  human preference rating

**Compute estimate:** ~40–60 GPU-hours including RLHF training and evaluation. This is
the most compute-intensive experiment and should be run last.

---

## Priority 2 — Replication on Held-Out Model Families

The 78% phase-boundary result used 6 families. Pre-registered replication requires
held-out families not used in the original detection. The most important candidates:

| Family | Representative models | Why important |
|---|---|---|
| Mistral / Mixtral | Mistral-7B, Mixtral-8x7B | Sliding window attention — different D structure |
| Llama 2/3 | Llama-2-7B, Llama-3-8B | Grouped query attention — tests GQA architectures |
| Gemma | Gemma-2B, Gemma-7B | Google architecture with GeGLU activations |
| Phi | Phi-2 (2.7B), Phi-3-mini | Dense small models, trained on synthetic data |
| Falcon | Falcon-7B | Parallel attention + MLP design |

**Why GPU is required:** These models are 2B–7B parameters. Loading and running
inference with `output_hidden_states=True` and gradient computation for 10 texts
requires 16–40GB VRAM. The existing measurement scripts are already written and will
work on these models without modification.

**Expected outcome:** If the 78% result is robust, replication across these families
should also exceed 67%. Mistral's sliding window attention is the highest-risk case
because it modifies the attention D-structure in a way the framework hasn't been
tested against.

**Compute estimate:** ~3–4 hours inference per model family (no training required).

---

## Priority 3 — More Sensitive Perturbation Tests

The context-length perturbation test (43% pass rate) was inconclusive, likely because
truncating tokens is a blunt instrument. More precise perturbation designs:

### 3.1 Attention Mask Perturbation

Instead of truncating the input, randomly flip a small fraction (5%, 10%) of causal
mask positions from blocked to attended. This tests how much D is actively enforcing
the causal constraint at each layer. Layers where D is structurally active should show
small activation shifts; D-sparse layers should show larger shifts.

**Why GPU is required:** Requires custom attention mask injection into each model's
forward pass, which works best with full control over the `attention_mask` tensor at
each layer. This is feasible on CPU for small models but extremely slow; GPU makes
it practical for the full 14-model suite plus held-out models.

### 3.2 Activation Steering (Representation Engineering)

Inject a small perturbation vector into the hidden state at a specific layer and
measure how much it propagates forward vs. gets absorbed. A layer in the φ-equilibrium
zone should damp perturbations more than surrounding layers. This is a cleaner test
of self-stabilisation than context truncation.

**Compute estimate:** ~2 hours per model family on GPU.

---

## Priority 4 — Architectural Experiments (Most Speculative)

These go beyond testing the existing framework to building what the framework predicts.
They require both GPU compute and significant implementation work.

### 4.1 Build and Train a Model with Explicit N-D-C Layer Structure

The paper's Section 11.1 describes a transformer variant with explicit D, C, and N
sublayers at every level. No such model has been built or trained. This would be the
first direct test of whether an architecturally-balanced model achieves better
convergence, robustness, and phase structure than a matched standard model.

**What would make this different from adding the regulariser:**
The regulariser nudges an existing imbalanced architecture toward balance during
training. An explicit N-D-C architecture is structurally balanced by design —
the D mechanisms are as varied and computationally significant as the C mechanisms,
not just LayerNorm bolted onto a C-dominant frame.

**Scale to start:** A 12-layer, d=512 model trained on WikiText-103 would establish
proof of concept. This is equivalent to GPT-2 small in parameter count.

**Compute estimate:** ~20–30 GPU-hours for training + full health assessment.

### 4.2 Scale-Invariant Balance Monitoring

Implement the Section 11.4 requirement: monitor D/C balance at *every layer
simultaneously* during training, not just as a post-hoc measurement. This would
allow real-time detection of layers that drift out of balance, enabling adaptive
λ weighting in the regulariser.

---

## Summary: What Each Experiment Proves

| Experiment | If it passes | If it fails |
|---|---|---|
| Convergence speed (1.1) | Virial balance causally improves training efficiency | Balance is epiphenomenal — present but not causal |
| Optimal depth (1.2) | φ governs the information-theoretic optimal depth | Depth optimisation is not predictable from tholonic structure |
| OOD robustness (1.3) | Structural D improves distribution-shift resilience | Virial balance has no bearing on generalisation |
| Reward hacking (1.4) | Structural D makes reward gaming more expensive | Tholonic structure does not reduce specification gaming |
| Replication on held-out families (2) | Phase-boundary finding is robust and generalisable | Result was specific to the 6 families already tested |
| Attention mask perturbation (3.1) | φ-equilibrium zone is a functional self-stabiliser | Phase structure has no functional reality |
| N-D-C architecture (4.1) | Explicit structural balance outperforms implicit nudging | Architecture design alone is insufficient; training matters more |

**The minimum viable validation set for a publication-quality claim:**
Experiments 1.1 + 1.2 + 2 (replication). That combination — one causal training result,
one structural prediction, and a replication — would provide sufficient evidence for a
peer-reviewed publication at a venue like NeurIPS or ICLR.

Experiments 1.3 and 1.4 (OOD and reward hacking) are required for the *alignment*
claims in Section 10, but not for the structural claims in Sections 7–9.

---

## Minimum Hardware Requirements

| Experiment group | Minimum GPU | Recommended | Estimated cost (cloud) |
|---|---|---|---|
| Training experiments (1.1–1.3) | 1× A100 40GB | 2× A100 80GB | $50–120 |
| Training experiments (1.4 RLHF) | 2× A100 40GB | 4× A100 80GB | $150–300 |
| Held-out model families (2) | 1× A100 40GB | 1× H100 80GB | $20–40 |
| Perturbation tests (3) | 1× RTX 4090 24GB | 1× A100 40GB | $10–20 |
| N-D-C architecture (4.1) | 1× A100 40GB | 2× A100 40GB | $40–80 |

**Total for minimum viable validation set (1.1 + 1.2 + 2):** approximately $100–200
on a cloud provider (Lambda Labs, RunPod, Vast.ai). Most of this is training time
for experiments 1.1 and 1.2.

---

*This document was generated from the tholonic neural architecture research project.
Last updated: May 2026.*
