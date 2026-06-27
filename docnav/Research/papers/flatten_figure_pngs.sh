#!/usr/bin/env bash
# Flatten PNG figures onto a white background (RGB, no alpha).
# Run from anywhere. Targets every *.png under this papers directory:
#   - docnav/Research/papers/figures/          (shared pool)
#   - docnav/Research/papers/<N>_<slug>/figures/
#
# Transparent PNGs embedded in PDFs produce soft-mask layers that break
# GitHub's inline PDF viewer. Flatten before rebuilding PDFs.
#
# Requires ImageMagick (magick or convert).

set -euo pipefail

PAPERS_ROOT="$(cd "$(dirname "$0")" && pwd)"

if command -v magick >/dev/null 2>&1; then
  identify_cmd() { magick identify -format '%A' "$1"; }
  flatten_png() { magick "$1" -background white -alpha remove -alpha off "$1"; }
elif command -v convert >/dev/null 2>&1 && command -v identify >/dev/null 2>&1; then
  identify_cmd() { identify -format '%A' "$1"; }
  flatten_png() { convert "$1" -background white -alpha remove -alpha off "$1"; }
else
  echo "error: ImageMagick required (magick, or convert + identify)" >&2
  exit 1
fi

flattened=0
skipped=0
total=0

while IFS= read -r -d '' png; do
  total=$((total + 1))
  alpha="$(identify_cmd "$png")"
  # Undefined / False = no transparency; Blend / True = alpha channel present.
  if [[ "$alpha" == "Undefined" || "$alpha" == "False" ]]; then
    skipped=$((skipped + 1))
    continue
  fi
  flatten_png "$png"
  echo "flattened: ${png#"$PAPERS_ROOT"/}"
  flattened=$((flattened + 1))
done < <(find "$PAPERS_ROOT" -type f -name '*.png' -print0 | sort -z)

echo "done: $flattened flattened, $skipped already opaque, $total PNG files scanned"
