#!/usr/bin/env python3
"""
Build docnav_manifest.tsv from entries_for_ai.txt (ENTRY_START blocks).

Implements the rules in docnav/AI_PROMPT_DOCNAV_MANIFEST.md using deterministic
keyword scoring on path plus excerpt. Run after regenerating entries_for_ai.txt.

Usage (from repository root):

  python3 docnav/docnav_manifest_from_entries.py
  python3 docnav/docnav_manifest_from_entries.py --entries docnav/entries_for_ai.txt \\
      --out docnav/docnav_manifest.tsv
"""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter

HEADER = "relative_path\ttitle\ttags\tsummary\tnotes"

DOCNAV = os.path.dirname(os.path.abspath(__file__))

TOPIC_LEXICON: list[tuple[str, tuple[str, ...]]] = [
    ("topic/tvpci", ("tvpci", "true value pricing", "convergence index", "radar chart")),
    ("topic/tholonic-ndc", ("tholonic", "n-d-c", "definition", "contribution", "negotiation", "d vs c", "d/c")),
    ("topic/pdi", ("pdi", "phase discovery", "ndc metrics", "value chain phase")),
    ("topic/supply-chain", ("supply chain", "comex", "vaulting", "bullion", "refining", "custody", "phase 0", "phase 1")),
    ("topic/value-chain", ("value chain", "margin", "profit capture")),
    ("topic/blue-carbon", ("blue carbon", "mangrove", "coastal", "ctvf")),
    ("topic/water", ("water", "replenish", "utility", "ocwd", "recycled water")),
    ("topic/game-theory", ("game theory", "gametheory", "slider", "prisoner")),
    ("topic/finance-esg", ("esg", "bond", "rating", "sovereign", "investor report", "sustainability-linked")),
    ("topic/ai-notes", ("concept_notes", "document_notes", "/ai_notes/")),
    ("topic/research-general", ("research/", "methodology", "hypothesis", "literature")),
]

FMT_BY_EXT: dict[str, str] = {
    ".md": "fmt/md",
    ".txt": "fmt/md",
    ".html": "fmt/html",
    ".htm": "fmt/html",
    ".pdf": "fmt/pdf",
    ".png": "fmt/png",
    ".jpg": "fmt/jpeg",
    ".jpeg": "fmt/jpeg",
    ".jpe": "fmt/jpeg",
    ".webp": "fmt/jpeg",
    ".gif": "fmt/png",
    ".svg": "fmt/svg",
    ".css": "fmt/css",
    ".js": "fmt/js",
    ".yaml": "fmt/yaml",
    ".yml": "fmt/yaml",
    ".json": "fmt/json",
    ".csv": "fmt/csv",
    ".tsv": "fmt/csv",
    ".tex": "fmt/md",
    ".ttl": "fmt/md",
    ".psd": "fmt/binary-other",
    ".xlsx": "fmt/xlsx",
    ".docx": "fmt/binary-other",
    ".blend": "fmt/binary-other",
    ".blend1": "fmt/binary-other",
}


def norm(s: str) -> str:
    return s.lower()


def score_topics(path: str, excerpt: str) -> dict[str, int]:
    blob = norm(path + " " + excerpt)
    scores: dict[str, int] = {}
    for tag, kws in TOPIC_LEXICON:
        scores[tag] = sum(blob.count(kw) for kw in kws)
    return scores


def pick_topic(scores: dict[str, int]) -> str:
    best = max(scores.values()) if scores else 0
    if best <= 0:
        return "topic/generic-doc"
    top_tags = [t for t, v in scores.items() if v == best]
    priority = [t for t, _ in TOPIC_LEXICON] + ["topic/generic-doc"]
    for p in priority:
        if p in top_tags:
            return p
    return top_tags[0]


def fmt_from_ext(ext: str) -> str:
    ext = ext.strip().lower()
    if not ext.startswith("."):
        ext = "." + ext if ext else ""
    return FMT_BY_EXT.get(ext, "fmt/binary-other")


def phase_tags(path: str, excerpt: str) -> list[str]:
    blob = norm(path + " " + excerpt)
    tags: list[str] = []
    for i in range(8):
        if re.search(rf"\bphase\s*{i}\b", blob) or re.search(rf"\bphase\s*-?\s*{i}\b", blob):
            tags.append(f"phase/{i}")
    if "vaulting" in blob or "phase 6" in blob:
        if "phase/6" not in tags:
            tags.append("phase/6")
    if "exchange" in blob and "comex" in blob:
        if "phase/7" not in tags:
            tags.append("phase/7")
    return sorted(set(tags))


def kind_tags(rel: str, excerpt: str, fmt_tag: str) -> list[str]:
    rel_n = norm(rel)
    kinds: list[str] = []
    if rel_n.startswith("sites/") and "_files/" in rel_n:
        kinds.append("kind/saved-site")
    elif rel_n.startswith("sites/") and rel_n.endswith(".html"):
        kinds.append("kind/saved-site")
    if "template" in rel_n or "pdi_template" in rel_n.replace("-", "_"):
        kinds.append("kind/template")
    if fmt_tag in ("fmt/png", "fmt/jpeg") and "kind/saved-site" not in kinds:
        kinds.append("kind/archive-image")
    if fmt_tag == "fmt/js" and "/_files/" in rel_n:
        kinds.append("kind/source-code-bundle")
    if fmt_tag == "fmt/css" and "/_files/" in rel_n:
        kinds.append("kind/source-code-bundle")
    return sorted(set(kinds))


