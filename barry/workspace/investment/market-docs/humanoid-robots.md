---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 2.5
  maturity-market-value: 50.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.45, confidence: 0.40}
      data-scale-advantage: {score: 0.60, confidence: 0.50}
      brand-reputation: {score: 0.35, confidence: 0.35}
      capital-intensity: {score: 0.65, confidence: 0.65}
      scale-economies: {score: 0.75, confidence: 0.65}
      regulatory-barriers: {score: 0.40, confidence: 0.40}
      switching-costs: {score: 0.35, confidence: 0.35}
  override:
    s1: 0.30
    r: 0.65
    reason: "The pooled trait model overstates durable winner-take-most effects for a geographically fragmented hardware market with heterogeneous applications, modular supply chains, and limited customer switching costs; a 30% leader and competitive tail better match the expected 2036 structure."
  hhi: 0.155844
  model-estimate:
    s1: 0.536732
    r: 0.486292
  method: selected-direct-ridge
  date: 2026-08-02
players:
  inputs:
    current:
      - rank: 1
        name: AgiBot
        share: 0.30
      - rank: 2
        name: Unitree Robotics
        share: 0.22
      - rank: 3
        name: UBTECH Robotics
        ticker: 9880.HK
        share: 0.14
      - rank: 4
        name: Leju Robotics
        share: 0.04
      - rank: 5
        name: EngineAI
        share: 0.03
  model-estimate:
    - rank: 1
      name: AgiBot
      hold-position-capture: 0.3
      mobility-adjusted-capture: 0.213828
      mobility-adjusted-revenue: 10.6914
    - rank: 2
      name: Unitree Robotics
      hold-position-capture: 0.195
      mobility-adjusted-capture: 0.156543
      mobility-adjusted-revenue: 7.82715
    - rank: 3
      name: UBTECH Robotics
      ticker: 9880.HK
      hold-position-capture: 0.12675
      mobility-adjusted-capture: 0.115078
      mobility-adjusted-revenue: 5.7539
    - rank: 4
      name: Leju Robotics
      hold-position-capture: 0.082388
      mobility-adjusted-capture: 0.076502
      mobility-adjusted-revenue: 3.8251
    - rank: 5
      name: EngineAI
      hold-position-capture: 0.053552
      mobility-adjusted-capture: 0.057371
      mobility-adjusted-revenue: 2.86855
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-02
---
# Humanoid Robots

## Market Definition

**Market scope.** This is the global market for general-purpose human-form embodied robots sold for industrial, logistics, commercial/service, healthcare, hazardous-work, and household use. It includes bipedal robots and human-scale two-arm robots on a wheeled mobile base when they are intended to perform tasks in human-designed environments. It excludes conventional fixed robot arms, cobots, warehouse AMRs without human-form manipulation, quadrupeds, telepresence-only devices, prototypes not sold or deployed for consideration, and components or robotics software sold independently of a complete robot.

**Revenue boundary.** Market value is annual revenue recognized by integrated robot OEMs from complete humanoid systems at the first arm's-length sale, plus OEM-recognized software, maintenance, and support tied to the installed fleet. It excludes customer implementation spend, distributor markup, component revenue earned by suppliers such as NVIDIA, contract-manufacturing revenue, GMV, and the value of labour displaced. Internal transfers, such as Tesla robots used inside Tesla factories, count only when an equivalent system sale or defensible transfer price would be recognized; otherwise they are adoption evidence rather than market revenue.

**Addressable unit and penetration.** The stable addressable unit is one full-time-equivalent physical-work position in industrial, logistics, commercial, care, or household settings that could structurally be served by a mobile two-arm robot. Penetration is a `stock` measure: active humanoid robots divided by eligible positions. Billable units are annual complete-system shipments and active robot-years receiving OEM software or support. The sizing bridge separates industrial/logistics, commercial/care, and household deployments, then sums them at the OEM revenue boundary.

**Time and value basis.** The base year is 2026 and the fixed horizon is 2036. Values are nominal USD. General inflation is included, but learning-driven hardware deflation is expected to dominate same-product pricing. The contract is deliberately narrower than broad reports that include components, non-humanoid service robots, downstream integration, or labour-market impact.

## Current View

