---
doc_id: frontend_docs_reports_water_waste_methodology
title: "Water, Waste, and Environmental Metrics Methodology"
type: methodology
status: active
domain: water_systems
layer: methodology
projects:
  []
tags:
  - methodology
  - water
  - water_systems
related_docs:
  []
key_claims:
  []
---

# Water, Waste, and Environmental Metrics Methodology
## Gold Supply Chain Intelligence Platform

**Date**: January 24, 2026  
**Version**: 1.0  
**Status**: Initial documentation for synthetic data + future real data collection

---

## Overview

This document defines how water, waste, and energy metrics are measured, calculated, and attributed across the gold supply chain (Phases 0-8). These metrics were added to integrate Sarah's "TRUE VALUE METRICS" requirements (`docs/Activities/SARAH_INTEGRATION_ANALYSIS.md`, lines 46-62) while maintaining compliance with the project's 9 Rule Sets.

---

## Core Principles

1. **Physical Units Only** - Litres, kilograms, kilowatt-hours (no financial interpretation)
2. **Phase-Specific** - Each metric maps to specific supply chain phases
3. **Source Attribution** - All values tagged as synthetic, public, paid, or inferred
4. **Transparency Classification** - Data availability varies by phase and metric type
5. **Industry Benchmarks** - Values based on World Gold Council, ICMM, and company reports

---

## Part 1: Water Metrics

### 1.1 Metric Definitions

| Metric Type | Unit | Description | Applicable Phases |
|-------------|------|-------------|-------------------|
| `water_consumed` | litres | Total freshwater withdrawn from any source | 1, 2, 4 |
| `water_recycled` | litres | Water reused in closed-loop systems | 2, 4 |
| `water_discharged` | litres | Water returned to environment (treated) | 1, 2, 4 |
| `water_source_blue` | litres | Surface/groundwater (rivers, aquifers) | 1, 2 |
| `water_source_grey` | litres | Treated wastewater reused | 2, 4 |
| `water_source_brown` | litres | Untreated wastewater (rare, non-compliant) | 2 |

**Source**: Sarah doc lines 50-52, adapted from FAO AGROVOC water source ontology

### 1.2 Phase-Specific Water Use

#### Phase 1: Mine Extraction
**Typical Range**: 500,000 - 4,000,000 litres/day (site-dependent)

**Uses**:
- Dust suppression on haul roads (30-40%)
- Ore washing before crushing (20-30%)
- Equipment cooling (10-15%)
- Potable water for workforce (5-10%)
- Environmental controls (dust, rehabilitation) (10-20%)

**Industry Benchmarks**:
- Open-pit mine: 1.5 - 3.0 million litres/day (Newmont, Barrick reports)
- Underground mine: 0.5 - 1.5 million litres/day (lower dust control needs)
- Arid regions: Higher due to evaporation, limited recycling

**Recycling Rate**: 10-30% (mostly equipment cooling water)

**Data Sources**:
- Newmont Sustainability Report (site-specific data)
- Barrick Water Stewardship Reports
- ICMM Water Reporting Guidelines
- World Gold Council: Responsible Gold Mining Principles

**Transparency**: High (publicly reported by major producers)

---

#### Phase 2: Ore Processing & Concentration
**Typical Range**: 5,000,000 - 12,000,000 litres/day (highest water use phase)

**Uses**:
- Cyanide leaching circuits (40-50%)
- Flotation concentration (25-35%)
- Gravity separation (10-15%)
- Tailings transport (5-10%)
- Wash water for equipment (5%)

**Industry Benchmarks**:
- 1,000 - 2,500 litres per tonne of ore processed
- Large operations (10,000 tonne/day): 10-25 million litres/day
- Carbon-in-leach (CIL) plants: 1,500-2,000 litres/tonne

**Recycling Rate**: 60-85% (closed-loop circuits common)

**Critical Factor**: Water quality matters
- Fresh water for leaching (impurities affect gold recovery)
- Recycled water for flotation (acceptable)
- Treated tailings water recycled back to process

**Data Sources**:
- Technical reports (NI 43-101, JORC filings)
- Company sustainability reports
- Academic literature (metallurgical journals)
- Equipment vendor specifications (leach tanks, flotation cells)

**Transparency**: High (technical data in mining feasibility studies)

