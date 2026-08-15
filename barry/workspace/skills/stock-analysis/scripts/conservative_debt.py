#!/usr/bin/env python3
"""Gather the data for the conservative-debt / financial-strength trait.

Pulls the targeted Yahoo figures the trait reads — leverage, interest coverage, and
the near-term-vs-long-term debt split — through yfin, and computes the derived ratios
so the agent never does the arithmetic:

  * net debt / EBITDA            — leverage, judged against the business type
  * EBIT / net interest          — interest coverage (EBITDA / net interest cross-check)
  * current vs long-term debt     — a maturity-wall proxy (current debt is due <12mo)
  * net debt / FCF, debt / equity — supporting gearing reads

It reports two views: a CURRENT snapshot from `yfin info` (TTM-ish, so it does not lag
the last annual filing) and an annual SERIES (newest first) so leverage can be read
through the cycle — a peak-of-cycle figure flatters a cyclical.

It deliberately does NOT score, and does NOT tag a band: which column of the trait's
net-debt/EBITDA and coverage tables a figure belongs in depends on the business type
and a through-cycle read — the agent's judgement, against the trait doc. The script
surfaces the sector/industry to inform that call, and lists what Yahoo cannot see
(the maturity ladder, fixed/floating split, undrawn facilities, pension/lease and
other off-balance-sheet claims) so those go to primary sources.

Usage:
    conservative_debt.py TICKER [--years N] [--format table|json]

All Yahoo access goes through yfin; this script has no network or secrets of its own.
"""
from __future__ import annotations

import argparse
import json

from traitlib import fail, first_present, millions, rnd, safe_div, yfin

# yfinance line-item aliases, preferred name first (see traitlib.first_present).
EBITDA_KEYS = ("EBITDA", "Normalized EBITDA")
INTEREST_EXPENSE_KEYS = ("Interest Expense", "Interest Expense Non Operating")
INTEREST_INCOME_KEYS = ("Interest Income", "Interest Income Non Operating")
CASH_KEYS = ("Cash Cash Equivalents And Short Term Investments", "Cash And Cash Equivalents")
CURRENT_DEBT_KEYS = ("Current Debt And Capital Lease Obligation", "Current Debt")
LONGTERM_DEBT_KEYS = ("Long Term Debt And Capital Lease Obligation", "Long Term Debt")
EQUITY_KEYS = ("Stockholders Equity", "Common Stock Equity")

# yfin can't see these; the agent gets them from filings (they live in the trait doc's
# refinancing-risk and hidden-claims bullets — not restated here, just pointed at).
NOT_COVERED = [
    "Maturity ladder / schedule (laddered vs a concentrated wall) beyond the current/long-term split",
    "Fixed vs floating split of the debt",
    "Undrawn committed credit facilities (liquidity backstop)",
    "Off-balance-sheet and hidden claims: pension deficits, factoring, guarantees, "
    "operating-lease detail beyond the capitalised lease figure shown",
]


def period_row(period: str, inc: dict, bal: dict, cf: dict) -> dict:
    """Compute one annual period's leverage and coverage figures from the statements."""
    ebit = inc.get("EBIT")
    ebitda, _ = first_present(inc, *EBITDA_KEYS)
    int_exp, _ = first_present(inc, *INTEREST_EXPENSE_KEYS)
    int_inc, _ = first_present(inc, *INTEREST_INCOME_KEYS)
    # Net interest = interest expense - interest income (fall back to gross expense).
    net_interest = int_exp - int_inc if (int_exp is not None and int_inc is not None) else int_exp

    total_debt = bal.get("Total Debt")
    cash, cash_key = first_present(bal, *CASH_KEYS)
    # Prefer the balance sheet's own Net Debt; else total debt - cash.
    net_debt = bal.get("Net Debt")
    if net_debt is None:
        net_debt = total_debt - cash if (total_debt is not None and cash is not None) else None
    current_debt, _ = first_present(bal, *CURRENT_DEBT_KEYS)
    longterm_debt, _ = first_present(bal, *LONGTERM_DEBT_KEYS)
    equity, _ = first_present(bal, *EQUITY_KEYS)
    leases = bal.get("Capital Lease Obligations")
    fcf = cf.get("Free Cash Flow")

    # Refinancing self-funding: can a year's maturities be met from cash + one year's
    # FCF without tapping credit markets? (times covered; >1 = self-fundable).
    liquidity = cash + fcf if (cash is not None and fcf is not None) else None

    return {
        "period": period,
        "ebit": ebit,
        "ebitda": ebitda,
        "net_interest": net_interest,
        "total_debt": total_debt,
        "cash": cash,
        "cash_basis": cash_key,
        "net_debt": net_debt,
        "current_debt": current_debt,
        "long_term_debt": longterm_debt,
        "capital_leases": leases,
        "stockholders_equity": equity,
        "free_cash_flow": fcf,
        # derived
        "net_debt_to_ebitda": rnd(safe_div(net_debt, ebitda)),
        "interest_coverage_ebit": rnd(safe_div(ebit, net_interest), 1),
        "interest_coverage_ebitda": rnd(safe_div(ebitda, net_interest), 1),
        "net_debt_to_fcf": rnd(safe_div(net_debt, fcf), 1),
        "debt_to_equity": rnd(safe_div(total_debt, equity)),
        "near_term_debt_cover": rnd(safe_div(liquidity, current_debt), 1),
    }


