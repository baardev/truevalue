#!/usr/bin/env python3
"""
generate_danube_data.py
=======================
Generates processed JSON data files for Danube Basin subprojects.

For each subproject, reads:
  - project.yaml (type, paired_with, data_availability, ndc_derivation)
  - data/schema/<slug>_supply_chain_phases.csv

Outputs:
  - data/processed/<slug>_supply_chain_ui.json
  - data/processed/<slug>_system_lifecycle_ndc.json
  - supply_chain/scenarios.json

Usage:
  python scripts/generate_danube_data.py --all
  python scripts/generate_danube_data.py --subproject natural_freshwater_availability
  python scripts/generate_danube_data.py --subproject human_freshwater_supply_infrastructure

D/C/N derivation follows the PDI-to-HTML pipeline rule:
  D = 200 + (D_flags x 20) + (boundary_score x 4)
  C = 200 + (C_flags x 20) + (opacity x 8)
  balance = high->90±4, medium->83±4, low->70±4
  N = round((D + C) / 2 * (balance / 100))

Natural services get an additional ecological_stock_ratio field.
"""

import argparse
import csv
import json
import os
import random
import yaml
from datetime import datetime
from pathlib import Path

DANUBE_DIR = Path(__file__).parent.parent / "frontend" / "project" / "danube"

