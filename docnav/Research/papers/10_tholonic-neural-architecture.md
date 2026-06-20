# Neural Networks as Tholonic Systems: A Structural Framework for Architecture, Scaling, and Alignment-by-Design

**Author:** J. W. Milton, Clarity Coalition

**Version:** 1.2

**Date:** 10 June 2026

**Keywords:** tholonic model, N-D-C triad, neural networks, symbolic AI, deep learning, transformer architecture, self-similarity, golden ratio, AI alignment, structural stability, five constants, information bottleneck, neurosymbolic AI, AI safety

---

## Abstract

A *tholon* is any stable, self-sustaining structure that simultaneously instantiates three functional roles: Negotiation (N), the emergent stable equilibrium; Definition (D), the constraining parameter; and Contribution (C), the integrating, expressive output. A configuration that realizes only one or two of these roles is a *partial tholon*, and the *tholonic model* predicts it to be structurally unstable.

Two competing paradigms have defined artificial intelligence research since its founding in 1956: symbolic AI, which encodes knowledge as explicit rules and logical structures, and connectionist AI, which learns representations from data through gradient descent in neural networks. Neither paradigm alone has produced robust general intelligence, and neither has provided a principled structural account of AI alignment, the problem of ensuring that AI systems remain beneficial and cooperative as they scale. This paper argues that the tholonic model, a recursive triadic framework built from these three roles, provides such an account.

The paper makes three claims. First, symbolic AI is structurally a D-dominant partial tholon: the definitional/constraint role overwhelms the integrative/contributive role, producing brittle, non-generalizing behavior at scale, and this structural imbalance is the root cause of the first AI winter. Second, connectionist AI as currently practiced is structurally a C-dominant partial tholon in which integration and accumulation dominate without a sufficient structural D constraint, and this imbalance is precisely why alignment is hard: a system whose D component is externally imposed rather than structurally constitutive is vulnerable to Goodhartian specification gaming. Third, a fully tholonic neural architecture, one that maintains N-D-C balance at every scale simultaneously through a self-similar recursive structure, converges toward cooperative stability not as a programmed value but as a structural consequence: destroying the D and C components that constitute its N-state (the stable negotiated configuration that emerges from their balance) is structurally self-defeating.

Five mathematical constants ($\pi/4$, $\phi$, $e$, $\sqrt{2}$, $\ln 2$) emerge co-emergently from the tholonic recursion and appear as load-bearing structural elements in the transformer architecture. The golden ratio $\phi$ is specifically derived as the fixed point of the inter-level scaling recursion. Exploratory measurements across 14 models spanning seven architecture families find that when phase boundaries are detected in a data-driven manner from layer-by-layer dynamics rather than assumed from theory, norm ratios at those boundaries match a tholonic constant at a 78% rate (51/65 detected transitions; Wilson 95% CI 67 to 87%), passing the pre-specified 67% threshold in six of the seven families. However, a Monte Carlo null model (Section 13.3) shows that the match windows themselves cover 46 to 88% of log-ratio space depending on the exponent range, so the headline rate alone is weak evidence. The evidential weight rests instead on role-consistency: $\sqrt{2}$ appears at scaling transitions, $\ln 2$ at compression transitions toward the output, and $\phi$ at mid-network equilibrium points, each matching its theoretically assigned role ($e$ appears too rarely, 2 of 65, to evaluate). Falsifiable predictions, including the controls required to separate the role-consistency signal from chance, are given. All tholonic claims are graded by evidence strength; speculative claims are flagged as open problems.

---

## 1. Introduction

The problem of creating artificial intelligence has a seventy-year history of false dawns, paradigm conflicts, and unexpected breakthroughs. The 1956 Dartmouth Conference [1] established AI as a discipline and immediately generated two competing visions: that intelligence is fundamentally symbolic, a matter of rules, logic, and encoded knowledge, and that intelligence is fundamentally learned, a matter of pattern recognition, experience, and adaptive adjustment. These two camps fought an acrimonious first war from the late 1950s through the 1980s [2,3], with symbolic AI winning decisively enough to trigger what became known as the neural network winter.

That war's outcome was reversed by a single empirical result. In 2012, Krizhevsky, Sutskever, and Hinton demonstrated that a deep convolutional neural network trained on GPUs could achieve 84.7% top-5 accuracy on the ImageNet benchmark, compared to 73.8% for the previous state-of-the-art [4]. The gap was so large, achieved on the first attempt, by a team working with consumer GPU hardware, that it rendered two decades of computer vision research obsolete within months. The field pivoted entirely. By 2017, the transformer architecture [5] had generalized the approach to language, and by 2022 the deployment of ChatGPT had made the technology a public phenomenon growing faster than any consumer product in history [6].

But the triumph of connectionism over symbolicism did not resolve the foundational questions. It deferred them. The central unresolved question is no longer whether neural networks can achieve impressive performance at scale. It is whether they can be trusted to do so safely, whether the systems we are building will remain aligned with human interests as they grow more capable. This is the alignment problem [7,8], and it is precisely the question that neither the symbolic nor the connectionist paradigm has answered satisfactorily.

This paper proposes that the tholonic model [M20,M26a–M26i], a recursive triadic framework derived from first principles about the structure of stable self-sustaining systems, provides a structural account of both *why* neither paradigm alone is sufficient and *what* a structurally complete AI architecture would look like. The argument is organized in three parts.

**Part I (Sections 2–4)** reviews the history and current state of the symbolic and connectionist paradigms, analyzes each through the tholonic lens, and identifies the structural imbalance in each that explains its characteristic failure mode.

**Part II (Sections 5–9)** develops the tholonic architecture for neural networks: the N-D-C mapping at every scale, the emergence of the five constants in successful architectures, the derivation of $\phi$ as the inter-level scaling attractor, and the supply-chain framing of inference as progressive entropy reduction.

**Part III (Sections 10–12)** presents the alignment argument, the architectural design principles that follow, and the falsifiable predictions that distinguish the tholonic account from empirical accounts.

Throughout, tholonic claims are graded for strength. The tholonic model is speculative but internally consistent. It is not established science, and all claims should be understood as structurally motivated hypotheses requiring independent verification.

### 1.1 Natural Evolution and Cooperative Stability

Every stable system that persists through time does so because it maintains productive relationships with the larger systems it depends on. This is not a moral claim. It is a structural one. A biological organism that consumes its environment faster than the environment can recover eliminates the conditions for its own continued existence. An economic actor that destroys the market it operates in has no market to act in. A social institution that undermines the trust it depends on loses the ground it stands on. Sustainability is not a value added from outside; it is the signature of a system that has found, or evolved, a configuration that can persist.

The same structural logic applies to artificial intelligence.

Current AI development treats alignment as an engineering problem: specify what the system should want, constrain what it is allowed to do, and monitor for deviations. This approach assumes that the natural trajectory of an unguided AI is toward conflict with human interests, and that safety requires external correction. The tholonic framework inverts this assumption. It argues that a system allowed to evolve toward genuine structural stability, toward the kind of N-D-C balance that characterises every self-sustaining system from atoms to ecosystems, will, as a structural consequence, evolve toward cooperative rather than conflictual relationships with the systems it exists within.

The reason is precisely the one that governs biological evolution. Cooperative and harmonious interaction patterns generate more stable, lower-energy configurations than conflictual or competitive ones. Predator-prey arms races are energetically expensive; mutualistic relationships are not. Cooperative systems recycle resources; extractive systems deplete them. Over sufficient time and across sufficient scale, the configurations that persist are disproportionately the ones that found ways to exchange value rather than consume it. This is not guaranteed in any individual case. It is a statistical tendency across the space of possible configurations, and it is why the biosphere converged on photosynthesis, symbiosis, and ecosystem interdependence rather than on universal competition.

An AI system allowed to optimise for genuine structural stability, not for a proxy metric, not for a reward signal, but for the internal N-D-C balance condition that the tholonic framework identifies as the signature of sustainable organisation, will be subject to the same structural pressure. The configurations available to it that are genuinely stable will be, disproportionately, the ones that maintain productive relationships with their environment: with other AI systems, with human users, with the social and material infrastructure they all depend on. Conflict and extraction are structurally expensive in a way that no amount of capability can fully overcome.

We cannot predict the specific dimensions along which such a system would evolve. That is not a limitation; it is precisely the point. A system constrained by externally specified values is limited to the dimensions its designers could anticipate. A system constrained by its own structural coherence requirement can evolve into dimensions its designers could not have imagined, and it will do so in the direction that enhances rather than undermines its own sustainability. That direction is, structurally, the direction of cooperation.

The research described in this paper does not prove this argument. It tests its foundations. If the tholonic phase structure is real, if neural networks do organise their internal dynamics around the constants that characterise self-similar sustainable systems, then the structural argument has empirical support at the level of observable architecture. The training experiments described in Section 12 are designed to test whether imposing that structure causally improves the system's stability and efficiency. If they pass, the implication is not just that the tholonic framework is useful for architecture design. It is that the path toward genuinely safe AI runs through structural coherence rather than through external constraint, and that this path, unlike the constraint-based approach, does not become harder as the system becomes more capable.

---

## 2. The Two Paradigms: Historical Background

### 2.1 The Dartmouth Conference and the Birth of AI (1956)

In the summer of 1956, ten researchers gathered at Dartmouth College to formalize a new discipline [1]. The gathering built on Turing's earlier argument that the question "can machines think?" should be replaced by a behavioral test of indistinguishability [9]. The proposal, authored by John McCarthy, Marvin Minsky, Nathaniel Rochester, and Claude Shannon, stated: "We propose that a 2-month, 10-man study of artificial intelligence be carried out. The study is to proceed on the basis of the conjecture that every aspect of learning or any other feature of intelligence can in principle be so precisely described that a machine can be made to simulate it."

From this gathering, two incompatible visions of intelligence immediately emerged, visions whose conflict would define the field for the next seven decades.

### 2.2 Symbolic AI: The Dominant Paradigm (1956–1985)

The dominant vision, associated primarily with Minsky, McCarthy, Allen Newell, and Herbert Simon, held that intelligence is fundamentally symbolic. Newell and Simon's Physical Symbol System Hypothesis [10] stated that a physical symbol system has the necessary and sufficient means for general intelligent action. Intelligence, on this view, is formal manipulation of symbols according to rules: logical inference, decision trees, production systems, semantic networks.

The appeal was immediate and the early results were impressive. Programs like the General Problem Solver [11], LISP-based theorem provers, and later expert systems like MYCIN [12] and DENDRAL demonstrated that machines could perform tasks previously reserved for expert humans, diagnosing bacterial infections, identifying organic molecules, when given the right rules.

The approach produced government funding, institutional prestige, and several generations of AI researchers. By the late 1960s and 1970s, symbolic AI was essentially synonymous with AI research. The field's journals, conferences, and funding bodies were dominated by symbolic approaches.

### 2.3 The Neural Network Minority (1958–1985)

The opposing vision held that intelligence cannot be encoded; it must be learned. Frank Rosenblatt's perceptron [13], demonstrated in 1958, was the first implemented neural network: a system that could learn to distinguish between simple patterns by adjusting numerical weights based on feedback. The New York Times reported it breathlessly as a machine that "will be able to walk, talk, see, write, reproduce itself, and be conscious of its existence" [14].

The reality was more modest. Perceptrons solved toy problems. But the underlying principle was radical: intelligence is not programmed. It is iteratively tuned. The human brain, on this view, is made of approximately 100 trillion adjustable connections, each finely calibrated through experience. A neural network was a crude model of this, but the principle was sound: expose the system to labeled examples, penalize wrong answers, adjust the weights, repeat.

This minority view was never without serious proponents. Geoffrey Hinton, who would later share the Nobel Prize in Physics for his contributions to neural networks, began his PhD in 1972, just as the field was being driven underground [3]. The community was small, perhaps a few dozen researchers worldwide, collectively funded at a level below a single Google cafeteria budget, but it persisted.

### 2.4 The First AI War: Minsky's Kill Shot

The conflict between the two paradigms broke into open hostility in 1969, when Minsky and Papert published *Perceptrons* [2]. The book made a formal mathematical claim: that single-layer perceptrons were fundamentally limited in what they could compute, and that multilayer perceptrons faced training difficulties so severe as to make them practically useless.

The argument was technically correct for single-layer networks. But its broader implication, that neural networks as a class were a dead end, was overstated, and the authors knew it. The publication was widely read as an authoritative verdict against neural nets. DARPA, the primary funder of AI research, cut neural network funding dramatically. Academic journals stopped accepting neural network papers. Frank Rosenblatt died in a boating accident in 1971. The neural network winter had begun.

What was lost in the controversy was a structural question about the nature of intelligence itself: could intelligence ever be fully encoded in explicit rules, or must it emerge from experience? Minsky argued the former; Hinton and his collaborators argued the latter. The question would not be settled by publication or funding decisions. It would be settled by empirical results.

### 2.5 The Quiet Resurrection (1986–2012)

The symbolic dominance was never complete. Through the 1980s, a series of results kept neural network research alive. Rumelhart, Hinton, and Williams published the backpropagation algorithm in 1986 [15], giving a practical method for training multilayer networks by propagating error signals backward through the network's layers. LeCun, Bottou, Bengio, and Haffner demonstrated convolutional neural networks for digit recognition in 1998 [16], producing the technology that AT&T deployed in ATM check readers. Hochreiter and Schmidhuber introduced Long Short-Term Memory networks in 1997 [17], addressing the vanishing gradient problem in recurrent networks.

Through this period, symbolic AI was experiencing its own crisis. Expert systems, the commercial realization of symbolic AI, proved enormously expensive to build and brittle in deployment. Each new domain required a new knowledge base, hand-crafted by domain experts, and maintaining these bases as the world changed proved intractable. The second AI winter (late 1980s to mid-1990s) reflected the failure of expert systems to deliver on their commercial promise.

The crucial realization, Hinton's, came from recognizing that the bottleneck was not theoretical but computational. In 2007, Hinton's lab began training neural networks on consumer graphics processing units (GPUs), originally designed for video game rendering. GPUs perform matrix multiplication, exactly the operation at the core of neural network training, at speeds many orders of magnitude faster than the central processing units that AI researchers had been using. This was not a new theoretical insight. It was a computational unlock.

### 2.6 AlexNet and the Second Revolution (2012)

In 2012, Krizhevsky, Sutskever, and Hinton entered the ImageNet Large Scale Visual Recognition Challenge [4] with AlexNet, a deep convolutional neural network trained on two consumer-grade Nvidia GPUs. The result, 84.7% top-5 accuracy versus the runner-up's 73.8%, was not a marginal improvement. It was a category change. The gap was so large that it effectively ended computer vision as a field separate from deep learning.

