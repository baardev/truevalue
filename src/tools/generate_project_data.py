#!/usr/bin/env python3
"""
generate_project_data.py
========================
Reads a completed PDI YAML instance and generates all data files for a project
under frontend/project/<material>/.

Usage:
    python src/tools/generate_project_data.py \
        --pdi frontend/docs/PDI/PDI_water_newwater_2026.yaml \
        --material water_newwater

    python src/tools/generate_project_data.py \
        --pdi frontend/docs/PDI/PDI_water_ocwd_2026.yaml \
        --material water_ocwd

Outputs (all under frontend/project/<material>/):
    data/sources_registry.json
    data/schema/water_supply_chain_phases.csv
    data/processed/<material>_supply_chain_ui.json
    data/processed/<material>_value_chain_ui.json
    data/processed/<material>_value_metrics.json
    data/processed/<material>_value_ndc_metrics.json
    supply_chain/scenarios.json

D/C/N derivation formula (from .cursor/rules/pdi-to-html-pipeline.mdc):
    D_flags  = B3 + B4 + B6  (definition/constraint signals)
    C_flags  = B9 + B11       (contribution/integration signals)
    opacity  = module_4_opacity[phase].opacity_score  (0-4)
    boundary_score = sum of B3/B4/B6/B9/B10/B11 flags

    D = 200 + (D_flags x 20) + (boundary_score x 4)
    C = 200 + (C_flags x 20) + (opacity x 8)
    balance:
        high   -> 90 + random(-4, +4)
        medium -> 83 + random(-4, +4)
        low    -> 70 + random(-4, +4)
    N = round((D + C) / 2 * (balance / 100))

    For Phase 0 (pre-commercial):
        D = 220
        C = 180 + opacity * 5
        balance per transparency tier as above
"""

import argparse
import csv
import json
import math
import os
import random
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Colour themes per material slug
# ---------------------------------------------------------------------------
THEMES = {
    "water_newwater": {
        "primary": "#00897b",
        "dark": "#004d40",
        "darker": "#00251a",
        "emoji": "🇸🇬",
        "title": "Singapore NEWater",
        "subtitle": "PUB full water cycle — single-actor institutional model",
    },
    "water_ocwd": {
        "primary": "#1976d2",
        "dark": "#0d47a1",
        "darker": "#002171",
        "emoji": "💧",
        "title": "Orange County GWRS",
        "subtitle": "OCWD full water cycle — fragmented institutional model",
    },
}

DEFAULT_THEME = {
    "primary": "#455a64",
    "dark": "#263238",
    "darker": "#000a12",
    "emoji": "💧",
    "title": "",
    "subtitle": "",
}

# ---------------------------------------------------------------------------
# Value metric definitions for water recycling projects
# ---------------------------------------------------------------------------
WATER_VALUE_METRICS = [
    {"metric_name": "treatment_cost_usd_per_m3", "label": "Treatment Cost", "unit": "USD/m³"},
    {"metric_name": "water_recovery_pct", "label": "Water Recovery Rate", "unit": "%"},
    {"metric_name": "recycling_share_pct", "label": "Recycling Share of Supply", "unit": "%"},
    {"metric_name": "energy_kwh_per_m3", "label": "Energy Intensity", "unit": "kWh/m³"},
    {"metric_name": "leakage_pct", "label": "System Leakage (NRW)", "unit": "%"},
    {"metric_name": "capex_usd_per_m3_capacity", "label": "Capital Cost per m³ Capacity", "unit": "USD/m³/day"},
]

