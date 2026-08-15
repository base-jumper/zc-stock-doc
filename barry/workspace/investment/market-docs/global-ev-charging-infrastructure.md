---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 60.0
  maturity-market-value: 340.0
penetration:
  inputs:
    target-series: data/global-ev-charging-infrastructure/penetration.csv
    measure: stock
    ceiling: 0.85
    analogs:
      - us-smartphones
      - us-home-computer
      - us-cable-tv
      - us-dishwashers
    w-fit: 0.5
  override:
    L: 0.85
    t0: 2038.593261216
    k: 0.1978277434
    reason: "Anchors 2026 stock penetration at 6.5% and 2035 at 28%, consistent with IEA 2026 current-policy EV-stock and charger trajectories; the analog blend over-extrapolates the China-heavy early ramp."
  model-estimate:
    L: 0.85
    t0: 2035.755303
    k: 0.279847
  method: logistic-blend
  date: 2026-08-03
concentration:
  inputs:
    traits:
      network-effects: {score: 0.10, confidence: 0.80}
      data-scale-advantage: {score: 0.20, confidence: 0.65}
      brand-reputation: {score: 0.40, confidence: 0.65}
      capital-intensity: {score: 0.45, confidence: 0.70}
      scale-economies: {score: 0.55, confidence: 0.75}
      regulatory-barriers: {score: 0.35, confidence: 0.80}
      switching-costs: {score: 0.45, confidence: 0.70}
  model-estimate:
    s1: 0.124292
    r: 0.845753
  hhi: 0.054262
  method: selected-direct-ridge
  date: 2026-08-03
players:
  inputs:
    current:
      - rank: 1
        name: StarCharge
        share: 0.065
      - rank: 2
        name: TELD New Energy
        share: 0.055
      - rank: 3
        name: ABB E-mobility
        ticker: ABB
        share: 0.045
      - rank: 4
        name: Delta Electronics
        ticker: 2308.TW
        share: 0.035
      - rank: 5
        name: ChargePoint
        ticker: CHPT
        share: 0.030
  model-estimate:
    - rank: 1
      name: StarCharge
      hold-position-capture: 0.124292
      mobility-adjusted-capture: 0.098574
      mobility-adjusted-revenue: 33.51516
    - rank: 2
      name: TELD New Energy
      hold-position-capture: 0.10512
      mobility-adjusted-capture: 0.084949
      mobility-adjusted-revenue: 28.88266
    - rank: 3
      name: ABB E-mobility
      ticker: ABB
      hold-position-capture: 0.088906
      mobility-adjusted-capture: 0.071872
      mobility-adjusted-revenue: 24.43648
    - rank: 4
      name: Delta Electronics
      ticker: 2308.TW
      hold-position-capture: 0.075192
      mobility-adjusted-capture: 0.057817
      mobility-adjusted-revenue: 19.65778
    - rank: 5
      name: ChargePoint
      ticker: CHPT
      hold-position-capture: 0.063594
      mobility-adjusted-capture: 0.046712
      mobility-adjusted-revenue: 15.88208
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-03
---

# Global EV Charging Infrastructure

## Market Definition

**Market scope.** Global electric-vehicle supply equipment (EVSE) for light- and heavy-duty road vehicles: AC and DC charging hardware sold for residential, workplace, fleet/depot and public use, plus charger-management software and vendor service tied to that equipment. It excludes electricity sold through chargers, charge-point-operator energy margins, vehicle-to-grid electricity-market revenue, land, grid reinforcement, civil works and third-party electrical installation. Battery swapping is excluded because it is a different asset and revenue model.

**Revenue boundary.** Annual recognized revenue of EVSE manufacturers and their directly attached charger-management software/service, measured at the vendor sale or subscription. Customer project spend, government funding, charger-network GMV and charging-session electricity revenue are not market value here.

