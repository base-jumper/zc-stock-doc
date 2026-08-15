---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.52
  maturity-market-value: 2.9
penetration:
  inputs:
    target-series: data/global-long-read-sequencing/penetration.csv
    measure: spend-share
    ceiling: 0.35
    analogs: [us-ecommerce-retail-share, uk-online-retail-share]
    w-fit: 0.5
  model-estimate:
    L: 0.35
    t0: 2033.761221
    k: 0.137421
  method: logistic-blend
  date: 2026-08-08
concentration:
  inputs:
    traits:
      network-effects: {score: 0.15, confidence: 0.85}
      data-scale-advantage: {score: 0.55, confidence: 0.65}
      brand-reputation: {score: 0.75, confidence: 0.80}
      capital-intensity: {score: 0.65, confidence: 0.75}
      scale-economies: {score: 0.75, confidence: 0.75}
      regulatory-barriers: {score: 0.65, confidence: 0.75}
      switching-costs: {score: 0.55, confidence: 0.75}
  model-estimate:
    s1: 0.235416
    r: 0.755948
  hhi: 0.129324
  method: selected-direct-ridge
  date: 2026-08-08
players:
  inputs:
    current:
      - rank: 1
        name: Oxford Nanopore Technologies
        ticker: ONT.L
        share: 0.68
      - rank: 2
        name: PacBio
        ticker: PACB
        share: 0.31
  model-estimate:
    - rank: 1
      name: Oxford Nanopore Technologies
      ticker: ONT.L
      hold-position-capture: 0.235416
      mobility-adjusted-capture: 0.187987
      mobility-adjusted-revenue: 0.545162
    - rank: 2
      name: PacBio
      ticker: PACB
      hold-position-capture: 0.177962
      mobility-adjusted-capture: 0.157835
      mobility-adjusted-revenue: 0.457722
  gone-probability: 0.1006
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-08-08
---
# Global Long-Read Sequencing

## Market Definition

**Market scope:** worldwide sequencing platforms that routinely generate native DNA or RNA reads thousands of bases long, including nanopore and single-molecule real-time/HiFi systems. Included products are sequencers, flow cells or other consumables, sample-preparation kits sold by the platform vendor, platform software, maintenance and support. Research, clinical, biopharma, public-health, agricultural and industrial uses are included. Short-read-only systems, optical genome mapping, array products, proteomics, contract sequencing laboratories, bioinformatics consulting, downstream interpretation, licensing and collaboration payments, and total laboratory or healthcare episode spend are excluded.

**Revenue boundary:** annual net revenue recognized by long-read platform manufacturers for the included products and services. Distributor mark-ups, customer sequencing-service revenue, grants, license revenue and GMV are not counted. The **addressable unit** is one dollar of worldwide sequencing-platform vendor revenue that could structurally migrate from short-read-only workflows to long-read or hybrid workflows. **Penetration** is `spend-share`: long-read platform vendor revenue divided by all sequencing-platform vendor revenue on the same basis. **Billable units** are instruments, consumable runs or flow cells, vendor kits, software entitlements and service contracts. Research, applied/industrial, biopharma and clinical workflows are distinct adoption segments but are aggregated at vendor revenue; no service-lab revenue is added. The base year is 2026, the fixed horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

This narrow contract makes disclosed Oxford Nanopore and PacBio revenue usable as the current anchor. It is materially narrower than many published "long-read sequencing markets," which also count contract research, sequencing services and downstream analysis, and vastly narrower than company-defined molecular-analysis TAMs.

## Current View

The expected 2026 market value is **$0.52b**, with a rough **$0.47b-$0.60b** range. Oxford Nanopore is the largest contributor. It reported £116.5m of first-half revenue and expects underlying full-year constant-currency growth of roughly 16%-20% before additional collaboration and licensing opportunities. Applying the midpoint to 2025 revenue of £223.9m and translating at approximately $1.33/£ gives about **$0.35b** of included 2026 platform revenue. License and collaboration revenue is excluded by contract.

PacBio reported $76.2m of first-half revenue and on 5 August guided to **$155m-$165m** for 2026; the $160m midpoint is almost entirely HiFi long-read instruments, consumables and service after selling the Onso short-read assets. A roughly $10m allowance for MGI/BGI's early CycloneSEQ activity and other emerging platforms brings the expected total to $0.52b. This gives current whole-market shares of about 68% for Oxford Nanopore, 31% for PacBio and 1% for the residual field.

