# Quick view: v2/data files not yet integrated

Assessment of the 11 files that had not been examined/integrated at the time of the last extraction. Purpose: decide whether to integrate, add as reference, or skip.

---

## 1. 080523-Acorn-Project-Summary-Completed.docx

**Content (from text extraction):** Acorn project summary for Golden Organics / Serious Shea. Senegal – Thies, Fatick, Diourbel (Merina Dakhar, Niakhane). Contacts: William Kwende (MD@golden-organics.com), Fatou Mboup (Country Manager). Local partner active since **2007** in Burkina, Benin, Togo, Ivory Coast, Nigeria, Cameroon. **PAPSEN**: >30M euros financing, 400 ha irrigated perimeters, Thiès/Diourbel/Fatick, Kolda/Sédhiou. Cooperatives: nurseries, planting, maintenance; women/youth/men – contracts with Serious Shea. Cash crops: Groundnuts, Millet, Rice, Maize, Sorghum. **50** existing farmer participants in Koul (pilot); **100,000** potential additional participants over 10 years. **1 ha** per farmer average plot. Native languages etc.

**Useful for integration?** **Yes.**  
- **Geography:** Regions/districts (Thies, Fatick, Diourbel, Merina Dakhar, Niakhane); PAPSEN 400 ha irrigated.  
- **Scale:** 50 pilot farmers, 100,000 potential participants, 1 ha/farmer.  
- **Entity/context:** PAPSEN financing scale (~30M euros), partner since 2007, cash crops.  
**Suggested use:** Add to `shea_data_sources.csv`; add metrics to `shea_phase_metrics.csv` or `shea_fund_and_project_context.csv` (e.g. pilot_farmers_50, potential_participants_100000, plot_size_ha_1, PAPSEN_irrigated_ha_400, regions list).

---

## 2. 230401-George-Commnts-SS-Senegal-BP-.docx

**Content:** George’s comments (April 2023) on the Serious Shea Senegal business plan. GGW / Trillion Trees Sahel 2021 winner; 2 years feasibility; Sahel **3 million km²**, 14 countries; GGW focus **116,000 sq.km** (11,662,500 ha) at highest risk/highest potential; **1,000,000 ha** “starts now with Senegal”. Senegal: **17 million** population, **196,712 sq.km**. Emphasis on branding “Serious Shea Senegal” and link to GGW. Suggests explaining ChainZy (value chain accountability).

**Useful for integration?** **Yes.**  
- **Geography/scale:** Senegal area 196,712 km²; population 17M; GGW priority area 116,000 km² (11.6M ha); 1M ha “starts with Senegal”.  
- **Context:** Clarifies GGW scope and Senegal’s role.  
**Suggested use:** Add source; add or align Senegal area/pop and GGW hectare figures in `shea_fund_and_project_context.csv` (we have Senegal GDP and rural energy; add area_km2, population, GGW_priority_ha if not already there).

---

## 3. 230428-Serious-Shea-Financial-Model-v1.1.xlsx

**Content (from shared strings):** 31-year financial forecast for Serious Shea’s **ARR (Afforestation, Reforestation, Revegetation) project in Senegal**. VCS and CCB project. Includes: Project Summary; NPV; Assumptions; Revenue Build (VCU, Other); Project Development & Monitoring Cost; Cost Build (ARR, Productive Activities); P&L; Cash Flow; Balance Sheet; WACC; VCU Volume. User-adjustable variables (pink cells); disclaimer (illustrative only). Format: EUR; no tax/forex in model.

**Useful for integration?** **Yes, for structure and assumptions.**  
- **Structure:** Revenue (VCU + other), costs (PD&M, ARR, productive), P&L, CFS, BS, WACC – aligns with BPlan figures we already integrated (e.g. revenue 2033 €55M).  
- **Use:** Add as **source** (Serious Shea Financial Model v1.1); note “detailed 31-year model; numeric extraction not done – use for reconciliation with BPlan”. Optional: extract key assumption rows (e.g. VCU price, volumes) manually later.

**Suggested use:** Add to `shea_data_sources.csv`; optionally add one-row “financial_model_reference” in fund context. No need to duplicate BPlan numbers already integrated.

---

## 4. 230607-V1-Draft-Covergence-Concept-Serious-Shea.pdf

**Content (from read):** Only page markers (1–5); no extractable text in the sampled read. Likely image-heavy or scanned.

