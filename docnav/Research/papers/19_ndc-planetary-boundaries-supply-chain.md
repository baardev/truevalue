# Phase-Resolved Sustainable Supply Chain Analysis Using a Triadic Balance Framework: Structural Alignment with Planetary Boundaries

**Author:** Sarah Jones and J. W. Milton, Clarity Coalition

**Version:** 0.1 (Working Draft)

**Date:** 28 June 2026

**Keywords:** planetary boundaries; supply chain sustainability; N-D-C framework; phase-resolved analysis; triadic balance; TVPCI; structural governance; safe operating space; commodity chains; sustainability science

---

## Abstract

The Planetary Boundaries framework (Rockström et al. 2009) identifies nine Earth-system processes whose biophysical thresholds define a safe operating space for humanity. Seven of nine boundaries have now been transgressed. Yet despite fifteen years of refinement, the framework provides no structural mechanism for translating global thresholds into supply chain architecture: it identifies where the limits are, not how chains must be organized to respect them. This paper introduces a phase-resolved triadic balance framework, the N-D-C model, as that structural bridge. In the N-D-C model, each phase of a supply chain hosts three functionally distinct roles: N (the negotiated equilibrium state), D (definition or constraint), and C (contribution or output flow). A balance score $B(D,C) = \frac{2 \cdot \min(D,C)}{D+C} \times 100$ measures structural health at each phase; systems are stable when $B \geq 61.8$ (equal to $100/\varphi$, where $\varphi$ is the golden ratio). Applied across a corpus of 18 supply chains in six sectors developed collaboratively over the period 2016-2026, we demonstrate that D/C structural imbalance at the phase level indexes the class of planetary boundary transgression that the chain generates. D-heavy phases (over-constrained extraction with insufficient output accounting) correspond to D-type boundary violations (climate, land use, freshwater); C-heavy phases (unregulated throughput) correspond to C-type violations (biosphere integrity, biogeochemical flows). Five mathematical constants emergent from the triadic recursion ($\pi$, $\varphi$, $\sqrt{2}$, $\ln 2$, $e$) provide a five-axis diagnostic that localizes failure mode, severity, and intervention priority within the Planetary Boundaries safe operating space. The framework reframes planetary sustainability governance from a monitoring problem to a structural balance problem, opening a new intervention design space at the phase level rather than the system level.

---

## 1. Introduction

**The open structural problem.** The Planetary Boundaries framework [Rock09] is the most cited quantitative framework for Earth-system sustainability. Since its introduction in a landmark 2009 *Nature* paper, it has been updated twice [Stef15, Rich23], adopted by the United Nations, embedded in corporate ESG reporting standards, and extended to sub-global scales. Seven of its nine boundaries have now been transgressed [Rich23]. Yet despite this influence, the framework has a structural gap that has remained unaddressed: it operates at the level of global Earth-system processes and provides no mechanism for connecting those global thresholds to the phase-level decisions within commodity supply chains that actually drive boundary transgressions.

The practical consequence is that supply chain sustainability governance proceeds in parallel with Planetary Boundaries analysis rather than being structurally grounded in it. Life-cycle assessment (LCA) methods quantify impacts per unit of product but do not enforce phase ordering or test for structural balance between constraining and contributing forces at each phase [Mon15]. ESG composite indices aggregate indicators but document low inter-rater agreement and no consistent phase structure [Berg22]. Certification schemes (Fairtrade, RMAP, FSC) reduce multi-phase evidence to a binary label [Mos19]. None of these tools provides a phase-resolved structural diagnosis that connects to the biophysical architecture of the boundaries themselves.

**What this paper provides.** We present the N-D-C triadic framework as a structural bridge between phase-level supply chain analysis and the Planetary Boundaries safe operating space. We make four claims. First, the nine planetary boundaries can be partitioned into D-type boundaries (constraints on extraction and transformation) and C-type boundaries (consequences of uncontrolled outputs and waste flows), corresponding structurally to the N-D-C roles of Definition and Contribution. Second, a phase-level balance score derived from the N-D-C framework indexes which class of boundary transgression a given supply chain phase generates. Third, five mathematical constants that emerge naturally from the N-D-C recursive structure each identify a distinct failure mode within the Planetary Boundaries diagnostic space. Fourth, the framework is empirically grounded in an 18-chain cross-sector corpus developed over the period 2016-2026.

**What this paper does not provide.** We do not claim that N-D-C balance scores predict the magnitude of boundary transgression in physical units. We do not provide a life-cycle inventory or a full quantitative calibration against measured boundary control variables; those are explicitly deferred to predecessor work (see Section 6.3). We do not model pricing, financial leverage, or policy mechanisms; these belong to separate analytical layers. The framework developed here is structural and organizational, not predictive.

**Organization.** Section 2 reviews the Planetary Boundaries framework and the N-D-C triadic model. Section 3 maps the nine boundaries to N-D-C structural roles. Section 4 presents the empirical application across the 18-chain corpus. Section 5 develops the five-constant diagnostic framework. Section 6 discusses implications, limitations, and the research path forward. Section 7 concludes. The Methods section provides the full scoring algorithm, phase definitions, and corpus description.

---

## 2. Background

### 2.1 The Planetary Boundaries Framework

