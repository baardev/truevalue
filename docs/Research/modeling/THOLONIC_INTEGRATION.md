# Tholonic N-D-C Framework Integration Guide

## Overview

The gold supply chain project now incorporates the **Tholonic Framework** for modeling complex adaptive systems using N-D-C (Negotiation-Definition-Contribution) dynamics.

---

## Core Concepts

### The Three Forces

#### N (Negotiation) - Emergent Reality
- **What it is**: The actual operational state that emerges from D-C interaction
- **In supply chain**: Current inventory levels, throughput rates, operational metrics
- **Formula**: `N = √(D × C) × balance_factor`
- **Meaning**: What actually happens when constraints meet integration
- **Scale**: 50-350 (typical operational range 150-280)
- **NOT directly measured** - calculated from D and C

#### D (Definition) - Constraints & Boundaries
- **What it is**: All limitations, specifications, standards, boundaries
- **In supply chain**: Ore grade requirements, purity standards, capacity limits, regulations
- **Growth pattern**: Exponential (self-referential, internally focused)
- **Cost**: Energy to maintain boundaries, reduced adaptability
- **Scale**: 0-100 per parameter, sum of 4-5 parameters = 150-350 typical
- **Measured by**: Intensity/stringency of each constraint parameter

#### C (Contribution) - Integration & Flow
- **What it is**: All connections, relationships, flows, exchanges
- **In supply chain**: Supplier networks, logistics flexibility, information systems, market access
- **Growth pattern**: Linear (relational, externally focused)
- **Cost**: Energy to maintain connections, coordination overhead
- **Scale**: 0-100 per parameter, sum of 4-5 parameters = 150-350 typical
- **Measured by**: Strength/diversity of each integration parameter

---

## Fundamental Principle: Sustainability Through Balance

### The Energy Equation

```
Sustainability = 1 / Energy_cost
Energy_cost = |D - C|² + E_base
```

**Key Insight**: Systems are most sustainable when **D ≈ C** (balanced)

---

## How N-D-C Values Are Calculated

### Scale and Range

All values use a **0-500 theoretical scale** (typical operational range: **50-350**):

| Value | Typical Range | Unit | Purpose |
|-------|---------------|------|---------|
| **D (Definition)** | 150-350 | index | Sum of constraint parameters |
| **C (Contribution)** | 150-350 | index | Sum of integration parameters |
| **N (Negotiation)** | 120-280 | index | Calculated operational capacity |
| **Balance Score** | 0-100 | percent | Proximity of D to C |
| **Sustainability** | 0.01-3.0 | index | Inverse of energy cost |

### Step-by-Step Calculation

#### 1. Measure Individual D Parameters (0-100 scale each)

Each constraint parameter is scored 0-100 based on intensity:

**Example - Phase 1 (Mining):**
```
D1: ore_grade_requirements      = 85  (strict 5g/t minimum)
D2: extraction_method_specs     = 70  (specific protocols required)
D3: safety_standards            = 90  (high safety requirements)
D4: environmental_regulations   = 65  (moderate environmental rules)
D5: production_capacity_limits  = 80  (near maximum capacity)

D_total = 85 + 70 + 90 + 65 + 80 = 390
```

**Individual Parameter Scale:**
- **0-20**: Minimal/negligible constraint
- **20-40**: Low constraint
- **40-60**: Moderate constraint ✓ (typical)
- **60-80**: High constraint
- **80-100**: Very high/maximum constraint

#### 2. Measure Individual C Parameters (0-100 scale each)

Each integration parameter is scored 0-100 based on strength/diversity:

**Example - Phase 1 (Mining):**
```
C1: equipment_suppliers         = 60  (6 alternative suppliers)
C2: labor_flexibility          = 55  (moderate workforce adaptability)
C3: energy_sources             = 50  (2-3 energy options)
C4: transportation_options     = 65  (multiple transport routes)
C5: market_access              = 70  (well-connected to buyers)

C_total = 60 + 55 + 50 + 65 + 70 = 300
```

