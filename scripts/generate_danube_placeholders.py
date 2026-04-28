#!/usr/bin/env python3
"""
generate_danube_placeholders.py
================================
Creates placeholder index.html pages for all Danube Basin subprojects
that have not yet been built out (all except the two pilot subprojects).

Run from repo root:
    python scripts/generate_danube_placeholders.py
"""

import os
from pathlib import Path

DANUBE_DIR = Path(__file__).parent.parent / "frontend" / "project" / "danube"

SKIP = {"natural_freshwater_availability", "human_freshwater_supply_infrastructure"}

# (slug, display_name, teeb_category, short_description, paired_slug_or_None)
SUBPROJECTS = [
    # ── Natural ──
    ("natural_fish_population",
     "Fish Population",
     "Provisioning",
     "The self-regenerating wild fish stock in the Danube river system. Includes 6 critically endangered sturgeon species. The natural asset underlying the paired fisheries extraction chain.",
     "paired_fisheries"),
    ("natural_wild_food_fodder",
     "Wild Food and Fodder",
     "Provisioning",
     "Wild plant, mushroom, and fodder resources produced by riparian and floodplain habitats. Provisioning service supporting rural communities across the basin.",
     None),
    ("natural_reed_bed",
     "Reed Bed Biomass",
     "Provisioning",
     "Reed (Phragmites australis) beds in the Danube Delta and floodplain — the largest reed habitat in Europe. Natural biomass production underpinning harvesting and building material supply chains.",
     "paired_reed_harvesting"),
    ("natural_river_groundwater_flow",
     "River-Groundwater Flow",
     "Regulating",
     "Natural hydrological connectivity between the Danube river channel and floodplain aquifers (hyporheic zone). Regulates water temperature, chemistry, and groundwater recharge.",
     None),
    ("natural_floodplain_forest_biomass",
     "Floodplain Forest Biomass",
     "Provisioning / Habitat",
     "Softwood and hardwood timber biomass in Danube floodplain forest ecosystems. Natural stock asset paired with the floodplain forestry extraction chain.",
     "paired_floodplain_forestry"),
    ("natural_flood_regulation",
     "Flood Regulation",
     "Regulating",
     "The natural capacity of floodplains, wetlands, and forested catchments to attenuate peak flows and reduce flood risk downstream. Quantifiable via peak-flow reduction metrics.",
     None),
    ("natural_water_purification",
     "Water Purification",
     "Regulating",
     "Natural filtration and chemical processing of pollutants by riparian vegetation, wetlands, and river sediments — reducing nutrient and contaminant loads before water reaches abstraction points.",
     None),
    ("natural_carbon_sequestration",
     "Carbon Sequestration",
     "Regulating / Climate",
     "Carbon capture and long-term storage by floodplain forests, riparian vegetation, and Danube Delta peatlands. Quantifiable via biomass carbon density and soil organic carbon surveys.",
     None),
    ("natural_erosion_sediment_regulation",
     "Erosion and Sediment Regulation",
     "Regulating",
     "Natural binding of soils by riparian vegetation and reduction of sediment transport into the river channel. Critical for navigation depth, delta formation, and water quality.",
     None),
    ("natural_groundwater_recharge",
     "Groundwater Recharge",
     "Regulating",
     "Natural replenishment of floodplain and karst aquifers by infiltrating precipitation and river bank filtration. Distinct from freshwater availability — focuses on the recharge process itself.",
     None),
    ("natural_climate_regulation",
     "Climate Regulation",
     "Regulating / Climate",
     "Local and regional climate moderation by the Danube Basin's wetlands, forests, and open water surfaces through evapotranspiration, albedo, and heat buffering.",
     None),
    ("natural_delta_biodiversity",
     "Delta Biodiversity Habitat",
     "Habitat / Supporting",
     "The Danube Delta — UNESCO World Heritage Site and Ramsar Wetland — supporting one of Europe's most biodiverse aquatic and terrestrial ecosystems across 5,800 km².",
     None),
    ("natural_migratory_bird_habitat",
     "Migratory Bird Habitat",
     "Habitat / Cultural",
     "Stop-over and breeding habitat for hundreds of migratory bird species along the Danube corridor. Supports ecotourism and is an indicator species for overall ecosystem health.",
     "paired_ecotourism"),
    ("natural_sturgeon_spawning_habitat",
     "Sturgeon Spawning Habitat",
     "Habitat / Supporting",
     "Spawning grounds for all 6 Danube sturgeon species (5 IUCN Critically Endangered). Free-flowing river sections and gravelled substrate are the key physical requirements.",
     None),
    ("natural_floodplain_forest_habitat",
     "Floodplain Forest Habitat",
     "Habitat / Supporting",
     "Structurally complex floodplain forest ecosystems providing habitat for specialist riparian species. Distinct from the biomass provisioning service — focuses on habitat connectivity and biodiversity.",
     None),
    ("natural_nutrient_cycling",
     "Nutrient Cycling",
     "Supporting",
     "Biological and chemical cycling of nitrogen, phosphorus, and organic matter through aquatic and riparian food webs. Fundamental supporting service underpinning all other ecosystem services.",
     None),
    ("natural_primary_production",
     "Primary Production",
     "Supporting",
     "Phytoplankton, periphyton, and macrophyte photosynthetic production forming the base of the aquatic food web. Measured via chlorophyll-a concentrations and satellite-derived productivity indices.",
     None),
    ("natural_river_channel",
     "River Channel",
     "Habitat / Regulating",
     "The physical river channel itself as a natural infrastructure: geomorphological form, flow regime, substrate, and connectivity. The structural basis for all in-channel ecosystem services.",
     None),

    # ── Human ──
    ("human_commercial_navigation",
     "Commercial Navigation",
     "Provisioning (Transport)",
     "The Danube is Europe's second busiest inland waterway. Commercial navigation infrastructure: locks, dredging, port facilities, and fleet management. Generates significant freight transport value.",
     "paired_navigation"),
    ("human_flood_embankments",
     "Flood Embankments",
     "Regulating (Infrastructure)",
     "Engineered flood embankments, dikes, and reservoirs protecting agricultural land and settlements. Major infrastructure asset across the lower Danube basin countries.",
     None),
    ("human_irrigation_infrastructure",
     "Irrigation Infrastructure",
     "Provisioning (Agriculture)",
     "Irrigation abstraction and distribution infrastructure for agricultural water supply. Hungary, Romania, Bulgaria, and Serbia are major users. Largest single abstraction sector (22 km³/yr).",
     "paired_agricultural_water"),
    ("human_cultural_heritage_management",
     "Cultural Heritage Management",
     "Cultural (Infrastructure)",
     "Managed cultural heritage sites along the Danube corridor: Roman fortifications, medieval castles, historic towns, and the Danube Delta cultural landscape. Supports cultural tourism.",
     None),

    # ── Paired ──
    ("paired_fisheries",
     "Fisheries",
     "Paired: Provisioning",
     "Paired service: natural fish population (ecological stock) + fisheries extraction and management (human activity chain). Commercial and subsistence fishing across 19 countries.",
     None),
    ("paired_reed_harvesting",
     "Reed Harvesting",
     "Paired: Provisioning",
     "Paired service: natural reed bed biomass (Danube Delta) + commercial reed harvesting operations. Delta reed is harvested for thatching, insulation, and construction markets.",
     None),
    ("paired_floodplain_forestry",
     "Floodplain Forestry",
     "Paired: Provisioning",
     "Paired service: natural floodplain forest biomass + managed forestry extraction chain. Floodplain timber supply with strict ecological constraints under EU Habitats Directive.",
     None),
    ("paired_freshwater_supply",
     "Freshwater Supply",
     "Paired: Provisioning",
     "The primary pilot pair — natural freshwater availability + human freshwater supply infrastructure. See the pilot subprojects for the fully developed versions of both components.",
     None),
    ("paired_agricultural_water",
     "Agricultural Water",
     "Paired: Provisioning",
     "Paired service: natural freshwater availability (agricultural allocation) + irrigation infrastructure chain. Largest water-use sector: 22 km³/yr abstraction across the basin.",
     None),
    ("paired_ecotourism",
     "Ecotourism",
     "Paired: Cultural",
     "Paired service: natural habitat services (Delta biodiversity, migratory birds, sturgeon) + ecotourism management infrastructure (visitor centres, guided tours, accommodation, transport).",
     None),
    ("paired_navigation",
     "Navigation",
     "Paired: Provisioning",
     "Paired service: natural river channel (the physical waterway) + commercial navigation infrastructure (locks, dredging, ports, fleet). Key economic artery for Central and Eastern Europe.",
     None),
]

