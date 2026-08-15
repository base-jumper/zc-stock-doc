---
subject: us-smartphones
base-year: 2015
penetration:
  logistic:
    L: 0.90
    t0: 2012.27
    k: 0.4779
analogs-used: [us-dvd-player, us-vcr, us-home-computer, us-color-tv]
w-fit: 0.9818
---

## Reasoning

By 2015, smartphone ownership had reached 68% of US adults after rising from 5% in 2007. The market was already past its inflection point, so the observed series is highly informative and the computed blend appropriately gives the target fit 98.2% weight.

I set the ceiling at 90%. Smartphones had strong utility, network effects, and an established mobile-phone distribution and replacement channel, supporting adoption near the high ceilings of DVD players, VCRs, and color televisions. I kept the ceiling below universal adoption because some adults would remain non-users due to affordability, usability, or preference; home computers provide a slower, lower-ceiling anchor. With `--as-of 2015`, the blend yields `k = 0.4779` and `t0 = 2012.27`, implying 89.8% penetration in 2025.

## Issues

The analog set spans materially different diffusion speeds. DVD players best represent rapid consumer-electronics replacement, while VCRs, home computers, and color televisions are older and slower. The strong target fit limits their effect, leaving the asserted 90% ceiling as the main judgment risk. The 2014 observation also shows a brief slowdown before renewed growth in 2015, which adds some path noise.
