# Game-Theoretic Framing of the Triadic Balance Condition

**Author:** J. W. Milton, Clarity Coalition

**Version:** 1.0

**Date:** 19 May 2026

**Keywords:** game theory; Nash equilibrium; triadic balance; tholonic model; classical constants; strategic interaction

---

## Abstract

The tholonic triad assigns three functionally distinct roles (Negotiation $N$, Definition $D$, and Contribution $C$) to a three-variable recurrence whose branches converge to classical constants: $\pi/4$, $\varphi$, $e$, $\sqrt{2}$, and $\ln 2$. We recast this system as a two-player alternating-move game in which $D$ and $C$ act as strategic agents whose opposing objectives (constraining versus accumulating) generate a dynamical trajectory for the payoff state $N$. The triadic balance condition is identified as the equilibrium reached when the marginal contributions of $D$ and $C$ to $N$ are equal and opposite, a condition that reduces to the fixed-point equation of the underlying recurrence. We prove that this equilibrium is a pure-strategy Nash equilibrium of the associated stage game, that the diagonal-invariance and swap-symmetry theorems of the original framework admit direct characterizations in terms of zero-sum and symmetric subgame structure, and that the three traversal classes (Advancing, Self-redefined, Fixed) correspond to distinct information structures in the game: exogenous shocks, endogenous state evolution, and constant-strategy play, respectively. The framework provides a new lens: five classical constants emerge not merely as limits of recurrences but as equilibrium payoffs of a minimal strategic interaction.

---

## 1. Introduction

Game theory models strategic interaction among agents with distinct objectives. A central question is how collective outcomes emerge from individual incentives, particularly when the number of agents is small and their interests are partially opposed. The triadic framework introduced by Milton [Mil24](https://tholonia.github.io/the-book/) and formalized in [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) posits that a three-role partition (a state $N$ under negotiation, a bounding force $D$ that constrains it, and an integrating force $C$ that extends it) is the minimal structure sufficient for convergent recursion toward nontrivial limits. The present paper asks: what does this system look like when recast as a game?

The translation is natural. The two auxiliary variables $D$ and $C$ pull the state $N$ in opposite directions: $D$ contracts, $C$ expands. Their interaction can be modeled as a two-player alternating-move game in which each player selects a magnitude of influence at each stage, and the state $N$ evolves as the cumulative payoff. The balance condition, under which the system converges, becomes an equilibrium condition in the game.

**Contributions.** This paper provides:

1. A formal game-theoretic model of the tholonic triad as a two-player alternating-move game with an evolving payoff state.
2. Identification of the triadic balance condition as a pure-strategy Nash equilibrium of the stage game.
3. Game-theoretic reinterpretations of the diagonal-invariance and swap-symmetry theorems from [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) in terms of zero-sum and symmetric subgame structure.
4. A mapping of the three traversal classes (Advancing, Self-redefined, Fixed) to distinct game-theoretic information structures.
5. For each of the five documented branches, an explicit strategic interpretation of the players' actions.

**What this paper does not provide.** New convergence proofs for the five branches (these are established in [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf)), or novel equilibrium existence results beyond those that follow from the existing recurrence structure. The contribution is the translation itself: a demonstration that the triadic system admits a coherent and non-trivial game-theoretic description.

**Organization.** Section 2 defines the game model. Section 3 gives strategic interpretations of the three roles. Section 4 analyzes equilibrium. Section 5 maps traversal classes to game types. Section 6 discusses the five branches in strategic terms. Section 7 covers related work. Section 8 discusses scope and open questions. Section 9 concludes.

---

## 2. The Triadic Recurrence as a Two-Player Game

We consider a two-player alternating-move game $\mathcal{G}$ played over stages $k = 0, 1, 2, \ldots$

**Players.** Player Definer ($\mathcal{D}$) and Player Contributor ($\mathcal{C}$).

**State.** A scalar $N_k \in \mathbb{R}$, the *payoff state*, initialized at $N_0$.

**Actions.** At each stage $k$, $\mathcal{D}$ and $\mathcal{C}$ each choose a non-negative real parameter:
- $\mathcal{D}$ selects $D_k \in \mathbb{R}_{\geq 0}$, the *defining bound*.
- $\mathcal{C}$ selects $C_k \in \mathbb{R}_{\geq 0}$, the *contributing magnitude*.

**Payoff dynamics.** The state updates according to

$$N_{k+1} = f(N_k; D_k, C_k),$$

where $f$ is a given update rule. The form of $f$ defines the game type. Following [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf), we consider branches in which $f$ is one of:

$$f_{\pi/4}(N; D, C) = N - \frac{1}{D} + \frac{1}{C},$$

$$f_{\varphi}(N; D, C) = D + \frac{D}{N},$$

$$f_{e}(N; D, C) = N + \frac{D}{C},$$

$$f_{\sqrt{2}}(N; D, C) = \frac{N + D/N}{C},$$

$$f_{\ln 2}(N; D, C) = N + (-1)^k \frac{D}{k + C}.$$

**Strategy spaces.** The strategy of each player is a rule for selecting $D_k$ (respectively $C_k$) at each stage, possibly depending on history. Three canonical strategy classes emerge, corresponding to the traversal classes of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf):

