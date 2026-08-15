---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.85
  maturity-market-value: 2.4
concentration:
  inputs:
    traits:
      network-effects: {score: 0.05, confidence: 0.85}
      data-scale-advantage: {score: 0.20, confidence: 0.65}
      brand-reputation: {score: 0.65, confidence: 0.70}
      capital-intensity: {score: 0.55, confidence: 0.65}
      scale-economies: {score: 0.60, confidence: 0.65}
      regulatory-barriers: {score: 0.20, confidence: 0.75}
      switching-costs: {score: 0.75, confidence: 0.75}
  override:
    s1: 0.16
    r: 0.75
    reason: "The pooled trait model hits its 2% leader-share floor, contradicting the boundary-matched current ranking; qualification-protected specialists and diversified vendors support a persistent mid-teens leader alongside a long tail."
  model-estimate:
    s1: 0.02
    r: 0.966903
  hhi: 0.058514
  method: selected-direct-ridge
  date: 2026-08-03
players:
  inputs:
    current:
      - rank: 1
        name: Chroma ATE
        ticker: 2360.TW
        share: 0.16
      - rank: 2
        name: Cohu
        ticker: COHU
        share: 0.12
      - rank: 3
        name: Micro Control Company
        share: 0.08
      - rank: 4
        name: Aehr Test Systems
        ticker: AEHR
        share: 0.06
  model-estimate:
    - rank: 1
      name: Chroma ATE
      ticker: 2360.TW
      hold-position-capture: 0.16
      mobility-adjusted-capture: 0.120803
      mobility-adjusted-revenue: 0.289927
    - rank: 2
      name: Cohu
      ticker: COHU
      hold-position-capture: 0.12
      mobility-adjusted-capture: 0.096569
      mobility-adjusted-revenue: 0.231766
    - rank: 3
      name: Micro Control Company
      hold-position-capture: 0.09
      mobility-adjusted-capture: 0.072812
      mobility-adjusted-revenue: 0.174749
    - rank: 4
      name: Aehr Test Systems
      ticker: AEHR
      hold-position-capture: 0.0675
      mobility-adjusted-capture: 0.056901
      mobility-adjusted-revenue: 0.136562
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-03
---
# Global Semiconductor Wafer-Level and Package-Level Burn-In and Reliability Test Equipment

## Market Definition

**Market scope:** worldwide equipment used to electrically stress, monitor and reliability-screen semiconductor devices at wafer, singulated-die/module or packaged-device level. Included products are production and engineering burn-in/reliability systems, chambers and system electronics, full-wafer contactors, burn-in boards and device-interface carriers, loaders/aligners, system upgrades, spares and vendor service. Aehr's FOX wafer-level systems, WaferPak/DiePak interfaces and aligners, and Sonoma/Tahoe/Echo package-level systems are fully included. General-purpose automatic test equipment used only for short functional production test, probe stations without a burn-in/reliability function, outsourced test-lab service revenue, chip revenue, and internally built equipment with no third-party vendor revenue are excluded.

**Revenue boundary:** annual recognized revenue of equipment and interface vendors at the first external sale, including attached service. This is not semiconductor-manufacturer capital expenditure at channel resale value, test-house service revenue, or the value of semiconductors screened.

**Addressable unit and penetration:** the addressable unit is installed burn-in/reliability test capacity, expressed as device-hours at the required power, temperature, parallelism and monitoring level. Penetration is `spend-share`: the share of structurally eligible semiconductor production and qualification activity using third-party included equipment rather than no burn-in or captive equipment. Billable units are new and replacement systems, chambers, contact/interface sets, automation modules, upgrades, spares and service-years. Wafer-level and package-level equipment are modeled separately and aggregated at the same vendor-revenue boundary.

**Time and value basis:** 2026 base year, fixed 2036 horizon, nominal USD at approximately constant current exchange rates. The market contract is unchanged for size, concentration and player capture.

## Current View

The expected 2026 market value is **$0.85b**, with a rough **$0.6b-$1.2b** range. No public industry series exactly matches the contract. The strongest boundary-matched anchor is Aehr's audited FY2026 revenue: its 10-K reports $31.5m from wafer-level systems, WaferPak products and service and $18.5m from package-level systems and service, totaling $50.0m, all inside this boundary. An estimated 6% whole-market share grosses that to $0.83b; rounding to $0.85b recognizes larger diversified and private suppliers whose burn-in revenue is not separately disclosed.

