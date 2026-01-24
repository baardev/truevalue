#!/usr/bin/env python3
"""
Project Health Check

Validates project structure, schema files, and data pipeline.
Run this to verify everything is set up correctly.
"""

import sys
from pathlib import Path
import pandas as pd
import json

class HealthChecker:
    """Validate project setup"""
    
    def __init__(self, project_root=None):
        self.project_root = Path(project_root or Path(__file__).parent.parent)
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, name, condition, error_msg="", warning=False):
        """Check a condition"""
        if condition:
            print(f"✅ {name}")
            self.passed += 1
            return True
        else:
            if warning:
                print(f"⚠️  {name} {error_msg}")
                self.warnings += 1
            else:
                print(f"❌ {name} {error_msg}")
                self.failed += 1
            return False
    
    def run(self):
        """Run all health checks"""
        print("=" * 60)
        print("Gold Supply Chain Intelligence - Health Check")
        print("=" * 60)
        print()
        
        # 1. Directory Structure
        print("📁 Directory Structure")
        self.check("schema/", (self.project_root / "schema").exists())
        self.check("data/raw/", (self.project_root / "data/raw").exists())
        self.check("data/processed/", (self.project_root / "data/processed").exists())
        self.check("src/ingest/", (self.project_root / "src/ingest").exists())
        self.check("src/analysis/", (self.project_root / "src/analysis").exists())
        self.check("src/api/", (self.project_root / "src/api").exists())
        self.check("docs/", (self.project_root / "docs").exists())
        print()
        
        # 2. Schema Files
        print("📋 Schema Files")
        phases_file = self.project_root / "schema/supply_chain_phases.csv"
        metrics_file = self.project_root / "schema/gold_supply_chain_metrics.csv"
        flow_file = self.project_root / "schema/custody_and_flow.csv"
        sources_file = self.project_root / "schema/data_sources.csv"
        
        phases_ok = self.check("supply_chain_phases.csv", phases_file.exists())
        metrics_ok = self.check("gold_supply_chain_metrics.csv", metrics_file.exists())
        flow_ok = self.check("custody_and_flow.csv", flow_file.exists())
        sources_ok = self.check("data_sources.csv", sources_file.exists())
        
        # Validate phase count
        if phases_ok:
            try:
                phases = pd.read_csv(phases_file)
                self.check("8 phases defined", len(phases) == 8, f"Found {len(phases)}")
                self.check("Phase IDs 0-7", set(phases['phase_id']) == set(range(8)))
            except Exception as e:
                self.check("Phase validation", False, str(e))
        print()
        
        # 3. Core Scripts
        print("🐍 Core Scripts")
        self.check("comex_scraper.py", (self.project_root / "src/ingest/comex_scraper.py").exists())
        self.check("data_importer.py", (self.project_root / "src/ingest/data_importer.py").exists())
        self.check("generate_frontend_data.py", (self.project_root / "src/api/generate_frontend_data.py").exists())
        print()
        
        # 4. Analysis Notebooks
        print("📓 Analysis Notebooks")
        phase7_nb = self.project_root / "src/analysis/phase7_comex_analysis.ipynb"
        self.check("phase7_comex_analysis.ipynb", phase7_nb.exists())
        print()
        
        # 5. Frontend Data
        print("🌐 Frontend Data Contract")
        processed = self.project_root / "data/processed"
        
        phases_json_ok = self.check("phases.json", (processed / "phases.json").exists())
        sim_json_ok = self.check("simulation_defaults.json", (processed / "simulation_defaults.json").exists())
        trans_json_ok = self.check("transparency_report.json", (processed / "transparency_report.json").exists())
        
        # Check phase summaries
        phase_summaries = sum(1 for i in range(8) if (processed / f"phase{i}_summary.json").exists())
        self.check(f"{phase_summaries}/8 phase summaries", phase_summaries == 8, 
                   f"Missing {8 - phase_summaries} summaries")
        
        # Validate JSON structure
        if trans_json_ok:
            try:
                with open(processed / "transparency_report.json") as f:
                    report = json.load(f)
                self.check("Transparency score calculated", 
                           'overall_score' in report,
                           "Missing overall_score field")
            except Exception as e:
                self.check("JSON validation", False, str(e))
        print()
        
        # 6. Documentation
        print("📚 Documentation")
        self.check("README.md", (self.project_root / "README.md").exists())
        self.check("QUICKSTART.md", (self.project_root / "QUICKSTART.md").exists())
        self.check("docs/RULES.md", (self.project_root / "docs/RULES.md").exists())
        self.check("docs/FRONTEND_API.md", (self.project_root / "docs/FRONTEND_API.md").exists())
        print()
        
        # 7. Data Status
        print("📊 Data Status")
        
        # Check if any metrics data exists
        if metrics_ok:
            try:
                metrics = pd.read_csv(metrics_file)
                if len(metrics) > 0:
                    self.check(f"Metrics data loaded", True, f"{len(metrics)} records")
                    
                    # Phase coverage
                    phases_with_data = metrics['phase_id'].unique()
                    self.check(f"Phase coverage", True, 
                               f"Phases with data: {sorted(phases_with_data.tolist())}", 
                               warning=True)
                else:
                    self.check("Metrics data", False, 
                               "No data yet (run data collection)", warning=True)
            except Exception as e:
                self.check("Metrics validation", False, str(e))
        print()
        
        # Summary
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"✅ Passed:   {self.passed}")
        print(f"❌ Failed:   {self.failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        print()
        
        if self.failed == 0:
            print("🎉 Project structure is healthy!")
            if self.warnings > 0:
                print("⚠️  Some warnings detected (likely missing data - expected for new project)")
            return 0
        else:
            print("❌ Project has structural issues. Check failed items above.")
            return 1


def main():
    """Run health check"""
    checker = HealthChecker()
    exit_code = checker.run()
    
    if exit_code == 0:
        print()
        print("Next steps:")
        print("  1. Run COMEX scraper: python3 src/ingest/comex_scraper.py")
        print("  2. Import data: python3 -c 'from src.ingest.data_importer import GoldDataImporter; ...'")
        print("  3. Analyze Phase 7: jupyter notebook src/analysis/phase7_comex_analysis.ipynb")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()


