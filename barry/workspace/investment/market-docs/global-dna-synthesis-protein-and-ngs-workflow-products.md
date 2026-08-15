---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 8.2
  maturity-market-value: 21.0
concentration:
  inputs:
    traits:
      network-effects: {score: 0.10, confidence: 0.90}
      data-scale-advantage: {score: 0.35, confidence: 0.70}
      brand-reputation: {score: 0.55, confidence: 0.75}
      capital-intensity: {score: 0.45, confidence: 0.80}
      scale-economies: {score: 0.60, confidence: 0.80}
      regulatory-barriers: {score: 0.45, confidence: 0.85}
      switching-costs: {score: 0.45, confidence: 0.75}
  model-estimate:
    s1: 0.151599
    r: 0.822048
  hhi: 0.070882
  method: selected-direct-ridge
  date: 2026-08-10
players:
  override:
    - name: Twist Bioscience
      ticker: TWST
      capture: 0.085
      reason: "Boundary-matched top-player rankings are unavailable because diversified suppliers do not disclose these products consistently. The override raises Twist from about 5.6% of the 2026 pool to 8.5% in 2036, reflecting its current 21% growth, integrated silicon synthesis platform, product expansion and capacity, while remaining near the structural model's fourth-rank share."
---
# Global DNA Synthesis, Protein Discovery and NGS Workflow Products

## Market Definition

**Market scope:** worldwide merchant products and services that Twist Bioscience sells today or has placed into commercial or early-access workflows: synthetic genes and gene fragments; oligonucleotide pools and DNA libraries; synthetic RNA and research-use nucleic-acid inputs; antibody libraries, antibody-discovery services, protein expression and characterization; and sequencer-agnostic NGS library preparation, sample preparation, target-enrichment probes and panels, adapters, indexes, synthetic controls and closely integrated workflow reagents. Research, biopharma, diagnostics-development, academic, government, agriculture and industrial customers are included.

**Revenue boundary:** annual net revenue recognized by the merchant manufacturer or service provider for the included products and contracted discovery work. The boundary excludes sequencers and flow cells, sequencing-service laboratories, diagnostic-test revenue, clinical interpretation, bioinformatics software, customer R&D spend, customer manufacturing revenue, royalties or milestones on downstream assets, DNA data storage, and all revenue from approved drugs, diagnostics, engineered crops, chemicals or other products created with these inputs. Distributor mark-ups and customer GMV are also excluded. This prevents a DNA order used to discover a drug from importing the drug's eventual sales into Twist's market.

The **addressable unit** is one dollar of eligible worldwide workflow-input spend that can structurally be supplied by an external specialist under the included contract. **Penetration** is `spend-share`: included merchant-vendor revenue divided by that eligible workflow-input spend. **Billable units** are genes, fragments, oligo pools, DNA or antibody libraries, proteins and characterization assays, discovery-project milestones, prepared samples, enrichment panels or probes, library-preparation reactions, adapters, indexes and controls. The market aggregates two segments at vendor revenue: DNA synthesis and protein solutions (DSPS), and NGS applications. Their separate revenue pools are summed; no downstream value is added. The base year is 2026, the horizon is 2036, and values are nominal USD at approximately constant current foreign-exchange rates.

A single penetration curve is not stored. The two segments combine mature outsourced products, new AI discovery workflows and diagnostic-volume consumables, and no consistent historical denominator exists across them. Fitting one logistic series would falsely treat product mix and addressable-category expansion as adoption. Segment revenue pools and their explicit growth rates therefore provide the sizing bridge.

## Current View

The expected 2026 market value is **$8.2B**, with a rough **$6.5B-$10B** plausible range. Twist's May 2026 Investor Day compiled a 2030 serviceable market of about **$6B for NGS applications** and **$7B-plus for DNA synthesis and protein solutions**, using BCC Research, DeciBio, Grand View Research and internal estimates. The disclosed segment growth rates were approximately 14% and 11%. Back-casting those segment pools four years gives about **$3.6B of 2026 NGS applications** and **$4.7B of DSPS**, or $8.2B after rounding.

