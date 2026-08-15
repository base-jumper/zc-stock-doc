---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 2.0
  maturity-market-value: 8.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.20, confidence: 0.85}
      data-scale-advantage: {score: 0.55, confidence: 0.65}
      brand-reputation: {score: 0.65, confidence: 0.75}
      capital-intensity: {score: 0.25, confidence: 0.80}
      scale-economies: {score: 0.60, confidence: 0.75}
      regulatory-barriers: {score: 0.20, confidence: 0.85}
      switching-costs: {score: 0.65, confidence: 0.80}
  model-estimate:
    s1: 0.155388
    r: 0.832075
  hhi: 0.078483
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: Dassault Systemes BIOVIA
        ticker: DSY.PA
        share: 0.13
      - rank: 2
        name: Schrodinger
        ticker: SDGR
        share: 0.11
      - rank: 3
        name: Siemens Dotmatics
        ticker: SIE.DE
        share: 0.09
      - rank: 4
        name: Revvity Signals
        ticker: RVTY
        share: 0.06
      - rank: 5
        name: Chemical Computing Group
        share: 0.045
  model-estimate:
    - rank: 1
      name: Dassault Systemes BIOVIA
      ticker: DSY.PA
      hold-position-capture: 0.155388
      mobility-adjusted-capture: 0.121957
      mobility-adjusted-revenue: 0.975656
    - rank: 2
      name: Schrodinger
      ticker: SDGR
      hold-position-capture: 0.129294
      mobility-adjusted-capture: 0.103773
      mobility-adjusted-revenue: 0.830184
    - rank: 3
      name: Siemens Dotmatics
      ticker: SIE.DE
      hold-position-capture: 0.107583
      mobility-adjusted-capture: 0.086647
      mobility-adjusted-revenue: 0.693176
    - rank: 4
      name: Revvity Signals
      ticker: RVTY
      hold-position-capture: 0.089517
      mobility-adjusted-capture: 0.071111
      mobility-adjusted-revenue: 0.568888
    - rank: 5
      name: Chemical Computing Group
      hold-position-capture: 0.074485
      mobility-adjusted-capture: 0.058643
      mobility-adjusted-revenue: 0.469144
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---
# Global Computational Molecular-Discovery Software

## Market Definition

**Market scope:** worldwide third-party software and hosted platforms used in discovery-stage molecular research to identify, design, simulate, rank, optimize, or computationally evaluate small molecules, biologics, and industrial molecules. Included products cover molecular modeling and simulation, cheminformatics, structure and sequence analysis used for molecule design, predictive property and toxicology tools, scientific-data platforms directly supporting computational design, and AI-native molecular-design applications sold as software.

**Revenue boundary:** annual revenue recognized by the external software or platform vendor from licences, subscriptions, hosted access, usage/compute credits, maintenance, and directly attached implementation or support. Drug-asset value, pipeline product revenue, equity consideration, research-service and CRO fees, wet-lab automation, collaboration milestones and royalties tied to compounds, general cloud/IaaS, generic ELN/LIMS, clinical-trial software, regulatory submissions, and commercial-stage analytics are excluded. Mixed vendors contribute only the estimated qualifying share of revenue. This is vendor revenue, not pharmaceutical R&D spend, deal value, customer savings, or drug-asset TAM.

**Addressable unit and penetration:** the denominator is annual worldwide discovery-stage molecular R&D activity spend that can structurally use computational tools. Penetration is `spend-share`: qualifying vendor revenue divided by that denominator. Billable units are enterprise and team subscriptions, seats, calculation entitlements, usage credits, and data/model modules. Enterprise biopharma, emerging biotech/CRO/chemical companies, and academia/public research are separate buying segments but aggregate at the same vendor-revenue boundary. The base year is 2026, the fixed horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

## Current View

Expected 2026 market value is **$2.0B**, with a rough **$1.5B-$2.8B** range. There is no audited total on this exact boundary, so the estimate reconciles disclosed and estimated supplier revenue to Siemens' much broader life-sciences R&D software opportunity. Schrödinger reported $199.5M of 2025 software revenue and, on 5 August 2026, guided to $218M-$228M of 2026 annual contract value. The $223M midpoint supports its 11% current share. All of the top 20 pharmaceutical companies licensed its software in 2025, and commercial-customer gross dollar retention was 96%, evidence that paid computational discovery is an established recurring category rather than experimental asset value.

