---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 10.5
  maturity-market-value: 27.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.18, confidence: 0.65}
      data-scale-advantage: {score: 0.48, confidence: 0.50}
      brand-reputation: {score: 0.70, confidence: 0.60}
      capital-intensity: {score: 0.55, confidence: 0.60}
      scale-economies: {score: 0.52, confidence: 0.55}
      regulatory-barriers: {score: 0.65, confidence: 0.70}
      switching-costs: {score: 0.62, confidence: 0.60}
  override:
    s1: 0.13
    r: 0.82
    reason: "The announced Thales-Exail combination is likely to create a larger 2036 leader than the pooled trait model predicts, while sovereign procurement, application-specific engineering, and a deep specialist tail keep the overall market fragmented."
  model-estimate:
    s1: 0.107313
    r: 0.871744
  hhi: 0.051587
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: Kongsberg Gruppen
        ticker: KOG.OL
        share: 0.060
      - rank: 2
        name: Teledyne Technologies
        ticker: TDY
        share: 0.058
      - rank: 3
        name: Thales
        ticker: HO.PA
        share: 0.050
      - rank: 4
        name: Saab
        ticker: SAAB-B.ST
        share: 0.040
      - rank: 5
        name: Exail Technologies
        ticker: EXA.PA
        share: 0.036
  override:
    - name: Thales
      ticker: HO.PA
      capture: 0.13
      reason: "Thales signed a binding agreement in July 2026 to acquire the Gorgé family's Exail stake and plans a tender for 100%; the expected 2027-28 closing should consolidate most Exail revenue into Thales well before 2036."
    - name: Exail Technologies
      ticker: EXA.PA
      capture: 0.0
      reason: "The announced Thales transaction is expected to eliminate Exail as a separately controlled vendor by 2028; its economic contribution is included in the Thales override."
  model-estimate:
    - rank: 1
      name: Kongsberg Gruppen
      ticker: KOG.OL
      hold-position-capture: 0.13
      mobility-adjusted-capture: 0.098786
      mobility-adjusted-revenue: 2.667222
    - rank: 2
      name: Teledyne Technologies
      ticker: TDY
      hold-position-capture: 0.1066
      mobility-adjusted-capture: 0.082325
      mobility-adjusted-revenue: 2.222775
    - rank: 3
      name: Thales
      ticker: HO.PA
      hold-position-capture: 0.087412
      mobility-adjusted-capture: 0.069137
      mobility-adjusted-revenue: 1.866699
    - rank: 4
      name: Saab
      ticker: SAAB-B.ST
      hold-position-capture: 0.071678
      mobility-adjusted-capture: 0.054222
      mobility-adjusted-revenue: 1.463994
    - rank: 5
      name: Exail Technologies
      ticker: EXA.PA
      hold-position-capture: 0.058776
      mobility-adjusted-capture: 0.042504
      mobility-adjusted-revenue: 1.147608
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---
# Global Underwater Robotics and Sonar

## Market Definition

**Market scope.** This is the global market for underwater robotic platforms and the acoustic sensing stack used to navigate, map, inspect, monitor, communicate, detect and intervene below the waterline. It includes autonomous underwater vehicles (AUVs), remotely operated vehicles (ROVs), underwater gliders and resident/hybrid systems; standalone and integrated active, passive, multibeam, side-scan and synthetic-aperture sonar; acoustic positioning and communications; mission software; first-party integration, maintenance, training and lifecycle support. Included customers are defence, offshore energy, subsea infrastructure, hydrography, ocean science, aquaculture and search/salvage. It excludes unmanned surface vessels except revenue for an included underwater payload, manned submarines and surface ships, weapons and expendable effectors, generic cameras/connectors/components sold outside an included system, offshore construction vessels, customer labour, and subsea production hardware.

**Revenue boundary.** Market value is annual revenue recognized by platform and sonar/acoustic-system vendors at the first arm's-length sale, plus their recognized software, integration and lifecycle-service revenue. It excludes shipyard revenue, prime-contract value attributable to ships or weapons, distributor markup, customer operating expenditure, offshore project GMV and duplicated component revenue. A sonar carried on an AUV is counted once: inside the robotic-system category when bundled by the vehicle OEM, or in the sonar category when sold separately, never both.

