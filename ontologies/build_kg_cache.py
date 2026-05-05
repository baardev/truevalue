#!/usr/bin/env python3
"""
Build the KG query cache tables in PostgreSQL.

Populates four tables that replace slow TTL parsing and complex joins:

  kg_property_groups  -- ontology group -> child relationship name mapping
  kg_flat_triples     -- fully denormalized entity-entity triples with group labels
  kg_entity_context   -- best source text passage per entity
  kg_edge_context     -- best co-occurrence passage per (source, target) pair

Run once after cognification, or after updating the ontology TTL files.
Re-running is safe: tables are dropped and rebuilt from scratch.

Usage:
    ./build_kg_cache.py [--skip-text] [--dataset DATASET]

    --skip-text     Skip populating kg_entity_context and kg_edge_context
                    (text retrieval is slow; use this for a fast structural rebuild)
    --dataset       Only process one dataset (default: all three)
"""

import os
import sys
import time
from pathlib import Path

try:
    from dotenv import find_dotenv, load_dotenv
    _p = (find_dotenv(usecwd=True)
          or find_dotenv(str(Path(__file__).parent))
          or find_dotenv("/home/jw/src/cognee"))
    if _p:
        load_dotenv(dotenv_path=_p, override=True)
except ImportError:
    pass

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    sys.exit("ERROR: psycopg2 not installed. Run: pip install psycopg2-binary")

try:
    from rdflib import Graph
except ImportError:
    sys.exit("ERROR: rdflib not installed. Run: pip install rdflib")

HERE = Path(__file__).parent

DATASET_ALIASES = {
    "KG01":               "ope-voy_KG01-tvfmodeling",
    "KG01-tvfmodeling":   "ope-voy_KG01-tvfmodeling",
    "KG02":               "ope-voy_KG02-tholonia-book",
    "KG02-tholonia-book": "ope-voy_KG02-tholonia-book",
    "KG03":               "ope-voy_KG03-iching_intro",
    "KG03-iching_intro":  "ope-voy_KG03-iching_intro",
}
ALL_DATASETS = ["ope-voy_KG01-tvfmodeling",
                "ope-voy_KG02-tholonia-book",
                "ope-voy_KG03-iching_intro"]


def pg_connect():
    url = os.getenv("DB_URL") or os.getenv("DATABASE_URL")
    if url:
        return psycopg2.connect(url)
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "cognee_db"),
        user=os.getenv("DB_USERNAME", "cognee"),
        password=os.getenv("DB_PASSWORD", "cognee"),
    )


def status(msg: str, end="\n"):
    print(f"  {msg}", end=end, flush=True)


# ── Schema ────────────────────────────────────────────────────────────────────

DDL = """
DROP TABLE IF EXISTS kg_edge_context;
DROP TABLE IF EXISTS kg_entity_context;
DROP TABLE IF EXISTS kg_flat_triples;
DROP TABLE IF EXISTS kg_property_groups;

CREATE TABLE kg_property_groups (
    group_name  TEXT NOT NULL,
    child_name  TEXT NOT NULL,
    PRIMARY KEY (group_name, child_name)
);

CREATE TABLE kg_flat_triples (
    id              SERIAL PRIMARY KEY,
    dataset_name    TEXT NOT NULL,
    source_slug     TEXT NOT NULL,
    source_name     TEXT NOT NULL,
    relationship    TEXT NOT NULL,
    rel_group       TEXT,
    target_slug     TEXT NOT NULL,
    target_name     TEXT NOT NULL
);
CREATE INDEX kg_ft_rel      ON kg_flat_triples(relationship);
CREATE INDEX kg_ft_source   ON kg_flat_triples(source_name);
CREATE INDEX kg_ft_target   ON kg_flat_triples(target_name);
CREATE INDEX kg_ft_dataset  ON kg_flat_triples(dataset_name);
CREATE INDEX kg_ft_group    ON kg_flat_triples(rel_group);
CREATE INDEX kg_ft_src_text ON kg_flat_triples USING gin(to_tsvector('english', source_name));
CREATE INDEX kg_ft_tgt_text ON kg_flat_triples USING gin(to_tsvector('english', target_name));

CREATE TABLE kg_entity_context (
    entity_slug     TEXT NOT NULL,
    dataset_name    TEXT NOT NULL,
    entity_name     TEXT,
    context_text    TEXT,
    PRIMARY KEY (entity_slug, dataset_name)
);
CREATE INDEX kg_ec_name ON kg_entity_context(entity_name);

CREATE TABLE kg_edge_context (
    source_slug     TEXT NOT NULL,
    target_slug     TEXT NOT NULL,
    context_text    TEXT,
    PRIMARY KEY (source_slug, target_slug)
);
"""


