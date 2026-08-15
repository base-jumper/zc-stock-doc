---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.0
  maturity-market-value: 42.0
concentration:
  inputs:
    traits:
      network-effects:      {score: 0.01, confidence: 0.95}
      data-scale-advantage: {score: 0.02, confidence: 0.90}
      brand-reputation:     {score: 0.12, confidence: 0.80}
      capital-intensity:    {score: 0.98, confidence: 0.95}
      scale-economies:      {score: 0.85, confidence: 0.90}
      regulatory-barriers:  {score: 0.95, confidence: 0.95}
      switching-costs:      {score: 0.08, confidence: 0.85}
  override:
    s1: 0.11
    r: 0.80
    reason: "The cross-market trait model cannot observe that geological scarcity is dispersed among unrelated deposits and that most qualifying projects are jointly owned. A bottom-up ownership map of the screened cohort supports an approximately 11% largest attributable-revenue share and a broad developer fringe in 2036."
  model-estimate:
    s1: 0.353592
    r: 0.623313
  hhi: 0.033611
  method: selected-direct-ridge
  date: 2026-08-09
players:
  override:
    - name: NGEx Minerals
      ticker: NGEX.TO
      capture: 0.019
      reason: "Los Helados-only expected value: 69.1% ownership multiplied by an approximately 190 ktpa full-rate copper case and a 50% probability-weighted commissioning/ramp factor gives about 66 kt of attributable 2036 copper. At the market's $7.30/lb nominal realization this is about $0.80bn, or 1.9% of the $42bn cohort pool. Lunahuasi receives no credit because it has no Mineral Resource Estimate or economic study."
---

# Global Undeveloped Tier-One Copper Projects

## Market Definition

**Market scope:** worldwide greenfield copper projects that were not producing and had not entered full construction by 1 January 2026, and that had either at least 4 Mt of contained copper in a compliant Mineral Resource or a published technical study supporting at least 100 ktpa of copper production. The fixed cohort includes large standalone or district developments such as Vicuña, Resolution, Cascabel, Los Azules, Los Helados, Taca Taca, El Pachón, NuevaUnión, Galore Creek, Winu, Frieda River and Pebble. It excludes operating-mine expansions, brownfield replacement, projects already in full construction, discoveries without a qualifying resource or study, recycled copper, and projects discovered after the cutoff.

**Revenue boundary:** annual producer-recognized revenue in 2036 attributable to payable contained copper from the fixed cohort at first external sale, assigned to economic owners rather than operators. Concentrate is valued net of treatment and refining charges; integrated cathode is reduced to the same mine-gate basis. Gold, silver, molybdenum, royalties, streams, refining and fabrication are excluded.

The **addressable unit** is the cohort's technically supportable annual copper-production capacity. **Penetration** is a `stock` measure: expected operating and ramped capacity in 2036 divided by that capacity if every qualifying project were developed. The **billable unit** is one metric tonne of payable contained copper produced during 2036. Projects are segmented by development maturity and jurisdictional/permitting risk, then probability-weighted and aggregated. Values are nominal USD in 2026 and 2036 at approximately constant current foreign-exchange rates.

## Current View

The cohort's 2026 market value is **zero** by contract: qualifying assets are pre-production and producer revenue begins only after commissioning. This is a vintage-project revenue pool, not the existing mined-copper market and not the in-situ value of resources.

The qualifying inventory is large but economically heterogeneous. Vicuña combines Filo del Sol and Josemaria under a 50/50 BHP-Lundin vehicle; Resolution could supply up to one-quarter of U.S. copper demand; Cascabel's 2024 PFS supports average production of 123 ktpa copper; and Los Helados contains 2.08 Bt of Indicated material at 0.40% copper plus 1.08 Bt Inferred at 0.34%. Resource tonnes establish scale, not expected production: sanction, financing, permits, infrastructure and ramp are modeled explicitly through project-level probability weights.

## Adoption Path

The expected 2036 pool is **$42bn**, with a plausible **$24bn-$65bn** range. The reference case is 2.6 Mt of payable copper at **$7.30/lb** ($16,100/t), matching the long-run nominal mine-gate realization used for the broader copper market. It represents roughly 10% of the 25.6 Mt 2036 primary requirement estimated in that market doc, a demanding but physically plausible contribution from the world's largest undeveloped assets.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Qualifying cohort full-rate capacity | n/a | ~5.5 Mtpa | Published studies plus normalized conceptual capacity for resource-only projects |
| Operating/ramped share | 0% | ~47% | Project-specific sanction, permit, construction and ramp probabilities |
| Billable copper | 0 Mt | **2.6 Mt** | Probability-weighted production; no by-product equivalent tonnes |
| Mine-gate realization | n/a | **$7.30/lb** | Nominal incentive-price anchor, net of concentrate deductions |
| Annual market value | **$0bn** | **$42bn** | Rounded expected values |