# NDC derivation hardcoded per subproject (from PDI YAMLs).
# Structure: phase_id -> {D, C, balance, N, sustainability}
NDC_DATA = {
    "natural_freshwater_availability": {
        "phases": {
            "0": {"D": 252, "C": 228, "balance": 91.0, "N": 218, "sustainability": 0.95,
                  "name": "Atmospheric Moisture", "transparency": "High"},
            "1": {"D": 280, "C": 248, "balance": 89.0, "N": 235, "sustainability": 0.94,
                  "name": "Precipitation over Basin", "transparency": "High"},
            "2": {"D": 276, "C": 248, "balance": 92.0, "N": 241, "sustainability": 0.95,
                  "name": "Catchment Runoff and River Flow", "transparency": "High"},
            "3": {"D": 244, "C": 236, "balance": 83.0, "N": 199, "sustainability": 0.98,
                  "name": "Groundwater Recharge", "transparency": "Medium"},
            "4": {"D": 280, "C": 268, "balance": 86.0, "N": 236, "sustainability": 0.98,
                  "name": "Available Flow to Beneficiaries", "transparency": "High"},
        },
        "coherence": {"pi": 88.0, "phi": 72.0, "sqrt2": 85.0, "ln2": 78.0, "e": 0.0},
        "type": "natural",
        "color_primary": "#2e7d32",
        "color_dark": "#1b5e20",
        "ecological_stock_ratio": 0.17,  # abstraction / renewable = 35 km3 / 206 km3
        "paired_with": "human_freshwater_supply_infrastructure",
    },
    "human_irrigation_infrastructure": {
        "phases": {
            "0": {"D": 276, "C": 248, "balance": 91.0, "N": 238, "sustainability": 0.95,
                  "name": "River and Canal Intake", "transparency": "High"},
            "1": {"D": 264, "C": 244, "balance": 79.0, "N": 201, "sustainability": 0.96,
                  "name": "Primary Canal Conveyance", "transparency": "Medium"},
            "2": {"D": 240, "C": 244, "balance": 77.0, "N": 186, "sustainability": 0.98,
                  "name": "Secondary Distribution Network", "transparency": "Low"},
            "3": {"D": 268, "C": 256, "balance": 84.0, "N": 220, "sustainability": 0.96,
                  "name": "Field Application", "transparency": "Medium"},
            "4": {"D": 244, "C": 244, "balance": 79.0, "N": 193, "sustainability": 1.00,
                  "name": "Drainage and Return Flow", "transparency": "Medium"},
        },
        "coherence": {"pi": 82.0, "phi": 55.0, "sqrt2": 62.0, "ln2": 68.0, "e": 15.0},
        "type": "human",
        "color_primary": "#388e3c",
        "color_dark": "#1b5e20",
        "ecological_stock_ratio": None,
        "paired_with": "paired_agricultural_water",
    },
    "human_freshwater_supply_infrastructure": {
        "phases": {
            "0": {"D": 276, "C": 248, "balance": 91.0, "N": 238, "sustainability": 0.95,
                  "name": "River and Groundwater Intake", "transparency": "High"},
            "1": {"D": 252, "C": 228, "balance": 88.0, "N": 211, "sustainability": 0.95,
                  "name": "Raw Water Conveyance", "transparency": "High"},
            "2": {"D": 300, "C": 248, "balance": 93.0, "N": 255, "sustainability": 0.91,
                  "name": "Water Treatment", "transparency": "High"},
            "3": {"D": 268, "C": 236, "balance": 81.0, "N": 204, "sustainability": 0.94,
                  "name": "Pressurized Distribution Network", "transparency": "Medium"},
            "4": {"D": 256, "C": 248, "balance": 90.0, "N": 227, "sustainability": 0.98,
                  "name": "Consumer Delivery and Metering", "transparency": "High"},
        },
        "coherence": {"pi": 88.6, "phi": 61.0, "sqrt2": 68.0, "ln2": 74.0, "e": 42.0},
        "type": "human",
        "color_primary": "#1565c0",
        "color_dark": "#0d47a1",
        "ecological_stock_ratio": None,
        "paired_with": "natural_freshwater_availability",
    },
    "natural_delta_biodiversity": {
        "phases": {
            "0": {"D": 276, "C": 264, "balance": 78.0, "N": 211, "sustainability": 0.96,
                  "name": "Basin Sediment and Nutrient Supply", "transparency": "Medium"},
            "1": {"D": 292, "C": 268, "balance": 85.0, "N": 238, "sustainability": 0.94,
                  "name": "Hydrological Pulse and Connectivity", "transparency": "High"},
            "2": {"D": 288, "C": 288, "balance": 88.0, "N": 253, "sustainability": 0.96,
                  "name": "Habitat Formation and Heterogeneity", "transparency": "High"},
            "3": {"D": 272, "C": 276, "balance": 82.0, "N": 225, "sustainability": 0.97,
                  "name": "Species Population Dynamics", "transparency": "Medium"},
            "4": {"D": 256, "C": 264, "balance": 80.0, "N": 208, "sustainability": 0.97,
                  "name": "Biodiversity Service Delivery", "transparency": "Medium"},
        },
        "coherence": {"pi": 83.0, "phi": 45.0, "sqrt2": 62.0, "ln2": 52.0, "e": 20.0},
        "type": "natural",
        "color_primary": "#2e7d32",
        "color_dark": "#1b5e20",
        "ecological_stock_ratio": None,
        "paired_with": "paired_ecotourism",
    },
    "human_cultural_heritage_management": {
        "phases": {
            "0": {"D": 264, "C": 256, "balance": 82.0, "N": 213, "sustainability": 0.95,
                  "name": "Heritage Inventory and Documentation", "transparency": "Medium"},
            "1": {"D": 272, "C": 240, "balance": 76.0, "N": 194, "sustainability": 0.93,
                  "name": "Site Preservation and Conservation", "transparency": "Medium"},
            "2": {"D": 276, "C": 272, "balance": 86.0, "N": 235, "sustainability": 0.97,
                  "name": "Visitor Access Infrastructure", "transparency": "High"},
            "3": {"D": 268, "C": 256, "balance": 81.0, "N": 213, "sustainability": 0.95,
                  "name": "Cultural Programming and Guided Services", "transparency": "Medium"},
            "4": {"D": 268, "C": 252, "balance": 78.0, "N": 203, "sustainability": 0.95,
                  "name": "Tourism Revenue and Sustainable Management", "transparency": "Medium"},
        },
        "coherence": {"pi": 81.0, "phi": 52.0, "sqrt2": 66.0, "ln2": 65.0, "e": 35.0},
        "type": "human",
        "color_primary": "#bf6900",
        "color_dark": "#7c4200",
        "ecological_stock_ratio": None,
        "paired_with": "paired_ecotourism",
    },
    "natural_floodplain_forest_biomass": {
        "phases": {
            "0": {"D": 268, "C": 248, "balance": 79.0, "N": 204, "sustainability": 0.94,
                  "name": "Hydrological Connectivity and Flood Pulse", "transparency": "High"},
            "1": {"D": 272, "C": 264, "balance": 84.0, "N": 225, "sustainability": 0.96,
                  "name": "Soil Formation and Nutrient Cycling", "transparency": "Medium"},
            "2": {"D": 276, "C": 272, "balance": 86.0, "N": 235, "sustainability": 0.97,
                  "name": "Tree Establishment and Canopy Formation", "transparency": "High"},
            "3": {"D": 268, "C": 256, "balance": 82.0, "N": 215, "sustainability": 0.95,
                  "name": "Biomass Accumulation and Carbon Sequestration", "transparency": "Medium"},
            "4": {"D": 264, "C": 232, "balance": 74.0, "N": 183, "sustainability": 0.93,
                  "name": "Ecosystem Service Delivery", "transparency": "Medium"},
        },
        "coherence": {"pi": 81.0, "phi": 55.0, "sqrt2": 69.0, "ln2": 58.0, "e": 22.0},
        "type": "natural",
        "color_primary": "#2e7d32",
        "color_dark": "#1b5e20",
        "ecological_stock_ratio": 0.47,  # area loss as structural stress indicator: 47% of original area gone
        "paired_with": "paired_floodplain_forestry",
    },
    "human_floodplain_forestry_operations": {
        "phases": {
            "0": {"D": 264, "C": 252, "balance": 79.0, "N": 203, "sustainability": 0.95,
                  "name": "Forest Inventory and Management Planning", "transparency": "Medium"},
            "1": {"D": 268, "C": 256, "balance": 82.0, "N": 215, "sustainability": 0.95,
                  "name": "Timber Harvesting and Extraction", "transparency": "Medium"},
            "2": {"D": 264, "C": 248, "balance": 77.0, "N": 197, "sustainability": 0.94,
                  "name": "Timber Processing and Value Addition", "transparency": "Medium"},
            "3": {"D": 268, "C": 240, "balance": 73.0, "N": 187, "sustainability": 0.92,
                  "name": "Market Access and Certification", "transparency": "Medium"},
            "4": {"D": 260, "C": 240, "balance": 70.0, "N": 175, "sustainability": 0.93,
                  "name": "Revenue Capture and Ecosystem Service Payments", "transparency": "Medium"},
        },
        "coherence": {"pi": 76.0, "phi": 48.0, "sqrt2": 62.0, "ln2": 61.0, "e": 28.0},
        "type": "human",
        "color_primary": "#33691e",
        "color_dark": "#1b5e20",
        "ecological_stock_ratio": None,
        "paired_with": "paired_floodplain_forestry",
    },
    "natural_fish_population": {
        "phases": {
            "0": {"D": 268, "C": 264, "balance": 83.0, "N": 218, "sustainability": 0.96,
                  "name": "Water Quality and Habitat Suitability", "transparency": "High"},
            "1": {"D": 264, "C": 220, "balance": 71.0, "N": 180, "sustainability": 0.91,
                  "name": "Habitat and Migration Corridor", "transparency": "Medium"},
            "2": {"D": 264, "C": 244, "balance": 79.0, "N": 203, "sustainability": 0.94,
                  "name": "Recruitment and Juvenile Development", "transparency": "Medium"},
            "3": {"D": 264, "C": 248, "balance": 80.0, "N": 207, "sustainability": 0.95,
                  "name": "Adult Biomass and Population Dynamics", "transparency": "Medium"},
            "4": {"D": 260, "C": 244, "balance": 77.0, "N": 197, "sustainability": 0.94,
                  "name": "Harvest-Ready Population Stock", "transparency": "Medium"},
        },
        "coherence": {"pi": 78.0, "phi": 45.0, "sqrt2": 63.0, "ln2": 52.0, "e": 18.0},
        "type": "natural",
        "color_primary": "#0277bd",
        "color_dark": "#01579b",
        "ecological_stock_ratio": 0.84,  # migration range blocked: 84% of historical range inaccessible
        "paired_with": "paired_fisheries",
    },
    "human_commercial_fishing": {
        "phases": {
            "0": {"D": 264, "C": 244, "balance": 78.0, "N": 200, "sustainability": 0.94,
                  "name": "Licencing, Quota Setting, and Effort Planning", "transparency": "Medium"},
            "1": {"D": 264, "C": 248, "balance": 80.0, "N": 207, "sustainability": 0.95,
                  "name": "Fishing Operations and Active Harvest", "transparency": "Medium"},
            "2": {"D": 260, "C": 232, "balance": 72.0, "N": 183, "sustainability": 0.92,
                  "name": "Processing, Cold Chain, and Preservation", "transparency": "Medium"},
            "3": {"D": 264, "C": 244, "balance": 77.0, "N": 197, "sustainability": 0.94,
                  "name": "Market Access and Distribution", "transparency": "Medium"},
            "4": {"D": 260, "C": 236, "balance": 74.0, "N": 190, "sustainability": 0.93,
                  "name": "Revenue Capture and Sector Reinvestment", "transparency": "Medium"},
        },
        "coherence": {"pi": 76.0, "phi": 44.0, "sqrt2": 60.0, "ln2": 58.0, "e": 24.0},
        "type": "human",
        "color_primary": "#0288d1",
        "color_dark": "#01579b",
        "ecological_stock_ratio": None,
        "paired_with": "paired_fisheries",
    },
    "natural_reed_bed": {
        "phases": {
            "0": {"D": 264, "C": 252, "balance": 81.0, "N": 211, "sustainability": 0.95,
                  "name": "Hydrological Regime and Nutrient Supply", "transparency": "High"},
            "1": {"D": 268, "C": 264, "balance": 84.0, "N": 225, "sustainability": 0.96,
                  "name": "Reed Establishment and Colonisation", "transparency": "Medium"},
            "2": {"D": 272, "C": 264, "balance": 85.0, "N": 229, "sustainability": 0.97,
                  "name": "Biomass Accumulation and Stand Maturation", "transparency": "Medium"},
            "3": {"D": 268, "C": 260, "balance": 83.0, "N": 220, "sustainability": 0.96,
                  "name": "Standing Stock and Harvest-Ready Biomass", "transparency": "Medium"},
            "4": {"D": 264, "C": 228, "balance": 74.0, "N": 186, "sustainability": 0.93,
                  "name": "Ecosystem Service Delivery", "transparency": "Medium"},
        },
        "coherence": {"pi": 81.0, "phi": 58.0, "sqrt2": 72.0, "ln2": 66.0, "e": 20.0},
        "type": "natural",
        "color_primary": "#558b2f",
        "color_dark": "#33691e",
        "ecological_stock_ratio": 0.16,  # only 16% of sustainable quota actually harvested: market/logistics constraint
        "paired_with": "paired_reed_harvesting",
    },
    "human_reed_industry": {
        "phases": {
            "0": {"D": 268, "C": 260, "balance": 84.0, "N": 225, "sustainability": 0.96,
                  "name": "Harvest Permitting and Zone Planning", "transparency": "High"},
            "1": {"D": 268, "C": 256, "balance": 81.0, "N": 213, "sustainability": 0.95,
                  "name": "Reed Harvesting Operations", "transparency": "Medium"},
            "2": {"D": 264, "C": 244, "balance": 77.0, "N": 197, "sustainability": 0.94,
                  "name": "Processing, Grading, and Bundling", "transparency": "Medium"},
            "3": {"D": 264, "C": 232, "balance": 72.0, "N": 183, "sustainability": 0.92,
                  "name": "Market Access and Certification", "transparency": "Medium"},
            "4": {"D": 260, "C": 244, "balance": 77.0, "N": 197, "sustainability": 0.94,
                  "name": "Revenue Capture and Sector Reinvestment", "transparency": "Medium"},
        },
        "coherence": {"pi": 78.0, "phi": 46.0, "sqrt2": 62.0, "ln2": 60.0, "e": 22.0},
        "type": "human",
        "color_primary": "#689f38",
        "color_dark": "#33691e",
        "ecological_stock_ratio": None,
        "paired_with": "paired_reed_harvesting",
    },
    "natural_river_channel": {
        "phases": {
            "0": {"D": 268, "C": 264, "balance": 85.0, "N": 228, "sustainability": 0.97,
                  "name": "Precipitation, Snowmelt, and Catchment Recharge", "transparency": "High"},
            "1": {"D": 268, "C": 264, "balance": 85.0, "N": 228, "sustainability": 0.97,
                  "name": "Tributary Confluence and Flow Accumulation", "transparency": "High"},
            "2": {"D": 264, "C": 232, "balance": 72.0, "N": 183, "sustainability": 0.92,
                  "name": "Channel Morphology and Substrate Function", "transparency": "Medium"},
            "3": {"D": 260, "C": 232, "balance": 72.0, "N": 178, "sustainability": 0.92,
                  "name": "Sediment Transport and Geomorphic Work", "transparency": "Medium"},
            "4": {"D": 268, "C": 256, "balance": 82.0, "N": 218, "sustainability": 0.95,
                  "name": "Flow Delivery to Delta and Black Sea", "transparency": "High"},
        },
        "coherence": {"pi": 79.0, "phi": 52.0, "sqrt2": 71.0, "ln2": 58.0, "e": 32.0},
        "type": "natural",
        "color_primary": "#1565c0",
        "color_dark": "#0d47a1",
        "ecological_stock_ratio": None,
        "paired_with": "paired_navigation",
    },
    "human_commercial_navigation": {
        "phases": {
            "0": {"D": 268, "C": 256, "balance": 83.0, "N": 218, "sustainability": 0.96,
                  "name": "Governance, Regulation, and Route Planning", "transparency": "High"},
            "1": {"D": 264, "C": 244, "balance": 78.0, "N": 197, "sustainability": 0.94,
                  "name": "Port Infrastructure and Cargo Handling", "transparency": "Medium"},
            "2": {"D": 264, "C": 232, "balance": 72.0, "N": 183, "sustainability": 0.92,
                  "name": "Fairway Maintenance and Dredging", "transparency": "Medium"},
            "3": {"D": 268, "C": 264, "balance": 85.0, "N": 228, "sustainability": 0.97,
                  "name": "Transit Operations and Lock Passage", "transparency": "High"},
            "4": {"D": 260, "C": 240, "balance": 78.0, "N": 198, "sustainability": 0.94,
                  "name": "Revenue Capture and Economic Impact", "transparency": "Medium"},
        },
        "coherence": {"pi": 79.0, "phi": 50.0, "sqrt2": 68.0, "ln2": 55.0, "e": 38.0},
        "type": "human",
        "color_primary": "#0277bd",
        "color_dark": "#01579b",
        "ecological_stock_ratio": None,
        "paired_with": "paired_navigation",
    },
}

