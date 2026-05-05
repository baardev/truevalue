# Knowledge Graph Query Tools

## Overview

This folder contains a suite of command-line tools for interrogating the TrueValue Framework (TVF) knowledge graph. The graph was built by running the Cognee cognification pipeline over three document collections and is stored in a local PostgreSQL database. It currently contains:

| Dataset | Entities | Entity-Entity Triples | Relationship Types |
|---|---|---|---|
| KG01-tvfmodeling | 4,852 | 215,539 | 2,099 |
| KG02-tholonia-book | 3,894 | 325,401 | 2,150 |
| KG03-iching_intro | 652 | 61,876 | 922 |

Each triple is a machine-extracted assertion of the form `(subject, predicate, object)`, grounded in a specific passage of source text. Every one of those triples is a candidate discovery about how concepts in supply chain finance, sustainability, and theoretical frameworks relate to one another.

The tools are designed to be used in sequence, moving from the broadest possible view down to specific grounded evidence, and finally to cross-concept path discovery.

---

## Performance: The PostgreSQL Cache

All query tools use a pre-built PostgreSQL cache for near-instant responses. Without the cache, each run would parse large OWL/Turtle files from disk and execute complex multi-table joins, taking 5-10 seconds per query. With the cache, every query runs in under 200ms.

The cache consists of four tables in the same PostgreSQL database as the knowledge graph:

| Table | Rows | Contents |
|---|---|---|
| `kg_property_groups` | 554 | Ontology group-to-child predicate mappings |
| `kg_flat_triples` | 44,502 | Fully denormalized entity-entity triples with group labels |
| `kg_entity_context` | 9,398 | Best source text passage per entity |
| `kg_edge_context` | 15,882 | Co-occurrence passage per (source, target) pair |

The `kg_entity_context` and `kg_edge_context` tables are what make `--text` and `--report` modes instant: instead of running expensive lateral joins at query time, the source passages are pre-fetched and stored.

**Building or rebuilding the cache:**

```bash
# Full build including all text contexts (~15 minutes on first run)
./build_kg_cache.py

# Structural rebuild only, no text (completes in ~5 seconds)
./build_kg_cache.py --skip-text

# Rebuild for a single dataset only
./build_kg_cache.py --dataset KG01-tvfmodeling
```

Run `build_kg_cache.py` whenever new data is cognified into the knowledge graph. All tools automatically fall back to the slower direct-query path if the cache tables do not exist.

---

## The Ontology Files

Two OWL ontology files (Turtle format) provide the structural scaffolding:

- **`cTVF-merged.ttl`**: The base ontology, generated from all three datasets. Contains entity classes, subclass hierarchies, and object property definitions with inferred characteristics (inverse, transitive, symmetric).
- **`property_groups.ttl`**: A supplementary layer that defines 20 abstract property group categories (e.g., `causation`, `parthood`, `measurement`) and maps specific extracted relationship names as sub-properties of those groups using `rdfs:subPropertyOf`. This is what makes the higher-level category queries possible.

These files are the source of truth for the ontology structure. The cache tables are derived from them and from the PostgreSQL knowledge graph. If you modify the TTL files, rebuild the cache.

---

## Dataset Aliases

All tools accept a `--dataset` flag. The following short aliases are supported:

| Alias | Full dataset name |
|---|---|
| `KG01` or `KG01-tvfmodeling` | `ope-voy_KG01-tvfmodeling` |
| `KG02` or `KG02-tholonia-book` | `ope-voy_KG02-tholonia-book` |
| `KG03` or `KG03-iching_intro` | `ope-voy_KG03-iching_intro` |

If `--dataset` is omitted, most tools search across all three datasets.

---

## Recommended Workflow

The tools form a natural five-step investigation pipeline:

```
Step 0: build_kg_cache.py         "Build the cache once before first use."
Step 1: query_top_catagories.py   "What are the dominant relationship themes?"
Step 2: query_children.py         "What specific predicates belong to a theme?"
Step 3: query_sources.py          "What triples exist, and what do the sources say?"
Step 4: query_path.py             "How do two concepts connect, even indirectly?"
```

