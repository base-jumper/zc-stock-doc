---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.20
  maturity-market-value: 4.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.15, confidence: 0.75}
      data-scale-advantage: {score: 0.25, confidence: 0.55}
      brand-reputation: {score: 0.55, confidence: 0.55}
      capital-intensity: {score: 0.55, confidence: 0.75}
      scale-economies: {score: 0.80, confidence: 0.80}
      regulatory-barriers: {score: 0.65, confidence: 0.65}
      switching-costs: {score: 0.75, confidence: 0.70}
  model-estimate:
    s1: 0.190236
    r: 0.807178
  hhi: 0.103855
  method: selected-direct-ridge
  date: 2026-08-04
players:
  inputs:
    current:
      - rank: 1
        name: SolydEra
        share: 0.19
      - rank: 2
        name: Ceres Power
        ticker: CWR.L
        share: 0.17
      - rank: 3
        name: Elcogen
        share: 0.13
  model-estimate:
    - rank: 1
      name: SolydEra
      hold-position-capture: 0.190236
      mobility-adjusted-capture: 0.145153
      mobility-adjusted-revenue: 0.580612
    - rank: 2
      name: Ceres Power
      ticker: CWR.L
      hold-position-capture: 0.153554
      mobility-adjusted-capture: 0.120133
      mobility-adjusted-revenue: 0.480532
    - rank: 3
      name: Elcogen
      hold-position-capture: 0.123946
      mobility-adjusted-capture: 0.10139
      mobility-adjusted-revenue: 0.40556
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-04
---
# Global Solid Oxide Fuel Cell IP and Components

## Market Definition

**Market scope:** worldwide third-party technology used to generate power with solid oxide fuel cells (SOFCs). Included revenue is from cell and stack intellectual-property licences, technology transfer, engineering tied to a licence, per-kW royalties, and externally sold SOFC cells, stacks and hot-box or stack-array modules supplied to an OEM or system integrator. Stationary distributed power, data-centre and commercial/industrial primary or backup power, microgrids, residential micro-CHP, and maritime auxiliary power are included. Solid oxide electrolysis (SOEC), hydrogen-production equipment, fuel, catalysts and generic ceramics, complete fuel-cell power systems, balance of plant, site EPC, financing, maintenance, electricity sales, and captive components consumed inside a vertically integrated vendor's own system are excluded.

**Revenue boundary:** annual revenue recognized by the independent SOFC IP licensor or merchant cell/stack/module supplier at the first external sale to a manufacturer or system integrator. It is not end-customer system spend, project value, electricity revenue, total OEM revenue, GMV, or an imputed transfer value for captive stacks. Ceres licence fees, engineering, technology hardware and royalties are in scope only to the extent they relate to SOFC power; Elcogen and SolydEra cell, stack and module sales are in scope only when sold externally.

**Addressable unit and penetration:** the stable denominator is annual GW of new distributed or on-site firm-power capacity in applications structurally compatible with SOFCs. Penetration is `new-sales-share`: SOFC capacity as a share of that eligible annual capacity flow. Billable units are externally monetized kW covered by a technology licence or sold as cells, stacks or modules, plus discrete technology-transfer and engineering programmes. IP/licensing and physical core components are separate economic segments, aggregated at the same vendor-recognized boundary.

**Time and value basis:** base year 2026, fixed horizon 2036, worldwide geography and nominal USD. The contract is unchanged across size, concentration and player capture. Reversible products contribute only their SOFC power revenue; SOEC revenue is excluded even when both modes use the same factory or stack platform.

## Current View

The 2026 market is estimated at **US$0.20b**. Ceres is the cleanest public revenue anchor: FY2025 revenue was £32.6m (about US$43m at a rounded US$1.32/£), comprising £10.3m of technology hardware, £22.2m of engineering services and licences, and its first £0.11m of royalties. That total includes SOEC and one-off technology-transfer work, so it is a ceiling rather than a pure SOFC number. Assigning roughly three quarters to the power/licensing boundary and treating Ceres as about 17% of the merchant pool implies approximately US$0.19b.

The supply-side cross-check supports a small but commercial market. Doosan began production in July 2025 at a Ceres-licensed 50MW-per-year factory; Ceres had four announced stack manufacturing licensees by year-end. Elcogen opened a 360MW combined SOFC/SOEC cell, stack and module facility in 2025 after operating at 10MW, while SolydEra describes itself as Europe's largest solid-oxide stack manufacturer and has supplied stacks to HnPower since 2019. These capacity disclosures are not revenue and mix SOFC with SOEC, but they show that the external core-technology layer is moving from pilot tens of MW toward hundreds of MW.

Published SOFC reports place the much broader 2025-26 system/component market between roughly US$0.91b and US$2.98b. Applying an 8-20% external IP/core-component revenue slice produces a US$0.07-0.60b diagnostic range. The stored US$0.20b sits toward the low end because it excludes complete systems, captive stacks and SOEC. Confidence is low: no participant or analyst publishes an audited market total on this exact boundary.

