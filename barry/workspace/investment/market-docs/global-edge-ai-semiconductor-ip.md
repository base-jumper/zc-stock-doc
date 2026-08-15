---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.12
  maturity-market-value: 1.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.45, confidence: 0.55}
      data-scale-advantage: {score: 0.30, confidence: 0.45}
      brand-reputation: {score: 0.65, confidence: 0.60}
      capital-intensity: {score: 0.35, confidence: 0.60}
      scale-economies: {score: 0.75, confidence: 0.65}
      regulatory-barriers: {score: 0.25, confidence: 0.55}
      switching-costs: {score: 0.80, confidence: 0.70}
  override:
    s1: 0.22
    r: 0.65
    reason: "The direct-ridge output implied a 37.4% leader and an invalid 108.3% modeled share mass; boundary-specific evidence instead shows multiple scaled IP ecosystems, internal and open-source substitution, and a large specialist fringe."
  model-estimate:
    s1: 0.373635
    r: 0.654894
  hhi: 0.08381
  method: selected-direct-ridge
  date: 2026-08-03
players:
  inputs:
    current:
      - rank: 1
        name: Ceva
        ticker: CEVA
        share: 0.18
      - rank: 2
        name: Arm
        ticker: ARM
        share: 0.16
      - rank: 3
        name: Cadence
        ticker: CDNS
        share: 0.13
      - rank: 4
        name: VeriSilicon
        ticker: 688521.SS
        share: 0.11
      - rank: 5
        name: GlobalFoundries / MIPS
        ticker: GFS
        share: 0.09
  model-estimate:
    - rank: 1
      name: Ceva
      ticker: CEVA
      hold-position-capture: 0.22
      mobility-adjusted-capture: 0.14968
      mobility-adjusted-revenue: 0.14968
    - rank: 2
      name: Arm
      ticker: ARM
      hold-position-capture: 0.143
      mobility-adjusted-capture: 0.107361
      mobility-adjusted-revenue: 0.107361
    - rank: 3
      name: Cadence
      ticker: CDNS
      hold-position-capture: 0.09295
      mobility-adjusted-capture: 0.076255
      mobility-adjusted-revenue: 0.076255
    - rank: 4
      name: VeriSilicon
      ticker: 688521.SS
      hold-position-capture: 0.060417
      mobility-adjusted-capture: 0.054823
      mobility-adjusted-revenue: 0.054823
    - rank: 5
      name: GlobalFoundries / MIPS
      ticker: GFS
      hold-position-capture: 0.039271
      mobility-adjusted-capture: 0.040405
      mobility-adjusted-revenue: 0.040405
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-03
---
# Global Edge-AI Semiconductor IP

## Market Definition

**Market scope:** worldwide third-party licensable semiconductor intellectual property whose primary function is accelerating AI inference inside edge-device SoCs. Included products are NPU, neural-processor, neuromorphic-accelerator and AI-optimized DSP cores, their required compiler/runtime IP, up-front licences, customization/NRE tied to those cores, and production royalties. Edge devices include MCUs, consumer and IoT devices, PCs, vehicles, industrial systems, robotics and other locally inferencing equipment. Finished chips and devices, cloud/data-centre accelerator IP, general CPU/GPU/DSP IP without an AI-specific core or licence, EDA tools, stand-alone AI software, customer silicon value and internally developed accelerators are excluded.

**Revenue boundary:** annual revenue recognized by the third-party AI-accelerator IP vendor for licences, related integration/NRE and production royalties. It is not the value of the host processor, the finished edge device, customer AI spend, or an imputed value for internally developed NPUs.

**Addressable unit and penetration:** the stable denominator is the annual flow of edge-device SoC designs that could structurally include dedicated local-inference acceleration. Penetration is `new-sales-share`: the share of eligible new SoC designs using externally licensed AI-specific accelerator IP. Billable units are licence/customization engagements and royalty-bearing SoC shipments. Consumer/IoT, automotive/industrial, and PC/high-compute edge are separate economic segments but aggregate at the same vendor-recognized revenue boundary.

