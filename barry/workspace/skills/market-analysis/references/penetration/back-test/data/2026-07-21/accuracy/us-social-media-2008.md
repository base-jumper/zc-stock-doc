---
subject: us-social-media
base-year: 2008
horizon-year: 2018
metrics:
  path-mae-pp: 4.25
  horizon-error-pp: 1.49
  ceiling-error-pp: 1.0
  timing-error-years: 1.0
  model-form-floor-pp: 2.36
  forecast-gap-pp: 2.25
---
# us-social-media-2008 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 4.3 pp | mean abs error over 2009-2018 |
| Horizon error (2018) | +1.5 pp | +over / -under-predicted final penetration |
| Ceiling error | +1.0 pp | asserted 0.75 vs realized 0.74 |
| Timing error | +1.0 yr | +late / -early to half of realized ceiling |
| Model-form floor | 2.4 pp | irreducible: best logistic vs reality |
| Forecast gap | 2.3 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.75 k=0.344 t0=2010; hindsight-optimal L=0.73 k=0.405 t0=2010. Analogs used: us-dvd-player, us-vcr, us-cable-tv, us-color-tv; w_fit=0.0.

## Attribution

The 2.4 pp floor and 2.3 pp gap split the error evenly. Prior-only timing was about one year late,
while the asserted low ceiling was accurate to 1 pp.

## Issues And Recommendations

The hardware-heavy prior was imperfect but useful. Add verified free consumer-software/network-effect
analogs; do not relax the prior-only fallback for fewer than four target observations.
