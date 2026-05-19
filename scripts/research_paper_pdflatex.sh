#!/usr/bin/env bash
# Two-pass pdflatex for a paper folder where <basename>/<basename>.tex holds the source
# (same layout as papers 1 to 5 and paper 6).
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <paper-dir-relative-to-repo-root>" >&2
  echo "Example: $(basename "$0") docnav/Research/papers/6_qualitative-nature-integers-triadic-roles" >&2
  exit 1
}

[[ $# -eq 1 ]] || usage

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REL="$1"
PAPER_DIR="$REPO_ROOT/$REL"
BASE="$(basename "$PAPER_DIR")"
TEX="${PAPER_DIR}/${BASE}.tex"

if [[ ! -f "$TEX" ]]; then
  echo "error: missing $TEX" >&2
  exit 1
fi

if ! command -v pdflatex >/dev/null 2>&1; then
  echo "error: pdflatex not found. Install a TeX distribution (for example texlive-most on Manjaro/arch)." >&2
  exit 1
fi

cd "$PAPER_DIR"
pdflatex -interaction=nonstopmode "${BASE}.tex"
pdflatex -interaction=nonstopmode "${BASE}.tex"
