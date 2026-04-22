# Shea Butter — Supply Chain Phase Instance

**Template reference:** This instance follows the [Abstract Supply Chain Phase Template](../Repos/intra/PDI/ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE.md). Each category is filled with current project data where we have it, marked **MISSING** where we do not, with example metrics for measurement. **Value chain** (income, prices, margins): [Shea value chain instance](../Repos/intra/PDI/SHEA_VALUE_CHAIN_PHASE_INSTANCE.md).

*Mapping:* Shea phase 0 ≈ Abstract 0+1 (origin + harvest); Shea 1–2 ≈ Abstract 2 (aggregation + trading); Shea 3 ≈ Abstract 3; Shea 4 ≈ Abstract 6 (logistics/export); Shea 5 ≈ Abstract 4 (manufacturing); Shea 6 ≈ Abstract 7 (retail). Abstract 5 (certification) and 8 (circular) have no dedicated shea phase; marked N/A or MISSING.

---

## Shea Phase 0 — Collection (Origin + primary extraction)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state (resource in situ) | D | Whole fruit (nuts) in shea belt | POPULATED | e.g. description; nut grade if defined |
| Location / geography | D | Burkina Faso, West Africa; Senegal (Thies, Fatick, Diourbel) | POPULATED | e.g. countries; regions; km² or ha shea belt |
| Identification / boundary | D | Shea belt; harvest area | PARTIAL | e.g. map reference; harvest zone boundary |
| Typical time scale | context | Seasonal May–October; 5 months | POPULATED | e.g. months; season start/end |
| Transparency level | D | — | MISSING | e.g. High / Medium / Low |
| D-parameters | D | OPAQUE in schema | PARTIAL | e.g. constraint index 0–100 |
| C-parameters | C | OPAQUE in schema | PARTIAL | e.g. integration index 0–100 |
| Physical state out (Phase 1) | D | Whole fruit (nuts) | POPULATED | e.g. nuts; kernels (form) |
| Primary transformation | D | Harvest | POPULATED | e.g. harvest; mechanical |
| Actors / custodians | C | Collectors (94% women); 3M employed BF (sector); 50 pilot farmers Koul (Senegal); 100k potential (10y) | POPULATED | e.g. persons; % women; count by role |
| Throughput / volume | N | — | MISSING | e.g. t/year; kg/collector/season |
| Volume per actor | N | — | MISSING | e.g. kg/collector/season (OPAQUE in metrics) |
| Custody (who holds after) | C | — | MISSING | e.g. custodian name; ownership Y/N |

---

## Shea Phase 1 — First sale / aggregation

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Whole fruit or kernels | POPULATED | e.g. nuts; kernels |
| Physical state out | D | Nuts/kernels (aggregated) | POPULATED | e.g. MT; bags |
| Primary transformation | D | Custody transfer to seller | POPULATED | e.g. custody transfer; storage |
| Actors | C | Sellers | POPULATED | e.g. count; role |
| Price / value flow | N | 150 US$/MT dry kernel; 425 US$/MT nuts; 250 CFA/kg | POPULATED | e.g. US$/MT; local currency/kg |
| Volume | N | — | MISSING | e.g. MT/year through this step |
| D-parameters | D | — | MISSING | e.g. quality/contract index |
| C-parameters | C | — | MISSING | e.g. buyer/seller network index |
| Custody (from → to) | C | — | MISSING | e.g. collector → seller; ownership change |

---

## Shea Phase 2 — Trading / bulking

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Kernels | POPULATED | e.g. dry kernel |
| Physical state out | D | Dry kernel (bulk) | POPULATED | e.g. MT bulk |
| Primary transformation | D | Custody transfer; possible storage | POPULATED | e.g. custody; storage |
| Actors | C | Traders; large exporters | POPULATED | e.g. count; role |
| Price / value flow | N | Traders 250 US$/MT; large exporters 250–800 US$/MT | POPULATED | e.g. US$/MT; range |
| Volume | N | — | MISSING | e.g. MT/year traded |
| D-parameters | D | — | MISSING | e.g. contract/spec index |
| C-parameters | C | — | MISSING | e.g. network index |
| Custody (from → to) | C | — | MISSING | e.g. seller → trader → exporter |

---

## Shea Phase 3 — Processing (nuts/kernels to butter)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Nuts or kernels | POPULATED | e.g. kernels |
| Physical state out | D | Shea butter | POPULATED | e.g. kg butter |
| Primary transformation | D | Mechanical/thermal (rendering) | POPULATED | e.g. rendering; thermal |
| Conversion / yield | N | 7 bags → 187 kg butter; 12 bags/MT; 0.53 MT butter/woman/month; 925 kg/woman/season | POPULATED | e.g. kg butter/kg kernel; recovery rate |
| Actors | C | Women processors (BAU); women's groups (Serious Shea) | POPULATED | e.g. custodian; count |
| Throughput | N | 3,774 MT/year agro-food (Serious Shea Senegal, all products) | PARTIAL | e.g. MT butter/year; kg/worker/season |
| Energy / inputs | D/N | BAU: firewood (20 kg wood/kg butter); Serious Shea: 100% renewable | POPULATED | e.g. kg wood/kg product; % renewable |
| CO₂e | N | BAU 10.374 kg CO₂e/kg butter; Serious Shea &lt;0.5187 kg CO₂e/kg | POPULATED | e.g. kg CO₂e/kg product |
| D-parameters | D | OPAQUE in schema | PARTIAL | e.g. process spec index |
| C-parameters | C | OPAQUE in schema | PARTIAL | e.g. supplier/tech index |
| Custody | C | Women processors / women's groups hold during processing | POPULATED | e.g. custodian |