This is deliberately far below all semiconductor ATE. SEMI's broader assembly-and-test-equipment statistics include handlers, probers and functional ATE that the contract excludes. The current estimate is low-to-moderate confidence because Chroma, Cohu and other diversified vendors do not report burn-in-only revenue and some Asian IC manufacturers use captive suppliers, as Aehr's 10-K notes.

## Adoption Path

The expected 2036 market is **$2.4b**, with a plausible **$1.4b-$4.0b** range. The bridge assumes installed third-party capacity roughly doubles as AI/HPC processors, silicon photonics, advanced multi-die packages, power semiconductors and high-reliability automotive/industrial devices require more device-hours and earlier screening. Nominal revenue per unit of effective capacity rises about 1%-2% annually as power density, cooling, monitoring and automation complexity more than offset same-product productivity and price pressure. Interfaces, boards, carriers, upgrades, spares and service grow with the installed base and represent about one-third of horizon revenue.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Third-party effective burn-in/reliability capacity | 1.0x | ~2.0x | More eligible device volume and more stress/monitoring intensity |
| Blended nominal revenue per unit of capacity | 1.0x | ~1.4x | Higher power/thermal complexity plus inflation, net of productivity |
| Systems and automation revenue | ~$0.60b | ~$1.60b | New installations plus replacement of an approximately 7-10 year durable base |
| Interfaces, upgrades, spares and service | ~$0.25b | ~$0.80b | Recurring installed-base ecosystem revenue |
| Annual market value | **$0.85b** | **$2.40b** | Vendor-recognized revenue, rounded expected value |

The implied CAGR is 10.9%. The durable-equipment check includes both growth installations and replacement: at the horizon, replacement of a larger 7-10 year installed base is material but new capacity for AI/HPC, photonics and power devices remains the larger systems driver. The main sensitivities are whether production burn-in migrates from package/system level to wafer level, AI-package power and volumes, silicon-photonics screening intensity, power-semiconductor recovery, useful life and customer self-build.

No logistic penetration block is configured because there is no consistent whole-market series for paid third-party burn-in capacity. The capacity and spend-share assumptions are disclosed sizing judgments, not a fitted adoption curve.

## Market Structure

Network effects are negligible: one customer's system does not improve another's. Data feedback is useful for diagnostics but customers own most device and yield data. Scale and reputation matter through power electronics, thermal engineering, software, global support and the cost of qualifying platforms. Capital requirements are meaningful but well below wafer-fab economics. Regulation does not limit vendor count, although automotive, aerospace and customer reliability standards raise qualification burden. Switching costs are high after a system, contactor or board set is correlated and qualified for a production device, but they protect several incumbents rather than one universal leader.

The unadjusted structural model hits its 2% leader-share floor and implies an HHI below 0.01. That is inconsistent with the boundary-matched current ranking and with the qualification-protected specialist platforms described in supplier filings. The documented override retains a 16% horizon leader, a 0.75 rank-decay ratio and a substantial long tail; its HHI remains fragmented-to-moderately concentrated rather than winner-take-most. A shift toward standardized high-power platforms could raise concentration; customer-designed systems, regional suppliers and device-specific interfaces could lower it.

## Players

Current shares are analyst estimates on the whole contract: Chroma ATE 16%, Cohu 12%, Micro Control 8% and Aehr 6%, leaving 58% for Advantest and other diversified vendors, regional specialists, board/interface suppliers and the competitive tail. These are not a published share table. Aehr's 6% is the only directly reconciled input: $50.0m audited FY2026 revenue divided by the $0.85b market equals 5.9%. Chroma, Cohu and Micro Control rank above Aehr based on their broader installed product portfolios and burn-in offerings, but their included revenue is not separately disclosed, so ranking confidence is low.

Aehr can gain rank because its FOX platform screens whole wafers or many die in parallel, proprietary WaferPak/DiePak interfaces create follow-on revenue, and Sonoma extends it into ultra-high-power packaged AI processors. Its July 2026 release reported $100.6m effective backlog and FY2027 revenue guidance of $130m-$150m, evidence the current fiscal-year share understates near-term momentum. It can lose capture if lead-customer programs do not broaden, customers self-build, larger ATE vendors integrate burn-in, or qualification, power delivery and manufacturing execution falter. The pooled mobility model intentionally does not convert that momentum into a company-specific override.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Chroma ATE | 16.00% | 12.08% | $289.9m |
| Cohu | 12.00% | 9.66% | $231.8m |
| Micro Control Company | 9.00% | 7.28% | $174.7m |
| Aehr Test Systems (AEHR) | 6.75% | **5.69%** | **$136.6m** |

