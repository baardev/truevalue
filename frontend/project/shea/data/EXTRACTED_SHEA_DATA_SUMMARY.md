---
doc_id: frontend_project_shea_data_extracted_shea_data_summary
title: "Extracted Shea Data – Summary (lives in `frontend/project/shea/data/` with the shea schema CSVs and source PDFs/Office files)"
type: summary
status: active
domain: shea_supply_chain
layer: methodology
projects:
  - shea
tags:
  - methodology
  - shea
  - shea_supply_chain
related_docs:
  []
key_claims:
  []
---

# Extracted Shea Data – Summary (lives in `frontend/project/shea/data/` with the shea schema CSVs and source PDFs/Office files)

This note summarises **new or updated data** extracted from the four documents and integrated into the shea CSVs. The **Clarity_Cleo_Shea_Value_Chain_Outline.md** was already the project’s synthesis; no duplicate extraction was done from it.

---

## 1. Mirova-Shea-Senegal-Feasibility-Report-v1.1.pdf

- **Status:** PDF is image/layout-heavy; only **one table** was reliably extracted.
- **Extracted:**
  - **Land use (Shea project site):** Shrubs 19.16%, Herbaceous 9.85%, Cropland 0.41%, Open forest 56.84%, Closed forest 13.49%, other categories small (table “Project / Site” ~p.92).
- **Integrated:** New rows in **shea_fund_and_project_context.csv** (land_use_shea_site_shrubs_pct, land_use_shea_site_open_forest_pct); new source row in **shea_data_sources.csv** (Mirova Feasibility, PARTIAL).

---

## 2. Clarity_Cleo_Shea_Value_Chain_Outline.md

- **Status:** Already the main narrative and numeric synthesis for Burkina Faso / West Africa and Cleo.
- **Action:** No re-extraction; existing **shea_phase_metrics.csv**, **shea_supply_chain_phases.csv**, and **shea_data_sources.csv** (Clarity/Cleo source #8) continue to reflect it.

---

## 3. Acorn-Local-Partner-Onboarding-Process.pdf

- **Status:** Generic **Acorn/Rabobank** agroforestry/carbon **onboarding process** (eligibility, additionality, agroforestry design, farmer onboarding, ground truth, LiDAR, recurring monitoring).
- **Extracted:** Process steps only; **no shea-specific metrics or numbers**.
- **Integrated:** New source row in **shea_data_sources.csv** with **REFERENCE_ONLY** (process reference for “local partner” / phase 0–1 context only).

---

## 4. 230424-ShortSeriousShea.BPlan_.Pres_.-V8Draft-SNJ.pdf (Serious Shea Senegal Business Plan V8, April 2023)

- **Status:** 27-slide business plan; **Senegal / Great Green Wall**; main source of new quantitative data.
- **Extracted and integrated:**

| Topic | Metric(s) | Where integrated |
|-------|-----------|-------------------|
| **BAU energy (phase 3)** | 20 kg firewood per 1 kg shea butter | **shea_phase_metrics.csv** (firewood_kg_per_kg_butter_BAU) |
| **Processing scale** | 3,774 MT/year agro-food (shea, mango, moringa, baobab) | **shea_phase_metrics.csv** (processing_throughput_serious_shea_senegal_agrofood); **shea_fund_and_project_context.csv** |
| **Investment & finance** | €25M investment; €50M p.a. gross profit Year 10; 40% Carbon Equity (Mirova), 60% Debt | **shea_fund_and_project_context.csv** |
| **Trees & carbon** | 35M trees by 2030; 80% survival; 4.2M tCO2e sequestered Year 10; 1M ha plantations; carbon @ €10/tCO2e | **shea_fund_and_project_context.csv** |
| **People** | 750 staff (50%+ women); 135,000 households; 13,500 cooperative workers (50%+ women); income ≥5× min wage; 20% shares Community Fund | **shea_fund_and_project_context.csv** |
| **Facilities** | 26 facilities (18 multi-use clean energy + 2 shea clusters with 2 regional + 3 collection centres each); 5 nurseries × 1M seedlings p.a. | **shea_fund_and_project_context.csv** |
| **Revenue** | Total revenue 2033 €55M (industry + carbon) | **shea_fund_and_project_context.csv** |
| **Context** | Senegal GDP US$27.7B; rural energy access 38%; min wage ref US$166.65/year (2023) or US$117/year | **shea_fund_and_project_context.csv** |
| **BF origins** | Serious Shea BF founded by Golden Organics, Impact Agri, Women’s Shea Butter Union; funded World Bank, AfDB, BF Government | **shea_fund_and_project_context.csv** |
| **Agritech** | 5–10,000 T/year shea nuts (Agritech Group) | **shea_fund_and_project_context.csv** |

- **Source:** New row in **shea_data_sources.csv** (Serious Shea BPlan V8 2023, POPULATED).

---

## Files updated

- **shea_data_sources.csv** – Added source_id 10 (Mirova Feasibility), 11 (Serious Shea BPlan), 12 (Acorn onboarding).
- **shea_phase_metrics.csv** – Added record_id 37 (firewood 20 kg/kg butter BAU), 38 (processing throughput 3774 MT/year Serious Shea Senegal agro-food).
- **shea_fund_and_project_context.csv** – Rebuilt and expanded with BF + Senegal + Agritech + Mirova land-use metrics; all figures traceable to document and page/slide where possible.

---

## Data status conventions

- **POPULATED** – Value(s) taken from the document.
- **PARTIAL** – Only some content extracted (e.g. Mirova: one table).
- **METADATA_ONLY** – Only title/nav or high-level labels (e.g. Clarity password-protected page).
- **REFERENCE_ONLY** – No shea metrics; process/structure reference only (Acorn).

---

*Generated when integrating Mirova Feasibility, Clarity outline, Acorn Onboarding, and Serious Shea BPlan V8 into `frontend/project/shea/data/` shea CSVs (previously also under v2).*