`query_search.py` can be used at any point to locate a concept across the entire graph before committing to a specific investigation path.

---

## Tool Reference

---

### `build_kg_cache.py`

**Purpose:** Builds the PostgreSQL cache tables that all other tools depend on for fast queries. Must be run at least once before using the query tools, and re-run after any new cognification. Safe to re-run at any time: tables are dropped and rebuilt from scratch.

**What it does:**
1. Parses `property_groups.ttl` and `cTVF-merged.ttl` and stores the group-to-child mappings in `kg_property_groups`.
2. Loads all entity-entity edges from the three datasets, denormalizes them with group labels, and writes them to `kg_flat_triples`.
3. For each entity, finds the longest source text passage linked to it and stores it in `kg_entity_context`. This pre-computes the SOURCE CONTEXT and TARGET CONTEXT used by `query_sources --text` and `query_path --report`.
4. For each (source, target) entity pair, finds the document chunk containing both entities and stores it in `kg_edge_context`. This pre-computes the RELATIONSHIP CONTEXT used by the same tools.

**Usage:**

```bash
# Full build including all text contexts (~15 minutes)
./build_kg_cache.py

# Structural rebuild only, no text (~5 seconds)
./build_kg_cache.py --skip-text

# Single dataset only
./build_kg_cache.py --dataset KG01-tvfmodeling
```

**Arguments:**

| Argument | Description |
|---|---|
| `--skip-text` | Skip `kg_entity_context` and `kg_edge_context` (fast structural rebuild) |
| `--dataset` | Rebuild only one dataset (default: all three) |

**When to run it:** Once after initial setup. Again after adding new documents to any dataset via cognification. The `--skip-text` flag is useful for quick rebuilds when only the ontology TTL files have changed.

---

### `query_top_catagories.py`

**Purpose:** Bird's-eye view of the knowledge graph. Shows which abstract relationship categories contain the most specific predicate types, giving you a map of where conceptual density is highest.

**What it returns:** A ranked list of the 20 abstract property groups with the count of member relationship names under each. The number is the count of distinct predicate types, not the count of triples.

**Usage:**

```bash
./query_top_catagories.py
./query_top_catagories.py --dataset KG01-tvfmodeling
```

**Example output:**

```
  Category                   Members
  -----------------------------------
   56  parthood
   44  causation
   41  attribution
   37  authorship
   36  description
   35  similarity
   32  measurement
  ...
```

**When to use it:** Always start here. A category with 56 members has far more semantic surface area than one with 10. This is your navigation map for the rest of the investigation.

---

### `query_children.py`

**Purpose:** Expands one abstract category into the specific relationship names (predicates) it contains. Tells you exactly which extracted predicate strings have been grouped under a given category.

**What it returns:** An ordered list of all member relationship names for the chosen category, with a total count shown in the header.

**Usage:**

```bash
./query_children.py <category> [--limit N] [--dataset DATASET]
```

**Arguments:**

| Argument | Description |
|---|---|
| `category` | Name of the abstract group (e.g., `causation`, `parthood`) |
| `--limit N` | Show only the first N members (default: all) |
| `--dataset` | Filter to a specific dataset |

**Example:**

```bash
./query_children.py causation --limit 20 --dataset KG01-tvfmodeling
```

**Example output:**

```
=== MEMBERS OF 'causation' (44 total) ===

   1.  affected_by
   2.  affects
   3.  arises_from
   4.  causes
   5.  depends_on
   6.  determines
   7.  drives
   8.  enables
   ...
```

**When to use it:** After identifying an interesting category in step 1. It answers: what specific predicates am I working with, and are there near-synonyms or noise that should be deduplicated?

---

### `query_sources.py`

**Purpose:** Retrieves the actual triples from PostgreSQL for a given relationship name, with optional retrieval of the source text passages the triples were extracted from. This is the grounding layer: it connects ontological structure back to the original documents.

**What it returns:**

