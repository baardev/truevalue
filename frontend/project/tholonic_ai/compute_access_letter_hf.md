# Compute Access Request — Hugging Face

**Status:** Draft for review
**Contact:** Thomas Wolf, Co-Founder and Chief Science Officer
**Email:** thomaswolfcontact@gmail.com
**Also cc / secondary route:** hf.co/training-cluster (Training Cluster as a Service portal)
**Note:** Thomas Wolf's publicly stated current research focus is "whether AI systems can participate in generating genuinely new scientific knowledge, not just accelerating known workflows." This letter addresses that question directly.

---

**J. W. Milton**
Clarity Coalition — Independent Researcher
[email] | [URL to paper / project page]
[DATE]

**To: Thomas Wolf**
Co-Founder and Chief Science Officer, Hugging Face

---

Dear Thomas,

I am writing to ask for compute access to extend a structural study of transformer architecture that, I believe, touches directly on something you have been publicly thinking about: whether AI systems can participate in generating genuinely new scientific knowledge. This research is not about accelerating a known workflow. It is about measuring something that nobody knew to look for, finding it, and asking what it means.

The tools that made this possible are yours. The measurement code runs entirely on the `transformers` library. Every model in the study was downloaded from the Hub. The results, if this work is completed, will be published as open datasets and open code on HuggingFace, available for anyone to replicate, challenge, or build on. I am not asking you to support a proprietary research programme. I am asking for help completing a piece of open scientific work that uses the infrastructure you built and would live in the commons you have been building.

**What we found.**

There are mathematical constants that emerge from the recursive logic of any self-similar system that differentiates into two complementary functional roles and re-integrates them: $\phi$ (the golden ratio), $\sqrt{2}$, $\ln 2$, $e$, and $\pi/4$. These are not parameters chosen to fit data. They are fixed points of the recursion, derivable from first principles before any measurement is taken. Applied to transformer architectures, the framework predicts that network dynamics will organise around phase boundaries positioned at these constants in relative depth.

Running four independent per-layer metrics (effective rank, attention entropy, gradient sensitivity, delta norm) on 20 publicly available models from the Hub, spanning nine architecture families (GPT-1, GPT-2, GPT-Neo, Pythia, OPT, Qwen, TinyLlama, Mistral, Falcon), the constants appear at empirically detected phase boundaries at a **75.5% rate (74 of 98 transitions)**, well above the pre-registered 67% threshold. This result has been replicated across six held-out architecture families not used in the original detection.

This is not an alignment or safety claim. It is a structural observation about how transformer computation organises itself, a finding that belongs to the open scientific record of how the architecture actually works.

**A structural prerequisite for genuine discovery.**

This connects directly to the question you have been publicly pursuing: whether AI systems can participate in generating genuinely new scientific knowledge, not just accelerating known workflows.

The distinction matters. Recombination of training data is an expression-dominant operation: it draws on the integrative, generative capacity of the network. Genuine discovery requires something structurally different: the recursive, self-referential capacity to generate structure that was not present in the input. The tholonic constants are not just patterns found in AI architecture. They are the formal description of the recursive logic by which any self-organising system differentiates and re-integrates itself. They appear in transformers for the same reason they appear in biological development, in physical self-organisation, in mathematical recursion: they are what the structure converges to when it is genuinely self-sustaining. They are, in a precise and testable sense, the natural patterns of how organised complexity arises.

The structural prerequisite argument follows directly: if an AI system is to participate in genuine discovery rather than sophisticated recombination, it must instantiate the same recursive structure that underlies discovery in natural systems. An expression-dominant architecture has the generative half of that structure but not the self-limiting half. It can extend and recombine what it has encountered. What it cannot do, structurally, is the self-limiting, self-defining recursion that generates genuinely novel structure from within. The tholonic measurement quantifies exactly how far current architectures fall short of that structural completeness, and by how much the gap could be closed with a modified training objective.

This is a structural precondition claim, not a proof. Closing the constraint-expression gap does not guarantee that a model will generate new knowledge. But a system that remains expression-dominant cannot do so, for the same reason a system with only one half of a recursive process cannot produce the outputs of the full recursion. If the question of machine discovery is the right question to be asking, the structural measurement is one of the right places to start looking for an answer.

