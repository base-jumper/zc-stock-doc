---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 1.8
  maturity-market-value: 12.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.15, confidence: 0.80}
      data-scale-advantage: {score: 0.60, confidence: 0.60}
      brand-reputation: {score: 0.70, confidence: 0.65}
      capital-intensity: {score: 0.30, confidence: 0.75}
      scale-economies: {score: 0.75, confidence: 0.70}
      regulatory-barriers: {score: 0.65, confidence: 0.80}
      switching-costs: {score: 0.65, confidence: 0.70}
  model-estimate:
    s1: 0.199172
    r: 0.793415
  hhi: 0.107073
  method: selected-direct-ridge
  date: 2026-08-03
players:
  inputs:
    current:
      - rank: 1
        name: GE HealthCare
        ticker: GEHC
        share: 0.10
      - rank: 2
        name: Siemens Healthineers
        ticker: SHL.DE
        share: 0.09
      - rank: 3
        name: Philips
        ticker: PHG
        share: 0.07
      - rank: 4
        name: Aidoc
        share: 0.05
      - rank: 5
        name: Lunit
        ticker: 328130.KQ
        share: 0.04
  model-estimate:
    - rank: 1
      name: GE HealthCare
      ticker: GEHC
      hold-position-capture: 0.199172
      mobility-adjusted-capture: 0.150174
      mobility-adjusted-revenue: 1.802088
    - rank: 2
      name: Siemens Healthineers
      ticker: SHL.DE
      hold-position-capture: 0.158026
      mobility-adjusted-capture: 0.122653
      mobility-adjusted-revenue: 1.471836
    - rank: 3
      name: Philips
      ticker: PHG
      hold-position-capture: 0.12538
      mobility-adjusted-capture: 0.101998
      mobility-adjusted-revenue: 1.223976
    - rank: 4
      name: Aidoc
      hold-position-capture: 0.099479
      mobility-adjusted-capture: 0.078409
      mobility-adjusted-revenue: 0.940908
    - rank: 5
      name: Lunit
      ticker: 328130.KQ
      hold-position-capture: 0.078928
      mobility-adjusted-capture: 0.061932
      mobility-adjusted-revenue: 0.743184
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-03
---
# Global AI Medical Imaging Software

## Market Definition

**Market scope:** worldwide commercial software and software-enabled analysis services whose primary function is AI-driven acquisition guidance, image reconstruction or enhancement, segmentation, detection, triage, quantification, interpretation support, or report drafting for radiological medical images, including X-ray, mammography, CT, MRI, ultrasound, PET and SPECT. Both independently sold applications and the attributable AI-software portion of an imaging OEM's offering are included. Imaging hardware, ordinary scanner control software, PACS/RIS and vendor-neutral archives, digital pathology and microscopy, ophthalmic fundus/OCT software, general clinical decision support, care coordination without image analysis, research-only tools, teleradiologist labour and procedure reimbursement are excluded.

**Revenue boundary:** annual revenue recognized by the software developer, imaging OEM or software-enabled analysis provider from licences, subscriptions, usage fees, implementation and support directly attached to the covered AI functionality. Bundled OEM revenue is included only at the estimated software value attributable to AI, not at scanner or service-contract value. The addressable unit is an eligible radiological imaging examination; penetration is the `spend-share` of eligible annual examinations processed by at least one paid covered AI product. Billable units are analysed studies, modality/site/enterprise subscription-years and attributable embedded-software licences, reconciled to a per-study revenue equivalent. Acquisition/reconstruction, diagnostic analysis/triage and reporting/workflow assistance are the operating segments, then are summed at the same vendor-revenue boundary. The base year is 2026, the fixed horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

## Current View

The expected 2026 market value is **$1.8b**, with a rough **$1.3b-$2.7b** range. No public source cleanly separates this contract's software revenue from hardware, generic imaging IT and professional services. The anchor is therefore a boundary-normalized triangulation of published broad-market totals: MarketsandMarkets reports about $1.5b in 2024 for hardware, software and services combined; Roots Analysis reports $1.75b in 2024; and Emergen Research reports $2.18b in 2025. Removing hardware and unrelated service content, then allowing two years of rapid commercial growth, supports a software-only 2026 midpoint around $1.8b.

