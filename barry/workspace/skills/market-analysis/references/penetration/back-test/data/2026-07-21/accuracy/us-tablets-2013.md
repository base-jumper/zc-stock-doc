---
subject: us-tablets
base-year: 2013
horizon-year: 2021
metrics:
  path-mae-pp: 19.28
  horizon-error-pp: 21.88
  ceiling-error-pp: 20.0
  timing-error-years: 0.04
  model-form-floor-pp: 2.16
  forecast-gap-pp: 21.0
---
# us-tablets-2013 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 19.3 pp | mean abs error over 2014-2021 |
| Horizon error (2021) | +21.9 pp | +over / -under-predicted final penetration |
| Ceiling error | +20.0 pp | asserted 0.75 vs realized 0.55 |
| Timing error | +0.0 yr | +late / -early to half of realized ceiling |
| Model-form floor | 2.2 pp | irreducible: best logistic vs reality |
| Forecast gap | 21.0 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.75 k=0.802 t0=2013; hindsight-optimal L=0.54 k=0.583 t0=2013. Analogs used: us-dvd-player, us-vcr, us-home-computer, us-cable-tv; w_fit=0.6946.

## Attribution

The 21.0 pp judgment gap dwarfed the 2.2 pp floor. The asserted ceiling was 20 pp too high and the
curve too steep; midpoint timing was nevertheless accurate. This is the intended early-curve ceiling
trap, not a failure of the logistic form.

## Issues And Recommendations

For secondary or overlapping products, ceiling reasoning must explicitly subtract users whose need
is already met by substitutes. Add a mandatory low-ceiling sensitivity for products with substantial
functional overlap; do not infer a high ceiling from rapid early adoption alone.
