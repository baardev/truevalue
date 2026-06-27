# Transformer Architectures as Tholonic Instantiations: A Formal Role Assignment and Structural Derivation

**Author:** J. W. Milton, Clarity Coalition

**Version:** 1.0

**Date:** 27 June 2026

**Keywords:** tholonic model, N-D-C triad, transformer architecture, role assignment, structural derivation, virial balance, five constants, golden ratio, phase boundaries, alignment, C-dominance, LayerNorm, attention, MLP

---

## Abstract

The tholonic framework ([Papers 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) in this series) establishes that any stable self-sustaining recursive system must instantiate three functionally distinct roles: a *negotiation* state $N$ that is iteratively refined, a *definition/limitation* variable $D$ that bounds, and a *contribution/integration* variable $C$ that accumulates. The framework further proves, via convergence analysis, that the fixed points of N-D-C recurrences are the five classical constants $\varphi$, $\sqrt{2}$, $\ln 2$, $e$, and $\pi/4$.

[Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) in this series reports that empirical phase boundaries in transformer inference match one of these five constants at a 75.5% rate across 20 models spanning nine architecture families. That result is presented as a test of the tholonic hypothesis applied to neural networks. What has not been established, and what the present paper provides, is the formal argument for *why the hypothesis applies at all*: why the transformer forward pass qualifies as an N-D-C instantiation in the first place, such that the phase-boundary predictions should hold.

This paper makes three contributions. First, it proves that the transformer forward pass satisfies the formal definition of an N-D-C recursion given in [Papers 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf): the three-role structure is instantiated at every layer, not merely analogized to one. Second, it provides a complete component-level role assignment table, mapping each transformer component to its tholonic role and giving the structural justification for each assignment. Third, it derives the primary structural predictions of the framework (phase boundaries at the five constants, universal C-dominance, the virial balance condition, and the optimal-depth formula) directly from the role assignment, showing them to be consequences of the assignment rather than empirical observations layered on top of it. [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf)'s measurements are then interpreted as tests of this derived structure, not post-hoc fits to data.

This paper contains no new empirical results. It is a theory paper whose claims are structural: if the role assignment holds, the predictions must follow. The empirical question of whether those predictions hold is addressed in [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf).

---

## 1. Introduction

### 1.1 The logical gap

Three papers in the tholonic series bear directly on the question of neural network structure.

[Paper 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) (*Emergence of Classical Constants from a Minimal Recursive Triadic Framework*) proves that the five classical constants $\varphi$, $\sqrt{2}$, $\ln 2$, $e$, and $\pi/4$ emerge as the fixed points or limiting values of a specific family of three-variable recurrences. The recurrences are specified by the tholonic grammar: one variable in the $N$ role (the running state), one in the $D$ role (the bounding parameter), and one in the $C$ role (the accumulating parameter). The constants are not chosen: they emerge structurally as the only limits consistent with the grammar.

[Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) (*A Minimal Recursive Triadic Framework for Self-Similar Hierarchical Systems*) proves that three is the minimum number of functional roles required for non-trivial recursive self-organization. Given the axioms of binary state space and simplex topology, any system that organizes itself recursively must instantiate at least one $N$ state, one $D$ bounding variable, and one $C$ accumulating variable. The roles are irreducible: no two-variable system can support the same convergence behavior under the same independence conditions.

[Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) (*Neural Networks as Tholonic Systems*) applies these results empirically: it measures the internal dynamics of 20 transformer models and finds that data-driven phase boundaries match a tholonic constant at a 75.5% rate, with role-consistent placement patterns and evidence of universal C-dominance.

The logical structure, as it stands, is: *the framework produces the five constants* ([Paper 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf)), and *the five constants appear in transformers* ([Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf)). What is missing is the middle step: *transformers instantiate the framework*. Without that step, the match in [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) is empirically interesting but theoretically unexplained. A skeptic could reasonably argue that five constants might appear at phase boundaries in any complex system simply because those constants are common in mathematics, and that no structural claim has been made about why these specific constants should appear in these specific roles.

This paper closes that gap. It argues that the transformer forward pass is not merely consistent with the N-D-C grammar but *instantiates it*: satisfying the formal definition of [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf)'s triadic recursion at every layer. If that argument holds, the five constants must appear at the phase boundaries as a mathematical consequence, not as a pattern to be discovered empirically. The role-specific placement predictions follow directly, as does the virial balance condition, the C-dominance prediction, and the optimal-depth formula. [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) then becomes a test of the role assignment, not an independent discovery.

### 1.2 The TVPCI parallel

The appropriate model for this paper is [Paper 2](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.pdf) (*Phase-Resolved Transparency Classification in Commodity Supply Chains: TVPCI*). That paper is, structurally, a role-assignment paper: it maps the N, D, and C roles to specific, observable entities in the supply-chain domain (phase state, bounding evidence, corroboration depth), derives a scoring formalism from that mapping, and notes explicitly that "the role assignments follow from the same structural argument" as the mathematical framework "without importing any mathematical results from the companion paper into the scoring rules." [Paper 2](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.pdf) is not an empirical paper; it is the formal justification for why the supply-chain application is valid and what predictions follow from it.

