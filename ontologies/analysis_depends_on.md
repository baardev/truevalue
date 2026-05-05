# Knowledge Graph Analysis: `depends_on` (causation group)

## What This Document Is

This document is a worked example of knowledge graph interrogation applied to the TrueValue Framework (TVF) modeling dataset. It demonstrates how a structured ontology, built from 215,539 entity-entity triples extracted across supply chain, sustainability, and theoretical framework documents, can be queried to surface supported, referenced, and cross-contextually validated conclusions.

The dataset (KG01-tvfmodeling) contains:

| Metric | Count |
|---|---|
| Entity-Entity triples | 215,539 |
| Distinct entities | 4,852 |
| Distinct relationship names | 2,099 |

Each of those 215,539 triples is a candidate discovery. It is a machine-extracted assertion, grounded in source text, that two named concepts stand in a specific relationship to one another. Across 20 relationship categories (parthood, causation, attribution, authorship, and so on), these triples form a queryable map of how concepts in supply chain finance and sustainability actually connect in practice, across documents, domains, and scales of abstraction.

The significance of this is not merely bibliographic. Because the knowledge graph spans both applied operational contexts (agroforestry carbon projects, gold and shea supply chains, water system finance) and theoretical frameworks (the Tholonic N-D-C model, the I-Ching, the Tholonia book), the same structural relationship can be validated independently at multiple levels. When the same pattern appears in a Senegalese nursery operation and in a mathematical model of recursive balance, that convergence is not accidental. It is evidence that the relationship reflects something real about how systems are structured.

This document focuses on a single relationship, `depends_on`, within the causation group. It is intended as a template: the same approach can be applied to any of the 2,099 relationship types to generate sourced, traceable, and analytically grounded claims about supply chain dependencies, sustainability stress points, and systemic failure modes.

---

**Dataset:** KG01-tvfmodeling  
**Date:** 2026-05-05  
**Tool:** `query_sources.py`, `query_children.py`, `query_top_catagories.py`

---

## Query Tools: Purpose and Output

Three command-line tools were used to produce this analysis. Each addresses a different level of the knowledge graph hierarchy.

---

### `query_top_catagories.py`

```bash
./query_top_catagories.py --dataset KG01-tvfmodeling
```

**Purpose:** Gives a bird's-eye view of the entire knowledge graph. It loads both the base ontology (`cTVF-merged.ttl`) and the property groups layer (`property_groups.ttl`), then counts how many specific relationship names (e.g., `depends_on`, `causes`, `arises_from`) have been mapped as sub-properties of each abstract category.

**What it returns:** A ranked list of the 20 abstract relationship categories, ordered by the number of member relationship types each contains. The number next to each category is the count of distinct relationship names grouped under it, not the count of triples. A high number means that category covers a broad and varied set of causal, descriptive, or structural relationships in the corpus.

**When to use it:** As the entry point. It tells you where the conceptual density is. A category with 56 members (parthood) has more semantic surface area than one with 10 (connectivity). Start here to decide which category is worth drilling into.

---

### `query_children.py`

```bash
./query_children.py causation --limit 20 --dataset KG01-tvfmodeling
```

**Purpose:** Expands a single abstract category into its constituent relationship names. It queries the `property_groups.ttl` ontology for all `rdfs:subPropertyOf` assertions under the named group and returns them as an ordered list.

**What it returns:** The specific relationship predicates that belong to the chosen category. For `causation`, this includes `depends_on`, `causes`, `drives`, `enables`, `feeds_into`, and 39 others. Each name on this list is a distinct predicate that an LLM identified in source text and assigned to a triple. The `--limit` flag controls how many are shown; the total count is always displayed regardless.

**When to use it:** After identifying a category of interest. It answers the question: exactly which relationship types are being grouped here, and how many are there? It also exposes LLM extraction patterns: near-synonyms like `contributes_to` and `contributed_to` appearing as separate entries reveal that the graph has not yet been deduplicated.

---

### `query_sources.py`

```bash
# Tabular view: all triples for a relationship
./query_sources.py causation:depends_on --dataset KG01-tvfmodeling

# Rich view: triples with source text passages
./query_sources.py causation:depends_on --limit 3 --dataset KG01-tvfmodeling --text
```

**Purpose:** Retrieves the actual triples from the PostgreSQL knowledge graph for a given relationship name, and optionally traces each triple back to the source text passages from which it was extracted. This is the grounding layer: it connects abstract ontological structure to the original documents.

