---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 1.8
  maturity-market-value: 18.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.45, confidence: 0.60}
      data-scale-advantage: {score: 0.40, confidence: 0.55}
      brand-reputation: {score: 0.70, confidence: 0.65}
      capital-intensity: {score: 0.90, confidence: 0.80}
      scale-economies: {score: 0.75, confidence: 0.70}
      regulatory-barriers: {score: 0.45, confidence: 0.65}
      switching-costs: {score: 0.65, confidence: 0.60}
  override:
    s1: 0.18
    r: 0.75
    reason: "The pooled trait model predicts a 42.8% leader and more than 100% modeled share, contradicting the boundary-matched 9% current leader, multi-modality competition and large software/services tail; an 18% leader preserves expected consolidation without a hard-oligopoly artifact."
  model-estimate:
    s1: 0.428001
    r: 0.598694
  hhi: 0.074057
  method: selected-direct-ridge
  date: 2026-08-09
players:
  inputs:
    current:
      - rank: 1
        name: IonQ
        ticker: IONQ
        share: 0.09
      - rank: 2
        name: IBM Quantum
        ticker: IBM
        share: 0.07
      - rank: 3
        name: Quantinuum
        share: 0.05
      - rank: 4
        name: D-Wave Quantum
        ticker: QBTS
        share: 0.018
  model-estimate:
    - rank: 1
      name: IonQ
      ticker: IONQ
      hold-position-capture: 0.18
      mobility-adjusted-capture: 0.135089
      mobility-adjusted-revenue: 2.431602
    - rank: 2
      name: IBM Quantum
      ticker: IBM
      hold-position-capture: 0.135
      mobility-adjusted-capture: 0.107544
      mobility-adjusted-revenue: 1.935792
    - rank: 3
      name: Quantinuum
      hold-position-capture: 0.10125
      mobility-adjusted-capture: 0.084919
      mobility-adjusted-revenue: 1.528542
    - rank: 4
      name: D-Wave Quantum
      ticker: QBTS
      hold-position-capture: 0.075937
      mobility-adjusted-capture: 0.07076
      mobility-adjusted-revenue: 1.27368
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-09
---
# Global Quantum Computing Systems

## Market Definition

**Market scope:** worldwide commercial quantum-computing systems and the product layers required to use them. Included are gate-model and annealing quantum computers sold for on-premises or cloud-service-provider deployment; paid cloud access to quantum processing capacity; quantum-specific control, middleware, development and application software; and vendor support and professional services attached to deploying or using an included system. Quantum sensing, quantum communications and networking sold without compute access, post-quantum cybersecurity, general classical high-performance computing, venture funding, government research grants and the downstream economic value of quantum-enabled discoveries are excluded. Classical simulation is included only when it is sold as part of a quantum development or hybrid-compute product, not as general HPC.

**Revenue boundary:** annual revenue recognized by the first-party quantum system, software or access vendor, including equipment delivered to a cloud provider and the provider's separately recognized quantum-access revenue. Channel pass-through is counted once. Customer R&D budgets, capital committed but not recognized as revenue, cloud gross transaction value and the value of end-user outcomes are not market revenue.

**Addressable unit and penetration:** the stable addressable unit is an enterprise, government or research compute program with a structurally eligible scientific, simulation, optimization or sampling workload and the talent and budget to evaluate quantum computation. Penetration is `spend-share`: included vendor revenue as a share of annual spending on those eligible advanced-compute workloads. Billable units are delivered quantum systems and upgrades, annual quantum processor capacity or job-hours, software subscriptions and licences, and attached service-years. On-premises hardware, CSP-enabling hardware, paid cloud access, software and attached services are modeled separately and aggregated at the same vendor-revenue boundary.

**Time and value basis:** 2026 base year, fixed 2036 horizon, nominal USD at approximately constant current exchange rates. The same scope and revenue boundary apply to size, concentration and player capture.

## Current View