The bottom-up cross-check uses about 5.0 billion eligible radiological examinations worldwide, approximately 11% paid AI coverage, and a blended $3.30 of vendor-recognized revenue per covered study. That yields about $1.8b. The revenue equivalent spreads enterprise subscriptions, embedded OEM licences, implementation and support over covered studies; it is not a claim that vendors literally charge every examination $3.30. The denominator and global coverage are necessarily estimated because published adoption studies are regional and supplier revenue is rarely separated from broader imaging portfolios.

Commercial adoption is real but uneven. A Dutch hospital census found clinical use at 20% of hospitals in 2020, 28% in 2021 and 33% in 2022; a January-March 2022 European Society of Radiology survey found practical clinical experience among 276 of 690 respondents; and a 2023 Korean Society of Radiology survey found 60.3% of respondents had used AI software as a medical device. Those are not interchangeable global measurements, but together they support early-to-middle diffusion rather than either negligible use or saturation. The FDA's continuously updated AI-enabled-device list is dominated by radiology entries and shows continued product proliferation through 2026.

## Adoption Path

The expected 2036 market value is **$12b**, with a broad **$6b-$22b** plausible range. The reference bridge grows eligible annual imaging examinations from roughly 5.0 billion to 6.3 billion, paid AI coverage from about 11% to 48%, and nominal vendor revenue per covered study from $3.30 to $3.90. That produces approximately $11.8b, rounded to $12b. The implied ten-year CAGR is 20.9%; growth decelerates below near-term published forecasts as the market becomes larger, procurement matures and algorithm prices face bundling pressure.

No logistic penetration block is configured. A boundary-matched global time series of paid examination coverage does not exist: the Netherlands series is a useful institutional-adoption proxy but has only three annual points and represents one advanced health system, while the ESR and Korean surveys use different respondent and usage definitions. The 11% and 48% spend-share figures below are disclosed sizing judgments, not fitted observations.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Eligible annual imaging examinations | ~5.0b | ~6.3b | Global radiological activity; 2.3% annual volume growth, rounded |
| Paid AI coverage | ~11% | ~48% | Spend-share of eligible studies processed by covered commercial AI |
| AI-covered examinations | ~0.55b | ~3.02b | Eligible studies multiplied by coverage |
| Vendor revenue per covered study | ~$3.30 | ~$3.90 | Nominal blended licence, usage, support and embedded-software realization |
| Annual market value | **$1.8b** | **$12b** | Vendor-recognized software revenue; rounded expected value |

The dominant horizon stream remains recurring enterprise, modality and usage software rather than one-time implementation. Acquisition and reconstruction AI expands the addressable base because it can attach to nearly every scan; diagnostic applications deepen revenue per examination through multi-condition packages; and reporting assistance may become part of the same imaging-software buying decision. Generic PACS/RIS, foundation-model infrastructure sold outside imaging applications and clinician labour remain excluded, preventing the horizon from silently becoming a broader healthcare-AI market.

The largest sensitivities are paid coverage outside affluent health systems, whether OEM bundling transfers scanner economics to separately monetized software, and realized revenue per study as multi-algorithm packages replace single-use products. A 30%-65% horizon coverage range and roughly $3-$5.40 revenue per covered study explain most of the stated market range. Regulation and clinical validation can slow diffusion; workload shortages, broader reimbursement and enterprise procurement can accelerate it.

## Market Structure

Direct network effects are weak: one hospital gains little merely because another hospital uses the same algorithm. The strongest indirect effect is ecosystem breadth through PACS, marketplaces and OEM platforms, but customers can multi-home and integrate several algorithms. Data scale can improve robustness across scanners, populations and sites, yet access to public, partner and licensed datasets plus diminishing model returns keeps it below a winner-take-all mechanism.

