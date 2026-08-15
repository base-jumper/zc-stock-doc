---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 5.0
  maturity-market-value: 14.0
penetration:
  inputs:
    target-series: data/southeast-asia-on-demand-mobility-and-delivery-platforms/penetration.csv
    measure: spend-share
    ceiling: 0.19
    analogs:
      - us-ecommerce-retail-share
      - uk-online-retail-share
    w-fit: 0.40
  model-estimate:
    L: 0.19
    t0: 2022.994406
    k: 0.184562
  method: logistic-blend
  date: 2026-08-08
concentration:
  inputs:
    traits:
      network-effects: {score: 0.65, confidence: 0.80}
      data-scale-advantage: {score: 0.62, confidence: 0.70}
      brand-reputation: {score: 0.58, confidence: 0.75}
      capital-intensity: {score: 0.32, confidence: 0.80}
      scale-economies: {score: 0.72, confidence: 0.80}
      regulatory-barriers: {score: 0.45, confidence: 0.75}
      switching-costs: {score: 0.22, confidence: 0.85}
  override:
    s1: 0.65
    r: 0.32
    reason: "The pooled trait model implies geometric share above 100%; country-local network effects, multi-homing, regulation, and credible national challengers cap the regional leader below its unconstrained estimate."
  model-estimate:
    s1: 0.720017
    r: 0.321993
  hhi: 0.4707
  method: selected-direct-ridge
  date: 2026-08-08
players:
  inputs:
    current:
      - rank: 1
        name: Grab
        ticker: GRAB
        share: 0.69
      - rank: 2
        name: GoTo On-Demand Services
        ticker: GOTO.JK
        share: 0.16
  model-estimate:
    - rank: 1
      name: Grab
      ticker: GRAB
      hold-position-capture: 0.65
      mobility-adjusted-capture: 0.463463
      mobility-adjusted-revenue: 6.488482
    - rank: 2
      name: GoTo On-Demand Services
      ticker: GOTO.JK
      hold-position-capture: 0.208
      mobility-adjusted-capture: 0.192325
      mobility-adjusted-revenue: 2.69255
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-08
---

# Southeast Asia On-Demand Mobility and Delivery Platforms

## Market Definition

**Market scope.** Consumer on-demand mobility and delivery platforms in ASEAN-10: Brunei, Cambodia, Indonesia, Laos, Malaysia, Myanmar, the Philippines, Singapore, Thailand and Vietnam. Included products are ride-hailing, taxi and two-wheel mobility booked through a platform; restaurant, grocery and convenience delivery; order- or trip-linked subscriptions and advertising; and operator-owned grocery sales reported inside an included segment. Excluded products are digital banking, lending, payments not attached to an included trip or order, ecommerce parcel logistics, online travel, merchant-direct ordering, public transport, vehicle rental and offline grocery sales outside a platform operator's included segment.

**Revenue boundary.** Annual revenue recognized by operators in their mobility and delivery segments, including commissions, consumer and merchant fees, subscriptions, advertising, logistics revenue and operator-owned grocery revenue consolidated inside those segments. Customer GMV, tips, taxes and driver or merchant gross earnings are not market value. This boundary intentionally matches GRAB's reported Deliveries and Mobility revenue; presentation differences between net marketplace revenue and gross first-party retail remain a current sizing uncertainty.

**Addressable unit and penetration.** The addressable unit is annual ASEAN-10 consumer spend on point-to-point private transport and restaurant, grocery and convenience transactions that could structurally move through an on-demand platform. Penetration is included platform GMV divided by that eligible spend, a `spend-share` measure. The target series reconstructs platform GMV from successive Google/Temasek/Bain digital-economy reports and an analyst estimate of eligible category spend; the numerator is stronger than the denominator.

**Billable units and segments.** Billable activity is mobility and delivery GMV. Recognized revenue is modeled separately for mobility and delivery before aggregation because trip economics and monetization differ. Country results aggregate only after translation to USD; the player shares, concentration and size use the same regional recognized-revenue boundary.

**Time and value basis.** Base year 2026, fixed horizon 2036, nominal USD at approximately current exchange rates. Ordinary population, category-spend inflation and platform monetization are included in the horizon value.

## Current View