PHASE_NOTES = {
    "natural_freshwater_availability": {
        "0": "Atmospheric moisture source: Atlantic and Mediterranean evaporation. ERA5 satellite coverage.",
        "1": "Precipitation 800mm/yr mean over 801,463 km2 = 641 km3/yr total basin input.",
        "2": "River discharge 6,500 m3/s mean at mouth; 206 km3/yr runoff. GRDC gauge network.",
        "3": "Groundwater stores ~88 km3; recharge ~12 km3/yr. GRACE-FO basin-scale monitoring.",
        "4": "2,543 m3/person/yr availability; water stress index 0.17 nationally. WFD good ecological status: 40% of water bodies (ICPDR 2021). Phase 4 balance reduced from 90 to 86 to reflect this C-output deficit.",
    },
    "human_irrigation_infrastructure": {
        "0": "Agricultural abstraction 22 km3/yr (63% of basin total). Largest sector. Romania 3.4 km3/yr.",
        "1": "Primary canals ~18,000 km; avg age 45 years; 60% earth (unlined); 18% conveyance loss.",
        "2": "Secondary distribution: ~85,000 km; farm metering only 35% coverage; 15% losses. Most opaque phase.",
        "3": "Field efficiency: gravity 47%, sprinkler 75%, drip 88%. Weighted avg 50%. 5.5 km3/yr saving potential.",
        "4": "Return flow 6.6 km3/yr (30% of abstraction); 62% of water bodies with agricultural pollution pressure.",
    },
    "human_freshwater_supply_infrastructure": {
        "0": "Municipal abstraction 8.5 km3/yr; 65% surface water, 35% groundwater. WFD permits required (EU).",
        "1": "Conveyance losses 2-5%; energy intensity 0.12 kWh/m3. Pipeline networks up to 80km.",
        "2": "EU Drinking Water Directive compliance 99.5%; treatment energy 0.35 kWh/m3. Most energy-intensive phase.",
        "3": "Non-revenue water 25% average; range 10-40%. Key infrastructure deficit in lower basin.",
        "4": "88% access to safely managed water (JMP 2023); 9.7M unserved in rural lower basin.",
    },
    "natural_delta_biodiversity": {
        "0": "Historical sediment 80 Mt/yr; current 34 Mt/yr (57% reduction by Iron Gate I/II dams). Primary structural bottleneck.",
        "1": "Mean discharge 6,500 m3/s at Ceatal Izmail; spring flood pulse to 15,800 m3/s. 22-station DDBRA network.",
        "2": "Reed beds 178,000 ha (largest in Europe); shallow lakes 83,500 ha; habitat diversity H'=2.31. Copernicus 10m mapping.",
        "3": "Dalmatian pelican 3,700 pairs (world's largest colony); fish species richness 45 spp; sturgeon <0.2% historical catch.",
        "4": "Ecotourism 80,000 visitors/yr; €28M revenue; 11 Mt CO2 reed carbon stock. Only 28% habitats in favourable status.",
    },
    "human_cultural_heritage_management": {
        "0": "15 UNESCO World Heritage Sites; Roman Danube Limes 600 km (2021 inscription). 7 of 10 countries with complete national register.",
        "1": "35% of sites in poor condition; EUR 180M/yr conservation funding gap; 340 flood-risk sites. Phase bottleneck.",
        "2": "85 visitor centres; EuroVelo 6 (4,448 km); 250,000 cruise passengers/yr; Vienna 17M, Budapest 5.7M visitors/yr.",
        "3": "3,200 certified guides; 40% informal operators; 180 annual festivals; 140 registered Delta ecotourism operators.",
        "4": "EUR 2.8 billion/yr cultural tourism revenue; 12% conservation reinvestment (benchmark 22%); 62% in formal accounts.",
    },
    "natural_floodplain_forest_biomass": {
        "0": "Flood pulse 40% reduced; lateral connectivity 0.55 (was 0.92); 2,800 km embankments. BOTTLENECK.",
        "1": "Connected floodplain SOC 28 g/kg vs 16 g/kg disconnected; 22% sites with legacy sediment contamination.",
        "2": "160,000 ha remaining (47% loss); 78% canopy in Natura 2000; 18% Robinia invasion; 8,500 ha old-growth.",
        "3": "120 m3/ha growing stock; 5.0 m3/ha/yr increment; 17 Mt CO2 total stock; 1.8 Mt CO2/yr sequestration.",
        "4": "EUR 715M/yr service value; only 3 carbon projects, 0.05 Mt CO2/yr vs 1.0 Mt potential. Service delivery gap.",
    },
    "human_floodplain_forestry_operations": {
        "0": "140,000 ha under management plan; 45% FSC/PEFC certified; 62% riparian zones with formal plans.",
        "1": "800,000 m3/yr harvest; 25% illegal logging in non-EU states; 35% sites with soil compaction from machinery.",
        "2": "210,000 m3/yr sawnwood; 1,200 GWh/yr biomass energy; 52% recovery rate; value-add index 1.6 vs 2.2 EU avg.",
        "3": "45% certified sales; only 50,000 tCO2/yr credits vs 1,000,000 potential; 95% EUTR EU vs 60% non-EU. BOTTLENECK.",
        "4": "EUR 48/ha/yr forest owner revenue (89% timber); carbon only 2%; arable land EUR 185/ha/yr creates conversion incentive.",
    },
    "natural_fish_population": {
        "0": "40% good WFD ecological status; 580 kt/yr N load; 42% eutrophication risk. Target 70% by 2034.",
        "1": "16% migration range accessible; 22% dams with fish pass; Iron Gate I+II NO functional pass. BOTTLENECK at 71%.",
        "2": "38 fish/100m channel vs 112/100m floodplain; 95% sturgeon juveniles from restocking; carp YCS 0.72.",
        "3": "420,000 t biomass; 38,000 t/yr sustainable yield; 58% exploitation rate; 10-yr trend declining.",
        "4": "22,000 t AAC; 72% compliance; 21% illegal catch; 10 countries with sturgeon ban; 480,000 recreational licences.",
    },
    "human_commercial_fishing": {
        "0": "18,500 commercial licences; 78% quota utilisation; coordination index 0.42; 5/10 countries stock-based quotas.",
        "1": "22,000 t legal catch; 31 kg/trip floodplain vs 18 channel CPUE; 4,600 t illegal; 71% gear compliance.",
        "2": "58% cold chain coverage; 8% loss EU vs 21% non-EU; 62% recovery rate; EUR 40M/yr value loss. BOTTLENECK.",
        "3": "68% domestic at EUR 3.80/kg carp; 7,000 t exports; 52% food safety certified; EUR 9.20/kg pike-perch.",
        "4": "EUR 5,800/yr average household income; 8% conservation reinvestment (benchmark 20%); EUR 320M EMFAF 2021-2027.",
    },
    "natural_reed_bed": {
        "0": "145 cm amplitude (was 210 cm; -31%); 380 kt/yr N; 57% sediment reduction. Structural upstream constraints.",
        "1": "850 ha/yr expansion; 320 ha/yr loss to subsidence; 530 ha/yr net gain; 0.25 t/ha new vs 0.48 t/ha mature.",
        "2": "9.8 t/ha mean biomass; 3.2 m culms; 8.4 mm diameter; 62% thatching quality; 17.2 Mt total delta biomass.",
        "3": "800 kt harvestable stock; 58,000 ha accessible; only 25% of sustainable quota (560 kt) actually harvested.",
        "4": "EUR 38M/yr capture vs EUR 232M/yr total ecosystem service value; only 16% monetised. Phase bottleneck.",
    },
    "human_reed_industry": {
        "0": "42,000 ha licensed; 200 kt quota; 140 kt actual (70%); 88% permit compliance; 87,500 ha core zone protected.",
        "1": "140 kt/yr; 65 machines; 12 t/machine-day; 38 ice-access days (declining 1.8 days/yr); 85% mechanical.",
        "2": "35% thatching grade; 65% bulk biomass; EUR 285/t thatching vs EUR 42/t bulk (6.8x differential). BOTTLENECK.",
        "3": "49 kt thatching exports; 42% to UK; no certification standard exists; market access score 0.42. BOTTLENECK.",
        "4": "EUR 1,850/season (4,500 workers); EUR 3.2M/yr DDBRA concession; 18% conservation reinvestment.",
    },
    "natural_river_channel": {
        "0": "6,500 m3/s mean at delta; 206 km3/yr; Alpine 35%; Carpathian 40%; groundwater 25%. Climate shifting snowmelt 2-3 weeks earlier.",
        "1": "350 m3/s Kelheim to 6,500 m3/s delta; 7 major tributaries (Inn; Sava; Tisza; Drava; Mures; Morava; Siret). 75% flow from tributaries.",
        "2": "18% WFD good status; 80% channelised; side-arm connectivity 0.22; 77% gravel bars lost. BOTTLENECK.",
        "3": "17 Mt/yr sediment to delta (was 40 Mt; -57% Iron Gate); 8 mm/yr bed incision; delta -3.7 mm/yr net. BOTTLENECK.",
        "4": "195 km3/yr to Black Sea; 380 kt N/yr; 12 kt P/yr; Chilia arm 58%; Sulina 21%; Sfantu Gheorghe 21%.",
    },
    "human_commercial_navigation": {
        "0": "13 member states; 85% harmonised vessel registration; 78% RIS coverage; 92% fairway notice currency.",
        "1": "68 ports; 34 Mt/yr throughput; 75 Mt/yr capacity (45% utilisation); 18 hr turnaround; 52% intermodal.",
        "2": "4.5 Mm3/yr dredged EUR 28M/yr; 42 restriction days avg (68 in 2022); 74% fairway compliance; 7 critical shallows. BOTTLENECK.",
        "3": "6,800 passages Iron Gate; 7,200 Gabcikovo; 3.2 hr lock wait; 13-day full transit; 95% AIS coverage. STRONGEST.",
        "4": "EUR 6.5 bn/yr trade value; EUR 420M/yr freight savings vs road; 93,000 port FTE; EUR 4.2 bn TEN-T backlog.",
    },
}


