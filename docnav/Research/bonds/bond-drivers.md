reference article: https://claritycoalition.net/2-degrees-is-too-much/

related research:
  - pittock_freshwater_synopsis.md: Synopsis of Jamie Pittock's freshwater ecosystem
    research and cross-reference with Danube project data. Key findings: irrigation
    efficiency paradox (Grafton et al. Science 2018), climate change flow gap (Colloff
    and Pittock Water 2022), environmental flow delivery gap, hydropower-fisheries
    trade-offs. Directly updates human_irrigation_infrastructure and
    natural_freshwater_availability PDI analyst notes and metrics CSVs.

Quantifiability key:
  [H] = High: publicly available, regularly updated, usable immediately
  [M] = Medium: available but modeled, infrequent, or requires processing
  [L] = Low: sparse, regional, estimated, or paywalled
  [X] = None: no standardized global dataset exists

---

# CO2

- adaptation (natural and manmade)
  - [L] UNFCCC NDC Adaptation Communications; Global Adaptation Index (Notre Dame GAIN); inconsistent national reporting
- mitigation (natural and manmade)
  - [H] UNFCCC NDC Registry; IEA World Energy Statistics; Global Carbon Project annual budget
- sequestering CO2
  - forests (photosynthesis, above-ground biomass)
    - [H] Global Forest Watch (Hansen/UMD, near real-time); FAO Global Forest Resources Assessment (every 5yr); Global Carbon Project
  - wetlands (peat, soil carbon)
    - [M] Global Peatlands Initiative; IPCC Wetlands Supplement; updates infrequent
  - mangroves (blue carbon)
    - [H] Global Mangrove Watch (JAXA satellite, annual); Blue Carbon Initiative stocks database
  - seagrass beds
    - [L] UNEP-WCMC Ocean+ Seagrass; global coverage patchy, primarily field surveys
  - oceans (dissolved CO2, biological pump)
    - [H] SOCAT (surface ocean CO2 atlas); ARGO float network; NOAA Ocean Carbon and Acidification program
- extracting CO2
  - deforestation (release of stored carbon)
    - [H] Global Forest Watch tree cover loss (near real-time); PRODES Brazil; FAOSTAT emissions
  - land-use conversion
    - [H] ESA CCI Land Cover (annual); Copernicus Global Land Service; Hansen/GFW change layers
  - soil degradation (loss of soil organic carbon)
    - [M] FAO GLADIS; ISRIC World Soil Information; globally modeled, not directly measured
  - burning biomass
    - [H] GFED (Global Fire Emissions Database); MODIS Active Fire; Copernicus GFAS (daily)
- storage (natural and manmade)
  - terrestrial: forests, peatlands, permafrost, soils
    - [M] IPCC AR6 carbon stock tables; ESA CCI Permafrost; Global Carbon Project; static snapshots, not live monitoring
  - oceanic: deep water, sediments
    - [L] Estimated from sparse ocean sampling campaigns; SOCAT covers surface only
  - engineered: CCS, biochar
    - [M] IEA CCS Tracker; Global CCS Institute project database; biochar highly fragmented
- use (natural and manmade)
  - combustion (energy, transport)
    - [H] IEA World Energy Statistics; EIA; BP Statistical Review (annual)
  - industrial process emissions
    - [H] EDGAR database (EU JRC, covers 200+ countries, sector-level, annual)
  - agricultural emissions (land conversion, livestock)
    - [H] FAOSTAT GHG domain; EDGAR agriculture module; livestock methane well-tracked

---

# Water

- freshwater supply
  - glacial retreat (supply for ~1 billion people across the Eastern Himalayas region)
    - [H] World Glacier Monitoring Service (WGMS); GRACE/GRACE-FO satellites (ice mass loss)
  - snowpack loss
    - [H] MODIS Snow Cover (daily); SNOTEL network (US); EUMETSAT H-SAF
  - groundwater depletion
    - [M] GRACE-FO (basin scale only); national monitoring networks highly variable in coverage
- water flow regulation
  - upland wetland protection (reduces flooding and contaminated water disease)
    - [L] No direct global monitoring; inferred from wetland extent (Ramsar/WCMC) + flood event databases
  - river restoration (Danube, Central Yangtze flood capacity)
    - [L] Global Runoff Data Centre (GRDC) has flow data; restoration outcomes tracked case-by-case only
  - dam and reservoir interaction
    - [M] GRanD database (global reservoirs and dams); HydroSHEDS; storage volumes available
