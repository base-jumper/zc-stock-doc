---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 300.0
  maturity-market-value: 410.0
concentration:
  inputs:
    traits:
      network-effects:      {score: 0.03, confidence: 0.95}
      data-scale-advantage: {score: 0.10, confidence: 0.80}
      brand-reputation:     {score: 0.20, confidence: 0.80}
      capital-intensity:    {score: 0.95, confidence: 0.95}
      scale-economies:      {score: 0.80, confidence: 0.90}
      regulatory-barriers:  {score: 0.90, confidence: 0.95}
      switching-costs:      {score: 0.20, confidence: 0.85}
  override:
    s1: 0.09
    r: 0.78
    reason: "Observed 2025 company shares are much flatter than the cross-market trait model: the leader is about 9% and FCX reports the top ten producers together supply only 38% of world mined copper. Fungibility, geographically dispersed orebodies and state-backed operators should preserve a large fringe through 2036."
  model-estimate:
    s1: 0.298047
    r: 0.678997
  hhi: 0.020684
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: BHP
        ticker: BHP
        share: 0.087
      - rank: 2
        name: Codelco
        share: 0.062
      - rank: 3
        name: Freeport-McMoRan
        ticker: FCX
        share: 0.050
      - rank: 4
        name: Zijin Mining
        ticker: 2899.HK
        share: 0.047
      - rank: 5
        name: Glencore
        ticker: GLEN.L
        share: 0.037
  override:
    - name: Freeport-McMoRan
      ticker: FCX
      capture: 0.055
      reason: "FCX's disclosed 2025 net-equity share was about 5%. A modest 2036 gain to 5.5% balances Grasberg's recovery and Kucing Liar, leach initiatives and possible Bagdad/El Abra growth against execution, ownership, depletion and permitting risk."
    - name: Ivanhoe Mines
      ticker: IVN.TO
      capture: 0.008
      reason: "Ivanhoe is outside the modeled current top five, so a company-specific 0.8% capture replaces the pooled mobility base rate. It represents about 205 kt of attributable 2036 copper: roughly 198 kt from Ivanhoe's 39.6% interest in Kamoa-Kakula at the independently supported >500 ktpa project rate from 2028, plus about 4 kt from its 64% interest in Platreef's funded Phase 2 6 ktpa copper output and a small operating allowance. It gives no production credit to unsanctioned Western Forelands discoveries or Platreef Phase 3."
  model-estimate:
    - rank: 1
      name: BHP
      ticker: BHP
      hold-position-capture: 0.09
      mobility-adjusted-capture: 0.069773
      mobility-adjusted-revenue: 28.60693
    - rank: 2
      name: Codelco
      hold-position-capture: 0.0702
      mobility-adjusted-capture: 0.05526
      mobility-adjusted-revenue: 22.6566
    - rank: 3
      name: Freeport-McMoRan
      ticker: FCX
      hold-position-capture: 0.054756
      mobility-adjusted-capture: 0.041783
      mobility-adjusted-revenue: 17.13103
    - rank: 4
      name: Zijin Mining
      ticker: 2899.HK
      hold-position-capture: 0.04271
      mobility-adjusted-capture: 0.032167
      mobility-adjusted-revenue: 13.18847
    - rank: 5
      name: Glencore
      ticker: GLEN.L
      hold-position-capture: 0.033314
      mobility-adjusted-capture: 0.02674
      mobility-adjusted-revenue: 10.9634
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---

# Global Primary Mined Copper

## Market Definition

**Market contract.** The market is worldwide primary copper contained in newly mined ore, concentrate, cathode and other first-sale forms. It includes copper recovered as the principal product or a mine by-product and values integrated mine output at an equivalent arm's-length mine-gate realization. It excludes recycled copper, smelting and refining fees, fabricated semis and products, streaming/royalty revenue, mining equipment and services, and the downstream value added to the same copper after its first sale.

The **revenue boundary** is producer-recognized revenue attributable to contained primary mined copper at its first external sale. A tonne of copper is counted once. Concentrate is valued net of treatment and refining charges; integrated cathode or rod is reduced to its mine-gate copper equivalent so refining and fabrication are not included. Gold, molybdenum, cobalt and other by-product revenue is excluded rather than credited against copper revenue.

The **addressable unit** is annual global copper use that can be supplied by either primary mines or recovered scrap. The **penetration measure** is primary mine supply as a `spend-share` of that annual copper requirement. It is not fitted with a logistic curve because the primary-versus-secondary mix is a commodity balance governed by scrap availability, collection economics and losses, not durable product adoption. The **billable unit** is a metric tonne of payable contained primary copper. End uses are aggregated because construction, grids, transport and industrial demand all buy into the same globally priced metal pool. Values are nominal USD in 2026 and 2036.

## Current View

USGS estimates world mine production at **23.0 Mt** in both 2024 and 2025. The IEA's independently compiled 2024 figure is **22.8 Mt**, while refined demand excluding direct-use scrap was **26.7 Mt**. The expected 2026 billable volume is **23.5 Mt**, reflecting a modest contribution from announced ramps but no assumption that the late-decade project pipeline closes the structural gap.

