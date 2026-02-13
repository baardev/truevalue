# Value Chain Layer Rules (Strictly Separate)

## Purpose

This layer models the **value chain** (profit, pricing, margins, cost structure) for the gold supply chain.

It is **strictly separated** from the physical **supply chain** layer.

## Non-Negotiable Separation

- **Do not** add value-chain metrics (USD, margins, pricing) into any supply-chain CSVs, notebooks, or dashboards.
- **Do not** infer physical supply constraints from value-chain outcomes.
- **Do not** introduce financial abstraction (paper claims, leverage, rehypothecation) here. That is a later layer.

## Linkage Rules (Allowed)

The only allowed linkage between layers is via **stable identifiers**:

- `phase_id` / `value_phase_id` (phase alignment)
- `entity_id` (shared registry key, but stored in separate value-chain CSVs)
- `country`, `date`

## Time Resolution (Quarterly + Annual)

This layer supports both **quarterly** and **annual** reporting, because:

- Quarterly is best for educational/sensitivity work (more temporal resolution).
- Annual is the most broadly compatible across institutions and opaque phases.

### Conventions

- `date` is the **period end** date.
  - Quarterly examples: `2024-03-31`, `2024-06-30`, `2024-09-30`, `2024-12-31`
  - Annual example: `2024-12-31`
- `period_type` is a categorical field:
  - `quarterly` | `annual` (extend later if needed)

No other cross-layer coupling is permitted in computations unless explicitly documented as a reconciliation step.

## Data-First Discipline

All value-chain claims must be representable as:

`value_phase_id → metric_name → metric_value → unit → source_type → source_name → url`

If data is missing, mark it explicitly as **OPAQUE** in `source_type` and explain structurally (commercial secrecy, jurisdictional limits).

## Phase Model

Value chain uses `value_phase_id` aligned 1:1 with supply-chain phases (0–8) for consistent indexing.

This keeps physical and value data comparable by *phase* without mixing datasets.

## Files (Value Chain Only)

- `schema/value_chain_metrics.csv` (data store)
- `schema/value_chain_metric_definitions.csv` (definitions)
- `schema/value_chain_data_sources.csv` (sources)
- `src/value_chain/` (logic + API generator)
- `frontend/value_chain/` (UI)

