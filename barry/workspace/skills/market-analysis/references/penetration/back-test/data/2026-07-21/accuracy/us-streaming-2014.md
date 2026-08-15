---
subject: us-streaming
base-year: 2014
horizon-year: 2024
metrics:
  path-mae-pp: 1.79
  horizon-error-pp: -0.53
  ceiling-error-pp: -3.0
  timing-error-years: -0.28
  model-form-floor-pp: 0.81
  forecast-gap-pp: 1.3
---
# us-streaming-2014 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 1.8 pp | mean abs error over 2015-2024 |
| Horizon error (2024) | -0.5 pp | +over / -under-predicted final penetration |
| Ceiling error | -3.0 pp | asserted 0.85 vs realized 0.88 |
| Timing error | -0.3 yr | +late / -early to half of realized ceiling |
| Model-form floor | 0.8 pp | irreducible: best logistic vs reality |
| Forecast gap | 1.3 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.85 k=0.317 t0=2013; hindsight-optimal L=0.88 k=0.318 t0=2014. Analogs used: us-dvd-player, us-vcr, us-cable-tv, us-home-computer; w_fit=0.0.

## Attribution

The small 1.3 pp judgment gap slightly exceeded the 0.8 pp floor. Steepness was essentially exact;
the modest errors came from a 3 pp low ceiling and a slightly early anchor.

## Issues And Recommendations

Despite only two observations and imperfect analogs, the prior-only forecast was strong. No method
change is warranted; a verified digital-subscription analog would improve mechanism match.
