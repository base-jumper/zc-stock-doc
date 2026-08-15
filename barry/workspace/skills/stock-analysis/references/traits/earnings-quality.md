---
id: earnings-quality
name: Earnings Quality / Consistent, Predictable Profits
---

# Trait: Earnings Quality / Consistent, Predictable Profits

**What we're looking for:**
**Demonstrated, consistent earning power** — a business that has been reliably profitable for years,
grows those profits with some predictability, and backs every dollar of reported profit with real
cash. This is the bedrock of the wonderful-business case: we are not forecasting a turnaround or
betting on an inflection, we are buying a track record. Buffett's framing is the test here —
*"demonstrated consistent earning power; future projections are of no interest to us, nor are
'turnaround' situations."*

The trait has three distinct strands, and a strong score needs all three:

| Strand | What it means | The failure it guards against |
|---|---|---|
| **Consistency** | A long, unbroken record of profitability — ideally through a full cycle (downturns included), not one good year | A single flattering year, or profits that vanish the moment conditions turn |
| **Predictability** | Profits grow on a smooth, low-variance path you could have forecast in advance — not lumpy, erratic, or violently cyclical | An average that hides wild swings; earnings you cannot underwrite |
| **Cash backing** | Reported profit converts to free cash flow; net income ≈ owner earnings over time | Accounting profit that never becomes cash — the quality-of-earnings trap |

**This is a *quality and consistency* trait, not a *growth-rate* trait.** It is deliberately the
complement of [Durable Growth](durable-growth.md), which rewards and *accelerating* growth
rate. Here we want consistency and predictability, that we can rely on for years.
A business going a dependable 8–10% a year through every cycle scores *better*
here than one lurching +40%/−15%/+25% — even though the lurching one has the higher average. The
*level* of profitability (how much capital it earns on) is assessed separately.

**Why this matters:**
A wonderful business is one whose future you can actually underwrite. Consistency proves the earning
power is structural rather than circumstantial; predictability lets you value it with confidence;
cash backing proves the profits are genuine. The cash strand is the classic quality-of-earnings
check: a persistent gap between reported profit and free cash flow is a red flag — it can signal
aggressive revenue recognition, capitalised costs, working-capital strain, serial "one-time"
charges, or earnings flattered by adjustments. **Profit that doesn't convert to cash is suspect, no
matter how smooth the reported line looks.**

**What to look at:**

* **Track record** — years of unbroken profitability; net income / EPS / operating income over a full
  cycle (ideally **7–10 years**), through at least one downturn. How many down years, and how deep?
* **Variance of growth** — is the growth path tight and forecastable, or does it swing? A low
  dispersion of year-on-year growth is the signal; high dispersion (or genuine cyclicality) is the
  tell that the earnings are hard to underwrite.
* **Cash conversion** — free cash flow versus net income over several years (cumulative FCF / cumulative
  net income). Persistently near or above 1.0 is good; a chronic shortfall needs explaining.
* **Accounting quality** — how much of the earnings story leans on *adjusted* / *underlying* figures,
  frequent restructuring or "one-off" charges, capitalised costs, rising receivables/inventory
  relative to sales, or stock-based comp excluded from "profit." Recurring one-offs are not one-offs.

**Key questions:**

* Has the company been profitable every year through the last cycle — and how deep were the worst years?
* Could you have forecast this year's profit three years ago and been roughly right? Is the growth
  path smooth or lumpy?
* Over the last several years, has free cash flow tracked reported net income — or is there a
  persistent gap?
* Is the headline profit clean, or propped up by adjustments, serial "one-offs", or aggressive accruals?
* Is the consistency structural (a durable business model) or just a benign stretch that a downturn
  would expose?

**Scoring guidance:**

* **0.70–1.00** Long, unbroken record of profitability growing through a full cycle; low-variance,
  predictable path; FCF closely tracks (or exceeds) net income over time; clean accounting with
  minimal reliance on adjustments.
* **0.40–0.69** Generally profitable but with real caveats — some lumpiness or cyclicality, a recent
  down year, a moderate profit-to-cash gap, or noticeable reliance on adjusted figures. Earning
  power is real but not fully dependable.
* **0.00–0.39** Erratic or thin profitability, losses in recent memory, profit that doesn't convert
  to cash, or accounting that materially flatters earnings — consistent earning power is not
  demonstrated, or not trustworthy.

**Documentation:**

* The profitability track record: years of unbroken profit and the net income / EPS trend over a full
  cycle (ideally 7–10 years), with source — and the worst year(s) and how deep
* A read on predictability: how smooth or lumpy the growth path is (down years, dispersion of
  year-on-year growth, any genuine cyclicality)
* Cash conversion: FCF vs net income over several years (a cumulative ratio is ideal), with source —
  and an explanation of any persistent gap
* Accounting-quality notes: reliance on adjusted figures, recurring "one-offs", capitalised costs,
  accruals trend, or stock-based comp — flag anything that flatters the earnings
* The reason for the score — why the earning power is judged consistent, predictable, and real (or not)

## Script

[`earnings_quality.py`](../../scripts/earnings_quality.py) gathers the three quantitative strands (the
accounting-quality read stays qualitative), via [`yfin`](../../../yahoo-finance/SKILL.md):

```bash
earnings_quality GOOGL             # 10 annual years requested (Yahoo serves ~4); --years N
earnings_quality GOOGL --format json
```

The series shows net income, diluted EPS, year-on-year growth and receivables/revenue; the summary
distils the strands — **consistency** (loss years, worst year), **predictability** (the std-dev
*dispersion* of YoY growth — low = forecastable, the complement of durable-growth), **cash backing**
(cumulative FCF / cumulative net income), and an **accruals tell** (receivables growing faster than
sales). yfinance serves only ~4 annual years, so the deep-cycle track record (and whether a downturn was
survived) comes from the filings — flagged in the output.
