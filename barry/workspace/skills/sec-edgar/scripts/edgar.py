#!/usr/bin/env python3
"""edgar — JSON-emitting SEC EDGAR CLI for deep annual financial history.

Yahoo (via `yfin`) caps its statements at 4 annual periods. This tool exists for
the one job that limit blocks: pulling a company's *long* history — ~15+ years of
revenue, margins, and share count — from the SEC's XBRL company-facts API. Its
first consumer is the TAM-capture valuation, which needs to read a mature "role
model" where it stood a decade ago (the margin-expansion path, the share-count
ramp) to calibrate the subject's assumptions.

Scope (deliberately narrow, mirroring the yfin/traitlib division of labour):
  * EDGAR is US-only. A ticker with no SEC filer errors out plainly — use a
    US-listed role model (most mature software/tech/med-device analogues are).
  * annual (10-K) figures only. Quarterly and balance-sheet concepts are out of
    scope for this first pass; add them when a caller needs them.
  * facts only — it fetches and derives, it never scores. Same fact/judgement
    line the trait scripts hold.

Data source: the SEC `companyfacts` endpoint (one request per company, then every
concept resolved locally), plus the ticker->CIK map. No API key; the SEC only asks
for a descriptive User-Agent with a contact address (see EDGAR_USER_AGENT). Both
downloads are cached under ~/.cache/edgar-cli with a TTL.

Output shape matches yfin's statements — {period_iso: {line_item: value}}, newest
period first — so a caller can treat an edgar pull and a yfin pull identically.

Run via the `edgar` wrapper on PATH (scripts/bin/edgar); stdlib only, no venv.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

# --- configuration -----------------------------------------------------------

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
DEFAULT_UA = "openclaw-stock-analysis (nbuters@gmail.com)"
CACHE_DIR = Path(os.environ.get("EDGAR_CACHE_DIR", Path.home() / ".cache" / "edgar-cli"))
TICKERS_TTL = 30 * 86400   # the ticker->CIK map drifts slowly
FACTS_TTL = 1 * 86400      # company facts change only with new filings
ANNUAL_MIN, ANNUAL_MAX = 340, 380  # a 10-K period is ~a year (52/53-week filers included)

# Canonical line item -> ordered candidate us-gaap tags. XBRL tag choice drifts
# across filers and over time (the same first_present discipline the trait
# scripts use for Yahoo's line-item names): the first candidate that carries data
# wins, and the tag actually used is echoed back under `_tags`.
CONCEPTS: dict[str, tuple[tuple[str, ...], str]] = {
    # name: (candidate tags, unit key)
    "Revenue": (
        ("RevenueFromContractWithCustomerExcludingAssessedTax",
         "Revenues",
         "SalesRevenueNet",
         "RevenueFromContractWithCustomerIncludingAssessedTax"),
        "USD",
    ),
    "Cost Of Revenue": (
        ("CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"),
        "USD",
    ),
    "Gross Profit": (("GrossProfit",), "USD"),
    "Operating Income": (("OperatingIncomeLoss",), "USD"),
    "Net Income": (("NetIncomeLoss", "ProfitLoss"), "USD"),
    "D&A": (
        ("DepreciationDepletionAndAmortization",
         "DepreciationAmortizationAndAccretionNet",
         "DepreciationAndAmortization"),
        "USD",
    ),
    "Diluted Shares": (("WeightedAverageNumberOfDilutedSharesOutstanding",), "shares"),
    "Basic Shares": (("WeightedAverageNumberOfSharesOutstandingBasic",), "shares"),
}
# The curated income series, in presentation order. EBITDA and (a fallback) Gross
# Profit are derived below rather than pulled.
INCOME_ORDER = ["Revenue", "Cost Of Revenue", "Gross Profit", "Operating Income",
                "EBITDA", "Net Income", "D&A", "Diluted Shares", "Basic Shares"]


# --- IO / serialization ------------------------------------------------------

def emit(obj) -> None:
    json.dump(obj, sys.stdout, default=str, indent=2)
    sys.stdout.write("\n")


def fail(msg, code: int = 1):
    json.dump({"error": str(msg)}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.exit(code)


def _user_agent() -> str:
    return os.environ.get("EDGAR_USER_AGENT") or DEFAULT_UA


def _get_json(url: str, cache_name: str | None, ttl: int, refresh: bool):
    """Fetch and parse JSON, with an optional on-disk cache (TTL in seconds)."""
    cache = (CACHE_DIR / cache_name) if cache_name else None
    if cache and not refresh and cache.exists() and (time.time() - cache.stat().st_mtime) < ttl:
        try:
            return json.loads(cache.read_text())
        except (json.JSONDecodeError, OSError):
            pass  # fall through and refetch
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(),
                                               "Accept-Encoding": "gzip, deflate"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                raw = gzip.decompress(raw)
            text = raw.decode("utf-8")
    except urllib.error.HTTPError as e:
        raise LookupError(f"SEC HTTP {e.code} for {url}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise LookupError(f"could not reach SEC ({e})") from e
    data = json.loads(text)
    if cache:
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache.write_text(text)
        except OSError:
            pass  # cache is best-effort
    return data


# --- ticker -> CIK -----------------------------------------------------------

def resolve_cik(ticker: str, refresh: bool) -> tuple[int, str]:
    """Map a ticker to its (CIK, company title), or fail with a US-only hint."""
    t = ticker.strip().upper()
    data = _get_json(TICKERS_URL, "company_tickers.json", TICKERS_TTL, refresh)
    for row in data.values():
        if str(row.get("ticker", "")).upper() == t:
            return int(row["cik_str"]), str(row.get("title", ""))
    fail(f"no SEC filer found for {t!r}. EDGAR covers US-listed filers only — "
         f"pick a US-listed company (e.g. a US role model for TAM-capture).")


def fetch_facts(cik: int, refresh: bool) -> dict:
    try:
        data = _get_json(FACTS_URL.format(cik=cik), f"facts_{cik:010d}.json", FACTS_TTL, refresh)
    except LookupError as e:
        fail(str(e))
    return data.get("facts", {}).get("us-gaap", {})


# --- annual-series extraction ------------------------------------------------

def _annual_series(usgaap: dict, tags: tuple[str, ...], unit: str) -> tuple[dict[str, float], str | None]:
    """{fiscal_year_end_iso: value} for the first candidate tag that carries annual
    10-K data, plus the tag used. One value per fiscal year end, taking the most
    recently filed (restated) figure on collisions."""
    for tag in tags:
        node = usgaap.get(tag)
        if not node:
            continue
        arr = node.get("units", {}).get(unit)
        if not arr:
            continue
        picked: dict[str, tuple[float, str]] = {}
        for f in arr:
            start, end = f.get("start"), f.get("end")
            val, form = f.get("val"), f.get("form", "")
            if start is None or end is None or val is None or not form.startswith("10-K"):
                continue
            try:
                dur = (date.fromisoformat(end) - date.fromisoformat(start)).days
            except ValueError:
                continue
            if not (ANNUAL_MIN <= dur <= ANNUAL_MAX):
                continue
            filed = f.get("filed", "")
            cur = picked.get(end)
            if cur is None or filed > cur[1]:
                picked[end] = (float(val), filed)
        if picked:
            return {k: v[0] for k, v in picked.items()}, tag
    return {}, None


def build_income(usgaap: dict, last: int | None) -> dict:
    """Assemble the curated annual income series across all concepts, aligned on
    fiscal-year-end and newest-first, with EBITDA / a Gross-Profit fallback derived."""
    series: dict[str, dict[str, float]] = {}
    tags_used: dict[str, str | None] = {}
    for name, (tags, unit) in CONCEPTS.items():
        s, tag = _annual_series(usgaap, tags, unit)
        series[name] = s
        tags_used[name] = tag

    periods = sorted({p for s in series.values() for p in s}, reverse=True)
    if last:
        periods = periods[:last]

    rows: dict[str, dict] = {}
    for p in periods:
        rev = series["Revenue"].get(p)
        cor = series["Cost Of Revenue"].get(p)
        gp = series["Gross Profit"].get(p)
        if gp is None and rev is not None and cor is not None:
            gp = rev - cor
        oi = series["Operating Income"].get(p)
        da = series["D&A"].get(p)
        ebitda = oi + da if (oi is not None and da is not None) else None
        rows[p] = {
            "Revenue": rev,
            "Cost Of Revenue": cor,
            "Gross Profit": gp,
            "Operating Income": oi,
            "EBITDA": ebitda,
            "Net Income": series["Net Income"].get(p),
            "D&A": da,
            "Diluted Shares": series["Diluted Shares"].get(p),
            "Basic Shares": series["Basic Shares"].get(p),
        }
    return {"periods": rows, "_tags": {k: v for k, v in tags_used.items() if v}}


# --- derived margins ---------------------------------------------------------

def _div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def build_metrics(usgaap: dict, last: int | None) -> dict:
    """Per-period margins and YoY revenue growth derived from the income series."""
    income = build_income(usgaap, None)["periods"]
    periods = list(income)  # newest-first
    out: dict[str, dict] = {}
    for i, p in enumerate(periods):
        r = income[p]
        rev = r["Revenue"]
        older = income[periods[i + 1]]["Revenue"] if i + 1 < len(periods) else None
        out[p] = {
            "gross_margin": _round(_div(r["Gross Profit"], rev)),
            "operating_margin": _round(_div(r["Operating Income"], rev)),
            "ebitda_margin": _round(_div(r["EBITDA"], rev)),
            "net_margin": _round(_div(r["Net Income"], rev)),
            "revenue_growth": _round(_div(rev - older, older) if (rev is not None and older) else None),
        }
    if last:
        out = {k: out[k] for k in list(out)[:last]}
    return out


def _round(x, n: int = 4):
    return round(x, n) if isinstance(x, (int, float)) else None


# --- field selection ---------------------------------------------------------

def _norm_fields(raw) -> list[str] | None:
    if not raw:
        return None
    if isinstance(raw, (list, tuple)):
        raw = ",".join(raw)
    return [f.strip() for f in raw.split(",") if f.strip()]


def _apply_fields(axis: dict, fields: list[str]) -> dict:
    """Keep only the requested line items within each period (exact, case-insensitive)."""
    out: dict[str, dict] = {}
    unmatched = set(fields)
    for period, rec in axis.items():
        lower = {k.lower(): k for k in rec}
        kept = {}
        for f in fields:
            ck = lower.get(f.lower())
            if ck is not None:
                kept[ck] = rec[ck]
                unmatched.discard(f)
        out[period] = kept
    if unmatched:
        out["_unmatched"] = sorted(unmatched)
    return out


# --- commands ----------------------------------------------------------------

def cmd_income(args) -> dict:
    cik, title = resolve_cik(args.ticker, args.refresh)
    usgaap = fetch_facts(cik, args.refresh)
    built = build_income(usgaap, args.last)
    rows = built["periods"]
    if args.list_fields:
        return {"fields": INCOME_ORDER}
    if args.fields:
        rows = _apply_fields(rows, _norm_fields(args.fields))
    return {"ticker": args.ticker.upper(), "cik": cik, "title": title,
            "unit": "USD (shares in count)", "periods": rows, "_tags": built["_tags"]}


def cmd_metrics(args) -> dict:
    cik, title = resolve_cik(args.ticker, args.refresh)
    usgaap = fetch_facts(cik, args.refresh)
    if args.list_fields:
        return {"fields": ["gross_margin", "operating_margin", "ebitda_margin",
                           "net_margin", "revenue_growth"],
                "definitions": {
                    "gross_margin": "Gross Profit / Revenue",
                    "operating_margin": "Operating Income / Revenue",
                    "ebitda_margin": "(Operating Income + D&A) / Revenue",
                    "net_margin": "Net Income / Revenue",
                    "revenue_growth": "YoY change in Revenue"}}
    metrics = build_metrics(usgaap, args.last)
    if args.fields:
        metrics = _apply_fields(metrics, _norm_fields(args.fields))
    return {"ticker": args.ticker.upper(), "cik": cik, "title": title, "periods": metrics}


def cmd_concept(args) -> dict:
    """Escape hatch: raw annual series for any us-gaap concept, e.g.
    `edgar concept AAPL ResearchAndDevelopmentExpense`."""
    cik, title = resolve_cik(args.ticker, args.refresh)
    usgaap = fetch_facts(cik, args.refresh)
    node = usgaap.get(args.concept)
    if not node:
        fail(f"concept {args.concept!r} not reported by {args.ticker.upper()} "
             f"(us-gaap taxonomy; check the exact tag name).")
    unit = args.unit or next(iter(node.get("units", {})), None)
    series, _tag = _annual_series(usgaap, (args.concept,), unit)
    periods = {k: series[k] for k in sorted(series, reverse=True)}
    if args.last:
        periods = {k: periods[k] for k in list(periods)[:args.last]}
    return {"ticker": args.ticker.upper(), "cik": cik, "title": title,
            "concept": args.concept, "unit": unit, "periods": periods}


def cmd_cik(args) -> dict:
    cik, title = resolve_cik(args.ticker, args.refresh)
    return {"ticker": args.ticker.upper(), "cik": cik,
            "cik_padded": f"CIK{cik:010d}", "title": title}


# --- entry point -------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="edgar",
                                description="JSON SEC EDGAR CLI — deep annual financial history (US filers).")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, fields=True):
        sp.add_argument("ticker", help="US ticker, e.g. ADBE, MSFT, CRM")
        sp.add_argument("--last", "-n", type=int, default=None, help="keep only the N most recent fiscal years")
        sp.add_argument("--refresh", action="store_true", help="bypass the on-disk cache and refetch")
        if fields:
            sp.add_argument("--fields", "-f", nargs="+", default=None, metavar="ITEM",
                            help="line items to keep (exact, case-insensitive; comma/space separated)")
            sp.add_argument("--list-fields", action="store_true", help="list selectable line items and exit")

    inc = sub.add_parser("income", help="curated annual income series (revenue, margins inputs, shares), ~15+ yrs")
    common(inc)
    met = sub.add_parser("metrics", help="per-period margins and YoY revenue growth, derived")
    common(met)
    con = sub.add_parser("concept", help="raw annual series for any us-gaap concept (escape hatch)")
    common(con, fields=False)
    con.add_argument("concept", help="exact us-gaap tag, e.g. ResearchAndDevelopmentExpense")
    con.add_argument("--unit", default=None, help="unit key (default: first reported, usually USD or shares)")
    ck = sub.add_parser("cik", help="resolve a ticker to its SEC CIK")
    ck.add_argument("ticker")
    ck.add_argument("--refresh", action="store_true")
    return p


DISPATCH = {"income": cmd_income, "metrics": cmd_metrics, "concept": cmd_concept, "cik": cmd_cik}


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    try:
        result = DISPATCH[args.cmd](args)
    except SystemExit:
        raise
    except Exception as e:  # surface as JSON, never a traceback
        fail(f"{type(e).__name__}: {e}")
    emit(result)


if __name__ == "__main__":
    main()