- **Tabular mode (default):** A table of `(source entity, relationship, target entity, dataset)` rows. The total triple count is shown in the header.
- **Text mode (`--text`):** For each triple, up to three source text passages:
  - **Relationship context:** The document chunk containing both entities simultaneously. This is the passage the LLM was reading when it extracted the relationship.
  - **Source context:** The longest chunk linked specifically to the source entity, providing background on what it is.
  - **Target context:** The longest chunk linked specifically to the target entity.

**Usage:**

```bash
# Tabular output
./query_sources.py <group>:<relationship> [--dataset DATASET] [--limit N]

# With source text passages
./query_sources.py <group>:<relationship> [--dataset DATASET] [--limit N] --text
```

**Arguments:**

| Argument | Description |
|---|---|
| `group:relationship` | The relationship to query, e.g., `causation:depends_on` |
| `--dataset` | Filter to a specific dataset |
| `--limit N` | Maximum triples to return (default: 20) |
| `--text` | Include source text passages for each triple |

**Examples:**

```bash
# List triples for depends_on
./query_sources.py causation:depends_on --dataset KG01-tvfmodeling

# Show 3 triples with full source text
./query_sources.py causation:depends_on --limit 3 --dataset KG01-tvfmodeling --text

# Without a group prefix (searches by relationship name directly)
./query_sources.py depends_on --limit 5 --text
```

**Example output (tabular):**

```
=== RELATIONSHIP: depends_on  (in group: causation)  (201 triples) ===
   Dataset filter: KG01-tvfmodeling

 SOURCE         RELATIONSHIP  TARGET              DATASET
 -------------------------------------------------------------
 acorn project  depends_on    nursery operations  KG01-tvfmodeling
 balance        depends_on    definition          KG01-tvfmodeling
 ...
```

**Example output (with `--text`):**

```
  [1]  acorn project  --depends_on-->  nursery operations
        Dataset: KG01-tvfmodeling

        RELATIONSHIP CONTEXT (passage containing both entities):
        ...the project boundaries are well defined with prior consent...

        SOURCE CONTEXT  [acorn project]:
        ...Senegal is a country that is particularly vulnerable to the impacts
        of climate change...
```

**When to use it:** When you have identified a specific relationship name from step 2 and want to see the actual triples it covers, or when you need the evidentiary basis for a specific claim. The `--text` flag turns this into a reading tool: use it to verify that extracted relationships are genuine and to understand the context in which they appear.

---

### `query_search.py`

**Purpose:** Searches for a term across the entire knowledge graph in two modes: by relationship name, or by the content of source text passages. Use this when you do not yet know which category or predicate to investigate, or when you want to find every triple that mentions a specific concept anywhere in the source documents.

**What it returns:**

- **Default mode:** Ontology matches (category or child names containing the term) plus database matches (relationship names containing the term with triple counts and group labels).
- **`--in-text` mode:** All triples extracted from passages whose text contains the search term, grouped by ontology category, with one example passage per group.

**Usage:**

```bash
# Search relationship names
./query_search.py <term> [--dataset DATASET] [--limit N]

# Search inside source text passages
./query_search.py <term> --in-text [--dataset DATASET] [--limit N]
```

**Examples:**

```bash
# Find all relationship names mentioning "balance"
./query_search.py balance

# Find triples from passages mentioning "twistor"
./query_search.py twistor --in-text

# Narrow to one dataset
./query_search.py supply --dataset KG01-tvfmodeling --in-text --limit 50
```

**Example output (default mode):**

```
  Search term: 'balance'

  CHILD RELATIONSHIP MATCHES IN ONTOLOGY (2):
    has_balance_score    (group: measurement)
    has_balance_score    (group: tholonic NDC)

  DATABASE MATCHES — relationship names containing 'balance':
  RELATIONSHIP                     TRIPLES   GROUP         DATASET
  ---------------------------------------------------------------
  balances                           946     (unmapped)    KG01-tvfmodeling
  balances_with                      490     (unmapped)    KG01-tvfmodeling
  involves_balance_of                344     (unmapped)    KG01-tvfmodeling
  ...
```

**Example output (`--in-text` mode):**

