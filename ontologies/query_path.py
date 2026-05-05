#!/usr/bin/env python3
"""
Find relationship paths between two entities in the knowledge graph.
Traverses the graph hop-by-hop to discover both direct and indirect connections.

Usage:
    ./query_path.py <entity1> <entity2> [--dataset DATASET] [--depth N] [--paths N]
                    [--report] [--analysis] [--research] [--token]

Examples:
    ./query_path.py water electricity
    ./query_path.py twistor sustainability --analysis --research
    ./query_path.py gold bank --depth 4 --paths 5
    ./query_path.py twistor sustainability --report
    ./query_path.py twistor sustainability --analysis
    ./query_path.py twistor ecosystem --token --report --analysis

Arguments:
    entity1, entity2    Substrings to match entity names (case-insensitive)
    --dataset / -d      Limit to one dataset (KG01, KG02, KG03, or full name)
    --depth / -n        Maximum hops to search (default: 4)
    --paths / -p        Maximum paths to return (default: 3)
    --report            Include source text for each entity and edge, formatted
                        as a structured analysis prompt ready to paste into an LLM
    --analysis          Send each path to the Anthropic API (claude-sonnet-4-5) and
                        print a structured deduction; results are saved as Markdown under qanalysis/
    --research          After each analysis, run web search and add Markdown sections for further reading
                        and suggested footnotes (implies --analysis; uses KG_RESEARCH_MODEL, see below)
    --token             Whole-token entity matching: excludes embedded substrings (twistor vs ambitwistor)
"""

import hashlib
import os
import re
import sys
import textwrap
from collections import defaultdict, deque
from pathlib import Path

ANTHROPIC_ENV = Path("/home/jw/src/cognee/.env-anthropic")
ANALYSIS_MODEL = "claude-sonnet-4-5"
# Web search (Anthropic server tool) requires a compatible model; override if needed.
RESEARCH_MODEL = os.getenv("KG_RESEARCH_MODEL", "claude-sonnet-4-6")
QANALYSIS_DIR = Path(__file__).parent / "qanalysis"

# Approximate API list prices (USD per million tokens), standard tier for Sonnet 4.5.
# Override with KG_ANALYSIS_PRICE_INPUT_PER_MTOK / KG_ANALYSIS_PRICE_OUTPUT_PER_MTOK.
# Confirm current numbers on https://docs.anthropic.com/en/about-claude/pricing
_ANALYSIS_PRICE_IN_PER_MTOK = float(
    os.getenv("KG_ANALYSIS_PRICE_INPUT_PER_MTOK", "3")
)
_ANALYSIS_PRICE_OUT_PER_MTOK = float(
    os.getenv("KG_ANALYSIS_PRICE_OUTPUT_PER_MTOK", "15")
)

# Single path component byte limit (Linux NAME_MAX is 255 UTF-8 bytes).
_MAX_FN_BYTES = int(os.getenv("KG_PATH_MAX_FILENAME_BYTES", "250"))

# ── DB connection ─────────────────────────────────────────────────────────────
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

