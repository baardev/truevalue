---
doc_id: lighter_quickstart
title: Lighter Supply Chain — Project Quickstart
type: documentation
status: active
domain: lighter_supply_chain
layer: supply_chain
projects:
  - lighter
tags:
  - lighter
  - quickstart
  - supply_chain
  - tvpci
related_docs:
  - LIGHTER_SUPPLY_CHAIN_PHASE_INSTANCE.md
key_claims:
  - 10 billion lighter units produced per year; approximately 90% from China (Wenzhou cluster)
  - Factory gate FOB price is $0.10-$0.15 for generic unbranded units
  - BIC Classic retails at $1.49 vs $0.89 for generic; brand premium is $0.60 (67%)
  - The brand premium is the only meaningful E-layer decoupling in the entire supply chain (coupling ratio 0.60)
  - Lighter disposal is near-zero recycling; approximately 50,000 MT of PP plastic waste per year
---

# Lighter Supply Chain — Project Quickstart

## What This Project Analyzes

The disposable plastic lighter is one of the most price-compressed manufactured goods on Earth. A single lighter contains 30+ precision-engineered components, holds pressurized butane at high internal pressure, must pass strict ISO 9994 and EN 13869 safety tests, and is packed into a container and shipped 10,000+ miles across the Pacific Ocean — all at a factory gate cost of $0.10-$0.15.

This project models the complete supply chain from raw material extraction (butane, polypropylene resin, ferrocerium, steel) through to retail sale, using the TVPCI (True Value Pricing Convergence Index) framework and the Tholonic N-D-C model. The primary analytical finding is that in a commodity this extreme, the only available rent is at the brand abstraction layer: the BIC name is worth $0.60 per unit, and nothing else in the chain has meaningful E-layer decoupling.

The Wenzhou/Zhejiang manufacturing cluster is also the canonical example of micro-margin optimization: wall thickness reduced by fractions of a millimeter; container packing density maximized to fit thousands of additional units per shipment; mold redesign to save $0.0001 per unit. No competitor outside this cluster can survive on these margins.

## Key Supply Chain Phases (8 phases, IDs 0-7)

| Phase | Name | Transparency | Key Finding |
|---|---|---|---|
| 0 | Raw Material Extraction | Medium | China is a net LPG importer; butane feedstock price is NYMEX-driven |
| 1 | Component Manufacturing | Low | 3,000 Wenzhou factories; 30+ parts at $0.04 total piece-part cost |
| 2 | Lighter Assembly | Low | 400 units/worker/hour; butane fill 4g; FOB $0.10-$0.15 |
| 3 | QA Testing & Certification | Medium | ISO 9994 + EN 13869 mandatory; ~21-day test cycle; $2,500/SKU |
| 4 | Packaging & Containerization | Medium | 2,000,000 units per 40ft FEU; $3,200 ocean freight per FEU |
| 5 | Ocean Freight & Import | High | UN Comtrade HS 9613 data public; $0.15 declared value per unit |
| 6 | Wholesale Distribution | Medium | 22% distributor margin (NACS); $0.45 wholesale generic price |
| 7 | Retail | High | $0.89 generic; $1.49 BIC; 38% retail margin; E-layer finding here |

Chain average balance: 81.9%. Bottleneck phases: 1 (70.0%) and 2 (72.0%).

## Key Data Sources

### Primary Public Sources

1. **World LPG Association (WLPGA) Annual Report 2023** — global LPG/butane production volumes (Phase 0)
   URL: https://www.wlpga.org

2. **CME Group NYMEX** — butane/propane spot and futures prices (Phase 0, E-layer)
   URL: https://www.cmegroup.com

3. **ICIS Polyolefins Price Report** — PP resin spot price (Phase 0)
   URL: https://www.icis.com

4. **China National Bureau of Statistics (NBS)** — Zhejiang minimum wage; light industry employment (Phases 1, 2)
   URL: https://www.stats.gov.cn

5. **China Lighter Industry Association (CLCA)** — factory count; industry output; technical specifications (Phases 1, 2)
   URL: https://www.clca.org.cn

6. **ISO 9994:2005/2024** — lighter safety requirements and test methods (Phase 3)
   URL: https://www.iso.org/standard/39985.html

7. **EN 13869:2016** — child-resistance requirements for lighters (Phase 3)
   URL: https://www.cen.eu