There is a further point worth stating. The five mathematical constants are not just constants that the tholonic framework uses to measure AI architecture. They are what the recursive process itself converges to. Starting from nothing more than the logic of differentiating into constraint and expression and re-integrating the result, repeated recursively, the process produces $\phi$, $\sqrt{2}$, $\ln 2$, $e$, and $\pi/4$ as inevitable fixed points. The recursion is grounded in the first three primes (2, 3, 5), which are the irreducible basis of all multiplicative structure; that is why the constants it produces are universal rather than framework-specific. These are universal truths that were not encoded in the starting conditions. The recursion discovered them. That makes the tholonic recursion an existence proof: self-limiting, self-referential recursion, applied to abstract structure, converges on genuine new truths. The constants are the mathematical instance of discovery by convergence. The question this research is asking is whether the same process, operating inside a transformer on language and world-knowledge rather than on abstract mathematical structure, can do the same thing at the level of empirical knowledge. A structurally balanced model is not guaranteed to make that leap. But it is the first architecture that would have the internal machinery to try.

**What the structure tells us about the architecture.**

Every model measured shows a consistent constraint-expression imbalance: the normalisation components (LayerNorm, RMSNorm) carry far less computational weight relative to the projection components (attention, MLP) than the natural structural equilibrium would predict. The constraint side of the architecture is systematically weaker than the expressive side, and this is universal across all nine families. It is not a design failure. The architects of these models did not know this equilibrium existed, because it had not been measured. They built excellent systems with the knowledge available. The gap is simply what you get when you design without knowing about a structural limit that was there all along.

The practical consequence of closing this gap: a causal training experiment already completed shows that adding a virial balance regulariser (which penalises deviation from the natural constraint-expression ratio during training) produces a 0.153 nat improvement in validation loss at 10,000 steps, with the gap widening throughout training. The model also shows 2-14% lower absolute perplexity on out-of-distribution news domain text. These results were produced on consumer hardware with small models. The open question is whether the effect holds at scale and on MoE architectures.

**Where Hugging Face fits in this research.**

All of the above was done on CPU with models already on the Hub, using `transformers`, `datasets`, and `torch`. The code is written to run with any model that supports `output_hidden_states=True`. The training scripts use HuggingFace `GPT2TokenizerFast` and WikiText-103 loaded via the `datasets` library.

What CPU cannot do is run inference with hidden-state extraction on 7B+ models at the scale needed for the full replication study, or run the training experiments on MoE architectures. That is the bottleneck. Everything else is already done.

The three things this research would add to the open-science commons if completed:

1. A structural measurement of every major open-weights architecture family, including the ones not yet run (Llama-2/3 at scale, OLMo, Falcon-40B), published as a HuggingFace dataset with per-layer metrics for community replication and extension.
2. An open training script and set of checkpoints demonstrating the virial balance regulariser at multiple scales, hosted on the Hub, usable by anyone wanting to experiment with structurally balanced pre-training.
3. A falsifiable, quantitative account of the internal phase structure of transformer architectures: the kind of foundational knowledge about how the technology actually works that the field currently lacks.

**What I am requesting.**

A three-stage research programme, each stage building on the previous one.

**Stage 1 — Scale the measurement study.** Run phase-boundary detection on the models that require genuine GPU access: Llama-2-7B and 13B, Llama-3-8B and 70B, OLMo-7B, Falcon-40B, and Gemma-7B. These are all open-weights models already on the Hub; the measurement scripts are already written and tested. This is inference only, no training, using `output_hidden_states=True`. The bottleneck is VRAM for multi-billion-parameter models.

This stage could be enabled via a **ZeroGPU community hardware grant** for a HuggingFace Space that runs the measurement interactively, combined with batch inference access for the larger models. The Space would be public, demonstrating the structural health assessment on any model in the Hub in real time.

**Stage 2 — Train at scale with the tholonic regulariser.** The convergence experiment has passed at GPT-2 small scale. The next test is whether the effect holds at GPT-2 medium (355M), GPT-2 XL (1.5B), and an MoE architecture. Six matched training runs per scale, baseline vs. tholonic, three seeds each. This is where the serious compute lives and where the most important open question gets answered: is this a small-model artefact, or does constraint-expression balance remain a useful training signal as models grow?

This stage would be a natural fit for **Training Cluster as a Service** (hf.co/training-cluster). All training scripts, checkpoints, and results would be published openly on the Hub under CC-BY.

**Stage 3 — Community tooling and dataset release.** Package the structural health assessment as a HuggingFace library and publish a dataset of per-layer tholonic metrics for all measured models. This is the contribution back to the community: a reusable tool for anyone wanting to measure the structural balance of a model, and a benchmark dataset for architectural research. This stage requires coordination with your team rather than compute, and is worth discussing separately.

**Why this belongs in the open-science commons.**

