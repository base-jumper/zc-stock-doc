---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.92
  maturity-market-value: 7.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.05, confidence: 0.90}
      data-scale-advantage: {score: 0.45, confidence: 0.65}
      brand-reputation: {score: 0.75, confidence: 0.80}
      capital-intensity: {score: 0.65, confidence: 0.75}
      scale-economies: {score: 0.75, confidence: 0.75}
      regulatory-barriers: {score: 0.90, confidence: 0.90}
      switching-costs: {score: 0.20, confidence: 0.75}
  model-estimate:
    s1: 0.285994
    r: 0.68972
  hhi: 0.156008
  method: selected-direct-ridge
  date: 2026-08-08
players:
  inputs:
    current:
      - rank: 1
        name: Inspire Medical Systems
        ticker: INSP
        share: 0.934
      - rank: 2
        name: Nyxoah
        ticker: NYXH
        share: 0.040
      - rank: 3
        name: ZOLL Medical
        share: 0.020
      - rank: 4
        name: LivaNova
        ticker: LIVN
        share: 0.006
  override:
    - name: ZOLL Medical
      capture: 0.04
      reason: "Company-specific boundary adjustment: remedē addresses the smaller CSA segment and ZOLL has no disclosed OSA implant platform, so the pooled rank-mobility model's 12.3% whole-market capture is too high absent an acquisition or indication expansion."
  model-estimate:
    - rank: 1
      name: Inspire Medical Systems
      ticker: INSP
      hold-position-capture: 0.285994
      mobility-adjusted-capture: 0.235382
      mobility-adjusted-revenue: 1.647674
    - rank: 2
      name: Nyxoah
      ticker: NYXH
      hold-position-capture: 0.197256
      mobility-adjusted-capture: 0.16295
      mobility-adjusted-revenue: 1.14065
    - rank: 3
      name: ZOLL Medical
      hold-position-capture: 0.136051
      mobility-adjusted-capture: 0.122808
      mobility-adjusted-revenue: 0.859656
    - rank: 4
      name: LivaNova
      ticker: LIVN
      hold-position-capture: 0.093837
      mobility-adjusted-capture: 0.08705
      mobility-adjusted-revenue: 0.60935
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-08
---
# Global Sleep-Apnea Neuromodulation Devices

## Market Definition

**Market scope:** worldwide implantable neuromodulation systems whose labelled therapeutic purpose is to treat obstructive sleep apnoea (OSA), central sleep apnoea (CSA), or a defined sleep-apnoea subtype by electrically stimulating an upper-airway nerve, the phrenic nerve, or another neural target. Initial pulse generators or stimulators, leads or electrodes, implanted sensors, patient remotes or activation chips, manufacturer-supplied disposable patches, replacement generators and device-specific monitoring or programming sold with the system are included. Diagnostic sleep studies, CPAP and other positive-airway-pressure equipment, oral appliances, GLP-1 drugs, conventional airway surgery, hospital and surgeon procedure revenue, anaesthesia, generic remote-patient-monitoring fees and research-only devices are excluded.

**Revenue boundary:** annual net revenue recognized by the device manufacturer for included systems, replacements, accessories and device-specific recurring supplies. Hospital procurement is counted at the manufacturer's recognized selling price; facility reimbursement, physician fees, distributor mark-ups and total episode cost are not. The **addressable unit** is one annual implant-treatment decision by a diagnosed moderate-to-severe sleep-apnoea patient who has failed, cannot tolerate or is ineligible for first-line therapy and meets the relevant device's anatomical, physiological and coverage criteria. **Penetration** is the `new-sales-share` of those annual treatment decisions resulting in an implant. **Billable units** are new systems, replacement generators/components, and attached manufacturer-sold accessories or supplies. OSA upper-airway stimulation and CSA phrenic-nerve stimulation are modelled as separate clinical segments and summed once at manufacturer revenue. The base year is 2026, the fixed horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