```
  Found 20 triple(s) from chunks containing 'twistor',
  across 2 relationship group(s):

  [ANALYSIS]  (3 triples)
  SOURCE                  RELATIONSHIP     TARGET
  ------------------------------------------------
  twistor theory          addresses        inherited constraints
  ...

  Example passage:
    ...The BCFW recursion is inter-level tholonic propagation applied
    to scattering amplitudes...
```

**When to use it:** At any point in the investigation when you need to locate a concept before you know where to look. It is especially useful for bridging between a topic you have in mind and the relationship categories that cover it.

---

### `query_path.py`

**Purpose:** Graph traversal. Given two concepts, finds a chain of relationships connecting them through the knowledge graph, even when no direct link exists. This is the most powerful discovery tool in the suite: it surfaces indirect connections that no amount of browsing individual triples would reveal.

**What it returns:**

- **Standard mode:** One or more shortest paths between the two concepts, displayed as chains of `[entity] --relationship--> [entity]` steps.
- **`--report` mode:** A full structured analysis prompt for each path, including the most relevant source text for every entity and every edge in the chain, plus five analysis questions. This output is designed to be pasted directly into an LLM for deep analysis.
- **`--analysis` mode:** Same context as `--report`, but each path is also sent to the Anthropic API (default model: `claude-sonnet-4-5`). Responses are printed and saved as **Markdown** (`.md`) under `qanalysis/` (see below). Each file ends with an **API usage** section: token table and **estimated USD cost** using published Sonnet 4.5 list rates (configurable via `KG_ANALYSIS_PRICE_INPUT_PER_MTOK` and `KG_ANALYSIS_PRICE_OUTPUT_PER_MTOK`). Requires `ANTHROPIC_API_KEY` (or key in `/home/jw/src/cognee/.env-anthropic` as used by this repo). You can combine `--report` and `--analysis`.
- **`--research` mode:** Implies `--analysis`. After each path analysis, a **second** request runs with Anthropic **web search** (default model: `claude-sonnet-4-6`, overridable via `KG_RESEARCH_MODEL`). The saved Markdown gains **Further reading** and **Suggested footnotes**. The research prompts **require** sources that **jointly** engage **both** query concepts (bridging, interdisciplinary, or explicit comparison), not standalone bibliographies for only one concept. If the open literature does not connect them, the model should say so and suggest paired search queries rather than padding with single-topic hits. Web search must be enabled for that model on your Anthropic account; confirm model IDs and tool support in Anthropic docs. Verify citations yourself before publication.

**Zero-hop paths:** If a **single** entity name contains **both** search substrings (for example `community` and `ecosystem projects` both appear in `community and ecosystem projects`), the tool reports a **0-hop** path: that entity alone, with no edges. Multi-hop paths may still be listed afterward if `--paths` allows.

**Usage:**

```bash
# Find paths
./query_path.py <entity1> <entity2> [--dataset DATASET] [--depth N] [--paths N]

# Find paths with full source text report
./query_path.py <entity1> <entity2> [--report] [--dataset DATASET] [--depth N] [--paths N]

# Report plus Claude analysis (saved under qanalysis/)
./query_path.py <entity1> <entity2> [--report] [--analysis] [--dataset DATASET] [--depth N] [--paths N]

# Analysis plus web research (further reading + footnotes; implies --analysis)
./query_path.py <entity1> <entity2> [--report] --research [--dataset DATASET] [--depth N] [--paths N]
```

**Arguments:**

| Argument | Description |
|---|---|
| `entity1`, `entity2` | Substrings to match entity names (case-insensitive) |
| `--dataset` | Limit to one dataset (default: search all three) |
| `--depth N` | Maximum hops to traverse (default: 4) |
| `--paths N` | Maximum number of paths to return (default: 3) |
| `--report` | Generate full source text report for each path |
| `--analysis` | Call Anthropic Claude for each path; save Markdown (`.md`) results under `qanalysis/` |
| `--research` | After analysis, run web search for authoritative sources; append further reading + footnotes (implies `--analysis`) |
| `--token` | Match entity names by **whole tokens** only (splits on non-alphanumeric). `twistor` matches `twistor theory` but not `ambitwistor` |

