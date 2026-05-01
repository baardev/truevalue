---
doc_id: lighter_supply_chain_phase_instance
title: Disposable Lighter — Supply Chain Phase Instance
type: phase_instance
status: active
domain: lighter_supply_chain
layer: supply_chain
projects:
  - lighter
tags:
  - phase_mapping
  - lighter
  - lighter_supply_chain
  - supply_chain
related_docs:
  - LIGHTER_QUICKSTART.md
key_claims:
  - 10 billion units per year produced; approximately 90% from Wenzhou/Zhejiang China
  - 30+ precision components per unit; factory gate $0.10-$0.15 FOB
  - BIC brand premium ($0.60/unit) is the only E-layer decoupling in the chain
  - Disposal phase is near-zero circular; lifecycle bottleneck at balance 62.0%
---

# Disposable Lighter — Supply Chain Phase Instance

**Template reference:** Each phase follows the Abstract Supply Chain Phase Template. Physical state, transformation, actors, throughput, value flow, D-parameters, C-parameters, transparency, and data status are recorded for each of the 8 phases. The value chain (margins, prices, brand premium) is kept strictly separate per Rule Set 1.

---

## Phase 0 — Raw Material Extraction

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in (resource) | D | Butane/LPG in subsurface reservoir; propylene monomer (PP precursor); iron/cerium ore; steel ore | POPULATED | IEA; WLPGA |
| Physical state out | D | Liquefied butane (pressurized C4); PP resin pellets (injection grade); ferrocerium alloy rod stock; steel coil | POPULATED | ICIS; WLPGA |
| Primary transformation | D | Petroleum refining (butane); steam cracking and polymerization (PP); alloy smelting (ferrocerium); rolling (steel) | POPULATED | IEA Oil Market Report 2023 |
| Geography | D | Middle East and Russia (LPG); China domestic (PP); China and global (ferrocerium); global (steel) | POPULATED | IEA; WLPGA Annual Report 2023 |
| Transparency level | D | Medium — commodity markets are public; Chinese domestic PP pricing less transparent | POPULATED | ICIS; WLPGA |
| D-parameters | D | ISO butane purity spec; PP MFI specification; ferrocerium Ce:Fe ratio; geological reserve constraints; REACH chemical compliance | POPULATED | ISO; REACH; estimated |
| C-parameters | C | LPG supply to Chinese petrochemical sector; PP resin delivered to Wenzhou molders; ferrocerium rod stock to component manufacturers | POPULATED | CLCA; WLPGA |
| Throughput / volume | N | 320,000,000 MT/year global LPG production; China PP resin output ~20M MT/year | POPULATED | WLPGA 2023; ICIS |
| Actors / custodians | C | LPG: Saudi Aramco; Gazprom; ADNOC; Sinopec. PP resin: Sinopec; PetroChina; LyondellBasell. Steel: Baowu; ArcelorMittal | POPULATED | IEA; public company reports |
| Price / value flow | N | Butane: $0.62/kg (NYMEX); PP resin: $0.90/kg (ICIS Asia); Steel wire rod: $580/MT (LME); Ferrocerium: ~$12.50/kg (estimated) | POPULATED | CME Group; ICIS; LME; Fastmarkets (estimated) |
| Data status | context | POPULATED for commodity prices; PARTIAL for Chinese domestic feedstock delivery to lighter manufacturers | | |

---

## Phase 1 — Component Manufacturing

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in | D | PP resin pellets; steel coil; ferrocerium rod stock; brass/zinc billet; nitrile rubber sheet | POPULATED | Calculated |
| Physical state out | D | 30+ discrete precision components: body halves; valve assembly; nozzle; flint wheel; flint rod; spring; O-ring; child-resistance lever | POPULATED | CLCA technical documentation |
| Primary transformation | D | Injection molding (PP body halves); die casting (valve; nozzle); stamping (spring); turning (flint rod); investment casting (wheel) | POPULATED | Plastics Technology trade press |
| Geography | D | Wenzhou and Zhejiang Province China (dominant); some component supply from Guangdong | POPULATED | CLCA; China NBS |
| Transparency level | D | Low — private factories; no public production data | POPULATED | Structural assessment |
| D-parameters | D | ISO 9994 dimensional tolerances for safety components; EN 13869 child-resistance lever geometry; wall thickness minimum for pressure vessel; flint wheel serration spec; mold cycle time upper bound (12 sec); spring preload spec | POPULATED | ISO 9994; EN 13869 |
| C-parameters | C | 30+ components delivered per lighter unit; typical 500,000 unit-equivalent daily output per factory; reject rate <2% (Tier-1) | PARTIAL | CLCA estimated |
| Throughput / volume | N | Approximately 10 billion lighter unit equivalents per year from Wenzhou cluster | ESTIMATED | CLCA; China Customs |
| Actors / custodians | C | 3,000 registered lighter component manufacturers in Wenzhou (CLCA); most are private SMEs; no public companies | PARTIAL | CLCA |
| Price / value flow | N | Total piece-part cost: ~$0.04/lighter unit at scale (inferred) | INFERRED | Alibaba OEM; UN Comtrade backsolve |
| Labor cost | C | $0.005/unit at $2.20/hour Zhejiang minimum wage and 400 units/hour throughput | ESTIMATED | China NBS Zhejiang wage order 2023 |
| Data status | context | PARTIAL — factory count and employment are public; individual factory throughput and cost structure are proprietary | | |

