---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 7.8
  maturity-market-value: 25.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.25, confidence: 0.80}
      data-scale-advantage: {score: 0.80, confidence: 0.75}
      brand-reputation: {score: 0.75, confidence: 0.80}
      capital-intensity: {score: 0.55, confidence: 0.80}
      scale-economies: {score: 0.80, confidence: 0.80}
      regulatory-barriers: {score: 0.75, confidence: 0.85}
      switching-costs: {score: 0.70, confidence: 0.75}
  override:
    s1: 0.26
    r: 0.72
    reason: "The raw model's 0.2846/0.7235 curve has 1.03 total modeled mass, outside mobility's whole-market validity regime. The override preserves its approximate decay while normalizing the leader and leaving a plausible specialist fringe."
  model-estimate:
    s1: 0.284634
    r: 0.723537
  hhi: 0.140365
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: Natera
        ticker: NTRA
        share: 0.155
      - rank: 2
        name: Guardant Health
        ticker: GH
        share: 0.145
      - rank: 3
        name: Caris Life Sciences
        ticker: CAI
        share: 0.135
      - rank: 4
        name: Tempus AI
        ticker: TEM
        share: 0.13
      - rank: 5
        name: Foundation Medicine (Roche)
        ticker: ROG.SW
        share: 0.10
  model-estimate:
    - rank: 1
      name: Natera
      ticker: NTRA
      hold-position-capture: 0.26
      mobility-adjusted-capture: 0.183552
      mobility-adjusted-revenue: 4.5888
    - rank: 2
      name: Guardant Health
      ticker: GH
      hold-position-capture: 0.1872
      mobility-adjusted-capture: 0.139753
      mobility-adjusted-revenue: 3.493825
    - rank: 3
      name: Caris Life Sciences
      ticker: CAI
      hold-position-capture: 0.134784
      mobility-adjusted-capture: 0.102559
      mobility-adjusted-revenue: 2.563975
    - rank: 4
      name: Tempus AI
      ticker: TEM
      hold-position-capture: 0.097044
      mobility-adjusted-capture: 0.075527
      mobility-adjusted-revenue: 1.888175
    - rank: 5
      name: Foundation Medicine (Roche)
      ticker: ROG.SW
      hold-position-capture: 0.069872
      mobility-adjusted-capture: 0.062354
      mobility-adjusted-revenue: 1.55885
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---
# U.S. Precision-Oncology Diagnostics and Data/AI

## Market Definition

**Market scope:** United States precision-oncology products used after cancer is suspected or diagnosed. Included molecular diagnostics are tissue and liquid comprehensive genomic profiling, companion-diagnostic and therapy-selection assays, prognostic molecular tests, minimal-residual-disease (MRD), recurrence and treatment-response monitoring, and germline testing ordered to manage an affected cancer patient or their treatment. Included data/AI products are oncology-specific clinico-genomic data licences, biomarker and companion-diagnostic analytics, algorithmic trial matching, oncology decision-support software, and computational/digital-pathology applications sold to providers or life-sciences customers. Products may be developed outside the United States, but only revenue attributable to U.S. patients, U.S.-sourced datasets or U.S. customer use is included.

**Explicit exclusions:** population cancer screening and multi-cancer early detection before clinical suspicion; therapeutics and drug royalties; ordinary histology, imaging, pathology and laboratory services without a covered molecular or AI product; consumer ancestry and non-oncology genetics; hereditary testing unrelated to management of an affected cancer patient; sequencing instruments, reagents and general cloud infrastructure; general-purpose EHR, PACS, LIMS and research software; wet-lab CRO execution, site management and clinician labour; and all non-U.S. activity. Tempus's Ambry rare-disease, reproductive, cardiology and unaffected hereditary-risk testing, and its Compass CRO labour, therefore sit outside the boundary.

