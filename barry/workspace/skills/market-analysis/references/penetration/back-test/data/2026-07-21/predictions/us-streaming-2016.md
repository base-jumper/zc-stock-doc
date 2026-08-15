---
subject: us-streaming
base-year: 2016
penetration:
  logistic:
    L: 0.85
    t0: 2013.4386
    k: 0.34550
analogs-used: [us-dvd-player, us-vcr, us-cable-tv, us-home-computer]
w-fit: 0.97444
---

## Reasoning

Paid streaming combines the low installation friction and rapid diffusion of media electronics with
the recurring-payment constraint of cable television. DVD players and VCRs provide fast and medium
media-adoption precedents; cable television is the closest subscription and distribution analog;
home computers provide a deliberately slower, broad-household technology anchor. All four analogs
had reached an observable plateau by 2016.

The ceiling is set at 85% of US households. This sits above cable television and home-computer
penetration because streaming requires little equipment and can serve multiple household members,
but below near-universal media-device ownership because some households will not pay for a video
subscription or will rely on free and linear alternatives.

The seven observations available through 2016 span the apparent midpoint and reach 59% penetration,
well above one-third of the asserted ceiling. The target fit is therefore informative enough to use
the script's uncapped inverse-variance weight of 0.97444. Running `blend` with `--as-of 2016` gives
`k = 0.34550` and `t0 = 2013.4386`, implying projected 2026 penetration of 83.91%.

## Issues

The target series uses top paid services as a proxy for any paid SVOD subscription, so smaller
services may be omitted and overlapping subscriptions do not improve household coverage. The analog
set lacks a mature, low-friction digital subscription product; its hardware-heavy members may
understate streaming's speed, while cable may overstate installation friction. The ceiling remains
the main judgment risk because the observed history had not yet demonstrated the size of the
persistent non-subscriber segment.
