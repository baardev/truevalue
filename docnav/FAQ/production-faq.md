# Production FAQ: The Physical Supply Chain

This document answers questions about how the Tholonic N-D-C framework applies to the physical supply chain: what phases are, how material moves and changes state from its geological origin to its final registered form, what custody means at each step, why some phases are opaque, and how structural health is diagnosed at the phase level.

> **Note on examples:** The gold supply chain is used as the worked example throughout this FAQ. Gold is the primary reference chain in this project: it has eight well-defined phases, spans high-transparency and low-transparency segments, involves multiple custody transfers, and terminates at a highly transparent exchange registration point (COMEX). All structural principles described here apply equally to other material supply chains (shea butter, cocoa, mangroves, water, and others modelled in this project), with phase names and physical states substituted accordingly.

For background on N, D, and C themselves, see the [Model FAQ](docnav/FAQ/tholonic-faq.md). For how financial instruments interact with the physical chain, see the [Finance FAQ](docnav/FAQ/finance-faq.md).

---

## The Phase Structure

### What is a supply chain phase, and why does the model insist on phases?

A phase is a discrete segment of the supply chain defined by a specific physical state of the material, a specific transformation that changes that state, and a specific custodian who is responsible for the material during that segment. A phase is not a business activity, a company type, or a reporting category. It is a physically bounded segment of the chain.

The model insists on phases for a structural reason: you cannot measure D and C for a system without first bounding the system. D (Definition) is everything that constrains and defines what the entity must be. C (Contribution) is everything the entity produces and passes forward. Both of those measurements require a defined boundary. Without a phase boundary, you cannot say what the constraints apply to or what the outputs are. You have a narrative, not a measurement.

The second reason is diagnostic. Supply chain problems rarely affect the whole chain uniformly. A structural failure in aggregation does not look the same as a structural failure in refining. Phase-level analysis locates the failure. Chain-level aggregation hides it. The model requires phases because healing a system requires knowing which part of it is sick.

---

### How many phases does the gold supply chain have?

The gold supply chain as modelled here has eight phases, numbered 0 through 7.

| Phase | Name | Physical state of gold | Transparency |
|---|---|---|---|
| 0 | Geological Occurrence and Prospecting | In situ (unextracted) | Medium |
| 1 | Mine Extraction | Run-of-mine ore | High |
| 2 | Ore Processing and Concentration | Concentrate | High |
| 3 | Doré Production | Doré bars | Medium |
| 4 | Refining | Fine gold (999.9 purity) | Medium |
| 5 | Bar Casting and Assay | Standard bullion bars | Medium-High |
| 6 | Logistics and Vaulting | Bullion in storage | Low |
| 7 | Exchange Registration | Deliverable bullion (COMEX-registered) | High |

Phase 0 is a pre-supply phase: gold exists in the ground and has not yet entered the chain as a commercial entity. Phases 1 and 2 are upstream. Phases 3, 4, and 5 are midstream transformation phases. Phases 6 and 7 are downstream custody and formalisation phases.

---

### What determines where one phase ends and the next begins?

A phase boundary is marked by two simultaneous events: a change in the physical state of the material (it is transformed into something chemically or physically different) and a change in custody (a different entity becomes responsible for it).

These two events usually coincide but do not always. When a mine smelts its own doré on site, the physical transformation (Phase 2 to Phase 3) happens without a custody change. When bullion is moved between vaults by the same custodian, custody changes without a physical transformation. The tholonic model treats the most restrictive of the two criteria as the phase boundary: a new phase begins when either condition changes. This produces the clearest possible boundaries for D and C measurement.

The practical significance: when the physical transformation and custody transfer are separated in time or location, a structural gap opens between phases. That gap is a region of opacity, because neither the sending nor the receiving custodian has full visibility of what the material is doing during the gap. Identifying those gaps is one of the primary outputs of phase-level analysis.

---

### What is Phase 0, and why is it counted as a phase at all?

Phase 0 is the geological and prospecting phase: gold in the ground that has been identified by exploration but not yet extracted. It is counted as a phase because it has measurable D constraints (geological grade thresholds that make extraction commercially viable, regulatory requirements for exploration licences, environmental impact assessment requirements, social licence conditions with affected communities) and measurable C outputs (resource estimates, reserve classifications, geological data that informs extraction planning).

