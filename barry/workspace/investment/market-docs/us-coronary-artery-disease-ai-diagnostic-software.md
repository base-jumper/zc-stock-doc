---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.25
  maturity-market-value: 2.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.10, confidence: 0.80}
      data-scale-advantage: {score: 0.80, confidence: 0.75}
      brand-reputation: {score: 0.75, confidence: 0.70}
      capital-intensity: {score: 0.20, confidence: 0.80}
      scale-economies: {score: 0.85, confidence: 0.80}
      regulatory-barriers: {score: 0.80, confidence: 0.90}
      switching-costs: {score: 0.55, confidence: 0.65}
  model-estimate:
    s1: 0.251894
    r: 0.740992
  hhi: 0.14071
  method: selected-direct-ridge
  date: 2026-08-03
players:
  inputs:
    current:
      - rank: 1
        name: Heartflow
        ticker: HTFL
        share: 0.78
      - rank: 2
        name: Cleerly
        share: 0.10
      - rank: 3
        name: Elucid
        share: 0.035
      - rank: 4
        name: Keya Medical
        share: 0.015
  model-estimate:
    - rank: 1
      name: Heartflow
      ticker: HTFL
      hold-position-capture: 0.251894
      mobility-adjusted-capture: 0.208467
      mobility-adjusted-revenue: 0.416934
    - rank: 2
      name: Cleerly
      hold-position-capture: 0.186651
      mobility-adjusted-capture: 0.158181
      mobility-adjusted-revenue: 0.316362
    - rank: 3
      name: Elucid
      hold-position-capture: 0.138307
      mobility-adjusted-capture: 0.120038
      mobility-adjusted-revenue: 0.240076
    - rank: 4
      name: Keya Medical
      hold-position-capture: 0.102485
      mobility-adjusted-capture: 0.097099
      mobility-adjusted-revenue: 0.194198
  gone-probability: 0.1006
  # Explicit outside-contender override for the stock-level TAM-capture valuation of AYA.AX.
  override:
    - name: Artrya
      ticker: AYA.AX
      capture: 0.05
      reason: "Analyst-owned outside-contender estimate for the stock-doc TAM-capture valuation: AYA holds an early FDA-cleared beachhead (Anatomy + Plaque live; Flow pending clearance) across three US foundation health systems but is not yet a top-dog with broad share. A 5% terminal capture of the whole US CAD-AI software market is consistent with the rule-breaker trait read (credible early beachhead, not yet proven category leader) and is deliberately below its underpenetrated-revenue potential. See stock-doc AYA.AX."
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-03
---
# U.S. Coronary Artery Disease AI Diagnostic Software

## Market Definition

**Market scope:** United States commercial software and software-enabled analysis services that apply AI or computational modelling to coronary CT angiography (CCTA) to detect, quantify, characterize or assess the functional significance of coronary artery disease (CAD). Covered products include FFR-CT/ischemia analysis, coronary plaque and stenosis quantification, and diagnostic workflow views delivered as part of a paid CAD analysis. CT scanners, contrast, image acquisition, generic advanced visualization and PACS, calcium scoring without covered AI analysis, clinician interpretation fees, traditional stress testing, invasive angiography/FFR, treatment, PCI planning sold separately, research-only tools, and products used only outside the United States are excluded.

**Revenue boundary:** annual revenue recognized by the CAD-AI developer or software-enabled analysis provider from U.S. licences, subscriptions and per-analysis usage fees. It excludes the provider's CCTA procedure reimbursement, professional fees, scanner revenue and patient out-of-pocket spend retained by a clinic. The addressable unit is an annual U.S. symptomatic stable or acute chest-pain diagnostic episode structurally eligible for CCTA. Penetration is the `spend-share` of the full-adoption CAD-AI revenue opportunity realized by paid covered products. Billable units are delivered FFR/ischemia analyses and plaque/stenosis analyses; one episode can generate both without double-counting the episode. Physiology and anatomical plaque/stenosis analysis are modelled separately and summed at the same vendor-revenue boundary. The base year is 2026, the fixed horizon is 2036, and values are nominal USD.

