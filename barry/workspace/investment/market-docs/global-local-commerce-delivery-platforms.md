---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 95.0
  maturity-market-value: 270.0
penetration:
  inputs:
    target-series: data/global-local-commerce-delivery-platforms/penetration.csv
    measure: spend-share
    ceiling: 0.30
    analogs:
      - us-ecommerce-retail-share
      - uk-online-retail-share
    w-fit: 0.50
  model-estimate:
    L: 0.3
    t0: 2029.195719
    k: 0.148254
  method: logistic-blend
  date: 2026-08-04
concentration:
  inputs:
    traits:
      network-effects: {score: 0.25, confidence: 0.80}
      data-scale-advantage: {score: 0.50, confidence: 0.70}
      brand-reputation: {score: 0.55, confidence: 0.70}
      capital-intensity: {score: 0.30, confidence: 0.75}
      scale-economies: {score: 0.65, confidence: 0.80}
      regulatory-barriers: {score: 0.45, confidence: 0.75}
      switching-costs: {score: 0.30, confidence: 0.80}
  override:
    s1: 0.27
    r: 0.70
    reason: "The pooled trait model treats local network effects as globally portable; city-level density, national regulation, multi-homing, and regionally disjoint leaders cap whole-global-market concentration."
  model-estimate:
    s1: 0.347687
    r: 0.644782
  hhi: 0.142941
  method: selected-direct-ridge
  date: 2026-08-04
players:
  inputs:
    current:
      - rank: 1
        name: Meituan delivery marketplaces
        ticker: 3690.HK
        share: 0.23
      - rank: 2
        name: Delivery Hero
        ticker: DHER.DE
        share: 0.18
      - rank: 3
        name: Uber Delivery
        ticker: UBER
        share: 0.17
      - rank: 4
        name: DoorDash
        ticker: DASH
        share: 0.15
      - rank: 5
        name: Alibaba Local Services
        ticker: BABA
        share: 0.07
  model-estimate:
    - rank: 1
      name: Meituan delivery marketplaces
      ticker: 3690.HK
      hold-position-capture: 0.27
      mobility-adjusted-capture: 0.195896
      mobility-adjusted-revenue: 52.89192
    - rank: 2
      name: Delivery Hero
      ticker: DHER.DE
      hold-position-capture: 0.189
      mobility-adjusted-capture: 0.139757
      mobility-adjusted-revenue: 37.73439
    - rank: 3
      name: Uber Delivery
      ticker: UBER
      hold-position-capture: 0.1323
      mobility-adjusted-capture: 0.102139
      mobility-adjusted-revenue: 27.57753
    - rank: 4
      name: DoorDash
      ticker: DASH
      hold-position-capture: 0.09261
      mobility-adjusted-capture: 0.07667
      mobility-adjusted-revenue: 20.7009
    - rank: 5
      name: Alibaba Local Services
      ticker: BABA
      hold-position-capture: 0.064827
      mobility-adjusted-capture: 0.068742
      mobility-adjusted-revenue: 18.56034
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-04
---

# Global Local-Commerce Delivery Platforms

## Market Definition

**Market scope.** Global third-party on-demand marketplaces that arrange delivery from restaurants, grocers, convenience stores and local retailers to consumers, including restaurant delivery, quick commerce and multi-category local retail. It includes marketplace ordering, platform-dispatched last mile, subscriptions and order-linked merchant advertising. It excludes ride-hailing, travel and hotel booking, in-store services, traditional parcel/e-commerce fulfilment, merchant-owned direct ordering and delivery, pure courier software, restaurant food sales and inventory revenue from first-party dark stores.

**Revenue boundary.** Annual revenue recognized by the marketplace operator from included delivery orders: merchant commissions, consumer delivery/service/subscription fees, logistics revenue and order-linked advertising. Customer gross order value (GOV/GMV), merchant food or merchandise sales, tips, taxes and amounts passed through to independent couriers are not market value. Where an operator reports gross rider or first-party inventory revenue, it is normalized toward platform net revenue; where segment disclosure combines delivery with in-store or travel, only the delivery-linked portion is estimated.

