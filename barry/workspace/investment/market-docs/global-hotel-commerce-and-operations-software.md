---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 6.8
  maturity-market-value: 15.5
penetration:
  inputs:
    target-series: data/global-hotel-commerce-and-operations-software/penetration.csv
    measure: stock
    ceiling: 0.90
    analogs:
      - us-home-computer
      - us-cable-tv
      - us-streaming-svod
    w-fit: 0.45
  model-estimate:
    L: 0.9
    t0: 2025.570334
    k: 0.188067
  method: logistic-blend
  date: 2026-08-09
concentration:
  inputs:
    traits:
      network-effects: {score: 0.25, confidence: 0.75}
      data-scale-advantage: {score: 0.45, confidence: 0.65}
      brand-reputation: {score: 0.55, confidence: 0.70}
      capital-intensity: {score: 0.15, confidence: 0.80}
      scale-economies: {score: 0.60, confidence: 0.75}
      regulatory-barriers: {score: 0.35, confidence: 0.70}
      switching-costs: {score: 0.75, confidence: 0.80}
  model-estimate:
    s1: 0.157282
    r: 0.837089
  hhi: 0.082656
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: Oracle Hospitality
        ticker: ORCL
        share: 0.13
      - rank: 2
        name: Amadeus Hospitality
        ticker: AMS.MC
        share: 0.11
      - rank: 3
        name: Shiji Group
        ticker: 002153.SZ
        share: 0.07
      - rank: 4
        name: Sabre Hospitality
        ticker: SABR
        share: 0.05
      - rank: 5
        name: Agilysys
        ticker: AGYS
        share: 0.04
  model-estimate:
    - rank: 1
      name: Oracle Hospitality
      ticker: ORCL
      hold-position-capture: 0.157282
      mobility-adjusted-capture: 0.123915
      mobility-adjusted-revenue: 1.920682
    - rank: 2
      name: Amadeus Hospitality
      ticker: AMS.MC
      hold-position-capture: 0.131659
      mobility-adjusted-capture: 0.10593
      mobility-adjusted-revenue: 1.641915
    - rank: 3
      name: Shiji Group
      ticker: 002153.SZ
      hold-position-capture: 0.11021
      mobility-adjusted-capture: 0.090104
      mobility-adjusted-revenue: 1.396612
    - rank: 4
      name: Sabre Hospitality
      ticker: SABR
      hold-position-capture: 0.092256
      mobility-adjusted-capture: 0.072183
      mobility-adjusted-revenue: 1.118837
    - rank: 5
      name: Agilysys
      ticker: AGYS
      hold-position-capture: 0.077226
      mobility-adjusted-capture: 0.058822
      mobility-adjusted-revenue: 0.911741
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---

# Global Hotel Commerce and Operations Software

## Market Definition

**Market scope.** Global purpose-built software used by hotels, resorts, hostels and serviced-apartment operators to sell and operate lodging inventory. Included modules are property management (PMS), central reservations (CRS), booking engines, channel management, revenue management, hotel-specific CRM and guest engagement, housekeeping and maintenance workflow, hotel point of sale, analytics, implementation and support, and vendor-provided payment enablement when sold as part of the hotel platform. Both cloud and supported on-premises deployments are included. Excluded are OTA and travel-agency commissions, global-distribution-system airline economics, hotel room revenue, vacation-rental marketplace or owner revenue, restaurant-only and cruise-only systems, building controls and physical security, general-purpose ERP/accounting/workforce software, telecom, hardware resale, and payment interchange or processor revenue not retained by the software vendor.

**Revenue boundary.** Annual revenue recognized by the hotel-software vendor for subscriptions, maintenance, licenses, implementation, hotel-specific transaction fees and the vendor's retained net payment revenue. Hotel gross booking value, room revenue, merchant payment volume, OTA commissions, taxes, pass-through processing costs and reseller channel revenue are not market value. Multi-vertical vendors are allocated only for hotel and lodging-property use; the same vendor-revenue boundary is used for sizing, concentration and shares.