Scale economies are strong because regulatory submissions, clinical validation, secure deployment, integrations and global sales are largely fixed costs. Brand and reputation matter because erroneous medical output creates patient, regulatory and procurement risk. FDA, EU and other approvals impose meaningful delays and quality-system expense without legally capping entrant count. Switching costs are substantial after a product is validated locally, integrated into PACS and worklists, embedded in longitudinal measurements, and contracted across an enterprise; they protect multiple incumbents rather than only the leader. Low physical capital intensity and hundreds of disease- and modality-specific products preserve a long tail.

The structural model yields a 19.92% horizon leader share, a 79.34% rank-to-rank decay ratio and HHI of 0.1071, equivalent to about 9.3 equal-sized competitors. That sits at the low end of the market-doc's moderately concentrated range. It implies consolidation from today's specialist-heavy field, but still leaves meaningful room for several OEM platforms, scaled independent vendors and an atomistic tail. The geometric shares sum to less than one, so the model remains within its valid fringe regime. No concentration override is used.

## Players

Current shares are low-confidence analyst estimates on the whole software-only revenue boundary: GE HealthCare 10%, Siemens Healthineers 9%, Philips 7%, Aidoc 5% and Lunit 4%, leaving 65% for Canon, Fujifilm, Viz.ai, Qure.ai, Gleamer, Sectra, Agfa, Tempus/Arterys, regional vendors and the specialist tail. MarketsandMarkets identifies GE, Siemens, Philips and Canon as the Tier I imaging OEM group and Aidoc, Arterys, Qure.ai, Gleamer and Viz.ai as cloud-native challengers, but public supplier revenue is not separated enough to produce audited shares. The ranking therefore combines breadth of attributable AI portfolios, installed distribution, regulatory presence and independent-vendor deployment evidence rather than pretending those proxies are disclosed market share.

GE, Siemens and Philips can retain leading positions because they control scanner, reconstruction, advanced-visualization and enterprise-imaging distribution, and can bundle AI into existing installed bases. They can lose share if customers prefer vendor-neutral orchestration, if bundled AI is not separately monetized, or if focused products outperform OEM modules. Aidoc can gain through a broad enterprise clinical-AI platform and its large FDA-cleared radiology portfolio, but faces procurement concentration and competition from both OEM platforms and disease specialists. Lunit reports adoption across more than 10,000 medical institutions and OEM partnerships, supporting a top-five place; its included imaging share can fall if oncology growth shifts toward digital pathology, which this contract excludes.

Viz.ai, Qure.ai, Canon/Fujifilm and application leaders are credible outside contenders. Viz.ai says its platform has more than 50 FDA-cleared algorithms across image-driven care pathways; Qure.ai has multiple FDA clearances and broad chest and neuro-imaging products. Company-specific momentum, pricing and private-company revenue are not visible enough to justify overrides. The pooled mobility calculation is therefore canonical.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| GE HealthCare (GEHC) | 19.92% | **15.02%** | **$1.80b** |
| Siemens Healthineers (SHL.DE) | 15.80% | **12.27%** | **$1.47b** |
| Philips (PHG) | 12.54% | **10.20%** | **$1.22b** |
| Aidoc | 9.95% | **7.84%** | **$0.94b** |
| Lunit (328130.KQ) | 7.89% | **6.19%** | **$0.74b** |

Mobility reduces each incumbent relative to simply holding its current rank because the pooled ten-year base rate allows rank churn, entry from outside today's top five and a 10.06% gone probability that is already embedded in adjusted capture. The five adjusted captures total about 51.5%; outside contenders and the long tail take the rest. The model does not see portfolio-specific momentum, bundling, acquisitions or execution, which remain company-level judgments rather than unsupported overrides.

## Watch

- Separated AI-software revenue, recurring revenue and paid-study volume from imaging OEMs and private platform vendors.
- Enterprise renewal, expansion and multi-algorithm attachment rates versus discontinued pilots.
- FDA, EU MDR and other regulatory throughput, post-market monitoring requirements and liability allocation.
- Reimbursement for autonomous or assisted interpretation and whether economics accrue to providers or software vendors.
- Bundled scanner/PACS pricing versus separately monetized vendor-neutral AI orchestration.
- Foundation-model reporting products moving from trials into regulated paid clinical use.
- Adoption and price realization in Asia, Latin America, the Middle East and Africa versus advanced-market proxies.
- Consolidation among point-solution vendors and whether OEM or independent marketplaces become control points.

