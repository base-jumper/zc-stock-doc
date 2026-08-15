---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.55
  maturity-market-value: 9.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.20, confidence: 0.80}
      data-scale-advantage: {score: 0.75, confidence: 0.65}
      brand-reputation: {score: 0.65, confidence: 0.65}
      capital-intensity: {score: 0.60, confidence: 0.75}
      scale-economies: {score: 0.70, confidence: 0.65}
      regulatory-barriers: {score: 0.45, confidence: 0.75}
      switching-costs: {score: 0.50, confidence: 0.65}
  model-estimate:
    s1: 0.264369
    r: 0.728465
  hhi: 0.148914
  method: selected-direct-ridge
  date: 2026-08-10
players:
  inputs:
    current:
      - rank: 1
        name: Schrodinger Drug Discovery
        ticker: SDGR
        share: 0.17
      - rank: 2
        name: XtalPi Drug Discovery Solutions
        ticker: 2228.HK
        share: 0.14
      - rank: 3
        name: Insilico Medicine
        ticker: 3696.HK
        share: 0.09
      - rank: 4
        name: Isomorphic Labs
        share: 0.06
      - rank: 5
        name: Recursion Pharmaceuticals
        ticker: RXRX
        share: 0.05
  model-estimate:
    - rank: 1
      name: Schrodinger Drug Discovery
      ticker: SDGR
      hold-position-capture: 0.264369
      mobility-adjusted-capture: 0.193468
      mobility-adjusted-revenue: 1.741212
    - rank: 2
      name: XtalPi Drug Discovery Solutions
      ticker: 2228.HK
      hold-position-capture: 0.192584
      mobility-adjusted-capture: 0.150102
      mobility-adjusted-revenue: 1.350918
    - rank: 3
      name: Insilico Medicine
      ticker: 3696.HK
      hold-position-capture: 0.14029
      mobility-adjusted-capture: 0.116559
      mobility-adjusted-revenue: 1.049031
    - rank: 4
      name: Isomorphic Labs
      hold-position-capture: 0.102197
      mobility-adjusted-capture: 0.083071
      mobility-adjusted-revenue: 0.747639
    - rank: 5
      name: Recursion Pharmaceuticals
      ticker: RXRX
      hold-position-capture: 0.074447
      mobility-adjusted-capture: 0.062748
      mobility-adjusted-revenue: 0.564732
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-10
---
# Global AI-Native Drug-Discovery Partnership Economics

## Market Definition

**Market scope.** This is the worldwide market for externally partnered drug discovery performed by AI-native, computational-first companies across small molecules and biologics. It includes target identification and validation, hit generation, molecular design and optimization, preclinical-enabling work, and platform-originated assets partnered before commercialization. Pure software subscriptions, conventional CRO work without a differentiated computational platform, clinical-trial services, internally retained pipeline economics, and drug sales retained by the pharmaceutical partner are excluded.

**Revenue boundary.** Market value is annual revenue recognized by the AI-native discovery partner from research funding and services, platform access bundled into a discovery collaboration, upfront and option fees, discovery/development/regulatory/commercial milestones, out-licensing consideration for platform-originated assets, and royalties on partnered products. Equity investments, announced but contingent deal value, the partner's drug sales before the provider's royalty, and revenue from wholly owned drugs are excluded. This boundary deliberately captures Recursion's collaboration economics rather than only generic molecular-discovery software.

**Addressable unit and penetration.** The stable denominator is one dollar of worldwide discovery-stage pharmaceutical and biotechnology R&D activity that could structurally be performed with an external AI-native partner. Penetration is a `spend-share`: included provider revenue divided by that addressable activity. Billable units are funded program-years, accepted maps or datasets, option exercises, milestone events, licensed assets, and royalty-bearing product sales. Small-molecule and biologic/antibody programs have different technical workflows but aggregate at the same provider-recognized-revenue boundary.

**Time and value basis.** The base year is 2026 and the fixed horizon is 2036. Values are nominal USD at approximately constant current foreign-exchange rates. The market contract is held constant across sizing, concentration, and player capture.

## Current View

Expected 2026 market value is **$0.55B**, with a rough **$0.40B-$0.80B** range. There is no audited aggregate on this narrow boundary, so the estimate is reconstructed from company disclosures. Schrödinger reported $45.9M of drug-discovery revenue in the first half of 2026, a $91.7M annualized run rate. XtalPi reported RMB537.9M (about $75M) of 2025 drug-discovery-solutions revenue. Insilico Medicine reported $49.0M of 2025 drug-discovery and pipeline-development revenue after excluding software and non-pharma discovery. Recursion reported $13.6M of first-half 2026 operating revenue from strategic-alliance R&D, a $27.2M run rate. These four disclosed anchors total about $243M.

