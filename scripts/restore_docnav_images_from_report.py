#!/usr/bin/env python3
"""
Restore broken docnav image links listed in broken_image_links_report.tsv.

- Archive appendix refs (../Images/...) copy into docnav/Repos/intra/TVPCI/Images/
  Primary source: /home/jw/Desktop/NULL/INDEXED/Images/
  Fallback for a few names: /home/jw/books/archive/normalized/

- TVPCI_FOUNDATION.md sibling PNGs copy from TVPCI_FOUNDATION/ next to the .md file.

Does not copy the whole 3.5G INDEXED tree, only files mentioned in the report.

Usage:
  python3 scripts/restore_docnav_images_from_report.py
  python3 scripts/restore_docnav_images_from_report.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCNAV = REPO / "docnav"
REPORT = DOCNAV / "broken_image_links_report.tsv"
INDEXED_IMAGES = Path.home() / "Desktop" / "NULL" / "INDEXED" / "Images"
NORMALIZED = Path.home() / "books" / "archive" / "normalized"
TVPCI = DOCNAV / "Repos" / "intra" / "TVPCI"
FOUNDATION_DIR = TVPCI / "TVPCI_FOUNDATION"


def locate_first(basename: str) -> Path | None:
    try:
        out = subprocess.run(
            ["locate", basename],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    skip_parts = (".Trash", "CLONE/BACKUP", "/Trash/")
    for line in out.stdout.strip().split("\n"):
        p = Path(line.strip())
        if not p.is_file():
            continue
        if p.name != basename:
            continue
        s = str(p)
        if any(x in s for x in skip_parts):
            continue
        return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not REPORT.is_file():
        print(f"Missing report: {REPORT}", file=sys.stderr)
        return 1

    rows: list[dict[str, str]] = []
    with REPORT.open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rows.append(row)

    copies: list[tuple[Path, Path]] = []

    for row in rows:
        reason = row.get("reason", "")
        if reason.startswith("broken_symlink"):
            continue
        ref = row["reference"].strip()
        dest = Path(row["resolved_path"].strip())
        if not ref or not str(dest):
            continue

        src: Path | None = None

        if ref.startswith("../Images/"):
            rel = ref[len("../Images/") :]
            cand = INDEXED_IMAGES / rel
            if cand.is_file():
                src = cand
            else:
                bn = Path(rel).name
                cand2 = NORMALIZED / bn
                if cand2.is_file():
                    src = cand2
                else:
                    loc = locate_first(bn)
                    if loc and loc.is_file():
                        src = loc

            if src:
                copies.append((src, dest))

        elif "/" not in ref.replace("\\", "/") and ref.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
        ):
            cand = FOUNDATION_DIR / ref
            if cand.is_file():
                copies.append((cand, dest))
            else:
                cand2 = FOUNDATION_DIR / "archive" / ref
                if cand2.is_file():
                    copies.append((cand2, dest))

    seen: set[tuple[str, str]] = set()
    unique_copies: list[tuple[Path, Path]] = []
    for s, d in copies:
        key = (str(s.resolve()), str(d.resolve()))
        if key in seen:
            continue
        seen.add(key)
        unique_copies.append((s, d))

    ok = 0
    fail = 0
    for src, dest in unique_copies:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if args.dry_run:
            print(f"would copy\n  {src}\n  -> {dest}")
            ok += 1
            continue
        try:
            shutil.copy2(src, dest)
            print(f"OK {dest.relative_to(DOCNAV)}")
            ok += 1
        except OSError as e:
            print(f"FAIL {dest}: {e}", file=sys.stderr)
            fail += 1

    symlink_path = DOCNAV / "Research" / "FRONTEND_SIMULATOR_VISUALIZATION_STRATEGY.md"
    target_rel = Path("../../frontend/project/gold/data/FRONTEND_SIMULATOR_VISUALIZATION_STRATEGY.md")
    real_target = (symlink_path.parent / target_rel).resolve()
    if real_target.is_file():
        if not args.dry_run and symlink_path.is_symlink():
            symlink_path.unlink()
            symlink_path.symlink_to(target_rel)
            print(f"symlink OK Research/FRONTEND_SIMULATOR_VISUALIZATION_STRATEGY.md -> {target_rel}")
        elif args.dry_run:
            print(f"would symlink {symlink_path} -> {target_rel}")

    print(f"\nplanned_unique={len(unique_copies)} copied_ok={ok} failed={fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