## Peer Comparison

**Approximately 41% over our estimate in 2029:** MarketsandMarkets projects $4.5b in 2029 versus an interpolated $3.2b on our path, from about $1.5b in 2024 at a stated 23.2% CAGR. Its boundary includes hardware, software and services, so the arithmetic is **not directly comparable** to this software-only vendor-revenue contract.

**Approximately 122% over our estimate in 2030:** Roots Analysis projects $8.56b in 2030 versus an interpolated $3.9b on our path, from $1.75b in 2024 at 30% CAGR. Its published scope describes deep-learning medical-imaging solutions and companies but does not provide a clean exclusion bridge for hardware and software-enabled services; treat the comparison as boundary-mismatched.

**Approximately 106% over our estimate in 2034:** Market.us projects $16.88b in 2034 versus an interpolated $8.2b on our path, from $1.70b in 2024 at 25.8% CAGR. The report uses hardware, software and services components, so it is broader and **not directly comparable**. The large gap also reflects our explicit assumption that growth decelerates over a full ten-year horizon rather than preserving early-stage CAGR indefinitely.

These peers bracket a much faster near-term category narrative but do not change the stored inputs because none publishes the same attributable software-only contract. The 2036 $12b estimate is intentionally below a mechanical extension of their headline CAGRs.

## Sources

- U.S. Food and Drug Administration, "Artificial Intelligence-Enabled Medical Devices," continuously updated list accessed 3 August 2026: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices
- MarketsandMarkets, "Artificial Intelligence in Medical Imaging Market," accessed 3 August 2026; approximately $1.5b in 2024 and $4.5b in 2029, with hardware, software and services included: https://www.marketsandmarkets.com/Market-Reports/ai-in-medical-imaging-market-21977207.html
- Roots Analysis, "AI in Medical Imaging Market," accessed 3 August 2026; $1.75b in 2024 and $8.56b in 2030: https://www.rootsanalysis.com/reports/deep-learning-market.html
- Market.us, "AI in Medical Imaging Market," accessed 3 August 2026; $1.70b in 2024 and $16.88b in 2034: https://market.us/report/ai-in-medical-imaging-market/
- Emergen Research, "AI in Medical Imaging Market," accessed 3 August 2026; $2.18b in 2025 and 27.6% forecast CAGR: https://www.emergenresearch.com/industry-report/ai-in-medical-imaging-market
- van Leeuwen et al., "Clinical use of artificial intelligence products for radiology in the Netherlands between 2020 and 2022," *European Radiology* 2024; hospital adoption of 20%, 28% and 33%: https://pmc.ncbi.nlm.nih.gov/articles/PMC10791748/
- European Society of Radiology, "Current practical experience with artificial intelligence in clinical radiology," *Insights into Imaging* 2022; 276 of 690 respondents reported practical clinical experience: https://pmc.ncbi.nlm.nih.gov/articles/PMC9213582/
- Hwang et al., "2023 Survey on User Experience of Artificial Intelligence Software in Radiology," *Korean Journal of Radiology* 2024; 60.3% of respondents had usage experience: https://pmc.ncbi.nlm.nih.gov/articles/PMC11214921/
- Aidoc, company and platform overview, accessed 3 August 2026: https://www.aidoc.com/about/
- Viz.ai, platform overview and more than 50 FDA-cleared algorithms, accessed 3 August 2026: https://www.viz.ai/
- Lunit, company history and more than 10,000 adopting medical institutions, accessed 3 August 2026: https://www.lunit.io/en/about/
- Siemens Healthineers, digital solutions and AI-powered decision-support portfolio, accessed 3 August 2026: https://www.siemens-healthineers.com/digital-health-solutions