---

## Shea Phase 4 — Export (Logistics / custody)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state | D | Shea butter (or kernels) | POPULATED | e.g. butter; kernels |
| Primary transformation | D | Logistics; custody transfer to buyer | POPULATED | e.g. transport; custody |
| Actors | C | — | MISSING | e.g. carriers; buyers; exporters |
| Routes / nodes | C | — | MISSING | e.g. origin–destination; ports |
| Volume | N | Region 265,000–445,000 t/year; BF export value 90–200M US$/annum | POPULATED | e.g. t/year; US$/annum |
| Share consumed in region | N | ~50% (41–57%) | POPULATED | e.g. ratio; % |
| D-parameters | D | — | MISSING | e.g. capacity; security index |
| C-parameters | C | — | MISSING | e.g. route/network index |
| Custody (from → to) | C | — | MISSING | e.g. processor → buyer; carrier |

---

## Shea Phase 5 — Manufacturing (butter to cosmetic)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Shea butter | POPULATED | e.g. raw butter |
| Physical state out | D | Packaged cosmetic product | POPULATED | e.g. jar; SKU type |
| Primary transformation | D | Formulation; packaging | POPULATED | e.g. formulation; packaging |
| Specification | D | Cleo: 95% shea per jar; 100% renewable energy | POPULATED | e.g. % ingredient; energy source |
| Actors | C | — | MISSING | e.g. manufacturer name; location |
| Throughput | N | — | MISSING | e.g. MT butter/year; units/year |
| Manufacturing location | D | — | MISSING | e.g. country; site |
| D-parameters | D | — | MISSING | e.g. spec/accreditation index |
| C-parameters | C | — | MISSING | e.g. client/certification index |
| Custody | C | — | MISSING | e.g. manufacturer; then to retailer |

---

## Shea Phase 6 — Retail (Market interface / delivery)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | Packaged product | POPULATED | e.g. jar; SKU |
| Physical state out | D | Consumer-held product | POPULATED | e.g. sold to consumer |
| Primary transformation | D | Sale; custody to consumer | POPULATED | e.g. sale; delivery |
| Actors | C | Consumer (end custodian) | POPULATED | e.g. retailer; consumer |
| Volume / turnover | N | SKU sizes 30, 50, 100 ml | POPULATED | e.g. units; ml |
| Price / value | N | 30 US$/30 g; 1 US$/g; 4,000 US$/MT to women (Serious Shea); 47,500 US$/MT to women (Cleo 10% share) | POPULATED | e.g. US$/unit; US$/MT |
| D-parameters | D | — | MISSING | e.g. retail standard index |
| C-parameters | C | — | MISSING | e.g. channel/access index |
| Custody | C | Consumer (custodian at end); ownership and physical move yes | PARTIAL | e.g. retailer → consumer |

---

## Shea — Abstract Phase 5 (Certification / standardisation)

*No dedicated shea phase; certification may be embedded in manufacturing or export.*

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Standard / regime | D | — | MISSING | e.g. standard name; certification body |
| Actors | C | — | MISSING | e.g. certifier; assay body |
| (All other categories) | — | — | N/A for shea as separate phase | Apply if a distinct certification step is added |

---

## Shea — Abstract Phase 8 (Circular / recovery)

*Not currently implemented for shea.*

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Physical state in | D | — | MISSING | e.g. waste butter; used packaging |
| Re-entry point | C | — | MISSING | e.g. phase 3 or 4 |
| Volume | N | — | MISSING | e.g. t/year recovered; % recycled |
| (All other categories) | — | — | N/A | To be defined if circular phase is added |

---

## Cross-phase (shea): Custody and flow

| Flow | custodian_from | custodian_to | ownership_change | custody_change | physical_move | Status | Example metrics |
|------|----------------|--------------|------------------|----------------|---------------|--------|------------------|
| 0→1 | — | — | — | — | — | MISSING | e.g. collector → seller; Y/N |
| 1→2 | — | — | — | — | — | MISSING | e.g. seller → trader |
| 2→3 | — | — | — | — | — | MISSING | e.g. trader → processor |
| 3→4 | — | — | — | — | — | MISSING | e.g. processor → exporter |
| 4→5 | — | — | — | — | — | MISSING | e.g. exporter → manufacturer |
| 5→6 | — | consumer | — | yes | yes | PARTIAL | e.g. manufacturer → consumer |

---

## Summary: Shea data status by category type

- **D (Definition):** Physical states, geography, transformation types, and some specs are often POPULATED; transparency, D-parameters (index), and some specification details are often MISSING or PARTIAL.
- **C (Contribution):** Actors and some custodians are POPULATED in several phases; custody_from/to for flows, routes, and C-parameters (index) are mostly MISSING.
- **N (Negotiation):** Prices, yields, throughput, CO₂e, and employment are POPULATED where we have sources; volume per actor and some throughputs are MISSING.

*Document ties to: `frontend/project/shea/data/` (shea CSVs, `Clarity_Cleo_Shea_Value_Chain_Outline.md`, `EXTRACTED_SHEA_DATA_SUMMARY.md`, and related Serious Shea source files). Remaining ad-hoc sources (e.g. Acorn 080523, Ep-Carbon) stay in `v2/data`.*