def build_supply_chain_ui(slug: str) -> dict:
    """Build the _supply_chain_ui.json structure for a subproject."""
    data = NDC_DATA[slug]
    phases = data["phases"]
    notes_map = PHASE_NOTES.get(slug, {})

    phase_meta = {}
    phases_synthetic = {}

    for pid, p in phases.items():
        phase_meta[pid] = {
            "name": p["name"],
            "transparency": p["transparency"],
            "transformation": "ecological_cascade" if data["type"] == "natural" else "engineered_process",
        }
        entry = {
            "D": p["D"],
            "C": p["C"],
            "balance": p["balance"],
            "N": p["N"],
            "sustainability": p["sustainability"],
            "notes": notes_map.get(pid, ""),
            "data_quality": "High" if p["transparency"] == "High" else "Medium",
            "scope1_tco2": None,
            "scope2_tco2": None,
            "scope_source": "Not provided — requires separate data input",
            "scope_quality": "No data",
            "water": None,
            "energy": None,
            "water_recycling_pct": None,
            "energy_clean_pct": None,
        }
        if data["type"] == "natural" and data.get("ecological_stock_ratio") is not None:
            entry["ecological_stock_ratio"] = data["ecological_stock_ratio"]
            entry["stock_ratio_note"] = "Ratio of total abstraction to annual renewable freshwater resource"
        phases_synthetic[pid] = entry

    avg_balance = sum(p["balance"] for p in phases.values()) / len(phases)
    min_phase = min(phases.items(), key=lambda x: x[1]["balance"])
    max_phase = max(phases.items(), key=lambda x: x[1]["balance"])

    return {
        "_meta": {
            "generated": datetime.now().isoformat(),
            "generator": "scripts/generate_danube_data.py",
            "material": slug,
            "basin": "danube",
            "service_type": data["type"],
            "paired_with": data.get("paired_with"),
            "sources": [
                f"frontend/project/danube/{slug}/data/PDI_{slug.replace(data['type'] + '_', '')}_danube_2026.yaml",
                f"frontend/project/danube/{slug}/data/schema/{slug}_supply_chain_phases.csv",
                f"frontend/project/danube/{slug}/data/schema/{slug}_supply_chain_metrics.csv",
            ],
            "note": "Synthetic baseline from PDI phase derivation. Re-run generate_danube_data.py to refresh.",
        },
        "entities": {
            "synthetic": {
                "label": "Synthetic Baseline",
                "description": f"PDI-derived baseline for Danube Basin {slug.replace('_', ' ')}. "
                               f"Not tied to a specific operator.",
            }
        },
        "phase_meta": phase_meta,
        "phases": {"synthetic": phases_synthetic},
        "system": {
            "synthetic": {
                "balance": round(avg_balance, 1),
                "average_N": round(sum(p["N"] for p in phases.values()) / len(phases)),
                "bottleneck_phase_ids": [
                    pid for pid, p in phases.items() if p["balance"] < 85
                ],
                "water_recycling_pct": None,
                "waste_circularity_pct": None,
                "clean_energy_pct": None,
                "interpretation": (
                    f"Chain average balance {avg_balance:.1f}%. "
                    f"Strongest phase: {max_phase[1]['name']} ({max_phase[1]['balance']}%). "
                    f"Weakest phase: {min_phase[1]['name']} ({min_phase[1]['balance']}%). "
                    + (f"Bottleneck phases: {[min_phase[0]]}." if avg_balance < 90 else "No significant bottlenecks detected.")
                ),
            }
        },
    }


