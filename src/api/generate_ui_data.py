#!/usr/bin/env python3
"""
UI Data Generator — supply chain JSON for frontend dashboards.

Reads from authoritative CSVs and phase summary JSONs, then writes
(additively) to data/frontend/gold_supply_chain_ui.json and
data/frontend/shea_supply_chain_ui.json.

"Additive" means:
  - Fields already present in the target JSON are only overwritten if
    the source CSV/JSON has a newer or non-null value.
  - The special key "overrides" (if present in the target JSON) is
    never touched by this script.
  - _meta.generated is always updated.

Usage:
    python src/api/generate_ui_data.py [--dry-run]

Requirements:
    pip install pandas
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parents[2]

GOLD_METRICS_CSV   = REPO / "schema" / "gold_supply_chain_metrics.csv"
GOLD_PHASES_CSV    = REPO / "schema" / "supply_chain_phases.csv"
GOLD_SOURCES_CSV   = REPO / "schema" / "data_sources.csv"
PHASE_SUMMARIES    = [REPO / "src" / "data" / "processed" / f"phase{i}_summary.json" for i in range(9)]

SHEA_DIR           = REPO / "frontend" / "project" / "shea" / "data"
SHEA_METRICS_CSV   = SHEA_DIR / "shea_phase_metrics.csv"
SHEA_PHASES_CSV    = SHEA_DIR / "shea_supply_chain_phases.csv"
SHEA_SOURCES_CSV   = SHEA_DIR / "shea_data_sources.csv"

GOLD_UI_JSON     = REPO / "data" / "frontend" / "gold_supply_chain_ui.json"
SHEA_UI_JSON     = REPO / "data" / "frontend" / "shea_supply_chain_ui.json"
GOLD_VC_UI_JSON  = REPO / "data" / "frontend" / "gold_value_chain_ui.json"
SHEA_VC_UI_JSON  = REPO / "data" / "frontend" / "shea_value_chain_ui.json"

NOW = datetime.now().isoformat(timespec="seconds")


# ── Helpers ───────────────────────────────────────────────────────────────────

def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        print(f"  [SKIP] {path} not found", file=sys.stderr)
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict, dry_run: bool = False):
    path.parent.mkdir(parents=True, exist_ok=True)
    out = json.dumps(data, indent=2, ensure_ascii=False)
    if dry_run:
        print(f"  [DRY-RUN] Would write {len(out)} bytes to {path.relative_to(REPO)}")
    else:
        path.write_text(out, encoding="utf-8")
        print(f"  [WRITE]   {path.relative_to(REPO)}  ({len(out)} bytes)")


def parse_float(val) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def additive_merge(target: dict, source: dict) -> dict:
    """
    Recursively merge source into target.
    - Source None / empty string → skip (keep target value).
    - Scalar: source wins if target is None or missing.
    - Dict: recurse.
    - Lists: source replaces target (lists are not merged).
    The special key "overrides" at any level is NEVER touched.
    """
    for k, v in source.items():
        if k == "overrides":
            continue
        if v is None or v == "":
            continue
        if k not in target or target[k] is None:
            target[k] = v
        elif isinstance(v, dict) and isinstance(target[k], dict):
            additive_merge(target[k], v)
        else:
            target[k] = v       # source value wins for scalars
    return target


# ── Scope 1 / Scope 2 emissions per phase ─────────────────────────────────────
# Sources:
#   Phase 0: Inferred — exploration industry benchmarks
#   Phase 1: WGC "Gold and Climate" 2023; Foran et al. 2005 Balancing Act Vol 2
#             (13% direct / 44% grid electricity split applied to Phase 1)
#   Phase 2: WGC 2023; Newmont 2024 Sustainability Report
#   Phase 3: Inferred — smelting industry benchmarks; IPCC industrial process data
#   Phase 4: Inferred — LBMA refinery benchmarks; chemical processing industry data
#   Phase 5: Inferred — metal casting industry benchmarks
#   Phase 6: Inferred — ICCT transport benchmarks; vault facility energy data
#   Phase 7: Inferred — financial sector emissions benchmarks (GHG Protocol)
#   Phase 8: WGC Gold Recycling Report 2023; secondary smelting benchmarks
# All values are annual global estimates in tCO₂e. Quality flags follow project
# transparency classification rules: Medium = citable public data; Low = inferred.

SCOPE_EMISSIONS: dict[str, dict] = {
    "0": {
        "scope1_tco2": 120_000,
        "scope2_tco2": 25_000,
        "scope_source": "Inferred — exploration industry benchmarks",
        "scope_quality": "Low",
        "scope_notes": "Diesel vehicles, drilling rigs, seismic equipment (S1); remote field power (S2).",
    },
    "1": {
        "scope1_tco2": 8_200_000,
        "scope2_tco2": 27_800_000,
        "scope_source": "WGC Gold and Climate 2023; Foran et al. 2005 (13% direct/44% grid split applied to Phase 1)",
        "scope_quality": "Medium",
        "scope_notes": "Diesel haul trucks, blasting, dewatering (S1); ventilation, grinding mills (S2). S2 dominant at 25% clean energy mix.",
    },
    "2": {
        "scope1_tco2": 3_000_000,
        "scope2_tco2": 17_000_000,
        "scope_source": "WGC Gold and Climate 2023; Newmont 2024 Sustainability Report",
        "scope_quality": "Medium",
        "scope_notes": "Chemical heating, reagent production (S1); grinding mills, flotation, pumping — most electricity-intensive phase (S2).",
    },
    "3": {
        "scope1_tco2": 3_800_000,
        "scope2_tco2": 2_600_000,
        "scope_source": "Inferred — smelting industry benchmarks; IPCC industrial process data",
        "scope_quality": "Low",
        "scope_notes": "Furnace fuel (heavy oil/gas) dominant; thermal process drives high S1 share. Moderate electricity for ancillary (S2).",
    },
    "4": {
        "scope1_tco2": 2_000_000,
        "scope2_tco2": 3_600_000,
        "scope_source": "Inferred — LBMA refinery benchmarks; chemical processing industry data",
        "scope_quality": "Low",
        "scope_notes": "Acid process heating, chlorine generation (S1); electrolytic cells, ventilation (S2). 50% clean energy reduces S2.",
    },
    "5": {
        "scope1_tco2": 500_000,
        "scope2_tco2": 700_000,
        "scope_source": "Inferred — metal casting industry benchmarks",
        "scope_quality": "Low",
        "scope_notes": "Casting furnace fuel (S1); assay equipment, environmental controls (S2). Smallest direct-process emissions phase.",
    },
    "6": {
        "scope1_tco2": 3_200_000,
        "scope2_tco2": 800_000,
        "scope_source": "Inferred — ICCT transport benchmarks; vault facility energy data",
        "scope_quality": "Low",
        "scope_notes": "Air freight, armoured vehicles, ship transport dominant (S1); vault HVAC, security systems (S2).",
    },
    "7": {
        "scope1_tco2": 40_000,
        "scope2_tco2": 200_000,
        "scope_source": "Inferred — financial sector GHG Protocol benchmarks",
        "scope_quality": "Low",
        "scope_notes": "Exchange operations minimal physical process; IT infrastructure, office buildings (S2 dominant).",
    },
    "8": {
        "scope1_tco2": 1_200_000,
        "scope2_tco2": 2_000_000,
        "scope_source": "WGC Gold Recycling Report 2023; secondary smelting benchmarks",
        "scope_quality": "Low",
        "scope_notes": "Secondary smelting, refining furnaces (S1); processing electricity (S2). Offsets ~28% of virgin production emissions.",
    },
}


# ── Water data per phase ───────────────────────────────────────────────────────
# Recycling rates and source citations from docs/Reports/WATER_WASTE_METHODOLOGY.md.
# Newmont 2024 SR confirms Phase 2 actual recycling = 71% (stored in metrics CSV).

WATER_DATA: dict[str, dict] = {
    "0": {"water_recycling_pct": 0,  "water_quality": "Low",    "water_source": "Negligible — field equipment, potable supply only",                                    "water_notes": "Dust control for drilling; no process water. Effectively zero consumption."},
    "1": {"water_recycling_pct": 20, "water_quality": "Medium", "water_source": "Newmont/Barrick Sustainability Reports; ICMM Water Reporting Guidelines (benchmark 10-30%)", "water_notes": "Dust suppression 30-40%, ore washing 20-30%, equipment cooling 10-15%. Recycling mostly cooling water."},
    "2": {"water_recycling_pct": 75, "water_quality": "High",   "water_source": "Newmont 2024 SR (71% actual); ICMM benchmark 60-85%",                                  "water_notes": "Cyanide leaching 40-50%, flotation 25-35%. Closed-loop circuits. Most water-intensive phase."},
    "3": {"water_recycling_pct": 80, "water_quality": "Low",    "water_source": "Inferred — smelting industry benchmarks (range 70-90%)",                               "water_notes": "Furnace cooling 60-70%, slag granulation 20-30%. Closed-loop cooling achieves high recycling."},
    "4": {"water_recycling_pct": 65, "water_quality": "Low",    "water_source": "Inferred — LBMA refinery benchmarks; Marsden & House (2006)",                          "water_notes": "Electrolytic baths 30-40%, aqua regia 20-30%, rinsing 15-25%. Ultra-pure water requirement limits recycling."},
    "5": {"water_recycling_pct": 30, "water_quality": "Low",    "water_source": "Inferred — metal casting industry benchmarks",                                         "water_notes": "Cooling water only. Small volume; limited recycling infrastructure at this process scale."},
    "6": {"water_recycling_pct": 0,  "water_quality": "Low",    "water_source": "Negligible — vault HVAC condensate only",                                              "water_notes": "No process water. HVAC climate control is the only source. Effectively zero net consumption."},
    "7": {"water_recycling_pct": 0,  "water_quality": "Low",    "water_source": "Negligible — office and data centre use only",                                         "water_notes": "No physical process water. Exchange operations are purely administrative."},
    "8": {"water_recycling_pct": 70, "water_quality": "Low",    "water_source": "WGC Gold Recycling Report 2023; UK Royal Mint; Umicore benchmarks (range 60-80%)",     "water_notes": "Similar process to Phase 4 with heterogeneous input. E-waste wash water adds variability."},
}


def inject_water_data(target: dict) -> None:
    """Add per-phase water recycling and source metadata (additive — never overwrites)."""
    target.setdefault("phases", {}).setdefault("synthetic", {})
    for pid, data in WATER_DATA.items():
        phase = target["phases"]["synthetic"].setdefault(pid, {})
        for k, v in data.items():
            if k not in phase or phase[k] is None:
                phase[k] = v


# ── Energy metadata per phase ──────────────────────────────────────────────────
# Energy unit confirmed kWh (see WATER_WASTE_METHODOLOGY.md, energy_base dict).
# Clean % from methodology base_clean_pct; Foran 2005 confirms 44% grid electricity
# share for Phase 1-2.  WGC 2030 target: 60% clean energy across operations.

ENERGY_DATA: dict[str, dict] = {
    "0": {"energy_unit": "kWh", "energy_clean_pct": 20, "energy_quality": "Low",    "energy_source": "Inferred — exploration industry benchmarks",                                              "energy_notes": "Small generators, field equipment. Some solar at modern exploration camps. Mostly diesel."},
    "1": {"energy_unit": "kWh", "energy_clean_pct": 25, "energy_quality": "Medium", "energy_source": "WGC Gold and Climate 2023; Foran et al. 2005; Newmont 30% renewable target by 2030",       "energy_notes": "Diesel 60-80% (haul trucks, excavators, drills); grid 10-30%; renewables 5-15% growing. Remote location limits grid access."},
    "2": {"energy_unit": "kWh", "energy_clean_pct": 40, "energy_quality": "Medium", "energy_source": "WGC 2023; Foran et al. 2005 (44% grid electricity split of total sector GHG)",            "energy_notes": "Grid electricity 70-90% (grinding mills, leach tanks, pumps). Most electricity-intensive phase. Grid-connected — easiest to decarbonise."},
    "3": {"energy_unit": "kWh", "energy_clean_pct": 35, "energy_quality": "Low",    "energy_source": "Inferred — smelting industry benchmarks",                                                  "energy_notes": "Furnace fuel (heavy oil/gas) 60-70%; grid electricity 30-40%. On-site smelting limits renewable options."},
    "4": {"energy_unit": "kWh", "energy_clean_pct": 50, "energy_quality": "Low",    "energy_source": "Inferred — LBMA refinery benchmarks; European refinery national grid data",               "energy_notes": "Electrolytic cells 50-60%; furnaces 30-40%. Urban location gives grid access; European refineries benefit from cleaner national grids."},
    "5": {"energy_unit": "kWh", "energy_clean_pct": 50, "energy_quality": "Low",    "energy_source": "Inferred — metal casting benchmarks (co-located with refineries)",                        "energy_notes": "Casting furnace and assay equipment. Shares refinery grid profile. Low absolute consumption."},
    "6": {"energy_unit": "kWh", "energy_clean_pct": 55, "energy_quality": "Low",    "energy_source": "Inferred — vault facility energy data",                                                    "energy_notes": "HVAC, lighting, security systems. Urban vaults benefit from cleaner grid. Very low absolute consumption."},
    "7": {"energy_unit": "kWh", "energy_clean_pct": 60, "energy_quality": "Low",    "energy_source": "Inferred — financial sector energy benchmarks; data centre renewable procurement trends", "energy_notes": "Exchange floor, data centres, IT infrastructure. Growing renewable procurement for data centres."},
    "8": {"energy_unit": "kWh", "energy_clean_pct": 45, "energy_quality": "Low",    "energy_source": "WGC Gold Recycling Report 2023; secondary smelting benchmarks",                          "energy_notes": "Similar to Phase 4 but variable input increases intensity. Saves 60-80% energy vs primary production."},
}


def inject_energy_data(target: dict) -> None:
    """Add per-phase energy unit, clean %, and source metadata (additive — never overwrites)."""
    target.setdefault("phases", {}).setdefault("synthetic", {})
    for pid, data in ENERGY_DATA.items():
        phase = target["phases"]["synthetic"].setdefault(pid, {})
        for k, v in data.items():
            if k not in phase or phase[k] is None:
                phase[k] = v


def inject_scope_emissions(target: dict) -> None:
    """Add Scope 1/2 baseline emissions data to each synthetic phase (additive — never overwrites)."""
    target.setdefault("phases", {}).setdefault("synthetic", {})
    for pid, scope_data in SCOPE_EMISSIONS.items():
        phase = target["phases"]["synthetic"].setdefault(pid, {})
        for k, v in scope_data.items():
            if k not in phase or phase[k] is None:
                phase[k] = v


# ── Gold generator ────────────────────────────────────────────────────────────

def build_gold_ui(dry_run: bool = False):
    print("\n── Gold Supply Chain UI ──────────────────────────────────")

    # Load existing target (to preserve hand-authored fields)
    target = load_json(GOLD_UI_JSON)
    if not target:
        print("  [NEW] No existing file; starting from scratch.")
        target = {}

    # ── Phase metadata from CSV ──────────────────────────────────────────────
    phases_csv = read_csv(GOLD_PHASES_CSV)
    phase_meta = {}
    for row in phases_csv:
        pid = str(row.get("phase_id", "")).strip()
        if not pid:
            continue
        phase_meta[pid] = {
            "name":         row.get("phase_name", "").strip() or target.get("phase_meta", {}).get(pid, {}).get("name"),
            "transparency": row.get("transparency_level", "").strip() or "OPAQUE",
            "recycling":    str(pid) == "8",
        }
    if phase_meta:
        target.setdefault("phase_meta", {})
        for pid, meta in phase_meta.items():
            target["phase_meta"].setdefault(pid, {})
            additive_merge(target["phase_meta"][pid], meta)

    # ── Metrics from CSV, grouped by entity and phase ────────────────────────
    metrics_rows = read_csv(GOLD_METRICS_CSV)
    by_entity_phase: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for row in metrics_rows:
        entity = (row.get("entity") or "synthetic").strip()
        pid    = str(row.get("phase_id", "")).strip()
        by_entity_phase[entity][pid].append(row)

    # Synthetic baseline: update notes and entity_metrics per phase
    target.setdefault("phases", {}).setdefault("synthetic", {})
    for pid, rows in by_entity_phase.get("Australian Gold and Lead Sector", {}).items():
        target["phases"]["synthetic"].setdefault(pid, {})
        # Append metric names as a note hint
        metric_names = [r.get("metric_name", "") for r in rows if r.get("metric_name")]
        if metric_names:
            existing = target["phases"]["synthetic"][pid].get("notes", "")
            hint = f"Source metrics: {', '.join(metric_names[:4])}{'...' if len(metric_names) > 4 else ''}."
            if hint not in existing:
                target["phases"]["synthetic"][pid]["notes"] = (existing + " " + hint).strip()

    # Newmont entity
    target["phases"].setdefault("newmont", {})
    for pid, rows in by_entity_phase.get("Newmont Corporation", {}).items():
        target["phases"]["newmont"].setdefault(pid, {})
        existing_metrics = target["phases"]["newmont"][pid].setdefault("entity_metrics", {})
        for row in rows:
            mname = row.get("metric_name", "").strip()
            mval  = row.get("metric_value")
            munit = row.get("unit", "")
            msrc  = row.get("source_name", "")
            mnote = row.get("notes", "")
            if mname and mname not in existing_metrics:
                entry = {"unit": munit, "source": msrc}
                fv = parse_float(mval)
                entry["value"] = fv if fv is not None else mval
                if mnote:
                    entry["note"] = mnote[:120]
                existing_metrics[mname] = entry

    # ── Phase summaries (transparency, data quality) ─────────────────────────
    for path in PHASE_SUMMARIES:
        summary = load_json(path)
        if not summary:
            continue
        pid = str(summary.get("phase_id", "")).strip()
        if not pid:
            continue
        target["phases"]["synthetic"].setdefault(pid, {})
        dq = summary.get("data_quality")
        if dq and not target["phases"]["synthetic"][pid].get("data_quality"):
            target["phases"]["synthetic"][pid]["data_quality"] = dq
        ndc = summary.get("ndc_notes")
        if ndc:
            target["phases"]["synthetic"].setdefault("_ndc_notes", {})[pid] = ndc

    # ── System summary ───────────────────────────────────────────────────────
    target.setdefault("system", {}).setdefault("synthetic", {
        "balance":               82.5,
        "water_recycling_pct":   73,
        "waste_circularity_pct": 5.2,
        "clean_energy_pct":      42,
        "target_clean_energy_pct": 60,
        "target_year":           2030
    })

    # ── Scope 1/2 emissions per phase ─────────────────────────────────────────
    inject_scope_emissions(target)

    # ── Water recycling and metadata per phase ────────────────────────────────
    inject_water_data(target)

    # ── Energy unit and clean % per phase ─────────────────────────────────────
    inject_energy_data(target)

    # ── Update _meta ─────────────────────────────────────────────────────────
    target["_meta"] = {
        "generated": NOW,
        "generator": "src/api/generate_ui_data.py",
        "sources": [
            str(GOLD_METRICS_CSV.relative_to(REPO)),
            str(GOLD_PHASES_CSV.relative_to(REPO)),
            "src/data/processed/phase*_summary.json",
            "SCOPE_EMISSIONS constant (see generator — WGC 2023, Foran 2005, industry benchmarks)",
            "WATER_DATA constant (see generator — Newmont 2024 SR, ICMM, WATER_WASTE_METHODOLOGY.md)",
            "ENERGY_DATA constant (see generator — WGC 2023, Foran 2005, WATER_WASTE_METHODOLOGY.md)",
        ],
        "note": "Auto-generated. Re-run src/api/generate_ui_data.py to refresh. "
                "Fields under 'overrides' are never modified.",
    }

    save_json(GOLD_UI_JSON, target, dry_run)
    print(f"  Phases found in CSV metrics: {sorted(set(r.get('phase_id','?') for r in metrics_rows))}")


# ── Shea generator ─────────────────────────────────────────────────────────

# ── Shea Scope 1/2 emissions per phase ────────────────────────────────────────
# Phase 3 uses Serious Shea scenario as the baseline (the lower-emission state).
# BAU comparison data stored in scope_bau_co2e_per_kg and scope_ss_co2e_per_kg.
# Source: Clarity/Cleo Value Chain Outline; Serious Shea BPlan V8 April 2023.

SHEA_SCOPE_EMISSIONS: dict[str, dict] = {
    "0": {
        "scope1_tco2": 45_000,
        "scope2_tco2": 5_000,
        "scope_source": "Inferred — manual collection, negligible motorised equipment",
        "scope_quality": "Low",
        "scope_notes": "Hand collection of shea nuts; seasonal May–Oct. Walking/donkey transport. Minimal combustion.",
        "scope_bau_note": "BAU = same; no mechanical intervention in either scenario at this phase.",
    },
    "1": {
        "scope1_tco2": 80_000,
        "scope2_tco2": 8_000,
        "scope_source": "Inferred — rural West Africa transport benchmarks",
        "scope_quality": "Low",
        "scope_notes": "Motorcycle/donkey transport of bagged nuts to village aggregation points. Diesel S1 dominant.",
        "scope_bau_note": "BAU comparable; transport mode unchanged between scenarios.",
    },
    "2": {
        "scope1_tco2": 250_000,
        "scope2_tco2": 30_000,
        "scope_source": "Inferred — West Africa truck transport benchmarks; IPCC transport emission factors",
        "scope_quality": "Low",
        "scope_notes": "Truck haulage from village to regional bulking depot and port/processing facility. Diesel trucks.",
        "scope_bau_note": "BAU comparable; bulk logistics mode unchanged.",
    },
    "3": {
        "scope1_tco2": 180_000,
        "scope2_tco2": 120_000,
        "scope_source": "Clarity/Cleo Value Chain Outline; Serious Shea BPlan V8 2023 — Serious Shea scenario (baseline)",
        "scope_quality": "Medium",
        "scope_notes": "Serious Shea scenario: 100% renewable processing. Residual S1 from generator backup and delivery transport.",
        "scope_bau_note": "BAU: 10.374 kg CO₂e/kg butter (firewood combustion). Serious Shea: <0.5187 kg CO₂e/kg (>95% reduction). Source: Clarity/Cleo outline.",
        "scope_bau_co2e_per_kg": 10.374,
        "scope_ss_co2e_per_kg": 0.5187,
    },
    "4": {
        "scope1_tco2": 520_000,
        "scope2_tco2": 40_000,
        "scope_source": "Inferred — ICCT freight transport benchmarks; IMO sea freight emission factors",
        "scope_quality": "Low",
        "scope_notes": "Container shipping (Dakar/Abidjan → EU ports) + inland truck. S1 from bunker fuel. EU CBAM adds cost from 2026.",
        "scope_bau_note": "BAU comparable; shipping route unchanged. EU Carbon Border Adjustment Mechanism adds cost from 2026.",
    },
    "5": {
        "scope1_tco2": 20_000,
        "scope2_tco2": 30_000,
        "scope_source": "Clarity/Cleo Value Chain Outline — Cleo Organics 100% renewable manufacturing",
        "scope_quality": "Medium",
        "scope_notes": "Cleo manufacturing 100% renewable. Minimal S1 (packaging, delivery). S2 near-zero (renewable electricity).",
        "scope_bau_note": "BAU conventional cosmetic manufacturer: ~5–8× higher emissions. Cleo is the best-practice benchmark.",
    },
    "6": {
        "scope1_tco2": 15_000,
        "scope2_tco2": 60_000,
        "scope_source": "Inferred — retail sector GHG Protocol benchmarks; European retail energy data",
        "scope_quality": "Low",
        "scope_notes": "Retail shelf, HVAC, lighting, point-of-sale. Urban European retail S2 dominant.",
        "scope_bau_note": "BAU conventional retail. Cleo online-heavy distribution reduces retail-floor footprint.",
    },
}


# ── Shea water data per phase ──────────────────────────────────────────────────
# Phase 3: boiling and washing in butter rendering.  Food science benchmarks
# (Olawale et al. 2020) document ~5-10 litres of water per kg shea butter.
# All other phases inferred; no water data exists in primary shea sources.

SHEA_WATER_DATA: dict[str, dict] = {
    "0": {
        "water": 0,
        "water_recycling_pct": 0,
        "water_quality": "Low",
        "water_source": "Negligible — rain-fed shea parkland, manual nut collection",
        "water_notes": "Shea trees are entirely rain-fed. Nut collection is manual. No process water.",
    },
    "1": {
        "water": 500,
        "water_recycling_pct": 0,
        "water_quality": "Low",
        "water_source": "Inferred — negligible; potable and washing use only",
        "water_notes": "Aggregation point sanitation and potable supply only. No process water.",
    },
    "2": {
        "water": 2_000,
        "water_recycling_pct": 0,
        "water_quality": "Low",
        "water_source": "Inferred — bulk storage depot operations",
        "water_notes": "Storage depot sanitation and dust control. Minimal process water.",
    },
    "3": {
        "water": 450_000,
        "water_recycling_pct": 20,
        "water_quality": "Medium",
        "water_source": "Inferred — shea processing food science benchmarks; Olawale et al. (2020) ~5-10 L/kg butter",
        "water_notes": "Boiling, washing, and phase separation in butter rendering. Traditional ~10 L/kg; Serious Shea mechanical ~5 L/kg. Limited recycling in field operations.",
    },
    "4": {
        "water": 1_000,
        "water_recycling_pct": 0,
        "water_quality": "Low",
        "water_source": "Inferred — export logistics operations",
        "water_notes": "Container depot and port operations. No process water; potable and cleaning only.",
    },
    "5": {
        "water": 80_000,
        "water_recycling_pct": 50,
        "water_quality": "Low",
        "water_source": "Inferred — EU cosmetic manufacturing benchmarks (~3-8 L/kg product)",
        "water_notes": "Emulsification, blending, filling line CIP cleaning. 50% recycling via closed-loop clean-in-place systems.",
    },
    "6": {
        "water": 500,
        "water_recycling_pct": 0,
        "water_quality": "Low",
        "water_source": "Negligible — retail/office use only",
        "water_notes": "Retail store sanitation only. No process water.",
    },
}


# ── Shea energy data per phase ─────────────────────────────────────────────────
# Phase 3 BAU: firewood thermal = 88 kWh/kg butter (20 kg × 4.4 kWh/kg wood).
# Phase 3 Serious Shea: 100% renewable electric mills; ~4.5 kWh/kg butter.
# Phase 5 Cleo: 100% renewable explicitly stated (Clarity/Cleo outline).
# WGC 2030 clean energy target (60%) used as benchmark — applies broadly to
# agri-food processing as well as mining.

SHEA_ENERGY_DATA: dict[str, dict] = {
    "0": {
        "energy": 200,
        "energy_unit": "kWh",
        "energy_clean_pct": 5,
        "energy_quality": "Low",
        "energy_source": "Inferred — manual collection, negligible motorised energy",
        "energy_notes": "Essentially human and animal energy. No mechanised collection in BAU or Serious Shea scenario.",
    },
    "1": {
        "energy": 2_000,
        "energy_unit": "kWh",
        "energy_clean_pct": 5,
        "energy_quality": "Low",
        "energy_source": "Inferred — rural West Africa transport; motorcycle and donkey cart",
        "energy_notes": "Motorcycle and donkey cart transport to aggregation points. ~95% diesel/animal energy.",
    },
    "2": {
        "energy": 15_000,
        "energy_unit": "kWh",
        "energy_clean_pct": 10,
        "energy_quality": "Low",
        "energy_source": "Inferred — diesel truck haulage West Africa; bulking depot generators",
        "energy_notes": "Diesel truck haulage between villages and depots. Small generators. Rural grid access ~38% nationally (Senegal).",
    },
    "3": {
        "energy": 95_000,
        "energy_unit": "kWh",
        "energy_clean_pct": 80,
        "energy_quality": "Medium",
        "energy_source": "Serious Shea BPlan V8 2023; Clarity/Cleo outline — Serious Shea scenario (100% renewable target)",
        "energy_notes": "Serious Shea: 100% renewable mechanical processing (electric mills, solar/biogas). BAU: firewood = 88 kWh/kg butter, 0% clean. 80% reflects near-target Serious Shea operational state.",
        "energy_bau_kwh_per_kg": 88.0,
        "energy_ss_kwh_per_kg": 4.5,
    },
    "4": {
        "energy": 180_000,
        "energy_unit": "kWh",
        "energy_clean_pct": 15,
        "energy_quality": "Low",
        "energy_source": "Inferred — ICCT sea freight; IMO 2023 emission factors",
        "energy_notes": "Container ship bunker fuel dominates. Port operations partially grid-powered. EU mandates clean-energy processing at destination.",
    },
    "5": {
        "energy": 35_000,
        "energy_unit": "kWh",
        "energy_clean_pct": 100,
        "energy_quality": "Medium",
        "energy_source": "Clarity/Cleo Value Chain Outline — Cleo Organics 100% renewable manufacturing",
        "energy_notes": "Cleo Organics 100% renewable energy for manufacturing. Explicitly stated in source. Best-practice benchmark for cosmetic manufacturing.",
    },
    "6": {
        "energy": 8_000,
        "energy_unit": "kWh",
        "energy_clean_pct": 65,
        "energy_quality": "Low",
        "energy_source": "Inferred — European retail sector energy benchmarks",
        "energy_notes": "European retail store HVAC and lighting. EU grid clean mix 40-65% by country. Cleo online-heavy model reduces store energy footprint.",
    },
}


def inject_shea_scope_emissions(target: dict) -> None:
    """Add Scope 1/2 baseline emissions to each shea phase (additive — never overwrites)."""
    target.setdefault("phases", {})
    for pid, data in SHEA_SCOPE_EMISSIONS.items():
        phase = target["phases"].setdefault(pid, {})
        for k, v in data.items():
            if k not in phase or phase[k] is None:
                phase[k] = v


def inject_shea_water_data(target: dict) -> None:
    """Add per-phase water data to shea phases (additive — never overwrites)."""
    target.setdefault("phases", {})
    for pid, data in SHEA_WATER_DATA.items():
        phase = target["phases"].setdefault(pid, {})
        for k, v in data.items():
            if k not in phase or phase[k] is None:
                phase[k] = v


def inject_shea_energy_data(target: dict) -> None:
    """Add per-phase energy data to shea phases (additive — never overwrites)."""
    target.setdefault("phases", {})
    for pid, data in SHEA_ENERGY_DATA.items():
        phase = target["phases"].setdefault(pid, {})
        for k, v in data.items():
            if k not in phase or phase[k] is None:
                phase[k] = v


def build_shea_ui(dry_run: bool = False):
    print("\n── Shea Supply Chain UI ──────────────────────────────────")

    target = load_json(SHEA_UI_JSON)
    if not target:
        print("  [NEW] No existing file; starting from scratch.")
        target = {}

    # ── Phase metadata ──────────────────────────────────────────────────────
    phases_csv = read_csv(SHEA_PHASES_CSV)
    if phases_csv:
        target.setdefault("phase_meta", {})
        for row in phases_csv:
            pid = str(row.get("phase_id", "")).strip()
            if not pid:
                continue
            target["phase_meta"].setdefault(pid, {})
            additive_merge(target["phase_meta"][pid], {
                "name":             row.get("phase_name", "").strip(),
                "transparency":     row.get("transparency_level", "").strip() or "OPAQUE",
                "physical_state":   row.get("physical_state", "").strip(),
                "transformation":   row.get("primary_transformation", "").strip(),
            })

    # ── Metrics CSV grouped by phase ─────────────────────────────────────────
    metrics_rows = read_csv(SHEA_METRICS_CSV)
    by_phase: dict[str, list] = defaultdict(list)
    for row in metrics_rows:
        pid = str(row.get("phase_id", "")).strip()
        by_phase[pid].append(row)

    target.setdefault("phases", {})
    for pid, rows in by_phase.items():
        target["phases"].setdefault(pid, {})
        phase_obj = target["phases"][pid]
        phase_obj.setdefault("metrics", {})
        for row in rows:
            mname = row.get("metric_name", "").strip()
            mval  = row.get("metric_value")
            munit = row.get("unit", "")
            msrc  = row.get("source_name", "")
            mnote = row.get("notes", "")
            if not mname:
                continue
            if mname not in phase_obj["metrics"]:
                entry = {"unit": munit, "source": msrc}
                fv = parse_float(mval)
                if fv is not None:
                    entry["value"] = fv
                elif mval:
                    entry["value"] = mval
                else:
                    entry["value"] = None
                if mnote:
                    entry["note"] = mnote[:120]
                phase_obj["metrics"][mname] = entry
            else:
                # Additive: update source/note if missing
                existing = phase_obj["metrics"][mname]
                if not existing.get("source") and msrc:
                    existing["source"] = msrc
                if not existing.get("note") and mnote:
                    existing["note"] = mnote[:120]

    # ── Sources (as reference only) ──────────────────────────────────────────
    sources = read_csv(SHEA_SOURCES_CSV)
    if sources:
        source_index = {r.get("source_id", ""): r.get("source_name", "") for r in sources}
        target["_source_index"] = source_index

    # ── Scope 1/2 emissions per phase ─────────────────────────────────────────
    inject_shea_scope_emissions(target)

    # ── Water data per phase ───────────────────────────────────────────────────
    inject_shea_water_data(target)

    # ── Energy data per phase ──────────────────────────────────────────────────
    inject_shea_energy_data(target)

    # ── Update _meta ─────────────────────────────────────────────────────────
    target["_meta"] = {
        "generated": NOW,
        "generator": "src/api/generate_ui_data.py",
        "sources": [
            str(SHEA_METRICS_CSV.relative_to(REPO)),
            str(SHEA_PHASES_CSV.relative_to(REPO)),
            str(SHEA_SOURCES_CSV.relative_to(REPO)),
            "SHEA_SCOPE_EMISSIONS constant (see generator — Clarity/Cleo outline, Serious Shea BPlan V8 2023)",
            "SHEA_WATER_DATA constant (see generator — food science benchmarks, Olawale et al. 2020)",
            "SHEA_ENERGY_DATA constant (see generator — Clarity/Cleo outline, Serious Shea BPlan V8 2023)",
        ],
        "note": "Auto-generated. Re-run src/api/generate_ui_data.py to refresh. "
                "Fields under 'overrides' are never modified.",
    }

    save_json(SHEA_UI_JSON, target, dry_run)
    print(f"  Phases found in CSV metrics: {sorted(by_phase.keys(), key=lambda x: int(x) if x.isdigit() else 99)}")


# ── Value Chain Environmental Cost Layer ──────────────────────────────────────

_GOLD_PHASE_NAMES = {
    "0": "Exploration & Geology",
    "1": "Mine Extraction",
    "2": "Ore Processing",
    "3": "Smelting & Doré",
    "4": "Refining",
    "5": "Assay & Certification",
    "6": "Logistics & Transport",
    "7": "Exchange Registration",
    "8": "End Use & Fabrication",
}

_SHEA_PHASE_NAMES = {
    "0": "Shea Tree Ecology",
    "1": "Nut Harvesting",
    "2": "Primary Processing",
    "3": "Extraction (Processing)",
    "4": "Logistics & Export",
    "5": "Manufacturing (Cleo)",
    "6": "Retail & End Use",
}

# Reference unit-cost parameters for the value chain layer.
# These are NOT stored in the supply chain JSON — they belong to the value layer.
GOLD_VC_PARAMS = {
    "carbon_price_usd_per_tco2": 65.0,    # EU ETS 2024 reference
    "energy_tariff_usd_per_kwh": 0.12,    # industrial grid
    "water_rate_usd_per_litre": 0.002,    # industrial supply
    "ref_production_oz_per_year": 106_100_000,  # ~3,300 MT global mine supply
    "baseline_aisc_usd_per_oz": 1385.0,   # seed value from value_metrics.json
}

SHEA_VC_PARAMS = {
    "carbon_price_usd_per_tco2": 12.0,    # VCM nature-based credits
    "energy_tariff_usd_per_kwh": 0.08,    # West Africa industrial
    "water_rate_usd_per_litre": 0.001,    # West Africa supply
    "ref_production_kg_per_year": 1_000_000,   # 1,000 MT Serious Shea reference
    "baseline_price_women_usd_per_mt": 4000.0,
    "bau_co2e_kg_per_kg": 10.374,    # Clarity/Cleo outline
    "ss_co2e_kg_per_kg": 0.5187,     # Clarity/Cleo outline (<5% of BAU)
}


def build_gold_value_chain_ui(dry_run: bool = False):
    """
    Build gold_value_chain_ui.json: translates supply chain physical quantities
    (tCO₂, kWh, litres) into financial cost components for the value chain layer.

    Physical source: gold_supply_chain_ui.json (unchanged).
    Output:          data/frontend/gold_value_chain_ui.json (new file, value layer).
    """
    p = GOLD_VC_PARAMS

    with open(GOLD_UI_JSON) as f:
        sc = json.load(f)
    sc_phases = sc.get("phases", {}).get("synthetic", {})

    phases = {}
    cumulative_s1 = 0.0
    cumulative_s2 = 0.0

    for pid in [str(i) for i in range(9)]:
        sp = sc_phases.get(pid, {})

        s1 = float(sp.get("scope1_tco2", 0) or 0)
        s2 = float(sp.get("scope2_tco2", 0) or 0)
        energy_kwh = float(sp.get("energy", 0) or 0)
        water_l = float(sp.get("water", 0) or 0)

        carbon_cost = (s1 + s2) * p["carbon_price_usd_per_tco2"]
        energy_cost = energy_kwh * p["energy_tariff_usd_per_kwh"]
        water_cost = water_l * p["water_rate_usd_per_litre"]
        total_env = carbon_cost + energy_cost + water_cost

        ref_oz = p["ref_production_oz_per_year"]
        carbon_per_oz = carbon_cost / ref_oz
        energy_per_oz = energy_cost / ref_oz
        water_per_oz = water_cost / ref_oz
        total_per_oz = total_env / ref_oz

        env_pct_aisc = (total_per_oz / p["baseline_aisc_usd_per_oz"]) * 100.0

        # Scope 3 cascade: upstream S1+S2 becomes this phase's inherited Scope 3
        scope3_upstream = cumulative_s1 + cumulative_s2
        scope3_liability_usd = scope3_upstream * p["carbon_price_usd_per_tco2"]

        phases[pid] = {
            "name": _GOLD_PHASE_NAMES.get(pid, f"Phase {pid}"),
            "scope1_tco2": s1,
            "scope2_tco2": s2,
            "scope3_upstream_tco2": round(scope3_upstream),
            "energy_kwh": energy_kwh,
            "water_litres": water_l,
            "energy_clean_pct": sp.get("energy_clean_pct", 0),
            "water_recycling_pct": sp.get("water_recycling_pct", 0),
            "d_value": sp.get("D"),
            "c_value": sp.get("C"),
            "balance": sp.get("balance"),
            # ── Cost outputs (at reference parameters) ──
            "carbon_cost_usd": round(carbon_cost),
            "energy_cost_usd": round(energy_cost),
            "water_cost_usd": round(water_cost),
            "total_env_cost_usd": round(total_env),
            "scope3_liability_usd": round(scope3_liability_usd),
            "carbon_cost_per_oz": round(carbon_per_oz, 4),
            "energy_cost_per_oz": round(energy_per_oz, 6),
            "water_cost_per_oz": round(water_per_oz, 6),
            "total_env_cost_per_oz": round(total_per_oz, 4),
            "env_pct_of_aisc": round(env_pct_aisc, 3),
        }

        cumulative_s1 += s1
        cumulative_s2 += s2

    total_chain_tco2 = sum(
        phases[pid]["scope1_tco2"] + phases[pid]["scope2_tco2"] for pid in phases
    )
    total_chain_env_usd = sum(phases[pid]["total_env_cost_usd"] for pid in phases)
    total_chain_per_oz = total_chain_env_usd / p["ref_production_oz_per_year"]

    result = {
        "_meta": {
            "generated_at": NOW,
            "version": "1.0",
            "description": (
                "Gold value chain environmental cost layer. "
                "Physical quantities sourced from gold_supply_chain_ui.json (supply chain layer, unchanged). "
                "Costs derived by applying reference unit-cost parameters."
            ),
            "sources": ["gold_supply_chain_ui.json (physical quantities — supply chain layer)"],
            "parameters": p,
            "chain_totals": {
                "total_scope1_tco2": sum(phases[pid]["scope1_tco2"] for pid in phases),
                "total_scope2_tco2": sum(phases[pid]["scope2_tco2"] for pid in phases),
                "total_chain_tco2": round(total_chain_tco2),
                "total_env_cost_usd": round(total_chain_env_usd),
                "total_env_cost_per_oz": round(total_chain_per_oz, 4),
                "env_pct_of_aisc": round(
                    total_chain_per_oz / p["baseline_aisc_usd_per_oz"] * 100, 3
                ),
            },
            "note": (
                "Re-run generate_ui_data.py to refresh. Carbon price, energy tariff, and water rate "
                "are reference parameters — use the value chain simulators to vary them dynamically."
            ),
        },
        "phases": phases,
    }

    save_json(GOLD_VC_UI_JSON, result, dry_run)
    print(f"  ✓ gold_value_chain_ui.json written ({len(phases)} phases, "
          f"total env cost ${total_chain_env_usd/1e9:.2f}B, "
          f"${total_chain_per_oz:.2f}/oz, "
          f"{total_chain_per_oz / p['baseline_aisc_usd_per_oz'] * 100:.2f}% AISC)")


def build_shea_value_chain_ui(dry_run: bool = False):
    """
    Build shea_value_chain_ui.json: translates shea supply chain physical quantities
    into value chain financial cost components including carbon credit revenue
    from the Serious Shea scenario.

    Physical source: shea_supply_chain_ui.json (unchanged).
    Output:          data/frontend/shea_value_chain_ui.json (new file, value layer).
    """
    p = SHEA_VC_PARAMS

    with open(SHEA_UI_JSON) as f:
        sc = json.load(f)
    sc_phases = sc.get("phases", {})

    # Carbon credit calculation (Serious Shea Phase 3)
    bau_co2e = p["bau_co2e_kg_per_kg"]      # 10.374 kg CO₂e/kg butter
    ss_co2e = p["ss_co2e_kg_per_kg"]         # 0.5187 kg CO₂e/kg butter
    co2e_saved_per_kg = bau_co2e - ss_co2e  # 9.8553 kg CO₂e saved per kg
    # tCO₂e saved per MT × carbon price = USD credit revenue per MT
    carbon_credit_per_mt = co2e_saved_per_kg * p["carbon_price_usd_per_tco2"]  # kg→tCO₂e ratio = 1/1000 * 1000 MT = 1:1
    carbon_credit_per_kg = carbon_credit_per_mt / 1000.0

    phases = {}
    cumulative_s1 = 0.0
    cumulative_s2 = 0.0

    for pid in [str(i) for i in range(7)]:
        sp = sc_phases.get(pid, {})

        s1 = float(sp.get("scope1_tco2", 0) or 0)
        s2 = float(sp.get("scope2_tco2", 0) or 0)
        energy_kwh = float(sp.get("energy", 0) or 0)
        water_l = float(sp.get("water", 0) or 0)

        carbon_cost = (s1 + s2) * p["carbon_price_usd_per_tco2"]
        energy_cost = energy_kwh * p["energy_tariff_usd_per_kwh"]
        water_cost = water_l * p["water_rate_usd_per_litre"]
        total_env = carbon_cost + energy_cost + water_cost

        ref_kg = p["ref_production_kg_per_year"]
        carbon_per_kg = carbon_cost / ref_kg
        energy_per_kg = energy_cost / ref_kg
        water_per_kg = water_cost / ref_kg
        total_per_kg = total_env / ref_kg

        scope3_upstream = cumulative_s1 + cumulative_s2

        phase_data = {
            "name": _SHEA_PHASE_NAMES.get(pid, f"Phase {pid}"),
            "scope1_tco2": s1,
            "scope2_tco2": s2,
            "scope3_upstream_tco2": round(scope3_upstream),
            "energy_kwh": energy_kwh,
            "water_litres": water_l,
            "energy_clean_pct": sp.get("energy_clean_pct", 0),
            "water_recycling_pct": sp.get("water_recycling_pct", 0),
            "d_value": sp.get("D"),
            "c_value": sp.get("C"),
            "balance": sp.get("balance"),
            # ── Cost outputs (at reference parameters) ──
            "carbon_cost_usd": round(carbon_cost),
            "energy_cost_usd": round(energy_cost),
            "water_cost_usd": round(water_cost),
            "total_env_cost_usd": round(total_env),
            "carbon_cost_per_kg": round(carbon_per_kg, 6),
            "energy_cost_per_kg": round(energy_per_kg, 6),
            "water_cost_per_kg": round(water_per_kg, 6),
            "total_env_cost_per_kg": round(total_per_kg, 6),
        }

        # Phase 3: add Serious Shea carbon credit data
        if pid == "3":
            phase_data.update({
                "bau_co2e_kg_per_kg": bau_co2e,
                "ss_co2e_kg_per_kg": ss_co2e,
                "co2e_saved_per_kg": round(co2e_saved_per_kg, 4),
                "carbon_credit_usd_per_mt": round(carbon_credit_per_mt, 2),
                "carbon_credit_usd_per_kg": round(carbon_credit_per_kg, 6),
                "bau_carbon_cost_per_kg": round(bau_co2e / 1000 * p["carbon_price_usd_per_tco2"], 6),
                "ss_carbon_cost_per_kg": round(ss_co2e / 1000 * p["carbon_price_usd_per_tco2"], 6),
            })

        phases[pid] = phase_data
        cumulative_s1 += s1
        cumulative_s2 += s2

    # Annual carbon credit revenue (at reference 1,000 MT production)
    annual_credit_rev = carbon_credit_per_mt * (p["ref_production_kg_per_year"] / 1000)

    result = {
        "_meta": {
            "generated_at": NOW,
            "version": "1.0",
            "description": (
                "Shea value chain environmental cost layer. "
                "Physical quantities from shea_supply_chain_ui.json. "
                "Includes Serious Shea carbon credit revenue opportunity for Phase 3."
            ),
            "sources": ["shea_supply_chain_ui.json (physical quantities — supply chain layer)"],
            "parameters": p,
            "serious_shea_carbon_credit": {
                "bau_co2e_kg_per_kg": bau_co2e,
                "ss_co2e_kg_per_kg": ss_co2e,
                "co2e_saved_per_kg": round(co2e_saved_per_kg, 4),
                "carbon_credit_usd_per_mt": round(carbon_credit_per_mt, 2),
                "annual_credit_revenue_usd_at_1000mt": round(annual_credit_rev),
                "note": (
                    f"At ${p['carbon_price_usd_per_tco2']}/tCO₂e VCM price, "
                    f"Serious Shea generates ${carbon_credit_per_mt:.2f}/MT carbon credit revenue vs BAU. "
                    f"At 1,000 MT/year: ${annual_credit_rev:,.0f}/year."
                ),
            },
            "chain_totals": {
                "total_scope1_tco2": sum(phases[pid]["scope1_tco2"] for pid in phases),
                "total_scope2_tco2": sum(phases[pid]["scope2_tco2"] for pid in phases),
                "total_env_cost_usd": sum(phases[pid]["total_env_cost_usd"] for pid in phases),
            },
        },
        "phases": phases,
    }

    save_json(SHEA_VC_UI_JSON, result, dry_run)
    print(f"  ✓ shea_value_chain_ui.json written ({len(phases)} phases, "
          f"carbon credit ${carbon_credit_per_mt:.2f}/MT, "
          f"${annual_credit_rev:,.0f}/yr at 1,000 MT)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate UI JSON from supply chain data sources.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be written without writing.")
    parser.add_argument("--gold-only", action="store_true")
    parser.add_argument("--shea-only", action="store_true")
    args = parser.parse_args()

    print(f"generate_ui_data.py  [{NOW}]")
    print(f"Repo root: {REPO}")

    if args.shea_only:
        build_shea_ui(args.dry_run)
        build_shea_value_chain_ui(args.dry_run)
    elif args.gold_only:
        build_gold_ui(args.dry_run)
        build_gold_value_chain_ui(args.dry_run)
    else:
        build_gold_ui(args.dry_run)
        build_gold_value_chain_ui(args.dry_run)
        build_shea_ui(args.dry_run)
        build_shea_value_chain_ui(args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