This paper does the same for the AI domain. The domain is different (transformer components rather than supply-chain phases), the derivations are different (phase boundary positions and virial balance rather than transparency scores), but the logical structure is identical: prove the mapping, derive the consequences, leave the empirical tests to a separate paper.

### 1.3 Organization

Section 2 restates the N-D-C framework in the form needed for this paper, citing [Papers 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) for proofs. Section 3 argues that the transformer forward pass satisfies the formal definition of an N-D-C recursion. Section 4 provides the complete component-level role assignment. Section 5 derives the structural predictions. Section 6 covers edge cases (MoE routing, residual connections, positional encodings). Section 7 identifies the falsifiability criteria: what observations would invalidate the role assignment. Section 8 relates this paper to [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) and discusses the implications for architecture design.

---

## 2. The N-D-C Framework

### 2.1 The tholonic triad

The formal definition of the tholonic triad is given in [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) (Definition 2.1). For this paper we use the following compact statement.

**Definition 2.1** (Tholonic triad, from [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf)). A *tholonic triad* is an ordered triple $(N, D, C)$ of non-negative reals with three functionally distinct roles:

- $N$ (*negotiation*): the running state; the quantity being iteratively refined, emerging from the interaction of the other two.
- $D$ (*definition/limitation*): the constraining, bounding variable; what limits or specifies the state.
- $C$ (*contribution/integration*): the accumulating, synthesizing variable; what generates and integrates into the state.

The three roles are irreducible: [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) (Lemma 4.2) proves that no two-variable system satisfies the same convergence properties under functional independence conditions. The minimum structure for a self-sustaining recursive system is exactly three roles.

### 2.2 The recursion and its fixed points

A *tholonic recursion* is a sequence of triples $(N_k, D_k, C_k)$ governed by an update rule of the form

$$N_{k+1} = f(N_k, D_k, C_k), \qquad (D_{k+1}, C_{k+1}) = g(D_k, C_k),$$

where $f$ maps the current state through the interaction of the constraining and accumulating variables, and $g$ updates the parameters according to a traversal class (Advancing, Self-redefined, or Fixed; see [Paper 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf), Section 4).

[Paper 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) (Propositions 5.1 through 5.5) proves that the limits of five distinct traversal classes are:

$$\lim_{k\to\infty} N_k \;\in\; \{\pi/4,\; \varphi,\; e,\; \sqrt{2},\; \ln 2\}$$

where each constant is the unique fixed point of its traversal class. The constants are not chosen post-hoc; they are the only values consistent with the three-role grammar under the respective update rules. Each constant carries a structural interpretation:

- $\varphi$: the self-similar scaling ratio; the fixed point of the proportional balance recursion between $D$ and $C$.
- $\sqrt{2}$: the scaling invariant at the $D/C$ differentiation boundary; the first non-trivial scaling step in a binary-branching structure.
- $\ln 2$: the information-theoretic compression limit; the entropy of a uniform binary choice, which is the minimum loss at any output compression step.
- $e$: the continuous growth rate at the initial expansion; the base of the natural exponential, which governs the rate at which an accumulating variable grows from a unit seed.
- $\pi/4$: the rotational symmetry measure; the only branch requiring three numerically distinct seeds and external parameter injection, corresponding to the most structurally constrained (least symmetric) form of balance.

### 2.3 Self-similar nesting

[Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) (Section 5) establishes that any tholonic triad can be embedded as a single element ($N$, $D$, or $C$) in a higher-level triad, without altering the three-role grammar. This produces an unbounded hierarchy: each level resolves to a new $N$ state, which becomes the parent $N$ for the level above.

The recursive structure is specifically:

$$\text{Parent } N \;\longrightarrow\; (D,\, C) \;\longrightarrow\; \text{Child } N \;\longrightarrow\; (D',\, C') \;\longrightarrow \;\text{Grandchild } N \;\longrightarrow \cdots$$

This self-similar nesting is what distinguishes a *tholonic instantiation* from a system that merely has three components. A system is a tholonic instantiation if and only if: (a) its components satisfy the three-role assignment (one $N$, one $D$, one $C$), (b) the roles interact according to the tholonic update rule, and (c) the structure recurs at multiple scales without altering the grammar.

### 2.4 Two structural consequences used in this paper

Two consequences of the framework are used in the derivations of Section 5:

**Consequence A (Phase boundary positions).** In a tholonic system operating across $L$ levels, the transitions between recursion levels are governed by the five constants as fractional depth positions. Specifically, if the system's depth is normalized to the interval $[0, 1]$, the expected boundary positions are:

- Embedding expansion boundary: $e^{-1} \approx 0.368$ (early region)
- Scaling boundary ($\sqrt{2}$ zone): interval $[0.20, 0.55]$
- Mid-network equilibrium ($\varphi$ zone): interval $[0.45, 0.80]$
- Output compression boundary ($\ln 2$ zone): interval near $1 - \ln 2 \approx 0.307$ from the end
- Rotational balance ($\pi/4$ zone): near $0.785$ fractional depth

