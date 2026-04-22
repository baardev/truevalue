"""
ln(2) Model Engine — Growth Conduit Efficiency Analysis

Implements the ln(2) layer of the five-model N-D-C framework.

The ln(2) model governs TRANSFORMATION PHASES — the points where a thing
changes its fundamental nature and multiplies in value: ore → concentrate,
nuts → butter, bars → jewelry. These are the natural growth conduits of
any supply chain.

Core principle:
  A phase operating as a minimal-gate doubling conduit should:
    - Have MINIMAL D constraints (ideally D=1: only the identity constraint)
    - Have FIRST-PRIME C output (C=2: the first real prime, a genuine doubling)
  The ratio C/D should approach 2.0 — each unit of constraint produces
  two units of contribution. When this holds, the phase naturally doubles
  value at the rate encoded in ln(2).

ln(2) configuration: inst=2, D=1, C=2
  D=1 is sub-prime: existence only, no specification beyond identity.
  C=2 is the first prime: specific, real, differentiated doubling output.
  The series 1 - 1/2 + 1/3 - 1/4 + ... converges to ln(2) = 0.69315...
  The oscillatory convergence mirrors seasonal cycles, price fluctuations,
  and demand rhythms in growth-conduit phases.

Measurement:
  For each transformation phase:
    d_natural      = constraints set by physics/biology (irreducible)
    d_institutional = constraints imposed by human systems (movable)
    d_total        = d_natural + d_institutional
    c_contribution = what the phase actually contributes (output value, differentiation)
    
    target_ratio = 2.0 (C/D ratio that corresponds to natural doubling)
    actual_ratio = c_contribution / d_total
    
    score = 100 × exp(-1.5 × |actual_ratio - 2.0| / 2.0)

Failure mode: Conduit capture
  When D-institutional >> 0, the phase has been loaded with artificial
  constraints that suppress natural doubling. Each unit of D-institutional
  added above the natural D=1 baseline is an intermediary toll on a growth
  conduit. The oscillatory ln(2) series shows this: each artificial constraint
  damps the natural swing, slowing convergence and reducing equilibrium value.

  D-institutional sources (chain-specific):
    Gold:  Royalties, taxes, LBMA certification costs, export restrictions
    Shea:  Firewood cost (processing), certification fees, minimum order quantities,
           lack of buyer commitment, market access barriers
"""

import math
from typing import List, Dict, Optional

LN2 = math.log(2)      # 0.69315...
LN2_LABEL = "ln(2) (0.69315...)"
TARGET_CD_RATIO = 2.0  # C/D ratio for natural doubling (D=1, C=2)


def ln2_coherence_score(d_total: float, c_contribution: float) -> float:
    """
    Score how close a transformation phase is to the natural ln(2) doubling rate.

    Measures whether C/D ≈ 2.0 (the minimal-gate maximal-output configuration).

    score = 100 × exp(-1.5 × |actual_ratio - 2.0| / 2.0)

    Returns:
      100.0 when c/d == 2.0 (perfect natural doubling)
      ~47   when ratio is 1.0 units from target (e.g., c/d = 1.0 or 3.0)
      ~22   when ratio is 2.0 units from target
      0     asymptotically as imbalance grows
    """
    if d_total <= 0:
        return 0.0
    ratio = c_contribution / d_total
    return 100.0 * math.exp(-1.5 * abs(ratio - TARGET_CD_RATIO) / TARGET_CD_RATIO)


def institutional_capture_score(d_natural: float, d_institutional: float) -> float:
    """
    Score the degree of institutional capture on a growth conduit.

    A healthy ln(2) phase has d_institutional ≈ 0 (existence only).
    Institutional burden = d_institutional / (d_natural + d_institutional)

    Returns 0-100 where 100 = no institutional capture.
    """
    d_total = d_natural + d_institutional
    if d_total <= 0:
        return 0.0
    institutional_fraction = d_institutional / d_total
    return 100.0 * math.exp(-2.5 * institutional_fraction)