**Time and value basis:** base year 2026, fixed horizon 2036, worldwide geography and nominal USD. The contract is unchanged across size, concentration and player capture. Open-source cores are excluded from licence revenue but included where a vendor recognizes boundary-matched implementation, support or royalty revenue.

## Current View

The 2026 market is estimated at **US$0.12b**. CEVA provides the cleanest public anchor: it reported US$63.6m of 2025 licensing revenue, said AI contributed more than 20%, and signed 10 NeuPro NPU agreements. That establishes an AI-licensing floor above US$12.7m before any AI-related royalties. In Q1 2026, AI again exceeded 20% of US$17.8m licensing revenue, while CEVA identified production deployment in Renesas's R-Car V4H automotive platform. Grossing an estimated US$20-25m of CEVA AI-specific licensing and royalty revenue at an 18% whole-market share implies roughly US$0.11-0.14b, supporting the rounded US$0.12b central estimate.

This triangulation is low confidence. Arm, Cadence, VeriSilicon and the former Synopsys ARC/NPX business now owned by GlobalFoundries do not disclose dedicated edge-AI-IP revenue; licences are lumpy and frequently bundled with CPU, DSP, interface, tools or custom-silicon work. The estimate deliberately excludes the far larger value of processors and devices containing these cores.

## Adoption Path

The expected 2036 market is **US$1.0b**, a 23.6% ten-year CAGR. The bridge assumes dedicated local inference becomes standard across a much larger share of eligible SoC designs, that externally licensed cores retain a meaningful role beside internal designs and open source, and that the revenue mix shifts from licence/NRE toward recurring per-chip royalties as 2025-26 design wins reach production. The growth rate is consistent with published broad edge-AI processor forecasts near the low-to-mid-20% range and is below Market.us's 34.7% edge-AI-IC forecast, reflecting internal NPU development, price pressure and open-source substitution at the narrower licensor boundary.

| Driver | 2026 | 2036 | Basis |
|---|---:|---:|---|
| Eligible edge-AI processor/device revenue | about US$25-35b | about US$150-220b | Broad chip-value bridge; not the stored market boundary |
| Externally monetized AI-IP revenue intensity | about 0.3-0.5% | about 0.4-0.7% | Licence/NRE plus production royalties divided by host-chip value |
| Third-party edge-AI semiconductor-IP market | US$0.12b | US$1.0b | Vendor-recognized revenue, reconciled to front matter |
| Implied CAGR | — | 23.6% | Fixed 2026-36 horizon |

The downside is roughly US$0.45b if leading device and semiconductor companies internalize NPUs, open-source Coral-class cores compress licence economics, and royalty ramps remain slow. The reference case is US$1.0b as licensed NPU/DSP IP spreads from evaluation into volume MCU, automotive, PC and consumer platforms. The upside is about US$1.8b if heterogeneous edge AI becomes standard across most eligible SoCs and third-party software/toolchain leverage raises licensor content per design. The stored value is a rounded probability-weighted expectation. There is no installed-base replacement calculation because the contract measures a flow of new SoC designs and royalty-bearing chip shipments.

## Market Structure

Compiler/runtime compatibility, model support and developer familiarity create moderate indirect network effects, but customers can port models through ONNX, TensorFlow Lite and other common layers. Centralized training-data advantage is weak because licensors generally do not own customer inference data. Reputation matters for tape-out risk, functional safety and long product cycles; R&D and verification scale strongly across customers even though licensees bear fabrication capital. Automotive safety requirements raise barriers in some segments but not across the whole market. The dominant mechanism is switching cost: replacing an accelerator after architecture selection can require model re-optimization, compiler work, software validation and a new silicon design cycle.

