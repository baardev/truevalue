# Research Compute Access — Letter Templates and Guide

**Purpose:** Request access to GPU compute and/or frontier model internals from AI companies for the purpose of replicating and extending the tholonic neural architecture research. This document contains a master template letter, company-specific notes, and a technical requirements annex to attach with each submission.

---

## Who to Contact and Where

| Company | Programme | URL |
|---|---|---|
| Anthropic | Researcher Access Programme | anthropic.com/research |
| OpenAI | Researcher Access / API credits | openai.com/research/overview |
| Google DeepMind | Academic Partnerships | deepmind.google/research/collaborations |
| Meta AI | Research partnership / LLaMA access | ai.meta.com/research |
| xAI | Research inquiries | x.ai |
| Mistral AI | Research collaboration | mistral.ai/research |
| AI2 / Allen Institute | Open research partnership | allenai.org |
| Cohere | For Good / Research credits | cohere.com/research |
| Hugging Face | Research compute grants | huggingface.co/grants |

**Notes on "Rock":** If you meant Reka AI, their contact is research@reka.ai. If you meant Grok / xAI, use the x.ai link above. Hugging Face is worth including because they operate ZeroGPU and research compute grant programmes independently of any one model provider.

---

## Master Template Letter

> **Instructions for use:** Replace every `[BRACKETED]` item before sending. See the company-specific notes below for what to customise in each version. Attach the Technical Requirements Annex (Section 3 of this document) as a one-page PDF appendix.

---

**[YOUR NAME]**
**[TITLE / AFFILIATION]**
J. W. Milton, Clarity Coalition
[email] | [URL to research paper or project page]
[DATE]

**To: Research Partnerships / R&D Team — [COMPANY NAME]**

Dear [COMPANY NAME] Research Team,

I am writing to request access to GPU compute resources and/or inference-level access to your model internals to support independent research on a structural framework for neural network architecture and alignment. I will describe the research briefly, explain what I have already demonstrated, and specify exactly what resources would allow me to complete the work.

**What the research is about.**

The tholonic model proposes that every stable self-sustaining system, physical, biological, or computational, instantiates three structural roles. *Coherence* (referred to here as **Negotiation**, or **N**) is the primary state: the dynamic potential from which the system differentiates. From that differentiation, two complementary roles emerge: *regularisation* (the definitional constraint that bounds behaviour, referred to here as **Definition**, or **D**), and *expressivity* (the integrative capacity that generates outputs, referred to here as **Contribution**, or **C**). Critically, D and C are not independent: their interaction produces a new N state, a resolved coherence that becomes the starting condition for the next cycle. N is therefore both parent and product. It gives rise to D and C, and D and C, through their interaction, reconstitute N. This recursive triadic structure is what the framework means by a "self-sustaining" system: one whose coherence is regenerated internally rather than maintained by continuous external correction.

Applied to transformer architectures, this predicts that inference proceeds in identifiable phases whose boundaries are governed by five mathematical constants (φ, √2, ln 2, e, π/4). These constants are not chosen arbitrarily or fitted post-hoc. Each is a fixed point or invariant that emerges via convergence from the N-D-C recursion when applied to abstract mathematical structure: φ as the self-similar ratio produced when D and C are in proportional balance; √2 as the scaling invariant at the D/C differentiation boundary; ln 2 as the information-theoretic compression limit at the output stage; e as the continuous growth rate at the embedding expansion stage; and π/4 as the rotational symmetry at the mid-network equilibrium. The same recursive system used to evaluate neural architectures is the system from which the evaluation constants themselves arise. This self-referential grounding is what distinguishes the tholonic framework from a post-hoc parameter fit: the constants were derived structurally before the neural measurements were taken.

The framework further predicts that current architectures are structurally C-dominant: their integrative components (attention, MLP projections) carry disproportionately more computational weight than their definitional components (LayerNorm, masking), and that this imbalance is the structural reason alignment is hard. A system whose definitional constraint is externally imposed rather than intrinsic to its organisation is vulnerable to specification gaming.

This is not a vague theoretical claim. It makes concrete, falsifiable predictions about measurable quantities inside running neural networks.

**What we have already established.**

Working entirely on CPU with publicly available models (14 models spanning six architecture families: GPT-1, GPT-2, GPT-Neo, Pythia, OPT, and Qwen), I have:

- Applied four independent per-layer metrics (effective rank, attention entropy, gradient sensitivity, delta norm) to detect phase boundaries from the network's own dynamics rather than from theoretical assumptions.
- Found that the five tholonic constants appear at those empirically detected boundaries at a **78% rate (51 of 65 transitions)**, passing the pre-registered 67% threshold. Each constant appeared in its theoretically predicted role (φ at mid-network equilibrium, ln 2 at output compression, √2 at early scaling, e at embedding expansion).
- Confirmed universal C-dominance: all 14 models show a D/C activation ratio substantially below the theoretically predicted virial target of 0.5, with the LayerNorm component carrying far less weight than the projection component. This is precisely the structural C-dominance that the tholonic framework predicts.
- Found family-level pass rates above 80% for GPT-Neo, Pythia, OPT, and Qwen, with all families above the 67% threshold.

The full research paper and supporting code are available at [URL to paper / project page]. All measurements are reproducible with the provided Python scripts.

**What I cannot do without GPU access.**

The observational results above are consistent with the hypothesis but cannot confirm it causally. What is needed are training experiments. Specifically:

1. **Convergence test:** Train matched pairs of models (with vs. without the tholonic virial balance regulariser active during training) on WikiText-103 and measure whether the regulariser produces faster convergence to the same validation loss. This is the most direct causal test of the core claim.

2. **Replication on held-out families:** The 78% result used six architecture families. Pre-registered replication requires testing on families not yet measured: Mistral, Llama, Gemma, Phi, and Falcon. These models (2B–13B parameters) require at least 16–40 GB VRAM for inference with hidden-state extraction.

3. **Robustness test:** Evaluate whether tholonically-trained models show smaller performance degradation under out-of-distribution inputs, using the WILDS benchmark.

4. **Optimal depth prediction:** Train fixed-width models at multiple depths and test whether the formula $L^* = \log_\phi(H_0/H_L)$ predicts the empirically optimal depth within ±2 layers.

A full technical specification of all required experiments, with compute estimates, is attached as an annex.

**What I am requesting.**

[CUSTOMISE PER COMPANY — see notes below. Examples:]

- [Anthropic / OpenAI / xAI / Cohere]: **API credits** sufficient to run inference on your frontier models with hidden-state access (logit-level outputs at minimum), enabling the replication experiments on held-out architectures without requiring local GPU deployment.

- [Google DeepMind / Meta AI / AI2]: **Compute allocation** on your research cluster (approximately 200 A100-hours total for all experiments in the attached annex) and access to model weights with hidden-state extraction enabled for the replication study.

- [Hugging Face]: **ZeroGPU allocation or a compute grant** of approximately 200 GPU-hours on A100 hardware, used entirely with publicly available model checkpoints already hosted on the Hub.

I am requesting only what is necessary to complete the experiments described in the annex. I am not requesting exclusive access, proprietary weights, or any data that is not already intended for research use. All results will be published openly, citing [COMPANY NAME] in the acknowledgements.

**Why this may be of interest to your organisation.**

[CUSTOMISE PER COMPANY — see notes below. The structural argument about C-dominance and alignment risk is directly relevant to Anthropic and OpenAI. The architecture efficiency angle is relevant to Mistral and Meta. The open-weights replication angle is relevant to Hugging Face and AI2.]

The tholonic framework, if its predictions hold at scale, offers a structural account of why alignment becomes harder as capability increases in C-dominant systems, and a concrete architectural alternative. The training experiments described above would either confirm that structural virial balance is a useful training signal (supporting the development of more stable, alignment-friendly architectures) or falsify the hypothesis cleanly, ruling out an entire class of structural arguments. Either outcome is useful.

**Structural integration and the alignment problem.**

Current alignment approaches, including RLHF, Constitutional AI, and RLAIF, share a common architectural assumption: that definitional constraint (D) can be imposed on a trained system from outside, after the fact, via reward signals, constitutional principles, or preference data. The tholonic framework predicts this approach will always be brittle. A C-dominant system whose integrative capacity substantially outweighs its definitional structure will tend to satisfy the letter of externally imposed constraints while drifting from their intent. Specification gaming, reward hacking, and distributional fragility are not training failures in this account. They are structural consequences of an architecture whose balance was never part of the training objective.

The virial balance regulariser addresses this at the architectural level. By embedding the D/C balance constraint directly into the training loss, the system learns to self-limit as part of its own optimisation rather than in response to an external fence. The structural prediction is that a virial-balanced model will remain more coherent with its operational context under distribution shift, capability scaling, and adversarial pressure, not because it has been more thoroughly patched, but because its definitional and integrative capacities are proportioned by design.

In the N-D-C framework, N (Negotiation) represents the system's ongoing dynamic relationship with its environment: the continuous mediation between internal structure and external context. A system in which D and C are chronically imbalanced cannot sustain that negotiation stably. It drifts. Virial balance is, in this sense, the architectural precondition for a system that remains integrated with its environment and purpose over time, rather than one that must be continually corrected from outside. This is not a claim that structural balance solves alignment. It is the more limited and testable claim that structural imbalance is a necessary condition for the failure modes alignment research is trying to address, and that Experiments 1 and 5 would provide the first direct causal evidence for or against that claim.

