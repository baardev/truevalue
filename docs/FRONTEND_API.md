# Gold Supply Chain Simulator - Frontend Data Contract

## Overview

This document defines the JSON API contract between the gold supply chain data pipeline and the interactive frontend simulator.

## Design Principles

1. **Phase-Resolved**: All data structured by supply chain phase (0-7)
2. **Variable-Driven**: Expose adjustable parameters for simulation
3. **Flow-Aware**: Track material flow between phases
4. **Transparency-Tagged**: Mark data quality explicitly
5. **Real-Time Reconciliation**: Enable validation against anchor data (COMEX)

---

## API Endpoints (Future FastAPI Implementation)

### 1. GET `/api/v1/phases`

Returns all supply chain phases with metadata.

**Response:**
```json
{
  "phases": [
    {
      "phase_id": 0,
      "phase_name": "Geological Occurrence & Prospecting",
      "phase_category": "Pre-supply",
      "physical_state": "In situ",
      "transformation_type": "None",
      "time_scale": "Years",
      "transparency_level": "Medium"
    },
    ...
  ]
}
```

---

### 2. GET `/api/v1/phase/{phase_id}/metrics`

Returns all metrics for a specific phase.

**Parameters:**
- `phase_id` (required): Integer 0-7
- `date_from` (optional): ISO date
- `date_to` (optional): ISO date

**Response:**
```json
{
  "phase_id": 7,
  "phase_name": "Exchange Registration (COMEX)",
  "transparency": "High",
  "metrics": [
    {
      "record_id": 1,
      "entity": "COMEX",
      "country": "USA",
      "date": "2026-01-23",
      "metric_name": "total_registered_inventory",
      "metric_value": 11250000,
      "unit": "oz",
      "source_type": "public",
      "source_name": "CME Group Daily Report"
    }
  ],
  "summary": {
    "total_records": 365,
    "date_range": {
      "start": "2025-01-01",
      "end": "2026-01-23"
    },
    "data_quality": "High"
  }
}
```

---

### 3. GET `/api/v1/flow`

Returns custody and flow data between phases.

**Response:**
```json
{
  "flows": [
    {
      "flow_id": 1,
      "from_phase": 1,
      "to_phase": 2,
      "custodian": "Mining company",
      "ownership_change": false,
      "typical_volume": 50000,
      "volume_unit": "tonnes ore",
      "visibility": "Medium"
    }
  ]
}
```

---

### 4. GET `/api/v1/simulation/config`

Returns adjustable simulation parameters.

**Response:**
```json
{
  "variables": [
    {
      "variable_id": "ore_grade",
      "display_name": "Ore Grade (g/t)",
      "phase_id": 1,
      "default_value": 3.5,
      "min_value": 0.5,
      "max_value": 15.0,
      "unit": "g/t",
      "description": "Grams of gold per tonne of ore",
      "impact_phases": [1, 2],
      "sensitivity": "high"
    },
    {
      "variable_id": "recovery_rate",
      "display_name": "Recovery Rate (%)",
      "phase_id": 2,
      "default_value": 92.0,
      "min_value": 70.0,
      "max_value": 98.0,
      "unit": "percent",
      "description": "Efficiency of gold extraction from ore",
      "impact_phases": [2, 3],
      "sensitivity": "medium"
    },
    {
      "variable_id": "refining_capacity",
      "display_name": "Refining Capacity (tonnes/year)",
      "phase_id": 4,
      "default_value": 2000,
      "min_value": 500,
      "max_value": 5000,
      "unit": "tonnes/year",
      "description": "Annual refinery throughput",
      "impact_phases": [4, 5, 6, 7],
      "sensitivity": "high"
    },
    {
      "variable_id": "vault_capacity",
      "display_name": "Vault Capacity (tonnes)",
      "phase_id": 6,
      "default_value": 500,
      "min_value": 100,
      "max_value": 2000,
      "unit": "tonnes",
      "description": "Total vault storage capacity",
      "impact_phases": [6, 7],
      "sensitivity": "medium",
      "transparency_note": "Low visibility - structural opacity"
    }
  ]
}
```

---

### 5. POST `/api/v1/simulation/run`

Execute simulation with custom variable values.

**Request Body:**
```json
{
  "scenario_name": "High ore grade, reduced refining capacity",
  "variables": {
    "ore_grade": 5.0,
    "recovery_rate": 94.0,
    "refining_capacity": 1500
  },
  "time_horizon_days": 365
}
```