COLORS = {
    "natural": {"primary": "#2e7d32", "dark": "#1b5e20", "light": "#e8f5e9", "bg": "#1b5e20, #2e7d32"},
    "human":   {"primary": "#1565c0", "dark": "#0d47a1", "light": "#e3f2fd", "bg": "#0d47a1, #1565c0"},
    "paired":  {"primary": "#e65100", "dark": "#bf360c", "light": "#fbe9e7", "bg": "#bf360c, #e65100"},
}

ICONS = {
    "natural": "🌿",
    "human":   "🏗️",
    "paired":  "🔗",
}

TEEB_ICONS = {
    "Provisioning": "🌱",
    "Regulating": "⚖️",
    "Habitat / Supporting": "🦋",
    "Supporting": "🔄",
    "Cultural": "🎭",
    "Paired: Provisioning": "🔗",
    "Paired: Cultural": "🔗",
}


def slug_to_name(slug):
    parts = slug.split("_")[1:]
    return " ".join(p.capitalize() for p in parts)


def build_placeholder(slug, display_name, teeb_category, description, paired_with):
    stype = slug.split("_")[0]  # natural / human / paired
    c = COLORS[stype]
    icon = ICONS[stype]
    teeb_icon = TEEB_ICONS.get(teeb_category.split(" /")[0].strip(), "📋")
    paired_html = ""
    if paired_with:
        paired_label = slug_to_name(paired_with)
        paired_type = paired_with.split("_")[0]
        paired_html = f"""
      <div style="background:#fff8e1;border-left:3px solid #f57f17;border-radius:8px;padding:12px 16px;margin-top:14px;font-size:13px;color:#6c757d;">
        <strong style="color:#e65100;">Paired with:</strong>
        <a href="../{paired_with}/index.html" style="color:#e65100;font-weight:700;text-decoration:none;">{paired_label}</a>
        &nbsp;({paired_type} service) — not yet available
      </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{display_name} — Danube Basin</title>
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:ui-sans-serif,system-ui,sans-serif; background:linear-gradient(135deg,{c['bg']} 100%); min-height:100vh; padding:24px; }}
    .container {{ max-width:760px; margin:0 auto; }}
    .panel {{ background:#fff; border-radius:14px; box-shadow:0 20px 60px rgba(0,0,0,0.28); padding:44px; text-align:center; }}
    .kicker {{ display:inline-block; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:{c['primary']}; background:{c['light']}; padding:5px 14px; border-radius:999px; margin-bottom:16px; }}
    h1 {{ font-size:32px; font-weight:300; color:#2c3e50; margin-bottom:8px; }}
    .type-badge {{ display:inline-block; font-size:11px; font-weight:700; color:#fff; background:{c['primary']}; padding:3px 10px; border-radius:999px; margin-left:8px; vertical-align:middle; }}
    .teeb {{ display:inline-block; font-size:12px; color:#6c757d; background:#f8f9fa; padding:4px 12px; border-radius:6px; margin:10px 0 18px; }}
    .desc {{ font-size:14px; color:#495057; line-height:1.7; max-width:560px; margin:0 auto 24px; text-align:left; }}
    .not-available {{
      background:#f8f9fa; border:2px dashed #dee2e6; border-radius:12px;
      padding:32px; margin:8px 0 24px;
    }}
    .not-available .icon {{ font-size:40px; margin-bottom:12px; }}
    .not-available h2 {{ font-size:20px; font-weight:400; color:#6c757d; margin-bottom:6px; }}
    .not-available p {{ font-size:13px; color:#9e9e9e; line-height:1.6; }}
    .btn {{ display:inline-block; padding:10px 22px; border-radius:8px; text-decoration:none; font-weight:700; font-size:13px; color:#fff; background:linear-gradient(135deg,{c['bg']} 100%); }}
    .btn:hover {{ opacity:.88; }}
    .back-link {{ margin-top:16px; font-size:13px; }}
    .back-link a {{ color:{c['primary']}; text-decoration:none; font-weight:700; }}
    .nav {{ text-align:center; margin-top:16px; }}
    .nav a {{ display:inline-block; color:rgba(255,255,255,.9); text-decoration:none; font-size:13px; font-weight:600; margin:0 10px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="panel">
      <div class="kicker">Danube Basin · {stype.capitalize()} Service</div>
      <h1>{icon} {display_name}<span class="type-badge">{stype.capitalize()}</span></h1>
      <div class="teeb">{teeb_icon} {teeb_category}</div>
      <p class="desc">{description}</p>

      <div class="not-available">
        <div class="icon">🚧</div>
        <h2>Not yet available</h2>
        <p>
          This subproject has not yet been built out. It will follow the same architecture
          as the pilot subprojects: PDI YAML, supply chain phases CSV, processed JSON data,
          N-D-C dashboard, system lifecycle view, and value chain layer.
        </p>
      </div>
      {paired_html}

      <a href="../index.html" class="btn">← Back to Danube Basin Hub</a>
    </div>
  </div>
  <div class="nav">
    <a href="../../index.html">← Danube Hub</a>
    <a href="/index.html">Main Homepage</a>
  </div>
</body>
</html>
"""


def main():
    created = 0
    for slug, display_name, teeb, desc, paired in SUBPROJECTS:
        if slug in SKIP:
            print(f"  [SKIP] {slug} (pilot — already built)")
            continue
        target_dir = DANUBE_DIR / slug
        target_dir.mkdir(parents=True, exist_ok=True)
        index_path = target_dir / "index.html"
        html = build_placeholder(slug, display_name, teeb, desc, paired)
        with open(index_path, "w") as f:
            f.write(html)
        print(f"  [OK]   {index_path.relative_to(DANUBE_DIR.parent.parent.parent)}")
        created += 1

    print(f"\nCreated {created} placeholder pages.")


if __name__ == "__main__":
    main()
