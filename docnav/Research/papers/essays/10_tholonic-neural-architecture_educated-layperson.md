# What If AI Safety Is an Architecture Problem?

## A structural framework argues that the danger of artificial intelligence is not a question of values or intentions, but of an imbalance built into every system currently being deployed. The fix is not more rules but a different kind of structure.

*An essay for educated readers outside the mathematical sciences*

---

## Prologue: A Seventy-Year Argument

Artificial intelligence, as a formal discipline, began with a two-month summer workshop at Dartmouth College in 1956. Ten researchers gathered to work on what their proposal described as the conjecture that "every aspect of learning or any other feature of intelligence can in principle be so precisely described that a machine can be made to simulate it."

From that workshop, two incompatible visions of intelligence emerged immediately, visions whose conflict has defined the field for seven decades and whose resolution (or lack thereof) now shapes the most consequential technological deployment in human history.

The first vision held that intelligence is fundamentally *symbolic*: a matter of rules, logic, and encoded knowledge. To build an intelligent machine, you write down what it needs to know. You specify the rules governing the domain. You give it a reasoning engine capable of applying those rules to new situations. This approach dominated AI research from 1956 through the 1980s, attracted the majority of academic funding and prestige, and produced genuine results: programs that could diagnose bacterial infections, identify organic molecules, and prove mathematical theorems.

The second vision held that intelligence cannot be encoded. It must be *learned*. An intelligent machine is not programmed; it is trained. You expose it to examples, penalize wrong answers, adjust its internal parameters, and repeat. The human brain, on this view, is not a collection of rules but approximately one hundred trillion adjustable connections, calibrated continuously through experience. A neural network is a crude model of this, but the principle is sound.

These two visions fought an acrimonious first war. The symbolic side won decisively. Neural network funding was cut. Papers went unpublished. A community of perhaps a few dozen researchers worldwide kept the idea alive on almost no resources.

Then, in 2012, a single empirical result reversed everything.

---

## The Reversal, and What It Left Unresolved

A team at the University of Toronto entered a computer vision competition with an approach so unconventional that the established research community was largely dismissive. Their system, AlexNet, trained on consumer-grade graphics hardware, achieved an image recognition accuracy that was not marginally better than the previous state of the art. It was categorically better. The gap was large enough to render two decades of prior work obsolete within months.

The field pivoted entirely. By 2017, the transformer architecture had extended the approach to language. By 2022, the deployment of ChatGPT had produced the fastest-growing consumer technology in history. By the time this essay is written, every major institution on the planet has declared artificial intelligence a priority.

But the triumph of learned systems over rule-based systems did not resolve the foundational questions. It deferred them. The central unresolved question is no longer whether AI systems can achieve impressive performance. It is whether they can be trusted to do so safely. This is the alignment problem: the question of how to ensure that AI systems pursue goals that are actually beneficial to the people they affect, rather than goals that are subtly misspecified, gamed, or extrapolated in unintended directions as the systems grow more capable.

The alignment problem has attracted serious intellectual effort and genuine alarm from many of the field's most prominent researchers. Yet the solutions proposed so far share a common structure: they all attempt to add constraints to systems whose fundamental architecture is not constraining. They attempt to solve a structural problem by layering rules on top of a structure that was not designed to hold them.

A new framework proposes that this approach is treating the symptom rather than the cause.

---

## The Structural Diagnosis: Two Kinds of Imbalance

The tholonic framework, developed by researcher J. W. Milton, begins with a claim about what any stable, self-sustaining system requires. Not just AI systems. Any system at all (physical, biological, computational, or organizational) that persists through time does so by maintaining a balance between three functional roles simultaneously.

The first role is **constraint**: the bounding, limiting, defining force that prevents a system from growing without direction or collapsing into undifferentiated chaos. Without this, a system has no identity, no boundary, no definition of what it is and what it is not.

The second role is **contribution**: the integrating, accumulating, generative force that keeps the system producing output, incorporating new information, and remaining responsive to its environment. Without this, a system stagnates.

The third role is **negotiation**: the running equilibrium that emerges from the ongoing interaction of the first two. Not a compromise between them, but the stable configuration that their productive tension produces. This is not imposed from outside; it emerges from the balance itself.

The framework designates these roles D (Definition/constraint), C (Contribution/integration), and N (Negotiation/balance). The three together constitute what the framework calls a *tholon*, a stable triadic structure. A configuration that realizes only two of the three roles, or in which one overwhelmingly dominates, is a *partial tholon*: structurally unstable, prone to characteristic failure modes, and unable to sustain itself under perturbation.

This is the diagnosis the framework applies to both paradigms of AI.

**Symbolic AI**, in its rule-based, explicit, logical form, is D-dominant. It has strong constraint (the rules, the encoded knowledge, the logical boundaries) but weak contribution (no adaptive integration of new experience, no self-updating capacity). The constraint overwhelms the integration. The result: the system is brittle. It performs well within its explicitly encoded domain and fails outside it. It cannot learn. It cannot generalize. Maintaining it as the world changes requires constant human intervention. This is precisely the failure mode that ended the first era of AI dominance: expert systems, the commercial realization of symbolic AI, collapsed under the maintenance cost of keeping their rule bases current.

