#!/usr/bin/env python3
"""Gather the data for the organic-growth trait — growth the company BUILT rather than
BOUGHT.

Yahoo doesn't disclose organic (ex-acquisition, constant-currency) revenue, so this
gives the M&A FINGERPRINT — the balance-sheet and cash-flow tracks that acquisitive
growth leaves — for the agent to weigh against the headline growth:

  * revenue growth — the headline the fingerprint is read against
  * goodwill — its level and trend, and as a share of total assets (a ballooning
    goodwill balance is bought growth accumulating on the balance sheet)
  * acquisition spend — cash out the door on M&A each year, and cumulatively
  * share-count trend — deals funded by issuing stock show up as dilution

A wide gap between healthy headline growth and a heavy M&A fingerprint (goodwill
climbing, big acquisition outflows, rising share count) is the tell that the growth was
bought. The clean organic figure, the price/multiple/premium paid, and any goodwill
impairments need the filings.

Usage:
    organic_growth.py TICKER [--years N] [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (aligned_periods, cagr, fail, first_present, footer, millions,
                      pct_change, pctf, pull, rnd, safe_div, title, trend, val, yfin)

GOODWILL_KEYS = ("Goodwill", "Goodwill And Other Intangible Assets")
ACQUISITION_KEYS = ("Purchase Of Business", "Net Business Purchase And Sale")
SHARES_KEYS = ("Diluted Average Shares", "Basic Average Shares")
NOT_COVERED = [
    "Organic (ex-acquisition, constant-currency) revenue growth — Yahoo gives only total",
    "Per-deal price/multiple paid, premium over the undisturbed price, goodwill created",
    "Goodwill impairments and divestitures of past acquisitions (evidence of overpayment)",
]


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    inc = pull(ticker, "income", years=years)
    bal = pull(ticker, "balance", years=years)
    cf = pull(ticker, "cashflow", years=years)
    periods = [p for p in aligned_periods(inc, bal, limit=years)
               if inc.get(p, {}).get("Total Revenue") is not None]
    if not periods:
        fail(f"no data for {ticker.upper()} — check the symbol or Yahoo coverage.")

    rows = []
    for p in periods:
        i, b, c = inc.get(p, {}), bal.get(p, {}), cf.get(p, {})
        rev = i.get("Total Revenue")
        gw, _ = first_present(b, *GOODWILL_KEYS)
        acq = first_present(c, *ACQUISITION_KEYS)[0]
        rows.append({
            "period": p,
            "revenue": rev,
            "goodwill": gw,
            "goodwill_pct_assets": rnd(safe_div(gw, b.get("Total Assets")), 3),
            "acquisition_spend": abs(acq) if isinstance(acq, (int, float)) else None,
            "diluted_shares": first_present(i, *SHARES_KEYS)[0],
        })

    # Revenue growth oldest->newest, attached newest-first.
    rev_on = [r["revenue"] for r in reversed(rows)]
    growths = [pct_change(c, p) for p, c in zip(rev_on, rev_on[1:])]
    for r, g in zip(rows[:-1], reversed(growths)):
        r["revenue_growth_yoy"] = rnd(g, 3)
    if rows:
        rows[-1].setdefault("revenue_growth_yoy", None)

    n = len(rows) - 1
    cum_acq = sum(r["acquisition_spend"] for r in rows if isinstance(r["acquisition_spend"], (int, float)))
    summary = {
        "periods_covered": len(rows),
        "revenue_cagr": rnd(cagr(rows[0]["revenue"], rows[-1]["revenue"], n), 3) if n > 0 else None,
        "goodwill_latest": rows[0]["goodwill"],
        "goodwill_pct_assets_latest": rows[0]["goodwill_pct_assets"],
        "goodwill_trend": trend(rows[0]["goodwill_pct_assets"], rows[-1]["goodwill_pct_assets"], eps=0.01),
        "cumulative_acquisition_spend": cum_acq,
        "share_count_change": rnd(pct_change(rows[0]["diluted_shares"], rows[-1]["diluted_shares"]), 3),
    }
    return {
        "ticker": ticker.upper(),
        "trait": "organic-growth",
        "currency": (info.get("identity") or {}).get("financialCurrency") if isinstance(info, dict) else None,
        "periods": rows,
        "summary": summary,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    sm = r["summary"]
    out = title(r["ticker"], "organic vs acquisitive growth (M&A fingerprint)", r["currency"])
    out += [
        f"  ANNUAL series (newest first, {r['currency'] or '?'} millions)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'Revenue':>12}{'Rev growth':>12}{'Goodwill':>11}{'GW/Assets':>11}{'Acq spend':>11}",
    ]
    for p in r["periods"]:
        out.append(
            f"    {p['period']:<12}{millions(p['revenue']):>12}{pctf(p.get('revenue_growth_yoy')):>12}"
            f"{millions(p['goodwill']):>11}{pctf(p['goodwill_pct_assets']):>11}{millions(p['acquisition_spend']):>11}"
        )
    out += ["", "  FINGERPRINT (over window)", "  " + "-" * 56,
            f"    Revenue CAGR        : {pctf(sm['revenue_cagr'])}",
            f"    Goodwill / assets   : {pctf(sm['goodwill_pct_assets_latest'])} latest, trend {sm['goodwill_trend']}",
            f"    Acquisition spend   : {millions(sm['cumulative_acquisition_spend'])}M cumulative",
            f"    Share count change  : {pctf(sm['share_count_change'])}   (+ = dilution, deals funded with stock)",
            "    Heavy fingerprint (goodwill climbing + big acq spend + rising shares) under healthy",
            "    headline growth = growth likely bought, not built."]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather the M&A fingerprint (goodwill / acquisition spend / dilution) for organic-growth.")
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
