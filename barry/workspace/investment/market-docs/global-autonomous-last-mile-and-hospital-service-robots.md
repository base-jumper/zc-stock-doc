---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.35
  maturity-market-value: 9.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.35, confidence: 0.55}
      data-scale-advantage: {score: 0.60, confidence: 0.60}
      brand-reputation: {score: 0.55, confidence: 0.50}
      capital-intensity: {score: 0.55, confidence: 0.55}
      scale-economies: {score: 0.65, confidence: 0.60}
      regulatory-barriers: {score: 0.55, confidence: 0.60}
      switching-costs: {score: 0.70, confidence: 0.65}
  override:
    s1: 0.22
    r: 0.72
    reason: "The pooled trait model implies a 28% leader and a hard-oligopoly tail, but this contract combines two adjacent segments with different buyers, regulations, workflows, and geographic operating density. A 22% leader with a broader competitive tail better reflects a market in which firms can lead hospital transport or outdoor delivery without controlling both globally."
  model-estimate:
    s1: 0.278987
    r: 0.729744
  hhi: 0.100498
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: Aethon
        ticker: S63.SI
        share: 0.14
      - rank: 2
        name: OMRON
        ticker: 6645.T
        share: 0.11
      - rank: 3
        name: Swisslog Healthcare
        share: 0.09
      - rank: 4
        name: Starship Technologies
        share: 0.08
      - rank: 5
        name: Serve Robotics
        ticker: SERV
        share: 0.04
  model-estimate:
    - rank: 1
      name: Aethon
      ticker: S63.SI
      hold-position-capture: 0.22
      mobility-adjusted-capture: 0.161581
      mobility-adjusted-revenue: 1.454229
    - rank: 2
      name: OMRON
      ticker: 6645.T
      hold-position-capture: 0.1584
      mobility-adjusted-capture: 0.122183
      mobility-adjusted-revenue: 1.099647
    - rank: 3
      name: Swisslog Healthcare
      hold-position-capture: 0.114048
      mobility-adjusted-capture: 0.089085
      mobility-adjusted-revenue: 0.801765
    - rank: 4
      name: Starship Technologies
      hold-position-capture: 0.082115
      mobility-adjusted-capture: 0.066246
      mobility-adjusted-revenue: 0.596214
    - rank: 5
      name: Serve Robotics
      ticker: SERV
      hold-position-capture: 0.059122
      mobility-adjusted-capture: 0.060654
      mobility-adjusted-revenue: 0.545886
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---
# Global Autonomous Last-Mile and Hospital Service Robots

## Market Definition

**Market scope.** This is the global market for compact autonomous mobile robots that transport small goods through human-centred environments in two segments: (1) outdoor sidewalk and campus last-mile delivery of food, groceries, parcels, and supplies; and (2) in-hospital transport of medications, specimens, linens, meals, equipment, and other supplies. It includes complete robots, autonomy and fleet-management software, deployment, maintenance, and robot-as-a-service or per-delivery operation when controlled by the robot provider. It excludes warehouse and factory AMRs, forklifts and pallet systems, road-going autonomous vehicles, drones, hotel-only robots, cleaning and disinfection robots, telepresence, pharmacy or laboratory automation that does not move through the hospital, surgical and rehabilitation robots, humanoids, and components sold independently.

**Revenue boundary.** Market value is annual revenue recognized by the provider controlling the autonomous robot system: complete-system sales plus tied software, deployment, maintenance, and support for customer-owned fleets, or fleet-service and subscription revenue when the provider retains the robots. Merchant and restaurant GMV, the consumer's underlying order value, delivery-platform commissions unrelated to robot operation, hospital labour savings, distributor mark-up, and component-supplier revenue are excluded. If a third party buys a system and separately operates deliveries, only the autonomy provider's system revenue is counted, preventing hardware and downstream delivery fees from being double-counted.

