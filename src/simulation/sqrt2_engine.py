"""
√2 Model Engine — Structural Transfer Coherence Analysis

Implements the √2 layer of the five-model N-D-C framework.

Unlike the π (operational) and φ (proportional) models, the √2 model
examines BOUNDARY PHASES — custody transfers, logistics, assay, and
vaulting steps where a thing crosses a boundary without fundamentally
changing its nature.

Core principle:
  A structurally coherent boundary phase has SYMMETRIC D and C loads.
  What is structurally demanded (D) should match what is structurally
  delivered (C). The natural overhead of any balanced boundary crossing
  is √2 ≈ 1.414 — the diagonal of a unit square, the most physically
  realizable irrational number.

√2 configuration: inst=2, D=2, C=2
  Both limit and contribution are the minimal prime — pure symmetric
  structural exchange. The series 1.0, 1.5, 1.417, 1.4142... converges
  to √2 from the first-generation child N of (1+2/1)/2 = 1.5.

Measurement:
  For each boundary phase:
    d_structural = structural requirements to cross the boundary (0-10)
                   (documentation, certification, specification burden)
    c_structural = structural deliverables that cross the boundary (0-10)
                   (verified outputs, custody receipts, form-matched transfers)
    symmetry_ratio = c_structural / d_structural
    target ratio = 1.0 (perfect structural symmetry, D=C=2)

  The natural overhead of √2 applies to the PATH cost, not the ratio.
  When D = C at the boundary, the crossing is symmetric and only natural
  overhead applies. When D >> C or D << C, the boundary has become
  asymmetric — either an extraction point (D>>C) or an under-specified
  conduit (D<<C).

Failure mode: Transfer asymmetry
  D >> C: the boundary demands more than it delivers (toll gate — hidden extraction)
  D << C: the boundary delivers more than it demands (under-specified — suspicious)
  Both indicate that the boundary is no longer a neutral conduit.
"""

import math
from typing import List, Dict, Optional

SQRT2 = math.sqrt(2)   # 1.41421356...
SQRT2_LABEL = "√2 (1.41421...)"
TARGET_SYMMETRY = 1.0  # perfect D=C balance target
NATURAL_OVERHEAD = SQRT2 - 1.0  # 0.4142 — 41.4% overhead of any balanced crossing


def sqrt2_coherence_score(d_structural: float, c_structural: float) -> float:
    """
    Score the structural symmetry of a boundary phase.

    Measures how closely the structural D-C load matches the ideal 1:1
    ratio. Uses exponential decay from the symmetry target:
      ratio = c / d
      score = 100 × exp(-2 × |ratio - 1.0|)

    Returns:
      100.0 when d_structural == c_structural (perfect symmetry)
      ~13.5 when ratio is 1.0 units away from target (e.g., ratio = 2 or 0)
      0     asymptotically as asymmetry grows
    """
    if d_structural <= 0:
        return 0.0
    ratio = c_structural / d_structural
    return 100.0 * math.exp(-2.0 * abs(ratio - TARGET_SYMMETRY))


def boundary_diagnosis(
    d_structural: float,
    c_structural: float,
    score: float,
    opacity: str = "medium"
) -> Dict:
    """
    Diagnose the structural symmetry state of a boundary.

    Returns:
        Diagnosis dict with type, severity, and recommended intervention
    """
    ratio = c_structural / d_structural if d_structural > 0 else 0.0

    if score >= 80:
        return {
            "status": "symmetric",
            "label": "Structurally balanced",
            "color": "excellent",
            "description": "D and C loads are symmetric — boundary imposes only natural overhead.",
            "intervention": None
        }
    elif score >= 60:
        return {
            "status": "near-symmetric",
            "label": "Near-symmetric",
            "color": "good",
            "description": f"Mild asymmetry (ratio {ratio:.2f}). Monitor for drift.",
            "intervention": "Review documentation requirements against actual delivery scope."
        }
    elif ratio < 0.5:
        return {
            "status": "extractive",
            "label": "Extraction point",
            "color": "poor",
            "description": (
                f"D >> C (ratio {ratio:.2f}): boundary demands substantially more "
                "than it delivers. Excess structural overhead — potential toll gate."
            ),
            "intervention": (
                "Investigate: (1) which requirements are institutional vs. natural, "
                "(2) whether documentation burden can be reduced without loss of integrity, "
                "(3) who captures the overhead delta between D and C at this boundary."
            )
        }
    elif ratio > 2.0:
        return {
            "status": "under-specified",
            "label": "Under-specified boundary",
            "color": "warn",
            "description": (
                f"D << C (ratio {ratio:.2f}): boundary delivers more than it formally demands. "
                "May indicate informal flows, undocumented custody changes, or missing requirements."
            ),
            "intervention": (
                "Investigate: (1) whether informal flows are bypassing formal requirements, "
                "(2) missing structural documentation on the D side, "
                "(3) custody chain gaps that appear as excess C delivery."
            )
        }
    else:
        return {
            "status": "asymmetric",
            "label": "Moderate asymmetry",
            "color": "fair",
            "description": f"Ratio {ratio:.2f} deviates from structural symmetry target (1.0).",
            "intervention": "Identify whether D or C can be rebalanced toward symmetry."
        }


