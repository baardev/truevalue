#!/usr/bin/env python3
"""
UI Data Generator — econ_history supply chain JSON.

Reads from:
  frontend/project/econ_history/data/schema/econ_history_phases_ndc.csv

Writes (additively):
  frontend/project/econ_history/data/processed/econ_history_supply_chain_ui.json

Uses tholonic_engine.Tholon to derive N, balance, sustainability, and balance_zone
for each epoch from the D_parameters and C_parameters in the CSV.

Usage:
    python3 src/api/generate_econ_history_ui.py [--dry-run]

Requirements:
    pip install pandas  (optional; uses csv module as fallback)
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PHASES_NDC_CSV = REPO / "frontend" / "project" / "econ_history" / "data" / "schema" / "econ_history_phases_ndc.csv"
PHASES_CSV     = REPO / "frontend" / "project" / "econ_history" / "data" / "schema" / "econ_history_phases.csv"
OUTPUT_JSON    = REPO / "frontend" / "project" / "econ_history" / "data" / "processed" / "econ_history_supply_chain_ui.json"
NOW = datetime.now().isoformat(timespec="seconds")

# Default numeric value assigned to each named D or C parameter token.
PARAM_DEFAULT = 50.0


def load_tholonic_engine():
    """Attempt to import tholonic_engine from the repo simulation directory."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "tholonic_engine",
            REPO / "src" / "simulation" / "tholonic_engine.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception as exc:
        print(f"  [WARN] tholonic_engine not loadable ({exc}); using inline calculations", file=sys.stderr)
        return None


def parse_params(raw: str) -> dict:
    """
    Parse pipe-separated parameter tokens like 'D1:name|D2:name|...'
    into {name: PARAM_DEFAULT} dict.
    """
    params = {}
    if not raw or not raw.strip():
        return params
    for token in raw.strip().split("|"):
        token = token.strip()
        if not token:
            continue
        # Token format: 'D1:param_name' or 'D1:param_name:default_value'
        parts = token.split(":")
        if len(parts) >= 2:
            name = parts[1].strip()
            default = float(parts[2]) if len(parts) >= 3 else PARAM_DEFAULT
            params[name] = default
        else:
            params[token] = PARAM_DEFAULT
    return params


def inline_balance(D: float, C: float) -> float:
    """
    Exponential balance score (0-100). Mirrors balance_exponential in tholonic_engine.
    Returns 100 when D == C, falls toward 0 as |D-C| grows.
    """
    import math
    if D <= 0 and C <= 0:
        return 0.0
    total = D + C
    if total == 0:
        return 0.0
    ratio = min(D, C) / max(D, C) if max(D, C) > 0 else 0.0
    # Exponential balance: 100 * exp(-k * (1-ratio)) where k tunes the curve
    k = 3.5
    return round(100.0 * math.exp(-k * (1.0 - ratio)), 2)


def classify_zone(balance: float) -> dict:
    """Mirrors classify_ndc_balance_zone from tholonic_engine."""
    import math
    PHI = (1 + math.sqrt(5)) / 2
    COHERENT = 80.0
    STRESSED  = 100.0 / PHI       # ~61.8
    FAILURE   = 100.0 * (1 - 1.0 / PHI)  # ~38.2
    if balance >= COHERENT:
        return {"zone": "coherent", "color": "green", "label": "Coherent",
                "note": "Self-sustaining; optional optimization."}
    if balance >= STRESSED:
        return {"zone": "stressed", "color": "amber", "label": "Stressed",
                "note": "Self-sustaining but over-constrained; improve D or C in-system."}
    if balance >= FAILURE:
        return {"zone": "failure", "color": "red", "label": "Failure",
                "note": "Cost export; external policy or infrastructure typically required."}
    return {"zone": "breakdown", "color": "dark_red", "label": "Breakdown",
            "note": "Systemic failure; requires structural intervention."}


