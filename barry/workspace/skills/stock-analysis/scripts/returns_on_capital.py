#!/usr/bin/env python3
"""Gather the data for the returns-on-capital trait — the quantitative fingerprint
of a moat: how much the business earns on the capital it employs, and whether it has
*kept* earning it.

Pulls the per-period return ratios `yfin metrics` already computes (ROIC, ROCE, ROE,
ROA — no arithmetic here) over a long window, then layers on the trait's three reads:

  * level & durability — the ROIC/ROCE level across the cycle and its trend
  * the leverage distortion check — the ROE-minus-ROIC gap (a wide gap = returns
    flattered by debt, not operating quality)
  * incremental returns — ΔNOPAT / ΔInvested Capital across the window, the
    forward-looking signal of whether recent capital is still earning the headline rate
  * the goodwill distortion flag — goodwill as a share of invested capital (a serial
    acquirer's reported ROIC can be depressed by goodwill, or flatter it ex-goodwill)

It does NOT judge whether the level is "high": that is the spread over THIS company's
cost of capital (WACC), which Yahoo doesn't carry — so the band is the agent's call
against the trait doc, read against the business's own cost of capital.

Usage:
    returns_on_capital.py TICKER [--years N] [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (aligned_periods, fail, footer, pull, rnd, safe_div,
                      title, trend, val, yfin)

NOT_COVERED = [
    "Cost of capital (WACC) — the spread of ROIC over it is the real 'high' test",
    "Returns ex-goodwill on tangible operating capital (Yahoo gives the goodwill figure, "
    "not a clean tangible-capital return) — recompute from filings for a serial acquirer",
]


def _tax_rate(inc: dict) -> float | None:
    r = inc.get("Tax Rate For Calcs")
    if r is not None:
        return r
    return safe_div(inc.get("Tax Provision"), inc.get("Pretax Income"))


def _nopat(inc: dict) -> float | None:
    ebit, rate = inc.get("EBIT"), _tax_rate(inc)
    return ebit * (1 - rate) if (ebit is not None and rate is not None) else None


def _invested_capital(bal: dict) -> float | None:
    ic = bal.get("Invested Capital")
    if ic is not None:
        return ic
    debt, eq = bal.get("Total Debt"), bal.get("Common Stock Equity")
    return debt + eq if (debt is not None and eq is not None) else None


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    metrics = pull(ticker, "metrics", years=years)
    inc = pull(ticker, "income", years=years)
    bal = pull(ticker, "balance", years=years)

    periods = [p for p in aligned_periods(metrics, limit=years)
               if any(metrics.get(p, {}).get(k) is not None for k in ("roic", "roce", "roe", "roa"))]
    if not periods:
        fail(f"no metrics returned for {ticker.upper()} — check the symbol or Yahoo coverage.")

    rows = []
    for p in periods:
        m = metrics.get(p, {})
        b = bal.get(p, {})
        rows.append({
            "period": p,
            "roic": rnd(m.get("roic"), 3),
            "roce": rnd(m.get("roce"), 3),
            "roe": rnd(m.get("roe"), 3),
            "roa": rnd(m.get("roa"), 3),
            # ROE minus ROIC: a wide positive gap = leverage flattering ROE.
            "roe_minus_roic": rnd((m["roe"] - m["roic"]), 3)
            if (m.get("roe") is not None and m.get("roic") is not None) else None,
            "goodwill_pct_capital": rnd(safe_div(b.get("Goodwill"), _invested_capital(b)), 3),
        })

    # Incremental ROIC across the window: change in NOPAT over change in invested capital.
    latest, earliest = periods[0], periods[-1]
    d_nopat = None
    inc_roic = None
    n0, n1 = _nopat(inc.get(earliest, {})), _nopat(inc.get(latest, {}))
    ic0, ic1 = _invested_capital(bal.get(earliest, {})), _invested_capital(bal.get(latest, {}))
    if None not in (n0, n1, ic0, ic1):
        d_nopat, d_ic = n1 - n0, ic1 - ic0
        inc_roic = rnd(safe_div(d_nopat, d_ic), 3)

    roics = [r["roic"] for r in rows if r["roic"] is not None]
    summary = {
        "periods_covered": len(rows),
        "roic_latest": rows[0]["roic"],
        "roic_avg": rnd(sum(roics) / len(roics), 3) if roics else None,
        "roic_trend": trend(rows[0]["roic"], rows[-1]["roic"], eps=0.02),
        "incremental_roic": inc_roic,
        "roe_minus_roic_latest": rows[0]["roe_minus_roic"],
    }
    prof = (info.get("profitability") or {}) if isinstance(info, dict) else {}
    snapshot = {
        "sector": (info.get("identity") or {}).get("sector") if isinstance(info, dict) else None,
        "roe_ttm": rnd(prof.get("returnOnEquity"), 3),
        "roa_ttm": rnd(prof.get("returnOnAssets"), 3),
    }
    return {
        "ticker": ticker.upper(),
        "trait": "returns-on-capital",
        "currency": (info.get("identity") or {}).get("financialCurrency") if isinstance(info, dict) else None,
        "snapshot": snapshot,
        "periods": rows,
        "summary": summary,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    s, sm = r["snapshot"], r["summary"]
    out = title(r["ticker"], "returns-on-capital (returns on capital employed)", r["currency"])
    out += [
        f"  Sector: {s.get('sector') or '—'}    ROE (TTM, info): {val(s.get('roe_ttm') and round(s['roe_ttm']*100,1), '%')}"
        f"    ROA (TTM): {val(s.get('roa_ttm') and round(s['roa_ttm']*100,1), '%')}",
        "",
        "  ANNUAL returns on capital (newest first, %)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'ROIC':>8}{'ROCE':>8}{'ROE':>8}{'ROA':>8}{'ROE-ROIC':>10}{'GW/IC':>8}",
    ]
    for p in r["periods"]:
        def pc(x):
            return f"{x*100:.1f}" if isinstance(x, (int, float)) else "—"
        out.append(
            f"    {p['period']:<12}{pc(p['roic']):>8}{pc(p['roce']):>8}{pc(p['roe']):>8}"
            f"{pc(p['roa']):>8}{pc(p['roe_minus_roic']):>10}{pc(p['goodwill_pct_capital']):>8}"
        )
    out += ["    ROE-ROIC = leverage distortion (wide gap = debt flattering ROE).  GW/IC = goodwill / invested capital."]

    out += ["", "  SUMMARY", "  " + "-" * 56,
            f"    ROIC   latest {val(sm['roic_latest'] and round(sm['roic_latest']*100,1),'%')}"
            f"   {len(r['periods'])}y avg {val(sm['roic_avg'] and round(sm['roic_avg']*100,1),'%')}"
            f"   trend {sm['roic_trend']}",
            f"    Incremental ROIC (ΔNOPAT/ΔIC over window): "
            f"{val(sm['incremental_roic'] and round(sm['incremental_roic']*100,1),'%')}"
            "   (forward signal — is recent capital still earning the rate?)"]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather ROIC/ROCE/ROE data for the returns-on-capital trait.")
    p.add_argument("ticker")
    p.add_argument("--years", "-n", type=int, default=10, help="annual periods (default 10)")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()
    if args.years < 1:
        fail("--years must be at least 1")
    r = gather(args.ticker, args.years)
    print(json.dumps(r, indent=2) if args.format == "json" else render_table(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