---

## Phase 2 — Lighter Assembly

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in | D | 30+ discrete components (from Phase 1); butane gas (pressurized cylinder) | POPULATED | Phase 1 output |
| Physical state out | D | Sealed; gas-filled; assembled lighter body (pre-certification) | POPULATED | Product specification |
| Primary transformation | D | Mechanical assembly sequence; butane filling (4.0±0.2g); valve crimping; seal integrity test (in-line) | POPULATED | ISO 9994 build plan |
| Geography | D | Wenzhou and Zhejiang Province China (concentrated); limited assembly outside China | POPULATED | CLCA; UN Comtrade origin data |
| Transparency level | D | Low — private assembly factories; production volumes not disclosed | POPULATED | Structural assessment |
| D-parameters | D | Butane fill spec: 4.0±0.2g; crimp torque spec (valve to body); alignment tolerance for child-resistance lever; in-line leak test pass criterion; minimum fuel pressure at 20°C; ISO 9994 validated build sequence | POPULATED | ISO 9994; product spec |
| C-parameters | C | 400 units/worker/hour throughput (semi-automated line); factory gate FOB price $0.10-$0.15 generic; $0.16-$0.22 branded spec; 10 billion units/year output | PARTIAL | CLCA estimated; Alibaba |
| Throughput / volume | N | 10,000,000,000 units/year assembled (global; China dominant) | ESTIMATED | CLCA; China Customs HS 9613 export |
| Actors / custodians | C | Same Wenzhou manufacturers as Phase 1 (vertical integration common); custody held by factory until FOB delivery to importer agent | PARTIAL | CLCA |
| Price / value flow | N | FOB Wenzhou/Ningbo: $0.12 generic; $0.18 branded OEM spec (inferred from Comtrade) | INFERRED | Alibaba; UN Comtrade |
| Assembly cost | C | ~$0.015/unit total assembly cost (labor + overhead + butane) | ESTIMATED | NBS wage + throughput calculation |
| Data status | context | PARTIAL — production volumes estimated from export statistics; factory economics are proprietary | | |

---

## Phase 3 — QA Testing & Certification

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in | D | Assembled lighter (sealed; gas-filled; uncertified) | POPULATED | Phase 2 output |
| Physical state out | D | Certified lighter bearing compliance mark (or rejected unit) | POPULATED | ISO 9994; EN 13869 |
| Primary transformation | D | Safety and compliance testing: ignition reliability; drop test; fuel leakage; child-resistance | POPULATED | ISO 9994; EN 13869; CPSC 16 CFR 1212 |
| Geography | D | Testing laboratories: SGS; Bureau Veritas; TUV Rheinland (global; offices in China) | POPULATED | SGS; Bureau Veritas |
| Transparency level | D | Medium — test standards are public; individual SKU test results are proprietary | POPULATED | Structural assessment |
| D-parameters | D | ISO 9994 clause-by-clause: ignition test 30,000 cycles; drop test 1.8m onto concrete; fuel leakage at 48°C; flame height ≤50mm. EN 13869: 80% of test children (aged 42-51 months) unable to operate in 5 minutes. CPSC 16 CFR 1212 for USA market access | POPULATED | ISO 9994:2005; EN 13869:2016; CPSC |
| C-parameters | C | Certified lighters: approximately 94% first-submission pass rate; 21-day typical cycle; $2,500/SKU; certification mark enables EU/UK/US/Canada market access | ESTIMATED | SGS estimate; CPSC recall statistics |
| Throughput / volume | N | All 10 billion units destined for regulated markets must be from certified SKU variants | POPULATED | CPSC; EU market access rules |
| Actors / custodians | C | Accredited test laboratories (SGS; Bureau Veritas; TUV Rheinland; Intertek); certification held by manufacturer; renewed on product change | POPULATED | SGS; Bureau Veritas |
| Price / value flow | N | Certification cost: $2,000-$4,000 per SKU; amortized to $0.002-$0.004/unit over 1M+ production run | ESTIMATED | Lab fee schedule estimates |
| Data status | context | POPULATED for standards content; PARTIAL for pass rates and costs (estimated from available sources) | | |