def compute_sqrt2_boundaries(boundaries: List[Dict]) -> List[Dict]:
    """
    Compute √2-coherence for all supply chain boundary phases.

    Each boundary dict must contain:
      - d_structural: float (0-10 scale, structural requirement burden)
      - c_structural: float (0-10 scale, structural delivery completeness)
      - from_phase, to_phase, opacity, notes, data_source

    Returns:
        Enriched boundary list with scores and diagnoses
    """
    results = []
    for b in boundaries:
        d = b.get("d_structural", 0)
        c = b.get("c_structural", 0)
        score = sqrt2_coherence_score(d, c)
        ratio = c / d if d > 0 else 0.0
        diagnosis = boundary_diagnosis(d, c, score, b.get("opacity", "medium"))

        results.append({
            **b,
            "symmetry_ratio": round(ratio, 3),
            "sqrt2_score": round(score, 1),
            "target_ratio": TARGET_SYMMETRY,
            "distance_from_target": round(abs(ratio - TARGET_SYMMETRY), 3),
            "natural_overhead_pct": round(NATURAL_OVERHEAD * 100, 1),
            **diagnosis
        })

    return results


def system_sqrt2_coherence(boundaries: List[Dict]) -> Dict:
    """
    Compute system-level √2-coherence from all scored boundaries.
    """
    if not boundaries:
        return {"system_sqrt2_score": 0, "status": "no_data"}

    scores = [b["sqrt2_score"] for b in boundaries]
    avg = sum(scores) / len(scores)
    min_s = min(scores)
    max_s = max(scores)

    worst = next(b for b in boundaries if b["sqrt2_score"] == min_s)
    best  = next(b for b in boundaries if b["sqrt2_score"] == max_s)

    symmetric_count  = sum(1 for s in scores if s >= 80)
    asymmetric_count = sum(1 for s in scores if s < 40)

    if avg >= 75:
        status = "Structurally balanced — boundaries impose natural overhead only"
    elif avg >= 55:
        status = "Moderate symmetry — isolated boundary asymmetries"
    elif avg >= 35:
        status = "Low symmetry — systemic boundary distortion"
    else:
        status = "Critical — chain-wide structural asymmetry"

    return {
        "system_sqrt2_score": round(avg, 1),
        "min_score": round(min_s, 1),
        "max_score": round(max_s, 1),
        "system_status": status,
        "symmetric_boundaries": symmetric_count,
        "asymmetric_boundaries": asymmetric_count,
        "total_boundaries": len(boundaries),
        "worst_boundary": worst.get("boundary_id", "?"),
        "worst_score": worst["sqrt2_score"],
        "best_boundary": best.get("boundary_id", "?"),
        "best_score": best["sqrt2_score"],
    }


# ── Pre-computed boundary data ───────────────────────────────────────────────
#
# d_structural: how much is formally REQUIRED to cross this boundary (0-10)
#   - documentation requirements, certification specs, grade/weight standards
#   - high = many formal requirements; low = informal/unspecified
# c_structural: how much is actually DELIVERED at this boundary (0-10)
#   - custody receipts, assay certs, verified weight, form-matched transfer
#   - high = fully documented delivery; low = informal/opaque delivery
#
# When D=C: the boundary is symmetric — what is required is delivered
# When D>C: boundary under-delivers relative to requirements (extraction risk)
# When D<C: boundary over-delivers relative to requirements (informal flow risk)

