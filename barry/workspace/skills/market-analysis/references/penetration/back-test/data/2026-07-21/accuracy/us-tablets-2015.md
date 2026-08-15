---
subject: us-tablets
base-year: 2015
horizon-year: 2021
metrics:
  path-mae-pp: 10.25
  horizon-error-pp: 11.66
  ceiling-error-pp: 10.0
  timing-error-years: 0.25
  model-form-floor-pp: 1.35
  forecast-gap-pp: 11.01
---
# us-tablets-2015 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 10.3 pp | mean abs error over 2016-2021 |
| Horizon error (2021) | +11.7 pp | +over / -under-predicted final penetration |
| Ceiling error | +10.0 pp | asserted 0.65 vs realized 0.55 |
| Timing error | +0.2 yr | +late / -early to half of realized ceiling |
| Model-form floor | 1.4 pp | irreducible: best logistic vs reality |
| Forecast gap | 11.0 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.65 k=0.655 t0=2013; hindsight-optimal L=0.54 k=0.583 t0=2013. Analogs used: us-dvd-player, us-vcr, us-cable-tv, us-home-computer; w_fit=0.7599962894.

## Attribution

Judgment again dominated (11.0 pp gap versus 1.4 pp floor). The emerging slowdown reduced the
ceiling miss to 10 pp, but the forecast still treated it as a pause rather than structural
saturation.

## Issues And Recommendations

When several observations show deceleration, require the analyst to test whether the product is a
complementary second device rather than a universal replacement. A lower-ceiling sensitivity would
have captured the realized path without changing the core model.