**Addressable unit and penetration.** The addressable denominator is the global light-duty vehicle fleet that could structurally become electric; the numerator is electric LDVs in operation, so penetration is a `stock` measure. The target history uses IEA electric-car/LDV stock and an approximately 1.45 billion passenger-car fleet in 2024, grown around 1.8% annually between observations. The 2024 point is directly cross-checked to IEA's statement that almost 58 million electric cars were about 4% of the passenger-car fleet. The 2026 point is an analyst estimate based on IEA's 76 million 2025 electric-LDV stock and 2026 sales trajectory, not a completed-year observation. This vehicle-stock adoption curve is a demand handoff, not a count of chargers.

**Billable units and segments.** Billable units are annual EVSE shipments/new installations, replacement units and managed charger-years. The size bridge separates (1) private LDV AC equipment, (2) public LDV slow equipment, (3) public LDV fast/ultra-fast equipment, (4) fleet/depot and public HDV equipment, and (5) attached software/service. Segment revenue is added once at vendor net realization.

**Time and value basis.** Base year 2026, fixed horizon 2036, nominal USD. Regional revenue is translated at roughly current exchange rates. The single contract is used for size, concentration and player shares.

## Current View

The expected 2026 market value is **USD 60 billion**. The strongest physical anchor is IEA's 2026 Global EV Outlook: at year-end 2025, roughly 76 million electric LDVs were supported by more than 43 million private LDV charging points and more than 7 million public points. Public stock grew more than 33% in 2025, including 4.7 million points in China; the average public connector was nearly 50 kW. The mix matters more than unit count: low-cost home AC boxes dominate units, while public fast/ultra-fast systems dominate vendor dollars.

A bottom-up 2026 reconstruction assigns roughly USD 8-10 billion to private AC units, USD 3-5 billion to public slow AC, USD 30-35 billion to public fast/ultra-fast equipment, USD 4-6 billion to HDV/depot equipment and USD 8-12 billion to attached software, warranties and vendor service. The ranges overlap around USD 60 billion after avoiding civil installation and electricity resale. As an external sense-check only, Precedence Research reports USD 59.94 billion for 2026, although its commercial-infrastructure boundary may include project elements that this contract excludes.

Evidence quality is medium. IEA's charger and EV stocks are strong, but global vendor net ASP and service attachment are not reported on a consistent basis. The present estimate is most sensitive to the public-fast share of shipments and whether third-party studies include installation.

## Adoption Path

The target series rises from about 0.7% of the global passenger-car fleet in 2020 to about 5.2% in 2025 and an estimated 6.5% in 2026. The ceiling is 85%: some remote, low-utilization and specialist vehicles should remain outside the practical LDV charging base even at long-run saturation. The analog set mixes fast consumer hardware (smartphones), a general-purpose durable (home computers), installed distribution (cable TV), and a deliberately slow home-installation anchor (dishwashers). Because the target remains below one-third of its ceiling, fit weight is capped at 0.5 to avoid extrapolating the early China-heavy ramp as if it were the mainstream global curve. The unadjusted blend reaches about 44% in 2036, above the IEA 2026 current-policy trajectory. The complete override instead anchors 2026 at 6.5%, 2035 at 28% and 2036 at about 31.8%, keeping the curve consistent with IEA's global EV-stock and charger outlook.

The size bridge is a durable installed-base ecosystem, not installed chargers multiplied by price each year. IEA projects more than 350 million LDV charger additions from 2026 through 2035 under current policies, with public chargers only 5% of the 2035 stock but about one-third of capacity coming from public fast and ultra-fast units. Public LDV capacity grows sixfold; private capacity nearly ninefold. IEA separately projects HDV charging stock growing from about 2 million in 2025 to more than 11 million in 2035.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Electric LDV fleet penetration | 6.5% | 31.8% | Global LDV stock share; selected logistic curve |
| LDV charger installed stock | about 65m | about 430m | IEA 2025 base and 2035 CPS trajectory, rolled one year |
| Annual private/slow charger shipments | about 16m | about 45m | New installations plus roughly 10-12 year replacement |
| Annual fast/ultra-fast and HDV units | about 1.0m | about 3.5m | Higher-power mix and early HDV build-out |
| Net vendor revenue per unit | segment-specific | segment-specific | Real AC price decline; higher rated-power mix offsets inflation in DC |
| Attached software/service | about USD 10bn | about USD 70bn | Managed installed base; excludes electricity resale |
| Annual market value | **USD 60bn** | **USD 340bn** | Nominal vendor revenue |

