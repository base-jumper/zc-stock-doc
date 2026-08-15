---
id: durable-growth
name: Evidence of Durable, Accelerating Growth
---

# Trait: Evidence of Durable, Accelerating Growth

**What we're looking for:**
The company's core business engine is compounding — and ideally the *rate* of growth is
holding steady or accelerating rather than quietly decelerating. The right metric depends on
the company's maturity. Share-price action is used as a continuous confirming signal, not as
the primary evidence.

**The right metric for the stage:**

| Stage | What to measure |
|-------|-----------------|
| **Early-stage** | Leading operational metrics: units sold, subscriptions, active users, bookings, revenue. Profitability is not expected yet. |
| **Maturing** | **Either** growing profit with free cash flow (FCF) closely tracking profit, **or** deliberate, disciplined reinvestment — suppressed profit that comes with expanding gross margins, improving unit economics, and a credible path to profitability. |

**Why FCF must track profit (for maturing companies):**
When a company is reporting profit, you want free cash flow to follow it closely. A persistent
gap between reported profit and cash generation is a quality-of-earnings red flag — it can
signal aggressive revenue recognition, capitalised costs, working-capital strain, or serial
"one-time" charges. Profit that doesn't convert to cash is suspect.

**Why the reinvestment carve-out matters:**
The greatest Rule Breakers often suppress profit for years to reinvest everything into growth
(Amazon did this for roughly two decades). Do **not** screen these out. The thing you're
guarding against is *burning cash with no improving economics* — not a company that is
deliberately and successfully trading near-term profit for durable market position.

**Watch the second derivative:**
Truly exponential growth is rare and never lasts. What you actually want is *sustained high
compounding*. Pay close attention to whether the growth rate is stable/accelerating or quietly
decelerating. A company going 40% → 38% → 35% is decelerating even though every number still
looks strong — and deceleration is one of the earliest signs a growth story is maturing.

**The role of share price:**
Financials are lagged and reported quarterly; price is continuous. Strong, sustained price
appreciation can be a *leading* indicator that confirms the growth engine is still intact
between reports. A meaningful move (up or down) that isn't yet explained by the financials is
a cue to investigate — not an automatic signal to act. Price is a confirming layer here, never
the primary evidence.

**Key questions:**
- Is the right metric for this company's stage growing at a high rate?
- Is that growth rate accelerating, steady, or decelerating?
- If the company reports profit, is FCF following it closely?
- If profit is suppressed, is it deliberate reinvestment with improving economics — or just
  cash burn?
- Does recent price action confirm the story, or is it diverging from the fundamentals?

**Scoring guidance:**
- **0.70–1.00** Strong growth in the stage-appropriate metric; rate stable or accelerating; FCF tracks
  profit (or reinvestment is disciplined with improving economics)
- **0.40–0.69** Growth present but clearly decelerating, or a worrying gap between profit and FCF, or
  reinvestment with no visible improvement in unit economics
- **0.00–0.39** Growth stalling or declining; cash burn with no improving economics; profit that doesn't
  convert to cash

**Documentation:**

* The company's stage and the stage-appropriate metric chosen (and why that metric)
* That metric over several recent periods — enough to show both the growth *rate* and whether it is accelerating or decelerating — with source
* Gross-margin / unit-economics trend; if profit is suppressed, where the reinvestment goes and the evidence it is working

## Script

[`durable_growth.py`](../../scripts/durable_growth.py) lays out the growth metrics and, crucially, their
second derivative, via [`yfin`](../../../yahoo-finance/SKILL.md):

```bash
durable_growth NVDA                # 5 annual years (default); --years N
durable_growth NVDA --format json
```

Per year it shows revenue, revenue growth, gross margin and FCF / net income; the summary gives the
window CAGR, the **deceleration read** (recent growth rate vs the earlier rate — *accelerating /
steady / decelerating*, the trait's core signal), the gross-margin trend, FCF tracking, and the 52-week
price move (the confirming-signal-only layer). Yahoo doesn't carry the operational leading metrics
(units, subs, bookings) an early-stage name should be judged on — those come from the filings, as the
output notes.