def conduit_diagnosis(
    d_natural: float,
    d_institutional: float,
    c_contribution: float,
    score: float
) -> Dict:
    """
    Diagnose the growth conduit state of a transformation phase.

    Returns:
        Diagnosis dict with status, severity, and intervention type
    """
    d_total = d_natural + d_institutional
    ratio = c_contribution / d_total if d_total > 0 else 0.0
    inst_fraction = d_institutional / d_total if d_total > 0 else 0.0

    if score >= 80:
        return {
            "status": "conduit",
            "label": "Natural growth conduit",
            "color": "excellent",
            "description": "Phase doubles value at approximately the natural ln(2) rate. Minimal institutional overhead.",
            "intervention": None
        }
    elif score >= 60:
        return {
            "status": "moderate",
            "label": "Moderate conduit",
            "color": "good",
            "description": f"Near-natural doubling (C/D = {ratio:.2f}). Some institutional overhead present.",
            "intervention": "Monitor D-institutional load for growth."
        }
    elif ratio < 1.0:
        return {
            "status": "suppressed",
            "label": "Conduit suppressed",
            "color": "poor",
            "description": (
                f"C/D = {ratio:.2f} — phase is contributing less than its constraint burden. "
                f"Institutional load = {inst_fraction*100:.0f}% of total D. "
                "A natural growth conduit has been converted into an extraction point."
            ),
            "intervention": (
                f"Reduce D-institutional burden ({d_institutional:.1f} / {d_total:.1f} total). "
                "Identify: (1) which institutional constraints are removable, "
                "(2) market access barriers, (3) certification cost relative to benefit."
            )
        }
    elif ratio > 4.0:
        return {
            "status": "captured",
            "label": "Concentrated value — captured",
            "color": "warn",
            "description": (
                f"C/D = {ratio:.2f} — massively over-amplifying relative to 2× target. "
                "Value is concentrated in this phase, but the question is: who captures it?"
            ),
            "intervention": (
                "High C/D can mask that producers are not benefiting from the amplification. "
                "Analyze value distribution between phase operator and input suppliers."
            )
        }
    else:
        return {
            "status": "constrained",
            "label": "Constrained conduit",
            "color": "fair",
            "description": f"C/D = {ratio:.2f} — natural growth is partially suppressed by institutional overhead ({inst_fraction*100:.0f}%).",
            "intervention": "Review institutional D-loading for reduction opportunities."
        }


def compute_ln2_phases(phases: List[Dict]) -> List[Dict]:
    """
    Compute ln(2)-coherence for all transformation phases.

    Each phase dict must contain:
      - d_natural, d_institutional, c_contribution (numeric)
      - phase_id, phase_name, phase_type (must be 'transformation')
      - optional: value_in_usd, value_out_usd (for monetary doubling data)
    """
    results = []
    for p in phases:
        d_nat  = p.get("d_natural", 0)
        d_inst = p.get("d_institutional", 0)
        c_cont = p.get("c_contribution", 0)
        d_total = d_nat + d_inst

        score = ln2_coherence_score(d_total, c_cont)
        cap_score = institutional_capture_score(d_nat, d_inst)
        ratio = c_cont / d_total if d_total > 0 else 0.0
        diagnosis = conduit_diagnosis(d_nat, d_inst, c_cont, score)

        # Monetary doubling (if data available)
        v_in  = p.get("value_in_usd")
        v_out = p.get("value_out_usd")
        monetary_multiplier = None
        ln2_steps_equivalent = None
        if v_in and v_out and v_in > 0:
            monetary_multiplier = round(v_out / v_in, 2)
            ln2_steps_equivalent = round(math.log(v_out / v_in) / LN2, 2) if v_out / v_in > 0 else None

        results.append({
            **p,
            "d_total": round(d_total, 2),
            "cd_ratio": round(ratio, 3),
            "target_ratio": TARGET_CD_RATIO,
            "ln2_score": round(score, 1),
            "capture_score": round(cap_score, 1),
            "institutional_fraction_pct": round((d_inst / d_total * 100) if d_total > 0 else 0, 1),
            "monetary_multiplier": monetary_multiplier,
            "ln2_steps_equivalent": ln2_steps_equivalent,
            **diagnosis
        })

    return results


def system_ln2_coherence(phases: List[Dict]) -> Dict:
    """
    Compute system-level ln(2)-coherence from all transformation phases.
    """
    if not phases:
        return {"system_ln2_score": 0, "status": "no_data"}

    scores   = [p["ln2_score"] for p in phases]
    avg      = sum(scores) / len(scores)
    min_s    = min(scores)
    max_s    = max(scores)

    worst = next(p for p in phases if p["ln2_score"] == min_s)
    best  = next(p for p in phases if p["ln2_score"] == max_s)

    conduit_count  = sum(1 for s in scores if s >= 80)
    captured_count = sum(1 for p in phases if p["institutional_fraction_pct"] > 50)

    # Weighted capture severity
    avg_inst_pct = sum(p["institutional_fraction_pct"] for p in phases) / len(phases)

    if avg >= 70:
        status = "Natural growth conduits intact — minimal institutional capture"
    elif avg >= 50:
        status = "Moderate conduit efficiency — partial institutional capture"
    elif avg >= 30:
        status = "Low conduit efficiency — systematic institutional capture"
    else:
        status = "Critical — growth conduits severely suppressed"

    return {
        "system_ln2_score": round(avg, 1),
        "min_score": round(min_s, 1),
        "max_score": round(max_s, 1),
        "system_status": status,
        "conduit_phases": conduit_count,
        "captured_phases": captured_count,
        "total_phases": len(phases),
        "avg_institutional_pct": round(avg_inst_pct, 1),
        "worst_phase": f"P{worst.get('phase_id','?')} {worst.get('phase_name','')}",
        "worst_score": worst["ln2_score"],
        "best_phase": f"P{best.get('phase_id','?')} {best.get('phase_name','')}",
        "best_score": best["ln2_score"],
    }