This contract is narrower than the full sleep-apnoea devices or treatment market and wider than hypoglossal-nerve stimulation alone. It deliberately includes remedē-style CSA devices because they are implantable sleep-apnoea neuromodulation, but it excludes the much larger clinical procedure bill around every implant.

## Current View

The expected 2026 market value is **$0.92b**, with a rough **$0.86b-$1.0b** range. Inspire Medical Systems anchors the estimate: its August 2026 guidance is $835m-$875m after first-half revenue of $405.2m. The midpoint, $855m, is already about 93% of the stored whole-market estimate and makes third-party category estimates below Inspire's reported revenue definitionally suspect.

Nyxoah reported first-half 2026 Genio revenue of EUR14.0m, including EUR9.5m in the United States, after FDA approval in August 2025. A simple second-half launch acceleration supports roughly $35m-$40m of 2026 revenue. ZOLL does not disclose remedē revenue separately, and LivaNova only received FDA PMA for aura6000 in March 2026; approximately $18m and $5m respectively are low-confidence placeholders. Together those four estimates reconcile to about $0.92b without adding facility or physician reimbursement.

Inspire's disclosed scale is the best volume check. Its August 2026 investor materials cite more than 140,000 cumulative patients, more than 1,500 implanters and more than $900m of 2025 revenue. Revenue divided by plausible annual implants implies manufacturer realization in the mid-$20,000s per new system. The 2026 midpoint therefore corresponds to roughly 35,000-40,000 new systems plus small replacement and accessory revenue, consistent with an early durable-device market rather than the cumulative installed base multiplied by price.

Current revenue evidence is unusually strong for the leader and weak for the private CSA segment. The $0.92b midpoint should move nearly dollar-for-dollar with Inspire's final 2026 result unless undisclosed remedē revenue proves material.

## Adoption Path

The expected 2036 market value is **$7.0b**, with a broad **$3.0b-$12b** plausible range. The reference bridge expands annual clinically and commercially actionable implant decisions from roughly 0.75 million in 2026 to 1.8 million in 2036 as diagnosis, surgeon capacity, reimbursement and product eligibility broaden. It raises implant share from about 5% to 17.5%, producing approximately 315,000 new implants. At about $20,000 of blended nominal manufacturer revenue per new system, new implants contribute $6.3b; replacement generators, Genio patches and other included recurring components contribute another $0.7b.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Annual eligible implant decisions | ~0.75m | ~1.8m | Refractory, anatomically eligible OSA plus smaller CSA flow in served markets |
| New-implant share | ~5% | ~17.5% | Share of annual eligible treatment decisions receiving neuromodulation |
| New implant systems | ~37,000 | ~315,000 | Eligible flow multiplied by implant share |
| Net manufacturer revenue per new system | ~$24,000 | ~$20,000 | Global mix; nominal price with real price pressure and lower-priced bilateral systems |
| Replacement/accessory revenue | ~$0.03b | ~$0.7b | Generator replacements, patches and device-specific components |
| Annual market value | **$0.92b** | **$7.0b** | Manufacturer-recognized revenue; rounded |

The implied ten-year CAGR is about **22.5%**. That is slower than Inspire's five-year historical growth but faster than many paid market-research forecasts. It requires a roughly eightfold increase in implant flow, not full penetration of the enormous epidemiological pool. Benjafield et al. estimated 936 million adults aged 30-69 with any OSA and 425 million with moderate-to-severe OSA in 2019; the binding denominator here is the much narrower stream that is diagnosed, refractory to first-line treatment, anatomically eligible, insured or funded, and able to reach a trained implant centre.

No logistic penetration block is configured. Public disclosures provide cumulative implants, company revenue and isolated launch metrics, but not a consistent annual series for implant share of the contract's global eligible-decision flow. Inspire's roughly 500,000 annual U.S. eligible-patient estimate is an internal funnel estimate, while reported cumulative patients and Nyxoah account activations use different geographies and denominators. Treating them as one time series would create false precision.