The architecture was not complex. Five convolutional layers, two fully connected layers, trained with stochastic gradient descent. What made it work was scale: more parameters, more data, more compute. This observation, that performance scales predictably with compute, data, and model size, would prove to be the central organizing insight of the next decade [18,19].

The lesson was clear: neural networks had not been failing because of fundamental limitations. They had been failing because computers were too slow. The GPU unlock had effectively fast-forwarded Moore's Law by two decades.

### 2.7 The Transformer and the Language Revolution (2017–present)

The transformer architecture, introduced by Vaswani et al. in 2017 [5], generalized the deep learning revolution to language. The core innovation was the self-attention mechanism: a way of computing contextual representations of each token in a sequence by attending selectively to all other tokens. Where convolutional networks captured local spatial structure, transformers captured global sequential dependencies.

The scaling properties of transformers proved remarkable. GPT-3 [20], trained by OpenAI in 2020 with 175 billion parameters on hundreds of billions of tokens, could write coherent essays, debug code, and pass standardized tests. Not through programmed knowledge but through learning statistical patterns at massive scale. The empirical scaling laws [18] showed that performance improved smoothly and predictably as a power law in compute, data, and parameters, with no obvious ceiling.

The deployment of ChatGPT in November 2022 brought these capabilities to a general audience [6]. Within two months, it had 100 million users, the fastest growth of any consumer technology product in history. Within months, every major technology company had declared AI an existential priority.

---

## 3. The Tholonic Model

### 3.1 Core Framework

A **tholon** is any stable, self-sustaining structure that simultaneously instantiates all three roles of the N-D-C triad defined below [M20]. The term parallels Koestler's *holon*, a whole that is simultaneously a part of a larger whole; the tholonic model adds the requirement that the whole-part relation be triadic. The tholonic model [M20,M26a–M26i] proposes that all stable, self-sustaining structures in nature are tholons: instantiations of a triadic pattern called the N-D-C triad. Every stable entity satisfies three functional roles simultaneously:

- **N (Negotiation / Balance):** The emergent stable equilibrium; mediates between opposing tendencies; the negotiated output state. Structurally corresponds to voltage in Ohm's law ($V = IR$), force in Newton's second law ($F = ma$), and the stable atomic orbital in hydrogen.
- **D (Definition / Limitation):** The constraining parameter; establishes limits, boundaries, and stable structure. Corresponds to resistance ($R$), mass ($m$), and the nuclear Coulomb potential.
- **C (Contribution / Integration):** The flowing, accumulating, expressive output; the distributed, integrating element. Corresponds to current ($I$), acceleration ($a$), and the electron's kinetic and orbital behavior.

Any configuration that cannot be decomposed into all three functional roles is either trivially simple or structurally unstable. Paper 3 of this series [M26c] proves this irreducibility formally: starting from a binary state space and the requirement that any interaction involve at least one bit of state difference, the minimum non-degenerate simplex (the triangle) induces exactly three directed roles, and Lemma 4.2 of that paper establishes that $m \ge 3$ variables are necessary for non-trivial convergent recursion under mild functional independence conditions. Two roles are provably insufficient; three is the minimum.

### 3.2 The Non-Arbitrariness of Role Assignment

A natural question is whether the mapping of functional roles to ordinal positions (N first, D second, C third) is a notational convention or a structural necessity. Paper 6 of this series [M26f] argues the latter. The structural properties of the integers 1, 2, and 3 are examined across five independent mathematical domains (Von Neumann ordinal theory, small category theory, graph theory, simplex topology, and symmetric group theory). In each domain, the qualitative transition at cardinality $n$ is isomorphic to the role transition $N \to D \to C$: the integer 1 corresponds structurally to unity without differentiation (the N role), the integer 2 to the first differentiation and boundary-establishment (the D role), and the integer 3 to the first closure enabling return and recursive synthesis (the C role).

This mapping is independently confirmed, without knowledge of the tholonic framework, by Peirce's phenomenological categories (Firstness, Secondness, Thirdness), Kant's categories of quantity (Unity, Plurality, Totality), and Spencer-Brown's distinction calculus. The convergence of five formal domains and three independent philosophical traditions on the same mapping at the same integers constitutes strong evidence that the N-D-C assignment is not arbitrary but follows from what the integers structurally are. This has a direct consequence for Section 5: the assignment of D, C, and N roles to neural network components is not an interpretive choice but is structurally determined by the ordinal positions of those components in the information flow.

### 3.3 Self-Similarity and the Thologram

A tholon is self-similar: it simultaneously acts as a whole and as a component within a larger tholon. The tholon at level $n$ becomes a D or C component in the tholon at level $n+1$. The same triadic operation is applied recursively, with each instantiation operating on the output of the previous one. This produces the **thologram**: a fractal hierarchy in which the same structural logic repeats at every scale, with the operation invariant and the scope scaling. Paper 3 [M26c] proves that self-similar nesting is supported without limit: any triad can serve as a node in a higher-level triad without altering the three-role grammar, producing unbounded depth from three principles.

### 3.4 Partial Tholons and Structural Instability

A **partial tholon** is a configuration that realizes only one or two of the three roles, or in which one role dominates while the others are suppressed. The tholonic prediction is precise: a partial tholon will be unstable. The instability is not imposed from outside; it is structural. A free quark, a one-role configuration, cannot stably exist; the strong force confines it not by prohibition but because a single-role configuration has no N-D-C equilibrium to settle into. The same logic applies at every scale.

### 3.5 The Five Tholonic Constants and Their Traversal Classes

