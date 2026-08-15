---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 35.0
  maturity-market-value: 160.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.05, confidence: 0.95}
      data-scale-advantage: {score: 0.35, confidence: 0.70}
      brand-reputation: {score: 0.75, confidence: 0.85}
      capital-intensity: {score: 0.80, confidence: 0.85}
      scale-economies: {score: 0.85, confidence: 0.85}
      regulatory-barriers: {score: 0.85, confidence: 0.90}
      switching-costs: {score: 0.25, confidence: 0.75}
  model-estimate:
    s1: 0.322487
    r: 0.661045
  hhi: 0.184715
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: Eli Lilly
        ticker: LLY
        share: 0.57
      - rank: 2
        name: Novo Nordisk
        ticker: NVO
        share: 0.415
  override:
    - name: Viking Therapeutics
      ticker: VKTX
      capture: 0.03
      reason: "Probability-weighted outside-contender estimate: wholly owned injectable VK2735 is in fully enrolled Phase 3 trials and its oral formulation is preparing for Phase 3, but approval, launch financing, manufacturing and commercial execution remain material risks."
  model-estimate:
    - rank: 1
      name: Eli Lilly
      ticker: LLY
      hold-position-capture: 0.322487
      mobility-adjusted-capture: 0.231697
      mobility-adjusted-revenue: 37.07152
    - rank: 2
      name: Novo Nordisk
      ticker: NVO
      hold-position-capture: 0.213178
      mobility-adjusted-capture: 0.171505
      mobility-adjusted-revenue: 27.4408
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---
# Global Obesity Pharmacotherapy

## Market Definition

**Market scope:** worldwide prescription medicines approved for chronic weight management in adults with obesity, or overweight with a labelled weight-related comorbidity. Injectable and oral incretins, amylin agents and older branded or generic anti-obesity drugs are included. Diabetes-labelled sales, off-label use that manufacturers report as diabetes revenue, compounded copies, paediatric-only use, bariatric procedures, devices, lifestyle programmes and telehealth-platform revenue are excluded.

**Revenue boundary:** annual net revenue recognized by the medicine manufacturer for included obesity-labelled products, not list-price spend, pharmacy or distributor markup, insurer expenditure or total treatment cost. The **addressable unit** is an adult meeting an included label's BMI and comorbidity criteria. **Penetration** is the `stock` share of that addressable adult base receiving an included medicine during the year. **Billable units** are treated patient-years, aggregated across U.S. and ex-U.S. segments because realized price and access differ materially. The base year is 2026, the fixed horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

## Current View

Expected 2026 manufacturer revenue is **$35b**, with a rough **$32b-$39b** range. Lilly reported **$9.09b** of first-half Zepbound revenue and $4.93b in Q2; continued volume growth supports about **$20b** for 2026. Novo reported **DKK44.06b** of adjusted first-half obesity-care sales; approximately DKK93b for the year converts to about **$14.5b** at DKK6.4 per USD. Older drugs and smaller suppliers contribute roughly $0.5b. The result implies current whole-market shares of about **57.0% Lilly, 41.5% Novo and 1.5% others**.

WHO counted 890 million adults with obesity in 2022, before adding overweight adults with labelled comorbidities. J.P. Morgan estimates roughly 2% of the global population with obesity currently uses GLP-1 treatment. An estimated 16 million obesity-drug patient-years at about $2,200 of blended manufacturer revenue reconciles to the $35b top-down total; uncertainty is concentrated in persistence, U.S. gross-to-net realization and unreported older-drug revenue.

## Adoption Path

Expected 2036 market value is **$160b**, with a broad **$90b-$260b** range. The reference bridge raises the structurally eligible adult base from about 1.3 billion to 1.8 billion and active treatment from about 16 million to 155 million patient-years. That is only **8.6%** penetration at the horizon, but nearly ten times current treated volume. Oral medicines, broader reimbursement, greater supply and chronic-care recognition drive volume; competition, international mix and generic entry reduce blended net manufacturer revenue to about **$1,030 per patient-year** despite general inflation.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Label-eligible adults | ~1.3b | ~1.8b | Obesity plus overweight with a qualifying comorbidity |
| Active treatment share | ~1.2% | ~8.6% | Patient-years divided by eligible adults |
| Treated patient-years | ~16m | ~155m | U.S. and ex-U.S. combined |
| Net manufacturer revenue per patient-year | ~$2,200 | ~$1,030 | Lower-priced oral, international and generic mix |
| Annual market value | **$35b** | **$160b** | Rounded manufacturer revenue |

