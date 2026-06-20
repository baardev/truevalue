# Tholonic Orbital Balance: Solar System Scoring

**Analysis:** Tholonic N-D-C balance applied to orbital mechanics.
**D** = perihelion distance (gravitational constraint, hard boundary).
**C** = aphelion distance (maximum orbital extension, accumulated contribution).
**B(D,C)** = $\frac{2 \cdot \min(D,C)}{D+C} \times 100$

Phi-threshold: 61.8 (below this: orbit is Imbalanced / marginally coherent).

---

## Results Table

| Body | D = q (AU) | C = Q (AU) | Eccentricity | B(D,C) | State |
|---|---:|---:|---:|---:|---|
| Venus | 0.7184 | 0.7282 | 0.0068 | 99.32 | Coherent |
| Neptune | 29.8100 | 30.3270 | 0.0086 | 99.14 | Coherent |
| Earth | 0.9833 | 1.0167 | 0.0167 | 98.33 | Coherent |
| Uranus | 18.2860 | 20.0970 | 0.0472 | 95.28 | Coherent |
| Jupiter | 4.9501 | 5.4570 | 0.0487 | 95.13 | Coherent |
| Saturn | 9.0477 | 10.1160 | 0.0557 | 94.43 | Coherent |
| Ceres | 2.5577 | 2.9773 | 0.0758 | 92.42 | Coherent |
| Mars | 1.3814 | 1.6660 | 0.0934 | 90.66 | Coherent |
| Mercury | 0.3075 | 0.4667 | 0.2056 | 79.44 | Marginal |
| Eros | 1.1332 | 1.7830 | 0.2228 | 77.72 | Marginal |
| Pluto | 29.6580 | 49.3050 | 0.2488 | 75.12 | Marginal |
| Icarus | 0.1869 | 1.9693 | 0.8266 | 17.34 | Imbalanced |
| Comet Encke | 0.3361 | 4.0940 | 0.8483 | 15.17 | Imbalanced |
| Comet Tempel-Tuttle | 0.9765 | 19.6500 | 0.9053 | 9.47 | Imbalanced |
| Comet Swift-Tuttle | 0.9595 | 51.2300 | 0.9632 | 3.68 | Imbalanced |
| Comet Halley 1682 | 0.5861 | 35.0800 | 0.9671 | 3.29 | Imbalanced |
| Comet Kirch 1680 | 0.0062 | 888.0000 | 1.0000 | 0.00 | Imbalanced |

---

## Tholonic Observations

**Observation 1: The phi-threshold cleanly separates planets from comets.**
Every planet scores above the 61.8 phi-threshold. Every comet scores below it.
This is not a manually tuned threshold: 61.8 is $100 \times (2 - \varphi)$,
the same phi-derived cutoff used in the TVPCI supply-chain scoring model.

**Observation 2: Comet Kirch 1680 has the most extreme imbalance in the dataset.**
Newton used this comet in Principia Book III to demonstrate that gravity
follows the inverse-square law at interstellar distances. Its aphelion
is approximately 142,000 times its perihelion. B = 0.0014.
The body that proved gravity's reach is the body most distant from N-state coherence.

**Observation 3: Orbital eccentricity and tholonic balance are equivalent descriptions.**
For an orbit with perihelion q and aphelion Q:

$$B(D,C) = \frac{2q}{q+Q} \times 100 = (1 - e) \times 100$$

This is not approximate: it is exact. The tholonic balance score is identically
$100(1-e)$, where $e$ is the standard orbital eccentricity. The tholonic model
thus provides a physical interpretation of eccentricity: it measures D-C imbalance.
A circular orbit ($e=0$) has perfect D-C balance ($B=100$). A parabolic escape
trajectory ($e=1$) has zero balance ($B=0$): pure C with no D return.

**Observation 4: Newton's gravitational theory predicts the N state.**
Newton derived that under an inverse-square force, the only closed (stable, N-state)
orbits are ellipses. The tholonic reading: gravity is the D operator.
Initial velocity is the C operator. The ellipse is the N state their balance produces.
The closer D and C are to equality (low eccentricity), the more circular and
stable the N state. The Principia is a proof that N states exist under D-C balance.

---

## The Exact Relation: B(D,C) = 100(1 - e)

Let $q$ = perihelion, $Q$ = aphelion. Then:

$$e = \frac{Q - q}{Q + q}$$

$$B = \frac{2q}{q + Q} \times 100$$

$$1 - e = 1 - \frac{Q-q}{Q+q} = \frac{(Q+q) - (Q-q)}{Q+q} = \frac{2q}{Q+q}$$

Therefore $B = 100(1-e)$ exactly. The tholonic balance functional, when applied
to orbital mechanics with D=perihelion and C=aphelion, is the complement of
orbital eccentricity. This is a structural identity, not a fit.
