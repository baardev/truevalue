# N-D-C Value Calculation Reference

## Quick Reference Guide

This document explains exactly how D_value, C_value, and N_value are calculated in the gold supply chain model.

---

## TL;DR

- **D_value** = Sum of constraint parameters (0-100 each) → typical total: 150-350
- **C_value** = Sum of integration parameters (0-100 each) → typical total: 150-350
- **N_value** = `√(D × C) × (balance_score/100)` → typical: 120-280
- **Scale**: Dimensionless index (relative, not absolute units)
- **Purpose**: Compare balance, identify bottlenecks, track changes over time

---

## The Math (Simple Version)

### 1. Measure Constraints (D)

Add up all constraint parameters:

```
D_total = D₁ + D₂ + D₃ + D₄ + D₅
```

**Example:**
```
Mining Constraints:
  Ore grade requirement     = 85
  Extraction method specs   = 70
  Safety standards         = 90
  Environmental rules      = 65
  Capacity limits         = 80
  ─────────────────────────
  D_total                 = 390
```

### 2. Measure Integrations (C)

Add up all integration parameters:

```
C_total = C₁ + C₂ + C₃ + C₄ + C₅
```

**Example:**
```
Mining Integrations:
  Equipment suppliers      = 60
  Labor flexibility       = 55
  Energy sources         = 50
  Transport options      = 65
  Market access         = 70
  ─────────────────────────
  C_total              = 300
```

### 3. Calculate Balance Score

How close are D and C?

```python
imbalance = |D_total - C_total|
balance_score = 100 × e^(-2 × imbalance / max(D, C))
```

**Example:**
```
imbalance = |390 - 300| = 90
balance_score = 100 × e^(-2 × 90/390)
              = 100 × e^(-0.46)
              = 63.2
```

### 4. Calculate N-State

What operational capacity emerges?

```python
N = √(D_total × C_total) × (balance_score / 100)
```

**Example:**
```
N = √(390 × 300) × 0.632
  = 342.1 × 0.632
  = 216.2
```

---

## Individual Parameter Scoring (0-100)

### Definition (D) Parameters

Score each constraint 0-100 based on **intensity/stringency**:

| Score | Intensity | Example |
|-------|-----------|---------|
| 0-20 | Minimal | Informal guidelines, flexible standards |
| 20-40 | Low | Basic requirements, some flexibility |
| 40-60 | Moderate | Standard protocols, typical enforcement |
| 60-80 | High | Strict protocols, strong enforcement |
| 80-100 | Maximum | Absolute requirements, zero tolerance |

**Examples:**
- **Ore grade = 85**: Must maintain 5 g/t minimum (strict, no exceptions)
- **Safety standards = 90**: Comprehensive safety protocols, frequent audits
- **Process specs = 60**: Defined protocols but some operational flexibility

### Contribution (C) Parameters

Score each integration 0-100 based on **strength/diversity**:

| Score | Strength | Example |
|-------|----------|---------|
| 0-20 | Isolated | Single option, no alternatives |
| 20-40 | Low | 2 options, limited flexibility |
| 40-60 | Moderate | 3-5 options, reasonable diversity |
| 60-80 | High | 6-10 options, good connectivity |
| 80-100 | Maximum | 10+ options, full integration |

**Examples:**
- **Suppliers = 60**: 6 alternative equipment suppliers, established relationships
- **Transport = 40**: 2-3 transport routes available
- **Market access = 85**: Connected to multiple exchanges, broad buyer network

---

## Interpreting the Results

### D_total (Total Constraints)

| Range | Interpretation | Action |
|-------|----------------|--------|
| 50-150 | Very flexible | May lack structure |
| 150-250 | Low-moderate | Room for optimization |
| 250-350 | Normal/healthy | ✓ Baseline |
| 350-450 | Highly constrained | Monitor stress |
| 450+ | Over-constrained | Urgent: reduce D or increase C |

### C_total (Total Integration)

| Range | Interpretation | Action |
|-------|----------------|--------|
| 50-150 | Isolated | Increase connections |
| 150-250 | Low-moderate | Build relationships |
| 250-350 | Normal/healthy | ✓ Baseline |
| 350-450 | Highly integrated | Monitor complexity |
| 450+ | Over-integrated | May lose focus/identity |

### N_value (Operational Capacity)

| Range | Interpretation | Efficiency |
|-------|----------------|------------|
| 50-120 | Severely limited | <40% |
| 120-200 | Constrained | 40-60% |
| 200-280 | Healthy | 70-90% ✓ |
| 280-350 | High capacity | >90% |

**Key Insight:** N tells you what percentage of theoretical maximum the system achieves given current D-C balance.

### Balance Score (0-100)

| Score | Status | D-C Relationship |
|-------|--------|------------------|
| 95-100 | Excellent | D ≈ C (±5%) |
| 80-95 | Good ✓ | D ≈ C (±10%) |
| 60-80 | Fair | Moderate imbalance |
| 40-60 | Poor | Significant imbalance |
| 0-40 | Critical | Severe imbalance |

### Sustainability Index

