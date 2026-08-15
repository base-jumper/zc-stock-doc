---
subject: us-streaming
base-year: 2012
horizon-year: 2022
metrics:
  path-mae-pp: 5.06
  horizon-error-pp: -1.41
  ceiling-error-pp: -3.0
  timing-error-years: -1.28
  model-form-floor-pp: 0.92
  forecast-gap-pp: 4.98
---
# us-streaming-2012 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 5.1 pp | mean abs error over 2013-2022 |
| Horizon error (2022) | -1.4 pp | +over / -under-predicted final penetration |
| Ceiling error | -3.0 pp | asserted 0.85 vs realized 0.88 |
| Timing error | -1.3 yr | +late / -early to half of realized ceiling |
| Model-form floor | 0.9 pp | irreducible: best logistic vs reality |
| Forecast gap | 5.0 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.85 k=0.318 t0=2012; hindsight-optimal L=0.88 k=0.318 t0=2014. Analogs used: us-dvd-player, us-vcr, us-cable-tv, us-home-computer; w_fit=0.0.

## Attribution

Judgment dominated (5.0 pp gap versus 0.9 pp floor), but not through steepness: predicted and
hindsight k were both 0.318. The prior-only anchor placed the midpoint roughly a year early, while
the ceiling was 3 pp low.

## Issues And Recommendations

With only three observations, the prior-only fallback behaved reasonably. Add a mature low-friction
digital-subscription analog; otherwise retain the fallback and expose timing sensitivity around the
latest-point anchor.
