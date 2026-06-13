# Programming manual (`scripts/`)

Executable scripts in this folder. Usage strings are in headers or `--help`; this file describes roles and dependencies.

## `all2html.py`

Walks the repo (with pruning for `.git`, `node_modules`, `site`, venvs, and existing `viewable/` output) and emits **HTML table viewers** for `.csv`, `.json`, `.yaml`, `.yml` under **`viewable/`**, mirroring relative paths. Delegates CSV to `csv2html.py` and JSON/YAML to `jsonyaml2html.py` (same directory; not necessarily executable).

**Depends on:** `bash`, `python3`, those two converters.

## `cognee_agent.py`

Minimal **HTTP client** that posts a fixed graph-completion style query to the configured **Cognee Cloud** tenant URL using `COGNEE_API_KEY`. Prints HTTP status and response body.

**Depends on:** Python with `requests`.

## `convert_inbox_sources.py`

Batch **document ingestion** helper: turns inbox files (DOC/DOCX/XLS/XLSX/HTML) into curated Markdown and CSV under `frontend/docs/Research/` for downstream tooling (for example AnythingLLM).

**Depends on:** Python 3; LibreOffice optional for legacy Office formats.

## `crawl_check_links.py`

**Breadth-first crawler** for a static site: follows same-origin links from HTML, collects `href` / `src`, optionally checks targets with HTTP GET. Used for automated link audits.

**Depends on:** Python 3 (stdlib).

## `crawl.sh`

Shell-driven **static site link audit** with colored console output. Defaults to a local base URL; optional `--all` extends checks beyond same-origin. Wraps curl/Python/grep per header comments.

**Depends on:** `bash`, `curl`, `python3`, `grep`.

## `csv2html.py`

Converts a single **CSV file** to a standalone themed HTML table page (stdin or path). Used heavily by `all2html.py`.

**Depends on:** Python 3 (stdlib).

## `md2html.sh`

Converts one **Markdown** file to standalone HTML via Pandoc with MathJax, TOC, syntax highlighting, embedded resources, and local image resolution rules documented in the script.

**Depends on:** `bash`, `pandoc`, network once if MathJax bundling requires it.

## `rebuild-site.sh`

**Orchestrator** for repo maintenance: optional health check, optional `generate_ui_data.py`, `all2html.py` pass, optional MkDocs build. Flags and step descriptions are inside the script.

**Depends on:** `bash`, `python3`, Pandoc/MkDocs stack when those steps enabled.

## `research_paper_pdflatex.sh`

Runs **two pdflatex passes** on a paper directory laid out as `<paper-dir>/<basename>.tex` (research papers under `docnav/Research/papers/`).

**Depends on:** `bash`, `pdflatex`, paper-local LaTeX assets.

## `serve.py`

**Static file server** for the repo root with optional HTTP redirect to HTTPS, auto-generated self-signed cert under `.certs`, or HTTP-only / HTTPS-only modes. Enforces HTTP Basic Auth on URL prefixes listed in `deploy/protected-paths.json` when `TV_AUTH_USER` and `TV_AUTH_PASSWORD` are set in `deploy/auth.env` (or `.env`).

**Depends on:** Python 3 (stdlib).

## `restart_server`

**Restart helper** for the static site. If the `tv-web` systemd unit is active, runs `systemctl restart tv-web`. Otherwise stops any running `serve.py` or legacy `http.server` on port 8000 and starts `serve.py --http-only`. Use after editing `deploy/auth.env` or `deploy/protected-paths.json`.

**Depends on:** `bash`, `python3`, optional `systemctl` / `sudo`.

## `START_SERVER`

Thin wrapper that runs `restart_server` from the repo root (also starts MkDocs helper when present).

**Depends on:** `bash`, `restart_server`.

## `tag_docnav_from_frontmatter.sh`

**Generated batch script** of `tmsu tag` commands for DocNav paths (state reflects the snapshot when it was generated). Applies TMSU tags from a prior scan of front matter keywords; requires a TMSU database rooted as expected by the paths inside.

**Depends on:** `bash`, TMSU (`tmsu`).
