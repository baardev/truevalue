# Math FAQ: The Tholonic Recurrence and Its Constants

This document answers mathematically precise questions about the tholonic recurrence: what it is, where the five constants come from, what has been formally proved, what remains conjectural, and how the framework relates to classical mathematics. It assumes comfort with sequences, limits, and basic calculus. Readers who want the full formal treatment should read the primary paper at [docnav/Research/papers/1_recursive-tholonic-five-constants.md](docnav/Research/papers/1_recursive-tholonic-five-constants.md).

> **Proof status:** This FAQ clearly distinguishes between proved results and open conjectures. Claims marked **[proved]** have formal proofs in the paper. Claims marked **[conjectural]** are numerically supported but not yet formally proved.

---

## The Core Recurrence

### What is the tholonic recurrence?

It is a family of three-variable discrete dynamical systems. Each branch is defined by an initial triple $(N_0, D_0, C_0)$ and an update rule of the form

$$N_{k+1} = f(N_k;\, D_k,\, C_k)$$

together with a *traversal rule* specifying how $(D_k, C_k)$ evolve at each step.

The three variables have fixed functional roles that persist across all five branches:

- $N$ (negotiation): the running state; the quantity being iteratively refined. It is what emerges.
- $D$ (definition/limitation): the constraining, bounding force. It limits the state.
- $C$ (contribution/integration): the accumulating, synthesizing force. It grows the state.

These are not just labels for three numbers. The roles are structurally distinct: $D$ always acts as a boundary and $C$ always acts as an integrator, even when their numerical values happen to be equal (as in the $\sqrt{2}$ branch, where $D_0 = C_0 = 2$).

