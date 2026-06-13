#!/usr/bin/env python3
"""Inject Phase Intervention Worksheets for all 12 Danube subprojects."""
import sys
sys.path.insert(0, '/home/jw/src/tv/scripts')
from worksheet_helpers import inject, worksheet, bottleneck_block

BASE = '/home/jw/src/tv/frontend/project/danube'

# ── HUMAN: COMMERCIAL FISHING ────────────────────────────────────────────────
# All phases below 80%: ph2 (72%), ph4 (74%), ph3 (77%), ph0 (78%), ph1 (80%)
inject(BASE + '/human_commercial_fishing/supply_chain/project_context.html', worksheet(
    'Danube Commercial Fishing Supply Chain', 76.2,
    pi=76.2, phi=74, sq2=70, ln2=72, e=65,
    axis_note=(
        'All five phases are below the Coherent threshold (80%). Chain balance 76.2%. '
        'phi (74) identifies a quota system that does not proportionally distribute access rights '
        'to all fisher groups. ln2 (72) reflects transformation failures at processing and '
        'cold chain (Phase 2, 72%). e (65) reflects no sustainability-linked bond or '
        'quota-performance instrument is in place for the Danube fishery.'
    ),
    blocks=[
        bottleneck_block(2, 'Processing, Cold Chain, and Preservation', 72.0, 260, 232, 'ln2 and sqrt2 (√2)',
            '<strong>Why ln2 and sqrt2 diagnose this failure:</strong> D=260 reflects the '
            'cold-chain infrastructure gap: the Danube corridor lacks the refrigerated transport '
            'and processing facility density that Baltic or North Sea fisheries have. C=232 is '
            'constrained by the short shelf life of freshwater fish (less than 48 hours without '
            'cold chain) and the fragmentation of small-scale processing operations. '
            'ln2 identifies the transformation failure: fish that leave the boat cannot be '
            'reliably converted to a shelf-stable or premium product before quality degrades. '
            'sqrt2 identifies structural overhead: the physical cold-chain gap raises D without '
            'adding C regardless of catch volume.',
            [
                ('Mobile cold-storage units at landing sites',
                 'Deploy refrigerated ISO containers (10-20 tonne capacity) at the six highest-volume '
                 'Danube landing sites. Each operational cold unit removes a quality-degradation D-flag '
                 'and adds a preservation C-flag. Estimated C increase: +10 to +15.',
                 '72.0% to 78-82%'),
                ('Shared cooperative processing facility',
                 'Pool fisher cooperative capital to fund a centralised filleting and vacuum-packing '
                 'facility. Each product-line added (fresh, smoked, vacuum-packed) adds a '
                 'value-added C-flag. EU EMFAF Rural Fisheries fund available. '
                 'Estimated C increase: +12 to +18.',
                 '72.0% to 80-84%'),
                ('Species traceability labelling (Aquatic Products Regulation compliance)',
                 'Apply catch-specific QR labels at landing. Each labelled batch removes a '
                 'species-fraud D-flag and adds a chain-of-custody C-flag.',
                 '72.0% to 76-79%'),
            ],
            'Combined effect: Phase 2 from 72% to 80-84%. This is the highest-impact single-phase '
            'intervention for the commercial fishing chain.'
        ),
        bottleneck_block(4, 'Revenue Capture and Sector Reinvestment', 74.0, 260, 236, 'phi (φ) and e',
            '<strong>Why phi and e diagnose this failure:</strong> D=260 (market access costs, '
            'wholesale margin extraction by intermediaries, certification overhead). C=236 reflects '
            'the sector\'s limited ability to retain value: most Danube fisher revenue is captured '
            'by middlemen, with limited reinvestment into gear, cold chain, or certification. '
            'phi identifies this as a value distribution failure. e identifies the absence of '
            'any performance-linked financial instrument for the fishery.',
            [
                ('Direct-to-consumer market development',
                 'Establish fish CSA (community-supported agriculture) model for Danube fishers. '
                 'Direct sales at 20-40% above wholesale. Each CSA subscription adds a C-flag. '
                 'Estimated C increase: +8 to +12.',
                 '74.0% to 79-82%'),
                ('Fishery improvement programme (FIP) with MSC pre-certification',
                 'Enroll the Danube commercial fishery in a FIP pathway toward MSC certification. '
                 'FIP status adds a phi-correction C-flag by documenting sustainable-yield basis. '
                 'Estimated D reduction: -5 to -8 (removes over-fishing risk D-flag).',
                 '74.0% to 78-81%'),
            ],
            'Combined effect: Phase 4 from 74% to 79-82%, above chain pi (76.2%).'
        ),
    ]
))

