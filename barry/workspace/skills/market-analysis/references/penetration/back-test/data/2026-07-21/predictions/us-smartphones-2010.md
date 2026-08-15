---
subject: us-smartphones
base-year: 2010
penetration:
  logistic:
    L: 0.85
    t0: 2012.1633290531722
    k: 0.4662107045498367
analogs-used: [us-dvd-player, us-vcr, us-cable-tv, us-home-computer]
w-fit: 0.5
---

## Reasoning

The observed series rose from 5% in 2007 to 24% in 2010, indicating rapid adoption but remaining just below one-third of the asserted ceiling. An 85% ceiling reflects a product likely to become broadly useful across US adults while allowing for non-adopters constrained by cost, preferences, or limited need.

DVD players and VCRs provide consumer-electronics and replacement-cycle comparisons; home computers capture a versatile connected device with affordability and capability barriers; cable television is the deliberate slower anchor and represents recurring service friction. All four analogs passed the 2010 plateau-admissibility filter.

The unconstrained statistical fit weight was 0.944, but the target was still early enough that its steep initial trajectory could overstate mainstream adoption speed. The fit weight was therefore capped at 0.5. Blending with `--as-of 2010` produced `k = 0.4662` and midpoint `2012.1633`, implying 2020 penetration of approximately 82.9%.

## Issues

The ceiling is the main judgment risk: only four annual observations were available and none directly identified saturation. The analog set spans markedly different purchase and subscription frictions, while smartphones combine a hardware replacement cycle with network and app-ecosystem effects that no single admissible analog captures cleanly.