## Current View

The expected 2026 market value is **$250m**, with a rough **$210m-$330m** range. Heartflow provides the hard anchor: it reported $48.99m of U.S. revenue in Q1 2026, or a $196m annualized run rate, after $162.73m in 2025. Its Q1 revenue grew 43% year over year and case volume grew 67%, partly offset by lower average selling price. Assigning Heartflow an estimated 78% share puts the whole covered market at approximately $251m. The residual roughly $54m is a low-confidence estimate for Cleerly, Elucid, Keya Medical and smaller or newly launched products; private-company revenue is not disclosed.

The volume cross-check is consistent. Heartflow assessed 195,000 U.S. patients in 2025, representing about 19% of current U.S. CCTA volume, and its U.S. average selling price disclosed in the 2025 S-1 was $1,067 for FFR-CT. Current annual paid CAD-AI activity is therefore plausibly around 0.24m-0.28m patient analyses at roughly $900-$1,050 of blended vendor revenue per revenue-generating case. This is still only about 2.5%-3% of the 9.5m annual U.S. non-invasive CAD testing episodes Heartflow estimated from Clarivate data; the current CCTA bottleneck, not the clinical pool, constrains realized market value.

Heartflow remains the only participant with public audited revenue and volume. Its 2025 U.S. revenue grew 41.5%, its platform was deployed at more than 1,465 U.S. accounts, and FFR-CT represented 98% of total company revenue. Dedicated reimbursement is now established: FFR-CT has a Category I CPT code and coverage representing approximately 99% of covered U.S. lives; plaque analysis gained CPT 75577 effective January 2026 and all seven Medicare Administrative Contractors covered it by January 2026. Those facts support a real, reimbursed software market rather than a count of FDA clearances or unpaid pilots.

## Adoption Path

The expected 2036 market value is **$2.0b**, with a broad **$1.0b-$3.5b** plausible range. The reference bridge grows eligible annual non-invasive CAD diagnostic episodes from roughly 9.7m to 10.4m, and assumes the share routed through CCTA with paid covered AI rises from about 2.6% to 31%. At the horizon, approximately one-third of AI-enabled CCTA episodes receive a paid physiology analysis and 60% receive a paid plaque/stenosis analysis. Applying nominal vendor realization of about $1,150 per physiology analysis and $390 per plaque analysis produces approximately $1.22b and $0.75b respectively, rounded to $2.0b. The implied ten-year CAGR is 23.1%.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Eligible annual CAD diagnostic episodes | ~9.7m | ~10.4m | Heartflow/Clarivate 9.5m 2023 NIT anchor; modest demographic growth |
| Paid CAD-AI/CCTA share | ~2.6% | ~31% | Realized share of eligible episodes; current revenue/volume cross-check and guideline-driven CCTA migration |
| AI-enabled CCTA episodes | ~0.25m | ~3.2m | Eligible episodes multiplied by paid adoption |
| Paid physiology analyses | ~0.23m | ~1.06m | Current market dominated by FFR-CT; horizon 33% clinical eligibility |
| Paid plaque/stenosis analyses | Nascent | ~1.93m | Horizon 60% clinical eligibility; can attach to the same episode |
| Net vendor revenue per analysis | ~$1,000 blended | ~$1,150 FFR; ~$390 plaque | Current Heartflow ASP anchor; nominal inflation, mix and volume discounting |
| Annual market value | **$0.25b** | **$2.0b** | Vendor-recognized covered software/service revenue |

No logistic penetration block is configured. The only defensible longitudinal series is Heartflow's own revenue and patient volume, not whole-market spend-share, and the analog library currently contains only one `spend-share` series. Fitting a precise market curve to one dominant company's three-year commercial ramp would falsely equate share gains and price/mix with category adoption. The 31% horizon share is therefore an explicit sizing judgment, tested against the 9.5m episode pool and the company's $5b full-adoption TAM rather than presented as a fitted result.