**Addressable unit and penetration.** The stable denominator is a global hotel-room-equivalent in structurally commercial lodging properties, aggregated from hotels, resorts, hostels and serviced apartments. The numerator is room-equivalents operated on a connected cloud or centrally hosted hotel commerce-and-operations platform, so penetration is a `stock` measure. The target series is an analyst reconstruction from disclosed vendor property footprints, hotel-system migrations and the 2025 estimate that cloud represented about 71% of category revenue; revenue share is used only as a cross-check because large chain rooms spend more per unit than small independents.

**Billable units and segments.** Billable units are active room-equivalents, properties, software modules, transactions and implementation projects. The bridge separates (1) enterprise chains and complex resorts, which have more rooms, modules and integration work per property, from (2) independent and small-group lodging, which has many more properties but lower revenue per room. Geographic estimates are translated to USD and aggregated only after excluding non-hotel verticals and duplicated reseller revenue.

**Time and value basis.** Base year 2026, fixed horizon 2036, nominal USD at approximately current exchange rates. Ordinary hotel-room growth, cloud migration and higher module/payment attachment are modeled separately.

## Current View

Expected 2026 market value is **USD 6.8 billion**, with a plausible range of USD 5.5-8.5 billion. The estimate is broader than a PMS-only category but narrower than generic hospitality technology. Direct disclosure anchors include Amadeus's EUR 1.052 billion of 2025 Hospitality and Transversal Solutions revenue, of which only the hotel-related share is included; Agilysys's USD 319.3 million of fiscal-2026 hospitality revenue, allocated away from cruise, foodservice, sports and healthcare; and SiteMinder's AUD 224.3 million of fiscal-2025 revenue, substantially all inside the contract. SiteMinder served 50,100 properties and processed more than AUD 85 billion of booking value, while Cloudbeds says it serves more than 20,000 properties. Oracle, Shiji, Sabre, Mews, Infor, IDeaS, Duetto, Lighthouse and the private regional tail require product- and vertical-level estimates because clean hotel-only revenue is generally not disclosed.

The bottom-up check uses roughly **50 million addressable room-equivalents**, 46% connected-platform penetration and about **USD 296 of annual vendor revenue per adopted room-equivalent**. That gives USD 6.8 billion after including enterprise implementation and transaction modules but excluding hotel booking value and pass-through payments. It also reconciles with published 2025 estimates ranging from USD 3.62 billion for a narrower hotel-management category to USD 6.07 billion for a broad PMS definition. The largest uncertainty is not room count but boundary: research publishers inconsistently include security/building systems, services, restaurant systems, CRS/distribution and payment revenue.

## Adoption Path

The reconstructed connected-platform share rises from 21% in 2018 to 46% in 2026. It represents room-equivalents rather than properties to avoid giving a five-room inn the same economic weight as a 500-room hotel. Evidence quality is low-to-medium: public vendors disclose customer or property counts, but not a deduplicated global installed base, and large chains often run several included vendors at once. The series should be replaced if an industry body publishes consistent hotel-room deployment data.

A 90% ceiling allows connected cloud or centrally hosted systems to become standard without assuming that every small or remote property adopts a full commercial platform. U.S. home computers provide a slow installed-base technology analog, cable TV captures a subscription with installation and switching friction, and streaming video supplies a faster cloud-subscription analog. Because the target is reconstructed and still below one-third of the asserted ceiling until recently, target-fit weight is capped at 45%.

The blended logistic curve has `L=0.90`, `t0=2025.57` and `k=0.1881`. It smooths the 46% reconstructed 2026 observation to 46.8% and reaches **78.9% in 2036**. The size bridge grows the room-equivalent denominator from about 50 million to 59 million (1.7% annually), applies that path, and raises recognized revenue per adopted room-equivalent from about USD 296 on the observed 2026 base to roughly USD 333. The modest nominal increase reflects broader RMS, CRM, payments, AI and guest-workflow attachment offset by commoditization and cloud efficiency. Category expansion is limited to modules already inside the contract; OTA distribution economics, hotel revenue, building automation and general-purpose software remain excluded.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Addressable room-equivalents | about 50m | about 59m | Hotels, resorts, hostels and serviced apartments; 1.7% annual growth |
| Connected-platform penetration | 46% observed / 46.8% curve | 78.9% | `stock` share of room-equivalents on connected cloud/hosted systems |
| Adopted room-equivalents | about 23m | about 46.6m | No second eligibility or attachment factor |
| Vendor revenue per adopted room-equivalent | about USD 296 | about USD 333 | Subscriptions, modules, implementation and retained hotel-platform transaction revenue |
| Annual market value | **USD 6.8bn** | **USD 15.5bn** | Nominal vendor-recognized revenue |