The expected 2026 market value is **$1.8b**, with a rough **$1.4b-$2.4b** range. QED-C and Hyperion Research provide the best attributable boundary-near anchor: their April 2026 industry study puts 2025 quantum-computing revenue at **$1.4b** and projects more than **$3b in 2028**, versus $1.07b in 2024. Applying the reported roughly 30% near-term growth to the 2025 observation gives $1.82b in 2026, rounded to $1.8b.

Public-company revenue is a useful lower-level check. IonQ reported $130.0m of 2025 GAAP revenue, D-Wave $24.6m, Rigetti $7.1m and Quantum Computing Inc. $0.7m. Together they account for only about 12% of QED-C's 2025 total, leaving room for IBM, Quantinuum, QuEra, cloud providers, private hardware and software companies, and product-attached services. Funding is not confused with revenue: QED-C separately reports $4.9b of 2025 venture capital and $12.7b of new government commitments.

The estimate is moderate-confidence. QED-C surveys more than 100 industry participants and is much closer to the contract than generic market reports, but the precise treatment of internal cloud-provider revenue, component suppliers and consulting is not fully public. Revenue is also lumpy: a small number of on-premises system deliveries can move a year's total materially.

## Adoption Path

The expected 2036 market is **$18b**, with a plausible **$7b-$40b** range. The reference path reaches QED-C's greater-than-$3b 2028 forecast, then slows from roughly 30% to about 25% annual growth as paid deployments broaden but hardware performance, error correction, specialist supply chains and customer proof-of-value remain constraints. The full-period 2026-2036 CAGR is 25.9%.

| Revenue stream | 2026 | 2036 | Bridge |
| --- | ---: | ---: | --- |
| On-premises and CSP-enabling systems | ~$0.70b | ~$6.3b | More sovereign, national-lab and enterprise installations; larger modular fault-tolerant systems; upgrades and replacement |
| Cloud access, middleware and applications | ~$0.85b | ~$9.0b | More paid workloads, hybrid orchestration, developer tooling and application software as useful compute emerges |
| Attached support and professional services | ~$0.25b | ~$2.7b | Deployment, calibration, algorithm enablement, maintenance and training tied to the installed base |
| Annual market value | **$1.8b** | **$18.0b** | Vendor-recognized revenue, rounded expected value |

The durable-system check includes both new installations and replacement or upgrade demand. Current systems turn over rapidly because processor, control and cryogenic designs are evolving; by 2036, a larger installed base creates recurring upgrades and service, while new capacity remains the larger hardware driver. Equipment pricing should not fall like ordinary compute cost per operation: learning and modularity reduce same-capability cost, but usable logical-qubit count, error-correction overhead, control complexity and system scope expand the product sold. Cloud and software revenue is expected to outgrow hardware after useful workloads become repeatable.

No logistic penetration block is configured. There is no consistent historical series for the contract's spend-share denominator, and qubit counts or cloud users are not interchangeable with paid workload adoption. The sizing bridge therefore states its adoption and revenue-mix judgments directly instead of fitting a spurious curve.

The downside assumes useful commercial advantage remains confined to narrow research tasks through the early 2030s, public procurement cools and classical AI/HPC captures most experimental budgets. The upside assumes fault-tolerant systems arrive near leading roadmaps, useful chemistry and materials workloads become repeatable, and cloud distribution converts experimentation into recurring application revenue. The biggest sensitivities are time to economically useful logical computation, system price and utilization, government-funded on-premises purchases, and how much application value accrues to quantum vendors rather than classical cloud and consulting providers.

## Market Structure

Network effects are moderate rather than dominant. Larger developer communities, libraries and cloud distribution make a platform easier to use, but customers can access several hardware modalities and open-source software reduces lock-in. Calibration, compiler and workload data can improve systems, although much of the highest-value application data stays with customers. Brand and technical reputation matter because buyers cannot fully verify roadmap credibility or system reliability before committing.

