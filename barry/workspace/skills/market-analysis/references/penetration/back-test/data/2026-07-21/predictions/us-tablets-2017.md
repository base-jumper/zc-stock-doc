---
subject: us-tablets
base-year: 2017
penetration:
  logistic:
    L: 0.60
    t0: 2012.7638
    k: 0.67082
analogs-used: [us-dvd-player, us-vcr, us-home-computer, us-cable-tv]
w-fit: 0.84242
---

## Reasoning

Tablet ownership rose rapidly from 3% in 2010 to 42% in 2014, then slowed markedly, reaching 51% in the latest available observation in 2016. I therefore assert a 60% ceiling: tablets had broad appeal and established consumer-electronics distribution, but their incremental utility was limited by overlap with smartphones and computers, making near-universal ownership unlikely.

DVD players provide a fast consumer-electronics and existing-channel analog; VCRs provide a medium-speed media-hardware precedent; home computers capture a slower, general-purpose device with a sub-universal ceiling; and cable TV supplies a lower-ceiling household technology anchor. The seven target observations span the takeoff and early flattening, so the uncapped statistical blend gives the target fit 84.2% weight. Running `blend` with `--as-of 2017` yields `k = 0.67082` and `t0 = 2012.7638`, projecting 60.0% penetration in 2027.

## Issues

There is no 2017 target observation, so the forecast is anchored to 2016. The largest judgment risk is interpreting the 2014–2016 slowdown: it may indicate durable saturation near 60%, but the short late-stage history cannot rule out a pause followed by further adoption. None of the admissible analogs combines tablet portability, rapid early diffusion, and substantial functional overlap with two already-established device categories; the prior set is therefore mechanism-adjacent rather than exact.