**Addressable unit and penetration.** The denominator is annual eligible merchant spend on prepared meals, groceries, convenience and local-retail goods in digitally connected urban and suburban catchments. The numerator is the GMV of that spend transacted through an included third-party delivery marketplace, making penetration a `spend-share` measure. The target series is an analyst reconstruction from disclosed platform GMV and broad category-spend estimates; it is not a single published series.

**Billable units and segments.** Billable activity is platform GMV by (1) restaurant meals and (2) grocery, convenience and local retail. Recognized revenue equals GMV multiplied by the net revenue margin, plus order-linked advertising and subscriptions not already included. Regional results are aggregated only after excluding non-delivery local services.

**Time and value basis.** Base year 2026, fixed horizon 2036, nominal USD at approximately current exchange rates. The same global vendor-revenue contract is used for sizing, concentration and player shares.

## Current View

Expected 2026 market value is **USD 95 billion**. The reconstruction starts with four unusually useful disclosures. DoorDash produced USD 13.72 billion of 2025 revenue on USD 102.0 billion of Marketplace GOV. Uber's Delivery operation was running above USD 100 billion of annualized bookings in Q4 2025 and generated USD 4.89 billion of Q4 revenue; the full-year revenue estimate is about USD 17 billion. Delivery Hero reported EUR 49.20 billion of GMV and EUR 14.80 billion of total segment revenue in 2025, although gross rider accounting and integrated quick-commerce sales make its reported revenue broader than a clean net take-rate. Meituan reported RMB 96.07 billion of delivery-service revenue and RMB 260.83 billion for Core Local Commerce; allocating delivery-linked commissions and advertising while excluding in-store, hotel and travel implies roughly USD 21-23 billion on this boundary.

Those anchors, plus lower-confidence estimates for Alibaba Local Services, iFood, Grab, Swiggy and regional platforms, sum to roughly USD 87 billion in 2025 and about USD 95 billion on a 2026 run-rate. As a GMV cross-check, the included platforms process about USD 0.75 trillion of orders against roughly USD 6.8 trillion of eligible category spend, implying 11% penetration and a blended 12.7% recognized-revenue yield. The yield is above a pure commission take-rate because some operators gross up delivery, subscription or first-party quick-commerce revenue; the reconstruction removes obvious inventory sales but cannot fully standardize IFRS/GAAP presentation.

Evidence quality is medium. Public-company revenue and GMV are strong primary anchors, but Meituan and Alibaba do not disclose a clean delivery-only segment and the private/regional tail is estimated. A plausible current range is USD 80-110 billion.

## Adoption Path

The target spend-share rises from 4.7% in 2019 to 11.0% in 2026. The 2020-2021 jump reflects pandemic channel migration; slower gains afterward reflect restaurant reopening and the harder economics of lower-density grocery and retail. A 30% ceiling assumes third-party platforms become a major convenience channel without displacing pickup, merchant-direct ordering, planned grocery shops or in-store local retail. The analogs are U.S. and UK ecommerce retail spend-share: both capture channel migration and a pandemic shock, while the UK series supplies a faster case and the U.S. series a slower anchor. With only two analogs and a target still early in its ceiling, fit weight is capped at 50% and the resulting curve remains a disciplined interpolation rather than a broad prior.