DATASET_ALIASES = {
    "KG01":               "ope-voy_KG01-tvfmodeling",
    "KG01-tvfmodeling":   "ope-voy_KG01-tvfmodeling",
    "KG02":               "ope-voy_KG02-tholonia-book",
    "KG02-tholonia-book": "ope-voy_KG02-tholonia-book",
    "KG03":               "ope-voy_KG03-iching_intro",
    "KG03-iching_intro":  "ope-voy_KG03-iching_intro",
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
    cur.execute("SELECT to_regclass('kg_flat_triples')")
    return cur.fetchone()[0] is not None


def load_graph(conn, dataset_names: list):
    """Load entity nodes and edges into memory. Uses cache if available."""
    cur = conn.cursor()

    if _cache_exists(conn):
        # Fast path: single table, pre-denormalized
        ds_shorts = [d.split("_", 1)[-1] for d in dataset_names]
        placeholders = ",".join(["%s"] * len(ds_shorts))
        cur.execute(f"""
            SELECT DISTINCT source_slug, source_name, relationship, target_slug, target_name
            FROM kg_flat_triples
            WHERE dataset_name IN ({placeholders})
        """, ds_shorts)
        rows = cur.fetchall()
        slug_to_name = {}
        adj = defaultdict(list)
        for src_slug, src_name, rel, tgt_slug, tgt_name in rows:
            slug_to_name[src_slug] = src_name
            slug_to_name[tgt_slug] = tgt_name
            adj[src_slug].append((rel, tgt_slug))
        return slug_to_name, adj

    # Fallback: original complex joins
    placeholders = ",".join(["%s"] * len(dataset_names))
    cur.execute(f"""
        SELECT DISTINCT ns.slug, ns.attributes->>'name'
        FROM nodes ns
        JOIN datasets d ON d.id = ns.dataset_id AND d.name IN ({placeholders})
        WHERE ns.type = 'Entity' AND ns.attributes->>'name' IS NOT NULL
    """, dataset_names)
    slug_to_name = {row[0]: row[1] for row in cur.fetchall()}

    cur.execute(f"""
        SELECT DISTINCT e.source_node_id, e.relationship_name, e.destination_node_id
        FROM edges e
        JOIN nodes ns ON ns.slug = e.source_node_id      AND ns.type = 'Entity'
        JOIN nodes nt ON nt.slug = e.destination_node_id AND nt.type = 'Entity'
        JOIN datasets d ON d.id = ns.dataset_id AND d.name IN ({placeholders})
        WHERE ns.attributes->>'name' IS NOT NULL AND nt.attributes->>'name' IS NOT NULL
    """, dataset_names)
    adj = defaultdict(list)
    for src, rel, tgt in cur.fetchall():
        if src in slug_to_name and tgt in slug_to_name:
            adj[src].append((rel, tgt))

    return slug_to_name, adj


def fetch_entity_text(conn, slug: str) -> str:
    """Return the best source text for an entity. Uses cache if available."""
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('kg_entity_context')")
    if cur.fetchone()[0]:
        cur.execute("SELECT context_text FROM kg_entity_context WHERE entity_slug = %s LIMIT 1", (slug,))
    else:
        cur.execute("""
            SELECT n.attributes->>'text'
            FROM edges e
            JOIN nodes n ON n.slug = e.source_node_id AND n.type = 'DocumentChunk'
            WHERE e.destination_node_id = %s AND n.attributes->>'text' IS NOT NULL
            ORDER BY length(n.attributes->>'text') DESC LIMIT 1
        """, (slug,))
    row = cur.fetchone()
    return (row[0] or "").strip() if row else ""


def fetch_edge_text(conn, src_slug: str, tgt_slug: str) -> str:
    """Return the co-occurrence passage for a (source, target) pair. Uses cache if available."""
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('kg_edge_context')")
    if cur.fetchone()[0]:
        cur.execute("""
            SELECT context_text FROM kg_edge_context
            WHERE source_slug = %s AND target_slug = %s LIMIT 1
        """, (src_slug, tgt_slug))
    else:
        cur.execute("""
            SELECT dc.attributes->>'text'
            FROM edges e
            JOIN nodes ns ON ns.slug = e.source_node_id      AND ns.type = 'Entity'
            JOIN nodes nt ON nt.slug = e.destination_node_id AND nt.type = 'Entity'
            JOIN edges ec_s ON ec_s.destination_node_id = ns.slug
            JOIN nodes dc   ON dc.slug = ec_s.source_node_id AND dc.type = 'DocumentChunk'
            JOIN edges ec_t ON ec_t.source_node_id = dc.slug
                           AND ec_t.destination_node_id = nt.slug
            WHERE ns.slug = %s AND nt.slug = %s AND dc.attributes->>'text' IS NOT NULL
            ORDER BY length(dc.attributes->>'text') DESC LIMIT 1
        """, (src_slug, tgt_slug))
    row = cur.fetchone()
    return (row[0] or "").strip() if row else ""


def match_entities(slug_to_name: dict, term: str, token_match: bool = False) -> dict:
    """Return {slug: name} for entities matching term.

    Default: name contains term as a substring (case-insensitive).
    With token_match=True: split term and name on non-alphanumeric runs; every
    term token must appear as an exact token in the name. So ``twistor`` matches
    ``twistor theory`` and ``twistor_theory`` but not ``ambitwistor``.
    """
    t = term.lower().strip()
    query_tokens = [x for x in re.split(r"[^a-z0-9]+", t) if x]
    if not query_tokens:
        return {}
    results = {}
    for slug, name in slug_to_name.items():
        n = name.lower()
        if token_match:
            name_tokens = set(x for x in re.split(r"[^a-z0-9]+", n) if x)
            if not all(qt in name_tokens for qt in query_tokens):
                continue
        else:
            if t not in n:
                continue
        if n.startswith("/") or n.startswith("http") or n.startswith("./"):
            continue
        if len(name.strip()) <= 2:
            continue
        results[slug] = name
    return results


def find_paths(adj: dict, sources: set, targets: set,
               max_depth: int = 4, max_paths: int = 3) -> list:
    """
    BFS to find shortest paths from any source slug to any target slug.
    Path format: [slug, rel, slug, rel, ..., slug]

    If the same entity name matches both search terms (for example
    'community' and 'ecosystem projects' both appear in
    'community and ecosystem projects'), returns a zero-hop path [slug]
    for each such entity. Multi-hop paths use len(path) > 1.
    """
    if not sources or not targets:
        return []

    overlap = sources & targets
    paths: list = []
    for s in sorted(overlap):
        paths.append([s])
        if len(paths) >= max_paths:
            return paths

    queue = deque()
    node_min_depth: dict = {}
    found_depth = None

    for s in sources:
        if s not in node_min_depth:
            node_min_depth[s] = 0
            queue.append((s, [s]))

    while queue and len(paths) < max_paths:
        current, path = queue.popleft()
        depth = (len(path) - 1) // 2

        if found_depth is not None and depth > found_depth:
            break

        # len(path) > 1: real graph path (zero-hop overlap handled above)
        if current in targets and len(path) > 1:
            paths.append(path)
            found_depth = depth
            continue

        if depth >= max_depth:
            continue

        path_slugs = set(path[i] for i in range(0, len(path), 2))

        for rel, neighbor in adj.get(current, []):
            if neighbor in path_slugs:
                continue
            neighbor_depth = depth + 1
            if neighbor_depth <= node_min_depth.get(neighbor, 9999):
                node_min_depth[neighbor] = neighbor_depth
                queue.append((neighbor, path + [rel, neighbor]))

    return paths


def format_path_inline(path: list, slug_to_name: dict) -> str:
    """Single-line path summary."""
    parts = []
    for i, item in enumerate(path):
        if i % 2 == 0:
            parts.append(f"[{slug_to_name.get(item, item)}]")
        else:
            parts.append(f"--{item}-->")
    return " ".join(parts)


def format_path_block(path: list, slug_to_name: dict) -> str:
    """Multi-line indented path for display."""
    parts = []
    for i, item in enumerate(path):
        if i % 2 == 0:
            parts.append(f"[ {slug_to_name.get(item, item)} ]")
        else:
            parts.append(f"  --{item}-->")
    return "\n        ".join(parts)


def wrap_text(text: str, width: int = 80, indent: int = 4, max_chars: int = 1200) -> str:
    """Wrap and truncate text for report display."""
    text = text.replace('\n', ' ').strip()
    if len(text) > max_chars:
        text = text[:max_chars] + " [... truncated ...]"
    pad = " " * indent
    return textwrap.fill(text, width=width, initial_indent=pad, subsequent_indent=pad)


def build_report(path: list, slug_to_name: dict, conn,
                 term1: str, term2: str, path_num: int) -> str:
    """
    Build a structured LLM analysis prompt for a single path,
    including source text for every entity and edge.
    """
    n_hops = (len(path) - 1) // 2
    entity_slugs = [path[i] for i in range(0, len(path), 2)]
    entity_names = [slug_to_name.get(s, s) for s in entity_slugs]
    edges = [(path[i - 1], path[i - 2], path[i])
             for i in range(2, len(path), 2)]  # (rel, src_slug, tgt_slug)

    lines = []
    div = "=" * 78
    thin = "-" * 78

    lines.append(div)
    lines.append(f"  KNOWLEDGE GRAPH PATH ANALYSIS PROMPT  —  Path {path_num}")
    lines.append(div)
    lines.append("")
    lines.append("  INSTRUCTIONS FOR THE ANALYST")
    lines.append("  " + thin)
    lines.append(textwrap.fill(
        f"The following is a relationship path automatically discovered in a "
        f"knowledge graph built from supply chain, sustainability, and theoretical "
        f"framework documents. Each step in the path is a real extracted triple "
        f"(subject, predicate, object), grounded in the source passages provided "
        f"below. Your task is to: (1) evaluate whether the path represents a "
        f"meaningful structural relationship or an artefact of imprecise entity "
        f"matching; (2) interpret what the chain of relationships reveals about "
        f"how '{term1}' and '{term2}' are connected; (3) identify what this "
        f"connection implies for supply chain analysis, sustainability assessment, "
        f"or theoretical coherence; and (4) note any gaps, anomalies, or "
        f"surprising elements in the chain.",
        width=78, initial_indent="  ", subsequent_indent="  "))
    lines.append("")

    # PATH SUMMARY
    lines.append("  PATH SUMMARY")
    lines.append("  " + thin)
    lines.append(f"  Hops: {n_hops}")
    if n_hops == 0:
        lines.append(
            "  Note: Zero hops. One knowledge-graph entity contains both "
            "search substrings, so no graph edges are required to relate the "
            "two terms."
        )
    lines.append(f"  Chain:")
    lines.append(f"    {format_path_inline(path, slug_to_name)}")
    lines.append("")

    # ENTITY CONTEXTS
    lines.append("  ENTITY CONTEXTS")
    lines.append("  " + thin)
    lines.append("  For each entity in the path, the following is the most")
    lines.append("  content-rich source passage from the knowledge base.")
    lines.append("")

    for slug, name in zip(entity_slugs, entity_names):
        lines.append(f"  [{name.upper()}]")
        text = fetch_entity_text(conn, slug)
        if text:
            lines.append(wrap_text(text))
        else:
            lines.append("    (no source text found for this entity)")
        lines.append("")

    # EDGE CONTEXTS
    lines.append("  RELATIONSHIP CONTEXTS")
    lines.append("  " + thin)
    lines.append("  For each edge in the path, the following passage is the")
    lines.append("  document chunk that contained both entities simultaneously.")
    lines.append("  This is the text the LLM was reading when it extracted the")
    lines.append("  relationship.")
    lines.append("")

    for i in range(0, len(path) - 1, 2):
        src_slug = path[i]
        rel      = path[i + 1]
        tgt_slug = path[i + 2]
        src_name = slug_to_name.get(src_slug, src_slug)
        tgt_name = slug_to_name.get(tgt_slug, tgt_slug)

        lines.append(f"  EDGE: [{src_name}] --{rel}--> [{tgt_name}]")
        text = fetch_edge_text(conn, src_slug, tgt_slug)
        if text:
            lines.append(wrap_text(text))
        else:
            lines.append("    (no co-occurrence passage found for this edge)")
        lines.append("")

    # ANALYSIS QUESTIONS
    lines.append("  ANALYSIS QUESTIONS")
    lines.append("  " + thin)
    lines.append(f"  1. Is the connection from '{term1}' to '{term2}' via this")
    lines.append(f"     path semantically valid? Does each step follow logically?")
    lines.append(f"  2. What does this path reveal about the structural or causal")
    lines.append(f"     relationship between '{term1}' and '{term2}'?")
    lines.append(f"  3. Are any of the intermediate entities acting as bridges")
    lines.append(f"     that would not be obvious without graph traversal?")
    lines.append(f"  4. What are the supply chain, sustainability, or theoretical")
    lines.append(f"     implications of this connection?")
    lines.append(f"  5. Does the source text support or undermine the extracted")
    lines.append(f"     relationship at each step?")
    lines.append("")
    lines.append(div)

    return "\n".join(lines)


def _load_anthropic_key() -> str:
    """Load Anthropic API key from .env-anthropic, then fall back to environment."""
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if key:
        return key
    if ANTHROPIC_ENV.exists():
        for line in ANTHROPIC_ENV.read_text().splitlines():
            line = line.strip()
            if line.startswith("LLM_API_KEY=") and "sk-ant-" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.getenv("LLM_API_KEY", "")


def _estimated_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """Approximate USD from published list prices (per million tokens)."""
    return (
        (input_tokens / 1_000_000.0) * _ANALYSIS_PRICE_IN_PER_MTOK
        + (output_tokens / 1_000_000.0) * _ANALYSIS_PRICE_OUT_PER_MTOK
    )


def _usage_report_markdown(usage, heading: str = "## API usage") -> str:
    """Markdown section for token counts and estimated cost."""
    lines = [heading, ""]
    if usage is None:
        lines.append(
            "*Usage object not present: token counts unavailable.*"
        )
        return "\n".join(lines)
    in_t = int(getattr(usage, "input_tokens", 0) or 0)
    out_t = int(getattr(usage, "output_tokens", 0) or 0)
    total = in_t + out_t
    cost = _estimated_cost_usd(in_t, out_t)
    lines.extend([
        "| Metric | Value |",
        "|:-------|------:|",
        f"| Input tokens | {in_t:,} |",
        f"| Output tokens | {out_t:,} |",
        f"| Total tokens | {total:,} |",
        f"| Estimated cost (USD) | {cost:.6f} |",
        "",
        "**Pricing basis:** Anthropic list rates for Sonnet 4.5 (standard tier): "
        f"input ${_ANALYSIS_PRICE_IN_PER_MTOK:g} / output ${_ANALYSIS_PRICE_OUT_PER_MTOK:g} per 1M tokens. "
        "Override with `KG_ANALYSIS_PRICE_INPUT_PER_MTOK` and "
        "`KG_ANALYSIS_PRICE_OUTPUT_PER_MTOK` if your invoice differs.",
    ])
    return "\n".join(lines)


def _anthropic_message_text(response) -> str:
    """Concatenate text blocks from an Anthropic message response."""
    chunks = []
    for block in getattr(response, "content", None) or ():
        if getattr(block, "type", None) == "text":
            chunks.append(block.text)
    return "\n".join(chunks).strip()


def build_kg_context_block(path: list, slug_to_name: dict, conn) -> str:
    """Entity and edge text excerpts for LLM prompts (analysis and research)."""
    entity_slugs = [path[i] for i in range(0, len(path), 2)]
    entity_names = [slug_to_name.get(s, s) for s in entity_slugs]
    context_parts = []
    context_parts.append(f"PATH: {format_path_inline(path, slug_to_name)}\n")
    context_parts.append("ENTITY CONTEXTS:")
    for slug, name in zip(entity_slugs, entity_names):
        text = fetch_entity_text(conn, slug)
        if text:
            preview = text[:800].replace("\n", " ")
            context_parts.append(f"  [{name}]: {preview}...")
    context_parts.append("\nRELATIONSHIP CONTEXTS:")
    for i in range(0, len(path) - 1, 2):
        src_slug, rel, tgt_slug = path[i], path[i + 1], path[i + 2]
        src_name = slug_to_name.get(src_slug, src_slug)
        tgt_name = slug_to_name.get(tgt_slug, tgt_slug)
        text = fetch_edge_text(conn, src_slug, tgt_slug)
        if text:
            preview = text[:800].replace("\n", " ")
            context_parts.append(
                f"  [{src_name}] --{rel}--> [{tgt_name}]:\n    {preview}..."
            )
    return "\n".join(context_parts)


def research_sources_with_web_search(
    term1: str,
    term2: str,
    path_summary: str,
    analysis_plain: str,
    kg_context: str,
) -> str:
    """
    Second API call with Anthropic web search: further reading and footnotes in Markdown.
    """
    try:
        import anthropic
    except ImportError:
        return (
            "\n---\n\n## Research pass\n\n"
            "`anthropic` package not installed.\n"
        )

    api_key = _load_anthropic_key()
    if not api_key:
        return (
            "\n---\n\n## Research pass\n\n"
            "No Anthropic API key found.\n"
        )

    if not (analysis_plain or "").strip():
        return ""

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = (
        "You are a scholarly research assistant with access to web search. "
        "Prefer peer-reviewed journals, university presses, major technical standards "
        "bodies, and established international organizations (for example IPCC, WHO, UN "
        "agencies, OECD, ISO, national metrology or statistical offices). "
        "Avoid predatory journals, anonymous blogs, and promotional pages. "
        "Only cite URLs that appear in search results from this conversation turn. "
        "If evidence is weak, say so clearly.\n\n"
        "**Hard requirement for this task:** The user is not looking for a general "
        "bibliography of either topic alone. Each recommended source must in some way "
        "**connect, compare, bridge, or jointly frame both** of the user's two concepts "
        "(even if the link is indirect, analogical, or interdisciplinary). "
        "Do **not** fill the list with authoritative works that discuss **only** one "
        "concept with no substantive tie to the other. If the literature is sparse, say "
        "so honestly rather than padding with single-topic surveys."
    )
    user_prompt = (
        f"The user compared these concepts in a knowledge graph: **'{term1}'** and **'{term2}'**.\n"
        f"**Path:** {path_summary}\n\n"
        "**Knowledge graph evidence excerpt:**\n"
        f"{kg_context[:7000]}\n\n"
        "**Analysis text (claims often concern how these two ideas relate):**\n"
        f"{analysis_plain[:8000]}\n\n"
        "**Your job**\n"
        "1. Use web search with queries that **pair** the two concepts (for example both "
        "terms in the same query, or phrases like *bridge*, *application of*, *in the context of*, "
        "*relation between*, *interdisciplinary*, *formal analogy*). Try several paired queries.\n"
        "2. In **Further reading**, include **only** sources where the work itself (not just your "
        "inference) engages **both** named ideas, or a clear intermediary that links them in one "
        "argument or framework. For each item, the relevance sentence must state **how** it touches "
        "**both** sides, not why it is a classic on one side only.\n"
        "3. If you find **no** suitable joint-source hits after real search attempts, write a short "
        "**Note on coverage** explaining that, and give 2 to 4 suggested **paired search queries** "
        "the user could run next. Do **not** substitute a list of famous single-topic references.\n"
        "4. **Suggested footnotes** should tie specific **cross-concept** claims from the analysis "
        "to sources that support that **joint** claim (same formatting as before).\n\n"
        "Respond in **Markdown** using exactly this outline:\n\n"
        "### Further reading\n"
        "Numbered list (or empty with explanation if joint sources are missing). Each item: "
        "author or organization if known, title, venue or publisher, year if known, stable HTTPS "
        "link, and **one sentence stating how this source jointly involves both concepts**.\n\n"
        "### Suggested footnotes\n"
        "Between 3 and 8 lines if you have joint sources; fewer if not. Format each as: "
        "[^n]: Short paraphrase of a **connection** claim from the analysis; source Author (Year) "
        "`Title`, URL\n"
        "Use consecutive n starting at 1. If a claim rests only on the graph excerpt with no "
        "joint external source, say so in the footnote.\n\n"
        "If searches return only single-topic material, comply with step 3 and do not pretend "
        "those items are joint sources."
    )

    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 8}]
    try:
        response = client.messages.create(
            model=RESEARCH_MODEL,
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except Exception as exc:
        return (
            "\n---\n\n## Research pass (web search)\n\n"
            f"**Could not run web research:** `{exc}`\n\n"
            "Try setting `KG_RESEARCH_MODEL` to a web-search-capable model on your Anthropic "
            "account (for example `claude-sonnet-4-6`). See Anthropic API docs: web search tool.\n"
        )

    body = _anthropic_message_text(response)
    if not body:
        body = "*No text content returned from the research pass.*"

    parts = [
        "",
        "---",
        "",
        "## Research pass (web search)",
        "",
        "_Links and citations below were produced using Claude with web search. "
        "Verify each source independently before academic, policy, or legal use._",
        "",
        f"**Research model:** `{RESEARCH_MODEL}`",
        "",
        body,
        "",
        "---",
        "",
        _usage_report_markdown(
            getattr(response, "usage", None),
            heading="## API usage (research pass)",
        ),
        "",
    ]
    return "\n".join(parts)


def analyze_with_claude(path: list, slug_to_name: dict, conn,
                        term1: str, term2: str, path_num: int) -> tuple:
    """
    Send the path and its source texts to Claude. Returns (markdown, model_plain_text).
    model_plain_text is empty on error.
    """
    try:
        import anthropic
    except ImportError:
        return (
            "## Error\n\n"
            "`anthropic` package not installed. Run: `pip install anthropic`\n",
            "",
        )

    api_key = _load_anthropic_key()
    if not api_key:
        return (
            "## Error\n\n"
            "No Anthropic API key found. Set `ANTHROPIC_API_KEY` or populate "
            "`.env-anthropic`.\n",
            "",
        )

    n_hops = (len(path) - 1) // 2
    context_block = build_kg_context_block(path, slug_to_name, conn)

    system_prompt = (
        "You are an expert analyst in the True Value Framework (TVF) and the Tholonic "
        "N-D-C model. The Tholonic model describes all systems using a triadic structure: "
        "Negotiation (N, the emergent stable state), Definition (D, constraints and "
        "boundaries), and Contribution (C, outputs and connections). The True Value "
        "Framework applies this model to supply chains, sustainability, and value systems "
        "to measure coherence, identify phase stress, and reveal structural dependencies "
        "that conventional financial analysis cannot see. "
        "Your role is to analyze knowledge graph paths and produce concise, grounded "
        "deductions. Be direct. Cite the source text when it supports your conclusion. "
        "Do not speculate beyond what the evidence warrants."
    )

    user_prompt = (
        f"Analyze the following knowledge graph path connecting '{term1}' to '{term2}' "
        f"({n_hops} hop{'s' if n_hops != 1 else ''}).\n\n"
        f"{context_block}\n\n"
        "In the context of the True Value Framework and the Tholonic N-D-C model, "
        "provide:\n"
        "1. A DEDUCTION: What does this path reveal about the structural or causal "
        "relationship between these two concepts?\n"
        "2. A TVF IMPLICATION: What does this connection mean for supply chain analysis, "
        "sustainability assessment, or value measurement?\n"
        "3. AN NDC READING: Which pole of the N-D-C triad does each entity occupy, "
        "and what does the path direction tell us about information or energy flow?\n"
        "4. A CONFIDENCE ASSESSMENT: Is this path well-supported by the source text, "
        "or is it a plausible but unverified inference?\n\n"
        "Be concise. Each section should be 2-4 sentences. "
        "Format your answer in Markdown: use `###` headings for each part "
        "(Deduction, TVF implication, NDC reading, Confidence).\n\n"
    )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=ANALYSIS_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": user_prompt}],
        system=system_prompt,
    )

    result_text = response.content[0].text
    path_summary = format_path_inline(path, slug_to_name)

    parts = [
        "## Claude analysis",
        "",
        f"**Path {path_num}:** `{path_summary}`",
        "",
        f"**Model:** `{ANALYSIS_MODEL}`",
        "",
        "### Model response",
        "",
        result_text.strip(),
        "",
        "---",
        "",
        _usage_report_markdown(getattr(response, "usage", None)),
        "",
    ]
    return "\n".join(parts), result_text.strip()