def build_snapshot(info: dict, inc_ttm: dict) -> dict:
    """Current read that does not lag the last annual filing: leverage from `yfin
    info` (TTM-ish) and coverage computed from the trailing-twelve-month income
    statement (info carries no interest line, so coverage needs the TTM statement)."""
    ident = info.get("identity", {}) or {}
    fin = info.get("financials", {}) or {}
    val = info.get("valuation", {}) or {}
    total_debt = fin.get("totalDebt")
    cash = fin.get("totalCash")
    ebitda = fin.get("ebitda")
    net_debt = total_debt - cash if (total_debt is not None and cash is not None) else None

    ebit_t = inc_ttm.get("EBIT")
    ebitda_t, _ = first_present(inc_ttm, *EBITDA_KEYS)
    int_exp_t, _ = first_present(inc_ttm, *INTEREST_EXPENSE_KEYS)
    int_inc_t, _ = first_present(inc_ttm, *INTEREST_INCOME_KEYS)
    net_int_t = (int_exp_t - int_inc_t) if (int_exp_t is not None and int_inc_t is not None) else int_exp_t
    return {
        "sector": ident.get("sector"),
        "industry": ident.get("industry"),
        "currency": ident.get("financialCurrency"),
        "total_debt": total_debt,
        "total_cash": cash,
        "ebitda_ttm": ebitda,
        "net_debt": net_debt,
        "net_debt_to_ebitda": rnd(safe_div(net_debt, ebitda)),
        "interest_coverage_ebit_ttm": rnd(safe_div(ebit_t, net_int_t), 1),
        "interest_coverage_ebitda_ttm": rnd(safe_div(ebitda_t, net_int_t), 1),
        "ev_to_ebitda": rnd(val.get("enterpriseToEbitda")),
        "current_ratio": rnd(fin.get("currentRatio")),
        "quick_ratio": rnd(fin.get("quickRatio")),
        "free_cash_flow_ttm": fin.get("freeCashflow"),
    }


def build_summary(rows: list[dict]) -> dict:
    """Through-cycle reads over the series: the worst (peak) leverage and weakest
    coverage years, and the leverage trend — all plain arithmetic, no judgement."""
    lev = [(r["period"], r["net_debt_to_ebitda"]) for r in rows if r["net_debt_to_ebitda"] is not None]
    cov = [(r["period"], r["interest_coverage_ebit"]) for r in rows if r["interest_coverage_ebit"] is not None]
    summary: dict = {"periods_covered": len(rows)}
    if lev:
        peak = max(lev, key=lambda x: x[1])
        summary["leverage_latest"] = {"period": lev[0][0], "net_debt_to_ebitda": lev[0][1]}
        summary["leverage_peak"] = {"period": peak[0], "net_debt_to_ebitda": peak[1]}
        if len(lev) >= 2:
            delta = lev[0][1] - lev[-1][1]  # newest minus oldest
            summary["leverage_trend"] = (
                "rising" if delta > 0.1 else "falling" if delta < -0.1 else "flat"
            )
    if cov:
        weakest = min(cov, key=lambda x: x[1])
        summary["coverage_latest"] = {"period": cov[0][0], "interest_coverage_ebit": cov[0][1]}
        summary["coverage_weakest"] = {"period": weakest[0], "interest_coverage_ebit": weakest[1]}
    sf = [(r["period"], r["near_term_debt_cover"]) for r in rows if r["near_term_debt_cover"] is not None]
    if sf:
        summary["near_term_cover_latest"] = {"period": sf[0][0], "near_term_debt_cover": sf[0][1]}
    return summary


def gather(ticker: str, years: int) -> dict:
    info = yfin("info", ticker)
    bal = yfin("balance", ticker, "-n", years)
    inc = yfin("income", ticker, "-n", years)
    cf = yfin("cashflow", ticker, "-n", years, "--fields", "Free Cash Flow")
    inc_ttm_raw = yfin("income", ticker, "--period", "ttm")
    inc_ttm = next(iter(inc_ttm_raw.values()), {}) if isinstance(inc_ttm_raw, dict) else {}

    # Annual statements share fiscal-year-end keys; align on the union, newest first,
    # dropping any trailing all-null column Yahoo returns (no debt and no EBIT figure).
    periods = [p for p in sorted(set(bal) | set(inc), reverse=True)[:years]
               if bal.get(p, {}).get("Total Debt") is not None or inc.get(p, {}).get("EBIT") is not None]
    rows = [period_row(p, inc.get(p, {}), bal.get(p, {}), cf.get(p, {})) for p in periods]

    snapshot = build_snapshot(info, inc_ttm)
    # An unknown symbol yields empty statements and a blank info dict rather than a
    # yfin error; catch that here so the agent gets a clear message, not a skeleton.
    if not rows and all(snapshot.get(k) is None for k in ("total_debt", "total_cash", "ebitda_ttm")):
        fail(f"no financial data returned for {ticker.upper()} — check the symbol "
             "(e.g. CBA.AX for ASX) or whether Yahoo covers this security.")
    return {
        "ticker": ticker.upper(),
        "trait": "conservative-debt",
        "currency": snapshot.get("currency"),
        "snapshot": snapshot,
        "periods": rows,
        "summary": build_summary(rows),
        "not_covered": NOT_COVERED,
    }


