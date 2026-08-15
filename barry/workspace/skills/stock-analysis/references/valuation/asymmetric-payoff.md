---
id: asymmetric-payoff
name: Asymmetric Payoff (probability-weighted)
script: ../../scripts/asymmetric_payoff_valuation.py
---

# Valuation method: Asymmetric Payoff

Estimates the **expected annualized ROI** of a freeroll bet — a stock bought near its floor for a
catalyst-driven re-rating. It is a **two-outcome, probability-weighted** model that mirrors the
freeroll thesis directly: the catalyst either fires and the stock re-rates to **fair value**
(probability `p`), or it fails and we exit back at the **floor** (probability `1 − p`). Both outcomes
are assumed to resolve at the catalyst horizon. The headline output is the annualized expected
return.

This is the asymmetry the [freeroll strategy](../strategies/freeroll.md) is built on, turned into a
number — the payoff calculation its *Writing it up* section calls for. It consumes the **floor**
(downside-support trait), the catalyst-implied **fair value** (quantified in the freeroll Valuation
write-up, not a scored trait), and the catalyst's **probability** and **window** (catalyst trait).

> **Price-only.** Income earned while waiting (dividends / carry) is *not* modelled — the payoff is
> the price move to floor-or-fair-value. For a high-yield freeroll where the covered dividend is a big
> part of the thesis, the true ROI is somewhat higher than this method reports; treat the output as a
> conservative, capital-only return.

## How it plugs in

Same contract as every valuation method (see the [SKILL](../../SKILL.md), *Estimating ROI*): the
**stock-doc holds the inputs**, the **script writes the output back**.

- **Inputs** live in the stock-doc front matter under `valuation.asymmetric-payoff`.
- **Output** is the annualized ROI, written back surgically as the `roi` child of the
  `valuation.asymmetric-payoff` block, together with the `date` it was computed — the
  staleness stamp the [SKILL](../../SKILL.md) (*Estimating ROI*) describes.

Hand-tweak an input (e.g. the probability) and re-run to refresh the ROI — nothing else is touched.

### Front-matter contract

```yaml
valuation:
  asymmetric-payoff:
    price: 1.00            # entry price per share (today) — the ROI denominator
    floor: 0.85            # downside-support floor per share (must be below price)
    fair-value: 1.60       # fair value once the catalyst plays out (fair-value-upside trait)
    probability: 60%       # the catalyst's probability of success, p (catalyst trait)
    years: 2               # the catalyst window, whole or fractional (catalyst trait)
    roi: 0.0               # written by the script — do not hand-edit; re-run instead
    date: 2026-06-21       # written by the script — the valuation's as-of date
```

`probability` accepts a decimal (`0.6`) or a `%`-suffixed string (`60%`).

## The model

```
downside_pct   = (price − floor)      / price          # loss if it falls to the floor
upside_pct     = (fair_value − price) / price          # gain if it re-rates to fair value
asymmetry      = upside_pct / downside_pct             # the up:down ratio (the freeroll edge)
expected_roi   = p · upside_pct − (1 − p) · downside_pct     # over the holding period
annualized_roi = (1 + expected_roi) ^ (1 / years) − 1
```

- The **asymmetry ratio** is the same number the fair-value-upside trait asks you to state (upside ≫
  downside). Here it is computed from the floor and fair value so it can't drift from the inputs.
- `expected_roi` is the **probability-weighted holding-period** return; `annualized_roi` annualizes
  it over the catalyst window. `floor > 0` and `floor < price` keep the downside real and bounded, so
  `1 + expected_roi` is always positive and the annualization is well-defined.
- A high asymmetry can still produce a poor ROI if `p` is low, and vice-versa — the model forces you
  to be explicit about **both** the payoff and the odds, which is exactly the freeroll discipline.

## Running the script

Do the maths with the script — never by hand. It mirrors `company_score.py`'s interface.

```bash
SCRIPT=skills/stock-analysis/scripts/asymmetric_payoff_valuation.py

# Stock-doc mode: read valuation.asymmetric-payoff inputs, write valuation.asymmetric-payoff.roi back.
"$SCRIPT" --stock-doc SRG.AX
"$SCRIPT" --stock-doc SRG.AX --dry-run --format json     # preview without writing

# Raw mode: an ad-hoc estimate with no stock-doc.
"$SCRIPT" --price 1.00 --floor 0.85 --fair-value 1.60 --probability 60% --years 2
```

## Reading the output

- **Annualized ROI** (`valuation.asymmetric-payoff.roi`) — the headline, comparable across ideas.
  Stamped alongside it is `valuation.asymmetric-payoff.date`, the as-of date of the run (today, or `--as-of`).
- **Expected return** — the probability-weighted return over the whole window (before annualizing).
- **Asymmetry** — upside % ÷ downside %. State it in the write-up; freeroll wants it clearly > 1.
- **Downside / upside %** — the distance to the floor and to fair value, the two legs of the bet.

Feed the result into the stock-doc **Valuation** section alongside the floor, fair value, catalyst,
and sell target the freeroll strategy already requires there (see
[freeroll.md](../strategies/freeroll.md), *Writing it up*). State the basis for `p` and the window so
the next update can re-run with refreshed odds.