The expected 2026 market value is **$2.5B**. TrendForce expects more than 50,000 global shipments in 2026, more than 700% above its 2025 comparison base. Applying about $48,000 of blended OEM hardware revenue per shipment gives $2.4B; roughly $0.1B of early fleet software and support reconciles the bottom-up estimate to the stored value. The blended price is an analyst estimate: low-cost Chinese platforms begin below $15,000, while full-size industrial systems remain around or above $100,000. This boundary is materially narrower than many published "humanoid robot market" totals.

Omdia's latest full-year evidence, reported by Xinhua, puts 2025 shipments at about 13,000, led by AgiBot (more than 5,100), Unitree (4,200), and UBTECH (1,000). TrendForce's April 2026 update says Unitree and AgiBot should together capture nearly 80% of Chinese shipments and that AgiBot passed 10,000 cumulative units in March. Those figures show genuine scale-up, but the mix still includes research, education, demonstrations, and pilots; paid multi-shift productive deployments remain the more important commercialization test.

The reference case is **$50B in 2036**, a 34.9% annual increase from 2026. A plausible range is roughly **$25B-$100B**. The downside is prolonged manipulation, safety, uptime, and integration failure; the upside requires household-capable autonomy or industrial economics that support several million annual units.

## Adoption Path

Adoption starts in structured industrial and logistics work where a human form avoids facility redesign: line-side material movement, tote handling, inspection, simple machine tending, and hazardous tasks. Commercial and care workflows follow as safety assurance and remote supervision improve. General household use is not required for the reference case and remains a small 2036 segment.

The sizing model does not force a logistic curve because the addressable-position denominator and early installed-base history are too uncertain for a defensible fit. Instead, it uses a durable-equipment stock-to-flow check. Active units rise from an estimated 65,000 in 2026 (about 0.04% of roughly 150M eligible positions) to about 6M in 2036 (about 3.3% of roughly 180M eligible positions). With a five-to-six-year useful life and continued new installations, this supports about 1.6M annual shipments in 2036.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Eligible physical-work positions | ~150M | ~180M | Broad industrial, logistics, service, care, and household task base |
| Active humanoid stock | ~65,000 | ~6.0M | Shipments accumulated net of retirements |
| Stock penetration | ~0.04% | ~3.3% | Active robots / eligible positions |
| Annual system shipments | >50,000 | ~1.6M | TrendForce current anchor; stock additions plus replacements at horizon |
| Net hardware revenue / shipment | ~$48,000 | ~$28,000 | Mix shift and learning outweigh nominal inflation |
| Hardware revenue | ~$2.4B | ~$44.8B | Annual shipments times OEM net revenue |
| OEM software and support | ~$0.1B | ~$5.2B | About $870 per active robot-year at horizon |
| **Annual market value** | **$2.5B** | **$50.0B** | Reconciles to front matter |

Hardware remains the dominant revenue stream in 2036. The most sensitive variables are productive deployment speed, realised rather than advertised ASP, and useful life. A faster curve also accelerates learning and price compression, so unit upside does not translate one-for-one into revenue upside.

## Market Structure

The structural trait model is expected to put heavy weight on manufacturing scale and deployment data. Both mechanisms are real: more volume improves component purchasing and production learning, while fleets generate manipulation data. Capital intensity also favours well-funded firms. Network effects are weaker than in a software marketplace because customers do not need to buy the same robot brand as peers, and models, components, and integration layers can be licensed or sourced.

The canonical concentration override assumes a 30% 2036 leader share and a 0.65 rank-decay ratio, producing an HHI of about `0.156`, or roughly 6.4 effective competitors. The override is used because the pooled trait model extrapolates hardware scale into an implausibly dominant single leader. Geography, national industrial policy, application-specific safety and service requirements, modular Asian supply chains, and low current switching costs should preserve a competitive tail even if the top few vendors achieve enormous scale.

The current market is unusually concentrated in units but less clearly so in revenue. Omdia shipment counts show AgiBot and Unitree far ahead; Unitree's lower-priced mix means unit share overstates its revenue share, while UBTECH's industrial mix likely does the opposite. The stored current revenue-share estimates apply these mix adjustments to the latest shipment ranking and are low-confidence inputs, not reported audited shares.

## Players

AgiBot, Unitree, and UBTECH are the current leaders. AgiBot combines full-size industrial and lower-cost platforms and had more than 5,100 2025 shipments in Omdia's count. Unitree has comparable volume, strong cost positioning, and a research/education-heavy mix; TrendForce reports humanoids exceeded half of its 2025 revenue. UBTECH is smaller in units but more exposed to higher-value automotive-factory deployments. Leju and EngineAI round out the current modeled top five.