**Individual Parameter Scale:**
- **0-20**: Minimal/isolated
- **20-40**: Low integration
- **40-60**: Moderate integration ✓ (typical)
- **60-80**: High integration
- **80-100**: Maximum integration

#### 3. Calculate D_total and C_total

Simply sum the individual parameters:

```
D_total = Σ D_i  (sum of all D parameters)
C_total = Σ C_j  (sum of all C parameters)
```

**Typical Totals:**
- **Balanced system**: D ≈ 250, C ≈ 250
- **D-dominant system**: D ≈ 400, C ≈ 180 (over-constrained)
- **C-dominant system**: D ≈ 180, C ≈ 400 (over-integrated)

#### 4. Calculate Imbalance

```python
imbalance = abs(D_total - C_total)
```

**Example:**
- D=390, C=300 → imbalance = 90
- D=250, C=245 → imbalance = 5 (excellent!)
- D=420, C=180 → imbalance = 240 (critical!)

#### 5. Calculate Balance Score (0-100)

```python
balance_score = 100 × exp(-2 × imbalance / max(D_total, C_total))
```

**How it works:**
- When D = C (imbalance = 0): balance_score = 100
- Small imbalance: balance_score 80-95
- Large imbalance: balance_score < 50

**Example:**
```
D=390, C=300:
  imbalance = 90
  balance_score = 100 × exp(-2 × 90/390) = 100 × exp(-0.46) = 63.2
```

**Balance Score Interpretation:**
- **95-100**: Excellent balance (D ≈ C)
- **80-95**: Good balance ✓ (baseline)
- **60-80**: Fair balance
- **40-60**: Poor balance
- **0-40**: Critical imbalance

#### 6. Calculate Sustainability Index

```python
energy_cost = imbalance² + E_base
sustainability = 100 / energy_cost
```

Where `E_base` is the minimum baseline energy (typically 10.0)

**Example:**
```
D=390, C=300:
  imbalance = 90
  energy_cost = 90² + 10 = 8,100 + 10 = 8,110
  sustainability = 100 / 8,110 = 0.0123

D=250, C=245:
  imbalance = 5
  energy_cost = 5² + 10 = 25 + 10 = 35
  sustainability = 100 / 35 = 2.857 (much better!)
```

**Sustainability Interpretation:**
- **>2.0**: Excellent (minimal energy cost)
- **1.0-2.0**: Good ✓ (baseline)
- **0.5-1.0**: Fair
- **0.1-0.5**: Poor
- **<0.1**: Critical (unsustainable)

#### 7. Calculate N-State (Emergent Equilibrium)

```python
balance_factor = balance_score / 100
N = sqrt(D_total × C_total) × balance_factor
```

**Example:**
```
D=390, C=300, balance_score=63.2:
  balance_factor = 0.632
  N = sqrt(390 × 300) × 0.632
  N = sqrt(117,000) × 0.632
  N = 342.1 × 0.632 = 216.2

D=250, C=245, balance_score=95:
  balance_factor = 0.95
  N = sqrt(250 × 245) × 0.95
  N = 247.5 × 0.95 = 235.1
```

**N-State Interpretation:**
- **N ≈ √(D × C)**: System operating near theoretical maximum
- **N << √(D × C)**: System constrained by imbalance
- **Higher N**: Greater operational capacity
- **Lower N**: Reduced capacity due to D-C friction

### Complete Example: Phase 2 (Ore Processing)

**Given:**
```
D1: recovery_rate_target       = 85
D2: process_specifications     = 70
D3: purity_standards          = 90
D4: throughput_capacity       = 80
D5: waste_management          = 75

C1: chemical_suppliers        = 45
C2: technology_integration    = 60
C3: water_sources            = 50
C4: byproduct_markets        = 40
C5: information_systems      = 55
```

**Calculations:**
```
D_total = 85 + 70 + 90 + 80 + 75 = 400
C_total = 45 + 60 + 50 + 40 + 55 = 250

imbalance = |400 - 250| = 150

balance_score = 100 × exp(-2 × 150/400) = 100 × exp(-0.75) = 47.2

energy_cost = 150² + 10 = 22,510
sustainability = 100 / 22,510 = 0.0044 (very low!)

balance_factor = 0.472
N = sqrt(400 × 250) × 0.472 = 316.2 × 0.472 = 149.3
```