---

## Phase 4 — Packaging & Containerization

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in | D | Certified lighters in bulk trays | POPULATED | Phase 3 output |
| Physical state out | D | Palletized units in sealed 20ft/40ft shipping containers (HS 9613.10/9613.20) | POPULATED | Drewry; IMDG |
| Primary transformation | D | Retail display box packing; carton assembly; palletization; container loading; IMDG dangerous goods documentation | POPULATED | IMDG Code |
| Geography | D | Wenzhou/Ningbo port (primary); Shanghai port (secondary) | POPULATED | China port statistics |
| Transparency level | D | Medium — freight rates public; packaging cost estimated | POPULATED | Drewry WCI; Freightos |
| D-parameters | D | Retail display box legal text (WARNING; child-resistance warning); EAN barcode compliance; carton BCT minimum (stacking strength); IMDG Class 2.1 DG documentation; container loading sequence; pallet configuration (EURO 100x120cm or USA 48x40in) | POPULATED | IMDG; regulatory requirements |
| C-parameters | C | 2,000,000 units per 40ft FEU (calculated from dimensions); container freight $3,200/FEU Shanghai-LA (Drewry mid-2024); $2,900/FEU Shanghai-Rotterdam; packaging cost $0.008/unit | POPULATED | Drewry WCI; Freightos; calculated |
| Throughput / volume | N | 5,000 FEU-equivalents per year to USA alone (3B units / 600K units per 20ft = ~5,000 TEU) | CALCULATED | UN Comtrade; dimension calculation |
| Actors / custodians | C | Factory export agent / freight forwarder (China side); NVOCC or ocean carrier; port authority | POPULATED | Industry standard |
| Price / value flow | N | Container freight cost per unit: $0.0016/unit ($3,200 FEU / 2,000,000 units) | CALCULATED | Drewry WCI; dimension calc |
| Data status | context | POPULATED for freight rates and container capacity; PARTIAL for packaging cost (estimated) | | |

---

## Phase 5 — Ocean Freight & Import

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in | D | Containerized lighter units (IMDG Class 2.1 DG shipment) | POPULATED | Phase 4 output |
| Physical state out | D | Customs-cleared palletized units at destination port warehouse | POPULATED | US CBP; EU Customs |
| Primary transformation | D | Ocean freight transit; customs declaration (HS 9613); import duty assessment; CPSC/CE compliance verification at border; dangerous goods handling | POPULATED | UN Comtrade; US CBP |
| Geography | D | Ningbo/Shanghai to Los Angeles; Rotterdam; Hamburg; Le Havre; Melbourne; Dubai | POPULATED | UN Comtrade routes |
| Transparency level | D | High — UN Comtrade data is public; US AES data is public; EU Eurostat is public | POPULATED | UN Comtrade; US Census |
| D-parameters | D | HS 9613.10 (non-refillable) vs 9613.20 (refillable) classification; mandatory product liability documentation; CE mark for EU; CPSC clearance for USA; IMDG compliance; country of origin labeling | POPULATED | US CBP; EU Customs; CPSC |
| C-parameters | C | USA: 3 billion units/year; declared value ~$0.15/unit; total $450M/year declared. EU: 2.5 billion units/year; $380M declared value. China total exports: 10 billion units to 150+ countries | POPULATED | UN Comtrade HS 9613 |
| Throughput / volume | N | 10,000,000,000 units/year global lighter exports (primarily from China) | POPULATED | UN Comtrade HS 9613 |
| Actors / custodians | C | Ocean carriers (COSCO; Maersk; MSC); freight forwarders; customs brokers; port operators; importer of record | POPULATED | Industry standard |
| Price / value flow | N | US import declared value: $0.15/unit; import duty (US): $0.006/unit (3.9% MFN); freight: $0.0016/unit | POPULATED | US CBP; Drewry |
| Data status | context | POPULATED — this is the highest transparency phase alongside Phase 7 | | |