def one_sentence_summary(excerpt: str) -> str:
    excerpt = re.sub(r"\s+", " ", excerpt.strip())
    if excerpt.startswith("opaque"):
        return "Opaque or unreadable; manual review."
    if not excerpt:
        return "Opaque or unreadable; manual review."
    cut = excerpt[:240]
    m = re.search(r"^.{10,240}?[.!?](?= |$)", excerpt)
    if m:
        return m.group(0).strip()[:240]
    if len(excerpt) <= 240:
        return excerpt
    sp = cut.rfind(" ")
    if sp > 80:
        cut = cut[:sp]
    return cut.strip() + "…"


def cell_escape(s: str) -> str:
    # Quotes break naive TSV readers that interpret RFC 4180 CSV quoting.
    return (
        s.replace("\t", " ")
        .replace("\r", " ")
        .replace("\n", " ")
        .replace('"', "'")
        .strip()
    )


def parse_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    blocks = text.split("ENTRY_START")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if "ENTRY_END" not in block:
            continue
        body, _, _ = block.partition("ENTRY_END")
        rel_m = re.search(r"^relative_path:\s*(.+)$", body, re.MULTILINE)
        ext_m = re.search(r"^extension:\s*(.+)$", body, re.MULTILINE)
        if not rel_m:
            continue
        rel = rel_m.group(1).strip()
        ext = ext_m.group(1).strip() if ext_m else ""
        if "(none)" in ext:
            ext = ""
        ex_idx = body.find("excerpt:")
        excerpt = ""
        if ex_idx >= 0:
            excerpt = body[ex_idx + len("excerpt:") :].strip()
        entries.append({"relative_path": rel, "extension": ext, "excerpt": excerpt})
    return entries


def build_title(rel: str, basename_counts: Counter[str]) -> str:
    base = os.path.basename(rel)
    title = f"docnav: {base}"
    if basename_counts[base] > 1:
        parent = os.path.dirname(rel).replace("\\", "/")
        frag = parent.split("/")[-2:] if parent else []
        suffix = "/".join(frag)
        title = f"docnav: {suffix}/{base}" if suffix else title
    title = title[:80]
    return title


def topic_tags_for_row(rel: str, picked_topic: str) -> list[str]:
    """
    Primary topic comes from keyword scoring. Paths under Repos/intra/PDI/ also get
    topic/pdi so PDI-folder HTML/Markdown appears when filtering facet topic/pdi even when
    the excerpt scores higher on topic/supply-chain (common for SCPI titles).
    """
    rel_n = norm(rel.replace("\\", "/"))
    out: list[str] = []
    if rel_n.startswith("repos/intra/pdi/"):
        out.append("topic/pdi")
    if picked_topic not in out:
        out.append(picked_topic)
    return out


def row_tags(
    topics: list[str], fmt_tag: str, phases: list[str], kinds: list[str], excerpt: str
) -> str:
    parts = list(topics) + [fmt_tag]
    parts.extend(phases)
    parts.extend(kinds)
    if excerpt.lower().startswith("opaque") or excerpt.strip() == "":
        parts.append("meta/low-confidence")
    seen: set[str] = set()
    ordered: list[str] = []
    for p in parts:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    return " ".join(ordered)


def notes_for(rel: str, excerpt: str) -> str:
    n: list[str] = []
    rel_n = norm(rel)
    if excerpt.lower().startswith("opaque") or not excerpt.strip():
        n.append("needs_manual_review")
    if rel_n.startswith("sites/") and "_files/" in rel_n:
        n.append("saved_site_bundle")
    return " ".join(n)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entries", default=os.path.join(DOCNAV, "entries_for_ai.txt"))
    ap.add_argument("--out", default=os.path.join(DOCNAV, "docnav_manifest.tsv"))
    args = ap.parse_args()

    with open(args.entries, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    entries = parse_entries(raw)
    entries.sort(key=lambda e: e["relative_path"].casefold())

    basenames = Counter(os.path.basename(e["relative_path"]) for e in entries)

    lines = [HEADER]
    for e in entries:
        rel = e["relative_path"]
        excerpt = e["excerpt"]
        ext = e["extension"]
        fmt_tag = fmt_from_ext(ext)

        base_l = os.path.basename(rel).casefold()
        if base_l in (
            "ai_prompt_docnav_manifest.md",
            "entries_for_ai.txt",
            "docnav_manifest.tsv",
            "index.html",
        ):
            topic = "topic/generic-doc"
        else:
            scores = score_topics(rel, excerpt)
            topic = pick_topic(scores)
        phases = phase_tags(rel, excerpt)
        kinds = kind_tags(rel, excerpt, fmt_tag)

        summary = one_sentence_summary(excerpt)
        title = build_title(rel, basenames)
        tags = row_tags(topic_tags_for_row(rel, topic), fmt_tag, phases, kinds, excerpt)
        note = notes_for(rel, excerpt)

        lines.append(
            "\t".join(
                [
                    cell_escape(rel),
                    cell_escape(title),
                    cell_escape(tags),
                    cell_escape(summary),
                    cell_escape(note),
                ]
            )
        )

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote {len(lines) - 1} rows to {args.out}")


if __name__ == "__main__":
    main()
