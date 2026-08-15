---
subject: us-smartphones
name: US smartphone ownership
unit-basis: US adults
measure: stock
realized-ceiling: 0.93
series: series/us-smartphones.csv
base-years: [2010, 2013, 2015]
model-form: clean-logistic
quality: benchmark-approximate
---
# US Smartphone Ownership Benchmark

The answer key for the smartphone penetration back-test: realized share of US adults owning a
smartphone. A clean, high-ceiling logistic — the well-behaved case. The iPhone launched in 2007 at
low single-digit penetration; Pew's tracking opens at 35% in 2011, adoption crossed ~50% in 2013, and
it plateaued at 90-91% by the mid-2020s. `realized-ceiling` is set to 0.93, a couple of points above
the observed 0.91 plateau to satisfy the logit fit's strict ceiling>max requirement.

The three base-years span the blend regimes: 2010 (four early points, penetration ~0.24, prior/analog
dominated), 2013 (mid-inflection ~0.56, blended), 2015 (post-inflection ~0.68, fit dominated). Each cell
is scored to `base-year + 10`. Base-years are unchanged from the original transcription — the corrected
Pew data leaves their regime roles intact.

Era note: admissible analogs must have plateaued by the base-year. For a 2010 base-year the era-matched
priors are DVD player, VCR, cable TV, and color TV — the modern fast diffusions (this same smartphone
series, internet, social media) are correctly excluded by `--as-of` because their ceilings were not yet
observable.

Quality: the Pew span (2011-2025) is verified point-by-point against the sources below. The four
pre-2011 points (2007-2010) predate Pew's series and are ESTIMATES retained as bridge points so the 2010
base-year cell has enough early observations to fit; because part of the series is estimated rather than
primary-sourced, the flag stays `benchmark-approximate`. The estimated points are marked in the CSV.

## Sources
- Pew Research Center, Mobile Fact Sheet — smartphone ownership among US adults (2011: 35%; 2016: 77%;
  2019: 81%; 2021: 85%; 2023: 90%; 2024: 91%; 2025: 91%).
  https://www.pewresearch.org/internet/fact-sheet/mobile/
- Pew Research Center, "Record shares of Americans have smartphones, home broadband" (Jan 2017) —
  2011: 35%, 2016: 77%. https://www.pewresearch.org/short-reads/2017/01/12/evolution-of-technology/
- Pew intermediate readings: 2012: 46% ("Nearly half of American adults are smartphone owners", Mar 2012);
  2013: 56% ("Smartphone Ownership 2013", Jun 2013); 2014: 58%; 2015: 68% (device-ownership reports).
  https://www.pewresearch.org/internet/2013/06/05/smartphone-ownership-2013/
- Pew Research Center, "Mobile Technology and Home Broadband 2021" — 2019: 81%, 2021: 85%.
  https://www.pewresearch.org/internet/2021/06/03/mobile-technology-and-home-broadband-2021/
- Pre-2011 (2007-2010) ESTIMATED from contemporaneous Nielsen/comScore US smartphone device reports
  (~5% of adults in 2007 rising to ~24% by 2010); not a primary Pew series. Flagged in the CSV.