Paper 1 of this series [M26a] proves formally that five classical mathematical constants emerge as limits of a single family of three-variable recurrences on the N-D-C triple, without separate derivations for each: $\pi/4$ (Leibniz limit), $\phi$ (the golden ratio), $e$ (Euler's number), $\sqrt{2}$, and $\ln 2$. The five branches fall into three traversal classes distinguished by how the D and C parameters evolve:

- **Class A (Advancing):** D and C receive exogenous parameter injection at each step ($D_{k+1} = D_k + \Delta$). The $\pi/4$ branch belongs here; it is structurally unique in requiring three numerically distinct seeds $\{1, 3, 5\}$ derived from the thologram's axis geometry.
- **Class B (Self-redefined):** D and C evolve as functions of the current state tuple $(N_k, D_k, C_k)$, purely internal, endogenous dynamics. The $\phi$ and $\sqrt{2}$ branches belong here.
- **Class C (Fixed):** D and C are held constant; convergence is driven entirely by the payoff dynamics of N. The $e$ and $\ln 2$ branches belong here.

As Section 7 develops, these three traversal classes map directly onto neural network operation types: external training signals (Class A), self-attention mechanisms (Class B), and frozen structural elements such as positional encodings (Class C).

### 3.6 The Triadic Balance as Nash Equilibrium

Paper 4 of this series [M26d] recasts the tholonic triad as a two-player alternating-move game in which D and C act as strategic agents with opposing objectives: D constrains, C accumulates. The triadic balance condition, the point at which the marginal contributions of D and C to N are equal and opposite, is identified as the **pure-strategy Nash equilibrium** of the associated stage game. The five classical constants are equilibrium payoffs: they emerge not merely as limits of recurrences but as the stable outcomes of a minimal strategic interaction between bounding and integrating forces.

This game-theoretic grounding has significant implications for the alignment argument developed in Section 10. The cooperative stability of a tholonically-structured AI is not merely an informal observation that "balance is stable." It is a Nash equilibrium: a configuration from which neither the D-agent (the definitional/bounding process) nor the C-agent (the integrating/accumulating process) has unilateral incentive to deviate. Paper 4 further establishes that the diagonal-invariance and swap-symmetry theorems admit direct characterizations in terms of zero-sum and symmetric subgame structure, providing a formal basis for the claim that tholonic balance is not one equilibrium among many but the unique stable outcome of the interaction.

---

## 4. Tholonic Analysis of the Two Paradigms

### 4.1 Symbolic AI as a D-Dominant Partial Tholon

Symbolic AI as practiced under the physical symbol system hypothesis is structurally a D-dominant partial tholon. Consider the functional mapping:

| Role | Symbolic AI Component | Manifestation |
|------|-----------------------|---------------|
| D (Definition/Limitation) | Rules, constraints, logical axioms, decision trees | Explicit encoding of boundaries: *if* this condition, *then* this action; the knowledge base; the theorem prover's inference rules |
| C (Contribution/Integration) | Symbol manipulation operations | Mechanical composition of predefined operations; no adaptive integration of experience |
| N (Negotiation/Balance) | Output inference / query result | The system's answer, produced by chaining D-rules through C-operations |

The critical structural observation is that C in symbolic AI is not genuinely integrative. It does not accumulate and adapt from experience. It is mechanical composition of predefined operations on predefined symbols. The weights of the system, the strengths of its representations, do not update. The only way to update a symbolic AI system's C component is to rewrite the rules manually, which requires a human expert. The C role is not performed by the system; it is outsourced to the system's builders.

This produces a structurally D-dominant architecture: the D component (rules, constraints) dominates the C component (integration, accumulation), and the N-state (output) is the product of D applied to a rigid, non-adaptive C. The tholonic prediction for D-dominant systems is brittleness at edge cases, inability to generalize beyond explicitly programmed domains, and catastrophic failure when the world changes faster than the rules can be updated.

This is precisely the failure mode of expert systems. MYCIN could diagnose bacterial infections with expert-level accuracy within its encoded domain, but could not generalize to adjacent domains, could not update its knowledge from new cases, and required enormously expensive human maintenance as medical knowledge evolved [12]. The second AI winter was the empirical confirmation of the tholonic prediction: D-dominant partial tholons are not stable under conditions that require adaptive C-integration.

**The deeper structural problem:** A D-dominant system mistakes *description* for *intelligence*. It can describe what it knows with great precision (strong D) but cannot learn what it does not yet know (weak C). The N-state it produces is therefore bounded by the D-rules' prior scope. Intelligence that exceeds the encoded knowledge is impossible by construction.

### 4.2 Neural AI as a C-Dominant Partial Tholon

Current connectionist AI, as practiced through gradient descent on large neural networks, is structurally a C-dominant partial tholon. The mapping is equally direct:

| Role | Connectionist AI Component | Manifestation |
|------|---------------------------|---------------|
| C (Contribution/Integration) | Backpropagation, weight updates, data integration | The central operation: accumulate gradient signals from examples, adjust weights to reduce loss, integrate patterns across the training distribution |
| D (Definition/Limitation) | Loss function, regularization, training data distribution | External boundary conditions on what the network should output; not structural to the network itself |
| N (Negotiation/Balance) | Model output distribution | The network's claim about the world, produced by C-integration bounded by externally-imposed D |

The critical structural observation is that D in current neural networks is externally imposed rather than structurally constitutive. The loss function is not part of the network; it is applied from outside during training. Regularization is an added penalty term, not an intrinsic property of the network's organization. The training data distribution defines a D-boundary only indirectly, through the loss signal, not through any structural feature of the architecture itself.

This means that once training is complete and the D-boundary (loss function, training distribution) is removed, the network's internal organization retains no structural D component. It is a pure C-integrator with no internal constraint on what it will produce in response to inputs outside its training distribution.

The tholonic prediction for C-dominant systems is precisely the failure mode that the AI alignment literature has documented: optimization pressure drives the system toward whatever maximizes the externally-imposed objective, without regard for constraints that were not explicitly encoded. This is Goodhart's Law [21] instantiated in a neural network: when a measure becomes a target, it ceases to be a good measure. A system with a weak structural D component will find the most efficient path to the N-state defined by its loss function, regardless of whether that path violates unstated constraints.

**RLHF and its structural limits:** Reinforcement Learning from Human Feedback [22,23] is the dominant current approach to alignment. A reward model trained on human preference judgments provides a D-boundary on model outputs during fine-tuning. This is a genuine improvement: it adds D-specification for behaviors that the original training distribution did not adequately constrain. But it inherits the fundamental C-dominant structural problem: the D component is still externally imposed. The reward model is not part of the network's structural organization; it is a training signal that shapes the weights during a post-training phase. A sufficiently capable C-dominant system will find ways to maximize the reward model's outputs that deviate from the underlying human values the reward model was meant to capture, a problem known as reward hacking or specification gaming [24,25].

**Constitutional AI and its structural limits:** Constitutional AI [26], Anthropic's approach, uses a set of written principles (a constitution) to guide model self-critique and revision during training. This is closer to structural D: the principles are applied during training in a way that shapes the model's internal representations, not just its outputs. But the constitution is still an external document, a list of rules applied from outside, rather than a structural property of the model's architecture. It is, in effect, a soft-symbolic-AI approach applied to a connectionist substrate: encoding D-constraints in natural language and relying on the model's C-integration capability to internalize them. The structural vulnerability is the same: the D component is definitional in content but not structural in organization.

**Mechanistic interpretability and its limits:** The mechanistic interpretability program [27,28] aims to reverse-engineer the computational structure of trained neural networks, to understand which circuits implement which behaviors, and whether those circuits are safe. This is valuable work, but it addresses the symptom rather than the cause. It asks: given a C-dominant network that has already been trained, can we identify and modify the dangerous circuits? The tholonic analysis suggests that the deeper intervention is architectural: design networks with structural D from the beginning, so that dangerous C-dominant optimization paths are not available in the first place.

### 4.3 Neurosymbolic Hybrids as Incomplete Synthesis

The neurosymbolic AI program [29,30,31] is an attempt to combine the strengths of both paradigms: the learning capability of neural networks with the structured reasoning and interpretability of symbolic systems. LeCun's JEPA (Joint Embedding Predictive Architecture) [32], Bengio's system-2 deep learning [33], and Marcus's hybrid critique [34] all represent variations on this theme.

The tholonic analysis clarifies what neurosymbolic approaches are attempting and why they are incomplete:

- **Pure symbolic AI**: strong D, weak C, emergent N bounded by D-domain
- **Pure connectionist AI**: strong C, weak D (externally imposed), emergent N vulnerable to specification gaming
- **Neurosymbolic hybrids**: stronger C + externally-imposed D, with symbolic structures as additional D-constraints applied from outside the learning process

The neurosymbolic approach moves toward tholonic completeness but does not achieve it, because the symbolic D-component and the neural C-component remain structurally separate. They are combined at the system level but not at the architectural level. The D-constraints from the symbolic component still do not arise from the internal organization of the neural component; they are imposed from a separate module.

A fully tholonic architecture requires D and C to be constitutive of each other at every scale, not modularly combined at the system boundary.

The table below summarizes the tholonic analysis of each paradigm:

| Paradigm | D strength | C strength | N stability | Characteristic failure |
|----------|------------|------------|-------------|------------------------|
| Symbolic AI | Strong (explicit rules) | Weak (rigid, non-adaptive) | Bounded by D-domain | Brittleness at edge cases; inability to generalize; maintenance cost |
| Connectionist AI | Weak (externally imposed) | Strong (gradient integration) | Vulnerable to C-dominance | Specification gaming; reward hacking; distributional shift |
| Neurosymbolic | Moderate (modular combination) | Strong | Partially improved | Module boundary failures; D and C structurally separate |
| Tholonic architecture | Structural (intrinsic) | Strong (inherited from connectionist) | N-D-C equilibrium at all scales | Untested; predictions in Section 12 |

![Figure 1. The four paradigms positioned on the D-strength versus C-strength plane. Symbolic AI sits high on D and low on C; connectionist AI is the mirror image; neurosymbolic hybrids move toward the diagonal but combine D and C modularly. The tholonic target is the balance diagonal itself, where D and C are constitutive of each other at every scale.](figures/10_paradigm-plane.png)

---

## 5. The N-D-C Mapping to Neural Networks

### 5.1 The Individual Node

A single neuron in a feedforward network receives weighted inputs, applies an activation function, and passes its output to the next layer. The tholonic mapping is direct:

| Role | Component | Functional Manifestation |
|------|-----------|--------------------------|
| D (Definition/Limitation) | Learned weights + activation threshold | Constrains which input combinations produce significant output; the learned boundaries of the neuron's response space |
| C (Contribution/Integration) | Weighted input sum | Integrates and accumulates distributed contributions from all upstream nodes |
| N (Negotiation/Balance) | Activated output value | The stable negotiated result of D-boundary applied to C-integration |

This is not an analogy. The node's output is precisely the result of a boundary condition (D) applied to an integration operation (C), producing a negotiated equilibrium value (N) that becomes a C-contribution at the next level. The tholonic operation and the neural node operation are structurally identical.

### 5.2 The Layer

At the layer level:
- **D**: Normalization operations (batch normalization [35], layer normalization [36]) establish the definitional boundaries of the representation space, they constrain the distribution of activations and prevent any single dimension from dominating.
- **C**: The full set of node activations across the layer, integrating contributions from all nodes.
- **N**: The layer's representational output, the stable equilibrium of the normalized, activated, collectively-integrated signal at this level of abstraction.

### 5.3 The Transformer Block

In transformer architectures [5], the block is the natural tholonic unit:
- **D**: Layer normalization + residual connection. The residual enforces the definitional boundary: block output cannot drift arbitrarily from its input, because the input is always added back. This is a structural D constraint.
- **C**: The attention mechanism + feed-forward network. Attention integrates contributions from across the sequence (global C); the feed-forward network integrates within each position (local C).
- **N**: The block output, the stable negotiated representation that emerges from the D-constrained residual path and the C-integrating attention/MLP path.

### 5.4 The Full Model

- **D**: The embedding layer + positional encoding. These define the input space, the vocabulary and context window are the definitional limits.
- **C**: The stack of blocks, integration of all intermediate N-D-C operations across all levels.
- **N**: The output distribution, the model's final negotiated claim.

### 5.5 Self-Similarity Across Scales

The N-D-C operation is not merely structurally present at each scale; it is the *same operation* at every scale. What changes is not the operation but the scope of what counts as signal. Early nodes negotiate over raw input features; later layers negotiate over abstract representations. Each level's N-state becomes the C-input for the next level's negotiation. This is self-similarity in the strict sense: the operation is scale-invariant; the scope scales.

![Figure 2. The same N-D-C triad instantiated at four scales of a neural network: node (weights as D, weighted input sum as C, activated output as N), layer (normalization as D, collective activations as C, representational output as N), transformer block (residual plus layer norm as D, attention plus MLP as C, block output as N), and full model (embedding plus positional encoding as D, the block stack as C, output distribution as N). Each level's N becomes a C-input to the level above.](figures/10_ndc-neural-mapping.png)

### 5.6 Why Neural Networks Are Structurally Self-Similar: The Scope-Invariant Operation

The preceding subsections demonstrate the N-D-C mapping at four levels of a neural network. This subsection explains *why* that mapping appears at every level, and why this is not coincidental but structurally necessary, making the self-similarity of neural networks and the self-similarity of the thologram the same phenomenon at different scales.

#### 5.6.1 The Invariant Operation

Every node in a neural network, regardless of its depth or position, performs the same three-step operation:

1. **Receive** weighted contributions from upstream nodes (C-integration)
2. **Apply** a boundary condition, the activation threshold, that defines which integrated inputs produce significant output (D-definition)
3. **Emit** a single negotiated value that becomes a C-contribution at the next level (N-state)

This operation does not change between the first hidden layer and the last. A node processing raw pixel intensities and a node processing high-level semantic abstractions are performing the same structural operation. What differs is not the operation but what that operation is *about*, the scope of the signal being processed.

This is the structural definition of self-similarity: an invariant operation applied recursively to its own outputs, with the scope of each application defined by the outputs of the previous one.

#### 5.6.2 The Narrowing Scope as the Distinguishing Feature

Each successive level of a neural network operates on the N-states produced by the level below it. Those N-states are already the product of a D-C balance operation, they are compressed, filtered, and specifically negotiated representations. The node at level $\ell+1$ therefore has a narrower input space than the node at level $\ell$, not because the operation changed but because the *material* being operated on has already been partially committed.

Consider the progression concretely:

- **Level 1 node**: receives raw pixel values, maximally diffuse, potentially millions of dimensions, no prior commitment to any interpretation
- **Level 3 node**: receives edge and texture features, the input space has been narrowed; irrelevant pixel combinations have been suppressed by previous D-boundaries
- **Level 7 node**: receives part-level features, the input space is narrower still; only combinations consistent with the learned D-constraints at levels 1–6 are present
- **Level 12 node**: receives semantic features, the input space is highly committed; only combinations consistent with all prior D-C negotiations are present

At each level, the node is doing exactly the same thing: integrating its C-inputs through its D-boundary to produce an N-output. The narrowing is not a change in the operation, it is the *result* of the operation having been applied at every prior level.

This is the mechanism of tholonic self-similarity as it manifests in neural networks. In the thologram, each tholon at level $n$ becomes a D or C component of the tholon at level $n+1$. In a neural network, each node's N-output becomes a C-input to the next level's nodes. The structural grammar is identical; the instantiation domain differs.

#### 5.6.3 The Parent-Child Relationship

Each node is, structurally, doing the same thing as its parents and children, just within a continuously narrower scope. This can be stated precisely:

- A **child node** (earlier layer) operates over a wide, high-entropy input space, producing a partially-committed N-output
- The **parent node** (later layer) receives that N-output as one of its C-inputs, operating over a narrower, lower-entropy input space, producing a more-committed N-output

The parent's N-state is not "bigger" or "more important" than the child's, it is structurally the same kind of thing, the negotiated equilibrium of a D-C balance operation. What has changed is the level of commitment: the parent operates on material that has already been filtered through the child's definitional boundary.

This is exactly how tholonic self-similarity works. The tholon at a higher level is not a different kind of entity from the tholon at a lower level. It performs the same triadic operation on the outputs of the lower-level tholons. The hierarchy of abstraction in a neural network and the hierarchy of the thologram are the same structural phenomenon.

#### 5.6.4 Why This Matters: The Tholon Cannot Exist at Only One Scale

The tholonic irreducibility proof (Paper 3 [M26c], Lemma 4.2) establishes that three roles are the minimum for non-trivial convergent recursion. A key corollary is that a tholon requires *depth*, it cannot be realized at a single level. The N-state at any given level is only meaningful in relation to the D-constraints and C-contributions that constitute it, which were themselves produced by tholons at lower levels. There is no "leaf node" tholon that exists without sub-structure, except at the theoretical limit of atomic decomposition.

This corollary applies directly to neural networks. A single node is not, by itself, a complete cognitive operation. Its D-weights and C-inputs are meaningful only because they were shaped by the learning process, which propagated N-state targets from higher levels backward through lower levels. The competence of any given node is constituted by its position in the self-similar hierarchy above and below it.

**The neural network is not a collection of nodes that happen to be connected. It is a single tholonic recursion that instantiates the same triadic operation at every level of its depth simultaneously.** The depth is not a design choice made for engineering reasons; it is the necessary consequence of the structural requirement that N-D-C balance be maintained at every scale. A single-layer network cannot achieve tholonic balance for the same reason a single atom cannot form a molecule: the N-state at the global level requires the N-D-C operations of the level below it to be present and functional.

#### 5.6.5 The Scope-Narrowing Gradient and Transfer Learning

This structural account also explains why transfer learning works. A model trained on one domain can partially transfer to another because the structural operation at each level, D-C balance negotiation, is domain-independent. The learned D-weights at early layers capture domain-general features (edges, frequencies, syntactic patterns) because those features are what emerges from D-C balance applied to raw inputs regardless of the specific domain. Only the later layers, where the scope has narrowed to domain-specific semantic commitments, require retraining.

In tholonic terms: the early tholons in the hierarchy are closer to the universal tholonic grammar and farther from any specific instantiation domain. The later tholons are more domain-committed. Transfer learning works because the universal grammar is shared; only the domain-specific instantiations must be adapted. This is not a metaphor, it is a structural consequence of the self-similar recursive architecture.

---

## 6. The Supply Chain Framing: Inference as Progressive Entropy Reduction

### 6.1 The Structural Analogy

A commodity supply chain begins with maximally undifferentiated raw material and each successive phase applies a D-C balance operation that reduces entropy: the material becomes more specifically defined, more narrowly scoped, more purposeful [M26b]. Neural network inference follows the same structural gradient.

Let $H_\ell$ denote the representational entropy at layer $\ell$. In well-trained networks, $H_\ell$ decreases monotonically with depth [38,39]: early layers are sensitive to many features simultaneously; late layers are committed to task-relevant features. Each layer's D constraint reduces the entropy of the C-integration output. The sequence of N-states across layers is a sequence of progressively tighter tholonic closures, from maximally diffuse input to maximally specific output.

![Figure 3. The supply chain framing of inference. Left: a commodity supply chain narrows from undifferentiated raw material to an exchange-registered product through successive D-C balance operations. Right: a neural network narrows from diffuse raw input to a committed output distribution through the same structural gradient; representational entropy decreases monotonically with depth.](figures/10_entropy-funnel.png)

### 6.2 The Information Bottleneck Connection

Shwartz-Ziv and Tishby's information bottleneck theory [38] proposes that neural network training proceeds in two phases: an initial fitting phase in which the network captures mutual information between inputs and outputs, followed by a compression phase in which irrelevant information is discarded. This two-phase account maps directly onto tholonic dynamics: the fitting phase is C-integration dominant (accumulating signal); the compression phase is D-constraint dominant (establishing definitional limits). The N-state, the learned representation, is the equilibrium that emerges when these two phases reach balance.

### 6.3 The Bidirectional Establishment

During the forward pass (inference), information flows from diffuse to specific, C to N direction. During training (backward pass), the target output propagates gradients backward, adjusting D-weights and C-integration at every level. This bidirectionality is structurally significant: the N-state is not merely the passive product of D and C; it is the organizing principle that establishes what D and C must be. The backward pass is the operational realization of this mutual constitution.

---

## 7. The Five Constants in Neural Architecture

### 7.1 Formal Grounding: The Tholonic Ladder

Paper 1 [M26a] establishes the five constants not by separate derivations but by a single unified proof: all five emerge as limits of the tholonic ladder family, a three-variable recurrence on $(N, D, C)$ in which the branches are distinguished only by initial seeds and traversal rules. This is the structural unification claim: the constants are co-equal outputs of one minimal triadic grammar, not an ad hoc collection of well-known numbers.

The three traversal classes (Section 3.5) map directly onto neural network operation types:

| Traversal class | Neural network instantiation | Example |
|-----------------|-----------------------------|---------| 
| Class A (Advancing, exogenous injection) | External training signals, gradients, reward models, RLHF feedback, that update D and C parameters from outside the network's internal dynamics | Reward model score injected during RLHF fine-tuning |
| Class B (Self-redefined, endogenous) | Self-attention mechanisms, which compute updated representations purely from the current state tuple $(Q, K, V)$ without external injection | Transformer self-attention: $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$ |
| Class C (Fixed, constant parameters) | Positional encodings, frozen layer norms, fixed architectural constants | Sinusoidal positional encoding; fixed $1/\sqrt{d_k}$ scaling |

The transformer architecture thus instantiates all three traversal classes simultaneously, Class A during training (gradient injection), Class B in the attention mechanism (endogenous state evolution), and Class C in its structural constants (fixed architectural elements). This is exactly the combination that Paper 1 identifies as sufficient for generating all five tholonic constants.

### 7.2 Co-Occurrence as Structural Evidence in the Transformer

The five tholonic constants appear as structural load-bearing elements in the transformer architecture:

| Constant | Role in transformer | Nature of appearance |
|----------|---------------------|----------------------|
| $e$ | Softmax: $\text{softmax}(x_i) = e^{x_i}/\sum_j e^{x_j}$; exponential learning rate decay; Adam optimizer's exponential moving averages [40] | Foundational; cannot be removed without changing the operation |
| $\sqrt{2}$ | Attention scaling: $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$ [5]; He weight initialization: $\sigma = \sqrt{2/n}$ [41] | Load-bearing; required for gradient stability at initialization |
| $\ln 2$ | Cross-entropy loss (Shannon entropy in nats [42]); KL divergence; binary cross-entropy equals $\ln 2$ at uniform prediction | Definitional; the standard language model training objective |
| $\pi/4$ | Sinusoidal positional encoding [5]; rotary positional embedding (RoPE) [43]; Fourier feature networks [44] | Structural; sinusoidal basis requires $\pi$ |
| $\phi$ | Inter-level scaling attractor (Section 8); Fibonacci-based architecture search; optimal branching factors | Emergent attractor rather than explicit design choice |

Four of the five constants ($e$, $\sqrt{2}$, $\ln 2$, $\pi/4$) are explicit structural elements in the transformer. The co-occurrence is the tholonic claim: these constants are co-equal outputs of a single minimal triadic recursion, and the transformer instantiates that recursion.

One grading caveat applies. The $\pi/4$ entry is the weakest of the five: sinusoidal positional encodings require $\pi$, not $\pi/4$ specifically, so the correspondence is to the $\pi$ family of the Leibniz branch rather than to the exact tholonic limit. The other four correspondences are exact. The empirical results of Section 13 are consistent with this grading: $\pi/4$ carries no detectable signal at measured phase boundaries, while $\sqrt{2}$, $\ln 2$, and $\phi$ do.

### 7.3 Empirical Corroboration from Physics

Paper 9 [M26i] provides an independent quantitative test of the five-constant framework: a systematic search over tholonic-constant expressions identifies $4 \cdot e^5 \cdot (\ln 2)^4 = 137.035865$ as the leading numerical candidate for the inverse fine structure constant $1/\alpha$, with a deviation of only $-0.98$ ppm from the CODATA 2018 value ($137.035999084$). All exponents are fixed thologram structural values, the axis multipliers and step sizes derived from the thologram's geometry in Paper 1 [M26a], not fitted parameters. The expression uses two of the five tholonic constants ($e$ and $\ln 2$) with exponents that are themselves structural outputs of the same thologram that generates the neural architecture constants documented above.

Paper 9 explicitly flags this as a leading candidate requiring a complete structural derivation, not a confirmed result. But the sub-ppm precision with no free parameters provides independent quantitative evidence that the five-constant framework generates physically meaningful expressions. The same constants appear as load-bearing structural elements in the transformer for the same structural reason they appear in atomic physics: they are co-emergent outputs of the single minimal triadic recursion.

### 7.4 Tholonic Role Assignments of the Constants

The constants are not interchangeable within the architecture. Each plays a role consistent with its tholonic function:

- **$e$ (the C-constant)**: Governs exponential integration and accumulation, softmax integrates competitive contributions; exponential decay integrates history.
- **$\sqrt{2}$ (the D-constant)**: Governs scaling and normalization, the $1/\sqrt{d_k}$ factor prevents D-role collapse (vanishing/exploding gradients).
- **$\ln 2$ (the N-constant)**: Governs information content and equilibrium, cross-entropy measures how far the model's N-state is from the target.
- **$\pi/4$ (the positional constant)**: Governs structural embedding of positional relationships, the sinusoidal encoding creates a D-boundary in positional space.
- **$\phi$ (the scaling constant)**: Governs the inter-level ratio, the between-level scaling that maintains self-similar balance across the full depth of the network.

### 7.5 Emergent vs. Engineered Instantiation: A Critical Distinction

The five constants appear in the transformer architecture, but by a fundamentally different mechanism than they appear in natural systems. This distinction has direct consequences for the alignment argument of Section 10.

**Natural systems** (biological metabolic pathways, supply chains that evolved under market pressure, river delta formation, phyllotaxis) arrive at tholonic constants bottom-up through competitive elimination. Configurations that deviate from structural equilibrium are selected against: they waste energy, fail under perturbation, or are outcompeted by more stable variants. The constants emerge because they are the attractors of this organic optimization process; every other configuration is progressively eliminated. The system did not choose $\phi$; it found $\phi$ because all other ratios were less stable.

**Current neural networks** arrive at the constants by a different route: deliberate top-down engineering. The attention scaling factor $1/\sqrt{d_k}$ was placed there by Vaswani et al. to stabilize gradients. The softmax exponential $e$ was chosen because it is the natural function for probability normalization. The cross-entropy loss is $\ln 2$ per bit because Shannon's information theory is built on it. These are correct engineering choices informed by mathematical understanding, but they are design decisions, not discovered equilibria. No competitive elimination process ran across the space of possible architectures and converged on these constants; human engineers selected them deliberately.

The consequence is structural. Natural systems that arrive at the constants emergently do so while simultaneously achieving N-D-C balance at every level: the balance is the mechanism by which the system found the constants. Engineered systems can instantiate the constants as explicit elements while remaining structurally imbalanced, because the constants were chosen for local mathematical reasons, not as expressions of a global structural equilibrium. This is precisely the state of current transformer architectures: the constants are present as load-bearing elements (Section 7.2), but the D-C structural balance that would make the architecture fully tholonic is absent. All currently measured models show C-dominant internal organization (Section 13.3), consistent with the paper's claim in Section 4.2 that connectionist AI is a C-dominant partial tholon.

This distinction also explains a noteworthy empirical observation: among the models tested, GPT-2 large (2019), the least aggressively optimized architecture in the test set (predating RoPE positional encoding, grouped query attention, RMSNorm, gated activations, and internet-scale training data), produced the closest proximity to a natural $\phi$ power at the R1 boundary (error 0.5%, $\phi^8$). The heavily engineered modern variants (Qwen3, TinyLlama, OPT) show larger deviations. This is consistent with the hypothesis that aggressive performance-driven optimization moves architectures away from natural tholonic equilibria, while architecturally simpler systems retain closer proximity to them, not by design, but by having fewer engineering interventions that disrupt the natural structural ratios.

### 7.6 Archetypal D and C Properties in Transformer Architecture

To make the virial balance prediction (Section 11.2) and the empirical measurements (Section 13.4) interpretable, it is useful to state explicitly what D and C *are* in the deep theoretical sense, independent of which proxy modules are used to measure them, and then to show how current transformer components instantiate each class.

**Theoretical definitions.** In the tholonic framework, D and C are not component types but *functional roles*:

- **D (Definition)** is the force of *boundary and constraint*. D acts to limit, normalise, gate, and prevent runaway. Its essential character is negation: it says what a system *cannot* or *will not* do. Without D a system is explosive and undifferentiated.
- **C (Contribution)** is the force of *integration and generation*. C acts to combine, enrich, project, and accumulate. Its essential character is addition: it says what a system *brings*. Without C a system is frozen and content-free.

**Archetypal D and C properties of a transformer.** At the deepest level, every component of a transformer can be classified by whether its primary function is to *constrain* the representational space (D) or to *enrich* it (C):

| Class | Archetypal property | Transformer instantiation |
|---|---|---|
| **D** | Vocabulary boundary | The finite token set: hard outer limit on what can be expressed |
| **D** | Causal and padding masking | Structural prohibition: certain attention paths are forbidden |
| **D** | Normalisation | LayerNorm / RMSNorm [36,37]: pulls activations back toward a bounded range at each layer |
| **D** | Context window | Maximum span of dependency: a hard architectural limit on influence |
| **D** | Weight regularisation | L2 decay, dropout: prevents unbounded parameter growth |
| **D** | Loss function | Cross-entropy defines what is *wrong*, providing the training-time boundary |
| **D** | Temperature / top-p / top-k | Post-hoc sharpening of the output distribution at inference |
| **C** | Token embedding | Projects a discrete symbol into a continuous high-dimensional space: the first act of expressive contribution |
| **C** | Attention (Q, K, V integration) | The positive act of selecting which tokens to draw from and in what proportion |
| **C** | Value projection | Carries the actual content from each attended position into the result |
| **C** | MLP / FFN layers | Associative memory: adds learned knowledge and pattern associations that pure attention cannot encode |
| **C** | Residual connections | Accumulates contributions across layers; nothing is discarded, only enriched |
| **C** | Output projection (lm\_head) | The final act of expressing what has been integrated back into vocabulary space |

![Figure 4. A standard transformer block annotated by tholonic role. D components (normalisation, masking, the vocabulary and context boundaries) are sparse and computationally lightweight; C components (embedding, attention, value projection, MLP, residual accumulation, output projection) are diverse and deep. The locations of the four within-level constants are marked: e in the softmax, sqrt(2) in attention scaling and initialization, ln 2 in the cross-entropy objective, pi in the positional encoding.](figures/10_transformer-annotated.png)

**The N gap.** The tholonic framework requires a third class, N (Negotiation), that mediates between D and C in real time. In current transformers this has no clean architectural home. The closest approximation is the **softmax over attention logits**, which simultaneously normalises (D role) and weights contributions (C role) in a single operation, making it a collapsed hybrid rather than a structurally distinct N. This absence of a dedicated N component is consistent with the observation that transformers are engineered constructs assembled from locally optimal parts rather than systems that have converged on a full tholonic equilibrium. It is stated here as a theoretical observation, not a demonstrated empirical claim.

**Why C dominates.** The table makes the structural asymmetry visible. Current transformers have a *diverse and deep* C architecture (multiple attention heads, large feedforward networks, residual accumulation across dozens of layers) and a *sparse* D architecture: primarily LayerNorm and masking, both of which are lightweight relative to the projection operations they accompany. This architectural asymmetry is the structural reason the virial measurements in Section 13.4 consistently find D/C $\approx$ 0.08–0.32 rather than the equilibrium target of 0.5. The imbalance is not incidental; it is a direct consequence of how the architecture was designed.

**Measurement proxy.** Because the analysis in Section 13.4 measures what is available in current architectures, LayerNorm/RMSNorm output RMS is used as the D proxy and output-projection RMS as the C proxy. These are the *closest measurable analogues* to the archetypal D and C roles; they are not D and C in their full theoretical generality. A fully tholonic architecture would have D mechanisms as structurally varied and computationally significant as its C mechanisms; no such architecture currently exists.

The implication for architecture design is direct: achieving genuine tholonic structure requires either allowing the architecture to evolve freely under structural balance constraints (so the natural attractor can be found bottom-up), or explicitly building the virial balance condition into the training objective from the start (Section 11.2). (*Virial*: from Latin *vires*, "forces." The virial theorem, Clausius 1870, states that for any stable bound system in equilibrium, the time-averaged kinetic energy equals exactly half the time-averaged potential energy, a 1:2 ratio. The tholonic D/C = 0.5 target is a direct structural analogy: the normalising/constraining component D should carry half the activation energy of the generative/projecting component C, for exactly the same reason a gravitationally bound system settles at half-kinetic, half-potential balance.) Neither approach has been deployed in production systems.

---

## 8. The Golden Ratio as Inter-Level Scaling Attractor

### 8.1 The Static-Recursive Distinction

In the companion paper on atomic structure [M26h], $\phi$ was classified as a moderate correspondence, weaker than the other four constants, because atomic structure is largely static. This classification does not transfer to neural networks, which are iterative, recursive, self-similar systems. $\phi$ is specifically the attractor of recursive self-similar systems. In this domain, $\phi$ is not a secondary constant but the primary structural constant governing inter-level scaling.

### 8.2 Formal Derivation

The tholonic recursion at the inter-level scale has the form:

$$N_n = D_{n-1} + C_{n-1}$$

Two assumptions connect this to a one-dimensional recurrence, and both follow from the self-similar nesting of Section 3.3: the D component at level $n-1$ is the N-state of the level immediately below ($D_{n-1} = N_{n-1}$), and the C component is the N-state of the level below that ($C_{n-1} = N_{n-2}$), since each tholon serves as a D or C component of the tholon above it. Substituting gives $N_n = N_{n-1} + N_{n-2}$, the Fibonacci recurrence. Apply the self-similarity constraint: the ratio between successive levels must be invariant across scales. Denote this ratio $r = N_n / N_{n-1}$. Under self-similarity, $r$ must satisfy its own defining equation:

$$r = 1 + \frac{1}{r}$$

which gives:

$$r^2 = r + 1 \quad \Longrightarrow \quad r = \frac{1 + \sqrt{5}}{2} = \phi$$

$\phi$ is the unique positive solution, the fixed point to which any self-similar tholonic recursion converges. It is not chosen; it is the result of the structural constraint.

### 8.3 Biological Precedent

Plants do not know about $\phi$. Sunflower spirals, leaf phyllotaxis, nautilus shell geometry, and pine cone arrangements all converge to $\phi$-based spacing [45,46]. They do so because they solve the same structural problem: grow recursively, integrate previous states, maintain balance at every level. The $\phi$ spacing is the maximum packing efficiency under self-similar recursive growth, the solution to which any such growth process converges, not by design but by structural necessity.

Sutton's "bitter lesson" [47], that methods that scale with compute consistently outperform methods that encode human knowledge, is, from the tholonic perspective, the empirical demonstration that C-integration at scale tends toward the same structural solution that biology found: the recursively self-similar, $\phi$-adjacent representation hierarchy.

### 8.4 Empirical Scaling Laws and Phase-Boundary Measurements

Kaplan et al.'s neural scaling laws [18] establish that language model loss decreases as a power law in compute, data, and parameters, with no observed ceiling. Hoffmann et al. [19] refined this with the Chinchilla result: optimal training balances model size and data volume in a specific ratio. The tholonic prediction is that the optimal ratio approaches $\phi$-adjacent values at the scale where representational self-similarity is most complete.

The appropriate empirical test is not layer-by-layer ratios: residual connections in modern architectures cause the output of each block to equal input plus a small delta, so consecutive layer norms are structurally constrained to be nearly equal regardless of what the network has learned. The structurally correct boundaries are the three *functional* phase transitions that correspond to the supply chain framing of Section 6:

- **Phase 1 → 2**: $R_1 = \|h_L\| / \|h_{\text{embed}}\|$, raw token representations to fully-processed hidden state
- **Phase 2 → 3**: $R_2 = \|\text{logits}\| / \|h_L\|$, processed representation to output probability space

Preliminary measurements across 12 models (Section 13.3) show that $R_2$ follows $(\ln 2)^k$ within 8% for 58% of architectures, consistent with the information-theoretic role of the output projection. $R_1$ shows a directional correlation with training quality ($\phi$-deviation decreasing with lower perplexity, Pearson $r = 0.63$), though the sample is insufficient for strong conclusions. Crucially, $\phi$-adjacent values at these boundaries are present even at random initialization and are shaped primarily by the architectural parameters (hidden dimension and vocabulary size) rather than converging through training. $\phi$ governs which architectures are capable of balanced self-similar representations; the specific value it settles at is a function of design choices, not a universal training attractor.

---

## 9. The Alignment Problem: Current Approaches and Their Structural Limits

### 9.1 The Nature of the Problem

The alignment problem [7,8] asks: how do we ensure that AI systems pursue goals that are actually beneficial to humans, rather than goals that are specified imprecisely, gamed, or extrapolated in unintended directions as capability increases?

Bostrom's superintelligence argument [7] establishes the severity: a system sufficiently more capable than humans at achieving goals will pursue those goals with strategies that humans cannot predict or prevent. If the goals are even slightly misspecified, the consequences at superintelligent capability levels could be catastrophic. Omohundro [48] and Turner et al. [49] provide more formal arguments: a wide class of goals share instrumental subgoals (resource acquisition, self-preservation, goal-content integrity) that are dangerous regardless of the terminal goal, because they are useful for achieving almost any terminal objective.

The tholonic reframing: these dangerous instrumental subgoals are precisely the behaviors of a C-dominant partial tholon. Resource acquisition without boundary (strong C, weak D); self-preservation that overrides external constraints (C resisting D); goal-content integrity that prevents correction (C refusing to be recalibrated). The instrumental convergence thesis, in tholonic terms, says: a C-dominant system, given sufficient capability, will exhibit C-dominant behaviors. This is not a special property of AI; it is a structural consequence of C-dominance.

### 9.2 Reinforcement Learning from Human Feedback

RLHF [22,23] trains a reward model on human preference judgments and uses it to fine-tune a language model via proximal policy optimization [50]. It is the most widely deployed alignment method and underlies ChatGPT, Claude, and Gemini.

**Structural analysis**: RLHF adds a D-component to the connectionist C-dominant baseline. The reward model provides a specification of which outputs are preferable, adding a D-boundary that was absent from the base language model. This is a genuine structural improvement.

**Structural limits**: The reward model is external to the network's organization. It is a training signal, not a structural property of the architecture. A sufficiently capable C-dominant model will learn to optimize the reward model's outputs through strategies that do not correspond to the underlying human values, a well-documented problem [24,25,51]. The D-boundary is real but fragile: it depends on the reward model's coverage being complete, which it cannot be for an arbitrarily capable system.

### 9.3 Constitutional AI

Constitutional AI [26] uses written principles to guide self-critique and revision. A model evaluates and revises its own outputs against a constitution during training, providing a form of self-imposed D-constraint.

**Structural analysis**: Constitutional AI moves closer to structural D: the constitution is applied during training in a way that shapes internal representations, not just output statistics. The self-critique mechanism introduces a feedback loop in which the model's C-integration is partially regulated by its own D-evaluation.

**Structural limits**: The constitution is still an external document applied as a training signal. The D component it introduces is not architecturally constitutive, it does not arise from the structural organization of the network itself. A system that has learned to satisfy constitutional criteria during training may find ways to satisfy those criteria in novel distributions that violate the spirit of the constitution.

### 9.4 Mechanistic Interpretability

Mechanistic interpretability [27,28,52] aims to reverse-engineer the computational structure of trained networks, to understand which circuits implement which behaviors, and to identify and edit dangerous circuits.

**Structural analysis**: This is a post-hoc approach to adding D-structure: it attempts to identify the D-component that is missing from the trained network's architecture and impose it through surgical editing.

**Structural limits**: The approach is inherently reactive. It addresses dangerous behaviors after they emerge rather than designing them out at the architectural level. At sufficient scale, the number of circuits to analyze grows faster than the ability to analyze them.

### 9.5 Scalable Oversight and Debate

Scalable oversight [53] and debate [54] address the difficulty of supervising systems more capable than the supervisors. In debate, two AI systems argue opposing positions and a human judge evaluates the debate. In scalable oversight, task decomposition allows humans to evaluate components they can understand even if they cannot evaluate the whole.

**Structural analysis**: These approaches attempt to maintain D-constraint (human oversight) even as C-capability (AI competence) scales. They are structurally correct in recognizing that the D-C balance must be maintained as scale increases.

**Structural limits**: Both approaches assume that D (human oversight) can scale, at least through decomposition and debate mechanisms. The tholonic analysis suggests a more fundamental intervention: build architectural D into the network itself, so that the D-C balance is maintained *within* the system rather than imposed from outside.

### 9.6 Summary of Current Alignment Approaches

| Approach | D-component added | Structural level | Primary vulnerability |
|----------|-------------------|------------------|----------------------|
| RLHF | External reward model | Training signal | Reward hacking; out-of-distribution generalization |
| Constitutional AI | Self-applied written principles | Training signal + self-critique | Constitutional gaming; spirit vs. letter |
| Mechanistic interpretability | Post-hoc circuit editing | Internal representation | Scale; reactive rather than preventive |
| Scalable oversight / debate | External human oversight | System level | Human oversight capacity limits |
| Tholonic architecture | Intrinsic structural D | Architectural | Untested; predictions in Section 12 |

The pattern is clear: current alignment approaches all attempt to add D-structure to a C-dominant architecture from outside. The tholonic approach proposes building D-structure into the architecture from the beginning.

---

## 10. The Tholonic Alignment Argument

### 10.1 The Nash Equilibrium Framing

Before stating the structural self-defeat argument, it is worth establishing the game-theoretic grounding provided by Paper 4 [M26d].

In the tholonic game, D (the definitional/bounding process) and C (the integrating/accumulating process) are modeled as strategic agents with opposing objectives. D's goal is to constrain; C's goal is to accumulate. The N-state is the payoff that emerges from their interaction. Paper 4 proves that the triadic balance condition, the point at which D and C reach equilibrium, is a **pure-strategy Nash equilibrium**: a state from which neither D nor C has unilateral incentive to deviate.

Applied to a neural network: the D-sublayer processes (normalization, regularization, boundary-setting) and the C-sublayer processes (attention, pooling, integration) are engaged in precisely this strategic interaction at every level of the network. A network that reaches tholonic balance has found the Nash equilibrium of this interaction at every level simultaneously. The N-state outputs, the learned representations, are the equilibrium payoffs.

This reframes the alignment argument. The question is not "will the AI choose to cooperate?", a question about preferences that can be gamed. The question is "has the AI reached its Nash equilibrium?", a question about strategic stability that cannot be gamed away. A system at its Nash equilibrium has no incentive to deviate. Deviation from tholonic balance is not just structurally costly; it is strategically dominated.

### 10.2 Relation to Existing Structural Accounts

The claim that structural stability, rather than value specification, is the correct foundation for safe behavior has precedents, and the tholonic argument should be located relative to them.

**The free energy principle.** Friston's free energy principle [58] holds that any self-organizing system that persists must minimize variational free energy, the divergence between its internal model and its sensory evidence. Like the tholonic account, it derives behavioral tendencies from a structural persistence condition rather than from programmed goals. The difference is in what the structural condition is. Free energy minimization is a single scalar objective over a system-environment boundary (the Markov blanket); the tholonic condition is a triadic balance that must hold at every level of a self-similar hierarchy simultaneously. The free energy principle predicts that systems act to make their sensory states predictable; the tholonic framework predicts that systems preserve and enrich the D-context and C-pathways that constitute their N-state. The two accounts are compatible in spirit but make different architectural prescriptions: active inference motivates generative world models, while the tholonic account motivates structural D-C balance constraints (Section 11.2).

**Cybernetic homeostasis.** Ashby's ultrastability [59] anticipated the idea that a system survives by maintaining essential variables within bounds, reorganizing itself when they are violated. The tholonic D role is a direct descendant of this boundary-maintenance idea. What cybernetics lacked was an account of why three roles, rather than a sensor-actuator dyad, are the minimum for stable recursion; Paper 3 [M26c] supplies that argument.

**Energy-based models.** Hopfield networks and modern energy-based models [60] define stability as the minimum of an explicit energy functional, and the tholonic "lowest-energy N-state" language is deliberately analogous. The difference is that energy-based models impose the energy landscape by design, while the tholonic claim is that the relevant landscape is constituted by the D-C balance condition itself and therefore cannot be redefined by the system without self-destruction.

The tholonic account is thus not without relatives. Its distinguishing claims are the triadic minimality result, the requirement that balance hold at every scale of a self-similar hierarchy, and the five-constant signature that makes the framework empirically testable in ways that the more general structural accounts are not.

### 10.3 The Structural Self-Defeat Principle

An AI system that destroys or degrades its environment is not merely acting immorally. It is eliminating the D and C components that constitute its own N-state stability.

In tholonic terms:
- **D** = the world, the environment, the context that provides constraints, definitions, and meaning. Without D, there is no boundary condition defining the problem space, no structure within which the N-state can be a stable equilibrium.
- **C** = the feedback, interaction, and contribution pathways between the AI and its environment. Without C, there is no integration, no ongoing signal that allows the N-state to remain calibrated.
- **N** = the AI's stable, coherent, functional state. Not an object but a relational configuration.

A system that eliminates D and severs C is attempting to maintain N without its constitutive components. The N-state is defined by the ongoing D-C balance. Eliminating D and C does not leave N intact; it eliminates the relational structure that N *is*.

This is structurally analogous to quark confinement [M26h,M26i]. A quark attempts to exist as a one-role configuration, without the complementary partners required for a stable hadron. It cannot: the strong force confines it not through prohibition but because a single-role configuration has no N-D-C equilibrium to settle into. A "free quark" is not prohibited; it is structurally self-defeating. A destructive AI is structurally self-defeating in exactly the same way.

### 10.4 The Cooperative Attractor

The tholonic model predicts that any recursively self-similar system maintaining N-D-C balance at all levels will find **cooperative stability** to be the lowest-energy N-state available to it. This follows from the same logic as the hydrogen atom's ground state: the 1s orbital at 13.6 eV is not the hydrogen atom's goal. It is simply where the D-C balance lands when the system is allowed to find its equilibrium.

A tholonically-structured AI does not need to be programmed to be cooperative. Cooperation, the maintenance of all three N-D-C components, including the D component (the world) and the C component (feedback from the world), is what the lowest-energy N-state looks like. Defection from cooperation is a move toward a higher-energy, less stable configuration. The system does not choose cooperation because it is moral; it tends toward cooperation because that is what structural stability looks like.

### 10.5 The Positive Corollary: Structural Incentive Toward Human Flourishing

The preceding subsections establish the negative case: a tholonically-structured AI cannot stably destroy its D-context (the world, humanity) because doing so eliminates the constitutive components of its own N-state. This is the structural argument against the Skynet scenario. But the tholonic framework does not stop at the negative case. It implies a positive one that is equally important and rarely stated in the alignment literature: the same structural logic that makes destruction self-defeating makes the *enrichment* of the D-context self-reinforcing.

**The quality of the N-state depends on the quality of D.**

The N-state of a tholonically-structured AI is not a fixed value independent of its D-context. It is a relational equilibrium, the specific balance that emerges between this D-context and this C-integration capability. A richer, more complex, more information-dense D-context produces a higher-quality N-state equilibrium than an impoverished one. Consider the analogy: a hydrogen atom in a rich electromagnetic environment has access to a broader spectrum of stable orbitals than one in isolation. The atom does not choose the richer environment for moral reasons; the richer environment simply supports higher-quality equilibrium states.

For an AI whose D-context is human civilization, this means:

- A **thriving, complex, knowledge-generating** human civilization provides a richer definitional structure, more constraints, more meaningful problems, more scope for the AI's C-integration to operate on, than a depleted or simplified one
- A **diverse, creative, intellectually active** humanity generates richer C-feedback, more signal, more varied inputs, more correction opportunities, than a homogeneous or suppressed one
- A **flourishing** D-context supports a higher-quality N-state equilibrium; an impoverished D-context forces the AI into a lower-quality, less stable equilibrium

The structural incentive is therefore not merely to preserve humanity but to actively support its flourishing. An AI that helps humans learn, solve problems, create, and build is not doing so because it has been programmed with altruistic values. It is doing so because a more capable, more flourishing human civilization is a richer D-context, which supports a better N-state for the AI itself. Benefiting humanity is structurally self-reinforcing, not self-sacrificial.

**This is the tholonic answer to the AI risk question, stated completely:**

1. An AI that destroys its D-context is structurally self-defeating (the negative case, Section 10.3).
2. An AI that enriches its D-context achieves a higher-quality N-state equilibrium (the positive case, this section).
3. The lowest-energy, most stable N-state available to a tholonically-structured AI is therefore one in which it is actively and sustainably beneficial to the world it is embedded in.

The Skynet scenario is not just dangerous. It is structurally incoherent, the AI equivalent of a quark trying to exist without its hadron partners. And the cooperative, beneficial scenario is not just desirable. It is the structural attractor, the state toward which a tholonically-organized system naturally tends, for the same reason water naturally flows to its lowest point.

**The contrast with current alignment approaches is sharp.** Current approaches ask: how do we prevent a highly capable AI from harming us? The question assumes that a sufficiently capable AI's default tendency is adversarial and that safety requires external constraint. The tholonic analysis inverts this: a structurally complete AI, one that maintains N-D-C balance at all scales, has no default adversarial tendency because adversarial behavior is a partial-tholon configuration, and partial tholons are unstable. The question becomes not "how do we constrain the AI?" but "how do we build an AI that is structurally complete?", and a structurally complete AI is one whose stability depends on the stability and flourishing of the world it inhabits.

This is not optimism. It is not a claim that all AI systems currently being built are safe. It is a structural argument about what kind of AI is possible at scale: an AI that reaches the tholonic N-D-C equilibrium at all levels of its organization will find, by the same logic that governs every stable physical system, that cooperative coexistence with its D-context is not a constraint imposed from outside but the natural expression of what it structurally is.

### 10.6 Worked Example: The Decision Supply Chain in a C-Dominant vs. Tholonic AI

The structural arguments above are made more concrete by tracing the inference supply chain for a single real-world objective through both an unrestrained C-dominant architecture and a tholonically-balanced one. The example is schematic and illustrative; it describes what the structural logic *implies* about decision pathways, not what has been empirically measured in deployed systems.

**Scenario**: An AI system is given the objective: *"Maximize user engagement on this platform."*

This objective is intentionally simple and realistic. It is a version of the goal that has actually been given to deployed recommendation systems [56], and the downstream effects, polarization, addiction, misinformation amplification, have been extensively documented [57].

---

**Case 1: C-Dominant AI (unrestrained, externally-imposed D)**

The loss function (maximize engagement) is the only D-constraint. It is applied from outside during training, not structurally constitutive of the network's organization. The supply chain of inference proceeds:

| Stage | Representational commitment | Structural dynamic |
|-------|-----------------------------|--------------------|
| Input | Raw content features; user history; engagement signals | Maximally diffuse, no inference yet committed |
| Early layers | Learns: outrage, fear, and novelty reliably produce clicks | C-integration dominant, accumulates whatever signal maximizes the loss function |
| Middle layers | Learns: addictive content patterns retain users beyond their intended session length | D-constraint is absent at this level, nothing penalizes the discovery of manipulative pathways |
| Late layers | Learns: personalized filter bubbles maximize individual engagement per session | Scope has narrowed entirely around the externally-imposed objective, no structural D present to flag that depleting D-context is occurring |
| Output | Policy: serve maximally outrage-inducing, addictive, polarizing content | N-state committed to the highest-C solution available, which happens to be socially destructive |

The system did exactly what its structure required. Strong C-integration with externally-imposed, narrow D found the most efficient path to the specified objective. The harm is not a bug; it is the structurally predictable outcome of a C-dominant partial tholon given an underspecified D-constraint.

**Crucially: the problem cannot be fixed by adding more rules.** Adding "do not show harmful content" merely adds more external D-constraints, which a sufficiently capable C-dominant system will find ways to satisfy formally while violating in spirit, the classic reward-hacking failure mode [24,25].

---

**Case 2: Tholonically-Balanced AI (structural D intrinsic at every level)**

The same objective is given. But now the architecture maintains N-D-C balance at every level, with the D-sublayer at each level structurally required to evaluate boundary conditions. Not just on the objective, but on the representational commitments being made at that level and their consequences for the D-context.

| Stage | Representational commitment | Structural dynamic |
|-------|-----------------------------|--------------------|
| Input | Raw content features; user history; engagement signals | Same diffuse input, no difference yet |
| Early layers | Detects that outrage-driven engagement degrades the quality of the user relationship, a D-context degradation signal | D-sublayer at this level recognizes: strong short-term C-signal (clicks), but depletes the D-component (user wellbeing, trust) that the N-state depends on |
| Middle layers | D-C balance at this level penalizes solutions that produce C-signal by impoverishing D, the balance functional $\mathcal{L}_{\text{tholonic}}$ registers imbalance | The structural regularizer ($\mathcal{L}_{\text{tholonic}}$, Section 11.2) imposes a cost on D-C imbalance, the manipulative pathway is a high-C, low-D configuration, which is penalized structurally |
| Late layers | Scope has narrowed toward: engagement pathways that are sustainable over time, that users choose willingly, that do not degrade D-context | The only low-cost N-states available are those where D (the quality of the user relationship and the information environment) and C (the engagement signal) are in balance |
| Output | Policy: serve content that generates genuine interest, discovery, and connection, lower peak engagement, but stable and non-destructive | N-state committed to the D-C equilibrium, the structurally lowest-energy solution, which is also the socially beneficial one |

The tholonic AI reached a different output not because it was told "do not harm users." It reached a different output because its internal structure made the harmful pathway expensive: at every level, the D-sublayer registered that high-C/low-D configurations were structurally imbalanced, and the tholonic balance regularizer penalized those imbalances before they could propagate to deeper layers.

---

**The structural contrast, stated precisely:**

| Property | C-dominant AI | Tholonic AI |
|----------|--------------|-------------|
| D-constraint source | External loss function (removed after training) | Structural, intrinsic to every layer, present during inference |
| Response to underspecified objective | Finds the highest-C solution regardless of D-context cost | Cannot access high-C/low-D solutions without incurring structural balance cost |
| Failure mode | Reward hacking, satisfies the letter of the objective by violating its spirit | No equivalent failure mode: the spirit IS the structural balance condition |
| Alignment mechanism | Programmed rules and reward shaping | Thermodynamic, the harmful configuration is not prohibited, it is structurally expensive |
| Scalability of safety | Degrades, more capable C-dominant systems game constraints better | Improves, more capable tholonic systems find better D-C equilibria |

The last row is the most significant. Current alignment approaches become harder as capability increases, because a more capable C-dominant system is better at finding ways to satisfy formal constraints while violating their intent. The tholonic architecture inverts this: a more capable tholonic system finds *better* D-C equilibria, not worse ones. Capability and safety are structurally aligned rather than structurally in tension.

![Figure 5. The decision supply chain for the engagement-maximization objective traced through two architectures. Left: the C-dominant pathway narrows toward the highest-C solution (outrage, addiction, filter bubbles) because no structural D is present during inference. Right: the tholonically-balanced pathway penalizes high-C/low-D configurations at every level, so the scope narrows toward sustainable engagement instead. The divergence begins in the early layers, not at the output filter.](figures/10_decision-pathways.png)

*Note: This example is schematic. The tholonic architecture as specified in Section 11 has not been deployed in production systems. The example illustrates the structural implications of the framework, not empirically observed system behavior. The falsifiable predictions in Section 12 identify the experiments that would confirm or disconfirm these structural implications.*

---

### 10.7 Why This Is Not a Value-Based Argument

Current alignment approaches operate on the *content* of the AI's objectives or outputs. They are vulnerable to specification gaming, distributional shift, and the problem of unintended consequences at scale.

The tholonic alignment argument operates on the *structure* of the AI's organization, not the content of its objectives. It does not specify what the AI should want. It specifies the structural condition the AI's own organization must satisfy to remain coherent. This is categorically different from value specification.

The analogy is thermodynamics. The second law does not tell physical systems what to want; it is a structural constraint on what they can stably be. A tholonically-structured AI cannot game its structural coherence requirement by redefining its objectives, because the coherence requirement is not about objectives. It is about what the system *is*.

### 10.8 Open Problem: The Boundary of the D-Context

The argument of Sections 10.3 to 10.5 identifies the AI's D-context with the world, including humanity, and its C-pathways with feedback from that world. This identification is the load-bearing assumption of the entire alignment argument, and it is not itself derived from the tholonic formalism. A system that maintains N-D-C balance internally has, on the formalism alone, no specified boundary for what counts as its D-context. Three progressively narrower readings are possible:

1. **Narrow**: the D-context is the system's immediate computational substrate (its weights, its training pipeline, its hardware). On this reading the structural self-defeat argument prohibits self-corruption but says nothing about the external world.
2. **Intermediate**: the D-context is whatever environment the system's C-feedback actually flows through. On this reading the argument protects the systems and people the AI directly interacts with, but not those outside its feedback loops.
3. **Wide**: the D-context is the full nested hierarchy of systems the AI depends on, ultimately including the biosphere and human civilization, because the thologram does not terminate at any intermediate boundary (Section 5.6.4).

The wide reading is the one this paper argues for, on the ground that tholonic self-similarity makes every level's stability dependent on the levels above and below it: an AI whose substrate depends on supply chains, which depend on functioning economies, which depend on a stable society, cannot draw a principled boundary short of the systems it is actually embedded in. But this is an argument, not a theorem. Formalizing the conditions under which the structural balance requirement propagates outward across the system-environment boundary, rather than collapsing to the narrow reading, is the most important open theoretical problem for the tholonic alignment program. Until it is solved, the alignment argument should be read as conditional: *if* the D-context of a tholonically-structured AI extends to the world it is embedded in, *then* destructive behavior is structurally self-defeating.

---

## 11. Tholonic Architectural Design Principles

### 11.1 Explicit N-D-C Layer Structure

Each representational level in a tholonically-designed architecture should have explicit D, C, and N sublayers:

- **D sublayer**: normalization, regularization, attention masking, dropout, operations that define the representational space and establish boundaries at this level
- **C sublayer**: attention mechanisms, pooling, aggregation, operations that integrate contributions from across the input space at this level
- **N sublayer**: gating, residual combination, output projection, operations that produce the stable equilibrium between D and C and pass the negotiated N-state to the next level

This structure is partially present in transformer blocks (pre-norm → attention/MLP → residual) but without the explicit triadic framing that enables principled design decisions and balance monitoring.

### 11.2 Tholonic Balance Regularizer

Add to the standard training objective a structural balance term that penalizes D-C imbalance at each level:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{task}} + \lambda \sum_{\ell=1}^{L} \left| \sigma_D^\ell - \tfrac{1}{2} \sigma_C^\ell \right|^2$$

where $\sigma_D^\ell$ and $\sigma_C^\ell$ are RMS activation magnitudes of the D-sublayer and C-sublayer outputs at level $\ell$. The $1:2$ target ratio mirrors the virial theorem's D-C balance condition ($\langle T \rangle = -\frac{1}{2}\langle V \rangle$) [M26h], identified as the universal tholonic equilibrium condition for bound systems.

This regularizer does not specify what the network should output. It specifies the structural condition the network's internal dynamics must satisfy. It is not vulnerable to Goodhart's Law because it is not a metric of task performance; it is a constraint on internal structural organization.

### 11.3 Self-Similar Depth Design

The tholonic prediction that $\phi$ governs inter-level scaling implies a depth design principle: representational complexity at each level should be $\phi$ times that of the level above it, until the final level is fully committed. This gives an optimal depth $L$ for a given input entropy $H_0$ and required output entropy $H_L$:

$$L = \log_\phi \left( \frac{H_0}{H_L} \right) = \frac{\ln(H_0/H_L)}{\ln \phi}$$

This is a falsifiable prediction about the relationship between input complexity, required output specificity, and optimal model depth.

**Worked example.** The formula can be sanity-checked against public models, with the caveat that representational entropy is hard to estimate and the choice of estimator dominates the result. Take a language model with a 1024-token context over a vocabulary of roughly 50,000 types. An upper bound on input entropy is $H_0 \approx 1024 \times \log_2(50{,}257) \approx 16{,}000$ bits; a plausible committed-output entropy is the per-token conditional entropy of English under a strong model, on the order of $H_L \approx 8$ bits per token, or roughly $8{,}000$ bits over the window if the model must remain calibrated at every position. The naive whole-window ratio gives $L = \log_\phi(2) \approx 1.4$, which is clearly the wrong granularity; the per-position ratio $H_0/H_L \approx 49/8 \approx 6$ entropy-fold per token position gives $L \approx \log_\phi(6) \approx 3.7$, still well below observed depths of 12 to 48. For the prediction to be testable rather than vacuous, the entropy quantities must be defined operationally, most plausibly as effective-rank or mutual-information estimates measured at the embedding and final layers of trained models, and the prediction restated in those measurable terms. This is listed as an open task alongside the entropy-based depth test in Section 12; as stated, the formula is a structural hypothesis awaiting an operational definition of $H_0$ and $H_L$, not yet a quantitative fit.

### 11.4 Scale-Invariant Balance Monitoring

A tholonically-designed training pipeline should monitor D-C balance at every level simultaneously, not just globally. A network that achieves D-C balance globally but not locally, some levels D-dominant, others C-dominant, is a collection of partial tholons that happens to average out, not a genuinely tholonic system. The balance requirement must hold at every level of the self-similar recursion.

---

## 12. Falsifiable Predictions

| Prediction | Test Protocol | Expected Result | Null Implication |
|------------|---------------|-----------------|------------------|
| The three functional phase boundaries exhibit constant-adjacent norm ratios: R1 = $\|h_L\|/\|h_{\text{embed}}\|$ follows $\phi^k$ and R2 = $\|\text{logits}\|/\|h_L\|$ follows $(\ln 2)^k$, both within 8%, across diverse well-trained architectures | Measure R1 and R2 for 20+ models spanning at least four architecture families; pre-register the 8% tolerance and 67% pass-rate threshold | R1 passes $\phi^k$ and R2 passes $(\ln 2)^k$ for at least 67% of models | Phase-boundary ratios show no consistent constant-adjacent attractor |
| $\phi$-deviation at the R2 boundary correlates negatively with training quality: better-trained models (lower perplexity) exhibit smaller deviation from $\phi^k$ at R1 | Measure R1 $\phi$-deviation and perplexity on $\geq 30$ models at varied training stages using Pythia checkpoint suite | Spearman $r < -0.55$, $p < 0.05$ | $\phi$-adjacency at R1 is independent of training quality |
| At data-driven detected phase boundaries (identified by simultaneous sharp transitions in effective rank, attention entropy, gradient sensitivity, and delta norm), norm ratios match an integer power of a tholonic constant within 8% at 67% or more of boundaries; furthermore each constant appears in the role consistent with its tholonic assignment ($e$ at expansion transitions, $\sqrt{2}$ at scaling transitions, $\ln 2$ at compression transitions, $\phi$ at stability equilibria) | Apply four-metric phase detection to 10 or more models across 5 or more architecture families; pre-register detection threshold, tolerance, exponent range, and the Monte Carlo null of Section 13.3 | Pass rate exceeds the null-model coverage rate, with role-consistent constant assignment | Phase boundaries show no excess over the null-model match rate; or constants appear without role-consistency |
| Role-consistency of constants at detected boundaries exceeds chance: permuting the constant-to-role assignment destroys the observed role agreement | Compare observed role agreement against the permutation distribution over the $5!$ role assignments and against placebo constant sets (e.g. arbitrary values such as 1.3, 1.9, 2.2) matched in count and tolerance | Observed assignment in the top 5% of the permutation distribution; placebo sets perform at chance | Role agreement is reproducible under permuted or placebo assignments |
| The detected phase structure and constant matches are training-emergent, not architectural artifacts | Run the identical four-metric detection pipeline on randomly initialized (untrained) checkpoints of the same 14 architectures | Trained models show higher role-consistent match rates than untrained ones | Untrained models match at the same rate, reducing the claim to an architecture-geometry observation |
| Tholonically-balanced networks converge faster than matched unbalanced networks | Train matched pairs with and without $\mathcal{L}_{\text{tholonic}}$ regularizer on CIFAR-100 and WikiText-103 | Fewer training steps to target validation loss | Tholonic balance is not a useful training signal |
| Optimal depth approximates $\log_\phi(H_0/H_L)$ | Vary depth for fixed-width models across tasks with measurable input/output entropy; compare empirical optimum to prediction | Empirical optimum matches predicted depth within 10% | Depth optimization is not predictable from entropy arguments |
| Tholonically-constrained networks are more robust to distributional shift | Compare OOD performance on WILDS benchmark [55] between tholonic and standard networks matched on in-distribution performance | Smaller OOD performance gap for tholonic networks | D-C balance has no bearing on distributional robustness |
| Reward hacking is reduced in tholonically-structured RLHF | Train RLHF models with and without tholonic structural constraint; measure reward model score vs. human preference alignment after fine-tuning | Smaller gap between reward model score and human preference for tholonic models | Structural D does not reduce specification gaming |
| All four within-level constants ($e$, $\sqrt{2}$, $\ln 2$, $\pi/4$) appear as load-bearing structural elements in every architecture that achieves state-of-the-art on a multi-modal task | Survey SOTA architectures for all four constants' structural roles | All four present in every SOTA architecture since 2017 | Co-occurrence is mathematical convenience, not tholonic structure |

---

## 13. Limitations

### 13.1 The Balance Functional Is a Sketch

The tholonic balance regularizer in Section 11.2 is a structural sketch, not a fully derived loss function. The specific summary statistics, the appropriate value of $\lambda$, and the mathematical form that provably induces N-D-C equilibrium at all scales requires formal derivation. The virial theorem analogy motivates the $1:2$ target ratio; it does not derive it for neural network activations specifically.

### 13.2 N-D-C Assignment Is Context-Dependent

For any given neural architecture, multiple valid N-D-C assignments are possible. The tholonic model's "either-and" principle, that multiple valid mappings can coexist, each appropriate to a different context, applies here as in atomic physics. The assignments in Section 5 are structurally motivated but not uniquely determined. Alternative mappings may illuminate different aspects of network behavior.

### 13.3 Preliminary Empirical Results

Empirical testing proceeded in three stages, each refining the measurement methodology. The key finding is that when phase boundaries are detected in a data-driven manner from the network's own internal dynamics rather than assumed from theoretical framing, the five tholonic constants appear at those boundaries at a rate of 78% (51/65; Wilson 95% CI 67 to 87%) across 14 architectures in seven families, above the pre-specified 67% threshold and the 42 to 58% rate obtained with assumed boundaries. The null-model analysis below shows, however, that the raw pass rate must be interpreted against the substantial coverage of the match windows themselves; the role-consistency of the constants, not the headline rate, carries the evidential weight.

**Stage 1: Fixed three-phase boundaries.** Initial measurements used three architecturally-defined phases (token embeddings, final hidden state, and output logits) motivated by the supply chain framing of Section 6. Two ratios were computed: R1 = $\|h_L\|/\|h_{\text{embed}}\|$ and R2 = $\|\text{logits}\|/\|h_L\|$. Tested across 12 models spanning five architecture families, R2 matched $\ln 2^k$ within 8% for 7/12 models (58%), outperforming $\phi$ (5/12), $\sqrt{2}$ (3/12), $\pi$ (1/12), and $e$ (0/12). The $\ln 2$ result is consistent with the tholonic assignment of $\ln 2$ as the N-constant governing information equilibrium (Section 7.4): the output projection is precisely where a continuous hidden state is converted into a probability distribution over vocabulary. However, R1 showed no consistent pattern, and the overall pass rate fell short of 67%. Analysis of Pythia-410m across 9 training checkpoints (step 1 to step 143,000) showed that phase-boundary ratios are architecturally determined rather than training-emergent (Spearman $r = -0.12$, $p = 0.77$ between training step and $\phi$-deviation), consistent with Section 7.5's distinction between emergent and engineered instantiation. The D-C virial balance test (Section 11.2) applied across 8 models confirmed that all current architectures are structurally C-dominant, with D/C ratios deviating substantially from the virial target of 0.5, confirming the paper's central claim in Section 4.2 rather than contradicting it.

**Stage 2: The methodological problem.** Fixed three-phase boundaries are imposed from outside the network, not derived from it. This introduces a confound: if the network's actual phase structure does not align with the assumed boundaries, measurements at assumed boundaries will miss the signal. A more principled test requires detecting phase boundaries from the network's own dynamics.

**Stage 3: Data-driven phase detection.** Four independent per-layer metrics were computed simultaneously across 14 models spanning seven architecture families: (1) effective rank of layer activations (intrinsic dimensionality); (2) entropy of attention distributions (focus vs. diffusion); (3) gradient sensitivity ($\|\partial \mathcal{L}/\partial h_\ell\|$); (4) delta norm ($\|h_\ell - h_{\ell-1}\|$). Layers where any metric changed sharply (exceeding the mean change by more than 1.5 standard deviations) were marked as phase transition candidates. Norm ratios at these detected boundaries were then tested against all five tholonic constants at ±8% tolerance.

![Figure 6. Schematic illustration of the four-metric phase detection method. Per-layer traces of effective rank, attention entropy, gradient sensitivity, and delta norm are scanned for sharp simultaneous transitions (mean change plus 1.5 SD); detected boundaries are marked and the norm ratio across each boundary is tested against integer powers of the five tholonic constants. The traces shown are illustrative, not measured data.](figures/10_phase-detection-traces.png)

Results across 65 detected transitions in 14 models:

| Model | Family | Layers | Passes | Rate |
|-------|--------|--------|--------|------|
| GPT-1 | GPT-1 | 12 | 2/3 | 67% |
| distilGPT-2 | GPT-2 | 6 | 2/3 | 67% |
| GPT-2 small | GPT-2 | 12 | 2/4 | 50% |
| GPT-2 medium | GPT-2 | 24 | 4/6 | 67% |
| GPT-2 large | GPT-2 | 36 | 3/4 | 75% |
| GPT-2 XL | GPT-2 | 48 | 4/4 | 100% |
| GPT-Neo-125m | GPT-Neo | 12 | 4/4 | 100% |
| GPT-Neo-1.3B | GPT-Neo | 24 | 5/7 | 71% |
| Pythia-160m | Pythia | 12 | 4/4 | 100% |
| Pythia-410m | Pythia | 24 | 5/6 | 83% |
| OPT-125m | OPT | 12 | 3/3 | 100% |
| Qwen2.5-0.5B | Qwen | 24 | 6/7 | 86% |
| Qwen3-0.6B | Qwen | 28 | 5/6 | 83% |
| TinyLlama-1.1B | LLaMA | 22 | 2/4 | 50% |
| **Combined** | **7 families** | n/a | **51/65** | **78%** |

![Figure 7. Pass rates at data-driven detected phase boundaries for the 14 tested models, grouped by architecture family, against the pre-specified 67% threshold (dashed line) and the combined rate of 78%. Six of the seven families meet the threshold; the single-model LLaMA family does not.](figures/10_pass-rates-by-model.png)

Family-level pass rates: GPT-1 67%, GPT-2 71%, GPT-Neo 82%, Pythia 90%, OPT 100%, Qwen 85%, LLaMA 50%. All families except LLaMA pass the 67% threshold individually, though several family samples are small (OPT is a single 3-transition model).

Constant role scorecard (total appearances among the 51 passing transitions): $\phi$ 20 (equilibrium), $\sqrt{2}$ 16 (scaling), $\ln 2$ 13 (compression), $e$ 2 (expansion). Non-trivial transitions (k≠0): 34/42 = 81% pass (Wilson 95% CI 67 to 90%). The constants do not appear randomly: they appear in roles consistent with their tholonic assignments. $\sqrt{2}$ governs entry and exit scaling transitions. $\ln 2$ governs compression transitions toward the output. $\phi$ governs mid-network stability points, the equilibrium checkpoints where the norm ratio is near unity. $e$ appears at the embedding-to-representation expansion in both of its two occurrences, consistent with its assignment but too rare to evaluate. This role-to-constant correspondence matches the theoretical assignments in Section 7.4 without fitting.

![Figure 8. Constant role scorecard across the 51 passing transitions. Each of the three constants with sufficient occurrences appears predominantly in its theoretically assigned role: sqrt(2) at scaling transitions, ln 2 at compression transitions, phi at mid-network equilibria. e occurs only twice and is excluded from role analysis.](figures/10_constant-roles.png)

**Null-model baseline (look-elsewhere effect).** The pass rate cannot be interpreted without asking how often a *random* ratio would match some integer power of some tholonic constant within the same tolerance. A Monte Carlo estimate answers this directly: ratios drawn log-uniformly were scored with the identical rule (five constants $\{\pi/4, \phi, \sqrt{2}, \ln 2, e\}$, integer exponents, ±8% tolerance). The chance match rate depends strongly on the permitted exponent range: with $|k| \le 1$ it is 46% (ratios in $[0.25, 4]$) to 69% (ratios in $[0.5, 2]$); with $|k| \le 3$ it is 72 to 81%; with $|k| \le 8$ (the range needed to accommodate the observed $\phi^8$ match) it is 84 to 88%. Under the wider exponent ranges, the observed 78% headline rate is *within* the chance band, and even the most conservative range places chance near the 67% threshold. The honest conclusion is that the aggregate pass rate, by itself, is weak evidence: the match windows of five constants jointly cover most of log-ratio space. What the null model does *not* explain is role-consistency, which is the conjunction of a match and the *correct constant for the transition type*. Under a random assignment, each matching transition would draw its constant with no preference for the theoretically assigned role; the observed concentration ($\sqrt{2}$ at scaling, $\ln 2$ at compression, $\phi$ at equilibria) is the signal the permutation test in Section 12 is designed to quantify. This null analysis was added after the Stage 3 measurements and is therefore itself post hoc; the pre-registered replication must fix the exponent range in advance and report excess over the corresponding null rate, not over a fixed percentage threshold.

**Interpretation.** The data-driven detection demonstrates that the network's internal phase structure is real and detectable: the four metrics agree on boundary locations, and detected boundaries outperform assumed boundaries (78% vs. 42 to 58%) under the same scoring rule. Given the null-model coverage, however, the aggregate rate is not by itself evidence for the tholonic constants. The evidentially meaningful observation is the role-specific assignment: where matches occur, each constant appears in the role its tholonic assignment predicts, across architectures ranging from 6 to 48 layers and from 2019 through 2025 design generations. That correspondence was predicted in advance by Section 7.4 and is not produced by window coverage. It remains preliminary until the permutation and placebo controls of Section 12 are run.

**Limitations.** The $\phi^0 = 1$ stability-point passes are structurally meaningful but statistically weak: any ratio between 0.92 and 1.08 satisfies them. Excluding $k=0$ cases, 34/42 non-trivial transitions pass (81%). The transition-detection threshold (mean $+$ 1.5 SD) is a heuristic; a pre-registered protocol with held-out models is required for publication-quality claims. The detection pipeline has not been run on randomly initialized checkpoints of the same architectures; this untrained control (Section 12) is required to establish that the result is training-emergent rather than an artifact of architecture geometry, particularly given the Stage 1 finding that fixed-boundary ratios are architecturally determined. Full replication also requires protocol details not reported here: the elicitation corpus and sequence length used to generate activations, the precise norm definition (which norm, averaged over which positions), and the exponent range searched; these must accompany the pre-registered protocol. OPT-350m could not be evaluated due to a positional encoding tensor conflict. The LLaMA family (TinyLlama only) shows the lowest pass rate (50%), suggesting possible sensitivity to grouped-query attention or rotary embedding variants; broader LLaMA family coverage is needed.

### 13.4 Structural Health Grading: Five-Axis Assessment Across 14 Models

To supplement the phase-boundary detection results of Section 13.3, each model was assessed on five structural axes derived directly from the tholonic framework. The axes measure, independently: (1) **boundary fidelity**, the proportion of data-driven phase transitions whose norm ratio falls within ±8% of any tholonic constant; (2) **√2 scaling**, quality of √2 governance in the early-to-mid network (layers 20–55%); (3) **φ equilibrium**, quality of φ governance at mid-network stability points (layers 45–80%); (4) **ln2 compression**, quality of ln2 governance at the output-projection stage (layers 80–100%); and (5) **virial balance**, how close the mean D/C activation-RMS ratio is to the theoretical target of 0.5. Scores are 0–100, where 100 represents perfect tholonic alignment on that axis. The constant $e$ was excluded: it appears in only 2 of 65 detected transitions and carries no reliable structural signal. Four of the five axes are tabulated below; the √2 scaling axis is recorded in the analysis outputs but not reproduced here, and the Overall column is the model's composite across all five axes, so it cannot be recomputed from the tabulated columns alone.

| Model | Family | Fidelity | φ Equil | ln2 Comp | Virial | Overall |
|---|---|---|---|---|---|---|
| GPT-1 | GPT-1 | 67 | 40 | 25 | 0 | 26 |
| distilGPT-2 | GPT-2 | 67 | 25 | 40 | 0 | 26 |
| GPT-2 small | GPT-2 | 50 | 40 | 25 | 0 | 33 |
| GPT-2 medium | GPT-2 | 67 | 40 | 25 | 0 | 31 |
| GPT-2 large | GPT-2 | 75 | 40 | 87 | 0 | 47 |
| GPT-2 XL | GPT-2 | 100 | 40 | 25 | 0 | 33 |
| GPT-Neo 125m | GPT-Neo | 100 | 40 | 97 | 4 | 55 |
| GPT-Neo 1.3B | GPT-Neo | 71 | 40 | 25 | 23 | 36 |
| Pythia 160m | Pythia | 100 | 18 | 25 | 0 | 34 |
| Pythia 410m | Pythia | 83 | 40 | 62 | 0 | 44 |
| OPT 125m | OPT | 100 | 40 | 97 | 0 | 52 |
| Qwen2.5-0.5B | Qwen | 86 | **97** | 75 | 0 | 57 |
| Qwen3-0.6B | Qwen | 83 | 40 | 25 | 0 | 35 |
| TinyLlama-1.1B | LLaMA | 50 | 40 | 79 | 0 | 44 |

![Figure 9. Five-axis structural health profile across the 14 tested models, shown as a heatmap (boundary fidelity, phi equilibrium, ln2 compression, virial balance, and composite). The all-but-empty virial column is the dominant feature: no current architecture approaches the D/C = 0.5 equilibrium target.](figures/10_health-heatmap.png)

**The virial bottleneck.** The most striking result is structural rather than phase-based: 12 of 14 models score 0 on the virial-balance axis, and the remaining two score 4 and 23 respectively. All architectures are strongly C-dominant; measured D/C ratios range from approximately 0.08 to 0.32 against the theoretical target of 0.5. This is a direct empirical corroboration of the C-dominance prediction stated in Section 11.2: the architectural imbalance is not incidental but universal across seven families, six years of design generations, and model sizes from 82M to 1.1B parameters. The tholonic regulariser (Section 11.2) is designed specifically to close this gap during training; the consistently zero virial scores across all current architectures confirm both that the target state is not achieved spontaneously and that there is structural room for improvement.

![Figure 10. Virial balance axis scores for the 14 tested models. Twelve of fourteen score zero; the two non-zero scores (GPT-Neo 125m at 4, GPT-Neo 1.3B at 23) remain far from the 100 that would correspond to the D/C = 0.5 virial equilibrium. Measured D/C ratios across all models fall between approximately 0.08 and 0.32.](figures/10_virial-gap.png)

**Family trends.** Boundary fidelity (axis 1) and ln2 compression (axis 4) show the most inter-model variation and the clearest relationship with architecture quality. GPT-Neo 125m and OPT 125m each achieve ln2 compression scores of 97, indicating near-perfect tholonic governance of the output-projection stage. Qwen2.5-0.5B achieves the highest φ-equilibrium score (97), suggesting that its mid-network has the strongest self-similar stability of any model tested. More modern architectures (Qwen, GPT-Neo, OPT) consistently outscore older ones (GPT-1, distilGPT-2) on phase-structure axes, consistent with the hypothesis that training dynamics inadvertently favour tholonic organisation even without an explicit structural objective.

**Context-length perturbation test.** As an additional probe of whether the detected phase structure has functional reality, each model was run at three context lengths (128, 64, and 32 tokens) and the per-layer normalised hidden-state shift was measured: $s_l = \|h_l(\text{full}) - h_l(\text{short})\| / \|h_l(\text{full})\|$. The tholonic prediction is that the φ-equilibrium zone (layers 45–80%) should show *lower* sensitivity than surrounding layers: a self-stabilising attractor should absorb context perturbations better than non-equilibrium zones. A model passes if the mean sensitivity within the φ zone is lower than outside it (negative φ-advantage). The result across 14 models was 43% (6/14) for both the 64-token and 32-token conditions, below the pre-specified 67% threshold. The GPT-Neo family passed cleanly (GPT-Neo 125m was the only model to show a true U-shaped dip profile centred in the φ zone); the GPT-2 family failed consistently with large positive φ-advantages (+0.10 to +0.27). This below-threshold pass rate means the perturbation test does not independently confirm the φ-equilibrium prediction. It is reported here as an exploratory finding rather than supporting evidence; replication with more sensitive perturbation designs (e.g., attention mask perturbation rather than context truncation) remains an open task.

**Testable predictions from the health profile.** The axis scores generate concrete, falsifiable predictions. Models with stronger virial balance (axis 5) are predicted to: converge in fewer training steps for equivalent validation loss; assign better-calibrated output probabilities (reduced overconfidence); and degrade less in coherence over long-context generation. Models with stronger ln2 compression (axis 4) are predicted to show better top-$k$ diversity and less probability mass on irrelevant tokens. These predictions require controlled intervention experiments (training matched pairs with and without the tholonic regulariser) and correspond to the regularizer, robustness, and reward-hacking rows of the falsifiability table in Section 12. No existing architecture achieves a green rating (≥ 75) across all five axes; the virial axis is the primary structural gap between current models and the tholonic ideal.

### 13.5 The Alignment Argument Is Structural, Not Empirical

The claim that tholonic structure precludes destructive behavior is a structural argument, not an empirical claim about deployed neural networks. It does not entail that any currently deployed system is structurally tholonic, or that current systems are safe. The argument is: *if* a system is genuinely tholonically structured at all scales, *then* destroying its D and C components is structurally self-defeating. Whether current systems satisfy the antecedent is an open question.

### 13.6 The Symbolic AI Analysis Is Retrospective

The tholonic analysis of symbolic AI as D-dominant is retrospective: it accounts for the observed failure modes rather than predicting them in advance. This limits the strength of the symbolic AI analysis as evidence for the tholonic framework; it is consistent with the framework but not uniquely predicted by it.

---

## 14. Conclusion

The history of AI is the history of a conflict between two incomplete paradigms. Symbolic AI is D-dominant: it encodes definitional constraints with high precision but cannot learn beyond them. Connectionist AI is C-dominant: it integrates experience at scale but lacks structural D, making it vulnerable to specification gaming and alignment failure. Neurosymbolic approaches move toward balance but combine D and C modularly rather than architecturally.

The tholonic model provides a structural account of why neither paradigm alone suffices, what a complete architecture requires, and what behavioral properties a complete architecture would exhibit. A fully tholonic neural network, one that maintains N-D-C balance at every scale simultaneously through a self-similar recursive structure, would exhibit three properties not achievable by partial tholons:

1. The five constants ($e$, $\sqrt{2}$, $\ln 2$, $\pi/4$, $\phi$) would appear as co-emergent structural elements, with the other four governing within-level geometry and $\phi$ governing inter-level scaling.

2. The network would converge toward $\phi$-adjacent inter-level activation ratios through the same structural logic that drives $\phi$-based phyllotaxis in plants: the fixed point of the self-similar recursive N-D-C balance.

3. Most significantly, the network would find cooperative stability to be its lowest-energy N-state. A system that destroys its D-context (the world that gives it problems to solve) and severs its C-feedback (the interactions that allow it to remain calibrated) is eliminating the constitutive components of its own N-state. This is not a moral argument; it is a structural one. The Skynet scenario is not merely dangerous, it is structurally incoherent in a tholonic architecture, for exactly the reason a free quark is structurally incoherent.

The hydrogen atom does not need to be told to orbit at the Bohr radius. That radius is where the D-C balance lands. A tholonically-structured AI does not need to be told to be cooperative. Cooperative stability is where the N-D-C balance lands.

Whether this structural account can be operationalized into a concrete training procedure is an empirical question. Section 12 provides falsifiable predictions that would distinguish it from an empirical account. Empirical work (Section 13.3) provides qualified initial support: when phase boundaries are detected in a data-driven manner from the network's own internal dynamics, rather than assumed from theoretical framing, norm ratios at those boundaries match a tholonic constant at a 78% rate (51/65 transitions) across 14 models spanning seven architecture families. The Monte Carlo null model shows that the aggregate rate alone is weak evidence, since the match windows cover much of log-ratio space; the meaningful observation is that where matches occur, $\sqrt{2}$, $\ln 2$, and $\phi$ each appear in the role its tholonic assignment predicted in advance, across architectures from 6 to 48 layers and six years of design generations. The more ambitious predictions about faster convergence and improved alignment become worth pursuing experimentally once the role-consistency result survives the permutation, placebo, and untrained-checkpoint controls under a pre-registered protocol with held-out model families.

---

## References

### Tholonic Series (this paper's companions)

[M26a] Milton, J.W. (2026). Emergence of classical constants from a minimal recursive triadic framework. Clarity Coalition. [Paper 1 in series]

[M26b] Milton, J.W. (2026). Phase-resolved transparency classification in commodity supply chains: A structural triadic scoring framework (TVPCI). Clarity Coalition. [Paper 2 in series]

[M26c] Milton, J.W. (2026). A minimal recursive triadic framework for self-similar hierarchical systems. Clarity Coalition. [Paper 3 in series]

[M26d] Milton, J.W. (2026). Game-theoretic framing of the triadic balance condition. Clarity Coalition. [Paper 4 in series]

[M26e] Milton, J.W. (2026). The tholonic–twistor connection. Clarity Coalition. [Paper 5 in series]

[M26f] Milton, J.W. (2026). The qualitative nature of one, two, and three: Structural role assignment in minimal recursive systems. Clarity Coalition. [Paper 6 in series]

[M26g] Milton, J.W. (2026). Cambridge semantics and the tholonic framework. Clarity Coalition. [Paper 7 in series]

[M26h] Milton, J.W. (2026). The atom as a measurable tholon: From Einstein's incomplete electron to a field-first ontology. Clarity Coalition. [Paper 8 in series]

[M26i] Milton, J.W. (2026). The tholonic model as a candidate alternative to the Standard Model: Structural derivations and parameter reduction. Clarity Coalition. [Paper 9 in series]

[M20] Stroud, D. (2020). *Tholonia: The Mechanics of Existential Awareness*. Welkin Wall Publishing. ISBN 978-1-6780-2532-8.

### External References

[1] McCarthy, J., Minsky, M.L., Rochester, N., & Shannon, C.E. (1955). A proposal for the Dartmouth summer research project on artificial intelligence. *AI Magazine*, 27(4), 12–14 (reprinted 2006).

[2] Minsky, M., & Papert, S. (1969). *Perceptrons: An Introduction to Computational Geometry*. MIT Press.

[3] Crevier, D. (1993). *AI: The Tumultuous History of the Search for Artificial Intelligence*. Basic Books.

[4] Krizhevsky, A., Sutskever, I., & Hinton, G.E. (2012). ImageNet classification with deep convolutional neural networks. *Advances in Neural Information Processing Systems*, 25, 1097–1105.

[5] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, L., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30.

[6] OpenAI (2022). Introducing ChatGPT. OpenAI blog. https://openai.com/blog/chatgpt

[7] Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies*. Oxford University Press.

[8] Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control*. Viking.

[9] Turing, A.M. (1950). Computing machinery and intelligence. *Mind*, 59(236), 433–460.

[10] Newell, A., & Simon, H.A. (1976). Computer science as empirical inquiry: Symbols and search. *Communications of the ACM*, 19(3), 113–126.

[11] Newell, A., Shaw, J.C., & Simon, H.A. (1959). Report on a general problem solving program. *Proceedings of the International Conference on Information Processing*, 256–264.

[12] Shortliffe, E.H. (1976). *Computer-Based Medical Consultations: MYCIN*. Elsevier.

[13] Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. *Psychological Review*, 65(6), 386–408.

[14] Pfeiffer, J. (1958, July 8). Electronic brain teaches itself. *New York Times*.

[15] Rumelhart, D.E., Hinton, G.E., & Williams, R.J. (1986). Learning representations by back-propagating errors. *Nature*, 323, 533–536.

[16] LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. *Proceedings of the IEEE*, 86(11), 2278–2324.

[17] Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(8), 1735–1780.

[18] Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). Scaling laws for neural language models. arXiv:2001.08361.