The dominant horizon stream remains per-case physiology analysis, but plaque becomes a material second module because it can attach to the same CCTA and has a separate code. The model does not assume that every NIT converts to CCTA or that every eligible CCTA buys every module. The largest sensitivities are the pace at which CCTA displaces stress imaging, realized plaque-analysis reimbursement and attachment, and FFR-CT price compression as automated competitors enter. The downside case assumes roughly 18% paid adoption and weaker plaque attachment; the upside assumes about 48% adoption and stronger multi-module monetization.

## Market Structure

Direct network effects are negligible: one hospital does not gain clinical value merely because another buys the same test. The material feedback loop is data scale. Heartflow reported more than 160m annotated CCTA images at year-end 2025 and a human-in-the-loop production system, which can improve automation, accuracy and product development; nevertheless, clinical datasets can be licensed or built through partnerships, so the advantage is strong rather than absolute.

Scale economies are high because regulatory submissions, prospective clinical evidence, reimbursement work, secure cloud infrastructure, integrations and specialist selling are largely fixed costs. Brand and clinical reputation matter because hospitals and payors demand diagnostic accuracy and outcome evidence. FDA clearance and payment coverage create substantial barriers but do not legally cap entrants: Heartflow itself identifies Cleerly, Elucid and Keya Medical as CCTA-AI competitors. Physical capital intensity is low. Switching costs are moderate after workflow integration, local validation, clinician education and payer contracting, while separate CPT codes and standard DICOM inputs preserve the ability to trial or multi-home across modules.

The structural model yields a 25.19% horizon leader share, a 74.10% rank-to-rank decay ratio and HHI of **0.14071**, equivalent to about 7.1 equal-sized competitors. This is a moderately concentrated specialist market and materially less monopolistic than today's Heartflow-led field as reimbursed plaque and ischemia alternatives scale. The geometric shares sum to about 97.2%, so the curve remains inside its valid fringe regime. No analyst override is used.

## Players

Current whole-market shares are low-confidence estimates anchored to Heartflow's audited revenue: Heartflow 78%, Cleerly 10%, Elucid 3.5% and Keya Medical 1.5%, leaving 7% for smaller products and rounding. Heartflow's Q1 2026 U.S. run rate divided by the $250m market estimate directly supports its share. The private-company ranking follows product breadth, U.S. clearance and commercial maturity, but their revenues are undisclosed; it should not be read as audited market-share data.

Heartflow can retain leadership through its installed base, reimbursement, published evidence, dataset and integrated roadmap/FFR/plaque workflow. It can lose share as plaque-specific reimbursement opens a second buying decision, as providers demand on-premise or faster fully automated analysis, or if ongoing patent and federal marketing investigations impair execution. Cleerly is the clearest challenger with integrated plaque, stenosis and ischemia analysis and a prevention-oriented offering; its constraints are scale, payer coverage and the patent litigation Heartflow filed in April 2026. Elucid's histology-validated plaque characterization differentiates it clinically but remains earlier commercially. Keya became more credible after 2026 U.S. plaque clearance, yet its domestic installed base is still nascent.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Heartflow (HTFL) | 25.19% | **20.85%** | **$417m** |
| Cleerly | 18.67% | **15.82%** | **$316m** |
| Elucid | 13.83% | **12.00%** | **$240m** |
| Keya Medical | 10.25% | **9.71%** | **$194m** |

Mobility is the canonical view because it allows current challengers to move across the future rank curve and already embeds a 10.06% gone probability. The four adjusted captures total about 58.4%, leaving roughly 41.6% for outside entrants, smaller vendors and the modeled tail. Heartflow's exceptionally wide current share gap supports better retention than a rank-only model, but the pooled ten-year base rate still cuts its capture below the 25.19% hold-rank view. The model does not see company-specific clinical evidence, payer execution, litigation, financing or acquisition outcomes, so no player overrides are used.

## Watch