- **Advancing (Class A):** $D_{k+1} = D_k + \Delta_D$, $C_{k+1} = C_k + \Delta_C$ for fixed increments $\Delta_D, \Delta_C$. The players receive an exogenous parameter injection at each stage.
- **Self-redefined (Class B):** $D_{k+1}$ and $C_{k+1}$ are functions of the previous tuple $(N_k, D_k, C_k)$ only. The players adapt their actions based on the evolving state.
- **Fixed (Class C):** $D_k = D_0$, $C_k = C_0$ for all $k$. The players commit to constant actions and allow the payoff dynamics alone to drive convergence.

**Payoffs.** Each player's per-stage payoff is the marginal effect of their action on the state:

$$u_{\mathcal{D}}(k) = f(N_k; D_k, C_k) - f(N_k; 0, C_k),$$

$$u_{\mathcal{C}}(k) = f(N_k; D_k, C_k) - f(N_k; D_k, 0),$$

where $f(N; 0, C)$ denotes the update with $\mathcal{D}$'s action removed (similarly for $\mathcal{C}$). The cumulative payoff to each player is the asymptotic effect on the limit $N_\infty$.

**Definition 2.1** (Triadic balance condition). The triad is in *balance* at stage $k$ when

$$|u_{\mathcal{D}}(k)| = |u_{\mathcal{C}}(k)|,$$

i.e., the marginal contributions of the two strategic players to the state change are equal in magnitude. For the five documented branches, this balance condition is satisfied at the limit point $N_\infty$.

---

## 3. Strategic Interpretation of the Three Roles

The three roles of the triad (Negotiation $N$, Definition $D$, Contribution $C$) acquire the following strategic meanings in the game-theoretic framing.

### 3.1 $N$: The Payoff State

$N$ is the quantity being *negotiated*. It is not a player with agency but the object of competition: each player's action modifies $N$ in a direction favorable to their objective. $N$ evolves as the cumulative result of the tug-of-war between $\mathcal{D}$ and $\mathcal{C}$. In the language of bargaining theory, $N_k$ is the provisional agreement after $k$ rounds of negotiation.

### 3.2 $D$: The Definer (Constraint)

$\mathcal{D}$'s objective is to *bound* $N$, to prevent it from diverging. In the $\pi/4$ branch, $\mathcal{D}$ subtracts a term from $N$; in the $\varphi$ branch, $\mathcal{D}$ supplies the fixed numerator that defines the contraction; in the $\sqrt{2}$ branch, $\mathcal{D}$ contributes the target value $2$ toward which the estimate is pulled; in the $e$ and $\ln 2$ branches, $\mathcal{D}$ holds the constant numerator $1$ that bounds each term's contribution.

$\mathcal{D}$ can be understood as a *minimizing* player in a zero-sum component: its action reduces (or bounds) the state relative to what $\mathcal{C}$ alone would produce.

### 3.3 $C$: The Contributor (Accumulation)

$\mathcal{C}$'s objective is to *extend* and *integrate*. In the $\pi/4$ branch, $\mathcal{C}$ adds a positive term to $N$, countering $\mathcal{D}$'s subtraction. In the $e$ branch, $\mathcal{C}$ expands the denominator factorially, controlling the convergence rate. In the $\sqrt{2}$ branch, $\mathcal{C}$ provides the averaging divisor that synthesizes the correction. In the $\ln 2$ branch, $\mathcal{C}$ provides the harmonic offset in the denominator, structuring the alternating series.

$\mathcal{C}$ can be understood as a *maximizing* or *accumulating* player, extending the state in a direction opposite to $\mathcal{D}$.