Five specific choices of initial triple and traversal rule produce five classical mathematical constants as limits: $\pi/4$, $\varphi$ (the golden ratio), $e$ (Euler's number), $\sqrt{2}$, and $\ln 2$.

---

### Why exactly three variables? Why not two?

This is answered by a formal lemma in the paper. **[proved]**

The argument is this: any recurrence where a state variable $N$ is being refined by two functionally independent control forces (one that limits, one that integrates) cannot collapse to two variables without destroying the independence of those forces. If you use only two variables, both control roles must be determined by a single auxiliary variable, which forces them to move together. The two roles are then not independent: they are the same quantity in different clothing.

In concrete terms: if you try to write the $\sqrt{2}$ branch with only two variables, you either lose the corrective force ($D/N$) or the averaging synthesis (division by $C$). Remove either and the iteration does not converge to $\sqrt{2}$. In the $e$ branch, $D = 1$ (fixed boundary, never changes) and $C$ grows as a factorial (expanding integrator, changes every step). They begin at the same numerical value but immediately diverge in behaviour. Merging them into a single variable erases the structural distinction between "that which limits" and "that which integrates," and the series no longer produces $e$.

Two variables produce either unconstrained growth or static limitation. Three variables produce the dynamic tension that converges to a non-trivial constant.

---

### What are the five branches and what do they each converge to?

The complete branch specification **[proved]**:

| Limit | $N_0$ | $D_0$ | $C_0$ | $N_{k+1}$ | Traversal rule |
|---|---|---|---|---|---|
| $\pi/4$ | 1 | 3 | 5 | $N - 1/D + 1/C$ | $D \leftarrow D+4$, $C \leftarrow C+4$ |
| $\varphi$ | 1 | 1 | 2 | $D/C + 1$ | $D \leftarrow C$, $C \leftarrow C+D$ |
| $e$ | 0 | 1 | 1 | $N + D/C$ | $C \leftarrow C \cdot k$ (factorial growth) |
| $\sqrt{2}$ | 1 | 2 | 2 | $(N + D/N)/C$ | $D$, $C$ fixed |
| $\ln 2$ | 0 | 1 | 1 | $N + (-1)^k \cdot D/(k+C)$ | $D$, $C$ fixed |

Each branch reduces to a classical result: the Leibniz series ($\pi/4$), Fibonacci ratios ($\varphi$), the reciprocal factorial series ($e$), the Newton-Babylonian (Heron) method ($\sqrt{2}$), and the alternating harmonic series ($\ln 2$). The convergence of each is proved from these classical results.

---

### How are the five branches classified?

The branches fall into three traversal classes based on how $(D_k, C_k)$ evolve. **[proved]**

**Class A (Advancing):** $(D_k, C_k)$ each receive a fixed external increment at every step. New information is injected from outside at each iteration. Only the $\pi/4$ branch belongs to this class.

**Class B (Self-redefined):** $(D_k, C_k)$ evolve by a transformation of their own current values. No external constant is injected beyond the iteration counter. The $\varphi$ branch uses a Fibonacci swap ($D \leftarrow C$, $C \leftarrow C + D$). The $e$ branch multiplies $C$ by $k$ (factorial growth). Both are Class B.

**Class C (Fixed):** $(D_k, C_k)$ are held constant at their seed values for all $k$. Convergence is driven entirely by the update map $f$. The $\sqrt{2}$ and $\ln 2$ branches are Class C.

This trichotomy is clean: one Class A, two Class B, two Class C.

---

## Each Branch Explained

### How does the $\pi/4$ branch work?

Starting from $(N_0, D_0, C_0) = (1, 3, 5)$ with step $\Delta = 4$, each iteration subtracts $1/D_k$ and adds $1/C_k$, while $D$ and $C$ each advance by 4. At iteration $n$, $D_n = 4n - 1$ and $C_n = 4n + 1$. The net contribution per step is:

$$-\frac{1}{4n-1} + \frac{1}{4n+1} = \frac{-2}{(4n-1)(4n+1)} = \frac{-2}{16n^2 - 1}$$

The accumulated sum is a regrouping of consecutive pairs from the Leibniz series $1 - 1/3 + 1/5 - 1/7 + \cdots$, which converges to $\pi/4$. **[proved]**

The step size $\Delta = 4$ is not arbitrary. It derives from the tholonic geometry: the Instantiation axis of the triangular figure has multiplier 2, and $\Delta = 2^2 = 4$ (or equivalently $2 \times 2 = 4$). Both operations on the same geometric constant yield the same integer. The seeds $3$ and $5$ are also geometrically derived: each role takes its seed from the axis that excludes it. **[proved for the step derivation; see Section 2.1 of the paper]**

The $\pi/4$ branch is structurally unique: it is the only Class A branch, the only branch requiring three numerically distinct seeds $\{1, 3, 5\}$, and the only branch that does not converge from the primitive seed set $\{0, 1, 2\}$. **[proved]**

Convergence is the slowest of the five: $O(1/k)$ per step, intrinsic to the alternating series structure. After $10^5$ iterations, the residual is approximately $1.2 \times 10^{-6}$.

---

### Why does the recurrence produce $\pi/4$ and not $\pi$?

There are four independent reasons, each sufficient on its own and mutually reinforcing.

**1. The recurrence computes $\arctan(1)$, not a circumference.**

$\pi$ arises as the ratio of a circle's circumference to its diameter, which requires measuring a continuous curve against a linear length. The tholonic recurrence works entirely with unit fractions: at step $k$ it subtracts $1/D_k$ and adds $1/C_k$. That pattern is an alternating series of unit fractions, which is precisely the Leibniz-Gregory series for $\arctan(1)$:

$$\frac{\pi}{4} = \arctan(1) = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots$$

There is no step in the recurrence that constructs a circumference or measures a diameter. $\pi$ is not accessible through a unit-fraction alternating series; $\pi/4$ is. The recurrence produces what it actually computes, and what it computes is $\arctan$ at the point of perfect balance: $\arctan(1)$, the angle at which D and C contributions are equal.

**2. The geometry fixes the step $\Delta = 4$, not $\Delta = 1$.**

The step size is not a free parameter. It is derived from the instantiation axis multiplier $\text{istep} = 2$ of the tholonic geometry via two operations: squaring ($2^2 = 4$) and doubling ($2 \times 2 = 4$). Both yield 4. The step $\Delta = 4$ ensures that $D_k = 4k - 1$ and $C_k = 4k + 1$, the $(4n-1, 4n+1)$ pairs required for the Leibniz series. The step is geometric necessity, and the step produces $\pi/4$.

**3. The seeds come from the axes of the excluded roles, and those seeds are $(1, 3, 5)$.**

Each axis in the tholonic geometry connects two role vertices and excludes the third. The axis multiplier of the excluded role supplies the seed for that role: the Contribution axis (multiplier 3) gives $D_0 = 3$; the Definition axis (multiplier 5) gives $C_0 = 5$; the Instantiation axis (multiplier 2) gives the multiplicative identity $N_0 = 1$. To produce $\pi$ directly you would need different seeds and a divergent step structure. The axis geometry does not make those seeds available.

**4. $\pi/4$ is the per-element primitive; $\pi$ is the full generation.**

Multiplying the emergent primitive by the step that generated it recovers $\pi$:

$$\frac{\pi}{4} \times \Delta = \frac{\pi}{4} \times 4 = \pi$$

The step $\Delta = 4$ counts exactly the number of distinct roles in one complete tholonic generation: the parent $N$, the $D$ pole, the $C$ pole, and the child $N$ that instantiates from their interaction. $\pi/4$ is the constant that belongs to a single role slot. $\pi$ is what you get when one full generation, all four positions, is accounted for. The recurrence advances one role slot at a time, so it naturally produces the per-slot quantity. $\pi$ is not absent; it is the product of the primitive and the generation size. The framework distinguishes the two precisely because the triadic structure has four positions per cycle, not one.

---

### How does the $\varphi$ branch work?

Starting from $(N_0, D_0, C_0) = (1, 1, 2)$, the traversal is the Fibonacci swap: $D \leftarrow C$, $C \leftarrow C + D$. This maintains $(D_k, C_k) = (F_{k+2}, F_{k+3})$, consecutive Fibonacci numbers. The update $N_{k+1} = 1 + D_k/C_k$ tracks the ratio of consecutive Fibonacci terms, which converges to $1/\varphi$. Therefore $N_\infty = 1 + 1/\varphi = \varphi$, by the defining identity $\varphi = 1 + 1/\varphi$. **[proved]**

Convergence is linear with geometric ratio $\varphi^{-2} \approx 0.382$ per step. The branch reaches machine precision within a few dozen iterations.

In role terms: $D$ is always the smaller (prior) Fibonacci term, the boundary. $C$ is always the larger accumulated term, the integrator. The ratio $D/C$ is always less than 1, pulling $N$ toward $\varphi$ from below.

---

### What metallic ratios are represented in the tholonic ladder?

All of them. **[proved]**

The metallic means are the infinite family $\sigma_m = (m + \sqrt{m^2+4})/2$ for positive integers $m$. They all satisfy the same fixed-point identity:

$$\sigma_m = m + \frac{1}{\sigma_m}$$

The $\varphi$ branch exploits exactly this identity via $N_{k+1} = 1 + D_k/C_k$, with the Fibonacci swap driving $D_k/C_k \to 1/\varphi$. The parametric extension replaces the additive base $N_0 = 1$ with any positive integer $m$ and the Fibonacci traversal $C \leftarrow C + D$ with the generalized rule $C \leftarrow mC + D$. The result maintains consecutive terms of the generalized Fibonacci recurrence $G_{k+1} = mG_k + G_{k-1}$, whose ratio converges to $1/\sigma_m$, giving $N_\infty = m + 1/\sigma_m = \sigma_m$.

The first few members:

| $m$ | Name | Value | Tholonic traversal rule |
|---|---|---|---|
| 1 | Golden | $\varphi \approx 1.618$ | $C \leftarrow C + D$ (canonical $\varphi$ branch) |
| 2 | Silver | $1 + \sqrt{2} \approx 2.414$ | $C \leftarrow 2C + D$ |
| 3 | Bronze | $(3+\sqrt{13})/2 \approx 3.303$ | $C \leftarrow 3C + D$ |
| 4 | Copper | $2 + \sqrt{5} \approx 4.236$ | $C \leftarrow 4C + D$ |

Only the golden ratio ($m = 1$) is one of the canonical five branches. The rest are members of the proved parametric extension (Proposition 6.6(ii) of the primary paper). The triadic grammar, three roles $N$, $D$, $C$ with the same functional assignments, is identical across all values of $m$. The entire infinite family follows from a single tholonic rule, with $m$ as the only free parameter.

---

### How does the $\sqrt{2}$ branch work?

Starting from $(N_0, D_0, C_0) = (1, 2, 2)$ with $D$ and $C$ fixed, the update is:

$$N_{k+1} = \frac{N_k + D/N_k}{C} = \frac{N_k + 2/N_k}{2}$$

This is Newton's method (equivalently, the Babylonian method, known to Heron of Alexandria) for finding the square root of 2. At the fixed point $N^* = \sqrt{2}$, the derivative of the update map is zero: $g'(\sqrt{2}) = (1 - 2/N^2)/2\big|_{N=\sqrt{2}} = 0$. This gives quadratic convergence: the number of correct digits roughly doubles with each iteration. **[proved]**

$D = 2$ is the target: the defining specification the iteration is converging toward. $C = 2$ is the averaging divisor: the synthesizer that takes the geometric mean of the overshoot and undershoot. They begin equal but serve opposite functions. Removing $D/N_k$ eliminates the corrective force. Dividing by 1 instead of $C = 2$ gives a different iteration that does not converge to $\sqrt{2}$.

The branch generalises directly: replacing $D = 2$ with $D = a$ gives Newton's method for $\sqrt{a}$, with quadratic convergence for any $a > 0$. **[proved]**

---

### How does the $e$ branch work?

Starting from $(N_0, D_0, C_0) = (0, 1, 1)$, $C$ grows by factorial multiplication at each step: $C_k = k!$. The update accumulates $D/C_k = 1/k!$. The running sum is $\sum_{k=0}^{K} 1/k!$, which converges to $e$ as $K \to \infty$. **[proved]**

$D = 1$ is fixed throughout: the unchanging numerator, the boundary that never changes. $C$ starts at 1 and grows factorially: $1, 1, 2, 6, 24, 120, \ldots$ Each subsequent term contributes a smaller and smaller fraction of 1 to the total. The factorial growth of $C$ makes this the fastest-converging of the five branches: super-exponential convergence, reaching machine precision within about 20 iterations.

A useful variant: if $N_0 = 2$ instead of 0, the branch converges to $e + 2$. The offset equals $N_0$ exactly. This holds for any pure-accumulation branch (one where the update adds to $N_k$ without using $N_k$ in the formula): the seed enters the limit additively and cannot be absorbed. **[proved]**

---

### How does the $\ln 2$ branch work?

Starting from $(N_0, D_0, C_0) = (0, 1, 1)$ with $D$ and $C$ fixed, the update alternates:

$$N_{k+1} = N_k + (-1)^k \frac{D}{k + C} = N_k + (-1)^k \frac{1}{k + 1}$$

This accumulates the alternating harmonic series: $1 - 1/2 + 1/3 - 1/4 + \cdots$, which converges to $\ln 2$. **[proved]**

Like the $\pi/4$ branch, convergence is $O(1/k)$: the slowest class, intrinsic to the alternating-series structure. After $10^5$ iterations, the residual is approximately $5 \times 10^{-6}$.

$D = 1$ is the fixed numerator: the defining boundary. $C = 1$ is the offset in the harmonic denominator: the integration base that steps through $1, 2, 3, \ldots$ As in the $e$ branch, $D$ and $C$ begin at the same numerical value but immediately diverge in structural function: one limits, one integrates.

The physical interpretation in the tholonic framework is temporal: the harmonic denominators $1/k$ represent diminishing marginal contributions over time. Early terms contribute a full unit; each subsequent term contributes less. This is the mathematical signature of a transformation process where the largest inputs arrive first and subsequent contributions decay, which is why the $\ln 2$ branch is used to score Transformation Efficiency.

---

## Structural Theorems

### What algebraic properties have been proved about the recurrence family as a whole?

Four structural theorems distinguish the tholonic ladder from an arbitrary collection of known limits. **[all four proved]**

**Seed partition.** The $\pi/4$ branch is the unique branch requiring three numerically distinct seeds; its seed set is $\{1, 3, 5\}$. The other four branches all draw seeds from the primitive set $\{0, 1, 2\}$: the four and smallest non-negative integers sufficient to distinguish zero, unit, and first duality. This clean partition is not a design choice; it is a consequence of the traversal class structure.

**Diagonal invariance.** For any Class A recurrence where $D_k = C_k$ for all $k$, the contributions at each step cancel: $-1/D_k + 1/C_k = 0$, and the series accumulates to zero net change. Non-trivial convergence requires $D \neq C$. The seeds $D_0 = 3$ and $C_0 = 5$ of the $\pi/4$ branch satisfy $D_0 \neq C_0$ by exactly 2, the minimum gap consistent with their parity class.

**Swap symmetry.** For Class A branches, swapping $D_0$ and $C_0$ produces a series that is antisymmetric around $N_0$: the two limits satisfy $N_\infty(D_0, C_0) + N_\infty(C_0, D_0) = 2 N_0$. Starting with seeds $(3, 5)$ gives limit $\pi/4$; starting with seeds $(5, 3)$ gives limit $2 - \pi/4$. The two runs mirror each other around the midline $N_0 = 1$ at every iteration.

**Perfect-square denominators.** In the $\pi/4$ branch, the product $D_n \cdot C_n = (4n-1)(4n+1) = 16n^2 - 1$ at each step. This yields the closed-form identity $\pi = \sum_{n=1}^{\infty} 8/(16n^2 - 1)$, expressing $\pi$ as a sum over perfect squares offset by unity. A post hoc framework would need to reproduce this algebraic corollary "accidentally."

---

### Where does the 61.8% coherence threshold come from mathematically?

The threshold $61.8\% = 1/\varphi$ arises directly from the $\varphi$ branch. **[proved for the derivation; threshold application is a design choice of the framework]**

The golden ratio $\varphi \approx 1.618$ satisfies the identity $\varphi = 1 + 1/\varphi$, which means $1/\varphi = \varphi - 1 \approx 0.618$. The $\varphi$ branch converges to $\varphi$ by tracking the ratio of consecutive Fibonacci terms. Below the ratio $D:C = \varphi : 1$ (equivalently, $C/D < 1/\varphi$), the proportional self-similarity that characterises healthy Fibonacci-like growth breaks down irreversibly.

In the tholonic scoring framework, the balance score expresses $C$ as a proportion of $D$. A score of $61.8\%$ means $C = (1/\varphi) \cdot D$, which is the exact point at which $D$ is $\varphi$ times larger than $C$. This is not an arbitrary round number; it is the value the $\varphi$ branch identifies as its own phase transition.

Whether $61.8\%$ is the right threshold for a given real-world application is an empirical question. The mathematical derivation provides the basis; field validation calibrates whether the tholonic coherence threshold maps correctly onto the specific system being analysed.

---

## What Is Proved and What Is Not

### What has been formally proved in the paper?

The following are formal theorems with complete proofs: **[all proved]**

1. The triadic irreducibility lemma: any recurrence with two functionally independent control forces requires at least three variables.
2. Convergence of all five branches to their claimed limits, via reduction to classical results (Leibniz alternating series, Fibonacci ratios, Newton's method, reciprocal factorial series, alternating harmonic series).
3. The seed partition theorem: $\pi/4$ uniquely requires seeds from $\{1, 3, 5\}$; the other four branches use seeds from $\{0, 1, 2\}$.
4. Diagonal invariance: Class A branches with $D_k = C_k$ accumulate no net change.
5. Swap symmetry: swapping $D_0$ and $C_0$ in Class A produces limits that sum to $2 N_0$.
6. Perfect-square denominators: $D_n \cdot C_n = 16n^2 - 1$ in the $\pi/4$ branch, yielding the $\pi$ identity.
7. Offset consistency: for pure-accumulation branches ($e$ and $\ln 2$), the limit is translation-equivariant in the seed: $N_\infty(N_0) = N_0 + N_\infty(0)$.
8. Parametric generalisation: the $\sqrt{2}$ branch generalises to $\sqrt{a}$ for any $a > 0$; the $\varphi$ branch generalises to the metallic means $\sigma_m$ for any positive integer $m$.
9. Explicit error bounds for the two $O(1/k)$ branches, derived from the alternating series theorem.
10. The step size $\Delta = 4$ of the $\pi/4$ branch is uniquely forced by the Instantiation axis multiplier of the tholonic geometry (squaring and doubling yield the same integer 4).

---

### What remains open or conjectural?

Four conjectures are explicitly stated in the paper and are not yet proved. **[all conjectural]**

**Conjecture 1 (Uniqueness of the $\pi/4$ seed).** The triple $(1, 3, 5)$ is the unique Class A admissible seed satisfying the parity and adjacency constraints that yields $N_\infty = \pi/4$ under step $\Delta = 4$. Status: numerically confirmed but not proved.

**Conjecture 2 (Exclusion of $\pi/4$ from the primitive lattice).** No triple drawn from $\{0, 1, 2\}$ with any Class B or Class C traversal rule produces $\pi/4$ as a limit. Status: $\pi/4$ is genuinely inaccessible from the primitive seed set. Numerically plausible but not proved.

**Conjecture 3 (Finite classification).** There exists a finite rule set such that the only convergent branches with limits in the set $\{\pi/4, \varphi, e, \sqrt{2}, \ln 2\}$ are exactly the five documented. This is the move from organisational taxonomy to a finiteness theorem. Status: the key open problem. If false, a reformulation as a local isolation claim (no continuous deformation moves one branch into another while preserving its limit) is the natural fallback.

**Conjecture 4 (Non-circularity of the $\pi/4$ grouping).** The Class A update form $N_{k+1} = N_k - 1/D_k + 1/C_k$ with step $\Delta = 4$ can be derived purely from structural constraints (rational update of degree $\leq 1$ in $D^{-1}$ and $C^{-1}$, opposite signs, Class A advancement via the geometric step) without assuming the value of $\pi$ as input. This is the key independence question. Until it is resolved, one cannot rule out that the $\pi/4$ grouping was selected post hoc to match the Leibniz series.

The paper's conclusion is honest: the framework as proved is organisational, not predictive. It provides a unified format with structural theorems attached, which distinguishes it from an arbitrary collection of known limits, but it does not yet prove that these five constants and no others are forced by the axioms.

---

## Connections to Classical Mathematics

### Are the underlying series new?

No. Every series and iterative method used in the five branches is classical and centuries old.

The Leibniz series for $\pi/4$ ($1 - 1/3 + 1/5 - \cdots$) dates to the late seventeenth century. The golden ratio's connection to Fibonacci ratios is ancient, formalised via Binet's formula. The Newton-Babylonian method for $\sqrt{2}$ was known to Babylonian mathematicians approximately 3700 years ago and was formalised by Heron of Alexandria. The reciprocal factorial series for $e$ was established in the eighteenth century. The alternating harmonic series for $\ln 2$ is a standard result in analysis.

The claim of the paper is not that these series are new. It is that all five descend from a single three-variable recurrence grammar with consistent role assignments, and that the structural theorems (seed partition, diagonal invariance, swap symmetry, perfect-square denominators, offset consistency) distinguish this unified framework from an arbitrary post hoc assembly of known limits.

---

### How does this relate to the Fibonacci sequence and continued fractions?

The $\varphi$ branch is directly a Fibonacci recurrence. The traversal rule $D \leftarrow C$, $C \leftarrow C + D$ maintains consecutive Fibonacci terms in the $(D, C)$ positions at every step. The ratio of consecutive Fibonacci terms converges to $1/\varphi$ with error contracting by factor $\varphi^{-2} \approx 0.382$ per step.

The golden ratio also has the continued fraction representation $\varphi = [1; 1, 1, 1, \ldots]$, the simplest nontrivial continued fraction and the "most irrational" number in the sense of being worst approximable by rationals. The $\varphi$ branch arrives at the same constant via a different route (Fibonacci ratio convergence rather than truncated continued fractions) but the limit is identical.

The $\sqrt{2}$ branch connects to the continued fraction $\sqrt{2} = [1; 2, 2, 2, \ldots]$ indirectly: the Newton-Babylonian iteration converges quadratically while the continued fraction truncations converge linearly, so the two approaches reach the same limit at very different rates. The tholonic framing adds no new connection here; it simply reexpresses the Babylonian method with explicit $D$ and $C$ roles.

---

### How does this relate to Newton's method more generally?

The $\sqrt{2}$ branch is Newton's method for the equation $x^2 - 2 = 0$. Generalising $D$ from 2 to any positive real $a$ gives Newton's method for $\sqrt{a}$, with the same quadratic convergence. **[proved]**

Newton's method for a general differentiable function $g(x) = 0$ takes the form $x_{k+1} = x_k - g(x_k)/g'(x_k)$. For $g(x) = x^2 - a$ this simplifies to $x_{k+1} = (x_k + a/x_k)/2$, which is exactly the tholonic $\sqrt{2}$ update with $D = a$ and $C = 2$. The tholonic role assignment maps cleanly: $D$ is the function's target ($a$, the specification being met), $C$ is the averaging constant that synthesises each correction, and $N$ is the current estimate.

This connection is not coincidental. Newton's method in general is a process of iteratively refining a state ($N$) by applying a correction derived from a constraint ($D$, the target function value) and a synthesis factor ($C$, the derivative). The three-variable structure of Newton's method is a specific instance of the triadic form.

---

### What did Leibniz connect to binary and the I Ching?

Leibniz discovered the $\pi/4$ series and simultaneously developed binary arithmetic. He drew an explicit connection between binary structure (everything built from 0 and 1) and the I Ching's system of hexagrams (built from broken and unbroken lines). He saw binary as a model of creation from minimal premises.

The tholonic framework formalises a version of this intuition: binary counting generates the minimum non-trivial simplex (the tetrahedron, which requires four vertices: a binary pair $\{0, 1\}$ expanded to three dimensions), the simplex induces the N-D-C triad, and the triad produces the five classical limits.

This interpretive layer is separable from the mathematical proofs and is not required for the convergence results. The paper notes the connection but does not claim it as a proof ingredient.

---

### Can the recurrence produce constants beyond the five documented?

Yes. **[proved for specific cases; general landscape is open]**

Proposition 6.6 in the paper establishes two explicit parametric families:

- Replacing $D = 2$ in the $\sqrt{2}$ branch with $D = a$ gives $N_\infty = \sqrt{a}$ for any $a > 0$.
- Replacing the update base in the $\varphi$ branch with a generalised Fibonacci rule (with base $m \in \mathbb{N}$) gives the metallic means $\sigma_m = (m + \sqrt{m^2 + 4})/2$. For $m = 1$ this is $\varphi$; for $m = 2$ it is the silver ratio; and so on.

The five documented branches are distinguished points within an infinite space of admissible seed-traversal combinations. What makes them notable is that their limits are among the most widely recurring constants in mathematics. Whether the set of such distinguished points is finite and fully characterised by a small axiom set is the content of Conjecture 3, which remains open.

---

### What is the convergence rate of each branch and why does it matter?

| Branch | Rate | Mechanism |
|---|---|---|
| $e$ | $O(1/k!)$ (super-exponential) | Factorial denominators; each term is smaller by a factor of $1/(k+1)$ |
| $\sqrt{2}$ | Quadratic | Newton's method; each iteration squares the error |
| $\varphi$ | Linear, ratio $\varphi^{-2} \approx 0.382$ | Geometric Fibonacci convergence (Binet's formula) |
| $\pi/4$ | $O(1/k)$ | Alternating series; error bounded by first omitted term $1/(4k+3)$ |
| $\ln 2$ | $O(1/k)$ | Alternating harmonic series; error bounded by $1/(k+1)$ |

The rates are intrinsic to the classical mechanisms, not to the tholonic framing. The two slow branches ($\pi/4$ and $\ln 2$) are conditionally convergent alternating series; series acceleration methods (Euler transform, Levin's method) would improve their speed but are not part of the framework.

The rates matter for the structural interpretation. The $e$ branch converges fastest because factorial growth is the most explosive denominator sequence possible (faster than any polynomial or exponential). This corresponds to the tholonic claim that financial instruments can mobilise resources at factorial speed. The $\sqrt{2}$ branch converges quadratically because Newton's method doubles the correct digits with each iteration: rapid self-correction once the estimate is close. The $O(1/k)$ branches require many iterations to converge closely, corresponding to the tholonic claim that $\pi$ and $\ln 2$ describe processes that require persistent external input ($\pi$) or long transformation cycles ($\ln 2$) to approach equilibrium.

---

*Primary source: [Emergence of Classical Constants from a Minimal Recursive Triadic Framework](docnav/Research/papers/1_recursive-tholonic-five-constants.md) (J. W. Milton, Clarity Coalition, June 2026). For the non-mathematical version of the five dimensions, see [Five Dimensions: Plain Labels](docnav/FAQ/five-dimensions-plain-labels.md).*
