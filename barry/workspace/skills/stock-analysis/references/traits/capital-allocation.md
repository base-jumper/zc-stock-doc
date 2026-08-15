---
id: capital-allocation
name: Capital Allocation
---

# Trait: Capital Allocation

**What we're looking for:**
Management that deploys the cash the business throws off **rationally** — sending each marginal dollar
to wherever it earns the highest per-share return. Capital allocation is the choice between the five
uses of cash (reinvest in the business, acquire, pay down debt, pay dividends, buy back shares),
funded from internal cash flow, debt, or new equity. Buffett calls it a CEO's most important job, and
notes the trap: a leader who rose through marketing or engineering often has no aptitude for it, yet
over a multi-year hold it dominates per-share outcomes more than operating skill does. 

What separates a good allocator is **discipline and counter-cyclicality** — buying (whether assets,
businesses, or its own shares) when they are cheap rather than when the company happens to be flush,
and returning cash instead of empire-building once high-return uses are exhausted:

| Use of cash | Rational | Value-destructive |
|---|---|---|
| **Reinvest in the business** | Funds growth while incremental returns stay high — see [returns on capital](returns-on-capital.md) and the runway to redeploy | Over-invests past the point returns fade, or starves a high-return business of capital |
| **Acquisitions** | Disciplined, strategic, sensibly-priced bolt-ons | Serial or overpriced empire-building and *diworsification* — the detail lives in [organic growth](organic-growth.md) |
| **Buy back shares** | Only below a conservative estimate of intrinsic value, genuinely shrinking the count | Repurchasing at peaks, or merely to mask dilution, regardless of price |
| **Dividends** | Sustainable and covered; paid once reinvestment opportunities are exhausted | Maintained by borrowing, or a token that defers the real allocation question |
| **Balance sheet** | Conservative, keeping optionality | Over-levering for buybacks or M&A, or hoarding idle cash that drags returns |

The acid test is the **per-share intrinsic value** created over a full cycle, and a track record of
rational decisions across it — not a single good or bad call. This is a distinct judgement from
overall [management quality](management-backing.md): a gifted operator can still be a poor allocator,
and the two are scored separately.

**Scoring guidance:**

* **0.70–1.00** A demonstrated rational allocator across a cycle: reinvests while returns are high,
  returns surplus cash rather than empire-building, repurchases only below intrinsic value, keeps M&A
  disciplined and well-priced, and runs a conservative balance sheet — per-share value clearly
  compounding.
* **0.40–0.69** Mostly sensible but with real lapses (a richly-priced deal, pro-cyclical buybacks,
  cash drag, or a stretched balance sheet), or too short a track record to judge with confidence.
* **0.00–0.39** Value-destructive allocation: serial overpriced M&A or diworsification, buybacks at
  peaks or merely to offset dilution, reckless leverage, or a persistent idle-cash drag — per-share
  value eroded.

**Documentation:**

* How the cash generated has been deployed across the five uses over recent years, with source
* Buyback record: the valuations at which repurchases occurred versus intrinsic value, and whether
  they were net of dilution
* M&A record: size, price/multiple, strategic fit, and subsequent outcomes (impairments, divestitures)
  — cross-referencing [organic growth](organic-growth.md)
* Balance-sheet posture and dividend coverage
* The verdict: per-share value created or destroyed over the cycle, and the reasoning behind the score

## Script

[`capital_allocation.py`](../../scripts/capital_allocation.py) reads the five uses of cash straight off
the cash-flow statement (via [`yfin`](../../../yahoo-finance/SKILL.md)):

```bash
capital_allocation AAPL            # 5 annual years (default); --years N
capital_allocation AAPL --format json
```

Per year it shows reinvestment (capex), acquisitions, dividends and buybacks **as a share of operating
cash flow**, plus net debt raised/repaid; the summary gives total returned to shareholders as a share of
FCF, dividend payout and FCF cover, cumulative M&A spend, and the **diluted-share-count change** (real
buybacks shrinking the count vs net dilution). The acid test — whether buybacks happened *below
intrinsic value* and whether M&A created per-share value — is judgement Yahoo can't supply; the script
gives the quantities, you supply the prices-paid read against the bands above.