Capital intensity and scale economies are high. Competitive systems require scarce quantum talent, custom fabrication or trapped-ion hardware, cryogenics, control electronics, packaging, error-correction research and long validation cycles. IBM's roadmap illustrates the integration burden: it targets a 200-logical-qubit, 100-million-gate fault-tolerant system in 2029. Google's Willow work shows below-threshold error correction but also emphasizes that its strongest benchmark did not yet have a practical commercial application. These mechanisms favour a finite set of well-funded architectures, while scientific uncertainty and modality differentiation prevent a single universal design from being assumed.

Regulation is a meaningful but incomplete barrier through export controls, national-security procurement and sovereignty requirements. Switching costs are moderate-to-high once a customer builds workflows around a specific SDK, error model and hardware topology, yet hybrid frameworks and cloud marketplaces permit multi-homing. The unadjusted structural model predicts a 42.8% horizon leader and a geometric curve whose modeled shares exceed 100%. That hard-oligopoly result contradicts the boundary-matched 9% current leader, multiple viable hardware modalities and the contract's large software and services tail. The documented override uses an 18% leader and 0.75 rank decay, producing **HHI 0.0741** (about 13.5 effective competitors): a moderately concentrated top tier after expected consolidation, with a valid long tail rather than a near-dominant vendor. Consolidation, failure of weaker architectures and vertical integration by hyperscalers could raise HHI; interoperable software and enduring modality-specific niches could lower it.

## Players

Current shares are analyst estimates on the whole contract. IonQ is ranked first at 9% because its audited $130.0m 2025 revenue equals 9.3% of QED-C's $1.4b market, although acquisitions mean not every future IonQ dollar will remain inside the compute-only boundary. IBM Quantum at 7% and Quantinuum at 5% are estimated because neither parent discloses boundary-matched quantum-computing revenue. Their rank is supported by broad hardware, software, cloud and enterprise footprints, not a published market-share table. D-Wave's audited $24.6m equals 1.8% of the 2025 market and anchors rank four. The remaining 77% includes QuEra, Google, Microsoft/Azure, Amazon Braket, Rigetti, Pasqal, PsiQuantum, Alice & Bob, Xanadu, Quantum Machines and a large software and services tail.

IonQ can win through improving trapped-ion fidelity, system sales, cloud distribution and an increasingly integrated compute stack; it can lose if acquisition-led revenue drifts outside the contract, scale-up slips or another modality reaches useful fault tolerance first. IBM can win through Qiskit, enterprise relationships, semiconductor and systems integration and its stated Starling roadmap; it can lose if the roadmap misses or customers prefer vendor-neutral cloud access. Quantinuum combines trapped-ion hardware with a broad software stack and Honeywell backing, but must convert technical performance and partnerships into separately visible commercial scale. D-Wave owns a differentiated annealing installed base and on-premises sales motion; it can lose if customers standardize on universal gate-model systems or optimization workloads remain classically competitive.

| Current player | Hold-position capture | Mobility-adjusted capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: |
| IonQ (IONQ) | 18.00% | **13.51%** | **$2.43b** |
| IBM Quantum (IBM) | 13.50% | **10.75%** | **$1.94b** |
| Quantinuum | 10.13% | **8.49%** | **$1.53b** |
| D-Wave Quantum (QBTS) | 7.59% | **7.08%** | **$1.27b** |

The pooled rank-mobility model is used as a base rate only. It sees current rank and share spacing but not architecture quality, fault-tolerance milestones, balance sheets, national procurement or company strategy. Mobility reduces the combined expected capture of the four named incumbents from 49.1% on a hold-position basis to 39.8%, allowing for outside winners, fringe positions and a pooled **10.06% gone probability** already embedded in each adjusted capture. No company-specific override is used.

## Watch

- QED-C/Hyperion annual revenue, segment-mix and on-premises-versus-cloud updates on a consistent boundary.
- Independent demonstrations of commercially useful advantage, not benchmark speed alone, and the cost per useful result versus classical HPC/AI.
- IBM's 2026-2029 error-correction and Starling milestones; comparable logical-qubit and logical-gate progress from Google, Quantinuum, IonQ, QuEra and others.
- On-premises system deliveries, recognized revenue and backlog conversion at IonQ, D-Wave, Rigetti, QuEra and private peers.
- Quantum cloud utilization, pricing, repeat workloads and the split of economics between hardware vendors, hyperscalers and application software.
- Export controls, sovereign procurement and supply constraints in cryogenics, lasers, photonics, control electronics and specialist fabrication.
- Consolidation, architecture abandonment and whether open software preserves multi-homing as hardware becomes more capable.

