"""
e Model Engine — Abstract claim coupling (paper vs physical)

Mirrors the Gold / Shea e_dashboard logic: claims rows from CSV, per-phase
minimum e_score, system coherence average over phases that have at least one
non-OPAQUE claim (same filter as the browser getSystemScore).

Financial interpretation stays on the value chain; this module only structures
coupling metrics for audit and frontend export.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GOLD_CLAIMS_CSV = REPO_ROOT / "frontend" / "project" / "gold" / "data" / "schema" / "gold_e_model_claims.csv"
SHEA_CLAIMS_CSV = REPO_ROOT / "frontend" / "project" / "shea" / "data" / "schema" / "shea_e_model_claims.csv"

E = math.e


def _parse_e_score(raw: str) -> int:
    try:
        return int(float(raw))
    except (TypeError, ValueError):
        return 0


def _parse_coupling(raw: str, status: str) -> Optional[float]:
    st = (status or "").strip().upper()
    rv = (raw or "").strip().upper()
    if st == "OPAQUE" or rv == "OPAQUE":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def load_claims_from_csv(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        return []
    rows: List[Dict[str, Any]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ctype = (row.get("claim_type") or "").strip().lower()
            if ctype in ("", "none"):
                continue
            status = (row.get("coupling_ratio_status") or "").strip()
            coupling = _parse_coupling(row.get("coupling_ratio"), status)
            e_score = int(_parse_e_score(row.get("e_score", "0")))
            if status == "OPAQUE":
                e_score = int(_parse_e_score(row.get("e_score", "5")))
            rows.append({
                "record_id": row.get("record_id"),
                "phase_id": int(row.get("phase_id") or -1),
                "phase_name": (row.get("phase_name") or "").strip(),
                "claim_type": (row.get("claim_type") or "").strip(),
                "coupling_ratio": coupling,
                "coupling_ratio_status": status,
                "e_score": e_score,
                "is_rehypothecated": (row.get("is_rehypothecated") or "").lower() in ("true", "1", "yes"),
                "physical_value_usd_billions": row.get("physical_value_usd_billions"),
                "abstract_value_usd_billions": row.get("abstract_value_usd_billions"),
                "source_type": (row.get("source_type") or "").strip(),
                "source_name": (row.get("source_name") or "").strip(),
                "notes": (row.get("notes") or "")[:600],
            })
    return rows


def compute_phase_claim_scores(claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_phase: Dict[int, List[Dict[str, Any]]] = {}
    for c in claims:
        pid = c["phase_id"]
        if pid < 0:
            continue
        by_phase.setdefault(pid, []).append(c)

    result: List[Dict[str, Any]] = []
    for pid in sorted(by_phase.keys()):
        pc = by_phase[pid]
        scores = [c["e_score"] for c in pc]
        min_score = min(scores)
        has_opaque = any((c["coupling_ratio_status"] or "").upper() == "OPAQUE" for c in pc)
        result.append({
            "phase_id": pid,
            "phase_name": pc[0].get("phase_name", ""),
            "phase_score": min_score,
            "claim_count": len(pc),
            "has_opaque": has_opaque,
            "claim_types": [c["claim_type"] for c in pc],
        })
    return result


def system_e_coherence(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Match e_dashboard getSystemScore: only non-OPAQUE claims define the phase set."""
    active = [c for c in claims if (c.get("coupling_ratio_status") or "").upper() != "OPAQUE"]
    phase_ids = sorted({c["phase_id"] for c in active if c["phase_id"] >= 0})
    if not phase_ids:
        return {"system_e_score": 0, "system_status": "no_data"}

    phase_scores = []
    for pid in phase_ids:
        pc = [c for c in active if c["phase_id"] == pid]
        if not pc:
            continue
        phase_scores.append(min(c["e_score"] for c in pc))

    if not phase_scores:
        return {"system_e_score": 0, "system_status": "no_data"}

    avg = sum(phase_scores) / len(phase_scores)
    mn, mx = min(phase_scores), max(phase_scores)

    if avg >= 70:
        status = "Strong abstract–physical coupling on scored claims"
    elif avg >= 40:
        status = "Moderate decoupling — review low e-score phases"
    else:
        status = "Severe decoupling — abstract layer diverges from physical"

    return {
        "system_e_score": round(avg, 1),
        "min_score": mn,
        "max_score": mx,
        "system_status": status,
        "phases_in_average": len(phase_scores),
        "total_claim_rows": len(claims),
    }


def generate_e_report(commodity: str = "gold") -> Dict[str, Any]:
    path = GOLD_CLAIMS_CSV if commodity == "gold" else SHEA_CLAIMS_CSV
    claims = load_claims_from_csv(path)
    phase_scores = compute_phase_claim_scores(claims)
    summary = system_e_coherence(claims)
    worst_claim = None
    if claims:
        worst_claim = min(claims, key=lambda c: c["e_score"])
    return {
        "commodity": commodity,
        "model": "e",
        "e_constant": round(E, 5),
        "data_source_path": str(path),
        "claims": claims,
        "phase_scores": phase_scores,
        "system_summary": summary,
        "worst_claim": worst_claim,
    }


if __name__ == "__main__":
    for c in ("gold", "shea"):
        rep = generate_e_report(c)
        print(f"e {c}: system score {rep['system_summary'].get('system_e_score')}")
