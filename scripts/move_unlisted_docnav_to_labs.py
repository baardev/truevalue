#!/usr/bin/env python3
"""Move docnav files not referenced in frontend/site-index.json to docnav/labs/."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCNAV = REPO / "docnav"
LABS = DOCNAV / "labs"
SITE_INDEX = REPO / "frontend" / "site-index.json"

# DocNav application files (not in site-index but required at original paths).
KEEP_ROOT_FILES = {
    "view.html",
    "index.html",
    "csvindex.html",
    "pandoc-docnav-theme.css",
    "catalog.json",
    "csv_catalog.json",
    "docnav_manifest.tsv",
    "entries_for_ai.txt",
    "docnav_extract_excerpts.py",
    "AI_PROMPT_DOCNAV_MANIFEST.md",
    "Progs.md",
}

KEEP_TOP_DIRS = {
    "api",
    "sites",
    "labs",
}


def collect_listed_paths(site_index_path: Path) -> set[str]:
    with site_index_path.open(encoding="utf-8") as f:
        data = json.load(f)

    listed: set[str] = set()

    def walk(obj: object) -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "url" and isinstance(value, str):
                    if "file=" in value:
                        match = re.search(r"file=([^&]+)", value)
                        if match:
                            listed.add(match.group(1))
                    elif value.startswith("/docnav/") and "view.html" not in value:
                        listed.add(value.removeprefix("/docnav/"))
                else:
                    walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return listed


def should_keep(rel_posix: str, listed: set[str]) -> bool:
    if rel_posix in listed:
        return True
    parts = rel_posix.split("/")
    if parts[0] in KEEP_TOP_DIRS:
        return True
    if len(parts) == 1 and parts[0] in KEEP_ROOT_FILES:
        return True
    return False


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    listed = collect_listed_paths(SITE_INDEX)
    print(f"Listed paths in site-index: {len(listed)}")

    to_move: list[tuple[Path, Path]] = []
    for path in sorted(DOCNAV.rglob("*")):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(DOCNAV)
        except ValueError:
            continue
        rel_posix = rel.as_posix()
        if rel_posix.startswith("labs/"):
            continue
        if should_keep(rel_posix, listed):
            continue
        dest = LABS / rel
        to_move.append((path, dest))

    print(f"Files to move: {len(to_move)}")
    if dry_run:
        for src, dest in to_move[:30]:
            print(f"  {src.relative_to(REPO)} -> {dest.relative_to(REPO)}")
        if len(to_move) > 30:
            print(f"  ... and {len(to_move) - 30} more")
        return 0

    moved = 0
    for src, dest in to_move:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            print(f"SKIP (exists): {dest.relative_to(REPO)}", file=sys.stderr)
            continue
        shutil.move(str(src), str(dest))
        moved += 1

    print(f"Moved {moved} files into docnav/labs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