**Saved analysis files (`qanalysis/`):**

When you pass `--analysis` (or `--research`, which enables analysis), each path produces one **Markdown** file (`.md`):

- **Folder name:** `{SEARCH_TERM1}--{SEARCH_TERM2}` with segments **sanitized and uppercased** (same style as entities in filenames).
- **File name:** The full path chain: **entity segments** (uppercase, underscores) and **predicate segments** (lowercase), joined with `--`, for example `COMMUNITY_CENTRED_DESIGN--relates_to--SUSTAINABILITY.md`.
- **Length limit:** Basenames are capped by **`KG_PATH_MAX_FILENAME_BYTES`** (default **250** UTF-8 bytes) so names stay within typical single-component OS limits. If the chain is longer, the file is named `path_NNN__<hash>.md` instead; the **full chain** is still recorded in the document header.

**File manager note:** Many UIs show an ellipsis (`...`) in the **middle** of a long basename to save column space. That is **display only**. The real name on disk is what you see in a tooltip, `ls`, or properties.

**Environment (optional):**

```bash
# Allow slightly longer basenames (still subject to OS max, often 255 bytes)
export KG_PATH_MAX_FILENAME_BYTES=255

# Optional: custom USD per million tokens for cost estimates in --analysis output
export KG_ANALYSIS_PRICE_INPUT_PER_MTOK=3
export KG_ANALYSIS_PRICE_OUTPUT_PER_MTOK=15

# Model for --research web search (must support the web search tool on your account)
export KG_RESEARCH_MODEL=claude-sonnet-4-6
```

**Examples:**

```bash
# Find how gold and bank connect
./query_path.py gold bank --dataset KG01-tvfmodeling

# Find how twistor theory connects to sustainability
./query_path.py twistor sustainability --dataset KG01-tvfmodeling

# Generate a full analysis prompt for pasting into an LLM
./query_path.py twistor sustainability --report > twistor_sustainability_report.txt

# Search deeper if no path found at default depth
./query_path.py "supply chain" tholonic --depth 6

# Run Claude analysis on each path (writes under qanalysis/)
./query_path.py twistor sustainability --report --analysis --dataset KG01-tvfmodeling

# Analysis + web research (further reading and footnotes in the same .md file)
./query_path.py twistor sustainability --research --dataset KG01-tvfmodeling
```

**Example output (standard):**

```
  Found 3 path(s), shortest is 2 hop(s):

  Path 1  (2 hops):
        [ twistor theory ]
          --is_instantiated_as-->
        [ tholonic model ]
          --is_applicable_when-->
        [ resource sustainability matters (condition) ]
```

**Example output (`--report` mode, excerpt):**

```
==============================================================================
  KNOWLEDGE GRAPH PATH ANALYSIS PROMPT  |  Path 1
==============================================================================

  PATH SUMMARY
    [twistor theory] --is_interpretable_as_tholonic_instantiation-->
    [tholonic model] --is_applicable_when-->
    [resource sustainability matters (condition)]

  ENTITY CONTEXTS
    [TWISTOR THEORY]
      ...The Tholonic model proposes that all formed and growing systems,
      from quantum fields to ecosystems to ideas, are governed by a
      universal triadic structure...

  RELATIONSHIP CONTEXTS
    EDGE: [twistor theory] --is_interpretable_as_tholonic_instantiation-->
          [tholonic model]
      ...This paper examines Roger Penrose's twistor theory, the most
      ambitious geometric reformulation of fundamental physics...

  ANALYSIS QUESTIONS
    1. Is the connection semantically valid? Does each step follow logically?
    2. What does this path reveal about the structural relationship?
    3. Are any intermediate entities acting as non-obvious bridges?
    4. What are the supply chain or sustainability implications?
    5. Does the source text support or undermine each extracted relationship?
```

**When to use it:** When you have two concepts you suspect are related but cannot find the direct link, or when you want to understand the structural path between a theoretical construct and an applied domain. The `--report` flag makes it a research generation tool: each output is a self-contained, sourced briefing ready for LLM-assisted analysis. With `--analysis`, Claude writes Markdown (`.md`) under `qanalysis/` for viewing in editors, wikis, or MkDocs. With `--research`, each file also gains web-backed **further reading** and **footnotes** (always verify links yourself).

