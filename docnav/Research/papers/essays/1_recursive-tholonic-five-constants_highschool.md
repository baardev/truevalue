# Five Famous Numbers and the Simple Recipe That Makes Them All

### A plain-language guide to one of math's most surprising coincidences

---

## The Setup: Five Numbers You Should Know

There are five numbers that show up over and over again in math, science, and nature. You've probably met at least a few of them.

**π (pi) ≈ 3.14159...**
The ratio of a circle's circumference to its diameter. Memorized by millions of students. It shows up in geometry, physics, statistics, and dozens of other places.

**φ (phi, the golden ratio) ≈ 1.618...**
The ratio that appears in sunflower spirals, seashell growth, and Renaissance paintings. If you cut a line segment so that the ratio of the whole to the long part equals the ratio of the long part to the short part, you get φ.

***e* ≈ 2.718...**
Euler's number. If you invest $1 at 100% interest, compounded continuously for one year, you end up with $*e*. It controls all natural growth and decay: bacteria populations, cooling temperatures, radioactive decay.

**√2 ≈ 1.414...**
The square root of 2. The length of the diagonal of a square with sides of length 1. The ancient Greeks proved this number can *never* be written as a fraction, which shocked the math world.

**ln 2 ≈ 0.693...**
The natural logarithm of 2. This one tells you the half-life of radioactive materials in terms of their decay rate. It also tells you how many coin flips' worth of information is in a single yes/no question.

---

These five numbers were discovered at different times, by different people, for completely different reasons. For centuries, mathematicians studied each one on its own.

But it turns out they are all related in a surprising way. They can all be produced by the *same simple machine*, just with different settings.

---

## The Machine: Three Buckets and a Rule

Imagine you have three buckets labeled **N**, **D**, and **C**. You put a starting number in each one. Then you follow a rule to update the buckets, over and over. After enough steps, the number in bucket **N** settles down and stops changing. That final settled value is the famous constant.

The three buckets are not just random containers. Each one has a *job*:

> **N: the negotiator.** This is your running answer. It changes a little bit with each step, getting closer and closer to the final value.

> **D: the definer.** This is the limiter. It puts a brake on things, preventing N from shooting off to infinity.

> **C: the contributor.** This is the accumulator. It pushes N forward, adding to the total.

The magic is in the tension between D and C. D says "slow down." C says "keep going." N finds the balance between them.

Here is the key point: **you need all three**. Two buckets are not enough. If you remove D, N grows without bound. If you remove C, N never moves. The three-bucket structure is the *minimum* needed for the machine to work. (This is actually proved mathematically in the full paper.)

---

## Running the Machine: Five Examples

### Example 1: Getting φ (the golden ratio)

Start with: **N = 1, D = 1, C = 2**

Rule: each step, set N = 1 + D/C. Then update D and C using the Fibonacci rule: D becomes what C was, and C becomes the sum of the old D and C.

Let's trace the first few steps:

| Step | N | D | C | D/C |
|------|---|---|---|-----|
| Start | 1 | 1 | 2 | 0.500 |
| 1 | 1.500 | 2 | 3 | 0.667 |
| 2 | 1.667 | 3 | 5 | 0.600 |
| 3 | 1.600 | 5 | 8 | 0.625 |
| 4 | 1.625 | 8 | 13 | 0.615 |
| 5 | 1.615 | 13 | 21 | 0.619 |
| ... | ... | ... | ... | ... |
| 20 | **1.61803...** | — | — | — |

After about 20 steps, N has settled to the golden ratio. Notice what D and C are doing: they are the Fibonacci numbers (1, 1, 2, 3, 5, 8, 13, 21, ...). The ratio of consecutive Fibonacci numbers always approaches φ. The machine is just doing that automatically.

D's job: it is always the *smaller* (older) Fibonacci number, the constraint, the boundary of where we've been.
C's job: it is always the *larger* (newer) Fibonacci sum, the accumulation of the last two generations.

