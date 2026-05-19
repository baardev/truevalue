---
name: content-sync
description: >- 
  Propagate a model or data change (TVPCI parameter update, new supply chain,
  simulation engine edit) across all affected documents, dashboards, and
  generated artifacts. Appends a summary entry to docs/content-sync-log.json.
  Use when the user says TVPCI changed, a supply chain was added or renamed,
  an algorithm was updated, or asks to sync documents after a data/model change.
---

# Content Sync

This skill walks the agent through propagating a change to the model or data
layer into every affected document, dashboard, and generated artifact in the
project, then records what was touched.

---

## Step 0: Identify the change type

Ask the user (or infer from context) which category applies:

| ID | Change type | Examples |
|----|------------|---------|
| `tvpci` | TVPCI formula or parameter update | New weight, revised formula, phase re-labelling |
| `new-chain` | New supply chain project added | Adding "shea-west-africa", "lithium", etc. |
| `engine` | Simulation engine change | Edit to `phi_engine.py`, `ln2_engine.py`, etc. |
| `schema` | Schema field added, renamed, or removed | CSV schema change under `schema/` |
| `paper` | Standalone paper revision only | No cross-project propagation needed |

Capture: the change type ID, a one-line human description of the change, and
the date (ISO 8601, e.g. `2026-05-10`).

---

## Step 1: Build the work list from the registry

Read `docs/document-registry.yaml`. Filter entries whose `tags` array contains
the concept(s) that changed (e.g. `tvpci`, `tvpci-r`, `recycling`), and whose
`status` is `active` or `provisional` (skip `deprecated`). That filtered list
is the work list for this run.

For each entry in the work list, also include any paths listed under `derived`
that may need rebuilding (TEX/PDF for papers, JSON for schemas).

The hardcoded impact tables below remain as a reference and a fallback when
the registry is unavailable or a new document has not yet been registered.
Always prefer the registry query over the hardcoded tables.

---

## Step 1b: Impact map (fallback / reference)

Use these tables only if the registry cannot be read or a file is not yet
registered. Only include rows matching the change type(s) from Step 0.

### `tvpci` impact

Work through document tiers in order. Do not skip to a lower tier until the
tier above it is complete and verified.

#### Tier 1: Primary TVPCI specification documents (update first)

These are the hand-authored source-of-truth documents. Any TVPCI change must
be reflected here before it propagates anywhere else.

| File | Action |
|------|--------|
| `docnav/Repos/intra/TVPCI/TVPCI_FOUNDATION.md` | Update the affected formula, constant, weight, or phase definition |
| `docnav/Repos/intra/TVPCI/TVPCI_FOUNDATION_INTRO.md` | Update any introductory description of the changed element |
| `docnav/Repos/intra/TVPCI/TVPCI_FOUNDATION_SIMPLE.md` | Update the simplified version to match |
| `docnav/Repos/intra/TVPCI/TVPCI_EXPLAINED_MATH.md` | Update the mathematical walkthrough if the formula or derivation changed |
| `docnav/Repos/intra/TVPCI/TVPCI_TRUE_VALUE_PRICING_CONVERGENCE_INDEX.md` | Update the overview description |

#### Tier 2: Research papers

Search each `.md` and `.tex` for the changed parameter name or formula.
Update only sections that contain the specific changed value.

| File | Action |
|------|--------|
| `docnav/Research/papers/2_supply-chain-transparency-tvpci.md` | Update changed parameter values, formulas, or phase descriptions |
| `docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.tex` | Mirror same edits; rebuild PDF via `research-paper-latex` skill |
| `docnav/Research/papers/3_minimal-recursive-triadic-framework/3_minimal-recursive-triadic-framework.tex` | Check for TVPCI references; update if present; rebuild PDF |
| `docnav/Research/papers/4_game-theoretic-triadic-balance/4_game-theoretic-triadic-balance.tex` | Same check-and-update pattern |
| `docnav/Research/papers/5_tholonic-twistor-connection/5_tholonic-twistor-connection.tex` | Same check-and-update pattern |
| `docnav/Research/papers/6_qualitative-nature-integers-triadic-roles/6_qualitative-nature-integers-triadic-roles.tex` | Same check-and-update pattern |

#### Tier 3: AI concept notes and document notes

These are derived summaries under `docnav/.ai_notes/`. Do not hand-edit them.
Instead, ask the AI to regenerate the relevant note(s) from the updated Tier 1
source. The notes most likely to need regeneration after a TVPCI change are:

- `docnav/.ai_notes/concept_notes/tvpci.md`
- `docnav/.ai_notes/concept_notes/pricing_convergence.md`
- `docnav/.ai_notes/document_notes/tvpci_foundation.md`
- `docnav/.ai_notes/document_notes/tvpci_explained_math.md`
- `docnav/.ai_notes/document_notes/tvpci_specification.md`

To regenerate a note: read the corresponding Tier 1 source file, then rewrite
the note to match its current frontmatter schema and section structure.

#### Tier 4: PDI status files (methodology change only)