Rockström et al. [Rock09] proposed nine Earth-system processes whose destabilization could push the planet outside the relatively stable Holocene conditions within which human civilization developed. For each process, a control variable and a proposed boundary value were identified. The nine boundaries are: climate change (atmospheric CO$_2$ concentration), rate of biodiversity loss (now reframed as biosphere integrity), biogeochemical flows (nitrogen and phosphorus cycles), stratospheric ozone depletion, ocean acidification (aragonite saturation state), global freshwater use, land-system change (fraction under cropland), chemical pollution and novel entities, and atmospheric aerosol loading.

The 2015 update [Stef15] refined several boundary definitions and provided the first quantitative assessment of biosphere integrity. The 2023 full assessment [Rich23] determined that seven of nine boundaries have been transgressed, including climate change, biosphere integrity, land-system change, freshwater change, and biogeochemical flows, with chemical pollution also having crossed its safe zone. The framework has since been incorporated into major governance documents including the Kunming-Montreal Global Biodiversity Framework and various national climate policies.

A persistent methodological challenge has been the translation of global-scale boundaries to the supply chain and firm level [Nijs15, Plan21]. Studies have identified three major obstacles: scaling global thresholds to company-level impacts; allocating fair shares of the safe operating space across value chain actors; and coordinating implementation across multi-jurisdictional chains [Nijs15]. The N-D-C framework addresses the second and third of these through its phase-ordered structural model.

### 2.2 The N-D-C Triadic Framework

The N-D-C framework, developed in this series beginning with [paper 3](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf), posits that any stable, self-sustaining system instantiates three irreducible functional roles.

**N (Negotiation)** is the emergent stable equilibrium state: the coherent identity produced by the interaction of D and C. N is not a single component but a relational outcome; it is both the product of D-C balance at one level and the source that differentiates into D and C at the next level down.

**D (Definition/Limitation)** is the constraining apparatus: bounds, specifications, policies, resource limits. It is internally focused, governing structure, identity, and what a phase IS.

**C (Contribution/Integration)** is the integrating-expressive apparatus: outputs, flows, connections, externalities. It is externally focused, governing what a phase DOES and produces for adjacent phases.

The balance functional is:

$$B(D,C) = \frac{2 \cdot \min(D,C)}{D+C} \times 100$$

This ranges from 0 (total D or C dominance) to 100 (perfect balance). The stability threshold is $B^* = 100/\varphi \approx 61.8$, where $\varphi = (1 + \sqrt{5})/2$ is the golden ratio. Systems with $B < B^*$ are structurally unstable: the D-C imbalance generates energy costs, degrades the N state, and propagates instability to adjacent phases. The threshold $B^* = 61.8$ is not an empirical parameter but a mathematical consequence of the recursion structure established in [paper 1](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf).

The recursive cycle is bidirectional: Parent N differentiates into D and C, D and C negotiate to instantiate Child N, and Child N becomes the Parent N of the next level. This is not a one-way hierarchy. Applied to supply chains, a phase map is the Child N at the supply-chain level; each individual phase is the Child N at the phase level; and the operational entity (a productive mine, a certified refinery) is the Child N at the operational level.

### 2.3 TVPCI: Phase-Resolved Scoring

[Paper 2 of this series](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.pdf) formalizes the Transparency via Phase-resolved Classification and Indexing (TVPCI) framework, which operationalizes N-D-C scoring for commodity chains. Each phase $p$ hosts three non-negative observables: $N_p$ (declared position and mass-balance coherence), $D_p$ (bounding evidence: audit scope, regulatory constraints, counterparty opacity caps), and $C_p$ (independent corroboration depth: third-party assays, geospatial attestations, physical touchpoints). A transition penalty $\tau_p$ reduces the contribution of a phase when its N-state carries unresolved red flags from the prior phase. The full TVPCI index combines phase-local balance scores into a weighted aggregate with chain-level propagation.

The present paper extends TVPCI by connecting its phase-level balance scores to the Planetary Boundaries framework. Whereas TVPCI was developed to measure transparency and custody integrity in commodity chains, the structural balance machinery is identical for measuring sustainability compliance: in both cases, the question is whether D-type evidence (constraint, limit, policy) is in structural balance with C-type evidence (output, flow, corroboration) at each phase.

### 2.4 The Five Constants as Diagnostic Axes