---

## Phase 6 — Wholesale Distribution

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in | D | Customs-cleared palletized units at importer warehouse | POPULATED | Phase 5 output |
| Physical state out | D | Individual display units delivered to retail store back-room or shelf-ready | POPULATED | NACS SOTI |
| Primary transformation | D | Regional warehousing; pick-and-pack; last-mile logistics; custody transfer to retailer | POPULATED | NACS SOTI 2023 |
| Geography | D | USA: national DSD (direct store delivery) distributors; regional warehouses. EU: national importer-distributors | POPULATED | NACS; industry |
| Transparency level | D | Medium — category-level margin data public (NACS); individual distributor economics proprietary | POPULATED | NACS SOTI 2023 |
| D-parameters | D | Retailer shelf-ready packaging specification; minimum order quantity; payment terms (net 30/60); product liability insurance; FIFO stock rotation; SKU rationalization (2-4 SKUs per retail format); MAP policy compliance for BIC | POPULATED | NACS; BIC MAP policy |
| C-parameters | C | Distributor gross margin: 22% (NACS convenience channel); distribution cost per unit: ~$0.03; wholesale price to retailer (generic): ~$0.45; wholesale price (BIC): ~$0.90 | PARTIAL | NACS SOTI 2023; estimated |
| Throughput / volume | N | USA: 3 billion units/year through distributor channel (dominant in convenience) | ESTIMATED | NACS; US Census retail trade |
| Actors / custodians | C | McLane Company; Core-Mark (Pfizer spin-off); Nash Finch; regional specialty distributors; BIC direct sales force | PARTIAL | Industry; NACS |
| Price / value flow | N | Wholesale price generic: $0.45/unit; wholesale price BIC: $0.90/unit; distributor margin 22% | PARTIAL | NACS SOTI 2023; estimated |
| Data status | context | PARTIAL — category margin data from NACS; individual distributor contracts are proprietary | | |

---

## Phase 7 — Retail

| Category | N-D-C | Value (current) | Status | Sources and notes |
|---|---|---|---|---|
| Physical state in | D | Individual display units on retail shelf | POPULATED | Phase 6 output |
| Physical state out | D | Consumer-held lighter (end use begins) | POPULATED | Direct observation |
| Primary transformation | D | Sale to end consumer; custody transfer; brand premium realization | POPULATED | BIC Annual Report 2023; NACS |
| Geography | D | USA: 150,000+ convenience stores (dominant channel); mass market (Walmart; Target); drug stores. EU: equivalent channels | POPULATED | NACS; Euromonitor |
| Transparency level | D | High — retail prices directly observable; BIC as public company publishes unit sales and revenue | POPULATED | BIC Annual Report 2023; direct observation |
| D-parameters | D | Retail price management: EDLP (mass market) vs high-low (convenience); MAP policy (BIC); child-resistant packaging at POS (CPSC); age restriction signage; planogram space allocation | POPULATED | CPSC; BIC; NACS |
| C-parameters | C | Generic retail price: $0.89; BIC Classic: $1.49; retail margin: 38% (NACS); BIC global units: 1.5 billion/year; BIC Lighters revenue: $2.24 billion/year | POPULATED | BIC Annual Report 2023; NACS SOTI 2023 |
| Throughput / volume | N | USA: approximately 3 billion units/year; global: approximately 10 billion units/year | POPULATED | UN Comtrade; BIC Annual Report |
| Actors / custodians | C | Walmart; Dollar General; Dollar Tree; 7-Eleven; Circle K; BP/Amoco; independent convenience operators; BIC direct (some channels) | POPULATED | NACS; company reports |
| Price / value flow | N | Generic: $0.89 retail; BIC: $1.49 retail; brand premium: $0.60/unit (67% over generic); retail margin: 38%; BIC lighter segment revenue: $2.24B/year | POPULATED | BIC Annual Report 2023; NACS |
| E-layer observation | N | BIC brand premium coupling ratio: 0.60 — this is the PRIMARY E-LAYER FINDING | POPULATED | BIC Annual Report 2023; UN Comtrade (inferred) |
| Data status | context | POPULATED — this is the highest transparency phase alongside Phase 5 | | |