This reconstruction is preferred to the presentation's much broader **greater-than-$90B NGS TAM** and **$18B DSPS TAM**. Those figures include potential future applications and value pools outside today's annual supplier-revenue boundary. The $2T-$4T bioeconomy impact cited in Twist's 2025 Form 10-K is an economic-output estimate, not product-vendor revenue, and is excluded entirely.

Twist's latest 2026 guidance is **$456M-$457M**, up about 21% year over year. Its nine-month revenue mix was 48% DSPS and 52% NGS applications, matching both sides of the contract. The $456.5M midpoint implies approximately **5.6% current whole-market share**. That is a useful reconciliation rather than a claim that the reconstructed denominator is precisely measured.

## Adoption Path

The expected 2036 market value is **$21B**, with a broad **$15B-$32B** plausible range. The bridge accepts Twist's 2030 segment map as the closest public, product-level boundary and then assumes growth decelerates as the categories scale: NGS applications grow 14% annually through 2030 and 9% from 2030 to 2036; DSPS grows 11% through 2030 and 8% thereafter. This yields approximately $10.1B of NGS applications and $11.3B of DSPS in 2036, rounded to a $21B total. The whole market grows about 9.9% annually from 2026.

| Driver | 2026 | 2030 | 2036 | Basis |
| --- | ---: | ---: | ---: | --- |
| NGS applications | ~$3.6B | ~$6.0B | ~$10.1B | Library/sample preparation, target enrichment, panels, probes, adapters and controls |
| DNA synthesis and protein solutions | ~$4.7B | ~$7.1B | ~$11.3B | Synthetic nucleic acids, libraries, proteins, discovery and characterization |
| Included annual vendor revenue | **$8.2B** | **~$13.1B** | **$21B** | Segment sum; rounded, nominal USD |

NGS volume is driven by liquid biopsy, minimal residual disease, rare disease, population genetics, single-cell and RNA workflows. Lower sequencing cost can expand sample counts even while reagent revenue per sample falls. DSPS is driven by more design-build-test cycles, AI-generated sequence candidates, higher-complexity genes, protein expression and characterization, and outsourced antibody discovery. Price declines in basic synthesis are offset in the reference case by volume, complexity, faster turnaround and movement into integrated workflows.

The revenue archetype is repeat-purchase consumables plus contracted services. There is no installed durable base multiplied by an equipment price. The largest sensitivities are research and biopharma funding, clinical validation and reimbursement, sequencing cost per sample, vendor price compression, AI-discovery wet-lab demand, and whether customers internalize or outsource workflow steps. The downside assumes slower diagnostics volumes and commoditization; the upside requires sustained double-digit sample growth and successful category expansion without importing downstream drug economics.

## Market Structure

Direct network effects are weak: a gene or enrichment panel does not become intrinsically better because more laboratories buy it. Protocol publication, validated panel content and partner ecosystems create modest indirect benefits, but customers can multi-source. Data scale provides a limited advantage in sequence manufacturability, quality control, enzyme engineering and AI-enabled discovery; much scientific data is customer-owned or public and returns should diminish.

Reputation matters because failed synthesis, bias or poor reproducibility wastes samples and development time. Capital requirements are meaningful but not prohibitive: automated synthesis, quality systems, laboratories and global fulfillment require investment, while contract capacity and conventional laboratory equipment remain available. Scale economies are material in silicon utilization, automation, reagent purchasing, fixed quality systems and spreading R&D across throughput. They should support several large platforms rather than one winner.

Regulation and IP slow entry without capping it. Screening obligations, export controls, clinical-quality requirements and platform patents matter, but much of the market remains research-use-only. Switching costs are moderate: customers validate panels, protocols and informatics, yet laboratories routinely qualify alternatives, use vendor-agnostic kits and dual-source critical inputs. Twist reported 99% of fiscal 2025 revenue from repeat customers, evidence of stickiness but not exclusive lock-in.