# ── HUMAN: COMMERCIAL NAVIGATION ─────────────────────────────────────────────
# ph2 (72%) worst, ph1 (78%), ph4 (78%), ph0 (83% coherent, ph3 (85%)
inject(BASE + '/human_commercial_navigation/supply_chain/project_context.html', worksheet(
    'Danube Commercial Navigation Supply Chain', 79.2,
    pi=79.2, phi=76, sq2=68, ln2=74, e=72,
    axis_note=(
        'Phase 2 Fairway Maintenance and Dredging (72.0%) is the primary bottleneck. '
        'Phases 1 and 4 (78%) are marginally below chain pi (79.2%). '
        'sqrt2 (68) identifies structural overhead: the Danube riverbed naturally accumulates '
        'sediment in critical navigational reaches (Romanian/Bulgarian sector, Iron Gates). '
        'ln2 (74) reflects the dredging-to-navigability transformation gap: dredging is capital '
        'intensive and politically contested across riparian states.'
    ),
    blocks=[
        bottleneck_block(2, 'Fairway Maintenance and Dredging', 72.0, 264, 232, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=264 reflects the '
            'combination of (a) natural sediment accumulation in the navigational channel, '
            '(b) political coordination requirements across 10 riparian states, '
            '(c) environmental permitting for dredging (EU WFD Article 4.7 exemptions required), '
            'and (d) equipment procurement cycles. C=232 is suppressed because the '
            'maintenance cycle is chronically underfunded relative to the rate of '
            'sedimentation: the fairway depth at critical sections (Giurgiu, Cernavoda) '
            'falls below the 2.5m minimum navigation draft repeatedly. '
            'sqrt2 identifies structural overhead: sediment is a physical constraint. '
            'ln2 identifies the transformation failure: the capital input (dredging funding) '
            'cannot be converted to navigational depth reliably because the institutional '
            'coordination mechanism (ICPDR Fairway Master Plan) is not fully funded.',
            [
                ('ICPDR Fairway Master Plan 2022-2027 full funding',
                 'The Danube Fairway Rehabilitation and Maintenance Plan requires EUR 280M over '
                 '5 years. Each funded dredging campaign removes a sediment D-flag and adds a '
                 'navigational-depth C-flag. TEN-T Cohesion Fund and CEF Transport available. '
                 'Estimated C increase: +15 to +20 per funded campaign.',
                 '72.0% to 79-83%'),
                ('Environmental impact pre-authorisation framework',
                 'Establish a standing WFD Article 4.7 exemption framework for routine maintenance '
                 'dredging. Pre-authorisation reduces permitting D-flag from 6-18 months to '
                 '60 days. Estimated D reduction: -10 to -15.',
                 '72.0% to 77-80%'),
                ('Continuous fairway depth monitoring (AIS + sonar)',
                 'Deploy real-time sonar buoys at 8 critical shallow sections. Real-time data '
                 'triggers early dredging before critical draft is reached. Each monitored '
                 'section adds a system-resilience C-flag.',
                 '72.0% to 75-78%'),
            ],
            'Combined effect: Phase 2 from 72% to 79-83%, above chain pi (79.2%).'
        ),
    ]
))

# ── HUMAN: CULTURAL HERITAGE MANAGEMENT ──────────────────────────────────────
# ph1 (76%), ph4 (78%), ph3 (81%), ph0 (82%), ph2 (86%)
inject(BASE + '/human_cultural_heritage_management/supply_chain/project_context.html', worksheet(
    'Danube Cultural Heritage Management Supply Chain', 80.6,
    pi=80.6, phi=77, sq2=74, ln2=79, e=68,
    axis_note=(
        'Phase 1 Site Preservation and Conservation (76.0%) is the primary bottleneck. '
        'Phase 4 Tourism Revenue and Sustainable Management (78.0%) is secondary. '
        'sqrt2 (74) identifies structural overhead: physical deterioration of archaeological sites '
        'and buildings under UNESCO and Council of Europe protection frameworks. '
        'e (68) reflects that EU cultural heritage bonds and tourism investment instruments '
        'are not yet operationally linked to site conservation KPIs.'
    ),
    blocks=[
        bottleneck_block(1, 'Site Preservation and Conservation', 76.0, 272, 240, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=272 reflects the '
            'constraint load of: (a) physical site deterioration from riverine flooding and '
            'erosion (especially Neolithic and Bronze Age sites in the Iron Gates gorge), '
            '(b) inadequate preventive conservation budgets across riparian state heritage agencies, '
            'and (c) conflicting legal frameworks for underwater archaeological sites '
            'in international river channels. C=240 is suppressed by the '
            'structural underfunding of conservation relative to inventory: more sites are '
            'documented than actively conserved. sqrt2 identifies physical erosion as the '
            'binding constraint. ln2 identifies the transformation gap: inventory data '
            'cannot be converted into conservation outcomes without capital.',
            [
                ('European Cultural Heritage Green Deal designation',
                 'Apply for EU Creative Europe and LIFE funding for Iron Gates archaeological '
                 'site protection. Each funded conservation project removes a deterioration D-flag '
                 'and adds a protected-site C-flag. Estimated C increase: +12 to +18.',
                 '76.0% to 82-86%'),
                ('Underwater site protection protocol (UNCLOS/UNESCO 2001 Convention)',
                 'Establish a transboundary underwater heritage protection protocol for the '
                 'Danube riverbed. Each protected underwater site removes a jurisdiction-gap '
                 'D-flag. Romania and Serbia have pending UNESCO nomination files.',
                 '76.0% to 79-82%'),
            ],
            'Combined effect: Phase 1 from 76% to 82-86%, above chain pi (80.6%).'
        ),
        bottleneck_block(4, 'Tourism Revenue and Sustainable Management', 78.0, 268, 252, 'phi (φ) and e',
            '<strong>Why phi and e diagnose this failure:</strong> D=268 (tourism infrastructure '
            'certification requirements, UNESCO buffer zone restrictions, seasonal visitor '
            'management obligations). C=252 reflects the limited ability of heritage sites '
            'to convert tourist visits into reinvestment capital for conservation. '
            'phi identifies value distribution failure: most tourism revenue is captured by '
            'hotel and transport operators outside the heritage zone. '
            'e identifies absence of a cultural tourism bond or revenue-sharing instrument.',
            [
                ('Cultural tourism revenue-sharing compact',
                 'Negotiate a tourism operator levy of 2% of accommodation revenue dedicated '
                 'to site conservation. Each hotel/operator joining the compact adds a '
                 'phi-rebalancing C-flag. Estimated C increase: +8 to +12.',
                 '78.0% to 82-84%'),
                ('Interpretive infrastructure investment',
                 'Fund visitor centres, trail infrastructure, and multilingual interpretation '
                 'at the five highest-volume sites. Each infrastructure addition reduces the '
                 'overcrowding D-flag (visitor pressure on unprotected sites). '
                 'EU ERDF Regional Development funding available.',
                 '78.0% to 81-84%'),
            ],
            'Combined effect: Phase 4 from 78% to 82-84%, above chain pi.'
        ),
    ]
))