- water quality
  - groundwater contamination (nutrient and agrochemical runoff)
    - [L] WHO/UNEP GEMS-Water; sparse and nationally inconsistent; no global operational product
  - increased evaporation rates (concentration of pollutants)
    - [M] GLEAM (Global Land Evaporation Amsterdam Model); ERA5 reanalysis evapotranspiration
  - sediment loading from erosion
    - [L] Limited global dataset; some regional via ADB and World Bank country studies
- flooding
  - wetland flood retention capacity (Central Yangtze: 75% = 2.8 Bm3)
    - [L] Dartmouth Flood Observatory tracks events, not retention capacity; modeled via HEC-RAS or LISFLOOD
  - natural floodplain restoration vs. engineered embankments
    - [L] No global comparison dataset; national studies only
  - extreme precipitation events
    - [H] NOAA GHCN-Daily; ERA5 reanalysis (hourly); GPM Global Precipitation Measurement (daily, near real-time)
- drought
  - Altai-Sayan: climate-driven drought killed 4.3 million livestock
    - [M] EM-DAT disaster database; NDMC; SPEI/PDSI indices; livestock loss data via FAO
  - reduced river flow (Ruaha Basin: 50% of Tanzania's electricity, 45% of GDP)
    - [M] GRDC streamflow; national hydrological services; coverage weakest in sub-Saharan Africa
  - soil moisture loss
    - [H] ESA CCI Soil Moisture (satellite composite, daily); NASA SMAP; ERA5

---

# Coastal and Marine Systems

- coastal defense
  - mangroves: wave energy absorption, storm surge reduction
    - [H] extent: Global Mangrove Watch (JAXA, annual); [M] service value: InVEST model, requires local calibration
  - coral reefs: wave breaking, sediment trapping
    - [H] extent: Allen Coral Atlas (global, 2020 baseline); GCRMN monitoring sites
    - [H] bleaching/thermal stress: NOAA Coral Reef Watch (near real-time satellite)
  - salt marshes: tidal buffering
    - [M] WCMC global salt marsh dataset; less complete than mangroves; updated infrequently
  - dunes: shoreline stabilization
    - [L] No standardized global dataset; shoreline position via Copernicus or CoastSat (research tool)
  - engineered alternatives costs (Sundarbans embankments: US$294M capital + US$6M/year maintenance)
    - [L] World Bank project databases; country-by-country; no unified global cost comparison
- fisheries productivity
  - reef-dependent fisheries
    - [M] FAO FishStat + Sea Around Us; reef-specific attribution requires modeling
  - mangrove nursery function
    - [L] WCMC; indirect/modeled relationship; no direct global measurement
  - Southern Ocean fisheries: ~US$1 billion/year
    - [H] CCAMLR annual statistical bulletin (direct source cited in article)
- sea level rise
  - rate
    - [H] NASA/CNES satellite altimetry (TOPEX, Jason-3, Sentinel-6); NOAA tide gauge network
  - coastal inundation risk
    - [H] CoastalDEM; IPCC AR6 regional sea level projections; Climate Central
  - saltwater intrusion into freshwater and agricultural land
    - [M] Modeled from DEM + sea level scenarios; national groundwater monitoring inconsistent
- ocean temperature and acidification
  - sea surface temperature
    - [H] NOAA OISST (daily); Copernicus Marine Service; ERSST
  - acidification (pH)
    - [M] SOCAT CO2 atlas; GOA-ON network; improving coverage but still patchy in Southern Hemisphere
  - coral bleaching events
    - [H] NOAA Coral Reef Watch thermal anomaly alerts (near real-time)
  - species range shift
    - [L] OBIS (Ocean Biodiversity Information System); presence data available, trend analysis requires modeling

---

# Terrestrial and Land Systems

- deforestation
  - rates
    - [H] Global Forest Watch (near real-time Hansen/UMD alerts); FAO FRA (every 5yr)
  - carbon emissions from loss
    - [H] Global Carbon Project; FAOSTAT; GFW carbon flux model
  - watershed regulation loss
    - [L] Modeled via InVEST or SWAT; no direct global operational dataset
- land-use conversion
  - agriculture expansion (soil carbon loss, biodiversity loss)
    - [H] ESA CCI Land Cover (annual); FAO Land Use domain; FAOSTAT
  - urbanization (impermeable surfaces, runoff increase)
    - [H] Global Human Settlement Layer (EU JRC, 1975-present); ESA CCI Urban
- soil erosion
  - rates (Gran Chaco-Salteño: 40-60% reduction in original soil cover)
    - [M] RUSLE/USLE global models (FAO, EU JRC ESDAC); modeled not directly measured
  - sedimentation of rivers and reefs
    - [L] Limited global dataset; ADB and World Bank regional studies; no operational product
- slope stabilization
  - landslide events and risk
    - [M] NASA Global Landslide Catalog; UNDRR DESINVENTAR; event-based, not continuous monitoring
  - forest cover as stabilization proxy
    - [H] Hansen/GFW tree cover and loss layers (directly usable)

---

# Biodiversity

- species extinction risk
  - current Red List status
    - [H] IUCN Red List (100,000+ species assessed, updated continuously)
  - habitat loss as driver
    - [H] Can be calculated from land cover change (GFW/ESA CCI) overlaid on IUCN species range maps
  - range compression under climate scenarios
    - [M] Species distribution models (SDMs) using GBIF occurrence data + CMIP6 climate projections
- gene pool protection
  - crop wild relatives
    - [M] Genesys (genebank accessions); GBIF; Kew Crop Wild Relative Portal; coverage improving
  - marine genetic diversity
    - [L] eDNA studies emerging; OBIS for presence; no global operational genetic diversity dataset
- ecosystem resilience
  - species richness
    - [H] GBIF (occurrence data); effort-corrected richness requires modeling but data is immediate
  - net primary production (correlated with richness)
    - [H] MODIS NPP (MOD17, monthly); Copernicus BioPAR; well-established operational product
  - functional diversity
    - [L] Research datasets only (TRY plant traits, PREDICTS); no operational global product
- invasive species
  - presence and spread
    - [M] GBIF; IUCN ISSG (Global Invasive Species Database); CABI ISC; usable but not real-time
  - economic impact
    - [L] EICAT impact assessments; Diagne et al. 2021 global cost database; incomplete

---

# Climate Forcing and Extreme Events

- temperature increase
  - global and regional mean surface temperature
    - [H] HadCRUT5; NOAA GHCN; Berkeley Earth; NASA GISTEMP; ERA5 reanalysis (monthly, near real-time)
  - species-specific thermal tolerance exceedance
    - [L] Species-specific research literature; no operational global database
  - altered precipitation patterns
    - [H] NOAA GHCN-Daily; ERA5; GPCP; GPM
- extreme weather events
  - frequency and damage
    - [H] EM-DAT (CRED, free, 1900-present); NOAA Storm Events; [M] Munich Re NatCatSERVICE (paid)
  - storm surge intensity
    - [M] NOAA SLOSH model; JRC Global Flood Database; hindcast available, real-time monitoring limited
  - flood and drought cycle trends
    - [H] EM-DAT event counts; SPEI/PDSI indices; ERA5 climate indices
- atmospheric greenhouse gas concentrations
  - CO2 (current: ~425 ppm, vs ~385 ppm at time of article)
    - [H] NOAA ESRL Mauna Loa (daily); OCO-2/3 satellites (column CO2, monthly); AGAGE network
  - CH4, N2O, F-gases
    - [H] NOAA GML; AGAGE network; GOSAT satellite; updated monthly
  - total carbon stocks (atmosphere, terrestrial, ocean)
    - [H] Global Carbon Project annual budget (published each November); IPCC AR6 tables

---

# Ecosystem Services (TEEB Classification)

- provisioning
  - food: fisheries
    - [H] FAO FishStat (annual national catch); Sea Around Us (reconstructed)
  - food: agriculture and wild harvest
    - [H] FAOSTAT (crop production, annual, country-level)
  - fresh water (access and supply)
    - [H] WHO/UNICEF JMP (drinking water access); AQUASTAT (withdrawal and availability)
  - wood and fiber
    - [H] FAO Global Forest Products database; FAOSTAT forestry domain
  - genetic resources
    - [L] Genesys; GBIF; incomplete and non-standardized globally
- regulating
  - climate regulation (carbon sequestration and storage)
    - [H] Global Carbon Project; GFW carbon flux model; directly quantifiable
  - flood regulation (wetlands, floodplains)
    - [L] Modeled via InVEST or similar; no direct global measurement of service delivery
  - disease regulation (clean water, vector habitat control)
    - [L] WHO vector disease databases; ecosystem linkage not directly measured at global scale
  - water purification
    - [L] GEMS-Water; patchy; ecosystem service attribution requires local modeling
  - erosion regulation
    - [M] RUSLE global models (EU JRC ESDAC); modeled but widely used and accepted
  - storm protection (mangroves, reefs as coastal shields)
    - [M] Can be modeled from mangrove/reef extent + historical storm track data (NOAA IBTrACS)
- habitat and supporting
  - soil formation and nutrient cycling
    - [L] ISRIC World Soil Information; FAO; mostly static inventories, not dynamic monitoring
  - life cycle maintenance (nursery habitat)
    - [L] Mangrove and reef extent as proxies; direct nursery function not globally monitored
  - gene pool protection
    - [L] As above under biodiversity
  - primary production (basis of all food chains)
    - [H] MODIS NPP (MOD17, monthly, global); Copernicus BioPAR; directly usable
- cultural (non-quantifiable in standard datasets)
  - recreation and tourism revenue
    - [M] UNWTO statistics; national park visitor data; ecosystem-specific attribution requires local study
  - aesthetic values
    - [X] No standardized quantitative global dataset
  - spiritual and religious values
    - [X] No standardized quantitative global dataset
  - indigenous and local community identity
    - [X] No standardized quantitative global dataset

---

# Human Systems (Interacting with Ecological Systems)

- infrastructure
  - climate damage costs (UNFCCC: US$2-41B/yr; EACC: US$13.5-29.5B/yr)
    - [M] EM-DAT (free, event-based); World Bank GFDRR risk data; complete for major events only
  - flood and storm vulnerability mapping
    - [M] World Risk Index; UNDRR country risk profiles; World Bank FATHOM flood layers
- health care
  - waterborne disease burden
    - [M] WHO Global Health Observatory; flooding attribution requires epidemiological modeling
  - heat-related mortality
    - [M] Lancet Countdown (annual tracking report); WHO; improving but still modeled
  - vector-borne disease range expansion
    - [M] WHO disease surveillance; ECDC for Europe; global range shift modeled via climate projections
- agriculture, forestry, fisheries
  - current production
    - [H] FAOSTAT (annual, country-level, all three sectors)
  - yield loss under climate scenarios
    - [M] Crop model studies (GAEZ+, DSSAT, GLAM); not operational real-time data
- coastal zone management
  - adaptation costs
    - [L] World Bank country studies; OECD; highly fragmented, no unified global product
- water supply and flood protection
  - access to safe water
    - [H] WHO/UNICEF JMP (annual, country-level)
  - supply adequacy under climate stress
    - [M] AQUASTAT + WRI Aqueduct water risk atlas
- energy production
  - electricity generation mix
    - [H] IEA; EIA; IRENA (annual, country-level)
  - hydropower vulnerability to river flow change
    - [M] Modeled from GRDC streamflow data + installed capacity (IRENA); not operational
- transport
  - climate damage to roads, ports, rail
    - [L] Fragmented national inventories; no global operational dataset; EM-DAT captures only major events
- financial institutions and insurance
  - insured losses
    - [M] Swiss Re Sigma (annual, free summary); Munich Re NatCatSERVICE (paid for detail)
  - adaptation finance flows
    - [M] OECD DAC climate-related development finance tracking (annual); methodology disputed
- indigenous and local community structures
  - climate displacement
    - [L] UNHCR; Internal Displacement Monitoring Centre (IDMC); climate attribution limited and contested
  - livelihood loss tied to ecosystem degradation
    - [X] No operational global dataset; case studies only

---

# Danube Basin

Reference: WWF Adaptation Case Study (Pittock, ed. "Water for Life", WWF-UK, 2008); ICPDR (International Commission for the Protection of the Danube River)

## Countries

The Danube Basin spans 19 countries across central and eastern Europe (per ICPDR basin delineation), divided into mainstream riparian states and catchment area nations.

### Mainstream Countries (10)

Countries through which the main Danube channel flows directly:

1. Germany (Bavaria; upper Danube headwaters)
2. Austria (upper Danube corridor, Vienna)
3. Slovakia (main channel, Bratislava)
4. Hungary (middle Danube, Budapest)
5. Croatia (Danube forms border section; Drava and Sava confluences)
6. Serbia (middle and lower Danube; Iron Gate gorge)
7. Bulgaria (lower Danube; right bank shared with Romania)
8. Romania (lower Danube; Danube Delta)
9. Moldova (Prut tributary confluence, lower basin margin)
10. Ukraine (Danube Delta north; Prut and Tisza headwaters)

### Catchment Area Nations (9)

Countries with significant basin territory draining into the Danube via tributaries, but not on the main channel:

1. Switzerland (Rhine-Danube watershed; Inn tributary headwaters)
2. Italy (Adige and Piave headwaters in eastern Alps)
3. Czech Republic (Morava and Thaya tributaries)
4. Slovenia (Sava tributary headwaters)
5. Bosnia and Herzegovina (Sava and Neretva tributary basins)
6. Montenegro (Drina tributary headwaters)
7. North Macedonia (Vardar and Morava tributary basins)
8. Poland (Vistula-San watershed margin; upper Tisza tributaries)
9. Albania (Drin tributary; marginal basin contribution)

---

## Ecosystem Services

Categories:
  [N] = Natural: ecological process; no human management required to produce the service
  [H] = Human: infrastructure or activity delivers the service, using nature as substrate
  paired: entries marked "paired with [X]" are the split halves of a formerly mixed service

Data availability ratings (inline):
  [data:H] = High: publicly available, regularly updated, usable immediately
  [data:M] = Medium: available but modeled, infrequent, or requires processing
  [data:L] = Low: sparse, regional, estimated, or paywalled
  [data:X] = None: no standardized global dataset exists

---

### Natural Services

**Provisioning**

- fish population (the stock itself)
  - paired with: fisheries extraction and management (see Human)
  - self-regenerating; Danube sturgeon (6 species, IUCN Red List)
  - [data:L] no current operational stock assessment; WWF Danube-Carpathian Programme tracking

- wild food and fodder availability (the resource itself)
  - [data:L] subsistence-scale; no unified basin dataset

- reed bed (natural regeneration and extent)
  - paired with: reed harvesting operations (see Human)
  - largest reed bed in Europe (~1,800 km2, Danube Delta)
  - [data:H] extent via Copernicus land cover

- freshwater availability (hydrological cycle output)
  - paired with: freshwater supply infrastructure (see Human)
  - supports ~81 million people across the basin
  - [data:H] AQUASTAT; ERA5 reanalysis

- river flow and groundwater (natural water source for agriculture)
  - paired with: irrigation distribution infrastructure (see Human)
  - [data:M] GRACE-FO; GRDC; national hydrological services

- floodplain forest growth and biomass
  - paired with: floodplain forestry and timber harvesting (see Human)
  - riparian softwood and hardwood; carbon accumulation; soil binding
  - [data:M] Copernicus/ESA CCI extent; FAO national forestry statistics

**Regulating**

- flood regulation by wetlands and floodplains
  - restored floodplain retention: 2,236 km2 pledged (Pittock/WWF 2008); US$140 million/year in services
  - [data:H] EM-DAT; ICPDR flood risk maps (2021); JRC Global Flood Database
  - [data:M] retention capacity modeled via InVEST or HEC-RAS

- water purification by wetland filtration
  - nitrogen and phosphorus load monitored by ICPDR (annual Joint Danube Survey)
  - [data:M] filtration efficiency modeled, not measured directly

- carbon sequestration (floodplain forests, delta wetlands, peatlands)
  - Danube Delta reed beds and sediment hold significant blue carbon
  - [data:M] national GHG inventories (LULUCF); EU LULUCF reporting; Global Carbon Project

- erosion and sediment regulation
  - significantly disrupted by Iron Gate I and II dams; sediment deficit to delta well-documented
  - [data:M] ICPDR sediment balance monitoring; GRDC; national hydrological services

- groundwater recharge
  - floodplain aquifer recharge
  - [data:M] GRACE-FO (basin scale); Austria and Hungary best-documented nationally

- local climate regulation (evapotranspiration, cooling)
  - [data:M] ERA5 reanalysis; GLEAM evapotranspiration; floodplain-specific effect modeled

**Habitat and Supporting**

- Danube Delta biodiversity and habitat (UNESCO World Heritage, Ramsar Wetland)
  - [data:H] extent and land cover: Copernicus; Ramsar Information Sheet; INCDDD (Romania)
  - [data:H] bird species: >320 species; BirdLife IBA database; EBCC breeding bird surveys
  - [data:M] fish diversity: >100 species; ICPDR Joint Danube Survey (every 6 years)

- migratory bird habitat
  - [data:H] BirdLife IBA data; Wetlands International waterbird census; EBCC pan-European monitoring

- sturgeon spawning habitat
  - severely degraded by Iron Gate dams
  - [data:L] current functional habitat poorly monitored; WWF Sturgeon Initiative tracking

- floodplain forest habitat (gallery forest, riparian woodland)
  - [data:M] Copernicus/ESA CCI extent; Natura 2000 condition reporting (EU members only; Serbia, Bosnia, Moldova less complete)

- nutrient cycling (floodplain-river exchange)
  - [data:M] ICPDR nutrient monitoring; modeled fluxes; not operational real-time

- primary production (photosynthesis, biomass)
  - [data:H] MODIS NPP (MOD17, monthly); Copernicus BioPAR

**Cultural**

- natural landscape (the asset underlying all cultural services)
  - paired with: ecotourism and recreation industry (see Human)
  - [data:X] no direct standardized dataset

- natural river channel (substrate for navigation)
  - paired with: commercial navigation infrastructure (see Human)
  - [data:H] GRDC streamflow; Danube Commission bathymetric surveys

---

### Human Services

**Provisioning**

- fisheries extraction and management
  - paired with: fish population (see Natural)
  - commercial and subsistence fishing (bream, carp, pike, zander); vessel fleets; processing; market distribution; quota and stock management
  - [data:M] FAO FishStat inland waters

- reed harvesting operations
  - paired with: reed bed natural regeneration (see Natural)
  - seasonal cutting, processing, commercial sale (construction, thatching, paper industry)
  - [data:M] Romanian national statistics; [data:H] reed extent via Copernicus

- floodplain forestry and timber harvesting
  - paired with: floodplain forest growth and biomass (see Natural)
  - silvicultural management, harvesting, processing, transport, sale
  - [data:M] FAO national forestry statistics; floodplain-specific breakdown requires national forest inventories

- freshwater supply infrastructure
  - paired with: freshwater availability (see Natural)
  - intake structures, treatment plants, distribution network, metering
  - [data:H] AQUASTAT; national utility statistics

- irrigation distribution infrastructure
  - paired with: river flow and groundwater (see Natural)
  - pumping stations, primary canals, farm-level delivery systems, scheduling
  - [data:H] AQUASTAT irrigation water withdrawal by country; FAO

**Regulating**

- flood embankments and engineered water management
  - human substitute for natural floodplain flood regulation
  - Sundarbans comparison: US$294M capital + US$6M/year maintenance vs. US$140M/year natural floodplain service
  - [data:M] World Bank GFDRR; national infrastructure registries; EU Floods Directive reporting

**Cultural**

- ecotourism and recreation industry
  - paired with: natural landscape (see Natural)
  - accommodation, guiding, transport, marketing, booking infrastructure; Danube Delta, EuroVelo 6, birdwatching, angling
  - [data:M] Romanian national tourism statistics; WWF estimates; no unified basin product
  - [data:L] cycling and angling visitor numbers tracked nationally; basin-level synthesis absent

- commercial navigation infrastructure (locks, dredging, ports, fleet)
  - paired with: natural river channel (see Natural)
  - Europe's second longest navigable river; freight, passenger, logistics chain
  - [data:H] Danube Commission annual freight statistics; directly quantifiable

- cultural heritage management and tourism infrastructure
  - conservation of historical settlements, archaeological sites, UNESCO designations; visitor infrastructure
  - [data:X] no standardized quantitative ecosystem service dataset; UNESCO heritage sites documented

- spiritual and subsistence values for riparian communities
  - the cultural relationship of communities with the river system; indigenous and local practices
  - [data:X] no standardized global dataset; ethnographic literature only
