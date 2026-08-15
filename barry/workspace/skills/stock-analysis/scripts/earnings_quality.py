#!/usr/bin/env python3
"""Gather the data for the earnings-quality trait — demonstrated, consistent earning
power, backed by cash. Covers the trait's three quantitative strands (the accounting-
quality read stays largely qualitative):

  * consistency   — the net-income / EPS track record: down years, loss years, the
    worst year and how deep
  * predictability — the dispersion (std-dev) of year-on-year growth: a tight, low-
    variance path is forecastable; wide dispersion (or true cyclicality) is the tell.
    This is the COMPLEMENT of durable-growth — a steady 8-10% scores better here than
    a lurching +40/-15/+25 with a higher average
  * cash backing  — cumulative FCF / cumulative net income over the window (sturdier
    than any single year); a chronic shortfall is the quality-of-earnings red flag

It also surfaces two accounting-quality tells Yahoo can see: receivables growing faster
than revenue (an accruals flag) and stock-based comp as a share of net income. The
heavier accounting judgement — reliance on adjusted figures, serial "one-offs",
capitalised costs — needs the filings.

Note yfinance serves only ~4 annual years; the trait wants 7-10, so deep-cycle history
(and whether a downturn was survived) comes from the filings.

Usage:
    earnings_quality.py TICKER [--years N] [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (aligned_periods, fail, first_present, footer, millions,
                      pct_change, pctf, pull, rnd, safe_div, stdev, title, val, yfin)

RECEIVABLES_KEYS = ("Accounts Receivable", "Receivables", "Gross Accounts Receivable")
NOT_COVERED = [
    "Deep-cycle track record (yfinance serves ~4 annual years; the trait wants 7-10, "
    "through a downturn) — get the long record from filings",
    "Reliance on adjusted/underlying figures, serial 'one-off' charges, capitalised costs",
]


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    inc = pull(ticker, "income", years=years)
    cf = pull(ticker, "cashflow", years=years)
    bal = pull(ticker, "balance", years=years)
    periods = [p for p in aligned_periods(inc, limit=years)
               if inc.get(p, {}).get("Total Revenue") is not None]
    if not periods:
        fail(f"no income data for {ticker.upper()} — check the symbol or Yahoo coverage.")

    rows = []
    for p in periods:
        i, c, b = inc.get(p, {}), cf.get(p, {}), bal.get(p, {})
        rev = i.get("Total Revenue")
        recv, _ = first_present(b, *RECEIVABLES_KEYS)
        rows.append({
            "period": p,
            "net_income": i.get("Net Income"),
            "diluted_eps": first_present(i, "Diluted EPS", "Basic EPS")[0],
            "revenue": rev,
            "fcf": c.get("Free Cash Flow"),
            "stock_based_comp": c.get("Stock Based Comp") or c.get("Stock Based Compensation"),
            "receivables_pct_revenue": rnd(safe_div(recv, rev), 3),
        })

    # Year-on-year net-income growth (oldest->newest) and its dispersion.
    ni_old_to_new = [r["net_income"] for r in reversed(rows)]
    growths = []
    for prev, cur in zip(ni_old_to_new, ni_old_to_new[1:]):
        g = pct_change(cur, prev)
        if g is not None:
            growths.append(g)
    for r, g in zip(rows[:-1], reversed(growths)):  # attach growth to the newer year
        r["ni_growth_yoy"] = rnd(g, 3)
    if rows:
        rows[-1].setdefault("ni_growth_yoy", None)

    ni_vals = [r["net_income"] for r in rows if isinstance(r["net_income"], (int, float))]
    cum_fcf = sum(r["fcf"] for r in rows if isinstance(r["fcf"], (int, float)))
    cum_ni = sum(v for v in ni_vals)
    worst = min(ni_vals) if ni_vals else None
    summary = {
        "periods_covered": len(rows),
        "loss_years": sum(1 for v in ni_vals if v < 0),
        "worst_year_net_income": worst,
        "ni_growth_dispersion": rnd(stdev(growths), 3),
        "ni_growth_avg": rnd(sum(growths) / len(growths), 3) if growths else None,
        "cumulative_cash_conversion": rnd(safe_div(cum_fcf, cum_ni), 2),
        "receivables_pct_revenue_trend": (
            f"{pctf(rows[-1]['receivables_pct_revenue'])} -> {pctf(rows[0]['receivables_pct_revenue'])}"
            if rows and rows[0]["receivables_pct_revenue"] is not None else "—"),
    }
    return {
        "ticker": ticker.upper(),
        "trait": "earnings-quality",
        "currency": (info.get("identity") or {}).get("financialCurrency") if isinstance(info, dict) else None,
        "periods": rows,
        "summary": summary,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    sm = r["summary"]
    out = title(r["ticker"], "earnings quality (consistent, cash-backed profit)", r["currency"])
    out += [
        f"  ANNUAL series (newest first, net income in {r['currency'] or '?'} millions)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'NetIncome':>11}{'DilEPS':>9}{'NI growth':>11}{'Recv/Rev':>10}",
    ]
    for p in r["periods"]:
        out.append(
            f"    {p['period']:<12}{millions(p['net_income']):>11}{val(p['diluted_eps']):>9}"
            f"{pctf(p.get('ni_growth_yoy')):>11}{pctf(p['receivables_pct_revenue']):>10}"
        )
    out += ["", "  SUMMARY", "  " + "-" * 56,
            f"    Consistency  : {sm['loss_years']} loss year(s) of {sm['periods_covered']}"
            f"   worst NI {millions(sm['worst_year_net_income'])}M",
            f"    Predictability: NI-growth dispersion {pctf(sm['ni_growth_dispersion'])}"
            f"   (avg growth {pctf(sm['ni_growth_avg'])}) — lower dispersion = more forecastable",
            f"    Cash backing : cumulative FCF / net income {val(sm['cumulative_cash_conversion'], 'x')}"
            "   (near/above 1.0x is good)",
            f"    Accruals tell: receivables/revenue {sm['receivables_pct_revenue_trend']}"
            "   (rising faster than sales is a flag)"]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather track-record / predictability / cash-backing data for earnings-quality.")
    p.add_argument("ticker")
    p.add_argument("--years", "-n", type=int, default=10, help="annual periods (default 10; Yahoo serves ~4)")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()
    if args.years < 1:
        fail("--years must be at least 1")
    r = gather(args.ticker, args.years)
    print(json.dumps(r, indent=2) if args.format == "json" else render_table(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
