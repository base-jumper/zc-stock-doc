---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 12.0
  maturity-market-value: 32.0
concentration:
  inputs:
    traits:
      network-effects:      {score: 0.05, confidence: 0.90}
      data-scale-advantage: {score: 0.20, confidence: 0.75}
      brand-reputation:     {score: 0.45, confidence: 0.80}
      capital-intensity:    {score: 0.90, confidence: 0.95}
      scale-economies:      {score: 0.75, confidence: 0.85}
      regulatory-barriers:  {score: 0.90, confidence: 0.95}
      switching-costs:      {score: 0.40, confidence: 0.75}
  model-estimate:
    s1: 0.213506
    r: 0.764654
  hhi: 0.109763
  method: selected-direct-ridge
  date: 2026-08-08
players:
  inputs:
    current:
      - rank: 1
        name: Kazatomprom
        ticker: KAP.L
        share: 0.2070
      - rank: 2
        name: Cameco
        ticker: CCJ
        share: 0.1693
      - rank: 3
        name: Orano
        share: 0.1132
      - rank: 4
        name: Uranium One
        share: 0.0968
      - rank: 5
        name: CGN
        ticker: 1164.HK
        share: 0.0957
  model-estimate:
    - rank: 1
      name: Kazatomprom
      ticker: KAP.L
      hold-position-capture: 0.213506
      mobility-adjusted-capture: 0.160424
      mobility-adjusted-revenue: 5.133568
    - rank: 2
      name: Cameco
      ticker: CCJ
      hold-position-capture: 0.163258
      mobility-adjusted-capture: 0.128724
      mobility-adjusted-revenue: 4.119168
    - rank: 3
      name: Orano
      hold-position-capture: 0.124836
      mobility-adjusted-capture: 0.097836
      mobility-adjusted-revenue: 3.130752
    - rank: 4
      name: Uranium One
      hold-position-capture: 0.095456
      mobility-adjusted-capture: 0.070847
      mobility-adjusted-revenue: 2.267104
    - rank: 5
      name: CGN
      ticker: 1164.HK
      hold-position-capture: 0.072991
      mobility-adjusted-capture: 0.052889
      mobility-adjusted-revenue: 1.692448
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-08
---

# Global Uranium

## Market Definition

**Market contract.** The market is worldwide primary mine-origin natural uranium concentrate, expressed as U3O8 equivalent, sold for civil nuclear-fuel use. It includes uranium recovered from conventional, in-situ-recovery and by-product mines. It excludes conversion to UF6, enrichment, fuel fabrication, reactor services, mine-development services, physical-fund units, and secondary material drawn from utility, government or commercial inventories. Recycled uranium and down-blended military material are also outside the primary-mining boundary.

The **revenue boundary** is producer-recognized revenue at the first external sale of mine-origin uranium concentrate. A pound is counted once. Integrated transfers are valued at the equivalent producer realization; utility fuel-cycle spend, exchange or fund trading volume, and downstream conversion/enrichment/fabrication revenue are excluded. Because most contracts are confidential, the market total uses mine-origin billable pounds multiplied by an estimated global average producer realization rather than spot-market turnover or end-customer fuel spend.

The **addressable unit** is annual natural-uranium demand from the operable and newly fuelled global civil reactor fleet. The **billable unit** is a pound of U3O8 equivalent sold by a primary producer. There is no stable product-adoption denominator: reactor requirements are a physical flow driven by reactor capacity, initial cores, burn-up and tails-assay choices. The analytical penetration class would be `spend-share`, but no logistic block is fitted because primary-versus-secondary sourcing is cyclical inventory management, not durable adoption. Segments are existing-reactor reloads and initial cores for new reactors, aggregated into one mine-origin revenue pool. Values are nominal USD in 2026 and 2036.

## Current View

World Nuclear Association reports 2024 mine production of **60,213 tU** (about **156.5 million lb U3O8**), equal to 90% of reactor requirements. Kazakhstan, Canada and Namibia supplied 39%, 24% and 12% respectively. The same source reports a concentrated but multi-player company field: Kazatomprom 21%, Cameco 17%, Orano 11%, Uranium One and CGN about 10% each by attributable production.

