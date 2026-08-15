---
name: market-analysis
description: Minimal methodology for researching markets and producing the body/front-matter assumptions that go into a market-doc. Use when Nick asks for fresh market research, a market deep dive, market sizing, 10-year market projection, market concentration, player capture estimates, market-doc content generation, or to run/assess the market analysis back-test.
---

# Market Analysis

How we research a market and write up the findings. This skill owns the **methodology** and the
**body** of a market-doc; the [market-doc skill](../market-doc/SKILL.md) owns the file name, the
front matter schema, and the tools for working with stored docs. Produce the analysis here, then
write it into the market-doc.

## Principles

- Use your own judgement to generate the required output. Keep the process simple for now.
- Separate facts from interpretation.
- State uncertainty and source quality.
- Include sources/citations where possible.
- Be concise and decision-useful.
- Reconcile the prose with the front matter before saving.
- Always use a fixed 10-year projection horizon: `maturity-duration: 10`.
- Keep player capture estimates internally consistent with the concentration estimate. If the HHI
  implies a winner-take-most market but the capture table implies fragmentation, resolve the
  contradiction before saving.

## Analysis Output

Generate the market-doc front matter values and body sections using the schema and storage rules in
the [market-doc skill](../market-doc/SKILL.md). Estimate the market's current market value, 10-year
projected market value, expected concentration at the 10-year horizon, and major-player market-value
capture at the 10-year horizon.

Do not estimate when the market will become mature. Use `base-year + 10` as the projection year for
every market. In prose, explain what the 10-year market state is expected to look like, why the
market-value and HHI estimates are reasonable for that horizon, why each major player can win or lose
capture, and what developments would change the stored assumptions.

## Market Contract

Define one market contract before running any sub-skill. This is a research-time interface, not
additional market-doc front matter. State it in the *Market Definition* section and use it unchanged
throughout the analysis:

- **Market scope:** geography, included products and use cases, and explicit exclusions.
- **Revenue boundary:** whose recognized revenue is measured and at which point in the value chain;
  distinguish vendor or manufacturer revenue from customer spend, GMV, and channel revenue.
- **Addressable unit:** the stable denominator that could structurally adopt, such as a person,
  patient, household, business, seat, vehicle, site, unit of capacity, or unit of spend/activity.
- **Penetration measure:** the numerator and denominator of adoption, classified as `stock`,
  `new-sales-share`, or `spend-share`.
- **Billable units:** the units to which price or recurring revenue applies; each may differ from
  the addressable unit.
- **Segments:** any customer, product, or geographic groups that require materially different
  adoption or monetization assumptions, plus the rule for aggregating them to the whole market.
- **Time and value basis:** base year, 10-year horizon, currency, and whether values are nominal or
  expressed in constant base-year currency.

Normalize evidence to this contract or disclose the mismatch; never silently change definitions
between sub-skills. The parent workflow owns the contract and orchestration. Sub-skills consume the
contract and return their own outputs without invoking or reproducing one another's methodology.

## Refreshing Stored Calculations

After updating analyst-owned market-doc inputs, preview every configured calculation with:

```bash
skills/market-analysis/scripts/market_analysis.py refresh <MARKET_ID> --dry-run
```

Review the output, then omit `--dry-run` to save it. Use `--as-of YYYY-MM-DD` when the calculation
date should differ from today and `--json` when structured output is useful.

The command runs concentration, penetration, and mobility in dependency order, passing newly
calculated concentration through to mobility even during a dry run. A calculation runs only when
its inputs exist; optional unconfigured calculations are reported as skipped. The prospective
combined front matter is validated before any write. A saving run then builds and validates the
updated document in a staging file before replacing the original, so a calculation, validation, or
writer failure cannot leave a partial refresh. Market size remains an analyst-owned research output.

This is the normal market-doc calculation entry point. Use individual sub-skill commands only when
diagnosing or maintaining a model.

## Penetration Estimation