Isomorphic Labs, Generate Biomedicines, Iambic, Owkin, Aqemia, Absci, BenevolentAI and other private or smaller providers do not disclose comparable current revenue. Adding an estimated $307M for Isomorphic, the specialist tail, and normalizing unusually lumpy milestone recognition gives the $0.55B expected value. AbCellera is excluded from the named ranking because its broader antibody platform is not consistently presented as AI-native, though qualifying AI-led programs belong in the tail. The current total and shares are therefore lower-confidence estimates; the audited supplier figures are firm but do not cover the whole market.

## Adoption Path

Expected 2036 market value is **$9.0B**, a 32.2% nominal CAGR, with a broad **$4B-$18B** plausible range. The reference bridge grows addressable discovery-stage R&D activity from about $95B to $160B and raises the included provider-revenue share from 0.58% to 5.6%. Adoption expands as validated platforms take responsibility for more targets and progress more programs into higher-value milestones and royalties. The model does not assume that AI-native providers replace internal pharma discovery; most customers will multi-source and retain core capabilities.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Addressable discovery-stage R&D activity | ~$95B | ~$160B | Analyst allocation of global biopharma R&D; nominal growth and mix |
| Included provider-revenue share | ~0.58% | ~5.6% | Provider revenue divided by addressable discovery activity |
| Research, platform and early milestones | ~$0.42B | ~$4.2B | Funded program-years, upfronts, options and discovery milestones |
| Later milestones, out-licensing and royalties | ~$0.13B | ~$4.8B | Risk-adjusted platform-originated asset economics |
| **Annual market value** | **$0.55B** | **$9.0B** | Reconciles to front matter |

No logistic penetration block is configured because no consistent historical series exists for the defined worldwide provider-revenue share; company revenue histories are distorted by milestone timing and changing boundaries. The largest sensitivities are clinical validation of AI-originated programs, partner willingness to externalize discovery, late-stage success and royalty conversion, and whether economics accrue to integrated discovery partners or are competed into software/CRO pricing.

## Market Structure

Direct network effects are weak: one pharmaceutical customer's program does not become more valuable because another uses the same platform, and customers can multi-source. Data scale is the strongest concentrator where proprietary perturbation, chemistry and assay data improve predictions and generate better experiments; Recursion's maps built from more than one trillion internally manufactured neuronal cells and XtalPi's AI-plus-robotics model illustrate the mechanism. The evidence is not yet sufficient to prove that returns to data persist across targets, so confidence remains moderate.

Scientific reputation matters because a weak target or molecule can waste years and large downstream budgets. Fixed investment in automated laboratories, datasets, compute, medicinal chemistry and multidisciplinary teams produces meaningful capital and scale barriers, but cloud compute, public structural data and CRO capacity remain rentable. Regulation applies principally to resulting drug candidates rather than licensing discovery providers. Multi-year collaborations, jointly generated IP and validation history create moderate switching costs, while target-by-target contracting protects multiple incumbents rather than a single platform.

The structural model is used without an analyst override. It produces a **26.44%** 2036 leader share, **0.7285** rank decay and **0.148914 HHI**, equivalent to about 6.7 equal-sized competitors. This moderately concentrated result is plausible: data, reputation and scale reward the strongest platforms, while therapeutic fragmentation, pharma multi-sourcing and target-specific science preserve several competitors. The geometric curve has a valid fringe and the player table uses the same whole-market boundary. Low-confidence mechanisms should be revisited when companies report platform-specific prospective validation, customer repeat rates and boundary-matched revenue.

## Players

Current whole-market shares are estimated from annualized or latest full-year boundary-matched revenue, then reconciled to the $0.55B market: Schrödinger Drug Discovery 17%, XtalPi Drug Discovery Solutions 14%, Insilico Medicine 9%, Isomorphic Labs 6%, and Recursion 5%. Schrödinger's $45.9M first-half 2026 drug-discovery revenue includes a $10M collaboration milestone and is therefore normalized rather than treated as a permanent run rate. XtalPi's $75M equivalent and Insilico's $49M are audited 2025 anchors. Isomorphic is estimated from its Novartis, Lilly and Johnson & Johnson collaborations because Alphabet does not disclose it separately. Recursion's share uses its $27.2M annualized first-half operating revenue.