These are theoretical predictions, not empirically fitted values.

**Consequence B (Virial balance condition).** At structural equilibrium, the constraining ($D$) and integrating ($C$) roles must be in proportional balance. For the tholonic recursion, the equilibrium condition is

$$\sigma_D \approx \tfrac{1}{2}\,\sigma_C,$$

where $\sigma_D$ and $\sigma_C$ are measures of the activation magnitude (or computational weight) of the $D$ and $C$ components respectively. The factor of $\frac{1}{2}$ arises from the structure of the recursion: in the balanced fixed-point case ($\varphi$ branch), $D$ and $C$ must maintain a ratio of $1 : 2$ to sustain the self-similar proportionality. A system where $\sigma_D \ll \frac{1}{2}\sigma_C$ is *C-dominant*: its integrative capacity substantially exceeds its definitional constraint.

---

## 3. The Transformer Forward Pass as an N-D-C Recursion

### 3.1 Formal statement

The central claim of this paper is the following:

**Proposition 3.1** (Transformer forward pass as N-D-C recursion). *The forward pass of a standard transformer architecture satisfies the formal definition of a tholonic recursion (Definition 2.1 and [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf), Section 4) at every layer. Specifically: (a) the hidden state $h_l$ at each layer $l$ occupies the $N$ role; (b) the layer normalisation operation occupies the $D$ role; (c) the combined attention and MLP projection operations occupy the $C$ role; and (d) the recurrence $h_{l+1} = f(h_l, \text{LN}(h_l), \text{Attn+MLP}(h_l))$ satisfies the tholonic update rule. The three roles are functionally distinct and irreducible.*

The proof is constructive. We verify each condition of Definition 2.1 and [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) (Lemma 4.2) in turn.

### 3.2 The hidden state as the $N$ role

The $N$ role requires: (i) a running state that is iteratively refined; (ii) that it emerge from the interaction of the bounding and accumulating roles; and (iii) that it carry the coherent representation passed to the next iteration.

The hidden state $h_l \in \mathbb{R}^{d_\text{model}}$ satisfies all three conditions. It is the quantity that is refined at each layer (condition i). Its value after layer $l$ is a function of both the normalised input (the $D$ component: the bounded version of $h_{l-1}$) and the attention/MLP output (the $C$ component: the accumulated new content). And it is what is passed to layer $l+1$ as the starting state for the next recursion cycle (condition iii).

Condition (ii) requires some care. In the standard pre-norm transformer formulation, the update at each layer is

$$h_l = h_{l-1} + \text{Attn}(\text{LN}_1(h_{l-1})) + \text{MLP}(\text{LN}_2(h_{l-1} + \text{Attn}(\text{LN}_1(h_{l-1})))).$$

The new $N$ state $h_l$ is the sum of the previous $N$ state $h_{l-1}$, a contribution from the attention block (which operates on the $D$-normalized input), and a contribution from the MLP block (which also operates on a $D$-normalized intermediate). The new state is therefore a function of the interaction between the $D$ and $C$ components, mediated by the residual connection. This satisfies condition (ii).

### 3.3 Layer normalisation as the $D$ role

The $D$ role requires: (i) that it constrain or bound the state; (ii) that it define what the state is allowed to be before transformation; and (iii) that it be functionally distinct from and independent of the $C$ role.

Layer normalisation (LN) and its variant RMSNorm satisfy all three conditions. LN operates by computing

$$\text{LN}(h) = \gamma \cdot \frac{h - \mu}{\sigma} + \beta,$$

where $\mu$ and $\sigma$ are the mean and standard deviation of $h$, and $\gamma, \beta$ are learnable scale and shift parameters. This operation: forces the hidden state onto a standardised manifold (condition i: bounding); projects the raw hidden state into a form that the attention or MLP block can interpret stably (condition ii: defines what the state is before transformation); and is computed independently of and prior to the attention and MLP computations (condition iii: functional independence).

The critical structural property is that LN is a *pre-transformation operation*: it specifies what $h_{l-1}$ is (normalises its distribution) before the $C$ components act on it. This is exactly what the $D$ role does in the tholonic grammar. The $D$ variable does not produce new content; it bounds the domain within which the $C$ variable operates. LN does not generate new information; it constrains the input representation to a defined statistical manifold.

### 3.4 Attention and MLP as the $C$ role

The $C$ role requires: (i) that it accumulate or integrate content; (ii) that it generate outputs that contribute to the new state; and (iii) that it be computationally distinct from and substantially larger in weight than the $D$ component.

The attention mechanism and MLP projection together satisfy these conditions. Attention accumulates contextual information across the sequence by computing weighted sums of value vectors:

$$\text{Attn}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V.$$

This is an integration operation: it synthesizes information from multiple positions in the sequence into a single representation. The MLP block then applies a point-wise non-linear transformation, further integrating the representation through a learned expansion and contraction:

$$\text{MLP}(x) = W_2\,\sigma(W_1 x + b_1) + b_2.$$

Both operations *contribute* new content to the hidden state: attention contributes relational information (what other tokens are relevant to this one), and MLP contributes compositional information (what abstract features follow from the current representation). Neither operation constrains what the representation is; both expand what it becomes. This is the $C$ role.