# ── HUMAN: FLOODPLAIN FORESTRY OPERATIONS ────────────────────────────────────
# ph4 (70%), ph3 (73%), ph2 (77%), ph0 (79%), ph1 (82%)
inject(BASE + '/human_floodplain_forestry_operations/supply_chain/project_context.html', worksheet(
    'Danube Floodplain Forestry Supply Chain', 76.2,
    pi=76.2, phi=73, sq2=68, ln2=74, e=66,
    axis_note=(
        'Phase 4 Revenue Capture and Ecosystem Service Payments (70.0%) and Phase 3 Market Access '
        'and Certification (73.0%) are both below chain pi (76.2%) and in the stressed zone. '
        'phi (73) identifies a value distribution failure: floodplain timber commands no market '
        'premium despite ecosystem co-benefits. ln2 (74) identifies transformation failure at '
        'Phase 4: ecosystem service payments (carbon, biodiversity) are not yet capturing '
        'the non-timber value of floodplain forests. e (66) reflects no payment-for-ecosystem-services '
        'instrument is operational for this forestry type.'
    ),
    blocks=[
        bottleneck_block(4, 'Revenue Capture and Ecosystem Service Payments', 70.0, 260, 240, 'phi (φ) and e',
            '<strong>Why phi and e diagnose this failure:</strong> D=260 reflects the cost '
            'structure of floodplain forestry: flood-adapted species (poplar, willow) have '
            'lower timber value than upland species; harvest windows are restricted by flood '
            'seasonality; and carbon sequestration in floodplain soils is poorly quantified '
            'in current carbon accounting frameworks. C=240 reflects the limited revenue '
            'capture: timber revenues are the primary income, but floodplain forests provide '
            'substantial non-timber value (flood peak attenuation, sediment filtration, '
            'biodiversity corridor). phi identifies the value distribution failure: operators '
            'bear the full management cost without receiving the ecosystem service revenue. '
            'e identifies the absence of any instrument linking financial returns to '
            'measured ecosystem service delivery.',
            [
                ('LIFE IP Danube-FLOODPLAIN carbon crediting scheme',
                 'Enroll floodplain forest management units in EU LIFE-funded carbon market pilot '
                 '(Verra Verified Carbon Standard for wetland restoration). Each enrolled hectare '
                 'adds a carbon-credit C-flag. Estimated C increase: +10 to +15.',
                 '70.0% to 76-80%'),
                ('Payment-for-ecosystem-services (PES) contract with Water Framework Directive bodies',
                 'Structure PES contracts with downstream water utilities (Vienna, Bratislava, '
                 'Budapest) for flood peak attenuation and water quality services. Each signed '
                 'PES contract adds an e-axis C-flag. Estimated C increase: +8 to +12.',
                 '70.0% to 76-79%'),
            ],
            'Combined effect: Phase 4 from 70% to 76-80%, approaching chain pi (76.2%).'
        ),
        bottleneck_block(3, 'Market Access and Certification', 73.0, 268, 240, 'phi (φ) and sqrt2 (√2)',
            '<strong>Why phi and sqrt2 diagnose this failure:</strong> D=268 reflects FSC/PEFC '
            'certification overhead for floodplain operations (the audit cycle does not '
            'distinguish between standard forestry and floodplain-constrained operations). '
            'C=240 is suppressed because certified floodplain timber commands no price premium '
            'in current markets: buyers do not distinguish flood-regime timber from standard '
            'softwood. phi identifies value distribution failure: certification costs are '
            'borne by operators but no premium is captured.',
            [
                ('FSC/PEFC floodplain ecosystem service addendum',
                 'Work with FSC to develop a floodplain-specific ecosystem service endorsement '
                 'label. Each forest unit with the addendum adds a market-differentiation C-flag '
                 'and commands a small price premium. Estimated C increase: +5 to +8.',
                 '73.0% to 76-78%'),
                ('Procurement policy: public sector floodplain timber preference',
                 'Advocate for national public procurement policies to prefer certified '
                 'floodplain timber for construction projects. Each public procurement contract '
                 'adds a market C-flag. EU Timber Regulation Article 6 framework available.',
                 '73.0% to 76-79%'),
            ],
            'Combined effect: Phase 3 from 73% to 76-79%, at or above chain pi.'
        ),
    ]
))