**What it returns (tabular mode):** A table of `(source entity, relationship, target entity, dataset)` rows. Each row is one extracted assertion. The total triple count for that relationship is shown in the header.

**What it returns (`--text` mode):** For each triple, up to three text passages:

- **Relationship context:** the document chunk that contained both entities simultaneously. This is the passage the LLM was reading when it extracted the relationship. It is the most direct evidence for why the triple exists.
- **Source context:** the longest chunk in the corpus that is linked to the source entity. This provides background on what the source entity is and what role it plays across the full document set.
- **Target context:** the longest chunk linked to the target entity, for the same purpose. If source or target context is identical to the relationship context, it is suppressed to avoid repetition.

**When to use it:** To validate a relationship, to find the evidentiary basis for a claim, or to read the actual content that gave rise to a specific triple. The `--text` flag turns the tool from a query interface into a reading interface.

---

## Top 20 Relationship Categories

```
Triples loaded: 116,548

  56  parthood
  44  causation
  41  attribution
  37  authorship
  36  description
  35  similarity
  32  measurement
  31  application
  26  analysis
  26  reference
  25  support
  23  participation
  22  governance
  21  classification
  20  transformation
  19  spatial
  18  temporal
  18  tholonic NDC
  14  provenance
  10  connectivity
```

---

## Members of the `causation` Group (44 total)

```
affected_by      affects          arises_from      causes
contributed_to   contributes_to   depends_on       determines
drives           emerges_from     emerges_in       enables
encouraged_by    enhanced_by      enhances         establishes
facilitates      feeds_into       flows_to         generated
...
```

---

## Triples: `causation:depends_on` (201 total)

Sample of 20 (tabular):

| SOURCE        | RELATIONSHIP | TARGET             | DATASET          |
|---------------|--------------|--------------------|------------------|
| acorn project | depends_on   | nursery operations | KG01-tvfmodeling |
| balance       | depends_on   | definition         | KG01-tvfmodeling |
| balance       | depends_on   | definition (d)     | KG01-tvfmodeling |
| balance       | depends_on   | contribution       | KG01-tvfmodeling |
| balance       | depends_on   | contribution (c)   | KG01-tvfmodeling |
| ...           | ...          | ...                | ...              |

---

## Source Text Evidence (limit 3, with context)

### Triple 1: `acorn project --depends_on--> nursery operations`

**Relationship context** (passage containing both entities):

> ...through legal instruments such as the Environment Code, the Forest Code, the Hunting and Wildlife Protection Code, adherence to various treaties and conventions, the adoption of a sector policy and development strategic framework. 24 How do the agroforestry practices in this project differ to current farming practices in the region? There are no current defined practices, education/training or understanding of the benefits, trees are use as delimitation only by owners. 25 Is planned harvesting part of the agroforestry design for this project?... The project boundaries are well defined with prior consent and the agreement reviewed by the national government agency will specify the exclusivity of the carbon accounting for... `[truncated]`

**Source context** (acorn project):

> ...Some of the most significant agricultural challenges faced by Senegalese farmers and their families, and the community in the project area which is center, east and northern Senegal are: Climate change and environmental degradation: Senegal is a country that is particularly vulnerable to the impacts of climate change. The country's agricultural sector is highly dependent on rainfall, and changes in rainfall patterns and temperature can significantly affect crop yields. Environmental degradation, such as deforestation and soil erosion, can also contribute to reduced agricultural productivity. Limited access to credit and inputs: Many Senegalese farmers have limited access to credit and inputs, such as seeds, fertilizers, and equipment... `[truncated]`

---

### Triple 2: `balance --depends_on--> contribution`

**Relationship context:**

> # AI Note: Tholonic Framework Supply and Value Chain Application
> **Document ID:** tholonic_framework_supply_value_chain
> **One-Sentence Summary:** Defines how the N-D-C framework applies to supply-chain and value-chain modeling while maintaining strict analytical separation between layers.
> **Key Claims:**
> - N-D-C models phase coherence through Definition, Contribution, and emergent Negotiation.
> - Balance between Definition and Contribution determines whether a stable Negotiation state can emerge.

**Source context** (balance):