The N state of Phase 0 is a prospectively viable deposit: a geological body that meets the grade and volume criteria to support a mine. When D and C are in balance, the deposit can proceed to extraction. When D is excessive (exploration licence costs are prohibitive, land access requirements are unresolvable, grade thresholds cannot be met), the phase N never instantiates and the deposit remains stranded.

Phase 0 matters for the full chain analysis because stranded deposits are the upstream failure mode that reduces Phase 1 supply. A chain analysis that begins at the mine gate misses the structural conditions that determine how much gold enters the chain at all.

---

## Physical States and Transformations

### What is run-of-mine ore, and what does it mean for Phase 1?

Run-of-mine ore is the raw material extracted from the mine before any processing. It is a mixture of gold-bearing rock and waste material, with gold content measured in grams per tonne (the ore grade). Phase 1 ends when this material leaves the mine and enters the processing circuit.

In D-C terms, Phase 1's D is defined by: the minimum ore grade that makes extraction viable, the safety regulations governing underground or open-pit operations, the energy and water inputs required for extraction, equipment maintenance and replacement specifications, environmental management obligations (tailings, dust, water discharge), and the workforce requirements for legal mining operations.

Phase 1's C is: run-of-mine ore delivered to the processing facility, with an associated composition profile specifying gold grade, penalty element concentrations, and moisture content. The custody handoff is the weighbridge receipt and assay certificate at the processing plant gate.

Phase 1 is characterised by high transparency because the mine's production volumes, ore grades, and operational parameters are reported to regulators and, for listed miners, to capital markets. This makes Phase 1 one of the best-documented phases in the chain.

---

### What happens in Phase 2 (ore processing and concentration), and why is it significant?

Phase 2 transforms run-of-mine ore into a concentrate: a material with much higher gold content per tonne achieved by removing most of the waste rock through physical and chemical separation. Common processes include flotation (using chemical reagents to cause gold-bearing minerals to attach to air bubbles), gravity concentration (exploiting density differences), and cyanide leaching (dissolving gold into a solution for subsequent recovery).

Phase 2 is structurally significant because it is where the first major D-C tension appears in the chain. The D side of Phase 2 is dominated by environmental and chemical management requirements: cyanide is acutely toxic, tailings must be contained, water management is critical, and regulatory compliance is intensive. These are legitimate and necessary constraints. But they grow independently of the gold price or production volume. A small-scale or artisanal operation faces essentially the same regulatory D-load as a large industrial operation, which means the D-C ratio worsens dramatically as scale decreases. This structural disadvantage for small-scale miners is the Phase 2 expression of a chain-wide equity problem.

---

### What is doré, and why does Phase 3 create an opacity gap?

Doré is an intermediate alloy produced by smelting the concentrate. It is typically 60-90% gold with silver and trace impurities, cast into bars for transport to a refinery. The transformation from concentrate to doré (Phase 3) happens at the mine site or at a centralised smelting facility.

Phase 3 creates an opacity gap for a structural reason. When doré is produced at the mine and transported to a refinery, it travels between two parties under a commercial contract that specifies the agreed gold content. But the actual gold content is only definitively measured at the refinery, after the doré is melted and assayed. During transport, the doré is a sealed container of uncertain value. The shipper's assay and the refinery's assay may differ. Resolving the difference requires a referee assay, which introduces delay and cost.

This gap is not fraud or malice. It is an unavoidable consequence of the physical chemistry: gold cannot be non-destructively assayed at high precision without melting and sampling the entire bar. The opacity is structural. It is the tholonic basis for the medium transparency rating of Phase 3.

---

### What is the significance of Phase 4 (refining)?

Refining transforms doré into fine gold: 999.9% purity (four nines), the international standard for deliverable bullion. The transformation uses chemical processes (chlorination or electrolytic refining) that are capital-intensive and require specialised facilities. There are only a small number of LBMA-accredited refineries globally.

Phase 4 is the most concentrated point of control in the entire gold supply chain. The small number of accredited refineries means that the vast majority of the world's mined gold passes through a handful of facilities to achieve deliverable purity. This concentration has two structural consequences.