### Example 2: Getting √2

Start with: **N = 1, D = 2, C = 2**

Rule: each step, set N = (N + D/N) / C.

This is actually an ancient method. The Babylonians used it to find square roots by hand over 3,000 years ago. Here is the idea: if your guess N is too big, then 2/N will be too small. Average them and you get a better guess.

| Step | N (guess for √2) | Error |
|------|-----------------|-------|
| Start | 1.0000 | 0.4142 |
| 1 | 1.5000 | 0.0858 |
| 2 | 1.4167 | 0.0025 |
| 3 | 1.4142 | 0.0000021 |
| 4 | **1.41421356...** | essentially zero |

Four steps! It converges so fast because each step *squares* the precision, roughly doubling the number of correct decimal places every iteration.

Notice: D = 2 and C = 2 are the same number. But they play different roles. D is the *target*, the value whose square root we want. C is the *averaging divisor*, which synthesizes the two sides of the estimate. If you tried to use a single variable for both, the formula wouldn't make structural sense anymore.

### Example 3: Getting *e*

Start with: **N = 0, D = 1, C = 1**

Rule: each step, add D/C to N. Then multiply C by the step count (so C grows as 1, 1, 2, 6, 24, 120, ..., the factorials).

This adds up the series: 1 + 1/1 + 1/2 + 1/6 + 1/24 + 1/120 + ...

Each term is the reciprocal of a factorial. The terms get tiny very fast, so the sum converges quickly:

| Step | Added term | Running total N |
|------|-----------|----------------|
| 0 | 1/1 = 1.000 | 1.000 |
| 1 | 1/1 = 1.000 | 2.000 |
| 2 | 1/2 = 0.500 | 2.500 |
| 3 | 1/6 = 0.167 | 2.667 |
| 4 | 1/24 = 0.042 | 2.708 |
| 5 | 1/120 = 0.008 | 2.717 |
| ... | ... | ... |
| 15 | tiny | **2.71828...** |

D's job: it stays at 1 the whole time, the fixed, unchanging numerator that never varies. It is the definition, the boundary that determines the size of each step.
C's job: it grows as a factorial, an ever-expanding denominator that makes each step smaller and smaller, integrating more and more precision into the total.

---

## The Big Surprise: One Grammar, Five Answers

Here is the table that shows all five constants together:

| Constant | Start N | Start D | Start C | What the rule does |
|---|---|---|---|---|
| **π/4** | 1 | 3 | 5 | Alternating adds and subtracts fractions |
| **φ** | 1 | 1 | 2 | Fibonacci ratio update |
| ***e*** | 0 | 1 | 1 | Factorial reciprocal sum |
| **√2** | 1 | 2 | 2 | Babylonian averaging |
| **ln 2** | 0 | 1 | 1 | Alternating harmonic sum |

In every single case:
- **N** is the running answer, being refined step by step
- **D** is the limiting force, preventing runaway growth
- **C** is the contributing force, driving the accumulation

The *operations* differ. But the *roles* are the same. Every time.

---

## The Odd One Out: Why π Is Different

Look at the starting values. Four of the five constants start with numbers chosen from only {0, 1, 2}, the most basic numbers imaginable. Zero means "nothing." One means "a single unit." Two means "the first doubling."

But π/4 starts with {1, 3, 5}. And unlike the others, it needs to receive new information from *outside* at every step. Its D and C values are updated by adding 4 each time, not by folding back on themselves.

Why? It comes from geometry. The framework is built on a triangular structure where each side of the triangle has a different "weight." One of those weights is 2. If you square it, you get 4, which is exactly the step size the π machine needs. The starting values 3 and 5 also come from the geometry of the triangle.

In other words: **π/4's weird starting values are not arbitrary**. They are forced by the shape of the triangle underneath the whole framework. The four other constants can be built from scratch with almost nothing. Only the circle, only π, demands a richer starting point.

---

## How Fast Do They Converge?

Not all five machines are equally efficient:

| Constant | Steps needed for 10 decimal places |
|---|---|
| *e* | ~15 |
| √2 | ~6 (doubles precision each step) |
| φ | ~20 |
| ln 2 | ~10,000,000 |
| π/4 | ~10,000,000 |

*e*, √2, and φ are fast. They converge because their machines are self-correcting in an aggressive way, where each new step makes use of all the accuracy built up so far.

π/4 and ln 2 are slow. They work by alternating addition and subtraction: first you overshoot, then you undershoot, then you overshoot again, each time by a slightly smaller amount. It works, but you need millions of steps to get high precision.

The framework predicts this difference. The fast constants use machines that fold back on their own state. The slow constants use machines that get fed new information one piece at a time from outside. That structural difference (self-contained versus externally driven) is the reason for the speed difference.

---

## What Does This All Mean?

Here are three ways to think about it:

**The modest view:** This is a neat way to organize five known things. It does not produce new facts about any of the five constants. But it shows they share a common skeleton, which is satisfying and may eventually be useful.

**The interesting view:** The fact that a *three*-role structure is the minimum needed to produce these constants, and that you need exactly a negotiator, a limiter, and a contributor, might say something deep about what kinds of processes can home in on precise values at all. It is a structure that appears in many other places: a predator-prey ecosystem has population (N), food limit (D), and reproduction (C). A good argument has a claim (N), a constraint (D), and supporting evidence (C). Whether this is a meaningful analogy or just a coincidence is an open question.

**The ambitious view:** If it can be proved that *only* these five constants (and no others) arise from the simplest possible versions of this three-role machine, that would be a genuine mathematical discovery. It would mean there is something *special* about π, φ, *e*, √2, and ln 2 that distinguishes them not just historically but *structurally* from all other numbers. The paper states four open problems that, if solved, would make this the case. The proofs are not yet in hand.

---

## Try It Yourself

You can run all five machines in Python. If you have Python installed, copy this into a file and run it:

```python
def golden_ratio(steps=20):
    N, D, C = 1.0, 1.0, 2.0
    for _ in range(steps):
        N = 1.0 + D / C
        D, C = C, C + D
    return N

def sqrt2(steps=10):
    N, D, C = 1.0, 2.0, 2.0
    for _ in range(steps):
        N = (N + D / N) / C
    return N

def euler_e(steps=15):
    N, D, C = 0.0, 1.0, 1.0
    for k in range(steps):
        N = N + D / C
        C = C * (k + 1) if k > 0 else C
    return N

def ln2(steps=100000):
    N, D, C = 0.0, 1.0, 1.0
    for k in range(steps):
        term = D / (k + C)
        N = N + term if k % 2 == 0 else N - term
    return N

print(f"Golden ratio φ  = {golden_ratio():.10f}  (should be 1.6180339887)")
print(f"Square root √2  = {sqrt2():.10f}  (should be 1.4142135624)")
print(f"Euler's number e = {euler_e():.10f}  (should be 2.7182818285)")
print(f"ln 2            = {ln2():.10f}  (should be 0.6931471806)")
```

Run it and see. The same N-D-C skeleton, four different rules, four famous numbers.

---

## Summary

| Big idea | In plain language |
|---|---|
| Five famous constants share a common structure | π, φ, *e*, √2, and ln 2 can all be produced by the same kind of recipe |
| The recipe needs exactly three ingredients | A running total (N), a limiter (D), and an accumulator (C). No fewer will do. |
| The roles are consistent across all five | Even though the operations differ, D always limits and C always accumulates |
| π is the odd one out | It alone requires more complex starting values and outside input at every step |
| Speed reveals structure | How fast each machine converges is predicted by whether it is self-contained or externally driven |
| The big question is still open | Can it be *proved* that only these five constants arise from the simplest versions of this recipe? |

---

*Based on "Emergence of Classical Constants from a Minimal Recursive Triadic Framework" by J. W. Milton, Clarity Coalition, June 2026.*