GOLD_BOUNDARIES = [
    {
        "boundary_id": "P0→P1",
        "from_phase": "Prospecting",
        "to_phase": "Mining",
        "from_phase_id": 0, "to_phase_id": 1,
        "d_structural": 8.0,   # formal permit/license requirements, geo survey specs
        "c_structural": 3.0,   # geological data largely private/confidential
        "opacity": "high",
        "notes": "Geological survey data is commercially sensitive. Permit requirements are formally specified but the underlying data (ore body estimates, exploration results) is proprietary. Structural asymmetry: high requirements, low public delivery.",
        "data_source": "inferred"
    },
    {
        "boundary_id": "P1→P2",
        "from_phase": "Mining",
        "to_phase": "Processing",
        "from_phase_id": 1, "to_phase_id": 2,
        "d_structural": 6.0,   # ore grade specs, transport manifests, internal tracking
        "c_structural": 5.0,   # run-of-mine grades tracked internally, transport receipts
        "opacity": "medium",
        "notes": "Mine-to-mill transfer uses internal tracking systems. Ore grade and tonnage reported in company disclosures but not in real-time. Some symmetry due to industry-standard run-of-mine documentation.",
        "data_source": "inferred"
    },
    {
        "boundary_id": "P2→P3",
        "from_phase": "Processing",
        "to_phase": "Doré Production",
        "from_phase_id": 2, "to_phase_id": 3,
        "d_structural": 7.0,   # LBMA assay standards, smelter specifications
        "c_structural": 6.0,   # assay certificates, doré bar weights, purity records
        "opacity": "medium",
        "notes": "LBMA Good Delivery standards create formal documentation requirements. Assay certificates provide C-side delivery. Slight asymmetry: requirements include proprietary smelter specs not always available.",
        "data_source": "inferred"
    },
    {
        "boundary_id": "P3→P4",
        "from_phase": "Doré Production",
        "to_phase": "Refining",
        "from_phase_id": 3, "to_phase_id": 4,
        "d_structural": 7.0,   # LBMA good delivery specs, assay tolerance standards
        "c_structural": 7.0,   # LBMA .9999 bars, fully documented, weights and fineness
        "opacity": "low",
        "notes": "LBMA Good Delivery standard creates near-perfect structural symmetry: every requirement is matched by a specific deliverable. Refinery-to-bar boundary is the most transparent in the chain.",
        "data_source": "public_LBMA"
    },
    {
        "boundary_id": "P4→P5",
        "from_phase": "Refining",
        "to_phase": "Vaulting / Custody",
        "from_phase_id": 4, "to_phase_id": 5,
        "d_structural": 8.0,   # vault entry requirements, COMEX eligibility, insurance
        "c_structural": 7.0,   # registered bar weights, serial numbers, custody receipts
        "opacity": "medium",
        "notes": "Vault entry requires bar registration (serial, weight, fineness), insurance documentation, and COMEX eligibility approval. Slight D>C asymmetry: eligibility requirements slightly exceed publicly available bar records.",
        "data_source": "inferred_COMEX"
    },
    {
        "boundary_id": "P5→P6",
        "from_phase": "Vaulting / Custody",
        "to_phase": "Exchange (COMEX)",
        "from_phase_id": 5, "to_phase_id": 6,
        "d_structural": 8.0,   # COMEX warehouse receipt requirements
        "c_structural": 8.0,   # warehouse receipts, exact bar inventory, daily reporting
        "opacity": "low",
        "notes": "COMEX warehouse receipts represent the highest structural symmetry in the gold chain: every bar is documented, weighted, assayed, and registered. The structural D=C balance is near-perfect.",
        "data_source": "public_COMEX"
    },
    {
        "boundary_id": "P6→P7",
        "from_phase": "Exchange (COMEX)",
        "to_phase": "Retail / Fabrication",
        "from_phase_id": 6, "to_phase_id": 7,
        "d_structural": 6.0,   # OTC delivery specs, fabrication standards, import requirements
        "c_structural": 4.0,   # partial — unallocated accounts common, OTC opaque
        "opacity": "medium",
        "notes": "OTC market operates with less structural symmetry than COMEX. Unallocated gold accounts, paper claims, and opaque OTC delivery create C-side deficiency relative to D-side requirements.",
        "data_source": "inferred"
    },
]

