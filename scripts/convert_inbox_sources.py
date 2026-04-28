#!/usr/bin/env python3
"""Convert inbox source files into curated Markdown and CSV outputs.

This script is intended for the repository document-intelligence workflow:

NEW/ raw files
  -> Markdown source notes in frontend/docs/Research/source_notes/
  -> CSV tables in frontend/docs/Research/source_data/
  -> AnythingLLM ingests the clean Markdown and CSV files

Supported inputs:
  .docx  Extracts document paragraphs into a Markdown source note.
  .doc   Uses LibreOffice, if available, to convert to docx, then extracts text.
  .xlsx  Converts each visible worksheet to a CSV and creates a Markdown index note.
  .xls   Uses LibreOffice, if available, to convert to xlsx, then extracts sheets.
  .html  Extracts readable article text into a Markdown source note.

Examples:
  python scripts/convert_inbox_sources.py -dry-run
  python scripts/convert_inbox_sources.py -since-marker NOW
  python scripts/convert_inbox_sources.py NEW/example.docx
  python scripts/convert_inbox_sources.py -file NEW/example.docx
  python scripts/convert_inbox_sources.py -overwrite
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


SUPPORTED_SUFFIXES = {".docx", ".doc", ".xlsx", ".xls", ".html", ".htm"}


@dataclass(frozen=True)
class ConversionOutput:
    source: Path
    outputs: list[Path]
    note: str


class ReadableHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip_depth = 0
        self.in_title = False
        self.title_parts: list[str] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip_depth += 1
        if tag == "title":
            self.in_title = True
        if tag in {"article", "section", "h1", "h2", "h3", "p", "li", "blockquote"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self.skip_depth:
            self.skip_depth -= 1
        if tag == "title":
            self.in_title = False
        if tag in {"h1", "h2", "h3", "p", "li", "blockquote"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = normalize_space(data)
        if not text:
            return
        if self.in_title:
            self.title_parts.append(text)
        self.parts.append(text + " ")

    @property
    def title(self) -> str:
        return normalize_space(" ".join(self.title_parts))

    @property
    def lines(self) -> list[str]:
        lines: list[str] = []
        seen: set[str] = set()
        noisy_fragments = [
            "cookie",
            "privacy policy",
            "user agreement",
            "sign in",
            "subscribe",
            "all rights reserved",
        ]
        for raw_line in "".join(self.parts).splitlines():
            line = normalize_space(raw_line)
            if len(line) < 30:
                continue
            lower = line.lower()
            if any(fragment in lower for fragment in noisy_fragments):
                continue
            if line in seen:
                continue
            seen.add(line)
            lines.append(line)
        return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert NEW inbox files into Markdown source notes and CSV tables."
    )
    parser.add_argument(
        "source_file",
        nargs="?",
        help=(
            "Single file to convert. Outputs are written next to this file with "
            "the converted extension, such as .md or .csv."
        ),
    )
    parser.add_argument("-inbox", default="NEW", help="Inbox folder to scan.")
    parser.add_argument(
        "-out-notes",
        default="frontend/docs/Research/source_notes",
        help="Output folder for generated Markdown source notes.",
    )
    parser.add_argument(
        "-out-data",
        default="frontend/docs/Research/source_data",
        help="Output folder for generated CSV data.",
    )
    parser.add_argument(
        "-since-marker",
        default="",
        help="Only process files newer than this marker file, for example NOW.",
    )
    parser.add_argument(
        "-file",
        action="append",
        default=[],
        help="Specific file to process. May be supplied more than once.",
    )
    parser.add_argument(
        "-dry-run",
        action="store_true",
        help="Print planned outputs without writing files.",
    )
    parser.add_argument(
        "-overwrite",
        action="store_true",
        help="Overwrite generated outputs if they already exist.",
    )
    return parser.parse_args()


def normalize_space(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "source"


def title_from_path(path: Path) -> str:
    return normalize_space(path.stem.replace("_", " ").replace("-", " ")).title()


def unique_path(path: Path, overwrite: bool) -> Path:
    if overwrite or not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def relative_display_path(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return current


def resolve_user_path(value: str, invocation_cwd: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (invocation_cwd / path).resolve()


def discover_inputs(repo_root: Path, args: argparse.Namespace) -> list[Path]:
    if args.source_file and args.file:
        raise SystemExit("Use either positional source_file or -file, not both.")

    if args.source_file:
        files = [resolve_user_path(args.source_file, Path.cwd().resolve())]
    elif args.file:
        files = [resolve_user_path(value, Path.cwd().resolve()) for value in args.file]
    else:
        inbox = (repo_root / args.inbox).resolve()
        files = sorted(path for path in inbox.rglob("*") if path.is_file())

    if args.since_marker:
        marker = (repo_root / args.since_marker).resolve()
        if not marker.exists():
            raise SystemExit(f"Marker file not found: {marker}")
        cutoff = marker.stat().st_mtime
        files = [path for path in files if path.stat().st_mtime > cutoff]

    return [path for path in files if path.suffix.lower() in SUPPORTED_SUFFIXES]


def read_docx_paragraphs(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = ET.fromstring(xml)
    paragraphs: list[str] = []
    for para in root.findall(".//w:p", ns):
        texts = [node.text for node in para.findall(".//w:t", ns) if node.text]
        text = normalize_space("".join(texts))
        if text:
            paragraphs.append(text)
    return paragraphs


def libreoffice_convert(source: Path, target_ext: str, work_dir: Path) -> Path:
    executable = shutil.which("libreoffice") or shutil.which("soffice")
    if not executable:
        raise RuntimeError(
            f"LibreOffice is required to convert {source.suffix} files. "
            "Install libreoffice or convert this file manually first."
        )
    result = subprocess.run(
        [
            executable,
            "--headless",
            "--convert-to",
            target_ext.lstrip("."),
            "--outdir",
            str(work_dir),
            str(source),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "LibreOffice conversion failed.")
    converted = work_dir / f"{source.stem}.{target_ext.lstrip('.')}"
    if not converted.exists():
        matches = list(work_dir.glob(f"{source.stem}.*"))
        if matches:
            return matches[0]
        raise RuntimeError(f"Converted file not found for {source}")
    return converted


def read_html(path: Path) -> tuple[str, list[str]]:
    parser = ReadableHtmlParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser.title or title_from_path(path), parser.lines


def markdown_note(
    *,
    title: str,
    doc_id: str,
    source: Path,
    source_rel: str,
    body_lines: list[str],
    tags: list[str],
    source_type: str,
) -> str:
    tag_lines = "\n".join(f"  - {tag}" for tag in tags)
    extracted = "\n\n".join(body_lines) if body_lines else "No readable text was extracted."
    return f"""---
