---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 7.6
  maturity-market-value: 14.0
concentration:
  inputs:
    traits:
      network-effects:      {score: 0.05, confidence: 0.90}
      data-scale-advantage: {score: 0.10, confidence: 0.80}
      brand-reputation:     {score: 0.20, confidence: 0.70}
      capital-intensity:    {score: 0.85, confidence: 0.75}
      scale-economies:      {score: 0.78, confidence: 0.75}
      regulatory-barriers:  {score: 0.90, confidence: 0.85}
      switching-costs:      {score: 0.30, confidence: 0.65}
  model-estimate:
    s1: 0.266135
    r: 0.712965
  hhi: 0.144052
  method: selected-direct-ridge
  date: 2026-08-08
players:
  inputs:
    current:
      - rank: 1
        name: China Northern Rare Earth Group
        ticker: 600111.SS
        share: 0.485
      - rank: 2
        name: China Rare Earth Group
        share: 0.207
      - rank: 3
        name: MP Materials
        ticker: MP
        share: 0.130
      - rank: 4
        name: Lynas Rare Earths
        ticker: LYC.AX
        share: 0.074
  model-estimate:
    - rank: 1
      name: China Northern Rare Earth Group
      ticker: 600111.SS
      hold-position-capture: 0.266135
      mobility-adjusted-capture: 0.209427
      mobility-adjusted-revenue: 2.931978
    - rank: 2
      name: China Rare Earth Group
      hold-position-capture: 0.189745
      mobility-adjusted-capture: 0.153035
      mobility-adjusted-revenue: 2.14249
    - rank: 3
      name: MP Materials
      ticker: MP
      hold-position-capture: 0.135282
      mobility-adjusted-capture: 0.115547
      mobility-adjusted-revenue: 1.617658
    - rank: 4
      name: Lynas Rare Earths
      ticker: LYC.AX
      hold-position-capture: 0.096451
      mobility-adjusted-capture: 0.091466
      mobility-adjusted-revenue: 1.280524
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-08
---

# Global Rare-Earth Materials

## Market Definition

**Market contract.** The market is worldwide primary rare-earth materials: lanthanides plus yttrium, generally expressed as rare-earth-oxide (REO) equivalent. It includes mined concentrate, separated oxides, compounds and metals used in magnets, catalysts, polishing, glass and ceramics, metallurgy and other industrial applications. It excludes scandium, fabricated permanent magnets, finished components, recycling equipment, mining services and the value of end products such as vehicles, turbines and electronics.

The **revenue boundary** is producer-recognized revenue at the first arm's-length sale of rare-earth feedstock or separated material. A tonne is counted once: integrated transfers are valued at the equivalent raw-material realization, while downstream magnet and component revenue is excluded. This avoids adding mine, separation and magnet revenue for the same material. Public market estimates do not consistently enforce that boundary, so the current value is triangulated rather than taken from one report.

The **addressable unit** and **billable unit** are metric tonnes of REO-equivalent annual demand. The analytical penetration class is `spend-share`: rare-earth material spend as a share of the functional-material spend that could use rare-earths or substitutes. It is not fitted because the cross-application denominator is unstable; commodity tonnage, element mix and realized price are more decision-useful. Segments are (1) magnet REEs—Nd, Pr, Dy and Tb—and (2) bulk and other REEs. Market value is their sum. Values are nominal USD in 2026 and 2036.

## Current View

USGS estimates 2025 world mine production at **390 kt REO**, including 270 kt from China, 51 kt from the United States and 29 kt from Australia. It also reports 2025 free-on-board oxide prices ranging from about $1/kg for lanthanum oxide and $1.71/kg for cerium oxide to $69/kg for NdPr oxide, $239/kg for dysprosium oxide and $1,010/kg for terbium oxide. The wide dispersion makes a single tonnes-times-spot-price estimate misleading.