---

#### Phase 3: Doré Production
**Typical Range**: 100,000 - 500,000 litres/day

**Uses**:
- Smelting furnace cooling (60-70%)
- Slag granulation (20-30%)
- Equipment wash-down (5-10%)

**Recycling Rate**: 70-90% (closed-loop cooling)

**Transparency**: Medium (aggregate company-level data)

---

#### Phase 4: Refining
**Typical Range**: 500,000 - 2,000,000 litres/day (chemical processing)

**Uses**:
- Aqua regia dissolution (20-30%)
- Electrolytic refining baths (30-40%)
- Rinsing and washing (15-25%)
- Cooling systems (10-15%)
- Waste treatment (5-10%)

**Industry Benchmarks**:
- 200-500 litres per kilogram of refined gold
- LBMA-accredited refineries: Higher due to purity requirements

**Recycling Rate**: 50-75% (cooling water mostly, process water less)

**Critical Factor**: Ultra-pure water needed for final stages
- Deionized water for electrolytic refining
- Rinse water must not contaminate 99.99% purity

**Data Sources**:
- Refinery technical disclosures (limited)
- LBMA Good Delivery standards (process requirements)
- Academic papers on refining chemistry
- Environmental permits (discharge limits)

**Transparency**: Medium (aggregated, some proprietary processes)

---

#### Phases 5-7: Minimal Water Use
- **Phase 5 (Bar Casting)**: <50,000 litres/day (cooling water)
- **Phase 6 (Vaulting)**: Negligible (climate control only)
- **Phase 7 (Exchange)**: Negligible

---

#### Phase 8: Recycling & Recovery
**Typical Range**: 800,000 - 1,500,000 litres/day

**Uses**:
- E-waste pre-processing (shredding, washing) (30-40%)
- Chemical extraction (similar to refining) (40-50%)
- Cooling and rinsing (10-20%)

**Recycling Rate**: 60-80%

**Note**: Similar to Phase 4 but higher variability due to heterogeneous input material

**Transparency**: Medium (growing industry, some public data from UK Royal Mint, Umicore)

---

### 1.3 Calculation Methodology

#### For Synthetic Data
```python
# Base consumption per phase (litres/day)
water_base = {
    0: 0,
    1: 2_000_000,      # Mining
    2: 8_000_000,      # Processing (highest)
    3: 300_000,        # Doré
    4: 1_000_000,      # Refining
    5: 30_000,         # Bar casting
    6: 0,
    7: 0,
    8: 1_000_000       # Recycling
}

# Add random variation (±25%)
import random
water_consumed = water_base[phase_id] * random.gauss(1.0, 0.25)

# Calculate recycled based on phase recycling rate
recycling_rate = {
    1: 0.20,   # 20%
    2: 0.75,   # 75% (closed-loop circuits)
    3: 0.80,
    4: 0.65,
    8: 0.70
}

water_recycled = water_consumed * recycling_rate.get(phase_id, 0)

# Water source breakdown
# Phase 1-2: Mostly blue water (surface/groundwater)
# Phase 2,4: Some grey water (recycled from tailings/process)
if phase_id in [1, 2]:
    water_source_blue = water_consumed * random.uniform(0.70, 0.90)
    water_source_grey = water_consumed * random.uniform(0.10, 0.30)
```

#### For Real Data (Future)
1. Extract from company sustainability reports (Table: Water Withdrawal by Source)
2. Convert to common unit (litres/day)
3. Attribute to specific phase based on operational context
4. Tag as `source_type: public`
5. Include URL and report page number

---

### 1.4 Data Quality Tiers

| Tier | Description | Example | Source Type |
|------|-------------|---------|-------------|
| **High** | Site-specific, measured data | Newmont Ahafo mine: 2.3M L/day (2024 report) | `public` |
| **Medium** | Company aggregate, estimated breakdown | Barrick total water: 45M L/day across 5 sites | `public` |
| **Low** | Industry benchmark applied to phase | Phase 2 avg: 1,800 L/tonne × 10,000 tonne/day | `inferred` |
| **Synthetic** | Model-generated for simulation | Phase 2: 8.2M L/day ±25% | `simulated` |

---

## Part 2: Waste Metrics

### 2.1 Metric Definitions

