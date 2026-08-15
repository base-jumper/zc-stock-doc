# Rank Mobility Runbook

Use rank mobility to convert today's leading-player shares and the predicted concentration curve
into player capture at the fixed 10-year horizon. The script owns both the transition estimate and
its combination with canonical concentration.

## When to Use It

Run mobility after the market contract and current player ranking are established. The ranking
must use the same market boundary and share basis as the concentration estimate. Apply the model
only to players currently ranked `1..5`; it is not calibrated for deeper origins.

Do not run mobility when a defensible current ranking cannot be established. Disclose material
basis mismatches rather than silently mapping a player from a different market definition.

## Prepare the Market Doc

Under `players.inputs.current`, record the current top two to five players with contiguous ranks,
names, optional tickers, and descending whole-market shares. Use the same market boundary and share
basis as concentration. Do not substitute shares of only the named subset.

Canonical concentration must already exist as `concentration.override` or
`concentration.model-estimate`. Its geometric rank-share curve must have total modeled mass no
greater than one. `size.maturity-market-value` must contain the predicted 10-year market value in
billions of the market doc's top-level currency.

## Run the Production Estimate

Calculate without writing first:

```bash
scripts/mobility_fit.py predict --market-doc <MARKET_ID> --dry-run
```

Review the current ranking, concentration selection, hold-position versus mobility-adjusted
capture, and implied revenue, then rerun without `--dry-run`. The script writes only
`players.model-estimate`,
`gone-probability`, `method`, and `date`; it preserves inputs, overrides, unrelated front matter,
and the body.

For model diagnostics outside a market doc, predict all five incumbent rows directly:

```bash
scripts/mobility_fit.py predict --coverage 5 --shares 0.62,0.18,0.09,0.05,0.03 --json
```

To return one current rank only:

```bash
scripts/mobility_fit.py predict --coverage 5 --shares 0.62,0.18,0.09,0.05,0.03 --rank N --json
```

In raw mode, `--shares` is required by the production `share` model and must contain exactly `coverage`
positive 0–1 fractions, ordered from current rank 1 through rank K. Values must use the same
whole-market boundary and basis as the current ranking; they need not sum to one because players
below K are omitted.

Use the default `share` model for production. `rank` is the no-share fallback; `constant` and
`maturity` are diagnostics. Do not substitute a fallback without a methodology decision recorded in
[calibration.md](calibration.md).

`predict` recalibrates from the current corpus on every call. Calibration intentionally includes
both `verified` and `seed-approximate` panels because verified coverage is still sparse.

## Read the Output

For each player, `hold-position-capture` is the canonical concentration share at its current rank.
`mobility-adjusted-capture` is its expected capture after weighting the complete geometric
rank-share curve by the transition model. Named destination ranks are weighted directly. The
aggregated `fringe` state receives the analytically weighted geometric tail beyond the named ranks;
`gone` receives zero.

`mobility-adjusted-revenue` is the mobility-adjusted capture multiplied by
`size.maturity-market-value`. It is expressed in billions of the top-level `currency` and remains a
model view even when an analyst-owned player override is canonical.

Canonical player capture is an entry in `players.override` when one matches the player, otherwise
the model's mobility-adjusted capture. An override can also add a named outside contender. Every
override needs a direct capture and a reason.

For each origin rank, `rows` gives probabilities for:

- `1..5`: the player's rank at the horizon;
- `fringe`: still present but below rank 5;
- `gone`: exited, defunct, or absorbed.

The full rows are returned in JSON diagnostics but are not stored in front matter. Each incumbent
row sums to 1. `relative-share-gaps` reports each incumbent's distance from its
nearest adjacent named rank, divided by its own share. A wider gap reduces fitted churn. `g` is the
common gone probability and is already included in every row; do not apply it as a second discount.

When all five rows are requested, `from-outside` reports the residual probability that each future
top-five rank is occupied by a player outside today's top five. It is a per-destination residual,
not another player's transition row.

## Write Up

In the *Players* section:

- state the current share source and boundary;
- compare hold-position and mobility-adjusted capture;
- explain each override or named outside contender;
- note evidence that makes the pooled historical base rate a poor target match.

Do not hand-edit model estimates or apply the gone probability again. Change current-share inputs,
change canonical concentration, or add an explained override, then rerun.

## Interpretation Limits

The model is a coarse pooled base rate. It sees the target market's current rank and share spacing,
but not company momentum, moat, management, financing, or strategy. Calibration windows currently
span 10–15 years, the gone probability is constant across ranks, and the fitted marginal rows do
not enforce a joint assignment across companies. See [calibration.md](calibration.md) for the
model, evidence, evaluation, corpus contract, and maintenance workflow.