The expected 2026 market value is **$7.6bn**. The bottom-up check applies approximately $62/kg to an estimated 100 kt of magnet REEs and $4.8/kg to roughly 290 kt of other REO, yielding $6.2bn and $1.4bn respectively. The magnet volume interpolates the IEA's 91 kt demand in 2024 and 123 kt in 2030; the total volume is anchored to USGS 2025 production. Research Nester's $7.6bn 2026 estimate provides a close top-down check, although its exact value-chain boundary is not fully disclosed.

Current producer shares are necessarily approximate. China no longer publishes all company quota allocations: the stored ranking annualizes the disclosed first-2024-batch split—94.58 kt of 135 kt for China Northern Rare Earth Group and the residual for China Rare Earth Group—against China's 270 kt output, then uses MP Materials' reported 50.692 kt 2025 production and Australia's 29 kt output as a proxy for Lynas. These are REO-volume proxies for the revenue boundary and are lower-confidence where product mix differs, especially heavy REEs.

## Adoption Path

This is a commodity-demand forecast, not a product-installed-base curve, so no logistic penetration block is configured. The IEA Stated Policies Scenario is the volume anchor: magnet-REE demand rises from 91 kt in 2024 to 123 kt in 2030 and 150 kt in 2040. Linear interpolation gives about 139 kt in 2036. EV motors, industrial equipment, wind turbines and other permanent magnets drive most incremental value; catalysts, polishing and other bulk uses grow more slowly.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Magnet-REE billable volume | 100 kt | 139 kt | IEA 2024/2030/2040 STEPS interpolation |
| Other-REE billable volume | 290 kt | 380 kt | 2.7% annual volume growth, constrained by mature bulk uses |
| Magnet-REE net realization | $62/kg | $86/kg | Nominal mix/price growth; greater Dy/Tb and tight diversified supply |
| Other-REE net realization | $4.8/kg | $5.3/kg | Mostly inflation offset by abundant La/Ce supply |
| Annual market value | **$7.6bn** | **$14.0bn** | Segment totals; 6.3% nominal CAGR |

The expected 2036 value is **$14.0bn**, with a plausible range of roughly **$9bn-$22bn**. The largest sensitivities are magnet-material intensity per EV/robot, substitution toward ferrite or rare-earth-reduced motors, non-Chinese mine and separation commissioning, Chinese quota/export policy, and heavy-REE pricing. The dominant horizon revenue stream remains magnet REEs. Recycling is a supply source within the same raw-material pool only when the recovered material is sold; equipment and service revenue remain excluded.

## Market Structure

There are almost no network effects, data flywheels or consumer brand preference. Concentration instead comes from multibillion-dollar, technically difficult mines and separation plants, steep process learning, environmental permitting, radioactive-tailings management and China's quota/licensing regime. Scale economies are strong, but customers can qualify alternative material suppliers within a product cycle, keeping switching costs below those of software or tightly integrated systems.

The structural model projects a 2036 leader share of about **26.6%**, rank decay of about **0.713** and **HHI 0.144**—roughly seven effective competitors. That is less concentrated than today's output because announced mines and separation projects in Australia, the United States, Brazil, Canada and Africa can diversify supply. It remains an oligopoly: the IEA expects the top three mining countries to hold 76% of magnet-REE supply in 2040 and the top three refining countries 92%. Company concentration is lower than country concentration because China has two quota groups and new capacity spans several operators.

## Players

The current rank order is China Northern Rare Earth Group, China Rare Earth Group, MP Materials and Lynas Rare Earths. It is based on REO-equivalent output proxies, not audited like-for-like raw-material revenue. The model views are:

| Current player | Hold current rank | Mobility-adjusted 2036 capture | Implied 2036 revenue |
|---|---:|---:|---:|
| China Northern Rare Earth Group | 26.6% | **20.9%** | **$2.93bn** |
| China Rare Earth Group | 19.0% | **15.3%** | **$2.14bn** |
| MP Materials | 13.5% | **11.6%** | **$1.62bn** |
| Lynas Rare Earths | 9.65% | **9.15%** | **$1.28bn** |