**Addressable units and penetration.** Outdoor adoption uses an addressable **service zone**: a dense neighbourhood, campus, grocery catchment, or mixed-use site with enough short-distance demand and permissive infrastructure. Hospital adoption uses an addressable **hospital site** large enough to support repeat internal transport. Penetration is a `stock` measure in both segments: active robot-enabled service zones divided by eligible zones, and hospitals with an active transport fleet divided by eligible hospitals. Billable units are completed autonomous deliveries or active robot-years outdoors, and annual system shipments plus supported robot-years in hospitals. The segments are modeled separately and summed at the common provider-revenue boundary.

**Time and value basis.** The base year is 2026 and the fixed horizon is 2036. Values are nominal USD. General inflation is included, while learning and competition lower real hardware prices and revenue per delivery. A single logistic penetration block is not fitted because outdoor service zones and hospitals have different denominators and no attributable global time series exists on this narrow boundary; forcing the two into one series would be false precision.

## Current View

The expected 2026 market value is **$0.35B**: about **$0.08B** from outdoor delivery and **$0.27B** from hospital logistics. The estimate is deliberately narrower than market reports that include drones, autonomous vans, warehouse AMRs, medical robots generally, or the value of the goods delivered.

The outdoor check begins with roughly 10,000 active robots globally. Starship reported more than 3,000 robots, 10 million cumulative deliveries, and operations at 300-plus locations in eight countries in April 2026; Serve reported more than 2,000 sidewalk robots at December 2025. Adding Robot.com/Kiwibot, Cartken, and Asian operators produces the round installed-base estimate. At about six paid deliveries per robot-day, 300 operating days, and $2.50 of provider revenue per delivery, fleet services contribute roughly $45M; third-party system sales, software, advertising, and support lift the segment to about $80M.

The hospital check assumes about 6,000 active transport robots, roughly 2,000 current-year shipments and new deployments, $90,000 of net system revenue per shipment, and $15,000 of annual software, support, and RaaS revenue per active robot. That yields about $270M. Aethon says its installed base spans hundreds of customer sites; Serve's acquired Diligent/Moxi operation generated $2.9M from January 27 through June 30, 2026. Serve's combined outdoor and indoor business reported $6.2M for the first half and $6.7M of pro-forma revenue including pre-acquisition Diligent, which is consistent with roughly a 4% share of the defined market rather than a broad robotics market.

The reference case is **$9.0B in 2036**, a 38.4% compound annual increase. A plausible range is roughly **$3B-$20B**. The downside is that human intervention, vandalism, permits, building integration, and weak utilization keep deployments site-specific. The upside requires reliable autonomy and dense utilization to make robots a standard transport layer for delivery platforms and hospitals.

## Adoption Path

Outdoor adoption expands first in campuses, planned communities, grocery catchments, and low-speed urban districts where routes are short and repeatable. Hospital adoption expands through multi-robot fleets integrated with elevators, doors, badge access, pharmacy, and clinical workflows. RaaS reduces up-front purchasing friction: IFR reported that professional-service-robot RaaS fleets grew 31% in 2024, while transportation-and-logistics RaaS grew 42%.

The 2036 bridge has two parts. Outdoor service grows to about 1.3M active robots across roughly 50,000 zones. At 12 deliveries per robot-day, 320 days, and $1.20 of provider revenue per delivery, it produces about $6.0B. The revenue per drop is consistent with Starship's long-term target of roughly $1 before allowing for software, advertising, and premium use cases. Hospitals grow to about 8,500 adopted sites, or one quarter of roughly 34,000 structurally eligible sites, with 12 robots per adopted site. About 25,000 annual new and replacement shipments at $70,000 plus $12,000 of support/RaaS per active robot produces about $3.0B.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Outdoor active service zones | ~800 | ~50,000 | Dense public or campus operating areas |
| Outdoor active robots | ~10,000 | ~1.3M | Fleet stock across adopted zones |
| Paid deliveries / robot-day | ~6 | ~12 | Utilization and platform matching improve |
| Provider revenue / delivery | ~$2.50 | ~$1.20 | Learning and competition outweigh nominal inflation |
| Outdoor annual market value | **$0.08B** | **$6.0B** | Fleet service plus tied systems/software |
| Eligible hospital sites | ~30,000 | ~34,000 | Medium and large sites with repeat transport demand |
| Hospital sites with fleets | ~1,000 | ~8,500 | About 3% to 25% site penetration |
| Active hospital robots | ~6,000 | ~102,000 | Six to twelve robots per adopted site |
| Annual new/replacement shipments | ~2,000 | ~25,000 | Installations plus five-to-seven-year replacement |
| Hospital annual market value | **$0.27B** | **$3.0B** | Systems plus software, support, and RaaS |
| **Total annual market value** | **$0.35B** | **$9.0B** | Reconciles to front matter |

