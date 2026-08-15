#!/usr/bin/env python3
"""Gather the data for the downside-support trait — does the price sit at or near a
structural valuation floor (asset value, net cash, or income) below which a further
decline would be unreasonable? This is the freeroll margin of safety.

The right floor depends on the business, so this lays out the obtainable anchors and
how far the price sits above each:

  * asset floor  — price / book and price / tangible-book (book and tangible-book
    per share vs the current price); a price near or below tangible book is asset support
  * cash floor   — net cash (cash − total debt) per share, and as a share of the price
    (how much of what you pay is backed by cash in the bank)
  * income floor — dividend yield and its FCF cover (a sustainable high yield defends
    the price; an uncovered one doesn't)

The bespoke floors — REIT/property NAV and cap rates, a fund's co-investment stake,
replacement value, sum-of-the-parts — need the filings; Yahoo carries only the generic
book / cash / yield anchors. Whether a floor is conservatively marked, durable, and
actively defended is the agent's read against the trait doc.

Usage:
    downside_support.py TICKER [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (fail, first_present, footer, millions, pctf, pull, rnd,
                      safe_div, title, val, yfin)

TANGIBLE_BOOK_KEYS = ("Tangible Book Value", "Net Tangible Assets")
NOT_COVERED = [
    "Bespoke floors: REIT/property NAV and cap rates, a fund's own co-investment stake, "
    "replacement value, sum-of-the-parts — from the filings",
    "Whether asset marks are conservative/current, and durable (not about to be impaired or spent)",
    "The mechanism that actually defends the price at the floor (yield-seekers, acquirers, NAV arbitrage)",
]


def gather(ticker: str) -> dict:
    info = yfin("info", ticker)
    if not isinstance(info, dict):
        fail(f"no data for {ticker.upper()} — check the symbol or Yahoo coverage.")
    ident = info.get("identity") or {}
    price_g = info.get("price") or {}
    val_g = info.get("valuation") or {}
    per = info.get("per_share") or {}
    fin = info.get("financials") or {}
    own = info.get("ownership") or {}
    div = info.get("dividends") or {}

    price = price_g.get("currentPrice")
    shares = own.get("sharesOutstanding")
    book_ps = per.get("bookValue")
    cash = fin.get("totalCash")
    debt = fin.get("totalDebt")

    bal = pull(ticker, "balance", years=1)
    latest_bal = next(iter(bal.values()), {}) if isinstance(bal, dict) else {}
    tangible_book, _ = first_present(latest_bal, *TANGIBLE_BOOK_KEYS)
    tangible_book_ps = safe_div(tangible_book, shares)

    net_cash = cash - debt if (cash is not None and debt is not None) else None
    net_cash_ps = safe_div(net_cash, shares)
    # Dividend cash paid and FCF (for cover) from the cash-flow statement — info's
    # freeCashflow is computed inconsistently, so use the statement's own figure.
    cf_latest = next(iter(pull(ticker, "cashflow", years=1).values()), {})
    fcf = cf_latest.get("Free Cash Flow")
    dividends_paid = first_present(cf_latest, "Cash Dividends Paid", "Common Stock Dividend Paid")[0]
    dividends_paid = abs(dividends_paid) if isinstance(dividends_paid, (int, float)) else None

    # yfinance returns dividendYield already in percent (3.3 == 3.3%); store a fraction.
    dy = div.get("dividendYield")
    dy_frac = dy / 100.0 if isinstance(dy, (int, float)) else None

    # Price is in the listing currency; statement-derived floors (tangible book, net
    # cash) are in the financial currency. When they differ, those need FX to compare.
    price_ccy, fin_ccy = ident.get("currency"), ident.get("financialCurrency")
    ccy_mismatch = bool(price_ccy and fin_ccy and price_ccy != fin_ccy)

    floors = {
        "price": price,
        "market_cap": val_g.get("marketCap"),
        "book_value_per_share": rnd(book_ps),
        "price_to_book": rnd(safe_div(price, book_ps)),
        "tangible_book_per_share": rnd(tangible_book_ps),
        "price_to_tangible_book": rnd(safe_div(price, tangible_book_ps)),
        "net_cash_per_share": rnd(net_cash_ps),
        "net_cash_pct_of_price": rnd(safe_div(net_cash_ps, price), 3),
        "dividend_yield": rnd(dy_frac, 4),
        "dividend_fcf_cover": rnd(safe_div(fcf, dividends_paid), 2),
    }
    return {
        "ticker": ticker.upper(),
        "trait": "downside-support",
        "currency": price_ccy,
        "price_currency": price_ccy,
        "financial_currency": fin_ccy,
        "currency_mismatch": ccy_mismatch,
        "floors": floors,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    f = r["floors"]
    out = title(r["ticker"], "downside support (valuation floor)", r["currency"])
    out += [f"  Price: {val(f['price'])} {r['price_currency'] or ''}    Market cap: {millions(f['market_cap'])}M"]
    if r["currency_mismatch"]:
        out += [f"  ⚠ price is in {r['price_currency']} but statements are in {r['financial_currency']} —"
                f" tangible-book and net-cash floors below need FX to compare (P/B uses {r['price_currency']} book, OK)."]
    out += [
        "",
        "  ASSET floor", "  " + "-" * 56,
        f"    Book value / share     : {val(f['book_value_per_share'])}   ->  P/B {val(f['price_to_book'], 'x')}",
        f"    Tangible book / share  : {val(f['tangible_book_per_share'])}   ->  P/TB {val(f['price_to_tangible_book'], 'x')}",
        "",
        "  CASH floor", "  " + "-" * 56,
        f"    Net cash (cash − debt) / share : {val(f['net_cash_per_share'])}"
        f"   = {pctf(f['net_cash_pct_of_price'])} of price",
        "",
        "  INCOME floor", "  " + "-" * 56,
        f"    Dividend yield : {pctf(f['dividend_yield'])}    FCF cover : {val(f['dividend_fcf_cover'], 'x')}",
    ]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather book / net-cash / dividend floor metrics for the downside-support trait.")
    p.add_argument("ticker")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()
    r = gather(args.ticker)
    print(json.dumps(r, indent=2) if args.format == "json" else render_table(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
