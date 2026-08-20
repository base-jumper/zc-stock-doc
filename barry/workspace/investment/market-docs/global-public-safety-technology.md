---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 40.0
  maturity-market-value: 115.0
concentration:
  inputs:
    traits:
      network-effects:       {score: 0.30, confidence: 0.55}
      data-scale-advantage:  {score: 0.55, confidence: 0.50}
      brand-reputation:      {score: 0.60, confidence: 0.65}
      capital-intensity:     {score: 0.45, confidence: 0.60}
      scale-economies:       {score: 0.65, confidence: 0.60}
      regulatory-barriers:   {score: 0.35, confidence: 0.50}
      switching-costs:       {score: 0.85, confidence: 0.70}
  model-estimate:
    s1: 0.186483
    r: 0.818398
  override:
    s1: 0.35
    r: 0.65
    reason: "The pooled direct-ridge model maps this high-switching-cost, moderate-network market to an s1 of ~0.19 with a slow-decay tail (r~0.82) and a modeled mass above 1, which understates the durable, procurement-locked installed bases of Motorola Solutions (mission-critical radio) and Axon (bundled evidence/AI subscriptions), and overstates the fragmenting tail. Long sole-source agency contracts, evidence data gravity, and LMR standards lock-in protect the top two; an ~35% leader with a 0.65 rank-decay (HHI ~0.21, ~5 effective competitors) better matches the observed 2026 structure and a defensible 2036 outcome."
  hhi: 0.212121
  method: selected-direct-ridge
  date: 2026-08-20
players:
  inputs:
    current:
      - rank: 1
        name: Motorola Solutions
        ticker: MSI
        share: 0.30
      - rank: 2
        name: Axon Enterprise
        ticker: AXON
        share: 0.08
      - rank: 3
        name: Thales
        ticker: HO.PA
        share: 0.06
      - rank: 4
        name: Hytera Communications
        ticker: 002583.SZ
        share: 0.04
      - rank: 5
        name: Getac
        ticker: 3005.TW
        share: 0.03
  model-estimate:
    - rank: 1
      name: Motorola Solutions
      ticker: MSI
      hold-position-capture: 0.35
      mobility-adjusted-capture: 0.275913
      mobility-adjusted-revenue: 31.729995
    - rank: 2
      name: Axon Enterprise
      ticker: AXON
      hold-position-capture: 0.2275
      mobility-adjusted-capture: 0.177355
      mobility-adjusted-revenue: 20.395825
    - rank: 3
      name: Thales
      ticker: HO.PA
      hold-position-capture: 0.147875
      mobility-adjusted-capture: 0.127849
      mobility-adjusted-revenue: 14.702635
    - rank: 4
      name: Hytera Communications
      ticker: 002583.SZ
      hold-position-capture: 0.096119
      mobility-adjusted-capture: 0.089252
      mobility-adjusted-revenue: 10.26398
    - rank: 5
      name: Getac
      ticker: 3005.TW
      hold-position-capture: 0.062477
      mobility-adjusted-capture: 0.066933
      mobility-adjusted-revenue: 7.697295
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-20
---
# Global Public Safety Technology

## Market Definition

**Market scope.** Global public-safety technology: hardware, software, and services sold to law-enforcement agencies, public-safety agencies, corrections, federal/national-security agencies, and enterprise security buyers. Includes conducted-energy (TASER) devices, body-worn/in-car/fixed cameras, digital evidence and records-management software, real-time operations and 911 call-handling platforms, drone-as-first-responder (DFR) and counter-drone systems, land-mobile-radio (LMR) networks and devices, and AI-driven public-safety products. Excludes pure defense weapons platforms (tanks, fighter aircraft), private consumer security cameras, and physical security guards/services.

**Revenue boundary.** Market value is **vendor recognized revenue** (what Axon, Motorola Solutions, Thales, Hytera, etc. actually book), from hardware devices plus recurring software/cloud/warranty/services revenue. It excludes agency budgets, GMV, and integrator/installer markup.

**Addressable unit and penetration.** The stable denominator is public-safety and enterprise agencies/institutions deploying connected devices and software. Because the market spans heterogeneous hardware and software, we size from **top-down spend** under a defensible market-value approach rather than forcing a single unit-denominator penetration curve.

**Time and value basis.** Base year 2026, fixed 10-year horizon 2036, USD, **nominal** dollars (general inflation included; normal when feeding future company revenue estimates).

## Current View

The expected 2026 market value is **$40B** (plausible range $35–50B).