The expected 2036 value is **USD 340 billion**, an implied 18.9% CAGR. A plausible range is USD 230-520 billion. The downside combines slower EV adoption, higher charger utilization and sharper DC hardware price compression; the upside combines policy acceleration, faster heavy-duty electrification, more ultra-fast power content and higher software attachment. Public fast/ultra-fast equipment remains the largest dollar stream, while software/service becomes the main recurring stream. No battery-swapping or electricity revenue is added.

## Market Structure

The whole-market share basis is vendor revenue under the contract. Network effects score low (0.10): roaming and payment interoperability help drivers but are local, multi-homed and frequently mandated, while an EVSE box does not become intrinsically better because more of the same brand exists. Data-scale advantage is limited (0.20); reliability telemetry helps operations, but it is not a hard-to-replicate product-quality loop. Brand/reputation is moderate (0.40) because uptime and safety matter in procurement, but specifications and certification remain decisive.

Capital intensity is moderate (0.45), reflecting power-electronics engineering, working capital and service footprints rather than billion-dollar scarce assets. Scale economies are meaningful but not winner-take-all (0.55): component buying, certification reuse and manufacturing learning help, yet contract manufacturing and regional supply chains let many firms reach viable scale. Regulatory barriers are moderate-low (0.35): electrical safety, grid codes and connector standards slow entry but open protocols and interoperability rules also fragment supply. Switching costs are moderate (0.45) in back-office software and fleet integrations, but hardware can be multi-vendor and replaced at refresh cycles.

Confidence below 0.8 is mostly irreducible for now because no publication maps these mechanisms to a boundary-matched global revenue pool. Confidence would improve with a global supplier cost/retention panel separating hardware, software and energy resale; revisit when the CharIN, IEA or a regulator publishes comparable vendor economics.

The deterministic trait model produces `s1=0.1243` and `r=0.8458`, implying a 2036 **HHI of 0.0543** and about 18.4 effective competitors. That is a fragmented market with a meaningful first tier, consistent with open standards, regional procurement and manufacturable power electronics. The result should be read as a coarse structural central estimate, not a claim that today's fragmented regional rankings are already mature.

## Players

There is no audited, boundary-matched global vendor-share table. The current top-five inputs are analyst estimates triangulated from public/private connector deployments, disclosed EV-charging revenue where available, China’s roughly two-thirds share of global public connectors, and supplier footprints. They deliberately exclude charging-session electricity revenue. StarCharge (6.5%), TELD New Energy (5.5%), ABB E-mobility (4.5%), Delta Electronics (3.5%) and ChargePoint (3.0%) are therefore lower-confidence whole-market estimates, not reported company shares.

The mobility model converts those current positions into 2036 capture using the canonical concentration curve. Hold-position capture answers what each incumbent receives if it keeps its rank; mobility-adjusted capture incorporates pooled ten-year rank churn and disappearance. The modeled gone probability is 10.06% and is already included in adjusted capture.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
|---|---:|---:|---:|
| StarCharge | 12.43% | 9.86% | USD 33.5bn |
| TELD New Energy | 10.51% | 8.49% | USD 28.9bn |
| ABB E-mobility | 8.89% | 7.19% | USD 24.4bn |
| Delta Electronics | 7.52% | 5.78% | USD 19.7bn |
| ChargePoint | 6.36% | 4.67% | USD 15.9bn |

The model does not see company strategy, balance sheets, manufacturing partnerships or regional policy. Chinese electrical-equipment makers, automaker-owned charging ecosystems and energy majors remain credible outside contenders, so the named list should not sum to the market. No company-specific override is used.

## Watch