**Revenue boundary:** annual revenue recognized by the diagnostic laboratory, test developer, oncology-data vendor or application provider from covered tests, data licences, subscriptions, usage fees, analytical deliverables, companion-diagnostic milestones and directly attached implementation/support. For payer-funded tests the measure is the vendor's GAAP revenue after estimated reimbursement and price concessions, not list price, claims submitted or total care spend. For biopharma products it is vendor revenue, not customer R&D spend, drug value, milestone opportunity or clinical-trial GMV. Diversified suppliers contribute only the estimated qualifying revenue.

**Units, penetration and segments:** the stable addressable unit is a U.S. cancer patient or survivor with a clinical decision or monitoring episode that could structurally use a covered product. Adoption is a composite `spend-share`: covered vendor revenue divided by the full-adoption revenue opportunity for the same patients and oncology R&D/workflow activity. Billable units are completed molecular reports and longitudinal monitoring tests; licensed records, cohorts and analytical projects; companion-diagnostic deliverables; and provider/site/application subscription-years. Initial therapy selection/prognosis, longitudinal MRD/response monitoring, and oncology data/AI are modelled separately, then summed at the same vendor-revenue boundary. The base year is 2026, the fixed horizon is 2036, and values are nominal USD.

## Current View

Expected 2026 market value is **$7.8B**, with a rough **$6.5B-$9.5B** range. The direct anchor is the annualized qualifying revenue of the largest vendors at the latest available quarter. Guardant reported Q2 2026 oncology revenue of $219.1M and biopharma/data revenue of $60.9M, a $1.12B run rate after excluding Shield screening and licensing/other. Caris reported $252.3M of molecular-profiling and $11.5M of pharma R&D revenue, or $1.05B annualized; 99% of first-half revenue was U.S. customer revenue. Natera processed 296,700 oncology units in Q2; applying about $1,020 recognized revenue per unit, consistent with management's statement that Signatera carries a higher ASP than its women's-health products, gives roughly $1.21B annualized qualifying revenue.

Tempus's boundary-normalized run rate is approximately **$1.0B**. Its Q2 Diagnostics revenue was $289.3M, but hereditary and other diagnostics are excluded. The filing says oncology tests rose to 96,500 and oncology revenue increased $37.5M; using the disclosed oncology reimbursement and product mix supports roughly $180M of quarterly oncology diagnostics. Adding the oncology-attributable share of $77.7M Insights and $6.3M Next revenue, while excluding $9.0M of Trials/CRO and non-oncology activity, produces about $250M for the quarter. This is an analyst allocation rather than a company-reported segment total.

Foundation Medicine does not disclose revenue inside Roche, so its $0.78B implied contribution is the least certain top-five input. Its scale is nevertheless supported by more than 1.5M cumulative comprehensive-genomic-profiling reports, 950+ supported trials, 100 approved NGS companion-diagnostic indications and a broad U.S. tissue, liquid, MRD and biopharma portfolio. Exact Sciences' separately reported $717.1M of 2025 global Precision Oncology revenue, NeoGenomics, Personalis and hospital/laboratory specialists sit just outside the named five. The named estimates total about $5.2B, leaving roughly one-third of the whole market for these vendors and the long tail.

The bottom-up cross-check starts with about 2.04M annual U.S. incident cancers, repeat therapy-decision testing in advanced disease, and a much larger survivor pool that can generate longitudinal monitoring. NCI reports 18.1M U.S. cancer survivors as of January 2022 and projects 26M by 2040. Approximately $6.3B of the current pool is clinical molecular testing and $1.5B is oncology data/AI, companion-diagnostic and algorithmic workflow revenue. The reconstruction is consistent with the supplier run rates without treating the $208.9B of U.S. cancer-care expenditure as vendor revenue.

## Adoption Path