The implied ten-year CAGR is **16.4%**. A segment check gives roughly 30 million U.S. patient-years at $2,300 and 125 million ex-U.S. patient-years at $730 in 2036. Those assumptions align directionally with Morgan Stanley's 9% U.S.-population usage scenario and Goldman's 8% ex-U.S. peak-penetration assumption. No logistic block is configured: public sources provide point estimates and company patient counts, not a consistent annual global series on the contract denominator. The largest sensitivities are persistence, coverage, net price, manufacturing capacity and the efficacy/tolerability of oral and next-generation drugs.

## Market Structure

Direct network effects are absent. Clinical and post-market data improve prescriber confidence, but scale does not make the molecule itself compoundingly better; data advantage is therefore moderate. Brand and reputation matter strongly because chronic prescribing depends on safety, outcomes, payer confidence and physician familiarity.

Capital, scale and regulatory barriers are high. Entrants must fund large outcome trials, regulatory submissions, pharmacovigilance, peptide or small-molecule manufacturing, global supply and payer contracting. Lilly's additional $4.5b Indiana manufacturing commitment illustrates the entry ticket, while sustained volume lowers manufacturing and commercial cost. Patents and approvals delay entry, but multiple Phase 3 assets and eventual generics prevent a legal cap on competitors. Switching costs are modest: titration and tolerability create friction, yet patients and payers can change therapy without migrating data or equipment.

The structural model yields a **32.25%** horizon leader share, **66.10%** rank decay and **0.1847 HHI**, equivalent to about **5.4 equal competitors**. This is a concentrated but contestable market: two scaled incumbents remain important, while oral therapies, retatrutide, amylin combinations, VK2735 and later generics support several meaningful challengers. The curve's modeled mass is about 95%, and `s1` remains below `1-r`, so a competitive fringe is valid. No concentration override is used; U.S. cloud infrastructure is a useful HHI-shape anchor, though its mechanism differs.

## Players

The current ranking uses expected 2026 obesity-labelled manufacturer revenue: Lilly 57.0% and Novo 41.5%. It excludes Mounjaro and Ozempic diabetes revenue even when used off-label. The mobility model applies a pooled ten-year rank-transition base rate to those two incumbents and already includes exit or absorption risk.

| Player | Hold-position capture | Mobility model | Canonical capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: | ---: |
| Eli Lilly (LLY) | 32.25% | 23.17% | **23.17%** | **$37.07b** |
| Novo Nordisk (NVO) | 21.32% | 17.15% | **17.15%** | **$27.44b** |
| Viking Therapeutics (VKTX) | n/a | n/a | **3.00%** | **$4.80b** |

Lilly's tirzepatide scale, retatrutide programme, manufacturing spend and payer access support leadership; it can lose capture through price erosion, safety, supply or better-tolerated rivals. Novo has deep obesity expertise, Wegovy's injectable and oral franchise, global reach and large-scale manufacturing, but recent U.S. price/share pressure shows that incumbency is not permanent.

Viking is an outside-contender override because rank mobility cannot value a pre-revenue entrant. Its **3.0% canonical capture** is probability-weighted: injectable VK2735's VANQUISH 1 and 2 Phase 3 trials are fully enrolled, oral VK2735 is expected to enter Phase 3 in Q4 2026, and Phase 2 data showed competitive efficacy. The discount reflects binary approval risk, a $502m cash position against late-stage and launch requirements, no commercial infrastructure and uncertain manufacturing. Positive terminal revenue is therefore explicit without assuming Viking reaches the model's 14.1% third-rank structural share.

## Watch

