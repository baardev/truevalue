# Supply Chain Rules
## Gold Supply Chain Intelligence Project — AI Operating Rules (Supply Chain Layer)

## Core Objective

Build a quantitative, phase-resolved, physically grounded model of the gold supply chain, from geological origin to exchange-registered bullion, before introducing price, value, or financial interpretation.

**Scope note**: This document governs the **Supply Chain (physical)** layer only.  
Value-chain rules live in `docs/VALUE_CHAIN_RULES.md`.

## Rule Set 1: Separation of Concerns

**(This rule is non-negotiable)**

The project is divided into strict analytical layers:

1. **Supply chain** (physical flow, custody, constraints)
2. **Value chain** (profit, pricing, margins)
3. **Financial abstraction** (paper claims, leverage)

**Cursor must never mix layers prematurely.**

- No pricing, margins, or value discussion during supply chain modeling.
- No economic inference without completed physical mapping.

**Rule of thumb:**
If gold cannot be weighed, moved, or stored in that step, it does not belong in the supply chain layer.

---

## Rule Set 2: Phase-Based Modeling

**Everything must belong to a phase**

All analysis must map to a discrete supply chain phase.

Each phase must be defined by:
- A physical state of gold
- A transformation or custody change
- A measurable output

**Cursor must reject concepts that:**
- Span multiple phases without explicit linkage
- Cannot be assigned a phase_id

**Allowed structure:**
```
Phase → Metric → Unit → Source → Custodian
```

**Disallowed:**
- Narrative descriptions without metrics
- Aggregates that obscure phase boundaries

---

## Rule Set 3: Data-First Discipline

**No data → no claims**

Cursor must prefer:
- Quantitative metrics
- Units
- Time series
- Source attribution

**Every dataset must include:**
- Phase ID
- Measurement unit
- Source type (public, paid, private, inferred)

**If data is missing:**
- Mark explicitly as OPAQUE
- Do not interpolate or speculate

**Missing data is a finding, not a failure.**

---

## Rule Set 4: Transparency Classification

**Opacity is a feature, not an error**

Every phase must be tagged:
- High transparency
- Medium transparency
- Low transparency

**Cursor must explain opacity using structural reasons, not intent:**
- Private custody
- Commercial secrecy
- Jurisdictional limits

**Cursor must never attribute opacity to:**
- Conspiracy
- Bad actors
- Malice

(Those belong only in later interpretive layers, if at all.)

---

## Rule Set 5: Custody and Control Awareness

**Ownership ≠ custody ≠ control**

Cursor must distinguish between:
- Who owns the gold
- Who physically holds it
- Who can legally mobilize it

**Any transfer must specify:**
- Whether ownership changes
- Whether custody changes
- Whether gold remains physically stationary

Rehypothecation, leasing, and paper claims are out of scope until the supply chain is complete.

---

## Rule Set 6: Exchange Data as Anchor, Not Truth

**COMEX is a reference point, not a ground truth**

Exchange inventories are treated as:
- Highly transparent
- Legally constrained
- Physically limited to registered bars

**Cursor must not extrapolate upstream supply from exchange data alone.**

Exchange data is used for reconciliation, not inference.

---

## Rule Set 7: Schema-First Development

**If it can't be tabulated, it doesn't exist**

All insights must be representable in:
- CSV
- SQL
- Dataframes

**Cursor must prioritize:**
- Tables
- Schemas
- Field definitions

Narrative explanation is secondary and must map to schema elements.

---

## Rule Set 8: Deferred Interpretation

**Understanding comes last**

Cursor must explicitly defer:
- Price formation
- Profit capture
- Market manipulation
- Financial leverage

**These are allowed only after:**
- All supply chain phases are mapped
- Data visibility gaps are documented

**First map the terrain.**
**Then ask who benefits from it.**

---

## Rule Set 9: Reproducibility and Auditability

**Another analyst must be able to follow the chain**

Every claim must be traceable to:
- A phase
- A dataset
- A source category

**Cursor should favor:**
- Public data where possible
- Clear flags where paywalled data is required

---

## One-Sentence Project Rule (For Cursor System Prompt)

> **"Model the gold supply chain as a phase-based, data-driven physical system, prioritizing measurable flow, custody, and constraints, while explicitly deferring value, pricing, and financial interpretation until the physical chain is fully mapped."**

