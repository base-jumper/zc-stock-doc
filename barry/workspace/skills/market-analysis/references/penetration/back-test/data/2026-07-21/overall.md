---
run-date: '2026-07-21'
cell-count: 12
mean-path-mae-pp: 6.45
median-path-mae-pp: 6.13
mean-ceiling-error-pp: 1.92
mean-model-form-floor-pp: 1.65
mean-forecast-gap-pp: 6.49
---
# Penetration Back-Test Overall

## Summary

12 cells across 4 subjects. Mean path MAE 6.5 pp,
median 6.1 pp. Mean model-form floor 1.6 pp
(irreducible); mean forecast gap 6.5 pp (judgment).

## Cells

| Subject | Base year | Path MAE (pp) | Horizon err (pp) | Ceiling err (pp) | Floor (pp) | Gap (pp) |
|---|---:|---:|---:|---:|---:|---:|
| us-smartphones | 2010 | 1.8 | +0.0 | -8.0 | 4.3 | 3.1 |
| us-smartphones | 2013 | 7.5 | -0.1 | -3.0 | 2.7 | 7.8 |
| us-smartphones | 2015 | 3.1 | -1.2 | -3.0 | 2.1 | 2.7 |
| us-social-media | 2008 | 4.3 | +1.5 | +1.0 | 2.4 | 2.3 |
| us-social-media | 2011 | 7.4 | +5.8 | +4.0 | 1.0 | 7.7 |
| us-social-media | 2014 | 8.3 | +7.6 | +6.0 | 0.7 | 8.0 |
| us-streaming | 2012 | 5.1 | -1.4 | -3.0 | 0.9 | 5.0 |
| us-streaming | 2014 | 1.8 | -0.5 | -3.0 | 0.8 | 1.3 |
| us-streaming | 2016 | 1.5 | +0.1 | -3.0 | 0.9 | 1.3 |
| us-tablets | 2013 | 19.3 | +21.9 | +20.0 | 2.2 | 21.0 |
| us-tablets | 2015 | 10.3 | +11.7 | +10.0 | 1.4 | 11.0 |
| us-tablets | 2017 | 7.2 | +6.9 | +5.0 | 0.5 | 6.8 |

## Reading This Run

- Within a subject, path MAE should fall as the base-year advances — that is the blend claim
  (priors early, fit late) working. Where it does not, inspect the cell.
- A high model-form floor flags a market the logistic cannot represent; a high forecast gap with a
  low floor flags a judgment miss (usually ceiling).
- Ceiling error is the leakage-sensitive lever: a suspiciously small ceiling error at an early
  base-year may indicate hindsight crept into the ceiling assertion.

## Recommendations

The logistic form was generally sound: the mean model-form floor was only 1.6 pp, while the 6.5 pp
mean forecast gap shows that judgment inputs dominate total error. Streaming was consistently strong
(1.5–5.1 pp MAE), and smartphones were acceptable except for the 2013 near-inflection overfit.

The principal weakness is ceiling selection. Tablets were overestimated by 20, 10, then 5 pp as
their slowdown became visible; social media was also increasingly overestimated as high fit weights
were applied before a durable plateau was established. Three changes should improve live work:

1. Require a low-ceiling sensitivity for products with substantial functional overlap or a plausible
   structural non-user segment.
2. Treat statistical fit weight as distinct from extrapolation confidence: flag or cap near-full
   weights when history is short, lacks sustained deceleration, or ends before the analysis year.
3. Expand the verified analog library with mature mobile devices, free network-effect software, and
   low-friction digital subscriptions. Keep the fewer-than-four-points prior fallback; its streaming
   results were strong.

Do not add a general era-speed correction from this run. Misses were not consistently slow; ceiling
and anchoring errors explain the material failures more directly.
