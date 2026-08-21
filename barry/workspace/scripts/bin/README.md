# Command wrappers

Thin launchers that let you run the stock-analysis scripts by name from any
directory, instead of `cd`-ing in and calling `python3 <script>.py`.

| Command            | Wraps                                                       |
|--------------------|------------------------------------------------------------|
| `company_score`    | `skills/stock-analysis/scripts/company_score.py`           |
| `asymmetric_payoff`| `skills/stock-analysis/scripts/asymmetric_payoff_valuation.py` |
| `exit_multiple`    | `skills/stock-analysis/scripts/exit_multiple_valuation.py` |
| `tam_capture`      | `skills/stock-analysis/scripts/tam_capture_valuation.py`   |
| `tam_capture_inputs`| `skills/stock-analysis/scripts/tam_capture_inputs.py`     |
| `weighted_average` | `skills/stock-analysis/scripts/weighted_average_valuation.py` |
| `conservative_debt`| `skills/stock-analysis/scripts/conservative_debt.py`      |
| `returns_on_capital`| `skills/stock-analysis/scripts/returns_on_capital.py`    |
| `free_cash_flow`   | `skills/stock-analysis/scripts/free_cash_flow.py`         |
| `earnings_quality` | `skills/stock-analysis/scripts/earnings_quality.py`       |
| `durable_growth`   | `skills/stock-analysis/scripts/durable_growth.py`         |
| `capital_allocation`| `skills/stock-analysis/scripts/capital_allocation.py`    |
| `organic_growth`   | `skills/stock-analysis/scripts/organic_growth.py`         |
| `fundamental_stability`| `skills/stock-analysis/scripts/fundamental_stability.py` |
| `downside_support` | `skills/stock-analysis/scripts/downside_support.py`       |
| `stock_doc`        | `skills/stock-doc/scripts/stock_doc.py`                    |
| `stock_focus`      | `skills/stock-update/scripts/stock_focus.py`               |
| `market_queue`     | `skills/market-queue/scripts/market_queue.py`              |
| `market_doc`       | `skills/market-doc/scripts/market_doc.py`                  |
| `penetration_fit`  | `skills/market-analysis/scripts/penetration_fit.py`       |
| `concentration_fit`| `skills/market-analysis/scripts/concentration_fit.py`     |
| `mobility_panels`  | `skills/market-analysis/scripts/mobility_panels.py`       |
| `mobility_fit`     | `skills/market-analysis/scripts/mobility_fit.py`          |
| `stock_announcements`| `skills/stock-announcements/scripts/stock_announcements.py` |
| `test_stock_announcements`| `skills/stock-announcements/scripts/test_stock_announcements.py` |
| `yfin`             | `skills/yahoo-finance/scripts/yfin.py`                     |
| `edgar`            | `skills/sec-edgar/scripts/edgar.py`                       |

Each wrapper resolves its own location (following symlinks) to find the repo,
so the scripts stay version-controlled in `skills/` and these only forward args.

`yfin` additionally needs a Python environment with `yfinance`; `install.sh`
builds a pinned virtualenv at `.venv/yahoo-finance` for it (preferring
`uv` when available). `edgar` is stdlib-only (SEC XBRL over `urllib`) and runs on
system `python3`, so it needs no virtualenv.

## Install

```bash
scripts/bin/install.sh          # symlinks into ~/.local/bin
BIN=~/bin scripts/bin/install.sh   # or a directory of your choice
```

Then, from anywhere:

```bash
company_score HMC.AX freeroll
company_score HMC.AX freeroll --dry-run
```

The ticker argument is the stock-doc filename (e.g. `HMC.AX`, not `HMC`).
All script flags pass straight through.