| Value | Status | Energy Cost |
|-------|--------|-------------|
| >2.0 | Excellent | Minimal |
| 1.0-2.0 | Good ✓ | Low |
| 0.5-1.0 | Fair | Moderate |
| 0.1-0.5 | Poor | High |
| <0.1 | Critical | Unsustainable |

---

## Complete Worked Example

### Scenario: Phase 6 Bottleneck

**Step 1: Measure D parameters**
```
D1: vault_capacity           = 70
D2: security_protocols       = 95
D3: insurance_requirements   = 85
D4: custody_standards        = 90
D5: jurisdictional_compliance = 80

D_total = 420
```

**Step 2: Measure C parameters**
```
C1: vault_network_size       = 35
C2: transport_flexibility    = 30
C3: insurance_access        = 45
C4: client_access           = 35
C5: information_opacity     = 35

C_total = 180
```

**Step 3: Calculate imbalance**
```
imbalance = |420 - 180| = 240
```

**Step 4: Calculate balance score**
```
balance_score = 100 × e^(-2 × 240/420)
              = 100 × e^(-1.14)
              = 31.9 (CRITICAL!)
```

**Step 5: Calculate sustainability**
```
energy_cost = 240² + 10 = 57,610
sustainability = 100 / 57,610 = 0.0017 (VERY LOW!)
```

**Step 6: Calculate N-state**
```
N = √(420 × 180) × 0.319
  = 274.95 × 0.319
  = 87.7 (SEVERELY LIMITED!)
```

**Diagnosis:**
- **Type**: D-dominant (over-constrained by 133%)
- **Issue**: Extremely high security/compliance vs. minimal network integration
- **Impact**: Only 32% efficiency (87.7 vs theoretical 274.95)
- **Fix**: Increase vault network OR reduce custody requirements

---

## Why This Scale?

### Design Rationale

1. **0-100 for parameters**: Intuitive (like percentages)
2. **Sum to 200-300**: Typical for 4-5 parameters per dimension
3. **Distinguishable states**: Easy to see balanced (250/250) vs. imbalanced (420/180)
4. **Natural variation**: ±15 points daily = ~6% (realistic fluctuation)
5. **No physical units**: Dimensionless index for relative comparison

### What It's NOT

- ❌ **Not absolute metrics**: Don't compare across different supply chains
- ❌ **Not physical units**: Not tons, dollars, or ounces
- ❌ **Not predictive**: Shows current state, not future outcomes
- ❌ **Not exhaustive**: Simplified model of complex reality

### What It IS

- ✅ **Relative comparison**: Compare phases within same supply chain
- ✅ **Pattern recognition**: Identify imbalances, bottlenecks, trends
- ✅ **Optimization guidance**: Shows where to adjust D or C
- ✅ **System health indicator**: Balance score reveals sustainability

---

## Data in CSV Files

When you see:
```csv
phase_id,d_value,c_value,n_value,balance_score,sustainability_index
2,276.49,270.79,262.57,95.96,2.3521
```

**This means:**
- Phase 2 (Ore Processing) has:
  - Total constraints = 276.49
  - Total integration = 270.79
  - Operational capacity = 262.57 (emerged from D×C interaction)
  - Balance = 95.96% (excellent! D ≈ C)
  - Sustainability = 2.35 (very efficient, low energy cost)

**Interpretation:**
Healthy, balanced phase operating at ~95% efficiency.

---

## Quick Diagnostic Checklist

1. **Check balance_score**:
   - <60? → System has problem
   - 60-80? → Fair, room for improvement
   - >80? → Good balance ✓

2. **Compare D to C**:
   - D >> C? → Over-constrained (rigid, isolated)
   - C >> D? → Over-integrated (unstable, unfocused)
   - D ≈ C? → Balanced ✓

3. **Check N vs. √(D×C)**:
   - N close to √(D×C)? → High efficiency
   - N << √(D×C)? → Imbalance limiting capacity

4. **Check sustainability**:
   - <0.5? → High energy cost (unsustainable)
   - >1.0? → Low energy cost ✓

---

## Common Patterns

### Healthy System
```
D = 250, C = 245
Balance = 95, Sustainability = 2.0, N = 237
→ Minimal imbalance, high efficiency
```

### D-Dominant (Over-Constrained)
```
D = 400, C = 180
Balance = 30, Sustainability = 0.002, N = 87
→ Too rigid, isolated, unsustainable
```

### C-Dominant (Over-Integrated)
```
D = 180, C = 400
Balance = 30, Sustainability = 0.002, N = 87
→ Too diffuse, unfocused, unstable
```

---

## Reference Equations

```python
# Core calculations
D_total = sum(D_parameters)
C_total = sum(C_parameters)
imbalance = abs(D_total - C_total)

# Balance and sustainability
balance_score = 100 * exp(-2 * imbalance / max(D_total, C_total))
energy_cost = imbalance**2 + 10
sustainability = 100 / energy_cost

# N-state (emergent capacity)
balance_factor = balance_score / 100
N = sqrt(D_total * C_total) * balance_factor
```

---

**For more details, see:**
- `docs/PDI/THOLONIC_INTEGRATION.md` - Complete framework guide
- `src/data/synthetic_data_generator.py` - Implementation code
- `/home/jw/books/tholonia/Tholonic_Framework_Supply_Chain_Application.md` - Theoretical foundation