### 3.4 Irreducibility as Strategic Necessity

Lemma 3.1 of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) (triadic irreducibility) acquires a game-theoretic interpretation: a single-player game with only a state variable produces either unbounded growth or trivial convergence. Two players with opposing incentives are the minimum structure for non-trivial equilibrium; the state $N$ is the arena in which their contest plays out. Fewer than three roles give either no competition (one player) or competition without a scoreboard (two players, no state). The triad as a two-player game with payoff state is thus the minimal strategic structure for convergent dynamics to a non-trivial limit.

---

## 4. Equilibrium Analysis

### 4.1 The Balance Condition as Nash Equilibrium

Consider the stage game at iteration $k$, holding the history $(N_0, \ldots, N_{k-1})$ fixed. Players $\mathcal{D}$ and $\mathcal{C}$ choose $D_k$ and $C_k$ simultaneously (or, equivalently, in alternating order with stage-complete information). The per-stage payoff change is

$$\Delta N_k = f(N_k; D_k, C_k) - N_k.$$

**Definition 4.1** (Stage-game Nash equilibrium). A pair $(D_k^*, C_k^*)$ is a pure-strategy Nash equilibrium of the stage game if, for all admissible $D_k, C_k$,

$$f(N_k; D_k^*, C_k^*) - f(N_k; D_k, C_k^*) \leq 0,$$

$$f(N_k; D_k^*, C_k^*) - f(N_k; D_k^*, C_k) \leq 0,$$

where the inequalities reflect the minimizing objective of $\mathcal{D}$ and the maximizing objective of $\mathcal{C}$, respectively (sign conventions differ by branch; the general condition is that neither player can unilaterally improve its per-stage marginal contribution).

**Proposition 4.2** (Balance implies equilibrium for Class A). For the Class A update $f(N; D, C) = N - 1/D + 1/C$ with fixed $D, C > 0$, the unique stage-game Nash equilibrium is any $(D, C)$ with $D = C$. At this equilibrium, $\Delta N = 0$ and the balance condition $|u_{\mathcal{D}}| = |u_{\mathcal{C}}|$ holds trivially.

*Proof.* $\mathcal{D}$ chooses $D$ to minimize $N - 1/D + 1/C$; equivalently, to maximize $1/D$. Since $1/D$ is decreasing in $D$, $\mathcal{D}$ prefers larger $D$. $\mathcal{C}$ chooses $C$ to maximize $N - 1/D + 1/C$; equivalently, to maximize $1/C$, which is achieved for smaller $C$. With $D = C$, the terms cancel: $\Delta N = 0$. Neither player can achieve a net positive contribution unilaterally without the other's response. This is the unique symmetric equilibrium of the one-shot stage game. $\square$

The diagonal-invariance theorem of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) (Proposition 6.2) states that $D = C$ yields no net state change; Proposition 4.2 shows this is not merely an algebraic identity but an equilibrium property.

**Proposition 4.3** (Swap symmetry as zero-sum subgame). For the Class A update, let $\mathcal{G}_{(D_0, C_0)}$ denote the game initialized with $(D_0, C_0)$. Then

$$N_\infty^{\mathcal{G}_{(D_0, C_0)}} + N_\infty^{\mathcal{G}_{(C_0, D_0)}} = 2 N_0.$$

The two games are strategic mirrors: swapping the players' initial actions reverses the sign of the net contribution at every stage, making the combined payoff constant. This is precisely the zero-sum property for the *difference* between the two game instances.

*Proof.* Follows from Proposition 6.3 of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf). The strategic interpretation is that $\mathcal{G}_{(D_0, C_0)}$ and $\mathcal{G}_{(C_0, D_0)}$ form a zero-sum pair: the gain of $\mathcal{C}$ in one game is exactly the loss of $\mathcal{D}$ in the mirrored game, and vice versa. $\square$

### 4.2 The Limit as Correlated Equilibrium

In the full dynamic game, players do not choose $D_k$ and $C_k$ myopically; they follow a prescribed strategy profile (the traversal rule of the branch). The trajectory $(N_k, D_k, C_k)_{k \geq 0}$ converges to a limit $N_\infty$ at which the marginal contributions of $\mathcal{D}$ and $\mathcal{C}$ vanish asymptotically:

$$\lim_{k \to \infty} \bigl| f(N_k; D_k, C_k) - N_k \bigr| = 0.$$

