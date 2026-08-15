---
subject: us-smartphones
base-year: 2013
horizon-year: 2023
metrics:
  path-mae-pp: 7.52
  horizon-error-pp: -0.13
  ceiling-error-pp: -3.0
  timing-error-years: -0.93
  model-form-floor-pp: 2.69
  forecast-gap-pp: 7.81
---
# us-smartphones-2013 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 7.5 pp | mean abs error over 2014-2023 |
| Horizon error (2023) | -0.1 pp | +over / -under-predicted final penetration |
| Ceiling error | -3.0 pp | asserted 0.90 vs realized 0.93 |
| Timing error | -0.9 yr | +late / -early to half of realized ceiling |
| Model-form floor | 2.7 pp | irreducible: best logistic vs reality |
| Forecast gap | 7.8 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.90 k=0.542 t0=2011; hindsight-optimal L=0.92 k=0.381 t0=2013. Analogs used: us-dvd-player, us-vcr, us-home-computer, us-cable-tv; w_fit=0.9901.

## Attribution

Judgment dominated: the 7.8 pp forecast gap was almost three times the 2.7 pp floor. The nearly
full-weight target fit inferred a curve that was too steep and about one year early; the ceiling miss
was modest and the horizon recovered once both curves saturated.

## Issues And Recommendations

Statistical fit confidence overstated extrapolation confidence near the inflection. Extend the
early-stage weight-cap guidance beyond the one-third-of-ceiling heuristic: flag implausibly high
weights when the target has only a short span or has not shown sustained deceleration.