# ── HUMAN: FRESHWATER SUPPLY INFRASTRUCTURE ──────────────────────────────────
# ph3 (81%) below chain pi (88.6%); all others coherent
inject(BASE + '/human_freshwater_supply_infrastructure/supply_chain/project_context.html', worksheet(
    'Danube Freshwater Supply Infrastructure', 88.6,
    pi=88.6, phi=87, sq2=83, ln2=88, e=80,
    axis_note=(
        'This chain is generally well-performing. Only Phase 3 Pressurized Distribution Network '
        '(81.0%) is below chain pi (88.6%). phi (87) reflects good value distribution. '
        'e (80) reflects that EU water utility bond instruments exist but are not fully '
        'linked to loss-reduction KPIs. sqrt2 (83) identifies moderate structural overhead '
        'in the distribution network (pipe age, non-revenue water losses).'
    ),
    blocks=[
        bottleneck_block(3, 'Pressurized Distribution Network', 81.0, 268, 236, 'sqrt2 (√2)',
            '<strong>Why sqrt2 diagnoses this failure:</strong> D=268 reflects non-revenue water '
            '(NRW) losses at 25-45% in many Danube basin utilities (vs EU best practice 10-15%), '
            'ageing pipe network (average >30 years in Romanian and Bulgarian utilities), and '
            'unmetered connections suppressing revenue C-flags. C=236 reflects functional '
            'but imperfect distribution: water reaches households but with significant losses. '
            'sqrt2 identifies structural overhead: the physical pipe deterioration raises D '
            '(maintenance burden, burst frequency) without adding C.',
            [
                ('Smart metering rollout with AMI (advanced metering infrastructure)',
                 'Deploy AMI smart meters at zone meter and consumer level. Each meter installed '
                 'adds a measurement C-flag and enables leak detection. EU Smart Water Networks '
                 'Directive (proposed) provides regulatory driver. '
                 'Estimated C increase: +10 to +15.',
                 '81.0% to 86-89%'),
                ('Pressure management and district metering zone (DMZ) creation',
                 'Establish DMZs with pressure control valves. Each DMZ with active pressure '
                 'management removes a burst-frequency D-flag. NRW reduction target: 25% to 15%. '
                 'Estimated D reduction: -8 to -12.',
                 '81.0% to 86-88%'),
            ],
            'Combined effect: Phase 3 from 81% to 86-89%, above chain pi (88.6% with both).'
        ),
    ]
))

# ── HUMAN: IRRIGATION INFRASTRUCTURE ─────────────────────────────────────────
# ph2 (77%), ph1 (79%), ph4 (79%) below chain pi (82%)
inject(BASE + '/human_irrigation_infrastructure/supply_chain/project_context.html', worksheet(
    'Danube Irrigation Infrastructure Supply Chain', 82.0,
    pi=82.0, phi=80, sq2=76, ln2=79, e=74,
    axis_note=(
        'Phases 2 (77%), 1 (79%), and 4 (79%) are all below chain pi (82%). '
        'sqrt2 (76) identifies structural overhead in the secondary distribution network '
        '(Phase 2): Soviet-era open-channel systems with high evaporation and seepage losses. '
        'ln2 (79) notes transformation gaps at field application (Phase 3) and drainage. '
        'e (74) reflects that CAP irrigation support instruments are not linked to '
        'measured water-use efficiency KPIs.'
    ),
    blocks=[
        bottleneck_block(2, 'Secondary Distribution Network', 77.0, 240, 244, 'sqrt2 (√2)',
            '<strong>Why sqrt2 diagnoses this failure:</strong> C=244 > D=240 (C-dominant, '
            'near-balanced) yet balance is 77%. The structural issue is that the secondary '
            'distribution network has high throughput capacity but high loss rates: open concrete '
            'channels in Romania and Bulgaria lose 30-50% of water to seepage and evaporation '
            'before reaching field level. sqrt2 identifies this as structural overhead: the '
            'physical infrastructure is carrying D-flags (maintenance burden, sedimentation, '
            'leakage) that raise the constraint load independently of water availability.',
            [
                ('Pipeline conversion of highest-loss channels',
                 'Convert the 20% of channels with the highest measured seepage losses to '
                 'underground pressure piping. EU CAP Rural Development Programme funding '
                 'available (Article 46 irrigation). Each converted kilometre removes a '
                 'seepage D-flag. Estimated D reduction: -8 to -12.',
                 '77.0% to 82-85%'),
                ('Channel lining with HDPE geomembrane',
                 'For channels not suitable for conversion, line with HDPE membrane. '
                 'Reduces seepage by 70-80%. Each lined section adds a water-retention C-flag. '
                 'Estimated C increase: +5 to +8.',
                 '77.0% to 80-83%'),
            ],
            'Combined effect: Phase 2 from 77% to 82-85%, at or above chain pi (82%).'
        ),
    ]
))

