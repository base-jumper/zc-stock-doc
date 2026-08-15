---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 7.0
  maturity-market-value: 55.0
penetration:
  inputs:
    target-series: data/us-direct-to-consumer-telehealth/penetration.csv
    measure: stock
    ceiling: 0.25
    analogs: [us-streaming-svod, us-cable-tv, us-internet-adults, us-home-computer]
    w-fit: 0.35
  model-estimate:
    L: 0.25
    t0: 2032.611616
    k: 0.267424
  method: logistic-blend
  date: 2026-08-02
concentration:
  inputs:
    traits:
      network-effects: {score: 0.25, confidence: 0.75}
      data-scale-advantage: {score: 0.45, confidence: 0.65}
      brand-reputation: {score: 0.65, confidence: 0.75}
      capital-intensity: {score: 0.35, confidence: 0.80}
      scale-economies: {score: 0.65, confidence: 0.75}
      regulatory-barriers: {score: 0.55, confidence: 0.80}
      switching-costs: {score: 0.40, confidence: 0.70}
  model-estimate:
    s1: 0.311443
    r: 0.682249
  hhi: 0.18146
  method: selected-direct-ridge
  date: 2026-08-02
players:
  inputs:
    current:
      - rank: 1
        name: Hims & Hers
        ticker: HIMS
        share: 0.30
      - rank: 2
        name: Ro
        share: 0.11
      - rank: 3
        name: BetterHelp
        ticker: TDOC
        share: 0.10
  model-estimate:
    - rank: 1
      name: Hims & Hers
      ticker: HIMS
      hold-position-capture: 0.311443
      mobility-adjusted-capture: 0.244407
      mobility-adjusted-revenue: 13.442385
    - rank: 2
      name: Ro
      hold-position-capture: 0.212482
      mobility-adjusted-capture: 0.158363
      mobility-adjusted-revenue: 8.709965
    - rank: 3
      name: BetterHelp
      ticker: TDOC
      hold-position-capture: 0.144965
      mobility-adjusted-capture: 0.114491
      mobility-adjusted-revenue: 6.297005
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-02
---
# U.S. Direct-to-Consumer Telehealth

## Market Definition

The market covers U.S. consumer-initiated digital-care platforms that acquire patients directly and recognize revenue from virtual clinical care, recurring condition-management programs, and prescriptions or health products they fulfill or sell as part of the same patient relationship. Included use cases are sexual health, hair loss, dermatology, mental health, obesity and metabolic care, hormonal health, sleep, and routine primary or preventive care. Traditional provider telehealth, hospital and insurer virtual-care programs, employer-funded digital health, enterprise telemedicine software, standalone pharmacies, and in-person services are excluded. A platform's payer- or employer-channel revenue is excluded where it can be separated.

The revenue boundary is annual revenue recognized by the consumer platform, including its net or gross accounting treatment for fulfilled prescriptions and products. It is not prescription GMV, total patient healthcare spend, pharmacy list price, or clinician billings outside the platform. This means comparisons require care: Hims & Hers recognizes much of the product revenue that some agency-model peers report only net.

The addressable unit is a U.S. adult. Penetration is the share of U.S. adults who are active paying users of at least one included platform during the year, classified as `stock`; one person counts once even if they buy several treatments or use several platforms. Billable units are active patient-years, consultations, treatment months, prescriptions, lab tests, and product shipments. For sizing they are collapsed into annual recognized revenue per active buyer, with separate judgment about product and service mix. Conditions are not separate additive addressable populations because one adult can have several; they instead affect penetration and revenue intensity. The base year is 2026, the horizon is 2036, values are nominal USD, and the geography is the United States.

## Current View

The expected 2026 market value is approximately `$7B`, with a plausible range of roughly `$5.5B-$9B`. Hims & Hers is the strongest anchor: it reported `$2.21B` of U.S. revenue in 2025, then `$608.1M` of total revenue and nearly 2.6 million subscribers in Q1 2026. Q1 revenue grew only `4%` during its U.S. weight-loss transition, but management raised full-year total-revenue guidance to `$2.8B-$3.0B` and expects growth to accelerate; international operations and the different economics of its weight-loss mix prevent using that guidance as a pure U.S. number. BetterHelp reported `$950M` of global 2025 segment revenue, down `9%`, with average monthly paying users down `5%`; its U.S. share and exact 2026 run-rate are not disclosed. Ro is private; the latest usable outside estimate was a roughly `$598M` annualized revenue run-rate in 2024. LifeMD reported 328,000 active patient subscribers at year-end 2025 and remains much smaller by revenue.