**Addressable unit and penetration.** The stable denominator is one active underwater mission system, host platform or monitored subsea site that can structurally use a qualifying robotic platform or sonar/acoustic suite. Penetration is conceptually a `stock` measure: eligible systems/sites with at least one qualifying robotic or advanced acoustic system divided by all eligible systems/sites. Billable units are annual vehicle and sonar-system deliveries, host retrofits and active installed systems receiving vendor software or support. Defence, offshore/infrastructure and science/commercial applications are modeled separately and aggregated at the vendor-revenue boundary.

**Time and value basis.** The base year is 2026 and the fixed horizon is 2036. Values are nominal USD. The contract is deliberately narrower than naval-modernization budgets and offshore inspection spending, but broader than reports covering only AUV/ROV hardware. A single logistic penetration fit is not configured because no attributable global series measures this mixed stock denominator consistently across vehicles, ship/submarine sonar, fixed seabed arrays and commercial sites.

## Current View

The expected 2026 market value is **$10.5B**. The anchor is a union, not a sum, of two overlapping published categories. Market Research Future puts underwater robotics at $5.44B in 2025 and MarketsandMarkets puts sonar systems at $5.70B. Rolling each category into 2026 and removing about $1.7B of sonar arrays, navigation and acoustic equipment already embedded in robotic-platform bundles produces approximately **$6.0B of robotic platforms and lifecycle revenue plus $4.5B of non-duplicated sonar/acoustic revenue**. The overlap is the least certain part of the current estimate; a plausible 2026 range is roughly $8.5B-$12.5B.

Supplier disclosures support the order of magnitude but do not report this exact contract. Teledyne reported **$680.1M** of 2025 Marine Instrumentation sales, covering underwater sensors, acoustic imaging, vehicles and interconnects, some of which sits outside the boundary. Kongsberg Discovery reported **NOK5.13B** (about $0.50B) of 2025 revenue across sonars, underwater communications/positioning and autonomous platforms alongside adjacent marine products; Kongsberg Defence & Aerospace also sells naval sonar. Exail reported **€373M** (about $0.42B) from Navigation and Maritime Robotics, including some surface-drone and non-underwater navigation revenue. These disclosures make low-to-mid-single-digit whole-market shares for the leaders more defensible than the double-digit shares implied by narrower product reports.

The reference case is **$27B in 2036**, a 9.9% annual increase from 2026. A plausible range is **$18B-$38B**. The downside combines delayed autonomous reliability, defence-program slippage and offshore-energy weakness; the upside requires fleets of resident systems, broad unmanned mine-countermeasure/anti-submarine deployment, and higher software/service attachment without severe hardware price deflation.

## Adoption Path

Robotic platforms grow faster than conventional sonar because autonomy lowers vessel and crew requirements, enables persistent coverage and creates new resident-inspection and distributed-defence use cases. ROVs remain important for manipulation, while AUVs, gliders and hybrid systems take a larger share of survey, monitoring and mine-countermeasure work. Sonar grows more slowly from a mature installed base, but array density, synthetic-aperture imaging, AI-assisted classification and more unmanned host platforms lift content per mission.

The sizing model uses project/installed-base revenue bridges rather than a false-precision global unit count. Indexed activity makes the assumptions explicit while direct category forecasts anchor dollars.

| Underwater robotics driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Eligible underwater mission systems/sites | 100 | 135 | More offshore assets, subsea cables, naval missions and monitored sites |
| Adoption/intensity per eligible system | 100 | 175 | More autonomous, persistent and multi-vehicle use |
| Annual billable platform/service activity | 100 | 236 | Addressable-base growth times adoption/intensity |
| Net vendor revenue per billable unit | 100 | 127 | Higher autonomy/software mix and nominal inflation, partly offset by hardware learning |
| **Annual market value** | **$6.0B** | **$18.0B** | Activity index times revenue intensity |

| Non-duplicated sonar/acoustic driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Eligible host platforms/sites | 100 | 125 | Naval fleet modernization, seabed monitoring and commercial/science hosts |
| Advanced acoustic content/adoption | 100 | 145 | Denser arrays, better imaging, communications and unmanned-host payloads |
| Annual billable system/support activity | 100 | 181 | Host growth times content/adoption |
| Net vendor revenue per billable unit | 100 | 110 | Nominal price/mix uplift with component deflation and procurement pressure |
| **Annual market value** | **$4.5B** | **$9.0B** | Excludes sonar already counted inside robotic systems |

