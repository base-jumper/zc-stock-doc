---
name: yahoo-finance
description: Yahoo Finance data via the `yfin` CLI (JSON output, no API key) — quotes, fundamentals/valuation, financial statements, derived ratios, dividends, holders, calendar, analyst estimates and ratings, and history. Use for any Yahoo Finance lookup or ticker check.
---

# Yahoo Finance

All data comes from the **`yfin`** CLI: source [scripts/yfin.py](scripts/yfin.py),
run via the `yfin` wrapper installed by
scripts/bin/install.sh, backed by a pinned
virtualenv at `.venv/yahoo-finance` (run `install.sh` to create it).

Every command takes a ticker as its first argument and prints JSON to stdout.
Errors are emitted as `{"error": "..."}` with a non-zero exit; stderr stays
quiet.

```bash
yfin quote AAPL                     # price snapshot: price, change, ranges, market cap
yfin info AAPL                      # curated fundamentals (see groups below)
yfin history AAPL -p 5d -i 1d       # OHLCV as a list of records
yfin history AAPL -s 2026-01-01 -e 2026-01-31
yfin income AAPL                    # income statement, annual
yfin income AAPL --period quarterly # also: --period ttm
yfin balance AAPL                   # balance sheet (no ttm)
yfin cashflow AAPL --period ttm     # cash flow, trailing twelve months
yfin metrics AAPL --fields roic -n 5  # derived ratios, computed per period
yfin dividends KO -n 8              # dividend history {date: amount}
yfin actions AAPL                   # dividends + splits by date
yfin calendar AAPL                  # next earnings/dividend dates + consensus
yfin ownership AAPL                 # insider/institution % held
yfin holders AAPL -n 10             # institutional + mutual-fund holders, tagged by Type
yfin insider-transactions AAPL -n 10
yfin insider-roster AAPL
yfin recommendations AAPL           # analyst buy/hold/sell counts by month
yfin upgrades AAPL -n 10            # recent rating changes (newest first)
yfin estimates AAPL                 # forward EPS/revenue/eps-trend/growth
```

`info` groups the most useful keys into a stable schema (every key present, null
when Yahoo omits it): `identity` (incl. `financialCurrency`), `valuation` (P/E,
PEG, P/B, P/S, EV/Revenue, EV/EBITDA), `per_share` (EPS, revenue/share, book
value), `profitability` (margins, ROA, ROE), `growth`, `financials` (revenue,
gross profit, EBITDA, cash, debt, ratios, FCF), `dividends`, `analyst` (price
targets, recommendation), `ownership` (holdings + short interest), `governance`
(risk scores, 1=low…10=high), and `price` (incl. 52-week change vs S&P).

Statement commands (`income`, `balance`, `cashflow`) return
`{period: {line_item: value}}`; `--period` is `annual` (default), `quarterly`,
or `ttm` (income and cashflow only).

### Trimming output

Output can be large, so narrow it before asking:

- `--last N` / `-n N` — keep only the N most recent entries. Periods for the
  statement and `metrics` commands (e.g. `-n 5` for 5 years on annual); rows for
  `dividends`, `splits`, `actions`, `upgrades`, and the list-style `holders`
  views.
- `--fields` / `-f` — field paths, comma- or space-separated
  (`--fields a,b`, `--fields a, b`, and `--fields a b` are equivalent); quote any
  path that itself contains spaces, e.g. `--fields "Total Revenue,EBIT"`. Give the
  ticker before `--fields`, since it greedily consumes following words. Available
  on every command whose records have named fields. Matching is **exact and
  case-insensitive**; paths that match nothing come back under `_unmatched`
  (omitted on list outputs, which can't carry it). The grammar is uniform across
  commands:
  - `x` — the whole top-level entry `x` (a flat field, or an entire group)
  - `y.z` — nested field `z` under `y`
  - `*.z` — field `z` under every nested group

  `--fields` only ever addresses fields *within* a record, never the
  period/horizon/row axis (trim that with `--last`/`--horizon`). So on the
  grouped `info`, `--fields "valuation.trailingPE, per_share.*, *.beta"` picks
  one nested field, a whole group, and a field from any group; on the flat
  statements, `--fields "EBIT,Total Revenue"` picks line items in every period.
- `--list-fields` — print the selectable paths (and, for `metrics`/`estimates`,
  their definitions/horizons) without values, so you can discover exact paths
  cheaply.

### Derived metrics

`metrics` computes ratios that are **not** raw yfinance fields, per period, so
the agent never does the arithmetic. Run `yfin metrics <ticker> --list-fields`
for the catalogue and exact formula of each: `roic`, `roce`, `roe`, `roa`,
`gross_margin`, `operating_margin`, `net_margin`, `fcf_margin`, `fcf`,
`debt_to_equity`. `--period` is `annual` (default) or `quarterly` — note that flow-based
quarterly metrics (e.g. `roic`, margins) are per-quarter, not annualized. A
period yields `null` for a metric when Yahoo omits a required line item (common
for the oldest annual period). Definitions are pinned in
[scripts/yfin.py](scripts/yfin.py); change them there to change the convention.

### Holders and analyst views

- Ownership splits into focused commands: `ownership` (insider/institution
  percentages, `{metric: value}`), `holders` (institutional and mutual-fund
  holders combined into one row list, each tagged with a `Type` of
  `institutional` or `mutual fund`), `insider-transactions`, and
  `insider-roster`. The list commands take `-n` to cap rows — for `holders` it
  caps each type, so `-n 10` yields up to 10 of each.
- `recommendations` returns buy/hold/sell counts keyed by month offset (`0m`,
  `-1m`, …); `upgrades` returns recent rating changes, newest first.
- `estimates` is nested `{horizon: {table: {field: value}}}` — horizon outermost
  since it is shared across tables. Horizons: `0q`=current quarter, `+1q`=next
  quarter, `0y`=current year, `+1y`=next year, `LTG`=long-term (growth only).
  Tables: `earnings`, `revenue`, `eps_trend`, `growth`. Each horizon is a record
  of `{table: {field}}`, so `--fields` follows the standard grammar: bare
  `growth` is a whole table, `earnings.growth` one nested field, `*.growth` that
  field across tables. `--horizon` (exact, comma-separated) trims to specific
  horizons without changing the shape, e.g.
  `yfin estimates HMC.AX --horizon "+1y" --fields earnings.growth`. Estimated
  earnings growth next year is `["+1y"]["earnings"]["growth"]`.

> The old standalone `yf` binary (`~/.local/bin/yf`, source `~/git/yf`)
> is superseded by `yfin` and should not be used.

## Symbol format

- US stocks: `AAPL`, `MSFT`, `GOOGL`
- ASX stocks: `CBA.AX`, `BHP.AX`, `WES.AX`
- Crypto: `BTC-USD`, `ETH-USD`
- Forex: `EURUSD=X`, `AUDUSD=X`

## Notes

- Yahoo data may be delayed or stale outside market hours; mention market
  status / timestamp when relevant.
- yfinance scrapes Yahoo and is subject to rate limits and occasional schema
  changes. The venv pins `yfinance==1.4.1`; bump `YF_VERSION` in `install.sh` if
  Yahoo changes break a command.
- Not yet wrapped in `yfin` but available in yfinance for future commands:
  share-count history (`get_shares_full`), recent news (`news`), SEC filing
  links (`sec_filings`), earnings-date history with surprises (`earnings_dates`),
  and the `yf.screen` equity screener.
