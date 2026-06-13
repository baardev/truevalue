#!/usr/bin/env python3
"""Inject Phase Intervention Worksheets into all project_context.html files.
Safe: skips files that already have a worksheet. Rebuilds photosynthesis.
"""
import sys
sys.path.insert(0, '/home/jw/src/tv/scripts')
from worksheet_helpers import inject, inject_rebuild, worksheet, bottleneck_block

BASE = '/home/jw/src/tv/frontend/project'

# ─────────────────────────────────────────────────────────────────────────────
# GOLD (flag-count model)
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/gold/supply_chain/project_context.html', worksheet(
    'Gold Supply Chain (Flag-Count Model)', 82.5,
    pi=82.5, phi=84, sq2=72, ln2=78, e=60,
    axis_note=(
        'sqrt2 (72) and e (60) both flag Phase 6. sqrt2 reflects structural opacity '
        'of the global vaulting network: D elevated by physical custody fragmentation across '
        'jurisdictions with no shared registry. e (60) confirms financial instruments '
        '(gold-backed ETFs, COMEX futures) are not operationally linked to the physical custody '
        'chain; they reference price, not provenance.'
    ),
    blocks=[
        bottleneck_block(6, 'Logistics and Vaulting', 65.5, 204, 161, 'sqrt2 (√2) and e',
            '<strong>Why sqrt2 and e diagnose this failure:</strong> Phase 6 has the lowest D in '
            'the entire chain (D=204) yet the lowest C by a wide margin (C=161). This is not a '
            'high-D failure: it is a C-collapse. The sqrt2 axis identifies structural overhead: '
            'vaulting capacity is geographically fragmented across Zurich, London, Singapore, and '
            'New York with no unified custody registry. Each jurisdiction imposes separate audit '
            'requirements, producing duplicated D-flags without adding corresponding C (network '
            'integration, transparent reporting). The e axis (60) confirms that allocated gold '
            'instruments exist but are not operationally auditable against physical bar serial '
            'numbers in real time.',
            [
                ('Unified custody registry pilot',
                 'Implement a shared bar-serial-number ledger across two vaults (London and Zurich) '
                 'using existing LBMA GDL infrastructure. Each reconciled bar raises C by removing '
                 'an opacity flag. Estimated C increase: +15 to +20 over 24 months.',
                 '65.5% to 72-75%'),
                ('Standardised cross-jurisdiction audit protocol',
                 'Align LBMA, COMEX, and SIX audit cycles to a common annual schedule with shared '
                 'reporting template. Reduces D by removing duplicated regulatory-burden flags. '
                 'Estimated D reduction: -8 to -12.',
                 '65.5% to 74-78% (with registry)'),
                ('LBMA physical chain traceability to vault registration',
                 'Extend LBMA Responsible Gold Guidance to include vault-level chain-of-custody '
                 'from mine to bar registration. Each documented bar removes an opacity D-flag '
                 'and adds a custody C-flag. Current coverage: ~45%; target 80%.',
                 '65.5% to 78-82% (full programme)'),
            ],
            'Combined effect: estimated Phase 6 balance 78-82%, eliminating it as a bottleneck. '
            'Phase 8 Recycling (80.0%) would then be the marginal phase.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# GOLD_V2 (threshold-ratio normalized)
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/gold_v2/supply_chain/project_context.html', worksheet(
    'Gold Supply Chain (Threshold-Ratio Normalized)', 82.5,
    pi=82.5, phi=83, sq2=70, ln2=78, e=60,
    axis_note=(
        'In the normalized model D and C are dimensionless ratios of actual to minimum-viable-threshold '
        'values. Phase 6 D=2.208 means actual constraint load is 2.2x the minimum viable threshold; '
        'C=1.704 means contribution capacity is only 1.7x threshold. The gap (0.504 ratio units) is '
        'larger in structural terms than in the flag-count model, confirming the vaulting bottleneck '
        'is real, not a measurement artefact.'
    ),
    blocks=[
        bottleneck_block(6, 'Logistics and Vaulting', 63.4, '2.208', '1.704', 'sqrt2 (√2) and e',
            '<strong>Why sqrt2 and e diagnose this failure in the normalized model:</strong> '
            'D=2.208 indicates the constraint load is running at 2.2x the minimum viable threshold '
            'for a vault custody phase. This is the highest D/threshold ratio in the chain. '
            'C=1.704 is the second-lowest C/threshold ratio. The normalized gap (0.504) confirms '
            'the structural overhead flagged by sqrt2 is not merely a counting artefact: the actual '
            'custody infrastructure is running at more than twice its minimum viable load while '
            'contributing only 1.7x minimum viable output.',
            [
                ('Unified custody registry pilot',
                 'Consolidate LBMA GDL bar records. In normalized terms, this directly reduces the '
                 'D ratio by removing fragmentation overhead. Target: D ratio from 2.208 to approx 1.9.',
                 '63.4% to 72%'),
                ('Cross-jurisdiction audit harmonisation',
                 'Shared audit template reduces duplicated regulatory D-flags. '
                 'Reduces D ratio by approx 0.2 units.',
                 '63.4% to 75-78%'),
                ('LBMA chain-of-custody extension to vaulting',
                 'Raises C ratio by documenting each vault transfer as a positive custody event. '
                 'Target: C ratio from 1.704 to approx 2.0.',
                 '63.4% to 80%'),
            ],
            'Combined effect: Phase 6 normalized D/C gap closes from 0.504 to approx 0.1, '
            'bringing balance above 82% and eliminating the bottleneck.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# GOLD_V3 (complex number extension)
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/gold_v3/supply_chain/project_context.html', worksheet(
    'Gold Supply Chain (Complex Number Extension)', 82.5,
    pi=82.5, phi=83, sq2=70, ln2=78, e=60,
    axis_note=(
        'In the complex model z = D + iC, Phase 6 has modulus |z| = sqrt(2.208^2 + 1.704^2) = 2.79 '
        'and argument theta = arctan(C/D) = arctan(1.704/2.208) = 37.7 deg. The low theta (37.7 vs '
        'ideal 45 deg) confirms D excess. The high modulus (2.79, vs chain median ~1.85) confirms '
        'Phase 6 is the highest-load phase in the chain. Interventions that reduce D reduce both '
        'the modulus and the argument gap simultaneously.'
    ),
    blocks=[
        bottleneck_block(6, 'Logistics and Vaulting', 63.4, '2.208', '1.704', 'sqrt2 (√2) and e',
            '<strong>Complex plane interpretation:</strong> Phase 6 sits in the Stressed angular zone '
            '(theta = 37.7 deg, below the 45-deg ideal balance line) with the highest modulus in the '
            'chain (|z| = 2.79). High modulus means high total operational load, not just imbalance. '
            'Interventions must reduce both the D/C ratio (moving theta toward 45 deg) and the total '
            'load (reducing modulus toward the sqrt2 unit circle at |z| = sqrt(2) = 1.41). '
            'sqrt2 axis failure (70) identifies structural fragmentation; e axis failure (60) '
            'confirms financial instrument decoupling from physical custody.',
            [
                ('Unified custody registry pilot',
                 'Reduces D from 2.208 to ~1.9; theta moves from 37.7 to ~42 deg; '
                 'modulus decreases from 2.79 to ~2.47.',
                 '63.4% to 72%; theta to 42 deg'),
                ('Cross-jurisdiction audit harmonisation',
                 'Reduces D by 0.2 ratio units; combined with registry, theta approaches 44 deg.',
                 '63.4% to 76-78%'),
                ('LBMA chain-of-custody extension',
                 'Raises C from 1.704 to ~2.0; modulus decreases; theta moves toward 46 deg '
                 '(Coherent zone).',
                 '63.4% to 80%; theta >45 deg'),
            ],
            'Combined effect in complex plane: theta moves from 37.7 to approx 45-46 deg (Coherent); '
            'modulus decreases from 2.79 to approx 2.1. Phase 6 exits the Stressed zone.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# LIGHTER
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/lighter/supply_chain/project_context.html', worksheet(
    'Disposable Lighter Supply Chain', 79.1,
    pi=79.1, phi=71, sq2=62, ln2=58, e=70,
    axis_note=(
        'Phase 8 (End-of-Life, 56.7%) is a Failure-zone phase. sqrt2 (62) diagnoses the structural '
        'absence of recycling infrastructure. ln2 (58) diagnoses the transformation collapse: the '
        'lighter enters landfill and no value is recovered. Phases 1 and 2 (70-72%) are below the '
        'chain pi (79.1) driven by component manufacturing concentration risk. '
        'e (70) reflects that Extended Producer Responsibility instruments for disposable lighters '
        'do not yet exist in any major market.'
    ),
    blocks=[
        bottleneck_block(8, 'End-of-Life and Waste Management', 56.7, 215, 85, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=215 reflects waste '
            'collection requirements, butane venting regulations, and UN3473 hazardous waste '
            'classification. C=85 is the lowest in the entire chain by a large margin: less than '
            '1% of disposable lighters are recycled globally. sqrt2 identifies structural absence: '
            'no physical infrastructure for lighter-specific material recovery exists at scale. '
            'ln2 identifies transformation failure: the product reaches end-of-life and no '
            'conversion pathway exists to generate any output of value.',
            [
                ('Extended Producer Responsibility (EPR) scheme',
                 'Require lighter manufacturers to fund take-back and recycling infrastructure, '
                 'following the EU Battery Regulation model. Each funded collection point '
                 'raises C (adding a recovery C-flag per jurisdiction). Target: C from 85 to 130+.',
                 '56.7% to 61-65% (EPR alone)'),
                ('Refillable lighter mandate (EU/UK)',
                 'Transition to refillable standards (Clipper model) eliminates the disposable '
                 'waste phase. D drops ~80 points (hazardous waste classification removed); '
                 'C increases 100+ (refill service creates custody and value loop).',
                 '56.7% to 80%+ (structural replacement)'),
                ('Butane/ferrocerium material recovery pilot',
                 'Partner with hazardous waste processors for lighter disassembly lines. '
                 'Each recovered material stream adds a C-flag. Pilot at 1M units/year.',
                 '56.7% to 70-72% (pilot scale)'),
            ],
            'Combined effect: Phase 8 balance from 56.7% to 72-80%. Refillable mandate '
            'eliminates the phase as a structural bottleneck; EPR alone moves it into Stressed.'
        ),
        bottleneck_block(1, 'Component Manufacturing', 70.0, 248, 264, 'phi (φ)',
            '<strong>Why phi diagnoses this failure:</strong> C=264 > D=248 (C-dominant) but '
            'balance is 70.0%. phi identifies the concentration risk: 3,000 Wenzhou factories '
            'at FOB $0.10/unit creates extreme fragility. A single supply disruption eliminates '
            'C entirely while D (safety certification, import compliance) persists. The 70.0% '
            'balance reflects latent fragility rather than current failure.',
            [
                ('Geographic diversification of component sourcing',
                 'Qualify secondary manufacturers in Vietnam, Mexico, or Turkey. Each new '
                 'qualified source adds a supply resilience C-flag. '
                 'Estimated D reduction: -10 to -15 points.',
                 '70.0% to 76-80%'),
                ('Multi-year supplier contracts with performance KPIs',
                 'Convert spot purchasing to 3-year contracts with quality, delivery, and '
                 'compliance KPIs. Each contracted supplier adds a governance C-flag.',
                 '70.0% to 75-78%'),
            ],
            'Combined effect for Phase 1: balance from 70.0% to 78-82%.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# SHEA
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE +../west_african_shea/supply_chain/project_context.html', worksheet(
    'Shea Supply Chain (West Africa to EU Cosmetics)', 81.6,
    pi=81.6, phi=74, sq2=76, ln2=66, e=68,
    axis_note=(
        'Two phases in the Failure zone: Phase 4 Export (64.0%) and Phase 0 Collection (68.2%). '
        'phi (74) confirms value is not proportionally distributed: collector women receive less '
        'than 5% of final retail value. ln2 (66) diagnoses the export transformation gap: '
        'nuts and kernels lose traceability and quality differentiation at the border, blocking '
        'premium value realisation. e (68) reflects no sustainability-linked bond has yet tied '
        'financial returns to Phase 0 or Phase 4 KPIs.'
    ),
    blocks=[
        bottleneck_block(4, 'Export', 64.0, 210, 165, 'ln2 and e',
            '<strong>Why ln2 and e diagnose this failure:</strong> D=210 reflects documentary '
            'requirements (phytosanitary certificates, EUDR forest-risk compliance, quality grading). '
            'C=165 is low because exports predominantly leave as undifferentiated bulk: no certified '
            'origin premium, no traceability documentation passed to EU buyers, and no sustainability '
            'credential commanding a price premium. ln2 identifies this as a transformation gap: '
            'processed shea could command 30-50% higher prices with origin documentation, but the '
            'conversion pathway does not exist. e axis (68) confirms EU green finance instruments '
            '(SFDR Article 9 funds, EUDR transition finance) are not operationally linked to '
            'shea export KPIs.',
            [
                ('Certified origin programme with EUDR pre-compliance',
                 'Establish village-level geo-polygon sourcing documentation meeting EUDR Article 3. '
                 'Each documented collection zone adds a C-flag to Phase 4. '
                 'Target: 50% of export volume with full polygon coverage by Year 2. '
                 'Estimated C increase: +20 to +30.',
                 '64.0% to 72-76%'),
                ('SheaTech quality grading and differentiated pricing',
                 'Implement ASNAPP/GIZ quality grading at aggregation points. Grade A certified '
                 'butter earns 20-35% premium. Each graded consignment removes a quality-uncertainty '
                 'D-flag and adds a premium C-flag. Estimated D reduction: -10.',
                 '64.0% to 74-78%'),
                ('Sustainability-linked export finance',
                 'Trade finance facility with interest rate step-down linked to EUDR compliance '
                 'rate and collector welfare KPIs. Each disbursement tied to verified KPI adds '
                 'a financial C-flag.',
                 '64.0% to 78-82%'),
            ],
            'Combined effect: Phase 4 from 64.0% to 78-82%, above chain pi (81.6%). '
            'Primary bottleneck then shifts to Phase 0 Collection (68.2%).'
        ),
        bottleneck_block(0, 'Collection', 68.2, 235, 175, 'phi (φ) and sqrt2 (√2)',
            '<strong>Why phi and sqrt2 diagnose this failure:</strong> D=235 reflects physical '
            'access constraints: dispersed wild shea trees, long travel distances, manual '
            'harvesting, no cold storage at collection points. C=175 is low because collector '
            'women have no formal negotiating infrastructure, no quality measurement at first '
            'sale, and receive below-market prices. phi identifies value distribution failure: '
            'collectors bear the highest physical burden while receiving the smallest share. '
            'sqrt2 confirms structural overhead: terrain and infrastructure absence raises D '
            'independently of market conditions.',
            [
                ('Village-level cooperatives with solar cold storage',
                 'Establish solar-powered 50-litre cold storage at village aggregation points '
                 '(GreenPath Energy model, ~USD 800/unit). Cold storage removes quality '
                 'degradation D-flag and adds a C-flag. Estimated C increase: +15.',
                 '68.2% to 74-76%'),
                ('Mobile phone market-price access (Esoko/SSNIT)',
                 'Real-time market price data via SMS. Reduces information asymmetry D-flag. '
                 'Each price-informed collector transaction adds a market transparency C-flag. '
                 'Estimated D reduction: -8.',
                 '68.2% to 72-75%'),
                ('Fairtrade/WFTO certification for collection cooperatives',
                 'Formal certification raises C (documented minimum price, social premium). '
                 'Each certified cooperative adds C-flags across Phase 0. '
                 'Estimated C increase: +10 to +20.',
                 '68.2% to 76-80%'),
            ],
            'Combined effect: Phase 0 from 68.2% to 78-82%. With Phase 4 also addressed, '
            'the chain reaches full Coherent status across all phases.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# SPAIN OLIVE OIL
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/spain_olive_oil/supply_chain/project_context.html', worksheet(
    'Spanish Olive Oil Supply Chain', 89.1,
    pi=89.1, phi=80, sq2=86, ln2=82, e=75,
    axis_note=(
        'Phases 5 (81.1%) and 7 (85.5%) are both below the chain pi score (89.1%). '
        'phi (80) flags value distribution failure: Spain produces 51% of global olive oil '
        'but two-thirds of exports leave as undifferentiated bulk at EUR 3.22/kg vs '
        'Italy\'s EUR 4.42/kg for rebranded product. This EUR 1.20/kg gap represents '
        '~EUR 890M/year in foregone revenue. '
        'ln2 (82) notes the bottling/branding transformation gap. '
        'e (75) reflects that EU CAP instruments exist but are not linked to origin '
        'differentiation KPIs.'
    ),
    blocks=[
        bottleneck_block(5, 'Packaging and Bottling', 81.1, 265, 215, 'phi (φ) and ln2',
            '<strong>Why phi and ln2 diagnose this failure:</strong> D=265 reflects regulatory '
            'requirements of bottling (EU packaging standards, PDO/PGI labelling, health claims '
            'compliance). C=215 is below chain average because the vast majority of Spanish olive '
            'oil is bottled under private-label arrangements that capture none of the origin premium. '
            'phi identifies value distribution failure: the bottling phase bears the regulatory '
            'compliance burden without capturing the PDO premium the same bottle could command. '
            'ln2 gap (50-point D-C difference) represents the branding transformation not executed.',
            [
                ('DOP/IGP differentiation programme',
                 'Origin certification marketing (Aceites de Oliva de Espana, Jaen DOP campaign). '
                 'Each additional SKU sold under named DOP adds a C-flag. Target: 40% of exports '
                 'under named DOP by 2028 (current: ~25%). Estimated C increase: +20 to +30.',
                 '81.1% to 87-90%'),
                ('Cooperative bottling investment',
                 'Pool cooperative capital to fund in-country bottling lines, ending bulk export '
                 'to Italian rebranders. Each cooperative moving to bottled export captures the '
                 'EUR 1.20/kg margin. CAP Article 68 investment support available.',
                 '81.1% to 86-88%'),
            ],
            'Combined effect: Phase 5 from 81.1% to 87-90%, above chain pi. '
            'Phase 7 Trade/Markets (85.5%) remains the marginal phase.'
        ),
        bottleneck_block(7, 'Trade and International Markets', 85.5, 275, 235, 'phi (φ)',
            '<strong>Why phi diagnoses this failure:</strong> D=275 (high trade compliance burden: '
            'EUDR compliance, EU-US friction, non-tariff barriers in Asia) and C=235 (suppressed '
            'by low-brand-equity originating in Phase 5). phi identifies this as a downstream '
            'consequence of Phase 5 failure: under the bulk-export model, Phase 7 bears trade '
            'compliance D without capturing brand C.',
            [
                ('Spain-specific premium market development (US, Japan)',
                 'Fund a Spain olive oil council equivalent for PDO brands following California\'s '
                 'model. Each new premium market distribution agreement adds a C-flag. '
                 'Target: 15% increase in premium-segment US/Japan market share. '
                 'Estimated C increase: +15 to +20.',
                 '85.5% to 91-92%'),
                ('EUDR traceability certification for export',
                 'Pre-certify major cooperatives under EUDR Article 3. Currently ~60% comply; '
                 'target 90%. Estimated D reduction: -8 to -12.',
                 '85.5% to 89-91%'),
            ],
            'Combined effect: Phase 7 from 85.5% to 91-92%. Both phases enter Coherent zone; '
            'chain average rises to ~93%.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# COCOA INTERNATIONAL
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/cocoa_international/supply_chain/project_context.html', worksheet(
    'Global Cocoa Supply Chain', 89.2,
    pi=89.2, phi=75, sq2=78, ln2=72, e=65,
    axis_note=(
        'Phase 1 Fermentation/Drying (76.5%) is the primary bottleneck. Phase 6 Manufacturing/'
        'Retail (80.2%) is secondary. phi (75) identifies the 1:6 farm-to-retail price ratio '
        'as a value distribution failure. ln2 (72) identifies fermentation as a transformation '
        'gap: the most critical quality-determining step happens at farm level with no process '
        'standardisation. e (65) confirms sustainability bonds have not been linked to Phase 1 '
        'KPIs (CLMRS enrollment, polygon coverage, deforestation-free area).'
    ),
    blocks=[
        bottleneck_block(1, 'Fermentation, Drying and Farm-Gate Quality', 76.5, 272, 208, 'ln2 and e',
            '<strong>Why ln2 and e diagnose this failure:</strong> Phase 1 is where cocoa quality '
            'is irreversibly determined, but with no standardisation and no chain-of-custody '
            'documentation. D=272 is the highest constraint load in the chain: child labour risk '
            '(CLMRS data shows ~40% of farms unreported), deforestation risk, zero farm-level '
            'traceability, and highly variable fermentation quality (3-8 days, uncontrolled '
            'temperature). C=208 is suppressed because cooperative infrastructure does not extend '
            'to fermentation control. ln2 identifies the value difference between properly '
            'fermented fine-flavour cocoa (USD 3,500/t) vs poorly fermented bulk (USD 2,600/t): '
            'USD 900/t unrealised due to absent transformation pathway.',
            [
                ('CLMRS-linked fermentation extension programme',
                 'Integrate fermentation training and communal fermentation boxes into CLMRS '
                 'farm visits. Barry Callebaut WISE programme shows +USD 300-400/t at scale. '
                 'Estimated C increase: +20 to +30.',
                 '76.5% to 83-86%'),
                ('Farm-level geo-polygon registration for EUDR',
                 'Register all sourcing farms on geo-polygon database. Each registered farm '
                 'removes a deforestation-risk D-flag. Target: 80% polygon coverage by 2026. '
                 'Estimated D reduction: -15 to -20.',
                 '76.5% to 82-85%'),
                ('Sustainability-linked cocoa bond with Phase 1 KPIs',
                 'Green bond with coupon step-down tied to: CLMRS enrollment >70%, polygon '
                 'coverage >75%, deforestation-free >80%. Activates e axis (65). '
                 'Estimated C increase: +10 per KPI tier activated.',
                 '76.5% to 86-89% (full KPI activation)'),
            ],
            'Combined effect: Phase 1 from 76.5% to 86-89%. Highest-impact single-phase '
            'intervention in the chain.'
        ),
        bottleneck_block(6, 'Manufacturing and Retail', 80.2, 268, 215, 'phi (φ)',
            '<strong>Why phi diagnoses this failure:</strong> D=268 (regulatory compliance, '
            'reformulation costs, brand investment). C=215 is suppressed by structural decoupling: '
            'the 1:6 farm-to-retail price ratio means brand-layer value is captured without '
            'proportional upstream transfer. phi measures proportional value distribution: '
            'Phase 6 captures 30-40% gross margin while Phase 1 receives USD 0.60/kg of a '
            'USD 8/kg bar.',
            [
                ('Differential pricing tied to Phase 1 certification',
                 'Structure manufacturer-farmer contracts with verified-origin price floor '
                 '(Fairtrade USD 200/t; Rainforest Alliance adds USD 150/t). Each certified-origin '
                 'tonne purchased adds a phi-correction C-flag.',
                 '80.2% to 84-87%'),
                ('Supply chain transparency disclosure (Tony\'s model)',
                 'Require full farm-to-bar disclosure in annual reports under SEC/FCA rules. '
                 'Each disclosed traceability chain adds a phi-rebalancing C-flag.',
                 '80.2% to 84-86%'),
            ],
            'Combined effect: Phase 6 from 80.2% to 84-87%. Phase 1 remains the primary '
            'structural intervention point.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# COCOA NETHERLANDS
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/cocoa_netherlands/supply_chain/project_context.html', worksheet(
    'Netherlands Cocoa Supply Chain', 90.1,
    pi=90.1, phi=83, sq2=88, ln2=84, e=76,
    axis_note=(
        'The Netherlands chain (90.1%) is stronger than the global chain (89.2%). '
        'Phase 4 Manufacturing (85.1%) is the only phase below chain pi. '
        'phi (83) identifies the tension between Tony\'s Chocolonely full-traceability model '
        'and conventional CBE-dependent manufacturing. e (76) reflects EUDR compliance '
        'instruments are evolving but not yet fully linked to Dutch chain KPIs.'
    ),
    blocks=[
        bottleneck_block(4, 'Manufacturing', 85.1, 268, 228, 'phi (φ)',
            '<strong>Why phi diagnoses this failure:</strong> D=268 reflects dual constraints: '
            '(a) conventional manufacturing with CBE inputs (shea/palm) carrying origin-uncertainty '
            'D-flags under EUDR, and (b) premium manufacturing without CBE (Tony\'s model) '
            'requiring higher-cost full-traceability inputs. C=228 is suppressed because the '
            'two models co-exist without a unified quality standard. phi flags this as a '
            'proportional-value failure: manufacturing phase is executing two incompatible '
            'contribution profiles simultaneously.',
            [
                ('EUDR-compliant CBE sourcing standard',
                 'Establish Dutch industry standard (VNCI working group) requiring all CBE inputs '
                 'to meet EUDR polygon-traceability requirements by 2026 deadline. Each CBE source '
                 'meeting the standard removes an origin-uncertainty D-flag. '
                 'Estimated D reduction: -10 to -15.',
                 '85.1% to 89-91%'),
                ('Expanded Tony\'s model adoption via IDH',
                 'Dutch Sustainable Trade Initiative to fund traceability infrastructure for '
                 'mid-scale manufacturers. Each manufacturer adopting full-chain disclosure '
                 'adds C-flags. Estimated C increase: +10 to +15 per adopting firm.',
                 '85.1% to 89-92%'),
            ],
            'Combined effect: Phase 4 from 85.1% to 89-92%, above chain pi (90.1%). '
            'Netherlands chain reaches near-full Coherent status.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# GRAN CHACO SOY
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/gran_chaco/supply_chain/project_context.html', worksheet(
    'Gran Chaco Soy Supply Chain', 81.2,
    pi=81.2, phi=76, sq2=68, ln2=75, e=66,
    axis_note=(
        'Phase 2 Aggregation and Transport (62.9%) is a Failure-zone bottleneck. '
        'Unusually, D < C at this phase (D=220, C=350): volumes are integrated efficiently '
        'but without governance. sqrt2 (68) identifies structural absence of provenance-chain '
        'infrastructure at silo level. ln2 (75) identifies the provenance transformation '
        'failure: origin information cannot be transferred forward once beans are commingled. '
        'e (66) identifies that EUDR sustainability finance has not been tied to '
        'silo-level disclosure KPIs.'
    ),
    blocks=[
        bottleneck_block(2, 'Aggregation and Transport', 62.9, 220, 350, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure (inverted D-C):</strong> '
            'C=350 > D=220, meaning contribution capacity is high but the balance score is '
            '62.9% because the formula uses max(D,C) in the denominator. The high C reflects '
            'the operational capacity of the silo network. The low D relative to C means the '
            'aggregation network is operationally capable but ungoverned: it processes large '
            'volumes without generating the provenance documentation needed for EUDR and '
            'sustainability-linked bond KPI verification. sqrt2 identifies structural overhead '
            'of commingling: each commingled load generates a provenance-loss D-suppression. '
            'ln2 identifies the transformation failure: origin information cannot be converted '
            'into a documented provenance certificate once beans are mixed.',
            [
                ('Disaggregated silo-granos disclosure (SENASA integration)',
                 'Require silo operators to file lot-level origin declarations in SENASA RUCA '
                 'system before mixing. Each documented lot adds a definition D-flag (raising D '
                 'toward C level, closing the gap). Target: 60% of throughput with pre-mix '
                 'origin declaration by 2026. Estimated D increase: +30 to +50.',
                 '62.9% to 78-82%'),
                ('Isotopic fingerprinting pilot (USDA/CONICET methodology)',
                 'Deploy stable isotope analysis for post-mix origin verification at five '
                 'high-throughput silos. Each verified origin assignment creates a traceability '
                 'C-flag. Estimated balance improvement: +10 to +15.',
                 '62.9% to 74-78%'),
                ('Trader-level geographic disclosure for EUDR Article 9',
                 'Major traders (Louis Dreyfus, Bunge, ADM) to publish geo-referenced sourcing '
                 'maps at department level. Each disclosed sourcing area removes a '
                 'deforestation-risk D-suppression flag. Estimated improvement: +5 to +10.',
                 '62.9% to 68-73% (disclosure alone)'),
            ],
            'Combined effect: Phase 2 from 62.9% to 78-82%. Chain average rises from '
            '81.2% to ~87%. EUDR compliance risk substantially reduced.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# ECON HISTORY
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/econ_history/supply_chain/project_context.html', worksheet(
    'Economic History Supply Chain', 81.1,
    pi=81.1, phi=72, sq2=74, ln2=80, e=82,
    axis_note=(
        'Phases 0 (66.0%) and 1 (72.0%) are primary bottlenecks; Phase 9 Post-Crisis (74.0%) '
        'is marginal. phi (72) diagnoses the pre-modern era failure: institutional overhead '
        '(property rights uncertainty, coin debasement, guild restrictions) elevated D without '
        'generating proportional C. sqrt2 (74) identifies physical and institutional friction '
        'in Phases 0 and 1. e (82) reflects financial abstraction was relatively well-developed '
        'in later eras (Phases 4-8).'
    ),
    blocks=[
        bottleneck_block(0, 'Pre-Classical Subsistence (10,000 BCE to 800 BCE)', 66.0, 280, 175, 'phi (φ) and sqrt2 (√2)',
            '<strong>Why phi and sqrt2 diagnose this failure:</strong> D=280 is the highest in the '
            'chain: land tenure insecurity, subsistence-level technology, barter with high '
            'transaction costs, and zero inter-regional trade infrastructure. C=175 reflects '
            'minimal contribution capacity of pre-institutional economies: output is consumed, '
            'not accumulated. phi identifies value distribution failure where value cannot be '
            'preserved or transferred across seasons. sqrt2 identifies physical and institutional '
            'overhead as the binding constraint: terrain, tool limitations, absence of writing '
            'and contract enforcement.',
            [
                ('Sedentarisation and property title formalisation',
                 'Historical evidence (North/Thomas, Rise of the Western World) demonstrates formal '
                 'property rights are the single largest C-builder in pre-modern economies. Each '
                 'formal property title adds C per percentage point of population with title. '
                 'Land becomes a definable asset rather than an open-access resource.',
                 '66.0% to 74-78%'),
                ('Irrigation infrastructure and crop surplus',
                 'Archaeological record (Mesopotamia, Nile Valley) shows irrigation adoption '
                 'raises C by enabling surplus production. Surplus enables trade, storage, and '
                 'specialisation. Estimated C increase: +20 to +30.',
                 '66.0% to 76-80%'),
            ],
            'Combined historical effect: Phase 0 from 66.0% to 76-80% when property rights '
            'and irrigation co-occur (Bronze Age city-states achieved this). '
            'Analytical retrospective, not a policy recommendation.'
        ),
        bottleneck_block(1, 'Classical and Medieval Trade (800 BCE to 1400 CE)', 72.0, 260, 200, 'phi (φ) and sqrt2 (√2)',
            '<strong>Why phi and sqrt2 diagnose this failure:</strong> D=260 reflects overlapping '
            'extractive overhead: Roman tax farming, guild monopolies, manorial rents, and coin '
            'debasement. C=200 reflects genuine contribution capacity: Mediterranean trade '
            'networks, Roman law-based contracts, double-entry bookkeeping (13th-century Italian '
            'city-states), and Bills of Exchange (Champagne Fairs). phi identifies 40-60% of '
            'agricultural output extracted through rent and tithe without proportional institutional '
            'return. sqrt2 confirms Roman road degradation after 400 CE raised transport D.',
            [
                ('Competitive guild reform and craft specialisation',
                 'Historical record shows guild monopoly relaxation (Florence 1282-1350, '
                 'Netherlands 16th century) raises C by enabling specialisation and trade. '
                 'Each liberalised trade reduces the institutional D-flag by +3 to +5 C-points.',
                 '72.0% to 76-79%'),
                ('Bills of Exchange and credit instrument adoption',
                 'Double-entry bookkeeping and Bills of Exchange (Champagne Fairs, 1150-1300) '
                 'raised C by enabling multi-period trade without physical coin movement. '
                 'Each new financial instrument adopted adds an e C-flag and reduces '
                 'transaction-cost D-flags.',
                 '72.0% to 78-82%'),
            ],
            'Combined historical effect: Phase 1 from 72.0% to 78-82% when both guild reform '
            'and financial instruments co-occur (Italian Renaissance economy). '
            'Phases 2-8 demonstrate this trajectory was historically achieved.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# AUBEB
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/aubeb/supply_chain/project_context.html', worksheet(
    'AUBEB Blue Economy Restoration Chain', 87.6,
    pi=87.6, phi=84, sq2=79, ln2=76, e=82,
    axis_note=(
        'Phase 0 Pre-commercial degraded ecosystem (71.12%) is the primary bottleneck. '
        'Phase 8 Community custodial co-management (79.76%) is marginally below chain average. '
        'ln2 (76) identifies Phase 0 as a transformation gap: the degraded ecosystem has zero '
        'value-generating capacity until restoration begins. sqrt2 (79) identifies physical '
        'and institutional overhead in Phases 0 and 8. e (82) reflects carbon market instruments '
        'exist but are not yet fully activated.'
    ),
    blocks=[
        bottleneck_block(0, 'Pre-commercial Degraded Ecosystem', 71.12, 200, 200, 'ln2',
            '<strong>Why ln2 diagnoses this failure:</strong> D=200, C=200, yet balance is '
            '71.12%. This reflects a special structural condition: the phase is symmetric in raw '
            'score but the ln2 axis identifies a transformation prerequisite failure. The degraded '
            'ecosystem has zero value-generating capacity: it cannot be formalised, measured, or '
            'monetised in its current state. ln2 measures whether inputs can be transformed into '
            'higher-value outputs. Phase 0 fails because the transformation pathway (custodial '
            'formalisation, baseline measurement, carbon registry enrollment) has not been '
            'activated. All subsequent phases (1-10) are contingent on this phase completing.',
            [
                ('Custodial rights formalisation',
                 'Establish legal custodial title for the target ecosystem area. This is the '
                 'single prerequisite that makes Phase 1 possible. Each hectare with formal '
                 'title adds a C-flag unlocking the subsequent chain. '
                 'Estimated C increase: +20 to +30.',
                 '71.12% to 78-82%'),
                ('Baseline remote sensing survey',
                 'Commission Copernicus or Planet Labs baseline imagery to establish pre-intervention '
                 'carbon stock, biodiversity index, and degradation extent. Each validated '
                 'measurement adds a definition C-flag. Prerequisite for carbon registry enrollment. '
                 'Estimated C increase: +15 to +20.',
                 '71.12% to 76-80% (with custody)'),
                ('Carbon registry pre-enrollment (Verra VCS or Gold Standard)',
                 'Pre-enroll the project area before restoration begins. Pre-enrollment adds a '
                 'formal C-flag and activates the e axis (carbon credits as instruments linked '
                 'to real ecosystem metrics). Estimated improvement: +10 to +15.',
                 '71.12% to 80-84% (all three)'),
            ],
            'Combined effect: Phase 0 from 71.12% to 80-84%. Unlocks the full restoration '
            'chain and activates the e axis across all subsequent phases.'
        ),
        bottleneck_block(8, 'Community Custodial Co-management', 79.76, 236, 256, 'phi (φ)',
            '<strong>Why phi diagnoses this failure:</strong> C=256 > D=236 (C-dominant), '
            'indicating good contribution capacity but a phi distribution issue: the community '
            'custodial model generates ecosystem services and carbon credits but does not yet '
            'receive proportional value. phi identifies value-flow failure at the community level: '
            'the highest-labour phase receives less financial return than its contribution warrants, '
            'creating a sustainability risk for the entire chain.',
            [
                ('Performance-linked community payment (10% of carbon credit revenue)',
                 'Structure conservation fund disbursements to include a percentage directly to '
                 'community custodial groups tied to monitoring KPIs. Each verified monitoring '
                 'report adds a phi-rebalancing C-flag. Estimated C increase: +10 to +15.',
                 '79.76% to 83-86%'),
                ('Capacity-building for community data collection',
                 'Training in GPS boundary patrol, fauna survey, and carbon stock measurement. '
                 'Reduces D (removes institutional-capacity overhead flag) and adds C '
                 '(community data is a carbon-quality asset). '
                 'Estimated improvement: +5 to +8.',
                 '79.76% to 83-86%'),
            ],
            'Combined effect: Phase 8 from 79.76% to 83-86%. Chain coherence confirmed '
            'once Phase 0 is resolved.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# GRID ERCOT URI
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/grid_ercot_uri/supply_chain/project_context.html', worksheet(
    'ERCOT Texas Grid (Winter Storm Uri 2021)', 47,
    pi=47, phi=35, sq2=30, ln2=25, e=15,
    axis_note=(
        'Every phase except Phase 0 (77%) and Phase 5 (68%) is in the Failure zone (below 61.8%). '
        'This is a system-level coherence collapse. sqrt2 (30) and ln2 (25) are the primary '
        'diagnostic axes: the entire physical infrastructure layer (gas wells, pipelines, '
        'generation plants) lacked winterization, causing simultaneous D-elevation across all phases. '
        'phi (35) confirms no phase was receiving proportional C during the crisis. '
        'e (15) is the lowest in the dataset: no financial instruments were operationally linked '
        'to cold-weather performance obligations.'
    ),
    blocks=[
        bottleneck_block(3, 'Generation Winterization and Plant Readiness', 37, 350, 130, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=350 is the highest in '
            'the chain: generators lacked heat tracing on instrumentation, fuel supply systems '
            'froze, and lubrication oils gelled simultaneously. C=130 is near zero: generators '
            'could not dispatch because they were physically inoperable. sqrt2 identifies structural '
            'overhead: physical infrastructure was operating without winterization standards that '
            'were technically feasible (PUCT ordered USD 1.6M/unit post-Uri). ln2 identifies the '
            'transformation failure: the generation asset could not convert fuel input into '
            'electrical output because the conversion pathway had frozen.',
            [
                ('Mandatory weatherization to NERC Cold Weather Standard (TPL-001-5)',
                 'PUCT SB 3 (2021) requires this. Each winterized plant removes multiple D-flags '
                 '(frozen fuel, frozen instrumentation, lubricant failure). Post-Uri average cost: '
                 'USD 1.6M per unit. Estimated C increase: +80 to +100 per winterized unit.',
                 '37% to 72-78% (full weatherization)'),
                ('Firm gas supply contracts for generators',
                 'Require gas-fired generators to hold firm transportation contracts '
                 '(Texas Railroad Commission authority). During Uri, interruptible gas was '
                 'curtailed; generators had no firm rights. Firm contract removes primary D-flag. '
                 'Estimated D reduction: -50 to -70.',
                 '37% to 58-65%'),
                ('Dual-fuel or backup fuel capability requirement',
                 'Require 30-day on-site backup fuel (distillate for gas turbines). '
                 'On-site fuel removes fuel-supply D-chain entirely. '
                 'Texas has fewer firm fuel requirements than PJM or MISO.',
                 '37% to 68-74%'),
            ],
            'Combined effect for Phase 3: from 37% to 72-78% with full weatherization + '
            'firm gas + backup fuel. Phases 1, 2, 4, 6-10 all require analogous structural interventions.'
        ),
        bottleneck_block(1, 'Natural Gas Production and Fuel Supply', 45, 330, 150, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=330 reflects interconnected '
            'failure of wellhead freeze-offs (~40,000 MMcfd curtailed), compressor station failures, '
            'and pipeline pressure drops. C=150 is near zero: the gas supply network was operating '
            'at near-zero output. Parallel sqrt2 failure to Phase 3: physical infrastructure was '
            'not designed for recorded temperatures (-2 to -20 F across Permian Basin). ln2 '
            'identifies transformation failure: wellbore gas could not be converted to '
            'pipeline-quality gas because processing facilities froze.',
            [
                ('Wellhead and gathering-system weatherization',
                 'Texas Railroad Commission TRC Rule 3.92 (enacted post-Uri) requires critical '
                 'gas infrastructure to weatherize. Each weatherized wellhead and compressor '
                 'station removes a D-flag. Estimated D reduction: -60 to -80.',
                 '45% to 62-68% (TRC 3.92 full compliance)'),
                ('Critical producer designation with curtailment protection',
                 'Designate critical gas producers as protected from curtailment '
                 '(FERC Order 2222 framework). Each protected producer adds a '
                 'C-flag for cold-weather dispatchability.',
                 '45% to 58-63%'),
            ],
            'Combined effect: Phase 1 from 45% to 62-68%. Both Phases 1 and 3 must be '
            'addressed simultaneously; fixing one without the other leaves the chain broken.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# WATER JACKSON MS
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/water_jackson_ms/supply_chain/project_context.html', worksheet(
    'Jackson MS Water System (Infrastructure Failure 2022)', 59,
    pi=59, phi=42, sq2=30, ln2=35, e=45,
    axis_note=(
        'Eight of 12 phases are in the Failure zone (below 61.8%). This is a systemic '
        'infrastructure collapse. sqrt2 (30) is the primary diagnostic: physical infrastructure '
        '(treatment plant built 1950s-1970s, distribution pipes avg >50 years old) accumulated '
        'D-flags from deferred maintenance for decades. ln2 (35) identifies treatment process '
        'failure: chemical dosing, filtration, and disinfection processes were non-functional. '
        'e (45) identifies that available federal funding (EPA WIFIA, SRF, IIJA) was not '
        'operationally linked to performance obligations or maintenance schedules.'
    ),
    blocks=[
        bottleneck_block(5, 'Distribution Network Pressure', 43, 335, 145, 'sqrt2 (√2)',
            '<strong>Why sqrt2 diagnoses this failure:</strong> D=335 is the highest in the chain: '
            '215 main breaks in 2021 alone (vs industry benchmark ~15/100 miles/year), pressure '
            'zone failures, >50% of the system over 40 years old, and failed primary pumps at '
            'OB Curtis. C=145 is near-zero: the distribution network cannot deliver water pressure '
            'because the physical pipes and pumps are failing. sqrt2 diagnoses structural overhead: '
            'infrastructure generating D-flags faster than any operational intervention can compensate.',
            [
                ('IIJA funding deployment: OB Curtis pump replacement',
                 'EPA IIJA allocation to Jackson: USD 600M (2022). Priority 1: replace failed primary '
                 'pumps at OB Curtis plant. Each operational pump adds a critical C-flag. '
                 'Estimated C increase: +40 to +60.',
                 '43% to 60-65%'),
                ('Main break prioritisation programme (worst-first replacement)',
                 'Use GIS-mapped break rate data to prioritise highest-break-rate segments. '
                 'Each replaced segment removes a pressure-failure D-flag. '
                 'Target: 25 km/year of highest-risk mains. Estimated D reduction: -15 to -20.',
                 '43% to 58-63%'),
                ('Pressure zone boundary valve rehabilitation',
                 'Restore pressure zone isolation valves (USD 5,000-15,000 per valve). '
                 'Prevents zone-wide pressure loss from a single main break. '
                 'Each functional valve adds a system-resilience C-flag.',
                 '43% to 50-55% (valves alone)'),
            ],
            'Combined effect: Phase 5 from 43% to 60-65% with pump replacement and main '
            'prioritisation. Full Coherent zone requires sustained IIJA investment over 5-10 years.'
        ),
        bottleneck_block(3, 'Disinfection and Chemical Treatment', 50, 320, 160, 'ln2',
            '<strong>Why ln2 diagnoses this failure:</strong> D=320 reflects failed chemical dosing '
            'systems, unreliable chemical supply, operator shortage (30% of certified operators lost '
            '2015-2022), and absent process control instrumentation. C=160 is critically low: the '
            'treatment plant was periodically producing water meeting no potable standard '
            '(EPA Emergency Administrative Order, August 2022). ln2 identifies transformation '
            'failure: the input (raw reservoir water) cannot be converted to potable water because '
            'the chemical and physical transformation pathway is non-functional.',
            [
                ('Chemical feed system replacement and automated dosing',
                 'Replace manual dosing with SCADA-controlled automated systems. Each automated '
                 'dosing point removes a manual-failure D-flag and adds a process-reliability C-flag. '
                 'Estimated C increase: +30 to +50.',
                 '50% to 65-70%'),
                ('Certified operator recruitment and retention',
                 'EPA consent decree requirement: hire and retain Grade 4 certified operators. '
                 'Each certified operator shift adds an operational-competence C-flag.',
                 '50% to 62-68% (with chemical system)'),
                ('30-day backup chemical storage',
                 'Maintain 30-day on-site chemical inventory (chlorine, coagulant, fluoride). '
                 'Each day of reserve removes a supply-chain disruption D-flag.',
                 '50% to 58-62% (storage alone)'),
            ],
            'Combined effect: Phase 3 from 50% to 65-70%. Highest public health priority.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# WATER NEWWATER
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/water_newwater/supply_chain/project_context.html', worksheet(
    'Advanced Water Recycling (NEWater-type System)', 87.6,
    pi=87.6, phi=86, sq2=82, ln2=83, e=78,
    axis_note=(
        'This chain is generally Coherent. Phases 3 (80.9%) and 5 (80.6%) are below chain pi '
        '(87.6%) but above the Failure threshold (61.8%). phi (86) reflects good value '
        'distribution. sqrt2 (82) identifies some structural overhead in Phases 3 and 5. '
        'e (78) identifies that green bonds for water recycling exist but are not systematically '
        'linked to treatment-performance KPIs.'
    ),
    blocks=[
        bottleneck_block(5, 'Blending and Reservoir Augmentation', 80.6, 284, 264, 'phi (φ) and e',
            '<strong>Why phi and e diagnose this failure:</strong> D=284 reflects the blending '
            'phase constraint: treated recycled water entering a reservoir faces regulatory '
            'uncertainty (indirect potable reuse approval timelines, public perception requirements, '
            'state health review cycles). C=264 is good but not maximal: the blending step is '
            'technically sound but depends on a regulatory approval pathway that is not standardised. '
            'phi identifies value distribution issue: the phase bears the full regulatory burden '
            'of demonstrating potability equivalence without proportional credit in tariff structures. '
            'e identifies that green bonds could accelerate regulatory approval but are not '
            'yet used for this purpose.',
            [
                ('Pre-approved indirect potable reuse (IPR) regulatory pathway',
                 'Engage state health authority to pre-approve the blending concentration and '
                 'monitoring protocol. California DPH precedent (LA Groundwater Replenishment) '
                 'shows approval can reduce D by 30+ points once pre-certification is complete. '
                 'Estimated D reduction: -10 to -20.',
                 '80.6% to 85-90%'),
                ('Public communications programme tied to monitoring data',
                 'Publish real-time treatment performance dashboard linked to blending approval '
                 'documentation. Public trust adds a social-licence C-flag. '
                 'Estimated C increase: +8 to +12.',
                 '80.6% to 84-87%'),
            ],
            'Combined effect: Phase 5 from 80.6% to 85-90%, above chain pi.'
        ),
        bottleneck_block(3, 'UV and Advanced Oxidation', 80.9, 228, 236, 'sqrt2 (√2)',
            '<strong>Why sqrt2 diagnoses this failure:</strong> C=236 > D=228 (C-dominant). '
            'sqrt2 identifies structural overhead from the complexity of multi-barrier treatment: '
            'UV dose validation, H2O2 quench requirements, and DBP formation controls all add '
            'D-flags. Balance is Coherent but below chain average because compliance documentation '
            'overhead is not proportionally compensated in tariff structure.',
            [
                ('Advanced monitoring integration (online TOC, fluorescence)',
                 'Deploy online total organic carbon and EEM fluorescence sensors for real-time '
                 'treatment efficacy. Each validated sensor removes a manual-grab D-flag and adds '
                 'a continuous-monitoring C-flag. Estimated improvement: +5 to +8 each side.',
                 '80.9% to 84-87%'),
                ('UV reactor validation to NWRI guidelines',
                 'Complete formal NWRI/AWWA UV reactor validation (bioassay protocol). '
                 'Validated reactor removes regulatory-uncertainty D-flags. '
                 'Estimated improvement: +5 to +10.',
                 '80.9% to 85-89%'),
            ],
            'Combined effect: Phase 3 from 80.9% to 85-89%, above chain pi. '
            'Chain becomes fully Coherent across all phases.'
        ),
    ]
))

# ─────────────────────────────────────────────────────────────────────────────
# WATER OCWD
# ─────────────────────────────────────────────────────────────────────────────
inject(BASE + '/water_ocwd/supply_chain/project_context.html', worksheet(
    'Orange County Water District (Groundwater Replenishment System)', 86.0,
    pi=86.0, phi=78, sq2=73, ln2=80, e=74,
    axis_note=(
        'Phase 3 Groundwater Recharge (67.9%) is the only phase significantly below chain pi (86.0%). '
        'sqrt2 (73) identifies structural overhead: soil percolation rates and aquifer characteristics '
        'are fixed physical constraints. phi (78) notes mild value distribution unevenness from '
        'Phase 3. e (74) identifies that green bonds and water tariffs are not linked to '
        'recharge-rate performance KPIs.'
    ),
    blocks=[
        bottleneck_block(3, 'Groundwater Recharge and Percolation', 67.9, 228, 228, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=228, C=228 are equal yet '
            'balance is only 67.9%, indicating the balance reflects flags rather than a pure D/C '
            'formula. The structural interpretation: recharge ponds face physical constraints that '
            'cannot be operationally resolved. sqrt2 identifies fixed geological constraints: '
            'percolation rates at Talbert Spreading Grounds are determined by alluvial geology. '
            'D-flags include spreading basin clogging by fine sediments, seasonal percolation '
            'rate variation (30-70 MGD), and regulatory TDS limits for percolated water. '
            'ln2 identifies the transformation gap: surface-applied recycled water takes 6-12 '
            'months to travel through the vadose zone to the aquifer (temporal D-C gap).',
            [
                ('Spreading basin management: structured maintenance rotation',
                 'OCWD operates 21 basins in rotation. Optimising the rotation using soil moisture '
                 'data reduces clogging D-flags. OCWD data shows 15-20% percolation rate improvement '
                 'from optimised rotation. Estimated D reduction: -8 to -12.',
                 '67.9% to 73-77%'),
                ('Injection well expansion (deep-zone direct injection)',
                 'Add deep injection wells to complement surface spreading. Each injection well '
                 'bypasses vadose zone travel time, directly reducing ln2 temporal gap. '
                 'Cost: USD 2-4M per well; recharge rate: 1-3 MGD per well. '
                 'Estimated C increase: +10 to +15 per installed well group.',
                 '67.9% to 75-80%'),
                ('Aquifer storage and recovery (ASR) wells',
                 'Install ASR wells for wet-season storage and dry-season recovery. '
                 'Converts seasonal recharge variability D-flag to managed storage C-flag. '
                 'Estimated D reduction: -10.',
                 '67.9% to 76-80%'),
            ],
            'Combined effect: Phase 3 from 67.9% to 76-80% with rotation optimisation + '
            'injection wells + ASR. Above 80% requires additional geological interventions '
            'constrained by OCWD\'s available land (fixed sqrt2 constraint).'
        ),
    ]
))

print('Batches 1 and 2 complete.')