# ---------------------------------------------------------------------------
# Per-material value metric baseline values (from PDI YAML analyst notes)
# ---------------------------------------------------------------------------
VALUE_BASELINES = {
    "water_newwater": {
        "treatment_cost_usd_per_m3":  {"value": 0.88, "source": "OECD (2012); PUB tariff structure analysis"},
        "water_recovery_pct":          {"value": 75.0, "source": "PUB Annual Report FY2023-24 (plant-level recovery)"},
        "recycling_share_pct":         {"value": 40.0, "source": "PUB Annual Report FY2023-24 (~40% of national supply)"},
        "energy_kwh_per_m3":           {"value": 3.5,  "source": "PUB Annual Report FY2023-24; WateReuse Association (2022)"},
        "leakage_pct":                 {"value": 4.5,  "source": "PUB Annual Report FY2023-24 (non-revenue water 4.5%)"},
        "capex_usd_per_m3_capacity":   {"value": 2100, "source": "Industry estimate; PUB does not publish disaggregated capex"},
    },
    "water_ocwd": {
        "treatment_cost_usd_per_m3":  {"value": 1.25, "source": "OCWD Annual Report FY2023-24 (operational cost data)"},
        "water_recovery_pct":          {"value": 85.0, "source": "OCWD GWRS System Fact Sheet (MF recovery ~90%; RO ~85% net)"},
        "recycling_share_pct":         {"value": 35.0, "source": "OCWD Annual Report FY2023-24 (~35% of basin replenishment from GWRS)"},
        "energy_kwh_per_m3":           {"value": 4.2,  "source": "OCWD Annual Report FY2023-24; Leverenz et al. (2011)"},
        "leakage_pct":                 {"value": 9.0,  "source": "CDWR benchmarks; estimated 8-10% NRW across OC agencies"},
        "capex_usd_per_m3_capacity":   {"value": 3700, "source": "Industry estimate ~USD 480M / 130 MGD; OCWD capital programme data"},
    },
}


