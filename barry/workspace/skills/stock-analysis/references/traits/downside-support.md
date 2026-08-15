---
id: downside-support
name: Downside Support / Valuation Floor
---

# Trait: Downside Support / Valuation Floor

**What we're looking for:**
The stock trades at or near a level below which a further decline would be unreasonable, because
some structural backstop — asset value, income, or take-out economics — would assert itself. This
is the **margin of safety** and the foundation of the whole strategy: we only take the bet when the
downside is already priced in. (Useful synonyms: *valuation floor*, *downside support*, *hard
floor*, *asset/income backstop*.)

The right *kind* of floor depends on the business:

| Company type | Typical floor | Why it binds |
|---|---|---|
| **REIT / property** | NAV (net tangible assets); implied cap rate / rental yield | A persistent discount to a credibly-marked NAV, or a rental yield well above funding cost, pulls in buyers |
| **Listed fund / asset manager** | Value of the manager's *own* balance-sheet investments (co-investments, seed/stake in its own funds) | If market cap falls to ≈ that stake, you get the fee-earning business for free |
| **Capital-intensive (miner, industrial, shipping)** | Tangible book / replacement value | Market cap well below book or replacement cost invites takeover or rationalisation |
| **High-quality dividend payer** | A *sustainable* dividend now yielding high (e.g. ~10%) on a depressed price | The yield itself attracts buyers and defends the price — provided the dividend is genuinely covered and durable |
| **Cash-rich / net-net** | Net cash or liquid assets near/above market cap | Hard to fall below the cash in the bank |
| **Conglomerate / holding co** | Sum-of-the-parts — one segment or listed stake worth ≈ the whole market cap | The rest of the company comes for free |

**The general rule:** identify a defensible, hard-to-erode valuation anchor and show the current
price sits at or near it. A good anchor is **(a) real and conservatively measured**, **(b) durable**
— not about to be impaired, written down, or spent — and **(c) binding**, i.e. there is an actual
mechanism (yield-seekers, acquirers, NAV arbitrage, buybacks) that defends the price there.

**Key questions:**

* What is the specific floor for this company, and what is it worth per share today (conservatively)?
* How far is the current price above that floor — i.e. how much realistic downside remains?
* Is the floor durable? Could it be impaired, written down, or consumed (dividend cut, asset
  write-down, cash burn) before the catalyst plays out?
* What mechanism actually defends the price at the floor?
* Is the floor measured conservatively — recent marks, tangible assets, liquidity haircuts?

**Scoring guidance:**

* **0.70–1.00** Clear, conservatively-measured floor close to the current price; durable and actively
  defended; little realistic downside.
* **0.40–0.69** A plausible floor with caveats — stale marks, some impairment/erosion risk, or price
  still meaningfully above it.
* **0.00–0.39** No credible floor, or the "floor" depends on optimistic asset values or an uncovered
  dividend; downside is open-ended. *(With a floor of 0 in this strategy, no real downside support
  disqualifies the stock — it's a falling knife, not an asymmetric bet.)*

**Documentation:**

* The floor type chosen and why it fits this business
* The floor's value per share, with method, source, and as-of date; any haircuts applied
* Current price vs floor → the quantified downside (%)
* Durability: what could erode the floor before the catalyst, and how likely
* The mechanism that defends the price at the floor

## Script

[`downside_support.py`](../../scripts/downside_support.py) lays out the obtainable valuation floors and
how far the price sits above each, via [`yfin`](../../../yahoo-finance/SKILL.md):

```bash
downside_support BHP.AX
downside_support BHP.AX --format json
```

It reports the **asset floor** (price / book and price / tangible-book), the **cash floor** (net cash
per share, and as a share of the price) and the **income floor** (dividend yield and its FCF cover).
Where the listing currency differs from the financial-statement currency (e.g. an ASX miner reporting in
USD), it flags that the statement-derived floors need FX to compare. The bespoke floors the trait
table lists — REIT/property NAV and cap rates, a fund's co-investment stake, replacement value,
sum-of-the-parts — need the filings; Yahoo carries only the generic book / cash / yield anchors.
