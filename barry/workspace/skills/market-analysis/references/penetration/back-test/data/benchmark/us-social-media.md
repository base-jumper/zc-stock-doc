---
subject: us-social-media
name: US social media use
unit-basis: US adults
measure: stock
realized-ceiling: 0.74
series: series/us-social-media.csv
base-years: [2008, 2011, 2014]
model-form: clean-logistic
quality: verified
---
# US Social Media Use Benchmark

Realized share of US adults using at least one social media site. A clean logistic with a distinctly
sub-1.0 ceiling: adoption climbed steeply from 7% in 2005 and flattened at ~72% by 2019-2021. This
subject tests whether the method holds the ceiling down when the analogs it is handed have higher
ceilings — the mirror image of the tablet trap. `realized-ceiling` is 0.74, just above the 0.72
observed plateau (strict ceiling>max requirement).

Base-years: 2008 (~0.25, prior dominated), 2011 (~0.50, blended), 2014 (fit dominated), each scored to
`base-year + 10`. Base-years are unchanged; the corrected Pew data preserves their regime roles. Note
the series has no separate 2014 point (Pew's readings that year land on the 2013 value, 0.62) — the
2014 base-year cell fits on the 2005-2013 span and anchors at 0.62, consistent with its "fit dominated"
role.

Every point is Pew Research Center. Pew reported a combined "% of US adults who use any social media"
metric through 2021 (72%) and then shifted to per-platform reporting, so the realized series ends at
2021. The plateau held near 72% thereafter (in 2023 YouTube alone reached 83% and Facebook 68%), so the
scorer's flat-hold beyond the last point is the correct realized behaviour for the 2014 cell's window
(to 2024). Because every data point is confirmed against a cited primary source, the flag is `verified`.

## Sources
- Pew Research Center, "Social Media Usage: 2005-2015" (Oct 2015) — annual trend: 2005: 7%, 2006: 11%,
  2008: 25%, 2009: 38%, 2010: 46%, 2011: 50%, 2012: 55%, 2013: 62%, 2015: 65%.
  https://www.pewresearch.org/internet/2015/10/08/social-networking-usage-2005-2015/
- Pew Research Center, Social Media Fact Sheet / "Social media use" trend chart — 2016: 69%, 2018: 69%,
  2019: 72%, 2021: 72%. https://www.pewresearch.org/internet/fact-sheet/social-media/
- Pew Research Center, "Social Media Use in 2021" — 72% of US adults use at least one social media site.
  https://www.pewresearch.org/internet/2021/04/07/social-media-use-in-2021/
