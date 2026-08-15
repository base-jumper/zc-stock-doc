# Rank Mobility Calibration

Maintainer reference for the model, calibration corpus, evaluation, and data-collection contract.
The daily agent should follow the [rank mobility runbook](mobility.md); it does not need this
background to apply the production estimate.

Calibrate **rank-transition probabilities**: for a player sitting at rank `n` in a market today,
the probability `p(n, i)` that it occupies rank `i` at the 10-year horizon. The
[concentration sub-skill](../concentration/concentration.md) projects the horizon share *vector*;
mobility projects **who lands where** in it. Weighting the complete geometric share curve by
transition probabilities replaces the silent assumption that every player keeps its rank
(`p(n, n) = 1`):

```
E[capture of player now at rank n] = Σ_i share(i) · p(n, i),  i = 1..∞
```

The fitted `fringe` probability aggregates ranks below the named top `K`; production capture
weights that state by the corresponding geometric concentration tail. `gone` has zero capture and
is therefore already baked into the expectation.

The top-`K`-origin to top-`K`-destination portion is conceptually a **doubly substochastic
incumbent block**: each row sum is at most 1 because an incumbent can move to the fringe or gone,
and each column sum is at most 1 because a future rank can be occupied by only one current
incumbent. A row's residual goes to fringe or gone; a destination column's residual is the
probability that the rank is won from outside today's top `K`. These constraints are what would
make per-stock expectations mutually consistent in a jointly constrained model.

## The Model

A player at rank `n` transitions to a destination in `{1..K, fringe, gone}`. Death/absorption
(the `gone` fates) is a constant hazard `g`; conditional on surviving, destination-rank weight
decays geometrically with rank distance, with the tail beyond `K` aggregated into the fringe:

```
p(gone) = g
p(i | alive)      ∝ ρ^|i−n|                i = 1..K
p(fringe | alive) ∝ ρ^(K+1−n) / (1−ρ)
```

`ρ ∈ (0,1)` is the churn parameter: 0 freezes the ranking, higher values shuffle it. For a
current share vector `s`, define player `n`'s relative share gap `q(n)` as its smallest gap to an
adjacent named rank divided by `s(n)` (the sole adjacent rank at either edge is used).
`mobility_fit.py fit` estimates four variants by maximum likelihood over pooled window
transitions and compares them by leave-one-panel-out NLL:

- **share** (production): `ρ(n,q) = sigmoid(a + c·(n−1) + d·q(n))` — this retains the rank
  effect and lets the target market's starting share spacing affect the estimate. The current fit
  has `d < 0`: an incumbent separated from its nearest ranked neighbour is stickier. Only windows
  with complete start-year top-K shares train this model.
- **rank** (no-share fallback): `ρ(n) = sigmoid(a + c·(n−1))` — stickiness is
  rank-dependent. Leaders hold far more than deep ranks (empirically rank 1 held in ~60% of
  windows, rank 3+ under 30%), and one pooled ρ cannot express that.
- **constant**: single ρ; the fallback if the rank effect stops validating.
- **maturity**: `ρ(F) = sigmoid(a + b·F)` with `F` the adoption-curve position at window start.
  On the current corpus this variant carries **no out-of-sample signal** and its coefficient's
  sign is unstable across fitting depths — the same verdict the concentration corpus gave the
  barrier index. Curve positions stay scored and reported as a diagnostic; the covariate is not
  wired into the production estimate until it earns its way in.

Fitting truncates panels to their **top-5 origins** (`MAX_RANKS`): stickiness is rank-dependent
beyond what the kernel expresses, deep ranks are noisier, and predictions are consumed for
top-ranked players, so the fit is calibrated at the depth where it is used.

**Known limitations.** The share-gap coefficient is supported by a small number of independent
panel windows and its out-of-panel improvement over rank alone is slight; treat the direction as
useful but the magnitude as coarse. The symmetric kernel treats a gap above or below a player the
same way and does not model company-specific momentum. Predicted rows are calibrated marginals:
the column constraint of the doubly substochastic incumbent block is not enforced by the fit.
`predict` reports each destination column's implied from-outside residual, but the output is not a
jointly constrained assignment model. The kernel is symmetric in rank distance, `g` is constant
across ranks and maturity, and window lengths vary (10–15 years) without correction. Treat every
number as a coarse base rate to discipline judgment, not replace it.

## The Data Unit: Named Ranking Panels

One panel = one market tracked over time under a **fixed definition**: the same share basis,
geography, and tracker throughout. Each covered year records the named top-`coverage` players in
order. Ranks and identities are the primary payload — the transition matrix is fit on counts of
who moved where. **Record share values whenever the source publishes them**: starting shares feed
the production model's relative-gap covariate, distinguish near-tie swaps from genuine upheavals,
and can support future momentum covariates. Shares are omitted only when
the source gives just an ordering — a rank-only panel is still valid, an estimated share never is.
The basis only needs to be consistent *within* a
panel: units for handsets and passengers for airlines pool fine, because rank transitions are
basis-agnostic.

Store **every year the source covers** — full annual series are the target. Two years a decade
apart is the minimum viable panel, not the goal: dense years let windows be placed deliberately on
the market's life rather than wherever coverage happens to start, feed the momentum covariate, and
later allow testing whether ten-year transitions compose from annual ones. Windows are derived at
fit time as non-overlapping pairs of covered years ≥ 10 apart.

## Files

- `data/panels/<id>.csv` — rows `year,rank,player,share`, ranks contiguous from 1 within each
  year, largest first. `share` is the player's fraction of the **whole defined market** (not of
  the top-`coverage` group), as a 0–1 fraction; leave it blank when the source gives only an
  ordering — never estimate it.
- `data/panels.yaml` — the index: market definition, basis, coverage, tracker, per-player facts,
  and per-year citations (`sources`). Field meanings are in the file header.

Player names must be canonical and stable across all years of a panel (use the most recent name;
note renames in the player's `notes`).

## Player Facts and Fates

Every player appearing in a panel needs `founded` — the year the company came into existence; this
is what calibrates the "didn't exist yet" entrant mass. `entered-market` is optional, for
companies that existed long before competing in this market. When a player leaves the
top-`coverage` ranks before the last covered year, record `fate` and `fate-year`:

| fate | meaning |
|---|---|
| `fringe` | fell below coverage, still competing |
| `exited` | left the market (business shut down or sold off) |
| `defunct` | company ceased to exist |
| `acquired` | absorbed by another player — also record `acquirer` |

**Acquisition rule:** the acquired player's trajectory ends at the acquisition; the acquirer
continues under its own identity. Never merge two players' histories into one line.

## Market Maturity

Mobility varies with where the market sits on its adoption S-curve — churn is highest while the
curve is steep and falls as it flattens — so curve position at window start is the model's main
planned covariate. Each panel records it as the two parameters of a normalized logistic in the
optional `penetration` block:

```
F(t) = 1 / (1 + exp(-k · (t − t0)))     t0 = inflection year, k = steepness per year
```

`F(t)` is the fraction of the path to saturation completed by year `t`, so the fit reads a
continuous maturity value off **any** covered year. The saturation ceiling `L` is deliberately
normalized to 1: what matters here is progress toward saturation, not the ceiling itself, and
normalizing makes positions comparable across markets. This is the same curve the
[penetration sub-skill](../penetration/penetration.md) fits. Corpus markets are historical, so the
curve has usually played out and `t0`/`k` are well pinned — the ceiling-identifiability problem
that makes live penetration estimation hard mostly doesn't apply; it returns only for panels whose
coverage ends mid-curve.

Record `provenance: fitted` when the parameters are pinned by actual adoption data through the
curve's bend (cite the data in `sources`); `estimated` when they rest on judgment or
extrapolation. Fit from adoption evidence, never from the observed churn — that would leak the
outcome into the covariate. Parameter tagging is analyst work, not collection work: panels arrive
without a `penetration` block and are scored before fitting. Note the covariate's current
standing in [The Model](#the-model): scored and reported, but diagnostic only.

## Collection Discipline

- **Never fabricate.** Every year's table comes from a fetched source; record one citation URL per
  year (or per multi-year table) in `sources`. Archived press releases via the Wayback Machine are
  fine — cite the archive URL.
- `quality: verified` only when every covered year is cited to a primary source; otherwise use
  `seed-approximate`. **Both qualities are intentionally included in calibration.** The verified
  corpus is currently too small to support a useful fit on its own, so seed-approximate panels are
  necessary provisional evidence. Keep the label honest, prefer verified panels when expanding the
  corpus, and use quality-split sensitivity checks before treating small model differences as
  meaningful.
- **No splicing.** A change of tracker or market definition inside a panel fakes churn. Note
  definition changes in `tracker-notes`; if a break materially changes the ranking basis, end the
  panel and start a new id.
- Do not use market-cap rankings (they measure expectations, not position) or sources that rank
  only public companies.
- Aim for spread: mature low-churn markets (regulated data — airlines, bank deposits, insurance)
  as well as turbulent tech markets (tracker press releases). A corpus of famous disruptions is
  biased toward predicting disruption — the same spread rule as the
  [concentration corpus](../concentration/concentration.md#growing-the-corpus).

## Maintainer Commands

```bash
scripts/mobility_panels.py validate    # contract checks; non-zero exit on errors
scripts/mobility_panels.py summary     # per-panel years, span, usable windows; corpus totals
scripts/mobility_fit.py windows        # derived windows, transitions, entrant composition
scripts/mobility_fit.py fit            # fit all variants, LOO comparison, baselines
```

All take `--json`. Stdlib + PyYAML. Run `validate` after adding or editing any panel. The daily
`predict` command is documented only in the [runbook](mobility.md).
