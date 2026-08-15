---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 30.0
  maturity-market-value: 100.0
penetration:
  inputs:
    target-series: data/global-small-business-accounting-and-payments-software/penetration.csv
    measure: stock
    ceiling: 0.78
    analogs: [us-home-computer, us-cable-tv, us-internet-adults]
    w-fit: 0.5
  model-estimate:
    L: 0.78
    t0: 2026.023957
    k: 0.148178
  method: logistic-blend
  date: 2026-08-09
concentration:
  inputs:
    traits:
      network-effects: {score: 0.45, confidence: 0.75}
      data-scale-advantage: {score: 0.55, confidence: 0.70}
      brand-reputation: {score: 0.65, confidence: 0.75}
      capital-intensity: {score: 0.25, confidence: 0.90}
      scale-economies: {score: 0.68, confidence: 0.80}
      regulatory-barriers: {score: 0.40, confidence: 0.75}
      switching-costs: {score: 0.82, confidence: 0.85}
  override:
    s1: 0.32
    r: 0.68
    reason: "The direct model's s1=0.328 and r=0.696 imply 107.8% total modeled share, which is invalid for whole-market mobility. A nearby 32% leader and 0.68 decay preserve the model's concentrated-oligopoly reading while keeping the infinite rank curve at exactly 100%."
  model-estimate:
    s1: 0.328155
    r: 0.695574
  hhi: 0.190476
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: Intuit
        ticker: INTU
        share: 0.29
      - rank: 2
        name: Sage
        ticker: SGE.L
        share: 0.11
      - rank: 3
        name: Xero
        ticker: XRO.AX
        share: 0.055
  model-estimate:
    - rank: 1
      name: Intuit
      ticker: INTU
      hold-position-capture: 0.32
      mobility-adjusted-capture: 0.250352
      mobility-adjusted-revenue: 25.0352
    - rank: 2
      name: Sage
      ticker: SGE.L
      hold-position-capture: 0.2176
      mobility-adjusted-capture: 0.179745
      mobility-adjusted-revenue: 17.9745
    - rank: 3
      name: Xero
      ticker: XRO.AX
      hold-position-capture: 0.147968
      mobility-adjusted-capture: 0.137603
      mobility-adjusted-revenue: 13.7603
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---
# Global Small-Business Accounting and Payments Software

## Market Definition

The market covers software sold worldwide to sole traders and businesses with fewer than 250 employees for the connected jobs of accounting, bookkeeping, invoicing, payroll, expense management, cash-flow administration and business payments. Included market value is vendors' recognized subscription, licence, maintenance and transaction revenue from those products, including the net revenue or take-rate earned on payments initiated inside the suite. Payment GMV, lending principal, interest on vendor-funded credit, consumer tax, marketing software, outsourced bookkeeping or BPaaS, practice-management software sold only to accountants, enterprise-only ERP, and standalone merchant-acquiring or point-of-sale platforms are excluded. The boundary therefore includes QuickBooks Payments and Xero/Melio bill payments but excludes Stripe and Block when they do not control the customer's accounting system of record.

The addressable unit is an economically active formal small business or sole trader that keeps business financial records, estimated at about 115 million entities in 2026 and 130 million in 2036. Penetration is the share paying for or actively using a qualifying digital suite, classified as `stock`; a business counts once even when it buys multiple modules. Billable units are business accounts, employees, seats and payment transactions, collapsed for sizing into recognized annual revenue per adopted entity. Geography is global, with North America, Europe/UK, developed Asia-Pacific and emerging markets modeled through different revenue intensity but aggregated at constant 2026 exchange rates. Values are nominal USD in 2026 and 2036.

## Current View

The expected 2026 market value is `$30B`, with a plausible range of `$24B-$38B`. A top-down check starts with public 2026 market-research estimates of roughly `$16B-$24B` for small-business accounting software alone and adds qualifying payroll, invoice, expense and embedded-payment monetization while excluding raw payment volume. A supplier check reaches a similar result: Intuit's FY2025 Global Business Solutions revenue was `$11.1B`, but roughly `$8.7B` is assigned to this contract after removing Mailchimp and lending-related revenue; Sage contributes an estimated `$3.3B` of small-business accounting, payroll and payments revenue; and Xero's FY2026 NZD2.753B operating revenue translates to about `$1.65B`. Those three anchors contribute approximately `$13.7B`; regional vendors such as Visma, DATEV, IRIS, MYOB, Zoho, FreshBooks, Wave, Odoo and hundreds of local tax-and-accounting suites make up the balance.