**Bottom-up anchor.** Motorola Solutions reported 2025 revenue of **$11.68B** (8.0% growth), ~all in scope (public-safety LMR + video + command-center, plus enterprise security); Axon reported 2025 revenue of **$2.78B** (+33%) and runs at ~$3.2B TTM by Q2 2026, also in scope. Top-two combined ≈ **$15.0B**. Applying their combined current share (~38%, consistent with the top-2 shares below) gives a total vendor-revenue market of roughly **$40B**.

**Consistency checks.**
- The *public-safety & security* market (MarketsandMarkets, broad: critical comms, biometrics, surveillance, emergency/disaster, cybersecurity) is put at **$575B (2025) → $982B (2030)**. That far exceeds our technology-only vendor-revenue boundary (it includes physical security, cybersecurity, and defense-facing spend) and is used as a sanity ceiling, not a benchmark.
- The *law enforcement software* market (CAD, case/incident/records, digital evidence, jail management) is forecast at **~$33B by 2030**. Our 2030 whole-market projection (interpolating ~11% CAGR) is ~$61B, above this software-only figure once hardware, drones, and real-time ops are added. Consistent lower band.
- Published segment totals used as building blocks: digital evidence management **~$9–10B in 2025** (Grand View, Mordor, Precedence); body-worn cameras **~$1.3–2.2B in 2025** (Business Research Insights $2.24B 2026; Data Bridge $1.29B 2024) though enterprise-inclusive estimates run to $8.5B; counter-drone **$2.7–4.5B in 2025** (MarketsandMarkets $4.48B; Arizton $2.7B); TETRA/LMR global **$5–7B in 2024** (MarketsandMarkets range 5–7).

**10-year 2036 reference case: $115B** (≈11.0% annualized from $40B). Drivers: software/services revenue growing ~15% annualized as cloud, AI, and digital-evidence attach scale; hardware (radios, cameras, CEDs, drones) growing ~8–9% annualized; drones/DFR, counter-drone, AI reporting, and enterprise security adding the delta. A plausible range is **$85–150B**. The main downside is agency budget stagnation and AI/our-era regulatory friction; the upside is fast DFR and generative-AI module adoption.

## Adoption Path

We do **not** run a formal logistic penetration sub-skill here. The market contract deliberately sizes from spend and value rather than a single addressable-unit penetration curve: the addressable base spans officers, radios, cameras, agencies, and enterprises with very different unit economics, so a one-logistic model would be a misleading abstraction. In its place we describe the adoption state of the main device categories.

**Adoption state per category:**
- **Conducted-energy devices (CED):** Axon reports US state-and-local penetration of its TASER bundle at just under 15% of the officer opportunity (Q2 2026 slides), with TASER 10 + AI upgrades driving the step-change. Global adoption is much earlier.
- **Body-worn cameras (BWC):** US law-enforcement agency adoption moved from ~one-third in 2014 to a strong majority by 2025; replacement + software/evidence attach now dominates unit growth. Europe, UK, ANZ follow; large emerging markets are early.
- **Evidence/records software:** migration from legacy on-prem to cloud is mid-S-curve; Axon reports ~95%+ of customer revenue on subscription plans and evidence cloud is the industry anchor.
- **Drones / DFR and counter-drone:** near-zero base; Axon (Q2 2026) sizes drones/robotics at ~$20B of its own $159B TAM, counter-drone at $14.5B by 2030 (MarketsandMarkets) — the fastest-growing line.

**How the market-value bridge derives the 2036 number:** apply ~11% aggregate CAGR but with mix shift: software/cloud/services grow 15%-ish and climb from ~30% of market value to ~45%–50% by 2036, while devices/radios/cameras grow at mid-single-to-high-single digits. A compact bridge:

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Devices & hardware (radios, cameras, CED, drones) | ~$27B | ~$58B | ~8% CAGR; replacements + DFR growth |
| Software/cloud/services (evidence, records, 911, AI attach) | ~$13B | ~$57B | ~16% CAGR; share of market value 33% → ~50% |
| **Annual market value** | **$40B** | **$115B** | Reconciles to front matter |