The blended logistic curve has `L=0.30`, `t0=2029.20` and `k=0.1483`. It smooths the reconstructed 11.0% 2026 observation to 11.5% and reaches 22.0% in 2036. The 2036 size bridge projects eligible spend from USD 6.8 trillion to about USD 10.2 trillion (roughly 4.1% nominal annual growth), applies that platform spend-share, and assumes monetization settles near 12.1% as advertising, membership and merchant software offset competitive pressure on commissions. Category expansion is limited to delivery-linked restaurant, grocery, convenience and local retail revenue already inside the contract; ride-hailing, travel, in-store reservations and parcel logistics remain excluded.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Eligible merchant spend | USD 6.8tn | USD 10.2tn | Nominal food-away-from-home, grocery and eligible local retail spend |
| Third-party delivery platform spend-share | 11.0% observed / 11.5% curve | 22.0% | Selected logistic path; 30% long-run ceiling |
| Platform GMV | about USD 0.75tn | about USD 2.24tn | Eligible spend multiplied by penetration |
| Recognized revenue / GMV | about 12.7% | about 12.1% | Mix of commissions, logistics, subscriptions and ads |
| Annual market value | **USD 95bn** | **USD 270bn** | Nominal platform-recognized revenue |

The expected 2036 market value is **USD 270 billion**, an 11.0% CAGR. A plausible range is USD 180-400 billion. The main downside is regulation or merchant resistance compressing take-rates while planned shopping remains offline/direct; the upside is grocery/retail frequency, subscriptions, advertising and autonomous fulfilment expanding monetization. Restaurant delivery remains the largest GMV segment, while grocery/retail and advertising contribute most incremental revenue.

## Market Structure

The share basis is global revenue under the stated delivery-platform contract. Network effects score 0.25 at this global boundary: courier density, consumer selection and merchant liquidity are strong inside a city, but they reset across cities and countries, and consumers and merchants commonly multi-home. Data-scale advantage is 0.50 because demand forecasting, dispatch and recommendations improve with data, although local operating data and commercial access matter more than a single global corpus. Brand/reputation is moderate at 0.55: trust and subscription ecosystems help, but local restaurant supply and price frequently override global brand.

Capital intensity is 0.30 because the core model is software and working-capital light even though subsidy wars and owned courier models require substantial funding. Scale economies score 0.65 through shared technology, payments, advertising tools and procurement, offset by irreducibly local courier and merchant operations. Regulatory barriers are 0.45 because labour classification, food safety, payments and foreign-ownership rules can entrench local incumbents but also fragment the global pool. Switching costs are low-moderate at 0.30 because consumers, merchants and couriers can multi-home, although memberships and merchant integrations add friction.

The deterministic trait model produces `s1=0.3477` and `r=0.6448`, implying too much whole-global concentration for a category whose network density resets locally. The canonical override instead uses a 27% leader share and 0.70 rank decay, producing a 2036 **HHI of 0.1429**, or about seven effective competitors. That is moderately concentrated: global technology and consolidation create a first tier, while regional systems and multi-homing preserve a meaningful tail. Revisit the override if a common cross-border technology stack demonstrably converts local density into global economics, or if consolidation removes multiple regional leaders.

## Players

Current whole-market shares are analyst estimates normalized to the vendor-revenue boundary: Meituan delivery marketplaces 23%, Delivery Hero 18%, Uber Delivery 17%, DoorDash 15% and Alibaba Local Services 7%. DoorDash's acquisition of Deliveroo is included in DoorDash; Delivery Hero's stake and brand portfolio are treated as one operator. The ranking is less certain than the disclosed group revenue because gross-versus-net accounting differs and Meituan/Alibaba require segment allocation.

The mobility model converts those current positions into 2036 hold-position and mobility-adjusted capture. Its pooled ten-year base rate sees current rank and share spacing, but not geographic exclusivity, subsidy intensity, autonomous-delivery capability, labour regulation or company-specific execution. The 10.06% gone probability is already included in adjusted capture.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
|---|---:|---:|---:|
| Meituan delivery marketplaces | 27.00% | 19.59% | USD 52.9bn |
| Delivery Hero | 18.90% | 13.98% | USD 37.7bn |
| Uber Delivery | 13.23% | 10.21% | USD 27.6bn |
| DoorDash | 9.26% | 7.67% | USD 20.7bn |
| Alibaba Local Services | 6.48% | 6.87% | USD 18.6bn |

