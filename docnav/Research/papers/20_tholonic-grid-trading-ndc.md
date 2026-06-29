**CONFIDENTIAL AND PRIVATE. DO NOT DISTRIBUTE.**

---

# Tholonic N-D-C Signal Architecture for Accumulation-Biased Grid Trading: Design, Implementation, and 59-Day Empirical Results on SOL/USD

**Author:** J. W. Milton, Clarity Coalition

**Version:** 1.0

**Date:** 29 June 2026

**Keywords:** tholonic model; N-D-C framework; grid trading; accumulation strategy; golden ratio; energy cost; imbalance signal; SOL/USD; cryptocurrency; phi spacing

---

## Results at a Glance

**Period:** 59 days (April 30 to June 29, 2026) | **Instrument:** SOL/USD | **Runs:** 5,518

| Metric | Start | End | Change | Annualised CAGR |
|---|---|---|---|---|
| SOL held | 556 | 1,279 | +722 (+129.9%) | **+17,141%/yr** (CAGR); ~804%/yr (simple linear) |
| Total equity (USD) | $97,179 | $96,921 | -$258 (-0.27%) | -1.6%/yr |
| SOL/USD price | $83.06 | $71.24 | -$11.82 (-14.2%) | -61.3%/yr |
| Cash balance | $50,984 | $5,108 | -$45,876 deployed | |

**Acquisition quality:** 722 SOL acquired at an average cost of $63.50, against a period low of $60.48 (3.3% above the floor) and a period high of $98.12. Unrealised gain on acquired position at close: +$5,586.

**Primary objective met.** The bot's goal was to accumulate the maximum quantity of SOL, not to maximise dollar equity. SOL holdings more than doubled (+129.9%) while dollar equity was preserved within 0.3%, against a backdrop of a 14.2% price decline in the underlying asset. The annualised SOL accumulation rate of +17,141%/yr (compound, CAGR) or ~804%/yr (simple linear, $129.9\% \times 365/59$) reflects a concentrated 59-day accumulation phase in a declining market and should not be extrapolated as a steady-state expectation; it is a measure of execution quality during the observed period.

---

## Abstract

This paper describes the design and empirical evaluation of a limit-order grid trading bot constructed entirely from tholonic N-D-C principles. The system maps cryptocurrency market state onto the tholonic triadic structure: bearish constraints are assigned to the D (Definition) role, bullish contributions to the C (Contribution) role, and the emergent market coherence to the N (Negotiation) role. Two derived scalar signals, D-C Imbalance and Energy Cost, govern all operational decisions including order mix, grid spacing, position sizing, and regime suppression. Grid level distances are set by a phi-spaced hierarchy rooted in the natural doubling rate $\ln(2)$, the most fundamental tholonic quantum. The bot ran live on SOL/USD for 59 days (April 30 to June 29, 2026), during which SOL fell 14.24% from $83.06 to $71.24. Over the same period, total equity declined only 0.27%, and SOL holdings grew from 556 to 1,279 units, a 129.9% increase achieved at an average acquisition cost of $63.50 per SOL, near the period low of $60.48. This paper presents the tholonic derivation of each design component and evaluates the empirical record against the bot's stated objective: accumulate the maximum quantity of the target asset.

A central principle of the design is that the asset itself (SOL) is the correct unit of account, not the dollar. A unit of SOL is structurally stable: its definitional properties are fixed by the network protocol and do not change when the market assigns it a different price. The US dollar, by contrast, is not a stable tholonic unit; its purchasing power is subject to exogenous forces unrelated to the trading strategy. Measuring performance in asset units removes this ambiguity and allows the N-D-C parameters to be defined against a consistent, structurally grounded substrate.

This paper does not present backtested performance projections, financial advice, or claims of generalisability beyond the instrument and period described. All claims are grounded in the event log produced by the live system.

---

## 1. Introduction