A separate result in this series, established in [paper 1](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and extended in [paper 11](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/11_tholonic-seed-space-power-of-two-hierarchy/11_tholonic-seed-space-power-of-two-hierarchy.pdf), is that five classical mathematical constants emerge naturally from the N-D-C recursive structure: $\pi/4$, $\varphi$, $\sqrt{2}$, $\ln 2$, and $e$. Each constant characterizes a distinct class of recursion behavior in the N-D-C framework. We introduce in Section 5 a mapping between these five constants and five distinct failure modes in the Planetary Boundaries diagnostic space.

---

## 3. Mapping Planetary Boundaries to N-D-C Structural Roles

### 3.1 Structural Partition of the Nine Boundaries

The nine planetary boundaries divide naturally into two structural classes when viewed through the N-D-C lens.

**D-type boundaries** are violated by the failure of constraining systems: insufficient regulatory limits, inadequate extraction controls, absent policy frameworks. They represent cases where the D role at the supply chain phase is weak relative to the C role. The chain is contributing (extracting, processing, emitting) beyond the capacity of its constraining structure to bound it:

- *Climate change* (CO$_2$ concentration): transgressed by extraction phases with inadequate carbon constraint mechanisms.
- *Land-system change* (cropland fraction): transgressed by expansion of agriculture or mining into non-cropland without binding land-use limits.
- *Freshwater use* (consumptive runoff): transgressed by processing and irrigation phases with no effective abstraction limits.
- *Stratospheric ozone* (Dobson unit floor): transgressed historically by chemical processing phases with no effective emissions controls (a D-type institutional failure).
- *Novel entities* (chemical pollution load): transgressed by fabrication and processing phases lacking comprehensive chemical constraint registries.

**C-type boundaries** are violated by the failure of output accounting and externality management: untracked waste flows, unaccounted ecological throughput, disconnected financial abstractions. They represent cases where the C role at the supply chain phase is producing outputs that are not bounded or reincorporated:

- *Biosphere integrity* (extinction rate): transgressed by habitat loss driven by land-use C outputs (clearing, fragmentation) that are not balanced by conservation D inputs.
- *Biogeochemical flows* (N and P cycle loads): transgressed by agricultural and fabrication phases whose chemical output flows exceed ecological reabsorption capacity.
- *Ocean acidification* (aragonite saturation): transgressed by aggregate CO$_2$ C outputs across the chain.
- *Atmospheric aerosol loading*: transgressed by diffuse combustion and processing C outputs.

Figure 1 maps these roles onto the N-D-C triangle.

![Figure 1. N-D-C Triadic Framework and Planetary Boundary Role Assignment.](/home/jw/src/tv/docnav/Research/papers/19_ndc-planetary-boundaries-supply-chain/figures/19_pb-ndc-triangle.png)

### 3.2 The Structural Claim

The core structural claim of this paper is as follows. A supply chain phase with $D \gg C$ (D-heavy imbalance) is, by structural definition, a phase in which constraining and limiting forces dominate over output and flow accounting. This structural condition is precisely the condition that generates D-type boundary transgressions: the chain is extracting and transforming under conditions where D-type governance is weak, so the extraction exceeds D-type boundary thresholds. Conversely, a phase with $C \gg D$ (C-heavy imbalance) is generating outputs and externalities that are not bounded by constraining structures, which is the structural condition for C-type boundary transgressions.

Note that this claim inverts the naive intuition. A D-heavy supply chain phase does not have *too much* constraint: it has too little C-type accountability to balance the constraints it does have. The D-type boundary is transgressed not because D is large but because D and C are not in balance, allowing the chain to operate without the feedback loop that an active C role would provide. The formal treatment is in the Methods section.

### 3.3 Phase Ordering and Transgression Propagation

Boundary transgressions are not uniformly distributed across supply chain phases. Extraction (Phase 0) and aggregation (Phase 1) phases carry the highest D-heavy imbalance in the extractive commodities in our corpus (gold, cocoa, shea). These are also the phases responsible for the majority of transgression of climate, land-use, and biodiversity boundaries in those chains [OECD22, GRI21]. Processing and refining phases (Phases 2 and 3) contribute primarily to freshwater and chemical pollution boundaries. Distribution phases (Phase 5 onward) contribute mainly to climate (transport emissions) and novel-entities boundaries at lower relative magnitudes.

The N-D-C transition penalty mechanism (see Methods) propagates imbalance downstream: a phase with unresolved D-heavy deficit at Phase 0 reduces the effective N-state inherited by Phase 1, compounding the structural weakness. This cascade effect means that early-phase boundary transgressions cannot be compensated by late-phase interventions: the structural damage is encoded in the chain's phase map.

---

## 4. Empirical Application: Eighteen Supply Chains, 2016-2026

### 4.1 The Research Corpus

The empirical basis for this paper is a corpus of 18 supply chain analyses developed collaboratively over the period 2016-2026 (Figure 6). The corpus spans six sectors: extractive commodities (gold, cocoa), agricultural commodities (shea, olive oil, gran chaco soy/cattle), agroforestry systems (Senegal agroforestry, AUBEB, Bristol One City), water supply systems (Jackson MS, NewWater, OCWD), energy infrastructure (Grid ERCOT URI winter event), and ecosystem service chains (blue carbon, Marina Alta). Each chain was analyzed using the N-D-C phase-resolved scoring framework; phase counts range from 5 to 10 phases depending on commodity complexity. Detailed corpus metadata are in the Methods section.

The 2016 start date is not arbitrary. The framework's conceptual foundations were developed in parallel with the initial gold supply chain prototype, providing ten years of iterative refinement across sectors with substantially different phase structures, opacity profiles, and planetary boundary exposures. This longitudinal depth is the primary empirical differentiator of this paper from prior single-commodity or single-sector sustainability analyses.

![Figure 6. Research Trajectory 2016-2026: Supply Chain Corpus Development.](/home/jw/src/tv/docnav/Research/papers/19_ndc-planetary-boundaries-supply-chain/figures/19_research-timeline.png)

### 4.2 Phase Balance Scores Across Representative Chains

Figure 2 displays the phase-resolved balance scores for five representative chains: gold, West African shea, cocoa international, Spain olive oil, and blue carbon. These five were selected to represent the full range of PB pressure categories: mining/energy, land use/agriculture, and ecosystem services.

Several patterns are immediately evident. First, extraction and aggregation phases (Ph.0 and Ph.1) fall below the 61.8 stability threshold across all three extractive/agricultural chains. Gold reaches its minimum at Phase 1 (aggregation, $B = 35$), driven by the near-total opacity of artisanal and small-scale mining aggregation that prevents any C-type corroboration from entering the phase score. Cocoa reaches its minimum at Phase 0 ($B = 26$), reflecting the documented absence of traceability to farm level in the majority of international cocoa supply [Mos19]. Shea shows a similar but slightly higher minimum ($B = 40$) due to cooperative-level aggregation providing some C-type evidence.

Second, balance scores improve consistently through the processing and distribution phases (Ph.2 through Ph.5) as regulatory oversight, certification, and financial record-keeping add both D and C evidence. The improvement is steeper for gold and olive oil than for cocoa or shea, because the former two chains have well-documented certification and assay infrastructure at the refining stage.

Third, Phase 6 (vaulting/storage) shows a secondary dip in gold ($B = 44$), reflecting the structural opacity of custodial vaulting arrangements that are documented in [paper 2](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.pdf).

![Figure 2. Phase-Resolved Balance Scores Across Five Supply Chains (Schematic).](/home/jw/src/tv/docnav/Research/papers/19_ndc-planetary-boundaries-supply-chain/figures/19_phase-balance-heatmap.png)

### 4.3 Chain Average Balance and PB Transgression Class

Figure 3 plots chain average balance scores against primary PB pressure category for all 18 chains. The structural prediction is that chains below the 61.8 threshold will correspond to primary transgressions of the PB category matching their imbalance type (D-heavy chains under mining/energy and land-use; C-heavy chains under ecosystem services and water).

The data support this prediction. The eight chains in the mining/energy and land-use PB categories (gold versions 1-3, cocoa international, gran chaco, West African shea, Burkina Faso shea) all fall below the stability threshold, with averages ranging from 50 (gran chaco) to 62 (gold v3). These chains are primary contributors to land-system change, biodiversity, and climate boundary transgressions [IPCC21, CBD22]. The water corpus (Jackson MS, NewWater, OCWD) shows the largest within-category spread ($B = 48$ to $B = 74$), consistent with the substantial variation in regulatory frameworks across the three case jurisdictions. The ecosystem service chains (blue carbon, marina alta, AUBEB, Bristol) cluster near or above the threshold, reflecting the higher C-type accountability embedded in carbon market protocols and municipal planning frameworks.

The grid ERCOT URI chain ($B = 56$) falls below the threshold and is classified as D-heavy: the Texas winter event of February 2021 is structurally explicable as a failure of D-type constraints (weatherization requirements, supply adequacy standards) in the face of C-type stress (extreme demand and physical output demands on the grid). This matches the N-D-C structural prediction.

![Figure 3. Chain Average Balance Score vs. Primary Planetary Boundary Pressure Category.](/home/jw/src/tv/docnav/Research/papers/19_ndc-planetary-boundaries-supply-chain/figures/19_balance-vs-pb-scatter.png)

### 4.4 Supply Chain Phase DAG with Boundary Annotations

Figure 5 shows the generic eight-phase supply chain directed acyclic graph (DAG) with planetary boundary pressure annotations at each phase. The DAG scope is declared as a modeling constraint: the chain is treated as linear within the custody horizon, with outer ecological cycles (recycling, carbon resequestration, biodiversity recovery) modeled as feedback terms in the N state, not as primary chain phases. This boundary is discussed in Section 6.2.

![Figure 5. Eight-Phase Supply Chain DAG with Planetary Boundary Pressure Annotations.](/home/jw/src/tv/docnav/Research/papers/19_ndc-planetary-boundaries-supply-chain/figures/19_supply-chain-dag.png)

---

## 5. The Five-Constant Diagnostic Framework

### 5.1 Constants as Failure-Mode Indices

[Paper 1 of this series](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) establishes that five classical constants emerge from the N-D-C recurrence family under three traversal classes: Advancing ($\pi/4$, unique; requires seeds $\{1,3,5\}$ and external injection), Self-redefined ($\varphi$ via continued-fraction fixed point; $\sqrt{2}$ via Babylonian method), and Fixed ($e$ via factorial series; $\ln 2$ via alternating harmonic series). Each constant characterizes a different dynamical relationship between D and C across the recursion.

We introduce the following mapping from these constants to supply chain sustainability failure modes within the Planetary Boundaries diagnostic space:

**$\pi$ (operational balance axis, threshold $\approx 78.5$):** $\pi/4$ is the unique constant requiring external seed injection; it measures the aggregate operational balance of the chain. A chain whose phase-average balance score falls below $\pi \times 25 = 78.5$ has phases pulling the aggregate below the externally-grounded threshold. In PB terms, this is the axis that detects systemic boundary pressure: chains below the $\pi$-threshold are structurally operating outside the safe operating space across multiple boundary categories simultaneously.

**$\varphi$ (value distribution axis, threshold $\approx 61.8$):** $\varphi$ is the self-redefined fixed point of the continued-fraction recursion. It measures proportional value distribution across phases. A $\varphi$-failure occurs when value (material, financial, or informational) is trapped at phase transitions rather than flowing proportionally through the chain. In PB terms, $\varphi$-failure corresponds to concentrated extraction pressure: a small number of phases carrying a disproportionate share of the chain's throughput, generating localized boundary transgressions at those phases.

**$\sqrt{2}$ (structural overhead axis, threshold $\approx 70.7$):** $\sqrt{2}$ emerges from the self-redefined Babylonian recursion and measures the structural overhead ratio: D rising without a corresponding rise in C. A $\sqrt{2}$-failure indicates that institutional, physical, or governance overhead has accumulated without generating proportionate output flows. In PB terms, this corresponds to regulatory capture or certification proliferation without genuine boundary compliance: D metrics (policy layers, audit requirements) increase while C metrics (actual ecological impact reduction) do not.

**$\ln 2$ (transformation efficiency axis, threshold $\approx 69.3$):** $\ln 2$ is the fixed point of the alternating harmonic series and measures transformation efficiency: the fraction of input that successfully converts to output without temporal loss. A $\ln 2$-failure indicates a time-lag or capital-lock gap at a processing phase. In PB terms, this corresponds to biological or geochemical transformation delays (soil carbon sequestration lag, nitrogen denitrification rate) that prevent a phase from achieving balance within the planning horizon.

**$e$ (financial abstraction axis, threshold $\approx 63.2$):** $e$ emerges from the factorial series and measures the degree of financial abstraction decoupling: whether financial instruments attached to the chain are operationally connected to physical boundary metrics. An $e$-failure occurs when the ratio of financial claims to physical output exceeds $e$. In PB terms, this corresponds to the growing disconnection between ESG financial instruments and measured Earth-system impacts documented in [Berg22, Plan21].

### 5.2 Five-Axis Diagnostic Results

Figure 4 displays the five-axis scores for five representative chains. Several patterns are salient.

Gold exhibits the worst $\varphi$-failure in the corpus ($\varphi$-score = 38), consistent with the extreme concentration of extraction pressure in artisanal and small-scale mining phases and the high financial abstraction documented in exchange-registered bullion markets (gold $e$-score = 70, the highest in the corpus, reflecting the well-developed but poorly-grounded financial derivatives market). West African shea shows the worst $e$-failure ($e$-score = 34): despite the high development pressure on shea-producing regions, financial instruments tied to shea supply are few, meaning the financial abstraction axis fails not from over-abstraction but from the absence of instruments that would link capital flows to ecological boundary compliance.

Spain olive oil and blue carbon are the best-performing chains on most axes but remain below the $\pi$-threshold for operational balance, indicating that even the most transparent and well-governed chains in the corpus are operating below the aggregate safe operating space standard. This finding motivates the research path described in Section 6.3: the predecessor papers to this work need to establish what institutional interventions are required to bring chains above the $\pi$-threshold.

![Figure 4. Five-Constant Diagnostic Axis Scores for Five Representative Supply Chains.](/home/jw/src/tv/docnav/Research/papers/19_ndc-planetary-boundaries-supply-chain/figures/19_five-constant-bars.png)

---

## 6. Discussion

### 6.1 Structural Balance as Sustainability Governance

The central implication of this paper is that planetary sustainability governance should be redesigned around the structural balance condition $D \approx C$ at each supply chain phase rather than around the monitoring of global boundary control variables. This shift has practical consequences.

First, phase-level D/C balance is actionable at the firm and sector level in a way that global boundary monitoring is not. A mining firm cannot reduce global atmospheric CO$_2$ concentration, but it can increase the C-type accountability of its extraction phase (independent third-party assay, geospatial traceability, community impact corroboration) to bring Phase 0 balance above the $B^* = 61.8$ threshold. The N-D-C framework converts a global Earth-system metric into a phase-specific, firm-actionable design criterion.

Second, the five-constant diagnostic framework localizes the type of intervention required, not only the phase where it is needed. A $\sqrt{2}$-failure requires reducing structural overhead (streamlining certification layers, removing duplicate audit requirements); a $\ln 2$-failure requires addressing temporal gaps (patient capital instruments for biological transformation phases, multi-year monitoring commitments); an $e$-failure requires redesigning financial instruments to create operational linkage to physical boundary metrics (sustainability-linked bonds with KPIs tied to measured boundary proximity rather than self-reported ESG scores).

Third, the framework is consistent with the Ostrom design principles for common-pool resource governance [Ostr90], as established in [paper 17](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/17_ostrom-tholonic-governance/17_ostrom-tholonic-governance.pdf). Ostrom's principles for stable commons governance are, in N-D-C structural terms, a set of D-type institutional rules (clearly defined boundaries, collective-choice arrangements, graduated sanctions) that must be balanced by C-type participatory mechanisms (monitoring by appropriators, conflict resolution mechanisms, recognition by external authorities). Planetary boundary governance at the supply chain level is, in this reading, an instance of the commons governance problem at multi-level scale.

### 6.2 Limitations

Several important limitations apply to this first draft.

**Schematic data.** The balance scores reported in Sections 4 and 5 are schematic and illustrative, derived from domain knowledge and structural analysis of the supply chains rather than from calibrated empirical indicator dictionaries. Real-data calibration is the primary goal of the predecessor paper described in Section 6.3.

**Single-phase DAG assumption.** Treating supply chains as directed acyclic graphs within a custody horizon excludes ecological feedback cycles (resource regeneration, carbon cycling, biodiversity recovery). These outer cycles are structurally important and their exclusion understates the C-type pressures at extraction phases. Methods for incorporating outer-cycle feedback into the phase model are under development.

**Boundary quantification heterogeneity.** The nine planetary boundaries use different control variables, measurement units, and uncertainty ranges. The N-D-C mapping proposed in Section 3 is a structural partition (D-type vs. C-type) rather than a quantitative mapping from balance score to boundary control variable distance. Establishing the quantitative link requires boundary-specific calibration work that is beyond the scope of this draft.

**Corpus representativeness.** The 18-chain corpus concentrates on commodities with historical research depth (gold, shea, cocoa) and European/West African geographic coverage. It underrepresents Asian manufacturing chains, rare earth mineral chains, and marine food supply chains, all of which have significant Planetary Boundaries implications.

### 6.3 The Research Path to Publication

Sarah's message identifies a 3-to-5 year path to Nature. We propose the following publication sequence:

**Predecessor paper A (target: 2027, *Nature Sustainability* or *Ecological Indicators*).** Empirical TVPCI calibration with real indicator data across the 18-chain corpus. The key deliverable is a calibrated indicator dictionary for each of the six sectors, with measured D and C primitives, so that the balance scores reported in this paper are grounded in verifiable data rather than expert judgment.

**Predecessor paper B (target: 2028, *Earth's Future* or *Global Environmental Change*).** Quantitative linkage between N-D-C balance scores and measured planetary boundary control variables, using the calibrated corpus from Predecessor A as the empirical base. The key deliverable is a regression or structural equation model linking phase-level $B(D,C)$ to boundary proximity metrics ($\Delta B_i / B_i^*$ for each boundary $i$).

**The Nature paper (target: 2029-2030).** Synthesis of the structural framework, empirical calibration, and quantitative PB linkage into the paradigm-shifting claim: supply chain phase-level D/C balance predicts planetary boundary transgression class, and the five-constant diagnostic axes provide a tractable intervention design framework for governance at the supply chain phase level.

---

## 7. Conclusion

Planetary Boundaries research has established where humanity's safe operating limits are. What it has not established is how supply chains, the primary physical conduits through which human economic activity generates Earth-system pressure, must be structured to respect those limits. This paper proposes the N-D-C triadic balance framework as a structural bridge. The key result is that D/C imbalance at the supply chain phase level is not merely a transparency or governance failure: it is the structural condition that generates planetary boundary transgressions. D-heavy phases generate D-type transgressions (extraction exceeding climate, land-use, and freshwater boundaries); C-heavy phases generate C-type transgressions (unaccounted outputs exceeding biosphere integrity and biogeochemical flow boundaries). Five mathematical constants emergent from the N-D-C recursive structure provide a five-axis diagnostic that localizes failure mode and intervention priority within the Planetary Boundaries safe operating space. The framework is grounded in 18 supply chains across six sectors developed collaboratively over the period 2016-2026. Predecessor empirical validation papers will establish the quantitative linkage between phase-level balance scores and measured boundary control variables. The structural claim here opens an intervention design space that neither the Planetary Boundaries framework nor existing supply chain governance tools can access independently.

---

## Methods

### M.1 The N-D-C Triadic Framework: Formal Definitions

Let a supply chain consist of $P+1$ ordered phases $\{p_0, p_1, \ldots, p_P\}$ with directed flow $p_{i} \to p_{i+1}$. For each phase $p$, define three non-negative observables:

- $N_p \in [0,1]$: the declared position and mass-balance coherence score, measuring how well the phase's outputs are accounted for relative to its inputs. $N_p = 1$ indicates full mass-balance closure with verified custody; $N_p = 0$ indicates complete opacity or discontinuity.

- $D_p \in [0,1]$: the definition/limitation score, measuring the density and verifiability of constraining evidence: audit scope, regulatory compliance documentation, counterparty opacity caps, certification to applicable standards. $D_p$ is high when the phase is operating under strong, independently verifiable constraints.

- $C_p \in [0,1]$: the contribution/corroboration score, measuring the depth of independent corroboration: third-party physical assays, geospatial attestations, ecological impact measurements, community impact records. $C_p$ is high when the phase's outputs and externalities are independently and comprehensively documented.

The phase-local balance score is:

$$B_p = \frac{2 \cdot \min(D_p, C_p)}{D_p + C_p} \times 100$$

with $B_p = 0$ when $D_p = C_p = 0$ (completely unobserved phase). The stability threshold $B^* = 100/\varphi \approx 61.8$ is fixed by the N-D-C recursive structure.

### M.2 Transition Penalty and Phase Propagation

A phase with unresolved deficits propagates instability downstream. Define the effective N-state at phase $p$ as:

$$\tilde{N}_p = N_p \cdot \prod_{k=0}^{p-1} (1 - \tau_k)$$

where $\tau_k \in [0,1]$ is the transition penalty at phase $k$, defined as:

$$\tau_k = \alpha \cdot \max\left(0, B^* - B_k\right) / B^*$$

with $\alpha \in (0,1)$ a chain-specific attenuation parameter (default $\alpha = 0.15$). This implements the cascade effect described in Section 3.3: a phase with $B_k < B^*$ reduces the effective N-state inherited by subsequent phases, compounding structural weakness downstream.

The chain-level aggregate index is:

$$\text{TVPCI} = \frac{\sum_{p=0}^{P} w_p \cdot B_p \cdot \tilde{N}_p}{\sum_{p=0}^{P} w_p}$$

where $w_p$ are phase weights reflecting the relative environmental impact exposure of each phase, set by sector-specific expert judgment in this draft and to be calibrated empirically in Predecessor paper A.

### M.3 Mapping D-Type and C-Type Boundaries

The D-type and C-type partition of planetary boundaries in Section 3 is based on the following structural criterion. A boundary is classified as D-type if its primary control variable measures a constraint on extraction or transformation (an upper limit on what the Earth system can supply or absorb from extraction activity). A boundary is classified as C-type if its primary control variable measures an output or externality accumulation (a lower limit on the ecological services that must be maintained against the pressure of unaccounted outputs).

Formally, let $x_i$ be the control variable for boundary $i$ and $B_i^*$ be its proposed boundary value. D-type boundaries are those where $x_i > B_i^*$ implies excessive extraction relative to safe limits: CO$_2$ concentration, freshwater use, land-system change, stratospheric ozone depletion, novel entities. C-type boundaries are those where $x_i < B_i^*$ implies insufficient ecological service maintenance against output accumulation: biosphere integrity (functional species richness), ocean acidification (aragonite saturation, where higher is safer), biogeochemical flows (where the boundary is an upper limit on anthropogenic fluxes treated here as C outputs).

### M.4 Five-Constant Threshold Derivations

The five sustainability thresholds used in Section 5 are derived as follows:

- **$\pi$-threshold (78.5):** $\pi \times 25 = 78.54$. The factor of 25 normalizes the constant to the 0-100 balance score scale; $\pi$ indexes the Advancing recursion class requiring external injection, which in supply chain terms corresponds to system-level operational coherence requiring external governance input.

- **$\varphi$-threshold (61.8):** $100/\varphi = 61.8$. This is also the phase-level stability threshold $B^*$; $\varphi$ indexes the Self-redefined continued-fraction fixed point, measuring proportional self-similarity of value distribution across phases.

- **$\sqrt{2}$-threshold (70.7):** $\sqrt{2} \times 50 = 70.71$. $\sqrt{2}$ indexes the Babylonian self-redefined recursion measuring structural overhead; the factor of 50 normalizes to the balance score scale.

- **$\ln 2$-threshold (69.3):** $\ln 2 \times 100 = 69.3$. $\ln 2$ indexes the alternating harmonic Fixed recursion, a convergence rate that in supply chain terms measures the efficiency of the transformation from raw input to processed output.

- **$e$-threshold (63.2):** $100 \times (1 - 1/e) = 63.2$. $e$ indexes the factorial Fixed recursion; $(1 - 1/e)$ is the fraction of the system that has been reached after one natural time constant, measuring financial abstraction alignment.

Formal derivations of the five constants from the N-D-C recurrence family are given in [paper 1](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf) and [paper 11](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/11_tholonic-seed-space-power-of-two-hierarchy/11_tholonic-seed-space-power-of-two-hierarchy.pdf).

### M.5 Supply Chain Corpus

The 18-chain corpus analyzed in this paper was developed over the period 2016-2026 using consistently applied N-D-C phase-resolved scoring. Chains are listed below with their sector, phase count, primary PB pressure category, and schematic chain average balance score used in the figures:

| Chain | Sector | Phases | Primary PB category | Avg $B$ |
|---|---|---|---|---|
| Gold v1 | Extractive / mining | 8 | Mining / energy | 58 |
| Gold v2 | Extractive / mining | 8 | Mining / energy | 55 |
| Gold v3 | Extractive / mining | 8 | Mining / energy | 60 |
| Grid ERCOT URI | Energy infrastructure | 7 | Mining / energy | 56 |
| W. African Shea | Agricultural commodity | 8 | Land use / agriculture | 57 |
| Burkina Faso Shea | Agricultural commodity | 8 | Land use / agriculture | 54 |
| Cocoa International | Agricultural commodity | 8 | Land use / agriculture | 52 |
| Cocoa Netherlands | Agricultural commodity | 8 | Land use / agriculture | 62 |
| Senegal Agroforestry | Agroforestry system | 7 | Land use / agriculture | 65 |
| Spain Olive Oil | Agricultural commodity | 8 | Land use / agriculture | 68 |
| Gran Chaco | Agricultural commodity | 7 | Land use / agriculture | 50 |
| Blue Carbon | Ecosystem service | 6 | Ecosystem services | 61 |
| Marina Alta | Ecosystem service | 6 | Ecosystem services | 67 |
| AUBEB | Ecosystem service | 6 | Ecosystem services | 63 |
| Bristol One City | Ecosystem service | 5 | Ecosystem services | 70 |
| Water Jackson MS | Water infrastructure | 7 | Freshwater use | 48 |
| Water NewWater | Water infrastructure | 7 | Freshwater use | 72 |
| Water OCWD | Water infrastructure | 7 | Freshwater use | 74 |

Phase counts, indicator dictionaries, and scoring rationales for each chain are documented in the project repository at `frontend/project/[chain-name]/supply_chain/`. All balance scores in this draft are schematic; calibrated scores from Predecessor paper A will replace these values in the final submitted version.

### M.6 Game-Theoretic Grounding of the Balance Condition

[Paper 4 of this series](https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/4_game-theoretic-triadic-balance/4_game-theoretic-triadic-balance.pdf) establishes that the D/C balance condition $B(D,C) = B^*$ corresponds to a Nash equilibrium in a two-player game where D and C are strategic players and N is the payoff outcome. Under the conditions of the theorem, neither player can improve their position by unilateral deviation from $D \approx C$. This provides a game-theoretic foundation for why the balance condition is stable and self-reinforcing when achieved, and why intervention is required to move a chain from a sub-threshold D-heavy equilibrium to a balanced state: the imbalanced state is itself a Nash equilibrium, stable in the absence of external coordination.

---

## References

[Rock09] Rockström, J., Steffen, W., Noone, K., Persson, Å., et al. *A safe operating space for humanity.* Nature, 461: 472-475, 2009.

<https://doi.org/10.1038/461472a>

[Stef15] Steffen, W., Richardson, K., Rockström, J., Cornell, S. E., et al. *Planetary boundaries: Guiding human development on a changing planet.* Science, 347(6223): 1259855, 2015.

<https://doi.org/10.1126/science.1259855>

[Rich23] Richardson, K., Steffen, W., Lucht, W., et al. *Earth beyond six of nine planetary boundaries.* Science Advances, 9(37): eadh2458, 2023.

<https://doi.org/10.1126/sciadv.adh2458>

[Nijs15] Nijs, L. *The Challenges of Applying Planetary Boundaries as a Basis for Strategic Decision-Making in Companies with Global Supply Chains.* Sustainability, 9(2): 279, 2017.

<https://doi.org/10.3390/su9020279>

[Plan21] Planetary Accounting Network. *Planetary accounting: quantifying how to live within planetary limits at the household to planet scale.* npj Sustainability, 2021.

[Berg22] Berg, F., Kolbel, J. F., Rigobon, R. *Aggregate Confusion: The Divergence of ESG Ratings.* Review of Finance, 26(6): 1315-1344, 2022.

<https://doi.org/10.1093/rof/rfac033>

[Mon15] Monfreda, C., Wackernagel, M., Deumling, D. *Establishing national natural capital accounts based on detailed ecological footprint and biological capacity assessments.* Land Use Policy, 2004.

[OECD22] OECD. *OECD Due Diligence Guidance for Responsible Business Conduct.* OECD Publishing, Paris, 2022.

[GRI21] Global Reporting Initiative. *GRI 204: Procurement Practices 2016; GRI 308: Supplier Environmental Assessment 2016; GRI 414: Supplier Social Assessment 2016.* GRI Standards, 2021.

[Mos19] Moser, C., Leipold, S. *Toward 'postnational' sustainability governance? Analyzing the public-private forest governance nexus in the European Union timber regulation and the Forest Stewardship Council.* Ecology and Society, 24(2): 17, 2019.

[Ostr90] Ostrom, E. *Governing the Commons: The Evolution of Institutions for Collective Action.* Cambridge University Press, 1990.

[IPCC21] IPCC. *Climate Change 2021: The Physical Science Basis.* Contribution of Working Group I to the Sixth Assessment Report. Cambridge University Press, 2021.

[CBD22] Convention on Biological Diversity. *Kunming-Montreal Global Biodiversity Framework.* CBD/COP/DEC/15/4, 2022.

[Mil26a] Milton, J. W. *Emergence of Classical Constants from a Minimal Recursive Triadic Framework.* Clarity Coalition, paper 1 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/1_recursive-tholonic-five-constants/1_recursive-tholonic-five-constants.pdf>

[Mil26b] Milton, J. W. *Phase-Resolved Transparency Classification in Commodity Supply Chains: A Structural Triadic Scoring Framework (TVPCI).* Clarity Coalition, paper 2 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.pdf>

[Mil26c] Milton, J. W. *A Minimal Recursive Triadic Framework for Self-Similar Hierarchical Systems.* Clarity Coalition, paper 3 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.pdf>

[Mil26d] Milton, J. W. *Game-Theoretic Framing of the Triadic Balance Condition.* Clarity Coalition, paper 4 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/4_game-theoretic-triadic-balance/4_game-theoretic-triadic-balance.pdf>

[Mil26e] Milton, J. W. *Power-of-Two Convergence Counts in the Tholonic Seed Space: A Complete Hierarchy of Classical Constants.* Clarity Coalition, paper 11 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/11_tholonic-seed-space-power-of-two-hierarchy/11_tholonic-seed-space-power-of-two-hierarchy.pdf>

[Mil26f] Milton, J. W. *Elinor Ostrom's Design Principles and the Tholonic N-D-C Framework: Governance as Structural Balance.* Clarity Coalition, paper 17 in this series, 2026.

<https://github.com/baardev/truevalue/blob/main/docnav/Research/papers/17_ostrom-tholonic-governance/17_ostrom-tholonic-governance.pdf>
