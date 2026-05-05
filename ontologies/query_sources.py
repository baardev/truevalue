#!/usr/bin/env python3
"""
Query actual source data (entity-relationship-entity triples) from the
cognee PostgreSQL knowledge graph for a given relationship or group.

Usage:
    ./ontologies/query_sources.py depends_on
    ./ontologies/query_sources.py causation              # all members of the group
    ./ontologies/query_sources.py causation:depends_on   # specific child (use : not >)
    ./ontologies/query_sources.py depends_on --limit 50
    ./ontologies/query_sources.py causation --limit 100 --dataset KG01-tvfmodeling
    ./ontologies/query_sources.py depends_on --text      # include source chunk text
    ./ontologies/query_sources.py depends_on --text --limit 5

NOTE: use colon (:) not greater-than (>) to separate group from child.
      The > character is a bash redirect operator and will break the command.
      Wrong:  ./query_sources.py causation>depends_on
      Right:  ./query_sources.py causation:depends_on
"""
import os
import sys
from pathlib import Path

try:
    from dotenv import find_dotenv, load_dotenv
    _p = find_dotenv(usecwd=True) or find_dotenv(str(Path(__file__).parent)) or find_dotenv("/home/jw/src/cognee")
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

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

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


def get_group_members(group_name: str) -> list[str]:
    """Return all sub-property names for a group. Uses cache if available."""
    conn = pg_connect()
    if _cache_exists(conn):
        cur = conn.cursor()
        cur.execute("""
            SELECT child_name FROM kg_property_groups
            WHERE lower(group_name) = lower(%s)
            ORDER BY child_name
        """, (group_name,))
        members = [r[0] for r in cur.fetchall()]
        conn.close()
        return members
    conn.close()
    # Fallback: parse TTL
    g = Graph()
    g.parse(HERE / "property_groups.ttl")
    members = []
    for row in g.query("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?propLabel ?groupLabel WHERE {
            ?prop rdfs:subPropertyOf ?group ;
                  rdfs:label ?propLabel .
            ?group rdfs:label ?groupLabel .
        } ORDER BY ?propLabel
    """):
        if str(row.groupLabel).lower() == group_name.lower():
            members.append(str(row.propLabel))
    return members


def list_groups() -> list[str]:
    """Return all group names. Uses cache if available."""
    conn = pg_connect()
    if _cache_exists(conn):
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT group_name FROM kg_property_groups ORDER BY group_name")
        groups = [r[0] for r in cur.fetchall()]
        conn.close()
        return groups
    conn.close()
    g = Graph()
    g.parse(HERE / "property_groups.ttl")
    groups = []
    for row in g.query("""
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label WHERE {
            ?group a owl:ObjectProperty ; rdfs:label ?label .
            ?child rdfs:subPropertyOf ?group .
        } GROUP BY ?label ORDER BY ?label
    """):
        groups.append(str(row.label))
    return groups


def query_triples(
    rel_names: list[str],
    limit: int,
    dataset_filter: str | None,
    include_text: bool = False,
) -> list[dict]:
    conn = pg_connect()
    cur = conn.cursor()
    use_cache = _cache_exists(conn)

    placeholders = ", ".join(["%s"] * len(rel_names))
    params: list = list(rel_names)

    ds_where = ""
    if dataset_filter:
        ds_where = "AND dataset_name ILIKE %s" if use_cache else "AND d2.name ILIKE %s"
        params.append(f"%{dataset_filter}%")
    params.append(limit)

    if use_cache and not include_text:
        cur.execute(f"""
            SELECT source_name, relationship, target_name, dataset_name
            FROM kg_flat_triples
            WHERE relationship IN ({placeholders})
              {ds_where}
            ORDER BY relationship, source_name
            LIMIT %s
        """, params)

    elif use_cache and include_text:
        cur.execute(f"""
            SELECT DISTINCT ON (ft.source_name, ft.relationship, ft.target_name)
                ft.source_name,
                ft.relationship,
                ft.target_name,
                ft.dataset_name,
                ec.context_text    AS shared_text,
                src_ctx.context_text AS source_text,
                tgt_ctx.context_text AS target_text
            FROM kg_flat_triples ft
            LEFT JOIN kg_edge_context   ec      ON ec.source_slug  = ft.source_slug
                                               AND ec.target_slug  = ft.target_slug
            LEFT JOIN kg_entity_context src_ctx ON src_ctx.entity_slug = ft.source_slug
            LEFT JOIN kg_entity_context tgt_ctx ON tgt_ctx.entity_slug = ft.target_slug
            WHERE ft.relationship IN ({placeholders})
              {ds_where}
            ORDER BY ft.source_name, ft.relationship, ft.target_name
            LIMIT %s
        """, params)

    elif include_text:
        # Fallback: original complex join
        ds_where_raw = "AND d2.name ILIKE %s" if dataset_filter else ""
        cur.execute(f"""
            SELECT DISTINCT ON (ns.attributes->>'name', e.relationship_name, nt.attributes->>'name')
                ns.attributes->>'name',
                e.relationship_name,
                nt.attributes->>'name',
                d2.name,
                dc.attributes->>'text',
                dc_src.txt,
                dc_tgt.txt
            FROM edges e
            JOIN nodes ns ON ns.slug = e.source_node_id  AND ns.type = 'Entity'
            JOIN nodes nt ON nt.slug = e.destination_node_id AND nt.type = 'Entity'
            JOIN datasets d2 ON d2.id = ns.dataset_id
            JOIN edges ec_s  ON ec_s.destination_node_id = ns.slug
            JOIN nodes dc    ON dc.slug = ec_s.source_node_id AND dc.type = 'DocumentChunk'
            JOIN edges ec_t  ON ec_t.source_node_id = dc.slug
                            AND ec_t.destination_node_id = nt.slug
            LEFT JOIN LATERAL (
                SELECT n2.attributes->>'text' AS txt
                FROM edges e2
                JOIN nodes n2 ON n2.slug = e2.source_node_id AND n2.type = 'DocumentChunk'
                WHERE e2.destination_node_id = ns.slug AND n2.attributes->>'text' IS NOT NULL
                ORDER BY length(n2.attributes->>'text') DESC LIMIT 1
            ) dc_src ON true
            LEFT JOIN LATERAL (
                SELECT n3.attributes->>'text' AS txt
                FROM edges e3
                JOIN nodes n3 ON n3.slug = e3.source_node_id AND n3.type = 'DocumentChunk'
                WHERE e3.destination_node_id = nt.slug AND n3.attributes->>'text' IS NOT NULL
                ORDER BY length(n3.attributes->>'text') DESC LIMIT 1
            ) dc_tgt ON true
            WHERE e.relationship_name IN ({placeholders})
              AND dc.attributes->>'text' IS NOT NULL
              {ds_where_raw}
            ORDER BY ns.attributes->>'name', e.relationship_name, nt.attributes->>'name'
            LIMIT %s
        """, params)

    else:
        ds_where_raw = "AND d2.name ILIKE %s" if dataset_filter else ""
        cur.execute(f"""
            SELECT ns.attributes->>'name', e.relationship_name,
                   nt.attributes->>'name', d2.name
            FROM edges e
            JOIN nodes ns ON ns.slug = e.source_node_id
            JOIN nodes nt ON nt.slug = e.destination_node_id
            JOIN datasets d2 ON d2.id = ns.dataset_id
            WHERE e.relationship_name IN ({placeholders})
              AND ns.attributes->>'name' IS NOT NULL
              AND nt.attributes->>'name' IS NOT NULL
              {ds_where_raw}
            ORDER BY e.relationship_name, ns.attributes->>'name'
            LIMIT %s
        """, params)

    rows = [
        {
            "source":       r[0],
            "relationship": r[1],
            "target":       r[2],
            "dataset":      r[3],
            "shared_text":  r[4] if include_text else None,
            "source_text":  r[5] if include_text else None,
            "target_text":  r[6] if include_text else None,
        }
        for r in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return rows


def count_triples(rel_names: list[str], dataset_filter: str | None) -> dict[str, int]:
    conn = pg_connect()
    cur = conn.cursor()
    use_cache = _cache_exists(conn)
    placeholders = ", ".join(["%s"] * len(rel_names))
    params: list = list(rel_names)

    if use_cache:
        ds_where = "AND dataset_name ILIKE %s" if dataset_filter else ""
        if dataset_filter:
            params.append(f"%{dataset_filter}%")
        cur.execute(f"""
            SELECT relationship, COUNT(*) AS cnt
            FROM kg_flat_triples
            WHERE relationship IN ({placeholders})
              {ds_where}
            GROUP BY relationship ORDER BY cnt DESC
        """, params)
    else:
        ds_join = ds_where = ""
        if dataset_filter:
            ds_join  = "JOIN datasets d ON d.id = ns.dataset_id"
            ds_where = "AND d.name ILIKE %s"
            params.append(f"%{dataset_filter}%")
        cur.execute(f"""
            SELECT e.relationship_name, COUNT(*) AS cnt
            FROM edges e
            JOIN nodes ns ON ns.slug = e.source_node_id
            {ds_join}
            WHERE e.relationship_name IN ({placeholders})
              {ds_where}
            GROUP BY e.relationship_name ORDER BY cnt DESC
        """, params)

    counts = {r[0]: r[1] for r in cur.fetchall()}
    cur.close()
    conn.close()
    return counts


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    args = sys.argv[1:]
    limit = 20
    dataset = None
    include_text = False
    positional = []

    i = 0
    while i < len(args):
        if args[i] in ("--limit", "-n") and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif args[i].startswith("--limit="):
            limit = int(args[i].split("=", 1)[1])
            i += 1
        elif args[i] in ("--dataset", "-d") and i + 1 < len(args):
            dataset = args[i + 1]
            i += 2
        elif args[i].startswith("--dataset="):
            dataset = args[i].split("=", 1)[1]
            i += 1
        elif args[i] in ("--text", "-t"):
            include_text = True
            i += 1
        else:
            positional.append(args[i])
            i += 1

    return " ".join(positional), limit, dataset, include_text


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    query_str, limit, dataset, include_text = parse_args()

    if not query_str:
        print(__doc__)
        sys.exit(1)

    # Resolve what was requested
    # Formats:  "depends_on"  /  "causation"  /  "causation>depends_on"
    rel_names: list[str] = []
    group_name: str | None = None
    specific_rel: str | None = None

    # Support both "causation:depends_on" and (quoted) "causation>depends_on"
    separator = ":" if ":" in query_str else ">" if ">" in query_str else None
    if separator:
        parts = query_str.split(separator, 1)
        group_name   = parts[0].strip()
        specific_rel = parts[1].strip()
        rel_names    = [specific_rel]
    else:
        # Try as a group name first
        members = get_group_members(query_str)
        if members:
            group_name = query_str
            rel_names  = members
        else:
            # Treat as a direct relationship name
            specific_rel = query_str
            rel_names    = [query_str]

    if not rel_names:
        print(f"Nothing found for '{query_str}'.")
        print("\nAvailable groups:")
        for g in list_groups():
            print(f"  {g}")
        sys.exit(1)

    # Count totals first
    counts = count_triples(rel_names, dataset)
    total = sum(counts.values())

    # Header
    if group_name and not specific_rel:
        print(f"=== GROUP: {group_name.upper()}  ({len(rel_names)} properties, {total:,} total triples) ===")
        if dataset:
            print(f"    Dataset filter: {dataset}")
        print()
        print("  Breakdown by property:")
        for rel in rel_names:
            n = counts.get(rel, 0)
            if n:
                print(f"    {n:6,}  {rel}")
        print()
    else:
        rel_label = specific_rel or rel_names[0]
        parent = f"  (in group: {group_name})" if group_name else ""
        print(f"=== RELATIONSHIP: {rel_label}{parent}  ({total:,} triples) ===")
        if dataset:
            print(f"    Dataset filter: {dataset}")
        print()

    # Fetch and display sample triples
    rows = query_triples(rel_names, limit, dataset, include_text)

    if not rows:
        print("  (no triples found)")
        return

    def _wrap(text: str, indent: int = 8, width: int = 76, max_lines: int = 15) -> str:
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

    if include_text:
        for i, r in enumerate(rows, 1):
            ds = (r["dataset"] or "")
            if "_" in ds:
                ds = ds.split("_", 1)[1]
            print(f"  [{i}]  {r['source']}  --{r['relationship']}-->  {r['target']}")
            print(f"        Dataset: {ds}")
            print()

            shared = r["shared_text"] or ""
            src    = r["source_text"] or ""
            tgt    = r["target_text"] or ""

            # Shared context (where the relationship was extracted)
            if shared:
                print(f"        RELATIONSHIP CONTEXT (passage containing both entities):")
                print(_wrap(shared))
                print()

            # Source-specific context (if different from shared)
            if src and src.strip() != shared.strip():
                print(f"        SOURCE CONTEXT  [{r['source']}]:")
                print(_wrap(src))
                print()

            # Target-specific context (if different from shared)
            if tgt and tgt.strip() != shared.strip():
                print(f"        TARGET CONTEXT  [{r['target']}]:")
                print(_wrap(tgt))
                print()

            print("  " + "─" * 70)
    else:
        # Tabular display
        src_w = min(40, max(len(r["source"])       for r in rows))
        rel_w = min(35, max(len(r["relationship"])  for r in rows))
        tgt_w = min(40, max(len(r["target"])        for r in rows))

        header = f"  {'SOURCE':{src_w}}  {'RELATIONSHIP':{rel_w}}  {'TARGET':{tgt_w}}  DATASET"
        print(header)
        print("  " + "-" * (src_w + rel_w + tgt_w + 20))

        for r in rows:
            src = r["source"][:src_w]
            rel = r["relationship"][:rel_w]
            tgt = r["target"][:tgt_w]
            ds  = (r["dataset"] or "")
            if "_" in ds:
                ds = ds.split("_", 1)[1]
            print(f"  {src:{src_w}}  {rel:{rel_w}}  {tgt:{tgt_w}}  {ds}")

    if total > limit:
        print(f"\n  Showing {limit} of {total:,} total.  Use --limit N to see more.")


if __name__ == "__main__":
    main()
