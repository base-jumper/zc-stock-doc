---
subject: us-streaming
base-year: 2016
horizon-year: 2024
metrics:
  path-mae-pp: 1.51
  horizon-error-pp: 0.14
  ceiling-error-pp: -3.0
  timing-error-years: -0.3
  model-form-floor-pp: 0.85
  forecast-gap-pp: 1.28
---
# us-streaming-2016 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 1.5 pp | mean abs error over 2017-2024 |
| Horizon error (2024) | +0.1 pp | +over / -under-predicted final penetration |
| Ceiling error | -3.0 pp | asserted 0.85 vs realized 0.88 |
| Timing error | -0.3 yr | +late / -early to half of realized ceiling |
| Model-form floor | 0.9 pp | irreducible: best logistic vs reality |
| Forecast gap | 1.3 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.85 k=0.345 t0=2013; hindsight-optimal L=0.88 k=0.318 t0=2014. Analogs used: us-dvd-player, us-vcr, us-cable-tv, us-home-computer; w_fit=0.97444.

## Attribution

Both components were small: 0.9 pp floor and 1.3 pp gap. The fit modestly overstated steepness and
understated the ceiling, but the effects offset at the scored horizon.

## Issues And Recommendations

No method change is justified. Preserve unit-basis scrutiny because service overlap and incomplete
provider coverage can otherwise masquerade as adoption dynamics.