| Metric Type | Unit | Description | Applicable Phases |
|-------------|------|-------------|-------------------|
| `waste_material_total` | kg | Total solid waste generated | 1, 2, 4 |
| `waste_material_overburden` | kg | Waste rock removed to access ore | 1 |
| `waste_material_tailings` | kg | Post-extraction ore waste (largest volume) | 2 |
| `waste_material_hazardous` | kg | Cyanide, acids, heavy metals | 2, 4 |
| `waste_material_slag` | kg | Doré smelting byproduct | 3 |
| `waste_material_recycled` | kg | Waste reused in production or sold | 2, 3, 4 |
| `waste_water_discharged` | litres | Treated wastewater returned to environment | 1, 2, 4 |

**Source**: Sarah doc lines 48, 51, 74 (circular economy emphasis)

### 2.2 Phase-Specific Waste Generation

#### Phase 1: Mine Extraction
**Typical Waste Ratio**: 3:1 to 20:1 (waste rock : ore)

**Waste Types**:
- **Overburden**: Soil, topsoil removed before mining (stored for rehabilitation)
- **Waste rock**: Non-ore rock removed to access ore body
- **Minimal hazardous waste**: Explosives residue, fuel/oil leaks (small compared to ore volume)

**Industry Benchmarks**:
- Low-grade mine (2 g/t): 10-20 tonnes waste per tonne ore
- High-grade mine (5+ g/t): 3-5 tonnes waste per tonne ore
- Open-pit: Higher waste ratios than underground

**Example**:
- Mine produces 10,000 tonnes ore/day at 4 g/t
- Waste rock: 50,000 tonnes/day (5:1 ratio)
- Overburden: 20,000 tonnes/day (additional)

**Circular Economy**: Waste rock used for haul road construction, pit backfill

**Transparency**: High (reported in technical studies, environmental permits)

---

#### Phase 2: Ore Processing & Concentration
**Typical Waste Ratio**: 95-98% of input ore becomes tailings

**This is the CRITICAL waste phase** - Sarah's emphasis on circular economy directly applies here.

**Waste Types**:
- **Tailings**: Crushed ore after gold extraction (massive volume)
  - Stored in tailings dams (environmental risk)
  - Contains residual cyanide, heavy metals
  - Particle size: Sand to clay (suspension in water)
  
- **Hazardous chemicals**:
  - Cyanide (sodium/calcium cyanide solutions)
  - Sulfuric acid (for flotation pH control)
  - Heavy metals leached from ore (arsenic, mercury, lead)

**Industry Benchmarks**:
- 1,000 kg ore → 950-980 kg tailings
- Gold recovery rate: 85-95% → remainder lost to tailings
- Tailings density: 1.4-1.8 tonnes/cubic meter

**Example**:
- Process 10,000 tonnes ore/day
- Extract 25 kg gold (at 85% recovery of 3 g/t ore)
- Generate 9,750 tonnes tailings/day
- Tailings dam: 5,400 cubic meters/day (cumulative environmental liability)

**Circular Economy Opportunities**:
- Reprocess old tailings (technology improving, recovering previously uneconomic gold)
- Use tailings for cement production (limited)
- Neutralize and use for mine backfill
- Extract byproduct metals (copper, silver)

**Critical Issue**: **Tailings dam failures** (e.g., Brumadinho 2019, Mariana 2015)
- Environmental catastrophe potential
- Long-term monitoring required (decades after mine closure)

**Transparency**: High (environmental permits require detailed tailings management plans)

---

#### Phase 3: Doré Production
**Typical Waste**: 2-5% of doré input becomes slag

**Waste Types**:
- **Slag**: Silicate byproduct from smelting (contains trace precious metals)
- Can be reprocessed for metal recovery

**Circular Economy**: Slag often sent to refineries for metal recovery

**Transparency**: Medium (company-level aggregates)

---

#### Phase 4: Refining
**Typical Waste**: <1% of input becomes waste

**Waste Types**:
- **Chemical waste**: Spent acids (aqua regia, nitric acid)
- **Metallic waste**: Silver, copper, other impurities removed
- **Filter residues**: Contain trace gold (reprocessed)

**Hazardous Handling**: Requires licensed waste treatment (acid neutralization)

**Circular Economy**: Silver, platinum group metals recovered and sold

