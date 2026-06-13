# A Grammar Beneath the Numbers

## On the discovery that five of mathematics' most celebrated constants share a common structural origin, and what that means for how we understand mathematical pattern

*An essay for educated readers outside the mathematical sciences*

---

## Prologue: A Question Worth Asking

Five numbers appear, again and again, at the foundations of mathematics and science. Each was discovered independently, by different people, in different centuries, for different reasons. Each has been studied intensively on its own for hundreds of years.

A new result asks a question that has rarely been posed directly: what if all five are not merely coincidentally famous, but structurally related: outputs of the same underlying process, varying only in the specific rules applied? What if there is a single generative grammar from which all five descend?

This essay explains what that claim means, what has been proved, what remains open, and why it matters.

---

## The Five Numbers and Their Histories

**π (pi) ≈ 3.14159...**
The ratio of a circle's circumference to its diameter. Known to Babylonian astronomers and Greek geometers, it was computed ever more precisely over centuries. What is strange about π is not its geometric meaning but its reach: it appears in equations governing waves, heat, probability, and quantum mechanics, in contexts that have nothing obvious to do with circles. Mathematicians sometimes speak of π as "unreasonably effective," turning up where it has no apparent business.

**φ (the golden ratio) ≈ 1.618...**
Studied by Euclid as the "extreme and mean ratio," it is the proportion in which a line segment must be divided so that the ratio of the whole to the larger part equals the ratio of the larger part to the smaller. It is the limiting ratio of consecutive Fibonacci numbers (1, 1, 2, 3, 5, 8, 13, 21...), the sequence where each number is the sum of the two before it.

***e* ≈ 2.718...**
Named for the mathematician Leonhard Euler, this number governs all processes of continuous growth or decay: compound interest, radioactive decay, population dynamics, heat loss. It is the base of the natural logarithm and the unique function in calculus that is its own rate of change.

**√2 ≈ 1.414...**
The length of the diagonal of a unit square. The first number ever proved to be *irrational*: it cannot be expressed as a ratio of two whole numbers, no matter how large. This proof reportedly caused a crisis in ancient Greek mathematical thought, which had held that all measurements must be expressible as ratios.

**ln 2 ≈ 0.693...**
The natural logarithm of 2. Less famous to non-specialists but ubiquitous in science: it determines the half-life of any exponentially decaying quantity, measures the information content of a single binary choice, and appears as a fundamental measure of computational efficiency.

---

## What They Have in Common: Nothing Obvious

These five numbers were not discovered together. There is no surface-level reason why the number governing circles should be related to the number governing compound interest, or why either should be related to the length of a diagonal. They come from entirely different mathematical problems, solved by different methods, centuries apart.

Yet mathematicians have long suspected that these constants are not merely coincidentally famous, that something deeper connects them. The question is not whether each constant has interesting properties (each has many) but whether *all five together* can be derived from a common source. Whether there is a grammar beneath the numbers.

---

## The Framework: A Template With Three Roles

The new proposal, developed by researcher J. W. Milton and published as a formal mathematical paper, offers exactly such a grammar. It is a *template* that can produce each of the five constants from the same starting structure, by varying only the initial values and the specific updating rule.

The template works as follows. You begin with three quantities, each playing a distinct role.

The first is a **running state**: your current best approximation of the answer, refined with each iteration.

The second is a **limiting force**: a constraint that prevents the running state from growing without bound, pulling it back when it overshoots.

The third is a **contributing force**: an accumulating pressure that keeps moving the running state toward its target, adding to the total with each step.

These roles are labeled N (the running *negotiation*, or balance), D (the *defining* constraint), and C (the *contributing* accumulator). What matters is not the specific numbers assigned to these roles but the *functional relationship* between them. D constrains. C accumulates. N finds the balance.

