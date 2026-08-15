---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 2.5
  maturity-market-value: 9.0
penetration:
  inputs:
    target-series: data/north-american-trades-business-management-software/penetration.csv
    measure: stock
    ceiling: 0.75
    analogs: [us-home-computer, us-cable-tv, us-internet-adults, us-social-media]
    w-fit: 0.45
  model-estimate:
    L: 0.75
    t0: 2028.849676
    k: 0.20739
  method: logistic-blend
  date: 2026-08-09
concentration:
  inputs:
    traits:
      network-effects:      {score: 0.25, confidence: 0.70}
      data-scale-advantage: {score: 0.55, confidence: 0.60}
      brand-reputation:     {score: 0.60, confidence: 0.65}
      capital-intensity:    {score: 0.15, confidence: 0.85}
      scale-economies:      {score: 0.67, confidence: 0.75}
      regulatory-barriers:  {score: 0.20, confidence: 0.80}
      switching-costs:      {score: 0.75, confidence: 0.85}
  model-estimate:
    s1: 0.195512
    r: 0.803903
  hhi: 0.10806
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: ServiceTitan
        ticker: TTAN
        share: 0.38
      - rank: 2
        name: Jobber
        share: 0.065
      - rank: 3
        name: Housecall Pro
        share: 0.05
      - rank: 4
        name: BuildOps
        share: 0.04
      - rank: 5
        name: Simpro
        share: 0.03
  override:
    - name: ServiceTitan
      ticker: TTAN
      capture: 0.23
      reason: "FY2026 revenue grew 24%, net dollar retention remained above 110%, gross retention exceeded 95%, and its current revenue lead is much wider than rank alone captures; a modest premium to the structural rank-one share is warranted while still allowing material share dilution."
  model-estimate:
    - rank: 1
      name: ServiceTitan
      ticker: TTAN
      hold-position-capture: 0.195512
      mobility-adjusted-capture: 0.164412
      mobility-adjusted-revenue: 1.479708
    - rank: 2
      name: Jobber
      hold-position-capture: 0.157173
      mobility-adjusted-capture: 0.125825
      mobility-adjusted-revenue: 1.132425
    - rank: 3
      name: Housecall Pro
      hold-position-capture: 0.126352
      mobility-adjusted-capture: 0.100704
      mobility-adjusted-revenue: 0.906336
    - rank: 4
      name: BuildOps
      hold-position-capture: 0.101574
      mobility-adjusted-capture: 0.081089
      mobility-adjusted-revenue: 0.729801
    - rank: 5
      name: Simpro
      hold-position-capture: 0.081656
      mobility-adjusted-capture: 0.065532
      mobility-adjusted-revenue: 0.589788
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---

# North American Trades Business Management Software

## Market Definition

**Market scope.** United States and Canada software used as the operating system for residential and commercial trades businesses: CRM and marketing, estimating, scheduling and dispatch, work orders, technician mobile workflows, inventory/job costing, invoicing, payments and financing enablement, reporting, and closely integrated AI automation. It includes residential service, commercial service, and specialty-trade construction contractors across HVAC, plumbing, electrical, roofing, landscaping, pest control, fire/life safety, and adjacent field-service trades. It excludes consumer lead-generation marketplaces, contractor customer spend/GTV, horizontal accounting/payroll/CRM sold separately, general-contractor project collaboration software, merchant interchange passed through to processors, and software revenue earned outside North America.

**Revenue boundary.** Annual revenue recognized by trades-specific platform vendors from North American customers: recurring subscriptions, net usage and FinTech revenue retained by the platform, and implementation/professional services. Payment volume, loan principal, end-customer spending, and customer GTV are not revenue. This matches ServiceTitan's net usage-revenue presentation and is broader than research definitions limited to scheduling and dispatch.

**Addressable unit and penetration.** The denominator is a structurally eligible trades business that has enough recurring field workflow to justify a dedicated paid platform, estimated at about 0.95 million businesses in 2026. Adoption is the stock share actively paying for a trades-specific cloud business-management platform; it is not the share using any digital tool. Billable units are customer accounts, seats/technicians, enabled modules, and platform-processed transactions. Residential/down-market, residential and commercial mid-market, and commercial/enterprise contractors have different account revenue, but aggregate to the same vendor-revenue boundary.

**Time and value basis.** Base year 2026 and fixed horizon 2036; nominal USD. Values are annual market revenue, not cumulative revenue or full-adoption TAM.

## Current View

The expected 2026 market value is **$2.5 billion**. ServiceTitan is the only major pure-play with public financials: FY2026 revenue was $961 million, of which $925 million was platform revenue, on $82.1 billion of customer GTV and about 10,800 active customers. As substantially all revenue comes from U.S. and Canadian trades businesses, it anchors roughly 38% of this contract.