**Transparency**: Medium (environmental permits, limited operational detail)

---

#### Phase 8: Recycling & Recovery
**Typical Waste**: 70-85% of e-waste input

**Waste Types**:
- **Plastics, circuit boards** (non-metallic components)
- **Ferrous/non-ferrous scrap** (sorted and sold)
- **Hazardous**: Batteries, leaded solder, brominated flame retardants

**Critical Factor**: E-waste is heterogeneous (unlike ore)
- Phones: 0.3-0.5 g gold per device
- Computers: 1-3 g gold per unit
- Requires pre-processing (dismantling, shredding, sorting)

**Circular Economy**: This IS circular economy - closing the loop

**Transparency**: Medium-high (growing regulatory requirements, WEEE directives in EU/UK)

---

### 2.3 Calculation Methodology

#### For Synthetic Data
```python
# Phase 2: Tailings generation (most critical)
def calculate_phase2_waste(ore_input_kg, ore_grade_g_per_tonne, recovery_rate):
    """
    ore_input_kg: Daily ore throughput (e.g., 10,000,000 kg = 10,000 tonnes)
    ore_grade_g_per_tonne: Gold content (e.g., 3.5 g/t)
    recovery_rate: Extraction efficiency (e.g., 0.85 = 85%)
    """
    # Gold extracted (kg)
    gold_in_ore = (ore_input_kg / 1000) * (ore_grade_g_per_tonne / 1000)
    gold_recovered = gold_in_ore * recovery_rate
    
    # Tailings = almost all the ore
    waste_tailings_kg = ore_input_kg * random.uniform(0.950, 0.980)
    
    # Hazardous waste (cyanide-containing tailings)
    # Typically 200-500 ppm cyanide in tailings slurry
    waste_hazardous_kg = waste_tailings_kg * random.uniform(0.05, 0.15)
    
    # Recycled waste (repurposed for backfill)
    waste_recycled_pct = random.uniform(0.02, 0.08)  # 2-8% (low currently)
    waste_recycled_kg = waste_tailings_kg * waste_recycled_pct
    
    return {
        'waste_material_tailings': waste_tailings_kg,
        'waste_material_hazardous': waste_hazardous_kg,
        'waste_material_recycled': waste_recycled_kg,
        'waste_material_total': waste_tailings_kg + waste_hazardous_kg
    }

# Phase 1: Overburden and waste rock
def calculate_phase1_waste(ore_production_tonnes, waste_to_ore_ratio):
    """
    waste_to_ore_ratio: Typically 3:1 to 20:1 depending on ore grade/mine type
    """
    waste_rock_tonnes = ore_production_tonnes * waste_to_ore_ratio
    waste_rock_kg = waste_rock_tonnes * 1000
    
    # Overburden (topsoil, stored separately)
    overburden_kg = waste_rock_kg * random.uniform(0.15, 0.30)
    
    return {
        'waste_material_overburden': overburden_kg,
        'waste_material_total': waste_rock_kg
    }
```

#### For Real Data (Future)
1. Extract from:
   - Environmental Impact Statements
   - Tailings Management Plans
   - Waste Discharge Permits
   - Sustainability Report sections on waste
2. Convert units (tonnes → kg, cubic meters → kg using density)
3. Classify by hazard level
4. Track circular economy metrics (% recycled, % reprocessed)

---

## Part 3: Energy Metrics (Extended)

### 3.1 Extended Metric Definitions

Beyond the existing `energy_base` field (kWh total), Sarah requires:

| Metric Type | Unit | Description | Applicable Phases |
|-------------|------|-------------|-------------------|
| `energy_consumed_total` | kWh | Total energy use (all sources) | 1, 2, 4, 5 |
| `energy_grid_type` | categorical | AC/DC/Local/Hybrid/Off-grid | 1, 2, 4 |
| `energy_source_clean_pct` | percentage | % from renewables (solar, wind, hydro) | 1, 2, 4 |
| `energy_source_fossil_pct` | percentage | % from fossil fuels (diesel, coal, gas) | 1, 2, 4 |
| `energy_storage_type` | categorical | Battery/Gravitational/Thermal/None | 1 |
| `energy_intensity` | kWh/kg_gold | Energy per unit output | 1, 2, 4 |

