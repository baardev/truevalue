"""
Phi (φ) Model Engine — Proportional Coherence Analysis

Implements the φ (golden ratio) layer of the five-model N-D-C framework.

Unlike the π (operational) model which analyzes each phase in isolation,
the φ model analyzes the PROPORTIONAL RELATIONSHIPS between adjacent phases.

Core principle:
  A harmonically coherent supply chain produces N-values that grow in
  φ-proportional ratios between phases. When N[i+1] / N[i] ≈ φ (1.61803...),
  value flows naturally between phases without extraction or suppression.

φ configuration: inst=2, D=2, C=3
  Child N (first Fibonacci term from D+C) = 5 — the same value that appears
  as C in the π configuration. This is the structural link between π and φ.

Failure mode: Disproportional value capture
  When a phase boundary shows ratio << φ: downstream phase is suppressed
  (value is not passing through proportionally — it is being retained upstream)
  When ratio >> φ: upstream phase is being extracted
  (value is collapsing through a bottleneck and recovering sharply downstream)
"""

import math
from typing import List, Dict, Tuple, Optional

PHI = (1 + math.sqrt(5)) / 2   # 1.61803398...
PHI_LABEL = "φ (1.61803...)"


def phi_coherence_score(ratio: float) -> float:
    """
    Score how close a phase-to-phase N-ratio is to φ.

    Uses exponential decay from the φ target:
      score = 100 × exp(-2 × |ratio - φ| / φ)

    Returns:
      100.0 when ratio == φ (perfect φ-proportion)
      ~74   when ratio is 0.5φ away from target
      ~14   when ratio is φ away from target
      0 → ∞ approaches 0 asymptotically
    """
    if ratio <= 0:
        return 0.0
    distance = abs(ratio - PHI)
    return 100.0 * math.exp(-2.0 * distance / PHI)


def boundary_diagnosis(ratio: float, score: float) -> Dict:
    """
    Diagnose the nature of a φ boundary failure.

    Args:
        ratio: N[i+1] / N[i]
        score: phi_coherence_score result

    Returns:
        Diagnosis dict with type, severity, and recommended intervention
    """
    if score >= 80:
        return {
            "status": "healthy",
            "label": "φ-proportional",
            "color": "good",
            "description": "Value passes through this boundary in natural proportion.",
            "intervention": None
        }
    elif score >= 55:
        return {
            "status": "moderate",
            "label": "Near-proportional",
            "color": "fair",
            "description": "Mild deviation from φ-proportion — monitor for drift.",
            "intervention": "Monitor phase N-values for sustained imbalance."
        }
    elif ratio < 1.0:
        return {
            "status": "suppressed",
            "label": "Value suppressed",
            "color": "poor",
            "description": (
                f"Downstream phase N-value collapsed to {ratio:.3f}× the upstream. "
                "Value is not passing through — either retained upstream or lost at boundary."
            ),
            "intervention": (
                "Investigate: (1) D-institutional barriers at boundary, "
                "(2) custody transfer overhead, "
                "(3) intermediary extraction between phases."
            )
        }
    elif ratio > PHI * 1.5:
        return {
            "status": "unstable",
            "label": "Disproportionate recovery",
            "color": "warn",
            "description": (
                f"N-value jumps {ratio:.3f}× across this boundary — far exceeding φ. "
                "A sharp recovery after a collapse is structurally unstable."
            ),
            "intervention": (
                "Investigate: (1) Preceding bottleneck creating artificial scarcity, "
                "(2) boundary serving as extraction point before recovery, "
                "(3) data anomaly — verify N-values."
            )
        }
    else:
        return {
            "status": "compressed",
            "label": "Under-proportional",
            "color": "fair",
            "description": (
                f"Ratio {ratio:.3f} is below φ — value growth is compressed at this boundary."
            ),
            "intervention": (
                "Strengthen downstream C parameters or reduce upstream D constraints "
                "to allow more proportional value flow."
            )
        }