The independent denominator check is a roughly **$5.7b** 2026 sequencing-platform vendor pool. Illumina alone expects $4.5b-$4.6b of 2026 company revenue, although a small portion is arrays and SomaLogic rather than sequencing; MGI, Thermo Fisher's Ion Torrent franchise, Ultima and smaller vendors make up most of the balance. The resulting **9.1% long-read spend share** is plausible and is not confused with the fraction of samples or bases sequenced, which can differ sharply because prices and throughput vary.

## Adoption Path

The expected 2036 market value is **$2.9b**, with a broad **$1.5b-$5.5b** plausible range. The reference bridge grows the total sequencing-platform revenue pool from about $5.7b to **$14.4b** at roughly 9.7% nominal annual growth, while long-read spend share rises from about 9.0% to **20.17%**. The implied long-read CAGR is about **18.8%**.

| Driver | 2026 | 2036 | Basis |
| --- | ---: | ---: | --- |
| Addressable sequencing-platform revenue | ~$5.7b | ~$14.4b | Instruments, consumables, software and service; nominal USD |
| Long-read spend share | ~9.0% | 20.17% | Logistic spend-share path; long reads coexist with short reads |
| Long-read platform revenue | **$0.52b** | **$2.9b** | Addressable pool multiplied by adoption share; rounded |
| Instruments | ~$0.10b | ~$0.35b | Lower system prices and expanding placements; not the dominant horizon stream |
| Consumables, software and service | ~$0.42b | ~$2.55b | Installed-base utilization, clinical volume and recurring flow cells/reagents |

The penetration series reconstructs 2021-2026 long-read vendor revenue from Oxford Nanopore and PacBio disclosures and divides it by an analyst-estimated whole sequencing-platform pool anchored to Illumina and other suppliers. It is approximate, and the 2024 dip reflects PacBio's instrument transition rather than a reversal in scientific adoption. The asserted 35% ceiling recognizes that short reads should retain price- and throughput-sensitive RNA-seq, targeted panels, screening and many population-scale workflows; hybrid workflows can use both technologies without long reads taking all spend.

The model uses the two available `spend-share` analogs, U.S. and U.K. online retail, and caps target-fit weight at 0.5 because the latest observation is well below one-third of the ceiling and early supplier volatility should not dictate the mainstream curve. The fitted logistic parameters are **L 35%, midpoint 2033.76 and k 0.1374**; the evaluated path moves from 8.96% in 2026 to 20.17% in 2036. The analogs are imperfect: sequencing procurement has higher validation friction but faster technical cost decline. The curve is therefore a disciplined central path, not a claim that adoption mechanics match ecommerce.

The revenue archetype is an installed-base ecosystem. Instruments create placements, while flow cells, reagents, software and maintenance scale with active-system utilization; horizon revenue is expected to be dominated by recurring consumables and service. The model does not multiply installed systems by their sale price each year. The largest sensitivities are cost per accurate genome, clinical reimbursement and regulatory clearance, bioinformatics workflow maturity, research funding, export controls, and whether short-read incumbents successfully add native long-read capability.

## Market Structure

Direct network effects are weak. A sequencer does not produce better reads merely because more laboratories own it, although publication density, compatible protocols and analysis-tool support create a modest ecosystem effect. Data scale is more meaningful: proprietary run data improves basecalling, pore models, error correction and instrument control, but public reference datasets, academic methods and diminishing returns prevent a search-like feedback monopoly.

Brand and reputation matter because scientists and clinical laboratories validate accuracy, reproducibility and support before committing precious samples or regulated workflows. Capital requirements are substantial but below semiconductor-fab scale: credible entrants need years of chemistry, sensor, instrument, software and manufacturing investment plus global support. Scale economies are strong in flow-cell yield, reagent procurement, manufacturing learning, compute and spreading R&D over a recurring installed base. IP and regulated-clinical approvals slow entry; Oxford Nanopore's litigation with MGI illustrates the patent barrier, but research-use sequencing remains legally open and multiple chemistries are feasible.