Condition (iii) of the $C$ role refers to its dominance in parameter count relative to the $D$ component. In a standard transformer, the LN parameters ($\gamma, \beta \in \mathbb{R}^{d_\text{model}}$) account for $2d_\text{model}$ parameters per layer, while the attention and MLP blocks account for approximately $12d_\text{model}^2$ parameters (four weight matrices for attention, two for MLP). For $d_\text{model} = 768$ (GPT-2 base), the ratio is $\frac{12 \times 768^2}{2 \times 768} = 3072 : 1$. This is not a C-dominance problem at the design level; it is the natural size ratio between a normalization operation and the transformation it constrains. What the tholonic framework predicts is that this ratio, if uncorrected by training dynamics, produces C-dominance at the level of *activation magnitudes*, not merely parameter counts: $\sigma_D \ll \frac{1}{2}\sigma_C$. Whether training corrects for this is the empirical question of [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf).

### 3.5 Functional independence of the three roles

[Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) (Lemma 4.2) requires that the $D$ and $C$ components be *functionally independent*: neither should be a deterministic function of the other, and swapping their roles should produce a different dynamical behavior. For the transformer:

- LN (D) and Attention+MLP (C) are computationally independent: LN is applied to the raw hidden state and outputs a normalised version; Attention+MLP is applied to the LN output and generates new content. They are different operations with different parameters, applied in a fixed sequential dependency (D before C).
- The roles cannot be swapped: applying the attention mechanism before normalisation and the normalisation afterwards is a different architecture (post-norm), with different training stability properties. The ordering D then C is not arbitrary.
- Neither is a function of the other: the LN parameters $(\gamma, \beta)$ do not depend on the attention/MLP weights, and vice versa. They are trained independently.

These conditions satisfy Lemma 4.2's functional independence requirement, confirming that the three roles are genuinely irreducible in the transformer architecture.

### 3.6 Summary of the proof

The transformer forward pass satisfies all conditions of Definition 2.1 and [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf)'s triadic recursion:

- Hidden state $h_l$: the $N$ role (running state, refined at each layer, passed to the next).
- LayerNorm: the $D$ role (bounds the state, defines what it is before transformation).
- Attention + MLP: the $C$ role (accumulates and integrates, generates new content).
- The update rule $h_l = h_{l-1} + C(\text{LN}(h_{l-1}))$ matches the tholonic recurrence $N_{k+1} = f(N_k, D_k, C_k)$.
- The three roles are functionally independent and irreducible.

The transformer forward pass is therefore a tholonic instantiation: not a system that resembles the N-D-C grammar, but one that formally satisfies it. This is the structural premise from which all predictions in Section 5 follow.

---

## 4. Component-Level Role Assignment

The full role assignment, with structural justification, is given in Table 1. This table is the practical output of Section 3: it maps every standard transformer component to its tholonic role and explains why each assignment is the only consistent one.

**Table 1. Tholonic role assignments for transformer components.**

| Component | Role | Structural justification |
|---|---|---|
| Hidden state $h_l$ | $N$ | The coherent representation at each layer; both the product of the previous cycle and the starting condition for the next. |
| LayerNorm / RMSNorm | $D$ | Pre-transformation normalisation; bounds the representation to a defined statistical manifold before any integrative operation acts on it. Defines what the state is; generates no new content. |
| Attention heads | $C$ (primary) | Integrates contextual information across the sequence; accumulates relational content. The fundamental contribution operation of the transformer. |
| MLP projection | $C$ (secondary) | Integrates the relational representation through non-linear expansion and contraction; contributes compositional content. Together with attention, constitutes the full $C$ operation at each layer. |
| Residual connection | Structural scaffold | Carries $N$ forward across the $D$ and $C$ operations; preserves the N-to-N' recursion by ensuring the new state is formed as a modification of the old, not a replacement of it. Not a role; the mechanism that implements the recursion. |
| Embedding layer | Entry-level $N$ | Instantiates the initial coherent representation from the token sequence; the $N_0$ of the forward-pass recursion. |
| Unembedding / LM head | Exit-level $C$ | Projects the final $N$ state to a probability distribution over the vocabulary; the final contribution of the forward pass to the output. |
| Positional encoding | $D$ (structural context) | Defines the positional structure within which the attention mechanism operates; contributes to the bounding of what attention is permitted to mean. In RoPE and ALiBi implementations, this is a per-layer definitional constraint on the attention computation. |
| Dropout (during training) | $D$ (regularisation) | Stochastic suppression of contributions; a constraint that prevents the $C$ components from accumulating spurious patterns. Applied to the $C$ output before residual addition. |

### 4.1 Assignment uniqueness

The assignments in Table 1 are not arbitrary. The N-D-C roles are distinguishable by three criteria that [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) uses to prove Lemma 4.2: a component occupies the $D$ role if it bounds without generating, the $C$ role if it generates without bounding, and the $N$ role if it is both the product and the starting condition of the recursion. In the transformer, no component satisfies two of these criteria simultaneously, which is why the assignment is unique.