def compute_phi_boundaries(
    phases: List[Dict],
    n_key: str = "N"
) -> List[Dict]:
    """
    Compute φ-coherence for all adjacent phase boundaries.

    Args:
        phases: List of phase dicts ordered by phase_id, each containing N-value
        n_key: Key name for the N-value in each phase dict

    Returns:
        List of boundary dicts, one per adjacent phase pair
    """
    boundaries = []
    for i in range(len(phases) - 1):
        from_phase = phases[i]
        to_phase = phases[i + 1]

        n_from = from_phase.get(n_key, 0)
        n_to = to_phase.get(n_key, 0)

        if n_from <= 0:
            ratio = 0.0
            score = 0.0
        else:
            ratio = n_to / n_from
            score = phi_coherence_score(ratio)

        diagnosis = boundary_diagnosis(ratio, score)

        boundaries.append({
            "from_phase_id": from_phase.get("phase_id", i),
            "from_phase_name": from_phase.get("phase_name", f"Phase {i}"),
            "to_phase_id": to_phase.get("phase_id", i + 1),
            "to_phase_name": to_phase.get("phase_name", f"Phase {i+1}"),
            "n_from": n_from,
            "n_to": n_to,
            "ratio": round(ratio, 4),
            "phi_target": round(PHI, 5),
            "distance_from_phi": round(abs(ratio - PHI), 4),
            "phi_score": round(score, 1),
            **diagnosis
        })

    return boundaries


def system_phi_coherence(boundaries: List[Dict]) -> Dict:
    """
    Compute system-level φ-coherence summary from all boundaries.

    Returns:
        Summary dict with overall score, best/worst boundaries, and diagnosis
    """
    if not boundaries:
        return {"system_phi_score": 0, "status": "no_data"}

    scores = [b["phi_score"] for b in boundaries]
    avg_score = sum(scores) / len(scores)
    min_score = min(scores)
    max_score = max(scores)

    worst = next(b for b in boundaries if b["phi_score"] == min_score)
    best = next(b for b in boundaries if b["phi_score"] == max_score)

    healthy_count = sum(1 for s in scores if s >= 80)
    critical_count = sum(1 for s in scores if s < 40)

    if avg_score >= 75:
        system_status = "Harmonically coherent"
    elif avg_score >= 55:
        system_status = "Moderate coherence — isolated boundary failures"
    elif avg_score >= 35:
        system_status = "Low coherence — systemic proportionality breakdown"
    else:
        system_status = "Critical — chain-wide proportionality failure"

    return {
        "system_phi_score": round(avg_score, 1),
        "min_score": min_score,
        "max_score": max_score,
        "system_status": system_status,
        "healthy_boundaries": healthy_count,
        "critical_boundaries": critical_count,
        "total_boundaries": len(boundaries),
        "worst_boundary": f"P{worst['from_phase_id']}→P{worst['to_phase_id']}",
        "worst_score": worst["phi_score"],
        "best_boundary": f"P{best['from_phase_id']}→P{best['to_phase_id']}",
        "best_score": best["phi_score"],
    }


