---
doc_id: shea_value_chain_phase_instance
title: "Shea Butter — Value Chain Phase Instance"
type: documentation
status: active
domain: pdi
layer: value_chain
projects:
  - shea
tags:
  - pdi
  - phase_mapping
  - shea
  - value_chain
related_docs:
  []
key_claims:
  []
---

# Shea Butter — Value Chain Phase Instance

**Template reference:** This instance follows the [Abstract Value Chain Phase Template](ABSTRACT_VALUE_CHAIN_PHASE_TEMPLATE.md). Shea value phases map to shea supply phases: 0 Collection, 1 First sale, 2 Trading, 3 Processing, 4 Export, 5 Manufacturing, 6 Retail. Certification (abstract 5) and Circular (8) have no dedicated shea value phase here.

Data from: `frontend/project/west_african_shea/data/shea_phase_metrics.csv`, `frontend/project/west_african_shea/data/Clarity_Cleo_Shea_Value_Chain_Outline.md`, `frontend/project/west_african_shea/data/shea_fund_and_project_context.csv`. Value metrics (income, prices, export value, value to women) filled where present; **MISSING** where absent.

---

## Shea Value Phase 0 — Collection (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Pre-revenue / labour context | POPULATED | e.g. employment; barriers |
| Employment (sector) | N | 3M (Burkina Faso shea sector); 50 pilot farmers Koul (Senegal); 100k potential (10y) | POPULATED | e.g. persons; baseline_workers |
| Additionality barriers | D | Finance, expertise, land, markets (Serious Shea Additionality Assessment) | POPULATED | e.g. barrier list; index |
| Revenue / income to collector | N | — | MISSING | e.g. USD/collector/season; local currency/kg |
| Typical time scale | context | Seasonal (5 months) | POPULATED | e.g. seasonal; annual |
| Transparency level | D | — | MISSING | e.g. High / Medium / Low |
| D-parameters (value) | D | — | MISSING | e.g. constraint index |
| C-parameters (value) | C | — | MISSING | e.g. market_access index |

---

## Shea Value Phase 1 — First sale / aggregation (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | First sale / seller income | POPULATED | e.g. income per MT |
| Income to sellers | N | 150 US$/MT dry kernel equivalent | POPULATED | e.g. income_sellers_per_MT_dry_kernel |
| Price (nuts) | N | 425 US$/MT nuts; 250 CFA/kg (2013) | POPULATED | e.g. price_nuts_per_MT; local currency/kg |
| Revenue / volume | N | — | MISSING | e.g. revenue_usd; MT/year |
| Margin | N | — | MISSING | e.g. margin_gross_pct |
| Typical time scale | context | Seasonal | POPULATED | e.g. seasonal |
| D-parameters (value) | D | — | MISSING | e.g. contract index |
| C-parameters (value) | C | — | MISSING | e.g. buyer_network index |

---

## Shea Value Phase 2 — Trading / bulking (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Trader / exporter income | POPULATED | e.g. income per MT |
| Income to traders | N | 250 US$/MT dry kernel | POPULATED | e.g. income_traders_per_MT |
| Income to large exporters | N | 250–800 US$/MT dry kernel | POPULATED | e.g. US$/MT range |
| Revenue / volume | N | — | MISSING | e.g. revenue_usd; MT/year |
| Margin | N | — | MISSING | e.g. margin_gross_pct |
| D-parameters (value) | D | — | MISSING | e.g. contract index |
| C-parameters (value) | C | — | MISSING | e.g. counterparty index |

---

## Shea Value Phase 3 — Processing (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Processing output; cost context (energy) | POPULATED | e.g. butter per woman; energy cost |
| Throughput (product) | N | 0.53 MT butter/woman/month; 925 kg/woman/season | POPULATED | e.g. kg/worker/season |
| Energy cost (BAU) | D/N | 20 kg firewood/kg butter (BAU); 100% renewable (Serious Shea) | POPULATED | e.g. cost or fuel/kg product |
| CO₂e (cost proxy) | N | BAU 10.374 kg CO₂e/kg; Serious Shea &lt;0.5187 kg CO₂e/kg | POPULATED | e.g. kg CO₂e/kg (environmental cost) |
| Revenue / price to processor | N | — | MISSING | e.g. USD/MT butter; price to women's groups |
| Margin | N | — | MISSING | e.g. margin_gross_pct |
| Serious Shea price to women (later phase) | N | 4,000 US$/MT (current) | POPULATED | e.g. Serious_Shea_price_to_women_groups_per_MT (value capture) |
| D-parameters (value) | D | — | MISSING | e.g. energy_cost index |
| C-parameters (value) | C | — | MISSING | e.g. buyer_commitment index |