The 2036 market is therefore **$18B robotics plus $9B non-duplicated sonar/acoustics**. Initial and replacement equipment still dominates, but mission software, data products and lifecycle support should become a materially larger recurring stream. The largest sensitivities are autonomous mission reliability, naval procurement conversion, offshore capex, the overlap deduction and how much productivity value vendors retain in price rather than pass through to customers.

## Market Structure

Direct network effects are weak: one navy or offshore operator gains little merely because another buys the same vehicle. Data scale is more meaningful because mission hours improve autonomy, classification and digital twins, but classified, customer-owned and geographically specific data limits a global flywheel. Reputation is strong in safety- and mission-critical procurement. Capital needs, pressure-rated manufacturing, long qualification cycles and export/security controls deter casual entry, while integration with host platforms, operator training, spares and mission data create switching friction. Scale economies exist in R&D, electronics purchasing and fleet software, but bespoke payloads and sovereign sourcing let specialists survive.

Those inputs produce an unadjusted pooled-model leader share of **10.7%**, rank-decay ratio of `0.872` and HHI of about `0.048`. The canonical override incorporates the announced Thales-Exail combination: a **13% leader share** and `0.82` rank-decay ratio imply an HHI of **0.0516**, or roughly 19 effective competitors. The result is still fragmented because the contract spans defence and civil buyers, many countries demand sovereign suppliers, and survey ROVs, mine-countermeasure systems, submarine sonar, fisheries acoustics and compact inspection robots are not one interchangeable product.

Confidence below 0.8 is mainly irreducible today because vendors rarely disclose contract-matched revenue or win/loss data. Confidence would improve with product-line revenue splits from Kongsberg/Thales/Saab, independently measured current whole-market shares, and multi-year evidence on autonomous fleet renewals and cross-vendor switching; these are carried into *Watch*.

## Players

Kongsberg, Teledyne, Thales, Saab and Exail are the current modeled top five. Their stored shares—6.0%, 5.8%, 5.0%, 4.0% and 3.6%—are analyst allocations from disclosed marine/product-line revenue and product breadth, not reported market shares. Kongsberg combines Discovery's ocean technology with relevant naval sonar; Teledyne's Marine Instrumentation disclosure is the cleanest numerical anchor; Thales and Saab allocations rely more heavily on portfolio and contract evidence because neither isolates underwater-system revenue.

The canonical 2036 curve gives hold-position shares of **13.0% Kongsberg, 10.7% Teledyne, 8.7% Thales, 7.2% Saab and 5.9% Exail**. Applying the pooled 10-year mobility base rate lowers these to **9.9%, 8.2%, 6.9%, 5.4% and 4.3%**, corresponding to **$2.67B, $2.22B, $1.87B, $1.46B and $1.15B** of model-view 2036 revenue. The 10.1% gone probability is already embedded and is not applied again.

Two analyst overrides reflect company-specific evidence the pooled model cannot see: **Thales receives 13% canonical capture**, while **Exail receives 0% separately**, because Thales signed a binding agreement in July 2026 to buy the Gorgé family's 35.51% stake, expects closing in Q3 2027 and plans a tender for 100% by early 2028. The economic contribution of Exail's robotics, navigation and sonar portfolio is included in Thales rather than double-counted. Canonical 2036 captures are therefore **13.0% Thales, 9.9% Kongsberg, 8.2% Teledyne, 5.4% Saab and 0% standalone Exail**.

Oceaneering, General Dynamics/Bluefin, L3Harris, Atlas Elektronik, RTX, Lockheed Martin, Fugro, Forum Energy Technologies, Sonardyne, Anduril and numerous regional specialists remain credible top-five or niche leaders. In particular, new defence autonomy entrants can move faster than the installed naval-sonar incumbents, while service companies can monetize fleets without becoming equipment leaders.

## Watch

