---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 5.5
  maturity-market-value: 21.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.20, confidence: 0.85}
      data-scale-advantage: {score: 0.55, confidence: 0.75}
      brand-reputation: {score: 0.75, confidence: 0.75}
      capital-intensity: {score: 0.72, confidence: 0.85}
      scale-economies: {score: 0.82, confidence: 0.85}
      regulatory-barriers: {score: 0.55, confidence: 0.85}
      switching-costs: {score: 0.78, confidence: 0.85}
  override:
    s1: 0.28
    r: 0.70
    reason: "Counterpoint's boundary-near 2035 forecast puts the five named ADAS/AV SoC leaders at 78% combined share; a 28% leader and 0.70 geometric rank decay reproduce 77.7% top-five share while retaining a regional and specialist fringe."
  model-estimate:
    s1: 0.228424
    r: 0.776482
  hhi: 0.153725
  method: selected-direct-ridge
  date: 2026-08-03
players:
  inputs:
    current:
      - rank: 1
        name: Mobileye
        ticker: MBLY
        share: 0.31
      - rank: 2
        name: NVIDIA
        ticker: NVDA
        share: 0.16
      - rank: 3
        name: Qualcomm
        ticker: QCOM
        share: 0.10
      - rank: 4
        name: Horizon Robotics
        ticker: 9660.HK
        share: 0.07
      - rank: 5
        name: Huawei
        share: 0.05
  model-estimate:
    - rank: 1
      name: Mobileye
      ticker: MBLY
      hold-position-capture: 0.28
      mobility-adjusted-capture: 0.215571
      mobility-adjusted-revenue: 4.526991
    - rank: 2
      name: NVIDIA
      ticker: NVDA
      hold-position-capture: 0.196
      mobility-adjusted-capture: 0.157984
      mobility-adjusted-revenue: 3.317664
    - rank: 3
      name: Qualcomm
      ticker: QCOM
      hold-position-capture: 0.1372
      mobility-adjusted-capture: 0.11425
      mobility-adjusted-revenue: 2.39925
    - rank: 4
      name: Horizon Robotics
      ticker: 9660.HK
      hold-position-capture: 0.09604
      mobility-adjusted-capture: 0.083869
      mobility-adjusted-revenue: 1.761249
    - rank: 5
      name: Huawei
      hold-position-capture: 0.067228
      mobility-adjusted-capture: 0.064771
      mobility-adjusted-revenue: 1.360191
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-03
---
# Global Automotive-Grade AI SoCs

## Market Definition

**Market scope:** worldwide merchant automotive-grade system-on-chips and inseparable silicon-level software or licences used for onboard AI inference in ADAS, automated driving and centralized vehicle perception/decision compute. Included products range from cost-efficient front-camera processors such as Mobileye EyeQ to high-performance domain and central-compute SoCs such as NVIDIA DRIVE, Qualcomm Snapdragon Ride, Horizon Journey and Huawei MDC/Ascend automotive processors. Excluded are general-purpose MCUs, connectivity-only and infotainment-only processors, memory, sensors, power semiconductors, complete ECUs beyond the included SoC/platform value, cloud training compute, robotaxi service revenue, contract-foundry revenue and captive chips with no external vendor revenue. A cockpit function is included only when it is inseparable from a sold central AI SoC that also performs included safety or driving workloads.

**Revenue boundary:** annual recognized revenue of the SoC/platform vendor at the first external sale, including software or licences inseparable from the silicon sale and excluding Tier-1/OEM hardware markup, vehicle price, foundry revenue and internal transfer value for captive OEM chips. Diversified vendors' reported automotive segments are used only after removing cockpit, connectivity, telematics and other out-of-contract content.

**Addressable unit:** a new light vehicle structurally capable of adopting an included AI SoC. **Penetration measure:** `new-sales-share`, the number of new light vehicles shipped with at least one included SoC divided by total new light-vehicle shipments. **Billable units:** included SoCs shipped, plus inseparable per-vehicle software/licence value; one vehicle can contain more than one billable SoC. **Segments:** cost-efficient L1/L2 front-camera ADAS and higher-performance L2+/L3/central compute are modeled separately, then added at the same vendor-revenue boundary.

**Time and value basis:** 2026 base year, fixed 2036 horizon, nominal USD at approximately constant current foreign-exchange rates. The contract is unchanged for size, concentration and player capture.

## Current View

The expected 2026 market value is **$5.5b**, with a rough **$4.0b-$7.5b** range. Public disclosures do not isolate this exact boundary, so the estimate triangulates supplier revenue and a vehicle-content bridge. Mobileye's 2025 Form 10-K reports $1.894b total revenue, 91% from EyeQ SoCs, and 35.7m EyeQ/SuperVision systems shipped; this implies about $1.72b of directly attributable EyeQ revenue and anchors the low-cost, high-volume tier. NVIDIA reported $2.349b FY2026 automotive revenue, while Qualcomm reported $3.957b FY2025 automotive revenue, but both totals include material software, systems, digital-cockpit, connectivity or other content outside the contract. Only the assessed driving-AI SoC portions are included here.