Estimate the 10-year adoption level from a logistic curve using
[references/penetration/penetration.md](references/penetration/penetration.md). That sub-skill fits
a logistic S-curve to an observed adoption measure, blends it with priors from a growing library of
historical analogs, and supports the market-doc penetration block and *Adoption Path* section. Put
the target series, measure, ceiling, analogs, and optional fit-weight judgment under
`penetration.inputs`, then run the parent refresh command. The penetration script writes
`penetration.model-estimate`, resolves an optional complete `penetration.override`, and returns the
annual adoption path through the 10-year horizon without storing that derived path. It does not
define the market contract, addressable-base quantities, unit economics, or market value.

## Size Estimation

Use the [size sub-skill](references/size/size.md) for the existing
`size.current-market-value` and `size.maturity-market-value` outputs. It accepts the market contract
and annual adoption path supplied by the parent workflow, then owns addressable-base projections,
unit economics, and the bridge to current and 10-year market value.

## Concentration Estimation

Derive the 10-year `concentration.model-estimate` and `concentration.hhi`
from the market's structural traits rather than guessing them directly, using
[references/concentration/concentration.md](references/concentration/concentration.md). That
sub-skill scores the market on winner-take-most and entry-barrier traits, maps the scores to the two
parameters `s1` and `r` of a geometric rank-share law, and yields the whole-market HHI and ranked
share curve mobility uses for player capture. Store all seven trait scores under
`concentration.inputs.traits`, then run the parent refresh command. The concentration script writes
the unadjusted `model-estimate` and derives HHI from the optional complete
`override` when present, otherwise from `model-estimate`. Do not adjust HHI separately. Multiplying
a player's capture by `size.maturity-market-value` gives its projected revenue, so the
concentration boundary must match the size boundary.

## Rank Mobility

Concentration predicts the horizon share *vector*, not which of today's players lands in which
rank. Apply the mobility sub-skill using its
[runbook](references/mobility/mobility.md); its model and corpus are documented separately in the
[calibration reference](references/mobility/calibration.md).
Store the current whole-market top-K ranking and shares under `players.inputs.current`, then run the
parent refresh command. The mobility script combines the fitted transition rows
with canonical concentration and writes both hold-position and mobility-adjusted capture under
`players.model-estimate`, plus mobility-adjusted revenue from the predicted market value. It values
the aggregated fringe from the geometric concentration tail; gone contributes zero and is already
included. Report both views in the *Players* section and use an explained per-player override for
company-specific evidence or a named outside contender.
The model is a coarse pooled base rate. It sees current rank and share spacing, but not a specific
company's momentum or moat.

## Peer Comparison

Run this final step only after completing and saving the analysis. Search market participants,
industry or government bodies, and market-research analysts for comparable projections. Prefer
5–10 year forecasts and market value; also capture useful revenue, share, concentration, TAM,
adoption, or volume estimates.

Under *Peer Comparison*, record each useful publication's publisher, date, link, forecast horizon,
figures, units, currency, and market boundary. Distinguish vendor revenue, customer spend, GMV, and
TAM; flag scope or horizon mismatches instead of presenting them as directly comparable. Prefer the
underlying publication to search snippets and label any calculated CAGR or currency conversion.
For each source, lead with `X% over/under our estimate` at the same forecast year, interpolating our
path when needed; label boundary-mismatched arithmetic as not comparable. Retain the detailed basis
and include credible disagreements. If no meaningful long-term comparison is found, say so.

Use peer data only as a benchmark: do not change prior findings or model inputs during this run. If
Nick later chooses a peer-informed input or override, document the source and rationale, then rerun
the normal dry-run and saving refresh. For back-tests, enforce the information cutoff and do not read
the hindsight benchmark.

## Documenting The Analysis

Write the findings into the market-doc using these sections, in order:

```markdown
# Market Name

## Market Definition

## Current View

## Adoption Path

## Market Structure

## Players

## Watch

## Peer Comparison

## Sources
```

Keep the prose focused on explaining the front matter.

## Back-Testing

For historical calibration runs, use [references/back-test/back-test.md](references/back-test/back-test.md).
Back-tests use the normal market-analysis methodology except that they run from a historical
`base-year`, must avoid post-base-year information leakage, and compare generated market docs
against hindsight benchmarks.

When Nick says "run the market analysis back-test", follow that reference's orchestration workflow:
create today's run folder, spawn one worker per benchmark subject, then generate `overall.md` after
all subject market docs and accuracy docs are complete.
