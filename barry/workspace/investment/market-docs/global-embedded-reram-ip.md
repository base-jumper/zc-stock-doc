---
base-year: 2026
currency: AUD
maturity-duration: 10
size:
  current-market-value: 0.04
  maturity-market-value: 0.4
concentration:
  inputs:
    traits:
      network-effects: {score: 0.25, confidence: 0.50}
      data-scale-advantage: {score: 0.35, confidence: 0.45}
      brand-reputation: {score: 0.45, confidence: 0.55}
      capital-intensity: {score: 0.45, confidence: 0.55}
      scale-economies: {score: 0.65, confidence: 0.60}
      regulatory-barriers: {score: 0.30, confidence: 0.60}
      switching-costs: {score: 0.80, confidence: 0.70}
  model-estimate:
    s1: 0.166467
    r: 0.832118
  hhi: 0.090095
  method: selected-direct-ridge
  date: 2026-08-02
players:
  inputs:
    current:
      - rank: 1
        name: Weebit Nano
        ticker: WBT.AX
        share: 0.34
      - rank: 2
        name: Crossbar
        share: 0.22
      - rank: 3
        name: eMemory
        ticker: 3529.TWO
        share: 0.14
  model-estimate:
    - rank: 1
      name: Weebit Nano
      ticker: WBT.AX
      hold-position-capture: 0.166467
      mobility-adjusted-capture: 0.13464
      mobility-adjusted-revenue: 0.053856
    - rank: 2
      name: Crossbar
      hold-position-capture: 0.13852
      mobility-adjusted-capture: 0.114668
      mobility-adjusted-revenue: 0.045867
    - rank: 3
      name: eMemory
      ticker: 3529.TWO
      hold-position-capture: 0.115265
      mobility-adjusted-capture: 0.098799
      mobility-adjusted-revenue: 0.03952
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-02
---
# Global Embedded ReRAM IP

## Market Definition

**Market scope:** worldwide third-party embedded resistive-RAM (ReRAM/RRAM) intellectual property used in semiconductor process platforms and system-on-chip designs. Included products are technology licences, process-transfer and integration work, non-recurring engineering (NRE), qualification fees, and production royalties for embedded ReRAM. Standalone memory chips, foundry wafer revenue, customer chip revenue, other emerging memories such as MRAM and FeRAM, conventional embedded flash, and the imputed value of internally developed ReRAM are excluded.

**Revenue boundary:** annual recognized revenue of the third-party ReRAM technology provider. This is not end-customer semiconductor spend, ReRAM device value, foundry wafer revenue, or the value of chips containing ReRAM.

**Addressable unit and penetration:** the stable denominator is annual semiconductor production value that could structurally use embedded ReRAM. Penetration is the `spend-share` of that production value using externally licensed ReRAM rather than internally developed memory. Billable units are licence and technology-transfer projects plus royalty-bearing chip production.

**Segments and value basis:** licence/NRE revenue and production royalties are modeled separately, then aggregated at provider-recognized value. The base year is 2026, the fixed horizon is 2036, and values are nominal AUD using approximately constant current foreign-exchange rates. The contract remains global and unchanged across sizing, concentration, and player capture.

## Current View

The current market is too young for a reliable published revenue series. Weebit's 31 July 2026 quarterly report upgraded unaudited FY26 revenue guidance to at least A$13.5m and disclosed A$3.4m of fourth-quarter customer receipts comprising licensing fees and NRE. This is the strongest boundary-matched public anchor. Grossing the revenue floor up at an estimated 34% share gives a roughly A$40m 2026 market (`A$13.5m / 34% = A$39.7m`). This triangulation is low confidence: Crossbar is private, eMemory does not separately disclose RRAM revenue, and licence milestones make annual revenue lumpy.

The present pool is dominated by licence, transfer, NRE, and qualification payments. Royalty revenue should dominate only after customer designs pass qualification and reach volume production. Weebit reported three customer chip-design tape-outs by July 2026, one already functional, but said product testing and qualification can take 12–18 months before mass production.

## Adoption Path

The 2036 A$0.40b expected market value is a revenue-intensity bridge, not the broader chip-market TAM. Yole's 2023 publication estimated embedded emerging-NVM device revenue of about US$2.7b in 2028. Weebit's January 2026 disclosure cites a later Yole forecast of US$3.26b in 2030, with ReRAM exceeding half and growing 45-fold over six years. Extending the device-level pool to 2036, restricting it to designs using external IP, and applying blended licence, NRE, and royalty economics supports a provider-revenue pool near A$0.4b, but the conversion is not independently published.

The downside case is about A$0.2b if foundries and IDMs retain most economics internally and royalties remain narrow; the reference case is A$0.4b as externally licensed ReRAM gains meaningful advanced-node share; and the upside case is about A$0.8b if ReRAM becomes a common embedded-flash successor and multiple high-volume platforms pay third-party royalties. The stored A$0.4b is a rounded probability-weighted expectation. ReRAM adoption versus MRAM, FeRAM, and flash, the externally licensed share, and royalty realization are the dominant sensitivities.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Third-party embedded ReRAM IP market value | A$0.04b | A$0.40b | Provider-recognized licence, NRE and royalty revenue |
| Revenue mix | Licence/NRE dominated | Royalty dominated | Volume follows qualification and customer production |
| Boundary-matched revenue anchor | Weebit ≥A$13.5m | No direct public forecast | Current guidance; horizon scenario bridge |
| Implied market CAGR | — | 25.9% | Ten-year growth from A$0.04b to A$0.40b |