The bottom-up check is approximately 93m new light vehicles, 47% carrying an included AI SoC, and $126 vendor revenue per equipped vehicle across low-cost and high-performance mixes, yielding $5.5b. The 93m denominator is consistent with OICA's recent world motor-vehicle production totals, while the adoption level is inferred from Counterpoint's published 2035 Level 2-and-above trajectory and Mobileye's disclosed shipment scale. The estimate is more reliable as an order of magnitude than as a precise market census because bundled-system allocation and Chinese supplier disclosure remain weak.

## Adoption Path

The expected 2036 market is **$21b**, with a plausible **$12b-$34b** range. Counterpoint expects global Level 2-and-above penetration to reach 84% in 2035 and related volume to grow at an 8% CAGR. The reference bridge assumes about 105m new light vehicles in 2036, 86% with an included AI SoC, and $232 vendor revenue per equipped vehicle. The content increase reflects migration from single front-camera processors toward multi-sensor fusion, redundancy and central compute; nominal inflation and richer mix outweigh learning-driven price declines for equivalent compute.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Addressable new light vehicles | ~93m | ~105m | Mature global production, about 1.2% annual growth |
| Included AI-SoC new-sales penetration | ~47% | ~86% | L1/L2 plus expanding L2+/L3; near Counterpoint's 84% L2+ view for 2035 |
| Adopted vehicle flow | ~44m | ~90m | Addressable flow multiplied by penetration |
| Billable activity | ~48m SoC-equivalents | ~113m SoC-equivalents | Some vehicles carry multiple safety/central-compute processors |
| Net vendor revenue per adopted vehicle | ~$126 | ~$232 | Rising compute, memory-interface and software value, nominal USD |
| Annual market value | **$5.5b** | **$21.0b** | Vendor-recognized included revenue, rounded expected value |

The implied 10-year CAGR is 14.3%. This is a new-sales flow market, so there is no installed-base replacement calculation: each year's billable activity is that year's vehicle production and included SoC count. Standalone recurring cloud, mapping and autonomy-service revenue is excluded; inseparable per-vehicle licences are included once. The main sensitivities are the pace of L2+/L3 adoption, compute centralization, the number of included SoCs per vehicle, real silicon price per unit of performance, Chinese localization and OEM captive designs.

No logistic penetration block is configured because the library has only one `new-sales-share` automotive analog and no consistent global historical series on this contract. The disclosed adoption path is therefore a direct industry-forecast and bottom-up sizing judgment, not a fitted curve.

## Market Structure

Direct network effects are low: one OEM's choice does not by itself improve another OEM's chip. Data can improve the driving stack, but OEMs frequently control fleet data and the benefit often accrues to software rather than the merchant SoC alone. Scale economies are strong because advanced-node design, verification, toolchains, safety cases and OEM support carry large fixed costs. Brand and qualification reputation matter in safety-critical sourcing. Functional-safety, reliability and cybersecurity requirements slow entry without legally capping vendor count. Switching costs are high because an OEM platform award entails years of hardware, software, sensor and validation integration; that protects several designed-in incumbents rather than guaranteeing one global winner.

The direct data-scale score remains below high confidence because supplier/OEM data rights and measured learning returns are not disclosed consistently; confidence would improve with contract-level data-rights disclosure or audited closed-loop performance evidence. Brand/reputation confidence is also below 0.8 because OEM win/loss and safety-qualification comparisons are private; this is irreducible for now and should be revisited as 2027-2029 platform awards and production launches reveal switching outcomes.

The unadjusted structural model gives a 22.84% horizon leader and 0.7765 rank decay, roughly 73% across the first five geometric ranks. The documented override uses Counterpoint's boundary-near projection that Mobileye, NVIDIA, Qualcomm, Horizon Robotics and Huawei together reach 78% share in 2035, up from 69% in 2025. A 28% leader and 0.70 rank decay reproduce 77.7% top-five share and raise projected HHI modestly to **0.1537** (about 1,537 on the conventional 10,000-point scale, or 6.5 effective competitors). This is a moderately concentrated market rather than winner-take-all. The remainder accommodates Renesas, NXP, Ambarella, Texas Instruments, Black Sesame, regional suppliers, OEM-sponsored designs and new entrants.

## Players

Current whole-market revenue shares are analyst estimates: Mobileye 31%, NVIDIA 16%, Qualcomm 10%, Horizon Robotics 7% and Huawei 5%, totaling Counterpoint's published 69% top-five aggregate. Mobileye is the strongest direct anchor: 91% of its $1.894b 2025 revenue equals about $1.72b, or 31% of the $5.5b pool. NVIDIA and Qualcomm shares remove broad out-of-contract content from their reported automotive revenue; Horizon and Huawei are the least certain because boundary-matched revenue is not public. These estimates should not be mistaken for Counterpoint's unpublished individual share table.

