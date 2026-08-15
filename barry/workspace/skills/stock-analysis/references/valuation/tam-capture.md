---
id: tam-capture
name: TAM-Capture Valuation
script: ../../scripts/tam_capture_valuation.py
---

# Valuation method: TAM-Capture

Estimate the annualized ROI of the "it works" case for an early-stage, growth-first company. Read
the company's terminal annual revenue from the market-analysis output, apply mature economics, and
bridge enterprise value to diluted per-share value. This is a survivor path, not a
probability-weighted expectation.

Unlike [exit-multiple](exit-multiple.md), this method does not grow today's earnings or FCF. The
market doc supplies the company's revenue at a fixed 10-year horizon. A matching player override is
canonical; otherwise the method reads `players.model-estimate[].mobility-adjusted-revenue`.

## Applicability

Use this method when the company's value depends on a future market it has yet to capture and a
current per-share earnings/FCF anchor is weak or absent. It requires:

- a market doc with either a matching positive player override or a `players.model-estimate` entry
  containing the company and a positive `mobility-adjusted-revenue`; and
- a credible mature role model for margin, exit multiple, and dilution calibration.

If no suitable market doc exists, stop before stock valuation and spawn a sub-agent to generate it
with the [market-analysis skill](../../../market-analysis/SKILL.md). Resume only after the market doc
has been saved. Use an existing document as-is; do not refresh it merely because valuation is being
run. An existing but incomplete or invalid document is an explicit blocker, not permission to fall
back to an internally estimated TAM or revenue.

## Front-matter contract

```yaml
valuation:
  tam-capture:
    market-doc: us-direct-to-consumer-telehealth
    market-player: HIMS    # optional; exact ticker or name, defaults to stock-doc ticker
    price: 34.38           # entry price per share, in the market doc's currency
    shares: 258230547      # today's diluted share count
    margin: 16%            # mature profit margin, from the role model
    margin-basis: EBIT     # EBITDA or EBIT; must match the exit multiple
    exit-multiple: 22      # EV/EBITDA or EV/EBIT at the 10-year endpoint
    dilution: 10%          # yearly issuance; scalar or a 10-value annual list
    net-debt: 381e6        # terminal net debt; negative means net cash. Default 0
    role-model: TDOC       # source of margin/multiple and dilution calibration
    roi: 0.0               # written by the script; do not hand-edit
    date: 2026-08-01       # written by the script
```

`market-doc` accepts a market id or explicit Markdown path. `market-player` is useful when the
market doc lacks the stock-doc ticker or uses a different security identifier. Matching is exact and
case-insensitive against the player override or model estimate's `ticker` and `name`.

Do not store `years`, `tam`, `capture`, or `terminal-revenue` in this valuation block. The market
doc is their single source of truth: `maturity-duration` supplies the 10-year holding period and the
selected player's canonical override or mobility estimate supplies terminal annual revenue.

The market doc stores revenue in billions of its top-level `currency`; the script converts it to
whole currency units. Express `price` and `net-debt` in that same currency. The script does not make
FX or ADR-ratio conversions.

## Model

```text
years              = market_doc.maturity-duration = 10
terminal_revenue   = canonical selected-player revenue × 1,000,000,000
terminal_profit    = terminal_revenue × margin
terminal_ev        = terminal_profit × exit_multiple
terminal_equity    = terminal_ev − net_debt
shares_10          = shares × Π(1 + dilution_i)
terminal_price     = terminal_equity ÷ shares_10
annualized ROI     = (terminal_price ÷ price)^(1/10) − 1
```

The return decomposes exactly into value creation and dilution:

```text
value creation = (terminal_equity ÷ today's market cap)^(1/10) − 1
dilution       = (1 ÷ Π(1 + dilution_i))^(1/10) − 1
```

## Choosing the remaining inputs

Use one mature role model to keep `margin` and `exit-multiple` on the same profit line. An
EV/EBITDA multiple requires an EBITDA margin; EV/EBIT requires an EBIT margin. Stage-align the role
model's historical share-count path to calibrate dilution. The market-analysis model—not the role
model—owns terminal capture and revenue.

`net-debt` defaults to zero. Set it only when the thesis implies material terminal debt or cash.

The role model is a survivor, and the market estimate is still conditional on the current player
remaining relevant. Treat the result as the reward if the thesis works; carry failure risk in the
strategy confidence rather than mislabelling this output as an unconditional expected return.

## Gathering inputs

Run the companion only after the market doc exists:

```bash
tam_capture_inputs HIMS \
  --market-doc us-direct-to-consumer-telehealth \
  --role-model TDOC
```

It reads terminal revenue and horizon from the market doc, gathers today's subject inputs from
Yahoo, and gathers role-model economics and history from Yahoo and EDGAR. Review currency, margin,
multiple, and dilution before pasting its block into the stock doc.

## Running the valuation

```bash
SCRIPT=skills/stock-analysis/scripts/tam_capture_valuation.py

"$SCRIPT" --stock-doc HIMS
"$SCRIPT" --stock-doc HIMS --dry-run --format json

"$SCRIPT" --ticker HIMS \
  --market-doc us-direct-to-consumer-telehealth \
  --price 34.38 --shares 258230547 --margin 16% \
  --margin-basis EBIT --exit-multiple 22 --dilution 10% \
  --net-debt 381e6 --role-model TDOC
```

The script fails loudly when the document is missing, its horizon is not 10 years, the player cannot
be matched, or the mobility-adjusted revenue is absent or non-positive. It never falls back to the
legacy `tam × capture` calculation.

## Reading the output

Record the market-doc id, selected player and terminal revenue, mature margin and multiple,
dilution, role model, resulting ROI, and value-creation/dilution attribution in the stock doc's
*Valuation* section. The script writes only `valuation.tam-capture.roi` and `date`.
