#!/usr/bin/env python3
"""
Generate a categorized file manifest for the tv project.

Output: .cursor/file_manifest.json

Run this script whenever significant files are added, moved, or removed.
The manifest is consumed by the filemanager subagent so parent agents can
resolve file paths without running live directory searches.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / ".cursor" / "file_manifest.json"

# Directories to exclude entirely from the manifest
EXCLUDE_DIRS = {
    ".git",
    "viewable",
    ".viewable",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
}

# File extensions considered binary or generated noise
EXCLUDE_EXTENSIONS = {".pyc", ".pyo", ".DS_Store", ".egg-info"}

# Extension-to-category mapping (first match wins)
CATEGORY_RULES = [
    # Cursor configuration
    (lambda p: p.parts[0] == ".cursor", "cursor_config"),
    # Scripts (Python utilities, shell scripts)
    (lambda p: p.parts[0] == "scripts", "scripts"),
    # Python source modules
    (lambda p: p.parts[0] == "src", "source"),
    # Schema CSVs and data files
    (lambda p: "schema" in p.parts and p.suffix == ".csv", "schema_csv"),
    # Processed JSON data files
    (lambda p: "processed" in p.parts and p.suffix == ".json", "data_processed"),
    # Raw data files
    (lambda p: p.parts[0] == "data", "data"),
    # Frontend HTML pages
    (lambda p: p.parts[0] == "frontend" and p.suffix == ".html", "frontend_html"),
    # Frontend JS/CSS assets
    (lambda p: p.parts[0] == "frontend" and p.suffix in {".js", ".css"}, "frontend_assets"),
    # Frontend JSON data
    (lambda p: p.parts[0] == "frontend" and p.suffix == ".json", "frontend_json"),
    # Documentation navigation
    (lambda p: p.parts[0] == "docnav", "docnav"),
    # Deployment files
    (lambda p: p.parts[0] == "deploy", "deploy"),
    # Root-level config/meta files
    (lambda p: len(p.parts) == 1, "root"),
]


def categorize(rel_path: Path) -> str:
    for predicate, category in CATEGORY_RULES:
        try:
            if predicate(rel_path):
                return category
        except (IndexError, AttributeError):
            pass
    return "other"


def collect_files() -> dict:
    categories: dict[str, list[dict]] = {}
    total = 0

    for abs_path in sorted(REPO_ROOT.rglob("*")):
        if not abs_path.is_file():
            continue

        rel = abs_path.relative_to(REPO_ROOT)
        parts = rel.parts

        # Skip excluded directories
        if any(part in EXCLUDE_DIRS for part in parts):
            continue

        # Skip excluded extensions
        if rel.suffix in EXCLUDE_EXTENSIONS:
            continue

        category = categorize(rel)
        entry = {
            "path": str(rel),
            "name": rel.name,
            "ext": rel.suffix,
        }

        categories.setdefault(category, []).append(entry)
        total += 1

    return categories, total


def main():
    print(f"Scanning {REPO_ROOT} ...")
    categories, total = collect_files()

    manifest = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": "scripts/generate_file_manifest.py",
            "repo_root": str(REPO_ROOT),
            "total_files": total,
            "categories": sorted(categories.keys()),
            "usage": (
                "Query this manifest instead of running directory searches. "
                "Fields per entry: path (repo-relative), name, ext. "
                "Regenerate with: python3 scripts/generate_file_manifest.py"
            ),
        },
        "files": categories,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    print(f"Wrote {total} files across {len(categories)} categories to {OUTPUT_PATH}")
    for cat, entries in sorted(categories.items()):
        print(f"  {cat}: {len(entries)}")


if __name__ == "__main__":
    main()
