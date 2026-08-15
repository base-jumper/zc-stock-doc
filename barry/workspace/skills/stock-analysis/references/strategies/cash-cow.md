---
strategy: cash-cow
name: Cash Cow
# Valuation method used to estimate annualized ROI for this strategy (see references/valuation/).
# The stock-analysis flow generates this method's inputs into the stock-doc's `valuation:` block and
# runs its script, which writes `valuation.<method>.roi` back. exit-multiple fits a cash cow when
# applied with low/flat growth, an exit multiple at or below entry (no re-rating), buybacks as negative
# dilution, and a high dividend/payout — so the return is carried by income and buyback, not multiple
# expansion. The cash-cow-specific way to apply it lives in the Valuation section below.
valuation: exit-multiple
# The scorer writes this strategy's normalized {score, confidence} into the stock-doc front matter
# under strategies.<strategy> (i.e. strategies.cash-cow); see references/scoring.md.
# Ordered trait list and floors. Floors encode importance INVERSELY: a LOWER floor makes the
# trait matter MORE (floor 0 = can veto). This block is the single source of truth for the
# floors — do not restate the numbers in the body, or they will drift.
traits:
  - {id: earnings-quality,          floor: 0.00}
  - {id: free-cash-flow-generation, floor: 0.00}
  - {id: fundamental-stability,     floor: 0.10}
  - {id: pricing-power,             floor: 0.15}
  - {id: capital-allocation,        floor: 0.15}
  - {id: returns-on-capital,        floor: 0.20}
  - {id: conservative-debt,         floor: 0.25}
  - {id: key-person-risk,           floor: 0.30}
  - {id: incentive-alignment,       floor: 0.50}
---

# Strategy: Cash Cow

## Applies to

Use this strategy for **mature, durable businesses that throw off far more cash than they can
reinvest, and return the surplus to shareholders**. Typical markers: stable, predictable earnings; high
free-cash-flow margins with low ongoing capital needs; a defended market position; sustainable
dividends and/or buybacks; and little reinvestment runway. We buy for the **cash yield plus modest
growth** and hold while the business hands the cash back — **not** for compounding through reinvestment,
and **not** for a re-rating.

It is a **poor fit** for early-stage, profitless disruptors (use [Rule Breakers](rule-breakers.md)),
for cheap, broken, or cyclical businesses bought for a catalyst re-rating (use [Freeroll](freeroll.md)),
and — the subtle boundary — for long-duration **compounders** (use [Wonderful and Fair](wonderful-and-fair.md)).
The line against a compounder is the **reinvestment runway**: a cash cow meets the same quality bar but
has **no high-return home for its cash**, so it returns it rather than redeploying it. The trait that
separates the two is [reinvestment-runway](../traits/reinvestment-runway.md) — present for a compounder,
absent for a cash cow — which is why this strategy drops it from the roster entirely (see *Traits*). The
thing that makes a company fit *here* is **durable, high-quality cash generation with nowhere left to
reinvest, so the cash comes back to you.** If a company sits on the boundary or could plausibly suit
more than one strategy, do not force it: evaluate the union of all strategies' traits and score each
(see the [SKILL](../../SKILL.md)).

## Philosophy

This strategy is built on **durable cash generation and disciplined capital return**, not on growth and
not on cheapness. A wonderful business with nowhere left to reinvest is still a wonderful holding — it
simply compounds through the cash it **pays out** rather than the cash it ploughs back. The return comes
from the free cash the business throws off, the discipline with which management hands it back, and
whatever modest organic growth a mature franchise still has.

The discipline has two halves, and both must hold:

1. **A durable cash machine** — high-quality, predictable, forward-capital-light cash generation,
   defended by a moat, and **not in secular decline**.
2. **The cash actually reaches you** — management returns the surplus rather than hoarding it or
   torching it on value-destroying M&A, and the payout is **covered by free cash flow, not debt**.

The cardinal sin this process guards against is the **value trap in slow motion** — the *melting ice
cube*: high current free cash and a fat yield masking structural decline, where the cash stream erodes
faster than it is paid out. Two traits stand guard together:
[fundamental-stability](../traits/fundamental-stability.md) (the demand persists) and the incremental
read of [returns-on-capital](../traits/returns-on-capital.md) (serving that demand stays profitable). A
cash cow is a *stable* harvest, not a liquidation.

This is also what separates the strategy from a compounder. A compounder reinvests at high returns and
you let intrinsic value compound; a cash cow has no such runway, so value is **returned, not
compounded**. Do not force a cow to look like a compounder by inventing a runway, and do not penalise it
for lacking one — distributing the cash *is* the correct answer when there is nowhere high-return to put
it (the [capital-allocation](../traits/capital-allocation.md) question).

## Traits

Score each trait on a 0–1 scale (see each trait file for its bands and documentation checklist).
As a guide: **0.70–1.00** clearly meets the trait | **0.40–0.69** partial or uncertain |
**0.00–0.39** fails or absent. Score continuously within these bands — the endpoints are anchors,
not the only allowed values.

This strategy uses the following traits, in order:

1. [Earnings Quality / Consistent, Predictable Profits](../traits/earnings-quality.md) — demonstrated, consistent earning power backed by real cash. **Make-or-break:** a cash cow's whole appeal is *dependable* cash, so erratic or unreal earnings veto.
2. [Free Cash Flow Generation](../traits/free-cash-flow-generation.md) — the defining positive: a large amount of genuinely free cash thrown off with low forward capital intensity. **Make-or-break:** a business that does not generate free cash is not a cash cow at all, so this vetoes.
3. [Fundamental Stability / Secular Durability](../traits/fundamental-stability.md) — the melting-ice-cube guard: the cash stream is not being structurally eroded. Heavily weighted — a structurally declining "cow" is a value trap, the strategy's central failure mode.
4. [Pricing Power / Durable Moat](../traits/pricing-power.md) — the moat that defends the margins the cash rests on. Heavily weighted, peer to capital allocation.
5. [Capital Allocation](../traits/capital-allocation.md) — whether management returns the surplus cash rationally rather than hoarding it or empire-building. Heavily weighted — for a cash cow, *returning the cash is the thesis*, so this bites harder here than in [Wonderful and Fair](wonderful-and-fair.md).
6. [High, Durable Returns on Capital](../traits/returns-on-capital.md) — the moat fingerprint, read here for **stability and incremental returns** over absolute level (infrastructure-style cows earn structurally modest but steady returns on a heavy sunk base). Weighted, a notch lighter than in Wonderful and Fair.
7. [Conservative Debt / Financial Strength](../traits/conservative-debt.md) — balance-sheet resilience, and crucially whether the payout is funded by free cash flow rather than debt. Supportive; the catastrophic end (insolvency) is left to the [disqualifier gate](../disqualifiers.md).
8. [Key-Person Risk](../traits/key-person-risk.md) — how badly the business breaks if one individual leaves; scored as resilience (high = low risk). Supportive guard against fragility.
9. [Incentive Alignment](../traits/incentive-alignment.md) — whether the pay-and-ownership system points management at long-term per-share value and rational distribution rather than size. Supportive check on stewardship, lightest-weighted of the set.

The exact floor for each trait lives in this strategy's front matter (above) and is read straight
from there by the scorer — the labels here ("make-or-break" / "supportive") describe the intent
behind those numbers without duplicating them.

## Valuation

This strategy values candidates with the [exit-multiple method](../valuation/exit-multiple.md), which
estimates an annualized ROI by growing a per-share fundamental, applying the multiple expected at sale,
collecting dividends along the way, and annualizing off today's price. That method doc owns the
mechanics and the front-matter contract; what follows is how to *apply* it to a cash cow. The return on
a cash cow is carried by **the cash it returns** — income and buyback — plus modest organic growth, with
little or no help from the multiple. Express that in the inputs:

- **`metric: FCF` — anchor on owner earnings / free cash.** The whole thesis is cash, so use the
  free-cash figure ([free-cash-flow-generation](../traits/free-cash-flow-generation.md) already produces
  a normalised one); reserve `metric: Earnings` for the rare case where accounting earnings are genuinely
  clean and the market prices the company on P/E.
- **`growth` — extrapolate the franchise, don't underwrite a runway.** Project growth forward from the
  business's *own demonstrated* trend — the volumes, pricing, and mix it has actually delivered — rather
  than from new products, markets, customers, or acquisitions. Growth of the latter kind leans on a
  high-return [reinvestment runway](../traits/reinvestment-runway.md), the very thing this strategy has
  already judged absent; importing it contradicts the thesis. Keep the figure consistent with the
  [fundamental-stability](../traits/fundamental-stability.md) read, and let that discipline set the
  number rather than forcing it into a range.
- **`exit-multiple.`** Set the multiple to what the business will
  *deserve at exit* given its maturity and quality then, not a hoped-for expansion.
- **`dilution`.** If the company returns cash through buybacks, model them as negative dilution,
  **separate** from `growth`, so share-count shrinkage is captured without being double-counted into the
  growth path.
- **`dividend-yield` / `payout`.** Set these from the *actual, FCF-covered* payout rather than an
  aspirational one; for most cows this income is the single largest contributor to the return.
- **`years` — 5 is fine.** There is no compounding to wait for, so the horizon need only be long enough
  to smooth a cycle.


## Scoring

The scoring mechanics — the two axes (Score / Confidence), the floor transform → geometric-mean
formula, and running the scorer — are shared by every strategy and documented once in
[references/scoring.md](../scoring.md). The score axis produces `cash-cow-score` and the confidence axis
`cash-cow-confidence`, using the floors from this strategy's front matter (above). Two traits carry a
floor of 0 and can therefore *veto* — [earnings-quality](../traits/earnings-quality.md) and
[free-cash-flow-generation](../traits/free-cash-flow-generation.md), the two things that define a cash
cow (dependable real earnings and genuine free cash): either at 0 drives the score to 0.

## Disqualifiers

Eligibility is gated separately from scoring: a company carrying a disqualifier is ineligible
regardless of how its traits score. Only the [universal disqualifiers](../disqualifiers.md) apply, and
cash-cow adds none of its own. The failures that would sink a candidate are already graded by its
traits, where they veto via their floors: no free cash by
[free-cash-flow-generation](../traits/free-cash-flow-generation.md), erratic or unreal earnings by
[earnings-quality](../traits/earnings-quality.md), and the **melting ice cube** by
[fundamental-stability](../traits/fundamental-stability.md) — graded, not gated, so a borderline
secular-decline call marks the trait down rather than forcing a binary verdict. The solvency extreme
that [conservative-debt](../traits/conservative-debt.md) defers to is the one place the gate does the
work. See [disqualifiers.md](../disqualifiers.md) for the gate mechanic and how to record the verdict.