The outdoor service stream dominates 2036 revenue. The largest sensitivities are deliveries per robot-day, the fraction of eligible zones that permits operation, hospital fleet size, and how much hardware price decline is retained by providers versus passed through to customers.

## Market Structure

The market has useful but bounded data and density advantages. More real-world miles expose autonomy systems to edge cases, and a dense local fleet improves depot, maintenance, and remote-supervision economics. These are not global single-home network effects: customers can use multiple delivery platforms, hospital procurements are local, and a competitor can enter one geography or workflow without replicating every incumbent location.

Scale economies are meaningful in autonomy R&D, robot manufacturing, fleet operations, insurance, and regulatory engagement. Switching costs are stronger inside hospitals because a deployed fleet integrates with elevators, doors, security, software, and staff workflows; outdoor platforms can multi-source more readily. Safety reputation and regulatory approval matter, but fragmented municipal rules and hospital procurement also preserve regional and application specialists.

The trait model's unadjusted result implies a roughly 28% leader and a hard-oligopoly tail. The canonical override instead uses a 22% leader and a 0.72 rank-decay ratio, producing a projected HHI of about **0.101**, equivalent to roughly ten effective competitors. The adjustment reflects the two-segment contract: one provider may dominate outdoor delivery while another leads hospital transport, without either controlling the combined global revenue pool.

## Players

Current whole-market shares are not published, so the stored ranking is a low-confidence revenue reconstruction from installed-site disclosures, fleet size, product mix, and Serve's audited revenue. Aethon is estimated at 14%, OMRON at 11%, Swisslog Healthcare at 9%, Starship at 8%, and Serve Robotics at 4%. These imply about $49M, $39M, $32M, $28M, and $14M of 2026 provider revenue, respectively. The first three are hospital-heavy; Starship is the outdoor scale leader; Serve spans both segments after acquiring Diligent Robotics.

Aethon's TUG robots have operated for two decades across hundreds of sites and handle large hospital payloads. OMRON and Swisslog bring established automation channels and hospital logistics integration. Starship has the largest disclosed outdoor fleet and a uniquely deep public-sidewalk operating dataset. Serve has more than 2,000 outdoor robots, platform integrations with Uber Eats and DoorDash, and Moxi's hospital workflow, but remains early in revenue. Relay Robotics, Robot.com/Kiwibot, Cartken, JD Logistics, Meituan, Alibaba, Panasonic, PAL Robotics, and new autonomy entrants form a substantial tail.

Holding today's ranks on the canonical 2036 curve would give Aethon, OMRON, Swisslog, Starship, and Serve 22.0%, 15.8%, 11.4%, 8.2%, and 5.9% capture. The mobility-adjusted estimates are **16.2%, 12.2%, 8.9%, 6.6%, and 6.1%**, corresponding to **$1.45B, $1.10B, $0.80B, $0.60B, and $0.55B** of 2036 provider revenue. The model's 10.1% gone probability is already embedded and is not applied again.

These outputs are pooled base rates. They do not see company-specific momentum, funding, product reliability, hospital channel quality, or the probability that a new entrant becomes a top-five player. No company-specific override is justified by the current evidence.

## Watch