# ── HUMAN: REED INDUSTRY ─────────────────────────────────────────────────────
# ph3 (72%), ph2 (77%), ph1 (81%), ph4 (77%), ph0 (84%)
inject(BASE + '/human_reed_industry/supply_chain/project_context.html', worksheet(
    'Danube Reed Industry Supply Chain', 78.2,
    pi=78.2, phi=75, sq2=72, ln2=70, e=67,
    axis_note=(
        'Phase 3 Market Access and Certification (72.0%) is the primary bottleneck. '
        'Phases 2 and 4 (77%) are also below chain pi (78.2%). '
        'ln2 (70) identifies the market transformation failure: Danube reed leaves the delta '
        'as a raw commodity without certification or differentiation. '
        'sqrt2 (72) identifies structural overhead in harvesting and processing. '
        'e (67) reflects that no sustainability-linked instrument ties Phragmites harvest '
        'volume to biodiversity conservation KPIs.'
    ),
    blocks=[
        bottleneck_block(3, 'Market Access and Certification', 72.0, 264, 232, 'ln2 and phi (φ)',
            '<strong>Why ln2 and phi diagnose this failure:</strong> D=264 reflects certification '
            'requirements (EU Ecolabel, ISO 14001 for thatching exporters) that are non-trivial '
            'for small delta operators to obtain. C=232 is suppressed because Danube reed is '
            'exported primarily as undifferentiated raw thatching material: no premium is '
            'captured for certified sustainable harvest. ln2 identifies the transformation failure: '
            'the raw reed input could command 20-30% premium as certified sustainable thatching '
            'in UK and Netherlands markets, but the certification conversion pathway is not '
            'available to most delta operators. phi identifies value distribution: large Dutch and '
            'Belgian thatching importers capture the premium without paying it upstream.',
            [
                ('Collective certification scheme for delta cooperatives',
                 'Pool certification costs across Danube Delta reed cooperatives under a '
                 'group FSC or EU Ecolabel certification. Each cooperative in the group scheme '
                 'adds a C-flag. Cost: EUR 5,000/cooperative (vs EUR 25,000 individually). '
                 'Estimated C increase: +15 to +20.',
                 '72.0% to 78-82%'),
                ('Direct EU thatching market development',
                 'Establish a Romanian/Ukrainian reed cooperative marketing office for '
                 'UK/Netherlands thatching market. Each direct buyer contract removes '
                 'an intermediary D-flag and adds a premium C-flag. '
                 'Estimated C increase: +10 to +15.',
                 '72.0% to 78-82%'),
            ],
            'Combined effect: Phase 3 from 72% to 78-82%, at or above chain pi.'
        ),
    ]
))

# ── NATURAL: DELTA BIODIVERSITY ──────────────────────────────────────────────
# ph0 (78%), ph4 (80%), ph3 (82%), others higher
inject(BASE + '/natural_delta_biodiversity/supply_chain/project_context.html', worksheet(
    'Danube Delta Biodiversity Supply Chain', 82.6,
    pi=82.6, phi=81, sq2=77, ln2=83, e=72,
    axis_note=(
        'Phase 0 Basin Sediment and Nutrient Supply (78.0%) is the primary bottleneck. '
        'Phase 4 Biodiversity Service Delivery (80.0%) is marginally below chain pi (82.6%). '
        'sqrt2 (77) identifies structural overhead: Iron Gates Dam (1972) permanently reduced '
        'sediment input by ~70%, raising a structural D-flag that cannot be removed without '
        'dam bypass or sediment augmentation. e (72) reflects that EU biodiversity bonds '
        'and ecosystem service payments are not yet linked to delta sediment-budget KPIs.'
    ),
    blocks=[
        bottleneck_block(0, 'Basin Sediment and Nutrient Supply', 78.0, 276, 264, 'sqrt2 (√2)',
            '<strong>Why sqrt2 diagnoses this failure:</strong> D=276 reflects the permanent '
            'D-flag introduced by the Iron Gates Dam system (Portile de Fier I and II): '
            '~70% of the Danube\'s former sediment load is now trapped behind the dams. '
            'C=264 reflects the residual contribution of nutrient-rich water that still '
            'reaches the delta (Danube carries ~63 mg/L total dissolved solids average). '
            'sqrt2 identifies structural overhead: the dam is a physical constraint that '
            'raises D (nutrient and sediment deficit that the delta ecosystem must compensate '
            'for) without adding C. The intervention pathway is sediment bypass or augmentation, '
            'not operational management.',
            [
                ('Sediment bypass feasibility study for Iron Gates I',
                 'Commission an ICPDR-led feasibility study for sluicing or bypass channels '
                 'at Iron Gates I during peak flow events. Each tonne of sediment successfully '
                 'bypassed adds a nutrient-input C-flag downstream. '
                 'EU LIFE+ and Danube River Protection Convention funding available. '
                 'Estimated C increase per bypass event: +3 to +5.',
                 '78.0% to 80-82% (partial bypass)'),
                ('Nutrient tributary restoration (Prut, Siret tributaries)',
                 'Restore natural floodplain retention in the Prut and Siret tributaries, '
                 'the main nutrient contributors to the lower Danube. Each restored '
                 'floodplain section adds a nutrient-delivery C-flag. '
                 'EU WFD Article 4.3 restoration planning framework. '
                 'Estimated C increase: +5 to +8.',
                 '78.0% to 82-84%'),
            ],
            'Combined effect: Phase 0 from 78% to 82-84%, at or above chain pi.'
        ),
    ]
))