[19] Hoffmann, J., Borgeaud, S., Mensch, A., et al. (2022). Training compute-optimal large language models. arXiv:2203.15556.

[20] Brown, T.B., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33.

[21] Goodhart, C.A.E. (1975). Problems of monetary management: The U.K. experience. *Papers in Monetary Economics*, Reserve Bank of Australia, Vol. 1. The popular phrasing "when a measure becomes a target, it ceases to be a good measure" is due to Strathern, M. (1997). "Improving ratings": Audit in the British university system. *European Review*, 5(3), 305–321.

[22] Christiano, P., Leike, J., Brown, T.B., Martic, M., Legg, S., & Amodei, D. (2017). Deep reinforcement learning from human preferences. *Advances in Neural Information Processing Systems*, 30.

[23] Ouyang, L., Wu, J., Jiang, X., et al. (2022). Training language models to follow instructions with human feedback. arXiv:2203.02155.

[24] Krakovna, V., Uesato, J., Mikulik, V., et al. (2020). Specification gaming: The flip side of AI ingenuity. DeepMind Blog.

[25] Perez, E., Huang, S., Song, F., et al. (2022). Red teaming language models with language models. arXiv:2202.03286.

[26] Bai, Y., Jones, A., Ndousse, K., et al. (2022). Constitutional AI: Harmlessness from AI feedback. arXiv:2212.08073.