**Source**: Sarah doc lines 54-58

### 3.2 Grid Type Classification

| Grid Type | Description | Typical Phases | Example |
|-----------|-------------|----------------|---------|
| **AC_grid** | Connected to national AC grid | 2, 4, 5 | Urban refineries, processing plants near infrastructure |
| **DC_microgrid** | Local DC distribution (often renewable) | 1 | Remote mines with solar/wind + battery |
| **Off_grid_diesel** | Isolated, diesel generators | 1 | Remote mines, pre-grid connection |
| **Hybrid** | Grid + on-site generation (solar/diesel) | 1, 2 | Mines transitioning to renewables |
| **Local** | On-site generation only (no grid) | 1 | Exploration camps, remote operations |

### 3.3 Energy Storage Classification

| Storage Type | Description | Typical Use | Example |
|--------------|-------------|-------------|---------|
| **Lithium_battery** | Li-ion battery banks | Solar/wind smoothing | Off-grid mine with solar array |
| **Pumped_hydro** | Gravitational storage | Load balancing | Large mines near reservoirs |
| **Thermal** | Molten salt, heat storage | Process heat buffering | Smelting operations |
| **Compressed_air** | CAES systems | Industrial scale | Rare in gold mining |
| **None** | No storage, direct consumption | Grid-connected facilities | Most refineries |

### 3.4 Phase-Specific Energy Details

#### Phase 1: Mine Extraction
**Energy Intensity**: 20-50 kWh per tonne ore moved (high variability)

**Energy Mix**:
- **Diesel fuel**: 60-80% (haul trucks, excavators, drills)
- **Grid electricity**: 10-30% (crushers, conveyors, ventilation)
- **Renewables**: 5-15% (growing, solar/wind at some sites)

**Grid Type**: Hybrid or Off_grid_diesel (depends on remoteness)

**Clean Energy Trend**: 
- Major miners committing to renewable transition
- Newmont: 30% renewable by 2030 target
- Barrick: Carbon neutral by 2050 target
- Challenge: Remote locations, heavy mobile equipment (hard to electrify)

**Example**:
- Australian mine: 35% solar + 65% diesel (microgrid with battery storage)
- Canadian mine: 90% hydro grid + 10% backup diesel
- West African mine: 95% diesel (no grid access)

---

#### Phase 2: Ore Processing
**Energy Intensity**: 15-40 kWh per tonne ore processed

**Energy Mix**:
- **Grid electricity**: 70-90% (grinding mills, leach tanks, pumps)
- **Renewables**: 10-30% (where grid is clean or on-site solar)
- **Diesel**: 5-10% (backup generation)

**Grid Type**: AC_grid (most processing plants near infrastructure)

**Major Consumers**:
- Semi-autogenous grinding (SAG) mills: 40-50% of total
- Ball mills: 20-30%
- Pumping (slurry, water): 15-20%
- Leaching aeration: 5-10%

**Clean Energy Potential**: High (stationary load, grid-connectable)

---

#### Phase 4: Refining
**Energy Intensity**: 100-300 kWh per kg refined gold

**Energy Mix**:
- **Grid electricity**: 80-95% (electrolytic cells, furnaces)
- **Natural gas**: 5-15% (smelting furnaces)
- **Renewables**: 10-40% (depends on grid source)

**Grid Type**: AC_grid (refineries in urban/industrial areas)

**Major Consumers**:
- Electrolytic refining: 50-60%
- Smelting furnaces: 20-30%
- HVAC and process control: 10-15%

**Clean Energy Status**: Grid-dependent (European refineries ~50% clean due to grid mix)

---

### 3.5 Calculation Methodology