No player override is used. The model's global rank mixing may be too harsh on geographically protected incumbents and too generous to a currently fifth-ranked Alibaba, so treat company outputs as base rates. iFood, Grab, Swiggy, JD and future regional consolidators remain credible outside contenders.

## Watch

- Clean delivery-only revenue and GMV disclosures from Meituan and Alibaba; these are the largest current share uncertainties.
- Grocery and retail share of DoorDash, Uber, Delivery Hero and Grab orders, and whether higher basket size offsets lower take-rate and fulfilment margins.
- Merchant-advertising revenue as a percentage of GMV; Delivery Hero reported EUR 1.5 billion of AdTech revenue in 2025 and targets more than 4% of GMV long term.
- Courier employment, minimum-pay and fee-cap rules in the EU, U.S., China, India and Latin America; distinguish higher platform revenue gross-up from genuine economic take-rate.
- Cross-border consolidation after DoorDash/Deliveroo and Prosus/Just Eat Takeaway, especially whether common technology creates global rather than merely local scale economies.
- Autonomous sidewalk, drone and robot delivery cost per completed order; include revenue effects only when deployments move beyond controlled pilots.
- Membership attachment, order frequency and consumer multi-homing, which determine whether switching costs rise enough to justify a higher concentration assumption.

## Peer Comparison

- **Not comparable; 186% over our 2035 estimate on the headline arithmetic:** Precedence Research (2026 page) forecasts **USD 694.65 billion in 2035** from USD 257.43 billion in 2025, versus roughly USD 243 billion on our interpolated vendor-revenue path. Its boundary appears to mix order value and delivery-service activity and includes merchant-direct food delivery; it is therefore much broader than platform-recognized revenue despite using the word revenue.
- **Not comparable; about 63% over our 2034 estimate:** IMARC Group (2026) forecasts **USD 357.3 billion in 2034** from USD 161.7 billion in 2025, versus roughly USD 219 billion on our path. IMARC includes order-focused, logistics-based and full-service systems and lists restaurant chains alongside third-party platforms, so customer food spend and merchant-direct models appear inside its boundary.
- **Company-specific, not a whole-market forecast:** Delivery Hero's 2025 annual report targets long-term AdTech revenue above **4% of group GMV** and an adjusted EBITDA/GMV margin of **5-8% by 2030**. The advertising target supports modest monetization expansion, but EBITDA margin is not revenue and cannot be compared directly with the market-value forecast.

The headline peer range is not useful for averaging: publications applying the same market label mix customer spend, restaurant revenue, gross platform revenue and net marketplace revenue. The disclosed-company bridge is retained as the primary estimate.

## Sources

- DoorDash, *Fourth Quarter and Full Year 2025 Financial Results*, February 18, 2026: https://ir.doordash.com/news/news-details/2026/DoorDash-Releases-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx
- Uber, *Fourth Quarter and Full Year 2025 Results*, February 4, 2026: https://investor.uber.com/news-events/news/press-release-details/2026/Uber-Announces-Results-for-Fourth-Quarter-and-Full-Year-2025/default.aspx
- Meituan, *Results for the Year Ended December 31, 2025*, March 26, 2026: https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0326/2026032600964.pdf
- Delivery Hero, *Annual Report 2025*, March 24, 2026: https://ir.deliveryhero.com/financial-reports-and-presentations
- Prosus, *FY2025 Financial Results*, June 2025: https://www.prosus.com/~/media/Files/P/prosus-corp-v2/results-reports-and-events-archive/latest-results/fy-2025/prosus-financial-results-fy25-booklet.pdf
- Precedence Research, *Online Food Delivery Market*, accessed August 4, 2026: https://www.precedenceresearch.com/online-food-delivery-market
- IMARC Group, *Online Food Delivery Market*, 2026: https://www.imarcgroup.com/online-food-delivery-market
