---
run-date: '2026-07-18'
subject-count: 3
mean-absolute-error-pct: 38.0
median-subject-mae-pct: 38.3
metrics:
  maturity-duration:
    mean-signed-error-pct: -36.2
    mean-absolute-error-pct: 36.2
    median-absolute-error-pct: 40.0
  current-market-value:
    mean-signed-error-pct: 13.3
    mean-absolute-error-pct: 16.4
    median-absolute-error-pct: 11.1
  maturity-market-value:
    mean-signed-error-pct: -48.1
    mean-absolute-error-pct: 48.1
    median-absolute-error-pct: 50.2
  hhi:
    mean-signed-error-pct: 5.7
    mean-absolute-error-pct: 51.5
    median-absolute-error-pct: 46.9
consistent-misses:
- metric: maturity-duration
  direction: underestimated
  mean-signed-error-pct: -36.2
  mean-absolute-error-pct: 36.2
- metric: maturity-market-value
  direction: underestimated
  mean-signed-error-pct: -48.1
  mean-absolute-error-pct: 48.1
comparison:
  previous-run-date: null
  mean-absolute-error-change-pct: null
  metric-changes-pct: {}
---

# Market Analysis Back-Test Overall

## Summary

This run covered 3 subject markets. Mean subject MAE was 38.0% and median subject MAE was 38.3%.

No prior dated run was found, so this is the baseline for future methodology checks.

## Comparison

| Run | Mean subject MAE | Change |
|---|---:|---:|
| 2026-07-18 | 38.0% | n/a |

## Metric Accuracy

| Metric | Mean signed error | Mean absolute error | Median absolute error |
|---|---:|---:|---:|
| Maturity duration | -36.2% | 36.2% | 40.0% |
| Current market value | +13.3% | 16.4% | 11.1% |
| Maturity market value | -48.1% | 48.1% | 50.2% |
| HHI | +5.7% | 51.5% | 46.9% |

## Subject Scorecard

| Market | Base year | Subject MAE | Maturity error | Current market-value error | Maturity market-value error | HHI error |
|---|---:|---:|---:|---:|---:|---:|
| Clear Aligner Orthodontics | 2001 | 38.3% | -54.2% | +11.1% | -41.2% | -46.9% |
| CRM Software | 2004 | 38.7% | -14.3% | -4.7% | -50.2% | +85.7% |
| Sleep Apnea CPAP Therapy | 1995 | 37.0% | -40.0% | +33.3% | -52.9% | -21.7% |

## Consistent Misses

- Maturity duration was underestimated in every subject (mean signed error -36.2%; MAE 36.2%).
- Maturity market value was underestimated in every subject (mean signed error -48.1%; MAE 48.1%).

## Subject Details

| Market | Generated maturity | Benchmark maturity | Generated maturity market value | Benchmark maturity market value | Generated HHI | Benchmark HHI |
|---|---:|---:|---:|---:|---:|---:|
| Clear Aligner Orthodontics | 2012 | 2025 | 3 | 5.1 | 0.26 | 0.49 |
| CRM Software | 2016 | 2018 | 24 | 48.23 | 0.13 | 0.07 |
| Sleep Apnea CPAP Therapy | 2010 | 2020 | 2.4 | 5.1 | 0.18 | 0.23 |

## Recommendations

Review the per-subject accuracy docs for qualitative misses. Treat consistent aggregate misses as candidates for methodology changes only when the same issue would plausibly improve live market work.