The template is run repeatedly, dozens, hundreds, or thousands of times depending on the desired precision. Each pass refines the running value. The constraint prevents it from diverging. The accumulator prevents it from stalling. Over many iterations, the running value settles toward a precise limit. Depending on which specific rules and starting values are used, that limit is one of the five famous constants.

---

## Why Three Roles, and Not Two

One of the more striking aspects of the framework is its claim that three roles are not merely convenient: they are the *minimum necessary*. This is a proved mathematical result, not an aesthetic choice.

Consider what happens with only two roles: a running state and a single auxiliary force. That force either pushes the running state toward a target, or it pulls it back. With only pushing, the running value grows without bound, with nothing to correct an overshoot. With only pulling, the running value stalls, with nothing to keep it moving. The *tension* that produces convergence, the productive friction between constraining and accumulating forces balanced by a running negotiation between them, requires all three roles simultaneously.

Two roles produce either runaway growth or frozen stillness. Three roles produce dynamic stability: the capacity to approach a precise value by successive correction. This is not a metaphor; it is a theorem.

---

## Running the Template: Three Examples

**The golden ratio.** Start with N = 1, D = 1, C = 2. Each step: update N to equal one plus the ratio of D to C; then update D and C by the Fibonacci rule (D takes C's old value; C becomes the sum of the old D and C). After about twenty repetitions, N has settled to 1.61803..., the golden ratio, accurate to all available decimal places. D is always the smaller, older Fibonacci number: the constraint, the definition of where the process has been. C is always the larger, newer sum: the accumulation of the two most recent steps.

**The square root of two.** Start with N = 1, D = 2, C = 2. Each step: update N to the average of N and D divided by N, then divide the result by C. This is the Babylonian method for approximating square roots, over three thousand years old: if your estimate is too high, dividing by the estimate gives something too low; averaging the two corrects the error. After only six repetitions, the result is accurate to more decimal places than will ever be needed in practice. Each step roughly *doubles* the number of correct digits. D is the target, the number whose square root we seek. C is the averaging factor, the synthesizer that corrects the overshoot and undershoot. Though D and C happen to be numerically equal here, their *roles* are different: one defines the target, one synthesizes the correction.

**Euler's number *e*.** Start with N = 0, D = 1, C = 1. Each step: add D divided by C to N; then multiply C by the step count (so C grows through the sequence 1, 1, 2, 6, 24, 120..., the factorials). The result accumulates the series 1 + 1 + 1/2 + 1/6 + 1/24 + ... which converges to *e*. D is the fixed numerator, the unchanging boundary, the unit that is divided at each step. C is the ever-growing denominator, absorbing more structure with each iteration, so that each successive term contributes less and less, integrating toward the limit.

---

## The Five Constants, Summarized

| Constant | Starting values | Rule type | How quickly it converges |
|---|---|---|---|
| **π/4** | 1, 3, 5 | Alternating additions, step of 4 | Slowly: millions of steps for high precision |
| **φ** | 1, 1, 2 | Fibonacci ratio | Very fast: machine precision in ~20 steps |
| ***e*** | 0, 1, 1 | Factorial reciprocal sum | Very fast: machine precision in ~15 steps |
| **√2** | 1, 2, 2 | Babylonian averaging | Extremely fast: precision doubles each step |
| **ln 2** | 0, 1, 1 | Alternating harmonic sum | Slowly: millions of steps for high precision |

In every case, D constrains and C accumulates, regardless of the specific mathematical operation involved. This functional consistency is not imposed by the framework. It emerges from the mathematics.

The framework also predicts *why* some constants converge quickly and others slowly. The fast ones use self-contained rules: each step builds on the full precision already accumulated. The slow ones use alternating addition and subtraction, overshooting, then undershooting, then overshooting again, each time by a slightly smaller amount. The structure of the rule determines the speed of convergence.

---

## The Odd One Out: π

Among the five, the constant governing circles behaves differently, and not in a subtle way.

The other four constants can be produced using only the numbers 0, 1, and 2 as starting values. These are, in a rigorous sense, the most primitive possible inputs: zero, unity, and the first doubling. All four of the other recipes are *self-contained*: they feed entirely on their own previous state, requiring nothing from outside.

π/4 requires starting values of 1, 3, and 5. And unlike the others, its rule must be *fed* new values from outside at every step. It cannot simply fold back on itself.

The paper argues this is not coincidental. The starting values of the π/4 recipe are derived from the geometric structure that underlies the entire framework: a triangular configuration in which each of three axes carries a specific weight. The numbers 3 and 5 come from two of those axes. The step size that drives the recipe is obtained by squaring one of the triangle's structural weights, yielding 4, exactly the increment used. Nothing is chosen arbitrarily; the geometry dictates the recipe.

In other words: the other four constants can be coaxed from almost nothing. Only the circle demands a richer starting structure, and the framework offers a precise geometric reason why.

---

## What Is Proved and What Remains Open

The paper is careful to distinguish between what has been established and what is still conjectural, and this distinction is worth preserving here.

**Established by proof:** All five constants are generated by the same three-role template. Several structural properties (symmetry laws, a clean partition of starting values, an algebraic identity linking π to perfect squares) hold as proved theorems, not observed regularities. The three-role minimum is proved. The π recipe is provably the only one requiring starting values outside {0, 1, 2}.

**Stated as open conjectures:** That these five constants are the *only* outputs of the simplest admissible versions of the template. That the π recipe's special starting values are *forced* by the underlying geometry rather than chosen to match a known result. That no other selection of simple starting values and rules can produce any of the five constants in a different way. Four numbered conjectures in the paper identify these gaps precisely.

The distinction is significant. What has been proved is what the paper calls an *organizational* result: a unified framework with genuine structural theorems. What has not yet been proved is the stronger *predictive* claim: that the framework does not merely *accommodate* the five constants but *necessitates* them. The path from the first to the second runs through the four open conjectures.

---

## A Note on Whether This Was Designed or Discovered

A natural concern with any unification framework is what the paper calls "post hoc flexibility": the suspicion that the author chose starting values and rules *after knowing the desired outputs*, making the apparent unification circular rather than genuine.

The paper addresses this directly. The symmetry theorems hold without reference to any specific target constant. The clean partition (four constants from {0, 1, 2}, one constant from {1, 3, 5}) is a sharp combinatorial fact that would not arise automatically from a backward-designed framework. The derivation of the π recipe's step size from the geometry of the underlying structure is either structurally forced or a coincidence; establishing which is identified as the key remaining question.

Whether these arguments fully defuse the concern is something each reader must judge. What is clear is that the paper asks the right question: not merely "does this framework fit the five constants?" but "would the framework survive the replacement of any one constant with a different number?" Posing the question this way is the appropriate standard, and the paper meets it by stating the answer honestly: not yet fully proved, but here is the precise work that would establish it.

---

## Conclusion

The tholonic framework does not resolve any old questions definitively. It opens the same questions more precisely.

What it establishes is that five of the most fundamental constants in mathematics, each discovered independently and each studied in isolation for centuries, share a common three-role generative structure. This is proved. What it proposes, but has not yet proved, is that these five are the *only* outputs of the simplest admissible versions of that structure. This is the work that remains.

For readers whose expertise lies outside mathematics, the significance of such a result (if the remaining proofs come in) would be substantial: not merely a tidier way to organize known facts, but evidence that these five numbers occupy a special position in the architecture of mathematical possibility. That they are not just interesting, but *necessary*.

The proof is not yet complete. But the question has never been posed this precisely before. That is itself a form of progress.

---

*This essay is a non-technical introduction to "Emergence of Classical Constants from a Minimal Recursive Triadic Framework" by J. W. Milton, Clarity Coalition, June 2026. All specific mathematical claims correspond to proved theorems or explicitly labeled conjectures in the source paper.*
