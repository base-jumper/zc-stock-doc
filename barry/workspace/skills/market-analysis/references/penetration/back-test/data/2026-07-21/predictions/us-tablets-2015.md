---
subject: us-tablets
base-year: 2015
penetration:
  logistic:
    L: 0.65
    t0: 2013.1002
    k: 0.6553876732
analogs-used: [us-dvd-player, us-vcr, us-cable-tv, us-home-computer]
w-fit: 0.7599962894
---

# US Tablet Penetration Forecast — 2015

## Reasoning

The observed series rose from 3% of US adults in 2010 to 45% in 2015, but growth slowed from eight percentage points in 2014 to three points in 2015. I therefore assert a 65% ceiling: tablets are easier to acquire than PCs, but they overlap substantially with smartphones and computers and are not necessary for every adult.

The analog set spans fast upgrade hardware (DVD players), medium-speed consumer electronics (VCRs), a recurring-fee product with a sub-universal ceiling (cable TV), and slower general-purpose hardware (home computers). All four had reached their indexed plateaus by 2015. The blend was run with `--as-of 2015`; its statistical fit weight of 0.759996 was retained because the target already had six observations and had moved beyond the early-adopter portion of the asserted ceiling. The resulting logistic has `k = 0.655388`, midpoint 2013.1002, and projects 64.97% penetration in 2025.

## Issues

The ceiling is the dominant uncertainty. By 2015, tablets combined rapid early adoption with an emerging slowdown, but the available history could not distinguish durable saturation from a temporary pause or replacement-cycle effects. The analog library also lacked a close prior for a secondary personal device whose functionality substantially overlaps two already widespread device categories.