**Diagnosis:**
- **Type**: D-dominant (over-constrained)
- **Severity**: 150/400 = 37.5% imbalance (critical!)
- **Issue**: Too many rigid specifications, insufficient supplier flexibility
- **Recommendation**: Increase C (add suppliers) OR reduce D (relax specifications)
- **N-state**: Only 149.3 capacity vs. theoretical 316.2 (53% efficiency loss!)

---

## Real-World Mapping Examples

### Mining Operation (Phase 1)

**Synthetic Values:**
- D_total = 270 (moderate constraints)
- C_total = 260 (moderate integration)
- N = 255 (healthy capacity)

**Real-World Equivalents:**
- D: Operating at 5 g/t ore grade with standard safety protocols
- C: Has 5-6 equipment suppliers, 3 energy sources, multiple transport options
- N: Achieving 85% of theoretical production capacity

### Vaulting Operation (Phase 6) - Bottleneck

**Synthetic Values:**
- D_total = 420 (very high constraints)
- C_total = 180 (low integration)
- N = 150 (severely limited capacity)

**Real-World Equivalents:**
- D: Strict security, insurance limits, jurisdictional compliance, capacity constraints
- C: Limited vault network, single transport provider, minimal client access
- N: Operating at only 40% capacity due to bottlenecks

### Why Balance Matters

#### Balanced System (D ≈ C)
- **Low energy cost**: Minimal friction between constraint and flow
- **High sustainability**: Can maintain state with minimal resources
- **Resilient**: Absorbs perturbations effectively
- **Efficient**: Maximum output per energy input

#### D-Dominant System (D >> C)
- **Symptoms**: Over-constrained, rigid, isolated, internally focused
- **Failure mode**: Resource depletion, obsolescence, inability to adapt
- **Example**: Mining operation with strict quality standards but limited supplier flexibility
- **Fix**: Increase C (enhance integration) OR decrease D (relax constraints)

#### C-Dominant System (C >> D)
- **Symptoms**: Over-integrated, unstable, boundary dissolution, identity loss
- **Failure mode**: Structural collapse, resource dissipation, exploitation
- **Example**: Refinery with extensive partnerships but insufficient process control
- **Fix**: Increase D (strengthen boundaries) OR decrease C (reduce connections)

---

## Gold Supply Chain Mapping

### Phase-by-Phase N-D-C Structure

#### Phase 0: Geological Prospecting
- **N**: Identified reserves, exploration targets
- **D**: Ore grade thresholds, geological certainty requirements, cost limits
- **C**: Survey technology access, data sharing, industry partnerships
- **Balance Target**: 0.75 (moderate balance acceptable given uncertainty)

#### Phase 1: Mine Extraction
- **N**: Actual production volume, cost per ounce
- **D**: Ore grade, extraction methods, safety/environmental standards, capacity
- **C**: Equipment suppliers, labor flexibility, energy sources, transportation
- **Balance Target**: 0.85 (high balance for operational stability)

#### Phase 2: Ore Processing & Concentration
- **N**: Recovery rate achieved, throughput
- **D**: Recovery targets, process specs, purity standards, capacity, waste management
- **C**: Chemical suppliers, technology integration, water sources, byproduct markets
- **Balance Target**: 0.90 (very high balance - critical transformation phase)

#### Phase 3: Doré Production
- **N**: Doré bars produced, purity range achieved
- **D**: Purity specifications, smelting protocols, bar weights, quality control
- **C**: Refinery network, transport providers, assay services, trade relationships
- **Balance Target**: 0.70 (moderate - buffered by inventory)

#### Phase 4: Refining
- **N**: Fine gold output, fineness achieved
- **D**: Fineness standards (99.99%), accreditation, capacity, process control
- **C**: Client base, equipment vendors, certification bodies, market integration
- **Balance Target**: 0.75 (moderate-high balance)