**Broader application and real-world context.**

The tholonic framework is not solely an AI architecture claim. The same NDC supply chain analysis is currently being evaluated for application to large-scale environmental governance, including a river basin restoration project under review by a 91-country consortium, a West African blue carbon and mangrove restoration initiative, and the long-term supply chain sustainability of shea butter production and distribution across West Africa. These applications test the same structural prediction: that phase-balanced systems are more resilient and efficient than phase-imbalanced ones, in domains where outcomes are measurable at scale and stakes are high. GPU access to validate the neural architecture predictions would simultaneously advance the AI-specific hypothesis and the broader framework on which the environmental work depends.

**Previous work and transparency.**

I am an independent researcher without institutional affiliation. The tholonic model is a speculative framework; all claims in the paper are graded by evidence strength and speculative claims are flagged. The 78% result is the strongest current evidence and is clearly labelled as preliminary pending pre-registered replication. I am not asking you to endorse the framework; I am asking for the computational resources to test it rigorously.

I would welcome a brief call to discuss the research and answer any technical questions before a formal decision. Thank you for your time and consideration.

Sincerely,

**Jeffrey W. Milton**
Clarity Coalition — Independent Researcher
[email]
[phone / LinkedIn / project URL]

---

## Company-Specific Customisation Notes

### Anthropic

- Emphasise the alignment angle directly. The claim that C-dominance is the structural root of specification gaming is a claim about *their core research problem*. Frame it as: "this is a falsifiable structural account of why RLHF models game the reward model, and the training experiment would test whether virial balance reduces that gap."
- The Constitutional AI connection is worth stating explicitly. Constitutional AI (Bai et al., 2022) adds D from outside: a fixed set of principles applied as a post-training or fine-tuning constraint. The tholonic argument is that constitutional constraints would be more robust if they were augmenting intrinsic structural balance rather than substituting for its absence. A C-dominant base model with a constitutional layer is still structurally C-dominant. The constitutional layer reduces the surface area of misalignment but does not address the underlying imbalance. Experiment 1 would test whether training with the virial regulariser produces a base model that is structurally less susceptible to reward gaming before any constitutional layer is applied, which is directly relevant to Anthropic's scaling roadmap.
- Request: **API credits with logprob access** (they offer extended logprob output for researchers). You don't need their closed weights. You need to run their models on your prompts and extract confidence distributions. Experiment 5 (reward hacking resistance) is the most Anthropic-relevant experiment and should be highlighted specifically in the Anthropic version of the letter.
- Contact: research-access@anthropic.com or apply via the Responsible Scaling Policy researcher access programme.

### OpenAI

- Frame around the **GPT-series architectural findings**. You have results for GPT-1 and GPT-2. The natural next step is GPT-3 and GPT-4 architecture families, which only OpenAI can provide access to.
- Request: **Researcher API access with logit extraction** (the `logprobs` parameter in the completions API) and possibly hidden-state access if they can grant it.
- Note: OpenAI's researcher programme requires a brief research proposal. Submit the abstract of the paper plus the annex.
- Contact: researcher-access@openai.com

### Google DeepMind

- Emphasise the Gemma and PaLM2 families, which are the primary held-out architectures for the replication study.
- Their research partnership programme prefers academic institutional affiliation. If you lack this, approach via the Google TPU Research Cloud (TRC) programme, which grants TPU access to independent researchers with a research proposal.
- Request: **TPU v4 allocation via TRC**, or Gemma model access for hidden-state extraction.
- Contact: tpu-research-cloud@google.com (for TRC); deepmind.com/research for partnership.

### Meta AI

- Emphasis: you have results for GPT-Neo and OPT; Llama-2 and Llama-3 are the obvious next architectures in the replication study. Meta already open-weights Llama: what you need is compute to run inference at scale with hidden-state extraction on the 7B and 13B variants.
- Request: **Research compute allocation** on their internal cluster, or simply confirmation that you can use their open Llama weights under the research licence. (You can already do this; the ask here is for GPU credits to run it.)
- Contact: ai-research@meta.com or via the Llama research licence request form.

### xAI (Grok)

- xAI is newer and does not have an established researcher access programme.
- Frame the request around **Grok's architecture** specifically: the Grok family has not been tested in the replication study and adding it would give you 7 architecture families.
- Expect a longer response time. Try direct email: research@x.ai

### Mistral AI

