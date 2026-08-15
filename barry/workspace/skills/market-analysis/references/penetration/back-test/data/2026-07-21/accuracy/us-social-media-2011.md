---
subject: us-social-media
base-year: 2011
horizon-year: 2021
metrics:
  path-mae-pp: 7.35
  horizon-error-pp: 5.82
  ceiling-error-pp: 4.0
  timing-error-years: -0.13
  model-form-floor-pp: 1.05
  forecast-gap-pp: 7.68
---
# us-social-media-2011 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 7.4 pp | mean abs error over 2012-2021 |
| Horizon error (2021) | +5.8 pp | +over / -under-predicted final penetration |
| Ceiling error | +4.0 pp | asserted 0.78 vs realized 0.74 |
| Timing error | -0.1 yr | +late / -early to half of realized ceiling |
| Model-form floor | 1.0 pp | irreducible: best logistic vs reality |
| Forecast gap | 7.7 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.78 k=0.505 t0=2009; hindsight-optimal L=0.73 k=0.405 t0=2010. Analogs used: us-dvd-player, us-vcr, us-cable-tv, us-home-computer; w_fit=0.9799.

## Attribution

Judgment overwhelmingly dominated (7.7 pp gap versus 1.0 pp floor). Timing was accurate, but the
ceiling was 4 pp too high and the near-full-weight fit was too steep, creating persistent path
overprediction.

## Issues And Recommendations

The series constrained timing better than saturation. Require a ceiling sensitivity case whenever
the fit receives high weight before a durable plateau is observed, especially for participation
markets with a structural non-user segment.