# ── NATURAL: FISH POPULATION ─────────────────────────────────────────────────
# ph1 (71%), ph4 (77%), ph2 (79%), ph3 (80%), ph0 (83%)
inject(BASE + '/natural_fish_population/supply_chain/project_context.html', worksheet(
    'Danube Natural Fish Population Supply Chain', 78.0,
    pi=78.0, phi=75, sq2=71, ln2=73, e=66,
    axis_note=(
        'Phase 1 Habitat and Migration Corridor (71.0%) is the primary bottleneck, '
        'near the Failure zone boundary. Phase 4 Harvest-Ready Population Stock (77%) is secondary. '
        'sqrt2 (71) identifies structural overhead: the Iron Gates Dam created a permanent '
        'migration barrier for anadromous species (beluga sturgeon, Allis shad). '
        'ln2 (73) identifies the recruitment-to-adult transformation failure. '
        'e (66) reflects the absence of any performance-linked conservation finance for '
        'Danube fish populations.'
    ),
    blocks=[
        bottleneck_block(1, 'Habitat and Migration Corridor', 71.0, 264, 220, 'sqrt2 (√2)',
            '<strong>Why sqrt2 diagnoses this failure:</strong> D=264 reflects the structural '
            'barrier imposed by the Iron Gates dam complex: the historic sturgeon migration '
            'route from the Black Sea to spawning grounds in Slovakia and Hungary has been '
            'physically severed since 1972. Additionally, the Gabcikovo-Nagymaros dam on the '
            'upper Danube created a second migration barrier. C=220 is the lowest C in the '
            'chain: the habitat and corridor phase generates the least contribution because '
            'the physical infrastructure for fish passage is absent. sqrt2 identifies this as '
            'a structural constraint: no operational intervention can restore natural migration '
            'without physical infrastructure (fish passage or dam bypass).',
            [
                ('Fish passage at Iron Gates II dam',
                 'Construct a bypass channel or fish lift at Iron Gates II (1.5km required). '
                 'EU LIFE IP Danube, WWF Iron Gates Nature Park funding. Each cm of functional '
                 'passage depth adds a migration-corridor C-flag for target species. '
                 'Cost estimate: EUR 25-40M. Estimated C increase: +20 to +30 over 10 years.',
                 '71.0% to 80-85% (fish passage operational)'),
                ('Sturgeon artificial propagation and stocking (interim)',
                 'Expand ICES-coordinated artificial propagation programme for beluga, '
                 'stellate, and Russian sturgeon. Each released juvenile adds a recruitment '
                 'C-flag for the downstream population stock. '
                 'LIFE+ Danube Sturgeon programme already active.',
                 '71.0% to 75-78% (stocking alone)'),
                ('Upper Danube floodplain habitat restoration',
                 'Reconnect 5,000 ha of floodplain habitat along the Slovak/Hungarian reach '
                 'as spawning and juvenile refuge. Each reconnected floodplain section '
                 'adds a habitat C-flag. EU Biodiversity Strategy 2030 Target 2 funding.',
                 '71.0% to 74-77%'),
            ],
            'Combined effect: Phase 1 from 71% to 80-85% over a 10-year horizon. '
            'Fish passage is the structural prerequisite; stocking and habitat restoration '
            'add incremental C in the interim.'
        ),
    ]
))

# ── NATURAL: FLOODPLAIN FOREST BIOMASS ───────────────────────────────────────
# ph4 (74%), ph0 (79%), ph3 (82%), ph1 (84%), ph2 (86%)
inject(BASE + '/natural_floodplain_forest_biomass/supply_chain/project_context.html', worksheet(
    'Danube Floodplain Forest Biomass Supply Chain', 81.0,
    pi=81.0, phi=79, sq2=75, ln2=78, e=70,
    axis_note=(
        'Phase 4 Ecosystem Service Delivery (74.0%) is the primary bottleneck. '
        'Phase 0 Hydrological Connectivity (79.0%) is secondary. '
        'sqrt2 (75) identifies structural overhead from flood pulse disruption (Iron Gates '
        'regulation alters the natural flood pulse that drives forest establishment). '
        'e (70) reflects that ecosystem service payments for floodplain carbon and biodiversity '
        'are not yet operational in the Danube corridor.'
    ),
    blocks=[
        bottleneck_block(4, 'Ecosystem Service Delivery', 74.0, 264, 232, 'phi (φ) and e',
            '<strong>Why phi and e diagnose this failure:</strong> D=264 reflects the '
            'ecological overhead of delivering ecosystem services (flood attenuation, carbon '
            'sequestration, water quality) without financial recognition. C=232 is suppressed '
            'because the forest provides services that are consumed by downstream beneficiaries '
            'but not compensated. phi identifies value distribution failure: no mechanism '
            'exists for downstream utilities or cities to pay for the flood attenuation service '
            'that the floodplain forest provides. e identifies absence of financial instruments '
            'linking forest management returns to measured service delivery.',
            [
                ('Flood attenuation PES contract with downstream utilities',
                 'Structure payment-for-ecosystem-services contracts between floodplain forest '
                 'managers and downstream water utilities (Bratislava, Vienna, Budapest water '
                 'authorities). Each contract adds a phi-rebalancing C-flag. '
                 'OECD PES design framework applicable. Estimated C increase: +10 to +15.',
                 '74.0% to 79-82%'),
                ('Voluntary carbon credit certification (wetland forest REDD+)',
                 'Enroll floodplain forest management in Verra VCS Wetland Restoration methodology. '
                 'Each verified tonne of CO2e adds a carbon C-flag and activates the e axis. '
                 'Estimated e axis C increase: +8 to +12.',
                 '74.0% to 78-81%'),
            ],
            'Combined effect: Phase 4 from 74% to 79-82%, approaching chain pi (81%).'
        ),
    ]
))

