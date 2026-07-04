---
name: export-project-pdfs
description: Render every page in a project's subtree into PDF via headless Chrome, then merge just that project's pages into one combined PDF for that project. Use when the user asks to export a project as PDF, snapshot every page of a project, or build a single combined PDF book for one (or more) specific projects. Each project gets its own combined PDF; this never merges pages across different projects.
---

# Export a Project's Full Page Tree to One Combined PDF

For each requested project, walks its folder under `frontend/project/<slug>/`,
renders every page in that project's subtree to its own PDF via headless
Chrome, then merges only that project's pages into one combined PDF. Each
project gets its own combined PDF; pages from different projects are never
merged together.

## Run it

```bash
python3 scripts/export_project_pdfs.py --projects gold
```

Omit `--projects` to export every project in `frontend/site-index.json`
(each one producing its own combined PDF, still separate from each other).
Multiple ids can be comma-separated: `--projects gold,west_african_shea`.

Output lands in `docs/pdf_exports/<slug>/`: one PDF per page (e.g.
`01_hub.pdf`, `02_supply_chain.pdf`, `03_supply_chain_dashboard.pdf`) plus
`<slug>_complete.pdf`, the combined PDF for that project. This mirrors the
existing hand-built `docs/pdf_exports/svb_analysis/` example.

Requires `all` sandbox permissions (Chrome needs `--no-sandbox` to run
headless in this environment).

## Options

| Flag | Purpose |
|---|---|
| `--projects gold,west_african_shea` | Export only specific project ids instead of all 31 |
| `--out <dir>` | Change the output root (each project still gets its own `<dir>/<slug>/` subfolder) |
| `--base-url <url>` | Point at an already-running server instead of starting a temporary one |

## How it works

1. Reads the `projects` array from `frontend/site-index.json` to resolve
   which project id(s) to run.
2. For each project, walks `frontend/project/<slug>/` with `rglob("*.html")`,
   skipping anything under a `data/` directory (schema/CSV table viewers,
   not real site pages). Pages are ordered: project root first, then
   `supply_chain/`, then `value_chain/`, then any other subfolders
   (alphabetical); within a folder, `index.html` / `dashboard.html` /
   `project_context.html` / `system_lifecycle.html` /
   `recycling_analysis.html` / `what_if_simulator.html` sort first if
   present, then everything else alphabetically.
3. If `--base-url` is not already serving the site, starts a temporary
   instance of `scripts/serve.py --http-only` on a free port and tears it
   down after.
4. Renders each page with `google-chrome-stable --headless --print-to-pdf`.
5. Merges that project's own pages (only) with `pypdf.PdfWriter` into
   `<slug>_complete.pdf`.

## Notes

- Projects listed in `deploy/protected-paths.json` (currently AUBEB and
  Senegal Agroforestry) are behind HTTP Basic Auth. The script reads
  `deploy/auth.env` (gitignored, see `deploy/auth.env.example`) and embeds
  the credentials in the request URL for pages under those prefixes. If
  `auth.env` is missing, those pages will only contain the browser's
  auth-challenge stub, not real content, and the script prints a warning.
- Large multi-subproject hubs (e.g. `danube`, with dozens of nested
  natural/human/paired pages) produce a correspondingly large combined PDF;
  this is expected, not a bug.
- Chrome must render against a live HTTP server (not `file://`) so relative
  asset and JSON fetches resolve correctly.
- If `google-chrome-stable` is unavailable, install Chrome or Chromium; the
  script also checks for `google-chrome`, `chromium`, and `chromium-browser`.

## Files touched

| File | Role |
|---|---|
| `scripts/export_project_pdfs.py` | Discover, render, and per-project merge script (this skill's only file) |
| `docs/pdf_exports/<slug>/` | Output per project: per-page PDFs + `<slug>_complete.pdf` |