#### Phase 5: Bar Casting & Assay
- **N**: Certified bars, serial numbers assigned
- **D**: Bar specifications, assay precision, serial protocols, storage standards
- **C**: Exchange relationships, vault network, transport logistics, documentation
- **Balance Target**: 0.80 (high - standardization critical)

#### Phase 6: Logistics & Vaulting ⚠️
- **N**: Vaulted inventory, custody transfers
- **D**: Vault capacity, security protocols, insurance requirements, compliance
- **C**: Vault network, transport flexibility, insurance access, client access
- **Balance Target**: 0.50 (LOW - structural opacity, custodial secrecy)
- **Note**: This is the system's weakest link (low transparency + low balance target)

#### Phase 7: Exchange Registration (COMEX)
- **N**: Registered inventory, eligible inventory, daily changes
- **D**: Exchange standards, registration requirements, warehouse specs, delivery protocols
- **C**: Market participants, clearing systems, information transparency, settlement
- **Balance Target**: 0.85 (high - regulatory framework ensures balance)

---

## Phase Interactions: Constraint Propagation

### How Imbalances Cascade

When **Phase i** has D >> C (over-constrained):
1. **Downstream effect**: Phase i+1 must increase its D to match upstream constraints
2. **Example**: Strict ore processing standards → refinery must maintain tight quality control
3. **Coupling strength**: Defined by `d_coupling` (0-1 scale)

When **Phase i** has C >> D (over-integrated):
1. **Downstream effect**: Phase i+1 must increase its C to handle flow
2. **Example**: High supplier diversity → increased coordination requirements downstream
3. **Coupling strength**: Defined by `c_coupling` (0-1 scale)

### Interaction Types

- **Direct**: Changes propagate immediately (tight coupling)
- **Buffered**: Inventory or time delays dampen propagation
- **Constrained**: One phase physically limits another (bottleneck)

---

## Evaluating Transactions/Processes with N-D-C

### Step-by-Step Evaluation

#### 1. Identify D Parameters
For the transaction/process, list all constraints:
- Specifications (what standards must be met?)
- Capacity limits (what can physically be done?)
- Regulations (what must legally be done?)
- Quality requirements (what defines acceptable?)

**Quantify each**: 0-100 scale based on stringency

#### 2. Identify C Parameters
For the transaction/process, list all integrations:
- Supplier relationships (how many? how flexible?)
- Information flows (how connected? how fast?)
- Distribution channels (how diverse? how accessible?)
- Partnerships (how collaborative?)

**Quantify each**: 0-100 scale based on strength/diversity

#### 3. Calculate Totals
```python
D_total = sum(D_parameters.values())
C_total = sum(C_parameters.values())
```

#### 4. Calculate Balance
```python
imbalance = abs(D_total - C_total)
balance_score = 100 * exp(-2 * imbalance / max(D_total, C_total))
```

#### 5. Calculate Sustainability
```python
energy_cost = imbalance² + 10.0
sustainability_index = 100 / energy_cost
```

#### 6. Diagnose
```python
if balance_score < 60:
    if D_total > C_total:
        issue = "Over-constrained: Need more integration"
        recommendation = "Increase supplier diversity, logistics flexibility, or information sharing"
    else:
        issue = "Over-integrated: Need more structure"
        recommendation = "Strengthen specifications, quality standards, or boundaries"
```

#### 7. Calculate N-State
```python
N = sqrt(D_total * C_total) * (balance_score / 100)
```

This N-value represents the **actual operational capacity** given current D-C configuration.

### Example: Evaluating a Doré Shipment (Phase 3→4)

```python
# Transaction: Ship doré from mine to refinery

D_parameters = {
    'purity_requirement': 85,  # Must be 80-90% gold
    'weight_specification': 90, # Strict bar weight tolerance
    'documentation': 95,        # Extensive paperwork required
    'insurance_requirement': 80 # High security standards
}
D_total = 350

C_parameters = {
    'transport_options': 40,    # Limited carriers (security)
    'refinery_network': 60,     # Multiple refineries available
    'information_tracking': 70, # Real-time GPS monitoring
    'trade_relationships': 50   # Established contracts
}
C_total = 220

# Analysis
imbalance = |350 - 220| = 130
balance_score = 100 * exp(-2 * 130/350) = 48.7  # LOW!

# Diagnosis: D-dominant (over-constrained)
# Issue: Too many restrictions, insufficient integration
# Recommendation: Increase transport flexibility or reduce documentation burden
```