def value_amplification_ratios(
    phases: List[Dict],
    value_key: str = "value_usd_per_mt"
) -> Optional[List[Dict]]:
    """
    Where monetary value data exists (e.g., shea), compute actual value
    amplification ratios between phases and compare to φ-expectation.

    Args:
        phases: Phase list with optional value_key fields
        value_key: Key name for monetary value per unit

    Returns:
        List of amplification dicts, or None if data insufficient
    """
    valued_phases = [p for p in phases if p.get(value_key) and p[value_key] > 0]
    if len(valued_phases) < 2:
        return None

    result = []
    for i in range(len(valued_phases) - 1):
        v_from = valued_phases[i][value_key]
        v_to = valued_phases[i + 1][value_key]
        actual_multiple = v_to / v_from if v_from > 0 else 0
        phi_steps_equivalent = math.log(actual_multiple) / math.log(PHI) if actual_multiple > 0 else 0

        result.append({
            "from_phase_id": valued_phases[i].get("phase_id"),
            "from_phase_name": valued_phases[i].get("phase_name"),
            "to_phase_id": valued_phases[i + 1].get("phase_id"),
            "to_phase_name": valued_phases[i + 1].get("phase_name"),
            "value_from": v_from,
            "value_to": v_to,
            "actual_multiple": round(actual_multiple, 2),
            "phi_steps_equivalent": round(phi_steps_equivalent, 2),
            "note": (
                f"{actual_multiple:.1f}× value amplification "
                f"≈ {phi_steps_equivalent:.1f} φ-steps"
            )
        })

    return result


# ── Pre-computed data for frontend use ──────────────────────────────────────

GOLD_PHASES = [
    {"phase_id": 0, "phase_name": "Prospecting",  "N": 183},
    {"phase_id": 1, "phase_name": "Mining",        "N": 259},
    {"phase_id": 2, "phase_name": "Processing",    "N": 263},
    {"phase_id": 3, "phase_name": "Doré",          "N": 229},
    {"phase_id": 4, "phase_name": "Refining",      "N": 253},
    {"phase_id": 5, "phase_name": "Casting",       "N": 237},
    {"phase_id": 6, "phase_name": "Vaulting",      "N": 118},
    {"phase_id": 7, "phase_name": "Exchange",      "N": 239},
]

SHEA_PHASES = [
    {"phase_id": 0, "phase_name": "Collection",     "N": 178, "value_usd_per_mt": None},
    {"phase_id": 1, "phase_name": "First Sale",     "N": 192, "value_usd_per_mt": 150},
    {"phase_id": 2, "phase_name": "Trading/Bulking","N": 218, "value_usd_per_mt": 250},
    {"phase_id": 3, "phase_name": "Processing",     "N": 241, "value_usd_per_mt": 4000},
    {"phase_id": 4, "phase_name": "Export",         "N": 158, "value_usd_per_mt": None},
    {"phase_id": 5, "phase_name": "Manufacturing",  "N": 234, "value_usd_per_mt": None},
    {"phase_id": 6, "phase_name": "Retail",         "N": 237, "value_usd_per_mt": 47500},
]


def generate_phi_report(commodity: str = "gold") -> Dict:
    """Generate full φ-model report for a commodity."""
    phases = GOLD_PHASES if commodity == "gold" else SHEA_PHASES
    boundaries = compute_phi_boundaries(phases)
    summary = system_phi_coherence(boundaries)

    report = {
        "commodity": commodity,
        "model": "phi",
        "phi_constant": round(PHI, 5),
        "phases": phases,
        "boundaries": boundaries,
        "system_summary": summary,
    }

    if commodity == "shea":
        amp = value_amplification_ratios(phases, "value_usd_per_mt")
        if amp:
            report["value_amplification"] = amp

    return report


if __name__ == "__main__":
    import json
    for commodity in ["gold", "shea"]:
        report = generate_phi_report(commodity)
        print(f"\n{'='*60}")
        print(f"φ Model Report — {commodity.upper()}")
        print(f"{'='*60}")
        print(f"System φ-coherence: {report['system_summary']['system_phi_score']}")
        print(f"Status: {report['system_summary']['system_status']}")
        print(f"\nBoundary scores:")
        for b in report["boundaries"]:
            bar = "█" * int(b["phi_score"] / 5)
            print(f"  P{b['from_phase_id']}→P{b['to_phase_id']}: "
                  f"ratio={b['ratio']:.3f}  score={b['phi_score']:5.1f}  {bar}")
        if "value_amplification" in report:
            print(f"\nValue amplification (shea):")
            for v in report["value_amplification"]:
                print(f"  {v['note']}")