- VK2735 VANQUISH efficacy, tolerability, discontinuation, cardiovascular safety, filing timing and manufacturing or partnership strategy; oral Phase 3 initiation and maintenance-dosing data.
- U.S. Medicare, Medicaid and employer coverage; realized prices under manufacturer-direct and negotiated channels.
- Persistence beyond one year and whether maintenance dosing or oral switching reduces discontinuation.
- Lilly retatrutide and oral Foundayo, Novo oral Wegovy and next-generation combinations, and credible amylin or muscle-preserving entrants.
- Peptide and small-molecule capacity, cold-chain relaxation, and generic entry in China, India, Brazil, Canada and Turkey.
- Boundary discipline: separate obesity-labelled revenue from diabetes sales and compounded or channel revenue.

## Peer Comparison

**14.6% over our 2035 estimate:** Goldman Sachs Research, 22 May 2025, forecasts the global anti-obesity medication market at **$120b in 2035**, after lowering its 2030 view to $95b. Our interpolated 2035 value is **$137.5b**. Goldman's manufacturer-sales boundary appears close; its 7% annual price erosion, $70b U.S. and $50b ex-U.S. peak split explains most of the difference.

**24.8% under our 2030 estimate:** Morgan Stanley Research, 7 May 2024, forecasts **$105b in 2030**, with a $144b high case, versus our interpolated **$78.9b**. Its branded-obesity-drug boundary is close, but the forecast predates the sharp price erosion and lower cash-pay prices visible by 2026.

**Not comparable:** J.P. Morgan Global Research, 27 February 2026, forecasts a **$200b global incretin market in 2030** and 30 million U.S. GLP-1 users. The revenue figure includes diabetes and other incretin indications, so comparing it arithmetically with obesity-only manufacturer revenue would overstate the peer difference. Its current 2% global obesity penetration and oral/generic access thesis support the volume path.

Peer evidence spans $95b-$144b around 2030-35 on close boundaries and $200b for the broader incretin category. It benchmarks, but does not replace, the patient-year and net-price bridge.

## Sources

- WHO, *Obesity and overweight*, updated 8 December 2025; 890 million adults with obesity and 2.5 billion adults overweight in 2022, plus obesity's chronic-disease framing: https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight
- WHO, 1 December 2025, global guideline on GLP-1 medicines for adults with obesity: https://www.who.int/news/item/01-12-2025-who-issues-global-guideline-on-the-use-of-glp-1-medicines-in-treating-obesity
- Eli Lilly, Q2 2026 results, 5 August 2026; Zepbound revenue of $4.928b in Q2 and $9.088b in H1, 2026 company guidance and manufacturing investment: https://www.sec.gov/Archives/edgar/data/59478/000005947826000077/q226lillysalesandearningsp.htm
- Novo Nordisk, H1/Q2 2026 financial report, 4 August 2026; adjusted obesity-care sales of DKK23.152b in Q2 and DKK44.064b in H1, 4.9 million obesity patients and pricing/access commentary: https://www.sec.gov/Archives/edgar/data/353278/000035327826000023/caq22026.htm
- Novo Nordisk, Annual Report 2025; obesity-care sales of DKK82.3b and 59.6% global branded obesity-volume share: https://annualreport.novonordisk.com/2025/strategic-aspirations/financial-performance.html
- Viking Therapeutics, Q2 2026 results, 29 July 2026; fully enrolled VANQUISH trials, oral Phase 3 timing, prior efficacy and $502m cash: https://www.sec.gov/Archives/edgar/data/1607678/000119312526323652/vktx-ex99_1.htm
- Goldman Sachs Research, *The anti-obesity drug market may prove smaller than expected*, 22 May 2025; $95b in 2030, $120b in 2035, 7% annual price erosion and regional assumptions: https://www.goldmansachs.com/insights/articles/the-anti-obesity-drug-market-may-prove-smaller-than-expected
- Morgan Stanley Research, *Scaling Up the Impact of Obesity Drugs*, 7 May 2024; $105b 2030 base case, $144b high case and U.S. adoption scenario: https://www.morganstanley.com/ideas/obesity-drugs-market-expanded-opportunity
- J.P. Morgan Global Research, *How demand for (and supply of) weight loss drugs is playing out in 2026*, 27 February 2026; $200b 2030 global incretin forecast, global penetration and U.S. users: https://www.jpmorgan.com/insights/global-research/current-events/obesity-drugs