Most sensitive variables: DFR/counter-drone ramp, AI-module pricing (e.g. Axon's $569 OSP + AI Era Plan), enterprise take-rate, and agency budget cycles.

## Market Structure

The 2036 market is projected to remain **moderately concentrated with a strong semi-duopoly at the top**: Motorola Solutions (LMR + video + command-center) and Axon (cloud evidence/records + sensors + AI) each hold durable, procurement-locked franchise positions. Long agency contract cycles, LMR radio standards, and data/evidence gravity create high switching costs; the middle tail (Thales, Hytera, Getac, camera-video vendors such as Axis/Avigilon(via MSI)/Verint/Genetec, and CAD vendors) stays fragmented.

The canonical 2036 concentration is the **analyst override**: **s1 = 0.35** leader share, **r = 0.65** rank-decay → **whole-market HHI = 0.2121** (~5 effective competitors; "concentrated" in the market-docs reading table). The pooled trait model's raw estimate (s1≈0.19, r≈0.82, HHI≈0.11) is directionally right but underestimates concentration on mechanism grounds: agency procurements, sole-source bundles, radio-standard lock-in, and evidence data gravity compound beyond what the corpus's median markets imply, and its parameter pair gives modeled mass >1 (invalid for whole-market rank assignment). The override's mass is exactly 1.0 (s1/(1−r)=1), so the geometric tail sums cleanly over the whole market.

The override's implied 2036 top shares: Motorola 35%, Axon 22.75%, Thales 14.79%, Hytera 9.61%, Getac 6.25%, heavy fringe remainder, with more than 25% of value in ranks 6+.

## Players

Current whole-market revenue shares (2026, analyst estimates on the defined boundary; not audited):

| Rank | Player | Ticker | Current share | Basis |
|---|---|---:|---|---:|
| 1 | Motorola Solutions | MSI | 30% | 2025 rev $11.7B; in-scope ≈ $11–12B |
| 2 | Axon Enterprise | AXON | 8% | TTM rev ~$3.2B; strong momentum |
| 3 | Thales | HO.PA | 6% | secure comms/PS electronics, ex-defense core |
| 4 | Hytera Communications | 002583.SZ | 4% | global LMR, China-heavy |
| 5 | Getac | 3005.TW | 3% | rugged field computing for LE/defense |

These shares are analyst estimates derived from reported revenue and credible vendor lists; the top two are well-supported, ranks 3–5 lower confidence.

**Mobility model.** On the canonical curve, holding today's ranks gives Motorola 35%, Axon 22.75%, Thales 14.8%, Hytera 9.6%, Getac 6.2%. The pooled rank-mobility model adjusts for the distribution of 10-year transitions, giving slightly lower adjusted capture per rank (churn-base) — see `players.model-estimate` for the exact stored values. Both views are included; canonical capture is the mobility-adjusted model estimate (no per-player override is stored).

The mobility model is a coarse pooled base rate: it sees current rank and share spacing but not momentum, moats, management, or outside entrants. For a company like Axon growing 30%+ while the model's churn is calibrated on slower ecosystems, the model can understate the upside; treat the adjusted revenue as a conservative base-rate input. Axon's stored mobility-adjusted revenue is positive and large (~$20.4B at 2036 in the model view, 17.7% capture of the $115B market) and is the authoritative terminal-revenue input for the stock-doc TAM-capture valuation.

## Watch

- Evidence-cloud and AI attach rates (Axon Draft One/redaction, MSI AI software, per-seat premiums).
- DFR / drone-as-first-responder and counter-drone regulatory and funding: permit frameworks, FAA, state laws — the biggest upside swing.
- Enterprise-security expansion by Axon and Motorola (frontline-worker and facility security).
- AI-in-policing acceptance and privacy regulation (generative AI for intake, redaction, predictive tools).
- Agency budget cycles and federal/state tech grants (COPS, state & local).
- LMR → broadband cellular transition (PTT-over-4G/5G, FirstNet) and the refresh cycle of U.S., U.K., EMEA projects.
- Competitive response: Axon vs Motorola in video + command-center + BWC; video vendors (Axis, AV), CAD vendors, drone entrants (Skydio, DJI-MATRICE).
- China export/competition policy for LMR/video vendors outside China.

## Peer Comparison

Peer figures are benchmarks only; they do not change the stored inputs in this run.

- **~16x over our estimate (not comparable):** MarketsandMarkets, "Public Safety & Security Market" (Oct 2025: $575B 2025 → $982B 2030, 11.3% CAGR). At 2026 their path implies ~$640B vs our $40B. Their scope adds cybersecurity, physical security, biometrics, disaster management, and defense systems; boundary-mismatched, used as a ceiling only.
- **~46% under our interpolated 2030 (software-only, not comparable):** MarketsandMarkets, "Law Enforcement Software Market" — $32.96B by 2030. Our 2030 whole-market (interpolating 11% CAGR from $40B) is ~$61B, so their software-only line is ~46% under and is inside our scope; consistent with our hardware+software boundary, not a disagreement.
- **~0.24× of our interpolated 2030 market (segment, not comparable as a total):** MarketsandMarkets, "Counter-UAS/Anti-Drone Market" — $4.48B 2025 → $14.51B 2030, 26.5% CAGR. This fast-growing segment is embedded in our hardware line; if it keeps ~20%+ growth to 2036 it approaches ~$28–35B, which we allow for in the drones/DFR/counter-drone portion of the ~$58B 2036 devices line.
- **Axon's own TAM (Q2 2026 slides: $159B; 2025: $129B; 2024: $77B; 2023: ~$50B)** — an *internal full-adoption TAM over all addressable workers/use-cases*, structurally larger than expected market value and not a like-for-like benchmark; our $115B 2036 market value sits between their TAM and their penetrated current revenue, consistent with a capture-based terminal.

No published source uses our exact vendor-recognized revenue boundary over a fixed 10-year horizon; the credible whole-market numbers bracket our view.

## Sources

- Motorola Solutions FY2025 earnings release and 10-K (Feb 2026): FY2025 revenue $11.68B, FY2024 $10.82B, record backlog ~$14.7B, record FCF $2.1B: https://www.motorolasolutions.com/content/dam/msi/investors/doc_financials/2025/q4/msi_2025_10-k.pdf
- Axon Q2 2026 investor slides via Investing.com (Aug 5 2026): $159B TAM (law-enforcement ≈50% of TAM; US state & local <15% penetration of a ~$15B opportunity; vehicle intelligence ~$30B; real-time ops ~$25B; drones/robotics ~$20B; Axon 2028 target ~$6B revenue): https://www.investing.com/news/company-news/axon-q2-2026-slides-159b-tam-powers-35-growth-despite-stock-drop-93CH-4839816
- Axon 2024 earnings call / 2025 report (Feb 2025): FY2024 revenue $2.08B (+33%), TAM $129B; Axon Q2 2026 TTM revenue $3.22B (+34.6%) via stockanalysis.com/AXON revenue (Fiscal.ai): https://stockanalysis.com/stocks/axon/revenue/
- Motorola Solutions revenue history & TTM (Q2 2026 quarter ended Jul 4 2026 revenue $3.13B; TTM $12.24B) via stockanalysis.com/MSI revenue (Fiscal.ai): https://stockanalysis.com/stocks/msi/revenue/
- MarketsandMarkets, "Public Safety & Security Market" (Oct 2025: $575.05B 2025 → $981.84B 2030, 11.3% CAGR); "Law Enforcement Software Market" ($32.96B by 2030); "Anti-Drone Market" (Jun 2026: $4.48B 2025 → $14.51B 2030, 26.5% CAGR): https://www.marketsandmarkets.com/PressReleases/counter-cuas-systems.asp
- Body-worn camera market: Business Research Insights ($2.24B 2026 → $8.19B 2035, 15.49%); Data Bridge ($1.29B 2024 → $5.47B 2032); Custom Market Insights ($8.5B 2025, broad enterprise-inclusive); Research Nester ($2.12B 2025 → $8.21B 2035).
- Digital evidence management: Grand View Research ($9.08B 2025 → CAGR ~12%); Mordor Intelligence ($9.65B 2025 → $16.10B 2030); Precedence Research ($8.75B 2025 → $21.98B 2035).
- Counter-UAS: MarketsandMarkets ($4.48B 2025 → $14.51B 2030); IMARC ($2.45B 2025 → $15.62B 2034); Arizton ($2.70B 2024 → $11.12B 2030).
- TETRA/LMR global market: MarketsandMarkets, "Terrestrial Trunked Radio (TETRA) Market" (Sep 2026: ~$5–7B 2024 → $11–14B 2036, 6–8% CAGR).
- Axon internal TAM history: Morgan Stanley (Dec 2024: ~$77B), Axon slides (2023 ~$50B, 2025 $129B, Aug 2026 $159B); Axon 2024 earnings release (TAM includes international governments and enterprises).
- EFF, "Beware the Bundle", Apr/May 2025, on single-source bundling and procurement dynamics in public-safety tech: https://www.eff.org/deeplinks/2025/04/beware-bundle-companies-are-banking-becoming-your-police-departments-favorite

---

*Analyst hand-off note: for the AXON stock-doc TAM-capture valuation, use the `players.model-estimate` row for ticker **AXON** → `mobility-adjusted-revenue` (≈$20.4B, 17.7% of the 2036 market) as terminal annual revenue. Do not apply the gone probability again; it is already embedded in the model rows.*