Update these only when the TVPCI change affects how PDI itself is structured
(e.g. a phase is renamed or a required field is added). Skip for parameter-only
changes such as weight adjustments.

| File | Action |
|------|--------|
| `frontend/project/aubeb/data/PDI_AUBEB_STATUS.md` | Update phase names or field requirements if affected |
| `frontend/project/water_newwater/data/PDI_water_newwater_STATUS.md` | Same |
| `frontend/project/water_ocwd/data/PDI_water_ocwd_STATUS.md` | Same |

#### Tier 5: Frontend dashboards and generated JSON

| File | Action |
|------|--------|
| `frontend/project/gold/supply_chain/scenarios.json` | Update TVPCI values, weights, or phase labels |
| `frontend/project/gold/supply_chain/index.html` | Update any hard-coded TVPCI labels, formula displays, or phase copy |
| `frontend/project/gold/supply_chain/dashboard.html` | Same |
| `src/api/generate_frontend_data.py` | Update TVPCI constants or phase definitions if coded here |
| `src/api/generate_ui_data.py` | Same |
| Regenerate JSON | Run `python3 src/api/generate_frontend_data.py && python3 src/api/generate_ui_data.py` from repo root after code edits |

### `new-chain` impact (gold-only scope for now)

| File | Action |
|------|--------|
| `frontend/project/gold/index.html` | Add entry for new chain if it is a sub-project of gold |
| `site-index.json` | Add new project entry; use `add-homepage-section` skill for the homepage card |
| `index.html` | Use `add-homepage-section` skill to add the hub section or project card |
| `docnav/Research/papers/2_supply-chain-transparency-tvpci.md` | Add new chain to any supply-chain inventory list or comparison table |
| `docnav/Research/papers/2_supply-chain-transparency-tvpci/2_supply-chain-transparency-tvpci.tex` | Mirror the addition; rebuild PDF |
| New frontend scaffold | Create `frontend/project/<name>/index.html` and `supply_chain/` subdirectory following the gold pattern |

### `engine` impact

| File | Action |
|------|--------|
| Affected engine file (`src/simulation/<engine>.py`) | This is the change source; confirm it is already edited |
| `frontend/project/gold/supply_chain/<engine>_dashboard.html` | Check for hard-coded constants that must match the engine |
| `src/api/generate_frontend_data.py` | Update if it imports or references the changed engine |
| Regenerate JSON | Run generate scripts after code edits (see `tvpci` row above) |
| Affected research papers | Search papers for the engine name or derived constants; update and rebuild PDF as needed |

### `schema` impact

| File | Action |
|------|--------|
| `schema/<changed>.csv` | This is the change source; confirm it is already edited |
| `src/api/generate_frontend_data.py` | Update field references |
| `src/api/generate_ui_data.py` | Update field references |
| `frontend/project/gold/data/schema/` | Copy or regenerate the updated CSV if it lives here |
| Regenerate JSON | Run generate scripts after code edits |

---

## Step 2: Execute the work list

For each file in the work list:

1. Read the current file.
2. Identify the exact section(s) to change (search for the parameter name, formula,
   chain name, or engine constant).
3. Make the targeted edit. Do not rewrite sections that are not affected.
4. For any `.tex` file that was edited: invoke the `research-paper-latex` skill
   to rebuild the PDF.
5. After all code or data edits, run the generate scripts if they are in the
   work list.

Do not mark a file "done" until the edit is verified (re-read the relevant
section and confirm the new value appears).

---

## Step 3: Update the sync log

Append one entry to `docs/content-sync-log.json`. The file is a JSON array;
create it as `[]` if it does not exist.

Entry schema:

```json
{
  "date": "YYYY-MM-DD",
  "change_type": "<id from Step 0>",
  "description": "<one-line human summary of the change>",
  "files_updated": [
    "relative/path/to/file1",
    "relative/path/to/file2"
  ],
  "pdfs_rebuilt": [
    "relative/path/to/paper.pdf"
  ],
  "json_regenerated": true,
  "notes": "<optional: anything the next person should know>"
}
```

Use relative paths from the repo root. Set `json_regenerated` to `false` if
the generate scripts were not run. Leave `notes` as `""` if nothing unusual
happened.

---

## Step 4: Report to the user

Summarize:

- How many files were updated.
- Which PDFs were rebuilt (or skipped because no TeX change was needed).
- Whether the generate scripts ran successfully.
- The log entry that was appended.
- Any files in the work list that were **skipped** (not changed) and why.

---

## Notes and constraints

- Never rewrite whole documents to "clean them up" as part of a sync run.
  Scope every edit to the changed value or section only.
- If a paper's `.md` and `.tex` are both in the work list, edit the `.md`
  first, then sync the same change into `.tex` manually. Do not re-run Pandoc
  just for a parameter update; that would overwrite any LaTeX-specific
  formatting.
- If the change type is ambiguous (e.g. TVPCI formula change that also
  requires a new schema field), treat it as multiple change types and merge
  the work lists before executing.
- The log at `docs/content-sync-log.json` is the audit trail. Keep every
  entry; do not delete old entries.