#### For Synthetic Data
```python
# Energy consumption by phase (kWh/day base)
energy_base = {
    0: 5000,         # Prospecting (minimal - field equipment)
    1: 250000,       # Mining (heavy equipment)
    2: 180000,       # Processing (grinding mills)
    3: 30000,        # Doré smelting
    4: 80000,        # Refining (electrolytic + smelting)
    5: 15000,        # Bar casting
    6: 5000,         # Vaulting (climate control)
    7: 2000,         # Exchange (data centers)
    8: 70000         # Recycling (similar to refining)
}

# Clean energy percentage by phase (varies by region)
def get_clean_energy_pct(phase_id, country):
    """
    Country affects grid mix
    Remote mines: Lower clean %
    Urban facilities: Higher clean % (better grid access)
    """
    base_clean_pct = {
        0: 20,   # Small equipment, some solar
        1: 25,   # Growing renewable adoption
        2: 40,   # Grid-connected, easier to green
        3: 35,
        4: 50,   # Urban location, cleaner grid
        5: 50,
        6: 55,
        7: 60,   # Data centers, some renewable focus
        8: 45
    }
    
    # Country modifiers (example)
    country_modifier = {
        'Norway': 1.8,    # 95%+ hydro grid
        'Iceland': 2.0,   # 100% renewables
        'Canada': 1.4,    # High hydro penetration
        'Australia': 1.2, # Growing solar
        'China': 0.9,     # Coal-heavy grid
        'USA': 1.0,       # Mixed
        'Ghana': 0.7      # Fossil-heavy
    }
    
    clean_pct = base_clean_pct[phase_id] * country_modifier.get(country, 1.0)
    return min(clean_pct, 95)  # Cap at 95% (always some backup diesel)

# Grid type assignment
def assign_grid_type(phase_id, country, remoteness):
    """
    remoteness: 0-100 (0=urban, 100=extremely remote)
    """
    if phase_id in [2, 4, 5, 7]:  # Processing, refining, casting, exchange
        return "AC_grid"  # Always grid-connected
    elif phase_id == 1:  # Mining
        if remoteness > 70:
            return "Off_grid_diesel"
        elif remoteness > 40:
            return "Hybrid"
        else:
            return "AC_grid"
    else:
        return "Local"
```

---

## Part 4: Mapping to NDC Framework

### 4.1 How Environmental Metrics Relate to D-C Parameters

#### Definition (D) Parameters - Constraints
Environmental regulations and standards appear as D-parameters:

**Phase 1 (Mining)**:
- `D4:environmental_regulations` ← water discharge limits, waste rock management
- Stricter regulations = Higher D value = More constrained operation

**Phase 2 (Processing)**:
- `D5:waste_management` ← tailings dam standards, cyanide handling protocols
- Higher waste generation = Higher D value (must manage more waste)

**Phase 4 (Refining)**:
- `D5:waste_recovery` ← acid treatment requirements, precious metal recovery standards

**NDC Impact**:
- High environmental D-parameters without corresponding C-integration = Bottleneck
- Example: Strict tailings standards but limited technology options → High D, Low C → Poor balance

---

#### Contribution (C) Parameters - Integration
Access to clean technology and waste solutions appear as C-parameters:

**Phase 1 (Mining)**:
- `C3:energy_sources` ← diversity of energy options (grid + solar + diesel)
- High clean energy % = Higher C value (more integrated with renewables)

**Phase 2 (Processing)**:
- `C3:water_sources` ← access to multiple water sources, recycling tech
- High recycling rate = Higher C value (better integrated water management)
- `C4:byproduct_markets` ← ability to sell/reuse waste (circular economy)

**Phase 4 (Refining)**:
- `C5:technology_adoption` ← use of clean refining tech, waste recovery systems

**NDC Impact**:
- High C-values in environmental integration = Sustainable operation
- Low C-values = Isolated, limited options, vulnerable to regulation changes

---

### 4.2 Sustainability Index Connection

Sarah's emphasis on sustainability (line 74: circular economy) maps directly to NDC sustainability index:

```
Sustainability_index = 100 / (|D - C|² + E_base)
```

**Environmental Interpretation**:
- **Balanced system** (D ≈ C): 
  - Environmental regulations matched by technology access
  - Example: Strict water limits + excellent recycling tech → Low waste, high efficiency
  
- **D-dominant** (D >> C):
  - Over-regulated relative to available technology
  - Example: Tailings standards require <10 ppm cyanide, but only costly tech available → High energy cost to comply
  
- **C-dominant** (C >> D):
  - Technology outpaces regulation (potentially waste of resources)
  - Example: Advanced recycling capacity but lax standards → Over-investment in compliance

