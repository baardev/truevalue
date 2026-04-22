"""
API Data Contract Generator

Converts CSV schema files to JSON format for frontend consumption.
Generates static JSON files matching the FRONTEND_API.md specification.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrontendDataGenerator:
    """Generate frontend-ready JSON from supply chain data"""
    
    def __init__(self, schema_dir="../../schema", data_dir="../../data"):
        self.schema_dir = Path(__file__).parent / schema_dir
        self.data_dir = Path(__file__).parent / data_dir
        self.output_dir = self.data_dir / "processed"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_phases_json(self):
        """Convert supply_chain_phases.csv to phases.json"""
        phases_csv = self.schema_dir / "supply_chain_phases.csv"
        
        if not phases_csv.exists():
            logger.error(f"{phases_csv} not found")
            return None
        
        df = pd.read_csv(phases_csv)
        
        phases_data = {
            "phases": df.to_dict(orient='records'),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_phases": len(df),
                "version": "1.0"
            }
        }
        
        output_file = self.output_dir / "phases.json"
        with open(output_file, 'w') as f:
            json.dump(phases_data, f, indent=2)
        
        logger.info(f"✓ Generated {output_file}")
        return phases_data
    
    def generate_phase_summaries(self):
        """Generate individual phase summary JSON files"""
        metrics_csv = self.schema_dir / "gold_supply_chain_metrics.csv"
        
        if not metrics_csv.exists():
            logger.warning(f"{metrics_csv} not found - creating empty summaries")
            df = pd.DataFrame()
        else:
            df = pd.read_csv(metrics_csv)
        
        phases = range(8)
        
        for phase_id in phases:
            phase_data = df[df['phase_id'] == phase_id] if len(df) > 0 else pd.DataFrame()
            
            summary = {
                "phase_id": phase_id,
                "transparency": self._get_phase_transparency(phase_id),
                "total_records": len(phase_data),
                "last_update": str(phase_data['date'].max()) if len(phase_data) > 0 else None,
                "data_quality": self._assess_data_quality(phase_data),
                "metrics_available": phase_data['metric_name'].unique().tolist() if len(phase_data) > 0 else []
            }
            
            output_file = self.output_dir / f"phase{phase_id}_summary.json"
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info(f"✓ Generated {output_file}")
    
    def generate_simulation_defaults(self):
        """Generate default simulation configuration"""
        defaults = {
            "version": "1.0",
            "variables": [
                {
                    "variable_id": "ore_grade",
                    "display_name": "Ore Grade (g/t)",
                    "phase_id": 1,
                    "default_value": 3.5,
                    "min_value": 0.5,
                    "max_value": 15.0,
                    "unit": "g/t",
                    "description": "Grams of gold per tonne of ore",
                    "impact_phases": [1, 2],
                    "sensitivity": "high"
                },
                {
                    "variable_id": "recovery_rate",
                    "display_name": "Recovery Rate (%)",
                    "phase_id": 2,
                    "default_value": 92.0,
                    "min_value": 70.0,
                    "max_value": 98.0,
                    "unit": "percent",
                    "description": "Efficiency of gold extraction from ore",
                    "impact_phases": [2, 3],
                    "sensitivity": "medium"
                },
                {
                    "variable_id": "refining_capacity",
                    "display_name": "Refining Capacity (tonnes/year)",
                    "phase_id": 4,
                    "default_value": 2000,
                    "min_value": 500,
                    "max_value": 5000,
                    "unit": "tonnes/year",
                    "description": "Annual refinery throughput",
                    "impact_phases": [4, 5, 6, 7],
                    "sensitivity": "high"
                },
                {
                    "variable_id": "vault_capacity",
                    "display_name": "Vault Capacity (tonnes)",
                    "phase_id": 6,
                    "default_value": 500,
                    "min_value": 100,
                    "max_value": 2000,
                    "unit": "tonnes",
                    "description": "Total vault storage capacity",
                    "impact_phases": [6, 7],
                    "sensitivity": "medium",
                    "transparency_note": "Low visibility - structural opacity"
                }
            ],
            "time_horizon_days": 365,
            "baseline_scenario": "Current market conditions"
        }
        
        output_file = self.output_dir / "simulation_defaults.json"
        with open(output_file, 'w') as f:
            json.dump(defaults, f, indent=2)
        
        logger.info(f"✓ Generated {output_file}")
        return defaults
    
    def generate_transparency_report(self):
        """Generate transparency assessment report"""
        metrics_csv = self.schema_dir / "gold_supply_chain_metrics.csv"
        
        if not metrics_csv.exists():
            df = pd.DataFrame()
        else:
            df = pd.read_csv(metrics_csv)
        
        transparency_map = []
        
        phase_names = [
            "Geological Occurrence & Prospecting",
            "Mine Extraction",
            "Ore Processing & Concentration",
            "Doré Production",
            "Refining",
            "Bar Casting & Assay",
            "Logistics & Vaulting",
            "Exchange Registration"
        ]
        
        for phase_id in range(8):
            phase_data = df[df['phase_id'] == phase_id] if len(df) > 0 else pd.DataFrame()
            
            transparency_map.append({
                "phase_id": phase_id,
                "phase_name": phase_names[phase_id],
                "transparency_level": self._get_phase_transparency(phase_id),
                "data_sources": phase_data['source_type'].unique().tolist() if len(phase_data) > 0 else ["OPAQUE"],
                "record_count": len(phase_data),
                "opacity_reason": self._get_opacity_reason(phase_id)
            })
        
        report = {
            "transparency_map": transparency_map,
            "overall_score": self._calculate_transparency_score(transparency_map),
            "high_transparency_phases": [1, 2, 7],
            "low_transparency_phases": [6],
            "generated_at": datetime.now().isoformat()
        }
        
        output_file = self.output_dir / "transparency_report.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"✓ Generated {output_file}")
        return report
    
    def _get_phase_transparency(self, phase_id):
        """Get transparency level for a phase"""
        levels = {
            0: "Medium",
            1: "High",
            2: "High",
            3: "Medium",
            4: "Medium",
            5: "Medium-High",
            6: "Low",
            7: "High"
        }
        return levels.get(phase_id, "Unknown")
    
    def _get_opacity_reason(self, phase_id):
        """Get explanation for opacity level"""
        reasons = {
            0: "Geological uncertainty",
            1: "Public reporting requirements",
            2: "Engineering constraints provide visibility",
            3: "Private contracts, variable purity",
            4: "Refinery secrecy, selective disclosure",
            5: "Standards exist but serial data private",
            6: "Custodial secrecy, jurisdictional controls, insurance limits",
            7: "Exchange regulatory disclosure"
        }
        return reasons.get(phase_id, "Unknown")
    
    def _assess_data_quality(self, df):
        """Assess data quality for a phase"""
        if len(df) == 0:
            return "No data"
        elif len(df) < 10:
            return "Low"
        elif df['source_type'].str.contains('OPAQUE').any():
            return "Low"
        elif df['source_type'].str.contains('public').any():
            return "High"
        else:
            return "Medium"
    
    def _calculate_transparency_score(self, transparency_map):
        """Calculate overall transparency score (0-10)"""
        scores = {
            "High": 10,
            "Medium-High": 7.5,
            "Medium": 5,
            "Low": 2
        }
        
        total = sum(scores.get(phase['transparency_level'], 0) for phase in transparency_map)
        return round(total / len(transparency_map), 1)
    
    def generate_all(self):
        """Generate all frontend JSON files"""
        logger.info("Generating frontend data contracts...")
        
        self.generate_phases_json()
        self.generate_phase_summaries()
        self.generate_simulation_defaults()
        self.generate_transparency_report()
        
        logger.info("✓ All frontend data contracts generated")


def main():
    generator = FrontendDataGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()