The data-scale, brand, capital, scale and switching scores remain below high confidence because matching supplier win/loss, retention and unit-cost data are not public. Boundary-matched customer retention by product, vendor gross-margin bridges and disclosed validation-cycle lengths would raise confidence; absent those disclosures, the uncertainty is irreducible for now and should be revisited in annual reports and investor-day materials.

The structural model is expected to describe a fragmented-to-moderately-concentrated supplier field. Twist's own 2025 Form 10-K names more than two dozen competitors across synthetic biology, NGS preparation and antibody discovery, including Danaher's IDT, Thermo Fisher's GeneArt, GenScript, Azenta's GENEWIZ, Eurofins, Agilent, Illumina, Roche, New England Biolabs, Curia, Charles River, AbCellera and specialist entrants. Diversified-company reporting prevents a defensible whole-contract ranking.

## Players

Twist is included through an analyst-owned override rather than the rank-mobility model. The mobility runbook requires a defensible current top-two-to-five ranking with whole-market shares on the exact contract. That evidence does not exist: major competitors bury relevant revenue inside broader life-science segments, private suppliers disclose little, and several competitors address only one of the two included segments. Inventing ranks would be less informative than an explicit company-specific capture judgment.

Twist's 2026 revenue midpoint gives a current share of about 5.6%. Its advantages are silicon-based parallel synthesis, high-throughput automation, an integrated menu from DNA through proteins and NGS preparation, strong repeat purchasing, roughly 3,800 fiscal 2025 customers, and current growth well above the reconstructed market. Its May 2026 Investor Day targeted more than doubling revenue organically from fiscal 2026 through fiscal 2031 and described line of sight to more than $1B of annual capacity with sustaining capital expenditure.

The canonical **8.5% 2036 capture** assumes Twist gains roughly three share points while remaining one of several scaled platforms. It is close to the structural geometric curve's approximate fourth-rank share rather than a leader case. Multiplying 8.5% by the $21B projected market gives **$1.785B of canonical 2036 TWST revenue**. This requires growth of about 14.6% annually from the 2026 guide midpoint, consistent with more-than-doubling by 2031 followed by high-single-digit growth. It does not credit downstream milestones, royalties or drug sales.

| Player | Current reference | Canonical 2036 capture | Implied 2036 revenue | Method |
| --- | ---: | ---: | ---: | --- |
| Twist Bioscience (TWST) | ~$0.457B / ~5.6% | **8.5%** | **$1.785B** | Explained per-player override |

The capture is most sensitive to durable NGS panel and library-prep growth, conversion of AI customers into repeat DNA-and-protein workflows, manufacturing yield and turnaround, gross-margin evidence of scale advantage, and larger competitors' willingness to bundle or price aggressively.

## Watch

- Fiscal 2026 actual revenue and fiscal 2027 guidance by DSPS and NGS applications versus the 21% 2026 growth rate.
- Progress toward more than doubling revenue through fiscal 2031 and whether capacity expands beyond the stated greater-than-$1B annual level.
- MRD, liquid-biopsy and rare-disease production volumes moving from validation to repeat commercial orders.
- AI-native drug-discovery customers converting into repeated DNA, protein-expression and characterization cycles rather than project revenue.
- FlexPrep, MRD Express, complex genes, RNA, protein and Invenra bispecific workflows expanding wallet share inside the strict supplier boundary.
- Gene shipment growth, turnaround time, manufacturing yield, gross margin and fixed-cost leverage at Wilsonville.
- Price-per-base and price-per-sample erosion versus mix gains from complexity, speed and integrated workflows.
- Boundary-matched product revenue or share disclosure from IDT/Danaher, Thermo Fisher, Agilent, GenScript, Azenta/GENEWIZ, Eurofins, QIAGEN and private specialists.
- Export-control, sequence-screening and clinical-quality rules that could favor scaled compliant suppliers or slow global demand.
- Evidence that customers are insourcing versus outsourcing DNA, protein-discovery or NGS-preparation steps.

## Peer Comparison

