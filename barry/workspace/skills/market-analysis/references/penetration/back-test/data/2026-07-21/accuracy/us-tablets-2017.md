---
subject: us-tablets
base-year: 2017
horizon-year: 2021
metrics:
  path-mae-pp: 7.2
  horizon-error-pp: 6.86
  ceiling-error-pp: 5.0
  timing-error-years: -0.53
  model-form-floor-pp: 0.49
  forecast-gap-pp: 6.81
---
# us-tablets-2017 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 7.2 pp | mean abs error over 2018-2021 |
| Horizon error (2021) | +6.9 pp | +over / -under-predicted final penetration |
| Ceiling error | +5.0 pp | asserted 0.60 vs realized 0.55 |
| Timing error | -0.5 yr | +late / -early to half of realized ceiling |
| Model-form floor | 0.5 pp | irreducible: best logistic vs reality |
| Forecast gap | 6.8 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.60 k=0.671 t0=2012; hindsight-optimal L=0.54 k=0.583 t0=2013. Analogs used: us-dvd-player, us-vcr, us-home-computer, us-cable-tv; w_fit=0.84242.

## Attribution

The low 0.5 pp floor confirms that logistic form was suitable; the 6.8 pp gap was a ceiling judgment
miss. The stale 2016 endpoint and a 5 pp high ceiling explain most of the remaining error.

## Issues And Recommendations

Apply an explicit stale-data penalty and give sustained flattening more weight in ceiling selection.
The shrinking error across tablet base years shows the method learns, but ceiling judgment remains
too slow to respond.
