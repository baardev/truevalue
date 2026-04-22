"""
Synthetic Gold Supply Chain Data Generator

Generates realistic simulated N-D-C data for development and testing.

Scenarios:
1. Baseline: Healthy, balanced supply chain
2. Bottleneck: Phase 6 (Vaulting) severe D-C imbalance
3. Shock: Supply disruption at Phase 2 (day 50)
4. Optimization: System improving over time
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SyntheticGoldChainData:
    """Generate realistic simulated data for development"""
    
    def __init__(self, seed=42):
        """Initialize generator with random seed for reproducibility"""
        np.random.seed(seed)
        self.phase_names = [
            'Geological Prospecting',
            'Mine Extraction',
            'Ore Processing',
            'Doré Production',
            'Refining',
            'Bar Casting & Assay',
            'Logistics & Vaulting',
            'Exchange Registration'
        ]
    
    def calculate_ndc_metrics(self, D, C):
        """Calculate N-D-C metrics from D and C values"""
        imbalance = abs(D - C)
        max_val = max(D, C, 1.0)
        
        # Balance score: 100 when D=C, decays exponentially
        balance = 100 * np.exp(-2 * imbalance / max_val)
        
        # Sustainability: inverse of energy cost
        energy_cost = imbalance**2 + 10.0
        sustainability = 100.0 / energy_cost
        
        # N-state: emergent equilibrium
        N = np.sqrt(D * C) * (balance / 100.0)
        
        return {
            'n_value': N,
            'balance_score': balance,
            'sustainability_index': sustainability,
            'imbalance': imbalance
        }
    
    def generate_baseline_scenario(self, days=365):
        """
        Generate balanced, healthy supply chain data
        
        All phases maintain D ≈ C with natural variation
        """
        logger.info(f"Generating baseline scenario ({days} days)...")
        
        records = []
        start_date = datetime(2025, 1, 1)
        
        # Phase-specific base values (slightly different per phase)
        phase_D_base = [220, 260, 280, 240, 270, 260, 200, 280]  # D bases
        phase_C_base = [210, 250, 275, 235, 260, 255, 195, 275]  # C bases (slightly lower, balanced)
        
        for day in range(days):
            date = start_date + timedelta(days=day)
            
            for phase_id in range(8):
                # Add daily variation
                daily_noise_D = np.random.normal(0, 15)
                daily_noise_C = np.random.normal(0, 18)
                
                # Seasonal trend (simulate quarterly cycles)
                seasonal = 10 * np.sin(2 * np.pi * day / 90)
                
                D = phase_D_base[phase_id] + daily_noise_D + seasonal
                C = phase_C_base[phase_id] + daily_noise_C + seasonal * 0.8
                
                # Ensure positive values
                D = max(D, 50)
                C = max(C, 50)
                
                metrics = self.calculate_ndc_metrics(D, C)
                
                records.append({
                    'record_id': len(records) + 1,
                    'phase_id': phase_id,
                    'entity': f'{self.phase_names[phase_id]}_Entity',
                    'country': 'USA',
                    'date': date.strftime('%Y-%m-%d'),
                    'metric_type': 'daily_state',
                    'metric_category': 'ndc_balance',
                    'd_value': round(D, 2),
                    'c_value': round(C, 2),
                    'n_value': round(metrics['n_value'], 2),
                    'balance_score': round(metrics['balance_score'], 2),
                    'sustainability_index': round(metrics['sustainability_index'], 4),
                    'unit': 'index',
                    'source_type': 'simulated',
                    'source_name': 'Synthetic Generator - Baseline',
                    'url': None,
                    'notes': 'Baseline balanced scenario - healthy supply chain'
                })
        
        logger.info(f"✓ Generated {len(records)} baseline records")
        return pd.DataFrame(records)
    
    def generate_bottleneck_scenario(self, days=180):
        """
        Generate data with Phase 6 (Vaulting) bottleneck
        
        Phase 6 has severe D-C imbalance (D >> C)
        Adjacent phases feel pressure
        """
        logger.info(f"Generating bottleneck scenario ({days} days)...")
        
        records = []
        start_date = datetime(2025, 1, 1)
        
        for day in range(days):
            date = start_date + timedelta(days=day)
            
            for phase_id in range(8):
                if phase_id == 6:
                    # Phase 6: D-dominant (over-constrained vaulting)
                    D = np.random.normal(420, 20)  # Very high constraints
                    C = np.random.normal(180, 15)  # Low integration
                else:
                    # Other phases: moderate balance
                    D = np.random.normal(250, 20)
                    C = np.random.normal(240, 25)
                
                # Propagate stress to adjacent phases
                if phase_id == 5:  # Phase 5 (upstream of bottleneck)
                    # Feels back-pressure - inventory builds up
                    stress = 30 * np.sin(day / 10)
                    D += stress * 0.5
                    C -= stress * 0.3
                
                if phase_id == 7:  # Phase 7 (downstream of bottleneck)
                    # Starved for supply - variability increases
                    stress = 40 * np.sin(day / 8)
                    D += stress * 0.6
                    C -= stress * 0.4
                
                D = max(D, 50)
                C = max(C, 50)
                
                metrics = self.calculate_ndc_metrics(D, C)
                
                records.append({
                    'record_id': len(records) + 1,
                    'phase_id': phase_id,
                    'entity': f'{self.phase_names[phase_id]}_Entity',
                    'country': 'USA',
                    'date': date.strftime('%Y-%m-%d'),
                    'metric_type': 'daily_state',
                    'metric_category': 'ndc_balance',
                    'd_value': round(D, 2),
                    'c_value': round(C, 2),
                    'n_value': round(metrics['n_value'], 2),
                    'balance_score': round(metrics['balance_score'], 2),
                    'sustainability_index': round(metrics['sustainability_index'], 4),
                    'unit': 'index',
                    'source_type': 'simulated',
                    'source_name': 'Synthetic Generator - Bottleneck',
                    'url': None,
                    'notes': 'Bottleneck at Phase 6 (Vaulting) - severe D-C imbalance'
                })
        
        logger.info(f"✓ Generated {len(records)} bottleneck records")
        return pd.DataFrame(records)
    
    def generate_shock_scenario(self, days=120, shock_at=40):
        """
        Generate supply shock scenario
        
        Phase 2 (Ore Processing) loses major supplier at day 40
        Watch imbalance cascade downstream
        """
        logger.info(f"Generating shock scenario ({days} days, shock at day {shock_at})...")
        
        records = []
        start_date = datetime(2025, 1, 1)
        
        for day in range(days):
            date = start_date + timedelta(days=day)
            
            for phase_id in range(8):
                if day < shock_at:
                    # Pre-shock: normal balanced operations
                    D = np.random.normal(250, 15)
                    C = np.random.normal(245, 18)
                else:
                    # Post-shock
                    days_since = day - shock_at
                    
                    if phase_id == 2:
                        # Phase 2: Lost major supplier (C drops)
                        D = np.random.normal(250, 15)
                        C = np.random.normal(150, 20)  # Severe drop
                        
                    elif phase_id > 2:
                        # Downstream phases: cascade builds over time
                        impact = min(days_since / 15.0, 1.0)  # Full impact by day 15
                        
                        D = np.random.normal(250 + 60*impact, 15)  # Constraints increase
                        C = np.random.normal(245 - 50*impact, 18)  # Integration drops
                        
                    else:
                        # Upstream phases: slight ripple
                        impact = min(days_since / 30.0, 0.3)  # Mild impact
                        D = np.random.normal(250 + 20*impact, 15)
                        C = np.random.normal(245 - 15*impact, 18)
                
                D = max(D, 50)
                C = max(C, 50)
                
                metrics = self.calculate_ndc_metrics(D, C)
                
                records.append({
                    'record_id': len(records) + 1,
                    'phase_id': phase_id,
                    'entity': f'{self.phase_names[phase_id]}_Entity',
                    'country': 'USA',
                    'date': date.strftime('%Y-%m-%d'),
                    'metric_type': 'daily_state',
                    'metric_category': 'ndc_balance',
                    'd_value': round(D, 2),
                    'c_value': round(C, 2),
                    'n_value': round(metrics['n_value'], 2),
                    'balance_score': round(metrics['balance_score'], 2),
                    'sustainability_index': round(metrics['sustainability_index'], 4),
                    'unit': 'index',
                    'source_type': 'simulated',
                    'source_name': 'Synthetic Generator - Shock',
                    'url': None,
                    'notes': f'Supply shock at Phase 2 on day {shock_at} - cascade propagation'
                })
        
        logger.info(f"✓ Generated {len(records)} shock records")
        return pd.DataFrame(records)
    
    def generate_optimization_scenario(self, days=200):
        """
        Generate optimization trajectory
        
        System starts imbalanced, gradual improvements applied
        Shows sustainability increasing over time
        """
        logger.info(f"Generating optimization scenario ({days} days)...")
        
        records = []
        start_date = datetime(2025, 1, 1)
        
        # Start with significant imbalance
        initial_D = [300, 320, 310, 290, 305, 295, 350, 300]
        initial_C = [180, 190, 185, 175, 185, 180, 160, 190]
        
        # Target balanced state
        target_D = [250, 260, 255, 245, 255, 250, 245, 260]
        target_C = [245, 255, 252, 240, 252, 248, 240, 255]
        
        for day in range(days):
            date = start_date + timedelta(days=day)
            
            # Optimization progress (sigmoid curve)
            progress = 1.0 / (1.0 + np.exp(-0.05 * (day - 100)))
            
            for phase_id in range(8):
                # Interpolate between initial and target
                D_base = initial_D[phase_id] + (target_D[phase_id] - initial_D[phase_id]) * progress
                C_base = initial_C[phase_id] + (target_C[phase_id] - initial_C[phase_id]) * progress
                
                # Add noise
                D = D_base + np.random.normal(0, 10)
                C = C_base + np.random.normal(0, 10)
                
                D = max(D, 50)
                C = max(C, 50)
                
                metrics = self.calculate_ndc_metrics(D, C)
                
                records.append({
                    'record_id': len(records) + 1,
                    'phase_id': phase_id,
                    'entity': f'{self.phase_names[phase_id]}_Entity',
                    'country': 'USA',
                    'date': date.strftime('%Y-%m-%d'),
                    'metric_type': 'daily_state',
                    'metric_category': 'ndc_balance',
                    'd_value': round(D, 2),
                    'c_value': round(C, 2),
                    'n_value': round(metrics['n_value'], 2),
                    'balance_score': round(metrics['balance_score'], 2),
                    'sustainability_index': round(metrics['sustainability_index'], 4),
                    'unit': 'index',
                    'source_type': 'simulated',
                    'source_name': 'Synthetic Generator - Optimization',
                    'url': None,
                    'notes': f'Optimization trajectory - progress: {progress:.2%}'
                })
        
        logger.info(f"✓ Generated {len(records)} optimization records")
        return pd.DataFrame(records)


def main():
    """Generate all scenarios and save to files"""
    generator = SyntheticGoldChainData(seed=42)
    
    # Use absolute path relative to project root
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate scenarios
    scenarios = {
        'baseline': generator.generate_baseline_scenario(days=365),
        'bottleneck': generator.generate_bottleneck_scenario(days=180),
        'shock': generator.generate_shock_scenario(days=120, shock_at=40),
        'optimization': generator.generate_optimization_scenario(days=200)
    }
    
    # Save individual scenarios
    for name, df in scenarios.items():
        output_file = output_dir / f"scenario_{name}.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✓ Saved {output_file}")
        
        # Print summary
        avg_balance = df['balance_score'].mean()
        avg_sustainability = df['sustainability_index'].mean()
        logger.info(f"  Avg Balance: {avg_balance:.2f}, Avg Sustainability: {avg_sustainability:.4f}")
    
    # Use baseline as default dataset
    baseline_file = project_root / "schema" / "gold_supply_chain_metrics_ndc.csv"
    
    # Just save baseline directly (already has correct header)
    scenarios['baseline'].to_csv(baseline_file, index=False)
    logger.info(f"\n✓ Loaded baseline scenario into {baseline_file}")
    logger.info(f"  {len(scenarios['baseline'])} records now available")
    
    print("\n" + "="*60)
    print("✅ Synthetic Data Generation Complete")
    print("="*60)
    print("\nGenerated Scenarios:")
    for name in scenarios.keys():
        print(f"  • {name.capitalize()}: data/processed/scenario_{name}.csv")
    print(f"\nActive Dataset: schema/gold_supply_chain_metrics_ndc.csv (baseline)")
    print(f"Total Records: {len(scenarios['baseline'])}")
    print("\nNext: Analyze data with Jupyter notebooks or run simulations")


if __name__ == "__main__":
    main()