# --- rendering ---------------------------------------------------------------

def _v(x: Any, suffix: str = "") -> str:
    """A figure for the table, or an em dash when missing."""
    return f"{x}{suffix}" if x is not None else "—"


def render_table(r: dict) -> str:
    s = r["snapshot"]
    out = [
        f"{r['ticker']}  —  conservative-debt (financial strength)   [{r.get('currency') or '?'}]",
        "=" * 66,
        f"  Sector / industry : {s.get('sector') or '—'} / {s.get('industry') or '—'}",
        "",
        "  CURRENT snapshot (yfin info + TTM income, so it doesn't lag the last filing)",
        "  " + "-" * 56,
        f"    Net debt / EBITDA : {_v(s['net_debt_to_ebitda'])}"
        f"      (net debt {millions(s['net_debt'])}M / EBITDA {millions(s['ebitda_ttm'])}M)",
        f"    Interest cover    : {_v(s['interest_coverage_ebit_ttm'], 'x')} EBIT"
        f"   {_v(s['interest_coverage_ebitda_ttm'], 'x')} EBITDA   (TTM, over net interest)",
        f"    EV / EBITDA       : {_v(s['ev_to_ebitda'])}"
        f"      Current ratio: {_v(s['current_ratio'])}   Quick: {_v(s['quick_ratio'])}",
        f"    FCF (TTM)         : {millions(s['free_cash_flow_ttm'])}M",
        "",
        f"  ANNUAL series (newest first, {r['currency'] or '?'} millions)",
        "  " + "-" * 56,
        f"    {'Period':<12}{'ND/EBITDA':>10}{'IntCov':>8}{'SelfFund':>9}{'NetDebt':>10}{'CurDebt':>9}{'LTDebt':>9}",
    ]
    for p in r["periods"]:
        out.append(
            f"    {p['period']:<12}"
            f"{_v(p['net_debt_to_ebitda']):>10}"
            f"{_v(p['interest_coverage_ebit'], 'x'):>8}"
            f"{_v(p['near_term_debt_cover'], 'x'):>9}"
            f"{millions(p['net_debt']):>10}{millions(p['current_debt']):>9}{millions(p['long_term_debt']):>9}"
        )
    out += ["    IntCov = EBIT / net interest.  SelfFund = (cash + 1yr FCF) / current debt, x-covered.",
            "    EBITDA coverage, net-debt/FCF, debt/equity and capital leases are in --format json."]

    sm = r["summary"]
    out += ["", "  THROUGH-CYCLE summary", "  " + "-" * 56]
    if "leverage_peak" in sm:
        lp, ll = sm["leverage_peak"], sm["leverage_latest"]
        out.append(f"    Leverage   latest {ll['net_debt_to_ebitda']} ({ll['period']})   "
                   f"peak {lp['net_debt_to_ebitda']} ({lp['period']})   trend {sm.get('leverage_trend', '—')}")
    if "coverage_weakest" in sm:
        cw, cl = sm["coverage_weakest"], sm["coverage_latest"]
        out.append(f"    Coverage   latest {cl['interest_coverage_ebit']}x ({cl['period']})   "
                   f"weakest {cw['interest_coverage_ebit']}x ({cw['period']})")
    if "near_term_cover_latest" in sm:
        nt = sm["near_term_cover_latest"]
        out.append(f"    Self-fund  latest {nt['near_term_debt_cover']}x ({nt['period']})   "
                   "(a year's maturities vs cash + 1yr FCF)")

    out += ["", "  NOT covered by Yahoo — get from filings:"]
    out += [f"    • {n}" for n in r["not_covered"]]
    out += ["", "  Score against the bands in the conservative-debt trait doc — the band depends",
            "  on the business type and a through-cycle read, which is the agent's call."]
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Gather leverage / coverage / maturity data for the conservative-debt trait.",
        epilog="Example: conservative_debt.py CBA.AX --years 6",
    )
    p.add_argument("ticker", help="ticker symbol, e.g. AAPL, CBA.AX")
    p.add_argument("--years", "-n", type=int, default=5, help="annual periods to pull (default 5)")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    if args.years < 1:
        fail("--years must be at least 1")
    result = gather(args.ticker, args.years)
    print(json.dumps(result, indent=2) if args.format == "json" else render_table(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