The durable-device bridge explicitly separates new systems from the installed base. A roughly 10-15 year generator life means the majority of 2036 revenue still comes from new implants, while the cohorts implanted during the 2020s begin to create a meaningful replacement stream. Genio's external activation chip and disposable patches add recurring revenue but do not justify applying a subscription to every implanted system. The biggest sensitivities are referral and diagnosis growth, coding and reimbursement, implant-centre capacity, competition from GLP-1 weight-loss therapy, real system pricing, and expansion into complete concentric collapse or broader BMI and AHI ranges.

## Market Structure

Direct network effects are almost absent: one patient's implant does not become more effective because other patients use it. There is a moderate data-scale advantage because large registries, device telemetry and therapy-optimization data can improve programming, safety surveillance and physician confidence, but clinical outcomes remain reproducible through trials and do not create a software-like feedback monopoly. Brand and reputation are strong because a permanently implanted device demands trust from patients, surgeons, payers and hospital committees.

Capital and scale barriers are substantial. A credible entrant must fund implant engineering, long pivotal trials, PMA approval, manufacturing validation, reimbursement, field clinical support, surgeon training and post-market surveillance. Unit economics improve with manufacturing volume and a denser field organization, so subscale challengers absorb materially higher commercial cost per implant. Regulatory and IP barriers are very high, although approvals for Genio and aura6000 show that the market is not legally closed.

Switching costs are deliberately scored low for market-share prediction. A patient with an implanted system is highly locked in, but the addressable revenue flow is mostly new patients making first-time choices. Surgeons can train on more than one system, and hospitals can stock competing devices; workflow familiarity creates friction but not the multi-year data migration found in enterprise software.

The structural model represents the 2036 global manufacturer-revenue pool rather than today's near-monopoly. It yields a **28.60%** leader share, **68.97%** rank-to-rank decay and **0.1560 HHI**, equivalent to about **6.4 equal-sized competitors**. That is moderately concentrated: Inspire, Nyxoah, LivaNova, ZOLL and additional approved designs can coexist as indications and geographies broaden, but clinical, regulatory and field-support barriers keep the market from fragmenting into dozens of scaled manufacturers. The geometric shares total about 92%, and `s1` remains below `1-r`, so the curve retains a valid competitive fringe. No concentration override is used.

## Players

Current whole-market shares are estimated at Inspire 93.4%, Nyxoah 4.0%, ZOLL 2.0% and LivaNova 0.6%. Inspire and Nyxoah are anchored to disclosed revenue or guidance; ZOLL and LivaNova are low-confidence estimates because neither discloses boundary-matched sleep-apnoea device revenue. The shares refer to manufacturer revenue across both OSA and CSA, not unit share within the narrower hypoglossal-stimulation segment.

Inspire brings the deepest clinical evidence, installed commercial channel, trained-surgeon base, reimbursement coverage and a closed-loop sensing system. Its risks are coding friction around Inspire V, real price pressure, Genio's incision and battery architecture, aura6000's multi-contact stimulation, and GLP-1 treatment delaying referrals. Nyxoah has FDA approval, a bilateral battery-free implant, 180 active high-volume U.S. accounts and EUR14m of first-half 2026 revenue; it can gain share quickly from a small base but must prove manufacturing yield, field execution and long-term adherence.

ZOLL's remedē system is the established transvenous phrenic-nerve therapy for moderate-to-severe CSA, a smaller and clinically distinct segment with cardiology-channel advantages. LivaNova's aura6000 received FDA PMA in March 2026 and inherits a scaled neuromodulation organization; it is the most credible newly approved outside design, but launch revenue is not separately reported and its commercial share remains negligible. Other future entrants may address complete concentric collapse, less invasive placement, lower prices or closed-loop optimization.