Expected 2036 market value is **$25B**, a 12.3% nominal CAGR, with a broad **$15B-$40B** plausible range. A single logistic penetration block is not defensible: therapy-selection tests, serial MRD assays, data licences and oncology applications have different denominators and no consistent historical U.S. spend-share series. The adoption figures below are disclosed sizing judgments rather than fitted observations.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| New U.S. cancer cases | ~2.04M | ~2.35M | NCI 2025 anchor; ageing-driven growth, not adoption |
| U.S. cancer survivors | ~20M | ~24M | Interpolation toward NCI's 26M 2040 projection |
| Therapy-selection/prognostic testing revenue | ~$4.8B | ~$8.5B | Broader guideline use, liquid/tissue retesting and nominal mix; vendor net revenue |
| MRD/recurrence/response-monitoring revenue | ~$1.5B | ~$8.5B | More eligible tumour types, serial tests and payer coverage; excludes screening |
| Oncology data/AI and CDx revenue | ~$1.5B | ~$8.0B | Data licences, analytics, CDx services and provider applications; excludes CRO labour |
| Annual market value | **$7.8B** | **$25B** | Same U.S. vendor-revenue boundary; rounded |

Initial profiling grows slower than the rest because tissue and liquid therapy-selection testing is already established. The major expansion is longitudinal: MRD and treatment-response products turn an incident patient into several billable tests across active treatment and survivorship, but the model does not assume every survivor is tested indefinitely. The reference view has roughly 2.1M monitored patient-years in 2036, about four tests per adopted patient-year and approximately $1,000 of nominal recognized revenue per test, yielding about $8.5B. This is below the full eligible population and therefore expected market value, not full-adoption TAM.

Oncology data/AI grows as larger longitudinal datasets support biomarker discovery, companion diagnostics, external control cohorts, trial matching, computational pathology and care-gap applications. The $8.0B horizon value assumes those products take a mid-single-digit share of relevant oncology R&D and provider workflow budgets; it does not capitalize drug economics or count the underlying R&D spend. Recurring monitoring and subscriptions/data access are expected to dominate horizon revenue, not one-time implementation.

The largest sensitivities are tumour-type coverage and clinical utility for MRD, payer reimbursement and realized test price, whether repeat testing changes treatment often enough to become standard care, and whether proprietary data produces paid products rather than merely supporting diagnostics. The downside reflects narrow MRD reimbursement and commoditized data; the upside requires broad pan-cancer monitoring, repeated testing and high-value multimodal AI without a collapse in per-test realization.

## Market Structure

Direct network effects are limited: one oncologist does not obtain much more utility simply because another uses the same laboratory. The weaker indirect effect is a provider/biopharma ecosystem around shared evidence, trial networks and integrated ordering, but customers can send samples to several vendors. Evidence that cross-customer participation materially improves product value or drives single-homing would raise the 0.25 network score; current disclosure does not establish it.

Data scale is strong. High-volume laboratories accumulate linked molecular, clinical, treatment and outcome records that can improve assay design, biomarker discovery and model validation. Tempus, Caris, Foundation and Guardant all commercialize this link, but confidential customer data, public cohorts and diminishing model returns prevent assuming an unassailable feedback loop. Comparative prospective validation showing that dataset scale creates durable diagnostic uplift would raise confidence above 0.75; this is irreducible for now until such studies mature.

Scale economies are strong because laboratories, payer evidence, FDA submissions, bioinformatics, data curation, secure infrastructure and specialized selling are largely fixed costs. Capital needs are meaningful but below semiconductor or infrastructure markets, and sequencing capacity can be purchased. FDA approvals, CLIA/CAP operations, state licensure, privacy rules, clinical-evidence requirements and reimbursement create substantial barriers without legally capping entrant count. Brand and clinical reputation matter because an incorrect result can alter cancer treatment; Foundation's 100 approved NGS companion-diagnostic indications and the leading vendors' trial relationships provide mechanism evidence. Separated test-level reimbursement, renewal and win/loss data would firm up the brand, capital and scale scores.

Switching costs are high for serial MRD because a patient-specific baseline and longitudinal history favour continuity, and meaningful for health systems after ordering, EHR, pathology, billing and evidence workflows are integrated. They are lower for one-off profiling, where physicians can order another validated assay. Switching costs therefore protect several incumbents rather than forcing monopoly. Cohort-level vendor retention and multi-homing disclosure would raise confidence above 0.75.