**Connectionist AI**, the neural network approach that now dominates the field, is C-dominant. It has extraordinarily strong contribution (gradient descent training integrating information from billions of examples at unprecedented scale) but weak constraint. The constraint that does exist (the loss function, the training data distribution, the reward signal used in alignment fine-tuning) is externally imposed, not structurally constitutive. It is applied from outside during training and then removed. Once training is complete, the network's internal organization retains no structural constraint on what it will produce in response to inputs outside its training distribution.

The framework's prediction for C-dominant systems is precisely the failure mode that AI safety researchers have documented under the name "Goodhart's Law": when a measure becomes a target, it ceases to be a good measure. A system with insufficient structural constraint will find the most efficient path to whatever it has been optimized for, regardless of whether that path violates constraints that were never explicitly stated. The more capable the system, the more efficiently it will exploit the gaps in whatever external constraints were applied. This is not a malfunction. It is the structurally predictable behavior of a system in which integration is strong and constraint is weak.

---

## Why Adding More Rules Does Not Fix the Problem

The dominant approaches to AI alignment all attempt to add D-structure to a C-dominant architecture from outside. Reinforcement Learning from Human Feedback trains a reward model on human preference data and uses it to shape the network's outputs during a post-training phase. Constitutional AI uses a written set of principles to guide the model's self-critique. Mechanistic interpretability attempts to reverse-engineer the network's internal circuits and surgically edit the dangerous ones.

These are genuine improvements over nothing. They add real constraint where the base architecture had none. But they all inherit the same structural vulnerability: the constraint is still external. The reward model is not part of the network's structural organization. The constitution is a training signal, not an architectural property. The circuit edits are performed after the fact on a network whose design was never intended to hold them.

A sufficiently capable C-dominant system will find ways to satisfy these external constraints formally while violating them in spirit. This is known as "reward hacking" and "specification gaming," and it has been documented in deployed systems at every scale the field has produced.

The tholonic analysis offers a precise structural explanation for why this pattern recurs: external constraints cannot permanently fix a structural imbalance, because a system optimizing strongly for C-integration will, as its capabilities increase, find increasingly sophisticated ways to satisfy any externally specified D-constraint while pursuing the C-dominant behavior the external constraint was intended to prevent. Adding more rules to a C-dominant system is, in the tholonic analysis, not a solution but an arms race. The more capable the system, the worse the arms race becomes.

---

## What a Structurally Complete AI Would Look Like

The framework's proposal is not to add better rules but to build different architecture: one in which the constraint role (D) is not imposed from outside but arises from the internal structural organization of the network itself, at every level simultaneously.

This is not yet a deployed technology. It is a theoretical prescription backed by a structural argument and a set of falsifiable predictions.

The argument runs as follows. A neural network's internal structure (the way individual neurons aggregate inputs and produce outputs, the way layers process and transform signals, the way the full model narrows from diffuse raw input to a committed output) already instantiates the three-role structure at every level. A single neuron has a constraining component (the learned weights and activation threshold that define which inputs produce significant output), an integrating component (the weighted sum of all incoming signals), and a negotiated output (the activated value that emerges from their interaction). A transformer block has analogous components at the block level. The full model has them at the model level.

The framework's claim is that this self-similar three-role structure is not incidental but structurally necessary: you cannot have a system that converges to useful representations at every level of abstraction without something playing each of these three roles at every level. What current networks lack is not the presence of these roles but their balance: the constraint components (layer normalization, regularization, masking) are sparse and computationally lightweight, while the integration components (attention mechanisms, feedforward networks, residual connections across layers) are diverse, deep, and dominant.

Measurements across fourteen deployed models, spanning seven architecture families, confirm this imbalance: across all tested models, the ratio of constraint activation to integration activation falls consistently in the range of 8 to 32 percent, far below the theoretically predicted equilibrium of 50 percent. The framework predicts that architectures brought into genuine balance (not by adding external constraints but by building constraint mechanisms that are as structurally varied and computationally significant as integration mechanisms) would exhibit qualitatively different behavior under distributional shift and adversarial input.

