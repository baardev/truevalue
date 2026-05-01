---
doc_id: frontend_docs_api_frontend_api
title: Gold Supply Chain Simulator - Frontend Data Contract
type: api_reference
status: active
domain: gold_supply_chain
layer: supply_chain
projects:
  []
tags:
  - api
  - gold
  - gold_supply_chain
  - supply_chain
related_docs:
  []
key_claims:
  []
---

# Gold Supply Chain Simulator - Frontend Data Contract

## Overview

This document defines the JSON API contract between the gold supply chain data pipeline and the interactive frontend simulator.

## Design Principles

1. **Phase-Resolved**: All data structured by supply chain phase (0-8, now includes Recycling)
2. **Variable-Driven**: Expose adjustable parameters for simulation
3. **Flow-Aware**: Track material flow between phases (including circular flows)
4. **Transparency-Tagged**: Mark data quality explicitly
5. **Real-Time Reconciliation**: Enable validation against anchor data (COMEX)
6. **Environmental Integration**: Water, waste, and energy metrics per Sarah's TRUE VALUE framework

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

### 7. GET `/api/v1/phase/{phase_id}/environmental`

Returns environmental sustainability metrics for a specific phase.

**NEW - Added for Sarah Document Integration (water/waste/energy metrics)**

**Parameters:**
- `phase_id` (required): Integer 0-8 (now includes Phase 8: Recycling)
- `date_from` (optional): ISO date
- `date_to` (optional): ISO date
- `aggregate` (optional): "daily" | "weekly" | "monthly" (default: "daily")

**Response:**
```json
{
  "phase_id": 2,
  "phase_name": "Ore Processing & Concentration",
  "transparency": "High",
  "date_range": {
    "start": "2025-01-01",
    "end": "2026-01-23"
  },
  "water_metrics": {
    "water_consumed_total": 8500000,
    "water_consumed_blue": 6800000,
    "water_consumed_grey": 1700000,
    "water_recycled": 6375000,
    "water_recycling_rate_pct": 75.0,
    "water_discharged": 2125000,
    "unit": "litres_per_day",
    "source_type": "public",
    "source_name": "Company Sustainability Report 2024",
    "data_quality": "High"
  },
  "waste_metrics": {
    "waste_material_total": 9750000,
    "waste_material_tailings": 9500000,
    "waste_material_hazardous": 950000,
    "waste_material_recycled": 487500,
    "waste_recycling_rate_pct": 5.0,
    "tailings_to_ore_ratio": 0.95,
    "unit": "kg_per_day",
    "source_type": "public",
    "source_name": "Technical Report NI 43-101",
    "data_quality": "High",
    "notes": "Phase 2 is critical waste phase - 95%+ of ore becomes tailings"
  },
  "energy_metrics": {
    "energy_consumed_total": 180000,
    "energy_grid_type": "AC_grid",
    "energy_source_clean_pct": 40.0,
    "energy_source_fossil_pct": 60.0,
    "energy_clean_types": ["solar", "grid_hydro"],
    "energy_intensity_per_tonne": 18.0,
    "unit": "kWh_per_day",
    "source_type": "public",
    "source_name": "Company Environmental Disclosure",
    "data_quality": "Medium"
  },
  "sustainability_summary": {
    "water_stress_level": "Medium",
    "waste_circular_economy_score": 5.0,
    "energy_clean_transition_progress": 40.0,
    "overall_environmental_score": 6.2,
    "unit": "index_0_to_10"
  },
  "comparison_to_industry": {
    "water_recycling_rate": "Above average (industry avg: 65%)",
    "waste_recycling_rate": "Below average (industry avg: 8%)",
    "clean_energy_pct": "Average (industry avg: 38%)"
  }
}
```

---

### 8. GET `/api/v1/entities`

Returns registry of real-world entities (companies, facilities) mapped to phases.

**NEW - Added for Sarah Document Integration (company mapping)**

