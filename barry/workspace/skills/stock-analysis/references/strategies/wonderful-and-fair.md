---
strategy: wonderful-and-fair
name: Wonderful and Fair
# Valuation method used to estimate annualized ROI for this strategy (see references/valuation/).
# The stock-analysis flow generates this method's inputs into the stock-doc's `valuation:` block and
# runs its script, which writes `valuation.<method>.roi` back. exit-multiple is the right fit for a
# long-duration compounder; the strategy-specific way to apply it (owner-earnings anchor, conservative
# exit multiple, why this expresses "fair, not cheap") lives in the Valuation section below.
valuation: exit-multiple
# The scorer writes this strategy's normalized {score, confidence} into the stock-doc front matter
# under strategies.<strategy> (i.e. strategies.wonderful-and-fair); see references/scoring.md.
# Ordered trait list and floors. Floors encode importance INVERSELY: a LOWER floor makes the
# trait matter MORE (floor 0 = can veto). This block is the single source of truth for the
# floors — do not restate the numbers in the body, or they will drift.
#
traits:
  - {id: earnings-quality,    floor: 0.00}
  - {id: returns-on-capital,  floor: 0.15}
  - {id: pricing-power,       floor: 0.15}
  - {id: reinvestment-runway, floor: 0.15}
  - {id: capital-allocation,  floor: 0.25}
  - {id: conservative-debt,   floor: 0.25}
  - {id: key-person-risk,     floor: 0.30}
  - {id: incentive-alignment, floor: 0.50}
---

# Strategy: Wonderful and Fair

## Applies to

Use this strategy for **high-quality, durable businesses that compound shareholder value over many
years, bought at a fair (not necessarily cheap) price**. Typical markers: a long record of consistent, 
predictable profitability, high and durable returns on capital, a moat with pricing power, rational 
capital allocation, and a runway to keep reinvesting at high returns. We buy to **hold for years and
 let the business compound** — we are not buying a catalyst or a turnaround.

It is a **poor fit** for early-stage, profitless disruptors (use [Rule Breakers](rule-breakers.md)),
and for cheap, broken, or cyclical businesses bought for a re-rating (use [Freeroll](freeroll.md)) —
this strategy explicitly *rejects* both the turnaround and the profitless hyper-growth story. The
thing that makes a company fit *here* is **proven business quality you can underwrite for years**. If
a company sits on the boundary or could plausibly suit more than one strategy, do not force it:
evaluate the union of all strategies' traits and score each (see the [SKILL](../../SKILL.md)).

## Philosophy

This strategy is built on **quality and durability**, not cheapness and not explosive growth. The
core idea, from Buffett: *"It's far better to buy a wonderful company at a fair price than a fair
company at a wonderful price."* We are looking for businesses whose future we can actually
underwrite — that earn high returns on capital, defend those returns with a real moat, are run by
managers who allocate capital rationally, and have somewhere to keep reinvesting. Owned long enough,
a business like that compounds intrinsic value at its return on capital, and the share price
eventually follows.

The discipline has two halves, and both must hold:

1. **Wonderful** — the business is genuinely high quality: demonstrated consistent earning power,
   durable high returns on capital, a moat with pricing power, and rational stewardship of the cash
   it throws off.
2. **Fair** — we don't overpay. Quality is not a licence to pay any price; a wonderful business
   bought at a silly multiple is still a bad investment. The price discipline is expressed in the
   **Valuation** write-up via the strategy's valuation method, not as a trait.

## Traits

Score each trait on a 0–1 scale (see each trait file for its bands and documentation checklist).
As a guide: **0.70–1.00** clearly meets the trait | **0.40–0.69** partial or uncertain |
**0.00–0.39** fails or absent. Score continuously within these bands — the endpoints are anchors,
not the only allowed values.

> **Roster under construction.** This strategy is being assembled one trait at a time. The list below
> is intentionally partial; a management-quality trait will be added as we draft it. Treat scores
> produced now as provisional. (Eligibility is gated by the shared disqualifiers — see below — not by
> a safety-switch trait.)

This strategy uses the following traits, in order:

1. [Earnings Quality / Consistent, Predictable Profits](../traits/earnings-quality.md) — demonstrated, consistent earning power backed by real cash. **Make-or-break:** without consistent, predictable, real earnings it isn't a wonderful business, so this vetoes.
2. [High, Durable Returns on Capital](../traits/returns-on-capital.md) — the quantitative fingerprint of a moat: high returns on capital, sustained across a cycle. Heavily weighted — a low floor makes mediocre returns bite hard, but it stops just short of an outright veto.
3. [Pricing Power / Durable Moat](../traits/pricing-power.md) — the qualitative *why* behind those returns: a structural moat that lets the business raise prices without losing customers. Heavily weighted, peer to returns on capital.
4. [Reinvestment Runway](../traits/reinvestment-runway.md) — the growth engine of a compounder: room to redeploy earnings at high returns for years. Heavily weighted — together with returns on capital it forms the compounding engine (intrinsic value grows at roughly ROIC × reinvestment rate). This strategy targets compounders specifically, so a business with no runway is a cash cow that belongs in a different strategy, not a wonderful-and-fair pick; a short runway bites hard here.
5. [Capital Allocation](../traits/capital-allocation.md) — how rationally management deploys the cash the moat throws off. Supportive — important to a multi-year compounder, but a strong business can partly absorb an imperfect allocator.
6. [Conservative Debt / Financial Strength](../traits/conservative-debt.md) — whether the balance sheet could carry the business through a full cycle without the debt forcing its hand. Supportive — graded resilience that protects the multi-year compounding thesis; a stretched balance sheet bites, but the catastrophic end (insolvency) is left to the [disqualifier gate](../disqualifiers.md).
7. [Key-Person Risk](../traits/key-person-risk.md) — how badly the business breaks if one individual leaves; scored as resilience (high = low risk). Supportive guard against fragility.
8. [Incentive Alignment](../traits/incentive-alignment.md) — whether the pay-and-ownership system points management at long-term per-share value rather than size or gameable metrics. Supportive check on stewardship, lightest-weighted of the set.

The exact floor for each trait lives in this strategy's front matter (above) and is read straight
from there by the scorer — the labels here ("make-or-break" / "supportive") describe the intent
behind those numbers without duplicating them.

## Valuation

This strategy values candidates with the [exit-multiple method](../valuation/exit-multiple.md), which
estimates an annualized ROI by growing a per-share fundamental, applying the multiple we expect at
sale, and annualizing off today's price. That method doc owns the mechanics and the front-matter
contract; what follows is how to *apply* it to a wonderful-and-fair compounder. The aim is to express
the "Fair" half of the philosophy — don't overpay — as a number, while letting the "Wonderful" half
carry the return.

The single most important refinement is the anchor: feed the method **owner earnings**, not headline
accounting earnings. Owner earnings is the cash an owner can take out without weakening the moat — net
income plus depreciation, amortization, and other non-cash charges, minus maintenance capex and
incremental working capital. In practice this means preferring `metric: FCF` whenever maintenance
capex or working capital are material, which is the usual case for a real business; reserve
`metric: Earnings` for those rare cases where accounting earnings are genuinely clean, recurring, and
the market prices the company on P/E. Whichever you pick, state in the write-up that the anchor is an
owner-earnings figure and how you arrived at it.

Apply the remaining inputs with the compounder thesis in mind:

- **`exit-multiple` — set it conservatively, ideally at or below the entry multiple.** A return that
  depends on the multiple expanding is a re-rating bet, which belongs in [Freeroll](freeroll.md), not
  here. Let business growth and income carry the return, and use the method's attribution to confirm
  that the multiple-re-rating contribution is small.
- **`growth` — fund it from the business, not optimism.** Sanity-check the growth path against ROIC ×
  reinvestment rate, so the growth you assume is one the [returns-on-capital](../traits/returns-on-capital.md)
  and [reinvestment-runway](../traits/reinvestment-runway.md) traits can actually pay for. The two
  numbers must tell the same story.
- **`years` — go long (5+).** A compounder needs time for price to follow intrinsic value; the horizon
  is where the quality advantage compounds.

The rationale for all of this is the convergence of return to quality. Held for years, a business
returns roughly **ROIC × reinvestment rate, plus its payout yield**, almost independently of the entry
multiple — the same compounding engine the [Traits](#traits) describe (intrinsic value grows at about
ROIC × reinvestment). The entry multiple still matters: it bounds the downside and sets how long you
wait for value to show up in price. But the *return* is earned by the business, which is the precise
mechanical meaning of buying a wonderful business at a fair price.

## Scoring

The scoring mechanics — the two axes (Score / Confidence), the floor transform → geometric-mean
formula, and running the scorer — are shared by every strategy and documented once in
[references/scoring.md](../scoring.md). The score axis produces `wonderful-and-fair-score` and the
confidence axis `wonderful-and-fair-confidence`, using the floors from this strategy's front matter
(above).

## Disqualifiers

Eligibility is gated separately from scoring: a company carrying a disqualifier is ineligible
regardless of how its traits score. Only the [universal disqualifiers](../disqualifiers.md) apply —
most relevantly the solvency extreme that [conservative-debt](../traits/conservative-debt.md) defers
to — and wonderful-and-fair adds none of its own: the quality failures that would sink a candidate (no
consistent earnings, no moat, no runway) are already graded by its traits, where they veto via their
floors. See [disqualifiers.md](../disqualifiers.md) for the gate mechanic and how to record the
verdict.