# ── Step 1: Property groups from TTL ─────────────────────────────────────────

def build_property_groups(conn):
    status("Building kg_property_groups from TTL files... ", end="")
    t0 = time.time()

    g = Graph()
    g.parse(HERE / "property_groups.ttl")
    g.parse(HERE / "cTVF-merged.ttl")

    rows = []
    for row in g.query("""
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?group_label ?child_label WHERE {
            ?group a owl:ObjectProperty ;
                   rdfs:label ?group_label .
            ?child rdfs:subPropertyOf ?group ;
                   rdfs:label ?child_label .
        }
    """):
        rows.append((str(row.group_label), str(row.child_label)))

    cur = conn.cursor()
    execute_values(cur,
        "INSERT INTO kg_property_groups (group_name, child_name) VALUES %s ON CONFLICT DO NOTHING",
        rows)
    conn.commit()
    status(f"done  ({len(rows):,} mappings in {time.time()-t0:.1f}s)")
    return {child: group for group, child in rows}


# ── Step 2: Flat triples ──────────────────────────────────────────────────────

def build_flat_triples(conn, dataset_names: list, group_map: dict):
    status(f"Building kg_flat_triples for {len(dataset_names)} dataset(s)...")
    t0 = time.time()
    cur = conn.cursor()
    total = 0

    for ds_name in dataset_names:
        ds_short = ds_name.split("_", 1)[-1]
        status(f"  Loading edges from {ds_short}... ", end="")
        cur.execute("""
            SELECT DISTINCT
                ns.slug,
                ns.attributes->>'name',
                e.relationship_name,
                nt.slug,
                nt.attributes->>'name'
            FROM edges e
            JOIN nodes ns ON ns.slug = e.source_node_id      AND ns.type = 'Entity'
            JOIN nodes nt ON nt.slug = e.destination_node_id AND nt.type = 'Entity'
            JOIN datasets d ON d.id = ns.dataset_id AND d.name = %s
            WHERE ns.attributes->>'name' IS NOT NULL
              AND nt.attributes->>'name' IS NOT NULL
        """, (ds_name,))
        raw = cur.fetchall()
        status(f"{len(raw):,} rows, inserting... ", end="")

        rows = [
            (ds_short,
             src_slug, src_name,
             rel, group_map.get(rel),
             tgt_slug, tgt_name)
            for src_slug, src_name, rel, tgt_slug, tgt_name in raw
            if src_name and tgt_name
        ]
        execute_values(cur, """
            INSERT INTO kg_flat_triples
                (dataset_name, source_slug, source_name,
                 relationship, rel_group,
                 target_slug, target_name)
            VALUES %s
        """, rows, page_size=2000)
        conn.commit()
        total += len(rows)
        status(f"done")

    status(f"  Total: {total:,} triples in {time.time()-t0:.1f}s")


# ── Step 3: Entity context (best text chunk per entity) ──────────────────────

def build_entity_context(conn, dataset_names: list):
    """
    For each entity, store the longest DocumentChunk that links to it.
    This is the SOURCE CONTEXT and TARGET CONTEXT used by query_sources --text.
    Uses a single bulk SQL query per dataset (no Python row-by-row loop).
    """
    status("Building kg_entity_context (best source text per entity)...")
    t0 = time.time()
    cur = conn.cursor()
    total = 0

    for ds_name in dataset_names:
        ds_short = ds_name.split("_", 1)[-1]
        status(f"  Processing {ds_short}... ", end="")

        # DISTINCT ON picks the longest chunk per entity in one pass
        cur.execute("""
            INSERT INTO kg_entity_context (entity_slug, dataset_name, entity_name, context_text)
            SELECT DISTINCT ON (ns.slug)
                ns.slug,
                %s,
                ns.attributes->>'name',
                n.attributes->>'text'
            FROM nodes ns
            JOIN datasets d ON d.id = ns.dataset_id AND d.name = %s
            JOIN edges e    ON e.destination_node_id = ns.slug
            JOIN nodes n    ON n.slug = e.source_node_id AND n.type = 'DocumentChunk'
            WHERE ns.type = 'Entity'
              AND ns.attributes->>'name' IS NOT NULL
              AND n.attributes->>'text'  IS NOT NULL
            ORDER BY ns.slug, length(n.attributes->>'text') DESC
            ON CONFLICT DO NOTHING
        """, (ds_short, ds_name))

        n = cur.rowcount
        conn.commit()
        total += n
        status(f"done  ({n:,} entities)")

    status(f"  Total: {total:,} entity contexts in {time.time()-t0:.1f}s")