**Water Example**:
```python
Phase 2 with excellent water management:
  D_parameters:
    D5:waste_management = 85 (strict standards)
  C_parameters:
    C3:water_sources = 80 (multiple sources + 75% recycling)
  
  Imbalance = |85 - 80| = 5
  Sustainability_index = 100 / (25 + 10) = 2.86 (excellent!)
  
  Interpretation: Regulations and capabilities aligned → minimal waste

Phase 2 with poor water management:
  D_parameters:
    D5:waste_management = 90 (strict standards)
  C_parameters:
    C3:water_sources = 30 (single source, no recycling)
  
  Imbalance = |90 - 30| = 60
  Sustainability_index = 100 / (3600 + 10) = 0.028 (critical!)
  
  Interpretation: Can't meet standards with available tech → unsustainable
```

---

## Part 5: Data Collection Strategy

### 5.1 Immediate (Synthetic Data)

**Status**: Implemented in `synthetic_data_generator.py`

**Approach**:
- Use industry benchmarks as base values
- Add realistic random variation (±15-30%)
- Phase-appropriate ranges
- Tag as `source_type: simulated`

**Purpose**:
- Frontend development
- Visualization testing
- Scenario modeling
- Identify data gaps

---

### 5.2 Short-Term (Public Company Data)

**Target Companies** (from Sarah's list):
1. **Newmont Corporation**
   - Sustainability reports: https://www.newmont.com/sustainability/
   - Data available: Water (by site), energy (by site), tailings volumes, GHG emissions
   - Quality: High (detailed, site-specific)
   
2. **Barrick Gold**
   - Sustainability reports: https://www.barrick.com/sustainability/
   - Data available: Water stewardship, energy mix, waste management
   - Quality: High (aligned with TCFD, GRI standards)
   
3. **Agnico Eagle**
   - Reports: https://www.agnicoeagle.com/English/sustainability/
   - Focus: Canadian operations (high data quality)
   
4. **UK Royal Mint** (Recycling)
   - Reports: https://www.royalmint.com/aboutus/policies-and-guidelines/
   - Data: E-waste volumes, precious metal recovery rates
   - Quality: Medium (limited public detail)

**Extraction Method**:
1. Download latest sustainability reports (PDF)
2. Parse tables: "Water Withdrawal by Source", "Energy Consumption", "Waste Generated"
3. Attribute to phases based on operational description
4. Store in CSV with source attribution

**Tools**:
- `src/ingest/company_scraper.py` (to develop)
- PDF parsing: `pdfplumber` or `tabula-py`
- Manual review for accuracy

---

### 5.3 Medium-Term (Industry Aggregates)

**Sources**:
1. **World Gold Council**
   - Annual sustainability reviews
   - Aggregate data (not site-specific)
   - Benchmarks for water/energy intensity
   
2. **ICMM (International Council on Mining & Metals)**
   - Performance expectations
   - Industry averages
   
3. **Technical Reports**
   - NI 43-101 (Canada), JORC (Australia)
   - Feasibility studies include water balance, energy requirements
   - Public for listed companies
   
4. **Academic Literature**
   - Metallurgical journals
   - Case studies of specific technologies

**Quality**: Medium (good for validation, not real-time)

---

### 5.4 Long-Term (Paid Data & Direct Contacts)

**Potential Paid Sources**:
- **SNL Metals & Mining** (S&P Global): Comprehensive company-level data
- **Wood Mackenzie**: Energy transition tracking for mining
- **CDP (Carbon Disclosure Project)**: Climate and water security data (some free)

**Direct Contacts** (if Sarah has access):
- Company sustainability teams
- Bristol One City Plan members
- UK Royal Mint recycling program managers

**Quality**: High (but requires budget or relationships)

---

## Part 6: Uncertainty and Limitations

### 6.1 Data Availability Issues

| Metric | Transparency | Common Gap | Workaround |
|--------|--------------|------------|------------|
| Water consumed (Phase 1-2) | High | Site-specific breakdown | Use company aggregates, estimate by site size |
| Water recycled (Phase 2) | Medium | Closed-loop % | Infer from technology type (CIL plants ~75%) |
| Tailings composition (Phase 2) | Medium | Chemical breakdown | Use regional ore geology as proxy |
| Energy mix (Phase 1) | Medium | Diesel vs. renewable % | Estimate from company targets, grid data |
| Waste to landfill (Phase 2) | Low | Circular economy % | Mark as OPAQUE, use industry avg (5%) |

### 6.2 Regional Variability

**Water Scarcity Context**:
- Australian mines (arid): Higher water intensity, more recycling investment
- Canadian mines (water-rich): Lower recycling rates historically
- Chilean mines (Atacama Desert): Seawater desalination, very high recycling

**Grid Carbon Intensity**:
- Norway refinery: 0.01 kg CO2/kWh (hydro grid)
- China refinery: 0.60 kg CO2/kWh (coal grid)
- Same energy consumption, 60x different carbon footprint

**Implication**: Can't compare absolute sustainability across regions without context

---

### 6.3 Temporal Changes

**Technology Evolution**:
- 2010: Typical Phase 2 water recycling ~50%
- 2025: Typical Phase 2 water recycling ~75%
- 2030 target: 85%+ (company commitments)

**Implication**: Historical data may underestimate current performance

**Regulatory Tightening**:
- Tailings dam standards stricter post-2019 disasters
- Cyanide discharge limits reduced in many jurisdictions
- GHG reporting now mandatory for large mines

**Implication**: D-parameters (constraints) increasing over time → Need for C-parameters (technology integration) to rise in parallel

---

## Part 7: Compliance with Project Rules

### 7.1 Rule Set Alignment

✅ **Rule Set 1: Separation of Concerns**
- All metrics are physical (litres, kg, kWh)
- No pricing, no margins
- Value interpretation deferred

✅ **Rule Set 2: Phase-Based Modeling**
- Every metric assigned to specific phases
- No aggregates that obscure phase boundaries

✅ **Rule Set 3: Data-First Discipline**
- Units specified for all metrics
- Source attribution required
- Missing data marked as OPAQUE

✅ **Rule Set 4: Transparency Classification**
- Water/energy: High transparency (Phase 1-2)
- Waste recycling: Medium-low (structural opacity in circular economy tracking)

✅ **Rule Set 7: Schema-First Development**
- All metrics tabulated in CSV format
- Field definitions provided

✅ **Rule Set 9: Reproducibility**
- Calculation methods documented
- Data sources specified
- Industry benchmarks cited

---

## Part 8: Future Enhancements

### 8.1 Carbon Footprint Calculation (Phase B)

Once water/waste/energy data established, calculate:
```
carbon_intensity_kg_CO2_per_kg_gold = 
    (energy_consumed_kWh × grid_carbon_intensity_kg_CO2_per_kWh) +
    (diesel_consumed_L × 2.68_kg_CO2_per_L) +
    (process_emissions_kg_CO2)  # e.g., lime calcination in processing
```

**Note**: This is interpretive (carbon pricing, climate impact) → Deferred per Rule Set 8

### 8.2 Biodiversity Impact (Phase C)

Sarah mentions "coordinates/hectares for biodiversity" (lines 71-72):
- Land use per phase (hectares)
- Habitat disturbance (hectares affected)
- Protected area offsets (hectares compensated)

**Status**: Valuable but lower priority than water/waste/energy

### 8.3 Social Metrics (Phase D)

Sarah includes "Person Hours" and "Payroll" (lines 59-61):
- Map to C-parameters (labor flexibility, skill diversity)
- Enable social sustainability analysis

**Status**: Medium priority, defer until environmental metrics stable

---

## References

### Industry Standards
- ICMM Water Reporting Framework (2021)
- World Gold Council: Responsible Gold Mining Principles (2019)
- GRI Standards: 303 (Water), 306 (Waste), 302 (Energy)
- LBMA Responsible Sourcing Programme

### Company Reports
- Newmont Sustainability Report 2023-2024
- Barrick Sustainability Report 2023
- AngloGold Ashanti ESG Report 2023

### Technical
- NI 43-101 Technical Reports (Canadian listings)
- JORC Code Technical Reports (Australian listings)
- Marsden & House (2006): "The Chemistry of Gold Extraction" (refining water use)

### Regulatory
- European WEEE Directive (e-waste recycling)
- US EPA: Hardrock Mining Environmental Regulations
- ICMM Tailings Governance Framework (2020)

---

**Document Status**: Initial methodology complete  
**Next**: Implement in `synthetic_data_generator.py`, test with frontend  
**Review Date**: After first real data ingestion (Newmont/Barrick)

