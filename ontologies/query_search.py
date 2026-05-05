#!/usr/bin/env python3
"""
Search for a term across ontology categories, child relationship names,
and optionally inside the source text of document chunks.

Usage:
    ./query_search.py <term> [--dataset DATASET] [--limit N] [--in-text]

Examples:
    ./query_search.py twister
    ./query_search.py twistor --in-text
    ./query_search.py supply --dataset KG01-tvfmodeling
    ./query_search.py balance --limit 20 --in-text

Modes:
    (default)   Search category names and child relationship names in the
                ontology, plus actual relationship_name values in the database.

    --in-text   Search the content of source document chunks for the term.
                Returns every triple (source, relationship, target) that was
                extracted from a passage containing that string, grouped by
                ontology category.
"""

import os
import sys
from pathlib import Path

# ── DB connection (same pattern as query_sources.py) ─────────────────────────
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
except ImportError:
    sys.exit("ERROR: psycopg2 not installed. Run: pip install psycopg2-binary")

try:
    from rdflib import Graph
except ImportError:
    sys.exit("ERROR: rdflib not installed. Run: pip install rdflib")

HERE = Path(__file__).parent

DATASET_ALIASES = {
    "KG01":              "ope-voy_KG01-tvfmodeling",
    "KG01-tvfmodeling":  "ope-voy_KG01-tvfmodeling",
    "KG02":              "ope-voy_KG02-tholonia-book",
    "KG02-tholonia-book":"ope-voy_KG02-tholonia-book",
    "KG03":              "ope-voy_KG03-iching_intro",
    "KG03-iching_intro": "ope-voy_KG03-iching_intro",
}


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


def _cache_exists(conn) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('kg_property_groups')")
    return cur.fetchone()[0] is not None


def build_group_map() -> dict:
    """Map child_name -> group_name. Uses cache if available."""
    conn = pg_connect()
    if _cache_exists(conn):
        cur = conn.cursor()
        cur.execute("SELECT group_name, child_name FROM kg_property_groups")
        result = {child: group for group, child in cur.fetchall()}
        conn.close()
        return result
    conn.close()
    from rdflib import Graph
    g = Graph()
    g.parse(HERE / "property_groups.ttl")
    g.parse(HERE / "cTVF-merged.ttl")
    results = g.query("""
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?group_label ?child_label WHERE {
            ?group a owl:ObjectProperty ; rdfs:label ?group_label .
            ?child rdfs:subPropertyOf ?group ; rdfs:label ?child_label .
        }
    """)
    return {str(r.child_label): str(r.group_label) for r in results}


def search_ontology(term: str):
    """Return (category_label, child_label) pairs where the term appears."""
    conn = pg_connect()
    t = term.lower()
    category_hits, child_hits, seen_cats = [], [], set()

    if _cache_exists(conn):
        cur = conn.cursor()
        cur.execute("SELECT group_name, child_name FROM kg_property_groups ORDER BY group_name, child_name")
        for group, child in cur.fetchall():
            if t in group.lower() and group not in seen_cats:
                category_hits.append(group); seen_cats.add(group)
            if t in child.lower():
                child_hits.append((group, child))
        conn.close()
        return category_hits, child_hits

    conn.close()
    from rdflib import Graph
    g = Graph()
    g.parse(HERE / "property_groups.ttl")
    g.parse(HERE / "cTVF-merged.ttl")
    for row in g.query("""
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?group_label ?child_label WHERE {
            ?group a owl:ObjectProperty ; rdfs:label ?group_label .
            ?child rdfs:subPropertyOf ?group ; rdfs:label ?child_label .
        } ORDER BY ?group_label ?child_label
    """):
        gl, cl = str(row.group_label), str(row.child_label)
        if t in gl.lower() and gl not in seen_cats:
            category_hits.append(gl); seen_cats.add(gl)
        if t in cl.lower():
            child_hits.append((gl, cl))
    return category_hits, child_hits