Schrödinger can win through physics-based chemistry, established pharma relationships and platform-originated assets, but pure software remains outside this contract. XtalPi combines automated wet labs with AI and scaled sharply in 2025, though one customer represented 45.5% of total group revenue. Insilico has broad pharma adoption and both discovery and asset-licensing economics, but its 2025 revenue fell as pipeline-development upfronts normalized. Isomorphic has premier technology and partners but an unproven disclosed revenue base. Recursion combines large proprietary biology maps, chemistry, wet-lab automation and up to 15 Sanofi and 40 Roche/Genentech programs; it can gain if these programs convert into development milestones and royalties, or lose if platform validation fails to translate into approved partnered products.

The mobility model produces the following canonical captures; there is no player override:

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Schrodinger Drug Discovery (SDGR) | 26.44% | **19.35%** | **$1.741B** |
| XtalPi Drug Discovery Solutions (2228.HK) | 19.26% | **15.01%** | **$1.351B** |
| Insilico Medicine (3696.HK) | 14.03% | **11.66%** | **$1.049B** |
| Isomorphic Labs | 10.22% | **8.31%** | **$0.748B** |
| Recursion Pharmaceuticals (RXRX) | 7.44% | **6.27%** | **$0.565B** |

The outputs are pooled base rates that see current rank, share gaps and the horizon concentration curve, but not company-specific scientific quality, balance sheet, management or deal momentum. For RXRX, the canonical 2036 result is **6.2748% capture and $0.5647B revenue**. The 10.06% gone probability is already embedded and must not be applied again.

## Watch

- Boundary-matched discovery-collaboration revenue from private providers, especially Isomorphic Labs, Generate Biomedicines, Iambic, Owkin and Aqemia.
- Recursion's Sanofi development-candidate milestones, Roche/Genentech target and small-molecule options, Merck KGaA progress, and eventual royalty-bearing clinical assets.
- Prospective comparisons of AI-originated program success rates, cycle time and cost against conventional discovery, separated from retrospective selection bias.
- Repeat collaborations and target expansion by existing partners versus cancellations, insourcing and multi-vendor procurement.
- The mix shift from research funding and upfronts toward development milestones, royalties and asset out-licensing.
- Whether proprietary experimental data continue to improve model quality across targets or public models and rentable automation narrow the gap.

## Peer Comparison

- **Not directly comparable; 162% over our 2035 path:** Precedence Research projects the broad AI-in-drug-discovery market from **$6.93B in 2025 to $17.81B in 2035**. Our compound path reaches about **$9.0B in 2036 and $6.8B in 2035**. Its current value is more than twelve times our 2026 anchor because the publication includes a much broader software, services and technology market, while this document excludes pure software and counts only recognized partnered-discovery economics. The long-horizon figure is directionally useful but not a boundary-matched reason to change the model.
- No clean 5–10 year publication was found for provider-recognized AI-native collaboration funding, milestones, out-licensing and royalties as one revenue pool. Announced headline deal values are not substitutes because most are contingent and may never become revenue.

## Sources

- Recursion Pharmaceuticals, Q2 2026 Form 10-Q, filed 5 August 2026: first-half operating revenue, collaboration accounting, Sanofi and Roche/Genentech economics, and program progress: https://www.sec.gov/Archives/edgar/data/1601830/000160183026000098/rxrx-20260630.htm
- Schrödinger, Q2 2026 Form 10-Q, filed 5 August 2026: $45.9M first-half drug-discovery revenue and Novartis, Lilly and BMS collaboration economics: https://www.sec.gov/Archives/edgar/data/1490978/000149097826000068/sdgr-20260630.htm
- XtalPi, 2025 Annual Report, 25 March 2026: RMB537.9M drug-discovery-solutions revenue, business definition and customer concentration: https://ir.xtalpi.com/media/05sd1uig/2025-annual-report.pdf
- Insilico Medicine, 2025 Annual Report, 28 April 2026: $25.0M drug-discovery and $23.9M pipeline-development revenue, software exclusion and collaboration model: https://ir.insilico.com/media/3cwezvxu/2025-annual-report-20260428-en.pdf
- Isomorphic Labs, Partnerships, accessed 10 August 2026: Novartis, Eli Lilly and Johnson & Johnson collaboration scope: https://www.isomorphiclabs.com/partnerships
- IQVIA Institute, *Global Trends in R&D 2026*, 2026: resilient 2025 funding, increased biopharma dealmaking and reported success-rate improvement among AI-driven programs: https://www.iqvia.com/insights/the-iqvia-institute/reports-and-publications/reports/global-trends-in-r-and-d-2025
- Precedence Research, *Artificial Intelligence in Drug Discovery Market*, accessed 10 August 2026: broad-market $6.93B 2025 and $17.81B 2035 estimates: https://www.precedenceresearch.com/artificial-intelligence-in-drug-discovery-market