The adoption series is an analyst reconstruction rather than a single global survey. It triangulates the rising share of small enterprises purchasing cloud services, the paid-customer histories of QuickBooks, Xero and regional cloud vendors, and national surveys such as Japan's MMRI series. It rises from `22%` in 2018 to `38%` in 2026. The boundary is narrower than generic bookkeeping-app usage because free spreadsheets and accountant-only systems do not count, and broader than cloud-accounting subscriptions because qualifying desktop suites and embedded payment workflows do count. The uncertainty in this reconstructed denominator is why the fit weight is capped at `50%` and the sizing range remains wide.

## Adoption Path

The target series is blended with U.S. home-computer, cable-TV and adult-internet adoption. Together they represent a general-purpose tool with slow replacement, a paid subscription migration with inertia, and a broad digital utility. The asserted `78%` ceiling leaves a persistent tail of informal, very small, inactive or fully outsourced businesses and firms satisfied with local or legacy tools.

The refreshed logistic curve has a `78%` ceiling, a `2026.0` midpoint and `0.148` steepness. It smooths penetration to `38.9%` in 2026 and projects `63.5%` in 2036. The target fit is capped at `50%`; the uncapped statistical fit would place too much trust in a reconstructed early series, while the three analogs supply a deliberately slower and broader prior.

The horizon sizing bridge is:

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Addressable businesses | 115m | 130m | Formal, economically active SMBs and sole traders; ordinary formation partly offset by consolidation/informality |
| Qualifying-suite penetration | 38.9% modeled | 63.5% modeled | Paying or active business accounts; one entity counted once |
| Adopted businesses | 44.8m | about 82.6m | Addressable base multiplied by the expected adoption path |
| Annual revenue per adopted business | about `$670` | about `$1,210` | Blended subscriptions, employees/modules and attached net payment revenue |
| Annual market value | `$30B` | `$100B` | Recognized vendor revenue; totals reconcile to front matter |

The `$100B` expected 2036 value has a plausible range of `$65B-$150B` and implies a `12.8%` nominal CAGR. Entity growth is minor; most growth comes from adoption and monetization. Accounting-only subscriptions should remain the largest stream in customer count, but payroll, payments and AI-assisted workflow should generate most incremental dollars. The central case assumes higher module attachment, ordinary price inflation and richer payment usage lift annual revenue per adopted business by about `5.1%` per year. It does not assume vendors capture payment GMV or replace the accountant's full labor bill.

The largest sensitivities are the quality of the global business-count denominator, whether free AI tools suppress paid adoption, and how much payment and payroll monetization remains attached to the accounting control point. The downside is rapid feature commoditisation and open financial APIs; the upside is that e-invoicing, real-time tax, payroll compliance and autonomous agents turn the accounting suite into the small business's financial operating system.

## Market Structure

Direct network effects are bounded: each business can keep books without other customers using the same vendor. Indirect effects arise through accountant familiarity, app ecosystems, bank feeds, tax integrations and payment rails, but they are national or regional and customers can multi-home. Data scale improves categorisation, fraud detection, cash-flow prediction and AI agents, although foundation models and standardized banking data keep the advantage below winner-take-all strength. Brand and compliance reputation matter because payroll, tax and payment errors are costly.

The category is asset-light, but product localization, regulatory maintenance, security, distribution, support and AI infrastructure create meaningful scale economies. Regulation is a hurdle rather than a scarce licence and often fragments the market by jurisdiction. Switching cost is the strongest trait: historical ledgers, payroll records, tax configuration, bank feeds, integrations, adviser workflows and audit trails make migration risky. These mechanisms support several entrenched global and regional suites rather than one monopoly. Confidence below `0.8` reflects the lack of a boundary-matched global share panel; audited segment revenue by product and customer size would improve it, and collecting that evidence is in *Watch*.

The direct trait model estimates a `32.8%` leader share and `0.696` rank decay, but its infinite geometric curve sums to `107.8%` and is invalid for whole-market mobility. The stored override keeps a nearby `32.0%` leader and lowers rank decay to `0.680`, so modeled shares sum to exactly `100%`. The resulting HHI is `0.190`, equivalent to about 5.25 equally sized competitors and just inside the concentrated band. The result should be read as a coarse concentrated-oligopoly expectation: local tax regimes protect regional specialists even as AI, compliance and payment infrastructure reward scale.

## Players