The expected 2036 market value is **USD 15.5 billion**, an 8.6% CAGR. A plausible range is USD 10-23 billion. The main downside is price compression and modular best-of-breed competition; the upside is faster independent-hotel digitization plus integrated payments, revenue intelligence and guest-commerce take-rates. Subscription and transaction revenue should dominate by 2036, while perpetual licenses and one-time migration work decline as a share.

## Market Structure

The share basis is global vendor revenue under the stated hotel-only contract. Network effects score 0.25: integration marketplaces, distribution connectivity and payment rails improve with ecosystem breadth, but hotels can multi-home across specialized applications and local implementation capacity matters. Data-scale advantage is 0.45 because pricing, forecasting and guest-personalization models improve with booking data, though hotels retain key data and demand is highly local. Brand and reputation score 0.55 because uptime, security and chain references matter in mission-critical deployments.

Capital intensity is low at 0.15, although enterprise migrations and global support require sustained investment. Scale economies score 0.60 through shared cloud infrastructure, integrations, compliance and product development, offset by local tax rules, support and implementation. Regulatory barriers are moderate-low at 0.35: PCI, privacy and local fiscalization create friction but rarely block new entry. Switching costs are high at 0.75 because the PMS/CRS is a system of record connected to payments, distribution, locks, POS and staff workflows; data migration and retraining are operationally risky.

The deterministic trait model gives `s1=0.1573` and `r=0.8371`, producing a 2036 **HHI of 0.0827**, or about 12 effective competitors. No override is used. Structurally, high switching costs protect several installed vendors rather than only the leader, while geographic and hotel-segment specialization sustain a long tail. The result is fragmented, not winner-take-most, and its predicted rank shares are consistent with a market where the named leaders cover well under half of current revenue. Revisit the traits if one platform converts payments, distribution data and an app ecosystem into portable global network effects, or if chain migrations and private-equity consolidation materially thin the regional tail.

## Players

Current whole-market shares are low-confidence analyst estimates normalized to the common boundary: Oracle Hospitality 13%, Amadeus Hospitality 11%, Shiji Group 7%, Sabre Hospitality 5% and Agilysys 4%. Oracle's rank rests on OPERA's enterprise installed base; Amadeus's disclosed Hospitality and Transversal revenue is allocated to hotel products; Shiji and Sabre require hotel-product estimates; Agilysys's fiscal-2026 revenue is allocated away from non-lodging verticals. The named five cover only 40%, consistent with a fragmented mix of Mews, Cloudbeds, SiteMinder, Infor, IDeaS, Duetto, Lighthouse, Guestline, Protel, regional PMS vendors and specialist modules.

The mobility model converts those current positions into hold-position and mobility-adjusted 2036 capture. Its pooled ten-year base rate sees current rank and share spacing but not company momentum, chain migration cycles, acquisition strategy or vendor-specific product breadth. The 10.06% gone probability is already included in mobility-adjusted capture and is not applied again.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
|---|---:|---:|---:|
| Oracle Hospitality | 15.73% | 12.39% | USD 1.92bn |
| Amadeus Hospitality | 13.17% | 10.59% | USD 1.64bn |
| Shiji Group | 11.02% | 9.01% | USD 1.40bn |
| Sabre Hospitality | 9.23% | 7.22% | USD 1.12bn |
| Agilysys | 7.72% | 5.88% | USD 0.91bn |

No player override is used; Mews, Cloudbeds and SiteMinder are the clearest outside contenders if cloud-native platforms keep compounding faster than legacy suites. The model view should not be read as company-specific conviction: its rising hold-position shares for ranks 3-5 come from the predicted market shape, while the mobility adjustment discounts all incumbents for rank churn and exit.

## Watch