def search_database(term: str, dataset: str | None, limit: int):
    """Search relationship names in the graph for the term."""
    conn = pg_connect()
    cur = conn.cursor()

    ds_name = DATASET_ALIASES.get(dataset, dataset) if dataset else None

    if _cache_exists(conn):
        ds_where = "AND dataset_name = %s" if ds_name else ""
        params = [f"%{term}%"]
        if ds_name:
            # strip prefix if needed
            ds_short = ds_name.split("_", 1)[-1]
            params.append(ds_short)
        params.append(limit)
        cur.execute(f"""
            SELECT relationship, COUNT(*) AS cnt, dataset_name
            FROM kg_flat_triples
            WHERE relationship ILIKE %s
              {ds_where}
            GROUP BY relationship, dataset_name
            ORDER BY cnt DESC
            LIMIT %s
        """, params)
    else:
        ds_where = "AND d.name = %s" if ds_name else ""
        params = [f"%{term}%"]
        if ds_name:
            params.append(ds_name)
        params.append(limit)
        cur.execute(f"""
            SELECT e.relationship_name, COUNT(*) AS cnt, d.name
            FROM edges e
            JOIN nodes ns ON ns.slug = e.source_node_id AND ns.type = 'Entity'
            JOIN nodes nt ON nt.slug = e.destination_node_id AND nt.type = 'Entity'
            JOIN datasets d ON d.id = ns.dataset_id
            WHERE e.relationship_name ILIKE %s
              {ds_where}
            GROUP BY e.relationship_name, d.name
            ORDER BY cnt DESC
            LIMIT %s
        """, params)

    rows = cur.fetchall()
    conn.close()
    return rows


def search_in_text(term: str, dataset: str | None, limit: int, group_map: dict):
    """Find triples extracted from chunks whose text contains the search term."""
    conn = pg_connect()
    cur = conn.cursor()

    ds_name = DATASET_ALIASES.get(dataset, dataset) if dataset else None
    ds_where = "AND d.name = %s" if ds_name else ""
    params = [f"%{term}%"]
    if ds_name:
        params.append(ds_name)
    params.append(limit)

    cur.execute(f"""
        SELECT DISTINCT
            ns.attributes->>'name'   AS source,
            e.relationship_name      AS relationship,
            nt.attributes->>'name'   AS target,
            d.name                   AS dataset,
            dc.attributes->>'text'   AS chunk_text
        FROM edges e
        JOIN nodes ns  ON ns.slug = e.source_node_id      AND ns.type = 'Entity'
        JOIN nodes nt  ON nt.slug = e.destination_node_id AND nt.type = 'Entity'
        JOIN datasets d ON d.id = ns.dataset_id
        -- chunk linked to source entity
        JOIN edges ec  ON ec.destination_node_id = ns.slug
        JOIN nodes dc  ON dc.slug = ec.source_node_id     AND dc.type = 'DocumentChunk'
        WHERE dc.attributes->>'text' ILIKE %s
          AND ns.attributes->>'name' IS NOT NULL
          AND nt.attributes->>'name' IS NOT NULL
          {ds_where}
        ORDER BY e.relationship_name, ns.attributes->>'name'
        LIMIT %s
    """, params)

    rows = cur.fetchall()
    conn.close()
    return rows


def parse_args():
    args = sys.argv[1:]
    term = None
    dataset = None
    limit = 30
    in_text = False
    i = 0
    while i < len(args):
        if args[i] in ("--dataset", "-d") and i + 1 < len(args):
            dataset = args[i + 1]; i += 2
        elif args[i] in ("--limit", "-l") and i + 1 < len(args):
            limit = int(args[i + 1]); i += 2
        elif args[i] == "--in-text":
            in_text = True; i += 1
        elif not args[i].startswith("-"):
            term = args[i]; i += 1
        else:
            i += 1
    return term, dataset, limit, in_text