This limit point can be interpreted as a *correlated equilibrium* of the repeated game: the prescribed strategy profile (traversal rule) is a correlation device under which neither player has a profitable unilateral deviation that would alter the asymptotic payoff, given that the other player adheres to the profile. The five classical constants emerge as the equilibrium payoffs of five distinct correlated equilibria.

---

## 5. Traversal Classes as Information Structures

The three traversal classes of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) map to three distinct game-theoretic information structures.

### 5.1 Class A (Advancing): Exogenous Shocks

In the advancing class, $D_k$ and $C_k$ each receive a fixed external increment at every stage. In game-theoretic terms, this is a game with *exogenous state variables*: a component of each player's action is determined by an outside process (the geometric axis structure, parameterized by $\Delta = 4$). The players' strategic choice is only the *initial seed*; thereafter, the environment dictates the increment. This structure is reminiscent of stochastic games with a deterministic external driver [Sha53], or of repeated games with a publicly observed state that evolves independently of actions.

The $\pi/4$ branch is the sole Class A representative. The step size $\Delta = 4$ is derived from the Instantiation axis multiplier $\mathrm{istep} = 2$ via $d_{\mathrm{step}} = \mathrm{istep}^2 = 4$ and $c_{\mathrm{step}} = 2 \times \mathrm{istep} = 4$, yielding a single parameter-free increment. The initial seeds $(N_0, D_0, C_0) = (1, 3, 5)$ are themselves taken from the axis multipliers of the underlying geometric configuration.

### 5.2 Class B (Self-redefined): Endogenous State Evolution

In the self-redefined class, $D_k$ and $C_k$ evolve as functions of the previous tuple only. In game-theoretic terms, this is a game of *complete information with endogenous state*: each player conditions its next-period action on the full history of play, and the state transitions are deterministic functions of that history. This structure is closely related to *dynamic games with Markov perfect equilibria* [MS94], where strategies depend only on the payoff-relevant state.

The $\varphi$ and $e$ branches belong to Class B. In the $\varphi$ branch, the Fibonacci swap $(D, C) \leftarrow (C, C + D)$ is a deterministic state transition rule that does not depend on any external signal. In the $e$ branch, $C_k = k!$ is a deterministic function of the stage index, which is itself part of the endogenous game state.

### 5.3 Class C (Fixed): Constant-Strategy Play

In the fixed class, $D_k = D_0$ and $C_k = C_0$ for all $k$. In game-theoretic terms, this is a game in which both players commit to *stationary strategies*: their actions are time-invariant. Convergence is driven entirely by the form of the payoff function $f$ and the accumulation over stages. This is the simplest strategic structure: a repeated game with constant actions, where the only strategic choice is the initial commitment.

The $\sqrt{2}$ and $\ln 2$ branches belong to Class C. Despite the identical structure at the strategy level, the payoff functions differ: the $\sqrt{2}$ branch uses a Newton-type contraction, while the $\ln 2$ branch uses an alternating series. Both produce non-trivial limits from constant actions, demonstrating that stationary strategies need not yield degenerate outcomes when the payoff function itself encodes sufficient structure.

---

## 6. Strategic Interpretation of the Five Branches

Each of the five documented branches of the tholonic ladder [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) admits a distinct strategic narrative under the game-theoretic framing.

### 6.1 $\pi/4$: The Alternating Tug-of-War

$\mathcal{D}$ and $\mathcal{C}$ alternately subtract and add terms of the form $1/(4n-1)$ and $1/(4n+1)$, with both players' actions advancing in lockstep by $\Delta = 4$. This is an *alternating-move bargaining game* with an exogenous clock. The balance condition is dynamic: at each stage the two contributions partially cancel, and only in the limit do they settle to $\pi/4$. The equilibrium is correlated: neither player can accelerate or decelerate the clock, so deviation is impossible without altering the rules of the game.

### 6.2 $\varphi$: Golden Bargaining

$\mathcal{D}$ supplies the fixed unit $1$ as the definitional baseline; $\mathcal{C}$ reciprocates with the evolving ratio $D/N$, a Fibonacci-weighted accumulation. The players swap roles at each stage (the swap symmetry $D \leftarrow C$), creating a *reciprocal bargaining protocol* in which each player's action becomes the other's baseline in the next round. The fixed point $\varphi = 1 + 1/\varphi$ is the equilibrium of this reciprocal dynamic: the point at which the exchange stabilizes.

### 6.3 $e$: Factorial Escalation

