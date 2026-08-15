---
strategy: freeroll
name: Freeroll
# Valuation method used to estimate annualized ROI for this strategy (see references/valuation/).
# The stock-analysis flow generates this method's inputs into the stock-doc's `valuation:` block and
# runs its script, which writes `valuation.<method>.roi` back. asymmetric-payoff IS the payoff calculation this
# strategy describes in "Writing it up": it probability-weights the floor (downside-support) against
# the catalyst-implied fair value over the catalyst window.
valuation: asymmetric-payoff
# The scorer writes this strategy's normalized {score, confidence} into the stock-doc front matter
# under strategies.<strategy> (i.e. strategies.freeroll); see references/scoring.md.
# Ordered trait list and floors. Floors encode importance INVERSELY: a LOWER floor makes the
# trait matter MORE (floor 0 = can veto). This block is the single source of truth for the
# floors — do not restate the numbers in the body, or they will drift.
traits:
  - {id: downside-support,       floor: 0.00}
  - {id: fundamental-stability,  floor: 0.20}
  - {id: mispricing,             floor: 0.15}
  - {id: catalyst,               floor: 0.00}
---

# Strategy: Freeroll

## Applies to

Use this strategy for **out-of-favour, cheap stocks where the downside is already priced in and an
identifiable catalyst should drive a re-rating within ≤4 years**. These are typically mature,
cyclical, asset-rich, income, or special-situation businesses — REITs at a discount to NAV, listed
fund/asset managers trading near their own co-investment stake, capital-intensive companies below
book, high-quality dividend payers on a depressed price, conglomerates worth more in parts, or
companies the market has marked down for a narrative we disagree with. We buy near the floor, hold
for the catalyst, and **sell at fair value** — this is not a forever-hold.

It is a **poor fit** for early-stage disruptors and long-duration compounders (use
[Rule Breakers](rule-breakers.md) there), and for expensive quality businesses with no floor and no
catalyst. The thing that makes a company fit *here* is the combination of **limited downside + an
identifiable, time-bound catalyst** — not business quality. If a company sits on the boundary or
could plausibly suit more than one strategy, do not force it: evaluate the union of all strategies'
traits and score each (see the [SKILL](../../SKILL.md)).

## Philosophy

This strategy is built on **asymmetry**, not quality. We are not trying to own the best business in
the world — we are trying to find bets where **heads we win a lot, tails we lose little**. The whole
edge comes from two things being true at once:

1. **The downside is already priced in.** There is a real, conservatively-measured floor — asset
   value, a covered high yield, take-out economics — that makes a much lower price unreasonable.
2. **The upside is not.** An identifiable catalyst, on a clock of ideally 1–2 (and at most 4) years,
   should force the market to re-rate the stock toward a fair value we can define today.

A company in this strategy **does not need a perfect scorecard** the way a Rule Breaker does. It can
be mature, unloved, even shrinking modestly — what matters is that we are buying it at a price with
limited downside and a concrete reason it will re-rate. The two cardinal sins this process guards
against are the **falling knife** (cheap with no real floor) and the **value trap** (cheap with a
floor but no catalyst, so it stays cheap forever). The discipline is mechanical: **buy near the
floor, hold for the catalyst, sell at fair value, then move on.**

## Traits

Score each trait on a 0–1 scale (see each trait file for its bands and documentation checklist).
As a guide: **0.70–1.00** clearly meets the trait | **0.40–0.69** partial or uncertain |
**0.00–0.39** fails or absent. Score continuously within these bands — the endpoints are anchors,
not the only allowed values.

These four traits assess whether the setup is a *valid* freeroll — a real floor, a real catalyst, and
a defensible reason it's cheap. They deliberately do **not** size the prize: the
magnitude of the asymmetry (the upside-to-downside payoff) is a separate **quantitative** figure,
derived from the floor and the catalyst-implied fair value, assessed in the Valuation write-up and
reflected in the 0–10 stock-doc `score` — not folded into the strategy score. See *Writing it up*.

This strategy uses the following traits, in order:

1. [Downside Support / Valuation Floor](../traits/downside-support.md) — the margin of safety. **Make-or-break:** no real floor vetoes (it's a falling knife).
2. [Fundamental Stability / No Value Trap](../traits/fundamental-stability.md) — the decline has bottomed / isn't terminal. Supportive guard against value traps.
3. [Mispriced for an Identifiable Reason](../traits/mispricing.md) — a defensible, differentiated view on *why* the market is wrong (the qualitative edge; the *size* of the gap is quantified separately). Supportive.
4. [Identifiable, Time-Bound Catalyst](../traits/catalyst.md) — the trigger that forces a re-rating. **Make-or-break:** no catalyst vetoes (it's dead money).

The exact floor for each trait lives in this strategy's front matter (above) and is read straight
from there by the scorer — the labels here ("make-or-break" / "supportive") describe the intent
behind those numbers without duplicating them.

## Scoring

The scoring mechanics — the two axes (Score / Confidence), the floor transform → geometric-mean
formula, and running the scorer — are shared by every strategy and documented once in
[references/scoring.md](../scoring.md), using the floors from this strategy's front matter (above).
Two traits have a floor of 0 and can therefore *veto*: **downside-support** and **catalyst** — the two
things that define an asymmetric bet (a real floor and a real trigger), either of which at 0 drives the
score to 0.

The strategy score measures how sound the *setup* is — not how big the prize is. A high score
confirms the bet is *well-formed*; it does **not** say the payoff is large, so always read it
alongside the asymmetry/ROI from the Valuation write-up.

## Disqualifiers

Eligibility is gated separately from scoring: a company carrying a disqualifier is ineligible
regardless of how its traits score. Only the [universal disqualifiers](../disqualifiers.md) apply —
freeroll adds none.

This is deliberate. The things that look like freeroll kill-shots all break either the *floor* or the
*catalyst*, and each is already graded by its trait — so they mark that trait down rather than gate
eligibility, and because **downside-support** and **catalyst** both carry a floor of 0, a trait driven
to 0 vetoes the whole strategy anyway:

* A **dividend that isn't covered** only matters when the dividend *is* the floor; that is exactly the
  case [downside-support](../traits/downside-support.md) scores down (an uncovered-dividend "floor"
  isn't real). When the floor is assets or cash instead, an uncovered dividend shouldn't gate at all.
* **Overstated asset values** are the conservatism/durability dimension of
  [downside-support](../traits/downside-support.md) — stale or aggressive marks mean the measured floor
  isn't real, and the trait grades that.
* A **permanently blocked catalyst** is simply the absence of a [catalyst](../traits/catalyst.md): no
  trigger that can close the gap on any timetable scores the trait at the floor.

Likewise *structural decline dressed up as cyclical* is graded by
[fundamental-stability](../traits/fundamental-stability.md), not gated. See
[disqualifiers.md](../disqualifiers.md) for the gate mechanic and how to record the verdict.

## Writing it up

The body sections are owned by the [SKILL](../../SKILL.md), but for this strategy two of them carry
the weight of the thesis and must be explicit:

* **Valuation** — this is where the **payoff** (the strategy's headline output) is quantified. State,
  as concrete numbers: the **floor** (per share, method, as-of date) and the remaining downside; the
  **fair value** (per share, method matched to the catalyst) and the upside; the resulting
  **asymmetry ratio**; the **catalyst and its expected window**; and the **sell target** at which we
  intend to exit. This asymmetry/ROI — derived from the floor and the catalyst-implied fair value —
  is deliberately *not* a trait; it is the quantitative figure that drives the 0–10 stock-doc
  `score`. Compute it with the strategy's valuation method, **asymmetric-payoff** (see
  [references/valuation/asymmetric-payoff.md](../valuation/asymmetric-payoff.md) and *Estimating ROI*
  in the [SKILL](../../SKILL.md)): record its inputs (price, floor, fair value, catalyst probability,
  window) in the stock-doc `valuation:` block and run the script to write `valuation.asymmetric-payoff.roi`.
* **Watch** — lead with the **catalyst's confirming signposts** and the **floor-erosion risks** (the
  things that would break the thesis). A scheduled update should be able to read this and immediately
  know whether the catalyst is on track and the floor still intact.
