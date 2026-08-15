---
strategy: rule-breakers
name: Rule Breakers
# Valuation method used to estimate annualized ROI for this strategy (see references/valuation/).
# This strategy's candidates span the profitless-to-just-profitable range, where the right lens
# depends on the company — so it uses the weighted-average meta-method to blend the two that apply:
#   - tam-capture  : terminal value built from market-analysis's 10-year company revenue estimate
#                    (works pre-profit; the usual lens here)
#   - exit-multiple: bottom-up off owner-earnings/FCF (only once the company is actually profitable)
# The map value lists the candidate components; per company, evaluate those that are applicable (see
# each method's Applicability), then weight them in the stock-doc's valuation.weighted-average.weights.
valuation:
  weighted-average: [tam-capture, exit-multiple]
# The scorer writes this strategy's normalized {score, confidence} into the stock-doc front matter
# under strategies.<strategy> (i.e. strategies.rule-breakers); see references/scoring.md.
# Ordered trait list and floors. Floors encode importance INVERSELY: a LOWER floor makes the
# trait matter MORE (floor 0 = can veto). This block is the single source of truth for the
# floors — do not restate the numbers in the body, or they will drift.
traits:
  - {id: right-place-and-time,  floor: 0.00}
  - {id: top-dog,               floor: 0.15}
  - {id: sustainable-advantage, floor: 0.20}
  - {id: durable-growth,        floor: 0.00}
  - {id: organic-growth,        floor: 0.30}
  - {id: management-backing,    floor: 0.25}
  - {id: incentive-alignment,   floor: 0.40}
  - {id: customer-devotion,     floor: 0.50}
---

# Strategy: Rule Breakers

## Applies to

Use this strategy for **emerging, growth-first companies that could become the dominant player in a
large and expanding opportunity** — disruptors changing how some part of the world works, where
success can compound on itself (better products → more customers → stronger data/networks →
widening advantage). Typical markers: a young or re-accelerating industry, high revenue growth, a
leading or fast-gaining position, a long runway, and a story that rewards holding for years.

It is a **poor fit** for mature, slow-growth, or cyclical businesses bought mainly for value,
income, or a turnaround — there the growth and "top dog in an emerging wave" traits will
structurally fail and the score will not be meaningful. If a company sits on the boundary, or could
plausibly suit more than one strategy, do not force it here: evaluate the union of all strategies'
traits and score each (see the [SKILL](../../SKILL.md)).

## Philosophy

This strategy is built around a simple but demanding idea: **only a small minority of companies
compound for long enough to become industry giants and produce truly outsized returns**. Most
businesses stall, get competed away, mature, dilute shareholders, or turn out to be less special
than they first appeared. The point of this process is not to be right about every company. The
point is to **maximise our odds of owning as many of the rare long-duration compounders as
possible**, and to avoid selling them just because they have already worked.

The best candidates are companies that are changing how the world works, expanding into large
markets, strengthening their competitive position as they scale, and giving shareholders a chance
to participate in many years of value creation. We are looking for businesses where success can
compound on itself: better products, more customers, stronger data, deeper networks, improving
unit economics, increasing brand trust, and widening strategic advantage.

This is a **long-term, optimistic, growth-first** approach — but not blind optimism. We expect many
ideas to fail or merely become average. That is acceptable if the portfolio is constructed to let
the exceptional few matter. One genuine 20x, 50x, or 100x winner can pay for a long list of
mistakes, but only if we identify it early enough, own enough of it, and have the temperament to
keep holding while the story plays out.

## Traits

Score each trait on a 0–1 scale (see each trait file for its bands and documentation checklist).
As a guide: **0.70–1.00** clearly meets the trait | **0.40–0.69** partial or uncertain |
**0.00–0.39** fails or absent. Score continuously within these bands — the endpoints are anchors,
not the only allowed values. A company need not score perfectly on the seven positive traits — they
work together as a holistic picture.

This strategy uses the following traits, in order:

