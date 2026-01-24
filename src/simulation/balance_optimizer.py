"""
Balance Optimization and Sustainability Metrics

Implements tholonic optimization algorithms for achieving
optimal D-C balance across the supply chain.

Key Metrics:
- Balance Score: Proximity of D to C
- Sustainability Index: Energy efficiency (inverse of cost)
- Resilience: Capacity to absorb perturbations
- System Health: Overall thologram viability
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SustainabilityMetrics:
    """Calculate sustainability and balance metrics for supply chain phases"""
    
    @staticmethod
    def calculate_balance_score(D: float, C: float) -> float:
        """
        Calculate D-C balance score (0-100)
        
        Score = 100 when D = C
        Score → 0 as |D - C| increases
        
        Args:
            D: Total Definition parameter value
            C: Total Contribution parameter value
        
        Returns:
            Balance score (0-100)
        """
        if D == 0 and C == 0:
            return 0.0
        
        max_val = max(D, C, 1.0)
        imbalance = abs(D - C) / max_val
        
        # Exponential decay as imbalance increases
        balance = 100.0 * np.exp(-2 * imbalance)
        
        return balance
    
    @staticmethod
    def calculate_sustainability_index(D: float, C: float, energy_base: float = 10.0) -> float:
        """
        Calculate sustainability index based on tholonic energy principle
        
        Sustainability = 1 / Energy_cost
        Energy_cost = |D - C|² + E_base
        
        Higher sustainability = lower maintenance energy required
        
        Args:
            D: Total Definition
            C: Total Contribution  
            energy_base: Minimum baseline energy
        
        Returns:
            Sustainability index (higher is better)
        """
        imbalance = abs(D - C)
        energy_cost = imbalance**2 + energy_base
        
        sustainability = 100.0 / energy_cost
        
        return sustainability
    
    @staticmethod
    def calculate_resilience(balance_history: List[float], window: int = 10) -> float:
        """
        Calculate system resilience from balance history
        
        Resilience = ability to maintain balance despite perturbations
        Higher variance = lower resilience
        
        Args:
            balance_history: Time series of balance scores
            window: Rolling window size
        
        Returns:
            Resilience score (0-100)
        """
        if len(balance_history) < window:
            return 50.0  # Insufficient data
        
        recent = balance_history[-window:]
        variance = np.var(recent)
        
        # Lower variance = higher resilience
        resilience = 100.0 * np.exp(-variance / 100.0)
        
        return resilience
    
    @staticmethod
    def calculate_energy_efficiency(D: float, C: float, output: float) -> float:
        """
        Calculate energy efficiency: output per unit energy cost
        
        Args:
            D: Definition total
            C: Contribution total
            output: System output (e.g., throughput, production)
        
        Returns:
            Efficiency ratio
        """
        energy_cost = abs(D - C)**2 + 10.0
        
        if output == 0:
            return 0.0
        
        efficiency = output / energy_cost
        
        return efficiency
    
    @staticmethod
    def diagnose_imbalance(D: float, C: float, threshold: float = 0.2) -> Dict:
        """
        Diagnose type and severity of D-C imbalance
        
        Args:
            D: Definition total
            C: Contribution total
            threshold: Severity threshold (proportion)
        
        Returns:
            Diagnosis dict with type, severity, recommendations
        """
        if D == 0 and C == 0:
            return {
                'type': 'undefined',
                'severity': 0.0,
                'recommendation': 'Initialize parameters'
            }
        
        max_val = max(D, C)
        imbalance_ratio = abs(D - C) / max_val
        
        if imbalance_ratio < threshold:
            return {
                'type': 'balanced',
                'severity': imbalance_ratio,
                'recommendation': 'Maintain current balance'
            }
        
        if D > C:
            return {
                'type': 'D-dominant (over-constrained)',
                'severity': imbalance_ratio,
                'recommendation': f'Increase C parameters (currently {C:.1f}, target ~{D:.1f}) OR reduce D constraints',
                'failure_mode': 'Resource depletion, rigidity, isolation',
                'strategy': 'Enhance integration: supplier diversity, logistics flexibility, information sharing'
            }
        else:
            return {
                'type': 'C-dominant (over-integrated)',
                'severity': imbalance_ratio,
                'recommendation': f'Increase D parameters (currently {D:.1f}, target ~{C:.1f}) OR reduce C connections',
                'failure_mode': 'Identity loss, instability, resource dissipation',
                'strategy': 'Strengthen definition: specifications, quality standards, boundaries'
            }


class BalanceOptimizer:
    """Optimize D-C balance for sustainability and performance"""
    
    def __init__(self, D_params: Dict[str, float], C_params: Dict[str, float],
                 constraints: Optional[Dict] = None):
        """
        Initialize optimizer
        
        Args:
            D_params: Definition parameters {name: value}
            C_params: Contribution parameters {name: value}
            constraints: Optional constraints {param: (min, max)}
        """
        self.D_params = D_params.copy()
        self.C_params = C_params.copy()
        self.constraints = constraints or {}
        self.optimization_history = []
    
    def objective_function(self, D_total: float, C_total: float, 
                          weights: Dict[str, float]) -> float:
        """
        Multi-objective function combining sustainability, balance, and performance
        
        Args:
            D_total: Sum of D parameters
            C_total: Sum of C parameters
            weights: Importance weights {metric: weight}
        
        Returns:
            Objective value (higher is better)
        """
        # Sustainability (energy efficiency)
        sustainability = SustainabilityMetrics.calculate_sustainability_index(D_total, C_total)
        
        # Balance (D-C proximity)
        balance = SustainabilityMetrics.calculate_balance_score(D_total, C_total)
        
        # Performance (combined D*C representing capability)
        performance = np.sqrt(D_total * C_total) if D_total > 0 and C_total > 0 else 0
        
        # Weighted combination
        objective = (
            weights.get('sustainability', 0.4) * sustainability +
            weights.get('balance', 0.4) * balance +
            weights.get('performance', 0.2) * performance
        )
        
        return objective
    
    def optimize_gradient_ascent(self, iterations: int = 100, 
                                 learning_rate: float = 0.01,
                                 weights: Optional[Dict] = None) -> Dict:
        """
        Optimize using gradient ascent
        
        Args:
            iterations: Number of optimization steps
            learning_rate: Step size
            weights: Objective weights
        
        Returns:
            Optimized parameters and final metrics
        """
        weights = weights or {'sustainability': 0.4, 'balance': 0.4, 'performance': 0.2}
        
        for i in range(iterations):
            D_total = sum(self.D_params.values())
            C_total = sum(self.C_params.values())
            
            # Calculate gradient (numerical approximation)
            epsilon = 0.1
            
            # Gradient w.r.t. D
            obj_plus_d = self.objective_function(D_total + epsilon, C_total, weights)
            obj_minus_d = self.objective_function(D_total - epsilon, C_total, weights)
            grad_d = (obj_plus_d - obj_minus_d) / (2 * epsilon)
            
            # Gradient w.r.t. C
            obj_plus_c = self.objective_function(D_total, C_total + epsilon, weights)
            obj_minus_c = self.objective_function(D_total, C_total - epsilon, weights)
            grad_c = (obj_plus_c - obj_minus_c) / (2 * epsilon)
            
            # Update parameters
            for param in self.D_params:
                self.D_params[param] += learning_rate * grad_d / len(self.D_params)
                # Apply constraints
                self.D_params[param] = np.clip(self.D_params[param], 0, 100)
            
            for param in self.C_params:
                self.C_params[param] += learning_rate * grad_c / len(self.C_params)
                # Apply constraints
                self.C_params[param] = np.clip(self.C_params[param], 0, 100)
            
            # Record history
            current_state = {
                'iteration': i,
                'D_total': sum(self.D_params.values()),
                'C_total': sum(self.C_params.values()),
                'objective': self.objective_function(
                    sum(self.D_params.values()), 
                    sum(self.C_params.values()), 
                    weights
                )
            }
            self.optimization_history.append(current_state)
        
        # Final state
        D_final = sum(self.D_params.values())
        C_final = sum(self.C_params.values())
        
        return {
            'D_params': self.D_params,
            'C_params': self.C_params,
            'D_total': D_final,
            'C_total': C_final,
            'balance': SustainabilityMetrics.calculate_balance_score(D_final, C_final),
            'sustainability': SustainabilityMetrics.calculate_sustainability_index(D_final, C_final),
            'objective': self.objective_function(D_final, C_final, weights),
            'iterations': iterations,
            'history': self.optimization_history
        }
    
    def optimize_target_balance(self, target_ratio: float = 1.0, 
                               iterations: int = 50) -> Dict:
        """
        Optimize to achieve specific D/C ratio
        
        Args:
            target_ratio: Desired D/C ratio (1.0 = perfect balance)
            iterations: Optimization steps
        
        Returns:
            Optimized state
        """
        learning_rate = 0.05
        
        for i in range(iterations):
            D_total = sum(self.D_params.values())
            C_total = sum(self.C_params.values())
            
            if C_total == 0:
                current_ratio = float('inf')
            else:
                current_ratio = D_total / C_total
            
            error = current_ratio - target_ratio
            
            # Adjust parameters to reduce error
            if error > 0:  # D too high, increase C or decrease D
                for param in self.C_params:
                    self.C_params[param] += learning_rate * abs(error)
                for param in self.D_params:
                    self.D_params[param] -= learning_rate * abs(error) * 0.5
            else:  # C too high, increase D or decrease C
                for param in self.D_params:
                    self.D_params[param] += learning_rate * abs(error)
                for param in self.C_params:
                    self.C_params[param] -= learning_rate * abs(error) * 0.5
            
            # Clip to valid range
            for param in self.D_params:
                self.D_params[param] = np.clip(self.D_params[param], 0, 100)
            for param in self.C_params:
                self.C_params[param] = np.clip(self.C_params[param], 0, 100)
        
        D_final = sum(self.D_params.values())
        C_final = sum(self.C_params.values())
        
        return {
            'D_params': self.D_params,
            'C_params': self.C_params,
            'D_total': D_final,
            'C_total': C_final,
            'achieved_ratio': D_final / C_final if C_final > 0 else float('inf'),
            'target_ratio': target_ratio,
            'balance': SustainabilityMetrics.calculate_balance_score(D_final, C_final)
        }


class SystemHealthAnalyzer:
    """Analyze overall supply chain health using tholonic metrics"""
    
    def __init__(self, thologram_state: pd.DataFrame):
        """
        Initialize analyzer
        
        Args:
            thologram_state: DataFrame with phase states
        """
        self.state = thologram_state
    
    def calculate_system_health_score(self) -> Dict:
        """
        Calculate comprehensive system health
        
        Returns:
            Health metrics and diagnosis
        """
        if len(self.state) == 0:
            return {'health_score': 0, 'status': 'no data'}
        
        # Average sustainability across phases
        avg_sustainability = self.state['sustainability'].mean()
        
        # Average balance across phases
        avg_balance = self.state['balance'].mean()
        
        # Identify critical imbalances
        critical_phases = self.state[self.state['balance'] < 50]
        
        # Overall health score (weighted)
        health_score = 0.5 * avg_sustainability + 0.5 * avg_balance
        
        # Status determination
        if health_score > 80:
            status = 'excellent'
        elif health_score > 60:
            status = 'good'
        elif health_score > 40:
            status = 'fair'
        elif health_score > 20:
            status = 'poor'
        else:
            status = 'critical'
        
        return {
            'health_score': health_score,
            'status': status,
            'avg_sustainability': avg_sustainability,
            'avg_balance': avg_balance,
            'critical_phases': critical_phases['phase_id'].tolist() if len(critical_phases) > 0 else [],
            'phase_count': len(self.state)
        }
    
    def identify_weakest_links(self, n: int = 3) -> List[Dict]:
        """
        Identify phases with lowest sustainability/balance
        
        Args:
            n: Number of weakest links to return
        
        Returns:
            List of phase diagnoses
        """
        # Sort by combined health metric
        self.state['health'] = 0.5 * self.state['sustainability'] + 0.5 * self.state['balance']
        weakest = self.state.nsmallest(n, 'health')
        
        results = []
        for _, row in weakest.iterrows():
            diagnosis = SustainabilityMetrics.diagnose_imbalance(
                row['D_total'], 
                row['C_total']
            )
            diagnosis['phase_id'] = row['phase_id']
            diagnosis['health_score'] = row['health']
            results.append(diagnosis)
        
        return results


def main():
    """Example usage"""
    # Example: Phase 2 (Ore Processing) analysis
    D_params = {
        'D1:recovery_rate_target': 85.0,
        'D2:process_specifications': 70.0,
        'D3:purity_standards': 90.0,
        'D4:throughput_capacity': 80.0
    }
    
    C_params = {
        'C1:chemical_suppliers': 45.0,
        'C2:technology_integration': 60.0,
        'C3:water_sources': 50.0,
        'C4:byproduct_markets': 40.0
    }
    
    # Calculate initial metrics
    D_total = sum(D_params.values())
    C_total = sum(C_params.values())
    
    logger.info(f"Initial state: D={D_total:.1f}, C={C_total:.1f}")
    
    balance = SustainabilityMetrics.calculate_balance_score(D_total, C_total)
    sustainability = SustainabilityMetrics.calculate_sustainability_index(D_total, C_total)
    
    logger.info(f"Balance: {balance:.2f}, Sustainability: {sustainability:.2f}")
    
    # Diagnose imbalance
    diagnosis = SustainabilityMetrics.diagnose_imbalance(D_total, C_total)
    logger.info(f"Diagnosis: {diagnosis}")
    
    # Optimize
    optimizer = BalanceOptimizer(D_params, C_params)
    result = optimizer.optimize_gradient_ascent(iterations=100)
    
    logger.info(f"\nOptimized state:")
    logger.info(f"D={result['D_total']:.1f}, C={result['C_total']:.1f}")
    logger.info(f"Balance: {result['balance']:.2f}, Sustainability: {result['sustainability']:.2f}")


if __name__ == "__main__":
    main()

