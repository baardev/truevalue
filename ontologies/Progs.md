# Programming manual (`ontologies/`)

Executable scripts in this folder. Usage strings are in each file’s docstring; this file describes roles and dependencies.

All query and cache tools expect **PostgreSQL** access to the Cognee or project KG database (connection via `DB_URL` / `DATABASE_URL` or discrete `DB_*` env vars). Several loaders look for a `.env` (including a fallback path under `/home/jw/src/cognee`).

## `build_kg_cache.py`

Rebuilds **denormalized KG tables** used for fast querying: property groups, flat triples, and optional text context tables for entities and edges. Safe to re-run; replaces cached tables from ontology TTL inputs after ingest.

**Depends on:** Python 3, `psycopg2`, `rdflib`, optional `python-dotenv`.

## `query_search.py`

Search by term across **ontology category names**, **child relationship names**, and stored relationship names; optional mode searches **document chunk text** (`--in-text`).

**Depends on:** Python 3, `psycopg2`, optional `python-dotenv`.

## `query_path.py`

Finds **paths between two entities** (substring match on names) with configurable depth and path cap. Optional modes format LLM-ready reports, call Anthropic for path analysis, and add web research sections.

**Depends on:** Python 3, DB stack as above; optional API keys and extra packages per feature flags (see script header).

## `query_children.py`

Lists **member relationship names** under an abstract ontology group, preferring the `kg_property_groups` cache with TTL fallback.

**Depends on:** Python 3, `psycopg2`, optional `python-dotenv`.

## `query_sources.py`

Pulls **actual triples** from PostgreSQL for a given relationship name or group, with optional source chunk text (`--text`). Note the documented **`group:child`** syntax (colon, not shell redirect).

**Depends on:** Python 3, `psycopg2`, optional `python-dotenv`.

## `query_top_catagories.py`

Ranks **top relationship categories** by predicate volume using the cache (TTL fallback).

**Depends on:** Python 3, `psycopg2`, optional `python-dotenv`.