## Peer Comparison

QED-C/Hyperion's boundary-near forecast is **approximately 0% over/under our estimate in 2028**: it projects the quantum-computing market from $1.4b in 2025 to **more than $3b in 2028** at about 30% annual growth, while our path is approximately $3.0b. It is the strongest peer because it measures supplier-market revenue and is based on a broad global participant survey, although its detailed inclusion rules are not fully public.

McKinsey's 2025 Quantum Technology Monitor estimates quantum-computing revenue at **$4b in 2024** and up to **$72b in 2035**. Its 2035 upper figure is about **400% above our interpolated $14.4b**, but the arithmetic is not directly comparable: McKinsey's starting value is already 274% above QED-C's $1.07b 2024 supplier-market estimate, indicating a materially broader revenue definition and the $72b figure is an upper case. It is useful as evidence of upside if fault-tolerant utility and application revenue arrive quickly, not as a boundary-matched base case.

The wide peer spread is the central finding. Near-term supplier revenue can be anchored reasonably; long-term forecasts mainly encode different assumptions about practical advantage, included software and services, and whether economic value or vendor revenue is being measured. The stored $18b expected value stays close to QED-C through 2028 and retains substantial but not upper-case commercialization thereafter.

## Sources

- QED-C, *State of the Global Quantum Industry 2026*, published April 2026; 2025 quantum-computing market of $1.4b and more than $3b forecast for 2028: https://quantumconsortium.org/publication/2026-state-of-the-global-quantum-industry-report/
- QED-C and Hyperion Research, *5th Annual Global QC Market Survey*, April 2025; $1.07b 2024 market, $2.206b 2027 forecast, segment mix and survey methodology: https://hyperionresearch.com/wp-content/uploads/2025/04/QED-C_Hyperion-Research_R-Sorensen_Global-Q-Computer-Market-Status-and-Prospects-April-2025.pdf
- QED-C, *2025 Market Forecast: Quantum Computing*; 2024 market value and global survey basis: https://quantumconsortium.org/publication/2025-market-forecast-quantum-computing/
- McKinsey & Company, *Quantum Technology Monitor 2025*, June 2025; $4b 2024 quantum-computing revenue and up to $72b in 2035: https://www.mckinsey.com/~/media/mckinsey/business%20functions/mckinsey%20digital/our%20insights/the%20year%20of%20quantum%20from%20concept%20to%20reality%20in%202025/quantum-monitor-2025.pdf
- IonQ, FY2025 Form 10-K filed 25 February 2026; $130.016m revenue: https://www.sec.gov/Archives/edgar/data/1824920/000119312526071562/
- D-Wave Quantum, FY2025 Form 10-K filed 26 February 2026; $24.587m revenue: https://www.sec.gov/Archives/edgar/data/1907982/000190798226000026/
- Rigetti Computing, FY2025 Form 10-K filed 4 March 2026; $7.088m revenue: https://www.sec.gov/Archives/edgar/data/1838359/000110465926023454/
- Quantum Computing Inc., FY2025 Form 10-K filed 2 March 2026; $0.682m revenue: https://www.sec.gov/Archives/edgar/data/1758009/000121390026022417/
- IBM, "IBM lays out clear path to fault-tolerant quantum computing," June 2025; Starling roadmap and system-integration requirements: https://www.ibm.com/quantum/blog/large-scale-ftqc
- Google Quantum AI, "Meet Willow, our state-of-the-art quantum chip," December 2024, updated June 2025; below-threshold error correction and limits of current benchmark utility: https://blog.google/technology/research/google-willow-quantum-chip/