First, the refineries hold enormous negotiating power over the doré producers (miners). The refining charge, the loss allowance, and the settlement timing are all determined by the refiner, and small miners have limited ability to negotiate. This is a phi ($\phi$) problem: value is being captured disproportionately at the Phase 4 transition.

Second, the concentration creates a structural opacity point. The LBMA accreditation system requires refineries to maintain responsible sourcing standards, but the actual gold flows through refineries are not publicly reported at the bar or batch level. What enters as doré from multiple sources exits as interchangeable fine gold with a new identity. The provenance link between mine and bar is broken at Phase 4, which is why chain-of-custody tracking programmes struggle structurally: the physical chemistry of refining erases identity by design.

---

### What is bar casting and assay (Phase 5), and why is it the registration anchor?

Phase 5 transforms fine gold into standard bullion bars: typically 400 troy ounce (12.4 kg) good delivery bars conforming to LBMA specifications, or 100 troy ounce kilobars. Each bar is assayed, weighed, stamped with a serial number and the refinery's hallmark, and issued an assay certificate. This is the first point in the chain where an individual bar has a unique, permanent, legally attested identity.

Phase 5 is the registration anchor in the tholonic model because it is where the material transitions from a fungible commodity (fine gold, interchangeable with any other fine gold of the same purity) to a discrete, identified object (a bar with a serial number, a known weight, a known purity, and a custody record). The assay certificate is the D-defining document for the bar's entire downstream life.

For the tholonic chain, Phase 5 is the highest-confidence measurement point: bar weights and purities are certified, serial numbers are recorded, and LBMA good delivery standards are well-defined and enforced. Phase 5 is the point where what was in the ground can, for the first time, be definitively and individually accounted for.

---

### Why is Phase 6 (logistics and vaulting) the lowest-transparency phase?

Phase 6 covers the movement of bullion from the refinery to storage vaults and the ongoing custody of bullion in those vaults. It is rated low transparency because almost all of it happens under commercial confidentiality.

Vault operators (central banks, commercial banks, private vaulting companies) do not disclose how much gold they hold, whose gold it is, or where the bars are physically located. This is not a regulatory failure. It is a deliberate structural feature of the vaulting business: confidentiality about holdings is the product. A vault that disclosed its clients' gold holdings would have no clients.

From the tholonic perspective, Phase 6 is a structural opacity point, not an ethical one. The opacity is produced by the custody structure: the entity with the information (the vault operator) has a commercial obligation to withhold it from everyone except the legal owner, and the legal owner is typically a financial institution that has its own reasons for non-disclosure. The D side of Phase 6 (custody agreements, security infrastructure, insurance requirements, regulatory reporting to central banks in aggregate) is well-documented. The C side (what moves, to whom, when) is almost entirely opaque to external analysis.

This is the tholonic framework's definition of a structural opacity: not hidden because of bad intent, but hidden because the custody structure that makes the phase function also makes its flows invisible.

---

### What is Phase 7 (exchange registration), and why is it used as the analytical anchor?

Phase 7 is the registration of bullion bars with an exchange (primarily COMEX in New York or the LBMA in London) as deliverable against futures contracts. A bar must pass a quality check, be held in an approved depository, and be formally registered in the exchange's warrant system before it can be delivered against a contract.

Phase 7 is used as the analytical anchor in the tholonic model because it is the highest-transparency downstream point in the chain. Exchange inventories are publicly reported daily (eligible and registered inventories for COMEX, vault holdings by depository). The bars are physically present in named, regulated, inspected depositories. The ownership is legally formalised through the warrant system. The quantity is independently verified.

The important caveat is that Phase 7 transparency is narrow. COMEX inventories cover only the gold that has been formally registered with the exchange, which is a small fraction of total above-ground gold. The high transparency of Phase 7 does not extend upstream: it tells us what is at the exchange, not what is in vaults, not what is in transit, and not what is in jewellery or central bank reserves. Phase 7 is an anchor, not a total count.

---

## Custody and Control

### What is custody, and how is it different from ownership?

Custody is physical possession and practical control of the material. Ownership is a legal claim to the material that may or may not coincide with custody. Control is the ability to legally mobilise (sell, lend, pledge, or transfer) the material.