1. [Right Place and Time](../traits/right-place-and-time.md) — the industry setup. **Make-or-break:** a dead industry vetoes.
2. [Top Dog](../traits/top-dog.md) — the company's position within the opportunity. Supportive.
3. [Sustainable Competitive Advantage](../traits/sustainable-advantage.md) — the durability of the lead. Supportive.
4. [Evidence of Durable, Accelerating Growth](../traits/durable-growth.md) — the compounding engine. **Make-or-break:** no growth vetoes.
5. [Organic Growth over Acquisitive Growth](../traits/organic-growth.md) — growth built, not bought. Supportive; favours organic compounders over serial/overpaying acquirers.
6. [Great Management & Smart Backing](../traits/management-backing.md) — the people and capital behind it. Supportive.
7. [Incentive Alignment](../traits/incentive-alignment.md) — whether pay and ownership point management at long-term per-share value rather than size or gameable metrics. Supportive; pairs with management quality as the stewardship check, and guards against the stock-based-comp dilution common in young disruptors.
8. [Customer Devotion](../traits/customer-devotion.md) — how much customers love it, B2C or B2B. Supportive (lightest weight).

The exact floor for each trait lives in this strategy's front matter (above) and is read straight
from there by the scorer — the labels here ("make-or-break" / "supportive") describe the intent
behind those numbers without duplicating them.

## Valuation

This strategy values candidates with the [weighted-average method](../valuation/weighted-average.md),
blending the two lenses that suit its profitless-to-just-profitable range:
[tam-capture](../valuation/tam-capture.md) (a terminal "it works" value built top-down from the market
doc's company-revenue estimate) and [exit-multiple](../valuation/exit-multiple.md) (bottom-up off
owner-earnings/FCF). Each method's file owns its mechanics; what follows is how to apply the set here.

Resolve TAM-capture's market-doc prerequisite before valuing the stock. Use an existing suitable
document unchanged; if none exists, spawn a sub-agent to generate it with `market-analysis`, wait for
the saved result, and pass its reference into the TAM-capture input block. Use a 10-year horizon for
the Rule Breakers exit-multiple component too, so both ROIs describe the same holding period before
they are blended.

Per company, run the methods that are **applicable** (see each method's *Applicability*) and weight
them in the stock-doc:

- **tam-capture is the workhorse and is almost always applicable** — a true rule-breaker is often
  still unprofitable, so there is no earnings base for exit-multiple to anchor on, and the top-down bet
  is the same one the [Traits](#traits) describe: a top dog in a large, expanding opportunity becoming
  dominant. The market doc's `mobility-adjusted-revenue` is authoritative; do not replace it with a
  stock-level TAM or capture estimate. Anchor `margin` and `exit-multiple` on the mature role model,
  and keep those assumptions consistent with [sustainable-advantage](../traits/sustainable-advantage.md).
  Because this remains a survivor path rather than a probability-weighted expectation, treat the ROI
  as the reward *conditional on the thesis working*, not a base rate.
- **Add exit-multiple once the company is genuinely profitable.** For a rule-breaker that has tipped
  into positive owner-earnings, the bottom-up anchor becomes meaningful, and running both lets the two
  lenses cross-check. Weight by which is better supported — not toward the lower number — and let a
  **wide spread between them lower the strategy's confidence** rather than disappear into the blend.
- **Take dilution seriously.** Young disruptors fund themselves with stock; the dilution input is the
  same stock-based-comp leakage the [incentive-alignment](../traits/incentive-alignment.md) trait
  guards against, so the two readings should agree.

## Scoring

The scoring mechanics — the two axes (Score / Confidence), the floor transform → geometric-mean
formula, and running the scorer — are shared by every strategy and documented once in
[references/scoring.md](../scoring.md), using the floors from this strategy's front matter (above).
Two traits have a floor of 0 and can therefore *veto*: **right-place-and-time** and **durable-growth**
— a dead industry or no growth drives the score to 0.

## Disqualifiers

Eligibility is gated separately from scoring: a company carrying a disqualifier is ineligible
regardless of how its traits score. Only the [universal disqualifiers](../disqualifiers.md) apply —
rule-breakers adds none. (A regulatory or legal action that would imminently void the business model is
one of those universal kill-shots; the *ordinary* regulatory overhang a maturing disruptor faces is
not — that is the [right-place-and-time](../traits/right-place-and-time.md) fit judgement, which the
score handles.)

Most things that look like rule-breaker "red flags" are not disqualifiers — decelerating growth, a
lost lead, margin compression, or weak stewardship are already graded by
[durable-growth](../traits/durable-growth.md), [top-dog](../traits/top-dog.md),
[management-backing](../traits/management-backing.md), and
[incentive-alignment](../traits/incentive-alignment.md), so they mark a trait down rather than
disqualify. See [disqualifiers.md](../disqualifiers.md) for the gate mechanic and how to record the
verdict.
