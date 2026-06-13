#!/usr/bin/env python3
"""
Check project folders for cross-project data or copy bleed.

The check is intentionally conservative:
- shared breadcrumb/resource-footer snippets are ignored by default
- comparison projects are skipped by default
- legitimate terms such as "Gold Standard" in AUBEB carbon-standard context are allowlisted

Exit code is non-zero when high-confidence data bleed is found.
Use --strict to treat cross-project wording as errors too.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_TERMS: dict[str, list[str]] = {
    "gold": [
        r"\bgold\b",
        r"\bCOMEX\b",
        r"\bLBMA\b",
        r"\bbullion\b",
        r"\btroy oz\b",
        r"\bDor[eé]\b",
        r"\bGood Delivery\b",
        r"\bunallocated\b",
        r"\bETF\b",
        r"\bmetal lease\b",
        r"\bpaper-to-physical\b",
        r"\bNewmont\b",
        r"\bBarrick\b",
        r"\bAISC\b",
    ],
    "west_african_shea": [
        r"\bshea\b",
        r"\bBurkina\b",
        r"\bshea butter\b",
        r"\bshea kernel\b",
        r"\bwomen['’]s cooperative\b",
    ],
    "aubeb": [
        r"\bAUBEB\b",
        r"\baubeb\b",
        r"\bmangrove\b",
        r"\bBlue Economy\b",
        r"\bODIN\b",
        r"\bCBEMR\b",
    ],
    "water_newwater": [
        r"\bNEWater\b",
        r"\bPUB\b",
        r"\bSingapore\b",
    ],
    "water_ocwd": [
        r"\bOCWD\b",
        r"\bOC San\b",
        r"\bGWRS\b",
        r"\bOrange County\b",
        r"\bFountain Valley\b",
    ],
    "water_jackson_ms": [
        r"\bJackson\b",
        r"\bMississippi\b",
        r"\bO\.B\. Curtis\b",
    ],
    "grid_ercot_uri": [
        r"\bERCOT\b",
        r"\bWinter Storm Uri\b",
        r"\bWinter Storm\b",
        r"\bload shedding\b",
    ],
}


INTENTIONAL_COMPARISON_PROJECTS = {
    "water_compare",
}


SCAN_SUFFIXES = {
    ".html",
    ".js",
    ".json",
    ".csv",
    ".yaml",
    ".yml",
}


SHARED_BLOCK_PATTERNS = [
    re.compile(r"<script>\s*/\*\s*.*?Auto-breadcrumb.*?</script>", re.DOTALL),
    re.compile(r"<script>\s*/\*\s*.*?Contextual Resource Footer.*?</script>", re.DOTALL),
]


@dataclass(frozen=True)
class Finding:
    severity: str
    own_project: str
    foreign_project: str
    path: str
    line: int
    kind: str
    match: str
    snippet: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def strip_shared_blocks(text: str) -> str:
    stripped = text
    for pattern in SHARED_BLOCK_PATTERNS:
        stripped = pattern.sub("", stripped)
    return stripped


def is_allowlisted(own_project: str, foreign_project: str, text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 80) : min(len(text), end + 80)]

    if foreign_project == "gold" and "Gold Standard" in window:
        return True

    if own_project.startswith("water_") and foreign_project.startswith("water_"):
        related_context = (
            "compare" in window.lower()
            or "comparison" in window.lower()
            or "benchmark" in window.lower()
            or "contrast" in window.lower()
            or "distinct from" in window.lower()
            or "related" in window.lower()
        )
        if related_context:
            return True

    return False


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def snippet(text: str, start: int, end: int) -> str:
    raw = text[max(0, start - 70) : min(len(text), end + 90)]
    return " ".join(raw.split())


def iter_project_files(project_dir: Path) -> Iterable[Path]:
    for path in project_dir.rglob("*"):
        if path.is_file() and path.suffix in SCAN_SUFFIXES:
            yield path


def compile_project_path_patterns(projects: Iterable[str]) -> dict[str, re.Pattern[str]]:
    patterns = {}
    for project in projects:
        patterns[project] = re.compile(
            rf"(?P<path>(?:/)?frontend/project/{re.escape(project)}/[^\s\"'<>)]*|/project/{re.escape(project)}/[^\s\"'<>)]*)"
        )
    return patterns


def scan_project(
    project_root: Path,
    own_project: str,
    all_projects: list[str],
    include_shared: bool,
    strict: bool,
    include_docs: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    project_dir = project_root / own_project
    path_patterns = compile_project_path_patterns(all_projects)

    for path in iter_project_files(project_dir):
        if path.suffix == ".md" and not include_docs:
            continue

        raw_text = path.read_text(errors="ignore")
        text = raw_text if include_shared else strip_shared_blocks(raw_text)
        rel = str(path.relative_to(project_root))

        for foreign_project in all_projects:
            if foreign_project == own_project:
                continue

            path_pattern = path_patterns[foreign_project]
            for match in path_pattern.finditer(text):
                matched_path = match.group("path")
                if is_allowlisted(own_project, foreign_project, text, match.start(), match.end()):
                    continue
                severity = "error" if "/data/" in matched_path else "warning"
                findings.append(
                    Finding(
                        severity=severity,
                        own_project=own_project,
                        foreign_project=foreign_project,
                        path=rel,
                        line=line_number(text, match.start()),
                        kind="foreign_path",
                        match=matched_path,
                        snippet=snippet(text, match.start(), match.end()),
                    )
                )

            for term in PROJECT_TERMS.get(foreign_project, []):
                term_pattern = re.compile(term, re.IGNORECASE)
                for match in term_pattern.finditer(text):
                    if is_allowlisted(own_project, foreign_project, text, match.start(), match.end()):
                        continue

                    findings.append(
                        Finding(
                            severity="error" if strict else "warning",
                            own_project=own_project,
                            foreign_project=foreign_project,
                            path=rel,
                            line=line_number(text, match.start()),
                            kind="foreign_term",
                            match=match.group(0),
                            snippet=snippet(text, match.start(), match.end()),
                        )
                    )

    return findings


def project_dirs(project_root: Path) -> list[str]:
    return sorted(
        path.name
        for path in project_root.iterdir()
        if path.is_dir() and path.name not in INTENTIONAL_COMPARISON_PROJECTS
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", action="append", help="Project slug to scan. Can be passed multiple times.")
    parser.add_argument("--include-shared", action="store_true", help="Include shared breadcrumb/resource-footer snippets.")
    parser.add_argument("--include-docs", action="store_true", help="Also scan markdown documentation under project folders.")
    parser.add_argument("--strict", action="store_true", help="Treat foreign domain terms as errors, not warnings.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--max-findings", type=int, default=200, help="Maximum findings to print in text mode.")
    args = parser.parse_args()

    root = repo_root()
    project_root = root / "frontend" / "project"
    all_projects = project_dirs(project_root)
    selected = args.project or all_projects

    unknown = sorted(set(selected) - set(all_projects))
    if unknown:
        print(f"Unknown project(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for project in selected:
        findings.extend(
            scan_project(
                project_root,
                project,
                all_projects,
                args.include_shared,
                args.strict,
                args.include_docs,
            )
        )

    error_count = sum(1 for finding in findings if finding.severity == "error")
    warning_count = sum(1 for finding in findings if finding.severity == "warning")

    if args.json:
        print(
            json.dumps(
                {
                    "errors": error_count,
                    "warnings": warning_count,
                    "findings": [finding.__dict__ for finding in findings],
                },
                indent=2,
            )
        )
    else:
        print("Project bleed check")
        print(f"Projects scanned: {', '.join(selected)}")
        print(f"Errors: {error_count}")
        print(f"Warnings: {warning_count}")
        print()

        if findings:
            print("Findings")
            for finding in findings[: args.max_findings]:
                print(
                    f"[{finding.severity}] {finding.own_project} -> {finding.foreign_project} "
                    f"{finding.path}:{finding.line} {finding.kind}: {finding.match}"
                )
                print(f"  {finding.snippet}")
            if len(findings) > args.max_findings:
                print(f"... {len(findings) - args.max_findings} more findings not shown")
        else:
            print("No cross-project bleed found.")

    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