Expected 2026 market value is **USD 5.0 billion**. Google, Temasek and Bain estimate ASEAN-10 food-delivery revenue of USD 2.4 billion and transport revenue of USD 1.9 billion in 2025, against GMV of USD 23.0 billion and USD 11.5 billion respectively. Their revenue definitions include advertising and distinguish direct seller revenue from third-party platform revenue, making the combined USD 4.3 billion the best available boundary-matched regional anchor. Applying the report's recent mid-teens sector growth and the public-company run rates produces the 2026 estimate.

GRAB reported 2025 Deliveries revenue of USD 1.800 billion and Mobility revenue of USD 1.219 billion, or USD 3.019 billion combined. In Q2 2026 the same segments generated USD 531 million and USD 331 million respectively, a USD 3.448 billion annualized run rate. GoTo reported FY2025 On-Demand Services net revenue of IDR 12.596 trillion and Q2 2026 net revenue of IDR 3.593 trillion; at its disclosed Q2 exchange rate, the latter is roughly USD 0.80 billion annualized. These disclosures reconcile to about 85% of the estimated market, with ShopeeFood, foodpanda, Maxim, inDrive, Xanh SM and smaller local platforms comprising the tail.

Evidence quality is medium-high for the market total and GRAB, and medium for player shares. The Google/Temasek/Bain total is a direct regional estimate and the two leaders disclose segment revenue, but operator-owned grocery accounting, currency movements and private-company revenue prevent exact normalization. A plausible 2026 range is USD 4.5-5.8 billion.

## Adoption Path

The reconstructed spend-share rises from 5.5% in 2019 to 12.0% in 2026, with a pandemic-related dip in mobility in 2020 offset partly by delivery. A 19% ceiling allows on-demand platforms to become a mainstream channel while leaving public transport, private vehicles, street-hail taxis, dine-in, pickup and planned grocery shopping outside the channel. U.S. and UK ecommerce spend-share are the only available like-measure analogs; both model digital channel migration, while the UK supplies a faster pandemic-shock path and the U.S. a slower anchor. Because the eligible-spend denominator is reconstructed and the target is already well into the asserted ceiling, fit weight is capped at 40%.

The blended logistic curve has `L=0.19`, `t0=2022.99` and `k=0.1846`; it smooths the 2026 observation to 12.1% and reaches 17.4% in 2036. The 2036 size bridge starts from Google/Temasek/Bain's 2025 ASEAN-10 platform GMV of USD 34.5 billion and its 2030 forecast of USD 58.5 billion. Growth then slows from about 11% to roughly 8% annually, reaching about USD 93 billion in 2036. Recognized revenue rises from 12.5% of GMV in 2025 to about 15% in 2036 as advertising, subscriptions and merchant tools expand, partly offset by affordability initiatives and competition. Category expansion is limited to included trips, delivery orders and attached monetization; fintech and travel remain excluded.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Eligible consumer spend | about USD 329bn | about USD 530bn | Nominal private transport and eligible food/retail spend |
| On-demand platform spend-share | 12.0% observed estimate | about 17.4% | Selected logistic path |
| Platform GMV | about USD 39.5bn | about USD 93bn | Eligible spend multiplied by penetration |
| Recognized revenue / GMV | about 12.7% | about 15.0% | Commissions, fees, ads, subscriptions and included first-party sales |
| Annual market value | **USD 5.0bn** | **USD 14.0bn** | Nominal operator-recognized revenue |

The expected 2036 market value is **USD 14 billion**, a 10.8% CAGR, with a plausible USD 9-21 billion range. The largest sensitivities are post-2030 GMV growth, monetization from advertising and subscriptions, and the persistence of low-cost offerings. Delivery remains the larger GMV pool; mobility's higher revenue yield and profitability make its contribution disproportionately valuable.

## Market Structure

The share basis is ASEAN-10 recognized mobility-plus-delivery revenue. Network effects score 0.65: consumer, driver and merchant liquidity materially improve wait times, selection and utilization, but users, drivers and merchants can multi-home and density resets by city and country. Data-scale advantage is 0.62 because mapping, dispatch, fraud, pricing and recommendation improve with proprietary activity data, although well-funded challengers can reach acceptable quality. Brand/reputation scores 0.58 because safety, reliability and habit influence choice without preventing price-led switching.

Capital intensity is 0.32 because core software and contracted supply are asset-light, despite substantial historical subsidy and working-capital needs. Scale economies score 0.72: shared technology, payments, advertising, procurement and cross-service driver utilization create persistent regional cost advantages, though physical service remains local. Regulatory barriers score 0.45 because transport licensing, labour rules and foreign-ownership constraints slow entry but also preserve national challengers. Switching costs are low at 0.22 because consumers and supply partners commonly install or serve multiple apps; memberships and wallets add only modest friction.

