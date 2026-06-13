#!/usr/bin/env python3
"""Rebuild the Phase Intervention Worksheet for photosynthesis using the current standard model."""
import re
import sys
sys.path.insert(0, '/home/jw/src/tv/scripts')
from worksheet_helpers import inject_rebuild, worksheet, bottleneck_block

FILE = '/home/jw/src/tv/frontend/project/photosynthesis/energy_chain/project_context.html'

# Photosynthesis data from JSON:
# pi=95.4 (chain average), phi=74.2, sqrt2=81.0, ln2=65.5, e=0
# phases: 0(94.1), 1(96.1), 2(98.0), 3(98.0), 4(97.9), 5(85.2 stressed), 6(97.9), 7(95.7)
# bottleneck: phase 5 Rubisco carbon fixation, D=270, C=230

inject_rebuild(FILE, worksheet(
    'Photosynthesis Energy Chain', 95.4,
    pi=95.4, phi=74.2, sq2=81.0, ln2=65.5, e=0,
    axis_note=(
        'Phase 5 Rubisco Carbon Fixation (85.2%) is the sole bottleneck: it is the only '
        'phase below the chain pi score (95.4%). The chain is otherwise highly Coherent. '
        'phi (74.2) identifies a value distribution failure: the photosynthesis chain is '
        'disproportionately efficient at light capture (Phases 0-4, 97-98%) but cannot '
        'distribute that energy gain proportionally to carbon fixation. '
        'ln2 (65.5) is the most stressed axis: it diagnoses the Rubisco oxygenase reaction '
        'as a transformation gap where 20-30% of enzyme active sites are wasted on O2 '
        'instead of CO2, representing a fundamental kinetic limitation. '
        'e (0) reflects that no financial abstraction layer exists in photosynthesis: '
        'this is a purely physical energy chain with no monetary instruments.'
    ),
    blocks=[
        bottleneck_block(5, 'Rubisco Carbon Fixation and Photorespiration', 85.2, 270, 230, 'ln2 and sqrt2 (√2)',
            '<strong>Why ln2 and sqrt2 diagnose this failure:</strong> D=270 reflects the '
            'constraint load of the Rubisco enzyme system: Rubisco (ribulose-1,5-bisphosphate '
            'carboxylase/oxygenase) is simultaneously the most abundant protein on Earth and '
            'the most catalytically inefficient enzyme in the photosynthesis pathway. Its dual '
            'specificity for CO2 and O2 means that at current atmospheric CO2:O2 ratios (0.04%:21%), '
            'approximately 20-30% of reactions produce 2-phosphoglycolate instead of 3-phosphoglycerate, '
            'initiating the photorespiratory bypass that consumes ATP and releases previously '
            'fixed CO2. This wasted reaction accounts for the entire D-C imbalance: '
            'D=270 (constraint: competitive oxygenation + regulatory overhead of '
            'photorespiration) vs C=230 (net carbon fixed per unit Rubisco active site). '
            'sqrt2 (81) identifies structural overhead: Rubisco\'s catalytic rate is '
            'physically constrained by its molecular architecture (3 reactions/second vs '
            '1,000+ for most enzymes), raising D through the large quantity of enzyme required. '
            'ln2 (65.5) is the most diagnostically significant axis: it identifies '
            'the transformation failure as a kinetic gap. The input (atmospheric CO2) is '
            'present; the conversion machinery (Rubisco) exists; but the transformation '
            'pathway cannot operate at full efficiency because the enzyme confuses substrate '
            'identity.',
            [
                ('C4 carbon-concentrating mechanism introduction',
                 'Engineer C4-type CO2 concentrating mechanism (bundle sheath + mesophyll '
                 'cell separation) into C3 crops following the IRRI C4 Rice Project protocol. '
                 'C4 mechanism pre-concentrates CO2 at Rubisco active sites to 10x atmospheric '
                 'concentration, effectively eliminating oxygenase reactions. '
                 'D-C mechanism: removes the oxygenase D-flag entirely; C increases by +20-30 '
                 'points as net carbon fixation rises 30-50% per unit leaf area. '
                 'Current status: IRRI C4 Rice Project; first field validation ~2030-2035.',
                 '85.2% to 93-96% (C4 pathway)'),
                ('Rubisco Sc/o specificity engineering (directed evolution)',
                 'Increase Rubisco CO2/O2 specificity factor (Sc/o) from current value (~80 '
                 'for C3 plants) toward the theoretical maximum (~200 for some red algae). '
                 'Each unit increase in Sc/o reduces the fractional oxygenase reaction rate, '
                 'directly reducing D. A 50% improvement in Sc/o reduces photorespiration by '
                 '~40%, adding +10-15 C-points and reducing D by ~8-12 points. '
                 'Current status: directed evolution campaigns underway (Zhu et al., 2022).',
                 '85.2% to 89-92% (partial Sc/o improvement)'),
                ('Photorespiratory bypass (glycolate-to-pyruvate shortcut)',
                 'Install a synthetic bypass route that converts photorespiratory glycolate '
                 'directly to pyruvate (re-entering the Calvin cycle) rather than releasing '
                 'CO2 through the full photorespiratory pathway. Reduces the energy cost '
                 'of photorespiration without requiring Rubisco modification. '
                 'D-C mechanism: C increases by +8-12 points (ATP recovery from what was '
                 'previously a carbon-releasing D-flag). '
                 'Current status: South et al. (2019, Science) demonstrated 20-40% yield '
                 'increase in tobacco in field conditions.',
                 '85.2% to 90-93% (bypass alone)'),
                ('Elevated atmospheric CO2 (CO2 fertilisation)',
                 'Operate in CO2-enriched environments (controlled atmosphere or open-top '
                 'chambers at 550-800 ppm CO2). Higher CO2:O2 ratio reduces oxygenase '
                 'reaction rate chemically. D-C mechanism: each 100 ppm CO2 increase '
                 'reduces the oxygenase fraction by approximately 5-8%, adding '
                 'proportional C-points. FACE (Free Air CO2 Enrichment) experiments '
                 'consistently show 10-20% yield increase at 550 ppm.',
                 '85.2% to 88-91% (550 ppm CO2)'),
            ],
            'Combined effect: C4 pathway (if achieved) removes the bottleneck entirely, '
            'raising Phase 5 to 93-96%. Photorespiratory bypass + elevated CO2 achievable '
            'on a 5-10 year horizon, raising Phase 5 to 90-93%. '
            'The fundamental ln2 constraint (Rubisco kinetics) requires either C4 '
            'engineering or Sc/o modification to fully resolve. '
            'Cross-reference: sqrt2 diagnoses the catalytic rate constraint; ln2 diagnoses '
            'the oxygenase specificity transformation failure; phi (74.2) confirms this '
            'single phase is disproportionately suppressing the otherwise near-perfect chain.'
        ),
    ]
))

print('Photosynthesis rebuilt.')