---

## Using the Simulation Engine

### Basic Usage

```python
from src.simulation.tholonic_engine import Thologram
from pathlib import Path

# Load supply chain
schema = Path("schema/supply_chain_phases_ndc.csv")
interactions = Path("schema/phase_interactions_ndc.csv")

thologram = Thologram(schema)
thologram.load_interactions(interactions)

# Check system health
sustainability = thologram.calculate_system_sustainability()
bottlenecks = thologram.identify_bottlenecks()

# Run simulation with perturbation
perturbations = {
    10: {  # At time step 10
        2: {  # Phase 2 (Ore Processing)
            'D': {'D4:throughput_capacity': 90}  # Capacity constraint tightens
        }
    }
}

history = thologram.run_simulation(duration=50, perturbations_schedule=perturbations)
```

### Optimization

```python
from src.simulation.balance_optimizer import BalanceOptimizer

# Define current state
D_params = {
    'recovery_rate_target': 85,
    'process_specifications': 70,
    'purity_standards': 90
}
C_params = {
    'supplier_diversity': 45,
    'technology_integration': 60,
    'information_systems': 50
}

# Optimize for sustainability
optimizer = BalanceOptimizer(D_params, C_params)
result = optimizer.optimize_gradient_ascent(iterations=100)

print(f"Optimized D: {result['D_total']}")
print(f"Optimized C: {result['C_total']}")
print(f"Balance achieved: {result['balance']}")
```

---

## Sustainability Metrics Dashboard

### Key Metrics to Monitor

1. **Balance Score** (0-100)
   - Target: >60 (acceptable), >80 (excellent)
   - Red flag: <40

2. **Sustainability Index** (higher is better)
   - Baseline: ~10 (typical)
   - Target: >15 (efficient)
   - Red flag: <5 (unsustainable)

3. **D-C Imbalance** (absolute)
   - Target: <20% of max(D,C)
   - Red flag: >50%

4. **System Health Score** (0-100)
   - Excellent: >80
   - Good: 60-80
   - Fair: 40-60
   - Poor: 20-40
   - Critical: <20

5. **Bottleneck Count**
   - Target: 0-1 phases with severe imbalance
   - Red flag: >3 phases

---

## Frontend Integration

### Data Contract Extension

The frontend can now request:

```javascript
// GET /api/v1/phase/{id}/ndc
{
  "phase_id": 2,
  "D_parameters": {
    "D1:recovery_rate_target": 85,
    "D2:process_specifications": 70,
    // ...
  },
  "C_parameters": {
    "C1:chemical_suppliers": 45,
    "C2:technology_integration": 60,
    // ...
  },
  "D_total": 325,
  "C_total": 195,
  "N": 187.5,
  "balance_score": 52.3,
  "sustainability_index": 0.46,
  "diagnosis": {
    "type": "D-dominant",
    "severity": 0.4,
    "recommendation": "Increase supplier diversity and information systems"
  }
}
```

### Visualization Recommendations

1. **Balance Gauge**: For each phase, show D vs C as dual horizontal bars
2. **Sustainability Heat Map**: Color phases by sustainability index
3. **Interaction Flow**: Sankey diagram showing how imbalances propagate
4. **Optimization Path**: Animated trajectory showing balance improvement
5. **System Health Dial**: Overall health score (0-100) with status indicator

---

## References

- Original framework: `/home/jw/books/tholonia/Tholonic_Framework_Supply_Chain_Application.md`
- Implementation: `src/simulation/tholonic_engine.py`
- Optimization: `src/simulation/balance_optimizer.py`
- Schema: `schema/supply_chain_phases_ndc.csv`

---

**Document Status**: Implementation Complete  
**Next**: Frontend integration and real-time monitoring dashboard