---

## Complete Example Workflow

The following illustrates a complete investigation starting from zero and ending with sourced, grounded conclusions.

**Question: How does twistor theory relate to sustainability?**

```bash
# 0. Build the cache (once; ~15 minutes; re-run after new cognification)
./build_kg_cache.py

# 1. Get the lay of the land
./query_top_catagories.py --dataset KG01-tvfmodeling
# -> See that "causation" (44 members) and "tholonic NDC" (18) are high-density categories

# 2. Check what "tholonic NDC" contains
./query_children.py "tholonic NDC" --dataset KG01-tvfmodeling
# -> See relationship names like has_balance_score, instantiates, corresponds_to

# 3. Search for twistor to see where it appears
./query_search.py twistor --in-text --dataset KG01-tvfmodeling
# -> Find triples from passages mentioning twistor, grouped by category

# 4. Find the path from twistor to sustainability
./query_path.py twistor sustainability --dataset KG01-tvfmodeling
# -> Discover: twistor theory --is_instantiated_as--> tholonic model
#              tholonic model --is_applicable_when--> resource sustainability

# 5. Generate a full sourced report for deep analysis
./query_path.py twistor sustainability --dataset KG01-tvfmodeling --report \
  > twistor_sustainability_report.txt
# -> Produces a complete LLM analysis prompt with all source passages included
```

---

## Notes on Entity Matching

All tools that accept entity name searches use **substring matching** (case-insensitive). This means:

- `water` will match "water infrastructure", "wastewater treatment", "groundwater", etc.
- `gold` will match "gold supply chain", "gold refinery", "anglogold ashanti", etc.

If a search returns too many matches or a path traversal is slow, use a more specific term or add `--dataset` to narrow the scope.

For **`query_path.py` only**, pass **`--token`** for **whole-token** matching: the name is split on non-alphanumeric characters and **every** word in your query must appear as an **exact** token. That way `twistor` matches `twistor theory` and `twistor_theory` but **not** `ambitwistor`, because the only token there is the full word `ambitwistor`.

If a **compound** entity name matches **both** of your search terms (substring match on each), `query_path.py` will report a **zero-hop** path for that entity in addition to any multi-hop chains.

File paths, URLs, and single-character entities are automatically filtered out from entity matching.

---

## Timing Reference

Measured on KG01-tvfmodeling with cache populated:

| Tool | Typical runtime |
|---|---|
| `query_top_catagories.py` | ~65ms |
| `query_children.py` | ~57ms |
| `query_sources.py` (tabular) | ~120ms |
| `query_sources.py --text` | ~150ms |
| `query_path.py` (graph load + BFS) | ~110ms |
| `query_path.py --report` | ~500ms |
| `query_path.py --analysis` | Graph work as above plus one API round trip per path (seconds, depends on latency) |
| `query_path.py --research` | As above plus a second web-search request per path (longer; extra API and search usage) |
| `query_search.py` | ~200ms |
| `query_search.py --in-text` | ~300ms |

Without cache (fallback mode): 5-10 seconds per query due to TTL parsing and complex SQL joins.

---

## Output Files in This Folder

| File | Description |
|---|---|
| `build_kg_cache.py` | Step 0: cache builder (run once before first use) |
| `query_top_catagories.py` | Step 1: category overview |
| `query_children.py` | Step 2: category member listing |
| `query_sources.py` | Step 3: triple retrieval with source text |
| `query_search.py` | Free-text and relationship-name search |
| `query_path.py` | Step 4: graph path traversal; optional `--report` / `--analysis` |
| `qanalysis/` | Output directory for `--analysis` runs (Markdown `.md` files, created on demand) |
| `cTVF-merged.ttl` | Base OWL ontology (all datasets merged) |
| `property_groups.ttl` | Abstract property group hierarchy (20 categories) |
| `analysis_depends_on.md` | Worked example analysis using `depends_on`, including path discovery and source text grounding for the twistor-sustainability connection |