def build_system_lifecycle_ndc(slug: str) -> dict:
    """Build the _system_lifecycle_ndc.json structure."""
    data = NDC_DATA[slug]
    phases_raw = data["phases"]
    phase_items = sorted(phases_raw.items(), key=lambda x: int(x[0]))

    lifecycle_phases = []
    for pid, p in phase_items:
        lifecycle_phases.append({
            "lifecycle_phase_id": int(pid),
            "phase_name": p["name"],
            "category": "Natural process" if data["type"] == "natural" else "Engineered",
            "parent_N": f"Phase {pid} output as stable state",
            "D_total": p["D"],
            "C_total": p["C"],
            "balance_score": p["balance"],
            "N": p["N"],
            "sustainability_index": p["sustainability"],
            "transparency_level": p["transparency"].lower(),
            "D_parameters": ["See supply_chain_phases.csv for phase-specific D parameters"],
            "C_parameters": ["See supply_chain_phases.csv for phase-specific C parameters"],
            "notes": PHASE_NOTES.get(slug, {}).get(pid, ""),
        })

    return {
        "_meta": {
            "material": slug,
            "basin": "danube",
            "service_type": data["type"],
            "layer": "system_lifecycle_ndc",
            "generated": datetime.now().strftime("%Y-%m-%d"),
            "sources": [
                f"frontend/project/danube/{slug}/data/PDI_{slug}_danube_2026.yaml",
                f"frontend/project/danube/{slug}/data/schema/{slug}_supply_chain_phases.csv",
            ],
            "note": f"Lifecycle N-D-C layer for Danube Basin {slug.replace('_', ' ')}.",
        },
        "lifecycle_definition": {
            "purpose": f"Evaluate {'ecological production function' if data['type'] == 'natural' else 'infrastructure supply chain'} performance and sustainability.",
            "service_type": data["type"],
            "paired_with": data.get("paired_with"),
            "phase_sequence": [p["name"] for _, p in phase_items],
        },
        "phases": lifecycle_phases,
    }


