# TrueValue Analytics: Project Roadmap

This file is the canonical tracker for planned and in-progress work across the
platform. Update it whenever a task is completed or a new task is identified.
Do not use it as a change log (that role belongs to `docs/content-sync-log.json`).

Last updated: 2026-05-10

---

## Legend

| Symbol | Meaning |
|--------|---------|
| [x] | Done |
| [ ] | Not started |
| [~] | In progress / partial |

---

## 1. Phase Discovery Instrument (PDI) — per-project status

The PDI must be completed for every project before TVPCI scoring is meaningful.
Gold (primary and recycling) is the reference implementation.

| Project | PDI complete | Schema CSVs | TVPCI scored | Notes |
|---------|-------------|-------------|--------------|-------|
| gold (primary) | [x] | [x] | [~] | Reference implementation |
| gold (recycling) | [x] | [ ] | [ ] | PDI_gold_recycling_2026.yaml created; schema not yet built |
| shea | [ ] | [x] | [ ] | Rich source data present; PDI not yet run |
| danube | [~] | [x] | [ ] | 13 PDI files present; review for v1.1 template conformance |
| aubeb | [~] | [ ] | [ ] | 1 PDI file present; review for v1.1 template conformance |
| water_newwater | [~] | [~] | [ ] | 1 PDI, 1 schema CSV; incomplete |
| water_ocwd | [~] | [~] | [ ] | 1 PDI, 1 schema CSV; incomplete |
| lighter | [ ] | [~] | [ ] | 4 schema CSVs; no PDI |
| photosynthesis | [ ] | [~] | [ ] | 3 schema CSVs; no PDI |
| econ_history | [ ] | [x] | [ ] | 5 schema CSVs; no PDI |
| blue_carbon | [ ] | [ ] | [ ] | Empty; scoping required |
| cuny_ephs | [ ] | [ ] | [ ] | Empty; scoping required |
| grid_ercot_uri | [ ] | [ ] | [ ] | Empty; scoping required |
| water_compare | [ ] | [ ] | [ ] | Comparative view; depends on jackson_ms + newwater + ocwd |
| water_jackson_ms | [ ] | [ ] | [ ] | Empty; scoping required |

### PDI v1.1 conformance check

PDI template was updated to v1.1 (2026-05-10) to add `chain_type`,
`primary_chain_link`, `reentry_primary_phase`, and `C5_reentry_documented`.
All existing PDI instances (danube x13, aubeb, water_newwater, water_ocwd)
need a conformance review to confirm or add the new fields.

- [ ] Review and update danube PDI instances for v1.1 fields
- [ ] Review and update aubeb PDI for v1.1 fields
- [ ] Review and update water_newwater PDI for v1.1 fields
- [ ] Review and update water_ocwd PDI for v1.1 fields

---

## 2. TVPCI scoring pipeline

- [ ] Build gold recycling chain schema CSVs (based on PDI_gold_recycling_2026.yaml)
- [ ] Run `generate_frontend_data.py` for gold recycling and wire score into gold hub
- [ ] Define $B_\text{chain}$ display on gold hub page (primary TVPCI + TVPCI-R combined score)
- [ ] Complete shea PDI, build schema CSVs, run pipeline
- [ ] Wire TVPCI scores into each project hub page as they become available
- [ ] Add TVPCI zone color coding (coherent / stressed / failure / breakdown) to dashboard pages

---

## 3. Research papers

| Paper | Status | Next action |
|-------|--------|-------------|
| Paper 1: Recursive tholonic five constants | [x] | Published |
| Paper 2: Supply chain transparency TVPCI | [x] | PDF rebuilt; recycling model updated |
| Paper 3: Minimal recursive triadic framework | [x] | PDF rebuilt |
| Paper 4: Game-theoretic triadic balance | [~] | TEX exists; review and rebuild PDF |
| Paper 5: Tholonic twistor connection | [~] | PDF rebuilt; TEX not confirmed in repo |
| Paper 6: Qualitative nature of integers | [~] | TEX and PDF present; review for correctness |
| Paper 7: Engineering Toward N: Cambridge Semantics as Empirical Validation | [x] | MD, TEX, and PDF built 2026-05-10; 11 pages |

- [ ] Confirm Paper 5 TEX source is committed
- [ ] Review Paper 4 for consistency with current N-D-C / TVPCI model
- [ ] Review Paper 6 for consistency with current model
- [x] Build Paper 7 TEX and PDF using the research-paper-latex skill
- [ ] Decide on target venue for Paper 7 (knowledge graph / semantic web conference, or philosophy of science journal)

---

## 4. Frontend and site structure

- [ ] Add recycling chain analysis page to gold hub
- [ ] Add TVPCI score badge to each project index.html (once scores are computed)
- [ ] Build shea hub page (supply chain + value chain pages exist but hub is minimal)
- [ ] Determine scope and start PDI for blue_carbon, cuny_ephs, grid_ercot_uri
- [ ] Build water_compare dashboard once all three water projects have scores
- [ ] Register all danube sub-project PDI files in `docs/document-registry.yaml`

---

## 5. Infrastructure and tooling

- [ ] Verify `deploy/tv-web.service` is running and serving correctly in production
- [ ] Confirm Nginx TLS + password gate (AUBEB) is configured and documented
- [ ] Add `water_jackson_ms` to `src/api/generate_frontend_data.py` once schema exists
- [ ] Health check: run `python3 scripts/health_check.py` and fix any reported issues

---

## 6. Documentation

- [ ] Update `docs/document-registry.yaml` with danube sub-project PDI files
- [ ] Add roadmap entry to `docs/document-registry.yaml`
- [ ] Write analyst notes (`docnav/.ai_notes/`) for shea once PDI is complete
- [ ] Consider a short "project status" section in each project's `index.html`

---

## Completed milestones (recent)

- [x] 2026-05-10: TVPCI recycling model standardized (parallel $R_p$ + $B_\text{chain}$, Phase 8 retired)
- [x] 2026-05-10: PDI v1.1 template released (chain_type, reentry_primary_phase, C5)
- [x] 2026-05-10: Gold recycling PDI instance created (PDI_gold_recycling_2026.yaml)
- [x] 2026-05-10: Document registry created (docs/document-registry.yaml)
- [x] 2026-05-10: Content sync skill created (.cursor/skills/content-sync/)
- [x] 2026-05-10: README rewritten as site management reference
- [x] 2026-05-10: User manual created (docs/user-manual.md)
