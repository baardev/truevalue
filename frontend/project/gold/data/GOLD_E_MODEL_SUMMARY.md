# Gold E-Model Claims Register
## Abstract Layer Decoupling Analysis — All Phases

**Reference date:** 2024
**Gold price reference:** ~$2,000/oz (2023 average)
**Source file:** schema/gold_e_model_claims.csv

---

### What This File Measures

The e-model (D=1, C=1) measures how cleanly each phase of the gold supply chain
participates in the financial and systemic whole. The core metric is the coupling ratio:

    coupling_ratio = physical_value_usd / abstract_value_usd

A ratio of 1.0 means abstract claims are fully backed by physical reality.
A ratio of 0.133 means only 13 cents of physical gold backs every $1 of paper claim.

E-score = min(100, coupling_ratio × 100). OPAQUE entries use analyst midpoint estimates.

---

### Phase-by-Phase Summary

| Phase | Phase Name              | Claim Type            | Coupling | E-Score | Rehypothecated |
|-------|-------------------------|-----------------------|----------|---------|----------------|
| 0     | Prospecting             | none                  | 1.00     | 100     | No             |
| 1     | Mine Extraction         | streaming_agreement   | 0.90     | 90      | No             |
| 1     | Mine Extraction         | royalty_interest      | 0.95     | 95      | No             |
| 1     | Mine Extraction         | forward_sales_hedge   | 1.00     | 100     | No             |
| 2     | Ore Processing          | none                  | 1.00     | 100     | No             |
| 3     | Doré Production         | none                  | 1.00     | 100     | No             |
| 4     | Refining                | metal_lease           | 0.40     | 40      | YES            |
| 4     | Refining                | loco_swap             | 0.95     | 95      | No             |
| 5     | Bar Casting & Assay     | none                  | 1.00     | 100     | No             |
| 6     | Logistics & Vaulting    | allocated_position    | 1.00     | 100     | No             |
| 6     | Logistics & Vaulting    | unallocated_position  | OPAQUE   | 5*      | YES            |
| 6     | Logistics & Vaulting    | etf_share             | 0.98     | 98      | No             |
| 7     | Exchange Registration   | futures_contract      | 0.133    | 13      | Structural     |
| 8     | Recycling & Recovery    | none                  | 1.00     | 100     | No             |

*OPAQUE — analyst estimate range 0.01–0.10, midpoint 0.05 used. Actual value unknown.

---

### Key Findings

**1. The upstream chain (Phases 0–3, 5, 8) is fully e-coherent.**
No abstract claims layer operates on ore, concentrate, doré, or scrap.
Physical transformation phases are not decoupled.

**2. Phase 4 (Refining) — first significant decoupling point.**
Gold leasing: 5,000–8,000 tonnes of gold (estimated $418B) is simultaneously
claimed as an asset by central banks AND as working capital by bullion banks.
The same physical gold backs 2–3 claims simultaneously.
Estimated coupling ratio: 0.40. E-score: 40.

**3. Phase 6 (Vaulting) — bifurcated: allocated is healthy, unallocated is the primary failure.**
- Allocated gold: 1:1 physically backed. E-score: 100.
- ETF gold: audited, segregated, ~0.98 coupling. E-score: 98.
- Unallocated LBMA positions: THE PRIMARY OPACITY. Not publicly disclosed.
  Analyst estimates: 50–100 units of paper claims per 1 unit of physical gold.
  Coupling ratio: 0.01–0.10 (OPAQUE). E-score: 5 (estimated).

**4. Phase 7 (Exchange/COMEX) — structurally decoupled by design.**
COMEX registered inventory ~6M oz. Open interest ~45M oz equivalent.
Coupling ratio: 0.133. E-score: 13.
This is disclosed and by design — the exchange functions as a price discovery
and hedging mechanism, not primarily as a physical delivery system.
~98% of contracts are cash-settled or rolled without delivery.

