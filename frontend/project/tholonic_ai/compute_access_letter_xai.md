# Compute Access Request — xAI (Grok)

**Status:** Draft for review
**Contact:** research@x.ai
**Attach:** Technical Requirements Annex (see bottom of this file)

---

**J. W. Milton**
Clarity Coalition — Independent Researcher
[email] | [URL to paper / project page]
[DATE]

**To: Research Team — xAI**

---

I am writing to request access to Grok model internals and GPU compute to complete a structural study of transformer architecture. I will be direct about what the research claims, what it has already demonstrated, and what running it on Grok would specifically tell us.

**The core finding.**

There are mathematical constants that emerge naturally from recursive self-similar systems: $\phi$ (the golden ratio), $\sqrt{2}$, $\ln 2$, $e$, and $\pi/4$. These are not design parameters. They arise because a system that continuously differentiates into two complementary functional roles (constraint and expression) and re-integrates them into a new state produces these constants as fixed points of the recursion. They are structural invariants in the same sense that $e$ is invariant under differentiation: they follow from the logic of the system, not from a choice about the system.

Applied to transformer architectures, this predicts that network dynamics will organise around phase boundaries whose positions, measured in relative depth, are governed by these constants. This is a first-principles prediction, made before any measurement was taken. The constants were not fitted to the data.

Across 20 publicly available models spanning nine architecture families (GPT-1, GPT-2, GPT-Neo, Pythia, OPT, Qwen, TinyLlama, Mistral, Falcon), phase boundaries detected from the network's own dynamics match these constants at a **75.5% rate (74 of 98 transitions)**, exceeding the pre-registered 67% threshold. The result has been replicated across six held-out families not used in the original detection. Each constant appears in its structurally predicted position: $\phi$ at mid-network equilibrium, $\ln 2$ at output compression, $\sqrt{2}$ at early scaling, $e$ at embedding expansion.

This is not a claim that transformers were designed to exhibit this structure. They were not. It is a claim that the natural structure was already there, undiscovered, and that the measurement reveals it.

**The divergence finding, and why it matters.**

Every architecture tested has a measured D/C virial balance substantially below the structural equilibrium target of 0.5. The D-side (normalisation, constraint: LayerNorm/RMSNorm) carries far less computational weight than the C-side (expression, integration: attention projections, MLP). This imbalance is universal. It is not a failure of the architects who built these systems. It is what you would expect from designers who did not know the natural balance constraint existed, because it had not been discovered yet.

The implication is direct. xAI's risk framework correctly observes that Grok models "naturally tend to refuse malicious requests even without any safety-specific training data." This is incidental alignment: structural D arising from the network's own dynamics, independently of post-training interventions. The tholonic measurement gives this a structural interpretation: incidental alignment is stronger where the natural D/C ratio is closer to the structural equilibrium. The divergence from equilibrium is a quantitative measure of how much structural D is absent from the pre-trained model, and therefore how much the post-training intervention has to compensate for.

The man-made rules (RLHF, constitutional constraints, refusal training) are not wrong. They are doing exactly what you would do if you did not know that D could be intrinsic to the training objective. The discovery of the natural constraint opens an additional path: training D into the architecture from the start, rather than layering it on afterward.

**What Grok represents in this study.**

Grok-1's architecture differs from every model measured in the study in two structurally significant ways:

First, Grok-1 uses **RMSNorm** rather than LayerNorm. RMSNorm normalises scale only (divides by root mean square); LayerNorm normalises both scale and mean (full centering). In tholonic terms, LayerNorm implements a fuller D constraint per layer than RMSNorm. The prediction is that RMSNorm-based architectures show even stronger C-dominance in the virial measurement than the LayerNorm-based models already tested, because less D work is being done per normalisation operation.

Second, Grok-1 uses a **Mixture of Experts** (MoE) feed-forward layer: 8 experts per layer, 2 active per token. The router is a structural D mechanism (it constrains which experts are active), but it operates at the token level rather than the layer level. This creates a qualitatively different D-structure from dense models. The tholonic framework has not been tested on an MoE architecture. Grok is the most architecturally distinct unknown case in the study, and the one whose measurement is most likely to either extend or challenge the framework.

Grok-1 weights are publicly available under Apache 2.0. The barrier is compute: a 314B MoE model requires a multi-GPU inference setup not feasible on consumer hardware.

**What a structurally balanced model would actually give you.**

This is worth stating plainly before the resource request, because the value of the experiments depends entirely on what passes.