Siemens expected Dotmatics to generate more than $300M of FY2025 revenue across life-sciences R&D software. Only an estimated 60% falls inside this narrower contract because GraphPad, generic scientific data management, and experimental-analysis workflows extend beyond computational molecule discovery. Certara generated $98.5M of software revenue in the first half of 2026, but only an estimated discovery-stage subset of its biosimulation, Chemaxon, and informatics portfolio qualifies. Simulations Plus disclosed that discovery contributed 20% of its $12.6M software revenue in the quarter to May 2026. BIOVIA, Revvity Signals, Chemical Computing Group, Cadence/OpenEye, CCDC, Genedata, NVIDIA BioNeMo, and numerous AI-native vendors do not disclose boundary-matched revenue. Estimated qualifying revenue for these named suppliers plus the specialist tail reconciles to $2.0B; supplier allocations are lower confidence than the rounded market total.

## Adoption Path

Expected 2036 market value is **$8.0B**, a 14.9% nominal CAGR, with a broad **$4.5B-$12B** plausible range. The reference bridge grows worldwide discovery-stage molecular R&D activity from an estimated $80B to $135B and its qualifying paid-software share from 2.5% to 5.9%. The first driver reflects ordinary R&D and price growth; the second reflects more scientists using predictive tools, broader enterprise deployment, biologics and materials expansion, and usage-based AI/physics workloads. The arithmetic is a sizing judgment, not a fitted penetration series; no logistic block is configured because a consistent worldwide history of the defined spend share is unavailable.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Addressable discovery-stage molecular R&D activity | ~$80B | ~$135B | Nominal analyst estimate; excludes clinical and commercial activity |
| Paid covered-software share | ~2.5% | ~5.9% | Vendor revenue as a share of the denominator |
| Annual billable activity | Enterprise/seat/usage mix | Broader enterprise and usage mix | Subscription, entitlement, credit, and module revenue |
| Annual market value | **$2.0B** | **$8.0B** | Vendor-recognized revenue; rounded |

Recurring software and hosted usage remain the dominant stream. AI-native design and predictive toxicology are included only when sold as tools; milestones, royalties, and downstream asset economics remain excluded even if a vendor's platform helped discover the molecule. The largest sensitivities are biopharma funding, enterprise expansion beyond specialist users, monetization of compute-intensive workloads, open-source and foundation-model price pressure, and whether customers buy integrated platforms or assemble best-of-breed tools.

## Market Structure

Direct network effects are weak because a customer's calculation does not become more useful merely because another customer uses the same vendor. Proprietary validation data and customer feedback can improve models, but confidential customer datasets are siloed and public data, open source, and licensed foundation models keep the data-scale loop moderate. Reputation matters because scientific error destroys project time and compounds downstream cost.

Scale economies are meaningful: algorithms, validation, scientific support, and enterprise deployment are high fixed-cost activities, while replication is cheap. They flatten before monopoly because expert teams, open-source components, and rented compute allow specialists to compete. Regulation does not directly license or cap discovery software vendors. Switching costs are material after workflows, scripts, file formats, models, and organizational validation are embedded; Schrödinger's 96% 2025 commercial gross dollar retention is a useful mechanism check. These costs protect several incumbents rather than only a leader. No override is used.

The structural model produces a **15.54%** 2036 leader share, **0.8321** rank decay, and **0.078483 HHI**, equivalent to about 12.7 equal-sized competitors. That is a moderately fractured market: integrated platforms gain scale, but best-of-breed specialists and new model architectures preserve a long tail. The geometric curve remains inside its valid fringe regime and is consistent with the player view.

## Players

Current shares are low-confidence analyst estimates on the whole $2.0B boundary: BIOVIA 13%, Schrödinger 11%, qualifying Dotmatics 9%, Revvity Signals 6%, and Chemical Computing Group 4.5%. The remaining 56.5% includes Cadence/OpenEye, Certara/Chemaxon, CCDC, Genedata, Simulations Plus, NVIDIA BioNeMo, cloud and AI-native platforms, regional vendors, and open-source-adjacent commercial support. Rankings reflect disclosed qualifying revenue where available, estimated product mix for diversified vendors, product breadth, and enterprise presence; they are not shares of only the named subset.