| Current player | Hold-position capture | Mobility model | Canonical capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: | ---: |
| Inspire Medical Systems (INSP) | 28.60% | 23.54% | **23.54%** | **$1.65b** |
| Nyxoah (NYXH) | 19.73% | 16.30% | **16.30%** | **$1.14b** |
| ZOLL Medical | 13.61% | 12.28% | **4.00%** | **$0.28b** |
| LivaNova (LIVN) | 9.38% | 8.70% | **8.70%** | **$0.61b** |

Mobility reduces every incumbent relative to simply holding its current rank because the pooled ten-year base rate allows entry, rank churn, fringe migration and a **10.06% gone probability** already embedded in adjusted capture. Inspire still has the largest expected share, but today's 93% revenue position is not projected to persist after three approved OSA systems, a separate CSA system and future entrants have a decade to scale.

ZOLL is the one company-specific override. Its pooled mobility result is 12.28%, but remedē addresses the smaller CSA segment and ZOLL has no disclosed OSA implant platform; **4.0% canonical capture** is more consistent with the market contract absent an acquisition or indication expansion. The model's $0.86b result remains visible above as a structural rank view, while the canonical $0.28b is the expected company view. The four canonical captures total about 52.5%, leaving room for future entrants and the unnamed geometric fringe. Mobility is a coarse pooled base rate: it does not see architecture, coding position, clinical outcomes, litigation, patent life or launch quality.

## Watch

- Inspire's final 2026 revenue versus the $835m-$875m guidance range and recovery from Inspire V coding/reimbursement friction.
- Genio U.S. implant conversion from the 427-patient prior-authorization pipeline, account productivity, gross margin and disposable-patch attachment.
- aura6000 commercial launch timing, separate revenue disclosure, reimbursement coding and comparative effectiveness after March 2026 PMA.
- remedē procedure growth and any ZOLL disclosure that allows the CSA segment to be sized directly.
- Whether GLP-1 treatment expands diagnosis and ultimately feeds implants or durably reduces the eligible refractory OSA pool.
- Label expansion for complete concentric collapse, BMI, AHI severity, paediatric OSA and additional anatomical phenotypes.
- Ten-year generator longevity, replacement pricing, revision/explant rates and recurring manufacturer revenue per installed patient.
- Surgeon and sleep-clinic capacity, time from referral to implant, and whether simpler procedures raise annual centre throughput.
- Patent litigation between Inspire and Nyxoah and the durability of sensing, lead, stimulation-pattern and battery architecture claims.
- Evidence that remote programming or closed-loop algorithms create a genuine data advantage rather than a table-stakes feature.

## Peer Comparison

**56.7% under our 2034 estimate, with a broader product boundary:** Growth Market Reports, updated June 2026, estimates the global hypoglossal-nerve-stimulation-devices market at **$667m in 2025** and **$2.02b in 2034**, a 13.1% CAGR. Our interpolated 2034 manufacturer-revenue estimate is **$4.66b**. Its stated boundary includes external devices and other neurological disorders but excludes phrenic-nerve CSA systems; it is therefore not directly comparable. Its 2025 total is also below Inspire's $912m reported revenue, which indicates a stale or inconsistent base even before scope alignment: https://growthmarketreports.com/report/hypoglossal-nerve-stimulation-devices-market

**64.3% under our 2032 estimate, nominally narrower but internally inconsistent:** Verified Market Research, updated January 2026, puts the global implantable hypoglossal-nerve-stimulator device market at **$624.8m in 2024** and **$1.109b in 2032**, a stated 7.46% CAGR. Our interpolated 2032 value is **$3.11b**. The title says implantable, while the public description repeatedly describes wearable non-invasive devices; it excludes CSA and gives no clean manufacturer-versus-procedure revenue definition, so the arithmetic is only a weak benchmark: https://www.verifiedmarketresearch.com/product/implantable-hypoglossal-nerve-stimulators-device-market/