No logistic penetration block is configured. A fixed cohort of large mining projects advances through lumpy binary approvals and multi-year construction, not repeatable unit adoption; a project-level probability-weighted capacity bridge is the more coherent model. The largest sensitivities are permitting and social licence, sponsor capital allocation, initial capex, power and water infrastructure, construction duration, metallurgy and the 2036 copper price.

## Market Structure

Network effects, data advantages, brand and customer switching costs are negligible. Capital, processing scale, orebody scarcity and permitting barriers are extreme, but they do not create one winner: geological endowment is geographically dispersed and joint ventures split several of the largest projects. The direct trait model therefore overstates company concentration for this fixed cohort.

The canonical override uses an **11% leader share** and **0.80 rank decay**, producing an **HHI of about 0.034** or roughly 30 effective owners. The geometric curve assigns about 55% to ranked owners and leaves the rest to a broad fringe. This is consistent with a cohort containing diversified majors, state-linked sponsors, mid-cap developers and multiple 50/50 or minority-owned projects; it is materially more concentrated than total mined copper but not winner-take-most.

## Players

No mobility calculation is used because there is no defensible 2026 revenue ranking: the cohort is pre-revenue, and ranking companies by in-situ resource would change the contract's share basis. NGEx is therefore an explained outside-contender override.

NGEx's canonical **1.9% capture** implies **$0.798bn of attributable 2036 copper revenue**. The cross-check gives credit only to Los Helados: 69.1% ownership, approximately 190 ktpa full-rate copper potential and a 50% probability-weighted commissioning/ramp factor imply about 66 kt attributable output. At $7.30/lb that is about $0.80bn. The 190 ktpa case is an analyst normalization for a Tier-One-scale block cave, not company guidance; Los Helados has no economic study. Lunahuasi receives zero canonical revenue because NGEx states that future drilling must still convert its exploration potential to a Mineral Resource Estimate.

The override is deliberately conservative on geological upside and explicit about schedule risk. It will be wrong if Los Helados is developed through a smaller Caserones feed scenario, if NGEx's ownership changes, or if Lunahuasi reaches a compliant resource and economic study quickly enough to support 2036 production.

## Watch

- Los Helados scoping or economic studies, especially throughput, recovery, capex, development route and Caserones synergies.
- A Lunahuasi Mineral Resource Estimate and first economic study; add it only when production scale and timing can be probability-weighted without inventing an orebody.
- Vicuña integrated technical studies and sanctions, which are the strongest read-through for high-Andes permitting, infrastructure and capital intensity.
- Project sanctions, permits and ownership changes across Resolution, Cascabel, Los Azules, Taca Taca, El Pachón, NuevaUnión, Galore Creek, Winu, Frieda River and Pebble.
- 2036 mine-gate copper realization and evidence that the broader primary-supply requirement remains near 25-26 Mt.

## Peer Comparison

- **Approximately aligned on physical scale:** the IEA's 2025 outlook implies about 25.6 Mt of primary copper requirement in 2036. This cohort's 2.6 Mt expected output is about 10% of that requirement. The IEA does not publish this fixed-vintage cohort, so this is a system-capacity check rather than a boundary-matched forecast.
- **Project-level anchors, not market forecasts:** Cascabel's published 123 ktpa average copper production and Resolution's potential to supply up to one-quarter of U.S. demand show that individual Tier-One projects can add 0.1-0.5 Mtpa. Applying those figures without schedule probabilities would materially overstate the 2036 pool.
- No public forecast was found for annual 2036 first-sale copper revenue from this exact fixed 2026 undeveloped-project cohort. Commercial copper-development reports generally mix operating expansions, projects already under construction and undiscovered future supply, so their totals are not comparable.

## Sources

- NGEx Minerals, "NGEx Welcomes Lundin Mining as New Partner at Los Helados," 11 March 2026; ownership, resource and proximity to Caserones: https://ngexminerals.com/news/ngex-welcomes-lundin-mining-as-new-partner-at-los-122805/
- NGEx Minerals, "NGEx Reports Q2 2026 Results," 6 August 2026; latest Lunahuasi status and explicit need to convert exploration potential to a Mineral Resource Estimate: https://ngexminerals.com/news/ngex-reports-q2-2026-results-phase-4-drilling-del-122817/
- Lundin Mining, Vicuña District project page; 50/50 BHP ownership and integrated Filo del Sol-Josemaria development: https://www.lundinmining.com/our-portfolio/projects/vicuna-district/
- SolGold, Cascabel Project 2024 PFS; average 123 ktpa copper, 277 kozpa gold and 794 kozpa silver over the initial 28-year mine plan: https://solgold.com/projects/ecuador/cascabel-project/
- Rio Tinto, Resolution Copper project page; proposed block cave and potential to supply up to one-quarter of U.S. copper demand: https://www.riotinto.com/en/operations/us/resolution
- International Energy Agency, *Global Critical Minerals Outlook 2025*, copper outlook and long project lead-time evidence: https://www.iea.org/reports/global-critical-minerals-outlook-2025
- U.S. Geological Survey, *Mineral Commodity Summaries 2026: Copper*, current mine-supply and price context: https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf
