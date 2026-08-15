---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.06
  maturity-market-value: 1.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.10, confidence: 0.80}
      data-scale-advantage: {score: 0.55, confidence: 0.55}
      brand-reputation: {score: 0.60, confidence: 0.60}
      capital-intensity: {score: 0.20, confidence: 0.80}
      scale-economies: {score: 0.70, confidence: 0.70}
      regulatory-barriers: {score: 0.70, confidence: 0.75}
      switching-costs: {score: 0.65, confidence: 0.65}
  model-estimate:
    s1: 0.133727
    r: 0.849573
  hhi: 0.064275
  method: selected-direct-ridge
  date: 2026-08-02
players:
  inputs:
    current:
      - rank: 1
        name: VIDA Diagnostics
        share: 0.28
      - rank: 2
        name: Thirona
        share: 0.20
      - rank: 3
        name: 4DMedical
        ticker: 4DX.AX
        share: 0.08
  model-estimate:
    - rank: 1
      name: VIDA Diagnostics
      hold-position-capture: 0.133727
      mobility-adjusted-capture: 0.108381
      mobility-adjusted-revenue: 0.108381
    - rank: 2
      name: Thirona
      hold-position-capture: 0.113611
      mobility-adjusted-capture: 0.095104
      mobility-adjusted-revenue: 0.095104
    - rank: 3
      name: 4DMedical
      ticker: 4DX.AX
      hold-position-capture: 0.096521
      mobility-adjusted-capture: 0.086997
      mobility-adjusted-revenue: 0.086997
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-02
---
# Global CT-Derived Pulmonary Function Imaging Software

## Market Definition

**Market scope:** worldwide software and software-enabled analysis services that turn thoracic CT images into quantitative pulmonary structure or function outputs used in respiratory diagnosis, treatment planning, longitudinal monitoring, or respiratory-drug development. Included outputs are ventilation, perfusion, air trapping, lung density, airway, emphysema, fibrosis, and pulmonary-vascular measurements when sold as pulmonary quantitative imaging. CT:VQ, XV LVAS, CT LVAS, LDAf and comparable specialist products are included. CT scanners, PACS and general radiology workflow, radiologist fees, hospital or imaging-centre reimbursement, contrast media, nuclear-medicine equipment and radiopharmaceuticals, MRI-only products, general chest-AI triage, lung-nodule malignancy detection, cancer screening and patient-navigation software are excluded.

**Revenue boundary:** annual revenue recognized by the specialist software or analysis-service provider from licences, subscriptions, per-scan fees, and pulmonary imaging analysis for clinical trials. This is not the reimbursement or customer spend attached to the underlying CT, V/Q, CTPA, intervention, or drug trial. The addressable unit is an eligible thoracic CT study that could structurally benefit from specialist pulmonary quantification. Penetration is the `spend-share` of eligible annual studies whose workflow pays an included specialist provider; it is not the share of hospitals owning a CT scanner. Billable units are analysed scans, site or enterprise subscription-years, and contracted clinical-trial imaging services. Clinical care and biopharma trials are separate segments because contracting and revenue intensity differ, then are summed at the same provider-recognized boundary. The base year is 2026, the fixed horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

## Current View

The expected 2026 market is approximately **$60m**, with a rough **$35m-$100m** range. There is no boundary-matched published market total: private specialists do not disclose pulmonary-only revenue, diversified imaging vendors do not separate these modules, and broad “medical image analysis” reports include hardware, oncology and unrelated anatomy. The estimate therefore starts with 4DMedical's FY26 operating revenue of A$7.2m (about US$4.7m at a rounded US$0.65/A$), which was generated across 540 SaaS sites and 344,075 annual scan analyses. Treating all of it as included is a conservative upper bound on 4DMedical's numerator because the company also sells some non-functional cardiothoracic tools. An estimated 8% share on that basis implies a market near $60m.

The gross-up is cross-checked against larger private footprints. VIDA documented more than 1,000 enabled imaging sites across more than 40 countries in 2022 and still described an extensive global trial-site network when announcing its September 2025 Thirona partnership. The same announcement says Thirona's LungQ portfolio is installed in more than 1,200 hospitals worldwide and validated in more than 200 peer-reviewed publications. Those installed-footprint measures are not revenue, but they support ranking both above 4DMedical today. The resulting market value should be read as an order-of-magnitude reconstruction, not audited industry revenue.

## Adoption Path