Those named anchors imply about `$4B` after estimating U.S. shares and rolling them into 2026. The remaining approximately `$3B` represents Noom, WeightWatchers Clinic, Thirty Madison/Nurx, Talkspace's direct consumer channel, Sesame, condition-specific providers, and other private platforms. Hims & Hers' Q1 softness does not change the rounded market estimate because its raised annual guide implies a sharp acceleration later in 2026 and the estimate already discounts its international revenue. The residual remains deliberately broad: private-company accounts and gross-versus-net drug accounting are not observable enough to support false precision.

The penetration series is an analyst reconstruction, not a published market series. It triangulates disclosed subscribers at Hims & Hers, BetterHelp, LifeMD, and WeightWatchers Clinic with estimated private-platform users and the specialty tail, then divides de-duplicated annual active buyers by U.S. adults. The observed 2026 input is `4.0%`; the blended curve smooths that to `3.6%`, about 9.8 million active buyers and roughly `$710` of annual recognized revenue per buyer. Broad telemedicine surveys report much higher usage because they include insurer, employer, and traditional-provider visits; they are useful only as an upper-bound check.

## Adoption Path

The selected analogs balance a fast, app-delivered subscription (`us-streaming-svod`) with recurring paid access and meaningful friction (`us-cable-tv`), broad digital adoption on an existing channel (`us-internet-adults`), and a deliberately slow anchor (`us-home-computer`). The asserted ceiling is `25%` of U.S. adults in a year: the category can expand far beyond today's stigmatized or convenience-led conditions, but a majority of adults should continue to obtain most care through insurance-led, employer-led, pharmacy-led, or traditional-provider channels. Because the market series is early, reconstructed, and well below one-third of the ceiling, the target fit is capped at a `35%` weight.

The blended logistic curve has a `25%` ceiling, `2032.6` midpoint, and `0.267` steepness. It projects penetration from `3.6%` in 2026 to `17.8%` in 2036. The size bridge treats U.S. adults as growing from about 270 million to 280 million over the same period. Annual recognized revenue per active buyer rises from about `$710` to roughly `$1,100` nominally as expensive chronic treatments, diagnostics, longitudinal primary care, and multi-condition relationships take more mix; ordinary inflation contributes part, but not all, of this increase.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| U.S. adults | 270M | 280M | Census projection, rounded |
| Active-buyer penetration | 3.6% | 17.8% | Blended logistic curve |
| Active buyers | 9.8M | 49.9M | Adults multiplied by modeled penetration |
| Annual revenue per active buyer | ~$710 | ~$1,100 | Nominal recognized revenue; richer treatment mix |
| Annual market value | `$7B` | `$55B` | Expected value; rounded |

The `$55B` expected 2036 value has a rough `$30B-$90B` plausible range. The largest sensitivities are adoption outside today's lifestyle conditions, the share of obesity and chronic-care drug economics retained by platforms, and whether platforms deepen into multi-condition longitudinal care or remain high-churn acquisition funnels. The expected value implies a roughly `23%` nominal CAGR; Hims & Hers' reiterated target of at least `$6.5B` revenue in 2030 provides a company-specific cross-check that the category can sustain high growth for several more years, but it is not treated as market evidence by itself.

## Market Structure

Direct network effects are weak: another patient rarely improves a patient's care. Scale still matters through national advertising, brand trust, clinician operations, pharmacy purchasing and fulfillment, compliance, fixed technology, and the ability to spread product-development cost across conditions. Proprietary longitudinal data can improve personalization and retention, but clinical protocols and general models are replicable and the returns to more data are uncertain. Regulation creates real operating hurdles without capping the number of entrants. Switching costs are moderate at most because subscriptions can be cancelled and prescriptions or care can move, although accumulated history and multi-condition convenience increase stickiness.

The model yields a `31.1%` horizon leader share and HHI of `0.181`, equivalent to about 5.5 equally sized competitors. This is just inside the concentrated range and is directionally consistent with national brand and fulfillment scale supporting a small group of platforms while condition-level specialists preserve a tail. It also sits near the model corpus's U.S. cloud infrastructure and health/personal-care retail anchors rather than its winner-take-most consumer platforms. Confidence is lowest on data advantage and switching costs; evidence that would raise it is cohort-level multi-condition retention and demonstrated outcome improvement attributable to proprietary longitudinal data, which public filings do not currently disclose.