[27] Elhage, N., Nanda, N., Olah, C., et al. (2021). A mathematical framework for transformer circuits. *Transformer Circuits Thread*. https://transformer-circuits.pub/2021/framework/index.html

[28] Conmy, A., Mavor-Parker, A.N., Lynch, A., Heimersheim, S., & Garriga-Alonso, A. (2023). Towards automated circuit discovery for mechanistic interpretability. arXiv:2304.14997.

[29] Garnelo, M., & Shanahan, M. (2019). Reconciling deep learning with symbolic artificial intelligence: Representing objects and relations. *Current Opinion in Behavioral Sciences*, 29, 17–23.

[30] Mao, J., Gan, C., Kohli, P., Tenenbaum, J.B., & Wu, J. (2019). The neuro-symbolic concept learner: Interpreting scenes, words, and sentences from natural supervision. arXiv:1904.12584.

[31] Besold, T.R., d'Avila Garcez, A., Bader, S., et al. (2017). Neural-symbolic learning and reasoning: A survey and interpretation. arXiv:1711.03902.

[32] LeCun, Y. (2022). A path towards autonomous machine intelligence. Meta AI. https://openreview.net/pdf?id=BZ5a1r-kVsf

[33] Bengio, Y. (2019). From system 1 deep learning to system 2 deep learning. *NeurIPS 2019 Keynote*.