The expected 2026 market value is **$12.0bn**. The bottom-up bridge uses approximately **66 ktU** of primary output (about **172 million lb U3O8**) and a **$70/lb** average producer realization. The volume is an analyst estimate anchored to 2024 actual output, Kazatomprom's 9% year-on-year attributable-production growth in the first half of 2026, and a broadly steady Cameco production plan. The price is deliberately below quoted indicators: Kazatomprom realized $67.88/lb at group level in the first half of 2026, while Cameco realized $62.11/lb in 2025 and its 2026 contract portfolio still lags market pricing. For context, Kazatomprom reported first-half 2026 spot and long-term indicators averaging $85.98/lb and $95.50/lb.

The current player inputs use WNA's 2024 attributable production divided by world mine output. They are therefore volume-based proxies for producer-revenue share; realized prices vary by contract and geography, but no complete like-for-like company revenue set exists. Multiplying each share by the common market realization is the least distorted auditable bridge.

## Adoption Path

This is a physical commodity-flow forecast, so no logistic penetration block is configured. WNA estimates current reactors require roughly **67.5 ktU** annually and its 2023 Nuclear Fuel Report reference case called for uranium demand to rise 28% from 2023 to 2030 and a further 51% across 2031-2040. Interpolating that path implies roughly **110 ktU** of reactor requirements in 2036. The reference case assumes secondary inventories remain available but become less able to cover structural growth; the expected bridge uses **105 ktU** of mine-origin sales at the horizon.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Reactor uranium requirements | 73 ktU | 110 ktU | Existing reloads plus initial cores; WNA reference-path interpolation |
| Primary mine-origin billable volume | 66 ktU / 172 Mlb U3O8 | 105 ktU / 273 Mlb U3O8 | 90% current primary share, rising toward 95% as secondary supply thins |
| Net producer realization | $70/lb | $117/lb | Contract repricing toward the 2026 long-term indicator, then roughly inflationary growth |
| Annual market value | **$12.0bn** | **$32.0bn** | 10.3% nominal CAGR; rounded expected values |

The 2036 expected value is **$32.0bn**, with a plausible range of roughly **$20bn-$45bn**. The largest sensitivities are reactor construction and retirement timing, initial-core demand, enrichment tails economics, inventory drawdowns, Kazakhstan production discipline, permitting and financing of replacement mines, and the incentive price required after cost inflation. The horizon price is not a spot-price call: it assumes legacy contracts reprice and a roughly $95/lb 2026 long-term indicator keeps pace with inflation. Mine sales remain the only revenue stream; conversion, enrichment and fuel fabrication stay excluded.

## Market Structure

Uranium has almost no network effects and little data flywheel. Concentration instead comes from scarce tier-one orebodies, very high development capital, long permitting and licensing cycles, environmental and radiological obligations, sovereign participation, and material operating scale in ISR fields and large mills. Reputation matters because utilities contract years ahead and value delivery reliability. Switching costs are moderate rather than high: U3O8 is fungible once specifications and transport routes are qualified, but sanctions, origin restrictions and long-term contracts can segment the practical supplier set.

The structural model projects a 2036 leader share of **21.4%**, rank decay of **0.765** and **HHI 0.110**—about nine effective competitors. That is moderately concentrated, not winner-take-most. The result fits a market where capital, regulation and resource quality keep the field oligopolistic, while fungible material, new projects and sovereign supply-security investment prevent one firm from dominating. The geometric curve assigns about 90.7% of the market to modeled ranks and the rest to an atomistic fringe. No analyst override is used.

## Players

The current rank order is Kazatomprom, Cameco, Orano, Uranium One and CGN, based on WNA's 2024 attributable production shares. The inputs are whole-market mine-output shares and therefore a transparent proxy for the contract's otherwise opaque producer-revenue shares.

The model views are:

| Current player | Hold current rank | Mobility-adjusted 2036 capture | Implied 2036 revenue |
|---|---:|---:|---:|
| Kazatomprom | 21.4% | **16.0%** | **$5.13bn** |
| Cameco | 16.3% | **12.9%** | **$4.12bn** |
| Orano | 12.5% | **9.78%** | **$3.13bn** |
| Uranium One | 9.55% | **7.08%** | **$2.27bn** |
| CGN | 7.30% | **5.29%** | **$1.69bn** |