# ── NATURAL: FRESHWATER AVAILABILITY ─────────────────────────────────────────
# ph3 (83%) only phase below chain pi (88.2%)
inject(BASE + '/natural_freshwater_availability/supply_chain/project_context.html', worksheet(
    'Danube Natural Freshwater Availability', 88.2,
    pi=88.2, phi=87, sq2=84, ln2=86, e=82,
    axis_note=(
        'This chain is highly Coherent. Only Phase 3 Groundwater Recharge (83.0%) is below '
        'chain pi (88.2%). phi (87) reflects good balance across the precipitation-to-delivery '
        'system. sqrt2 (84) notes some structural overhead from groundwater over-extraction '
        'in agricultural zones. e (82) reflects that EU Water Framework Directive instruments '
        'are in place but groundwater recharge performance is not explicitly funded.'
    ),
    blocks=[
        bottleneck_block(3, 'Groundwater Recharge', 83.0, 244, 236, 'sqrt2 (√2)',
            '<strong>Why sqrt2 diagnoses this failure:</strong> D=244 reflects structural '
            'overhead from agricultural groundwater over-extraction in the Danube basin '
            '(Hungary, Romania: irrigation withdrawals 30-60% above sustainable yield in '
            'drought years). C=236 is slightly suppressed: natural recharge is functioning '
            'but cannot keep pace with extraction. sqrt2 identifies the structural constraint: '
            'the physical recharge capacity of alluvial aquifers is fixed by geological '
            'permeability; the constraint is on the extraction side, not the recharge side.',
            [
                ('Irrigation scheduling optimisation (deficit irrigation)',
                 'Introduce soil-moisture-sensor-based irrigation scheduling to replace '
                 'calendar-based irrigation in the basin. Each farm adopting deficit irrigation '
                 'reduces groundwater extraction D-flag by approximately 20-30%. '
                 'Estimated D reduction: -5 to -8.',
                 '83.0% to 86-88%'),
                ('Managed aquifer recharge (winter surplus infiltration)',
                 'Use winter Danube peak-flow periods to actively recharge aquifers via '
                 'infiltration basins. Each operational infiltration basin adds a recharge C-flag. '
                 'EU WFD Annex III groundwater quantitative status framework applies.',
                 '83.0% to 87-89%'),
            ],
            'Combined effect: Phase 3 from 83% to 87-89%, at chain pi. '
            'Chain reaches full Coherent status.'
        ),
    ]
))

# ── NATURAL: REED BED ────────────────────────────────────────────────────────
# ph4 (74%), ph0 (81%), ph3 (83%), ph1 (84%), ph2 (85%)
inject(BASE + '/natural_reed_bed/supply_chain/project_context.html', worksheet(
    'Danube Natural Reed Bed Supply Chain', 81.4,
    pi=81.4, phi=80, sq2=77, ln2=79, e=71,
    axis_note=(
        'Phase 4 Ecosystem Service Delivery (74.0%) is the primary bottleneck. '
        'Phase 0 Hydrological Regime (81.0%) is marginally below chain pi (81.4%). '
        'phi (80) reflects reasonably good distribution. '
        'e (71) identifies the absence of financial instruments linking reed bed management '
        'returns to measured water quality and biodiversity services.'
    ),
    blocks=[
        bottleneck_block(4, 'Ecosystem Service Delivery', 74.0, 264, 228, 'phi (φ) and e',
            '<strong>Why phi and e diagnose this failure:</strong> D=264 reflects the '
            'management overhead of maintaining reed beds for ecosystem service delivery: '
            'rotational harvesting to maintain habitat heterogeneity, water level management, '
            'and invasive species (Phragmites australis monoculture preventing ecological '
            'succession). C=228 reflects that reed beds deliver water filtration, carbon '
            'storage, and wildlife habitat services without being financially compensated. '
            'phi identifies value distribution failure: downstream beneficiaries '
            '(fisheries, tourism, water utilities) benefit from reed bed ecosystem services '
            'without contributing to maintenance costs. e identifies the absence of any '
            'PES or ecosystem credit instrument.',
            [
                ('Water quality PES contract with water utilities',
                 'Structure payment contracts between reed bed managers and downstream utilities '
                 'benefiting from natural water filtration. Each contract adds a phi-rebalancing '
                 'C-flag. The Danube Delta Biosphere Reserve Authority can provide contracting '
                 'framework. Estimated C increase: +10 to +15.',
                 '74.0% to 79-82%'),
                ('Ramsar Wetland Conservation Fund enrollment',
                 'Apply for Ramsar Small Grants Fund and EU LIFE Wetlands programme for '
                 'reed bed biodiversity management. Each funded management action adds an '
                 'e-axis C-flag. Estimated C increase: +8 to +12.',
                 '74.0% to 78-81%'),
            ],
            'Combined effect: Phase 4 from 74% to 79-82%, approaching chain pi.'
        ),
    ]
))

