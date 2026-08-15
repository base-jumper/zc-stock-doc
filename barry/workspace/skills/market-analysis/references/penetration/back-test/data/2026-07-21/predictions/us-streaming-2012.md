---
subject: us-streaming
base-year: 2012
penetration:
  logistic:
    L: 0.85
    t0: 2012.9706306746
    k: 0.3176299366
analogs-used: [us-dvd-player, us-vcr, us-cable-tv, us-home-computer]
w-fit: 0.0
---

## Reasoning

Paid streaming rides households' existing televisions and broadband connections, so adoption should
face less installation and purchase friction than cable television or home computers. DVD players
provide a fast media-adoption analog, while VCRs, cable television, and home computers provide
slower anchors and guard against extrapolating the early takeoff too aggressively. A ceiling of 85%
allows streaming to exceed cable's historical reach because it does not require a dedicated home
installation, while retaining a non-subscriber segment for households unwilling or unable to pay
for another media service.

The target history available through 2012 has only three observations, which is insufficient for a
target fit. The blend therefore uses the analog prior at full weight (`w-fit: 0.0`) and anchors it to
the observed 2012 penetration of 36%. Running the blend with `--as-of 2012` gives `k = 0.31763` and
midpoint `2012.9706`, projecting penetration of 80.43% in 2022.

## Issues

The forecast is prior-only because the target series has fewer than four observations. No close,
mature software-subscription analog was available by 2012; the chosen analogs span the relevant
media and household-technology mechanisms but all involve more hardware or installation friction.
The asserted ceiling is therefore the largest judgment uncertainty.
