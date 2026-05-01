# AI prompt: generate `docnav_manifest.tsv` for DocNav / TiddlyWiki index

This document describes the manifest schema and tagging rules for DocNav. The **canonical implementation** is `docnav_manifest_from_entries.py`: run that script after `entries_for_ai.txt` is regenerated so output stays consistent.

Use this file when you want an AI (or a human) to understand how rows are built **without** reading Python. For routine updates, you do **not** need to ask an AI to write the TSV: run `sh docnav/REFRESH`.

---

## Inputs

1. **`entries_for_ai.txt`**, produced by `docnav_extract_excerpts.py`. Each file under `docnav/` becomes one block:

```
ENTRY_START
relative_path: Repos/example/note.md
extension: .md
excerpt:
<first ~800 chars of cleaned text, or OPAQUE …>
ENTRY_END
```

2. Parse **only** blocks that contain both `relative_path:` and `ENTRY_END`. Read `excerpt:` from the line after `excerpt:` through the end of the body before `ENTRY_END`.

---

## Output: `docnav_manifest.tsv`

- Encoding: UTF-8, Unix newlines.
- One header row, then one row per parsed entry.
- Delimiter: tab (`\t`).
- Do **not** put raw tabs, newlines, or double quotes inside cells (normalize spaces; replace `"` with `'` if needed).

### Columns (in order)

| Column | Meaning |
|--------|---------|
| `relative_path` | Path relative to `docnav/` (forward slashes). |
| `title` | Short catalog title (see Title rules). |
| `tags` | Space-separated tokens (see Tags rules). |
| `summary` | One short sentence or clipped line from excerpt (see Summary rules). |
| `notes` | Optional flags (see Notes rules). |

Sort rows by `relative_path` case-insensitively.

---

## Title rules

- Default: `docnav: <basename>` (e.g. `docnav: note.md`).
- If the same basename appears more than once under different folders, disambiguate: `docnav: <parent>/<basename>` using the last two path segments of the parent directory (implementation caps length at 80 characters).

---

## Format tag (`fmt/*`)

Derive from file extension (lowercase):

| Extension(s) | Tag |
|--------------|-----|
| `.md`, `.txt`, `.tex`, `.ttl` | `fmt/md` |
| `.html`, `.htm` | `fmt/html` |
| `.pdf` | `fmt/pdf` |
| `.png`, `.gif` | `fmt/png` |
| `.jpg`, `.jpeg`, `.jpe`, `.webp` | `fmt/jpeg` |
| `.svg` | `fmt/svg` |
| `.css` | `fmt/css` |
| `.js` | `fmt/js` |
| `.yaml`, `.yml` | `fmt/yaml` |
| `.json` | `fmt/json` |
| `.csv`, `.tsv` | `fmt/csv` |
| `.xlsx` | `fmt/xlsx` |
| `.psd`, `.docx`, `.blend`, `.blend1` | `fmt/binary-other` |
| anything else | `fmt/binary-other` |

---

## Topic tag (`topic/*`)

Score each topic by counting keyword hits (case-insensitive) in **`relative_path + " " + excerpt`**. Keywords per topic:

| Tag | Keywords (each occurrence counts) |
|-----|----------------------------------|
| `topic/tvpci` | tvpci, true value pricing, convergence index, radar chart |
| `topic/tholonic-ndc` | tholonic, n-d-c, definition, contribution, negotiation, d vs c, d/c |
| `topic/pdi` | pdi, phase discovery, ndc metrics, value chain phase |
| `topic/supply-chain` | supply chain, comex, vaulting, bullion, refining, custody, phase 0, phase 1 |
| `topic/value-chain` | value chain, margin, profit capture |
| `topic/blue-carbon` | blue carbon, mangrove, coastal, ctvf |
| `topic/water` | water, replenish, utility, ocwd, recycled water |
| `topic/game-theory` | game theory, gametheory, slider, prisoner |
| `topic/finance-esg` | esg, bond, rating, sovereign, investor report, sustainability-linked |
| `topic/ai-notes` | concept_notes, document_notes, /ai_notes/ |
| `topic/research-general` | research/, methodology, hypothesis, literature |

Pick the topic with the **highest** score. If tied, break ties using the **table order above** (tvpci first, … research-general last). If all scores are zero, use `topic/generic-doc`.

**Path boost:** any file whose normalized path starts with `repos/intra/pdi/` receives **`topic/pdi`** as an **additional** topic tag before the scored topic (deduplicated). That keeps PDI-folder exports visible when the catalog facet filter `topic/pdi` is active even if the excerpt scores higher on `topic/supply-chain`.

**Forced generic:** if basename is exactly `AI_PROMPT_DOCNAV_MANIFEST.md`, `entries_for_ai.txt`, `docnav_manifest.tsv`, or `index.html`, set topic to `topic/generic-doc` (skip keyword scoring).

---

## Phase tags (`phase/*`)

Inspect path + excerpt (lower case). Add `phase/<n>` for `n` in `0`–`7` when phase **n** is mentioned in typical forms (e.g. `phase 3`, `phase-3`). Also add `phase/6` if vaulting or “phase 6” appears; add `phase/7` if both “exchange” and “comex” appear. Deduplicate and sort.

---

## Kind tags (`kind/*`)

Path-based hints (lower-case path):

| Condition | Tag |
|-----------|-----|
| Under `sites/` and path contains `_files/` OR `sites/…html` saved page | `kind/saved-site` |
| Path suggests template / `pdi_template` | `kind/template` |
| Image (`fmt/png` or `fmt/jpeg`) and not saved-site | `kind/archive-image` |
| `fmt/js` or `fmt/css` under `/_files/` | `kind/source-code-bundle` |

Deduplicate and sort.

---

## Meta tag

If excerpt is empty or starts with `opaque` (case-insensitive), append **`meta/low-confidence`** to tags (once).

---

## Tag column assembly

Build tags in this order, **deduplicating** while preserving first occurrence:

1. **`topic/pdi`** first when path is under `Repos/intra/PDI/` (see Path boost above), then the scored primary `topic/*`
2. `fmt/*`
3. all `phase/*`
4. all `kind/*`
5. `meta/low-confidence` if applicable

Join with a single space.

---

## Summary rules

- Collapse whitespace in excerpt.
- If excerpt is empty or starts with `opaque`: use **`Opaque or unreadable; manual review.`**
- Else prefer the first sentence ending in `.` `!` or `?` within roughly the first 240 characters; otherwise clip at ~240 chars on a word boundary and add `…` if truncated.

---

## Notes column

Space-separated flags:

- `needs_manual_review` if excerpt empty or opaque.
- `saved_site_bundle` if path under `sites/` and contains `_files/`.

Use empty string if none apply.

---

## Optional step 2: TiddlyWiki JSON

After `docnav_manifest.tsv` exists, generate import JSON:

```bash
python3 scripts/docnav_manifest_to_tiddlywiki_json.py
```

Optional base URL for links:

```bash
DOCNAV_PUBLIC_BASE_URL=https://example.com/docnav/ python3 scripts/docnav_manifest_to_tiddlywiki_json.py
```

Default output: `docnav/docnav_tiddlers_import.json`.

---

## Routine automation (recommended)

From repository root:

```bash
sh docnav/REFRESH
```

That regenerates `entries_for_ai.txt`, `docnav_manifest.tsv`, and `catalog.json`. Run `python3 scripts/docnav_manifest_to_tiddlywiki_json.py` separately when you need the TiddlyWiki bundle updated.