The 2036 expected value is **$1.0b**, with a broad **$0.4b-$2.0b** plausible range. The bridge uses roughly 20 million eligible annual thoracic CT studies worldwide by 2036, 35% paid specialist-analysis penetration, and about $120 of nominal provider revenue per analysed scan, producing about $0.84b. Site subscriptions, enterprise minimums and respiratory clinical-trial analysis add about $0.16b without counting the underlying CT reimbursement or pharmaceutical trial spend. The implied 32.5% ten-year CAGR is high but starts from a tiny commercial base and assumes quantitative outputs move from specialist and trial use into routine clinical pathways.

No logistic penetration block is configured. A boundary-matched adoption history does not exist, and 4DMedical's site series would measure one vendor across a broader product portfolio rather than whole-market paid-study penetration. The 5% and 35% figures below are disclosed sizing judgments, not fitted observations.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Eligible annual thoracic CT studies | ~10m | ~20m | Existing V/Q and CTPA pathways plus defined respiratory planning, monitoring and trial use; rounded |
| Paid specialist-analysis penetration | ~5% | ~35% | Spend-share of eligible studies; analyst estimate |
| Paid analysed studies | ~0.5m | ~7.0m | Eligible studies multiplied by penetration |
| Net provider revenue per analysed study | ~$90 | ~$120 | Nominal blended per-scan realization; excludes imaging-provider reimbursement |
| Scan-linked provider revenue | ~$45m | ~$840m | Annual analysed studies multiplied by provider realization |
| Site, enterprise and trial revenue | ~$15m | ~$160m | Minimum subscriptions and contracted analysis not already charged per scan |
| Annual market value | **$60m** | **$1.0b** | Provider-recognized revenue; rounded expected value |

The addressable-study count is anchored to 4DMedical's July 2026 statement that the U.S. pathway comprises about one million existing nuclear V/Q studies plus roughly five million CTPA studies. The global conversion is deliberately below a mechanical extrapolation of management's reimbursement-framed opportunity because software-provider revenue is narrower than the value of the medical procedure. Additional use cases such as lung-volume-reduction selection, pulmonary-hypertension assessment and respiratory drug biomarkers are included only where they purchase the same pulmonary quantitative-analysis layer. Lung-cancer detection and incidental-finding adjacencies remain excluded.

The principal sensitivities are clinical evidence and reimbursement supporting routine use, the fraction of CTPA or nuclear V/Q workflows that actually migrate, and how much procedure economics the software vendor retains. A $60-$180 per-scan horizon range moves the core pool by roughly half in either direction. The analysis-service model has no durable-equipment installed-base replacement stream: recurring revenue comes from each new study, subscriptions and trials.

## Market Structure

Direct network effects are weak because one hospital receives little extra value merely because another hospital uses the same analysis. Scale is still important: regulatory submissions, disease-specific validation, scanner and PACS integration, secure cloud infrastructure, sales coverage and trial-site support are mostly fixed costs. Proprietary annotated data and multi-centre outcome data can improve algorithms and acceptance, but hospitals and sponsors can generate or license comparable datasets and returns should diminish. Regulatory clearance, quality systems, patents and clinical evidence create meaningful entry delay without legally limiting the number of vendors.

Reputation matters because clinicians, hospitals and pharmaceutical sponsors bear safety, trial-integrity and procurement risk. Switching costs are also meaningful once a tool is validated in a protocol, integrated into workflow, embedded in longitudinal measurements, or specified across a multi-year trial. They protect multiple incumbents rather than creating one global monopoly. Low capital intensity and weak network effects leave room for disease specialists, imaging OEM modules and geographically strong vendors, so the 2036 market should be fragmented-to-moderately concentrated despite software scale economics.

The structural model yields a 13.37% horizon leader share, an 84.96% rank-to-rank decay ratio, and HHI of 0.0643, equivalent to about 15.6 equal-sized competitors. This is at the fragmented edge of the market-doc reading table and is consistent with multiple protected clinical and trial incumbencies plus a substantial specialist tail. The result is a coarse central estimate; no concentration override is used.

## Players

Current shares are analyst estimates on the whole narrow revenue boundary: VIDA Diagnostics 28%, Thirona 20%, and 4DMedical 8%, leaving 44% for imaging-OEM modules, clinical-research organizations, regional specialists and unlisted tools. VIDA's documented 1,000-plus-site trial network, global trial-management control point and broad respiratory biomarker platform support rank one. Thirona's 1,200-plus hospital installations and 200-plus-publication validation base support rank two. 4DMedical's A$7.2m FY26 operating revenue, 540 sites and 344,075 scans support an approximately 8% ceiling on current share; the exact included fraction is unavailable, so its rank and share remain low confidence.

