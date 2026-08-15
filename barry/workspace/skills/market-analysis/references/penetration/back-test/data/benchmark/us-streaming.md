---
subject: us-streaming
name: US paid streaming video (SVOD) adoption
unit-basis: US households with at least one of the top SVOD services (Netflix, Amazon Prime Video, and/or Hulu)
measure: stock
realized-ceiling: 0.88
series: series/us-streaming.csv
base-years: [2012, 2014, 2016]
model-form: clean-logistic
quality: benchmark-approximate
---
# US Paid Streaming Video (SVOD) Benchmark

The answer key for the streaming penetration back-test: realized share of US households subscribing to at
least one paid SVOD service, with Netflix as the anchor. A clean S-curve — from ~16% of households in
2010 to a plateau in the low-to-mid 80s by 2022-2023. Netflix seeded the category (streaming launched
2007, in 28% of households by 2011); Amazon Prime Video and Hulu, then Disney+/HBO/Paramount+, broadened
it into a near-utility.

**Basis.** Penetration is measured on US households (not adults). The frozen series uses Leichtman
Research Group's (LRG) long-running "% of US households with a top SVOD service (Netflix, Amazon Prime
Video, and/or Hulu)" — the most consistent multi-year series available and a close proxy for "at least
one paid SVOD". This top-three proxy modestly undercounts the true "any paid streaming" figure at the
tail (households subscribing only to Disney+, HBO Max, Paramount+, etc.): by 2024 the top-three measure
was ~83% while "at least one of any streaming service" was ~86%. `realized-ceiling` is set to 0.88 —
above the 0.83 series max (required for the logit fit) and consistent with the higher "any streaming"
saturation the market is approaching.

**Base-years** are 2012, 2014, 2016, spanning the blend regimes:
- 2012 (~0.36, three points on or before the base-year → prior/analog-dominated; the script falls back
  to prior-only below four points).
- 2014 (~0.47, blended — five points, mid-inflection).
- 2016 (~0.59, fit-dominated — seven points, past the steepest rise).

Each cell scores to `base-year + 10`. **Short-window caveat:** this market matured recently, so the
latest base-year's effective forecast window is shorter than ten years. The 2016 cell scores to 2026,
but the realized series plateaus by ~2022 and the frozen data ends 2024 (held flat thereafter by the
scorer) — so the last ~2-3 years of that window are plateau, not fresh adoption. This is expected for a
subject whose S-curve completes within the back-test's own recency window and is not a data gap.

**Analog note.** Admissible analogs (plateaued by the base-year) for a 2012-2016 base are one-generation-
back media-distribution diffusions — DVD, cable TV, home broadband, VCR — which is the right vintage
match for a streaming forecast.

Quality: LRG figures (2011, 2014-2024) are confirmed via LRG's press releases and their reputable
secondary coverage; the 2010, 2012, 2013, and 2021 points are Netflix-anchored estimates/interpolations
between LRG readings. Because part of the series is estimated rather than drawn point-by-point from a
primary release, the flag is `benchmark-approximate`. Estimated points are marked in the CSV.

## Sources
- Leichtman Research Group, annual SVOD studies — % of US households with a top SVOD service (Netflix,
  Amazon Prime Video and/or Hulu): 2015: 52%, 2016: 59%, 2017: 64%, 2018: 69%, 2019: 74%, 2020: 78%,
  2022: 83%, 2023: 83%. Reported via TV Tech and NewscastStudio.
  https://www.tvtechnology.com/news/top-three-svod-services-are-in-78-of-us-households
  https://www.newscaststudio.com/2023/08/09/over-80-of-u-s-households-now-subscribed-to-svod-service/
- Leichtman Research Group (Mar 2024) — 86% of US households have at least one streaming video service;
  88% including 15 top SVOD/DTC services; top-three SVOD ~83%. Reported via MediaPost.
  https://www.mediapost.com/publications/article/388097/household-share-dominance-of-netflix-amazon-hulu.html
- Leichtman Research Group — Netflix in 28% of US households (2011), rising to 44% (2014); early SVOD
  household penetration anchor. Reported via Media Play News / StreamTV Insider.
  https://www.streamtvinsider.com/programming/new-study-finds-more-americans-splitting-their-streaming-budget
- 2010, 2012, 2013, 2021: Netflix-anchored ESTIMATES/interpolations between LRG readings (Netflix ended
  2010 at ~20M US members ≈ 16% of households; 2021 interpolated between the 2020 and 2022 LRG figures).
  Flagged in the CSV.
