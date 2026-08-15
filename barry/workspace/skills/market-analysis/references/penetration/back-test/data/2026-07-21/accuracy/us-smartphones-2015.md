---
subject: us-smartphones
base-year: 2015
horizon-year: 2025
metrics:
  path-mae-pp: 3.05
  horizon-error-pp: -1.18
  ceiling-error-pp: -3.0
  timing-error-years: 0.09
  model-form-floor-pp: 2.1
  forecast-gap-pp: 2.68
---
# us-smartphones-2015 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 3.1 pp | mean abs error over 2016-2025 |
| Horizon error (2025) | -1.2 pp | +over / -under-predicted final penetration |
| Ceiling error | -3.0 pp | asserted 0.90 vs realized 0.93 |
| Timing error | +0.1 yr | +late / -early to half of realized ceiling |
| Model-form floor | 2.1 pp | irreducible: best logistic vs reality |
| Forecast gap | 2.7 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.90 k=0.478 t0=2012; hindsight-optimal L=0.92 k=0.381 t0=2013. Analogs used: us-dvd-player, us-vcr, us-home-computer, us-color-tv; w_fit=0.9818.

## Attribution

Model form and judgment were comparable (2.1 pp floor versus 2.7 pp gap). Timing was essentially
correct; the remaining miss came from a slightly low ceiling and a fitted steepness above the
hindsight curve.

## Issues And Recommendations

No method change is justified by this 3.1 pp result. Preserve explicit ceiling sensitivity and add
closer mobile-device analogs when verified data becomes available.