The mobility model uses estimated current whole-market revenue shares of 30%, 22%, 14%, 4%, and 3%, respectively. These are derived from Omdia shipment ranks adjusted for relative product mix; they are less reliable than the shipment figures themselves. On the canonical 2036 share curve, holding today's ranks would give AgiBot, Unitree, UBTECH, Leju, and EngineAI 30.0%, 19.5%, 12.7%, 8.2%, and 5.4% capture. The pooled mobility model instead gives **21.4%, 15.7%, 11.5%, 7.7%, and 5.7%**, corresponding to **$10.7B, $7.8B, $5.8B, $3.8B, and $2.9B** of 2036 OEM revenue. The 10.1% gone probability is already embedded and is not applied again.

Tesla, Figure AI, Boston Dynamics, Agility Robotics, and 1X are credible outside challengers, but the evidence does not support a company-specific override today. Tesla in particular has manufacturing and internal-demand advantages, while its externally recognized humanoid revenue is still negligible under this contract. The mobility outputs are base rates, not company theses; they cannot see funding, product quality, management, or an outside entrant's momentum.

## Watch

- Paid deployments that progress from dozens of robots to repeat orders in the hundreds or thousands.
- Productive hours, intervention rate, task-success rate, injury and near-miss data, and total cost per useful hour.
- Evidence that 2026 shipment forecasts translate into recognized OEM revenue rather than inventory or subsidized demonstrations.
- Realized ASP and service attachment as Chinese suppliers push entry prices lower.
- Tesla Optimus, Figure, Boston Dynamics Atlas, Agility Digit, and 1X production versus announced capacity.
- Whether robot foundation models create proprietary data compounding or become broadly licensed commodities.
- Regulation, workplace liability, cybersecurity, and restrictions on Chinese embodied-AI systems.

## Peer Comparison

- **3% over our estimate at the same forecast year:** Goldman Sachs Research projects a **$38B** global humanoid market in 2035 and about **1.4M annual units**. Extending our 2026-to-2036 compound path gives **$37.1B in 2035**, so Goldman's value is 2.5% higher and is the closest boundary-and-horizon match. The implied Goldman revenue per unit is about $27,000, close to our $28,000 2036 hardware assumption.
- **398% over our estimate in 2036:** Future Market Insights projects **$248.9B** from **$10.69B in 2026**, versus our $50B and $2.5B. Its stated scope—complete bipedal and wheeled platforms plus bundled software, maintenance, and deployment services—is broadly similar, making this a real disagreement rather than a clean scope reconciliation. Its 2026 value implies about $214,000 per TrendForce-forecast shipment before allowing for any units outside TrendForce's definition, far above the observed low-cost Chinese mix; we therefore retain the lower bottom-up anchor.
- **51% over a mechanical continuation, but not directly comparable:** Morgan Stanley projects a **$5T** market and nearly **1B active humanoids in 2050**, 14 years beyond this document's fixed horizon. Mechanically extending our 34.9% growth rate produces $3.3T, but that extrapolation is not a forecast and Morgan Stanley includes a much later household-adoption wave plus hardware, software, data, and services. Its 2050 price assumptions—about $50,000 in high-income and $15,000 in lower-income countries—are useful long-run checks, not reasons to change the 2036 input set.

## Sources

- TrendForce, "Diverging Humanoid Robot Strategies...", December 9, 2025: https://www.trendforce.com/presscenter/news/20251209-12825.html
- TrendForce, "China's Humanoid Robot Output to Surge 94% in 2026...", April 9, 2026: https://www.trendforce.com/presscenter/news/20260409-13007.html
- Xinhua, summarising Omdia's *General-purpose Embodied Intelligent Robots* report, January 9, 2026: https://english.news.cn/20260109/bab6612656664145bb5becc3781edd59/c.html
- Goldman Sachs Research, "The global market for humanoid robots could reach $38 billion by 2035", February 27, 2024: https://www.goldmansachs.com/insights/articles/the-global-market-for-robots-could-reach-38-billion-by-2035
- Morgan Stanley Research, "Humanoids: A $5 Trillion Market", May 14, 2025: https://www.morganstanley.com/insights/articles/humanoid-robot-market-5-trillion-by-2050
- Future Market Insights, "Humanoid Robot Market: Global Industry Analysis and Opportunity Assessment, 2036", 2026: https://www.futuremarketinsights.com/reports/humanoid-robot-market
