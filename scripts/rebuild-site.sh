 #!/usr/bin/env bash
# =============================================================================
# rebuild-site.sh  —  TrueValue Analytics site rebuild script
# =============================================================================
#
# Run from anywhere; script cd's to the repo root automatically.
# Usage:
#   ./scripts/rebuild-site.sh                  # default: viewable + mkdocs
#   RUN_GENERATE_UI=1 ./scripts/rebuild-site.sh # also regenerate UI JSON
#   RUN_MKDOCS=0       ./scripts/rebuild-site.sh # viewable only
#   RUN_VIEWABLE=0     ./scripts/rebuild-site.sh # mkdocs only
#   RUN_HEALTHCHECK=1  ./scripts/rebuild-site.sh # run health_check.py first
#
# ----------------------------------------------------------------------------
# WHAT EACH STEP DOES
# ----------------------------------------------------------------------------
#
# [healthcheck]  python3 scripts/health_check.py
#   Validates directory structure, schema files, and JSON data contracts.
#   Safe to run any time; does not change any files.
#   Run this when you're unsure something is wired up correctly.
#
# [generate_ui]  python3 src/api/generate_ui_data.py
#   Reads source CSVs (gold schema under schema/, shea CSVs under
#   frontend/project/shea/data/) and writes processed JSON payloads used
#   by the frontend simulators:
#       data/frontend/gold_supply_chain_ui.json
#       data/frontend/shea_supply_chain_ui.json
#       data/frontend/gold_value_chain_ui.json
#       data/frontend/shea_value_chain_ui.json
#   Run this when you have edited any of those source CSVs.
#   Requires: pandas  (pip install pandas)
#
# [viewable]     bash scripts/all2html.py
#   Walks the whole repo tree and converts every .csv, .json, .yaml/.yml
#   to an HTML table viewer under viewable/<same-relative-path>.html
#   e.g.  frontend/project/shea/data/shea_phase_metrics.csv
#         → viewable/frontend/project/shea/data/shea_phase_metrics.html
#   The green HTML badges in the data catalog (frontend/csv/index.html) resolve
#   to /viewable/<path> — so re-run this after any rename, move, or new file.
#   The same .html is also copied into frontend/project/.../data/schema/ next to
#   the CSVs so /frontend/project/gold/data/schema/*.html and shea/.../schema/*.html
#   (footer links) do not 404.
#   Note: also converts mkdocs.yml → viewable/mkdocs.html (harmless artifact;
#   cleaned up automatically by CLEAN_ARTIFACT below).
#
# [mkdocs]       mkdocs build
#   Converts docs/*.md (and embedded HTML like docs/Reports/index.html) into
#   the static wiki under site/.
#   Config: mkdocs.yml (repo root).
#   Theme overrides: overrides/partials/header.html, nav.html
#   Styles:          docs/stylesheets/mkdocs-site.css
#   Run this after any change under docs/, mkdocs.yml, or overrides/.
#
# [restart_server] (optional, off by default)
#   Kills any running python http.server on port 8000 and restarts it.
#   Also notes the mkdocs serve command if you want the live wiki preview.
#   Only useful when running a local dev server.
#
# ----------------------------------------------------------------------------
# WHEN TO RUN WHAT
# ----------------------------------------------------------------------------
#
#  Scenario                                         | Steps needed
# --------------------------------------------------|-----------------------------
#  Added / renamed / moved a CSV, JSON, or YAML     | viewable
#  Edited a doc under docs/ or mkdocs.yml           | mkdocs
#  Edited gold/shea source CSVs for the simulators  | generate_ui  →  viewable
#  Edited a frontend/ HTML page                     | nothing (static; edit live)
#  Moved source files (e.g. shea data to shea/data) | viewable  +  fix hrefs
#  Full rebuild after a big restructure             | generate_ui + viewable + mkdocs
#  Not sure if anything is broken                   | healthcheck
#
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# ── toggles (override via environment variable) ──────────────────────────────
: "${RUN_HEALTHCHECK:=0}"     # 1 = run health_check.py before anything else
: "${RUN_GENERATE_UI:=0}"     # 1 = regenerate processed UI JSON from CSVs
: "${RUN_VIEWABLE:=1}"        # 1 = regenerate viewable/ HTML viewers
: "${RUN_MKDOCS:=1}"          # 1 = mkdocs build → site/
: "${RUN_RESTART_SERVER:=0}"  # 1 = restart local http.server on port 8000
: "${CLEAN_ARTIFACT:=1}"      # 1 = remove viewable/mkdocs.html after all2html

# ── helpers ───────────────────────────────────────────────────────────────────
sep() { echo; echo "────────────────────────────────────────"; }
skip() { echo "(skip) $1  —  set $2=1 to enable"; }

echo
echo "=== rebuild-site.sh ==="
echo "    repo:             $REPO_ROOT"
echo "    RUN_HEALTHCHECK:  $RUN_HEALTHCHECK"
echo "    RUN_GENERATE_UI:  $RUN_GENERATE_UI"
echo "    RUN_VIEWABLE:     $RUN_VIEWABLE"
echo "    RUN_MKDOCS:       $RUN_MKDOCS"
echo "    RUN_RESTART_SERVER: $RUN_RESTART_SERVER"

# ── healthcheck ───────────────────────────────────────────────────────────────
sep
if (( RUN_HEALTHCHECK )); then
  echo "==> Health check"
  python3 scripts/health_check.py
else
  skip "health check" "RUN_HEALTHCHECK"
fi

# ── generate UI JSON ──────────────────────────────────────────────────────────
sep
if (( RUN_GENERATE_UI )); then
  echo "==> Generate UI JSON from CSVs  (src/api/generate_ui_data.py)"
  python3 src/api/generate_ui_data.py
else
  skip "generate_ui_data.py" "RUN_GENERATE_UI"
fi

# ── viewable HTML viewers ─────────────────────────────────────────────────────
sep
if (( RUN_VIEWABLE )); then
  echo "==> Regenerate viewable/  (scripts/all2html.py)"
  bash "$SCRIPT_DIR/all2html.py"
  if (( CLEAN_ARTIFACT )) && [[ -f viewable/mkdocs.html ]]; then
    rm -f viewable/mkdocs.html
    echo "    cleaned up: viewable/mkdocs.html"
  fi
else
  skip "all2html" "RUN_VIEWABLE"
fi

# ── mkdocs wiki ───────────────────────────────────────────────────────────────
sep
if (( RUN_MKDOCS )); then
  echo "==> MkDocs build  (docs/ → site/)"
  mkdocs build
else
  skip "mkdocs build" "RUN_MKDOCS"
fi

# ── optional: restart local dev server ───────────────────────────────────────
sep
if (( RUN_RESTART_SERVER )); then
  echo "==> Restarting http.server on port 8000"
  pkill -f "http.server 8000" 2>/dev/null || true
  nohup python3 -m http.server 8000 > /tmp/tv-http.log 2>&1 &
  echo "    started (pid $!); log: /tmp/tv-http.log"
  echo
  echo "    For the MkDocs live wiki preview (port 8001), run separately:"
  echo "      bash scripts/RUN_MKWIKI"
else
  skip "server restart" "RUN_RESTART_SERVER"
fi

sep
echo
echo "Done."
