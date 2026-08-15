---
subject: us-social-media
base-year: 2008
penetration:
  logistic:
    L: 0.75
    t0: 2010.017614007759
    k: 0.3435479620454526
analogs-used: [us-dvd-player, us-vcr, us-cable-tv, us-color-tv]
w-fit: 0.0
---

## Reasoning

The available series rose from 7% of US adults in 2005 to 11% in 2006 and 25% in 2008. That is consistent with rapid diffusion, but three observations do not support a standalone target fit. The forecast therefore uses the admissible-analog prior and anchors it through the 2008 observation.

A 75% ceiling reflects a free, low-friction service with network effects that could become broadly useful, while retaining a meaningful non-adopter segment because participation requires internet access, interest in online social interaction, and willingness to accept privacy and safety trade-offs. The ceiling is held below the high-ceiling consumer-electronics analogs and close to cable television's broader-but-not-universal reach.

DVD players provide a recent fast-diffusion analog; VCRs provide an earlier consumer-media adoption path; cable television captures recurring-service and household-choice friction; and color television is the deliberate slower anchor. All passed the 2008 plateau-admissibility filter. Running the blend with `--as-of 2008` produced `k = 0.3435`, midpoint `2010.0176`, and projected 2018 penetration of approximately 70.5%.

## Issues

No admissible analog closely matches a free network-effects service, so the prior mixes hardware and subscription adoption mechanisms. The target has only three observations, leaving the ceiling entirely judgment-driven and forcing `w-fit = 0.0`; uncertainty around internet access and persistent non-participation is therefore the largest forecast risk.
