#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  md2html.sh input.md [output.html]

Description:
  Converts a Markdown file to a standalone HTML file with:
    - embedded images/resources (--embed-resources; needs network once to bundle MathJax)
    - MathJax for LaTeX math ($...$, $$...$$), so full TeX (\frac, \text, etc.) typesets correctly
    - images found via --resource-path: the .md’s directory, plus a same‑named subfolder
      (e.g. MyDoc.md + MyDoc/ for figures) when that folder exists
    - CSS styling
    - syntax highlighting
    - table of contents
    - metadata support

Examples:
  ./md2html.sh notes.md
  ./md2html.sh notes.md notes.html
EOF
    exit 1
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage
fi

INPUT="$1"
INPUT_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
INPUT="$(cd "$INPUT_DIR" && pwd)/$(basename "$INPUT")"

if [[ ! -f "$INPUT" ]]; then
    echo "Error: input file not found: $INPUT" >&2
    exit 1
fi

if [[ $# -eq 2 ]]; then
    OUTPUT="$2"
else
    OUTPUT="${INPUT%.*}.html"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CSS_FILE="$SCRIPT_DIR/md2html.css"
TEMPLATE_FILE="$SCRIPT_DIR/md2html-template.html"

if ! command -v pandoc >/dev/null 2>&1; then
    echo "Error: pandoc is not installed." >&2
    echo "Install it with:" >&2
    echo "  sudo pacman -S pandoc" >&2
    exit 1
fi

EMBED_FLAG="--embed-resources"
if ! pandoc --help 2>/dev/null | grep -q -- '--embed-resources'; then
    EMBED_FLAG="--self-contained"
fi

TITLE="$(basename "${INPUT%.*}")"
# Figures often live in a subfolder named like the source file (e.g. TVPCI_FOUNDATION/TVPCI_FOUNDATION.md + TVPCI_FOUNDATION/*.png)
STEM_DIR="$INPUT_DIR/$TITLE"
if [[ -d "$STEM_DIR" ]]; then
  RESOURCE_PATH="${INPUT_DIR}:${STEM_DIR}"
else
  RESOURCE_PATH="$INPUT_DIR"
fi

# Use MathJax for math: Pandoc's default HTML path converts TeX to MathML via texmath,
# which often warns and leaves raw $...$ for \frac, \text, \sqrt, \boldsymbol, etc.
# MathJax in the browser typesets full TeX; requires network (or a cached script) to load.
pandoc "$INPUT" \
    --from markdown+smart \
    --to html5 \
    --standalone \
    --mathjax \
    --resource-path="$RESOURCE_PATH" \
    "$EMBED_FLAG" \
    --css "$CSS_FILE" \
    --template "$TEMPLATE_FILE" \
    --metadata title="$TITLE" \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --highlight-style=pygments \
    --wrap=preserve \
    --output "$OUTPUT"

echo "Created: $OUTPUT"
