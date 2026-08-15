---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.55
  maturity-market-value: 7.5
concentration:
  inputs:
    traits:
      network-effects: {score: 0.05, confidence: 0.90}
      data-scale-advantage: {score: 0.30, confidence: 0.60}
      brand-reputation: {score: 0.65, confidence: 0.70}
      capital-intensity: {score: 0.55, confidence: 0.75}
      scale-economies: {score: 0.65, confidence: 0.75}
      regulatory-barriers: {score: 0.80, confidence: 0.85}
      switching-costs: {score: 0.20, confidence: 0.75}
  model-estimate:
    s1: 0.231379
    r: 0.737129
  hhi: 0.117239
  method: selected-direct-ridge
  date: 2026-08-03
players:
  inputs:
    current:
      - rank: 1
        name: CSPC Pharmaceutical Group
        ticker: 1093.HK
        share: 0.45
      - rank: 2
        name: Simcere Pharmaceutical
        ticker: 2096.HK
        share: 0.18
      - rank: 3
        name: Mitsubishi Tanabe Pharma
        ticker: 4188.T
        share: 0.10
      - rank: 4
        name: EVER Pharma
        share: 0.07
      - rank: 5
        name: Pharmasoft
        share: 0.05
  override:
    - name: Argenica Therapeutics
      ticker: AGN.AX
      capture: 0.005
      reason: "Named outside contender: xaranetide has human safety and subgroup efficacy signals but remains pre-pivotal and under an FDA clinical hold, so 0.5% is a probability-weighted 2036 market capture rather than an if-approved share."
  model-estimate:
    - rank: 1
      name: CSPC Pharmaceutical Group
      ticker: 1093.HK
      hold-position-capture: 0.231379
      mobility-adjusted-capture: 0.184762
      mobility-adjusted-revenue: 1.385715
    - rank: 2
      name: Simcere Pharmaceutical
      ticker: 2096.HK
      hold-position-capture: 0.170556
      mobility-adjusted-capture: 0.139941
      mobility-adjusted-revenue: 1.049558
    - rank: 3
      name: Mitsubishi Tanabe Pharma
      ticker: 4188.T
      hold-position-capture: 0.125722
      mobility-adjusted-capture: 0.103339
      mobility-adjusted-revenue: 0.775042
    - rank: 4
      name: EVER Pharma
      hold-position-capture: 0.092673
      mobility-adjusted-capture: 0.077837
      mobility-adjusted-revenue: 0.583778
    - rank: 5
      name: Pharmasoft
      hold-position-capture: 0.068312
      mobility-adjusted-capture: 0.061199
      mobility-adjusted-revenue: 0.458993
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-03
---
# Global Acute Ischaemic Stroke Neuroprotection

## Market Definition

**Market scope:** worldwide prescription drugs and purpose-built devices administered during the acute ischaemic-stroke episode whose primary therapeutic purpose is to preserve threatened brain tissue, reduce reperfusion injury, or otherwise limit neuronal death. Regionally approved agents such as butylphthalide, edaravone, edaravone-dexborneol, Cerebrolysin and Mexidol are included when used for acute ischaemic stroke, as are future peptides, small molecules, biologics, cooling systems and other products approved with a direct acute-neuroprotection claim. Thrombolytics such as alteplase and tenecteplase, thrombectomy devices and procedure revenue, antiplatelet or anticoagulant therapy, diagnostics and imaging, stroke-unit care, rehabilitation, secondary prevention, chronic cognitive treatment, supplements and research-only interventions are excluded. The boundary does not count a legacy product's use after the acute episode or in another neurological indication.

**Revenue boundary:** annual revenue recognized by the drug or device manufacturer for the covered acute course, net of rebates and channel discounts. Hospital labour, infusion, imaging, procedure and distributor mark-ups are excluded. The addressable unit is one incident acute ischaemic-stroke episode that reaches medical care early enough to retain salvageable tissue; penetration is the `new-sales-share` of those structurally eligible episodes receiving at least one covered product. Billable units are drug courses, one-off doses, or single-patient device procedures. Pharmacological and device neuroprotection are separate operating segments and are summed once at manufacturer revenue. The base year is 2026, the fixed horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