SHEA_BOUNDARIES = [
    {
        "boundary_id": "P0→P1",
        "from_phase": "Collection",
        "to_phase": "First Sale",
        "from_phase_id": 0, "to_phase_id": 1,
        "d_structural": 2.0,   # minimal formal requirements (informal market)
        "c_structural": 6.0,   # collectors deliver quantity but informal, no formal docs
        "opacity": "high",
        "notes": "Informal market: collectors deliver nuts with minimal formal specification. D is near-zero (no formal requirements at first sale), but C appears high because delivery is informal and volume-based — the asymmetry is real but reversed from extraction (under-specified delivery, not over-demanded).",
        "data_source": "inferred_informal"
    },
    {
        "boundary_id": "P1→P2",
        "from_phase": "First Sale",
        "to_phase": "Trading / Bulking",
        "from_phase_id": 1, "to_phase_id": 2,
        "d_structural": 3.0,   # basic quality sorting, bag weight standards
        "c_structural": 6.0,   # quantity delivered informally, loose quality grading
        "opacity": "high",
        "notes": "Bulking aggregators purchase from multiple collectors with minimal formal specification. Volume is the primary metric; moisture, quality grade, and provenance are not formally tracked. Structural asymmetry: low D, high informal C.",
        "data_source": "inferred_informal"
    },
    {
        "boundary_id": "P2→P3",
        "from_phase": "Trading / Bulking",
        "to_phase": "Processing",
        "from_phase_id": 2, "to_phase_id": 3,
        "d_structural": 6.0,   # processor quality standards, FFA%, moisture max
        "c_structural": 5.0,   # some quality testing, but informal delivery still common
        "opacity": "medium",
        "notes": "Processors apply quality standards (FFA%, moisture, trash content) but documentary evidence of pre-delivery testing is rare. C-side partially met: delivery occurs with informal quality checks rather than formal certificates.",
        "data_source": "inferred"
    },
    {
        "boundary_id": "P3→P4",
        "from_phase": "Processing",
        "to_phase": "Export",
        "from_phase_id": 3, "to_phase_id": 4,
        "d_structural": 7.0,   # export phytosanitary cert, MSDS, buyer COA requirements
        "c_structural": 4.0,   # documentation often incomplete; certifications vary by buyer
        "opacity": "high",
        "notes": "Export boundary has high D-side requirements (phytosanitary, MSDS, Certificates of Analysis, Organic certification if applicable). C-side delivery is partial — many small processors cannot meet full documentation requirements, creating structural asymmetry that functions as an export barrier.",
        "data_source": "public_export_docs"
    },
    {
        "boundary_id": "P4→P5",
        "from_phase": "Export",
        "to_phase": "Manufacturing",
        "from_phase_id": 4, "to_phase_id": 5,
        "d_structural": 7.0,   # import specs, cosmetic-grade quality cert, REACH compliance
        "c_structural": 3.0,   # largely OPAQUE — B2B import data not public
        "opacity": "high",
        "notes": "OPAQUE. The boundary between shea export and European/global manufacturing is the least visible in the chain. Import specifications (REACH compliance, cosmetic-grade certificates) are high D, but actual delivery documentation is private B2B data.",
        "data_source": "OPAQUE"
    },
    {
        "boundary_id": "P5→P6",
        "from_phase": "Manufacturing",
        "to_phase": "Retail",
        "from_phase_id": 5, "to_phase_id": 6,
        "d_structural": 5.0,   # cosmetic safety dossier, labeling, ingredient disclosure
        "c_structural": 4.0,   # labeling varies; traceability claims often incomplete
        "opacity": "medium",
        "notes": "EU cosmetics regulation requires safety dossiers and labeling. However, shea traceability claims (origin, organic, fair trade) are inconsistently documented at retail. D side is formally specified; C side delivery is partial.",
        "data_source": "public_EU_cosm_reg"
    },
]


def generate_sqrt2_report(commodity: str = "gold") -> Dict:
    """Generate full √2-model report for a commodity."""
    raw = GOLD_BOUNDARIES if commodity == "gold" else SHEA_BOUNDARIES
    boundaries = compute_sqrt2_boundaries(raw)
    summary = system_sqrt2_coherence(boundaries)

    return {
        "commodity": commodity,
        "model": "sqrt2",
        "constant": round(SQRT2, 5),
        "natural_overhead_pct": round(NATURAL_OVERHEAD * 100, 1),
        "boundaries": boundaries,
        "system_summary": summary,
    }


if __name__ == "__main__":
    import json
    for commodity in ["gold", "shea"]:
        report = generate_sqrt2_report(commodity)
        print(f"\n{'='*60}")
        print(f"√2 Model Report — {commodity.upper()}")
        print(f"{'='*60}")
        print(f"System √2-coherence: {report['system_summary']['system_sqrt2_score']}")
        print(f"Status: {report['system_summary']['system_status']}")
        print(f"\nBoundary scores (structural symmetry):")
        for b in report["boundaries"]:
            bar = "█" * int(b["sqrt2_score"] / 5)
            arrow = "↑" if b["symmetry_ratio"] > 1.0 else ("↓" if b["symmetry_ratio"] < 1.0 else "=")
            print(f"  {b['boundary_id']:10s}: D={b['d_structural']:.0f} C={b['c_structural']:.0f} "
                  f"ratio={b['symmetry_ratio']:.2f}{arrow}  score={b['sqrt2_score']:5.1f}  {bar}")