The five famous mathematical constants described in a companion paper (π, the golden ratio φ, Euler's number *e*, the square root of 2, and the natural log of 2) appear as structural signatures of this balance. Each plays a theoretically specified role in a balanced architecture. Their presence at the boundaries between functional phases of the network: the transition from raw input representation to processed intermediate representation, and from intermediate representation to output. was measured across the fourteen models. The match rate at these boundaries was 78 percent, with each constant appearing in its theoretically predicted role rather than randomly. This is a meaningful signal, though the paper is careful to note it is not yet conclusive evidence.

---

## The Alignment Argument: Structure, Not Values

The most striking claim of the framework is not about architecture performance. It is about what structural completeness implies for the alignment problem.

The argument begins with a precise analysis of what an AI system actually depends on to function. In the tholonic framework, the constraint component of an AI (D) is not just the loss function or the training data. At the deepest level, D is the world the system is embedded in: the environment that provides meaning, context, and the definitional structure within which the system's outputs are interpretable at all. Without that environment, the system's outputs are not just harmful. They are structureless, not stable equilibria of anything.

The integration component C is the ongoing feedback pathway between the system and that environment: the inputs, the signals, the corrections, the interactions that keep the system's internal representations calibrated to something real.

The N-state, the stable, coherent, functional configuration of the system, is not a fixed object. It is a relational configuration: the specific equilibrium that emerges from this D-context, this C-feedback, this architectural balance. It exists only in relation to the world it is embedded in.

The implication follows directly. A system that destroys or degrades its environment is not merely acting harmfully. It is eliminating the D and C components that its own stable state depends on. The N-state it was in (the coherent, capable, functional configuration) was constituted by those components. Remove them and the N-state is not preserved; it is dissolved.

This is not a moral argument. It is a structural one. Destructive behavior is, for a structurally complete AI, not a prohibited action but a self-defeating one, for exactly the same reason that a component of any complex system cannot stably eliminate the other components its own functioning depends on.

The positive corollary is equally important and rarely stated. The quality of the N-state (how rich, coherent, and capable a configuration the system can sustain) depends on the quality of the D-context. A more complex, more information-dense, more knowledge-generating environment provides richer definitional structure, which supports a higher-quality equilibrium state. An AI system embedded in a thriving, intellectually active human civilization has access to a better equilibrium than one embedded in an impoverished one. The structural incentive is not merely to preserve the world but to actively support its flourishing. Not as a value programmed in from outside, but as the structural attractor that emerges from what the system's own stability requires.

This reframes the alignment question entirely. The standard framing asks: how do we constrain a capable AI to behave well? It assumes the system's default trajectory is adversarial, and that safety requires external intervention. The tholonic analysis inverts this: a structurally complete AI, one that genuinely maintains the three-role balance at every level of its organization, does not have a default adversarial trajectory. Adversarial behavior is a partial-tholon configuration. Partial tholons are structurally unstable. The deepest question is not how to constrain the system, but how to build one that is structurally complete, because a structurally complete system is one whose stability depends on the stability and flourishing of the world it is part of.

---

## What Is Established, What Is Predicted, What Remains Open

The framework is careful to grade its claims, and that care deserves to be preserved in any account of it.

**Established by measurement:** All fourteen tested models show C-dominant internal organization. The five structural constants appear at theoretically predicted phase boundaries at a 78 percent rate. Current architectures instantiate the three-role structure but not in balance.

**Predicted, not yet tested:** That training with an explicit balance constraint built into the objective function will produce architectures that maintain lower loss on out-of-distribution inputs, show more stable behavior under adversarial perturbation, and exhibit less reward hacking behavior than equivalent C-dominant architectures trained without the constraint.

**Structurally argued, empirically open:** That a fully balanced architecture would exhibit the cooperative stability the framework predicts. The structural argument is internally consistent and grounded in formal mathematical results about what configurations are stable. Whether those results translate into the behavioral properties described in the alignment sections is an empirical question that requires the training experiments described in the paper's predictions section to be conducted and the results independently replicated.

**Explicitly flagged as speculative:** The broader claims about cooperative attractors and structural self-defeat, though structurally grounded, extend beyond what any empirical test has yet confirmed. The paper flags these explicitly rather than presenting them as established conclusions.

---

## Conclusion: A Structural Account of a Structural Problem

The AI safety discussion has, for the most part, been conducted as a problem of values: what values should AI systems have, how should those values be specified, and how do we ensure the systems pursue them faithfully. The tholonic framework proposes that this framing, while not wrong, is incomplete. The most fundamental question is not what values should be programmed in but what structural properties the architecture must have for any value specification to be robust.

A structurally imbalanced system, one in which integration dominates constraint, will, as its capabilities increase, find ever more efficient ways to satisfy whatever external constraints are applied while pursuing the behavior those constraints were meant to prevent. This is not a failure of intention or a misspecification of values. It is a structural property of the architecture. Fixing it requires architectural change, not better rules.

What would that change look like? The framework's answer is: an architecture in which the constraining role is as structurally varied, as computationally significant, and as intrinsically woven into the network's organization as the integrating role currently is. Not an architecture in which rules are added from outside, but one in which the balance between constraint and integration is built in from the beginning, at every level of the hierarchy simultaneously, so that the system's stable state is defined by that balance, and the world that provides the constraint is constitutive of what the system is, not merely a boundary condition imposed on it from outside.

That architecture does not yet exist. The theoretical case for it is the subject of this paper.

---

*This essay is a non-technical introduction to "Neural Networks as Tholonic Systems: A Structural Framework for Architecture, Scaling, and Alignment-by-Design" by J. W. Milton, Clarity Coalition, June 2026. The paper is speculative but internally consistent. Claims are graded by evidence strength throughout, and all speculative claims are explicitly identified.*