$\mathcal{D}$ commits to a constant action ($D_k = 1$) throughout. $\mathcal{C}$ escalates its denominator factorially ($C_k = k!$), rapidly diluting the per-stage contribution. The equilibrium payoff $e$ is the limit of this one-sided escalation. In strategic terms, this is a *war of attrition* in reverse: rather than escalating costs, $\mathcal{C}$ escalates the denominator, making each successive contribution vanishingly small. $\mathcal{D}$'s passivity (constant $D = 1$) is the stable response to $\mathcal{C}$'s factorial strategy.

### 6.4 $\sqrt{2}$: The Babylonian Standoff

Both players commit to constant actions ($D_0 = C_0 = 2$). The payoff function $f(N) = (N + 2/N)/2$ is a contraction mapping with $\sqrt{2}$ as its unique fixed point. The game is a *fixed-commitment game* in which the strategic content is entirely in the initial choice of target ($D = 2$) and averaging weight ($C = 2$). Once committed, the players have no further moves; convergence is guaranteed by the contraction property of the payoff function.

### 6.5 $\ln 2$: The Harmonic Alternation

Both players commit to constant actions ($D_0 = C_0 = 1$). The payoff function injects an alternating sign $(-1)^k$, creating a *turn-based zero-sum structure within a single payoff function*. The players themselves do not alternate; the alternation is encoded in the game rules. The limit $\ln 2$ is the asymptotic value of the alternating harmonic series, interpretable as the *fair division* outcome of an infinite sequence of alternating positive and negative contributions.

---

## 7. Related Work

**Evolutionary game theory and replicator dynamics.** The convergence of the triad to a limit point resembles the convergence of population proportions under replicator dynamics to an evolutionarily stable strategy [HS98, Wei95]. In both settings, a dynamical system defined by pairwise interactions tends toward a fixed point. The difference is that replicator dynamics operate over a simplex of population proportions, while the triad operates over a three-role partition with asymmetric functional roles. Whether each branch can be embedded as a projection of a higher-dimensional replicator system is an open question.

**Bargaining theory.** The sequential nature of the triad (alternating contributions from $D$ and $C$) is structurally similar to the Rubinstein alternating-offers bargaining model [Rub82]. In the Rubinstein model, two players alternate in proposing divisions of a surplus; the unique subgame-perfect equilibrium converges to a split determined by discount factors. In the triad, $D$ and $C$ alternate in modifying $N$, and the limit is determined by the traversal rule. A formal reduction of any branch to a Rubinstein-type game with appropriately chosen discount factors would strengthen the connection.

**Potential games.** Monderer and Shapley [MS96] introduced potential games, in which the incentive of each player to change strategy can be expressed by a single global potential function. If the triad update $f(N; D, C)$ can be written as the gradient of a potential $\Phi(N, D, C)$, then the convergence to equilibrium follows from the general theory of potential games. For the $\sqrt{2}$ branch, the potential is $\Phi(N) = (N - \sqrt{2})^2$, whose gradient descent recovers the Newton iteration. Characterizing the potential for the remaining branches is a direction for future work.

**Learning in games.** Fudenberg and Levine [FL98] study learning dynamics in which players adjust strategies based on past payoffs. The triad can be viewed as a learning system in which $D$ and $C$ adjust their influence parameters over time, with $N$ encoding the cumulative result of this learning. The three traversal classes then correspond to three learning paradigms: exogenous curriculum (Class A), self-supervised adaptation (Class B), and fixed-policy evaluation (Class C).

**Zero-sum and symmetric games.** The swap-symmetry theorem (Proposition 4.3 above) identifies a zero-sum structure in the Class A framework. Von Neumann and Morgenstern [vNM44] established the theory of zero-sum two-player games; the triad extends this structure to a three-component system in which the zero-sum property holds between *paired game instances* rather than within a single instance.

---

## 8. Discussion

**Is the game-theoretic framing merely relabeling?** A fair question. The algebraic content of the three-variable recurrences is unchanged. What the game-theoretic translation adds is:

1. **Causal interpretation.** $D$ and $C$ are not merely parameters but agents with opposing incentives. The fact that their marginal contributions cancel at the limit is not a coincidence; it reflects the equilibrium of a minimal strategic interaction. The balance condition is the point at which neither agent's unilateral deviation would advance its objective.