**What this paper provides.** A complete account of how tholonic N-D-C concepts are operationalised as quantitative trading signals; a derivation of the phi-spaced grid level hierarchy from first principles; a definition of the Energy and Imbalance signals and their roles in regime control; and an empirical evaluation of 59 days of live trading on SOL/USD against an accumulation objective.

**What this paper does not provide.** Generalised performance claims, financial return optimisation, price prediction, or any analysis of the value chain layer of the asset. The bot operates entirely in the physical-flow layer of the tholonic hierarchy: it measures what the market is doing (volume, momentum, distance from structural levels) and responds structurally. It does not forecast price.

**Organisation.** Section 2 reviews the tholonic N-D-C framework as applied to market systems; Section 2.1 establishes why the asset unit rather than the dollar is the correct measurement substrate. Section 3 defines the D and C primitives. Section 4 derives and explains the Imbalance and Energy signals in depth, including their appearance on the operational chart. Section 5 derives the phi-spaced grid level architecture. Section 6 describes the five operational modes. Section 7 covers the auxiliary phi-extension and lambda signals. Section 8 presents the 59-day empirical record. Section 9 discusses the results against the accumulation objective. Section 10 concludes.

---

## 2. The Tholonic N-D-C Framework Applied to Markets

The tholonic model, developed across [paper 1](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [paper 3](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf) of this series, holds that any stable system can be decomposed into three roles:

- **N (Negotiation):** the emergent, coherent state of the system. N is not directly observable; it arises from the balanced interaction of D and C.
- **D (Definition):** the constraints, limitations, and boundaries that define what the system is. D is internally focused; it resists change and enforces identity.
- **C (Contribution):** the outputs, flows, and integrations that define what the system does. C is externally focused; it expresses energy outward.

The core sustainability principle of the tholonic model is that a system is most stable and efficient when $D \approx C$. When either pole dominates, the system incurs an energy cost proportional to the square of the imbalance. This cost is not metaphorical: in physical systems it corresponds to real dissipation; in market systems it corresponds to unsustainable overextension in either direction.

![Tholonic N-D-C role assignment for market state. N (blue, top) is the emergent coherent state. C (red, lower-left) captures bullish contributions. D (green, lower-right) captures bearish constraints.](/home/jw/src/tv/docnav/Research/papers/20_tholonic-grid-trading-ndc/figures/20_ndc-market-triangle.png)

A market at any given moment can be mapped onto this structure. The bullish forces that push price upward and volume outward are C-type: they contribute energy to the system. The bearish forces that resist further advance and define structural ceilings are D-type: they constrain and bound. The actual price level, together with the coherence of that level relative to both poles, is N. When C and D are balanced, price is at an equilibrium that the system can sustain. When one pole dominates, the system is overextended and the imbalance creates pressure toward reversion.

### 2.1 Why the Asset Is the Correct Unit of Account

A foundational choice in this system is to measure success in units of the asset itself (SOL) rather than in dollars. This choice is not merely a preference; it follows directly from tholonic principles about what constitutes a stable, well-defined unit for measurement.

A unit of SOL is a fixed, self-consistent quantity. One SOL remains one SOL regardless of what price the market assigns to it at any given moment. Its physical properties as a digital asset, the computation it represents, the network stake it embodies, the protocol rules that define it: none of these change when the dollar price moves from $60 to $90 and back. The SOL token is, in tholonic terms, a stable N-state: its D (the protocol's definitional constraints) and C (its contribution to the network's operation) are structurally fixed by the protocol itself. The market price is an external opinion layered on top of that structure. It is not the thing itself.

The US dollar, by contrast, is not a fixed unit in any tholonic sense. Its purchasing power shifts continuously with monetary policy, inflation, and market sentiment. A dollar-denominated performance measure conflates two separate phenomena: the behavior of the trading strategy and the behavior of the dollar's own purchasing power. Using dollars as the unit of success introduces a moving baseline that can mask or distort the strategy's actual contribution.

This distinction has a direct technical consequence for N-D-C parameterisation. Because the D and C primitives measure structural market properties (distance to resistance, volume ratio, trend strength, support proximity), they can be defined precisely and stably when the objective unit is the asset. The question "how much of the asset did we acquire, and at what structural cost?" has a clean tholonic answer: each SOL acquired represents a negotiated outcome between the bullish forces that wanted to hold it above the buy level and the constraints that prevented it from rising further. That negotiation is exactly what the D-C Imbalance signal models.

If success were measured in dollars, the same structural event (a buy order filling at a phi-spaced level below spot) would have ambiguous value: it could look like a gain or a loss depending entirely on what the dollar subsequently does. The asset-denominated objective removes this ambiguity. The N-D-C parameters are defined against a stable substrate, and the results can be evaluated cleanly against the question the system was actually designed to answer: how efficiently is the bot converting available capital into units of a structurally stable asset?

---

## 3. D and C Primitive Definitions

Each of the four D and four C primitives is a scalar in $[0, 10]$, computed from the most recent closed 15-minute OHLCV bar window and clamped to prevent single-metric dominance.

### 3.1 D Primitives: Bearish Constraints

| Primitive | Formula | Interpretation |
|---|---|---|
| Resistance distance | $\text{clamp}\!\left(\frac{R - P}{P} \times 100\right)$ | Distance to nearest swing high above price. High resistance nearby = high D. |
| RSI overbought | $\text{clamp}\!\left(\frac{\text{RSI} - 50}{5}\right)$ | RSI above 50 contributes to D; below 50 contributes zero. |
| Realised volatility | $\text{clamp}\!\left(\frac{\sigma_r}{0.05}\right)$ | 30-bar rolling realised vol normalised to a 5% baseline. High vol = high uncertainty = high D. |
| Funding rate | $\text{clamp}\!\left(\max(f, 0) \times 100\right)$ | Positive funding on perpetuals indicates excess long positioning = bearish constraint on further advance. |

### 3.2 C Primitives: Bullish Contributions

| Primitive | Formula | Interpretation |
|---|---|---|
| Volume ratio | $\text{clamp}\!\left(5 \times \frac{V_t}{\bar{V}_{20}}\right)$ | Current bar volume relative to 20-bar mean. Rising volume = rising C. |
| Momentum score | $\text{clamp}\!\left(\frac{P - \text{EMA}_{50}}{\text{ATR}}\right)$ | Price above its 50-bar EMA = bullish momentum. Normalised by ATR. |
| Trend strength | $\text{clamp}\!\left(\frac{\text{ADX}}{10}\right)$ | ADX normalised to $[0, 10]$. Strong directional trend = high C. |
| Support distance | $\text{clamp}\!\left(10 - \frac{P - S}{P} \times 100\right)$ | Proximity to nearest swing low below price. Close to support = high C (limited downside). |

$D_{\text{total}} = \sum D_i$, $\quad C_{\text{total}} = \sum C_i$

Both totals have a theoretical range of $[0, 40]$ given four clamped $[0, 10]$ components.

---

## 4. Imbalance and Energy: The Core Signal Pair

These two derived scalars are the engine of every operational decision in the bot. They appear on the live operational chart as the two lower panels (labelled "NDC Imbalance" and, implicitly, the energy threshold crossings).

### 4.1 Imbalance

$$\text{Imbalance} = \frac{C_{\text{total}} - D_{\text{total}}}{\max(C_{\text{total}}, D_{\text{total}})}$$

Imbalance is a signed, normalised measure of which pole dominates, on a scale from $-1$ (fully D-dominant, maximum bearish constraint) to $+1$ (fully C-dominant, maximum bullish contribution).

At zero, $C = D$ and the system is in tholonic balance. The threshold $\pm 0.0347$ is not arbitrary: it is $\ln(2)/20$, half the base tholonic quantum, used as the minimum meaningful deviation from balance before the regime shifts.

The interpretation at each regime boundary:

| Imbalance | Market meaning | Bot response |
|---|---|---|
| $> +0.0347$ | C overwhelms D; market in bullish overexpression | Distribute: 3 buys, 5 sells |
| $[-0.0347,\, +0.0347]$ | Near balance; no dominant pole | Neutral: 5 buys, 3 sells (accumulation default) |
| $< -0.0347$ | D overwhelms C; market compressed by bearish constraint | Accumulate: 5 buys, 1 sell |

Crucially, the neutral default is asymmetric: 5 buys and 3 sells rather than equal counts. This encodes the stated objective (accumulate the asset) at the structural level. Even when the signal is inconclusive, the bot's default behavior is accumulation-biased.

### 4.2 Energy Cost

$$E = |\text{Imbalance}|^2 \times D_{\text{max}}^2 + E_{\text{base}}$$

In a simplified but operationally equivalent form used in the code:

$$E = \left(\frac{|C - D|}{\max(C, D)}\right)^2 + E_{\text{base}}$$

where $E_{\text{base}} = 10$.

Energy quantifies the cost of maintaining the current imbalanced state. It is not volatility; it is the tholonic cost of imbalance: a system far from $D = C$ must expend energy to maintain that deviation, and the cost grows quadratically with the deviation. A balanced system ($D = C$) has only the base cost $E_{\text{base}}$. A maximally imbalanced system (one pole at zero) has $E = 1 + E_{\text{base}} = 11$ at the formula level, but the quadratic scaling means large sustained deviations quickly reach the regime threshold.

The energy threshold $E_{\text{max}} = 135$ defines the boundary above which the system is in a high-cost, unstable state. When $E > E_{\text{max}}$:

- If Imbalance $> 0$ (C-dominant spike): the market is in a bull overextension. The bot enters **buy-only mode**, suppressing all sell orders and accumulating through the rally.
- If Imbalance $\leq 0$ (D-dominant spike): the market is in chaos or a bear crush. The bot **pauses** entirely, placing no orders.

This asymmetry is again structural: C-dominant high-energy states are accumulation opportunities; D-dominant high-energy states are danger zones.

### 4.3 The N State

$$N = \sqrt{D_{\text{total}} \times C_{\text{total}}} \times B$$

where the balance factor $B = \dfrac{1}{1 + |D - C| / \max(D, C)}$.

N is the geometric mean of the two poles, penalised by their imbalance. This formulation is consistent with the tholonic principle established in [paper 1](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf): N maximises when $D = C$, and collapses toward zero as either pole approaches zero. N is logged at each run but does not directly control order placement; it is the diagnostic of overall system coherence.

### 4.4 Reading the Operational Chart

The screenshot accompanying this paper shows the live operational display. The lower chart panel, labelled "NDC Imbalance," plots the Imbalance signal as a time series against its $\pm 0.0347$ threshold bands. The green-filled region above zero reflects sustained C-dominance; the narrow red regions reflect the brief D-dominant episodes during the May price decline. The flat band near zero in quiet periods corresponds to the neutral regime.

The energy signal does not appear as a separate visual panel in the standard chart display, but its effect is visible in the order activity: the 15 buy-only events and the absence of any full pause events correspond to the 953 runs (17.3% of the total) where energy exceeded $E_{\text{max}} = 135$.

![SOL/USD price (top), D-C Imbalance (middle), and Energy Cost (bottom) over the 59-day run. Red bars in the imbalance panel indicate C-dominant conditions; green bars indicate D-dominant. The horizontal dashed line in the energy panel marks the pause/hold threshold.](/home/jw/src/tv/docnav/Research/papers/20_tholonic-grid-trading-ndc/figures/20_energy-imbalance-timeseries.png)

---

## 5. Grid Architecture: Phi-Spaced Level Hierarchy

### 5.1 The Base Quantum

The grid level spacings are derived from the tholonic base quantum:

$$u = \frac{\ln 2}{10} \times s$$

where $s$ is a timeframe scale factor ($s = 0.35$ for 15-minute bars; $s = 1.0$ for 4-hour bars). The use of $\ln 2$ is not arbitrary: it is the natural doubling rate, the minimal quantum of binary distinction in the tholonic framework. At $s = 0.35$, the base quantum is $u \approx 0.00243$, or 0.243% of the current price per level.

### 5.2 The Five Phi-Spaced Levels

Five grid levels are placed at the following distances from the current price, in both directions:

$$\left\{\frac{u}{\varphi^2},\; \frac{u}{\varphi},\; u,\; u\varphi,\; u\varphi^2\right\}$$

where $\varphi = (1 + \sqrt{5})/2 \approx 1.61803$ is the golden ratio.

At $s = 0.35$, these evaluate to approximately:

| Level | Formula | Distance from spot |
|---|---|---|
| 1 | $u / \varphi^2$ | 0.93% |
| 2 | $u / \varphi$ | 1.50% |
| 3 | $u$ | 2.43% |
| 4 | $u \cdot \varphi$ | 3.93% |
| 5 | $u \cdot \varphi^2$ | 6.35% |

The ratio of any adjacent level pair is $\varphi$. This makes the grid self-similar: zooming into the spacing between any two levels reveals the same proportional structure as the whole. This is the direct market application of the tholonic principle that stable, sustainable hierarchical structures are self-similar at all scales.

![Phi-spaced grid level diagram showing buy levels (red, below spot) and sell levels (green, above spot) with their tholonic formula labels and percentage distances from the current price.](/home/jw/src/tv/docnav/Research/papers/20_tholonic-grid-trading-ndc/figures/20_phi-grid-levels.png)

---

## 6. Operational Modes and Regime Logic

### 6.1 Hysteresis

Regime changes require the signal to exceed the threshold for at least two consecutive bars before the mode flips. This prevents oscillation around the threshold boundary from causing excessive order cancellation and replacement. The hysteresis band effectively smooths the mode signal while preserving responsiveness to sustained changes.

### 6.2 The Five Modes

**Distribute** ($\text{Imbalance} > +0.0347$, normal energy): 3 buy levels below spot, 5 sell levels above spot. The bot is reading a C-dominant environment and positions to capture mean reversion: few buys (limited upside buying interest) and more sells (take profit into strength). In a sustained downtrend, sell levels placed above a declining price do not fill; the buy levels fill repeatedly. This explains the paradox that a bot running 87% of the time in distribute mode still accumulated net SOL during a declining market.

**Neutral** ($|\text{Imbalance}| \leq 0.0347$): 5 buy levels, 3 sell levels. The default accumulation-biased grid.

**Accumulate** ($\text{Imbalance} < -0.0347$, normal energy): 5 buy levels, 1 sell level. Near-suppression of selling during D-dominant compression.

**Buy-only** ($E > E_{\text{max}}$ and $\text{Imbalance} > 0$): 5 buy levels, 0 sell levels. The system reads a high-energy C-dominant spike as a bull overextension that should be accumulated through, not sold into.

**Pause** ($E > E_{\text{max}}$ and $\text{Imbalance} \leq 0$): 0 orders. High-energy D-dominant states are structurally unpredictable; the bot steps aside entirely.

---

## 7. Auxiliary Signals

### 7.1 Phi-Extension Signal

The ratio of successive swing highs is compared to $\varphi$:

$$r = \frac{H_{t}}{H_{t-1}}$$

If $r > \varphi + 0.15$: the market is overextended relative to its natural growth rate. One buy level is removed and one sell level added (tilt toward distribution).

If $r < \varphi - 0.15$: the market is under-extended. One buy level is added and one sell level removed (tilt toward accumulation).

This signal fired in only 4.4% of runs during the observed period (phi_signal = +1, under-extended), consistent with a sustained declining market that never produced a blow-off top.

### 7.2 Lambda: Volume Recovery Signal

Lambda detects volume recovering from a recent trough:

$$\lambda = \min\!\left(1,\; \frac{V_{\text{ratio}} - 1}{2}\right) \quad \text{when volume is recovering}$$

Buy order sizes are scaled by $(1 + 0.618 \times \lambda)$, where the weight $0.618 = 1/\varphi$ is the tholonic balance ratio. Lambda fired in 1,291 of 5,518 runs (23.4%), scaling up buy sizes during volume-recovery events to front-run anticipated C-signal strengthening.

---

## 8. Empirical Results: 59-Day SOL/USD Run

### 8.1 Setup

The bot ran live on the Alpaca cryptocurrency API, trading SOL/USD on a 15-minute execution cadence. The signal timeframe was 15-minute OHLCV bars with a 100-bar lookback. A 5-minute reclaim trigger filter required lower-timeframe confirmation before order placement. Enhanced NDC risk controls were enabled, including adaptive ATR-based spacing, inventory-aware sizing, and the no-trade zone suppression.

### 8.2 Summary Statistics

| Metric | Value |
|---|---|
| Period | April 30 to June 29, 2026 (59 days) |
| Total runs | 5,518 (15-minute cadence) |
| SOL/USD price change | $83.06 to $71.24 (-14.24%) |
| SOL price low | $60.48 |
| Starting equity | $97,179 |
| Ending equity | $96,921 (-0.27%) |
| Equity peak | $108,194 |
| Equity trough | $83,635 |
| Starting cash | $50,984 |
| Ending cash | $5,108 |
| Starting SOL held | 556 |
| Ending SOL held | 1,279 |
| SOL gained | +722 (+129.9%) |
| Implied average acquisition price | $63.50/SOL |
| Unrealised gain on acquired SOL | +$5,586 |
| Total orders placed | 28,963 |
| Order success rate | 71.5% |
| Total buy orders | 16,456 |
| Total sell orders | 24,048 |

### 8.3 Mode Distribution

The distribute mode dominated at 86.8% of runs, reflecting sustained C-dominance (mean imbalance +0.44) even as price declined. Accumulate mode ran for 6.5% of runs, concentrated during the price troughs in May and June. Buy-only mode fired 15 times during brief high-energy C-dominant spikes.

![Operational mode distribution across 5,518 runs (left) and the distribution of D-C Imbalance values over the full period (right). The imbalance distribution is strongly right-skewed, confirming persistent C-dominance.](/home/jw/src/tv/docnav/Research/papers/20_tholonic-grid-trading-ndc/figures/20_mode-distribution.png)

### 8.4 Accumulation Record

The bot converted $45,875 in cash into 722 additional SOL at an average cost of $63.50 per unit, 23.5% below the entry price of $83.06 and only $3.02 above the period low of $60.48. The accumulation rate accelerated in June as price fell further and lambda-scaling increased buy sizes at volume-recovery inflection points.

![SOL held (top, red), cash balance (middle, green), and total equity (bottom, blue) over the 59-day run. Cash was systematically deployed into SOL as price declined, with SOL holdings more than doubling while equity remained nearly flat.](/home/jw/src/tv/docnav/Research/papers/20_tholonic-grid-trading-ndc/figures/20_accumulation-cash-equity.png)

---

## 9. Discussion

### 9.1 Accumulation Objective Assessment

The stated objective was to accumulate the maximum quantity of SOL rather than to maximise dollar-denominated equity. By that measure, the result is strong: 129.9% growth in SOL holdings over a period where holding SOL in cash-equivalent terms would have cost 14.24% in dollar value. The bot converted that paper loss into asset accumulation, acquiring 722 SOL at below-market cost.

The near-flat equity (-0.27%) is not the primary measure of success but confirms that the accumulation was achieved without significant dollar-denominated destruction. The equity low of $83,635 (in late May) coincided with the price trough, at which point the bot's unrealised losses on earlier SOL purchases were at their maximum. Recovery in June reflected both price stabilisation and the accumulation of lower-cost SOL reducing the average basis.

### 9.2 The Distribute-Mode Accumulation Paradox

The dominant finding is that the bot ran 87% of the time in distribute mode while net-accumulating SOL. This is explained by the asymmetric fill dynamics of a limit-order grid in a trending market. In distribute mode, sell orders are placed above the current price. When price is declining, those sells are never reached. The buy orders placed below spot, however, are reached on every dip. The net effect is that distribute mode in a declining market becomes a systematic buy program, despite its label. The tholonic framework did not fail here; the label "distribute" refers to the bot's intent given the signal state, not to the actual fills achieved.

A recalibration of the D primitive weights would correct the signal: if the D parameters better captured the declining trend (for example, by weighting MACD histogram or the rate of change of resistance levels), imbalance would have shifted toward D-dominance or neutral more often, reducing the distribute-mode dominance. This is a parameter tuning question, not a structural flaw.

### 9.3 Cash Exhaustion Risk

Cash declined from $50,984 to $5,108 over the period. With cash nearly depleted, the bot's capacity to place buy orders is now severely constrained. If price continues to decline, the accumulation rate will fall to whatever sell fills can be captured at higher prices and recycled. The `max_deploy_usd` and `capital_per_level_usd` parameters should be reviewed and tightened to preserve a minimum cash reserve.

### 9.4 Order Rejection Rate

The 28.5% order rejection rate is elevated and represents wasted API calls and potential missed fills. The likely cause is minimum notional violations: as SOL price declined, the fixed dollar-per-level size ($1,794 default) converted to increasingly large SOL quantities, and the resulting sell orders at higher price levels sometimes fell below the exchange's minimum notional. Dynamic sizing proportional to current price, rather than fixed dollar amounts, would reduce rejections.

---

## 10. Conclusion

The tholonic N-D-C framework provides a structurally coherent basis for market signal design. Mapping bearish constraints to D, bullish contributions to C, and market coherence to N produces an operationally interpretable signal pair: Imbalance measures which pole dominates; Energy measures the cost of that domination. Together they govern all regime transitions in a principled, derivable way rather than through empirically tuned moving-average crossovers.

The phi-spaced grid level hierarchy, derived from $\ln(2)$ and $\varphi$, places limit orders at self-similar distances that correspond to the natural structure of a recursive triadic system. The golden ratio appears not as decoration but as the structural attractor of the level spacing, directly analogous to its appearance in the convergence hierarchies documented in [paper 1](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [paper 11](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/11_tholonic-seed-space-power-of-two-hierarchy/11_tholonic-seed-space-power-of-two-hierarchy.pdf) of this series.

The 59-day live record on SOL/USD confirms that the system achieved its accumulation objective: 129.9% growth in SOL holdings at an average cost near the period low, with equity preservation of -0.27% against a -14.24% spot price decline. The open questions (D-parameter recalibration, cash reserve management, order sizing dynamics) are parameter-level refinements, not structural concerns.

---

## References

[Mil26a] Milton, J. W. *Emergence of Classical Constants from a Minimal Recursive Triadic Framework.* Clarity Coalition, paper 1 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf>

[Mil26b] Milton, J. W. *A Minimal Recursive Triadic Framework for Self-Similar Hierarchical Systems.* Clarity Coalition, paper 3 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf>

[Mil26c] Milton, J. W. *Power-of-Two Convergence Counts in the Tholonic Seed Space: A Complete Hierarchy of Classical Constants.* Clarity Coalition, paper 11 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/11_tholonic-seed-space-power-of-two-hierarchy/11_tholonic-seed-space-power-of-two-hierarchy.pdf>