---

## Shea Value Phase 4 — Export (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Export value (country/region) | POPULATED | e.g. export value USD |
| Export value (Burkina Faso) | N | 90–200M US$/annum | POPULATED | e.g. export_value_burkina_faso_min/max |
| Export volume (region) | N | 265,000–445,000 t/year | POPULATED | e.g. t/year (context for value) |
| Share consumed in region | N | ~50% (41–57%) | POPULATED | e.g. ratio (value split proxy) |
| Revenue / price per unit | N | — | MISSING | e.g. US$/MT exported; realized_price |
| Transport / logistics cost | N | — | MISSING | e.g. transport_cost_usd_per_kg |
| D-parameters (value) | D | — | MISSING | e.g. route_cost index |
| C-parameters (value) | C | — | MISSING | e.g. buyer_network index |

---

## Shea Value Phase 5 — Manufacturing (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Formulation; specification (shea %) | POPULATED | e.g. 95% shea per jar |
| Specification | D | Cleo: 95% shea per jar; 100% renewable energy | POPULATED | e.g. % shea; energy source |
| Gross price (cosmetics segment) | N | Organic cosmetics 6,199.75; non-organic 4,476.15; food 2,410–2,746 US$/MT (2019 range) | POPULATED | e.g. US$/MT by segment (Clarity) |
| Revenue / throughput | N | — | MISSING | e.g. revenue_usd; units/year |
| Margin | N | — | MISSING | e.g. margin_gross_pct |
| Manufacturing location | D | — | MISSING | e.g. country (for cost/tax context) |
| D-parameters (value) | D | — | MISSING | e.g. spec_compliance index |
| C-parameters (value) | C | — | MISSING | e.g. client_diversity index |

---

## Shea Value Phase 6 — Retail (value context)

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Definition scope | D | Retail price; value share to producers | POPULATED | e.g. retail price; % to women |
| Retail price | N | 30 US$/30 g (1 US$/g); SKU sizes 30, 50, 100 ml | POPULATED | e.g. retail_price_30g; US$/g |
| Value to women's groups (Serious Shea) | N | 4,000 US$/MT (current) | POPULATED | e.g. US$/MT |
| Value to women's groups (Cleo 10% share) | N | 47,500 US$/MT (0.0475 US$/g × 10% of retail) | POPULATED | e.g. Cleo_value_to_women_per_MT_10pct_share |
| Income uplift (Cleo vs baseline) | N | 47,500 / 4,000 = 11.875× | POPULATED | e.g. ratio (Clarity) |
| Revenue / turnover | N | — | MISSING | e.g. revenue_usd; USD/annum |
| Margin | N | Cleo margin 50% (retail) cited in Clarity | PARTIAL | e.g. margin_gross_pct |
| D-parameters (value) | D | — | MISSING | e.g. retail_margin index |
| C-parameters (value) | C | — | MISSING | e.g. channel index |

---

## Shea — Abstract value Phase 5 (Certification) and Phase 8 (Circular)

*No dedicated shea value phase for certification or circular in current mapping.*

| Category | N-D-C | Value (current) | Status | Example metrics to measure |
|----------|-------|------------------|--------|----------------------------|
| Certification fee / cost | N | — | MISSING | e.g. USD/unit; % of value |
| Recycling value / cost | N | — | MISSING | e.g. USD/unit recovered; % of supply |

---

## Summary: Shea value data status

- **D (Definition):** Definition scope, employment, barriers, specification (e.g. 95% shea) **POPULATED** where we have context. Formal D/C parameter indices **MISSING**.
- **C (Contribution):** Actor and segment context **POPULATED**. C-parameter indices **MISSING**.
- **N (Negotiation):** Income and prices by phase (sellers 150, traders 250, exporters 250–800 US$/MT; export value 90–200M US$/annum; retail 30 US$/30g; value to women 4,000 and 47,500 US$/MT) **POPULATED**. Revenue_usd, margin_gross_pct, and transport/insurance costs **MISSING** or PARTIAL.

*Supply chain instance (physical):* Shea supply chain instance (not yet in this repo).  
*Data:* `frontend/project/west_african_shea/data/shea_phase_metrics.csv`, `shea_fund_and_project_context.csv`, `Clarity_Cleo_Shea_Value_Chain_Outline.md` (same directory).