def build_scenarios(slug: str) -> dict:
    """Build the supply_chain/scenarios.json file."""
    data = NDC_DATA[slug]
    phases = data["phases"]
    coherence = data["coherence"]
    phase_ids = sorted(phases.keys(), key=int)

    def make_scenario_phases(multipliers: dict, default: float = 1.0) -> list:
        result = []
        for pid in phase_ids:
            p = phases[pid]
            m = multipliers.get(pid, default)
            score = round(min(100, p["balance"] * m), 1)
            N = round(min(290, p["N"] * m))
            result.append({"score": score, "N": N})
        return result

    def avg_score(scenario_phases: list) -> float:
        return round(sum(p["score"] for p in scenario_phases) / len(scenario_phases), 1)

    current_phases = make_scenario_phases({}, 1.0)
    optimum_phases = make_scenario_phases({}, 1.0)
    optimum_phases = [{"score": 100, "N": round(min(290, p["N"] * 1.08))} for _, p in phases.items()]
    shock_phases = make_scenario_phases({"3": 0.65}, 0.92)
    drought_phases = make_scenario_phases({"2": 0.70, "3": 0.60}, 0.90)
    invest_phases = make_scenario_phases({"3": 1.20}, 1.05)
    climate_phases = make_scenario_phases({"1": 0.85, "2": 0.80}, 0.95)

    c = coherence
    return {
        "pi": {
            "scenarios": {
                "current":  {"label": "Current State",        "description": "Baseline from PDI derivation", "phases": current_phases,  "cards": {"balance": {"val": str(avg_score(current_phases)), "pct": avg_score(current_phases), "cls": "good", "status": "Good"}}},
                "optimum":  {"label": "All Optimum",          "description": "All phases at full balance",   "phases": optimum_phases,  "cards": {"balance": {"val": "100", "pct": 100, "cls": "excellent", "status": "Excellent"}}},
                "shock_1":  {"label": "Drought / Low Flow",   "description": "Reduced flow in phases 2-3",   "phases": shock_phases,    "cards": {"balance": {"val": str(avg_score(shock_phases)),  "pct": avg_score(shock_phases),  "cls": "fair", "status": "Stressed"}}},
                "shock_2":  {"label": "Climate Shift",        "description": "Reduced precipitation phases 1-2", "phases": climate_phases, "cards": {"balance": {"val": str(avg_score(climate_phases)), "pct": avg_score(climate_phases), "cls": "fair", "status": "Stressed"}}},
                "expansion":{"label": "Infrastructure Investment", "description": "Network improvement (phase 3 upgrade)", "phases": invest_phases, "cards": {"balance": {"val": str(avg_score(invest_phases)), "pct": avg_score(invest_phases), "cls": "good", "status": "Improving"}}},
                "regulatory":{"label": "Drought + Investment", "description": "Climate stress with partial mitigation", "phases": drought_phases, "cards": {"balance": {"val": str(avg_score(drought_phases)), "pct": avg_score(drought_phases), "cls": "fair", "status": "Mixed"}}},
            }
        },
        "phi": {"scenarios": {}},
        "sqrt2": {"scenarios": {}},
        "ln2": {"scenarios": {}},
        "e": {"scenarios": {}},
        "coherence_scores": {
            "scenarios": {
                "current":    {"label": "Current State",          "pi": c["pi"],  "phi": c["phi"],  "sqrt2": c["sqrt2"], "ln2": c["ln2"], "e": c["e"]},
                "optimum":    {"label": "All Optimum",            "pi": 100,      "phi": 99.0,      "sqrt2": 100.0,      "ln2": 100.0,    "e": 100},
                "shock_1":    {"label": "Drought / Low Flow",     "pi": round(c["pi"] * 0.82, 1), "phi": round(c["phi"] * 0.80, 1), "sqrt2": round(c["sqrt2"] * 0.88, 1), "ln2": round(c["ln2"] * 0.78, 1), "e": round(c["e"] * 0.70, 1) if c["e"] > 0 else 0},
                "shock_2":    {"label": "Climate Shift",          "pi": round(c["pi"] * 0.78, 1), "phi": round(c["phi"] * 0.75, 1), "sqrt2": round(c["sqrt2"] * 0.82, 1), "ln2": round(c["ln2"] * 0.72, 1), "e": round(c["e"] * 0.65, 1) if c["e"] > 0 else 0},
                "expansion":  {"label": "Infrastructure Invest",  "pi": round(min(99, c["pi"] * 1.05), 1), "phi": c["phi"], "sqrt2": round(min(99, c["sqrt2"] * 1.08), 1), "ln2": c["ln2"], "e": round(min(99, c["e"] * 1.20), 1) if c["e"] > 0 else 0},
                "regulatory": {"label": "Drought + Investment",   "pi": round(c["pi"] * 0.90, 1), "phi": c["phi"], "sqrt2": c["sqrt2"], "ln2": c["ln2"], "e": c["e"]},
            }
        },
    }


