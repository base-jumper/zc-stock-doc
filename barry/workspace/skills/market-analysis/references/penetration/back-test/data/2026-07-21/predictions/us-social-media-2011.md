---
subject: us-social-media
base-year: 2011
penetration:
  logistic:
    L: 0.78
    t0: 2009.47
    k: 0.5046
analogs-used: [us-dvd-player, us-vcr, us-cable-tv, us-home-computer]
w-fit: 0.9799
---

## Reasoning

By 2011, social-media use had risen from 7% of US adults in 2005 to 50%, with a smooth path through 11% in 2006, 25% in 2008, 38% in 2009, and 46% in 2010. I set the ceiling at 78%: participation had strong network effects and negligible incremental purchase friction, but it still depended on internet access and voluntary participation, leaving a durable non-user segment plausible.

DVD players supply a recent fast-diffusion analog; VCRs offer a slower consumer-adoption comparison; cable TV captures a lower-ceiling network service; and home computers represent the access technology and a deliberate slow anchor. All four passed the 2011 plateau-admissibility filter. The observed target was already well beyond one-third of the asserted ceiling and fit a logistic cleanly, so I retained the computed 97.99% fit weight. Running the blend with `--as-of 2011` produced `k = 0.5046` and midpoint `2009.47`, implying 77.77% penetration in 2021.

## Issues

No eligible analog directly matches free consumer software with strong interpersonal network effects. The 78% ceiling is therefore the main judgment risk: the 2011 history constrains timing and steepness well, but cannot distinguish a persistent participation ceiling from eventual near-universal use as internet access expands. The fitted curve also reconstructs 2011 at 53.4%, modestly above the observed 50%.