# ── Step 4: Edge context (co-occurrence chunk per source-target pair) ─────────

def build_edge_context(conn, dataset_names: list):
    """
    For each (source_entity, target_entity) pair, store the longest DocumentChunk
    that contains BOTH entities.  This is the RELATIONSHIP CONTEXT used by
    query_sources --text and query_path --report.
    Uses a single bulk SQL query per dataset.
    """
    status("Building kg_edge_context (co-occurrence text per edge pair)...")
    t0 = time.time()
    cur = conn.cursor()
    total = 0

    for ds_name in dataset_names:
        ds_short = ds_name.split("_", 1)[-1]
        status(f"  Processing {ds_short}... ", end="")

        # DISTINCT ON picks the longest shared chunk per (source, target) pair
        cur.execute("""
            INSERT INTO kg_edge_context (source_slug, target_slug, context_text)
            SELECT DISTINCT ON (ns.slug, nt.slug)
                ns.slug,
                nt.slug,
                dc.attributes->>'text'
            FROM edges e
            JOIN nodes ns   ON ns.slug = e.source_node_id      AND ns.type = 'Entity'
            JOIN nodes nt   ON nt.slug = e.destination_node_id AND nt.type = 'Entity'
            JOIN datasets d ON d.id = ns.dataset_id AND d.name = %s
            -- chunk must link to source entity
            JOIN edges ec_s ON ec_s.destination_node_id = ns.slug
            JOIN nodes dc   ON dc.slug = ec_s.source_node_id AND dc.type = 'DocumentChunk'
            -- same chunk must also link to target entity
            JOIN edges ec_t ON ec_t.source_node_id = dc.slug
                           AND ec_t.destination_node_id = nt.slug
            WHERE dc.attributes->>'text' IS NOT NULL
            ORDER BY ns.slug, nt.slug, length(dc.attributes->>'text') DESC
            ON CONFLICT DO NOTHING
        """, (ds_name,))

        n = cur.rowcount
        conn.commit()
        total += n
        status(f"done  ({n:,} pairs with shared passage)")

    status(f"  Total: {total:,} edge contexts in {time.time()-t0:.1f}s")


# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary(conn):
    cur = conn.cursor()
    status("\n  Cache table sizes:")
    for table in ["kg_property_groups", "kg_flat_triples",
                  "kg_entity_context", "kg_edge_context"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        n = cur.fetchone()[0]
        status(f"    {table:<30} {n:>10,} rows")


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args():
    args = sys.argv[1:]
    skip_text = "--skip-text" in args
    dataset = None
    i = 0
    while i < len(args):
        if args[i] in ("--dataset", "-d") and i + 1 < len(args):
            dataset = args[i + 1]; i += 2
        else:
            i += 1
    return skip_text, dataset


def main():
    skip_text, dataset = parse_args()

    if dataset:
        ds_names = [DATASET_ALIASES.get(dataset, dataset)]
    else:
        ds_names = ALL_DATASETS

    print(f"\n  KG Cache Builder")
    print(f"  Datasets : {', '.join(d.split('_',1)[-1] for d in ds_names)}")
    print(f"  Skip text: {skip_text}")
    print()

    conn = pg_connect()
    cur = conn.cursor()

    status("Creating schema... ", end="")
    cur.execute(DDL)
    conn.commit()
    status("done")
    print()

    group_map = build_property_groups(conn)
    print()
    build_flat_triples(conn, ds_names, group_map)

    if not skip_text:
        print()
        build_entity_context(conn, ds_names)
        print()
        build_edge_context(conn, ds_names)

    print_summary(conn)
    conn.close()

    print()
    status("Cache build complete. All query tools will now use the cache automatically.")
    print()


if __name__ == "__main__":
    main()
