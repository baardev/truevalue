#!/usr/bin/env python3
"""
Build catalog.json from docnav_manifest.tsv.

Skips .html / .htm rows when a sibling .md exists (same stem), so the catalog
prefers view.html?file=... on Markdown and avoids dead Pandoc HTML links after
those exports are removed.

Paths listed in catalog_exclude.txt (under this directory) are omitted from
catalog.json entirely. Edit that file to hide tooling, hub pages, or any doc.

Typical pipeline (from repository root):

  python3 docnav/docnav_extract_excerpts.py > docnav/entries_for_ai.txt
  python3 docnav/docnav_manifest_from_entries.py
  python3 docnav/docnav_build_catalog_json.py
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import os

KEEP = {".csv", ".html", ".htm", ".md", ".pdf", ".txt"}
DEFAULT_BASE = "https://tvf.tholonia.com/docnav/"
EXCLUDE_LIST_NAME = "catalog_exclude.txt"

# Used only when catalog_exclude.txt is missing (first clone or deleted file).
_FALLBACK_EXCLUDES = frozenset(
    {
        "index.html",
        "catalog.html",
        "view.html",
        "catalog.json",
        "entries_for_ai.txt",
        "docnav_manifest.tsv",
        EXCLUDE_LIST_NAME,
        "REFRESH",
        "docnav_extract_excerpts.py",
        "docnav_manifest_from_entries.py",
        "docnav_build_catalog_json.py",
    }
)


def _norm_rel(rel: str) -> str:
    return rel.replace("\\", "/").strip().lstrip("./")


def load_catalog_exclude_patterns(docnav_dir: str) -> tuple[frozenset[str], tuple[str, ...]]:
    """
    Returns (exact_paths, glob_patterns). Glob patterns use fnmatch against full rel path.
    """
    path = os.path.join(docnav_dir, EXCLUDE_LIST_NAME)
    exact: set[str] = set()
    globs: list[str] = []
    if not os.path.isfile(path):
        return frozenset(_FALLBACK_EXCLUDES), ()
    with open(path, encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            line = _norm_rel(line)
            if "*" in line or "?" in line or "[" in line:
                globs.append(line)
            else:
                exact.add(line)
    return frozenset(exact), tuple(globs)


def catalog_row_excluded(rel_nf: str, exact: frozenset[str], globs: tuple[str, ...]) -> bool:
    if rel_nf in exact:
        return True
    for pat in globs:
        if fnmatch.fnmatch(rel_nf, pat):
            return True
    return False


def main() -> None:
    _docnav = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Build docnav/catalog.json from manifest TSV.")
    ap.add_argument(
        "--manifest",
        default=os.path.join(_docnav, "docnav_manifest.tsv"),
        help="Input manifest from docnav_manifest_from_entries.py",
    )
    ap.add_argument(
        "--out",
        default=os.path.join(_docnav, "catalog.json"),
        help="Output JSON path",
    )
    ap.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help="Absolute base URL for doc.url fields (trailing slash optional)",
    )
    args = ap.parse_args()

    docnav_root = os.path.dirname(os.path.abspath(args.out))
    exclude_exact, exclude_globs = load_catalog_exclude_patterns(docnav_root)

    rows: list[dict[str, str]] = []
    with open(args.manifest, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rel = r.get("relative_path", "").strip()
            ext = os.path.splitext(rel)[1].lower()
            if ext not in KEEP:
                continue
            rel_nf = _norm_rel(rel)
            if catalog_row_excluded(rel_nf, exclude_exact, exclude_globs):
                continue
            rows.append(r)

    path_set = {r["relative_path"].strip() for r in rows}

    base = args.base.rstrip("/") + "/"
    out: list[dict[str, object]] = []
    for r in rows:
        rel = r["relative_path"].strip()
        ext = os.path.splitext(rel)[1].lower()
        if ext in (".html", ".htm"):
            stem = os.path.splitext(rel)[0]
            md_rel = stem + ".md"
            md_path = os.path.join(docnav_root, md_rel)
            if md_rel in path_set or os.path.isfile(md_path):
                continue
        title = r["title"].strip()
        tags = [t.strip() for t in r["tags"].split() if t.strip()]
        summary = r["summary"].strip()
        url_rel = rel.replace("\\", "/")
        out.append(
            {
                "title": title,
                "path": rel,
                "tags": tags,
                "summary": summary,
                "url": base + url_rel,
            }
        )

    out.sort(key=lambda x: str(x["title"]).casefold())
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(out)} entries to {args.out}")


if __name__ == "__main__":
    main()
