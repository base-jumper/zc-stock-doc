#!/usr/bin/env python3
"""Gather the data for the capital-allocation trait — how rationally management deploys
the cash the business throws off, across the five uses of cash.

The cash-flow statement itemises the five uses directly, so this lays them out per year
as a share of operating cash flow (where did the cash go?) and computes the read-outs:

  * reinvestment   — capex / OCF
  * acquisitions   — cash spent on M&A / OCF (the price/fit/outcome detail is organic-growth's)
  * dividends      — payout (dividends / net income) and FCF cover (FCF / dividends)
  * buybacks       — repurchases / OCF, and the share-count trend (genuinely shrinking
    the count, or merely offsetting dilution?)
  * balance sheet  — net debt raised (+) or repaid (−)

Plus the headline: total returned to shareholders (dividends + buybacks) as a share of
FCF, and the diluted-share-count change across the window.

The acid test — whether buybacks happened BELOW intrinsic value, and whether the M&A
created per-share value — is judgement Yahoo can't supply; this gives the quantities,
the agent supplies the prices-paid read against the trait doc.

Usage:
    capital_allocation.py TICKER [--years N] [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (aligned_periods, fail, first_present, footer, millions,
                      pct_change, pctf, pull, rnd, safe_div, title, val, yfin)

ACQUISITION_KEYS = ("Purchase Of Business", "Net Business Purchase And Sale")
DIVIDEND_KEYS = ("Cash Dividends Paid", "Common Stock Dividend Paid")
BUYBACK_KEYS = ("Repurchase Of Capital Stock", "Common Stock Payments")
DEBT_KEYS = ("Net Issuance Payments Of Debt", "Net Long Term Debt Issuance")
SHARES_KEYS = ("Diluted Average Shares", "Basic Average Shares")
NOT_COVERED = [
    "The valuations buybacks occurred at vs intrinsic value (the acid test for buybacks)",
    "M&A price/multiple, strategic fit, and subsequent outcomes (see the organic-growth script)",
    "Dividend sustainability judgement beyond the coverage ratios shown",
]


def _abs(x):
    return abs(x) if isinstance(x, (int, float)) else None


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    cf = pull(ticker, "cashflow", years=years)
    inc = pull(ticker, "income", years=years)
    periods = [p for p in aligned_periods(cf, limit=years)
               if cf.get(p, {}).get("Operating Cash Flow") is not None]
    if not periods:
        fail(f"no cash-flow data for {ticker.upper()} — check the symbol or Yahoo coverage.")

    rows = []
    for p in periods:
        c, i = cf.get(p, {}), inc.get(p, {})
        ocf = c.get("Operating Cash Flow")
        fcf = c.get("Free Cash Flow")
        ni = i.get("Net Income")
        capex = _abs(c.get("Capital Expenditure"))
        acq = _abs(first_present(c, *ACQUISITION_KEYS)[0])
        div = _abs(first_present(c, *DIVIDEND_KEYS)[0])
        buyback = _abs(first_present(c, *BUYBACK_KEYS)[0])
        debt = first_present(c, *DEBT_KEYS)[0]  # signed: + raised, - repaid
        shares = first_present(i, *SHARES_KEYS)[0]
        rows.append({
            "period": p,
            "operating_cash_flow": ocf,
            "free_cash_flow": fcf,
            "net_income": ni,
            "capex": capex,
            "acquisitions": acq,
            "dividends": div,
            "buybacks": buyback,
            "net_debt_issuance": debt,
            "diluted_shares": shares,
            # derived (shares of OCF, plus dividend reads)
            "capex_pct_ocf": rnd(safe_div(capex, ocf), 3),
            "acq_pct_ocf": rnd(safe_div(acq, ocf), 3),
            "dividends_pct_ocf": rnd(safe_div(div, ocf), 3),
            "buybacks_pct_ocf": rnd(safe_div(buyback, ocf), 3),
            "payout_ratio": rnd(safe_div(div, ni), 2),
            "dividend_fcf_cover": rnd(safe_div(fcf, div), 2),
        })

    def cum(key):
        return sum(r[key] for r in rows if isinstance(r[key], (int, float)))

    cum_returned = cum("dividends") + cum("buybacks")
    shares_latest, shares_oldest = rows[0]["diluted_shares"], rows[-1]["diluted_shares"]
    summary = {
        "periods_covered": len(rows),
        "shareholder_returns_pct_fcf": rnd(safe_div(cum_returned, cum("free_cash_flow")), 2),
        "cumulative_dividends": cum("dividends"),
        "cumulative_buybacks": cum("buybacks"),
        "cumulative_acquisitions": cum("acquisitions"),
        "payout_ratio_latest": rows[0]["payout_ratio"],
        "dividend_fcf_cover_latest": rows[0]["dividend_fcf_cover"],
        # +ve = share count grew (dilution); -ve = count shrank (real buybacks)
        "share_count_change": rnd(pct_change(shares_latest, shares_oldest), 3),
    }
    return {
        "ticker": ticker.upper(),
        "trait": "capital-allocation",
        "currency": (info.get("identity") or {}).get("financialCurrency") if isinstance(info, dict) else None,
        "periods": rows,
        "summary": summary,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    sm = r["summary"]
    out = title(r["ticker"], "capital allocation (the five uses of cash)", r["currency"])
    out += [
        "  ANNUAL uses of cash as a share of operating cash flow (newest first)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'Capex':>9}{'Acq':>9}{'Dividend':>10}{'Buyback':>9}{'NetDebt':>11}",
    ]
    for p in r["periods"]:
        out.append(
            f"    {p['period']:<12}{pctf(p['capex_pct_ocf']):>9}{pctf(p['acq_pct_ocf']):>9}"
            f"{pctf(p['dividends_pct_ocf']):>10}{pctf(p['buybacks_pct_ocf']):>9}"
            f"{millions(p['net_debt_issuance']):>11}"
        )
    out += ["    NetDebt = net debt raised (+) or repaid (−), in millions.  Payout & FCF-cover in --format json."]
    out += ["", "  SUMMARY (over window)", "  " + "-" * 56,
            f"    To shareholders: {pctf(sm['shareholder_returns_pct_fcf'])} of FCF"
            f"   (dividends {millions(sm['cumulative_dividends'])}M + buybacks {millions(sm['cumulative_buybacks'])}M)",
            f"    Acquisitions   : {millions(sm['cumulative_acquisitions'])}M spent",
            f"    Dividend       : payout {pctf(sm['payout_ratio_latest'])}   FCF cover {val(sm['dividend_fcf_cover_latest'], 'x')}",
            f"    Share count    : {pctf(sm['share_count_change'])} over window"
            "   (− = real buybacks shrinking the count; + = net dilution)"]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather the five-uses-of-cash data for the capital-allocation trait.")
    p.add_argument("ticker")
    p.add_argument("--years", "-n", type=int, default=5, help="annual periods (default 5)")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()
    if args.years < 1:
        fail("--years must be at least 1")
    r = gather(args.ticker, args.years)
    print(json.dumps(r, indent=2) if args.format == "json" else render_table(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