# When a single extracted "entity" name embeds a verb used as a predicate elsewhere,
# keep that token lowercase in entity filename segments (see _safe_entity).
# Do not list very short or ambiguous tokens (e.g. "on", "to", "in").
_ENTITY_FILENAME_EDGE_TOKENS = frozenset({
    "requires", "required", "requiring",
    "enables", "enabled", "enabling",
    "depends", "depending",
    "determines", "determined", "determining",
    "affects", "affected", "affecting",
    "causes", "caused", "causing",
    "drives", "drove", "driving",
    "facilitates", "facilitated", "facilitating",
    "contributes", "contributed", "contributing",
    "establishes", "established", "establishing",
    "enhances", "enhanced", "enhancing",
    "generates", "generated", "generating",
    "analyzes", "analyzed", "analyzing",
    "evaluates", "evaluated", "evaluating",
    "applies", "applied", "applying",
    "supports", "supported", "supporting",
    "defines", "defined", "defining",
    "develops", "developed", "developing",
    "creates", "created", "creating",
    "produces", "produced", "producing",
    "provides", "provided", "providing",
    "includes", "included", "including",
    "relates", "related", "relating",
    "connects", "connected", "connecting",
    "feeds", "fed", "feeding",
    "flows", "flowed", "flowing",
    "arises", "arose", "arising",
    "emerges", "emerged", "emerging",
    "implements", "implemented", "implementing",
    "integrates", "integrated", "integrating",
})