doc_id: {doc_id}
title: {title}
type: source_note
status: draft
domain: research
layer: methodology
projects:
  - unassigned
tags:
{tag_lines}
related_docs: []
key_claims: []
source_file: {source_rel}
source_type: {source_type}
created: {date.today().isoformat()}
---

# {title}

## Source Context

Generated from `{source_rel}` by `scripts/convert_inbox_sources.py`.

## Extracted Text

{extracted}

## Handling Notes

Review this source note before promoting it to active status, adding claims, or adding relationships.
"""


def convert_text_source(
    repo_root: Path,
    source: Path,
    notes_dir: Path,
    overwrite: bool,
    same_dir: bool = False,
) -> ConversionOutput:
    suffix = source.suffix.lower()
    source_rel = relative_display_path(repo_root, source)
    if suffix == ".docx":
        title = title_from_path(source)
        lines = read_docx_paragraphs(source)
        source_type = "private"
        tags = ["converted_docx", "source_note"]
    elif suffix == ".doc":
        with tempfile.TemporaryDirectory() as tmp:
            converted = libreoffice_convert(source, ".docx", Path(tmp))
            title = title_from_path(source)
            lines = read_docx_paragraphs(converted)
        source_type = "private"
        tags = ["converted_doc", "source_note"]
    else:
        title, lines = read_html(source)
        source_type = "public"
        tags = ["converted_html", "source_note"]

    slug = slugify(title)
    doc_id = f"{slug}_source_note"
    if same_dir:
        note_path = unique_path(source.with_suffix(".md"), overwrite)
    else:
        note_path = unique_path(notes_dir / f"{slug.upper()}_SOURCE_NOTE.md", overwrite)
    content = markdown_note(
        title=title,
        doc_id=doc_id,
        source=source,
        source_rel=source_rel,
        body_lines=lines,
        tags=tags,
        source_type=source_type,
    )
    note_path.write_text(content, encoding="utf-8")
    return ConversionOutput(source=source, outputs=[note_path], note=f"Markdown note: {note_path}")


def cell_value(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def convert_workbook(
    repo_root: Path,
    source: Path,
    notes_dir: Path,
    data_dir: Path,
    overwrite: bool,
    same_dir: bool = False,
) -> ConversionOutput:
    try:
        import openpyxl
    except ImportError as exc:
        raise RuntimeError("openpyxl is required for Excel conversion. Install it with pip.") from exc

    original_source = source
    with tempfile.TemporaryDirectory() as tmp:
        if source.suffix.lower() == ".xls":
            source = libreoffice_convert(source, ".xlsx", Path(tmp))

        workbook = openpyxl.load_workbook(source, data_only=True, read_only=True)
        title = title_from_path(original_source)
        slug = slugify(title)
        workbook_dir = original_source.parent if same_dir else data_dir / slug
        workbook_dir.mkdir(parents=True, exist_ok=True)
        visible_sheets = [
            sheet for sheet in workbook.worksheets if sheet.sheet_state == "visible"
        ]

        csv_outputs: list[Path] = []
        for sheet in visible_sheets:
            sheet_slug = slugify(sheet.title)
            if same_dir and len(visible_sheets) == 1:
                csv_path = unique_path(original_source.with_suffix(".csv"), overwrite)
            elif same_dir:
                csv_path = unique_path(
                    workbook_dir / f"{original_source.stem}_{sheet_slug}.csv",
                    overwrite,
                )
            else:
                csv_path = unique_path(workbook_dir / f"{sheet_slug}.csv", overwrite)
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                for row in sheet.iter_rows(values_only=True):
                    writer.writerow([cell_value(value) for value in row])
            csv_outputs.append(csv_path)

    if same_dir:
        return ConversionOutput(
            source=original_source,
            outputs=csv_outputs,
            note=f"CSV file(s): {', '.join(str(path) for path in csv_outputs)}",
        )

    source_rel = relative_display_path(repo_root, original_source)
    doc_id = f"{slug}_spreadsheet_source_note"
    note_path = unique_path(notes_dir / f"{slug.upper()}_SPREADSHEET_SOURCE_NOTE.md", overwrite)
    csv_lines = "\n".join(
        f"- `{path.relative_to(repo_root).as_posix()}`" for path in csv_outputs
    )
    content = markdown_note(
        title=f"{title} Spreadsheet Source Note",
        doc_id=doc_id,
        source=original_source,
        source_rel=source_rel,
        body_lines=[
            "This workbook was converted to CSV files for ingestion and review.",
            "Generated CSV files:",
            csv_lines or "No visible worksheets were found.",
        ],
        tags=["converted_excel", "spreadsheet", "csv"],
        source_type="private",
    )
    note_path.write_text(content, encoding="utf-8")
    return ConversionOutput(
        source=original_source,
        outputs=[note_path, *csv_outputs],
        note=f"Spreadsheet note and CSV files: {note_path}",
    )


def planned_outputs(
    repo_root: Path,
    source: Path,
    notes_dir: Path,
    data_dir: Path,
    same_dir: bool = False,
) -> list[Path]:
    title = title_from_path(source)
    if source.suffix.lower() in {".html", ".htm"}:
        title, _lines = read_html(source)
    slug = slugify(title)
    if same_dir:
        if source.suffix.lower() in {".xlsx", ".xls"}:
            return [source.with_suffix(".csv")]
        return [source.with_suffix(".md")]
    if source.suffix.lower() in {".xlsx", ".xls"}:
        return [
            notes_dir / f"{slug.upper()}_SPREADSHEET_SOURCE_NOTE.md",
            data_dir / slug,
        ]
    return [notes_dir / f"{slug.upper()}_SOURCE_NOTE.md"]


def main() -> int:
    args = parse_args()
    invocation_cwd = Path.cwd().resolve()
    repo_root = find_repo_root(invocation_cwd)
    notes_dir = (repo_root / args.out_notes).resolve()
    data_dir = (repo_root / args.out_data).resolve()
    inputs = discover_inputs(repo_root, args)
    same_dir = bool(args.source_file) or len(args.file) == 1

    print(f"Input files: {len(inputs)}")
    if not inputs:
        return 0

    if args.dry_run:
        for source in inputs:
            rel = relative_display_path(repo_root, source)
            print(f"would convert: {rel}")
            for output in planned_outputs(repo_root, source, notes_dir, data_dir, same_dir):
                print(f"  -> {relative_display_path(repo_root, output)}")
        print("Dry run complete. No files written.")
        return 0

    if not same_dir:
        notes_dir.mkdir(parents=True, exist_ok=True)
        data_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for source in inputs:
        rel = relative_display_path(repo_root, source)
        try:
            if source.suffix.lower() in {".xlsx", ".xls"}:
                result = convert_workbook(
                    repo_root,
                    source,
                    notes_dir,
                    data_dir,
                    args.overwrite,
                    same_dir=same_dir,
                )
            else:
                result = convert_text_source(
                    repo_root,
                    source,
                    notes_dir,
                    args.overwrite,
                    same_dir=same_dir,
                )
        except Exception as exc:
            failures += 1
            print(f"failed: {rel}: {exc}", file=sys.stderr)
            continue
        print(f"converted: {rel}")
        for output in result.outputs:
            print(f"  -> {relative_display_path(repo_root, output)}")

    if failures:
        print(f"Completed with {failures} failure(s).", file=sys.stderr)
        return 1
    print("Conversion complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