Switching costs are moderate. Installed instruments, validated library preparation, bioinformatics pipelines, staff skills, service contracts and clinical certifications protect incumbents, yet well-funded laboratories routinely multi-home and can validate a second platform over a procurement cycle. The structure is therefore an oligopoly with room for specialist or regional challengers, not a single-platform network market.

The structural model uses these mechanisms rather than today's observed duopoly. It projects a **23.54% leader share**, **75.59% rank-to-rank decay** and **0.129324 HHI**, equivalent to about **7.7 equal-sized competitors**. That is moderately concentrated: the current leaders retain meaningful capture, while MGI/BGI, possible short-read incumbents and new single-molecule architectures have a decade to win positions. The geometric curve assigns about 96.5% of revenue to modeled ranks and leaves a small atomistic fringe; `s1` remains just below `1-r`, so the curve stays inside its normal validity regime. No concentration override is used.

## Players

Current whole-market revenue shares are estimated at **68% Oxford Nanopore** and **31% PacBio**, leaving about 1% for MGI/BGI and other early systems. Oxford Nanopore's share is based on the midpoint of its underlying 2026 guide translated to USD; PacBio uses the midpoint of its August 2026 revenue guide. Both are compared at vendor-recognized platform revenue, not read count, installed instruments, service-lab revenue or a broader genomics TAM.

Oxford Nanopore brings real-time native DNA/RNA sequencing, portability from MinION to PromethION, direct methylation detection, a broad workflow ecosystem and faster growth in clinical and biopharma uses. Its risks are basecalling or yield gaps in accuracy-sensitive applications, China and Middle East exposure, uneven large-project timing, IP litigation and the need to convert research ubiquity into regulated routine use.

PacBio's HiFi platform offers highly accurate long reads and strong positioning in rare disease, near-complete genome work, population projects and complex assembly. SPRQ-Nx lowers its list price per whole genome to $345 and can expand utilization, but the company has weaker scale, persistent cash burn, pricing pressure and a narrower platform range. MGI/BGI's CycloneSEQ is the most visible outside contender; its commercial revenue is not disclosed separately and Oxford Nanopore is pursuing patent and trade-secret claims.

| Current player | Hold-position capture | Mobility model | Canonical capture | Implied 2036 revenue |
| --- | ---: | ---: | ---: | ---: |
| Oxford Nanopore Technologies (ONT.L) | 23.54% | 18.80% | **18.80%** | **$0.55b** |
| PacBio (PACB) | 17.80% | 15.78% | **15.78%** | **$0.46b** |

Mobility reduces both incumbents relative to mechanically keeping today's rank because the ten-year pooled base rate includes rank churn, new entry, fringe migration and a **10.06% gone probability** already embedded in adjusted capture. No company-specific override is used: the model cannot see technology momentum, clinical evidence, financing or litigation, so its result is kept as a structural expected-value handoff rather than fine-grained company forecasting. The two canonical captures total 34.6%, consistent with the moderately concentrated HHI and leaving the majority for entrants, additional incumbents and the modeled tail.

## Watch

- Oxford Nanopore's 19 August 2026 interim results: organic versus license revenue, PromethION utilization, China weakness and the retained FY26 guide.
- PacBio delivery against the $155m-$165m 2026 guide, SPRQ-Nx pull-through, Revio/Vega placements and cash runway.
- Independent, boundary-matched revenue for MGI/BGI CycloneSEQ and progress of Oxford Nanopore's Australian and U.K. litigation.
- Long-read cost per accurate human genome relative to NovaSeq X and emerging short-read platforms, including compute and sample-preparation costs.
- Clinical reimbursement, regulated product clearances and evidence that long reads improve diagnostic yield enough to replace sequential testing.
- Population-scale projects moving from pilots to repeatable production rather than one-off funded programmes.
- Consumables pull-through and active installed-base utilization at Oxford Nanopore and PacBio.
- Entry by Illumina, Thermo Fisher, Roche, Ultima or a new single-molecule architecture within the strict platform-revenue boundary.
- Whether direct RNA, methylation, rapid pathogen surveillance and biopharma quality control expand the category beyond DNA whole-genome sequencing.
- Better whole-market sequencing-vendor revenue data to replace the analyst-reconstructed spend-share denominator.

## Peer Comparison

**About 890% over our 2034 estimate, but not comparable:** Market Data Forecast, current 2026 page, estimates **$3.27b in 2026** and **$21.10b in 2034**, a 26.25% CAGR. Our interpolated 2034 platform-vendor estimate is about **$2.13b**. Its base is more than six times the disclosed 2026 revenue of the two dominant platform suppliers and its competitive set includes sequencing-service companies and broader workflow vendors, indicating that services and downstream activity are counted. The arithmetic is therefore boundary-mismatched and does not justify changing the stored platform view: https://www.marketdataforecast.com/market-reports/long-read-sequencing-market

**About 536% over our 2034 estimate, but not comparable:** IMARC, 2026 edition, estimates **$906.5m in 2025** and **$13.543b in 2034**, a 34.0% CAGR. Its product segmentation includes instruments, consumables and "others," while the profiled competitive set includes contract sequencing laboratories such as BaseClear, Future Genomics and MicrobesNG. Its 2025 base is roughly twice Oxford Nanopore plus PacBio reported revenue, again signalling a broader services boundary. Our interpolated 2034 value is about $2.13b: https://www.imarcgroup.com/long-read-sequencing-market

**TAM rather than expected market value:** Oxford Nanopore's 2025 annual report frames a **$20b-$25b serviceable addressable market** and commercial focus on $13b-$14b of higher-priority segments within more than $150b of long-term molecular-analysis opportunities. Those figures span addressable sequencing and sensing workflows and represent opportunity at broader adoption, not expected 2036 vendor revenue. Our $2.9b view is about 12%-15% of the stated SAM and is therefore compatible with substantial remaining headroom rather than directly over or under it.

The paid-research forecasts disagree with disclosed supplier revenue at the base year and mix platform and service boundaries. They are retained as evidence that external forecasters expect rapid category growth, but the stored estimate remains anchored to supplier filings and a defined spend-share bridge.

## Sources

- Oxford Nanopore Technologies, half-year trading update, 13 July 2026; £116.5m H1 revenue, underlying FY26 constant-currency growth of 16%-20% excluding additional collaboration and licensing opportunities, applied-market growth and regional headwinds: https://www.investegate.co.uk/announcement/rns/oxford-nanopore-technologies--ont/half-year-trading-update-and-notice-of-results/9664204
- Oxford Nanopore Technologies, 2025 annual results, 2 March 2026; £223.9m revenue, product/end-market mix, platform adoption, PromethION growth, clinical collaborations and MGI litigation: https://www.investegate.co.uk/announcement/rns/oxford-nanopore-technologies--ont/annual-results-for-the-year-ended-31-december-2025/9452172
- Oxford Nanopore Technologies, Annual Report & Accounts 2025; company-defined SAM/TAM, research and applied workflow opportunity, product and risk disclosures: https://nanoporetech.com/api/assets/f/196663/x/e6a62a9b49/ont-ar25-interactive-final.pdf
- PacBio, Q2 2026 results, 5 August 2026; $39.0m quarterly revenue, $155m-$165m full-year guide, SPRQ-Nx launch, Revio/Vega placements and clinical long-read evidence: https://www.pacb.com/press_releases/pacbio-announces-second-quarter-2026-financial-results/
- PacBio, 2025 annual results, 12 February 2026; $160.0m revenue, $82.0m consumables, $53.8m instruments, $24.2m service and sale of short-read assets: https://www.pacb.com/press_releases/pacbio-announces-fourth-quarter-and-full-year-2025-financial-results/
- Illumina, 2025 results and 2026 outlook, 5 February 2026; $4.343b 2025 revenue and $4.5b-$4.6b 2026 guidance used to anchor the broader sequencing-platform spend denominator: https://investor.illumina.com/news-releases/news-release-details/illumina-reports-financial-results-fourth-quarter-and-fiscal
- Market Data Forecast, "Long Read Sequencing Market," fetched 8 August 2026; $3.27b 2026 and $21.10b 2034 on a boundary that profiles service and workflow companies: https://www.marketdataforecast.com/market-reports/long-read-sequencing-market
- IMARC, "Long Read Sequencing Market," 2026 edition; $906.5m 2025 and $13.543b 2034 with instruments, consumables, other products and contract-service companies: https://www.imarcgroup.com/long-read-sequencing-market