**Useful for integration?** **Unclear.**  
- **Suggested use:** **Skip** for automated extraction. If you have a text version or can OCR it, a human could later pull “convergence concept” narrative and any metrics and add them manually.

---

## 5. 230608-Serious-Shea-Senegal-for-Covergence.pptx

**Content:** Binary; not readable as text in this environment.

**Useful for integration?** **Unknown.**  
- **Suggested use:** **Defer.** If it’s a presentation version of the BPlan or Convergence concept, it may duplicate content already in the BPlan PDF. Manual review could confirm and add any extra figures.

---

## 6. Ep-Carbon-new-Requirements.xlsx

**Content (from shared strings):** **Plantation site list** – “Plantation Site List” with columns Site Name, Primary Area (Ha), Secondary Area (Ha). Sites include: PAPSEN, Ndiakhate Saer, Nghass, Darou Salam, Mbodiene Ndiaye, Darou Gaye, Lamsing, Keur Abdou Ndiaye, Batal, Sine Macoumba, Bousra Leye, Sao, Nder Nar, Goly, Gade Niandoul, Tieye Tieye, Ndiarga, Mbalene, Tambacounda 1 & 2, Belle, Belle Nursery Zone, Dialiguel, Sarre, Bema/Gouniag, Bakel Nursery, Fenaye Dieri (1 & 2), Loumbol, Eco Village Makoumbel, GGW Senegal; TOTAL. Also: Farmers, Fatick, Diourbel, Shea Plantation Zone, “Community Land/Private Land Protected by the Ministry of Environment and Forestry”, Region, Merina Dakhar, Niakhane-Merina Dakhar, and a Google Maps link.

**Useful for integration?** **Yes.**  
- **Geography/sites:** Named plantation sites and regions (Fatick, Diourbel, Tambacounda, etc.); Shea Plantation Zone; GGW Senegal.  
- **Use:** Site list and regions can support **entity/site registry** or **phase 0/1 geography** (collection/planting zones). Primary/Secondary Area (Ha) would need cell extraction for each site.  
**Suggested use:** Add source “EP Carbon new Requirements”; add a **shea_plantation_sites_senegal.csv** (or rows in an existing geography table) with site names and regions; optionally add “EP Carbon site list” as reference in schema README. Area (Ha) per site: extract from xlsx when needed.

---

## 7. scenarios 3-1.pdf

**Content (from read):** Generic **sustainability scenarios** deck (73 pages): “What is sustainability?”; “What are scenarios?”; 2050 predictions; oil reserves (e.g. 1200 billion barrels, exhausted in &lt;40 years); consumer behaviour (“only 2% buy green”); Scenario 1 Solar energy; Scenario 2 ECO x ECO; sustainable cities/homes. **Not shea- or Senegal-specific.**

**Useful for integration?** **No** for shea data.  
- **Suggested use:** **Do not integrate** into shea CSVs. Keep as optional general reference only if desired.

---

## 8. Serious-Shea-Acorn-Eligibility-Checklist.xlsx

**Content (from shared strings):** Acorn **eligibility checklist** structure: Project details (name, location, date); Topic/Sub-topic/Requested information/Result; Organizational capacity (Sustainability, GDPR, Participant organization, Project effects); Entity; Local presence; Local policies; Influence; Resources; Data collection; Training; Participant identity; Sustainable land use; Project design; Deforestation; Additionality; Existing agroforestry (i)/(ii); New agroforestry; “Sufficient supply of seedlings, inputs, water”; Naturalized species; Current habitat; Yes/No/N/A; Organizational structure; voluntary participation. **No numeric shea metrics** – it’s a checklist template.

**Useful for integration?** **Reference only.**  
- **Use:** Documents **Acorn eligibility criteria** (additionality, agroforestry, land use, data, etc.). Useful for “what’s required for Acorn/carbon projects” and for aligning phase 0/1 process.  
**Suggested use:** Add to `shea_data_sources.csv` as **REFERENCE_ONLY** (e.g. “Acorn eligibility checklist – Serious Shea; no shea-specific metrics”). Optionally add a short “Acorn eligibility topics” list to a process/requirements doc.

---

## 9. Serious-Shea-Additionality-Assessment1.docx