def generate_subproject(slug: str, danube_dir: Path) -> None:
    if slug not in NDC_DATA:
        print(f"  [SKIP] {slug} — not in NDC_DATA registry")
        return

    subproject_dir = danube_dir / slug
    processed_dir = subproject_dir / "data" / "processed"
    sc_dir = subproject_dir / "supply_chain"
    processed_dir.mkdir(parents=True, exist_ok=True)
    sc_dir.mkdir(parents=True, exist_ok=True)

    # supply_chain_ui.json
    ui_data = build_supply_chain_ui(slug)
    ui_path = processed_dir / f"{slug}_supply_chain_ui.json"
    with open(ui_path, "w") as f:
        json.dump(ui_data, f, indent=2)
    print(f"  [OK] {ui_path.relative_to(danube_dir.parent.parent.parent)}")

    # system_lifecycle_ndc.json
    lifecycle_data = build_system_lifecycle_ndc(slug)
    lc_path = processed_dir / f"{slug}_system_lifecycle_ndc.json"
    with open(lc_path, "w") as f:
        json.dump(lifecycle_data, f, indent=2)
    print(f"  [OK] {lc_path.relative_to(danube_dir.parent.parent.parent)}")

    # scenarios.json
    scenarios_data = build_scenarios(slug)
    sc_path = sc_dir / "scenarios.json"
    with open(sc_path, "w") as f:
        json.dump(scenarios_data, f, indent=2)
    print(f"  [OK] {sc_path.relative_to(danube_dir.parent.parent.parent)}")


def main():
    parser = argparse.ArgumentParser(description="Generate Danube Basin subproject JSON data files")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Process all registered subprojects")
    group.add_argument("--subproject", type=str, help="Process a single subproject by slug")
    args = parser.parse_args()

    danube_dir = DANUBE_DIR
    if not danube_dir.exists():
        print(f"ERROR: Danube project directory not found: {danube_dir}")
        return

    if args.all:
        slugs = list(NDC_DATA.keys())
    else:
        slugs = [args.subproject]

    print(f"\nGenerating Danube Basin data files — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Base dir: {danube_dir}")
    print("-" * 60)

    for slug in slugs:
        print(f"\n[{slug}]")
        generate_subproject(slug, danube_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
