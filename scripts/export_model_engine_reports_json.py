#!/usr/bin/env python3
"""Export all five model reports to frontend/project/shared/data/model_engine_reports.json."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    from src.simulation.pi_engine import generate_pi_report
    from src.simulation.phi_engine import generate_phi_report
    from src.simulation.sqrt2_engine import generate_sqrt2_report
    from src.simulation.ln2_engine import generate_ln2_report
    from src.simulation.e_engine import generate_e_report

    payload = {
        "_meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "note": "Regenerate: python3 scripts/export_model_engine_reports_json.py",
            "modules": [
                "src.simulation.pi_engine",
                "src.simulation.phi_engine",
                "src.simulation.sqrt2_engine",
                "src.simulation.ln2_engine",
                "src.simulation.e_engine",
            ],
        },
        "pi": {
            "gold": generate_pi_report("gold"),
            "shea": generate_pi_report("shea"),
        },
        "phi": {
            "gold": generate_phi_report("gold"),
            "shea": generate_phi_report("shea"),
        },
        "sqrt2": {
            "gold": generate_sqrt2_report("gold"),
            "shea": generate_sqrt2_report("shea"),
        },
        "ln2": {
            "gold": generate_ln2_report("gold"),
            "shea": generate_ln2_report("shea"),
        },
        "e": {
            "gold": generate_e_report("gold"),
            "shea": generate_e_report("shea"),
        },
    }
    out_path = (
        REPO_ROOT
        / "frontend"
        / "project"
        / "shared"
        / "data"
        / "model_engine_reports.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
