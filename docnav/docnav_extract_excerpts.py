#!/usr/bin/env python3
"""
Walk this docnav tree and print one ENTRY_START … ENTRY_END block per file.

Usage (from repository root):

  python3 docnav/docnav_extract_excerpts.py > docnav/entries_for_ai.txt
"""

import json
import os
import re
import sys
import zipfile

DOCNAV_DIR = os.path.dirname(os.path.abspath(__file__))
EXCERPT_CHARS = 800

# Skip top-level tooling files inside docnav/ (this script lives here too).
_SKIP_ROOT_FILES = frozenset(
    {
        "REFRESH",
        "docnav_extract_excerpts.py",
        "docnav_manifest_from_entries.py",
        "docnav_build_catalog_json.py",
    }
)

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".jpe", ".webp", ".gif", ".ico", ".bmp",
    ".psd", ".psd2",
    ".woff", ".woff2", ".ttf", ".eot",
    ".mp4", ".mp3", ".wav", ".ogg",
    ".zip", ".gz", ".tar",
    ".blend", ".blend1",
}

BUNDLE_EXTENSIONS = {
    ".xlsx", ".docx", ".odt", ".ods", ".pptx",
}


def clean(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_html(path: str) -> str:
    try:
        from bs4 import BeautifulSoup
        with open(path, "rb") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        return clean(soup.get_text(separator="\n"))
    except Exception:
        return ""


def extract_pdf(path: str) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        pages = []
        for page in reader.pages[:4]:
            pages.append(page.extract_text() or "")
            if sum(len(p) for p in pages) > EXCERPT_CHARS * 3:
                break
        return clean("\n".join(pages))
    except Exception:
        return ""


def extract_office(path: str) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            xml_names = [n for n in z.namelist()
                         if n.endswith(".xml") and "word/document" in n
                         or "xl/sharedStrings" in n
                         or "ppt/slides" in n]
            if not xml_names:
                xml_names = [n for n in z.namelist() if n.endswith(".xml")][:3]
            parts = []
            for name in xml_names[:3]:
                raw = z.read(name).decode("utf-8", errors="replace")
                text = re.sub(r"<[^>]+>", " ", raw)
                parts.append(clean(text))
            return "\n".join(parts)
    except Exception:
        return ""


def extract_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return clean(f.read())
    except Exception:
        return ""


def get_excerpt(path: str, ext: str) -> str:
    text = ""
    ext_lower = ext.lower()

    if ext_lower in (".html", ".htm"):
        text = extract_html(path)
    elif ext_lower == ".pdf":
        text = extract_pdf(path)
    elif ext_lower in BUNDLE_EXTENSIONS:
        text = extract_office(path)
    elif ext_lower in (".md", ".txt", ".yaml", ".yml", ".json", ".csv",
                       ".tsv", ".py", ".js", ".css", ".tex", ".ttl",
                       ".toml", ".ini", ".cfg", ".sh", ".bat"):
        text = extract_text(path)
    elif ext_lower in SKIP_EXTENSIONS:
        return "OPAQUE (image or binary; no text extracted)"
    else:
        return "OPAQUE (unrecognized format; manual review)"

    if not text:
        return "OPAQUE (extraction returned empty)"
    return text[:EXCERPT_CHARS]


def main():
    docnav = os.path.realpath(DOCNAV_DIR)
    if not os.path.isdir(docnav):
        print(f"ERROR: docnav directory not found: {docnav}", file=sys.stderr)
        sys.exit(1)

    entries = []
    for dirpath, dirnames, filenames in os.walk(docnav):
        dirnames[:] = [d for d in sorted(dirnames) if not d.startswith(".")]
        for fname in sorted(filenames):
            if fname.startswith("."):
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, docnav)
            if os.path.dirname(rel) == "" and fname in _SKIP_ROOT_FILES:
                continue
            _, ext = os.path.splitext(fname)
            entries.append((rel, ext, full))

    for rel, ext, full in entries:
        excerpt = get_excerpt(full, ext)
        print("ENTRY_START")
        print(f"relative_path: {rel}")
        print(f"extension: {ext if ext else '(none)'}")
        print("excerpt:")
        print(excerpt)
        print("ENTRY_END")
        print()


if __name__ == "__main__":
    main()