Those mechanisms favour several scaled ecosystems rather than a single standard. The direct-ridge model predicted a 37.4% leader and a geometric share mass of 108.3%, outside the model's valid fringe regime and inconsistent with the boundary-specific evidence. The complete override sets a 22% horizon leader and 0.65 rank decay, leaving about 37% for the long specialist fringe. The script derives a **0.08381 HHI**, equivalent to roughly 11.9 effective competitors and a fragmented-to-moderately-concentrated revenue pool. Concentration could rise if one compiler/runtime becomes the de facto cross-device deployment target or if CPU-plus-NPU platform bundling wins broadly. It would fall if open-source NPU IP, RISC-V modularity, customer-owned accelerators and domain-specific specialists keep design wins dispersed.

## Players

No boundary-matched market-share table was found. Current shares are therefore analyst estimates based on dedicated product breadth, disclosed licensing momentum, customer/production evidence and overall processor-IP reach: CEVA 18%, Arm 16%, Cadence 13%, VeriSilicon 11%, and GlobalFoundries/MIPS 9%, leaving 33% for Quadric, Imagination, Expedera, BrainChip, Synaptics/Google Coral implementation activity and other specialists. The ranking is the weakest model input and must not be read as a published league table.

CEVA has the best current public evidence: 10 NeuPro NPU agreements in 2025, more than 20% of annual licensing revenue from AI, named adoption by Microchip, ALi and Nextchip, and six NPU customers expected to have silicon back by end-2026. Arm brings the third-generation Ethos-U85 and a large CPU/software ecosystem. Cadence's Neo NPU spans 8 GOPS to 80 TOPS per core with a common NeuroWeave SDK. VeriSilicon combines established Vivante NPU deployment with the open-source Coral NPU collaboration announced with Google in 2025. GlobalFoundries completed its acquisition of Synopsys's ARC processor-IP business in June 2026, combining ARC AI cores with MIPS and a reported ecosystem of more than 300 processor-IP customers.

Quadric is the most visible outside contender: it raised a US$30m Series C in January 2026 after reported design wins across edge LLM, automotive and enterprise applications, and Kyocera licensed its Chimera GPNPU IP in 2025. BrainChip is differentiated in ultra-low-power neuromorphic inference but FY2025 revenue of US$1.89m, including non-IP product and service revenue, remains too small for the current top five. Company-specific momentum is not embedded in the pooled mobility model and no player override is used.

At the 2036 concentration curve, hold-position capture is 22.0% for rank one, 14.3% for rank two, 9.30% for rank three, 6.04% for rank four and 3.93% for rank five. The pooled mobility model lowers CEVA to **14.97%** expected capture (US$149.7m), Arm to **10.74%** (US$107.4m), Cadence to **7.63%** (US$76.3m), and VeriSilicon to **5.48%** (US$54.8m); GlobalFoundries/MIPS rises slightly to **4.04%** (US$40.4m) because lower current ranks can move up as well as down. The 10.06% gone probability is already included. These are coarse base rates, not company-specific forecasts, and the wide fringe preserves room for current specialists and new entrants.

## Watch

- CEVA's six expected 2026 NPU silicon returns, then first separately attributable AI royalty ramps.
- Production adoption and disclosed customers for Arm Ethos-U85, Cadence Neo and the ARC/NPX portfolio under GlobalFoundries/MIPS.
- Whether Google's open-source Coral NPU expands the licensable pool through implementation/support or destroys licence value.
- Quadric, Expedera and BrainChip design wins converting into named high-volume royalty programs.
- External-versus-internal NPU share in MCU, automotive, PC, consumer and robotics SoCs.
- A boundary-matched IPnest, Omdia or company disclosure separating AI-specific processor-IP revenue and shares.

## Peer Comparison

**Not comparable — about 51,900% above our 2034 estimate:** Market.us, published 17 March 2025, projects the global edge-AI-IC market from US$17.3b in 2024 to **US$340.2b in 2034**, a 34.7% CAGR. Our interpolated 2034 licensor-revenue estimate is US$0.654b. The arithmetic gap is not a forecast disagreement: Market.us measures finished CPU/GPU/ASIC/other IC revenue, including internally developed silicon, while this document measures third-party AI-specific IP licences, NRE and royalties. Its CAGR is 11.1 percentage points above ours and supports using a high-growth underlying chip pool while applying a narrow licensor conversion.