Intuit is estimated at `29%` of the current pool, based on approximately `$8.7B` of qualifying QuickBooks accounting, desktop, payroll and money revenue. Its FY2025 Global Business Solutions revenue grew `16%` to `$11.1B`, online ecosystem revenue grew `20%` to `$8.3B`, and QuickBooks Online Accounting grew `22%`. The accountant channel, U.S. brand, data and payments attachment support its lead, while limited international growth and strong regional compliance franchises constrain global capture.

Sage is estimated at `11%`. Its durable base in the UK, Europe and Africa, payroll and accountant relationships are defenses, but product and customer-size disclosure does not perfectly match the contract. Xero is estimated at `5.5%`: FY2026 operating revenue was NZD2.753B, customers reached `4.92M`, and the Melio acquisition materially increased U.S. payments revenue. Xero's cloud-native product and accountant channel can gain, while its smaller North American accounting base and the cost of localizing into more countries remain risks.

The current shares are whole-market revenue estimates, not subscriber shares. Regional private vendors and the long tail exceed half of the market, so deployment surveys limited to a country or only the named companies are not comparable. The refreshed mobility model is the canonical 2036 capture view; its gone probability is already incorporated and must not be applied twice.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Intuit | 32.0% | 25.0% | `$25.0B` |
| Sage | 21.8% | 18.0% | `$18.0B` |
| Xero | 14.8% | 13.8% | `$13.8B` |

The mobility view discounts Intuit for rank churn and assigns meaningful upside to Sage and Xero if either moves up the modeled rank curve. The common `10.1%` gone probability is already embedded. This pooled historical model does not know Intuit's execution, Xero's Melio integration, Sage's cloud transition or the likelihood that an outside AI-native, bank or payments contender enters the top three; no company-specific override is used.

## Watch

Obtain a boundary-matched global adoption series and audited revenue splits for Intuit accounting/payments/payroll net of Mailchimp and lending, Sage by customer size and module, and Xero subscription versus direct and syndication payments. Track Xero/Melio payment take-rates, QuickBooks international online growth, Sage cloud-native ARR, e-invoicing mandates, bank-feed and tax-API portability, AI-agent pricing, accountant-channel preferences, churn after material price rises, and whether standalone payment processors or banks displace the accounting suite as the financial control point.

## Peer Comparison

Business Research Insights' 2026 publication estimates small-business accounting software at `$24.45B` in 2026 and `$58.08B` in 2035. Our path interpolates to about `$89B` in 2035, so the peer is `35% under our estimate` at the same year. The peer is useful for the accounting core but not directly comparable because its public definition does not clearly include attached payroll and vendor-recognized payment revenue.

MarketsNxt estimates `$18.6B` in 2024 and `$48.2B` in 2034 for global small-business accounting software. Our path reaches about `$79B` in 2034, making the peer `39% under our estimate`. Again, the direction is consistent and the gap is mostly the wider integrated-suite contract plus faster module and payment monetization. Neither peer publishes enough free detail to normalize geography, customer-size cutoffs or gross-versus-net payment accounting, so both are benchmarks rather than model inputs.

## Sources

- Intuit, FY2025 results, August 21, 2025: https://investors.intuit.com/news-events/press-releases/detail/1266/intuit-reports-strong-fourth-quarter-and-full-year-fiscal-2025-results-sets-fiscal-2026-guidance-with-double-digit-revenue-growth-and-continued-operating-margin-expansion
- Intuit, FY2025 Form 10-K, Global Business Solutions product and revenue definitions: https://www.sec.gov/Archives/edgar/data/896878/000089687825000035/intu-20250731.htm
- Xero, FY2026 annual results investor presentation, May 14, 2026: https://brandfolder.xero.com/NE531UQB/as/bx8xwhj65zjm36s5fn4kc4gx/Xero_FY26_Annual_Results_Investor_Presentation
- Xero investor page, FY2026 results and customer count: https://www.xero.com/au/investors/
- Sage, FY2025 annual report and results centre: https://www.sage.com/en-gb/company/investors/results-reports-presentations/
- IFC, MSME finance overview and formal MSME financing-gap context: https://www.ifc.org/en/what-we-do/sector-expertise/financial-institutions/msme-finance
- Eurostat, digital economy and society statistics for enterprise cloud adoption: https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Cloud_computing_-_statistics_on_the_use_by_enterprises
- Business Research Insights, *Small Business Accounting Software Market*, 2026: https://www.businessresearchinsights.com/market-reports/small-business-accounting-software-market-104294
- MarketsNxt, *Global Small Business Accounting Software Market*, 2026: https://marketsnxt.com/reports/global/information-technology-electronics/small-business-accounting-software-market/