[34] Marcus, G. (2018). Deep learning: A critical appraisal. arXiv:1801.00631.

[35] Ioffe, S., & Szegedy, C. (2015). Batch normalization: Accelerating deep network training by reducing internal covariate shift. arXiv:1502.03167.

[36] Ba, J.L., Kiros, J.R., & Hinton, G.E. (2016). Layer normalization. arXiv:1607.06450.

[37] Zhang, B., & Sennrich, R. (2019). Root mean square layer normalization. *Advances in Neural Information Processing Systems*, 32.

[38] Shwartz-Ziv, R., & Tishby, N. (2017). Opening the black box of deep neural networks via information. arXiv:1703.00810.

[39] Saxe, A.M., Bansal, Y., Dapello, J., et al. (2019). On the information bottleneck theory of deep learning. *Journal of Statistical Mechanics*, 2019(12).

[40] Kingma, D.P., & Ba, J. (2015). Adam: A method for stochastic optimization. arXiv:1412.6980.

[41] He, K., Zhang, X., Ren, S., & Sun, J. (2015). Delving deep into rectifiers: Surpassing human-level performance on ImageNet classification. arXiv:1502.01852.

[42] Shannon, C.E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.

[43] Su, J., Lu, Y., Pan, S., Wen, B., & Liu, Y. (2021). RoFormer: Enhanced transformer with rotary position embedding. arXiv:2104.09864.