def _safe_entity(s: str) -> str:
    """
    Sanitize for a filename segment. Mostly UPPERCASE for entities.

    Underscore-separated tokens that match common graph predicate stems are
    lowercased so a compound label like 'AUBEB PDI requires ecosystem mapping'
    becomes AUBEB_PDI_requires_... instead of ..._REQUIRES_... when those words
    are edge verbs, not part of an acronym block. (Odd path steps still use
    _safe_predicate exclusively.)
    """
    import re
    s = s.strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "_", s)
    s = s.strip("_").upper()
    if not s:
        return ""
    parts = [p for p in s.split("_") if p]
    out = []
    for p in parts:
        low = p.lower()
        if low in _ENTITY_FILENAME_EDGE_TOKENS:
            out.append(low)
        else:
            out.append(p)
    return "_".join(out)


def _safe_predicate(s: str) -> str:
    """Sanitize for a filename segment. Predicates are lowercase."""
    import re
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "_", s)
    return s.strip("_")


def _build_filepath(term1: str, path: list, term2: str,
                    slug_to_name: dict, path_index: int = 1) -> Path:
    """
    Build the output path:
        qanalysis/{SEARCH_TERM1}--{SEARCH_TERM2}/
            {ENTITY}--{predicate}--{ENTITY}--{predicate}--{ENTITY}.md

    The folder is named after the two search terms (entity style, all caps).
    The file alternates entity segments (ALL CAPS) and predicate segments
    (lowercase). Double dashes separate components; underscores stay within
    each name.

    The full alternating chain is always used as the basename when its UTF-8
    length is within the per-component byte limit (see KG_PATH_MAX_FILENAME_BYTES,
    default 250). Longer chains would exceed typical OS limits (255 bytes), so
    the file is named path_NNN__<hash>.md instead; the saved report header still
    contains the complete chain.

    Note: file managers often show an ellipsis in the middle of a long name for
    display only; that is not part of the real filename on disk.
    """
    folder = QANALYSIS_DIR / (
        f"{_safe_entity(term1)}--{_safe_entity(term2)}"
    )
    folder.mkdir(parents=True, exist_ok=True)

    # Build alternating chain: entity--predicate--entity--predicate--entity
    parts = []
    for i, item in enumerate(path):
        if i % 2 == 0:
            name = slug_to_name.get(item, item)
            parts.append(_safe_entity(name))
        else:
            parts.append(_safe_predicate(item))

    stem = "--".join(parts)
    filename = stem + ".md"
    encoded = filename.encode("utf-8")

    if len(encoded) <= _MAX_FN_BYTES:
        return folder / filename

    digest = hashlib.sha256(encoded).hexdigest()[:16]
    short = f"path_{path_index:03d}__{digest}.md"
    return folder / short