Mobility reduces each incumbent's expected capture because it allows rank changes, fringe outcomes and exit. The model's **10.06% gone probability** is already included and is not applied again. It is a pooled 10-15 year base rate that sees current rank and share spacing, not reserve quality, project pipelines, sanctions, sovereign policy or contract books. No company-specific override is used.

Kazatomprom has the low-cost ISR resource base and scale advantage but remains exposed to Kazakhstan's production policy and transport routes. Cameco owns unusually high-grade Canadian assets and a deep utility contract book. Orano, Uranium One and CGN combine mine interests with sovereign or integrated fuel-cycle backing. Outside contenders include NexGen, Denison, Paladin, Boss Energy, Energy Fuels and Uranium Energy Corp.; none has enough operating evidence to receive a horizon-capture override.

## Watch

- WNA reactor-requirements revisions through 2035-2040, especially China, India, US life extensions and first-core demand.
- Primary mine supply versus reactor requirements and the pace of utility, government and financial-inventory drawdowns.
- Kazatomprom annual guidance, sulphuric-acid availability, JV ownership changes and trans-Caspian versus Russian transport.
- Cameco's McArthur River/Key Lake and Cigar Lake reliability, contracting, purchases and realized price.
- Commissioning evidence from NexGen Rook I, Denison Phoenix, Orano Zuuvch-Ovoo and Uzbekistan expansions.
- Spot and long-term indicators versus actual Kazatomprom and Cameco realizations.
- Sanctions and origin restrictions affecting Russian-linked uranium and western utility qualification.
- Enrichment tails assays: expensive SWU can raise natural-uranium feed requirements even without reactor growth.

## Peer Comparison

- **Approximately 0% over/under our 2036 requirements estimate:** WNA's 2023 Nuclear Fuel Report reference path, as summarized in *Uranium Markets*, raises demand 28% from 2023 to 2030 and then 51% across 2031-2040. Interpolating the published percentages gives roughly **110 ktU in 2036**, matching our total-requirements bridge. This is the principal volume anchor rather than a fully independent peer and covers reactor requirements, not primary-producer revenue.
- **Not directly comparable on value:** Cameco reported a 2025 average spot indicator of **$73.54/lb**, long-term indicator of **$81.96/lb**, and company realization of **$62.11/lb**; Kazatomprom reported first-half 2026 spot, long-term and group-realized figures of **$85.98/lb**, **$95.50/lb** and **$67.88/lb**. These current observations bracket the $70/lb producer realization used in our 2026 market value but are not long-term forecasts.
- No attributable 5-10 year third-party forecast was found that both publishes a dollar market value and enforces the same first-sale, mine-origin revenue boundary. Public report summaries commonly leave unclear whether they count spot turnover, uranium compounds, secondary material or downstream fuel-cycle services; presenting those figures as directly comparable would be false precision.

## Sources

- World Nuclear Association, *World Uranium Mining Production*, current table with 2024 country, company and mine output: https://world-nuclear.org/information-library/nuclear-fuel-cycle/mining-of-uranium/world-uranium-mining-production
- World Nuclear Association, *Uranium Markets*, current demand, primary/secondary supply and 2023 Nuclear Fuel Report reference-path discussion: https://world-nuclear.org/information-library/nuclear-fuel-cycle/uranium-resources/uranium-markets
- Kazatomprom, *2Q26 Operations and Trading Update*, August 3, 2026: https://www.kazatomprom.kz/en/media/view/operatsionnie_rezultati_deyatelnosti_ao_nak_kazatomprom_za_2i_kvartal_2026_goda
- Cameco, *2025 Annual Report*, March 2026: https://www.cameco.com/sites/default/files/documents/cameco-2025-annual-report.pdf
- OECD Nuclear Energy Agency and IAEA, *Uranium 2024: Resources, Production and Demand*, 2025: https://www.oecd-nea.org/jcms/pl_103467/uranium-2024-resources-production-and-demand
