"""
π (pi) Model Engine — Operational per-phase D–C balance

Implements the π layer of the five-model N-D-C framework: each phase is scored
in isolation using the TVPCI exponential balance (same as tholonic_engine).

Data source: processed supply chain UI JSON (synthetic baseline), not a separate
invented phase table, so π scores stay aligned with hub JSON used in the browser.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List

from src.simulation.tholonic_engine import balance_exponential, classify_ndc_balance_zone

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GOLD_UI_JSON = REPO_ROOT / "frontend" / "project" / "gold" / "data" / "processed" / "gold_supply_chain_ui.json"
SHEA_UI_JSON = REPO_ROOT / "frontend" / "project" / "west_african_shea" / "data" / "processed" / "shea_supply_chain_ui.json"

PI = math.pi


def _as_float(x: Any, default: float = 0.0) -> float:
    if x is None:
        return default
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def _load_phases(ui_json_path: Path, phase_root_key: str = "synthetic") -> List[Dict[str, Any]]:
    """Load D/C/balance/N per phase from a processed supply-chain UI JSON."""
    if not ui_json_path.is_file():
        return []
    with open(ui_json_path, encoding="utf-8") as f:
        data = json.load(f)
    phases_root = data.get("phases", {})
    # Gold uses phases.synthetic; shea stores phases directly at the integer keys.
    if phase_root_key in phases_root:
        ph = phases_root[phase_root_key]
    else:
        ph = phases_root
    meta = data.get("phase_meta", {})
    out: List[Dict[str, Any]] = []
    for key in sorted((k for k in ph.keys() if k.isdigit()), key=int):
        row = ph[key]
        if not isinstance(row, dict):
            continue
        d = row.get("D")
        c = row.get("C")
        if not isinstance(d, (int, float)) or not isinstance(c, (int, float)):
            continue
        pid = int(key)
        m = meta.get(key, {})
        name = row.get("name") or m.get("name") or f"Phase {pid}"
        balance_json = _as_float(row.get("balance"), 0.0)
        balance_calc = balance_exponential(float(d), float(c))
        zone = classify_ndc_balance_zone(float(balance_calc))
        out.append({
            "phase_id": pid,
            "phase_name": name,
            "D": float(d),
            "C": float(c),
            "dc_ratio": round(float(d) / float(c), 3) if float(c) > 0 else None,
            "balance_reported": round(balance_json, 2),
            "balance_exponential": round(balance_calc, 2),
            "N": _as_float(row.get("N"), 0.0),
            "balance_zone": zone["zone"],
            "balance_zone_label": zone["label"],
            "balance_zone_color": zone["color"],
            "notes": (row.get("notes") or "")[:500],
        })
    return out


def system_pi_summary(phases: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not phases:
        return {"system_pi_score": 0, "status": "no_data"}

    scores = [p["balance_exponential"] for p in phases]
    avg = sum(scores) / len(scores)
    mn, mx = min(scores), max(scores)
    worst = min(phases, key=lambda p: p["balance_exponential"])
    best = max(phases, key=lambda p: p["balance_exponential"])
    zones: Dict[str, int] = {}
    for p in phases:
        z = p.get("balance_zone", "unknown")
        zones[z] = zones.get(z, 0) + 1

    if avg >= 80:
        status = "Operationally coherent — most phases in healthy balance"
    elif avg >= 60:
        status = "Moderate operational stress — isolated D–C drift"
    elif avg >= 40:
        status = "Low operational coherence — systemic imbalance risk"
    else:
        status = "Critical — chain-wide operational breakdown"

    return {
        "system_pi_score": round(avg, 1),
        "min_score": round(mn, 1),
        "max_score": round(mx, 1),
        "system_status": status,
        "total_phases": len(phases),
        "zone_counts": zones,
        "worst_phase": f"P{worst['phase_id']} {worst['phase_name']}",
        "worst_score": worst["balance_exponential"],
        "best_phase": f"P{best['phase_id']} {best['phase_name']}",
        "best_score": best["balance_exponential"],
    }


def generate_pi_report(commodity: str = "gold") -> Dict[str, Any]:
    """Full π-model report from processed UI JSON."""
    if commodity == "gold":
        phases = _load_phases(GOLD_UI_JSON, phase_root_key="synthetic")
        src = str(GOLD_UI_JSON)
    else:
        phases = _load_phases(SHEA_UI_JSON, phase_root_key="")
        src = str(SHEA_UI_JSON)
    summary = system_pi_summary(phases)
    return {
        "commodity": commodity,
        "model": "pi",
        "pi_constant": round(PI, 5),
        "data_source_path": src,
        "phases": phases,
        "system_summary": summary,
    }


if __name__ == "__main__":
    for c in ("gold", "shea"):
        rep = generate_pi_report(c)
        print(f"π {c}: system score {rep['system_summary']['system_pi_score']}")
