---
subject: us-streaming
base-year: 2014
penetration:
  logistic:
    L: 0.85
    t0: 2013.3291
    k: 0.316847
analogs-used: [us-dvd-player, us-vcr, us-cable-tv, us-home-computer]
w-fit: 0.0
---

## Reasoning

Paid streaming already reached 47% of US households by 2014. I set the ceiling at 85%: delivery over an existing broadband connection and low setup friction support adoption above cable TV's historical ceiling, while the recurring fee, households without adequate broadband, and non-subscribers argue against universal penetration.

DVD players provide the fast, existing-TV-channel analog; VCRs provide a slower media-device comparison; cable TV captures recurring-fee media distribution; and home computers provide a slow broadband-adjacent consumer-technology anchor. All four had matured by 2014. With only the 2013 and 2014 target observations available, the target cannot be fitted reliably, so the blend uses the analog prior entirely (`w-fit: 0.0`) and anchors it through the 2014 observation. The resulting curve has `k = 0.316847`, midpoint 2013.3291, and projects 82.20% penetration in 2024.

## Issues

Only two target observations were available, leaving the steepness wholly prior-driven. The analog set lacks a mature, low-friction digital subscription product as of 2014: hardware analogs carry purchase friction, while cable carries installation friction. The 85% ceiling is therefore the largest judgment uncertainty.