- Heartflow U.S. revenue cases, realized price, account additions and the mix of clinic versus hospital volume.
- Plaque-analysis revenue after CPT 75577, commercial-payer policies and attachment to FFR-CT on the same CCTA.
- U.S. CCTA volumes and the extent to which guideline adoption displaces SPECT, PET and stress echocardiography.
- Disclosed revenue, paid-case volume and payer coverage from Cleerly, Elucid, Keya and new entrants.
- Heartflow-Cleerly patent litigation and the Department of Justice investigation disclosed by Heartflow.
- FDA policy for AI-enabled medical devices, algorithm-change protocols and post-market evidence requirements.
- Price compression from automation, on-premise offerings, OEM bundling or provider-developed models.
- Expansion to asymptomatic screening; it is excluded unless regulatory indication, reimbursement and workflow make it part of the same covered buying decision.

## Peer Comparison

No independent 5-10 year forecast was found with the same U.S., CAD-specific, vendor-revenue boundary. The most useful benchmark is Heartflow's July 2025 S-1 estimate of a **$5b current U.S. TAM**: $3.3b for 3.1m FFR-CT-eligible patients at a $1,067 ASP plus $1.7b for 5.5m plaque-eligible patients at an estimated $300 price. Our $2.0b 2036 expected market value is **60% below that $5b figure**, but the arithmetic is **not directly comparable** because Heartflow's number is full-adoption TAM across the entire NIT pool, not expected realized revenue in a forecast year. It is still a useful ceiling check: our expected value realizes roughly 32% of an inflation-adjusted version of that opportunity.

Heartflow also reported that its 195,000 U.S. patients in 2025 were less than 2% of its 9.5m-test overall opportunity and about 19% of current U.S. CCTA volume. That supports both the large substitution runway and the need to model the CCTA migration bottleneck. Broad forecasts for AI in cardiology or AI medical imaging include ECG, echocardiography, monitoring, hardware and non-CAD applications, so they were rejected as non-comparable rather than used to tune the estimate.

## Sources

- Heartflow, Form 10-Q for the quarter ended 31 March 2026, filed 14 May 2026; U.S. revenue of $48.99m, 67% case-volume growth, product and litigation updates: https://www.sec.gov/Archives/edgar/data/1464521/000146452126000071/htfl-20260331x10q.htm
- Heartflow, Form 10-K for 2025, filed 18 March 2026; $162.73m U.S. revenue, 195,000 U.S. patients, 19% of CCTA volume, 1,465 U.S. accounts, reimbursement and competitors: https://www.sec.gov/Archives/edgar/data/1464521/000146452126000042/htfl-20251231x10k.htm
- Heartflow, Form S-1/A, filed 6 August 2025; 9.5m U.S. NIT episodes, $5b combined U.S. TAM, $1,067 FFR-CT ASP and $300 plaque price: https://www.sec.gov/Archives/edgar/data/1464521/000162828025038091/heartflowinc-sx1a2.htm
- Gulati et al., "2021 AHA/ACC Guideline for the Evaluation and Diagnosis of Chest Pain," *Journal of the American College of Cardiology* 2021; CCTA and FFR-CT recommendations: https://www.jacc.org/doi/10.1016/j.jacc.2021.07.053
- U.S. Food and Drug Administration, "Artificial Intelligence-Enabled Medical Devices," continuously updated list accessed 3 August 2026: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices
- Centers for Medicare & Medicaid Services, Medicare Physician Fee Schedule lookup and 2026 payment files, accessed 3 August 2026: https://www.cms.gov/medicare/payment/fee-schedules/physician/lookup-tool
- Cleerly, product overview for AI-based plaque, stenosis and ischemia quantification, accessed 3 August 2026: https://cleerlyhealth.com/
- Elucid, coronary plaque-analysis platform overview, accessed 3 August 2026: https://elucid.com/
- Keya Medical, company and DeepVessel product overview, accessed 3 August 2026: https://www.keyamedical.com/
