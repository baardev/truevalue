#!/usr/bin/env bash
# =============================================================================
# crawl.sh  —  Crawl every link in a static site and report broken URLs
# =============================================================================
#
# Usage:
#   ./scripts/crawl.sh                               # default: http://localhost:8000
#   ./scripts/crawl.sh http://localhost:8001         # custom base URL
#   ./scripts/crawl.sh http://localhost:8000 --all   # include external links
#
# Output:
#   Only prints lines where the response is NOT 2xx/3xx.
#   Each line: status, method, failed URL, referring page.
#   Exits 1 if any broken links found, 0 if clean.
#
# Requirements: curl, python3, grep
# =============================================================================

set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
SAME_ORIGIN_ONLY=true
[[ "${2:-}" == "--all" ]] && SAME_ORIGIN_ONLY=false

TIMEOUT=10
MAX_PAGES=600
UA="tv-crawl/1.0 (link audit)"

BASE_URL="${BASE_URL%/}"
BASE_HOST="$(python3 -c "from urllib.parse import urlparse; print(urlparse('$BASE_URL').netloc)")"

RED='\033[0;31m'
GREY='\033[0;90m'
GREEN='\033[0;32m'
RESET='\033[0m'

# ── Extract raw href/src values from HTML (stdin → stdout) ────────────────────
# Drops JS template artifacts (anything containing a single quote) and
# anything obviously not a URL path.
extract_links() {
  grep -oiP '(?:href|src)="[^"]*"' \
    | grep -ioP '(?<=")[^"]+' \
    | grep -v "^#" \
    | grep -v "'"
}

# ── Resolve all links for one page in a single Python call ───────────────────
# Reads raw relative URLs from stdin, writes normalized absolute URLs to stdout.
resolve_links() {
  local base="$1"
  python3 -c "
import sys
from urllib.parse import urljoin, urlparse, urlunparse, quote
from posixpath import normpath
from html import unescape

base, base_host, same_origin = sys.argv[1], sys.argv[2], sys.argv[3] == 'true'
SKIP = ('javascript:', 'mailto:', 'tel:', 'data:', 'about:')

for line in sys.stdin:
    rel = unescape(line.strip())   # decode &amp; &apos; etc.
    if not rel or rel.startswith('#') or any(rel.startswith(p) for p in SKIP):
        continue
    if len(rel) > 2000:
        continue
    try:
        u = urlparse(urljoin(base, rel))
    except Exception:
        continue
    if u.scheme not in ('http', 'https'):
        continue
    if same_origin and u.netloc != base_host:
        continue
    path = normpath(u.path) if u.path else '/'
    # Re-encode path so spaces/special chars are valid in the URL
    path = quote(path, safe='/:@!$&()*+,;=')
    print(urlunparse((u.scheme, u.netloc, path, u.params, u.query, '')))
" "$base" "$BASE_HOST" "$SAME_ORIGIN_ONLY"
}

# ── Check a URL with curl ─────────────────────────────────────────────────────
check_url() {
  local url="$1" from="${2:-(start)}"
  local code method

  code="$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time "$TIMEOUT" -H "User-Agent: $UA" -L --head "$url" 2>/dev/null || echo "ERR")"

  if [[ "$code" == "405" || "$code" == "501" || "$code" == "000" ]]; then
    code="$(curl -s -o /dev/null -w "%{http_code}" \
      --max-time "$TIMEOUT" -H "User-Agent: $UA" -L "$url" 2>/dev/null || echo "ERR")"
    method="GET"
  else
    method="HEAD"
  fi

  [[ "$code" == "000" ]] && code="ERR"
  total_checked=$(( total_checked + 1 ))

  if [[ ! "$code" =~ ^[23] ]]; then
    printf "  ${RED}%3s  %-4s  %-60s  %s${RESET}\n" "$code" "$method" "$url" "$from"
    broken+=( "$code  $url  (from: $from)" )
  fi
}

# ── State ─────────────────────────────────────────────────────────────────────
declare -A seen=()
declare -A from_page=()
declare -a queue=()
declare -a broken=()
queue_idx=0
total_checked=0
pages_crawled=0

# ── Bootstrap ─────────────────────────────────────────────────────────────────
START_URL="${BASE_URL}/index.html"
queue=("$START_URL")
seen["$START_URL"]=1
from_page["$START_URL"]="(start)"

echo ""
echo "  Base  : $BASE_URL"
echo "  Start : $START_URL"
printf "  ${GREY}%-3s  %-4s  %-60s  %s${RESET}\n" "STS" "METH" "FAILED URL" "FROM PAGE"
echo "  $(printf '%.0s-' {1..130})"

# ── BFS crawl ─────────────────────────────────────────────────────────────────
while [[ $queue_idx -lt ${#queue[@]} && $pages_crawled -lt $MAX_PAGES ]]; do
  current_url="${queue[$queue_idx]}"
  queue_idx=$(( queue_idx + 1 ))
  pages_crawled=$(( pages_crawled + 1 ))

  printf "\r  [%d crawled / %d queued]  " \
    "$pages_crawled" "$(( ${#queue[@]} - queue_idx ))" >&2

  check_url "$current_url" "${from_page[$current_url]:-(crawl)}"

  html="$(curl -s --max-time "$TIMEOUT" -H "User-Agent: $UA" -L "$current_url" 2>/dev/null || true)"
  [[ -z "$html" ]] && continue

  # Resolve all links for this page in one Python call
  while IFS= read -r abs; do
    [[ -z "$abs" ]] && continue

    [[ -n "${seen[$abs]+_}" ]] && continue
    seen["$abs"]=1
    from_page["$abs"]="$current_url"

    lower="${abs,,}"
    lower="${lower%%\?*}"
    if [[ "$lower" =~ \.(html|htm)$ || "$lower" =~ /$ ]]; then
      queue+=("$abs")
    else
      check_url "$abs" "$current_url"
    fi
  done < <(echo "$html" | extract_links | resolve_links "$current_url")
done

printf "\r%80s\r" "" >&2

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "  $(printf '%.0s-' {1..130})"
printf "  Pages crawled : %d\n" "$pages_crawled"
printf "  URLs checked  : %d\n" "$total_checked"
printf "  Broken        : %d\n" "${#broken[@]}"

if [[ ${#broken[@]} -gt 0 ]]; then
  exit 1
fi

  echo -e "  ${GREEN}All links OK.${RESET}"
echo ""
exit 0
