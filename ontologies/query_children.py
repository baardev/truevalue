#!/usr/bin/env python3
"""
List all member relationship names within an abstract category.
Uses kg_property_groups cache table; falls back to TTL parsing if cache absent.

Usage:
    ./query_children.py <group> [--limit N] [--dataset DATASET]

Examples:
    ./query_children.py causation
    ./query_children.py parthood --limit 20
"""
import os, sys
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
except ImportError:
    sys.exit("ERROR: psycopg2 not installed.")

HERE = Path(__file__).parent

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

def cache_exists(conn):
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('kg_property_groups')")
    return cur.fetchone()[0] is not None

def parse_args():
    args = sys.argv[1:]
    positional, limit, dataset = [], None, None
    i = 0
    while i < len(args):
        if args[i] in ("--limit", "-l") and i + 1 < len(args):
            limit = int(args[i + 1]); i += 2
        elif args[i] in ("--dataset", "-d") and i + 1 < len(args):
            dataset = args[i + 1]; i += 2
        elif not args[i].startswith("-"):
            positional.append(args[i]); i += 1
        else:
            i += 1
    group = " ".join(positional).lower().strip()
    return group, limit, dataset

def main():
    group, limit, dataset = parse_args()
    if not group:
        print(__doc__); sys.exit(1)

    conn = pg_connect()

    if cache_exists(conn):
        cur = conn.cursor()
        # Get all groups for fuzzy match
        cur.execute("SELECT DISTINCT group_name FROM kg_property_groups ORDER BY group_name")
        all_groups = [r[0] for r in cur.fetchall()]
        matched = [g for g in all_groups if g.lower() == group]
        if not matched:
            matched = [g for g in all_groups if group in g.lower()]
        if not matched:
            print(f"  No group named '{group}' found.\n  Available groups:")
            for g in all_groups:
                print(f"    {g}")
            conn.close(); return

        group_name = matched[0]
        cur.execute("""
            SELECT child_name FROM kg_property_groups
            WHERE group_name = %s
            ORDER BY child_name
        """, (group_name,))
        children = [r[0] for r in cur.fetchall()]
    else:
        conn.close()
        print("  (cache not built; falling back to TTL)\n")
        from rdflib import Graph
        g = Graph()
        g.parse(HERE / "property_groups.ttl")
        g.parse(HERE / "cTVF-merged.ttl")
        results = g.query("""
            PREFIX owl:  <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?group_label ?child_label WHERE {
                ?grp a owl:ObjectProperty ; rdfs:label ?group_label .
                ?child rdfs:subPropertyOf ?grp ; rdfs:label ?child_label .
            } ORDER BY ?group_label ?child_label
        """)
        groups = {}
        for row in results:
            gl = str(row.group_label).lower()
            groups.setdefault(gl, []).append(str(row.child_label))
        if group not in groups:
            print(f"  No group named '{group}' found.\n  Available groups: {', '.join(sorted(groups))}")
            return
        group_name = group
        children = groups[group]
        conn = None

    total = len(children)
    display = children[:limit] if limit else children

    print(f"\n=== MEMBERS OF '{group_name}' ({total} total) ===\n")
    for i, child in enumerate(display, 1):
        print(f"  {i:>4}.  {child}")
    print()
    if limit and total > limit:
        print(f"  (showing {limit} of {total}; use --limit {total} to see all)\n")

    if conn:
        conn.close()

if __name__ == "__main__":
    main()
