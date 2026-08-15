---
subject: us-social-media
base-year: 2014
horizon-year: 2021
metrics:
  path-mae-pp: 8.28
  horizon-error-pp: 7.62
  ceiling-error-pp: 6.0
  timing-error-years: -0.26
  model-form-floor-pp: 0.72
  forecast-gap-pp: 7.97
---
# us-social-media-2014 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 8.3 pp | mean abs error over 2015-2021 |
| Horizon error (2021) | +7.6 pp | +over / -under-predicted final penetration |
| Ceiling error | +6.0 pp | asserted 0.80 vs realized 0.74 |
| Timing error | -0.3 yr | +late / -early to half of realized ceiling |
| Model-form floor | 0.7 pp | irreducible: best logistic vs reality |
| Forecast gap | 8.0 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.80 k=0.446 t0=2009; hindsight-optimal L=0.73 k=0.405 t0=2010. Analogs used: us-dvd-player, us-cable-tv, us-home-computer, us-vcr; w_fit=0.98237.

## Attribution

This was a clear judgment miss: 8.0 pp gap against a 0.7 pp floor. The 6 pp high ceiling dominated;
the target fit also placed the midpoint early. A missing base-year observation made the effective
information set one year older than the label suggests.

## Issues And Recommendations

Make data staleness explicit in live forecasts and reduce effective fit confidence when the latest
observation predates the analysis year. Require a lower-ceiling sensitivity when growth is already
bending but a persistent non-adopter share remains plausible.