- Closing, remedies or failure of the Thales-Exail transaction; any forced divestiture would change both leader capture and HHI.
- Contract-matched underwater revenue or backlog splits from Kongsberg, Teledyne, Thales, Saab and Exail, including product versus service/software mix.
- U.S., European, Australian and Asian procurement converting prototype UUV, unmanned mine-countermeasure and anti-submarine programs into serial fleets.
- Resident subsea systems moving from pilots to multi-year offshore infrastructure contracts, with disclosed vehicle utilization and vessel-day savings.
- Autonomous mission success, intervention rate, endurance, navigation drift, acoustic bandwidth and battery-density progress.
- Offshore wind, oil-and-gas inspection, subsea-cable protection and ocean-science budgets versus announced project pipelines.
- Evidence that proprietary mission data creates a durable autonomy moat rather than remaining customer-owned, classified or transferable across vendors.
- Pricing and service attachment: hardware learning could expand unit adoption while compressing revenue below the reference case.

## Peer Comparison

- **6% over our estimate at the same forecast year:** Market Research Future, updated August 4, 2026, projects underwater robotics from **$5.44B in 2025 to $17.09B in 2035** at 12.1%. Our robotics component is about **$16.1B in 2035**, interpolated from $6.0B in 2026 to $18.0B in 2036. Its ROV/AUV scope is close, though its component/service treatment may include sonar that this document removes from the standalone sonar component.
- **39% over our estimate in 2035:** Roots Analysis projects underwater robotics from **$5.29B in 2025 to $22.38B in 2035** at 14%. The scope covers AUVs and ROVs across defence, commercial and research applications and is broadly comparable to the robotics component. The disagreement is mainly adoption speed; its 14% forecast assumes a faster autonomy and inspection ramp than our 11.6% component CAGR.
- **41% over our estimate in 2035, before overlap reconciliation:** MarketsandMarkets projects the total sonar-systems market from **$5.70B in 2025 to $11.80B in 2035** at 7.6%, versus our **$8.4B** non-duplicated sonar/acoustic component in 2035. Its total includes sonar payloads that this contract counts inside bundled underwater robots, so the arithmetic overstates the true disagreement.
- **4% under our estimate in 2035:** Roots Analysis projects sonar systems from **$5.31B in 2025 to $8.11B in 2035** at 3.91%, versus our non-duplicated sonar component of about $8.4B. The values are close despite a likely boundary mismatch, providing a useful lower-growth check on the more bullish MarketsandMarkets forecast.
- No credible long-term publication found reports the exact union of underwater robotic platforms and non-duplicated sonar/acoustic vendor revenue. Summing the two peer categories without an overlap deduction is not comparable to this market contract.

## Sources

- Market Research Future, *Underwater Robotics Market*, updated August 4, 2026: https://www.marketresearchfuture.com/reports/underwater-robotics-market-7605
- Roots Analysis, *Underwater Robotics Market, Till 2035*, accessed August 9, 2026: https://www.rootsanalysis.com/underwater-robotics-market
- MarketsandMarkets, *Sonar Systems Market - Global Forecast to 2035*, accessed August 9, 2026: https://www.marketsandmarkets.com/Market-Reports/sonar-systems-technology-market-142612945.html
- Roots Analysis, *Sonar Systems Market, Till 2035*, accessed August 9, 2026: https://www.rootsanalysis.com/sonar-systems-market
- Kongsberg Gruppen, *Annual Report 2025*, published 2026: https://www.kongsberg.com/globalassets/kongsberg/5.-investor-relations/4.-reports-and-presentations/annual-report/annual-report-2025/annual-report-english-2025-v2.pdf
- Teledyne Technologies, *2025 Annual Report*, published 2026: https://www.teledyne.com/en-us/investors/Documents/2025%20Teledyne%20Annual%20Report.pdf
- Exail Technologies, *FY 2025 Results Presentation*, March 18, 2026: https://www.exail-technologies.com/wp-content/uploads/2026/03/exail-technologies-fy-2025-results-presentation-1.pdf
- Thales and Exail Technologies, *Thales to acquire the Gorgé family's stake in Exail, with a view to launching a tender offer for 100% of the company*, July 6, 2026: https://www.exail-technologies.com/wp-content/uploads/formidable/4/06-july-2026-pr-thales-to-acquire-the-gorge-familys-stake-in-exail-with-a-view-to-launching-a-te.pdf
