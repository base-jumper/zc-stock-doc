---
market-id: sleep-apnea-cpap-therapy
run-date: 2026-07-18
base-year: 1995
errors:
  mean-absolute-error-pct: 37.0
  maturity-duration-error-pct: -40.0
  current-market-value-error-pct: 33.3
  maturity-market-value-error-pct: -52.9
  hhi-error-pct: -21.7
  player-capture:
    - name: ResMed
      ticker: RMD
      error-pct: -42.1
    - name: Philips Respironics
      ticker: PHG
      error-pct: 11.1
    - name: Fisher & Paykel Healthcare
      ticker: FPH.NZ
      error-pct: -100.0
    - name: Lowenstein Medical
      ticker: PRIVATE
      error-pct: -100.0
    - name: BMC Medical
      ticker: PRIVATE
      error-pct: -100.0
---
# Sleep Apnea CPAP Therapy Back-Test Accuracy

## Summary

The generated doc was directionally useful on early market scale, clinical bottlenecks, and the likely ResMed/Respironics leader set. It overestimated 1995 TAM by 33%, but that is close for a sparse historical device market.

The largest misses were maturity timing and mature TAM. The forecast treated the market as mature by 2010, while the benchmark uses 2020, and it undersized mature therapy revenue by 53% by underweighting installed-base resupply, masks, humidification, and connected adherence.

## Scorecard

| Metric | Generated | Benchmark | Error | Assessment |
|---|---:|---:|---:|---|
| Maturity duration | 15 years | 25 years | -40.0% | Too early |
| Current TAM | $0.24B | $0.18B | 33.3% | Reasonable |
| Mature TAM | $2.40B | $5.10B | -52.9% | Too small |
| Mature HHI | 0.18 | 0.23 | -21.7% | Directionally right, too fragmented |
| ResMed capture | 22% | 38% | -42.1% | Underestimated winner quality |
| Respironics/Philips capture | 30% | 27% | 11.1% | Good |
| Fisher & Paykel capture | 0% | 6% | -100.0% | Missed |

Respironics is mapped to Philips Respironics because Philips later owned the franchise. ResMed's generated 1995 ticker `RESM` is mapped to benchmark ticker `RMD`.

## Largest Errors

The forecast compressed the adoption curve. It correctly identified diagnosis, reimbursement, sleep-lab capacity, and adherence as bottlenecks, but assumed those constraints would clear by 2010 rather than becoming a longer 25-year buildout.

The mature TAM was too low because the model leaned on flow-generator setups and active-user counts, then only lightly capitalized recurring masks, tubing, filters, humidification, and adherence software. The benchmark market is a therapy revenue pool, not just a machine market.

The player list overfit the 1995 field. It captured ResMed and Respironics, but kept Healthdyne, Nellcor Puritan Bennett, and Sunrise/DeVilbiss as mature share holders while missing Fisher & Paykel and later regional suppliers.

## What The Skill Missed

For chronic device markets, the durable installed base can matter more than the initial device sale. The generated doc mentioned replacement parts but did not model resupply as the central mature-market economics.

The process also needs a clearer successor mapping for player capture. A correct 1995 forecast may name Respironics, but scoring needs to map that to Philips Respironics; similarly, early tickers can differ from mature public tickers.

## What The Skill Got Right

It used a clean 1995 TAM anchor from Respironics' OSA revenue and inferred a plausible current market size. It identified CPAP as clinically validated before commercial maturity, and it emphasized the right adoption constraints: sleep-lab capacity, reimbursement, homecare distribution, mask comfort, and adherence.

It also recognized the durable top-two structure. ResMed was underweighted, but the generated doc still elevated ResMed and Respironics above diversified respiratory-device competitors.

## Recommendations

Add an installed-base resupply step to `market-analysis` for chronic device markets: estimate active users, new starts, replacement cycle, consumables per active user, and software/service attach before setting mature TAM.

Add a back-test scoring convention for corporate successor mapping and ticker changes.

When base-year sources show a one-time device sale plus recurring accessories, require the doc to state which component dominates mature TAM.