This contract deliberately excludes the much broader “acute ischaemic stroke treatment” market. Reperfusion restores blood flow; this market measures the distinct adjunctive product revenue paid to protect brain tissue. A combined thrombolytic-neuroprotective molecule would include only the manufacturer revenue attributable to the approved neuroprotective claim unless the two functions cannot be sold separately, in which case the full net product revenue is included and the boundary mismatch is disclosed.

## Current View

The expected 2026 market value is **$0.55b**, with a rough **$0.30b-$1.0b** range. This is a small, geographically uneven commercial market despite a very large clinical burden. GBD 2021 reports 7.8 million incident ischaemic strokes worldwide; extrapolation of its rising absolute burden supports about 8.4 million incidents in 2026. However, no neuroprotectant has broad guideline-backed adoption across the United States and Europe. Revenue is concentrated in China, Japan, Russia and other markets where regionally approved products are used, while many acute courses are inexpensive and some labelled drugs have disputed evidence.

Two listed-company disclosures constrain the estimate but do not directly state the contract total. CSPC reported RMB7.817b of 2025 nervous-system revenue, with NBP (butylphthalide) a core product, but that segment also includes thrombolysis, Parkinson's, epilepsy and other products and NBP use beyond the acute episode. CSPC says NBP has benefited more than 40 million patients cumulatively. Simcere reported RMB2.753b of 2025 neuroscience revenue, another broad upper bound; within it, Sanbexin injection covered about 410,000 patients and held approximately 31% of China's “stroke injection” market in 2025. Neither company discloses boundary-matched acute neuroprotection revenue.

The bottom-up cross-check uses approximately 7.5 million structurally eligible episodes, about 12% current covered-product use, and roughly $610 of blended manufacturer revenue per treated episode. That produces about $0.55b. The blended realization covers low-priced China courses and generic regional products rather than assuming US specialty-drug pricing. A 2025 Chinese cost-effectiveness study used approximately RMB706 for a 14-day edaravone-dexborneol sublingual course and RMB29.68 per injection dose; those healthcare-system inputs are not manufacturer net revenue, but they confirm that today's largest-volume products are priced far below a novel US hospital biologic.

The principal current evidence is stronger in China than elsewhere. Simcere's injection was approved in China in 2020 and its sublingual formulation in 2024; the company says the injection and tablet are intended to form a 14-day sequential course. CSPC's NBP is established in China and the 1,216-patient BAST trial evaluated it alongside thrombolysis or thrombectomy. By contrast, multiple historical international neuroprotection programs failed, and nerinetide's 850-patient ESCAPE-NEXT Phase III registry results show 206 independent outcomes among 454 nerinetide participants versus 181 among 396 placebo participants—essentially no unadjusted difference. The current market is therefore commercial, but it is not yet a globally validated standard of care.

## Adoption Path

The expected 2036 market value is **$7.5b**, with a very wide **$1.3b-$20b** plausible range. The reference bridge grows incident ischaemic strokes to approximately 10 million, uses about 9 million structurally eligible acute episodes, assumes 38% receive a covered therapy, and applies about $2,200 of blended nominal manufacturer revenue per treated episode. That yields roughly 3.4 million treated episodes and $7.5b. The implied ten-year CAGR from today's narrow regional base is 29.8%, but that arithmetic should not be mistaken for a smooth forecast: most value arrives only after positive pivotal trials, major-market approvals, reimbursement and guideline adoption.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Incident ischaemic strokes | ~8.4m | ~10.0m | GBD 2021 base and published 2036 incidence direction; absolute-count estimate |
| Structurally eligible acute episodes | ~7.5m | ~9.0m | Reaches care while salvageable tissue remains; wider than thrombolytic eligibility |
| Covered-product penetration | ~12% | ~38% | Share of eligible episodes receiving at least one included therapy |
| Treated episodes | ~0.90m | ~3.4m | Eligible episodes multiplied by penetration |
| Manufacturer revenue per episode | ~$610 | ~$2,200 | Global blend of access-priced regional products and premium novel therapies |
| Annual market value | **$0.55b** | **$7.5b** | Manufacturer-recognized acute neuroprotection revenue; rounded |

No logistic penetration block is configured. There is no consistent global annual series for the share of eligible stroke episodes receiving a product within this contract: company patient counts cover different formulations and geographies, while national studies mix acute, subacute and chronic use. The 12% and 38% penetration points are disclosed sizing judgments, not fitted observations. Creating a pseudo-series from incompatible product volumes would add false precision.

