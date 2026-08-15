---
subject: us-smartphones
base-year: 2010
horizon-year: 2020
metrics:
  path-mae-pp: 1.82
  horizon-error-pp: 0.01
  ceiling-error-pp: -8.0
  timing-error-years: 0.35
  model-form-floor-pp: 4.29
  forecast-gap-pp: 3.1
---
# us-smartphones-2010 Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | 1.8 pp | mean abs error over 2011-2020 |
| Horizon error (2020) | +0.0 pp | +over / -under-predicted final penetration |
| Ceiling error | -8.0 pp | asserted 0.85 vs realized 0.93 |
| Timing error | +0.4 yr | +late / -early to half of realized ceiling |
| Model-form floor | 4.3 pp | irreducible: best logistic vs reality |
| Forecast gap | 3.1 pp | judgment: forecast vs best logistic |

Predicted logistic L=0.85 k=0.466 t0=2012; hindsight-optimal L=0.92 k=0.381 t0=2013. Analogs used: us-dvd-player, us-vcr, us-cable-tv, us-home-computer; w_fit=0.5.

## Attribution

The 4.3 pp model-form floor exceeds the 3.1 pp forecast gap, so the path miss was driven more by
departures from a smooth logistic than by forecast judgment. The low ceiling was offset by slightly
faster timing, producing an essentially exact horizon estimate.

## Issues And Recommendations

The admissible library lacked a close mobile-device analog, and four early observations could not
identify saturation. Retain the early-stage fit-weight cap: it prevented an unstable high-weight fit
from dominating and delivered a strong result. Expand the verified analog library with mature mobile
personal devices before changing the method.