The addressable denominator is semiconductor production value, so no durable-equipment installed-base replacement calculation applies. Royalties recur with annual chip production; licence and NRE fees are modeled as the project flow enabling that production. Adjacent standalone memory, compute-in-memory chip sales, and foundry manufacturing revenue remain excluded.

## Market Structure

Qualification across a process node and redesign risk create high switching costs, while foundry/IDM trust, reliability data, and process-transfer experience provide moderate scale and reputation advantages. Direct network effects are weak, fabrication capital is borne largely by licensees, and patents and qualification standards create barriers without preventing alternative memory technologies from competing. These traits support a fragmented-to-moderately concentrated mature revenue pool rather than a single winner.

The structural scores are intentionally separated from the current share estimates. Confidence is moderate at best because today's market is pre-royalty and annual milestone revenue can distort ranks. Developments that could raise concentration include one IP becoming standard across several leading process platforms; foundry-owned implementations, alternative NVM adoption, or customer multi-sourcing would lower it.

## Players

Current shares are analyst estimates on the defined third-party embedded-ReRAM-IP boundary: Weebit 34%, Crossbar 22%, and eMemory 14%, leaving 30% for other private, university-linked, and specialist providers. They are anchored to Weebit's A$13.5m FY26 revenue guidance and public evidence that Crossbar and eMemory offer ReRAM/RRAM technology, but are not sourced from a published market-share table. Crossbar's current site confirms active 22nm ReRAM technology and more than 200 patents but gives no licensing revenue; eMemory's public material confirms embedded-memory IP activity without separately identifying RRAM revenue. The ranking is therefore the weakest model input and should be replaced when boundary-matched revenue becomes available.

Weebit's current lead is supported by qualified IP at DB HiTek and SkyWater, licences with Texas Instruments and onsemi, and three customer tape-outs. Its risks are slow qualification, customers developing internally, alternative emerging memories, and royalty terms or product volumes below expectations. Crossbar has long-standing ReRAM IP and could regain rank as it commercializes advanced-node and security architectures. eMemory brings a broad logic-NVM customer and foundry ecosystem, but its RRAM revenue is not separately visible.

The concentration curve assigns Weebit 16.65% capture if it holds rank one. The pooled mobility model reduces this to 13.46%, or A$53.9m of 2036 revenue, after allowing for rank churn, the competitive fringe, and a 10.06% gone probability that is already included. Crossbar moves from 13.85% hold-position capture to 11.47% mobility-adjusted capture (A$45.9m), while eMemory moves from 11.53% to 9.88% (A$39.5m). Mobility is especially material because current revenue is lumpy and outside contenders can reshape the market before royalties scale; no company-specific override is used.

## Watch

- First disclosed production royalty revenue and the royalty rate or chip-volume bridge.
- Completion of Texas Instruments and onsemi transfer/qualification and movement into production.
- Whether DB HiTek customer products complete their stated 12–18 month qualification path.
- Independent embedded-ReRAM IP revenue or share data for Crossbar, eMemory, and private competitors.
- Updated Yole/Omdia forecasts separating ReRAM device value from licensor revenue.
- MRAM, FeRAM, and embedded-flash cost/performance at sub-28nm nodes.

## Peer Comparison

**Not comparable — broader device-revenue boundary:** Yole Group's 2023 forecast of about US$2.7b of embedded emerging-NVM revenue in 2028 is far above our interpolated A$0.063b IP-provider revenue in that year, but the arithmetic percentage is not meaningful because Yole measures embedded-memory device value while this document measures third-party licence, NRE, and royalty revenue.

**Not comparable — broader device-revenue boundary:** the later Yole forecast cited by Weebit puts embedded emerging NVM at US$3.26b in 2030, with ReRAM exceeding half. Our interpolated IP-provider path is about A$0.10b in 2030. Again, a percentage over/under would falsely compare device-market value with licensor revenue. No independent 5–10 year forecast with the same narrow revenue boundary was found, so the sizing remains low confidence.

## Sources

- Weebit Nano, “Weebit Nano expands licensing agreements with key customers; three customer chip designs taped-out to-date,” 31 July 2026: https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/
- Weebit Nano, “Weebit Nano signs largest customer to date; technology qualified at DB HiTek,” 30 January 2026; includes the company-cited Yole forecast: https://www.weebit-nano.com/news/press-releases/weebit-nano-signs-largest-customer-to-date-technology-qualified-at-db-hitek/
- Weebit Nano, “Weebit Nano achieves record half-year revenue; licenses ReRAM to Tier-1 Texas Instruments,” 27 February 2026: https://www.weebit-nano.com/news/press-releases/weebit-nano-achieves-record-half-year-revenue-licenses-reram-to-tier-1-texas-instruments/
- Yole Group, “Emerging Non-Volatile Memory: all eyes on embedded applications,” 2023; embedded-ENVM device-revenue forecast: https://www.yolegroup.com/press-release/yg-press-news-emerging-non-volatile-memory-all-eyes-on-embedded-applications/
- Crossbar, company and ReRAM technology overview, accessed 2 August 2026: https://crossbar-inc.com/
- eMemory Technology, company and RRAM product overview, accessed 2 August 2026: https://www.ememory.com.tw/en-US