The horizon price mix assumes roughly 1.4 million courses in high-income or premium-reimbursed settings at about $4,800 net and 2.0 million access-priced courses at about $400, for a blended $2,200. A single-dose therapy with demonstrated functional benefit can support meaningful value-based pricing because stroke disability costs are enormous, but the forecast remains well below the $10,000-$12,000 US alteplase comparison cited in Argenica's 2025 presentation. China procurement, branded competition and multi-product use put a ceiling on realization; the same patient cannot be counted twice merely because two neuroprotective mechanisms are combined.

The expected value reflects asymmetric development risk. A downside with no broadly approved modern therapy leaves a roughly $1.3b regional/generic market in 2036. A reference case with one or two positive-outcome products approved across major markets supports approximately $8b-$10b. An upside with safe pre-hospital delivery, several complementary mechanisms and strong functional-outcome economics can exceed $20b. Rough probability weighting across those states supports the stored $7.5b rather than treating clinical success as certain.

The largest sensitivities are whether functional benefit survives pivotal trials, the treatment window and eligible severity range, global reimbursement, and whether net prices reward disability avoided. TASTE-2 is encouraging: Simcere reported 90-day functional independence of 55.0% with edaravone-dexborneol plus thrombectomy versus 49.6% with placebo plus thrombectomy in 1,362 Chinese patients. But the nominal P value of 0.047, geographic concentration and two-week regimen leave room for regulatory and replication risk. Nerinetide's negative overall ESCAPE-NEXT outcome and decades of failed translation justify the wide downside.

## Market Structure

Direct network effects are essentially absent: one stroke centre gains no treatment benefit because another uses the same drug. Data scale has moderate value through larger safety databases, imaging-defined responder selection and trial-design learning, but patient-level data do not create an automatic feedback loop comparable with software. Brand and reputation matter because neurologists, emergency clinicians and payers will favour therapies with clean functional-outcome evidence in a time-critical setting.

Regulatory barriers are high. Large acute-stroke trials require rapid consent, heterogeneous patients, imaging selection, drug compatibility with thrombolysis and thrombectomy, and 90-day disability endpoints. Argenica's FDA clinical hold despite completed Australian Phase II work illustrates how non-clinical and protocol requirements can delay a small entrant. Capital intensity and scale economies are meaningful because global pivotal trials, sterile manufacturing, hospital distribution and post-market safety are fixed-cost heavy. Switching costs are low at the patient level—each stroke is a new episode—but formulary inclusion, guideline placement and hospital protocols create some institutional persistence.

The structural model is intended to represent the 2036 manufacturer-revenue pool, not today's China-heavy share distribution. Broader approvals should reduce today's leader concentration by admitting differentiated mechanisms and global commercial partners, while regulatory fixed costs prevent a fully fragmented field. The model yields a **23.14%** horizon leader share, **73.71%** rank-to-rank decay and **0.1172 HHI**, equivalent to about **8.5 equal-sized competitors**. This is moderately concentrated: several scaled therapies can coexist, while the approval and evidence burden limits the tail. The geometric shares total about 88%, so the curve remains inside its valid fringe regime. No concentration override is used.

## Players

Current shares are low-confidence estimates on the whole contract: CSPC 45%, Simcere 18%, Mitsubishi Tanabe 10%, EVER Pharma 7% and Pharmasoft 5%, leaving 15% for generic edaravone, citicoline and other regionally marketed products. CSPC's NBP scale, 40-million-patient cumulative disclosure and RMB7.817b nervous-system segment support first place. Simcere's 410,000 Sanbexin-injection patients and 31% share of China's stroke-injection submarket support second place, but its submarket share is not a global neuroprotection share. The remaining ranks are triangulated from regional product presence rather than audited revenue, so mobility outputs should be read as a structural base rate.

CSPC can retain a leading position through NBP's installed clinical base, evidence generation and China distribution, but can lose share if pivotal global products displace therapies with mostly regional acceptance. Simcere has the strongest current path toward international validation: Sanbexin sublingual tablets have FDA Breakthrough Therapy designation, and its China injection/tablet franchise now has randomized functional-outcome evidence. Mitsubishi Tanabe's edaravone heritage provides recognition and manufacturing experience, while generic erosion and uncertain Western AIS adoption cap its position. EVER Pharma's Cerebrolysin and Pharmasoft's Mexidol retain regional channels but face the greatest evidence and pricing risk.