def load_pdi(pdi_path: Path) -> dict:
    """Load and parse a PDI YAML file."""
    with open(pdi_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["pdi"]


def get_event_by_number(events: list, number: int) -> dict | None:
    for e in events:
        if e.get("event_number") == number:
            return e
    return None


def get_opacity_by_phase(opacity_list: list, phase_number: int) -> dict | None:
    for o in opacity_list:
        if o.get("phase") == phase_number:
            return o
    return None


def derive_balance(transparency: str, seed: int | None = None) -> float:
    """Derive balance score from transparency tier with small random offset."""
    rng = random.Random(seed)
    offsets = {
        "high":   (90.0, 4.0),
        "medium": (83.0, 4.0),
        "low":    (70.0, 4.0),
    }
    base, spread = offsets.get(transparency, (80.0, 4.0))
    return round(base + rng.uniform(-spread, spread), 1)


def derive_ndc(phase_number: int, event: dict, opacity_record: dict) -> dict:
    """
    Derive D, C, N, balance, sustainability for a phase using the PDI pipeline formula.
    """
    opacity_score = opacity_record.get("opacity_score", 0)
    transparency = opacity_record.get("transparency", "medium").lower()

    if phase_number == 0:
        D = 220
        C = 180 + opacity_score * 5
    else:
        b3 = 1 if event.get("B3_physical_state_changes") is True else 0
        b4 = 1 if event.get("B4_unit_changes") is True else 0
        b6 = 1 if event.get("B6_process_class_changes") is True else 0
        b9 = 1 if event.get("B9_custody_changes") is True else 0
        b10 = 1 if event.get("B10_ownership_changes") is True else 0
        b11 = 1 if event.get("B11_output_defined") is True else 0

        d_flags = b3 + b4 + b6
        c_flags = b9 + b11
        boundary_score = event.get("boundary_score", b3 + b4 + b6 + b9 + b10 + b11)

        D = 200 + (d_flags * 20) + (boundary_score * 4)
        C = 200 + (c_flags * 20) + (opacity_score * 8)

    balance = derive_balance(transparency, seed=phase_number * 17)
    N = round((D + C) / 2 * (balance / 100))

    # Sustainability: ratio of balance to ideal (100); N relative to theoretical max
    sustainability = round((balance / 100) * (N / 290), 3)

    return {
        "D": D,
        "C": C,
        "balance": balance,
        "N": N,
        "sustainability": sustainability,
    }


def build_supply_chain_ui(pdi: dict, material: str) -> dict:
    """Build <material>_supply_chain_ui.json from PDI data."""
    today = date.today().isoformat()
    events = pdi.get("module_2_events", [])
    phase_map = pdi.get("module_3", {}).get("phase_map", [])
    opacity_list = pdi.get("module_4_opacity", [])
    sources_overview = pdi.get("sources_overview", "")
    summary = pdi.get("summary", {})

    phases_out = {}
    phase_meta_out = {}

    for pm in phase_map:
        phase_num = pm["phase"]
        event_num = pm.get("begins_at_event")
        event = get_event_by_number(events, event_num) if event_num else {}
        opacity_record = get_opacity_by_phase(opacity_list, phase_num) or {}

        ndc = derive_ndc(phase_num, event or {}, opacity_record)

        # Phase summary row from PDI summary table
        summary_row = next(
            (r for r in summary.get("phase_summary_table", []) if r.get("phase") == phase_num),
            {},
        )

        transparency = opacity_record.get("transparency", "medium").lower()
        phases_out[str(phase_num)] = {
            **ndc,
            "notes": pm.get("tvpci_notes", summary_row.get("child_n_output", "")),
            "data_quality": "high" if transparency == "high" else ("medium" if transparency == "medium" else "low"),
            "scope1_tco2": None,
            "scope2_tco2": None,
            "scope_source": "Not provided — requires separate data input",
            "scope_quality": "No data",
            "water": None,
            "energy": None,
            "water_recycling_pct": None,
            "energy_clean_pct": None,
        }

        phase_meta_out[str(phase_num)] = {
            "name": pm["name"],
            "transparency": transparency.upper(),
            "transformation": summary_row.get("physical_state_out", ""),
        }

    # System-level balance
    all_balances = [v["balance"] for v in phases_out.values()]
    system_balance = round(sum(all_balances) / len(all_balances), 1) if all_balances else 0.0

    # Source list from overview
    source_lines = [s.strip() for s in sources_overview.strip().splitlines() if s.strip()]

    return {
        "_meta": {
            "generated": today,
            "generator": "src/tools/generate_project_data.py",
            "material": material,
            "sources": source_lines,
            "note": "Generated from PDI YAML. Re-run generate_project_data.py to refresh.",
        },
        "entities": {
            "synthetic": {
                "label": pdi.get("analyst", "PDI Synthetic"),
                "description": f"Generated from PDI YAML for {material}",
            }
        },
        "phase_meta": phase_meta_out,
        "phases": {
            "synthetic": phases_out,
        },
        "system": {
            "synthetic": {
                "balance": system_balance,
                "water_recycling_pct": None,
                "waste_circularity_pct": None,
                "clean_energy_pct": None,
            }
        },
    }


def build_scenarios(phases_data: dict) -> dict:
    """Build scenarios.json from base N values."""
    base_ns = [int(v["N"]) for v in phases_data.values()]
    phase_count = len(base_ns)

    def cap(val):
        return min(int(val), 290)

    def scenario(name, transform_fn):
        return {"name": name, "n_values": [cap(transform_fn(i, n)) for i, n in enumerate(base_ns)]}

    return {
        "scenarios": [
            scenario("current",    lambda i, n: n),
            scenario("optimum",    lambda i, n: n * 1.08),
            scenario("shock_1",    lambda i, n: n * 0.65 if i == 3 else n * 0.92),
            scenario("shock_2",    lambda i, n: n * 0.60 if i in (5, 6) else n * 0.90),
            scenario("expansion",  lambda i, n: n * 1.05),
            scenario("regulatory", lambda i, n: n * 1.15 if i == 4 else (n * 0.80 if i == 6 else n)),
        ],
        "phase_count": phase_count,
        "_meta": {"generated": date.today().isoformat()},
    }


def build_value_chain_ui(material: str, supply_ui: dict) -> dict:
    """Build <material>_value_chain_ui.json."""
    baselines = VALUE_BASELINES.get(material, {})
    today = date.today().isoformat()
    phases_data = supply_ui["phases"]["synthetic"]

    metrics_out = {}
    for m in WATER_VALUE_METRICS:
        slug = m["metric_name"]
        baseline = baselines.get(slug, {})
        metrics_out[slug] = {
            "label": m["label"],
            "unit": m["unit"],
            "value": baseline.get("value"),
            "source": baseline.get("source", "UNKNOWN"),
        }

    return {
        "_meta": {
            "generated": today,
            "generator": "src/tools/generate_project_data.py",
            "material": material,
            "note": "Value chain data for water recycling. Metrics are treatment cost, recovery, recycling share, energy, leakage.",
        },
        "metrics": metrics_out,
        "phases": {
            str(k): {
                "D": v["D"],
                "C": v["C"],
                "N": v["N"],
                "balance": v["balance"],
            }
            for k, v in phases_data.items()
        },
    }


def build_value_metrics(material: str) -> list:
    """Build <material>_value_metrics.json — time-series style records (365 days)."""
    baselines = VALUE_BASELINES.get(material, {})
    today = date.today()
    records = []
    rng = random.Random(42)

    for day_offset in range(365):
        record_date = date(today.year - 1, 1, 1)
        record_date = date(record_date.year, record_date.month, record_date.day)
        # Simple day offset
        from datetime import timedelta
        record_date = date(today.year - 1, 1, 1) + timedelta(days=day_offset)

        for m in WATER_VALUE_METRICS:
            slug = m["metric_name"]
            baseline = baselines.get(slug, {})
            base_val = baseline.get("value", 0) or 0
            noise = rng.gauss(0, base_val * 0.08) if base_val else 0
            records.append({
                "record_id": f"{material}_{slug}_{day_offset:04d}",
                "phase_id": 8,  # Advanced treatment is the key phase for water value metrics
                "entity": "synthetic",
                "date": record_date.isoformat(),
                "metric_name": slug,
                "metric_label": m["label"],
                "value": round(base_val + noise, 4),
                "unit": m["unit"],
                "source_type": "simulated",
                "source_name": baseline.get("source", "PDI Synthetic Generator"),
            })

    return records


def build_value_ndc_metrics(material: str, supply_ui: dict) -> list:
    """Build <material>_value_ndc_metrics.json — D/C/N per phase per day (365 days)."""
    phases_data = supply_ui["phases"]["synthetic"]
    today = date.today()
    records = []
    rng = random.Random(99)
    from datetime import timedelta

    for day_offset in range(365):
        record_date = date(today.year - 1, 1, 1) + timedelta(days=day_offset)
        for phase_str, vals in phases_data.items():
            for metric_name, base_val in [("d_value", vals["D"]), ("c_value", vals["C"]), ("n_value", vals["N"])]:
                noise = rng.gauss(0, base_val * 0.03)
                records.append({
                    "record_id": f"{material}_ph{phase_str}_{metric_name}_{day_offset:04d}",
                    "phase_id": int(phase_str),
                    "entity": "synthetic",
                    "date": record_date.isoformat(),
                    "metric_name": metric_name,
                    "value": round(base_val + noise, 2),
                    "unit": "index",
                    "source_type": "simulated",
                    "source_name": "PDI Synthetic Generator",
                })

    return records


def build_sources_registry(pdi: dict) -> list:
    """Build sources_registry.json from PDI sources_overview and event sources."""
    sources_overview = pdi.get("sources_overview", "")
    source_lines = [s.strip() for s in sources_overview.strip().splitlines() if s.strip()]
    events = pdi.get("module_2_events", [])

    registry = []
    for i, line in enumerate(source_lines):
        registry.append({
            "source_id": f"S{i+1:02d}",
            "short_name": line[:80],
            "full_citation": line,
            "url": "",
            "source_type": "public",
            "phases_cited": [],
            "metrics_cited": [],
            "access_date": "2026-04",
        })

    # Tag event sources
    event_source_map = {}
    for event in events:
        event_src = event.get("sources", "")
        if event_src:
            for reg in registry:
                if any(word in event_src for word in reg["short_name"].split()[:3] if len(word) > 4):
                    phase_guesses = []
                    # Map event to phase via phase_map
                    registry_entry = reg
                    # Just note the event number
                    reg.setdefault("events_cited", [])
                    if event.get("event_number") not in reg["events_cited"]:
                        reg["events_cited"].append(event.get("event_number"))

    return registry


def build_phases_csv(pdi: dict) -> list[dict]:
    """Build water_supply_chain_phases.csv content."""
    phase_map = pdi.get("module_3", {}).get("phase_map", [])
    opacity_list = pdi.get("module_4_opacity", [])
    summary = pdi.get("summary", {})

    rows = []
    for pm in phase_map:
        phase_num = pm["phase"]
        opacity_record = get_opacity_by_phase(opacity_list, phase_num) or {}
        summary_row = next(
            (r for r in summary.get("phase_summary_table", []) if r.get("phase") == phase_num),
            {},
        )
        rows.append({
            "phase_id": phase_num,
            "phase_name": pm["name"],
            "physical_state_in": summary_row.get("physical_state_in", ""),
            "physical_state_out": summary_row.get("physical_state_out", ""),
            "custodian_class": summary_row.get("custodian_class", ""),
            "transparency_level": opacity_record.get("transparency", "medium"),
            "opacity_score": opacity_record.get("opacity_score", 0),
            "child_n_output": pm.get("child_n_output", ""),
        })
    return rows


def validate_output(supply_ui: dict, material: str):
    """Basic validation of generated supply chain UI JSON."""
    phases = supply_ui.get("phases", {}).get("synthetic", {})
    errors = []

    if not phases:
        errors.append("No phases generated")
        return errors

    for phase_str, vals in phases.items():
        for field in ("D", "C", "N", "balance"):
            if vals.get(field) is None:
                errors.append(f"Phase {phase_str}: null {field}")
        if vals.get("N", 0) <= 0:
            errors.append(f"Phase {phase_str}: N must be positive")
        if not (0 < vals.get("balance", 0) <= 100):
            errors.append(f"Phase {phase_str}: balance out of range")

    if len(phases) < 5:
        errors.append(f"Only {len(phases)} phases — minimum is 5 (PDI rule)")

    return errors


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  wrote: {path}")


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  wrote: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate project data files from a completed PDI YAML instance."
    )
    parser.add_argument("--pdi", required=True, help="Path to PDI YAML file")
    parser.add_argument("--material", required=True, help="Material slug (e.g. water_newwater)")
    parser.add_argument("--repo-root", default=None, help="Repo root path (auto-detected if omitted)")
    args = parser.parse_args()

    # Resolve paths
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        # Auto-detect: walk up from this script until we find index.html
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir
        for _ in range(5):
            if (repo_root / "index.html").exists():
                break
            repo_root = repo_root.parent

    pdi_path = Path(args.pdi).resolve() if Path(args.pdi).is_absolute() else repo_root / args.pdi
    material = args.material
    project_dir = repo_root / "frontend" / "project" / material

    print(f"\n=== generate_project_data.py ===")
    print(f"  PDI:      {pdi_path}")
    print(f"  material: {material}")
    print(f"  output:   {project_dir}")
    print()

    # Load PDI
    if not pdi_path.exists():
        print(f"ERROR: PDI file not found: {pdi_path}")
        sys.exit(1)

    pdi = load_pdi(pdi_path)
    print(f"  loaded PDI: {pdi.get('material')} ({len(pdi.get('module_3', {}).get('phase_map', []))} phases)")

    # Ensure output directories
    processed_dir = project_dir / "data" / "processed"
    schema_dir = project_dir / "data" / "schema"
    supply_chain_dir = project_dir / "supply_chain"
    for d in (processed_dir, schema_dir, supply_chain_dir):
        ensure_dir(d)

    # 1. Sources registry
    print("\n[1] Building sources_registry.json")
    sources_registry = build_sources_registry(pdi)
    write_json(project_dir / "data" / "sources_registry.json", sources_registry)

    # 2. Supply chain phases CSV
    print("\n[2] Building water_supply_chain_phases.csv")
    phases_csv_rows = build_phases_csv(pdi)
    write_csv(schema_dir / "water_supply_chain_phases.csv", phases_csv_rows)

    # 3. Supply chain UI JSON
    print("\n[3] Building supply_chain_ui.json")
    supply_ui = build_supply_chain_ui(pdi, material)

    errors = validate_output(supply_ui, material)
    if errors:
        print("  VALIDATION ERRORS:")
        for e in errors:
            print(f"    - {e}")
        sys.exit(1)
    else:
        print(f"  validation OK: {len(supply_ui['phases']['synthetic'])} phases")

    write_json(processed_dir / f"{material}_supply_chain_ui.json", supply_ui)

    # 4. Scenarios JSON
    print("\n[4] Building scenarios.json")
    scenarios = build_scenarios(supply_ui["phases"]["synthetic"])
    write_json(supply_chain_dir / "scenarios.json", scenarios)

    # 5. Value chain UI JSON
    print("\n[5] Building value_chain_ui.json")
    value_chain_ui = build_value_chain_ui(material, supply_ui)
    write_json(processed_dir / f"{material}_value_chain_ui.json", value_chain_ui)

    # 6. Value metrics JSON
    print("\n[6] Building value_metrics.json")
    value_metrics = build_value_metrics(material)
    write_json(processed_dir / f"{material}_value_metrics.json", value_metrics)

    # 7. Value NDC metrics JSON
    print("\n[7] Building value_ndc_metrics.json")
    value_ndc_metrics = build_value_ndc_metrics(material, supply_ui)
    write_json(processed_dir / f"{material}_value_ndc_metrics.json", value_ndc_metrics)

    print(f"\nDone. All data files written to {project_dir}/")
    print("\nNext step: run HTML template adaptation for this project.")
    print(f"  Copy from: frontend/project/gold/")
    print(f"  Target:    {project_dir}/")
    print(f"  Theme:     {THEMES.get(material, DEFAULT_THEME)}")


if __name__ == "__main__":
    main()
