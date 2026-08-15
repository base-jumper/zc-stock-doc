#!/usr/bin/env python3
"""Gather the data for the free-cash-flow-generation trait — how much genuinely free
cash the business throws off, and how little capital it must keep putting in.

Reads one quantity (the free cash generated) through the trait's two lenses, per year
and over the window, with the ratios computed:

  * magnitude       — FCF margin (FCF / revenue), industry-relative
  * forward intensity — capex / operating cash flow (how much OCF survives as FCF)
  * conversion       — FCF / net income, the quick cross-check (decompose when weak:
    accruals are earnings-quality's half, capex is this trait's)
  * the harvesting flag — capex / D&A: persistently below ~1 on a physical-asset
    business flatters FCF now at the cost of a future replacement cliff
  * SBC drag         — stock-based comp as a share of FCF (an add-back that is a real
    cost to owners, so it shouldn't pad the figure)

Yahoo can't split growth vs maintenance capex, so the harvesting read is capex-vs-D&A
plus judgement — the agent's call against the trait doc.

Usage:
    free_cash_flow.py TICKER [--years N] [--format table|json]
"""
from __future__ import annotations

import argparse
import json

from traitlib import (aligned_periods, fail, first_present, footer, millions,
                      pctf, pull, rnd, safe_div, title, trend, ttm_row, val, yfin)

DA_KEYS = ("Depreciation And Amortization", "Depreciation Amortization Depletion",
           "Depreciation & amortization")
NOT_COVERED = [
    "Growth vs maintenance capex split (Yahoo gives only total capex)",
    "Asset condition / replacement cycle behind a capex-below-D&A reading",
    "Deeper-than-Yahoo history (yfinance serves ~4 annual years; the trait wants 5+)",
]


def _row(period: str, inc: dict, cf: dict) -> dict:
    rev = inc.get("Total Revenue")
    ni = inc.get("Net Income")
    fcf = cf.get("Free Cash Flow")
    ocf = cf.get("Operating Cash Flow")
    capex = cf.get("Capital Expenditure")
    da, _ = first_present(cf, *DA_KEYS)
    sbc = cf.get("Stock Based Compensation")
    capex_abs = abs(capex) if isinstance(capex, (int, float)) else None
    return {
        "period": period,
        "revenue": rev,
        "net_income": ni,
        "fcf": fcf,
        "operating_cash_flow": ocf,
        "capex": capex,
        "depreciation_amortization": da,
        "stock_based_comp": sbc,
        # derived
        "fcf_margin": rnd(safe_div(fcf, rev), 3),
        "capex_intensity": rnd(safe_div(capex_abs, ocf), 3),
        "fcf_conversion": rnd(safe_div(fcf, ni), 2),
        "capex_to_da": rnd(safe_div(capex_abs, da), 2),
        "sbc_pct_fcf": rnd(safe_div(sbc, fcf), 2),
    }


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    inc = pull(ticker, "income", years=years)
    cf = pull(ticker, "cashflow", years=years)
    periods = [p for p in aligned_periods(cf, inc, limit=years)
               if inc.get(p, {}).get("Total Revenue") is not None]
    if not periods:
        fail(f"no cash-flow data for {ticker.upper()} — check the symbol or Yahoo coverage.")
    rows = [_row(p, inc.get(p, {}), cf.get(p, {})) for p in periods]

    # info.freeCashflow is computed inconsistently with the statement (often ~½); take
    # the TTM figure from the cash-flow statement so it reconciles with the series.
    cf_ttm = ttm_row(ticker, "cashflow", fields="Free Cash Flow,Operating Cash Flow")
    inc_ttm = ttm_row(ticker, "income", fields="Total Revenue")
    fcf_ttm = cf_ttm.get("Free Cash Flow")
    snapshot = {
        "fcf_ttm": fcf_ttm,
        "fcf_margin_ttm": rnd(safe_div(fcf_ttm, inc_ttm.get("Total Revenue")), 3),
        "operating_cash_flow_ttm": cf_ttm.get("Operating Cash Flow"),
    }

    margins = [r["fcf_margin"] for r in rows if r["fcf_margin"] is not None]
    # Cumulative conversion over the window is sturdier than any single year.
    cum_fcf = sum(r["fcf"] for r in rows if isinstance(r["fcf"], (int, float)))
    cum_ni = sum(r["net_income"] for r in rows if isinstance(r["net_income"], (int, float)))
    summary = {
        "periods_covered": len(rows),
        "fcf_margin_latest": rows[0]["fcf_margin"],
        "fcf_margin_avg": rnd(sum(margins) / len(margins), 3) if margins else None,
        "fcf_margin_trend": trend(rows[0]["fcf_margin"], rows[-1]["fcf_margin"], eps=0.02),
        "cumulative_fcf_conversion": rnd(safe_div(cum_fcf, cum_ni), 2),
        "capex_to_da_latest": rows[0]["capex_to_da"],
    }
    return {
        "ticker": ticker.upper(),
        "trait": "free-cash-flow-generation",
        "currency": (info.get("identity") or {}).get("financialCurrency") if isinstance(info, dict) else None,
        "snapshot": snapshot,
        "periods": rows,
        "summary": summary,
        "not_covered": NOT_COVERED,
    }


def render_table(r: dict) -> str:
    s, sm = r["snapshot"], r["summary"]
    out = title(r["ticker"], "free-cash-flow generation", r["currency"])
    out += [
        f"  FCF (TTM): {millions(s['fcf_ttm'])}M    FCF margin (TTM): {pctf(s['fcf_margin_ttm'])}",
        "",
        f"  ANNUAL series (newest first, {r['currency'] or '?'} millions)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'FCFmargin':>10}{'Capex/OCF':>10}{'FCF/NI':>8}{'Capex/DA':>9}{'FCF':>10}",
    ]
    for p in r["periods"]:
        out.append(
            f"    {p['period']:<12}{pctf(p['fcf_margin']):>10}{pctf(p['capex_intensity']):>10}"
            f"{val(p['fcf_conversion'], 'x'):>8}{val(p['capex_to_da'], 'x'):>9}{millions(p['fcf']):>10}"
        )
    out += ["    Capex/OCF = forward intensity (lower = more OCF survives as FCF).",
            "    Capex/DA < 1x can flag harvesting.  SBC/FCF and OCF are in --format json."]
    out += ["", "  SUMMARY", "  " + "-" * 56,
            f"    FCF margin  latest {pctf(sm['fcf_margin_latest'])}   avg {pctf(sm['fcf_margin_avg'])}"
            f"   trend {sm['fcf_margin_trend']}",
            f"    Cumulative FCF / net income over window: {val(sm['cumulative_fcf_conversion'], 'x')}"
            "   (sturdier than any single year)"]
    out += footer(r["trait"], r["not_covered"])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Gather FCF margin / capital-intensity data for the FCF-generation trait.")
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