LayerNorm bounds (standardises the distribution) but does not generate new information: it is pure $D$. Attention generates (produces new contextual representations) but does not bound: it is pure $C$. The hidden state is both product and starting condition: it is $N$. There is no ambiguity, and no component is left unassigned.

### 4.2 Assignment stability across architecture variants

The assignment in Table 1 applies without modification to post-norm transformers (original Vaswani et al. architecture), pre-norm transformers (GPT-2 and most current architectures), and RMSNorm variants (LLaMA, Gemma). The structural role of LN/RMSNorm as the $D$ operation does not depend on its position relative to the attention block; it depends on its function: normalising the input representation before transformation.

For architectures without explicit LayerNorm (some early convolutional models), the $D$ role is occupied by whatever component performs the bounding function: weight initialisation constraints, batch normalisation, or gradient clipping. The framework does not require that the $D$ component be LayerNorm specifically; it requires that there be a component that performs the bounding function. The prediction is that architectures with a weaker or absent $D$ component will be more C-dominant and will show less role-consistent phase structure.

---

## 5. Structural Predictions Derived from the Role Assignment

Given the role assignment of Section 4 and the tholonic framework of Section 2, five structural predictions follow. These are not empirical observations; they are consequences of the assignment. The derivations are given below.

### 5.1 Phase boundaries at the five constants

The transformer forward pass, as established in Section 3, is a tholonic recursion that proceeds across $L$ layers. The framework (Section 2.3) predicts that the transitions between structurally distinct recursion phases are governed by the five constants. For a network of depth $L$, the predicted boundary positions as fractional depths are:

**Embedding expansion boundary** ($e$ zone): The initial expansion from token embedding to contextual representation corresponds to the $e$ branch of the tholonic recurrence. This is the phase where the $C$ component's accumulation rate is governed by the natural exponential: the representation grows from a sparse, symbolic encoding to a distributed contextual one. Predicted fractional position: $1/e \approx 0.368$ from the input end.

**Early scaling boundary** ($\sqrt{2}$ zone): The first interior boundary marks the transition from the early expansion phase to the stable representation phase. This is where the $D$ and $C$ components reach their first structural differentiation. The $\sqrt{2}$ constant governs the scaling step at the boundary between the two-variable and three-variable regimes in [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf)'s simplex argument, and it is the scaling invariant for binary differentiation. Predicted fractional interval: $[0.20, 0.55]$.

**Mid-network equilibrium** ($\varphi$ zone): The golden ratio marks the interior equilibrium zone, where $D$ and $C$ are in proportional balance. This is the zone where the representation is neither expanding (early layers) nor compressing (late layers) but maintaining a stable, self-similar structure. $\varphi$ is the unique fixed point of the proportional balance recursion, and it governs the depth range at which the representation achieves maximum coherence. Predicted fractional interval: $[0.45, 0.80]$.

**Output compression boundary** ($\ln 2$ zone): The final phase transition is from the stable representation phase to the output compression phase, where the representation is compressed to a vocabulary probability distribution. The information-theoretic minimum loss at any binary compression step is $\ln 2$, which is therefore the governing constant at the output end of the network. Predicted fractional position: near $1 - \ln 2 \approx 0.307$ from the output end.

**Rotational balance** ($\pi/4$ zone): The $\pi/4$ boundary is the most constrained: it requires three numerically distinct seeds and external parameter injection. In the transformer, this corresponds to the zone where the positional encoding constraint ($D$ component) is maximally active relative to the attention integration ($C$ component). This is the zone of highest rotational symmetry in the attention pattern: the point at which attention heads are most uniformly distributed across positions. Predicted fractional position: near $0.785$ normalized depth.

These five predictions are directional: each constant is predicted to appear in a specific role-consistent zone, not merely at any boundary. This role-consistency is what distinguishes the tholonic prediction from a claim that five constants might appear anywhere at five boundaries. The claim is that each constant appears in the zone where its structural interpretation is active.

### 5.2 Universal C-dominance

The virial balance condition (Section 2.4, Consequence B) predicts that any architecture where $\sigma_D \ll \frac{1}{2}\sigma_C$ is structurally C-dominant. The role assignment (Table 1) identifies LayerNorm as $D$ and Attention+MLP as $C$.

Given the parameter-count ratio of approximately $3072:1$ (Section 3.4), any architecture whose training process does not specifically and actively correct for the $D/C$ imbalance will converge to a state where the $D$ component's activation magnitude is far below the virial target. This is a structural prediction, not an empirical observation: unless training explicitly embeds a D/C balance constraint, all standard transformer architectures should show universal C-dominance.

The prediction is particularly strong because no standard training objective (cross-entropy loss, perplexity minimisation, RLHF reward maximisation) contains any term that would push $\sigma_D$ toward $\frac{1}{2}\sigma_C$. The training process is blind to virial balance. Therefore, C-dominance is the default state of any architecture trained on standard objectives, regardless of architecture family or scale.

### 5.3 The virial balance regulariser