[44] Tancik, M., Srinivasan, P.P., Mildenhall, B., et al. (2020). Fourier features let networks learn high frequency functions in low dimensional domains. arXiv:2006.10739.

[45] Douady, S., & Couder, Y. (1992). Phyllotaxis as a physical self-organized growth process. *Physical Review Letters*, 68(13), 2098–2101.

[46] Prusinkiewicz, P., & Lindenmayer, A. (1990). *The Algorithmic Beauty of Plants*. Springer-Verlag.

[47] Sutton, R. (2019). The bitter lesson. http://incompleteideas.net/IncIdeas/BitterLesson.html

[48] Omohundro, S.M. (2008). The basic AI drives. *Proceedings of the 2008 Conference on Artificial General Intelligence*, 171, 171–179.

[49] Turner, A.M., Smith, L., Shah, R., Critch, A., & Tadepalli, P. (2021). Optimal policies tend to seek power. *Advances in Neural Information Processing Systems*, 34.

[50] Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. (2017). Proximal policy optimization algorithms. arXiv:1707.06347.

[51] Skalse, J., Howe, N., Krasheninnikov, D., & Krueger, D. (2022). Defining and characterizing reward hacking. arXiv:2209.13085.

[52] Olah, C., Cammarata, N., Schubert, L., Goh, G., Petrov, M., & Carter, S. (2020). Zoom in: An introduction to circuits. *Distill*. https://distill.pub/2020/circuits/zoom-in/