NoNO remains a scientifically important outside competitor, but ESCAPE-NEXT did not show the expected overall functional benefit. Its 600-patient NoNO-42 Phase II trial was recruiting in the current ClinicalTrials.gov record and tests a new formulation in patients selected for thrombolysis with or without thrombectomy. Cooling, normobaric oxygen, intra-arterial delivery and other devices remain contenders, but most are earlier or operationally more complex.

Argenica Therapeutics is stored as a **0.5% canonical outside-contender capture**, equivalent to about **$38m of 2036 revenue** at the market midpoint. This is an expected, probability-weighted market view—not an “if xaranetide succeeds” case. Xaranetide was safe and tolerated in Argenica's 92-patient Phase II SEANCON trial, but the overall secondary infarct-volume endpoint was negative. The stronger results are subgroup and post-hoc AI-standardized signals in severe strokes. As of 11 June 2026, Argenica had completed the three FDA-requested safety assays but still needed a Phase IIb protocol and a successful response to lift the clinical hold. Those facts do not support assuming a major share today; they do justify naming the company rather than burying it in the fringe.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| CSPC Pharmaceutical Group (1093.HK) | 23.14% | **18.48%** | **$1.39b** |
| Simcere Pharmaceutical (2096.HK) | 17.06% | **13.99%** | **$1.05b** |
| Mitsubishi Tanabe Pharma / Mitsubishi Chemical Group (4188.T) | 12.57% | **10.33%** | **$0.78b** |
| EVER Pharma | 9.27% | **7.78%** | **$0.58b** |
| Pharmasoft | 6.83% | **6.12%** | **$0.46b** |
| Argenica Therapeutics (AGN.AX), outside-contender override | n/a | **0.50%** | **$0.038b** |

Mobility reduces each incumbent relative to simply retaining today's rank because the pooled ten-year base rate allows entry, rank churn, fringe migration and a **10.06% gone probability** that is already embedded in adjusted capture. The five incumbent estimates total about 56.7%; Argenica's override and unnamed future entrants take part of the remainder. Mobility is a coarse pooled base rate: it sees current rank and share spacing but not pivotal-trial success, patent life, licensing partners, pricing, or an acquisition. Argenica's explicit outside-contender override is therefore separate from the incumbent model estimates.

## Watch

- Simcere's US or global pivotal protocol, IND timing and whether TASTE-SL/TASTE-2 functional benefit replicates outside China.
- Full peer-reviewed TASTE-2 effect size, multiplicity treatment, subgroup consistency and regulatory interpretation.
- China procurement price and acute-only patient volumes for NBP and Sanbexin, separated from chronic or other neuroscience uses.
- Results and publication of NoNO-42, plus the commercial response to negative ESCAPE-NEXT overall data.
- Argenica's FDA clinical-hold response, final Phase IIb design, funding or partner, pre-specified imaging severity criteria and trial start.
- Whether xaranetide's apparent severe-stroke benefit replicates prospectively rather than remaining a subgroup/post-hoc signal.
- Guideline treatment of edaravone-dexborneol, butylphthalide, Cerebrolysin and other regionally approved agents.
- Hospital net pricing, reimbursement and disability-avoidance evidence for any first broadly approved product.
- Pre-hospital feasibility and compatibility with alteplase, tenecteplase and thrombectomy workflows.
- Neuroprotective devices or combination products broadening the contract beyond drugs without double-counting reperfusion revenue.

## Peer Comparison

**Boundary-mismatched and therefore not directly comparable:** Argenica's May/August 2025 presentations cited Verified Market Research's global thrombolytic-drug market at **$1.1b in 2022 and $3.8b in 2030**. Our interpolated 2030 neuroprotection estimate is about **$1.7b**, so the thrombolytic forecast is roughly 124% higher. It measures clot-dissolving drugs rather than tissue protection, uses a narrower eligible population and much higher per-dose US pricing; it is a workflow analogue, not a peer estimate of this market.

**Approximately 56% over our 2036 estimate, but not boundary matched:** the previous AGN.AX stock note carried an **A$18b** eight-year “it works” TAM, about **US$11.7b** at a representative 0.65 USD/AUD conversion, based on a broad acute-ischaemic-stroke drug-treatment opportunity. Against this document's US$7.5b expected 2036 manufacturer-revenue pool, that is approximately 56% higher before aligning the year. The stock input includes an explicit success framing and was not a probability-weighted, neuroprotection-only market contract, so it should not be substituted here.