The raw structural model produces a 28.46% leader share and 72.35% rank decay, but its infinite curve contains 103% of market mass and is therefore invalid for whole-market mobility. The canonical override uses a 26% leader and 72% decay, preserving the model's approximate shape while leaving a 7.1% atomistic fringe. This is a model-validity correction, not a separate HHI judgment. The resulting **0.140365 HHI** is equivalent to about 7.1 equal-sized competitors, a moderately concentrated market consistent with scaled laboratory/data platforms and a durable specialist tail. The current top-five shares and player outcomes use the identical U.S. vendor-revenue contract.

## Players

The current whole-market ranking is an evidence-normalized estimate, not a ranking of only public companies. Natera's 15.5% share implies $1.21B and is anchored to Q2 oncology volume and a disclosed higher relative ASP. Guardant's 14.5% implies $1.13B and matches its reported oncology plus biopharma/data run rate. Caris's 13.5% implies $1.05B and matches its reported profiling plus pharma-R&D run rate. Tempus's 13.0% implies $1.01B and matches the boundary-normalized allocation above. Foundation Medicine's 10.0% implies $0.78B and is the lower-confidence estimate. Shares are of the full $7.8B market, descend contiguously and leave 33.5% for Exact Sciences, NeoGenomics, Personalis, institutional labs and specialists.

Natera can retain leadership if Signatera becomes a broad pan-cancer monitoring standard, but its patient-specific workflow, reimbursement concentration and heavy evidence burden create execution risk. Guardant combines liquid-biopsy leadership with biopharma data and can gain as blood-based therapy selection and MRD expand; screening is excluded, so Shield does not support its share here. Caris can gain through whole-exome/transcriptome profiling and its linked clinico-genomic platform, but must sustain reimbursement and prove its newer blood and AI products. Foundation has unmatched companion-diagnostic depth and Roche distribution, while the absence of separated revenue makes its current share uncertain.

Tempus combines oncology testing, licensed multimodal data, trial-matching analytics and provider applications on one platform. It can gain as testing feeds higher-margin data/AI products, Paige adds computational pathology, and the announced Personalis transaction adds MRD and biopharma capabilities if it closes. It can lose if the data flywheel does not create measurable clinical advantage, acquisitions add non-core revenue without integration, or reimbursement lags test volume. The pooled mobility model does not see this company-specific momentum or the pending transaction, so no unsupported override is used.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Natera (NTRA) | 26.00% | **18.36%** | **$4.59B** |
| Guardant Health (GH) | 18.72% | **13.98%** | **$3.49B** |
| Caris Life Sciences (CAI) | 13.48% | **10.26%** | **$2.56B** |
| Tempus AI (TEM) | 9.70% | **7.55%** | **$1.89B** |
| Foundation Medicine/Roche (ROG.SW) | 6.99% | **6.24%** | **$1.56B** |

Mobility-adjusted capture incorporates pooled 10-year rank churn, outside entry, fringe value and the **10.06%** gone probability once. It reduces Tempus from 9.70% hold-position capture to the canonical **7.5527%**, or **$1.888B** of 2036 revenue. The five adjusted captures total about 56.4%; outside contenders and the tail take the rest. No player override is used.

## Watch

- Tempus reporting that separates oncology diagnostics, oncology Insights/Next, non-oncology Ambry and CRO revenue; this would firm up its current share.
- Completion and integration of the announced Personalis acquisition, including MRD volume, revenue and whether Personalis remains separately marketed.
- Natera oncology revenue or product-level ASP disclosure rather than inference from units and consolidated mix.
- Foundation Medicine U.S. revenue, annual test volume and data/CDx revenue inside Roche.
- Prospective pan-cancer MRD utility, recurrence lead time, treatment-change rates and payer coverage by tumour type.
- Repeat-test frequency, realized reimbursement and longitudinal retention by provider and patient cohort.
- Comparative evidence that proprietary dataset scale improves diagnostic or AI performance after controlling for assay design.
- Provider multi-homing, enterprise renewal and ordering-share data to firm up network, brand and switching-cost scores.
- FDA, CLIA/LDT and privacy-policy changes that alter the cost or speed of launching covered tests and applications.
- Whether oncology data and AI contracts become repeatable subscriptions or remain bespoke projects and milestones.