- Mistral's sliding window attention is architecturally the *highest-risk* case for the replication study: it modifies the attention D-structure in a novel way, and it is not clear whether the tholonic phase detection will generalise to it. Frame this as: "your architecture is specifically the most interesting unknown case in the held-out replication."
- Request: **Access to Mistral-7B or Mixtral-8x7B hidden states** (they are open-weights, so you already have this in principle: the ask is for compute to run 7B inference with gradient computation).
- Contact: research@mistral.ai

### Hugging Face

- This is probably the **most accessible** option. Apply for a ZeroGPU grant or a compute grant directly.
- Frame around: you are already using HF Hub for all model downloads; your scripts are written against the transformers library; the experiment outputs would be published as a HF dataset for community replication.
- Request: **ZeroGPU allocation or $500–1000 in compute credits** via the HF grant programme.
- Contact: compute-grant@huggingface.co or apply at huggingface.co/grants

### AI2 / Allen Institute

- AI2 operates the Semantic Scholar API and the OLMo open-weights family. They are sympathetic to independent structural AI research.
- Frame around: OLMo has not been tested in the replication study; adding it would complete a full spectrum from small (GPT-2) to mid-scale (OLMo-7B) architectures.
- Request: **GPU compute allocation via their research cluster** or OLMo model access for hidden-state extraction.
- Contact: research@allenai.org

---

## Annex — Technical Requirements (attach with each letter)

*This one-page annex can be formatted as a PDF and attached to every submission.*

---

**Technical Requirements Annex**
**Tholonic Neural Architecture Research — Compute Access Request**
Jeffrey W. Milton — [email] — [date]

**Completed work (no GPU required)**

All measurements below were performed on 14 publicly available models (GPT-1 through GPT-2 XL, GPT-Neo 125m and 1.3B, Pythia 160m and 410m, OPT 125m and 350m, Qwen3 0.6B and 1.7B) running on consumer CPU. The 78% phase-boundary detection result passes the pre-registered 67% threshold. All code is open and reproducible.

**Experiment 1 — Convergence Speed**

*Objective:* Test whether adding the virial balance regulariser $\mathcal{L}_\text{virial} = \lambda \sum_l |\sigma_D^l - \tfrac{1}{2}\sigma_C^l|^2$ to the training objective produces faster convergence to a given validation loss.

*Compute:* 6 training runs × GPT-2 small (124M) on WikiText-103 × ~2h each = **~12 A100-hours.** 3 baseline, 3 tholonic, matched random seeds.

*Pass criterion:* Tholonic condition reaches validation loss thresholds (4.5, 4.0, 3.7 nats) in fewer gradient steps for ≥ 2/3 seed pairs, p < 0.05 paired t-test.

**Experiment 2 — Replication on Held-Out Architectures**

*Objective:* Apply four-metric data-driven phase detection to 5 held-out architecture families (Mistral, Llama-2/3, Gemma, Phi, Falcon) not used in the original study.

*Compute:* 10 inference runs per model × 5 families × ~30 min each (7B models) = **~25 A100-hours.** No training; inference only with `output_hidden_states=True`.

*Pass criterion:* ≥ 67% of detected boundaries match a tholonic constant at ±8% tolerance, replicating the main result.

**Experiment 3 — Optimal Depth Test**

*Objective:* Train fixed-width (d=512) models at depths 2, 4, 6, 8, 12, 16, 24 on WikiText-103; compare empirical optimal depth to the prediction $L^* = \log_\phi(H_0/H_L)$.

*Compute:* 7 training runs × ~3h each = **~21 A100-hours.**

*Pass criterion:* Predicted depth within ±2 layers of empirical optimum.

**Experiment 4 — OOD Robustness**

*Objective:* Compare OOD perplexity degradation between baseline and tholonically-trained models on a domain-shifted evaluation set (scientific text, code, or dialogue, none seen during WikiText-103 training).

*Compute:* Evaluation only (models already trained in Exp. 1) = **~2 A100-hours.**

**Experiment 5 — Reward Hacking Resistance (optional, most resource-intensive)**

*Objective:* Fine-tune matched pairs via RLHF on Anthropic HH-RLHF with and without the tholonic regulariser; measure reward model score vs. human preference alignment.

*Compute:* **~60 A100-hours.** Requires 2× A100 40GB minimum. Recommended only if Experiments 1–4 pass.

**Total compute requested (Experiments 1–4):** approximately **60 A100-hours**, equivalent to one week of access to a single A100 instance.

**Software:** All measurement and training code is written in Python (PyTorch + HuggingFace transformers), open-sourced, and available for review on request.

**Data outputs:** All results will be published openly under CC-BY licence with the contributing organisation credited in the acknowledgements.

---

*End of Annex.*