- Paid deliveries per robot-day, autonomous miles between interventions, remote-supervisor ratio, and contribution margin per delivery.
- Repeat fleet expansion at the same hospital or service zone after an initial pilot.
- Municipal permits, accessibility incidents, sidewalk obstruction rules, and insurance requirements.
- Hospital elevator, door, badge, cybersecurity, and HIPAA integration time and renewal rates.
- Starship's conversion of 10M cumulative deliveries and 3,000-plus robots into durable provider revenue.
- Serve's outdoor utilization and the post-acquisition growth, margins, and cross-selling of Diligent/Moxi.
- Asian outdoor fleets and hospital AMR vendors whose revenue and deployment counts are poorly disclosed in English-language sources.
- Whether general-purpose indoor/outdoor AMR platforms commoditize hardware or proprietary autonomy data creates a durable quality gap.

## Peer Comparison

- **About 340% over our 2030 combined-market path, but not directly comparable:** Next Move Strategy Consulting estimated the hospital-logistics-robots market at **$1.21B in 2022** and **$5.64B in 2030** (20.9% CAGR). Our combined narrow contract reaches about **$1.28B in 2030**, including only mobile in-hospital transport plus sidewalk delivery. The peer report's participant list includes broad AMR and industrial-automation suppliers and its stated drivers include telemedicine and remote care, indicating a substantially wider hospital-logistics boundary.
- **About 150% over our 2033 combined-market path, but not directly comparable:** Grand View Research values autonomous mobile delivery robots at **$1.5B in 2024** and **$8.4B in 2033** (21.9% CAGR), versus about **$3.4B** on our interpolated 2033 path. Its scope includes manufacturing and other indoor/outdoor material movement beyond last-mile and hospitals; the gap is therefore mainly boundary, not a clean forecast disagreement.
- **About 360% over our 2030 combined-market path, not directly comparable:** Grand View Research estimates autonomous last-mile delivery at **$1.6B in 2024** and **$5.9B in 2030** (24.8% CAGR). The category includes autonomous road vehicles and drones as well as ground robots, while our outdoor segment is limited to compact sidewalk/campus robots and our 2030 comparison figure also includes hospitals.
- IFR's **102,900 transportation-and-logistics professional service robots sold in 2024** is a useful physical ceiling, not a market-value forecast. IFR says indoor transport without public traffic dominates the category and explicitly warns that its sample of 294 suppliers is not projected to the whole industry. Our narrow current volume—about 12,000 combined outdoor robots and hospital shipments/active deployments—is plausible as a small subset of that broader class.

## Sources

- International Federation of Robotics, "Service Robots See Global Growth Boom," October 7, 2025: https://ifr.org/ifr-press-releases/news/service-robots-see-global-growth-boom
- Starship Technologies, "Autonomous Delivery Moves Into the Mainstream as Starship Technologies Passes 10 Million Deliveries," April 2026: https://www.starship.xyz/press/autonomous-delivery-moves-into-the-mainstream-as-starship-technologies-passes-10-million-deliveries/
- Serve Robotics, 2025 Form 10-K, filed March 12, 2026: https://www.sec.gov/Archives/edgar/data/1832483/000183248326000010/patr-20251231.htm
- Serve Robotics, Q2 2026 Form 10-Q, filed August 2026: https://www.sec.gov/Archives/edgar/data/1832483/000183248326000035/serv-20260630.htm
- Aethon, company and hospital-robot deployment overview, accessed August 9, 2026: https://aethon.com/
- Cartken, indoor/outdoor AMR product and deployment overview, accessed August 9, 2026: https://www.cartken.com/
- Next Move Strategy Consulting via GlobeNewswire, "Global Hospital Logistics Robots Market to Generate USD 5637.9 Million by 2030," March 21, 2023: https://www.globenewswire.com/news-release/2023/03/21/2631334/0/en/Global-Hospital-Logistics-Robots-Market-to-Generate-USD-5637-9-Million-by-2030-Outlines-a-New-Report-by-Next-Move-Strategy-Consulting.html
- Grand View Research, "Autonomous Mobile Delivery Robots Market," accessed August 9, 2026: https://www.grandviewresearch.com/industry-analysis/autonomous-mobile-delivery-robots-market-report
- Grand View Research, "Autonomous Last Mile Delivery Market," accessed August 9, 2026: https://www.grandviewresearch.com/industry-analysis/autonomous-last-mile-delivery-market
