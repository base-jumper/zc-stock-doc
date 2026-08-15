#!/usr/bin/env python3
"""Gather the data for the fundamental-stability trait — is the earning power durable,
or is it a melting ice cube in secular decline?

The trait is a qualitative DIAGNOSIS (cyclical vs one-off vs structural), but its one
quantitative input is the trajectory of the fundamentals — is the earning power stable,
deteriorating, or recovering? This lays that trajectory out and measures the erosion:

  * revenue, gross / operating / net margin, EPS and FCF, year by year
  * for each, the latest vs its window peak — the drawdown-from-peak is the melting
    measure — and a coarse direction

A business sitting near its peak with steady margins is stable; one a long way below
peak on every line and still falling is the ice cube. WHY it is falling — and whether
that cause is cyclical, one-off, or structural — is the agent's diagnosis, from the
operating evidence (volumes, churn, occupancy, orders) Yahoo doesn't carry.

Usage:
    fundamental_stability.py TICKER [--years N] [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (aligned_periods, fail, first_present, footer, millions,
                      pctf, pull, rnd, safe_div, title, trend, val, yfin)

NOT_COVERED = [
    "The CAUSE of any weakness — cyclical / one-off / structural — the trait's core diagnosis",
    "Operating leading indicators (volumes, churn, occupancy, orders, demand signals)",
    "Structural threats gathering against a currently-healthy business (disruption, substitution)",
]


def _drawdown(latest, peak):
    """How far below its window peak the latest figure sits (a fraction, <= 0)."""
    if latest is None or peak is None or peak == 0:
        return None
    return (latest - peak) / abs(peak)


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    inc = pull(ticker, "income", years=years)
    cf = pull(ticker, "cashflow", years=years)
    periods = [p for p in aligned_periods(inc, limit=years)
               if inc.get(p, {}).get("Total Revenue") is not None]
    if not periods:
        fail(f"no income data for {ticker.upper()} — check the symbol or Yahoo coverage.")

    rows = []
    for p in periods:
        i, c = inc.get(p, {}), cf.get(p, {})
        rev = i.get("Total Revenue")
        rows.append({
            "period": p,
            "revenue": rev,
            "gross_margin": rnd(safe_div(i.get("Gross Profit"), rev), 3),
            "operating_margin": rnd(safe_div(i.get("Operating Income"), rev), 3),
            "net_margin": rnd(safe_div(i.get("Net Income"), rev), 3),
            "diluted_eps": first_present(i, "Diluted EPS", "Basic EPS")[0],
            "fcf": c.get("Free Cash Flow"),
        })

    def line(key):
        vals = [r[key] for r in rows if isinstance(r[key], (int, float))]
        if not vals:
            return None
        latest, peak = rows[0][key], max(vals)
        return {
            "latest": rnd(latest, 3) if isinstance(latest, (int, float)) else None,
            "peak": rnd(peak, 3),
            "off_peak": rnd(_drawdown(latest, peak), 3),
            "trend": trend(rows[0][key], rows[-1][key],
                           eps=0.01 if key.endswith("margin") else max(abs(peak) * 0.02, 1e-9)),
        }

    summary = {"periods_covered": len(rows),
               **{k: line(k) for k in ("revenue", "operating_margin", "diluted_eps", "fcf")}}
    return {
        "ticker": ticker.upper(),
        "trait": "fundamental-stability",
        "currency": (info.get("identity") or {}).get("financialCurrency") if isinstance(info, dict) else None,
        "periods": rows,
        "summary": summary,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    out = title(r["ticker"], "fundamental stability (is the earning power eroding?)", r["currency"])
    out += [
        f"  ANNUAL trajectory (newest first, revenue/FCF in {r['currency'] or '?'} millions)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'Revenue':>11}{'GrossMgn':>10}{'OpMgn':>8}{'NetMgn':>8}{'DilEPS':>9}{'FCF':>10}",
    ]
    for p in r["periods"]:
        out.append(
            f"    {p['period']:<12}{millions(p['revenue']):>11}{pctf(p['gross_margin']):>10}"
            f"{pctf(p['operating_margin']):>8}{pctf(p['net_margin']):>8}{val(p['diluted_eps']):>9}{millions(p['fcf']):>10}"
        )
    out += ["", "  EROSION READ (latest vs window peak)", "  " + "-" * 56]
    labels = {"revenue": "Revenue", "operating_margin": "Operating margin",
              "diluted_eps": "Diluted EPS", "fcf": "Free cash flow"}
    for key, lab in labels.items():
        s = r["summary"].get(key)
        if s:
            out.append(f"    {lab:<18} {pctf(s['off_peak'])} off peak   trend {s['trend']}")
    out += ["    A long way off peak on every line and still falling = the melting ice cube;",
            "    near peak and steady = stable. The CAUSE is the agent's diagnosis."]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather the fundamentals trajectory (erosion read) for fundamental-stability.")
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
