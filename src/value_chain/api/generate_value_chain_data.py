"""
Value Chain Data Contract Generator (Standalone)

Converts value-chain CSV schema files to JSON for frontend consumption.
Writes only into data/value_chain/processed to preserve strict separation
from supply-chain outputs.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValueChainDataGenerator:
    def __init__(self, schema_dir="../../../schema", data_dir="../../../data/value_chain"):
        self.schema_dir = Path(__file__).parent / schema_dir
        self.data_dir = Path(__file__).parent / data_dir
        self.output_dir = self.data_dir / "processed"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_metric_definitions(self):
        src = self.schema_dir / "value_chain_metric_definitions.csv"
        df = pd.read_csv(src) if src.exists() else pd.DataFrame()
        df = df.astype(object).where(pd.notna(df), None)

        payload = {
            "metric_definitions": df.to_dict(orient="records"),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0",
                "source_file": str(src),
            },
        }

        out = self.output_dir / "value_metric_definitions.json"
        out.write_text(json.dumps(payload, indent=2, allow_nan=False))
        logger.info(f"✓ Generated {out}")
        return payload

    def generate_sources(self):
        src = self.schema_dir / "value_chain_data_sources.csv"
        df = pd.read_csv(src) if src.exists() else pd.DataFrame()
        df = df.astype(object).where(pd.notna(df), None)

        payload = {
            "sources": df.to_dict(orient="records"),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0",
                "source_file": str(src),
            },
        }

        out = self.output_dir / "value_sources.json"
        out.write_text(json.dumps(payload, indent=2, allow_nan=False))
        logger.info(f"✓ Generated {out}")
        return payload

    def generate_phase_summaries(self, max_phase_id: int = 8):
        src = self.schema_dir / "value_chain_metrics.csv"
        df = pd.read_csv(src) if src.exists() else pd.DataFrame()
        df = df.astype(object).where(pd.notna(df), None)

        for value_phase_id in range(max_phase_id + 1):
            phase_df = df[df["value_phase_id"] == value_phase_id] if len(df) > 0 else pd.DataFrame()
            metrics_available = phase_df["metric_name"].unique().tolist() if len(phase_df) > 0 else []

            payload = {
                "value_phase_id": value_phase_id,
                "total_records": int(len(phase_df)),
                "last_update": str(phase_df["date"].max()) if len(phase_df) > 0 else None,
                "metrics_available": metrics_available,
                "data_quality": self._assess_data_quality(phase_df),
                "metadata": {"generated_at": datetime.now().isoformat(), "version": "1.0"},
            }

            out = self.output_dir / f"value_phase{value_phase_id}_summary.json"
            out.write_text(json.dumps(payload, indent=2, allow_nan=False))
            logger.info(f"✓ Generated {out}")

    def generate_ndc_metrics_json(self):
        """
        Emit the full value-chain NDC table for frontend use.
        """
        src = self.schema_dir / "value_chain_metrics_ndc.csv"
        df = pd.read_csv(src) if src.exists() else pd.DataFrame()
        df = df.astype(object).where(pd.notna(df), None)

        payload = {
            "records": df.to_dict(orient="records"),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0",
                "source_file": str(src),
                "row_count": int(len(df)),
            },
        }

        out = self.output_dir / "gold_value_ndc_metrics.json"
        out.write_text(json.dumps(payload, indent=2, allow_nan=False))
        logger.info(f"✓ Generated {out}")
        return payload

    def generate_ndc_phase_summaries(self, max_phase_id: int = 8):
        src = self.schema_dir / "value_chain_metrics_ndc.csv"
        df = pd.read_csv(src) if src.exists() else pd.DataFrame()
        df = df.astype(object).where(pd.notna(df), None)

        for value_phase_id in range(max_phase_id + 1):
            phase_df = df[df["value_phase_id"] == value_phase_id] if len(df) > 0 else pd.DataFrame()
            metrics_available = phase_df["metric_category"].unique().tolist() if len(phase_df) > 0 else []

            payload = {
                "value_phase_id": value_phase_id,
                "total_records": int(len(phase_df)),
                "last_update": str(phase_df["date"].max()) if len(phase_df) > 0 else None,
                "categories_available": metrics_available,
                "data_quality": self._assess_data_quality(phase_df),
                "metadata": {"generated_at": datetime.now().isoformat(), "version": "1.0"},
            }

            out = self.output_dir / f"value_ndc_phase{value_phase_id}_summary.json"
            out.write_text(json.dumps(payload, indent=2, allow_nan=False))
            logger.info(f"✓ Generated {out}")

    def generate_metrics_json(self):
        """
        Emit the full value-chain metric table for frontend use.
        This is intentionally separate from supply-chain outputs.
        """
        src = self.schema_dir / "value_chain_metrics.csv"
        df = pd.read_csv(src) if src.exists() else pd.DataFrame()
        df = df.astype(object).where(pd.notna(df), None)

        payload = {
            "records": df.to_dict(orient="records"),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0",
                "source_file": str(src),
                "row_count": int(len(df)),
            },
        }

        out = self.output_dir / "gold_value_metrics.json"
        out.write_text(json.dumps(payload, indent=2, allow_nan=False))
        logger.info(f"✓ Generated {out}")
        return payload

    @staticmethod
    def _assess_data_quality(df: pd.DataFrame) -> str:
        if df is None or len(df) == 0:
            return "OPAQUE"
        sources = set(df.get("source_type", pd.Series(dtype=str)).dropna().astype(str).str.lower().tolist())
        if "public" in sources:
            return "High"
        if "paid" in sources:
            return "Medium"
        if "private" in sources:
            return "Low"
        if "simulated" in sources or "synthetic" in sources:
            return "Synthetic"
        return "OPAQUE"


def main():
    gen = ValueChainDataGenerator()
    gen.generate_metric_definitions()
    gen.generate_sources()
    gen.generate_metrics_json()
    gen.generate_phase_summaries(max_phase_id=8)
    gen.generate_ndc_metrics_json()
    gen.generate_ndc_phase_summaries(max_phase_id=8)
    print("✅ Value-chain JSON generation complete.")


if __name__ == "__main__":
    main()