Mobility reduces every incumbent's expected capture because it allows rank changes, fringe outcomes and exit; the model's 10.06% gone probability is already included and is not applied again. No company-specific override is used. The output is a pooled base rate that sees current rank and share spacing, not execution, financing, policy support or resource quality.

China's two state groups retain advantages from resource access, quotas, integrated separation and domestic magnet demand. MP and Lynas have strategic value as scaled non-Chinese suppliers, but their economics depend on commissioning downstream separation, customer qualification and government-backed price/offtake support. Outside contenders include Iluka, Arafura, Energy Fuels and Brazilian ionic-clay projects; none receives an override before commercial evidence supports a whole-market share.

## Watch

- IEA magnet-REE demand and announced-project supply revisions, especially the 2030-2040 slope.
- China mining/separation quotas, export licensing and whether company allocations become public again.
- MP Materials' NdPr separation ramp and Fort Worth magnet qualification.
- Lynas' Kalgoorlie/Malaysia ramp, heavy-REE separation and Mt Weld expansion.
- Iluka Eneabba, Arafura Nolans and Brazilian projects reaching financed, qualified production.
- Ferrite, induction and rare-earth-reduced motor adoption; magnet recycling yields and economics.
- NdPr, Dy and Tb realized prices versus the nominal bridge used here.

## Peer Comparison

- **4.3% under our estimate at the same 2035 horizon:** Research Nester (December 2025) forecasts **$12.6bn in 2035** from $7.2bn in 2025. Our constant-CAGR path is $13.17bn in 2035. Its global rare-earth-metals scope appears broadly similar but does not clearly state how integrated mine, separation and downstream sales are de-duplicated.
- **13.9% over our estimate at the same 2035 horizon:** Wise Guy Reports (June 2026) forecasts **$15.0bn in 2035** from $7.18bn in 2025, a stated 7.7% CAGR. Its application segmentation includes permanent magnets, catalysts, phosphors, metallurgy and batteries; whether the value is rare-earth material revenue or broader product revenue is not fully disclosed, so the arithmetic is directionally comparable rather than exact.
- **20.2% under our estimate at the same 2034 horizon:** Fortune Business Insights (July 2026) forecasts **$9.89bn in 2034** from $4.54bn in 2026, versus our $12.39bn interpolated 2034 value. The lower base implies a narrower or differently measured value boundary; treat it as a credible disagreement, not a reason to average the estimates.
- **Volume benchmark, not directly comparable:** the IEA projects magnet-REE demand from **91 kt in 2024 to 123 kt in 2030 and 150 kt in 2040** under STEPS. It covers only Nd, Pr, Dy and Tb and reports tonnes rather than revenue, but it supports the magnet-volume leg of the bridge.

## Sources

- USGS, *Mineral Commodity Summaries 2026: Rare Earths*, February 2026: https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf
- IEA, *Global Critical Minerals Outlook 2025*, rare-earth chapters and annex tables, May 2025: https://www.iea.org/reports/global-critical-minerals-outlook-2025
- MP Materials, *Fourth Quarter and Full Year 2025 Results*, February 26, 2026: https://investors.mpmaterials.com/investor-news/news-details/2026/MP-Materials-Reports-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx
- Lynas Rare Earths, *2025 Annual Report*, August 28, 2025: https://lynasrareearths.com/investors-media/reporting-centre/annual-reports/
- Fastmarkets, *China issues first batch of rare earths quotas for 2024*, February 7, 2024: https://www.fastmarkets.com/insights/china-issues-first-batch-of-rare-earths-quotas-for-2024/
- Research Nester, *Rare Earth Metals Market Size & Share, Growth Forecasts 2035*, updated December 19, 2025: https://www.researchnester.com/reports/rare-earth-metals-market/5142
- Wise Guy Reports, *Rare Earth Market Trends | Industry Analysis & Insights 2035*, June 29, 2026: https://www.wiseguyreports.com/reports/rare-earth-market
- Fortune Business Insights, *Rare Earth Elements Market Size, Share & Global Report [2034]*, July 20, 2026: https://www.fortunebusinessinsights.com/rare-earth-elements-market-102943