4DMedical can gain rank because CT:VQ combines ventilation and perfusion from routine non-contrast CT, has entered full commercial use at five U.S. academic medical centres, and is moving into SimonMed's 170-plus-centre outpatient network on per-scan commercial terms. Its July filing also reports paid Australian contracts, a respiratory-imaging analytics contract with GSK, and a CLEAR study pathway into acute pulmonary embolism. It can lose capture if head-to-head evidence does not change clinical practice, reimbursement accrues mainly to imaging providers rather than the software vendor, or incumbents and CT OEMs replicate or bundle comparable outputs.

VIDA has a strong clinical-trial control point, a large global site network and a broad respiratory biomarker set, but may capture less routine-care revenue if trials remain its centre of gravity. Thirona has extensive installed reach and validated structural lung quantification, including a partnership with VIDA, but partnership and multi-vendor workflows also demonstrate that customers can combine suppliers. Large scanner vendors, research-platform providers and new cleared algorithms are credible outside contenders. No company-specific capture override is used; the pooled mobility result is the canonical ten-year view.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| VIDA Diagnostics | 13.37% | 10.84% | $108.4m |
| Thirona | 11.36% | 9.51% | $95.1m |
| 4DMedical (4DX.AX) | 9.65% | **8.70%** | **$87.0m** |

Mobility reduces each incumbent for rank churn, entry from outside the current top three and a pooled 10.06% gone probability that is already embedded in the adjusted captures. 4DMedical's model revenue is positive and equals its 8.70% adjusted capture multiplied by the $1.0b 2036 market. The model does not see CT:VQ's company-specific momentum, financing, clinical differentiation or execution risk, so those factors remain stock-level judgments rather than an unsupported override here.

## Watch

- Separate CT:VQ and pulmonary-analytics revenue, paid scan volume, and realized provider revenue per scan at 4DMedical.
- SimonMed's August 2026 launch, paid study ramp and conversion from academic centres into community imaging.
- CLEAR head-to-head results versus CTPA and any new indication, guideline or reimbursement decision.
- Durable U.S. payer realization beyond the published procedure reimbursement and Australia's MBS pathway.
- Comparable revenue or annual paid-study disclosure from VIDA, Thirona and imaging-OEM modules.
- Multi-year trial wins, renewal rates and whether biomarker platforms standardize on one provider or remain multi-vendor.
- Competitive FDA clearances or OEM-bundled ventilation, perfusion and quantitative lung-analysis tools.

## Peer Comparison

No independent five-to-ten-year forecast was found with this provider-recognized, pulmonary-CT-only boundary. Available reports for “medical image analysis software,” “AI in medical imaging,” and “lung cancer screening” mix unrelated anatomy, hardware, radiology workflow, or malignancy detection that this contract explicitly excludes. 4DMedical's July 2026 **US$3b U.S. obtainable-market** statement is also not directly comparable: it applies to roughly one million V/Q and five million CTPA studies and is framed around the clinical imaging opportunity, whereas this document recognizes only the specialist software provider's per-scan, licence, subscription and trial-analysis revenue. The management figure is therefore an addressable-procedure-spend ceiling, not a peer forecast of the $1.0b global provider-revenue estimate, and it did not change the stored inputs.

## Sources

- 4DMedical, “Quarterly Activity Report and Appendix 4C for Q4 FY26,” 31 July 2026: https://announcements.asx.com.au/asxpdf/20260731/pdf/0728mtlwfrq57v.pdf
- VIDA Diagnostics, “VIDA Network Expands Beyond 1,000 Sites Globally,” 16 May 2022; more than 1,000 enabled sites in more than 40 countries: https://blog.vidalung.ai/vida-network-1000-sites
- VIDA Diagnostics, “VIDA Partners with Thirona to Expand Respiratory Clinical Trial Imaging Capabilities,” 27 September 2025; current platform scope, extensive global network, and Thirona footprint: https://blog.vidalung.ai/vida-partners-with-thirona-to-expand-respiratory-clinical-trial-imaging-capabilities
- Thirona, LungQ platform and pulmonary precision-medicine scope, accessed 2 August 2026: https://thirona.eu/
- Coreline Soft, chest-CT analysis product and company overview, reviewed as an outside-contender check, accessed 2 August 2026: https://corelinesoft.com/en/
