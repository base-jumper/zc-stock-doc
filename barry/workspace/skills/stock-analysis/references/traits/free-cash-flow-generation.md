---
id: free-cash-flow-generation
name: Free Cash Flow Generation
---

# Trait: Free Cash Flow Generation

**What we're looking for:**
A business that throws off a **large amount of genuinely free cash** while needing **little ongoing
capital** to sustain it. This is the defining positive of a cash cow: it earns, and most of what it
earns is left over to distribute after the business has been fed. We read one quantity — the free cash
generated — through two lenses: its **magnitude** (the FCF margin) and the **forward capital intensity**
that drives it (how little must be reinvested to keep that cash coming). These are cause and effect, not
two independent axes — a fat FCF margin is largely what a profitable business *gets* when it reinvests
little — so weigh the size of the free cash together with the reason it is there, never as separate
confirmations.

A familiar headline metric, **FCF conversion (FCF/net income)**, is deliberately *not* a third scored
axis: it blends two things this roster keeps apart — accrual quality (whether earnings show up as
operating cash), owned by [earnings quality](earnings-quality.md), and capital intensity (whether capex
then consumes that cash), owned here. Use it as a quick cross-check, and when it looks weak, decompose
it to see which half is responsible.

The capital that matters here is **forward**, not historical. We read the capital the business must
keep putting in to sustain — and modestly grow — its current cash yield, *not* the size of the asset
base it has already built. Sunk capital is irrelevant to next year's free cash; where that base is
large and hard to replicate, it is a **moat**, not a demerit. So a heavy-asset business that has
already built its network and now needs little to keep it running is the *archetypal* cash cow, not an
exception. (The moat value of that base is [pricing power](pricing-power.md); the rate it earns is
[returns on capital](returns-on-capital.md); this trait owns only how much free cash comes out the
front, and how little must go back in.)

This trait is about the *quality of the business's cash generation*, not the cash yield at today's
price. FCF **per share against the share price** (the FCF yield) is a return input and belongs in the
Valuation write-up — not here.

**Putting numbers on it:**
Use these as anchors for a typical operating company. Lead with the **combination**, not either column
alone. **Forward capital intensity travels across industries; FCF margin is industry-relative** — read
the margin against peers and the company's own history rather than a fixed bar.

| Reading | FCF margin (FCF/revenue) | Forward capital intensity (capex/OCF) |
|---|---|---|
| **Strong** (0.70–1.00) | **≥ ~15%** (vs peers) | **≤ ~30%** — most of OCF falls to FCF |
| **Decent / mixed** (0.40–0.69) | **~5–15%** | **~30–60%** |
| **Poor** (0.00–0.39) | **< ~5%** | **> ~60%** — capex eats the cash |

* **FCF** is operating cash flow minus capex, on an owner-earnings basis — normalised through-cycle,
  not a single year flattered by timing. Define it and state the figure.
* **Capital intensity below depreciation is good only if earned, not harvested.** When capex runs below
  economic depreciation the FCF margin looks unusually fat; confirm that is genuine capital-lightness,
  not deferred maintenance that will reverse (see *Watch for* below).
* **Durability counts.** A single strong year off a working-capital release is not the trait; we want
  the margin and the low intensity *sustained* across several years.

**Watch for — the cash that isn't really free:**

* **Harvesting / deferred capex.** Maintenance capex run below economic depreciation flatters FCF now
  at the cost of a future replacement or refurbishment cliff. Check maintenance capex against D&A and
  the asset's condition and replacement cycle. Persistent capex << D&A on a physical-asset business is
  a flag, not a feature — and it ties directly to [fundamental stability](fundamental-stability.md): a
  melting ice cube and a harvested asset look identical on this year's FCF.
* **Working-capital releases.** A one-off unwind of working capital, or stretching payables, can
  inflate FCF for a year or two. Normalise to a through-cycle figure.
* **Add-backs that are real costs.** Stock-based compensation added back to cash flow is an economic
  cost to owners; don't let it pad the FCF figure. Treat asset-sale proceeds as one-off, not recurring
  free cash.

**Key questions:**

* What is normalised, through-cycle FCF, and what is the FCF margin against peers and the company's own
  history?
* Over the last 5+ years, is the FCF margin stable, rising, or eroding — and where FCF/net income
  conversion looks weak, is it the accruals or the capex dragging it?
* How much capital must keep going in to sustain and modestly grow today's cash — capex as a share of
  operating cash flow, split growth vs maintenance where discernible?
* Is maintenance capex covering economic depreciation, or is FCF being flattered by deferring it?
* Strip out one-offs (working-capital swings, asset sales, SBC add-backs): how much free cash is
  genuinely recurring and distributable?

**Scoring guidance:**

(What counts as **strong** / **decent** / **poor** on each axis is defined once in *Putting numbers on
it* above; the bands below describe the combined, quality read.)

* **0.70–1.00** Strongly and durably cash-generative — a high FCF margin for its industry, driven by
  low forward capital intensity and sustained across several years, with the cash genuine (capex covers
  economic depreciation; not a working-capital one-off). Most of what the business earns is free to
  distribute.
* **0.40–0.69** Moderately cash-generative, or strong on the surface with caveats — a moderate FCF
  margin, **or** a strong one undercut by a meaningful capex drag or by headline FCF partly flattered
  by deferred capex, working-capital timing, or add-backs that aren't yet resolved.
* **0.00–0.39** Weak free cash generation — capex- or working-capital-hungry, so little of earnings
  reaches free cash; a thin or eroding FCF margin; **or** apparent free cash that is harvesting (capex
  below depreciation) and will reverse.

**Documentation:**

* The FCF definition used and the normalised figure, with source — and how one-offs were stripped out
* FCF margin versus peers and the company's own history
* The FCF margin over 5+ years, with the trend — and, where FCF/net income conversion is weak, which
  half (accruals vs capex) drives it
* Forward capital intensity (capex / OCF), with the growth-versus-maintenance split where discernible
* The maintenance-capex-versus-depreciation check — the deferred-capex / harvesting read, cross-referenced
  to [fundamental stability](fundamental-stability.md)
* The verdict — roughly how much of earnings is genuinely free and distributable, and how sustained it is

## Script

[`free_cash_flow.py`](../../scripts/free_cash_flow.py) pulls the cash-flow and income statements (via
[`yfin`](../../../yahoo-finance/SKILL.md)) and computes the trait's ratios so you read off prepared
numbers:

```bash
free_cash_flow KO                  # 5 annual years (default); --years N
free_cash_flow KO --format json
```

A TTM snapshot (FCF and margin, taken from the cash-flow statement — not the unreliable `info`
free-cash-flow field) sits above an annual series carrying, per year, **FCF margin** (magnitude),
**capex / OCF** (forward intensity), **FCF / net income** (conversion) and **capex / D&A** (the
harvesting flag — persistently below ~1x on a physical-asset business flatters FCF now). The summary
adds the window-average margin, its trend, and the **cumulative FCF / net-income conversion** (sturdier
than any single year). Yahoo can't split growth from maintenance capex, so that read stays the agent's
against the bands above.
