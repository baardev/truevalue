# TVPCI

## Definition

The True Value Pricing Convergence Index: a phase-resolved, triadic scoring framework that measures how structurally coherent a commodity supply chain is, using five irreducible mathematical constants ($\varphi$, $e$, $\ln 2$, $\sqrt{2}$, $\pi/4$) as benchmarks. Each chain phase receives $(N_p, D_p, C_p)$ scores, and the aggregate TVPCI measures how close the chain operates to its structural ideal.

## Extended model: TVPCI-R and B_chain

The forward custody chain (TVPCI) is complemented by a parallel recycling observable $R_p$ defined at each phase, measuring how visible and managed the waste outputs and ecological return flows of each phase are. Aggregated as $\text{TVPCI-R}$ (using waste-intensity weights $\omega_p$ rather than phase-position weights), it is combined with TVPCI into a chain-level balance score:

$$B_\text{chain} = 100 \cdot \exp\!\left(-2 \cdot \frac{|\text{TVPCI} - \text{TVPCI-R}|}{\max(\text{TVPCI},\,\text{TVPCI-R})}\right)$$

Tholonic role assignment: TVPCI = D (forward definition), TVPCI-R = C (ecological return contribution), $B_\text{chain}$ = N (emergent chain-parent balance).

Recycling is not modeled as a Phase 8 in the forward chain. It is a parallel structure that closes the $\pi/4$ equilibrium cycle without disrupting the DAG property of the primary chain.

## Why It Matters

TVPCI belongs to the methodology and value-chain interpretation layer, not to raw physical supply-chain mapping. TVPCI-R extends the model into ecological accountability.

## Related Documents

- [[tvpci_explained_math]]
- [[tvpci_specification]]
- [[tvpci_foundation]]

## Related Claims

- five_constants_provide_coherence_reference_points
- pricing_convergence_can_be_evaluated_against_tholonic_balance
- recycling_modeled_as_parallel_R_p_not_phase_8