The deterministic trait model produces `s1=0.7200` and `r=0.3220`, implying an exceptionally dominant leader and a thin tail. Its unconstrained geometric mass exceeds 100%, which is invalid for mobility assignment. The canonical override sets a 65% leader share and 0.32 rank decay, explicitly allowing a durable regional leader, one meaningful challenger and a small country-level tail. The resulting **HHI is 0.4707**, equivalent to about 2.1 effective competitors and consistent with a dominant regional leader. Revisit the override if cross-border technology meaningfully weakens national challengers, if Grab-GoTo consolidation occurs, or if Shopee converts ecommerce reach into sustained on-demand share.

## Players

The current ranking uses 2026 recognized-revenue run rates on the market contract. GRAB is estimated at 69% from USD 3.448 billion of annualized Q2 Deliveries and Mobility revenue against a USD 5.0 billion market. GoTo is estimated at 16% from Q2 On-Demand Services net revenue annualized at its disclosed USD/IDR rate. These are whole-market shares, not shares of the named pair; the remaining 15% belongs to private and product-specific challengers.

The mobility model converts current position and share spacing into 2036 hold-position and mobility-adjusted capture. Its pooled historical base rate sees current rank and the wide gap between GRAB and GoTo, but not GRAB's company-specific execution, multi-service ecosystem, regulatory relationships or a possible merger. No player override is used. The modeled gone probability is already included in adjusted capture and is not applied again.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
|---|---:|---:|---:|
| Grab | 65.00% | 46.35% | USD 6.49bn |
| GoTo On-Demand Services | 20.80% | 19.23% | USD 2.69bn |

## Watch

- GRAB Deliveries revenue excluding Jaya Grocer and Everrise, and whether owned-store consolidation materially inflates recognized-revenue share relative to asset-light peers.
- Google/Temasek/Bain's annual transport and food GMV and revenue revisions, especially the 2030 forecast and the implied revenue yield.
- GoTo's on-demand GTV growth after its 2025 affordability reset and whether improving monetization comes at the expense of share.
- ShopeeFood, foodpanda, Maxim, inDrive and Xanh SM revenue or GMV disclosures sufficient to extend the current ranking beyond two players.
- Advertising, subscription and merchant-tool revenue as a percentage of GMV; the 15% horizon revenue yield depends on these streams offsetting price pressure.
- Driver employment, minimum-pay, transport-licensing and foreign-ownership rules by country; regulation can either entrench the leader or preserve national fragmentation.
- Autonomous-vehicle and electric two-wheeler unit economics, but only after deployments affect completed-trip cost at scale.

## Peer Comparison

No additional boundary-matched 5-10 year vendor-revenue forecast was found. Published ride-hailing and online-food-delivery market forecasts generally report customer spend, booking value or merchant food sales and therefore cannot be compared with this operator-recognized-revenue boundary. The Google/Temasek/Bain 2030 GMV forecast is used as a sizing input rather than as an independent peer benchmark; retaining that distinction avoids false precision from market labels that mix GMV and revenue.

## Sources

- Google, Temasek and Bain & Company, *e-Conomy SEA 2025*, November 2025, pp. 12-20: https://services.google.com/fh/files/misc/e_conomy_sea_2025_report.pdf
- Grab Holdings, *Fourth Quarter and Full Year 2025 Results*, February 11, 2026: https://www.sec.gov/Archives/edgar/data/1855612/000185561226000011/a2025q4-earningspressrelea.htm
- Grab Holdings, *Second Quarter 2026 Results*, August 4, 2026: https://www.sec.gov/Archives/edgar/data/1855612/000185561226000123/a2026q2-earningspressrelea.htm
- Grab Holdings, *Annual Report for the Year Ended December 31, 2025*, March 6, 2026: https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm
- GoTo Group, *Fourth Quarter and Full Year 2025 Earnings Presentation*, March 11, 2026: https://content.goinfra.co.id/asts/InvestorRelation/FinancialInformation/2026-03-11/GOTO%20Q4%20FY25%20Earnings%20Presentation.pdf
- GoTo Group, *Second Quarter 2026 Earnings Presentation*, July 29, 2026: https://content.goinfra.co.id/asts/InvestorRelation/FinancialInformation/2026-07-29/GOTO%202Q26%20Earnings%20Presentation.pdf
