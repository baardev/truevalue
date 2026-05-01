#!/usr/bin/env python3
"""
Convert docnav_manifest.tsv to TiddlyWiki 5 JSON import (array of tiddlers).

Rules aligned with docnav/AI_PROMPT_DOCNAV_MANIFEST.md optional step 2.

Usage:
  python3 scripts/docnav_manifest_to_tiddlywiki_json.py
  DOCNAV_PUBLIC_BASE_URL=https://example.com/docnav/ python3 scripts/docnav_manifest_to_tiddlywiki_json.py
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from urllib.parse import quote

DOCNAV = os.path.join(os.path.dirname(__file__), "..", "docnav")


def path_for_url(rel: str) -> str:
    return quote(rel, safe="/")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=os.path.join(DOCNAV, "docnav_manifest.tsv"))
    ap.add_argument("--out", default=os.path.join(DOCNAV, "docnav_tiddlers_import.json"))
    ap.add_argument(
        "--base-url",
        default=os.environ.get(
            "DOCNAV_PUBLIC_BASE_URL", "https://tvf.tholonia.com/docnav/"
        ),
    )
    args = ap.parse_args()

    base = args.base_url.rstrip("/") + "/"

    tiddlers: list[dict[str, str]] = []
    with open(args.manifest, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rel = row["relative_path"].strip()
            title = row["title"].strip()
            tags = row["tags"].strip()
            summary = row["summary"].strip()
            url = base + path_for_url(rel)
            label = os.path.basename(rel) or rel
            text = (
                f"[[Open file|{url}]]\n\n"
                f"Summary: {summary}\n\n"
                f"Path: `{rel}`"
            )
            tiddlers.append({"title": title, "tags": tags, "text": text})

    out_path = args.out
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tiddlers, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(tiddlers)} tiddlers to {out_path}")


if __name__ == "__main__":
    main()