## Adoption Path

The expected 2036 market is **US$4.0b**, a 34.9% ten-year CAGR. The bridge assumes eligible on-site and distributed firm-power additions roughly double, SOFC new-sales share rises from about 1.5% to 24%, and external licensing/merchant components take a larger share of the core technology layer as industrial OEMs adopt partner or specialist platforms. Billable external capacity therefore rises from about 0.19GW to 18GW. Net vendor revenue falls from roughly US$1,050/kW to US$220/kW as automated mass manufacture, learning and royalty-heavy licensing reduce recognized revenue intensity; Elcogen's factory plan explicitly targets a 60% cost reduction, providing a useful directional check.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Eligible distributed/on-site firm-power additions | about 50GW | about 110GW | Data centres, C&I, microgrids, residential CHP and maritime auxiliary power |
| SOFC new-sales share | about 1.5% | about 24% | Adoption assumption; complete SOFC system capacity, not stored revenue |
| SOFC adopted annual capacity | about 0.75GW | about 26GW | Denominator multiplied by new-sales share |
| Externally licensed or merchant core share | about 25% | about 70% | Excludes captive vertically integrated stacks |
| Billable external capacity | about 0.19GW | about 18GW | Royalty-bearing or externally sold cells, stacks and modules |
| Net recognized revenue per billable kW | about US$1,050 | about US$220 | Licence, engineering, royalty and component mix; nominal USD |
| Annual market value | **US$0.20b** | **US$4.0b** | Reconciles to front matter after rounding |

There is no installed-base replacement calculation because the contract measures annual new-sales capacity and associated licence/component revenue. The downside is about US$1.3b if SOFC remains a niche behind gas engines, turbines, batteries and grid upgrades, captive technology dominates, and cost reduction flows mostly to customers. The reference case is US$4.0b. The upside is about US$8.0b if data-centre time-to-power demand drives multi-GW deployment, SOFC approaches Ceres' 22GW 2030 opportunity sooner, and licensing becomes the standard route for industrial OEM entry. The largest sensitivities are SOFC capacity adoption, the merchant-versus-captive share, and recognized revenue per kW. A deterministic penetration curve is not configured because no boundary-consistent historical annual capacity-share series with at least four observations was found.

## Market Structure

Direct network effects are weak: one user's stack does not become more useful because another user adopts it. Operating data and field feedback improve durability and manufacturing yield, but they are fragmented across licensees and do not create a strong global data flywheel. Reputation matters because OEMs and end customers underwrite safety, degradation, uptime and long asset lives. Entry needs specialized ceramic/metal processing, test equipment and manufacturing capital, but Elcogen's roughly €50m 360MW facility shows a meaningful rather than billion-dollar ticket.

Scale is the strongest concentrator. Automated production, shared R&D, yield learning, common tooling and purchasing spread across more kW; Elcogen expects its new plant to cut cost by 60%. IP and know-how are material barriers: Ceres reports more than 150 patent families plus trade secrets and manufacturing knowledge. Switching costs are also high after a partner tools a factory, validates a stack, designs thermal and control systems around it, and certifies a product. Those costs protect several installed platforms rather than necessarily creating one monopoly.

The structural-trait model produces a 19.02% horizon leader and 0.807 rank decay, leaving a long tail. The script-derived **0.103855 HHI** is equivalent to about 9.6 effective competitors and is consistent with a fragmented-to-moderately-concentrated specialist market. No override is used. Concentration could rise if one platform becomes the preferred standard for data-centre OEMs or if scale-driven cost gaps force consolidation. It would fall if regional certification, fuel choice, form factor and application requirements sustain separate local specialists or if large OEMs internalize the technology.

## Players

No boundary-matched current share table was found. The current ranking is therefore an analyst estimate based on externally sold product scope, disclosed revenue/capacity, manufacturing claims and licensing reach: SolydEra 19%, Ceres Power 17% and Elcogen 13%, leaving 51% for Kyocera, Niterra, Convion, WATT Fuel Cell and other stack, module, materials and engineering specialists. Vertically integrated system vendors such as Bloom Energy, Doosan Fuel Cell, Mitsubishi Power and Aisin are not ranked unless they recognize an external sale at the defined IP/component boundary.

SolydEra is ranked first because it describes itself as Europe's largest solid-oxide stack manufacturer, sells stacks and modules and has multi-year external supply relationships. Ceres is second on the strength of FY2025 boundary-adjacent revenue, four announced manufacturing licensees, more than 150 patent families and first Doosan royalties, though SOEC and milestone revenue make the 17% estimate imprecise. Elcogen is third: its existing revenue is undisclosed, but the move from 10MW to 360MW capacity and a customer base spanning 30 countries make it the clearest scaling challenger. The pooled mobility model will be used as a base rate only; it does not see Ceres' partner momentum, Elcogen's utilization ramp or private-company financing risk.