Mobileye can defend high-volume front-camera ADAS through cost efficiency, a 230m-plus vehicle installed history and OEM integration, but can lose as high-compute central architectures and OEM in-sourcing expand. NVIDIA can win premium central compute through its programmable AI stack and DRIVE platform but can lose on cost, power, supply or OEM desire for control. Qualcomm can cross-sell Snapdragon Ride beside its cockpit/connectivity footprint but must prove safety-driving deployment at scale. Horizon and Huawei benefit from Chinese localization, local OEM ties and protected supply chains; both face geographic limits, while export controls and OEM captive programs can reshape the field.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| Mobileye (MBLY) | 28.00% | **21.56%** | **$4.53b** |
| NVIDIA (NVDA) | 19.60% | **15.80%** | **$3.32b** |
| Qualcomm (QCOM) | 13.72% | **11.42%** | **$2.40b** |
| Horizon Robotics (9660.HK) | 9.60% | **8.39%** | **$1.76b** |
| Huawei | 6.72% | **6.48%** | **$1.36b** |

Mobility-adjusted capture is lower than holding today's rank for every incumbent because the pooled model allows churn, entry from outside today's top five, the competitive fringe and a **10.06% gone probability** already embedded in each estimate. The five adjusted captures total 63.6%; the gap to the 77.7% abstract top-five concentration is mainly the chance that future top ranks are occupied by outside contenders. The model sees current rank and share spacing but not company momentum, platform awards, geopolitics, software quality or management; no company-specific player override is used.

## Watch

- Boundary-matched AI-driving SoC revenue or unit/ASP disclosure from NVIDIA, Qualcomm, Horizon Robotics and Huawei.
- Counterpoint's next Global Autonomous Vehicle SoCs forecast, especially individual shares and whether the 78% top-five view holds.
- Mobileye EyeQ shipment volume, average system price, SuperVision/Chauffeur mix and the transition from EyeQ5 to EyeQ6.
- 2027-2029 OEM platform awards and production launches, which will firm up brand and switching-cost assumptions.
- Supplier/OEM disclosures on fleet-data ownership and measurable closed-loop learning returns, which will firm up the data-scale score.
- L2+/L3 regulatory approvals, liability changes and real-world safety evidence by region.
- Chinese localization, U.S. export controls, advanced-node foundry access and OEM captive silicon.
- Central-compute consolidation: included SoCs per vehicle versus integration into broader vehicle processors.

## Peer Comparison

Peer benchmarks are recorded after the primary estimate and do not change it. QYResearch's automotive AI chipset forecast is narrower or differently classified: $1.453b in 2024 and $6.854b in 2030. Our smooth reference path reaches about $9.4b in 2030, so QYResearch is **27% below our estimate** for that year; incomplete public boundary detail and an unusual vendor list make this a low-quality comparison. Grand View Research's broader automotive AI market is $6.4b in 2026 and $14.9b in 2030, **59% above our 2030 estimate**, but it includes software and services beyond SoCs and is therefore not directly comparable.

Counterpoint's October 2025 forecast is the strongest scope-near benchmark. It expects 84% global Level 2-and-above penetration in 2035 and the top five ADAS/AV SoC suppliers to hold 78% combined share. Our path is about 84%-85% penetrated in 2035 and the concentration override gives 77.7% to the top five at the fixed 2036 horizon: effectively aligned after the one-year horizon mismatch. Counterpoint does not publish market revenue in the accessible summary, so it benchmarks adoption and concentration rather than the $21b value.

## Sources

- Mobileye Global, 2025 Form 10-K filed 12 February 2026, especially $1.894b revenue, 91% EyeQ revenue share, 35.7m systems shipped, 230m-plus cumulative vehicle deployments and 50-plus OEM relationships: https://www.sec.gov/Archives/edgar/data/1910139/000110465926014300/mbly-20251227x10k.htm
- NVIDIA, FY2026 Form 10-K filed 25 February 2026, especially $2.349b automotive revenue, 39% annual growth, DRIVE platform, software ecosystem and fabless manufacturing: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- Qualcomm, FY2025 Form 10-K filed 5 November 2025, especially $3.957b QCT automotive revenue and the disclosed importance of Snapdragon digital-cockpit launches: https://www.sec.gov/Archives/edgar/data/804328/000080432825000085/qcom-20250928.htm
- Counterpoint Research, "Global Shifts in ADAS and Autonomous Vehicles to Reshape Competitive SoC Suppliers Landscape by 2035," 16 October 2025: https://counterpointresearch.com/en/insights/Global-Shifts-in-ADAS-and-Autonomous-Vehicles
- OICA, Production Statistics, 2024 world motor-vehicle production dataset and 2026 Q1 update, accessed 3 August 2026: https://oica.net/production-statistics/
- QYResearch, "Global Automotive AI Chipset Market Insights, Forecast to 2030," published 2024, reporting $1.453b in 2024 and $6.854b in 2030: https://www.qyresearch.com/reports/2410111/automotive-ai-chipset
- Grand View Research, "Automotive Artificial Intelligence Market," accessed 3 August 2026, reporting $6.4b in 2026 and $14.9b in 2030 for a broader boundary: https://www.grandviewresearch.com/industry-analysis/automotive-artificial-intelligence-market-report
- ISO, ISO 26262 road-vehicle functional-safety standard overview, accessed 3 August 2026: https://www.iso.org/standard/68383.html
