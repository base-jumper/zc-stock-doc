# Market Concentration Estimation

Estimate how concentrated a market will be at the 10-year horizon — the leader's share and the
whole-market HHI — by scoring the market on structural traits and mapping those scores to the two
parameters of a geometric rank-share law. The output fills the market-doc
`concentration.model-estimate` and derived `concentration.hhi` fields. Mobility consumes the
canonical rank-share curve for player assignment and adjusted capture. Accept the market scope,
revenue boundary, segments, and horizon from the parent [market contract](../../SKILL.md#market-contract); do not
redefine them here. Terminology (HHI, capture, market value) is defined in the
market-docs README at investment/market-docs/README.md; the HHI reading table lives there.

Concentration projects *how the defined revenue pool splits* among players; the
[size sub-skill](../size/size.md) projects how large that pool becomes. Multiplying a player's
capture by the projected market value gives its revenue — the point of the exercise.

## The Model

Player shares follow a two-parameter **geometric rank-share** law, ranks ordered largest-first:

```
share(i) = s1 · r^(i-1)          i = 1, 2, 3, ...
```

`s1` is the leader's share; `r ∈ (0, 1)` is the rank-to-rank decay ratio. The two parameters are
deliberately decoupled: `s1` sets **how dominant the leader is**, `r` sets **how fast the field
thins** (how many players matter). Both raise concentration but through different mechanisms.

The modeled players need not sum to 1. The remainder `1 − s1/(1 − r)` is an **atomistic competitive
fringe** — many tiny players whose contribution to HHI vanishes. This makes the whole-market
quantities exact closed forms:

```
HHI               = s1² / (1 − r²)
effective players = 1 / HHI
capture(i)        = share(i)   for each named player slotted into a rank
```

**Validity regime.** A genuine fringe exists only when `s1 ≤ 1 − r`. Above that (e.g. a hard
duopoly: high `s1`, high `r`) the geometric tail is fictitious — enumerate only the real players and
ignore ranks beyond them; the HHI closed form still holds. `concentration_fit.py project` warns when
`s1 > 1 − r`.

**Why geometric, and its limits.** Real firm-size distributions are often closer to a power law
(heavier tail), but for concentration only the top handful of ranks matter — tiny shares square to
≈0 in HHI — so a geometric anchored at the leader is accurate where it counts. It describes two
shapes poorly: **flat oligopoly tops** (three near-equal leaders) and **leaders detached far above
their tail**. The fit reports `geom_rmse` and flags these; when flagged, trust `s1` and HHI (which
are matched exactly) over the interior per-rank shares. This validation applies only to observed
ranked shares. Synthetic geometric shares are generated from the law itself and are therefore
excluded: testing their geometric fit would be tautological.

## From Traits to Parameters

Concentration is predicted from **structural traits**, scored the way stock-analysis scores company
traits — each trait rated `{score, confidence}` on 0–1 (see the stock-analysis
[scoring mechanics](../../../stock-analysis/references/scoring.md) for the two-axis convention). The
traits live in [traits/](traits/). Score all seven so the corpus can continue testing the model;
the frozen production specification uses [network-effects](traits/network-effects.md),
[scale-economies](traits/scale-economies.md), and [switching-costs](traits/switching-costs.md).
[Data-scale advantage](traits/data-scale-advantage.md), [brand/reputation](traits/brand-reputation.md),
[capital intensity](traits/capital-intensity.md), and
[regulatory barriers](traits/regulatory-barriers.md) remain candidate features, not production
inputs.

Production fits **two independent standardized ridge regressions**:

```
z(trait) = (score − corpus mean) / corpus standard deviation
s1       = clip(βs,0 + Σ βs,j · z(trait j), 0.02, 0.99)
r        = clip(βr,0 + Σ βr,j · z(trait j), 0.02, 0.98)
```

The feature set and ridge penalty `alpha = 1` are frozen; only corpus means, scales, intercepts, and
coefficients are refitted on each call. Ridge penalizes large coefficients while leaving the
intercept unpenalized, stabilizing a small, correlated corpus. `r` is predicted directly rather
than forced to follow from `s1`.

The selected signs are economically coherent: network effects and scale economies raise `s1` and
lower `r`, concentrating share at the top; switching costs lower `s1` and raise `r`, protecting
multiple incumbents rather than only the leader. Nested leave-one-out evaluation scored the selected
model at roughly `0.18` RMSE for `s1` and `0.17` for `r`, versus `0.22` and `0.20` for the former
noisy-OR pipeline. It also remained best when whole sectors were held out. Transfer between the
observed-share and Census-synthetic subsets was materially weaker for every method, so treat the
result as a coarse central estimate and keep expanding observed-share coverage.

## The Calibration Corpus

The calibration corpus in [data/](data/) is what connects traits to parameters — it *is* the model,
not a convenience. Each entry is one labelled example: the **structural trait scores** a market
exhibits (the input) paired with the rank-share distribution it has developed at **maturity** (the
outcome). See [../penetration/penetration.md](../penetration/penetration.md) for why this differs
from penetration's per-forecast priors — there the target's own accruing data eventually identifies
the curve; here the target's mature shape never exists in time to help, so the corpus carries the
whole relationship.

- `data/shares/<id>.csv` — the canonical `rank,share` outcome, largest-first. Files may contain
  observed shares or a finite geometric sequence generated from aggregate moments.
- `data/moments/*.csv` — source/staging data containing HHI and CR4/CR8/CR20/CR50. It is not read
  by live calibration. HHI and CR4/CR8 estimate `(s1, r)`; CR20/CR50 are held out as source-shape
  diagnostics before synthetic shares are generated.
- `data/calibration.yaml` — the index: per entry the share basis, the maturity year, category tags,
  outcome provenance/quality, and the **structural trait scores**. Field meanings are in the header.

Parameters are derived fresh from the canonical share files. Observed ranked shares are preferred.
Synthetic shares are reproducible derived data: `concentration_census.py synthesize` fits the source
moments, emits enough geometric ranks to preserve HHI within tolerance, and stops before cumulative
share exceeds one. `outcome-quality: synthetic-geometric-shares` identifies them and
`derived-from` points back to the source row.

`moments/census-2022-pilot.csv` contains 30 screened Census outcomes, all materialized as synthetic
shares and included in the corpus. The full corpus has 42 entries with verified trait scores.

Two roles beyond calibration: observed outcomes and source moments let you **validate the geometric
form**, and the corpus provides the **nearest-neighbour anchors** used to sanity-check a `params`
prediction (`list`, then `fit` a close analog) before trusting it.

### Scoring discipline: mechanism, not outcome

The one thing that corrupts this corpus is **circularity** — inferring a trait score from the
concentration it produced ("Google won search, so search *must* have had a strong data moat"). That
leaks the outcome (`y`) into the feature (`x`), inflates the apparent trait→param relationship, and
makes live predictions overconfident. Confidence does not fix it: circularity is a *bias*, not
variance. The discipline that prevents it:

- **Score the mechanism, using all available evidence — but never justify a score by pointing at the
  realized market shares.** You may use everything now understood about *how the mechanism works*
  (that search relevance genuinely compounds with query volume); you may not reason from the fact
  that the market ended up concentrated. Cite the mechanism evidence.

This is deliberately *not* an as-of-date cutoff. Restricting to information available at some early
year would answer a different question (how well an analyst scores from thin data) and just adds
noise. What keeps the corpus valid for live use is that live scoring is *also* mechanism-based — the
same feature definition, only with less evidence and therefore lower confidence. More evidence in the
corpus reduces variance without shifting the mean, **provided the extra evidence is about the
mechanism, not the outcome**. The temptation is strongest for the outcome-entangled traits
([network-effects](traits/network-effects.md), [data-scale-advantage](traits/data-scale-advantage.md));
be strictest there, where independent structural evidence is thin. Capital, scale, and regulatory
barriers usually have outcome-independent evidence (capex, cost curves, licensing regimes) and are
safer.

Set `quality: verified` only when the trait scores have been checked against outcome-independent
mechanism evidence and cited; otherwise `seed-approximate`. The share basis is verified separately
(cited in `sources`); an entry can carry verified shares while its traits are still
`seed-approximate`.

## Workflow

1. **Define the market and share basis.** State what a "share" measures (revenue, units,
   subscribers, queries) and the geography. Only compare like bases when borrowing parameters.
2. **Score and store the seven traits** for the target as it stands today, `{score, confidence}`
   each, using [traits/](traits/) and the scoring discipline below. Write them under
   `concentration.inputs.traits` and explain the material mechanisms in the market-doc prose.
3. **Predict `(s1, r)`.** Run
   `concentration_fit.py params --market-doc <MARKET_ID> --dry-run` to inspect the result, then
   rerun without `--dry-run` to write `model-estimate`, `hhi`, `method`, and `date`. The script
   refits the frozen direct-ridge models from the corpus on every call. Treat the estimate as a
   coarse central value: sanity-check it against the nearest calibration entries (`list`, then
   `fit`) and against your own read of the market. Heed the `s1 > 1 − r` warning
   (hard-duopoly regime).
4. **Reconcile.** Check the HHI against the market-docs README at investment/market-docs/README.md
   reading table and against the player-capture prose — they must describe the same market (the
   market-analysis SKILL's consistency rule). Resolve contradictions before saving.
5. **Override only when justified.** To depart from the model, add the complete replacement
   `{s1, r, reason}` under `concentration.override` and rerun the same command. The canonical
   parameters are `override` when present, otherwise `model-estimate`; no third resolved copy is
   stored. The script always derives `concentration.hhi` from that canonical pair. Explain the
   traits, any override, and the resulting structure in *Market Structure*. Return the canonical
   rank-share curve to mobility for player assignment and adjusted capture; do not write player
   outputs here.

## Script

```bash
scripts/concentration_fit.py list                              # summarise the calibration corpus
scripts/concentration_fit.py fit <shares.csv> [--json]         # summarise one distribution as (s1, r)
scripts/concentration_fit.py fit-moments <moments.csv> --id ID  # fit one aggregate-moment row
scripts/concentration_fit.py params --traits ne=0.6,se=0.7,sc=0.3 \
    [--names A,B,C] [--json]                                   # predict s1, r, HHI from trait scores
scripts/concentration_fit.py params --market-doc MARKET_ID \
    [--dry-run] [--as-of YYYY-MM-DD] [--json]                  # read inputs + write model outputs
scripts/concentration_fit.py project --s1 0.32 --r 0.60 \
    --names AWS,Azure,GCP [--min-share 0.01] [--json]          # HHI + capture table for chosen params
scripts/concentration_evaluate.py [--validation loo|source|sector] \
    [--methods NAME,...] [--details] [--json]
                                                               # nested model comparison
scripts/concentration_census.py list EC2200SIZECONCEN.zip       # screen Census outcomes
scripts/concentration_census.py extract EC2200SIZECONCEN.zip \
    --codes 311230,326211                                      # normalize selected outcomes
scripts/concentration_census.py synthesize data/moments/census-2022-pilot.csv \
    --output-dir data/shares                                   # generate canonical share files
```

Stdlib + PyYAML only. `fit` anchors `s1` to the observed leader share and sets `r` to reproduce the
empirical HHI (`r = √(1 − s1²/HHI)`) — a moment-match, not a least-squares fit, so the leader's share
and the HHI are exact and the long tail cannot drag them around. It reports `geom_rmse` and flags
`POORLY GEOMETRIC` shapes; interpret that diagnostic only for observed data. `fit-moments` holds HHI
exact, fits the remaining degree of freedom to CR4/CR8, and reports separate top and held-out
CR20/CR50 errors. `params` refits the frozen direct-ridge coefficients from the corpus and predicts
`s1` and `r` independently. It reports a fixed-model leave-one-out diagnostic; use the evaluator's
nested result when comparing methods because ordinary LOO does not account for the feature-selection
decision. Trait scores are passed as `--traits id=score,…` (full ids or aliases
`ne dsa br sc ci se rb`); `ne`, `se`, and `sc` are required. `project` generates the ranked capture
table and whole-market HHI for parameters supplied directly.

### Method evaluation

`concentration_evaluate.py` is the exploratory counterpart to the production fitter. It compares
the former dominance model with arithmetic and power-mean aggregators, all-trait ridge models, a
dominance-plus-barriers hybrid, and nested feature selection. Reported RMSE and MAE are outer
leave-one-out results. Power exponents, ridge penalties, and feature subsets are selected again
inside every outer training fold; selecting them once on the full corpus would leak held-out
outcomes into the comparison. `--details` prints per-market residuals, while `--json` includes
fold-level selections for stability review. Do not change the production model on a small metric
edge: prefer a material improvement that is stable across folds and economically intelligible.
Use `--validation source` to test transfer between observed-share and Census-synthetic outcomes.
Use `--validation sector` to hold out each broad economic sector, including all related markets,
at once. Census sectors follow broad two-digit NAICS groupings; observed markets use the explicit
sector map in the evaluator. Grouped reports include both market-weighted RMSE and the unweighted
mean across groups.

## Growing the Corpus

Expanding the corpus is the highest-value ongoing work — it both defines and tests the trait→param
mapping, so more (and more carefully scored) entries directly improve every estimate. When an
analysis wants a market not yet covered, spawn a sub-task to add it. The contract:

- Add observed `data/shares/<id>.csv` rows, or add a screened aggregate-moment row and generate its
  synthetic share file. Then append the outcome provenance/quality and traits to `calibration.yaml`.
- Score the seven traits from **mechanism evidence**, honouring the scoring discipline above (score
  the mechanism, never the outcome); cite sources for both the shares and the trait evidence.
- Aim for spread across the concentration spectrum, not just famous winner-take-all cases — a corpus
  built from monopolies is biased toward predicting monopoly.
- Sanity-check observed shares with `fit`. For aggregate sources, check `fit-moments` before
  generation; never use the generated shares to assess whether the source market is geometric.

For cheap breadth, use the U.S. Economic Census `EC2200SIZECONCEN` table. Work only from six-digit
NAICS rows with `TYPOP=00` (all establishments), numeric HHI, and complete CR4/8/20/50. Screen with
`concentration_census.py list`; curate across sectors and concentration levels; reject categories
whose national NAICS boundary is a poor competitive market; then extract selected rows into
`data/moments/` and run `synthesize` to create the canonical share files. Do not add multiple NAICS
hierarchy levels or multiple years of the same industry as independent examples. Aggregate moments
solve the outcome side cheaply, but every entry still needs outcome-independent trait scoring;
`seed-approximate` marks provisional scores awaiting evidence-backed review.