**80.3% under our 2035 estimate, hypoglossal-only:** Expert Market Research, updated 4 April 2026, estimates the global hypoglossal-nerve-stimulation-therapy market at **$358.72m in 2025** and **$1.124b in 2035**, a 12.1% CAGR. Our interpolated 2035 estimate is **$5.71b**. The source is narrower because it excludes CSA, but its base is less than half Inspire's 2025 revenue and its listed distribution channels and competitive set do not match the implant-device industry, so it cannot be reconciled to reported supplier revenue: https://www.expertmarketresearch.com/reports/hypoglossal-nerve-stimulation-therapy-market

The public peer set disagrees sharply and generally fails a simple leader-revenue check. It therefore does not justify changing the stored bridge: the $7.0b 2036 view rests on annual eligible implant decisions, implant share, net system realization and replacement/accessory revenue rather than a market-research category label.

## Sources

- Inspire Medical Systems, Q2 2026 results and guidance, 3 August 2026; $200.6m Q2 revenue and $835m-$875m full-year outlook: https://www.sec.gov/Archives/edgar/data/1609550/000160955026000045/insp2026-q2pressreleaseex9.htm
- Inspire Medical Systems, Q2 2026 investor presentation, 3 August 2026; more than 140,000 cumulative patients, more than 1,500 implanters, more than $900m 2025 revenue and internal 500,000-patient annual U.S. eligible funnel: https://www.sec.gov/Archives/edgar/data/1609550/000160955026000045/q22026investorpresentati.htm
- Inspire Medical Systems, Q2 2026 Form 10-Q, 3 August 2026; first-half revenue, Inspire V coding uncertainty and product indication: https://www.sec.gov/Archives/edgar/data/1609550/000160955026000047/insp-20260630.htm
- Nyxoah, Q2 and first-half 2026 results, 5 August 2026; EUR14.0m first-half revenue, 180 U.S. accounts, 262 trained surgeons and 427 active prior authorizations: https://www.sec.gov/Archives/edgar/data/1857190/000110465926091104/nyxh-20260630xex99d1.htm
- Nyxoah, first-half 2026 interim report, 5 August 2026; FDA approval, indication, geographic revenue and Genio recurring-patch accounting: https://www.sec.gov/Archives/edgar/data/1857190/000110465926091104/nyxh-20260630xex99d2.htm
- LivaNova, Q2 2026 Form 10-Q, 5 August 2026; FDA PMA for aura6000 on 18 March 2026 and inclusion within neuromodulation: https://www.sec.gov/Archives/edgar/data/1639691/000163969126000090/livn-20260630.htm
- FDA, PMA P130008, Inspire Upper Airway Stimulation system approval record and supplements: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id=P130008
- FDA, PMA P160039, remedē System approval record: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id=P160039
- Benjafield et al., "Estimation of the global prevalence and burden of obstructive sleep apnoea," *Lancet Respiratory Medicine*, 2019; 936 million adults aged 30-69 with OSA and 425 million with moderate-to-severe OSA: https://pubmed.ncbi.nlm.nih.gov/31300334/
- Growth Market Reports, "Hypoglossal Nerve Stimulation Devices Market 2034," updated June 2026; $667m 2025 and $2.02b 2034, with external-device and other-neurological-disorder boundary: https://growthmarketreports.com/report/hypoglossal-nerve-stimulation-devices-market
- Verified Market Research, "Implantable Hypoglossal Nerve Stimulators Device Market," updated January 2026; $624.8m 2024 and $1.109b 2032: https://www.verifiedmarketresearch.com/product/implantable-hypoglossal-nerve-stimulators-device-market/
- Expert Market Research, "Hypoglossal Nerve Stimulation Therapy Market," updated 4 April 2026; $358.72m 2025 and $1.124b 2035: https://www.expertmarketresearch.com/reports/hypoglossal-nerve-stimulation-therapy-market