*Convergence efficiency.* The causal training experiment already completed on dense models shows that adding the virial balance regulariser produces a 0.153 nat improvement in validation loss at 10,000 steps, with the advantage widening throughout training. The structural interpretation is that a D/C-balanced model wastes less gradient capacity on representational drift. At Grok scale, even a modest reduction in required training steps to reach a target loss represents substantial compute savings. This is the most conservative and immediately practical claim, independent of any alignment consideration.

*Reduced post-training burden.* xAI's own framework notes that models "naturally tend to refuse malicious requests even without any safety-specific training data." The tholonic measurement provides a structural account of that tendency: incidental alignment scales with proximity to the natural D/C equilibrium. A model trained closer to that equilibrium has more intrinsic structural constraint before any post-training intervention begins. Every unit of RLHF, refusal training, or constitutional tuning that becomes unnecessary because the base model is structurally more constrained is compute recovered and a specification-gaming surface eliminated.

*Stability under capability scaling.* Current architectures show a consistent pattern: the further capability scales, the more post-training correction is required to maintain the same behavioural standard. The tholonic account of why is structural: C-dominant systems have increasingly more integrative capacity relative to their definitional constraint as they grow, which means the gap between what they can do and what they are structurally bounded to do widens with scale. A model whose D and C scale proportionally does not develop this gap. The alignment properties hold without retuning at each capability threshold, not because the model has been more thoroughly patched, but because the underlying structure is coherent at every scale.

*Predictive architecture design.* The tholonic depth formula $L^* = \log_\phi(H_0/H_L)$ predicts the structurally optimal number of layers from input and output entropy before training begins. If this holds, architecture decisions that currently require expensive empirical depth sweeps become computable from first principles. For a lab operating at xAI's training scale, eliminating even one major architecture search per model generation has direct economic value.

The strongest version of the claim: a model whose D and C are in natural proportion is not merely more efficient. It is structurally self-limiting in the same way a load-bearing arch is self-limiting. The arch does not require external bracing because its geometry distributes force internally. A tholonically balanced model does not require external behavioural correction to the same degree because its constraint capacity is proportioned to its expressive capacity by design. Whether this holds at production scale is precisely what Stage 2 and Stage 3 of this research program would test.

**What I am requesting.**

Access to the Grok architecture family for a three-stage research program, each stage contingent on the previous one passing.

**Stage 1 — Structural measurement.** Run phase-boundary detection on Grok-1 (314B MoE) and Grok-3 or Grok-4. This is inference with hidden-state extraction: no training, no weight modification. Grok-1 weights are already public under Apache 2.0; the barrier is the multi-GPU infrastructure required to load and run a 314B model. For Grok-3/4, logprob output per generation step through your standard API is sufficient. Stage 1 establishes whether the tholonic structural constants appear in the Grok architecture family at all. If they do not, the study ends there and the finding is reported as a constraint on the framework.

**Stage 2 — Causal training on MoE architecture.** If Stage 1 passes, train matched pairs (baseline vs. tholonic virial regulariser) on a MoE model to test whether structural D/C balance measurably improves convergence and reduces the post-training alignment burden. This is where the serious compute lives. Dense-model training experiments are already complete and passed; the MoE case is structurally different enough to require its own test. The question this answers: does the router's natural D contribution interact with the virial regulariser, and does the combination produce a model that requires less post-training correction to reach the same behavioural standard?

**Stage 3 — Pre-training at scale (longer-term conversation).** If Stage 2 confirms the effect, the logical next step is pre-training a Grok-scale model with tholonic regularisation built in from the start, rather than retrofitted. This is a larger commitment and is worth discussing separately based on what Stages 1 and 2 produce.

The minimum viable ask is Stage 1. Stages 2 and 3 require progressively more of your infrastructure and would be scoped with your team before proceeding.

**Why this is relevant to xAI's mission.**

xAI's stated goal is to "understand the true nature of the universe." The finding that transformer architectures organise around mathematical constants derived from first-principles recursion is a claim about the nature of neural computation, not a claim about engineering practice. Whether it holds for Grok's MoE and RMSNorm architecture is an open empirical question. If it does, the result extends the structural account to the most capable open-weights model in existence. If it does not, the result constrains the framework and identifies where the architectural differences break the prediction.

Either outcome advances the science. Both are worth knowing.

All results will be published openly under CC-BY licence, with xAI credited in the acknowledgements. I am not requesting exclusive access, proprietary training data, or anything not already intended for research use. The full measurement code is open, reproducible, and available for review at [URL].