# ── Pre-computed phase data ──────────────────────────────────────────────────
#
# d_natural:       constraints from physics/chemistry/biology (irreducible)
# d_institutional: constraints from regulation, licensing, market structure
# c_contribution:  what the phase actually delivers (transformed output, differentiated value)
#
# All values on 0-10 scale for comparability.
# value_in_usd / value_out_usd: monetary anchor points where data exists.

GOLD_TRANSFORM_PHASES = [
    {
        "phase_id": 1,
        "phase_name": "Mining",
        "phase_type": "transformation",
        "d_natural":        4.0,  # ore grade min, extraction method, geology constraints, safety
        "d_institutional":  5.0,  # royalties, taxes, environmental regs, community agreements
        "c_contribution":   5.0,  # run-of-mine ore, operational throughput, custody transfer
        "value_in_usd":     None,  # in-situ ore value OPAQUE
        "value_out_usd":    None,  # run-of-mine ore value OPAQUE
        "data_source":      "synthetic",
        "institutional_examples": "State royalties (3–6%), corporate income tax, environmental bond, community benefit agreements",
        "d_institutional_note": "High. Mining jurisdiction matters enormously: identical ore faces D-institutional loads ranging from 2 (permissive) to 8 (high-tax, high-compliance)."
    },
    {
        "phase_id": 2,
        "phase_name": "Processing / Milling",
        "phase_type": "transformation",
        "d_natural":        5.0,  # ore type, crush specifications, chemical treatment
        "d_institutional":  4.0,  # environmental water/tailings permits, energy compliance
        "c_contribution":   7.0,  # concentrate output, upgraded metal content, tailings disposal
        "value_in_usd":     None,  # run-of-mine ore to concentrate: OPAQUE
        "value_out_usd":    None,
        "data_source":      "synthetic",
        "institutional_examples": "Tailings management permits, water use licenses, cyanide discharge standards",
        "d_institutional_note": "Moderate. Environmental compliance creates significant but reducible D-institutional load."
    },
    {
        "phase_id": 3,
        "phase_name": "Smelting / Doré Production",
        "phase_type": "transformation",
        "d_natural":        3.0,  # metallurgy, temperature, flux chemistry (fixed by physics)
        "d_institutional":  3.0,  # trade regulations, environmental permits, trade finance
        "c_contribution":   6.0,  # doré bars, assay certificate, defined precious metal content
        "value_in_usd":     None,  # doré composition varies: OPAQUE
        "value_out_usd":    None,
        "data_source":      "synthetic",
        "institutional_examples": "Concentrate trade regulations, environmental permits for SO2 emissions, anti-money-laundering documentation",
        "d_institutional_note": "Moderate. The smelting chemistry is natural; the surrounding documentation burden is institutional."
    },
    {
        "phase_id": 4,
        "phase_name": "Refining",
        "phase_type": "transformation",
        "d_natural":        4.0,  # LBMA fineness requirements (.9999), chemical processes
        "d_institutional":  3.0,  # LBMA accreditation, banking relationships, AML/KYC
        "c_contribution":   7.0,  # LBMA Good Delivery bars, fully documented purity
        "value_in_usd":     None,  # doré value to bar value: OPAQUE (proprietary margins)
        "value_out_usd":    None,
        "data_source":      "synthetic_LBMA",
        "institutional_examples": "LBMA Good Delivery accreditation, correspondent banking requirements, AML/KYC reporting",
        "d_institutional_note": "Moderate-low. LBMA standards are close to natural requirements; accreditation costs are the main institutional burden."
    },
    {
        "phase_id": 7,
        "phase_name": "Fabrication",
        "phase_type": "transformation",
        "d_natural":        3.0,  # alloy specification, manufacturing quality, hallmarking
        "d_institutional":  6.0,  # import duties, hallmarking regulations, VAT, licensing
        "c_contribution":   5.0,  # jewelry, electronics, dental products
        "value_in_usd":     None,  # bar to jewelry: multiply ~3–8× but OPAQUE
        "value_out_usd":    None,
        "data_source":      "synthetic",
        "institutional_examples": "Import duties (0–12% by jurisdiction), hallmarking legal requirements, VAT on gold, luxury tax",
        "d_institutional_note": "High. Fabrication is the most institutionally captured transformation phase. Import duties and VAT create major D-institutional load that does not correspond to physical transformation cost."
    },
]