def _wrap(text: str, indent: int = 6, width: int = 78, max_lines: int = 6) -> str:
    pad = " " * indent
    words = (text or "").strip().replace('\n', ' ').split()
    line, out_lines = [], []
    for w in words:
        if sum(len(x) + 1 for x in line) + len(w) > width:
            out_lines.append(pad + " ".join(line))
            line = [w]
        else:
            line.append(w)
    if line:
        out_lines.append(pad + " ".join(line))
    result = "\n".join(out_lines[:max_lines])
    if len(out_lines) > max_lines:
        result += f"\n{pad}[... truncated ...]"
    return result


def main():
    term, dataset, limit, in_text = parse_args()
    if not term:
        print(__doc__)
        sys.exit(1)

    print(f"\n  Search term: '{term}'")
    if dataset:
        print(f"  Dataset:     {dataset}")
    if in_text:
        print(f"  Mode:        full-text search inside document chunks")
    print()

    group_map = build_group_map()

    # ── Full-text mode: search inside chunk text ───────────────────────────────
    if in_text:
        rows = search_in_text(term, dataset, limit, group_map)
        if not rows:
            print(f"  No triples found in chunks containing '{term}'.\n")
            return

        # Group results by ontology category
        from collections import defaultdict
        by_group = defaultdict(list)
        for src, rel, tgt, ds, chunk in rows:
            group = group_map.get(rel, "(unmapped)")
            by_group[group].append((src, rel, tgt, ds, chunk))

        print(f"  Found {len(rows)} triple(s) from chunks containing '{term}',")
        print(f"  across {len(by_group)} relationship group(s):\n")

        for group in sorted(by_group):
            entries = by_group[group]
            print(f"  [{group.upper()}]  ({len(entries)} triples)")
            print(f"  {'SOURCE':<30}  {'RELATIONSHIP':<30}  TARGET")
            print("  " + "-" * 90)
            for src, rel, tgt, ds, chunk in entries:
                ds_short = ds.split("_", 1)[1] if "_" in ds else ds
                print(f"  {src:<30}  {rel:<30}  {tgt}")
            print()

            # Show one example passage per group
            _, _, _, _, sample_chunk = entries[0]
            print(f"  Example passage (from '{entries[0][3].split('_',1)[-1]}'):")
            print(_wrap(sample_chunk or ""))
            print()
            print("  " + "─" * 90)

        if len(rows) == limit:
            print(f"  (showing top {limit}; use --limit N to see more)")
        return

    # ── Default mode: search relationship names ───────────────────────────────
    cat_hits, child_hits = search_ontology(term)

    if cat_hits:
        print(f"  CATEGORY MATCHES ({len(cat_hits)}):")
        for c in cat_hits:
            print(f"    [category]  {c}")
        print()

    if child_hits:
        print(f"  CHILD RELATIONSHIP MATCHES IN ONTOLOGY ({len(child_hits)}):")
        for group, child in child_hits:
            print(f"    {child:<40}  (group: {group})")
        print()

    if not cat_hits and not child_hits:
        print("  No matches in ontology (categories or child relationships).\n")

    db_rows = search_database(term, dataset, limit)

    if db_rows:
        print(f"  DATABASE MATCHES — relationship names containing '{term}':")
        print(f"  {'RELATIONSHIP':<45}  {'TRIPLES':>8}  {'GROUP':<22}  DATASET")
        print("  " + "-" * 110)
        for rel, count, ds in db_rows:
            ds_short = ds.split("_", 1)[1] if "_" in ds else ds
            group = group_map.get(rel, "(unmapped)")
            print(f"  {rel:<45}  {count:>8,}  {group:<22}  {ds_short}")
        print()
        if len(db_rows) == limit:
            print(f"  (showing top {limit}; use --limit N to see more)")
    else:
        print(f"  No database triples found with relationship names containing '{term}'.\n")


if __name__ == "__main__":
    main()