---

### Abstract Value Totals (Estimated, 2024, gold at ~$2,000/oz)

| Claim Type               | Physical Value | Abstract Value | Coupling |
|--------------------------|----------------|----------------|----------|
| Streaming agreements     | $225B/yr       | ~$11B/yr       | 0.90     |
| Royalty interests        | $225B/yr       | ~$4.5B/yr      | 0.95     |
| Forward sales hedges     | $6.4B          | $6.4B          | 1.00     |
| Metal leases             | $418B          | $418B+         | 0.40*    |
| ETF holdings             | $180B          | $180B          | 0.98     |
| Unallocated positions    | OPAQUE         | OPAQUE         | OPAQUE   |
| COMEX futures            | $12B           | $90B           | 0.133    |

*Coupling of 0.40 reflects rehypothecation — same gold backing 2–3 claims.

**Quantifiable abstract claims (excl. unallocated OPAQUE layer):**
~$580B in abstract claims against ~$210B in identifiable physical value.
Implied system-wide coupling (excl. unallocated): ~0.36

**Including estimated unallocated layer:**
If LBMA unallocated adds ~$500B–$1T in additional paper claims (analyst estimates),
total abstract claims reach $1.1–1.6T against physical registered gold of ~$15–20B
at the exchange/vault layer. System-wide e-layer coupling: 0.01–0.02.

---

### Data Gaps and OPAQUE Flags

The following fields remain structurally opaque and cannot be sourced from public data:

1. **LBMA unallocated positions (aggregate)** — no regulator collects or publishes this.
   The Bank of England publishes total gold held in its vaults but not the
   unallocated/allocated breakdown for all institutions. This is the most
   significant information gap in the entire gold supply chain e-layer.

2. **Central bank gold lending (individual institution detail)** — IMF/BIS/WGC
   publish aggregate estimates but individual central bank lending positions
   are not publicly disclosed. The Bank of England acknowledges gold lending
   as a service but does not publish volumes.

3. **Bullion bank proprietary positions** — HSBC, JPMorgan, UBS and others are
   not required to separately report their gold lending or unallocated positions
   beyond standard bank capital reporting.

These gaps are not data collection failures. They are structural features of the
market architecture. Documenting them as OPAQUE is the correct analytical response
per project Rule Set 4: opacity is a finding, not a failure.

---

### Sources

| Source | Type | Coverage |
|--------|------|----------|
| COMEX Daily Warehouse Reports | Public, free, daily | Phase 7: registered/eligible inventory |
| CFTC Commitment of Traders Report | Public, free, weekly | Phase 7: open interest by category |
| World Gold Council ETF Tracker | Public, free, monthly | Phase 6: ETF holdings |
| World Gold Council Gold Demand Trends | Public, annual | Phase 4: leasing estimates |
| GLD Prospectus (SEC filing) | Public | Phase 6: ETF structure/custodian |
| IAU Prospectus (SEC filing) | Public | Phase 6: ETF structure/custodian |
| LBMA Account Documentation | Public | Phase 6: allocated/unallocated definitions |
| Jeffrey Christian CFTC Testimony, March 2010 | Public record | Phase 6: paper/physical ratio estimate |
| BIS OTC Derivatives Statistics | Public, semi-annual | Phase 4/6/7: derivatives volumes |
| IMF Article IV Consultations | Public, annual | Phase 4: central bank gold lending |
| Company 10-K Filings (Newmont, Barrick, etc.) | Public, annual | Phase 1: streaming/royalty/hedging |
| Franco-Nevada 2023 Annual Report | Public | Phase 1: streaming counterparty |
| Wheaton Precious Metals 2023 Annual Report | Public | Phase 1: streaming counterparty |

---

*Generated for the Gold Supply Chain Intelligence Project — e-model layer*
*This file should be updated when COMEX/CFTC/WGC figures are refreshed (monthly/quarterly)*