def read_csv(path: Path) -> list:
    if not path.exists():
        print(f"  [SKIP] {path} not found", file=sys.stderr)
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def generate(dry_run: bool = False):
    engine = load_tholonic_engine()
    ndc_rows  = read_csv(PHASES_NDC_CSV)
    base_rows = read_csv(PHASES_CSV)

    # Build base phase lookup
    base_lookup = {int(r["phase_id"]): r for r in base_rows if r.get("phase_id", "").strip().lstrip("-").isdigit()}

    phase_meta = {}
    phases_synthetic = {}
    all_balances = []

    for row in ndc_rows:
        pid = int(row["phase_id"])
        base = base_lookup.get(pid, {})

        d_params = parse_params(row.get("D_parameters", ""))
        c_params = parse_params(row.get("C_parameters", ""))
        energy_base = float(row.get("energy_base", "10.0") or "10.0")

        D_total = sum(d_params.values())
        C_total = sum(c_params.values())

        # Use tholonic_engine if available
        if engine:
            try:
                tholon = engine.Tholon(
                    phase_id=pid,
                    D_params=d_params,
                    C_params=c_params,
                    energy_base=energy_base
                )
                state = tholon.get_state()
                D_total   = state["D_total"]
                C_total   = state["C_total"]
                N         = round(state["N"])
                balance   = round(state["balance"], 2)
                sust      = round(state["sustainability"], 3)
                zone_info = state
            except Exception as exc:
                print(f"  [WARN] tholonic_engine failed for phase {pid}: {exc}", file=sys.stderr)
                engine = None

        if not engine:
            # Inline fallback
            balance = inline_balance(D_total, C_total)
            import math
            N = round(math.sqrt(D_total * C_total) * (balance / 100.0))
            imbalance = abs(D_total - C_total)
            sust = round(100.0 / (imbalance ** 2 + energy_base), 3)

        zone_info = classify_zone(balance)

        phase_meta[str(pid)] = {
            "name": row.get("phase_name", f"Phase {pid}"),
            "epoch": base.get("epoch_start", "") + " – " + base.get("epoch_end", ""),
            "transparency": row.get("transparency_level", "Medium"),
            "paradigm_state": base.get("paradigm_state", ""),
        }

        phases_synthetic[str(pid)] = {
            "D": round(D_total),
            "C": round(C_total),
            "balance": balance,
            "N": N,
            "sustainability": sust,
            "balance_zone": zone_info.get("zone", ""),
            "balance_zone_label": zone_info.get("label", ""),
            "balance_zone_color": zone_info.get("color", ""),
            "balance_zone_note": zone_info.get("note", ""),
            "notes": base.get("notes", ""),
            "data_quality": "Derived from schema CSV — see econ_history_metrics.csv for anchors",
            "custodian": base.get("custodian_class", ""),
            "key_transition_trigger": base.get("primary_transformation", ""),
        }
        all_balances.append(balance)

    chain_avg = round(sum(all_balances) / len(all_balances), 1) if all_balances else 0.0

    output = {
        "_meta": {
            "generated": NOW,
            "generator": "src/api/generate_econ_history_ui.py",
            "material": "econ_history",
            "sources": [
                str(PHASES_NDC_CSV.relative_to(REPO)),
                str(PHASES_CSV.relative_to(REPO)),
            ],
            "note": "N-D-C values derived from Tholonic engine using D_parameters and C_parameters in schema CSV."
        },
        "entities": {
            "synthetic": {
                "label": "Synthetic Baseline",
                "description": "Chain-average N-D-C values across all 10 paradigm epochs"
            }
        },
        "phase_meta": phase_meta,
        "phases": {"synthetic": phases_synthetic},
        "system": {
            "synthetic": {
                "balance": chain_avg,
                "average_N": round(sum(v["N"] for v in phases_synthetic.values()) / len(phases_synthetic)) if phases_synthetic else 0,
                "bottleneck_phase_ids": [pid for pid, v in phases_synthetic.items() if v["balance"] < 80],
                "pi_score": chain_avg,
                "phi_score": None,
                "sqrt2_score": None,
                "ln2_score": None,
                "e_score": 0,
                "interpretation": (
                    "Intellectual supply chain of economics: 10 paradigm epochs from pre-3000 BCE to present. "
                    "Chain avg balance {:.1f}%. Three epochs stressed (below 80%): Ancient Exchange, "
                    "Classical Antiquity, and Post-Crisis Fragmentation. Peak N in Keynesian Macro epoch."
                ).format(chain_avg)
            }
        }
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    out_text = json.dumps(output, indent=2, ensure_ascii=False)
    if dry_run:
        print(f"  [DRY-RUN] Would write {len(out_text)} bytes to {OUTPUT_JSON.relative_to(REPO)}")
    else:
        OUTPUT_JSON.write_text(out_text, encoding="utf-8")
        print(f"  [WRITE] {OUTPUT_JSON.relative_to(REPO)} ({len(out_text)} bytes)")

    print(f"  Chain avg balance: {chain_avg}%")
    print(f"  Phases generated: {len(phases_synthetic)}")


def main():
    parser = argparse.ArgumentParser(description="Generate econ_history supply chain UI JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written without writing")
    args = parser.parse_args()
    generate(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