No useful 5–10 year publication was found for the same acute-neuroprotection manufacturer-revenue boundary. Published market-research pages generally combine thrombolytics, antiplatelets, anticoagulants, diagnostics or all stroke therapeutics, while clinical publications forecast epidemiology rather than product revenue. The absence of a matching peer is itself decision-useful: the stored estimate rests on the patient, adoption and price bridge above, not on a category label copied from a broader report.

## Sources

- Liu et al., “Epidemiology and future trend predictions of ischemic stroke based on the global burden of disease study 1990–2021,” *Communications Medicine*, 3 July 2025; 7.8 million incident ischaemic strokes in 2021 and rising projected incidence through 2036: https://www.nature.com/articles/s43856-025-00939-y
- CSPC Pharmaceutical Group, 2025 Annual Report, released 24 March 2026; RMB7.817b nervous-system revenue, NBP product and cumulative-patient disclosures: https://doc.irasia.com/listco/hk/cspc/annual/2025/ar2025.pdf
- Simcere Pharmaceutical Group, 2025 Annual Report, released 28 April 2026; RMB2.753b neuroscience revenue, 410,000 Sanbexin-injection patients and approximately 31% China stroke-injection share: https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0428/2026042803397.pdf
- Simcere, “China NMPA approves Simcere's Sanbexin sublingual tablets,” 4 December 2024; China approval, 14-day sequential therapy and more than three million patients helped by the injection over four years: https://www.simcere.com/news/detail.aspx?mtt=1480
- Simcere, “TASTE-2 study published in The BMJ,” 7 January 2026; 1,362 participants and 55.0% versus 49.6% 90-day functional independence: https://www.simcere.com/en/news/detail.aspx?mtt=1569
- Menet et al., “Cost-effectiveness of edaravone dexborneol sublingual tablet versus concentrated solution for injection,” *Frontiers in Pharmacology*, 13 November 2025; 14-day regimen and China cost inputs: https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2025.1661581/full
- ClinicalTrials.gov, ESCAPE-NEXT (NCT04462536), record updated 22 June 2025; 850 participants and posted results: https://clinicaltrials.gov/study/NCT04462536
- ClinicalTrials.gov, NoNO-42 (NCT06403267), record accessed 3 August 2026; 600-patient Phase II recruiting study: https://clinicaltrials.gov/study/NCT06403267
- ClinicalTrials.gov, BAST (NCT03539445), 1,216-patient Phase III butylphthalide study: https://clinicaltrials.gov/study/NCT03539445
- Dammavalam et al., “Neuroprotection during Thrombectomy for Acute Ischemic Stroke: A Review of Future Therapies,” *International Journal of Molecular Sciences*, 2024: https://pubmed.ncbi.nlm.nih.gov/38255965/
- Argenica Therapeutics, “Topline Phase 2 Trial Results of ARG-007 in AIS Patients,” 3 September 2025; safety primary met, negative overall infarct-volume secondary endpoint and 92 participants: https://wcsecure.weblink.com.au/clients/argenica/headline.aspx?headlineid=61281868
- Argenica Therapeutics, “AI Analysis Reveals Efficacy in Severe Stroke Patients,” 11 December 2025; post-hoc imaging-standardized subgroup results and severe-patient target: https://wcsecure.weblink.com.au/clients/argenica/headline.aspx?headlineid=61302835
- Argenica Therapeutics, “ARG-007 (Xaranetide) Completes All Three FDA Requested Assays,” 11 June 2026; clinical-hold status and Phase IIb prerequisites: https://wcsecure.weblink.com.au/clients/argenica/headline.aspx?headlineid=61329022
- Argenica Therapeutics, investor presentation, 19 May 2025; thrombolytic-market workflow comparison citing Verified Market Research: https://wcsecure.weblink.com.au/clients/argenica/headline.aspx?headlineid=61265085
- Verified Market Research, “Thrombolytic Drug Market,” cited by Argenica for $1.1b in 2022 and $3.8b in 2030; boundary does not match neuroprotection: https://www.verifiedmarketresearch.com/product/thrombolytic-drug-market/
