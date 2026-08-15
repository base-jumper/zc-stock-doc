# Penetration Back-Testing

Calibrates the [penetration sub-skill](../penetration.md) against markets that have already run their
adoption curve. Each test forecasts a mature market's penetration path from a historical base-year,
using only information available then, and scores the projection against what actually happened.

This document describes only what differs from a normal penetration run. Use the penetration sub-skill
for the method and the script.

## What Is Being Tested

Two distinct things, which the scoring keeps separate:

1. **Judgment** — the inputs the forecaster supplies: analog selection, the asserted ceiling, the
   target-series definition, and any blend-weight override. The logistic fit itself is deterministic
   given these, so the judgment inputs are the real variable.
2. **Method validity** — whether a logistic even describes the market. Perfect judgment cannot save a
   forecast of a market that does not follow an S-curve. Every cell is therefore compared against a
   **hindsight-optimal logistic** (the best logistic fit to the full realized series). Its residual is
   the *model-form floor* — the irreducible error. The remainder, the gap between the forecaster's
   base-year curve and that best logistic, is the *forecast gap* — the judgment component.

## Two Leakage Channels

The market-analysis back-test only has to keep the subject's future out. Penetration has a second
channel: **the analog library**. An analog's stored `ceiling-estimate` is its *known mature* ceiling —
using an analog that had not yet plateaued by the base-year borrows a ceiling that was not observable
then. Admissibility is therefore stricter than "series ends before the base-year": the analog must have
reached its plateau (≥90% of ceiling) by the base-year.

This is enforced mechanically. `penetration_fit.py blend --as-of YEAR` truncates every series at YEAR
and drops any analog not yet plateaued by then; it also drops the subject's own series if it appears in
the library. Always pass `--as-of <base-year>` in a back-test. The forecaster must still avoid
*judgment* leakage — do not eyeball the post-base-year trajectory when defining the target series or
asserting the ceiling.

## Base-Year Recency And The Acceleration Effect

Diffusion has accelerated across generations, so a mid-century analog systematically under-predicts a
modern market's steepness. A back-test is only a fair proxy for live use when its *analog-vintage gap*
matches live use: forecasting a 2026 market today draws on analogs that matured ~2020, one generation
back. So back-test base-years are kept recent (≈2008-2015), which makes their admissible analogs the
one-generation-back set (DVD, VCR, cable, home computer) rather than mid-century appliances. Any residual
slow-bias then shows up as a consistent under-prediction of steepness across cells — a measured quantity
that would justify an era correction in the skill, rather than a guess.

## Subjects And Scenarios

A cell is a (subject, base-year) pair. Each subject is run at three base-years spanning the blend
regimes — few early points (prior/analog dominated), mid-inflection (blended), post-inflection (fit
dominated) — so a single subject's cells test the core claim that priors dominate early and the fit
takes over as history accumulates. Within a subject, path MAE should fall as the base-year advances.

Benchmarks live in `data/benchmark/`: one `<subject>.md` (front matter + narrative + sources) and the
frozen realized series in `data/benchmark/series/<subject>.csv`. These are answer keys, kept separate
from the mutable analog library even where a subject is also an analog.

| Subject | Base-years | Ceiling | Role |
|---|---|---:|---|
| `us-smartphones` | 2010, 2013, 2015 | ~0.91 | Clean high-ceiling logistic — the well-behaved case. |
| `us-social-media` | 2008, 2011, 2014 | ~0.73 | Clean logistic with a low ceiling; tests holding the ceiling *down* against higher-ceiling analogs. |
| `us-tablets` | 2013, 2015, 2017 | ~0.54 | Adversarial: adoption looked smartphone-like then stalled. Tests ceiling judgment; the trap is asserting a high ceiling at 2013. |
| `us-streaming` | 2012, 2014, 2016 | ~0.88 | Clean logistic (paid SVOD, household basis) that matured recently; the latest base-year's forecast window runs past saturation — an intentionally short effective window. |

Adding subjects is encouraged as the library grows. The highest-value gap is a genuine **model-form
breaker** — a boom-then-decline stock (MP3 players, standalone GPS) that no logistic can represent, which
would exercise a high model-form floor. It needs a well-documented series before it can be added.

## Metrics

All in penetration points (pp), not relative %. Per cell, `penetration_backtest.py` computes:

- **path MAE** — mean absolute pp error across the forecast window (base+1 to base+10).
- **horizon error** — signed pp error at base+10 (+ over-, − under-predicted).
- **ceiling error** — asserted minus realized ceiling; the leakage-sensitive lever.
- **timing error** — years to half the realized ceiling, predicted minus actual.
- **model-form floor** and **forecast gap** — the decomposition above.

## Running A Back-Test

When Nick says "run the penetration back-test":

1. Read this file and the penetration sub-skill.
2. Create the run folder `data/<today>/predictions/`.
3. For each benchmark subject and each of its `base-years`, spawn a forecaster subagent for that cell.
   Tell each subagent: it forecasts one cell; it must use `--as-of <base-year>`; it must not read the
   benchmark series beyond the base-year or use any post-base-year knowledge when choosing analogs,
   defining the target series, or asserting the ceiling; it owns exactly one file,
   `predictions/<subject>-<base-year>.md`; and it is not alone in the codebase.
4. Each prediction doc carries this front matter plus a short body (Reasoning, and an **Issues** section
   noting anything that made the forecast hard — a missing fast analog, an ambiguous ceiling, a noisy
   series):

   ```yaml
   ---
   subject: <subject>
   base-year: <YYYY>
   penetration:
     logistic:
       L: 0.0
       t0: <YYYY.0>
       k: 0.0
   analogs-used: [<id>, <id>]
   w-fit: 0.0
   ---
   ```

5. After all cells are written, score the run:

   ```bash
   python3 skills/market-analysis/scripts/penetration_backtest.py score <today>
   ```

   This writes one `accuracy/<subject>-<base-year>.md` per cell (metrics front matter + scorecard, with
   Attribution and Issues sections left for synthesis) and `overall.md`.
6. As orchestrator, fill each accuracy doc's **Attribution** (model-form vs judgment, which lever
   dominated) and the **Recommendations** — pulling from subagents' Issues sections and the numbers.
   Propose skill changes only where they would also improve live work; do not turn every historical
   miss into a rule.

The generated artifact per cell is a focused penetration prediction, not a full market doc — the
back-test isolates the adoption curve, not size, TAM, or price.