At the 2036 concentration curve, hold-position capture is 19.02% for rank one, 15.36% for rank two and 12.39% for rank three. The pooled mobility model lowers SolydEra to **14.52%** expected capture (US$0.581b), Ceres Power to **12.01%** (US$0.481b), and Elcogen to **10.14%** (US$0.406b). The 10.06% gone probability is already included and must not be applied again. These are coarse base rates, not company-specific forecasts; the long modeled tail preserves room for current specialists and new entrants.

## Watch

- Doosan sell-through and the size of Ceres royalties after its 50MW factory's first commercial year.
- Delta's planned SOFC factory start, Weichai's China factory timetable, and any per-kW economics disclosed by Ceres.
- Elcogen's actual SOFC versus SOEC utilization at the 360MW ELCO I plant and evidence that the claimed 60% cost reduction reaches volume output.
- SolydEra external stack/module shipments, customer concentration and any expansion beyond current European capacity.
- SOFC data-centre deployments versus gas turbines, engines, batteries plus grid, and Bloom's vertically integrated systems.
- A boundary-matched merchant cell/stack/module revenue or shipment-share dataset; current player shares are the weakest input.

## Peer Comparison

**About 1,650% above our 2030 estimate, but not boundary-comparable:** MarketsandMarkets, accessed 3 August 2026, forecasts the global SOFC market from US$2.98b in 2025 to **US$11.61b in 2030**, a 31.2% CAGR. Our interpolated 2030 external IP/component estimate is US$0.663b. The peer includes stacks, balance of plant, stationary, transport and portable applications and appears to measure a broad product/system revenue pool; this document excludes complete systems, balance of plant, captive stacks and SOEC. Its growth rate is close to our 34.9%, supporting rapid category growth, while the level mainly illustrates the boundary difference.

**About 6.6% under our 2035 estimate despite a broader boundary:** Business Research Insights, accessed 3 August 2026, projects the global SOFC market from US$0.91b in 2026 to **US$2.77b in 2035**, a 13% CAGR. Our interpolated 2035 merchant IP/component estimate is US$2.96b. The peer includes stationary, transportation and portable/military SOFC products, so its lower endpoint is not directly comparable and is a warning that our reference case requires a much faster commercialization path than this conservative industry forecast.

**About 86% under Ceres' 2030 physical opportunity, not a revenue comparison:** Ceres' 2025 annual report cites house analysis based on BloombergNEF data that the global SOFC power opportunity could be **22GW in 2030**. Geometric interpolation of this document's physical bridge gives about 3.1GW of SOFC annual capacity in 2030. Ceres describes an addressable opportunity rather than expected shipments, and it covers system capacity rather than external IP/component revenue. The gap therefore reflects deliberately slower adoption, not a direct forecast disagreement.

No independent 5-10 year forecast was found for the exact third-party SOFC-power licence, royalty, cell, stack and module revenue boundary. The stored US$4.0b estimate remains low confidence; the broad peer range and the 22GW opportunity chiefly constrain the ceiling and adoption speed.

## Sources

- Ceres Power, *Annual Report 2025*, published 14 April 2026: FY2025 revenue mix, first royalties, four manufacturing licensees, 22GW 2030 SOFC opportunity, business model and patent portfolio: https://www.ceres.tech/media/lponbtjc/ceres_annual-report_2025.pdf
- Ceres Power and Doosan Fuel Cell, “Doosan Fuel Cell begins mass production of fuel cell power systems using Ceres technology,” 28 July 2025: 50MW annual factory capacity and product scope: https://www.ceres.tech/media/1ppfrodd/external_ceres-power-doosan-sop-announcement-20250728-final.pdf
- Elcogen, “Elcogen launches new high-volume solid oxide fuel cell factory in Europe,” accessed 3 August 2026: 10MW-to-360MW capacity expansion, €50m investment and cells/stacks/modules boundary: https://elcogen.com/elcogen-launches-new-high-volume-solid-oxide-fuel-cell-factory-in-europe-to-meet-global-demand-for-clean-energy-solutions/
- Elcogen, “Elcogen's new production facility to expand manufacturing capacity to 360 MW,” accessed 3 August 2026: planned automation and 60% cost reduction: https://elcogen.com/elcogens-new-production-facility-to-expand-manufacturing-capacity-to-360-mw/
- SolydEra, company and product overview, accessed 3 August 2026: stacks/modules, external SOFC supply and claim as Europe's largest solid-oxide stack manufacturer: https://www.solydera.com/
- MarketsandMarkets, *Solid Oxide Fuel Cell Market*, accessed 3 August 2026: broad system/component market of US$2.98b in 2025 and US$11.61b in 2030: https://www.marketsandmarkets.com/Market-Reports/solid-oxide-fuel-cell-market-39365796.html
- Business Research Insights, *Solid Oxide Fuel Cell (SOFC) Market Size & Global Report*, accessed 3 August 2026: broad market of US$0.91b in 2026 and US$2.77b in 2035: https://www.businessresearchinsights.com/market-reports/solid-oxide-fuel-cell-sofc-market-120341