The remainder is reconstructed from disclosed customer footprints, pricing/seat mix, embedded-payment availability, funding-stage scale, and the long tail of FieldEdge, ServiceTrade, WorkWave, JobNimbus, AccuLynx, vertical specialists, and legacy products. Jobber disclosed more than 100,000 customers in May 2026; Housecall Pro says it is trusted by 200,000+ professionals; and BuildOps reports 1,500+ North American contractors. Those are not comparable units, so their revenue shares are analyst estimates rather than reported market shares. The implied range is **$2.1-3.0 billion**; $2.5 billion is the expected value.

ServiceTitan's 2024 IPO filing estimated $650 billion of serviceable trades spend and a $13 billion revenue opportunity at a 2% take of customer GTV. Inflating the serviceable spend to roughly $700 billion in 2026, the current category earns about 0.36% of underlying contractor revenue, leaving substantial room for paid adoption, modules, payments, and AI-based workflows without assuming the category reaches the vendor's full TAM.

## Adoption Path

The target series estimates paid-platform adoption at 9% in 2018, 12% in 2020, 16% in 2022, 21% in 2024, and 27% in 2026. It triangulates disclosed vendor customer counts against the estimated eligible-business base; it is not a directly published census series. Because the history is short and reconstructed, the fit receives only 45% weight. The 75% ceiling allows persistent non-adoption among sole proprietors, very small operators, and businesses satisfied with horizontal tools.

The analog set combines home computers and cable subscriptions as slower paid-workflow anchors with internet and social-media adoption as faster cloud-distribution anchors. The blended logistic path reaches about **61% in 2036**.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Structurally eligible trades businesses | 0.95m | 1.08m | 1.3% annual net growth from formation, consolidation, and eligibility expansion |
| Paid dedicated-platform penetration | 26.7% | 61.1% | Logistic blend, 75% ceiling |
| Adopted businesses | 0.25m | 0.66m | Addressable businesses x penetration |
| Annual vendor revenue per adopted business | ~$9,900 | ~$13,600 | Blended accounts, seats, modules, net transaction revenue; nominal USD |
| Annual market value | **$2.5bn** | **$9.0bn** | Reconciles to stored size fields |

The $9.0 billion horizon value implies a 13.7% CAGR and remains below the static $13 billion ServiceTitan opportunity cited in 2024 even before a decade of nominal growth. A plausible 2036 range is **$6-13 billion**. The largest sensitivities are whether down-market businesses adopt paid suites, the net payment/financing take retained by platforms, and whether AI agents expand platform revenue or compress seat-based pricing. Subscription revenue remains the core, but usage/FinTech and AI modules should supply a larger share of incremental revenue.

## Market Structure

This is not a direct-network-effect market: one contractor gains little merely because another uses the same product. There are modest ecosystem and benchmarking effects, and proprietary workflow/payment data can improve automation, but data advantages should diminish and competitors can build credible products on common cloud and AI infrastructure.

Scale economies are strong in product development, compliance, integrations, sales, and support, while capital intensity and formal regulation are low. Switching costs are the strongest durable barrier because dispatch, price books, customer history, payments, reporting, and employee routines become deeply embedded. ServiceTitan's FY2026 gross retention above 95% supports the 0.75 switching-cost score. High switching costs protect several installed bases rather than producing a monopoly.

The structural model projects a leader share near 20%, a gradual rank curve, and **HHI about 0.108** in 2036, equivalent to roughly nine effective competitors. That is moderately concentrated but consistent with a large fringe of vertical and segment specialists. Consolidation should remove some narrow vendors, while low entry capital and new AI-native products keep the market from becoming winner-take-all.

## Players

Current revenue shares use the whole North American contract, not customer-count share. ServiceTitan's 38% is anchored to reported revenue; private-company shares are estimates from disclosed scale, pricing, and product mix and should be treated as lower-confidence.

| Player | Current share | Hold-position 2036 capture | Mobility-adjusted capture | Canonical capture | Canonical 2036 revenue |
|---|---:|---:|---:|---:|---:|
| ServiceTitan | 38.0% | 19.6% | 16.4% | **23.0% override** | **$2.07bn** |
| Jobber | 6.5% | 15.7% | 12.6% | 12.6% | $1.13bn |
| Housecall Pro | 5.0% | 12.6% | 10.1% | 10.1% | $0.91bn |
| BuildOps | 4.0% | 10.2% | 8.1% | 8.1% | $0.73bn |
| Simpro | 3.0% | 8.2% | 6.6% | 6.6% | $0.59bn |

ServiceTitan receives a 23% override: FY2026 growth of 24%, net dollar retention above 110%, gross retention above 95%, and the current revenue gap support a modest premium to the structural rank-one share, while the override still assumes significant share dilution from 38%. Jobber can win down-market and now has more than 100,000 customers, but lower account revenue and easier switching make its revenue capture less secure. Housecall Pro has a broad small-business community and payments/AI expansion, but competes intensely with Jobber and point solutions. BuildOps is differentiated in complex commercial contracting and has 1,500+ North American customers, though its segment is narrower. Simpro brings mature field-service workflows and international experience, but its North American scale is smaller. The pooled mobility model does not see company momentum, product quality, financing, or strategy; unlisted incumbents and AI-native entrants can occupy future top ranks.

