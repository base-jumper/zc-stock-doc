# Market Analysis Back-Testing

Back-testing calibrates the `market-analysis` skill against historical markets that began as immature
rule-breaker opportunities and later produced important industry leaders. A back-test asks: using
only information available at the subject's historical base year, would the skill have produced
useful 10-year estimates for market value, concentration, and major-player capture?

This document only describes what differs from a normal market-analysis run. Use the
[market-analysis skill](../../SKILL.md) for the body sections and methodology, and the
[market-doc skill](../../../market-doc/SKILL.md) for the front matter schema and storage rules.

## Subject Selection

Choose markets that now have mature or substantially matured industry leaders, but where the selected `base-year` predates obvious hindsight. The base year should be near the point when relevant companies were immature rule-breakers becoming available to public-market investors, such as an IPO year, direct listing year, spin-out year, or the first year when a public pure-play proxy existed.

Prefer subjects with enough historical source material to reconstruct what a diligent investor could have known at the base year. Avoid subjects where the future winner was already obviously dominant or where the market definition is so broad that the later outcome cannot be compared cleanly.

## Available Benchmarks

The benchmark subject set is the set of Markdown files in `data/benchmark`. When running the full
back-test, include every benchmark file unless Nick explicitly asks for a subset.

| Market id | Base year | Benchmark |
|---|---:|---|
| `clear-aligner-orthodontics` | 2001 | [Clear aligner orthodontics](data/benchmark/clear-aligner-orthodontics.md) |
| `crm-software` | 2004 | [Customer relationship management software](data/benchmark/crm-software.md) |
| `sleep-apnea-cpap-therapy` | 1995 | [Sleep apnea and CPAP therapy](data/benchmark/sleep-apnea-cpap-therapy.md) |

## Candidate Subjects

These are candidate subjects for future back-test selection. Treat the base years as provisional public-market anchors to verify before detailed benchmark work.

### Software And Digital Markets

| Market | Base year | Anchor company | Why it is useful |
|---|---:|---|---|
| Online retail and e-commerce | 1997 | Amazon | Tests TAM expansion, long adoption curves, logistics scale, and whether the process could identify an eventual category leader early. |
| Online travel booking | 1999 | Priceline | Tests dot-com-era signal quality, market consolidation, intermediary economics, and eventual mature winner concentration. |
| Paid video streaming and digital home entertainment | 2002 | Netflix | Tests business-model transition from an early public proxy, plus adoption timing and content economics. |
| Search advertising | 2004 | Google | Tests network effects, data advantages, advertising TAM expansion, and high 10-year concentration. |
| SaaS CRM and cloud business software | 2004 | Salesforce | Tests enterprise SaaS adoption, subscription economics, incumbent displacement, and category-leader durability. |
| Battery electric passenger vehicles | 2010 | Tesla | Tests hardware adoption, infrastructure constraints, incumbents versus new entrants, and long-cycle market-value/concentration estimates. |

### Medical, Device, And Hard-Tech Markets

| Market | Base year | Anchor company | Why it is useful |
|---|---:|---|---|
| Robotic-assisted surgery | 2000 | Intuitive Surgical | Tests hardware adoption, hospital capex, surgeon training, recurring instruments, and high 10-year concentration. |
| Continuous glucose monitoring | 2005 | DexCom | Tests regulatory risk, reimbursement, patient behavior, and platform competition against Abbott and Medtronic. |
| Genomic sequencing platforms | 2000 | Illumina | Tests hard-tech life-sciences tools, pricing curves, TAM uncertainty, and durable equipment/platform concentration. |
| Sleep apnea and CPAP therapy | 1995 | ResMed | Tests reimbursement complexity, diagnosis bottlenecks, international expansion, and durable device-market leadership. |
| Stool DNA and non-invasive cancer screening | 2001 | Exact Sciences | Tests diagnostics adoption, reimbursement timing, clinical evidence thresholds, and long commercialization delays. |

## Data Layout

Back-test data lives under `skills/market-analysis/references/back-test/data`.

`data/benchmark` stores one benchmark market doc per subject. Benchmarks describe how the market
actually looked at `base-year + 10` using real historical data. They may use hindsight and
post-base-year sources because they are the answer key, not the simulated forecast.

Each run gets one date-named folder, using `YYYY-MM-DD`. Store generated files inside that folder:

```text
data/
  benchmark/
    <market-id>.md
  YYYY-MM-DD/
    overall.md
    market-docs/
      <market-id>.md
    accuracy/
      <market-id>.md
```

Use the same `<market-id>` for the benchmark, generated market doc, and accuracy doc so the set can be joined mechanically.

## Running A Back-Test

When Nick says "run the market analysis back-test", run the full benchmark set automatically:

1. Read this file, the `market-analysis` skill, and the `market-doc` skill.
2. Create today's run folder: `data/YYYY-MM-DD/market-docs` and `data/YYYY-MM-DD/accuracy`.
3. Spawn one subagent per benchmark subject. Each generated market doc must use
   `maturity-duration: 10`. Each subagent owns exactly two output files:
   `market-docs/<market-id>.md` and `accuracy/<market-id>.md`.
4. Tell every subagent that it is not alone in the codebase, must not revert other edits, and must
   not read `data/benchmark/<market-id>.md` until after it has written its simulated market doc.