# ── NATURAL: RIVER CHANNEL ───────────────────────────────────────────────────
# ph2 (72%), ph3 (72%), ph4 (82%), ph0 (85%), ph1 (85%)
inject(BASE + '/natural_river_channel/supply_chain/project_context.html', worksheet(
    'Danube Natural River Channel Supply Chain', 79.2,
    pi=79.2, phi=77, sq2=68, ln2=75, e='n/a',
    axis_note=(
        'Phases 2 (72.0%) and 3 (72.0%) are co-primary bottlenecks: Channel Morphology and '
        'Sediment Transport. Both are in the Stressed zone below chain pi (79.2%). '
        'sqrt2 (68) identifies structural overhead: the Danube river channel has been '
        'heavily regulated (bank reinforcement, gravel extraction, dam impoundment) over '
        '150 years, altering the natural morphological processes. '
        'ln2 (75) identifies transformation failures in the geomorphic work (Phase 3) and '
        'channel substrate (Phase 2): regulated rivers cannot perform natural geomorphic '
        'transformation at the same rate as unregulated channels.'
    ),
    blocks=[
        bottleneck_block(2, 'Channel Morphology and Substrate Function', 72.0, 264, 232, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=264 reflects the '
            'cumulative D-flags from over a century of river engineering: bank reinforcement '
            'with riprap armour, removal of gravel bars, isolation of floodplains by levees, '
            'and gravel extraction (Danube gravel extraction: 40M m3/year peak in 1970s). '
            'C=232 reflects the reduced capacity of the regulated channel to perform its '
            'natural morphological functions: habitat creation, sediment sorting, gravel bed '
            'maintenance, and hyporheic exchange. sqrt2 identifies structural overhead: each '
            'bank reinforcement adds a D-flag that constrains lateral channel movement. '
            'ln2 identifies transformation failure: the river cannot convert its flow energy '
            'into morphological work at natural rates.',
            [
                ('Gravel augmentation at sediment-starved reaches',
                 'Introduce gravel at selected reaches downstream of dams (Iron Gates, '
                 'Gabcikovo) to compensate for trapped sediment. Each augmented section '
                 'removes a sediment-deficit D-flag and adds a substrate-function C-flag. '
                 'Rhine gravel augmentation programme provides precedent. '
                 'Estimated C increase: +8 to +12 per augmented reach.',
                 '72.0% to 77-80%'),
                ('Bank protection setback and meander restoration',
                 'Remove or set back bank protection at 10 selected reaches to allow natural '
                 'lateral migration. Each setback section adds a geomorphic-work C-flag and '
                 'reduces the engineering-overhead D-flag. EU WFD Article 4.3 funding available.',
                 '72.0% to 76-79%'),
            ],
            'Combined effect: Phase 2 from 72% to 77-80%, approaching chain pi (79.2%). '
            'Phase 3 (Sediment Transport, 72%) requires the same gravel augmentation intervention.'
        ),
        bottleneck_block(3, 'Sediment Transport and Geomorphic Work', 72.0, 260, 232, 'sqrt2 (√2) and ln2',
            '<strong>Why sqrt2 and ln2 diagnose this failure:</strong> D=260 reflects the '
            'same structural constraints as Phase 2 but manifesting in the longitudinal '
            'transport dimension: the Danube\'s bedload transport has been reduced by >90% '
            'in the lower reach below Iron Gates (ICPDR monitoring data). C=232 reflects '
            'the reduced geomorphic work output: delta formation is slowing, channel '
            'incision is accelerating, and gravel bed habitat is degrading. ln2 identifies '
            'the transformation failure: the river\'s flow energy cannot be converted into '
            'geomorphic outputs at natural rates when bedload is absent.',
            [
                ('Gravel augmentation programme continuity',
                 'Same intervention as Phase 2: gravel augmentation upstream of the delta '
                 'reach. Each augmented reach adds a bedload-transport C-flag for Phase 3. '
                 'Requires coordination with Romanian and Bulgarian authorities. '
                 'Estimated C increase: +8 to +12.',
                 '72.0% to 77-80%'),
                ('Delta front monitoring and managed retreat pilot',
                 'Commission LIDAR delta survey every 2 years to quantify delta erosion rate. '
                 'Each verified survey event adds a monitoring C-flag. Provides evidence base '
                 'for intervention funding. Estimated balance improvement: +3 to +5.',
                 '72.0% to 75-77%'),
            ],
            'Combined effect: Phase 3 from 72% to 77-80%. Both Phase 2 and Phase 3 '
            'benefit from the same gravel augmentation intervention.'
        ),
    ]
))

print('Danube worksheets complete.')
