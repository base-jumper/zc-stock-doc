#!/usr/bin/env python3
"""Gather the data for the durable-growth trait — is the core engine compounding, and
is the growth RATE holding/accelerating rather than quietly decelerating?

Lays out the stage-appropriate growth metrics and, crucially, their second derivative:

  * revenue / EPS / FCF growth, year by year and as a window CAGR
  * the deceleration read — recent growth rate vs the earlier rate (a company going
    40% -> 38% -> 35% is decelerating even though every number still looks strong)
  * gross-margin trend — for a company suppressing profit to reinvest, expanding gross
    margin and improving unit economics is the evidence the reinvestment is working
  * FCF tracking profit — a persistent profit-vs-cash gap is the quality red flag
  * price action — the 52-week move, a continuous *confirming* signal between reports
    (never the primary evidence)

Yahoo carries financials and price, not the operational leading metrics (units, subs,
active users, bookings) an early-stage name should be judged on — those come from the
filings/investor decks.

Usage:
    durable_growth.py TICKER [--years N] [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (aligned_periods, cagr, fail, footer, millions, pct_change,
                      pctf, pull, rnd, safe_div, title, trend, val, yfin)

NOT_COVERED = [
    "Operational leading metrics for an early-stage name (units, subscriptions, active "
    "users, bookings) — from filings / investor decks",
    "Where profit is deliberately suppressed: unit economics and the path to profitability",
]


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    inc = pull(ticker, "income", years=years)
    cf = pull(ticker, "cashflow", years=years)
    # Drop trailing periods Yahoo returns as an all-null column (revenue absent).
    periods = [p for p in aligned_periods(inc, limit=years)
               if inc.get(p, {}).get("Total Revenue") is not None]
    if not periods:
        fail(f"no income data for {ticker.upper()} — check the symbol or Yahoo coverage.")

    rows = []
    for p in periods:
        i, c = inc.get(p, {}), cf.get(p, {})
        rev, gp, ni = i.get("Total Revenue"), i.get("Gross Profit"), i.get("Net Income")
        rows.append({
            "period": p,
            "revenue": rev,
            "gross_margin": rnd(safe_div(gp, rev), 3),
            "net_income": ni,
            "fcf": c.get("Free Cash Flow"),
            "fcf_tracks_ni": rnd(safe_div(c.get("Free Cash Flow"), ni), 2),
        })

    # Revenue growth oldest->newest, then attach newest-first to each newer year.
    rev_old_new = [r["revenue"] for r in reversed(rows)]
    growths = [g for g in (pct_change(c, p) for p, c in zip(rev_old_new, rev_old_new[1:]))]
    for r, g in zip(rows[:-1], reversed(growths)):
        r["revenue_growth_yoy"] = rnd(g, 3)
    if rows:
        rows[-1].setdefault("revenue_growth_yoy", None)

    n = len(rows) - 1
    rev_cagr = cagr(rows[0]["revenue"], rows[-1]["revenue"], n) if n > 0 else None
    # Deceleration: most recent YoY growth vs the one before it.
    recent = [g for g in (r.get("revenue_growth_yoy") for r in rows) if g is not None]
    decel = "—"
    if len(recent) >= 2:
        decel = ("accelerating" if recent[0] - recent[1] > 0.02
                 else "decelerating" if recent[0] - recent[1] < -0.02 else "steady")
    price = (info.get("price") or {}) if isinstance(info, dict) else {}
    summary = {
        "periods_covered": len(rows),
        "revenue_growth_latest": rows[0].get("revenue_growth_yoy"),
        "revenue_cagr": rnd(rev_cagr, 3),
        "growth_rate_direction": decel,
        "gross_margin_trend": trend(rows[0]["gross_margin"], rows[-1]["gross_margin"], eps=0.01),
        "fcf_tracks_ni_latest": rows[0]["fcf_tracks_ni"],
        "price_change_52w": rnd(price.get("52WeekChange"), 3),
    }
    return {
        "ticker": ticker.upper(),
        "trait": "durable-growth",
        "currency": (info.get("identity") or {}).get("financialCurrency") if isinstance(info, dict) else None,
        "periods": rows,
        "summary": summary,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    sm = r["summary"]
    out = title(r["ticker"], "durable / accelerating growth", r["currency"])
    out += [
        f"  ANNUAL series (newest first, revenue in {r['currency'] or '?'} millions)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'Revenue':>12}{'Rev growth':>12}{'GrossMgn':>10}{'FCF/NI':>9}",
    ]
    for p in r["periods"]:
        out.append(
            f"    {p['period']:<12}{millions(p['revenue']):>12}{pctf(p.get('revenue_growth_yoy')):>12}"
            f"{pctf(p['gross_margin']):>10}{val(p['fcf_tracks_ni'], 'x'):>9}"
        )
    out += ["", "  SUMMARY", "  " + "-" * 56,
            f"    Revenue   latest growth {pctf(sm['revenue_growth_latest'])}"
            f"   {len(r['periods'])-1}y CAGR {pctf(sm['revenue_cagr'])}"
            f"   rate is {sm['growth_rate_direction']}",
            f"    Gross margin trend: {sm['gross_margin_trend']}"
            f"     FCF tracks profit (latest): {val(sm['fcf_tracks_ni_latest'], 'x')}",
            f"    Price (52w): {pctf(sm['price_change_52w'])}   (confirming signal only, not primary evidence)"]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather growth-rate / deceleration / margin data for the durable-growth trait.")
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