> ...The tholonic model agrees with this principle but proposes a different answer to the question of "where" such reversal occurs. We understand electromagnetic energy as the spectrum of non-material energy expressed through waves, frequencies, and photons. Thermodynamic entropy is a material phenomenon fundamentally tied to systems that experience the flow of time... From the reference frame of a photon traveling at light speed, proper time equals zero, and spatial distance contracts to zero. Photons in transit exist in a timeless state outside the conventional framework of spacetime entropy... `[truncated]`

**Target context** (contribution):

> ...# Clarity True Value Framework and KPMG True Value
> ## A Comparative Research Paper on Structural System Coherence and Monetized Externality Accounting
> ### Abstract
> This paper compares the Clarity True Value Framework, a tholonic N-D-C system for phase-based analysis of physical, lifecycle, and value systems, with the existing KPMG True Value methodology. KPMG True Value is a corporate impact measurement approach that identifies economic, social, and environmental externalities... `[truncated]`

---

### Triple 3: `balance --depends_on--> contribution (c)`

**Relationship context:**

> ...6180339887), Euler's number (*e*, 2.7182818285), the natural logarithm of 2 (ln(2), 0.6931471806), and the square root of 2 ($\sqrt{2}$, 1.4142135623). This capacity to generate diverse fundamental constants demonstrates that the Tholonic recursion isn't just a specialized $\pi$ calculator; it's a generalized symbolic engine, capable of embodying multiple structural equilibria within mathematics. Each constant ($\pi$, $\phi$, $e$, $\ln(2)$, $\sqrt{2}$) emerges naturally as a symbolic and numeric representation of the specific philosophical dynamics of *Negotiation*, *Definition*, *Contribution*, and generational complexity that characterize its initial conditions... `[truncated]`

*(Source and target contexts are identical to Triple 2.)*

---

## Conclusion: What `depends_on` Reveals Across Contexts

The three triples above are structurally identical statements expressed at different levels of abstraction:

| Level | Source (N state) | Relationship | Target (C pole) |
|-------|-----------------|--------------|-----------------|
| Applied (agroforestry) | acorn project | depends_on | nursery operations |
| Abstract (tholonic) | balance | depends_on | contribution |

This is not coincidence. It is the same pattern, instantiated at different scales. The Acorn project is a Negotiation state. Nursery operations is its Contribution pole. The tholonic triple is the abstract formulation of the same structural dependency.

**Systems fail from the outside in.**

The Contribution pole is the exposed surface of any system. When the environment becomes hostile, C degrades before D does. Balance collapses not because the system loses its identity (D remains intact) but because it loses its ability to produce and connect outward.

The source context for the Acorn project confirms this directly: the threats listed are all C-side degradations:

- Climate change attacking rainfall (disrupting productive capacity)
- Limited credit access (constraining operational output)
- Poor infrastructure (blocking market connection)

None of the threats are definitional. Nobody questions what the Acorn project *is*. The threat is always to what it can *produce and deliver*.

**Predictive implication:**

Any intervention aimed at stabilizing a system under stress should target the C pole first, restoring productive capacity before refining internal structure. Rebuilding identity (D) while the contribution pathway remains broken is wasted effort.

This prediction holds equally for a Senegalese agroforestry project and for an analytical framework under conceptual pressure. The pattern transcends context. That is the point.

---

# BUT WAIT, THERE'S MORE!!

Okay, but here's the real mind-blowing kicker. Now that we have all of these relationships that are in one way or another directly or indirectly connected to each other we can find any relationship or pattern between any two concepts for example (and I won't show the technical details), if we wanted to see the relationship between twister theory and supply chain sustainability we can just ask it to find that relationship and what we get is the following...



> If twistor theory is a tholonic instantiation, and the tholonic model is scale-invariant and applicable to sustainability, then the geometric intuitions of twistor theory are transferable to sustainability modeling. Specifically: a supply chain phase in sustainable equilibrium is analogous to an on-shell state in twistor space. It satisfies a null-like condition, maximum contribution relative to constraints, with minimum waste. A phase that is out of balance is off-shell: it requires external energy input (subsidies, regulatory intervention, debt financing) to sustain itself, exactly as a virtual particle requires borrowed energy. When that external input is withdrawn, the off-shell state collapses.

> This is not a metaphor. It is a structural isomorphism between two formally described systems, documented in the source text, confirmed by the graph traversal, and testable against the supply chain data already in the corpus. The three paths to sustainability from twistor theory are three ways the graph has independently noticed and recorded the same underlying fact.