## Players

The current ranking uses whole-market 2026 estimates, not shares of the named subset. Hims & Hers is rank one at approximately `30%`, based primarily on its disclosed U.S. revenue and 2026 guidance. Ro is placed second at `11%` and BetterHelp third at `10%`; the difference is within the uncertainty of Ro's private revenue and BetterHelp's undisclosed U.S. mix, so these two ranks should be treated as provisional.

Hims & Hers can defend leadership through brand, acquisition scale, vertically integrated pharmacy and diagnostics, a broadening condition set, and cross-sell into personalized multi-condition care. Its Q1 2026 GLP-1 reset illustrates the counter-case: it can lose capture if regulatory constraints weaken compounded-drug economics, branded drug manufacturers control the patient relationship, or high marketing intensity masks weak long-term retention.

Ro has a similar vertically integrated consumer model and a strong obesity franchise, but private disclosure makes its current economics and momentum hard to verify. BetterHelp has a trusted mental-health brand and provider-matching scale, but paying users declined to 390,000 in 2025 and its single-specialty model may capture less revenue per buyer than medication-heavy platforms. WeightWatchers, Noom, Thirty Madison, Amazon, large pharmacies, and manufacturer-direct channels are credible outside contenders; their inclusion as named horizon winners would require a company-specific override rather than pretending the pooled mobility model sees their strategy.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Hims & Hers | 31.1% | 24.4% | `$13.4B` |
| Ro | 21.2% | 15.8% | `$8.7B` |
| BetterHelp | 14.5% | 11.4% | `$6.3B` |

The mobility-adjusted view is canonical. It discounts every incumbent for rank churn, a `10.1%` pooled gone probability, and entry from outside today's top three; the gone probability is already embedded and is not applied again. Hims & Hers' unusually wide current share lead helps it retain more capture than the lower-ranked platforms, but the model does not see company-specific execution or momentum. No player override is used on this first pass.

## Watch

Replace the reconstructed penetration series with a repeatable annual consumer survey or de-duplicated claims/payment dataset if one becomes available. Verify Ro, Noom, and Thirty Madison revenue and active-patient figures; re-rank Ro and BetterHelp when U.S.-only figures can be separated. Track whether Hims & Hers delivers the second-half acceleration embedded in its raised 2026 guide, alongside U.S. revenue, subscriber growth, multi-condition adoption, and long-term cohort retention. Track platform gross-versus-net accounting for branded and compounded drugs, FDA and state action on personalized compounding, the durability of federal telemedicine prescribing flexibilities, manufacturer-direct GLP-1 channels, and whether payer coverage expands or displaces cash-pay demand.

## Peer Comparison

Published forecasts are not consistent enough to provide a clean independent estimate. Reports using nearly identical market names differ by more than sixfold at the starting point, largely because “DTC telehealth” can mean virtual-care service or software revenue, consumer healthcare spend, or an integrated platform's recognized care-and-product revenue. Our `$7B` in 2026 and `$55B` in 2036 retain the market contract above; the comparisons below are benchmarks only and did not change any stored input.