- Oracle, Amadeus, Shiji and Sabre disclosure that separates hotel software from transversal payments, airline/travel distribution and other verticals.
- Mews, Cloudbeds and private-vendor ARR or revenue disclosures; property counts alone obscure room mix and payment monetization.
- SiteMinder's property growth, revenue per property, transaction-product adoption and progress toward its medium-term 30% revenue-growth ambition.
- Share of global hotel rooms on cloud/hosted PMS and CRS, ideally from a consistent room-level series rather than vendor customer counts.
- Chain-level migrations from OPERA on-premises and legacy proprietary systems to OPERA Cloud, Amadeus, Shiji, Mews or Cloudbeds.
- Net payment revenue retained by hotel platforms versus pass-through processor revenue; payment volume is not market value.
- Whether AI pricing, guest messaging and autonomous operations become paid modules or are bundled into base subscription prices.
- Consolidation among regional PMS, RMS and guest-experience vendors, and whether app marketplaces preserve modular competition.

## Peer Comparison

- **About 50% under our 2030 estimate:** The Business Research Company (2026) forecasts hotel and hospitality management software from **USD 3.62 billion in 2025 to USD 4.78 billion in 2030**, versus about USD 9.5 billion on our interpolated path. Its scope includes building automation, security and communications but appears narrower on CRS, revenue management, hotel POS and retained transaction revenue, so the arithmetic is directionally comparable but the boundary is not identical.
- **About 40% under our 2035 estimate:** SNS Insider (2026) forecasts **USD 8.55 billion in 2035** from USD 4.19 billion in 2025, versus about USD 14.3 billion on our path. Its stated modules cover PMS, revenue management and guest systems and its 7.4% CAGR is close to ours; the lower level likely reflects a narrower software boundary and less retained transaction revenue.
- **About 41% under our 2035 estimate:** Expert Market Research (2026) forecasts **USD 8.37 billion in 2035** from USD 4.72 billion in 2025. It includes software and services plus some building/security categories, but does not clearly include the full commerce stack; treat the comparison as a useful lower-bound growth path rather than an exact match.
- **About 30% under our 2035 estimate:** Market Research Future (May 2026) forecasts hospitality PMS from **USD 6.07 billion in 2025 to USD 10.0 billion in 2035**, versus about USD 14.3 billion on our path. The current level is close, while the 5.12% forecast CAGR is slower and the stated boundary is PMS rather than the full hotel commerce-and-operations stack.

The comparable long-term publications cluster around USD 8-10 billion in 2035. Our higher USD 14.3 billion 2035 interpolation rests on broader but fixed module coverage and increased paid-module/payment attachment; if those adjacencies are bundled rather than separately monetized, the peer cluster is a credible downside.

## Sources

- SiteMinder, *FY25 Annual Report*, August 27, 2025: https://www.siteminder.com/wp-content/uploads/2025/08/250827_FY25-Annual-Report.pdf
- SiteMinder, *What is SiteMinder?*, accessed August 9, 2026: https://www.siteminder.com/about/
- Amadeus, *Global Report 2025 — Amadeus Profile and Corporate Performance*, 2026: https://amadeus.com/documents/en/global-report-2025/chapters/amadeus-profile-and-corporate-performance.pdf
- Agilysys, *Form 10-K for the fiscal year ended March 31, 2026*, May 21, 2026: https://www.sec.gov/Archives/edgar/data/78749/000119312526234423/agys-20260331.htm
- Oracle Hospitality, *OPERA Cloud Property Management*, accessed August 9, 2026: https://www.oracle.com/hospitality/hotel-property-management/hotel-pms-software/
- Cloudbeds, *Hospitality Management Platform*, accessed August 9, 2026: https://www.cloudbeds.com/
- Mews, *The operating system for modern hotels*, accessed August 9, 2026: https://www.mews.com/en
- The Business Research Company, *Hotel and Hospitality Management Software Global Market Report 2026*: https://www.thebusinessresearchcompany.com/report/hotel-and-hospitality-management-software-global-market-report
- SNS Insider, *Hotel and Hospitality Management Software Market*, 2026: https://www.snsinsider.com/reports/hotel-and-hospitality-management-software-market-6525
- Expert Market Research, *Hotel and Hospitality Management Software Market*, 2026: https://www.expertmarketresearch.com/reports/hotel-and-hospitality-management-software-market
- Market Research Future, *Hospitality Property Management Software Market*, updated May 15, 2026: https://www.marketresearchfuture.com/reports/hospitality-property-management-software-market-42704
