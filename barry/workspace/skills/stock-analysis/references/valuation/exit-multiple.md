---
id: exit-multiple
name: Exit-Multiple Valuation
script: ../../scripts/exit_multiple_valuation.py
---

# Valuation method: Exit-Multiple

Estimates the **expected annualized ROI** of holding a stock for a set number of years. Rather than
discounting cash flows to a fair value, it works forward: grow a fundamental, apply the multiple you
expect at sale, collect dividends along the way, and annualize the gain off today's price. The
output is a forward return you can compare against other ideas.

This is an **equity, per-share** model — anchor on Earnings/share or FCF/share, never on enterprise
metrics (EV/EBITDA). There is no net-debt bridge; debt and capital structure are assumed to live
inside the per-share earnings/FCF path already. (That equity-only basis is why this method does
**not** fit asset/NAV or sum-of-the-parts catalysts — those need a different method.)

## Applicability

Applicable only when the company has a **positive per-share fundamental to anchor on** — i.e. it is
already earning (or generating FCF) enough that today's owner-earnings figure is positive and not a
rounding artefact. For a pre-profit or barely-profitable company the anchor and the implied entry
multiple are meaningless, so this method does not apply; value it with [tam-capture](tam-capture.md)
instead. When a strategy blends methods via [weighted-average](weighted-average.md), **omit
exit-multiple from the weights** for any company that fails this test (the script will refuse a
non-positive fundamental regardless).

## How it plugs in

This is one valuation method in the [ROI estimation flow](../../SKILL.md) (*Estimating ROI*). A
strategy that names `valuation: exit-multiple` in its front matter uses it. The mechanics are the
same as scoring: **the stock-doc holds the inputs, the script writes the output back.**

- **Inputs** live in the stock-doc front matter under `valuation.exit-multiple` (the analyst
  generates them during the analysis, the same way trait scores are generated).
- **Output** is the annualized ROI, written back surgically as the `roi` child of the
  `valuation.exit-multiple` block, together with the `date` it was computed — the
  staleness stamp the [SKILL](../../SKILL.md) (*Estimating ROI*) describes — and the
  `entry-multiple` (`price ÷ fundamental`), recorded next to `price` so the reader sees
  what multiple that price implied.

This lets you hand-tweak an input and re-run the script to refresh the ROI, with no other edits.

### Front-matter contract

```yaml
valuation:
  exit-multiple:
    price: 476.89          # entry price per share (today) — the ROI denominator
    entry-multiple: 24.36  # written by the script — price ÷ fundamental; do not hand-edit
    years: 5               # holding period, whole years
    metric: Earnings       # Earnings or FCF — must match `fundamental` and `exit-multiple`
    fundamental: 19.575    # best estimate for TODAY's per-share fundamental, not trailing or forward
    growth: 8%             # AGGREGATE business growth; scalar, or a per-year list [10%, 9%, 8%, 7%, 6%]
    exit-multiple: 22      # P/E or P/FCF expected at sale; must match metric
    dilution: -1.5%        # signed share-count change: + dilution / - buyback. Optional, default 0
    dividend-yield: 1.2%   # OR payout: 30% (fraction of the fundamental). Optional; omit for non-payers
    roi: 0.0               # written by the script — do not hand-edit; re-run instead
    date: 2026-06-21       # written by the script — the valuation's as-of date
```

Store rates as decimals (`0.08`) or `%`-suffixed strings (`8%`) — both work. `growth` and `dilution`
accept a YAML list for a per-year fade. Keep `growth` and `dilution` **separate**: if you fold share
issuance into `growth` and also pass it as `dilution`, you double-count it.

### Choosing the fundamental

`fundamental` must be the best estimate of the company's **current** per-share fundamental as of the
price date. Do **not** use a stale trailing figure or a pure forward estimate directly. Instead,
triangulate between the most recent actual result/run-rate and credible forward guidance/consensus to
estimate what the business is earning or producing **today**. State the basis in the Valuation
section, including whether the anchor is interpolated, run-rate adjusted, seasonally adjusted, or
normalised.