The tholonic model requires that every phase analysis specify all three, because they can and do separate in the gold supply chain.

A mine produces gold and retains custody until it ships doré to the refinery. At that point custody transfers to the shipper or the refiner, but ownership may remain with the mine (if it is a toll-refining arrangement) or transfer to the refinery (if it is a purchase arrangement). A central bank may own gold bars that are physically stored in a foreign central bank's vault and legally mobilised through a lease to a commercial bank. In that case the owner, the custodian, and the entity with current control are three different institutions.

The separation of ownership, custody, and control is why the tholonic model uses "custody" as the primary chain descriptor rather than ownership or title. What matters for phase analysis is who has the physical material and what can be done with it, not who has a legal claim to it on a balance sheet somewhere.

---

### What does a custody handoff look like at a phase boundary?

A custody handoff is a discrete event: a specific moment when responsibility for the material passes from one entity to another. It is documented by a delivery note, an assay certificate, a weighbridge receipt, a bill of lading, or a vault receipt, depending on the phase.

In the tholonic model, the custody handoff is the C output of one phase and the D input of the next. The handing phase produces the material in its defined state with its defined documentation. The receiving phase accepts it under those specifications and takes on the D obligations of managing it going forward.

The quality of the custody handoff determines the quality of the phase boundary. A handoff with complete documentation (assay certificate, weight, serial numbers, provenance declaration, chain-of-custody form) is a high-quality boundary: the next phase can accurately characterise its D. A handoff with incomplete documentation is a low-quality boundary: the receiving phase must work with uncertainty, which adds D (verification costs, dispute resolution, conservative management) without adding C.

Poor-quality handoffs are the primary source of structural friction at phase transitions. They are a $\sqrt{2}$ signal: D is rising (more overhead to manage the uncertainty) without C rising (the material itself has not changed). Improving handoff documentation quality is a structural intervention, not an operational one, because it changes the D-C ratio at the boundary rather than improving performance within a phase.

---

### What is rehypothecation, and is it part of the supply chain model?

Rehypothecation is the practice of using an asset that has been pledged as collateral as collateral again for a second, separate obligation. In gold markets, this means that the same physical bar may underlie multiple simultaneous financial claims: an owner pledges it to a bank, which pledges it to another bank, which uses it as backing for a financial product sold to retail investors.

Rehypothecation is explicitly outside the scope of the supply chain layer of the tholonic model. The hardcoded rules for this project state that financial abstraction (paper claims, leverage) is deferred until the physical chain is fully mapped. Rehypothecation is a financial abstraction: it does not change the physical state, location, or custody of the bar. The bar is still in the vault. What multiplies is the number of financial claims written against it.

The supply chain model maps the bar. The financial model maps the claims. Mixing them produces a confused model where the same physical unit is counted multiple times. The tholonic separation of layers prevents this.

What the supply chain model does record: at Phase 6, opacity is structural, and one structural reason for that opacity is that custodians cannot disclose holdings without revealing information about the financial claims their clients have written against those holdings. The rehypothecation structure is a cause of Phase 6 opacity even though it is not itself within the supply chain scope.

---

## Transparency and Opacity

### What does "opacity" mean in the tholonic model?

Opacity means that the C output of a phase (what the phase produces and passes forward) cannot be measured or verified by external observers. The phase exists and has a D side (constraints, requirements, regulatory obligations that are sometimes public) but its C side (what actually moves, in what quantity, to whom, when) is not observable.

