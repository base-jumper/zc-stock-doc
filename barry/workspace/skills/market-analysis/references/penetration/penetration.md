# Market Penetration Estimation

Estimate a market's unit-penetration path 10 years out using a logistic S-curve whose parameters
blend a fit to observed history with priors borrowed from historical analogs. Accept the market
scope, addressable-unit definition, penetration measure, segments, and horizon from the parent
[market contract](../../SKILL.md#market-contract); do not redefine them here. Store analyst choices
under `penetration.inputs`; the script writes `penetration.model-estimate`, while an optional
complete `penetration.override` remains analyst-owned. Return the canonical curve evaluated for
every year from the base year through the 10-year horizon to the parent workflow for sizing, but
do not store those rates separately because they are derived from the curve.

## Definitions

**Penetration `p(t)`** is a decimal in `[0, 1]` measured exactly as the market contract specifies.
The standard `stock` measure is the fraction of the addressable base actively using or owning the
product. Never substitute annual unit sales, which follow a different peaking curve. Two
flow-adjacent measures are admissible because they are themselves S-shaped:
`new-sales-share` for replacement-cycle goods (EVs as a share of new car sales) and `spend-share`
for migration markets (e-commerce as a share of retail). Fit and borrow parameters only between
like measure types.

**The model** is a three-parameter logistic:

```
p(t) = L / (1 + exp(-k · (t - t0)))
```

`L` is the saturation ceiling (max penetration ever reached), `k` the steepness (fraction-per-year
growth rate at the midpoint; the curve takes ≈ `4.4/k` years to go from 10% to 90% of `L`), `t0`
the midpoint year. `L` is asserted from analogs plus judgment, not fitted: pre-inflection data
cannot identify a ceiling, and fixing `L` makes the fit a well-behaved least-squares problem on
`logit(p/L)` with honest standard errors. Only fit `L` (grid search) on mature, post-inflection
series such as completed analogs.

## Workflow

1. **Gather the target series.** Build a `year,penetration` CSV for the market (see *Data format*);
   the standard location is `investment/market-docs/data/<market-id>/penetration.csv`. Put its path
   under `penetration.inputs.target-series`; relative paths resolve from the market doc's
   directory. Even 3–4 points constrain the curve once the ceiling and steepness come from
   elsewhere.
2. **Select analogs.** Run `penetration_fit.py list` and pick 3–5 analogs matching the market on
   the drivers of adoption speed: purchase friction (free software vs. installed capital good),
   network effects, replacement-cycle length, and whether the product rides an existing channel.
   Match on mechanism, not surface industry. Include at least one slow analog unless there is a
   specific reason the market cannot be slow — priors built only from famous successes are biased
   fast. If a clearly better analog is missing from the library, add it first (see *Growing the
   library*).
3. **Record the inputs.** Under `penetration.inputs`, set the target `measure`, asserted `ceiling`,
   and selected `analogs`. Set `w-fit` only when overriding the computed weight, and
   `as-of-year` only when the calculation must exclude later information. State the ceiling and
   analog reasoning in the market doc.
4. **Fit and blend.** Run `penetration_fit.py blend --market-doc <MARKET_ID> --dry-run` first. It
   fits each analog (fixed at its indexed ceiling), forms a
   prior on `k` (mean and spread across analogs), fits the target, and combines them with
   inverse-variance weights — so priors dominate when history is short or flat and the fit
   dominates as informative history accumulates. The prior curve is anchored through the latest
   observation. Blending happens in parameter space to preserve the logistic shape.
5. **Sanity-check the weight.** The computed `w_fit` reflects statistical noise only. If the market
   is still early on the curve (latest `p` below roughly a third of `L`), the fitted `k` reflects
   early-adopter dynamics that may not extrapolate to the mainstream; consider capping the fit
   weight with `penetration.inputs.w-fit` (e.g. `0.5`) and say so in the doc.
6. **Write and explain.** Rerun without `--dry-run`. The script writes only
   `model-estimate`, `method`, and `date`, preserving the inputs, override, other front matter,
   and body. It prints the canonical annual path from the base year through the 10-year horizon
   for the parent workflow. Explain analog choice, ceiling reasoning, blend weight, and any
   override in the *Adoption Path* section.

The canonical curve is `penetration.override` when present, otherwise
`penetration.model-estimate`. An override must supply all of `{L, t0, k}` plus a non-empty
`reason`; do not store a third resolved copy.

## Script

```bash
scripts/penetration_fit.py list
scripts/penetration_fit.py blend --market-doc <MARKET_ID> [--dry-run] [--json]
scripts/penetration_fit.py fit <series.csv> --ceiling 0.85 [--project-to 2036] [--json]
scripts/penetration_fit.py fit <mature-series.csv>              # grid-searches the ceiling
scripts/penetration_fit.py blend <target.csv> --ceiling 0.85 \
    --analogs us-smartphones,us-color-tv,us-dishwashers \
    [--horizon-year 2036] [--w-fit 0.5] [--as-of 2015] [--json]
scripts/penetration_fit.py project --ceiling 0.85 --k 0.25 --t0 2031 --from-year 2026 --to-year 2036
```

Stdlib + PyYAML only. Market-doc mode reads the horizon from `base-year + maturity-duration`,
checks that every selected analog has the same measure type as the target, and returns the annual
path without storing it. `fit` reports `k`, `t0`, standard errors, and fit quality (`r2` in logit
space, RMSE in penetration space). Raw `blend` prints the analog fits, prior, weight, blended
parameters, and projection. Its `--as-of YEAR` equivalent in market-doc mode is
`penetration.inputs.as-of-year`; it truncates every series and drops analogs not yet plateaued by
then. The script validates series on load (values in `[0,1)`, at least four points to fit, warning
on non-monotonic dips); with fewer than four target points it falls back to prior-only, anchored at
the latest observation.

## Data Format

The analog library lives in [data/](data/):

- `data/series/<id>.csv` — one file per analog, `year,penetration` rows, raw observed values
  (do not pre-normalize by the ceiling). Irregular year spacing is fine.
- `data/analogs.yaml` — the index: one entry per analog with measure type, base definition,
  category tags, ceiling estimate, quality flag, and sources. Field meanings are documented in
  the file header.

Raw series are the single source of truth; fitted parameters are always derived fresh by the
script and never cached in the index. Published parameter estimates (e.g. Bass p/q tables) may be
noted in an analog's `notes` as corroboration but never substitute for a series.

## Growing the Library

When an analysis wants an analog not yet in the library, spawn a sub-task to add it rather than
researching inline. The sub-task contract:

- Produce `data/series/<id>.csv` and append a complete entry to `data/analogs.yaml`.
- Use the standard penetration definition; state the measure type and base explicitly.
- Cite sources for every series; prefer primary series (Pew, Our World in Data / CHAT, US Census,
  IEA, EIA, World Bank, industry bodies, company filings). Flag interpolated or estimated points
  in `notes`.
- Set `quality: verified` only when the numbers were checked against the cited source; otherwise
  `seed-approximate`.
- Sanity-check with `penetration_fit.py fit` before finishing: the series must load clean and
  produce a plausible fit.

The seed analogs are marked `seed-approximate`: figures are from well-known published series but
transcribed from memory. Before an analog carries significant weight in a real decision, verify it
against its source and upgrade the flag.

Analogs also carry an era: diffusion has sped up across generations, so an older analog under-predicts
a modern market's steepness. Prefer analogs roughly one product generation back from the target (the
`era-*` tags help), and keep mid-century series such as dishwashers and color TV as deliberate *slow
anchors* rather than default priors.

## Back-Testing

To calibrate the method against markets whose adoption curve is already known, see
[back-test/back-test.md](back-test/back-test.md). It forecasts mature markets from a historical
base-year using only information available then (enforced by `blend --as-of`), and scores each
projection in penetration points — separating irreducible model-form error from the forecaster's
judgment. Run it with "run the penetration back-test".