Use `metric: FCF` when cash conversion is central, capex/working capital are meaningful, accounting
earnings are noisy, or valuation is usually cash-flow based. Use `metric: Earnings` when earnings are
clean, recurring, comparable, and the market normally values the company on P/E. Keep the exit
multiple consistent: `FCF` → P/FCF; `Earnings` → P/E.

## The model

```
fundamental_t = fundamental_0 × Π(1 + gᵢ) / Π(1 + dᵢ)      (per-share path)
exit_price    = exit_multiple × fundamental_N
annualized ROI = IRR[ −price ,  div₁ … div_{N−1} ,  div_N + exit_price ]
```

- **`gᵢ` is aggregate (business) growth** of net income / FCF — *not* per-share growth.
- **`dᵢ` is the signed dilution rate**, a percentage of shares on issue. It converts aggregate growth
  to a per-share figure. `+` = dilution (drags per-share down), `−` = net buybacks (accretive).
- **Dividends are always reinvested.** Reinvesting interim cash flows at the project's own return is
  exactly what an IRR assumes, so the expected return is simply the IRR of the cash-flow stream — no
  intra-period price path is needed or assumed.
- The **entry multiple is implied**, not an input: `price ÷ fundamental_0`. The script records it
  back as `entry-multiple` (a derived stamp, not an input — re-run rather than hand-edit it). The gap
  between it and your `exit-multiple` is the re-rating, and it shows up in the attribution.

## Running the script

Do the maths with the script — never by hand. It mirrors `company_score.py`'s interface.

```bash
SCRIPT=skills/stock-analysis/scripts/exit_multiple_valuation.py

# Stock-doc mode: read valuation.exit-multiple inputs, write valuation.exit-multiple.roi back.
"$SCRIPT" --stock-doc HUBB
"$SCRIPT" --stock-doc HUBB --dry-run --format json     # preview without writing

# Raw mode: an ad-hoc estimate with no stock-doc.
"$SCRIPT" --price 100 --years 5 --fundamental 5 \
          --growth 10% --exit-multiple 18 --payout 30% --dilution 1.5%
```

Two gotchas in **raw** mode (front-matter mode is immune to both — YAML handles it):

- **Rates are decimals unless suffixed with `%`.** `--growth 0.10` and `--growth 10%` are the same;
  `--growth 10` means **1000%**. Prefer the `%` suffix.
- **Negative values (buybacks) need the `=` form**, or argparse mistakes them for a flag:
  `--dilution=-2%` ✓, not `--dilution -2%` ✗. Per-year lists work too: `--dilution=-2%,-2%,1%,1%`.

## Reading the output

- **Annualized ROI** (`valuation.exit-multiple.roi`) — the headline annualized total return (IRR), with the
  total return multiple over the holding period. Stamped alongside it are `valuation.exit-multiple.date`,
  the as-of date of the run (today, or `--as-of`), and `valuation.exit-multiple.entry-multiple`, the
  `price ÷ fundamental` multiple paid at entry.
- **Return attribution** — the Damodaran-style breakdown of where the return comes from:
  - **business growth** — the aggregate earnings/FCF CAGR,
  - **dilution** — the per-share drag (negative) or buyback lift (positive),
  - **multiple re-rating** — entry multiple → exit multiple,
  - **income** — the dividend contribution.

  The first three compose (multiplicatively) into the price return; income is the additional uplift.
  Use this to see *why* a return is what it is — a result leaning on multiple expansion is more
  fragile than one carried by growth.

Feed the result into the stock-doc **Valuation** section: record the assumptions used (growth, exit
multiple, holding period), the resulting ROI, and the attribution, so the next update can re-run with
refreshed numbers. State the assumptions explicitly — the output is only as good as the exit multiple
and growth path you feed it, so make them defensible and note their source.
