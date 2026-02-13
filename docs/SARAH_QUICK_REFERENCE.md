# Sarah Document Quick Reference
## Integration Summary for tv-sarah.txt

---

## TL;DR

✅ **70% Already Aligned** - Your framework matches Sarah's philosophy  
⚠️ **30% Requires Extension** - Add environmental metrics + entities + recycling phase  
🎯 **Action**: Start with entity registry + water/waste metrics this week

---

## What's Already Integrated

| Sarah's Requirement | Your Implementation | File |
|--------------------|--------------------|------|
| Physical flow first | Rule Set 1: Separation of Concerns | docs/SUPPLY_CHAIN_RULES.md |
| Phase-based model | 8 phases (0-7) | schema/supply_chain_phases_ndc.csv |
| Quantitative metrics | Schema-first with units | schema/*.csv |
| Transparency levels | High/Medium/Low per phase | PROJECT_STATUS.md |
| Sustainability index | NDC framework | docs/THOLONIC_INTEGRATION.md |

---

## What's Missing (Priority Order)

### 🔴 CRITICAL (Must Add)

#### 1. Entity Registry
**Sarah provides**: Specific company names (Newmont, Barrick, UK Royal Mint, etc.) - lines 87-123

**What to do**:
```bash
# Create new file
touch schema/entity_registry.csv

# Add columns: entity_id, entity_name, entity_type, phase_ids, countries, hq_location, sustainability_report_url
# Map Sarah's companies to your phases
```

**Why**: Can't collect real data without knowing which companies to target

---

#### 2. Water Metrics
**Sarah requires**: Litres consumed, litres recycled, source type (Blue/Grey/Brown) - lines 50-52

**What to do**:
```csv
# Add to gold_supply_chain_metrics_ndc.csv
metric_type: water_consumed, water_recycled, water_source_blue, water_source_grey
unit: litres
applicable_phases: 1 (Mining), 2 (Processing), 4 (Refining)
```

**Why**: Mining and ore processing are massively water-intensive (millions of litres/day)

---

#### 3. Waste Metrics
**Sarah requires**: Waste materials kg, waste water litres, circular economy tracking - lines 48, 51, 74

**What to do**:
```csv
# Add to gold_supply_chain_metrics_ndc.csv
metric_type: waste_material_tailings, waste_material_hazardous, waste_material_recycled
unit: kg
applicable_phases: 2 (Processing - 95% of ore becomes waste), 4 (Refining)
```

**Why**: Can't claim sustainability without tracking waste. Phase 2 generates ~950kg waste per 1000kg ore

---

### 🟡 IMPORTANT (Should Add Soon)

#### 4. Energy Details
**Sarah requires**: Energy grid type (AC/DC/Local), energy storage type, clean % - lines 55-58

**What to do**:
```csv
# Extend existing energy metrics
metric_type: energy_grid_type, energy_storage_type, energy_clean_pct
unit: categorical, categorical, percentage
```

**Why**: Your current `energy_base` is too aggregated for sustainability analysis

---

#### 5. Phase 8: Recycling
**Sarah emphasizes**: Circular economy, re-use of waste products - line 74

**What to do**:
```csv
# Add to supply_chain_phases_ndc.csv
phase_id: 8
phase_name: Recycling & Recovery
physical_state: Scrap/waste
primary_transformation: Thermal/Chemical
Output: Feeds back to Phase 4 (Refining)
```

**Why**: ~25-30% of annual gold supply is recycled (World Gold Council). Can't ignore this flow.

---

### 🟢 NICE TO HAVE (Later)

#### 6. Labor Metrics
**Sarah requires**: Person-hours by category, payroll - lines 59-61

**Status**: Medium priority, defer to Phase D (6-8 weeks)

---

#### 7. Land Use
**Sarah requires**: Hectares for production, waste storage, biodiversity - lines 62, 71-72

**Status**: Medium priority, useful for environmental assessment

---

#### 8. Governance Models
**Sarah mentions**: Coops, employee share schemes, corporate, state-owned - lines 35-40

**Status**: DEFER - This is Rule Set 8 (Deferred Interpretation), value chain layer

---

## Company Data Sources (From Sarah)

### Primary Producers (Phase 1)
| Company | HQ | URL (Add to entity registry) |
|---------|-----|------------------------------|
| Newmont Corporation | Denver, CO | https://www.newmont.com/sustainability/ |
| Barrick Gold | Toronto, Canada | https://www.barrick.com/sustainability/ |
| Agnico Eagle | Toronto, Canada | https://www.agnicoeagle.com/English/sustainability/ |
| Zijin Mining | Longyan, China | http://www.zijinmining.com/ |

### Recyclers (Phase 8 - New)
| Entity | Location | Focus |
|--------|----------|-------|
| UK Royal Mint | Wales | Phone recycling |

---

## This Week's Action Items

### Day 1-2: Schema Extensions
```bash
cd /home/jw/src/tv

# 1. Create entity registry
cat > schema/entity_registry.csv << 'EOF'
entity_id,entity_name,entity_type,phase_ids,countries,hq_location,sustainability_report_url,data_quality
E001,Newmont Corporation,producer,"0,1,2,3",Multi,Denver CO USA,https://www.newmont.com/sustainability/,high
E002,Barrick Gold,producer,"0,1,2,3",Multi,Toronto Canada,https://www.barrick.com/sustainability/,high
E003,UK Royal Mint,recycler,"8,4,5",UK,Llantrisant Wales,https://www.royalmint.com/aboutus/policies-and-guidelines/,medium
EOF

# 2. Add Phase 8 to phases file
vim schema/supply_chain_phases_ndc.csv
# Add: 8,Recycling & Recovery,Circular,Scrap/waste,Thermal/Chemical,Days-Weeks,Medium,...

# 3. Document new metric types
vim schema/gold_supply_chain_metrics_ndc.csv
# Add water_consumed, water_recycled, waste_material_tailings, etc.
```

### Day 3-4: Update Data Generator
```bash
# 4. Extend synthetic data to include environmental metrics
vim src/data/synthetic_data_generator.py
# Add water_consumption dict, waste_ratio calculations, energy_clean_pct

# 5. Regenerate data
python src/data/synthetic_data_generator.py

# 6. Regenerate frontend JSONs
python src/api/generate_frontend_data.py
```

### Day 5: Documentation
```bash
# 7. Create methodology doc
cat > docs/WATER_WASTE_METHODOLOGY.md
# Document industry benchmarks, data sources, calculation methods

# 8. Update API docs
vim docs/FRONTEND_API.md
# Add GET /api/v1/phase/{id}/environmental endpoint
```

---

## Quick Compliance Check

| Sarah's Principle | Your Rule Set | Status |
|------------------|---------------|--------|
| Physical metrics first | Rule Set 1: Separation of Concerns | ✅ |
| Phase-based analysis | Rule Set 2: Phase-Based Modeling | ✅ |
| Units for everything | Rule Set 3: Data-First Discipline | ✅ |
| Source attribution | Rule Set 9: Reproducibility | ✅ |
| Defer value judgments | Rule Set 8: Deferred Interpretation | ✅ |

**Overall**: 100% philosophical alignment ✅

---

## What NOT to Do (Rule Set Violations)

❌ **Don't add pricing/margins yet** - Rule Set 1 violation  
❌ **Don't model governance before physical flow complete** - Rule Set 8 violation  
❌ **Don't add "Beyond GDP" metrics yet** - Rule Set 8 violation  
❌ **Don't attribute opacity to conspiracy** - Rule Set 4 violation  

These belong in later interpretive layers, after Phase 0-7 physical mapping is complete with real data.

---

## Integration Phases (Timeline)

```
Week 1-2:  Schema extensions (entity registry, water/waste metrics)
Week 3-4:  Synthetic data update, documentation
Week 5-6:  Real data scraping (Newmont, Barrick reports)
Week 7-8:  Phase 8 (Recycling) full implementation
Week 9-12: Labor metrics, land use (if needed)
Week 12+:  Interpretive layers (governance, beyond GDP) - DEFERRED
```

---

## Key Insights from Sarah's Doc

1. **She has industry contacts** - Bristol One City Plan, potential customer network (lines 133-176)
2. **Multi-commodity scope** - Gold is one of several (lithium, copper, shea, cherries) - lines 9-14
3. **2018 precedent** - She already built a Shea supply chain model without AI (line 21)
4. **Clarity Coalition website** - She has a platform for publishing (lines 192, 203)
5. **Newmont specifically mentioned** - Advanced sustainability reporting (line 88)

**Implication**: Your gold model could be:
- A template for other commodities (lithium, copper)
- Potentially deployed via her existing Clarity Coalition platform
- Pitched to her Bristol network for funding/pilot customers

---

## Questions to Ask Sarah (If Contact Possible)

1. **Priority**: Water, waste, or energy first? Or all simultaneously?
2. **Recycling scope**: E-waste, jewelry scrap, industrial waste, or all?
3. **Data access**: Does she have contacts at Newmont/Barrick sustainability teams?
4. **Geographic focus**: Global, or specific region (Ghana, Wales, China)?
5. **Timeline**: When does she need a demonstrable prototype?

---

## Files Modified/Created

### New Files
- ✅ `docs/SARAH_INTEGRATION_ANALYSIS.md` (full analysis)
- ✅ `docs/SARAH_QUICK_REFERENCE.md` (this file)
- ⏳ `schema/entity_registry.csv` (to create)
- ⏳ `docs/WATER_WASTE_METHODOLOGY.md` (to create)

### Files to Modify
- ⏳ `schema/supply_chain_phases_ndc.csv` (add Phase 8)
- ⏳ `schema/gold_supply_chain_metrics_ndc.csv` (add water/waste metrics)
- ⏳ `src/data/synthetic_data_generator.py` (add environmental logic)
- ⏳ `docs/FRONTEND_API.md` (add environmental endpoints)

---

**Status**: Analysis complete, ready for Week 1 implementation  
**Next**: Create entity registry, extend metrics schema  
**Review**: February 7, 2026

