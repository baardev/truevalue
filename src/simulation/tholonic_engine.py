"""
Tholonic Simulation Engine for Gold Supply Chain

Implements C-G-N (Constraints-Growth-Negotiation) dynamics
based on the Tholonic Framework for complex adaptive systems.

Core Concepts:
- C (Constraints):   Boundaries, specifications, limitations  [formerly D]
- G (Growth):        Integration, connections, flow, relationships  [formerly C]
- N (Negotiation):   Emergent equilibrium state (actual operational reality)

Sustainability emerges when C ≈ G (balanced system)
Energy cost = |C - G|² (imbalance penalty)

Balance score formula (exponential, 0-100 scale):
    B = 100 × exp(-2 × |C - G| / max(C, G))

This is consistent with the φ-score decay function used in phi_engine.py
and matches the TVPCI specification.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Tholon:
    """
    Fundamental tholonic unit representing a single supply chain phase
    
    Attributes:
        phase_id: Supply chain phase (0-7)
        D: Definition parameters (constraints, boundaries)
        C: Contribution parameters (connections, flows)
        N: Negotiation state (emergent equilibrium)
        balance: D-C balance score
        sustainability: Energy efficiency metric
    """
    
    def __init__(self, phase_id: int, D_params: Dict[str, float], 
                 C_params: Dict[str, float], energy_base: float = 10.0):
        self.phase_id = phase_id
        self.D_params = D_params
        self.C_params = C_params
        self.energy_base = energy_base
        
        self.D_total = sum(D_params.values())
        self.C_total = sum(C_params.values())
        self.N = None
        self.balance = None
        self.sustainability = None
        
        self._calculate_n_state()
    
    def _calculate_n_state(self):
        """
        Calculate emergent N-state from D and C parameters.

        Balance score — exponential form (0-100), consistent with φ-score decay:
            B = 100 × exp(-2 × |D - C| / max(D, C))
            B = 100 when D == C (perfect balance)
            B → 0 as imbalance grows

        N-state — emergent operational capacity:
            N = √(D × C) × (B / 100)
        """
        imbalance = abs(self.D_total - self.C_total)
        denom = max(self.D_total, self.C_total, 1.0)

        # Exponential balance score (0-100); matches TVPCI spec and phi_engine.py
        self.balance = 100.0 * np.exp(-2.0 * imbalance / denom)

        # Sustainability = 1 / energy_cost; energy cost minimises when D ≈ C
        energy_cost = imbalance ** 2 + self.energy_base
        self.sustainability = 100.0 / energy_cost

        # N-state: balance scaled back to 0-1 fraction for the geometric mean
        self.N = np.sqrt(self.D_total * self.C_total) * (self.balance / 100.0)

        return self.N
    
    def update_d_parameter(self, param_name: str, new_value: float):
        """Update a Definition parameter and recalculate N-state"""
        if param_name in self.D_params:
            self.D_params[param_name] = new_value
            self.D_total = sum(self.D_params.values())
            self._calculate_n_state()
    
    def update_c_parameter(self, param_name: str, new_value: float):
        """Update a Contribution parameter and recalculate N-state"""
        if param_name in self.C_params:
            self.C_params[param_name] = new_value
            self.C_total = sum(self.C_params.values())
            self._calculate_n_state()
    
    def get_state(self) -> Dict:
        """Return current tholon state"""
        return {
            'phase_id': self.phase_id,
            'D_total': self.D_total,
            'C_total': self.C_total,
            'N': self.N,
            'balance': self.balance,
            'sustainability': self.sustainability,
            'imbalance': abs(self.D_total - self.C_total),
            'energy_cost': abs(self.D_total - self.C_total)**2 + self.energy_base
        }
    
    def get_optimization_gradient(self) -> Tuple[float, float]:
        """
        Calculate gradient of sustainability with respect to D and C totals.

        Sustainability = 100 / (|D - C|² + E_base)

        Returns: (dS/dD, dS/dC) — both evaluated at current D_total, C_total.
        Note: balance is not differentiated here; use SustainabilityMetrics
        for balance-aware optimisation.
        """
        imbalance = self.D_total - self.C_total
        denominator = (imbalance**2 + self.energy_base)**2
        
        # Partial derivatives of sustainability
        dS_dD = -200.0 * imbalance / denominator
        dS_dC = 200.0 * imbalance / denominator
        
        return (dS_dD, dS_dC)


class Thologram:
    """
    Hierarchical structure of interconnected tholons
    Represents complete gold supply chain (Phases 0-7)
    """
    
    def __init__(self, schema_file: Path):
        self.tholons = {}
        self.interactions = {}
        self.history = []
        
        self._load_schema(schema_file)
    
    def _load_schema(self, schema_file: Path):
        """Load phase definitions and create tholons"""
        df = pd.read_csv(schema_file)
        
        for _, row in df.iterrows():
            phase_id = row['phase_id']
            
            # Parse D parameters
            D_params = {}
            if pd.notna(row['D_parameters']):
                for param in row['D_parameters'].split('|'):
                    name, default = param.split(':')
                    D_params[name] = 50.0  # Default value
            
            # Parse C parameters
            C_params = {}
            if pd.notna(row['C_parameters']):
                for param in row['C_parameters'].split('|'):
                    name, default = param.split(':')
                    C_params[name] = 50.0  # Default value
            
            energy_base = row.get('energy_base', 10.0)
            
            self.tholons[phase_id] = Tholon(phase_id, D_params, C_params, energy_base)
        
        logger.info(f"Loaded {len(self.tholons)} tholons from schema")
    
    def load_interactions(self, interaction_file: Path):
        """Load phase interaction definitions"""
        df = pd.read_csv(interaction_file)
        
        for _, row in df.iterrows():
            key = (row['from_phase'], row['to_phase'])
            self.interactions[key] = {
                'type': row['interaction_type'],
                'd_coupling': row['d_coupling'],
                'c_coupling': row['c_coupling'],
                'balance_transfer': row['balance_transfer'],
                'constraint_propagation': row['constraint_propagation']
            }
        
        logger.info(f"Loaded {len(self.interactions)} phase interactions")
    
    def propagate_constraints(self):
        """
        Propagate D-C imbalances through the supply chain
        
        When Phase i has D >> C, it constrains Phase i+1
        When Phase i has C >> D, it demands integration from Phase i+1
        """
        for (from_phase, to_phase), interaction in self.interactions.items():
            if from_phase not in self.tholons or to_phase not in self.tholons:
                continue
            
            from_tholon = self.tholons[from_phase]
            to_tholon = self.tholons[to_phase]
            
            # Calculate influence based on coupling strength
            d_coupling = interaction['d_coupling']
            c_coupling = interaction['c_coupling']
            
            # D-dominant upstream phase constrains downstream
            if from_tholon.D_total > from_tholon.C_total:
                d_pressure = (from_tholon.D_total - from_tholon.C_total) * d_coupling
                # Increase downstream D to match upstream constraint
                for param in to_tholon.D_params:
                    current = to_tholon.D_params[param]
                    to_tholon.update_d_parameter(param, current + d_pressure * 0.1)
            
            # C-dominant upstream phase demands integration downstream
            if from_tholon.C_total > from_tholon.D_total:
                c_pressure = (from_tholon.C_total - from_tholon.D_total) * c_coupling
                # Increase downstream C to handle flow
                for param in to_tholon.C_params:
                    current = to_tholon.C_params[param]
                    to_tholon.update_c_parameter(param, current + c_pressure * 0.1)
    
    def simulate_step(self, time_step: int, perturbations: Optional[Dict] = None):
        """
        Execute one simulation time step
        
        Args:
            time_step: Current time index
            perturbations: External shocks {phase_id: {'D': {}, 'C': {}}}
        """
        # Apply perturbations
        if perturbations:
            for phase_id, changes in perturbations.items():
                if phase_id in self.tholons:
                    if 'D' in changes:
                        for param, value in changes['D'].items():
                            self.tholons[phase_id].update_d_parameter(param, value)
                    if 'C' in changes:
                        for param, value in changes['C'].items():
                            self.tholons[phase_id].update_c_parameter(param, value)
        
        # Propagate constraints through chain
        self.propagate_constraints()
        
        # Record state
        state = {
            'time': time_step,
            'phases': {pid: t.get_state() for pid, t in self.tholons.items()}
        }
        self.history.append(state)
        
        return state
    
    def run_simulation(self, duration: int, perturbations_schedule: Optional[Dict] = None):
        """
        Run multi-step simulation
        
        Args:
            duration: Number of time steps
            perturbations_schedule: {time_step: perturbations_dict}
        
        Returns:
            List of states over time
        """
        logger.info(f"Starting simulation for {duration} steps")
        
        for t in range(duration):
            perturb = perturbations_schedule.get(t) if perturbations_schedule else None
            self.simulate_step(t, perturb)
        
        logger.info(f"Simulation complete. {len(self.history)} states recorded")
        return self.history
    
    def calculate_system_sustainability(self) -> float:
        """Calculate overall supply chain sustainability"""
        if not self.tholons:
            return 0.0
        
        # Weighted average of phase sustainabilities
        total_sustainability = sum(t.sustainability for t in self.tholons.values())
        return total_sustainability / len(self.tholons)
    
    def identify_bottlenecks(self) -> List[Tuple[int, str, float]]:
        """
        Identify phases with severe D-C imbalance
        
        Returns: [(phase_id, issue_type, severity), ...]
        """
        bottlenecks = []
        
        for phase_id, tholon in self.tholons.items():
            imbalance = abs(tholon.D_total - tholon.C_total)
            severity = imbalance / max(tholon.D_total, tholon.C_total, 1.0)
            
            if severity > 0.3:  # 30% imbalance threshold
                if tholon.D_total > tholon.C_total:
                    issue = "D-dominant (over-constrained, under-integrated)"
                else:
                    issue = "C-dominant (over-integrated, under-constrained)"
                
                bottlenecks.append((phase_id, issue, severity))
        
        return sorted(bottlenecks, key=lambda x: x[2], reverse=True)
    
    def optimize_balance(self, target_phase: int, iterations: int = 100) -> Dict:
        """
        Optimize D-C balance for a specific phase using gradient ascent
        
        Args:
            target_phase: Phase to optimize
            iterations: Optimization steps
        
        Returns:
            Optimized D and C values
        """
        if target_phase not in self.tholons:
            return {}
        
        tholon = self.tholons[target_phase]
        learning_rate = 0.01
        
        for i in range(iterations):
            dS_dD, dS_dC = tholon.get_optimization_gradient()
            
            # Gradient ascent (maximize sustainability)
            for param in tholon.D_params:
                current = tholon.D_params[param]
                new_value = current + learning_rate * dS_dD
                tholon.update_d_parameter(param, max(0, min(100, new_value)))
            
            for param in tholon.C_params:
                current = tholon.C_params[param]
                new_value = current + learning_rate * dS_dC
                tholon.update_c_parameter(param, max(0, min(100, new_value)))
        
        return tholon.get_state()
    
    def export_state(self) -> pd.DataFrame:
        """Export current state as DataFrame"""
        records = []
        for phase_id, tholon in self.tholons.items():
            state = tholon.get_state()
            state['timestamp'] = pd.Timestamp.now()
            records.append(state)
        
        return pd.DataFrame(records)


def main():
    """Example usage"""
    schema_file = Path("../../frontend/project/gold/data/schema/supply_chain_phases_ndc.csv")
    interaction_file = Path("../../frontend/project/gold/data/schema/phase_interactions_ndc.csv")
    
    # Create thologram (complete supply chain)
    thologram = Thologram(schema_file)
    thologram.load_interactions(interaction_file)
    
    # Check initial state
    logger.info(f"System sustainability: {thologram.calculate_system_sustainability():.2f}")
    
    # Identify bottlenecks
    bottlenecks = thologram.identify_bottlenecks()
    if bottlenecks:
        logger.info("Bottlenecks detected:")
        for phase_id, issue, severity in bottlenecks:
            logger.info(f"  Phase {phase_id}: {issue} (severity: {severity:.2f})")
    
    # Run simulation
    # Example: Phase 2 experiences capacity constraint increase at t=10
    perturbations = {
        10: {2: {'D': {'D4:throughput_capacity': 85.0}}}
    }
    
    history = thologram.run_simulation(duration=20, perturbations_schedule=perturbations)
    
    # Export results
    final_state = thologram.export_state()
    logger.info(f"\nFinal state:\n{final_state}")


if __name__ == "__main__":
    main()