Opacity is classified by degree: high transparency (C is publicly measurable), medium transparency (C is measurable with access to industry data or regulatory filings), low transparency (C is not measurable without direct access to the custodian's records).

The critical point is that opacity is a structural description, not a moral judgment. The tholonic model does not attribute opacity to bad actors or concealment. It attributes opacity to the custody structure of the phase. When the structural conditions that make a phase function also prevent its C from being observed, opacity is an unavoidable property of that phase design. The appropriate response is to document the structural reason for the opacity, not to assert that someone is hiding something.

---

### Which phases are opaque and why?

| Phase | Transparency | Structural reason for opacity level |
|---|---|---|
| 0 | Medium | Exploration data is commercially sensitive; geological resource estimates are disclosed for listed companies but not for private operators or artisanal prospecting |
| 1 | High | Mine production is reported to regulators and capital markets; physical access enables independent verification |
| 2 | High | Processing outputs (concentrate grades, volumes) are reported in offtake contracts and regulatory filings |
| 3 | Medium | Doré composition is known to shipper and refiner but not publicly reported; transport routing is confidential for security reasons |
| 4 | Medium | Refinery inputs and outputs are not publicly disclosed; LBMA accreditation requires internal traceability but not public reporting |
| 5 | Medium-High | Bar serial numbers and assay certificates exist; LBMA good delivery bars are identifiable, but their subsequent movement is not |
| 6 | Low | Vault holdings are commercially confidential; aggregate central bank holdings are reported annually but without bar-level detail or precise timing |
| 7 | High | Exchange inventories are published daily; depository and warrant records are legally formalised |

Phase 6 is the structural opacity gap in the gold chain. It sits between the Phase 5 high-quality registration point and the Phase 7 exchange anchor. Bars enter the vault system with documented identities and re-emerge at the exchange, but what happens between those two events is invisible.

---

### Why is opacity a "finding, not a failure"?

The phrase comes from the project's analytical discipline: opacity is a data condition, not an accusation. Calling a phase opaque means the analyst cannot measure its C outputs with available data. It does not mean the phase is dysfunctional, corrupt, or concealing wrongdoing.

If the analyst treated opacity as a failure, the chain analysis would bias toward blaming the custodians with the most confidential operations. But those custodians (commercial vaults, central banks, private refineries) are often the most professionally managed parts of the chain. Their opacity is a feature of their business model, not a symptom of dysfunction.

Opacity becomes diagnostically useful when it is combined with custody analysis. If a phase is opaque and also has weak or ambiguous custody documentation (the handoffs from that phase lack the assay certificates, serial numbers, or delivery notes that other phases produce), that combination is a structural concern. The opacity plus weak handoffs means that material could move through that phase without a traceable record. That is a data gap the tholonic model marks as a structural finding and recommends for further investigation when evidence-based remediation is possible.

The phrase "opacity is a finding, not a failure" enforces analytical discipline: report what can be measured, mark what cannot, explain why, and do not speculate beyond the evidence.

---

## Phase Health and Propagation

### What does the B-score measure at the phase level?

The B-score (Balance score) is the primary measure of phase health. It expresses the D-C balance of a phase as a percentage: a score of 100 means D and C are exactly equal. A score above 80 indicates healthy operation. A score in the 61.8-80 range indicates the phase is coherent but under stress. A score below 61.8% (the coherence threshold, derived from the inverse of the golden ratio) indicates a phase in structural failure: the D-C imbalance has crossed the point where the phase can self-correct without external intervention.

The 61.8% threshold is not arbitrary. In the tholonic framework, 61.8% is $1/\phi$ (the reciprocal of the golden ratio). At this point, the ratio of D to C has reached the golden ratio itself: D is exactly $\phi$ times larger than C. This is the unique mathematical point at which the D-C relationship breaks self-similarity: below this threshold, the proportional relationship that characterises a healthy phase has irreversibly broken down.

A phase below the coherence threshold is still operating: miners still dig, processors still crush ore, refineries still smelt doré. But the structural health is degraded, and the phase is operating under conditions that will deteriorate further unless an intervention changes the D-C balance.

---

### How does a failure in one phase propagate to adjacent phases?

Phases are connected by custody handoffs. The C output of one phase is the material input to the next. When a phase's C falls (it produces less, produces worse-quality material, or produces material with incomplete documentation), the receiving phase faces an immediate D-C problem: it must now work harder to manage reduced or degraded inputs, adding D to its own operations without the expected C arriving.

This propagation follows two directions. Downstream propagation is the more obvious: a mining strike (Phase 1 C falls) reduces concentrate supply to Phase 2, which reduces doré to Phase 3, which reduces refinery throughput at Phase 4. The reduction in supply cascades forward through the chain.

Upstream propagation is less obvious but equally important: when a downstream phase changes its requirements (the refinery increases its quality specifications, the exchange changes its good delivery standards), it adds D to every upstream phase that must now comply with those new requirements. This D-addition propagates backward up the chain.

The tholonic model captures both directions. A change in Phase 4 refining specifications sends a new D-wave upstream to Phase 3 (doré composition requirements change), Phase 2 (concentrate must now meet different penalty element limits), and Phase 1 (ore types with high penalty element concentrations become unviable). The supply chain is not just a sequence of independent phases; it is a network of bidirectional D-C relationships.

---

### What does "D-heavy" mean at the phase level, and what causes it?

A D-heavy phase is one where the D side of the D-C balance has grown faster than the C side, pushing the B-score below the optimal range. D can grow for several reasons.

**Regulatory accumulation.** Each new compliance requirement adds D. Requirements generally do not reduce when conditions change. Over time, phases in heavily regulated industries accumulate D without corresponding C growth. This is the $\sqrt{2}$ (structural friction) signal.

**Degraded inputs.** When a phase receives lower-quality inputs from the previous phase (ore at lower grades, concentrate with higher impurity levels, doré with anomalous composition), the receiving phase must spend more on characterisation, quality control, and process adjustment. These are D-additions: they constrain what the phase can do without contributing to output.

**Seasonal or supply constraints.** Agricultural and natural resource chains often have C that is seasonally limited while D (infrastructure, licensing, staffing, regulatory compliance) remains constant year-round. During the off-season, the phase is D-heavy not because D has grown but because C has fallen. This is a $\ln 2$ (Transformation Efficiency) signal.

**Capital rationing.** A phase that cannot invest in maintenance or equipment replacement sees its C capacity erode while D (operating requirements, safety standards, contractual obligations) remains fixed. This is a slow D-heaviness that develops over multiple reporting cycles and is often invisible until equipment failure or workforce degradation makes it acute.

---

### What is the difference between a phase-level problem and a chain-level problem?

A phase-level problem is one whose root cause lies within a single phase: its specific D constraints are excessive, its C outputs are inadequate, or its handoff quality is poor. The intervention targets that phase's specific D or C conditions.

A chain-level problem is one where the root cause is in the relationship between phases: a custody gap between two adjacent phases, a D-wave propagating backward from a downstream phase, or a phi ($\phi$) imbalance where value is being captured at one phase at the expense of the phases doing the most structural work. The intervention targets the relationship, not a single phase.

The practical distinction matters for investment and policy. Funding a new processing facility (Phase 2 C-activation) does not fix a chain-level value distribution problem where Phase 2's margins are structurally suppressed by Phase 4's negotiating power. The phase-level intervention improves Phase 2's local B-score, but the chain-level phi score remains poor because the value captured by Phase 2 still does not reflect its structural contribution. Both interventions may be needed, but they address different levels of the hierarchy.

---

### What does COMEX registered inventory tell us, and what does it not tell us?

COMEX registered inventory is the quantity of gold bars that have been formally presented to the exchange, passed a quality inspection, been placed in an approved depository, and had a warrant issued against them. The warrant is a legal document entitling the holder to take delivery of a specific bar. Registered inventory is the gold that can actually be delivered against a futures contract.

What COMEX data tells us: the daily quantity of gold in specific depositories that meets LBMA good delivery standards and is available for delivery. The aggregate eligible inventory (bars meeting quality standards but not yet warranted) is also published. This is the highest-resolution publicly available data on gold at a specific point in the physical supply chain.

What COMEX data does not tell us: the provenance of the bars (which mine, which refinery, which country of origin), the ownership chain (the bar may have changed hands multiple times since being warranted), the relationship between registered inventory and total above-ground gold (COMEX holds a small fraction of global bullion), or the state of Phases 3-6 that produced and transported the bar before it arrived.

The tholonic model uses COMEX as the Phase 7 anchor: it is the most reliable downstream measurement point. But anchoring at Phase 7 does not retroactively illuminate the opaque phases above it. It confirms arrival; it does not trace the journey.

---

*Source of truth: the project `.cursorrules`, the supply chain phase schema at `frontend/project/gold/data/schema/supply_chain_phases.csv`, and the N-D-C framework documentation. For the five analytical dimensions applied to production phases, see [Five Dimensions: Plain Labels](docnav/FAQ/five-dimensions-plain-labels.md).*