**Response:**
```json
{
  "entities": [
    {
      "entity_id": "E001",
      "entity_name": "Newmont Corporation",
      "entity_type": "producer",
      "phase_ids": [0, 1, 2, 3],
      "countries": ["Multi"],
      "hq_location": "Denver CO USA",
      "sustainability_report_url": "https://www.newmont.com/sustainability/",
      "data_quality": "high",
      "notes": "World's largest gold miner - advanced sustainability reporting",
      "environmental_data_available": true,
      "latest_data_year": 2024
    },
    {
      "entity_id": "E013",
      "entity_name": "UK Royal Mint",
      "entity_type": "recycler",
      "phase_ids": [8, 4, 5],
      "countries": ["UK"],
      "hq_location": "Llantrisant Wales",
      "sustainability_report_url": "https://www.royalmint.com/aboutus/policies-and-guidelines/",
      "data_quality": "medium",
      "notes": "E-waste recycling - phones to coins",
      "environmental_data_available": true,
      "latest_data_year": 2023
    }
  ],
  "summary": {
    "total_entities": 22,
    "producers": 12,
    "recyclers": 1,
    "royalty_companies": 3,
    "synthetic_placeholders": 9,
    "high_quality_data": 8,
    "medium_quality_data": 5,
    "synthetic_only": 9
  }
}
```

---

### 9. GET `/api/v1/circular_economy`

Returns circular economy metrics including Phase 8 (Recycling) integration.

**NEW - Added for Sarah Document Integration (circular economy tracking)**

**Response:**
```json
{
  "recycling_metrics": {
    "phase_8_id": 8,
    "phase_8_name": "Recycling & Recovery",
    "transparency": "Medium",
    "annual_recycled_gold_supply": {
      "value": 1200,
      "unit": "tonnes_per_year",
      "percentage_of_total_supply": 28.5,
      "source": "World Gold Council"
    },
    "recycling_sources": [
      {
        "source_type": "E-waste",
        "contribution_pct": 45.0,
        "gold_content_per_unit": "0.3-0.5 g per phone",
        "collection_rate_pct": 20.0,
        "data_quality": "Medium"
      },
      {
        "source_type": "Jewelry scrap",
        "contribution_pct": 40.0,
        "gold_content_per_unit": "Variable by karat",
        "collection_rate_pct": 60.0,
        "data_quality": "Medium"
      },
      {
        "source_type": "Industrial waste",
        "contribution_pct": 15.0,
        "gold_content_per_unit": "Variable",
        "collection_rate_pct": 80.0,
        "data_quality": "Low"
      }
    ]
  },
  "feedback_loop": {
    "description": "Recycled gold re-enters supply chain at Phase 4 (Refining)",
    "from_phase": 8,
    "to_phase": 4,
    "flow_type": "recycled",
    "blended_sustainability_impact": {
      "energy_savings_vs_primary": "60-80% reduction",
      "water_savings_vs_primary": "90% reduction",
      "no_mining_waste": true
    }
  },
  "waste_reuse_by_phase": [
    {
      "phase_id": 2,
      "phase_name": "Ore Processing",
      "waste_material_recycled_pct": 5.0,
      "reuse_methods": ["Backfill for underground mines", "Tailings reprocessing (limited)"],
      "improvement_potential": "High - technology advancing"
    },
    {
      "phase_id": 4,
      "phase_name": "Refining",
      "waste_material_recycled_pct": 85.0,
      "reuse_methods": ["Silver recovery", "Platinum group metal recovery"],
      "improvement_potential": "Low - already highly optimized"
    }
  ],
  "circular_economy_score": {
    "overall": 4.2,
    "unit": "index_0_to_10",
    "interpretation": "Moderate - recycling established but ore processing waste underutilized",
    "target_2030": 6.5
  }
}
```

---

## Static Data Files (Initial Implementation)

Before implementing FastAPI, use these JSON files for frontend development:

### `/frontend/project/gold/data/processed/phases.json`

Complete phase definitions (generated from `supply_chain_phases.csv`)