**About 21% under our 2031 DSPS estimate, but boundary-mismatched:** Mordor Intelligence, updated in 2026, estimates the gene-synthesis market at **$2.85B in 2026** and **$6.09B in 2031**, a 16.38% CAGR. Our DSPS path reaches about **$7.67B in 2031**. Mordor is narrower because it is labelled gene synthesis, while our DSPS segment also includes antibody discovery, protein expression and characterization. Its 2026 value is therefore not evidence that the total stored market is too large: https://www.mordorintelligence.com/industry-reports/gene-synthesis-market

**About 189% over our 2030 DNA-synthesis sub-pool, but not directly comparable:** Grand View Research projects the global gene-synthesis market to **$5.78B in 2030** at a 16.1% 2023-2030 CAGR. Twist's investor-day segment map allocates about **$2.0B** to DNA synthesis in 2030, inside the $7.1B DSPS pool. The disagreement likely reflects inclusion of different synthesis methods, service layers and application revenues; Grand View's forecast is retained as an upside boundary for the DNA portion rather than added to antibody or protein pools: https://www.grandviewresearch.com/industry-analysis/gene-synthesis-market-report

**About 518% over our 2030 antibody-discovery-services sub-pool, but not comparable:** Mordor Intelligence estimates **$9.09B in 2025** and **$15.45B in 2030** for antibody discovery. The report says in-house discovery held 52.6% of the 2024 market, whereas this contract counts only vendor-recognized products and contracted services. Its 2030 figure is therefore far broader than the approximately **$2.5B antibody-discovery-services** pool in Twist's segment map and cannot be added to the stored market: https://www.mordorintelligence.com/industry-reports/antibody-discovery-market

No useful independent long-term forecast was found for the exact sequencer-excluded NGS library-prep, sample-prep and target-enrichment boundary. Published NGS forecasts commonly include instruments, sequencing services, diagnostics or downstream analysis. That absence is a principal source-quality limitation and supports the wide stored range rather than a peer-informed change to the base case.

## Sources

- Twist Bioscience, fiscal third-quarter 2026 results, 3 August 2026; $118.4M quarterly revenue, 39% DSPS growth, 12% NGS growth and $456M-$457M fiscal 2026 guidance: https://www.sec.gov/Archives/edgar/data/1581280/000158128026000044/twst-2026630xex991.htm
- Twist Bioscience, Form 10-Q for the quarter ended 30 June 2026, filed 3 August 2026; nine-month revenue, product mix, customer and gene-shipment disclosures: https://www.sec.gov/Archives/edgar/data/1581280/000158128026000047/twst-20260630.htm
- Twist Bioscience, Investor Day 2026 presentation, 21 May 2026; 2030 DSPS and NGS serviceable-market map, market-growth rates, product roadmap, multi-year growth outlook and capacity commentary: https://investors.twistbioscience.com/static-files/b091befc-c055-44c7-a7ce-9becedaa4607
- Twist Bioscience, Form 10-K for fiscal 2025, filed 17 November 2025; $376.6M revenue, product revenue detail, 3,800-plus customers, 99% repeat-customer revenue, products, competition, platform and risk disclosures: https://www.sec.gov/Archives/edgar/data/1581280/000158128025000025/twst-20250930.htm
- Mordor Intelligence, "Gene Synthesis Market," updated 2026; $2.85B 2026 and $6.09B 2031 forecast at 16.38% CAGR on a gene-synthesis boundary: https://www.mordorintelligence.com/industry-reports/gene-synthesis-market
- Grand View Research, "Gene Synthesis Market Size & Growth Analysis Report, 2030," current page; $5.78B 2030 forecast and 16.1% 2023-2030 CAGR: https://www.grandviewresearch.com/industry-analysis/gene-synthesis-market-report
- Mordor Intelligence, "Antibody Discovery Market," current 2030 report; $9.09B 2025 and $15.45B 2030 forecast including in-house discovery: https://www.mordorintelligence.com/industry-reports/antibody-discovery-market