## Watch

- ServiceTitan's GTV growth, platform earn rate, active-customer growth, and durability of >110% net retention.
- Verified revenue or North American account disclosures from Jobber, Housecall Pro, BuildOps, and Simpro; private-player shares are the weakest current input.
- Whether AI voice, dispatch, estimating, and back-office agents expand module revenue faster than they reduce paid seats.
- Payment-processing penetration and net take rates after interchange, fraud, and partner economics.
- Consolidation of contractors and software vendors: it can increase enterprise ARPU while reducing account counts.
- Adoption among firms with five or fewer employees, which ServiceTitan excluded from its 2024 serviceable opportunity but Jobber and Housecall Pro actively serve.

## Peer Comparison

- **Boundary-mismatched; not directly comparable.** MarketsandMarkets (2025) forecasts the global FSM market from **$5.10 billion in 2025 to $9.17 billion in 2030**, a 12.5% CAGR. Our path is about **$4.2 billion in 2030**. Applying a rough 38% North American share to the peer gives $3.5 billion, about **17% below our estimate**; the difference is directionally explained by our inclusion of trades-specific CRM/ERP, net FinTech, and implementation revenue beyond core FSM.
- **Boundary-mismatched; not directly comparable.** Mordor Intelligence (January 2026) estimates global FSM at **$6.26 billion in 2026** and **$9.87 billion in 2031**, with North America at 37.89% of 2025 revenue. Holding that regional share implies roughly $3.7 billion in 2031 versus our **$4.7 billion**, about **21% below our estimate**. Its universe includes utilities, telecom, manufacturing, and healthcare but may omit the fuller trades operating-system and embedded-FinTech boundary.
- **TAM, not expected revenue.** ServiceTitan's November 2024 S-1 calculates a **$13 billion serviceable market opportunity** from $650 billion of trades spend at a 2% potential revenue capture. That static TAM is **44% above our $9.0 billion 2036 expected market value** and is not a forecast: it assumes full customer penetration and use of the complete product suite.

## Sources

- [ServiceTitan FY2026 Form 10-K, filed March 25, 2026](https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm) - business scope, competition, active customers, retention, GTV, revenue mix, geographic concentration, and risks.
- [ServiceTitan FY2026 results, March 12, 2026](https://investors.servicetitan.com/news-releases/news-release-details/servicetitan-announces-fiscal-fourth-quarter-and-full-fiscal) - $961.0m revenue, $925.4m platform revenue, $82.1bn GTV, ~10,800 active customers, and FY2027 outlook.
- [ServiceTitan S-1, November 18, 2024](https://www.sec.gov/Archives/edgar/data/1638826/000119312524260611/d577298ds1.htm) - $1.5tn trades spend, $650bn serviceable spend, 1% current and 2% potential platform earn rate, $13bn serviceable opportunity, and down-market exclusions.
- [Jobber surpassed 100,000 customers, May 12, 2026 (Google News/PR Newswire)](https://news.google.com/rss/articles/CBMilgJBVV95cUxPdG00TVc4ZEMxN1JSOFpUdHUwOG4tTVlmRXN4MC1teGJNOTV6WmdHV0w2Z3o0alNtSFNVTnlEd0wycGhaS3V0X2FPSVpWbnlsZjVGdUpSelR6V1hVSlZFbkdZZDI3RzE3ZlUtNmIwUXVtQjc1YzlLNnRvQ2xZc3F4MDJBcDlRSE93VHhBUUk0MFhxTUF1endpWjZGNDBTcW9hM2lIVTNGa2N2WUtfYjFjNEM0bWV3U09BbVFCSXZqU2NFZVlBaC1wWDNsNjB0VGswSlgwZ0NHSG1qQ1U1MnZEMnI1UUV5Z3V5NEtDMWplRWN6Z0NmTmRvTkRsSWpVRTAzYkU3b1pOajVQMW5HQTlNa2F2dkMwUQ?oc=5) - current customer footprint.
- [Housecall Pro homepage, accessed August 9, 2026](https://www.housecallpro.com/) - 200,000+ professionals, 100m+ jobs, product scope, and supported team sizes.
- [BuildOps company page, accessed August 9, 2026](https://buildops.com/about) - 1,500+ North American contractors, commercial-only focus, and company scale.
- [BuildOps Series C announcement](https://buildops.com/resources/series-c) - $127m financing, $1bn valuation, and $300bn commercial-contracting industry context.
- [MarketsandMarkets FSM forecast 2025-2030](https://www.marketsandmarkets.com/Market-Reports/field-service-management-market-209977425.html) - global market values, CAGR, scope, and regional ranking.
- [Mordor Intelligence FSM forecast, updated January 2026](https://www.mordorintelligence.com/industry-reports/field-service-management-market) - global values, North American share, cloud/SME adoption, and forecast CAGR.