The expected 2026 market value is **$300bn**. The bottom-up bridge is 23.5 Mt multiplied by approximately **$5.80/lb** of payable contained copper, or about $12,800/t. This mine-gate realization is below FCX's second-quarter 2026 realized price of $6.17/lb and the quarter's $6.05/lb LME average, allowing for geographic price dispersion, concentrate deductions and a weaker first-quarter average. It is materially above the USGS 2025 LME average of $4.40/lb, consistent with the sharp market tightening visible by mid-2026.

The current company inputs use attributable or net-equity mined output divided by the 23 Mt global total. BHP's approximately 2.0 Mt is about 8.7%; Codelco's roughly 1.4 Mt is about 6.2%; FCX explicitly reports about **5%** and third place on Wood Mackenzie's 2025 net-equity basis; Zijin's approximately 1.1 Mt is about 4.7%; and Glencore's approximately 0.85 Mt is about 3.7%. Calendar and fiscal-year cutoffs differ slightly, so these are structural ranking inputs rather than precise revenue-accounting shares.

## Adoption Path

No logistic penetration block is configured. The relevant bridge is physical primary supply and mine-gate realization. In the IEA Stated Policies Scenario, total copper demand rises from **26.7 Mt in 2024 to 31.3 Mt in 2030 and 34.1 Mt in 2040**, while secondary supply and reuse rises from 4.4 Mt to 5.4 Mt and 8.7 Mt. Primary requirements therefore reach 25.9 Mt in 2030 and 25.4 Mt in 2040. Interpolation supports approximately **25.6 Mt** in 2036.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Total refined demand | 28.2 Mt | 33.0 Mt | IEA STEPS path; excludes direct-use scrap |
| Secondary supply and reuse | 4.7 Mt | 7.4 Mt | Rising collection and recycling, net of process losses |
| Primary mine-origin billable volume | **23.5 Mt** | **25.6 Mt** | Current production anchor and IEA primary-requirements path |
| Net mine-gate realization | **$5.80/lb** | **$7.30/lb** | Current payable realization; roughly 2.3% annual nominal increase |
| Annual market value | **$300bn** | **$410bn** | Rounded expected values; 3.2% nominal CAGR |

The expected 2036 value is **$410bn**, with a plausible range of roughly **$280bn-$600bn**. Volume is relatively bounded by demand, recycling and substitution; price is the dominant uncertainty because new supply must compensate for declining grades, depletion, long lead times and higher capital intensity. The IEA finds only 14 of 239 copper deposits discovered since 1990 were found in the past decade and reports a typical 17-year discovery-to-production lead time. The horizon price is not a spot forecast: it assumes current scarcity rents partly normalize, then the incentive price broadly keeps pace with inflation and mine-cost escalation. Mine-origin copper remains the only revenue stream.

## Market Structure

Copper has negligible network effects, weak brand differentiation and low buyer switching costs once chemistry and delivery are qualified. Entry barriers are nevertheless severe: tier-one orebodies are scarce, projects require multibillion-dollar capital, average grades are declining, permitting is long and jurisdiction-specific, and large mines benefit from infrastructure and processing scale. These mechanisms support durable incumbents without creating winner-take-most economics because ore deposits are geographically dispersed, the product is fungible and sovereign or state-backed operators can finance projects on non-commercial terms.

The structural trait model materially overpredicts concentration for this commodity boundary, producing a leader near 30%. The stored override instead uses a **9.0% leader share** and **0.78 rank decay**, consistent with the current leader and FCX's disclosure that the top ten producers supply only **38%** of world mined copper. The resulting **HHI is expected to remain extremely low**, around 0.021 or about 48 effective competitors. The geometric ranks represent about 41% of the market, leaving a large competitive fringe. This is a company-ownership view, not the more concentrated country view: the IEA expects the top three mining countries to rise from 48% in 2024 to 53% in 2040.

## Players

The current ranking is BHP, Codelco, Freeport-McMoRan, Zijin Mining and Glencore on an attributable or net-equity mine-output basis. It matches the market's producer ownership boundary more closely than consolidated operating volumes or refined-copper revenue.

The script-calculated views after applying the horizon concentration curve are:

| Current player | Hold current rank | Mobility-adjusted 2036 capture | Model-implied 2036 revenue |
|---|---:|---:|---:|
| BHP | 9.00% | **6.98%** | **$28.6bn** |
| Codelco | 7.02% | **5.53%** | **$22.7bn** |
| Freeport-McMoRan | 5.48% | **4.18%** | **$17.1bn** |
| Zijin Mining | 4.27% | **3.22%** | **$13.2bn** |
| Glencore | 3.33% | **2.67%** | **$11.0bn** |

FCX's canonical **5.5%** capture is an analyst override, so its canonical revenue differs from the unoverridden model revenue shown above. It is only modestly above the company's disclosed current **5%** share: Grasberg's return to normal rates, Kucing Liar's planned 2030s ramp, leach recovery initiatives, and possible Bagdad and El Abra expansions can support gains, but project sanction, ownership, permitting and depletion risks preclude a more aggressive assumption. At the $410bn market value, 5.5% implies approximately **$22.6bn** of 2036 mine-origin copper revenue attributable to FCX's economic interest.

