#!/usr/bin/env bash
set -euo pipefail

# Batch-generate HTML viewers from CSV, JSON, and YAML under the repo root.
# Output: viewable/<mirrored-repo-relative-path>.html (mirrors the source file path;
#   e.g. frontend/project/gold/data/schema/x.csv → viewable/frontend/project/gold/data/schema/x.html)
# Run from anywhere; working directory is set to the repository root.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

VIEWABLE="viewable"
CSV_CONV="${SCRIPT_DIR}/csv2html.py"
JSONYAML_CONV="${SCRIPT_DIR}/jsonyaml2html.py"

for c in "$CSV_CONV" "$JSONYAML_CONV"; do
  if [[ ! -f "$c" ]]; then
    echo "Error: converter not found: $c" >&2
    exit 1
  fi
done

# Prune VCS, dependencies, generated MkDocs site, and our output tree from searches
FIND_PRUNE=(
  ! -path '*/.git/*'
  ! -path '*/node_modules/*'
  ! -path '*/site/*'
  ! -path '*/.venv/*'
  ! -path '*/venv/*'
  ! -path "./${VIEWABLE}/*"
)

while IFS= read -r -d '' f; do
  rel="${f#./}"
  base="${rel%.csv}"
  html_file="${VIEWABLE}/${base}.html"
  echo "Converting: $f -> $html_file"
  python3 "$CSV_CONV" "$f" "$html_file"
done < <(find . -type f -name "*.csv" "${FIND_PRUNE[@]}" -print0)

while IFS= read -r -d '' f; do
  case "$f" in
    */package-lock.json) continue ;;
  esac
  rel="${f#./}"
  if [[ "$f" == *.json ]]; then
    base="${rel%.json}"
  elif [[ "$f" == *.yaml ]]; then
    base="${rel%.yaml}"
  else
    base="${rel%.yml}"
  fi
  html_file="${VIEWABLE}/${base}.html"
  echo "Converting: $f -> $html_file"
  python3 "$JSONYAML_CONV" "$f" "$html_file"
done < <(find . -type f \( -name "*.json" -o -name "*.yml" -o -name "*.yaml" \) "${FIND_PRUNE[@]}" -print0)

# Also place schema table viewers under frontend/.../data/schema/ (same path as
# the source CSV) so /frontend/project/.../schema/*.html works for footers and
# badges, not only /viewable/frontend/... (see rebuild-site.sh header).
for d in "frontend/project/gold/data/schema" "frontend/project/shea/data/schema"; do
  v="${VIEWABLE}/${d}"
  if [[ -d "$v" && -d "$d" ]]; then
    shopt -s nullglob
    for h in "$v"/*.html; do
      base="$(basename "$h")"
      cp -f "$h" "$d/$base"
    done
    shopt -u nullglob
    echo "Synced HTML viewers: $d/"
  fi
done

echo "Done."
