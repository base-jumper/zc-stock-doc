---
subject: us-tablets
name: US tablet ownership
unit-basis: US adults
measure: stock
realized-ceiling: 0.55
series: series/us-tablets.csv
base-years: [2013, 2015, 2017]
model-form: low-ceiling-stall
quality: benchmark-approximate
---
# US Tablet Ownership Benchmark

The adversarial subject. Tablet ownership rose fast from the 2010 iPad launch — 3% to 42% by early 2014,
looking smartphone-like through 2013 — then stalled around 0.50-0.53 as phablets and large phones
absorbed the use case. `realized-ceiling` is 0.55, just above the 0.53 observed plateau (strict
ceiling>max requirement) and far below where the early trajectory and consumer-hardware analogs point.

This is a ceiling-judgment trap, not primarily a model-form failure: a logistic *can* fit a low-ceiling
stall, so the hindsight-optimal logistic floor is low. The discriminating question is whether the
forecaster, at 2013, resisted asserting a smartphone-like ceiling. Expect the error to be dominated by
the `forecast-gap` (judgment) rather than the `model-form floor`, and to shrink sharply at the 2015 and
2017 base-years once the stall is visible in the data.

Base-years: 2013 (~0.34 and still climbing — the trap), 2015 (~0.45, stall emerging), 2017 (~0.51,
stall visible), each scored to `base-year + 10`. Base-years are unchanged; the corrected Pew data
preserves their regime roles.

A true model-form breaker — a boom-then-decline stock such as MP3 players or standalone GPS units, which
no logistic can represent — is a valuable future addition once a well-documented series is sourced. See
back-test.md.

Quality: 2010-2016 are verified against Pew's standalone tablet-ownership readings. The flag stays
`benchmark-approximate` for two reasons: the 2011 point is an approximate early-2011 Pew reading, and
Pew discontinued the single tablet trend line after 2016 — the 2019 (0.52) and 2021 (0.53) points are
DERIVED by aggregating Pew's per-generation / per-age tablet-ownership breakdowns rather than taken from
a single published figure. Post-2016 points are flagged in the CSV.

## Sources
- Pew Research Center, "25% of American Adults Own Tablet Computers" (Oct 2012) — 2010: ~3% (Sep 2010),
  2012: 25%. https://www.pewresearch.org/internet/2012/10/04/25-of-american-adults-own-tablet-computers/
- Pew Research Center, "Tablet and E-reader Ownership" (Jan 2014) — 42% as of Jan 2014, up 8 pts from
  September 2013 (34%). https://www.pewresearch.org/internet/2014/01/16/tablet-and-e-reader-ownership-2/
- Pew Research Center, "Technology Device Ownership 2015" — tablet ownership 45% (2015).
  https://www.pewresearch.org/internet/2015/10/29/technology-device-ownership-2015/
- Pew Research Center, "Record shares of Americans have smartphones, home broadband" (Jan 2017) —
  tablet ownership rose to 51% as of Nov 2016.
  https://www.pewresearch.org/short-reads/2017/01/12/evolution-of-technology/
- Pew Research Center, "Millennials stand out for their technology use" (Sep 2019) and "Share of those
  65 and older who are tech users has grown" (Jan 2022) — per-generation/age tablet breakdowns from
  which the 2019 (~52%) and 2021 (~53%) all-adult figures are derived.
  https://www.pewresearch.org/short-reads/2019/09/09/us-generations-technology-use/