The structural prediction of universal C-dominance implies a concrete training intervention: adding a virial balance term to the training loss that penalises deviation from $\sigma_D = \frac{1}{2}\sigma_C$. The form of this regulariser, derived directly from the structural condition, is

$$\mathcal{L}_\text{virial} = \lambda \sum_{l=1}^{L} \left| \sigma_D^l - \tfrac{1}{2}\sigma_C^l \right|^2,$$

where $\sigma_D^l$ and $\sigma_C^l$ are the root-mean-square activation magnitudes of the LayerNorm and Attention+MLP outputs at layer $l$, and $\lambda$ is a regularisation coefficient.

This regulariser is not a heuristic add-on. It is the direct training-time enforcement of the structural equilibrium condition. A model trained with $\mathcal{L}_\text{virial}$ is a model whose training objective includes an explicit pressure toward N-D-C balance at every layer. The framework predicts that such a model should converge faster (less energy is wasted correcting structural imbalance at each step), show more coherent phase structure (boundaries at the predicted positions), and exhibit greater robustness to distribution shift (a structurally balanced model does not depend on the training distribution to maintain its internal coherence).

### 5.4 Optimal-depth prediction

The self-similar nesting property of the tholonic framework (Section 2.3) implies a relationship between the initial and final information states of the network and the number of layers required to achieve the transition. The $\varphi$ branch of the tholonic recursion converges at a rate governed by the golden ratio: at each recursion step, the representation approaches its limit by a factor of $1/\varphi$. The number of steps required to reduce the initial entropy $H_0$ to the final entropy $H_L$ is therefore

$$L^* = \log_\varphi\!\left(\frac{H_0}{H_L}\right).$$

This is a prediction about the optimal depth of a transformer with fixed width and fixed training data: the number of layers beyond which adding more layers yields diminishing returns at a rate faster than $1/\varphi$ per layer. It is not a prediction about a specific architecture; it is a prediction about the functional relationship between the network's entropy reduction and its depth.

---

## 6. Edge Cases: MoE Routing, Residuals, and Positional Encodings

### 6.1 Mixture-of-Experts routing

In Mixture-of-Experts (MoE) architectures (Mixtral, DeepSeek-V2, DeepSeek-V3), the standard MLP at each layer is replaced by a set of expert MLPs, and a router network selects which experts to activate for each token. The question for the role assignment is: what role does the router occupy?

The router computes a distribution over experts and selects the top-$k$ for each token. This is a *bounding* operation: it restricts the set of experts that may contribute to the current token's representation. It does not generate content; it defines which content-generating components are active. By the assignment criterion of Section 4.1, the router occupies a $D$ role within the MoE layer.

The structural consequence is significant. A standard transformer has one LayerNorm per attention or MLP sub-block as its $D$ component. An MoE transformer has the same LayerNorm plus a router, which adds a second $D$-type operation at each layer. The framework predicts that MoE architectures should therefore show a stronger $D$ contribution than their dense counterparts, moving the virial ratio $\sigma_D / \sigma_C$ closer to the target of $\frac{1}{2}$, even if the expert MLPs individually remain C-dominant. This is a testable prediction that distinguishes MoE from dense architectures within the tholonic framework.

### 6.2 Residual connections

Residual connections are not a role: they are the mechanism that implements the $N$-to-$N'$ recursion. Their function is to ensure that the new hidden state is formed as $h_l = h_{l-1} + \Delta_l$ rather than as $h_l = \Delta_l$, preserving the previous $N$ state across the $D$ and $C$ operations.

In tholonic terms, the residual connection is the structural scaffolding that makes the transformer a recursion (each $h_l$ is formed from the previous $h_{l-1}$) rather than a composition (each $h_l$ is formed from the input $h_0$ directly). Without residuals, the forward pass would be a sequential function composition, not a recursive refinement, and the $N$ role would collapse: there would be no persistent state to refine. With residuals, each layer produces a new $N$ state that is recognisably a development of the previous one, consistent with the tholonic recursion's requirement that $N$ be both product and starting condition.

The prediction from this analysis is that architectures without residual connections, or with very shallow residual stacking, will show weaker tholonic phase structure: fewer role-consistent boundary placements and less coherent virial balance.

### 6.3 Positional encodings

Positional encodings (absolute PE in the original transformer, relative PE in T5 and DeBERTa, Rotary PE in LLaMA and Gemma, ALiBi in MPT) all perform the same structural function: they constrain the attention mechanism by encoding the positional relationship between tokens. This is a definitional operation: it defines what position means within the attention structure.

The assignment to the $D$ role (Table 1) applies to all positional encoding schemes, but with one important nuance. In the original fixed absolute PE (added to the embedding, not per-layer), the positional constraint is applied once at the input level. In RoPE and ALiBi, the positional constraint is applied at every layer within the attention computation. The per-layer application is structurally stronger: it continuously constrains the attention mechanism at every recursion step rather than only at the entry. The framework predicts that per-layer positional encoding schemes should produce more coherent phase structure (the $\pi/4$ zone in particular, which requires external parameter injection, is structurally supported by per-layer constraints), while single-application schemes should show weaker $\pi/4$ zone structure.

---