**Content (from text extraction):** **Acorn Additionality Assessment** for Serious Shea Senegal. Location: Senegal, Thies, Fatick, Diourbel. **Barriers:** farmers don’t know agroforestry; trees don’t produce income in Sahel; limited access to finance; limited technical expertise; lack of suitable land (degraded soils, erosion, land tenure); lack of market opportunities. **Planting:** “Farmers will plant all the trees in one year on their land” (easier to manage, same age, same inputs). “Non applicable” for multi-year planting.

**Useful for integration?** **Yes, for context.**  
- **Barriers:** Finance, expertise, land, markets – can be tagged as **additionality/context** (e.g. phase 0/1 constraints).  
- **Design:** “All trees in one year” – clarifies planting phasing.  
**Suggested use:** Add source; add a short “additionality barriers” note or table (e.g. in SHEA_SCHEMA_README or a short “additionality_context” section) and reference in phase 0/1 notes where relevant.

---

## 10. Serious-Shea-Business-Case-Template-Acorn1.xlsx

**Content (from shared strings):** Only indices and a few numbers (e.g. 45075) in the first sheet; likely a **template** with placeholders. No substantive shea metrics extracted.

**Useful for integration?** **Low.**  
- **Suggested use:** Add to `shea_data_sources.csv` as **REFERENCE_ONLY** (“Acorn business case template – Serious Shea; template structure only”) or skip.

---

## 11. Serious-Shea-Global-Indicator-Framework-after-2023-refinement.English.xlsx

**Content (from shared strings):** **SDG indicator framework** aligned with 2030 Agenda. Columns include: Goals and targets; Indicators; UNSD Indicator Codes; **Baseline**; **Serious Shea 2030**; Means of Verification. Example: Goal 1 (poverty) – baseline “**100,000 workers, 1 M people**”, Serious Shea 2030 “**Zero**”, MoV “Cooperatives”. Many SDG targets (1.1, 1.2, 1.3, 1.4, 1.5, 1.a, 1.b, etc.) with codes (C010101, C010201, …). Framework is **disaggregation**-oriented (income, sex, age, etc.).

**Useful for integration?** **Yes.**  
- **Metrics:** Baseline “100,000 workers, 1 M people” and target “Zero” (poverty) give **impact scale** and **targets**.  
- **Use:** Aligns with BPlan (135,000 households, 13,500 coop workers) – possible slight difference in definition (workers vs people).  
**Suggested use:** Add source; add to `shea_fund_and_project_context.csv` or phase metrics: e.g. **baseline_workers_100000**, **baseline_people_1M**, **target_poverty_zero**; link to SDG 1 and “Serious Shea 2030”. Cross-check with BPlan figures for consistency.

---

## Summary table

| File | Useful? | Integrate? | Add as reference? | Suggested action |
|------|--------|------------|--------------------|------------------|
| 080523-Acorn-Project-Summary-Completed.docx | Yes | Yes | — | Add source; add pilot 50, potential 100k, 1 ha, PAPSEN 400 ha, regions. |
| 230401-George-Commnts-SS-Senegal-BP-.docx | Yes | Yes | — | Add source; add Senegal 196,712 km², 17M pop, GGW 116k km² / 1M ha. |
| 230428-Serious-Shea-Financial-Model-v1.1.xlsx | Yes | Light | Yes | Add source; note “31-year model; reconcile with BPlan”. |
| 230607-V1-Draft-Covergence-Concept-Serious-Shea.pdf | Unclear | No | Optional | Skip automated extraction; manual/OCR if needed. |
| 230608-Serious-Shea-Senegal-for-Covergence.pptx | Unknown | No | Optional | Defer; manual review if BPlan duplicate. |
| Ep-Carbon-new-Requirements.xlsx | Yes | Yes | — | Add source; add site list (names + regions) – new table or fund/geography. |
| scenarios 3-1.pdf | No | No | No | Do not integrate (generic sustainability). |
| Serious-Shea-Acorn-Eligibility-Checklist.xlsx | Reference | No | Yes | Add source REFERENCE_ONLY (Acorn eligibility). |
| Serious-Shea-Additionality-Assessment1.docx | Yes | Yes | — | Add source; add additionality barriers + “plant in one year”. |
| Serious-Shea-Business-Case-Template-Acorn1.xlsx | Low | No | Optional | REFERENCE_ONLY or skip. |
| Serious-Shea-Global-Indicator-Framework...xlsx | Yes | Yes | — | Add source; add baseline 100k workers / 1M people, target Zero. |

---

*Quick view completed. Next step: apply “Suggested action” for each “Yes” / “Light” / “Reference” file in the shea CSVs and schema README.*
