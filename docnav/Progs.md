# Programming manual (`docnav/`)

Executable scripts in this folder. Invocation details live in script headers; this file describes what each program is for.

## `CSV_REFRESH`

Thin shell wrapper run from the **repository root**. Calls `docnav/docnav_build_csv_catalog_json.py` to regenerate **`docnav/csv_catalog.json`** from CSV files discovered under `frontend/project/`.

**Depends on:** `sh`, `python3`, and the Python helper (not executable).

## `REFRESH`

Thin shell wrapper run from the **repository root**. Regenerates the DocNav excerpt dump, manifest TSV, and catalog JSON by running, in order:

1. `docnav/docnav_extract_excerpts.py` (stdout redirected to `docnav/entries_for_ai.txt`)
2. `docnav/docnav_manifest_from_entries.py`
3. `docnav/docnav_build_catalog_json.py`

Ends with a line count summary.

**Depends on:** `sh`, `python3`, and those helpers (not executable).

## `check_docnav_md_images.py`

Validates **local image targets** referenced from Markdown under `docnav/` (`![](...)`, optional titles, and `<img src="...">`). Skips remote URLs and fragment-only links. Can emit JSON for tooling.

**Depends on:** Python 3 only (stdlib).