def _analysis_file_header_markdown(
    timestamp: str,
    term1: str,
    term2: str,
    ds_names: list,
    path: list,
    slug_to_name: dict,
    outfile: Path,
) -> str:
    """YAML-free Markdown front matter for saved --analysis reports."""
    path_inline = format_path_inline(path, slug_to_name)
    ds_list = ", ".join(d.split("_", 1)[-1] for d in ds_names)
    lines = [
        "# Knowledge graph path analysis",
        "",
        f"- **Generated:** {timestamp}",
        f"- **Query A:** {term1}",
        f"- **Query B:** {term2}",
        f"- **Datasets:** {ds_list}",
        f"- **Path:** `{path_inline}`",
    ]
    if outfile.name.startswith("path_") and outfile.suffix == ".md":
        full_stem = "--".join(
            _safe_entity(slug_to_name.get(path[j], path[j]))
            if j % 2 == 0
            else _safe_predicate(path[j])
            for j in range(len(path))
        )
        lines.append(
            "- **Full chain filename stem** (on-disk basename length limit): "
            f"`{full_stem}.md`"
        )
    lines.extend(["", "---", ""])
    return "\n".join(lines)


def _tee(text: str, fh) -> None:
    """Print text to stdout and write to file handle simultaneously."""
    print(text)
    fh.write(text + "\n")