8. **Drewry World Container Index** — container freight rates Shanghai to LA/Rotterdam (Phase 4, 5)
   URL: https://www.drewry.co.uk

9. **Freightos Baltic Index (FBX)** — container freight rates (Phase 4, 5)
   URL: https://www.freightos.com

10. **UN Comtrade HS 9613** — import/export volumes and declared values by country (Phase 5)
    URL: https://comtrade.un.org

11. **US CBP HTS 9613.10** — US import duty rate (3.9% MFN) for lighters (Phase 5)
    URL: https://hts.usitc.gov

12. **NACS State of the Industry Report 2023** — distributor and retail margins in convenience channel (Phases 6, 7)
    URL: https://www.nacsonline.com

13. **BIC Group Annual Report 2023** — BIC unit sales; revenue; brand pricing (Phases 7, E-layer)
    URL: https://www.bic-group.com/investors

### Inferred and Estimated Sources

- **Alibaba / Global Sources OEM listings**: FOB price range for generic lighters (inferred)
- **Panjiva / ImportGenius**: shipper-level US customs manifests (subscription; public underlying data)
- **SGS / Bureau Veritas / TUV**: certification lab fee schedules (estimated)
- **Fastmarkets minor metals**: ferrocerium pricing (estimated from cerium oxide market)
- **Product dimension calculation**: units-per-container derived from lighter dimensions and FEU cubic capacity

## Key E-Layer Findings

The E-model (financial abstraction layer) analysis identifies five claim types in the lighter supply chain:

| Phase | Claim Type | Coupling Ratio | Status |
|---|---|---|---|
| 0 | LPG commodity futures | 0.90 | Well-coupled |
| 0 | PP resin forwards | 0.85 | Well-coupled |
| 2 | OEM purchase orders vs production | 0.85 | Well-coupled; order cancellation risk |
| 5 | Letters of credit | 0.95 | Well-coupled |
| 6 | Retailer sourcing agreements vs sell-through | 0.70 | Moderate decoupling |
| 7 | BIC brand premium claim | 0.60 | **SIGNIFICANT DECOUPLING** |

**Primary E-layer finding:** The BIC brand premium ($0.60/unit) is the only meaningful abstract value in this supply chain. The physical product (BIC Classic vs generic OEM) is functionally identical — same ISO 9994 compliance, same butane fill, same ferrocerium flint, same ignition reliability. The entire $0.60 premium is brand abstraction. This is the TVPCI story for lighters: in a supply chain compressed to the physical and economic limit, the only rent available is the brand claim at the consumer endpoint.

## Key Sustainability Findings

The lifecycle analysis (5 phases) identifies disposal as the critical failure:

- **Near-zero recycling rate:** >99% of 10 billion annual units go to landfill
- **Plastic waste:** approximately 50,000 MT of PP polymer per year (non-recyclable as mixed waste)
- **Butane venting:** approximately 40,000 MT/year from incompletely exhausted units at disposal
- **No take-back program** exists at scale from any major lighter manufacturer
- **Lifecycle bottleneck phase:** Phase 4 (Disposal and Circularity), balance score 62.0% — the weakest phase in the system
- **Sustainability index for disposal:** 0.05 (severe failure mode)

The Tholonic model confirms: the lighter is optimized for production efficiency (Phase 1-2 D-C optimization) at the complete expense of lifecycle circularity (Phase 4 D-C collapse). This is a systemic design choice, not a regulatory gap.

## TVPCI Relevance

The lighter supply chain is the canonical TVPCI example of a commodity at the physical and economic limit. The key TVPCI observations are:

1. **Manufacturing efficiency compression:** The Wenzhou cluster has reduced manufacturing cost to below the theoretical minimum for a Western-economy producer. This is not cheap labor; it is micro-optimization of every variable simultaneously.

2. **Price convergence:** The generic lighter factory gate price ($0.12 FOB) represents near-total convergence between cost and price. There is no margin left in the physical supply chain except at the brand abstraction layer.

3. **Brand as the only rent:** The TVPCI convergence score for the physical supply chain is extremely high (phases are price-cost converged). The only divergence is the BIC brand premium, which is a pure pricing power abstraction with no physical basis.

4. **Lifecycle penalty:** The TVPCI framework's sustainability dimension flags the disposal phase as a systemic failure. The true value of a lighter, accounting for environmental externalities (plastic waste, butane emissions), is significantly negative at end of life. This cost is not internalized in the retail price.
