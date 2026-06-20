#!/usr/bin/env python3
"""
Build csv_catalog.json listing CSV files under frontend/project/.

Paths in JSON are relative to docnav/ (e.g. ../frontend/project/gold/data/foo.csv)
so docnav/view.html can fetch them when the site root is the repository root.

Typical usage (from repository root):

    python3 docnav/docnav_build_csv_catalog_json.py
"""

from __future__ import annotations

import argparse
import csv
import json
import os

DEFAULT_SITE_BASE = "https://tvf.tholonia.com/"
PROJECT_REL = os.path.join("frontend", "project")


def _repo_root_from_docnav(docnav_dir: str) -> str:
    return os.path.abspath(os.path.join(docnav_dir, ".."))


def _path_for_viewer(docnav_dir: str, abs_csv: str) -> str:
    rel = os.path.relpath(abs_csv, docnav_dir)
    return rel.replace("\\", "/")


def _url_public(site_base: str, repo_root: str, abs_csv: str) -> str:
    rel = os.path.relpath(abs_csv, repo_root).replace("\\", "/")
    base = site_base.rstrip("/") + "/"
    return base + rel


def _hub_and_tags(repo_root: str, abs_csv: str) -> tuple[str, list[str]]:
    rel_repo = os.path.relpath(abs_csv, repo_root).replace("\\", "/")
    parts = rel_repo.split("/")
    tags: list[str] = ["fmt/csv"]
    hub = "project"
    if len(parts) >= 3 and parts[0] == "frontend" and parts[1] == "project":
        hub = parts[2]
    tags.append(f"topic/{hub}")
    if "/schema/" in f"/{rel_repo}/":
        tags.append("kind/schema")
    if "/processed/" in f"/{rel_repo}/":
        tags.append("kind/processed")
    return hub, tags


def _summary_preview(abs_csv: str, max_line: int = 240) -> str:
    try:
        with open(abs_csv, encoding="utf-8", errors="replace", newline="") as f:
            r = csv.reader(f)
            row1 = next(r, None)
            row2 = next(r, None)
    except OSError:
        return ""
    parts: list[str] = []
    if row1:
        line = ", ".join(cell.strip() for cell in row1[:24])
        if len(row1) > 24:
            line += ", …"
        if len(line) > max_line:
            line = line[: max_line - 1] + "…"
        parts.append("Header: " + line)
    if row2:
        line2 = ", ".join(cell.strip() for cell in row2[:16])
        if len(row2) > 16:
            line2 += ", …"
        if len(line2) > 120:
            line2 = line2[:119] + "…"
        parts.append("Sample row: " + line2)
    return " · ".join(parts)


def main() -> None:
    docnav_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = _repo_root_from_docnav(docnav_dir)
    project_root = os.path.join(repo_root, PROJECT_REL)

    ap = argparse.ArgumentParser(description="Build docnav/csv_catalog.json from frontend/project CSV files.")
    ap.add_argument(
        "--project-root",
        default=project_root,
        help="Directory to scan recursively for *.csv (default: <repo>/frontend/project)",
    )
    ap.add_argument(
        "--out",
        default=os.path.join(docnav_dir, "csv_catalog.json"),
        help="Output JSON path",
    )
    ap.add_argument(
        "--base",
        default=DEFAULT_SITE_BASE,
        help="Absolute site base for csv.url (trailing slash optional)",
    )
    args = ap.parse_args()

    scan_root = os.path.abspath(args.project_root)
    if not os.path.isdir(scan_root):
        print(f"Warning: project root not found: {scan_root}", file=__import__("sys").stderr)
        out_list: list[dict[str, object]] = []
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out_list, f, ensure_ascii=False, indent=2)
        print(f"Wrote 0 entries to {args.out}")
        return

    csv_paths: list[str] = []
    for dirpath, dirnames, filenames in os.walk(scan_root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            if name.lower().endswith(".csv"):
                csv_paths.append(os.path.join(dirpath, name))

    csv_paths.sort(key=lambda p: p.casefold())

    out: list[dict[str, object]] = []
    for abs_csv in csv_paths:
        hub, tags = _hub_and_tags(repo_root, abs_csv)
        name = os.path.basename(abs_csv)
        title = f"csv ({hub}): {name}"
        rel_view = _path_for_viewer(docnav_dir, abs_csv)
        out.append(
            {
                "title": title,
                "path": rel_view,
                "tags": tags,
                "summary": _summary_preview(abs_csv),
                "url": _url_public(args.base, repo_root, abs_csv),
            }
        )

    out.sort(key=lambda x: str(x["title"]).casefold())
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(out)} entries to {args.out}")


if __name__ == "__main__":
    main()
