---
doc_id: frontend_docs_index
title: Documentation wiki
type: documentation
status: active
domain: project_documentation
layer: methodology
projects:
  []
tags:
  - methodology
  - project_documentation
related_docs:
  []
key_claims:
  []
---

# Documentation wiki

Welcome to the **Supply Chain Intelligence** documentation. This wiki covers supply- and value-chain modeling (including gold, shea, and AUBEB where documented), rules, APIs, and methodology.

Paths below are **relative to the documentation root** (`frontend/docs/` in the repository; for example `Repos/intra/PDI/…` on disk is `frontend/docs/Repos/intra/PDI/…`).

## Quick links

| Section | Description |
|--------|-------------|
| [Abstract template](Repos/intra/PDI/ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE.md) | Product-agnostic phase template (0-8) with N-D-C tagging and example metric types |
| [Gold instance](Repos/intra/PDI/ABSTRACT_SUPPLY_CHAIN_PHASE_TEMPLATE_GOLD_INSTANCE.md) | Gold supply chain instance of the same template (phases 0-8) |
| [Abstract value template](Repos/intra/PDI/ABSTRACT_VALUE_CHAIN_PHASE_TEMPLATE.md) | Value chain phase template (profit, pricing, margins); phases align with supply by id |
| [Shea value instance](Repos/intra/PDI/SHEA_VALUE_CHAIN_PHASE_INSTANCE.md) | Shea value chain instance (income, prices, value to women) |
| [Gold value instance](Repos/intra/PDI/GOLD_VALUE_CHAIN_PHASE_INSTANCE.md) | Gold value chain instance (schema + definitions; value metrics MISSING) |
| [Supply chain rules](Research/modeling/SUPPLY_CHAIN_RULES.md) | AI operating rules for the physical supply chain layer |
| [Value chain rules](Research/modeling/VALUE_CHAIN_RULES.md) | Rules for value chain (profit, pricing, margins) |
| [Frontend API](api/FRONTEND_API.md) | Data contract for the supply chain simulator frontend |
| [Water, waste & environment](Reports/WATER_WASTE_METHODOLOGY.md) | Water, waste, and energy metrics methodology (gold) |
| [TVPCI foundation](Reports/TVPCI_FOUNDATION.html) | TVPCI mathematical foundation (HTML; equations and figures) |

## Structure

Source files are grouped under **`frontend/docs/`** in these **top-level directories** (MkDocs `docs_dir`):

- **`Repos/intra/`** — Primary project trees, including **`PDI/`** (phase templates and protocol), **`TVPCI/`**, **`gametheory/`**, and other intra-repo documentation.
- **`Repos/extra/`** — Static report HTML/PDF variants (e.g. Generic, UBS, Deutsche) referenced from hubs.
- **`Activities/`** — Filled instances and integration write-ups (e.g. shea supply chain, Sarah).
- **`Guidelines/`** — Supply and value chain rules for modeling and AI use.
- **`Reports/`** — Methodology, topical summaries, the [TVPCI foundation (HTML)](Reports/TVPCI_FOUNDATION.html), and linked briefings.
- **`Research/`** — Deeper notes and PDFs, including **`Research/modeling/`**, **`Research/archive/`**, and **`Research/gametheory/`** where present.
- **`api/`** — Frontend and value chain API contracts (`FRONTEND_API.md`, `VALUE_CHAIN_API.md`).
- **`archives/`** — Ad-hoc or supplemental **non-wiki** files (e.g. media); not the main documentation tree.
- **`sites/`** — Mirrored or saved **static web assets** from external sites (HTML/CSS/images); not canonical Markdown sources for the wiki.

Other Markdown and assets may appear at the **documentation root** or nested under the folders above. The **sidebar** follows `scripts/mkdocs.yml`; use **search** for anything not listed as a first-class page.