BIOVIA can retain leadership through breadth and integration with Dassault's scientific and product-lifecycle stack, but an expansive portfolio can lose focused computational-design workloads. Schrödinger combines a respected physics-based platform, all-top-20-pharma adoption, high retention, and growing hosted use; it can gain as customers scale predictive computation, or lose if AI-native and open tools become good enough at lower cost. Dotmatics has more than 14,000 customers across its broader portfolio and can use Siemens distribution and an integrated data layer, but much of its revenue lies outside the contract. Revvity Signals and Chemical Computing Group have embedded chemistry workflows; Cadence/OpenEye, Certara/Chemaxon, NVIDIA and newer AI platforms are credible outside contenders.

The pooled mobility result is canonical and deliberately does not see company momentum, scientific quality, acquisition strategy, or product roadmap. The gone probability is already included in mobility-adjusted capture and must not be applied again. No player override is used.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Dassault Systemes BIOVIA (DSY.PA) | 15.54% | **12.20%** | **$0.976B** |
| Schrodinger (SDGR) | 12.93% | **10.38%** | **$0.830B** |
| Siemens Dotmatics (SIE.DE) | 10.76% | **8.66%** | **$0.693B** |
| Revvity Signals (RVTY) | 8.95% | **7.11%** | **$0.569B** |
| Chemical Computing Group | 7.45% | **5.86%** | **$0.469B** |

The 10.06% pooled gone probability, rank churn, and entry from outside today's top five reduce every incumbent below the hold-position curve. The five adjusted captures total 43.8%, leaving ample room for current specialists and outside entrants. For SDGR, the canonical 2036 model result is **10.3773% capture and $0.8302B revenue**.

## Watch

- Boundary-matched revenue or ACV from BIOVIA, Dotmatics, Revvity Signals, Chemical Computing Group, Cadence/OpenEye, and AI-native vendors; this would firm up the current ranking.
- Schrödinger software ACV, hosted mix, commercial gross/net retention, top-pharma expansion, and predictive-toxicology uptake.
- Enterprise seat and calculation growth versus procurement consolidation and price compression.
- Whether proprietary customer feedback produces measurable model advantage despite siloed data; this would firm up the data-scale score.
- Open-source and foundation-model substitution, including the share monetized by application vendors rather than general cloud compute.
- M&A-driven platform bundling and whether scientific-data layers become a control point.
- Biopharma funding cycles and adoption outside large pharmaceutical companies.

## Peer Comparison

No clean long-term publication matches this contract. Siemens' April 2025 acquisition release describes an **$11B life-sciences software TAM** and says software spending is expected to double over five years. That is **not comparable** with the $2.0B current market value here: Siemens includes a wider research-to-production software stack, while its figure is a total addressable opportunity rather than expected recognized revenue. Directionally, its doubling observation is close to this document's 14.9% CAGR and supports a roughly fourfold decade outcome without resolving the narrower market level.

## Sources

- Schrödinger, 2025 Form 10-K, filed 25 February 2026: $199.5M software revenue, $198.5M ACV, all top-20 pharma adoption, and 96% commercial gross dollar retention: https://www.sec.gov/Archives/edgar/data/1490978/000149097826000010/sdgr-20251231.htm
- Schrödinger, Q2 2026 results, 5 August 2026: $218M-$228M FY2026 ACV outlook and hosted-transition update: https://www.sec.gov/Archives/edgar/data/1490978/000149097826000067/sdgr-20260630x8kxexx991.htm
- Siemens, "Siemens acquires Dotmatics to extend AI-powered software portfolio to Life Sciences," 2 April 2025: $11B broader TAM, software-spend outlook, more than $300M expected FY2025 Dotmatics revenue, over 14,000 customers: https://press.siemens.com/global/en/pressrelease/siemens-acquires-dotmatics-extend-ai-powered-software-portfolio-life-sciences
- Certara, Q2 2026 Form 10-Q, filed 4 August 2026: $98.5M first-half software revenue across its broader portfolio: https://www.sec.gov/Archives/edgar/data/1827090/000182709026000028/cert-20260630.htm
- Simulations Plus, Q3 FY2026 Form 10-Q, filed 9 July 2026: $12.6M quarterly software revenue, 20% classified as discovery: https://www.sec.gov/Archives/edgar/data/1023459/000102345926000038/simu-20260531.htm
- Dassault Systèmes BIOVIA product portfolio: https://www.3ds.com/products/biovia
- Cadence Molecular Sciences/OpenEye product portfolio: https://www.cadence.com/en_US/home/tools/molecular-sciences.html
- Revvity Signals scientific software portfolio: https://revvitysignals.com/
- Chemical Computing Group molecular operating environment: https://www.chemcomp.com/Products.htm