Ivanhoe Mines is an outside contender rather than a sixth mobility-model input because the stored current ranking is limited to the market's top five. Its company-specific override is **0.8%**, implying **$3.28bn** of attributable 2036 primary mined copper revenue. The physical cross-check is approximately **205 kt** of attributable copper against the market's 25.6 Mt billable volume: about 198 kt from Ivanhoe's 39.6% interest in Kamoa-Kakula at the updated independent mine plan's more-than-500 ktpa project rate from 2028, about 4 kt from its 64% interest in Platreef Phase 2's approximately 6 ktpa copper output, and a small operating allowance. This is a conservative base case: it gives no production credit to Western Forelands, where early development work has begun but no economic study or production plan exists, or to the unsanctioned Platreef Phase 3 expansion.

The mobility model is a pooled 10-15 year base rate. It sees current rank and share spacing but not resource quality, sovereign ownership, project pipelines or company-specific noncontrolling interests. Its gone probability is already included in mobility-adjusted capture and is not applied again. FCX and Ivanhoe are the only company overrides.

## Watch

- IEA revisions to 2030-2040 primary requirements, recycling and the announced-project deficit.
- Mine commissioning, disruption and grade evidence at Escondida, Codelco, Grasberg, Kamoa-Kakula, Oyu Tolgoi, Collahuasi and Quebrada Blanca.
- Ivanhoe's 2027 Kamoa-Kakula life-of-mine plan, the ramp back above 500 ktpa, Platreef Phase 2 delivery and any economic study or sanction for Western Forelands.
- FCX's Grasberg ramp, Kucing Liar development, Indonesian ownership negotiations, leach-recovery run rate, and Bagdad/El Abra sanction decisions.
- LME and producer realizations versus treatment/refining charges and the $5.80/lb current anchor.
- Copper intensity and substitution in grids, data centres, EVs, industrial equipment and construction.
- Scrap collection, direct-use scrap and secondary-refining growth, which determine how much end demand reaches primary mines.
- Permitting lead times, capital intensity, ore-grade decline, tax/royalty changes and resource nationalism.

## Peer Comparison

- **Approximately 0% over/under our 2036 volume estimate:** the IEA's STEPS primary requirement is 25.9 Mt in 2030 and 25.4 Mt in 2040. Interpolation gives about 25.6 Mt in 2036, matching our billable-volume bridge. This is the principal physical benchmark, not an independent dollar forecast.
- **Not directly comparable on value:** the USGS values 1.0 Mt of 2025 U.S. mine production at $11bn while its global table reports 23 Mt of mine output. The U.S. value confirms the tonnes-times-realization method but cannot be grossed up cleanly because U.S. COMEX pricing, concentrate/cathode mix and domestic premiums differ from the world market.
- No credible public 5-10 year forecast was found that both publishes nominal dollar market value and isolates first-sale primary-mine copper revenue. Commercial "copper market" reports generally measure refined metal, semi-fabricated products or an undisclosed value-chain boundary; their headline values are not comparable enough to calculate a meaningful percentage difference.

## Sources

- U.S. Geological Survey, *Mineral Commodity Summaries 2026: Copper*, February 2026, pp. 72-73: https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf
- International Energy Agency, *Global Critical Minerals Outlook 2025*, May 2025, pp. 101-110: https://www.iea.org/reports/global-critical-minerals-outlook-2025
- Freeport-McMoRan, *2025 Form 10-K*, filed February 13, 2026: https://www.sec.gov/Archives/edgar/data/831259/000083125926000012/fcx-20251231.htm
- Freeport-McMoRan, *Second-Quarter and Six-Month 2026 Results*, July 23, 2026: https://www.sec.gov/Archives/edgar/data/831259/000083125926000033/a2q2026exhibit991.htm
- BHP, *Operational Review for the year ended 30 June 2025*, July 2025: https://www.bhp.com/investors/annual-reporting/annual-report-2025
- Codelco, *Annual Report 2025*: https://www.codelco.com/memoria-anual
- Zijin Mining, *2025 Annual Report*: https://www.zijinmining.com/global/investor/Financial-Reports.htm
- Glencore, *2025 Annual Report*: https://www.glencore.com/publications
- Ivanhoe Mines, *Updated, Independent Study Results for the Kamoa-Kakula Copper Complex*, March 31, 2026: https://www.ivanhoemines.com/news-stories/news-release/ivanhoe-mines-announces-updated-independent-study-results-for-the-kamoa-kakula-copper-complex/
- Ivanhoe Mines, *2026 Second-Quarter Financial Results, Overview of Operations and Exploration Activities*, July 29, 2026: https://www.ivanhoemines.com/news-stories/news-release/ivanhoe-mines-issues-2026-second-quarter-financial-results-overview-of-operations-and-exploration-activities/