### `/data/processed/phase{N}_summary.json`

Per-phase aggregated metrics (N = 0-7)

### `/frontend/project/gold/data/processed/simulation_defaults.json`

Default simulation configuration

### `/frontend/project/gold/data/processed/transparency_report.json`

Current data availability assessment

### `/frontend/project/gold/data/schema/entity_registry.csv`

**NEW**: Real-world companies and facilities mapped to phases (from Sarah's document)

### Environmental Metrics (Future Static Files)

- `/data/processed/environmental_phase{N}.json` - Water/waste/energy metrics per phase
- `/data/processed/circular_economy_report.json` - Recycling and reuse tracking

---

## Frontend Implementation Notes

### Visualization Requirements

1. **Phase Flow Diagram**
   - Sankey diagram showing gold flow from Phase 0 → 8 (including Recycling)
   - Width proportional to volume
   - Color-coded by transparency level
   - **NEW**: Show circular flow from Phase 8 → Phase 4 (recycled gold)

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

6. **Environmental Dashboard (NEW - Sarah Integration)**
   - Water consumption and recycling rates by phase
   - Waste generation with circular economy opportunities highlighted
   - Energy mix (clean vs. fossil) with transition progress
   - Phase 2 tailings waste emphasized (95%+ of ore volume)
   - Comparison to industry benchmarks (Newmont, Barrick data)

7. **Entity Mapping (NEW - Sarah Integration)**
   - Map real companies to phases (Newmont, Barrick, UK Royal Mint, etc.)
   - Link to sustainability report URLs
   - Show data quality by entity

### Recommended Tech Stack

- **Framework**: React or Svelte
- **Visualization**: D3.js or Plotly.js
- **State Management**: Zustand or Redux
- **API Client**: Axios or Fetch API

---

## Data Update Cadence

| Phase | Update Frequency | Source | Environmental Data Frequency |
|-------|------------------|--------|------------------------------|
| 0 | Annual | Geological surveys | Annual |
| 1 | Quarterly | Company reports | Annual (sustainability reports) |
| 2 | Quarterly | Technical filings | Annual (sustainability reports) |
| 3-5 | Semi-annual | Industry reports | Annual |
| 6 | OPAQUE | N/A | N/A |
| 7 | Daily | COMEX reports | N/A |
| 8 (NEW) | Annual | World Gold Council, recyclers | Annual (e-waste statistics) |

**Environmental Metrics Update**: Annual (aligned with company sustainability reporting cycles)

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

1. ✅ Generate static JSON files from current CSV data
2. ✅ Add Phase 8 (Recycling) to schema
3. ✅ Create entity registry with Sarah's company list
4. Build simple FastAPI server for `/phases` and `/metrics` endpoints
5. **NEW**: Implement `/environmental` endpoint with water/waste/energy data
6. **NEW**: Implement `/entities` endpoint for company mapping
7. **NEW**: Implement `/circular_economy` endpoint for recycling tracking
8. Implement simulation engine (separate module)
9. Add WebSocket support for real-time updates when COMEX data refreshes
10. **Future**: Scrape Newmont/Barrick sustainability reports for real environmental data

---

## Sarah Document Integration Status

✅ **Completed**:
- Entity registry created with gold producers and recyclers
- Phase 8 (Recycling & Recovery) added to supply chain
- Water/waste/energy metrics documented in `WATER_WASTE_METHODOLOGY.md`
- API endpoints designed for environmental data
- Circular economy tracking specified

⏳ **Future**:
- Generate synthetic environmental data (extend `synthetic_data_generator.py`)
- Scrape real data from company sustainability reports
- Add labor metrics (person-hours, payroll)
- Add land use metrics (hectares)
- Implement "Beyond GDP" interpretive layer (deferred per Rule Set 8)

---

**Document Version**: 1.1  
**Last Updated**: 2026-01-24 (Sarah Integration)  
**Compatibility**: Gold Supply Chain Intelligence v0.2