## Peer Comparison

**Approximately 58% under the company TAM in the same nominal amount:** Tempus's 2024 IPO prospectus estimated a **$60B annual global oncology-testing opportunity**, including more than **$20B** for solid-tumour recurrence and treatment monitoring. Our **$25B 2036 expected U.S. market value** is not directly comparable: it is one geography and expected recognized revenue at partial adoption, while Tempus's figure is global full-adoption opportunity. Our contract also adds oncology data/AI but excludes screening and unaffected hereditary-risk testing. The gap is therefore directionally sensible rather than evidence that the projection is too low.

**Not comparable to the broader spending pools:** the same prospectus cited $50B of clinical-trial services, $51B of biomarker discovery and $18B of real-world-evidence research opportunities. Those are customer-spend/TAM categories, include non-oncology activity and CRO work, and overlap. The $8.0B data/AI horizon stream counts only covered vendor revenue and deliberately avoids summing those headline pools.

No independent long-term forecast found through the cutoff used the same U.S. combined diagnostic-plus-data/AI vendor boundary. Published precision-oncology reports commonly include therapeutics, screening, instruments or worldwide spend, so they are not presented as like-for-like validation.

## Sources

- Tempus AI, Q2 2026 Form 10-Q, filed 30 July 2026: Diagnostics and Data and applications revenue; test volumes; oncology revenue bridge; Insights, Trials and Next revenue; reimbursement; product definitions: https://www.sec.gov/Archives/edgar/data/1717115/000119312526326090/tem-20260630.htm
- Tempus AI, 2024 IPO prospectus, filed 17 June 2024: global oncology-testing opportunity, recurrence/monitoring opportunity, oncology incidence/adoption assumptions and broader data-services spending pools: https://www.sec.gov/Archives/edgar/data/1717115/000119312524161989/d221145d424b4.htm
- Guardant Health, Q2 2026 Form 10-Q, filed 30 July 2026: $219.1M oncology and $60.9M biopharma/data quarterly revenue; product and revenue definitions; exclusion of Shield screening: https://www.sec.gov/Archives/edgar/data/1576280/000157628026000037/gh-20260630.htm
- Caris Life Sciences, Q2 2026 Form 10-Q, filed 5 August 2026: $252.3M molecular-profiling and $11.5M pharma-R&D quarterly revenue, 59,200 clinical cases, 99% U.S. first-half revenue and 1.13M cumulative profiled cases: https://www.sec.gov/Archives/edgar/data/2019410/000201941026000055/cai-20260630.htm
- Natera, Q2 2026 Form 10-Q, filed 7 August 2026: 296,700 quarterly oncology units, Signatera product definition, consolidated revenue and relative ASP commentary: https://www.sec.gov/Archives/edgar/data/1604821/000162828026054525/ntra-20260630.htm
- Exact Sciences, 2025 Form 10-K, filed 13 February 2026: $717.1M Precision Oncology revenue, including $223.8M international revenue, and product boundary: https://www.sec.gov/Archives/edgar/data/1124140/000112414026000011/exas-20251231.htm
- Foundation Medicine, U.S. company and portfolio overview, accessed 9 August 2026: more than 1.5M CGP reports, 950+ supported trials, 100 approved NGS companion-diagnostic indications, data and provider products: https://www.foundationmedicine.com/
- National Cancer Institute, Cancer Statistics, accessed 9 August 2026: 2,041,910 estimated U.S. new cancer cases in 2025, 18.1M survivors in January 2022, 26M projected survivors by 2040 and $208.9B 2020 cancer-care expenditure: https://www.cancer.gov/about-cancer/understanding/statistics
- U.S. Food and Drug Administration, cleared or approved companion-diagnostic devices, updated 17 December 2025: https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-cleared-or-approved-companion-diagnostic-devices-in-vitro-and-imaging-tools
