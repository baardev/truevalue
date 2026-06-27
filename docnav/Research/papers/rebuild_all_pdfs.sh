#!/usr/bin/env bash
# Rebuild every research paper PDF under docnav/Research/papers/.
#
# Pipeline per paper (see .cursor/skills/create-research-paper and
# .cursor/skills/research-paper-latex):
#   1. pandoc: Markdown -> latex/_<slug>_pandoc_raw.tex
#   2. pandoc_paper_postprocess.py --md: raw .tex -> <slug>/<slug>.tex
#   3. research_paper_pdflatex.sh: two-pass pdflatex (+ bibtex if refs.bib exists)
#
# Usage:
#   ./rebuild_all_pdfs.sh              # all numbered papers
#   ./rebuild_all_pdfs.sh --flatten    # flatten PNGs first, then rebuild all
#   ./rebuild_all_pdfs.sh 16          # single paper by number
#   ./rebuild_all_pdfs.sh 16_tholonic-spinoza-leibniz   # single paper by slug
#
# Requires: pandoc, python3, pdflatex (texlive).

set -euo pipefail

PAPERS_ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${PAPERS_ROOT}/../../.." && pwd)"

FLATTEN=false
ONLY=()

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage 0
      ;;
    --flatten)
      FLATTEN=true
      shift
      ;;
    --)
      shift
      ONLY+=("$@")
      break
      ;;
    -*)
      echo "error: unknown option $1" >&2
      usage 1
      ;;
    *)
      ONLY+=("$1")
      shift
      ;;
  esac
done

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: $1 not found ($2)" >&2
    exit 1
  fi
}

require_cmd pandoc "install pandoc"
require_cmd python3 "python3 required"
require_cmd pdflatex "install TeX (e.g. texlive-most)"

paper_slugs() {
  local f slug
  for f in "${PAPERS_ROOT}"/[0-9]*_*.md; do
    [[ -f "$f" ]] || continue
    slug="$(basename "$f" .md)"
    case "$slug" in
      *_AI_NOTES|*_NOTES) continue ;;
    esac
    if [[ ! -d "${PAPERS_ROOT}/${slug}" ]]; then
      echo "warn: skipping ${slug} (no paper directory)" >&2
      continue
    fi
    echo "$slug"
  done | sort -t_ -k1n
}

resolve_slug() {
  local arg="$1"
  local slug

  if [[ "$arg" =~ ^[0-9]+$ ]]; then
    for slug in $(paper_slugs); do
      if [[ "$slug" =~ ^${arg}_ ]]; then
        echo "$slug"
        return 0
      fi
    done
    echo "error: no paper numbered $arg" >&2
    return 1
  fi

  if [[ -f "${PAPERS_ROOT}/${arg}.md" && -d "${PAPERS_ROOT}/${arg}" ]]; then
    echo "$arg"
    return 0
  fi

  echo "error: unknown paper '$arg' (need <N> or <N>_<slug>)" >&2
  return 1
}

build_paper() {
  local slug="$1"
  local md="${PAPERS_ROOT}/${slug}.md"
  local raw_tex="latex/_${slug}_pandoc_raw.tex"
  local out_tex="${PAPERS_ROOT}/${slug}/${slug}.tex"
  local paper_dir_rel="docnav/Research/papers/${slug}"

  echo "=== ${slug} ==="

  mkdir -p "${PAPERS_ROOT}/latex" "${PAPERS_ROOT}/${slug}"

  (
    cd "$PAPERS_ROOT"
    pandoc "${slug}.md" \
      -o "$raw_tex" \
      --standalone \
      -V documentclass=article \
      -V papersize=letter \
      -V geometry=margin=1in \
      -V fontsize=11pt
  )

  python3 "${REPO_ROOT}/scripts/pandoc_paper_postprocess.py" \
    "${PAPERS_ROOT}/${raw_tex}" \
    "$out_tex" \
    --md "$md"

  "${REPO_ROOT}/scripts/research_paper_pdflatex.sh" "$paper_dir_rel"

  echo "built: ${PAPERS_ROOT}/${slug}/${slug}.pdf"
}

if $FLATTEN; then
  echo "flattening figure PNGs..."
  "${PAPERS_ROOT}/flatten_figure_pngs.sh"
  echo
fi

TARGETS=()
if [[ ${#ONLY[@]} -gt 0 ]]; then
  for arg in "${ONLY[@]}"; do
    TARGETS+=("$(resolve_slug "$arg")")
  done
else
  mapfile -t TARGETS < <(paper_slugs)
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  echo "error: no papers to build" >&2
  exit 1
fi

failed=()
built=0

for slug in "${TARGETS[@]}"; do
  if build_paper "$slug"; then
    built=$((built + 1))
  else
    failed+=("$slug")
    echo "FAILED: $slug" >&2
  fi
  echo
done

echo "done: $built built, ${#failed[@]} failed"
if [[ ${#failed[@]} -gt 0 ]]; then
  printf '  failed: %s\n' "${failed[@]}"
  echo "After committing, run ./pushpng.sh from the repo root to upload LFS binaries."
  exit 1
fi

echo "After committing, run ./pushpng.sh from the repo root to upload LFS binaries."