| Publisher | Publication | Forecast | At a glance | Boundary and comparison |
| --- | --- | --- | --- | --- |
| Grand View Research, republished by Research and Markets | August 2024; 2023–2030 | `$1.47B` in 2023 to `$9.53B` in 2030; `30.3%` stated CAGR; USD revenue | **40% under our 2030 estimate** | U.S. “DTC telehealth services,” segmented by delivery technology and interaction type. Its service-oriented boundary appears to omit much of the prescription and product revenue recognized by integrated platforms: Hims & Hers' U.S. revenue alone reached `$2.21B` in 2025. Our interpolated 2030 value is about `$16B`, above this forecast because our boundary includes fulfilled treatments and products even though our implied `22.9%` CAGR is slower. |
| Emergen Research | Page accessed August 2, 2026; 2024–2034 | `$9.5B` in 2024 to `$30.2B` in 2034; `12.2%` stated CAGR; USD revenue | **16% under our 2034 estimate** | Nominally U.S. DTC telehealth services, but the report includes remote monitoring and mobile apps, employer and healthcare-provider end users, and B2B-oriented competitors. Its starting value is therefore broader than our consumer-platform boundary. Its 2034 forecast is below our interpolated `$36B`; extrapolating its stated CAGR two years gives about `$38B` in 2036, inside our `$30B-$90B` range but below the `$55B` expected value. |
| Mordor Intelligence | February 2025; 2025–2030 | `$66.75B` in 2025 to `$198.77B` in 2030; `24.39%` stated CAGR; USD market value | **1,142% over our 2030 estimate**; not comparable | All U.S. telehealth: products and services across telemedicine, patient monitoring, education, healthcare facilities, and homecare. Named suppliers include Philips, GE HealthCare, Oracle, Siemens, and Amwell. This is an outer-category benchmark, not a comparable revenue pool; its much larger values mainly demonstrate why hospital, enterprise, equipment, and payer-led telehealth must remain excluded. |
| Hims & Hers | May 2026 company outlook; 2030 | At least `$6.5B` total company revenue in 2030 | **59% under our 2030 market estimate**; not comparable | A participant target rather than a market forecast, and it includes non-U.S. operations. Against our interpolated `$16B` U.S. market in 2030, `$6.5B` would equal roughly `41%`, but that ratio is not a valid share forecast because the numerator is global and the mobility model applies at 2036. It is still a useful lower-bound check: if Hims & Hers approaches its target, a service-only `$9.53B` U.S. category cannot represent the integrated care-and-product boundary used here. |

Fresh page checks on August 2, 2026 reconfirmed the three published market forecasts and units above; none supplies a closer match to the integrated-platform recognized-revenue boundary. The closest directional agreement remains Emergen's slower-growth case, which reaches the lower half of our 2036 range after horizon alignment. Grand View's higher growth rate supports rapid adoption but its absolute values conflict with disclosed integrated-platform revenue, while broad telehealth forecasts are too expansive to adjudicate our estimate. The comparison therefore increases confidence in the direction and plausible range, not in the `$55B` point estimate; resolving the point estimate still requires a boundary-matched dataset covering private platforms and consistent gross-versus-net drug accounting.

## Sources

- Hims & Hers Health, 2025 Form 10-K, U.S. revenue, subscriber definitions, conditions served, and revenue recognition: https://www.sec.gov/Archives/edgar/data/1773751/000177375126000022/hims-20251231.htm
- Hims & Hers Health, May 11, 2026 Q1 earnings release, revenue, subscriber count, U.S. weight-loss transition, 2026 guidance, and 2030 target: https://www.sec.gov/Archives/edgar/data/1773751/000177375126000074/hims-20260331x8xkearningsr.htm
- Teladoc Health, 2025 Form 10-K, BetterHelp revenue and paying users: https://www.sec.gov/Archives/edgar/data/1477449/000147744926000012/tdoc-20251231.htm
- LifeMD, 2025 Form 10-K, active patient subscribers and telehealth model: https://www.sec.gov/Archives/edgar/data/948320/000149315226009549/form10-k.htm
- WW International, 2025 Form 10-K, WeightWatchers Clinical offering and subscribers: https://www.sec.gov/Archives/edgar/data/105319/000119312526107176/ww-20251231.htm
- Talkspace, 2025 Form 10-K, direct-consumer revenue: https://www.sec.gov/Archives/edgar/data/1803901/000119312526105146/talk-20251231.htm
- Sacra, Ro revenue estimate, 2024 annualized basis: https://sacra.com/c/ro/
- U.S. Census Bureau, National Population Projections: https://www.census.gov/programs-surveys/popproj.html
- CDC/NCHS Data Brief 445, telemedicine use among U.S. adults in 2021; broad-boundary upper check: https://www.cdc.gov/nchs/products/databriefs/db445.htm
- FDA, concerns and current policy context for unapproved compounded GLP-1 drugs: https://www.fda.gov/drugs/drug-alerts-and-statements/fdas-concerns-unapproved-glp-1-drugs-used-weight-loss
- Grand View Research, “U.S. Direct To Consumer Telehealth Services Market,” August 2024, report details republished by Research and Markets: https://www.researchandmarkets.com/report/united-states-direct-to-consumer-telehealth-services-market
- Emergen Research, “US Direct To Consumer Telehealth Services Market Size, Growth Outlook 2034,” accessed August 2, 2026: https://www.emergenresearch.com/industry-report/us-direct-to-consumer-telehealth-services-market
- Mordor Intelligence, “United States Telehealth Market Size & Growth to 2030,” updated February 6, 2025: https://www.mordorintelligence.com/industry-reports/united-states-telehealth-market