5. Wait for all subagents to finish. If a subagent discloses contamination before the simulated doc
   was written, rerun that subject with a clean replacement worker.
6. Generate `overall.md` from the completed run using:

```bash
python3 skills/market-analysis/scripts/backtest_overall.py YYYY-MM-DD
```

The script reads benchmark and generated front matter, recomputes numeric errors, detects
same-direction misses across subjects, compares against the most recent prior dated run when one
exists, and writes aggregate front matter plus a concise Markdown summary.

For each subject, create a market doc using the normal market-analysis methodology with one exception: every research source, fact, estimate, and interpretation must be constrained to information available on or before the subject's `base-year`.

Do not use later filings, later market-share data, later analyst retrospectives, modern company descriptions, current Wikipedia summaries, post-base-year news, or any other source that would reveal how the market actually developed. If a modern page links to historical primary sources, use only the underlying historical source and cite it directly where possible.

When uncertainty would have existed at the base year, preserve it. The back-test should experience the same ambiguity, missing data, hype, weak signals, and false trails that a live `market-doc` run faces.

## Benchmark Docs

Benchmark docs use the same front matter schema as normal market docs, but their job is to record
actual historical outcomes at `base-year + 10`. Use real historical data to estimate:

- actual current and 10-year market value on the same market definition used by the generated doc
- actual 10-year market concentration using HHI where enough share data exists
- actual major-player market-value capture at the 10-year horizon

Document any unavoidable mismatch between the simulated market definition and the observable historical data. The benchmark should make those caveats explicit instead of silently forcing precision.

## Accuracy Docs

Write one accuracy doc per subject in the run folder. The accuracy doc should assess the generated market doc against the benchmark and identify the largest errors.

Each accuracy doc must start with standardized front matter so successive runs can be compared quickly. Error fields are percentages, not decimal shares. Use signed percentage error for direction:

```text
(generated - benchmark) / benchmark * 100
```

A positive error means the generated market doc overestimated the benchmark; a negative error means it underestimated the benchmark. Use `null` when the benchmark value is zero, unavailable, or not comparable, and explain the gap in prose.

Use this front matter:

```yaml
---
market-id: <market-id>
run-date: YYYY-MM-DD
base-year: YYYY
errors:
  mean-absolute-error-pct: 0.0
  current-market-value-error-pct: 0.0
  maturity-market-value-error-pct: 0.0
  hhi-error-pct: 0.0
  player-capture:
    - name: Company Name
      ticker: TICKER
      error-pct: 0.0
---
```

`maturity-duration` is fixed at `10` in both generated and benchmark market docs, so duration is not
an accuracy metric. `mean-absolute-error-pct` is the simple average of the absolute non-null
top-level errors: current market value, 10-year market value (`maturity-market-value`), and HHI. Player-capture errors stay in
`errors.player-capture` and are not included in the headline average unless the skill is deliberately
revised.

Use this structure:

```markdown
# <Market Name> Back-Test Accuracy

## Summary

## Scorecard

## Largest Errors

## What The Skill Missed

## What The Skill Got Right

## Recommendations
```

The scorecard should compare at least current market value, 10-year market value, HHI, and major-player capture. Report directional quality as well as numeric error; a forecast can be useful even when the exact number is wrong if it correctly identifies the market structure, adoption bottleneck, or likely winner set.

Recommendations should be concrete changes to the `market-analysis` skill, the `market-doc` tools,
or the research process. Do not turn every historical miss into a rule; prioritize changes that would
also improve future live market work.

## Overall Doc

After all subject accuracy docs are complete, write `overall.md` at the root of the run folder. Use
`skills/market-analysis/scripts/backtest_overall.py` rather than hand-calculating aggregate metrics.

The front matter is the comparison surface for future methodology changes:

```yaml
---
run-date: YYYY-MM-DD
subject-count: 3
mean-absolute-error-pct: 0.0
median-subject-mae-pct: 0.0
metrics:
  current-market-value:
    mean-signed-error-pct: 0.0
    mean-absolute-error-pct: 0.0
    median-absolute-error-pct: 0.0
  maturity-market-value:
    mean-signed-error-pct: 0.0
    mean-absolute-error-pct: 0.0
    median-absolute-error-pct: 0.0
  hhi:
    mean-signed-error-pct: 0.0
    mean-absolute-error-pct: 0.0
    median-absolute-error-pct: 0.0
consistent-misses:
  - metric: maturity-market-value
    direction: underestimated
    mean-signed-error-pct: -50.0
    mean-absolute-error-pct: 50.0
comparison:
  previous-run-date: YYYY-MM-DD
  previous-mean-absolute-error-pct: 0.0
  mean-absolute-error-change-pct: 0.0
  metric-changes-pct:
    current-market-value: 0.0
    maturity-market-value: 0.0
    hhi: 0.0
---
```

`mean-absolute-error-pct` is the average of the subject-level headline MAEs. Negative
`mean-absolute-error-change-pct` means the current run improved versus the prior run; positive means
it worsened. Metric changes use the same sign convention.

Use this body structure:

```markdown
# Market Analysis Back-Test Overall

## Summary

## Comparison

## Metric Accuracy

## Subject Scorecard

## Consistent Misses

## Subject Details

## Recommendations
```
