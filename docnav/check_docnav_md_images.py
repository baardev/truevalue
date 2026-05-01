#!/usr/bin/env python3
"""
Scan Markdown under docnav/ for image references and report broken local targets.

Checks:
  - ![alt](url)
  - ![alt](url "title")
  - <img src="...">

Relative URLs resolve from the directory containing the .md file.
http/https and mailto: are skipped (not verified).
Fragment-only (#...) skipped.

Usage:
  python3 scripts/check_docnav_md_images.py
  python3 scripts/check_docnav_md_images.py --json docnav/broken_image_links.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

DOCNAV = Path(__file__).resolve().parent.parent / "docnav"

# ![ ... ]( ... )
MD_IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
# <img ... src="..." ...>
HTML_IMG_SRC = re.compile(
    r"<img\b[^>]*\bsrc\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
    re.IGNORECASE,
)


def strip_md_title(url_part: str) -> str:
    s = url_part.strip()
    # trailing title: spaces + quoted string
    s = re.sub(r'\s+"[^"]*"\s*$', "", s)
    s = re.sub(r"\s+'[^']*'\s*$", "", s)
    return s.strip()


def normalize_target(raw: str) -> str:
    s = strip_md_title(raw)
    if s.startswith("<") and s.endswith(">"):
        s = s[1:-1].strip()
    return s


def collect_refs(text: str) -> list[str]:
    refs: list[str] = []
    for m in MD_IMG.finditer(text):
        refs.append(normalize_target(m.group(1)))
    for m in HTML_IMG_SRC.finditer(text):
        url = m.group(1) or m.group(2) or m.group(3) or ""
        url = url.strip()
        if url:
            refs.append(url)
    return refs


def should_skip_remote(target: str) -> bool:
    t = target.strip()
    lower = t.lower()
    if lower.startswith(("http://", "https://", "mailto:", "#")):
        return True
    if lower.startswith("//"):
        return True
    return False


def resolve_local(md_path: Path, target: str) -> Path | None:
    """Return absolute path if target is local filesystem ref, else None."""
    t = target.strip()
    if not t or should_skip_remote(t):
        return None
    if "://" in t:
        return None
    t = t.split("#", 1)[0].split("?", 1)[0]
    if not t:
        return None
    if os.path.isabs(t):
        return Path(t)
    return (md_path.parent / t).resolve()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=DOCNAV)
    ap.add_argument("--tsv", type=Path, default=DOCNAV / "broken_image_links_report.tsv")
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()
    root = args.root.resolve()

    broken: list[dict[str, str]] = []
    scanned_files = 0
    total_refs = 0
    local_checked = 0

    for md in sorted(root.rglob("*.md")):
        scanned_files += 1
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            reason = "read_error"
            if md.is_symlink():
                tip = md.readlink()
                tgt = (md.parent / tip).resolve()
                if not tgt.exists():
                    reason = "broken_symlink"
            broken.append(
                {
                    "markdown_file": str(md.relative_to(root)),
                    "reference": str(md.readlink()) if md.is_symlink() else "",
                    "resolved_path": str(md.resolve()),
                    "reason": f"{reason}: {e}",
                }
            )
            continue

        for target in collect_refs(text):
            total_refs += 1
            if not target.strip():
                continue
            if should_skip_remote(target):
                continue
            resolved = resolve_local(md, target)
            if resolved is None:
                continue
            local_checked += 1
            try:
                exists = resolved.is_file()
            except OSError:
                exists = False
            if not exists:
                broken.append(
                    {
                        "markdown_file": str(md.relative_to(root)),
                        "reference": target,
                        "resolved_path": str(resolved),
                        "reason": "missing_file",
                    }
                )

    args.tsv.parent.mkdir(parents=True, exist_ok=True)
    with args.tsv.open("w", encoding="utf-8", newline="\n") as f:
        f.write("markdown_file\treference\tresolved_path\treason\n")
        for row in broken:
            f.write(
                "\t".join(
                    [
                        row["markdown_file"].replace("\t", " "),
                        row["reference"].replace("\t", " "),
                        row["resolved_path"].replace("\t", " "),
                        row["reason"].replace("\t", " "),
                    ]
                )
                + "\n"
            )

    summary = {
        "docnav_root": str(root),
        "markdown_files_scanned": scanned_files,
        "image_ref_occurrences": total_refs,
        "local_paths_checked": local_checked,
        "broken_local_count": len(broken),
        "report_tsv": str(args.tsv),
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps({"summary": summary, "broken": broken}, indent=2),
            encoding="utf-8",
        )

    print(json.dumps(summary, indent=2))
    if broken:
        print(f"\nBroken local image links ({len(broken)}):\n")
        for row in broken:
            print(f"  {row['markdown_file']}")
            print(f"    ref: {row['reference']}")
            print(f"    expected: {row['resolved_path']}")
            print()
    else:
        print("\nNo broken local image links found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