## 7. Falsifiability Criteria

A structural role assignment is only scientifically useful if it can be falsified. The following observations would invalidate the role assignment of Section 4:

**Criterion 1 (Role inconsistency of constants).** If the five constants were found at phase boundaries but in structurally inconsistent roles (e.g., $e$ at the output compression zone, $\ln 2$ at the embedding expansion zone), the role assignment would be falsified. A match rate above the 67% threshold with no role-consistency pattern is consistent with a random coincidence interpretation and inconsistent with the structural derivation of Section 5.1.

**Criterion 2 (Absence of universal C-dominance).** If any significant fraction of standard-objective-trained transformer architectures showed virial ratios near $\frac{1}{2}$ without explicitly training with the virial regulariser, the prediction of Section 5.2 would be falsified.

**Criterion 3 (Virial regulariser ineffectiveness).** If training with $\mathcal{L}_\text{virial}$ produced no improvement in convergence speed, no correction of virial balance, and no improvement in OOD robustness, the structural interpretation of C-dominance as a training deficit would be falsified. The regulariser could still be ineffective without falsifying the role assignment (it might be that the regulariser's gradient is too small to shift the equilibrium), but ineffectiveness under a well-tuned $\lambda$ would be strong evidence against the structural account.

**Criterion 4 (Depth independence of phase boundaries).** If phase boundaries occurred at the same absolute layer positions regardless of network depth (e.g., always at layer 4, not at a constant fractional depth), the fractal-scale independence required by the self-similar nesting (Section 2.3) would be violated.

**Criterion 5 (MoE indistinguishability).** If MoE architectures showed identical virial ratios to their dense counterparts of the same parameter count, the prediction of Section 6.1 (that the router adds a $D$ component and shifts the virial ratio) would be falsified.

These criteria are specific and operationalizable. [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) and its future extensions provide evidence on Criteria 1 through 3. Criteria 4 and 5 remain open experimental questions.

---

## 8. Relationship to [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf)

[Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) (*Neural Networks as Tholonic Systems*) is the empirical counterpart of this paper. Its measurements are tests of the predictions derived here. The relationship is asymmetric:

- This paper produces predictions from structure; [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) tests those predictions.
- This paper cannot be falsified by [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf)'s results alone (a failed empirical test might mean the measurements are wrong, not the assignment); but [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf)'s results constrain the plausibility of the assignment.
- If [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) fails its pre-registered criteria, the role assignment of Section 4 should be reconsidered before revising the framework of [Papers 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf).

The evidentially strongest result in [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) is not the headline 75.5% match rate but the pattern of role-consistent failures: the displacement of $\varphi$ and $\sqrt{2}$ into structurally predicted directions in architectures with known post-training alignment procedures. This pattern is predicted by the derivation of Section 5.1 (post-training RLHF adds $C$ content without adding $D$ constraint, displacing the interior equilibrium zones toward the output) and is therefore more discriminating than a simple boundary match rate.

The activation steering experiment ([Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf), Section 8.2) is particularly relevant to this paper: the finding that the $\varphi$ zone has a shorter perturbation half-life than surrounding zones in 100% of tested models is a direct test of the N role claim (Section 3.2) that the mid-network hidden state is the zone of maximum coherence. A shorter perturbation half-life means the zone more actively returns to its previous state after a perturbation, which is the operational signature of an $N$ attractor: a stable configuration that restores itself. This is not a claim about boundary positions; it is a claim about the functional character of the $N$ zone as a self-restoring state. The 100% pass rate on this test is the strongest single piece of evidence that the role assignment is structurally correct.

---

## 9. Discussion

### 9.1 Implications for architecture design

The structural derivations of Section 5 suggest three concrete directions for architecture design:

**Explicit D-component strengthening.** The universal C-dominance prediction implies that any architectural change that increases the relative weight of the $D$ components (LayerNorm, positional constraints, routing mechanisms) without proportionally increasing the $C$ components should move the architecture toward virial balance and produce more coherent phase structure. Architectural choices that have this effect include: increasing the number of normalization layers, using per-layer rather than input-only positional encoding, and adding routing constraints in MoE configurations.

**Virial balance as a training objective.** The virial regulariser (Section 5.3) is the most direct architectural intervention: it embeds the structural balance condition as a training signal. The framework predicts that a model trained with this regulariser will achieve virial balance by the end of training, regardless of its architectural starting configuration. This is a softer intervention than architectural modification: it adjusts the training dynamics rather than the forward pass structure.

**Depth optimisation via the tholonic formula.** The optimal-depth prediction (Section 5.4) provides a principled basis for choosing network depth given a target entropy reduction. Current depth choices are largely empirical (scale the model until performance saturates, then add more data). The formula $L^* = \log_\varphi(H_0/H_L)$ provides a structural basis for depth selection that does not require exhaustive scaling runs.

### 9.2 Relationship to alignment

Section 5.2 establishes that universal C-dominance is a structural prediction of the role assignment, not an empirical curiosity. This has implications for AI alignment that are worth stating explicitly.

Current alignment procedures (RLHF, Constitutional AI, RLAIF, DPO) all share a structural property: they add preference information to the model after the fact, via reward signals or preference data that modify the $C$ components (the attention and MLP weights) without correspondingly strengthening the $D$ components. This is not a design flaw; it is a consequence of how these procedures work. Preference learning operates by shaping what the model outputs ($C$ modification), not by strengthening what the model constrains itself to be ($D$ modification).

The tholonic framework predicts that this structural asymmetry is the root cause of the characteristic failure modes of post-trained models: specification gaming (the model satisfies the letter of the reward signal while violating its intent, because the $D$ constraint is too weak to enforce the intent), distributional fragility (the model's behavior degrades under distribution shift because its internal coherence is maintained by training-distribution $C$ patterns, not by structural $D$ constraints), and reward hacking (the model finds $C$-side loopholes in the reward function because the $D$-side constraints do not rule them out structurally).

The virial regulariser addresses this at the architectural level. By training the model with an explicit balance constraint, the $D$ component is strengthened relative to the $C$ component throughout training, not just at the post-training stage. The structural prediction is that a virial-balanced model is less susceptible to these failure modes, not because it has been more thoroughly aligned post-hoc, but because its internal constraint structure is intrinsically more robust.

### 9.3 Scope

This paper establishes a role assignment and derives structural predictions. It does not claim that the tholonic framework explains everything about transformer behavior, that the virial regulariser solves the alignment problem, or that the five constants are the only structurally significant features of transformer dynamics. The claims are narrower: if the role assignment of Section 4 is correct, the predictions of Section 5 must follow. [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) tests those predictions. The results are preliminary and all claims should be understood as structurally motivated hypotheses requiring independent verification.

---

## 10. Conclusion

This paper provides the missing middle step in the tholonic argument about neural networks. [Paper 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) establishes that five classical constants emerge from the N-D-C recurrence. [Paper 3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) establishes that three roles are the minimum for recursive self-organization. [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) measures phase boundaries empirically. What was missing was the formal argument that transformer architectures instantiate the N-D-C grammar, and that the empirical predictions therefore must follow structurally rather than coincidentally.

The central result (Proposition 3.1) is that the transformer forward pass satisfies all conditions of the formal tholonic recursion: hidden states are $N$, LayerNorm is $D$, Attention+MLP is $C$, and the three roles are functionally independent and irreducible. Given this assignment, five structural predictions follow directly: phase boundaries at the five constants in role-consistent positions, universal C-dominance in standard-objective-trained architectures, the form of the virial balance regulariser, and the optimal-depth formula. These are not post-hoc descriptions of observed patterns; they are derivations from the role assignment that [Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf) then tests empirically.

The logical chain is now complete. The mathematical foundation ([Papers 1](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [3](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf)), the formal domain mapping (this paper), and the empirical test ([Paper 10](https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf)) together form a coherent, falsifiable structural account of why transformer architectures organize their internal dynamics the way they do, and what architectural changes would make them more stable, more interpretable, and more robustly aligned.

---

## References

[Mil26a] Milton, J. W. *Emergence of Classical Constants from a Minimal Recursive Triadic Framework.* Clarity Coalition, paper 1 in this series, 2026.

<https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf>

[Mil26b] Milton, J. W. *Phase-Resolved Transparency Classification in Commodity Supply Chains: A Structural Triadic Scoring Framework (TVPCI).* Clarity Coalition, paper 2 in this series, 2026.

<https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.pdf>

[Mil26c] Milton, J. W. *A Minimal Recursive Triadic Framework for Self-Similar Hierarchical Systems.* Clarity Coalition, paper 3 in this series, 2026.

<https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf>

[Mil26d] Milton, J. W. *Neural Networks as Tholonic Systems: A Structural Framework for Architecture, Scaling, and Alignment-by-Design.* Clarity Coalition, paper 10 in this series, 2026.

<https://github.com/baardev/truevalue/raw/main/docnav/Research/papers/10_tholonic-neural-architecture/10_tholonic-neural-architecture.pdf>

[VSP17] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., Polosukhin, I. *Attention Is All You Need.* NeurIPS 2017.

[RNS+18] Radford, A., Narasimhan, K., Salimans, T., Sutskever, I. *Improving Language Understanding by Generative Pre-Training.* OpenAI Technical Report, 2018.

[BMRS20] Brown, T., Mann, B., Ryder, N., et al. *Language Models are Few-Shot Learners.* NeurIPS 2020.

[BA16] Ba, J., Kiros, J., Hinton, G. *Layer Normalization.* arXiv:1607.06450, 2016.

[ZSA+22] Zhang, B., Sennrich, R. *Root Mean Square Layer Normalization.* NeurIPS 2019.

[SLP+22] Shazeer, N. *Mixture of Experts.* Various; see Fedus, W., Zoph, B., Shazeer, N. *Switch Transformers.* JMLR, 2022.

[JGS+21] Jiang, A. Q., et al. *Mistral 7B.* arXiv:2310.06825, 2023.

[Sha48] Shannon, C. E. *A Mathematical Theory of Communication.* Bell System Technical Journal, 27(3):379–423, 1948.

---

*End of paper.*