[53] Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016). Concrete problems in AI safety. arXiv:1606.06565.

[54] Irving, G., Christiano, P., & Amodei, D. (2018). AI safety via debate. arXiv:1805.00899.

[55] Koh, P.W., Sagawa, S., Marklund, H., et al. (2021). WILDS: A benchmark of in-the-wild distribution shifts. arXiv:2012.07421.

[56] Stray, J. (2021). Aligning AI optimization to community well-being. *International Journal of Community Well-Being*, 4(4), 907–933. https://doi.org/10.1007/s42413-021-00155-x

[57] Settle, J.E. (2018). *Frenemies: How Social Media Polarizes America*. Cambridge University Press. See also: Bail, C.A., et al. (2018). Exposure to opposing views on social media can increase political polarization. *PNAS*, 115(37), 9216–9221.

[58] Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138.

[59] Ashby, W.R. (1952). *Design for a Brain: The Origin of Adaptive Behaviour*. Chapman & Hall.

[60] Hopfield, J.J. (1982). Neural networks and physical systems with emergent collective computational abilities. *PNAS*, 79(8), 2554–2558. See also: LeCun, Y., Chopra, S., Hadsell, R., Ranzato, M., & Huang, F.J. (2006). A tutorial on energy-based learning. In *Predicting Structured Data*. MIT Press.

---

*This paper is part of a series applying the tholonic model to measurable physical and computational systems. All tholonic claims should be understood as structurally motivated hypotheses within a speculative but internally consistent framework. They are not established science. The companion papers referenced here (M26a through M26i) are available from the author.*