def parse_args():
    args = sys.argv[1:]
    entities = []
    dataset = None
    max_depth = 4
    max_paths = 3
    report = False
    analysis = False
    research = False
    token_match = False
    i = 0
    while i < len(args):
        if args[i] in ("--dataset", "-d") and i + 1 < len(args):
            dataset = args[i + 1]; i += 2
        elif args[i] in ("--depth", "-n") and i + 1 < len(args):
            max_depth = int(args[i + 1]); i += 2
        elif args[i] in ("--paths", "-p") and i + 1 < len(args):
            max_paths = int(args[i + 1]); i += 2
        elif args[i] == "--token":
            token_match = True; i += 1
        elif args[i] == "--report":
            report = True; i += 1
        elif args[i] == "--research":
            research = True
            analysis = True
            i += 1
        elif args[i] == "--analysis":
            analysis = True; i += 1
        elif not args[i].startswith("-"):
            entities.append(args[i]); i += 1
        else:
            i += 1
    return (
        entities,
        dataset,
        max_depth,
        max_paths,
        report,
        analysis,
        research,
        token_match,
    )


def main():
    (
        entities,
        dataset,
        max_depth,
        max_paths,
        report,
        analysis,
        research,
        token_match,
    ) = parse_args()

    if len(entities) < 2:
        print(__doc__)
        sys.exit(1)

    term1, term2 = entities[0], entities[1]

    if dataset:
        ds_names = [DATASET_ALIASES.get(dataset, dataset)]
    else:
        ds_names = list(dict.fromkeys(DATASET_ALIASES.values()))

    print(f"\n  Entity A:  '{term1}'")
    print(f"  Entity B:  '{term2}'")
    print(f"  Max hops:  {max_depth}")
    print(f"  Datasets:  {', '.join(d.split('_',1)[-1] for d in ds_names)}")
    if report:
        print(f"  Mode:      full report with source text")
    if analysis:
        print(f"  Mode:      Claude analysis ({ANALYSIS_MODEL})")
    if research:
        print(
            f"  Mode:      web research pass ({RESEARCH_MODEL}, further reading + footnotes)"
        )
    if token_match:
        print(f"  Matching:  whole-token (not embedded substring)")
    print("\n  Loading graph... ", end="", flush=True)

    conn = pg_connect()
    slug_to_name, adj = load_graph(conn, ds_names)

    total_entities = len(slug_to_name)
    total_edges = sum(len(v) for v in adj.values())
    print(f"done  ({total_entities:,} entities, {total_edges:,} edges)\n")

    matches_a = match_entities(slug_to_name, term1, token_match)
    matches_b = match_entities(slug_to_name, term2, token_match)

    if not matches_a:
        print(f"  No entities found matching '{term1}'. Try a broader term.\n")
        conn.close(); return
    if not matches_b:
        print(f"  No entities found matching '{term2}'. Try a broader term.\n")
        conn.close(); return

    def show_matches(label, matches):
        names = sorted(set(matches.values()))
        print(f"  Matched '{label}' to {len(names)} entity/entities:")
        for n in names[:8]:
            print(f"    - {n}")
        if len(names) > 8:
            print(f"    ... and {len(names) - 8} more")
        print()

    show_matches(term1, matches_a)
    show_matches(term2, matches_b)

    sources = set(matches_a.keys())
    targets = set(matches_b.keys())

    print(f"  Searching for paths (max {max_depth} hops, up to {max_paths} paths)...\n")
    paths = find_paths(adj, sources, targets, max_depth, max_paths)

    if not paths:
        print(f"  No path found within {max_depth} hops.")
        print(f"  Try --depth {max_depth + 2} or broader entity terms.\n")
        conn.close(); return

    hops = (len(paths[0]) - 1) // 2
    if hops == 0:
        print(
            "  Found {n} path(s): zero-hop match (one entity name matches "
            "both terms).\n".format(n=len(paths))
        )
    else:
        print(
            f"  Found {len(paths)} path(s), shortest is {hops} hop(s):\n"
        )
    print("  " + "=" * 70)

    for i, path in enumerate(paths, 1):
        n_hops = (len(path) - 1) // 2
        print(f"\n  Path {i}  ({n_hops} hop{'s' if n_hops != 1 else ''}):\n")
        print(f"        {format_path_block(path, slug_to_name)}")
        print()

    print("  " + "=" * 70 + "\n")

    if report:
        print("\n\n")
        print("  " + "=" * 70)
        print("  FULL ANALYSIS REPORTS WITH SOURCE TEXT")
        print("  " + "=" * 70)
        print()
        for i, path in enumerate(paths, 1):
            print(build_report(path, slug_to_name, conn, term1, term2, i))
            print()

    if analysis:
        import datetime
        print("\n\n")
        print("  " + "=" * 70)
        print(f"  CLAUDE ANALYSIS  ({ANALYSIS_MODEL})")
        print("  " + "=" * 70)
        print()
        for i, path in enumerate(paths, 1):
            outfile = _build_filepath(
                term1, path, term2, slug_to_name, path_index=i
            )
            print(f"  Querying Claude for path {i}... ", end="", flush=True)
            result, analysis_plain = analyze_with_claude(
                path, slug_to_name, conn, term1, term2, i
            )
            print("done\n")

            research_md = ""
            if research and analysis_plain:
                print("  Web research (authoritative sources)... ", end="", flush=True)
                kg_ctx = build_kg_context_block(path, slug_to_name, conn)
                research_md = research_sources_with_web_search(
                    term1,
                    term2,
                    format_path_inline(path, slug_to_name),
                    analysis_plain,
                    kg_ctx,
                )
                print("done\n")

            body = result + research_md

            header = _analysis_file_header_markdown(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                term1,
                term2,
                ds_names,
                path,
                slug_to_name,
                outfile,
            )

            with open(outfile, "w") as fh:
                fh.write(header)
                fh.write(body)

            # Print same Markdown to console (preview)
            print(header)
            print(body)
            print()
            print(f"  Saved: {outfile}\n")
            if outfile.name.startswith("path_"):
                print(
                    "  (Short on-disk name: path exceeded KG_PATH_MAX_FILENAME_BYTES; "
                    "full chain is in the file header.)\n"
                )

    conn.close()


if __name__ == "__main__":
    main()