- IEA's next Global EV Outlook: charger additions, rated-power mix, EV stock and the ratio of electric LDVs per public point.
- Public-fast and ultra-fast equipment pricing versus power rating; a 20% change in net USD/kW materially moves the forecast.
- HDV megawatt-charging standards, depot deployments and grid-connection lead times.
- Open Charge Point Protocol, Plug & Charge and roaming rules: interoperability reduces lock-in, while vertically integrated fleets could reverse that.
- Comparable EVSE-only revenue disclosures from StarCharge, TELD, ABB E-mobility, Delta and ChargePoint; use them to replace the provisional current shares.
- Whether charger-management software monetization shifts from per-port subscriptions to energy/payment take-rates, which would require revisiting the revenue boundary.

## Peer Comparison

- **72% over our 2035 estimate:** Precedence Research (2026 page; accessed 2026-08-03) forecasts **USD 492.59 billion in 2035**, versus about **USD 285.9 billion** on our interpolated path. It reports USD 47.61 billion in 2025 and 26.32% CAGR for 2026-2035. Its segmentation by charger type and application is directionally close, but the public page does not clearly separate vendor equipment/software revenue from installation and other project spend, so the arithmetic is only partly comparable. https://www.precedenceresearch.com/electric-vehicle-charging-infrastructure-market
- **11% under our 2034 estimate, but not directly comparable:** IMARC Group (2026) forecasts **USD 213.75 billion in 2034**, versus about **USD 240.3 billion** on our path, from USD 21.58 billion in 2025 at 28.15% CAGR. IMARC explicitly includes hardware, software, installation, maintenance, charge-point-operator operations and roaming. That is broader downstream scope than our vendor-recognized boundary, while its base-year value is much lower; the mismatch likely reflects different treatment of commercial DC systems and revenue recognition. https://www.imarcgroup.com/electric-vehicle-charging-station-market
- **18% over our 2032 estimate:** Polaris Market Research's 2024-vintage forecast is **USD 200.08 billion in 2032**, versus about **USD 169.9 billion** on our path, from USD 32.20 billion in 2024 at 25.6% CAGR. The report covers charger type, charging type, connector, installation and end use, but does not expose a precise value-chain revenue boundary. Treat it as an infrastructure-spend benchmark rather than a clean vendor-revenue comparison. https://www.polarismarketresearch.com/industry-analysis/electric-vehicle-ev-charging-infrastructure-market

The spread is wide: same-label forecasts differ by more than 2x at nearby horizons. That disagreement supports retaining the bottom-up physical bridge and explicit exclusions instead of averaging peer headlines.

## Sources

- International Energy Agency, *Global EV Outlook 2026 — Electric vehicle charging*, 2026: https://www.iea.org/reports/global-ev-outlook-2026/electric-vehicle-charging-chap-6-and-10
- International Energy Agency, *Global EV Outlook 2026 — Outlook for electric mobility*, 2026: https://www.iea.org/reports/global-ev-outlook-2026/outlook-for-electric-mobility-chap-9-11
- International Energy Agency, *Global EV Outlook 2025 — Trends in electric car markets*, 2025: https://www.iea.org/reports/global-ev-outlook-2025/trends-in-electric-car-markets-2
- International Energy Agency, *Global EV Outlook 2025 — Electric vehicle charging*, 2025: https://www.iea.org/reports/global-ev-outlook-2025/electric-vehicle-charging
- Precedence Research, *Electric Vehicle Charging Infrastructure Market*, accessed 2026-08-03: https://www.precedenceresearch.com/electric-vehicle-charging-infrastructure-market
- IMARC Group, *Electric Vehicle Charging Station Market*, 2026: https://www.imarcgroup.com/electric-vehicle-charging-station-market
- Polaris Market Research, *Electric Vehicle (EV) Charging Infrastructure Market*, forecast vintage 2024, accessed 2026-08-03: https://www.polarismarketresearch.com/industry-analysis/electric-vehicle-ev-charging-infrastructure-market