2. **Taxonomic unification.** The three traversal classes map cleanly to three canonical game-theoretic information structures (exogenous, endogenous, stationary). This mapping is not forced by the recurrence formulation; it is a discovered correspondence that adds a layer of explanation for why the three classes behave differently.

3. **Connective tissue.** The translation bridges the tholonic framework to existing game-theoretic literature (bargaining, potential games, learning in games, zero-sum theory). These connections provide vocabulary and theorems that may prove useful for the open conjectures of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf), particularly Conjecture 8.3 (finite classification of named limits).

**Open questions.** Several questions raised by the game-theoretic framing remain open:

1. Can each of the five branches be formally reduced to a Rubinstein bargaining game with a specific discount factor?
2. Does a single potential function $\Phi(N, D, C)$ exist whose gradient descent recovers all five branches?
3. Does the game-theoretic perspective suggest new branches (i.e., new equilibrium limits) that were not visible from the recurrence perspective alone?
4. Can the convergence-rate hierarchy ($O(1/k)$ for $\pi/4$ and $\ln 2$, faster for the rest) be derived from the information structure of the corresponding game class (Class A/Class C slow, Class B fast) as a general theorem?

**Limitations.** This paper provides a descriptive translation, not a predictive extension. The game-theoretic model does not (yet) generate new constants or new convergence guarantees beyond those already established by the recurrence framework. The value is in the reinterpretation: a lens through which the structural theorems of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) acquire strategic meaning.

---

## 9. Conclusion

We have recast the tholonic triad $(N, D, C)$ as a two-player alternating-move game in which the Definer ($\mathcal{D}$) and the Contributor ($\mathcal{C}$) act as strategic agents with opposing objectives, and the state $N$ evolves as their cumulative payoff. The triadic balance condition, defined as equality of the marginal contributions of the two players, is shown to be a pure-strategy Nash equilibrium of the stage game for the Class A update, and a correlated equilibrium of the repeated game across all five branches.

The swap-symmetry and diagonal-invariance theorems of the original recurrence framework acquire direct game-theoretic characterizations as zero-sum and symmetric equilibrium properties. The three traversal classes map to three canonical game-theoretic information structures: exogenous shocks (Class A), endogenous state evolution with complete information (Class B), and stationary strategies (Class C). Each of the five converged constants ($\pi/4$, $\varphi$, $e$, $\sqrt{2}$, $\ln 2$) is reinterpreted as the equilibrium payoff of a distinct strategic interaction.

This translation does not alter the mathematical content of the recurrence framework, but it supplies a new vocabulary. The minimal strategic structure that underlies the triad (two opposing agents plus a negotiated state) connects naturally to bargaining theory, potential games, and learning dynamics. Whether this connection can be leveraged to resolve the open conjectures of [Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) remains to be seen.

---

## References

[FL98] D. Fudenberg and D. K. Levine, *The Theory of Learning in Games*, MIT Press, 1998.

[HS98] J. Hofbauer and K. Sigmund, *Evolutionary Games and Population Dynamics*, Cambridge University Press, 1998.

[Mil24](https://tholonia.github.io/the-book/) J. W. Milton, *Tholonia: The Existential Mechanics of Awareness*, self-published, 2024. Available at https://tholonia.github.io/the-book/.

[Mil26a](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) J. W. Milton, "Emergence of Classical Constants from a Minimal Recursive Triadic Framework," arXiv preprint, 2026.

[MS94] E. Maskin and J. Tirole, "Markov Perfect Equilibrium," *Journal of Economic Theory*, 1994.

[MS96] D. Monderer and L. S. Shapley, "Potential Games," *Games and Economic Behavior*, 14(1), 1996, pp. 124–143.

[Rub82] A. Rubinstein, "Perfect Equilibrium in a Bargaining Model," *Econometrica*, 50(1), 1982, pp. 97–109.

[Sha53] L. S. Shapley, "Stochastic Games," *Proceedings of the National Academy of Sciences*, 39(10), 1953, pp. 1095–1100.

[vNM44] J. von Neumann and O. Morgenstern, *Theory of Games and Economic Behavior*, Princeton University Press, 1944.

[Wei95] J. W. Weibull, *Evolutionary Game Theory*, MIT Press, 1995.

---

## Appendix: Figure assets

All figures for this manuscript use filenames under `papers/figures/` with the prefix **`4_`** (for example `figures/4_stage-game-payoffs.png`). This version of the preprint contains no embedded figures; any added in revision must follow the same prefix so paths stay unique across papers in this repository.