**Response:**
```json
{
  "scenario_id": "sim_20260123_001",
  "scenario_name": "High ore grade, reduced refining capacity",
  "status": "completed",
  "execution_time_ms": 234,
  "results": {
    "phase_outputs": [
      {
        "phase_id": 1,
        "phase_name": "Mine Extraction",
        "total_output_oz": 120000000,
        "bottleneck": false
      },
      {
        "phase_id": 4,
        "phase_name": "Refining",
        "total_output_oz": 48000000,
        "bottleneck": true,
        "capacity_utilization": 98.5
      },
      {
        "phase_id": 7,
        "phase_name": "Exchange Registration",
        "total_output_oz": 45000000,
        "reconciliation_delta_oz": -2000000,
        "reconciliation_status": "warning"
      }
    ],
    "sustainability_metrics": {
      "energy_consumption_gwh": 1500,
      "water_usage_megalitres": 45000,
      "co2_emissions_tonnes": 250000
    },
    "profit_loss": {
      "note": "Value chain analysis deferred per Rule Set 8"
    }
  }
}
```

---

### 6. GET `/api/v1/transparency/report`

Returns transparency assessment across all phases.

**Response:**
```json
{
  "transparency_map": [
    {
      "phase_id": 0,
      "phase_name": "Geological Occurrence & Prospecting",
      "transparency_level": "Medium",
      "data_sources": ["public"],
      "record_count": 150,
      "opacity_reason": "Geological uncertainty"
    },
    {
      "phase_id": 6,
      "phase_name": "Logistics & Vaulting",
      "transparency_level": "Low",
      "data_sources": ["OPAQUE"],
      "record_count": 5,
      "opacity_reason": "Custodial secrecy, jurisdictional controls"
    }
  ],
  "overall_score": 6.8,
  "high_transparency_phases": [1, 2, 7],
  "low_transparency_phases": [6]
}
```

---

## Static Data Files (Initial Implementation)

Before implementing FastAPI, use these JSON files for frontend development:

### `/data/processed/phases.json`

Complete phase definitions (generated from `supply_chain_phases.csv`)

### `/data/processed/phase{N}_summary.json`

Per-phase aggregated metrics (N = 0-7)

### `/data/processed/simulation_defaults.json`

Default simulation configuration

### `/data/processed/transparency_report.json`

Current data availability assessment

---

## Frontend Implementation Notes

### Visualization Requirements

1. **Phase Flow Diagram**
   - Sankey diagram showing gold flow from Phase 0 → 7
   - Width proportional to volume
   - Color-coded by transparency level

2. **Variable Control Panel**
   - Sliders for each adjustable variable
   - Real-time impact preview
   - Reset to baseline button

3. **Bottleneck Detection**
   - Highlight phases operating at >95% capacity
   - Show upstream/downstream cascade effects

4. **Reconciliation View**
   - Compare simulated Phase 7 output to actual COMEX data
   - Show delta and flag discrepancies

5. **Transparency Overlay**
   - Toggle to show data quality by phase
   - Opacity reasons displayed on hover

### Recommended Tech Stack

- **Framework**: React or Svelte
- **Visualization**: D3.js or Plotly.js
- **State Management**: Zustand or Redux
- **API Client**: Axios or Fetch API

---

## Data Update Cadence

| Phase | Update Frequency | Source |
|-------|------------------|--------|
| 0 | Annual | Geological surveys |
| 1 | Quarterly | Company reports |
| 2 | Quarterly | Technical filings |
| 3-5 | Semi-annual | Industry reports |
| 6 | OPAQUE | N/A |
| 7 | Daily | COMEX reports |

---

## Validation Rules

Frontend should validate:

1. **Phase sequence**: Flow must follow phase order (no backward flow without explicit loop)
2. **Unit consistency**: All calculations respect metric units
3. **Conservation of mass**: Total input ≥ Total output (accounting for losses)
4. **Transparency tagging**: All data points must have source_type
5. **COMEX reconciliation**: Final output should approximate Phase 7 actual data within 10%

---

## Error Handling

```json
{
  "error": {
    "code": "INVALID_PHASE_ID",
    "message": "Phase ID must be between 0 and 7",
    "phase_id": 9,
    "timestamp": "2026-01-23T14:32:00Z"
  }
}
```

---

## Next Steps

1. Generate static JSON files from current CSV data
2. Build simple FastAPI server for `/phases` and `/metrics` endpoints
3. Implement simulation engine (separate module)
4. Add WebSocket support for real-time updates when COMEX data refreshes

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-23  
**Compatibility**: Gold Supply Chain Intelligence v0.1