SHEA_TRANSFORM_PHASES = [
    {
        "phase_id": 0,
        "phase_name": "Collection / Harvest",
        "phase_type": "transformation",
        "d_natural":        3.0,  # seasonal timing, tree density, manual harvest constraints
        "d_institutional":  4.0,  # land tenure insecurity, no market price support, no credit
        "c_contribution":   3.0,  # raw shea nuts, seasonal delivery, no formal quality grade
        "value_in_usd":     None,  # pre-harvest value OPAQUE
        "value_out_usd":    150.0, # USD/MT first-sale price (Senegal, WCA average)
        "data_source":      "public_WCA_markets",
        "institutional_examples": "No formal market price mechanism, land tenure insecurity (women's collection rights often informal), no access to credit for tools/transport",
        "d_institutional_note": "High relative to D-natural. Women collectors operate without formal price discovery, market access, or institutional support — all of which are institutional barriers that elevate D above its natural D=1 baseline."
    },
    {
        "phase_id": 3,
        "phase_name": "Processing (nuts → butter)",
        "phase_type": "transformation",
        "d_natural":        4.0,  # conversion chemistry, water quality, pressing method
        "d_institutional":  3.0,  # firewood cost barrier, certification fees, equipment access
        "c_contribution":   8.0,  # shea butter: specific, differentiated, export-grade product
        "value_in_usd":     150.0, # input: nuts at first-sale price USD/MT
        "value_out_usd":    4000.0, # output: shea butter USD/MT (West Africa processor price)
        "data_source":      "public_RONGEAD_Acorn",
        "institutional_examples": "Firewood/fuel cost (natural but constrained by market), Organic certification barrier (~$5,000–$15,000 upfront), equipment financing gaps",
        "d_institutional_note": "Moderate. Firewood scarcity is a natural-institutional hybrid: the physics are natural (fire needed to boil) but the fuel cost and access are institutional. Certification creates a hard D-institutional gate for export markets."
    },
    {
        "phase_id": 5,
        "phase_name": "Manufacturing (butter → cosmetics)",
        "phase_type": "transformation",
        "d_natural":        3.0,  # formulation chemistry, stability testing, packaging
        "d_institutional":  7.0,  # EU Cosmetics Regulation, REACH, labeling, MOQ minimums
        "c_contribution":   6.0,  # branded cosmetic product, differentiated, consumer-facing
        "value_in_usd":     4000.0, # input: shea butter price USD/MT
        "value_out_usd":    47500.0, # output: retail cosmetic equivalent USD/MT shea content
        "data_source":      "public_Cleo_retail_RONGEAD",
        "institutional_examples": "EU Cosmetics Regulation 1223/2009, REACH compliance, allergen labeling, minimum order quantities (100k–1M units), cosmetic safety assessment dossier",
        "d_institutional_note": "Very high. EU cosmetic regulation creates significant D-institutional load for formulation, testing, and market access. MOQ requirements mean small-batch producers cannot access premium retail channels regardless of product quality."
    },
]


def generate_ln2_report(commodity: str = "gold") -> Dict:
    """Generate full ln(2)-model report for a commodity."""
    raw = GOLD_TRANSFORM_PHASES if commodity == "gold" else SHEA_TRANSFORM_PHASES
    phases = compute_ln2_phases(raw)
    summary = system_ln2_coherence(phases)

    return {
        "commodity": commodity,
        "model": "ln2",
        "constant": round(LN2, 5),
        "target_cd_ratio": TARGET_CD_RATIO,
        "phases": phases,
        "system_summary": summary,
    }


if __name__ == "__main__":
    for commodity in ["gold", "shea"]:
        report = generate_ln2_report(commodity)
        print(f"\n{'='*60}")
        print(f"ln(2) Model Report — {commodity.upper()}")
        print(f"{'='*60}")
        print(f"System ln(2)-coherence: {report['system_summary']['system_ln2_score']}")
        print(f"Status: {report['system_summary']['system_status']}")
        print(f"Avg institutional load: {report['system_summary']['avg_institutional_pct']}%")
        print(f"\nPhase scores (growth conduit efficiency):")
        for p in report["phases"]:
            bar = "█" * int(p["ln2_score"] / 5)
            inst_flag = "⚠" if p["institutional_fraction_pct"] > 50 else " "
            mult = f"  {p['monetary_multiplier']:.1f}×" if p.get("monetary_multiplier") else ""
            print(f"  {inst_flag}P{p['phase_id']} {p['phase_name']:30s}: "
                  f"D={p['d_total']:.1f}(inst={p['d_institutional']:.0f}) "
                  f"C={p['c_contribution']:.0f} "
                  f"C/D={p['cd_ratio']:.2f}  score={p['ln2_score']:5.1f}{mult}  {bar}")