Mobility allows for rank churn, entry from outside the current top four, the competitive fringe and a pooled 10.06% gone probability already embedded in adjusted capture. Aehr's positive $136.6m model revenue equals 5.69% of the $2.4b 2036 market. It is close to management's FY2027 guidance midpoint, but that agreement is coincidental: the model uses current rank/share and pooled historical transitions, not Aehr's backlog, customer momentum, moat or strategy. No player override is used.

## Watch

- Aehr FY2027 revenue conversion versus $130m-$150m guidance and diversification beyond lead AI customers.
- Boundary-matched burn-in/reliability revenue or share disclosure from Chroma, Cohu, Advantest and Micro Control.
- AI-accelerator package power, production volume and the split between wafer-, package- and system-level burn-in.
- Silicon-photonics and co-packaged-optics production screening requirements.
- WaferPak, DiePak, boards, fixtures, service and upgrades as a share of installed-base revenue.
- Customer self-build and captive Asian equipment suppliers.

## Peer Comparison

No independent forecast was found with this exact vendor-recognized boundary. Two newly published system-only forecasts are nevertheless useful directional checks. Our interpolated 2035 value is approximately **$2.16b**:

- SNS Insider (2026) estimates **$868.4m in 2026** and **$1.807b in 2035**, an 8.48% CAGR. Its 2035 value is **16% below our estimate**. The current value nearly matches our $0.85b anchor, but the report is framed around burn-in *systems* and does not clearly include contactors, boards, carriers, spares and vendor service, making its horizon value narrower and not strictly comparable.
- Industry Research (2026) estimates **$949.7m in 2026** and **$1.961b in 2035**, an 8.3% CAGR. Its 2035 value is **9% below our estimate**. It likewise describes system/chamber shipments and does not establish inclusion of our installed-base ecosystem streams, so the arithmetic is boundary-mismatched.

The peers' 8.3%-8.5% growth rates are below our 10.9% through 2036. The gap is plausible only if high-power AI/HPC platforms, wafer-level screening and attached interfaces/service outgrow conventional chambers; failure of those mix shifts would move the outcome toward the peer path. Broader semiconductor-test forecasts generally include short-duration functional ATE, handlers and probers and remain unusable. Aehr's own FY2027 guidance is company revenue, not a market forecast; at the midpoint it would equal roughly 15% of the current $0.85b pool before market growth, underscoring momentum but not defining 2036 market size.

## Sources

- Aehr Test Systems, FY2026 Form 10-K filed 27 July 2026, especially product definitions, $31.5m wafer-level and $18.5m package-level revenue, competition and system qualification: https://www.sec.gov/Archives/edgar/data/1040470/000165495426006919/aehr_10k.htm
- Aehr Test Systems, “Reports Fiscal 2026 Fourth Quarter and Full Year Financial Results with Record Quarterly Bookings and $100 Million Effective Backlog,” 14 July 2026: https://www.aehr.com/2026/07/aehr-test-systems-reports-fiscal-2026-fourth-quarter-and-full-year-financial-results-with-record-quarterly-bookings-and-100-million-effective-backlog/
- Aehr Test Systems, FOX and package-level product overview, accessed 3 August 2026: https://www.aehr.com/products/
- Micro Control Company, high-power burn-in systems and burn-in-board product overview, accessed 3 August 2026: https://www.microcontrol.com/high-power-burn-in-systems/
- Chroma ATE, semiconductor/IC test product overview, accessed 3 August 2026: https://www.chromaate.com/en/products_list/soc_test_system
- Cohu, semiconductor test and inspection product overview, accessed 3 August 2026: https://www.cohu.com/semiconductor-test-and-inspection/
- SEMI, annual semiconductor equipment sales and forecast publications, reviewed as a broader-boundary check: https://www.semi.org/en/news-resources/press-releases
- SNS Insider, “Burn-In Test System for Semiconductor Market Size Report 2035,” 2026; $868.4m in 2026 and $1.807b in 2035: https://www.snsinsider.com/reports/burn-in-test-system-for-semiconductor-market-9262
- Industry Research, “Burn-In Test System for Semiconductor Market Growth & Size,” 2026; $949.7m in 2026 and $1.961b in 2035: https://www.industryresearch.biz/market-reports/burn-in-test-system-for-semiconductor-market-116677