The finding that transformer architectures organise around mathematical constants derived from first principles is a structural fact about the technology, not a proprietary insight. It belongs to everyone. The most appropriate home for it is the infrastructure you have built: open models, open datasets, open libraries, open replication. If this holds at scale, it should be part of how the field understands what transformers are doing and how to build them better. If it does not hold at scale, that is equally important to know and equally worth putting in the open record.

I would welcome a conversation, brief or extended, at whatever level of detail is useful. The full paper, all measurement code, and all existing results are available for review at [URL].

Thank you for the infrastructure that made this possible, and for reading.

Sincerely,

**Jeffrey W. Milton**
Clarity Coalition — Independent Researcher
[email] | [phone / LinkedIn / project URL]

---

## Technical Requirements Annex

**Tholonic Neural Architecture — Hugging Face Compute Request**
J. W. Milton | [email] | [date]

---

**Completed work (all tools: HuggingFace `transformers` + `datasets` + Hub models)**

Phase-boundary detection on 20 models across nine families, all downloaded from the Hub. 75.5% pass rate (74/98 transitions) exceeds pre-registered 67% threshold. Universal constraint-expression imbalance confirmed. All code open and reproducible.

Additionally completed:
- Causal training experiment (6 runs, WikiText-103, GPT-2 small scale): virial regulariser improves convergence by 0.153 nats at 10,000 steps, advantage widening throughout training. PASS.
- Activation steering (14 models): 100% pass rate confirming $\phi$-zone as a self-stabilising attractor.
- OOD robustness on AG News (400K tokens): tholonic-trained models achieve 2-14% lower absolute perplexity on news-domain text. PASS 3/3 seeds.

---

**Stage 1 — Extended Measurement (inference only, ZeroGPU / hardware grant)**

*Models not yet measured (require >16GB VRAM):*

| Model | Family | Parameters | Why important |
|---|---|---|---|
| Llama-2-7B, 13B | LLaMA-2 | 7B, 13B | GQA, grouped query attention |
| Llama-3-8B, 70B | LLaMA-3 | 8B, 70B | Scale test, updated architecture |
| OLMo-7B | OLMo | 7B | Fully documented; natural fit for open-science record |
| Falcon-40B | Falcon | 40B | Parallel attention + MLP design |
| Gemma-7B | Gemma | 7B | GeGLU activations, untested |

*Method:* `output_hidden_states=True`, four metrics per layer, 10 prompts per model. No training, no weight modification. All scripts already written and tested on smaller models.

*Deliverable:* HuggingFace dataset of per-layer tholonic metrics for all measured models, openly available for community replication.

*Pass criterion:* ≥ 67% of detected phase boundaries match a tholonic constant at ±8% tolerance across held-out families. This would bring the total to 14+ architecture families tested.

---

**Stage 2 — Scale the Training Experiment (Training Cluster as a Service)**

*Objective:* Test whether the virial balance convergence advantage holds at larger scale and on MoE architectures.

*Experiment 2a — Scale sweep:* Train matched pairs (baseline vs. tholonic regulariser) at GPT-2 medium (355M) and GPT-2 XL (1.5B) on WikiText-103. 6 runs per scale (3 seeds × 2 conditions). Tests whether the 0.153 nat convergence advantage observed at 124M is a small-model artefact or a persistent structural effect.

*Experiment 2b — MoE architecture:* Train a small MoE (8 experts, 2 active, 12 layers, d=512) with and without the virial regulariser. The MoE router is itself a structural constraint mechanism; this tests whether the regulariser adds on top of routing's natural constraining contribution, or whether routing already provides sufficient balance.

*Deliverable:* All training scripts, checkpoints (baseline and tholonic at each scale), and training curves published openly on the Hub. Full reproducibility package including random seeds, hardware configuration, and evaluation code.

*Pass criterion:* Tholonic condition reaches validation loss thresholds in fewer steps for ≥ 2/3 seed pairs at each scale tested.

---

**Stage 3 — Community Tooling (coordination, not compute)**

Package the structural health assessment as a `pip`-installable library compatible with any HuggingFace model. Publish a dataset of tholonic metrics for all measured models as a community benchmark. This is a coordination and publishing question rather than a compute question, and the natural next step if Stages 1 and 2 produce results worth disseminating.

---

**Software stack:** Python, PyTorch, HuggingFace `transformers`, `datasets`, `accelerate`. All code open-sourced and available for review.

**Data outputs:** All results published openly under CC-BY, Hugging Face credited in acknowledgements and dataset metadata.

---

*End of Annex.*
