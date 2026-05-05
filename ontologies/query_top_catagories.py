#!/usr/bin/env python3
"""
Show the top relationship categories ranked by number of member predicates.
Uses kg_property_groups cache table; falls back to TTL parsing if cache absent.

Usage:
    ./query_top_catagories.py [--dataset DATASET]
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

def from_cache(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT group_name, COUNT(*) AS cnt
        FROM kg_property_groups
        GROUP BY group_name
        ORDER BY cnt DESC
    """)
    return cur.fetchall()

def from_ttl():
    from rdflib import Graph
    g = Graph()
    g.parse(HERE / "property_groups.ttl")
    g.parse(HERE / "cTVF-merged.ttl")
    print(f"Triples loaded: {len(g):,}\n")
    rows = []
    for row in g.query("""
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label (COUNT(?child) AS ?num) WHERE {
            ?group a owl:ObjectProperty ;
                   rdfs:label ?label .
            ?child rdfs:subPropertyOf ?group .
        } GROUP BY ?label ORDER BY DESC(?num)
    """):
        rows.append((str(row.label), int(row.num)))
    return rows

def parse_args():
    args = sys.argv[1:]
    dataset = None
    i = 0
    while i < len(args):
        if args[i] in ("--dataset", "-d") and i + 1 < len(args):
            dataset = args[i + 1]; i += 2
        else:
            i += 1
    return dataset

def main():
    dataset = parse_args()
    conn = pg_connect()

    if cache_exists(conn):
        rows = from_cache(conn)
        source = "cache"
    else:
        conn.close()
        print("  (cache not built; falling back to TTL — run build_kg_cache.py for faster queries)\n")
        rows = from_ttl()
        source = "ttl"
        conn = None

    if dataset:
        print(f"  Dataset filter: {dataset}\n")

    print(f"  {'Category':<25}  Members")
    print(f"  {'-'*35}")
    for name, cnt in rows:
        print(f"  {int(cnt):3}  {name}")

    if conn:
        conn.close()

if __name__ == "__main__":
    main()
