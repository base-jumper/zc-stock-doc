#!/usr/bin/env python3
"""Gather the inputs for the TAM-capture valuation — the data-side companion to
tam_capture_valuation.py.

The valuation method (see references/valuation/tam-capture.md) draws its inputs from
three places:

  * SUBJECT, today (yfin) — price, diluted share count, net debt.
  * MARKET DOC — the subject's 10-year mobility-adjusted annual revenue.
  * ROLE MODEL, current snapshot (yfin) — the mature margin and the EV/EBITDA
    multiple the market pays it, which anchor `margin` and `exit-multiple`.
  * ROLE MODEL, deep history (edgar) — the 15+-year margin-expansion path and
    share-count ramp that calibrates `dilution`. Yahoo caps
    at 4 years, so this comes from SEC EDGAR and needs a US-listed role model.

The market-analysis skill owns the market sizing, concentration, mobility, and
company-revenue estimate. This script only reads that stored output; it never
re-estimates terminal revenue.

Usage:
    tam_capture_inputs.py SUBJECT --market-doc MARKET --role-model ROLE [--years-hist 15]
    tam_capture_inputs.py HIMS --market-doc us-direct-to-consumer-telehealth --role-model TDOC
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from traitlib import edgar, fail, yfin
import tam_capture_valuation as tc


# --- small helpers -----------------------------------------------------------

def _num(x):
    return x if isinstance(x, (int, float)) else None


def _pctf(x, dp: int = 1) -> str:
    return f"{x * 100:.{dp}f}%" if isinstance(x, (int, float)) else "—"


def _human(x) -> str:
    if not isinstance(x, (int, float)):
        return "—"
    for unit, scale in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(x) >= scale:
            return f"{x / scale:,.2f}{unit}"
    return f"{x:,.0f}"


def _soft_edgar(*args):
    """edgar() but degrading to (None, message) instead of exiting — so a non-US
    role model (no SEC filer) still yields the yfin snapshot, just without history."""
    try:
        return edgar(*args), None
    except SystemExit as e:
        # Strip traitlib's "error: " and the echoed "edgar <args>: " so the caller
        # surfaces just the underlying reason.
        msg = str(e)
        if msg.startswith("error: "):
            msg = msg[len("error: "):]
        if msg.startswith("edgar ") and ": " in msg:
            msg = msg.split(": ", 1)[1]
        return None, msg


# --- subject side (yfin) -----------------------------------------------------

def gather_subject(ticker: str) -> dict:
    quote = yfin("quote", ticker)
    info = yfin("info", ticker)
    fin = (info.get("financials") or {}) if isinstance(info, dict) else {}
    ident = (info.get("identity") or {}) if isinstance(info, dict) else {}
    own = (info.get("ownership") or {}) if isinstance(info, dict) else {}

    # Prefer the diluted average from the income statement; fall back to shares out.
    inc = yfin("income", ticker, "-n", "1", "--fields", "Diluted Average Shares,Basic Average Shares")
    latest = next(iter(inc.values()), {}) if isinstance(inc, dict) else {}
    shares = _num(latest.get("Diluted Average Shares")) or _num(latest.get("Basic Average Shares")) \
        or _num(own.get("sharesOutstanding"))

    total_debt, total_cash = _num(fin.get("totalDebt")), _num(fin.get("totalCash"))
    net_debt = (total_debt - total_cash) if (total_debt is not None and total_cash is not None) else None

    return {
        "ticker": ticker.upper(),
        "price": _num(quote.get("price")) if isinstance(quote, dict) else None,
        "market_cap": _num(quote.get("marketCap")) if isinstance(quote, dict) else None,
        "shares": shares,
        "net_debt": net_debt,
        "total_debt": total_debt,
        "total_cash": total_cash,
        "currency": ident.get("financialCurrency") or (quote.get("currency") if isinstance(quote, dict) else None),
    }


# --- role model current snapshot (yfin) --------------------------------------

def gather_role_snapshot(ticker: str) -> dict:
    info = yfin("info", ticker)
    val = (info.get("valuation") or {}) if isinstance(info, dict) else {}
    prof = (info.get("profitability") or {}) if isinstance(info, dict) else {}
    ident = (info.get("identity") or {}) if isinstance(info, dict) else {}
    return {
        "ticker": ticker.upper(),
        "name": ident.get("longName") or ident.get("shortName"),
        "ebitda_margin": _num(prof.get("ebitdaMargins")),
        "operating_margin": _num(prof.get("operatingMargins")),
        "ev_ebitda": _num(val.get("enterpriseToEbitda")),
        "ev_revenue": _num(val.get("enterpriseToRevenue")),
    }


# --- role model deep history (edgar) -----------------------------------------

def gather_role_history(ticker: str, years: int) -> dict:
    """The long annual ramp from EDGAR: margin-expansion path and share-count trend.
    Returns {"error": msg} (non-fatal) when the role model has no SEC filer."""
    inc, err = _soft_edgar("income", ticker, "-n", str(years))
    if err is not None:
        return {"error": err}
    met, _ = _soft_edgar("metrics", ticker, "-n", str(years))
    periods = inc.get("periods", {}) if isinstance(inc, dict) else {}
    mrows = met.get("periods", {}) if isinstance(met, dict) else {}
    order = list(periods)  # newest-first
    if not order:
        return {"error": f"no annual history returned for {ticker.upper()}"}

    newest, oldest = order[0], order[-1]
    span = len(order) - 1
    rev_new = _num(periods[newest].get("Revenue"))
    rev_old = _num(periods[oldest].get("Revenue"))
    sh_new = _num(periods[newest].get("Diluted Shares"))
    sh_old = _num(periods[oldest].get("Diluted Shares"))

    def cagr(new, old):
        if new and old and old > 0 and new > 0 and span > 0:
            return (new / old) ** (1.0 / span) - 1.0
        return None

    rows = []
    for p in order:
        m = mrows.get(p, {})
        rows.append({
            "period": p,
            "revenue": _num(periods[p].get("Revenue")),
            "operating_margin": _num(m.get("operating_margin")),
            "ebitda_margin": _num(m.get("ebitda_margin")),
            "diluted_shares": _num(periods[p].get("Diluted Shares")),
        })
    return {
        "title": inc.get("title"),
        "periods_covered": len(order),
        "span_years": span,
        "first_year": oldest,
        "last_year": newest,
        "revenue_cagr": cagr(rev_new, rev_old),
        "operating_margin_first": rows[-1]["operating_margin"],
        "operating_margin_last": rows[0]["operating_margin"],
        "ebitda_margin_first": rows[-1]["ebitda_margin"],
        "ebitda_margin_last": rows[0]["ebitda_margin"],
        "shares_first": sh_old,
        "shares_last": sh_new,
        "share_cagr": cagr(sh_new, sh_old),
        "rows": rows,
    }


# --- assembling the suggested inputs -----------------------------------------

def choose_margin_and_multiple(snap: dict, hist: dict) -> dict:
    """Pick the margin and multiple to seed the YAML. Prefer yfin's current snapshot;
    if the role model's current EBITDA is depressed/negative, fall back to EDGAR's
    latest mature margin and flag it."""
    warns = []
    margin = snap.get("ebitda_margin")
    if margin is None or margin <= 0:
        alt = hist.get("ebitda_margin_last") if isinstance(hist, dict) else None
        if alt and alt > 0:
            margin, m_src = alt, "edgar latest (yfin EBITDA margin was null/negative)"
            warns.append("role model's current EBITDA margin is null/negative — used EDGAR's latest "
                         "instead; confirm the role model is genuinely mature.")
        else:
            margin, m_src = None, None
            warns.append("no positive EBITDA margin for the role model from yfin or EDGAR — "
                         "is it mature enough to be a role model?")
    else:
        m_src = "yfin current"

    mult = snap.get("ev_ebitda")
    if mult is None or mult <= 0:
        warns.append("role model's current EV/EBITDA is null/negative (needs positive EBITDA) — "
                     "supply exit-multiple from a mature comparable by hand.")
        mult = None
    return {"margin": margin, "margin_source": m_src, "exit_multiple": mult, "warnings": warns}


def build(
    subject: str,
    role: str | None,
    years: int,
    market_doc: str,
    market_player: str | None = None,
    market_dir: Path = tc.DEFAULT_MARKET_DIR,
) -> dict:
    market = tc.load_market_revenue(market_doc, market_player or subject, market_dir)
    subj = gather_subject(subject)
    currency_warnings = []
    if subj.get("currency") and subj["currency"] != market["currency"]:
        currency_warnings.append(
            f"subject financial currency {subj['currency']} differs from market-doc currency "
            f"{market['currency']} — convert price and net debt to the market-doc currency"
        )
    if role is None:
        return {"subject": subj, "market": market, "role_model": None, "history": None, "seed": None,
                "warnings": currency_warnings + ["no --role-model given: only the subject inputs were gathered. "
                             "The role model supplies margin, exit-multiple, and dilution "
                             "calibration — pick a US-listed mature analogue and re-run."]}
    snap = gather_role_snapshot(role)
    hist = gather_role_history(role, years)
    picked = choose_margin_and_multiple(snap, hist)
    return {"subject": subj, "market": market, "role_model": snap, "history": hist, "seed": picked,
            "warnings": currency_warnings + picked["warnings"]}


# --- rendering ---------------------------------------------------------------

def _fmt_margin(m):
    return f"{m * 100:.1f}%" if isinstance(m, (int, float)) else "TODO"


def render_yaml_block(r: dict) -> list[str]:
    subj, market, snap, seed = r["subject"], r["market"], r["role_model"], r["seed"]
    price = subj.get("price")
    shares = subj.get("shares")
    net_debt = subj.get("net_debt")
    out = ["  Paste into the stock-doc front matter, then fill the TODOs and run tam_capture:",
           "  " + "-" * 62,
           "    valuation:",
           "      tam-capture:",
           f"        price: {price if price is not None else 'TODO'}            # subject, today (yfin)",
           f"        shares: {int(shares) if isinstance(shares, (int, float)) else 'TODO'}          # subject diluted, today (yfin)",
           f"        net-debt: {int(net_debt) if isinstance(net_debt, (int, float)) else 'TODO'}        # subject, today (yfin); negative = net cash",
           f"        market-doc: {market['market_id']}",
           f"        market-player: {market['player_ticker'] or market['player_name']}  # 10-year revenue: {market['terminal_revenue_billions']:.6f}bn {market['currency']}"]
    if snap is not None:
        out += [
            f"        role-model: {snap['ticker']}",
            f"        margin: {_fmt_margin(seed['margin'])}            # role-model EBITDA margin ({seed.get('margin_source') or 'n/a'})",
            f"        margin-basis: EBITDA",
            f"        exit-multiple: {round(seed['exit_multiple'], 1) if seed['exit_multiple'] else 'TODO'}       # role-model current EV/EBITDA (yfin)",
            f"        dilution: TODO           # calibrate from role-model share ramp below (stage-aligned)",
        ]
    return out


def render_table(r: dict) -> str:
    subj = r["subject"]
    out = [f"{subj['ticker']}  —  TAM-capture inputs   [{subj.get('currency') or '?'}]",
           "=" * 66, "",
           "  SUBJECT (today, via yfin)",
           "  " + "-" * 44,
           f"    price          : {subj.get('price') if subj.get('price') is not None else '—'}",
           f"    market cap     : {_human(subj.get('market_cap'))}",
           f"    diluted shares : {_human(subj.get('shares'))}",
           f"    net debt       : {_human(subj.get('net_debt'))}   (debt {_human(subj.get('total_debt'))} - cash {_human(subj.get('total_cash'))}; neg = net cash)"]

    market = r["market"]
    out += ["", f"  MARKET DOC — {market['market_id']}", "  " + "-" * 44,
            f"    player          : {market['player_name']} ({market.get('player_ticker') or 'no ticker'})",
            f"    horizon         : {market.get('projection_year') or 'base year + 10'} ({market['years']} years)",
            f"    terminal revenue: {market['terminal_revenue_billions']:.6f}B {market['currency']}  (mobility-adjusted)"]

    snap = r["role_model"]
    if snap is not None:
        out += ["", f"  ROLE MODEL current snapshot — {snap['ticker']} ({snap.get('name') or ''}) (via yfin)",
                "  " + "-" * 44,
                f"    EBITDA margin  : {_pctf(snap.get('ebitda_margin'))}   -> seeds `margin`",
                f"    operating marg : {_pctf(snap.get('operating_margin'))}",
                f"    EV / EBITDA    : {snap.get('ev_ebitda') if snap.get('ev_ebitda') is not None else '—'}   -> seeds `exit-multiple`",
                f"    EV / Revenue   : {snap.get('ev_revenue') if snap.get('ev_revenue') is not None else '—'}"]

        hist = r["history"]
        out += ["", f"  ROLE MODEL deep history (via edgar, SEC XBRL)", "  " + "-" * 44]
        if isinstance(hist, dict) and hist.get("error"):
            out += [f"    unavailable: {hist['error']}",
                    "    -> EDGAR is US-only. For a non-US role model, read the margin-expansion",
                    "       and dilution ramp from its filings / investor decks (Quartr) instead."]
        elif isinstance(hist, dict):
            out += [f"    coverage       : {hist['periods_covered']} yrs  ({hist['first_year']} -> {hist['last_year']})",
                    f"    revenue CAGR   : {_pctf(hist.get('revenue_cagr'))}   ({_human(hist.get('rows',[{}])[-1].get('revenue'))} -> {_human(hist['rows'][0].get('revenue'))})",
                    f"    op margin path : {_pctf(hist.get('operating_margin_first'))} -> {_pctf(hist.get('operating_margin_last'))}  (expansion with scale)",
                    f"    EBITDA margin  : {_pctf(hist.get('ebitda_margin_first'))} -> {_pctf(hist.get('ebitda_margin_last'))}",
                    f"    diluted shares : {_human(hist.get('shares_first'))} -> {_human(hist.get('shares_last'))}  ({_pctf(hist.get('share_cagr'))}/yr; +ve = dilution)",
                    "",
                    "    Per-year ramp (oldest first — read the role model at the subject's STAGE, not today):",
                    f"      {'year':<12}{'revenue':>12}{'op margin':>11}{'EBITDA marg':>12}{'dil.shares':>13}"]
            for row in reversed(hist["rows"]):
                out.append(f"      {row['period']:<12}{_human(row['revenue']):>12}{_pctf(row['operating_margin']):>11}"
                           f"{_pctf(row['ebitda_margin']):>12}{_human(row['diluted_shares']):>13}")

    out += ["", *render_yaml_block(r)]

    out += ["", "  STILL YOURS — judgement inputs:",
            "  " + "-" * 44,
            "    • margin / exit-multiple — keep both on the same profit basis and anchor them",
            "      on the role model.",
            "    • dilution — stage-align the subject with the role model's share-count ramp.",
            "    • currency — price and net debt must use the market doc's currency.",
            "",
            "  The market doc owns terminal revenue. Fill the remaining TODOs, then run tam_capture."]

    warns = r.get("warnings") or []
    if warns:
        out += ["", "  NOTES:"] + [f"    ! {w}" for w in warns]
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Gather TAM-capture inputs from the subject, market doc, and mature role model.")
    p.add_argument("subject", help="the subject ticker being valued (any exchange; yfin symbol)")
    p.add_argument("--market-doc", required=True,
                   help="market id or path containing players.model-estimate revenue")
    p.add_argument("--market-player",
                   help="exact player ticker or name in the market doc (default: subject ticker)")
    p.add_argument("--market-dir", type=Path, default=tc.DEFAULT_MARKET_DIR)
    p.add_argument("--role-model", "-r", default=None,
                   help="the mature role-model ticker — US-listed for deep EDGAR history")
    p.add_argument("--years-hist", type=int, default=15, help="years of role-model history to pull (default 15)")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()
    if args.years_hist < 1:
        fail("--years-hist must be at least 1")
    r = build(args.subject, args.role_model, args.years_hist, args.market_doc,
              args.market_player, args.market_dir)
    print(json.dumps(r, indent=2, default=str) if args.format == "json" else render_table(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