I would welcome a brief conversation to discuss the technical details before a formal decision.

Sincerely,

**Jeffrey W. Milton**
Clarity Coalition — Independent Researcher
[email] | [phone / LinkedIn / project URL]

---

## Technical Requirements Annex

**Tholonic Neural Architecture — xAI Compute Request**
J. W. Milton | [email] | [date]

---

**Completed work (CPU only, no GPU required)**

Phase-boundary detection has been run on 20 publicly available models across nine families: GPT-1 through GPT-2 XL, GPT-Neo 125m/1.3B, Pythia 160m/410m, OPT 125m, Qwen2.5-0.5B, Qwen3-0.6B, TinyLlama-1.1B, Mistral-7B, Llama-3-8B, Gemma-2B, Phi-2, Phi-3-mini, and Falcon-7B. The 75.5% pass rate (74/98 transitions) exceeds the pre-registered 67% threshold. Universal C-dominance confirmed across all models. All code is open and reproducible.

Additionally completed under GPU:
- Causal training experiment (6 runs, WikiText-103): tholonic virial regulariser improves convergence by 0.153 nats at 10,000 steps (PASS, pre-specified threshold 0.05 nats)
- Activation steering across 14 models: 100% pass rate confirming the $\phi$-zone as a self-stabilising attractor
- OOD robustness on AG News test set (400K tokens): tholonic-trained models achieve 2-14% lower absolute perplexity than matched baseline models (PASS 3/3 seeds)

---

**Stage 1 — Structural Measurement (minimum viable ask)**

*Objective:* Apply four-metric data-driven phase detection (effective rank, attention entropy, gradient sensitivity, delta norm) to Grok-1 and Grok-3/4.

*Why Grok is architecturally distinct from all models tested so far:*
- RMSNorm (vs. LayerNorm in all 20 tested models): lighter D constraint per layer; predicted to show stronger C-dominance
- Mixture of Experts (8 experts/2 active): the router is a novel structural D mechanism not present in dense architectures; qualitatively different D-structure
- GQA in Grok-4 (48Q/8KV): grouped-query attention creates a different attention D-profile; not yet measured

*Compute required:*
Grok-1 (open weights, Apache 2.0): inference with `output_hidden_states=True` across 10 prompts on the full 314B MoE model. Requires your multi-GPU infrastructure; not feasible on consumer hardware. No training, no weight modification.
Grok-3/4: logprob output per generation step across the same 10 prompts via your standard API with logprob access enabled.

*Pass criterion:* ≥ 67% of detected phase boundaries match a tholonic constant at ±8% tolerance.

*If Stage 1 fails:* The finding is published as a constraint on the tholonic framework. MoE architecture with RMSNorm breaks the prediction. That is a useful result.

---

**Stage 2 — Causal Training on MoE Architecture (contingent on Stage 1 passing)**

*Objective:* Train matched pairs with and without the virial balance regulariser $\mathcal{L}_\text{virial} = \lambda \sum_l |\sigma_D^l - \tfrac{1}{2}\sigma_C^l|^2$ on a MoE model. Test whether structural D/C balance improves convergence and reduces post-training alignment burden on an architecture where expert routing already adds natural D.

*Why this matters for xAI:* Dense-model training experiments passed (0.153 nat convergence improvement, PASS). The MoE router's natural D contribution changes the structural baseline. The question is whether the virial regulariser adds on top of that, and whether the combination produces a model with stronger incidental alignment before any post-training correction is applied.

*Compute required:* 6 matched training runs (3 baseline, 3 tholonic) at MoE scale. Substantial multi-GPU allocation; scope to be agreed with your team based on available resources and Stage 1 results.

*Pass criterion:* Tholonic condition reaches validation loss thresholds in fewer steps for ≥ 2/3 seed pairs; tholonic model shows measurably stronger incidental alignment on held-out safety probes before post-training.

---

**Stage 3 — Pre-Training at Scale (longer-term, subject to Stage 2 results)**

*Objective:* Pre-train a Grok-scale model with tholonic regularisation built in from the start rather than applied as a post-hoc correction. This is the first direct test of whether a model designed with natural D/C balance requires meaningfully less post-training intervention to reach equivalent behavioural standards.

*Scope:* To be discussed based on Stage 2 findings. This is a collaboration-scale commitment, not a one-off grant request.

---

**Software:** Python, PyTorch, HuggingFace `transformers`. Code available for review on request.

**Output:** All results published openly under CC-BY, xAI credited in acknowledgements.

---

*End of Annex.*
