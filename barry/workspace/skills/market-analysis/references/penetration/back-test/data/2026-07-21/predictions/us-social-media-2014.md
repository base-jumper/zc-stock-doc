---
subject: us-social-media
base-year: 2014
penetration:
  logistic:
    L: 0.80
    t0: 2009.8587
    k: 0.44578
analogs-used: [us-dvd-player, us-cable-tv, us-home-computer, us-vcr]
w-fit: 0.98237
---

## Reasoning

The asserted 80% ceiling reflects a free, low-friction service with strong network effects, tempered by adults who lack internet access or opt out for privacy, preference, or capability reasons. Adoption had already reached 62% in the latest available observation (2013), so a ceiling materially below 75% looked too restrictive, while universal adoption looked implausible.

DVD players supply a fast, channel-riding diffusion analog; cable TV contributes a lower-ceiling media-network case; home computers provide a slower technology-access constraint; and VCRs add a medium-speed consumer-media anchor. With eight target observations spanning the takeoff and later growth, the statistical fit receives 0.98237 weight. Running `blend` with `--as-of 2014` gives `k = 0.44578` and midpoint `2009.8587`, projecting penetration of about 79.85% in 2024.

## Issues

The source series has no 2014 observation, so the forecast is anchored to 2013 despite the 2014 base-year. The largest judgment uncertainty is the ceiling: the observed curve was already bending, but the available history could not distinguish a durable plateau near 80% from a slower climb toward the broader internet-user ceiling. No mature analog combines social software's near-zero adoption cost and network effects, so the prior set is mechanism-adjacent rather than close.