**Not comparable — about 32,600% above our 2028 estimate:** AI Business's 12 March 2024 report said the edge-AI-chip market could reach **US$60b by 2028**. Our interpolated 2028 IP-provider revenue is US$0.183b. This is again host-chip value rather than licensor revenue, so the percentage gap is boundary-mismatched; it is useful only as a ceiling and royalty-intensity check.

**Not comparable — broader IP product scope:** MarketsandMarkets' 22 June 2026 forecast puts the entire semiconductor-IP market at **US$18.64b in 2032**. Our interpolated edge-AI-specific IP estimate is US$0.428b in that year, or about 2.3% of the broader total. Both use licensor revenue, but the peer includes CPU, GPU, interface, memory, verification and other IP, so it is a scope ceiling rather than a direct peer forecast.

No independent 5-10 year forecast with the same narrow AI-specific third-party-IP revenue boundary was found. The stored US$1.0b estimate therefore remains low confidence and should be replaced or recalibrated when IPnest, Omdia or a participant publishes category revenue rather than host-chip value.

## Sources

- CEVA, “Ceva Highlights Breakthrough Year for AI Licensing and Physical AI Adoption in 2025,” accessed 3 August 2026: https://www.ceva-ip.com/press/ceva-highlights-breakthrough-year-for-ai-licensing-and-physical-ai-adoption-in-2025/
- CEVA, “Fourth Quarter and Full Year 2025 Financial Results,” 17 February 2026: https://www.ceva-ip.com/press/ceva-inc-announces-fourth-quarter-and-full-year-2025-financial-results/
- CEVA, “First Quarter 2026 Financial Results,” 11 May 2026: https://www.ceva-ip.com/press/ceva-inc-announces-first-quarter-2026-financial-results/
- Arm, Ethos-U85 product overview, accessed 3 August 2026: https://www.arm.com/products/silicon-ip-cpu/ethos/ethos-u85
- Cadence, Neo NPU product page and September 2023 release: https://www.cadence.com/en_US/home/tools/ip/ai-ip-platform/neo-npu.html and https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2023/cadence-accelerates-on-device-and-edge-ai-performance-and.html
- GlobalFoundries, “GlobalFoundries completes acquisition of Synopsys' Processor IP Solutions Business,” 2 June 2026: https://gf.com/news-and-events/news/globalfoundries-completes-acquisition-of-synopsys-processor-ip-solutions-business-delivering-a-holistic-technology-platform-for-physical-ai/
- Business Wire, “VeriSilicon and Google Jointly Launch Open-Source Coral NPU IP,” 12 November 2025: https://www.businesswire.com/news/home/20251112204217/en/
- PR Newswire, “Quadric, Inference Engine for On-Device AI Chips, Raises $30M Series C,” 14 January 2026: https://www.prnewswire.com/news-releases/quadric-inference-engine-for-on-device-ai-chips-raises-30m-series-c-as-design-wins-accelerate-across-edge-llms-automotive-and-enterprise-302660732.html
- BrainChip Holdings, FY2025 results and 2025 annual report, revenue context: https://investor.brainchip.com/
- Market.us, “Edge AI ICs Market Size, Share | CAGR of 34.7%,” 17 March 2025; broader chip-revenue boundary: https://market.us/report/edge-ai-ics-market/
- AI Business, “Edge AI Chip Market to Hit $60B by 2028 as Small Models, PCs Boost Demand,” 12 March 2024; broader chip-revenue boundary: https://aibusiness.com/edge-computing/edge-ai-chip-market-to-hit-60b-by-2028-as-small-models-pcs-boost-demand
- MarketsandMarkets, “Semiconductor Intellectual Property (IP) Market worth $18.64 billion by 2032,” 22 June 2026; broader semiconductor-IP boundary: https://www.marketsandmarkets.com/PressReleases/semiconductor-ip.asp
