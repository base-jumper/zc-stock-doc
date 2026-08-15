#!/usr/bin/env python3
"""yfin — JSON-emitting Yahoo Finance CLI for the yahoo-finance skill.

Wraps the `yfinance` library and prints JSON to stdout, shaped for a downstream
agent to parse. One subcommand per data domain; adding a domain is a single
`@command`-decorated function plus its subparser.

Run via the `yfin` wrapper on PATH (see scripts/bin/yfin), which execs this file
with the skill's pinned virtualenv interpreter.
"""
import argparse
import json
import logging
import sys

import yfinance as yf

# yfinance logs delisting/HTTP warnings to stderr; silence them so the agent
# consuming this CLI sees only our JSON (errors are re-emitted via fail()).
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

try:
    import pandas as pd
    _isna = pd.isna
except Exception:  # pandas is a yfinance dependency; this is belt-and-suspenders
    def _isna(v):
        return v is None


# --- serialization helpers ---------------------------------------------------

def _num(v):
    """Coerce a cell to a JSON-friendly scalar (float/None), leaving strings."""
    try:
        if v is None or _isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(v, (int, float)):
        return v
    try:
        return float(v)
    except (TypeError, ValueError):
        return str(v)


def _col_key(col):
    return col.date().isoformat() if hasattr(col, "date") else str(col)


def _statement_to_dict(df):
    """{period_iso: {line_item: value}} from a yfinance statement DataFrame."""
    if df is None or getattr(df, "empty", True):
        return {}
    out = {}
    for col in df.columns:
        out[_col_key(col)] = {str(k): _num(v) for k, v in df[col].items()}
    return out


def _scalar(v):
    """JSON-friendly leaf: dates -> iso string, numbers -> number, else str/None."""
    if v is None:
        return None
    try:
        if _isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if not isinstance(v, str) and hasattr(v, "isoformat"):
        return v.date().isoformat() if hasattr(v, "date") else v.isoformat()
    if isinstance(v, bool):
        return v
    return _num(v)


def _jsonify(v):
    """Recursively coerce dicts/lists/scalars (e.g. the calendar dict) to JSON."""
    if isinstance(v, dict):
        return {str(k): _jsonify(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, set)):
        return [_jsonify(x) for x in v]
    return _scalar(v)


def _series_to_dict(s):
    """{iso_key: value} from a yfinance Series (e.g. dividends, splits)."""
    if s is None or getattr(s, "empty", True):
        return {}
    return {str(_scalar(i)): _scalar(v) for i, v in s.items()}


def _df_records(df):
    """List of {column: value} row dicts; the integer index is dropped."""
    if df is None or getattr(df, "empty", True):
        return []
    return [{str(k): _scalar(v) for k, v in row.items()} for _, row in df.iterrows()]


def _df_records_dated(df, field="date"):
    """List of row dicts with the (datetime) index surfaced as `field`."""
    if df is None or getattr(df, "empty", True):
        return []
    out = []
    for idx, row in df.iterrows():
        rec = {field: _scalar(idx)}
        rec.update({str(k): _scalar(v) for k, v in row.items()})
        out.append(rec)
    return out


def _df_by_index(df):
    """{index_label: {col: val}}, flattened to {index_label: val} if one column."""
    if df is None or getattr(df, "empty", True):
        return {}
    single = len(df.columns) == 1
    col0 = df.columns[0] if single else None
    out = {}
    for idx, row in df.iterrows():
        key = str(_scalar(idx))
        out[key] = _scalar(row[col0]) if single else {str(k): _scalar(v) for k, v in row.items()}
    return out


# --- filtering helpers -------------------------------------------------------

def _split_fields(raw):
    """Normalise a --fields value into a clean list, or None.

    `raw` may be a single comma-separated string or a list of shell tokens
    (argparse nargs='+'), so `--fields "a,b"`, `--fields a,b`, `--fields a, b`,
    and `--fields a b` all resolve identically. Comma is the canonical
    separator; field paths containing spaces must therefore be quoted.
    """
    if not raw:
        return None
    if isinstance(raw, (list, tuple)):
        raw = ",".join(raw)
    return [f.strip() for f in raw.split(",") if f.strip()]


def _ci_exact(canonical, requested):
    """Case-insensitive *exact* match of requested names against canonical names.

    Returns (matched_canonical, unmatched_requested). No substring matching:
    a request resolves only if it equals a canonical name ignoring case.
    """
    lookup = {c.lower(): c for c in canonical}
    matched, unmatched = [], []
    for r in requested:
        c = lookup.get(r.lower())
        (matched if c is not None else unmatched).append(c if c is not None else r)
    return matched, unmatched


def _limit_periods(stmt, last):
    """Keep the N most recent periods (statements are already newest-first)."""
    if not last:
        return stmt
    return {k: stmt[k] for k in list(stmt)[:last]}


# --- field selection (--fields / --list-fields) ------------------------------
# A command's output has one of three shapes; --fields always operates on the
# *record* (never the period/horizon/row axis, which --last/--horizon trim):
#   "record" — the whole output is one record dict (info, quote, calendar, ...)
#   "axis"   — {axis_key: record} (statements, metrics, actions, estimates, ...)
#   "list"   — [record, ...] (history, upgrades, holders, insiders)
# Path grammar within a record: `x` (whole top-level entry), `y.z` (nested z
# under y), `*.z` (z under every nested top-level entry). Exact, case-insensitive.

def _parse_field_patterns(fields):
    """['x', 'y.z', '*.z'] -> [(orig, head, tail)]; tail None means the whole head."""
    pats = []
    for f in fields:
        if "." in f:
            head, tail = (s.strip() for s in f.split(".", 1))
            pats.append((f, head, None if tail == "*" else tail))
        else:
            pats.append((f, f.strip(), None))
    return pats


def _select_from_record(record, patterns, matched):
    """Filter one record by the patterns, adding matched originals to `matched`."""
    if not isinstance(record, dict):
        return record  # scalar record (e.g. a dividends value): nothing to select
    lower = {k.lower(): k for k in record}
    out = {}

    def take_nested(topkey, val, tail, orig):
        if not isinstance(val, dict):
            return
        ck = {k.lower(): k for k in val}.get(tail.lower())
        if ck is not None:
            dst = out.get(topkey)
            if not isinstance(dst, dict):
                dst = out[topkey] = {}
            dst[ck] = val[ck]
            matched.add(orig)

    for orig, head, tail in patterns:
        if head == "*":
            for k, v in record.items():
                if tail is None:
                    out[k] = v
                    matched.add(orig)
                else:
                    take_nested(k, v, tail, orig)
        else:
            ck = lower.get(head.lower())
            if ck is None:
                continue
            if tail is None:
                out[ck] = record[ck]
                matched.add(orig)
            else:
                take_nested(ck, record[ck], tail, orig)
    return out


def _schema_paths(record):
    """Selectable paths for a record: `key` when flat, `key.sub` when nested."""
    paths = []
    if isinstance(record, dict):
        for k, v in record.items():
            if isinstance(v, dict):
                paths.extend(f"{k}.{sk}" for sk in v)
            else:
                paths.append(k)
    return paths


def _representative(data, shape):
    if shape == "axis":
        return next(iter(data.values()), {}) if isinstance(data, dict) else {}
    if shape == "list":
        return data[0] if isinstance(data, list) and data else {}
    return data


def apply_fields(data, raw, shape):
    """Apply a --fields selection to built output of the given shape."""
    patterns = _parse_field_patterns(_split_fields(raw))
    matched = set()
    if shape == "axis":
        result = {k: _select_from_record(v, patterns, matched) for k, v in data.items()}
    elif shape == "list":
        result = [_select_from_record(r, patterns, matched) for r in data]
    else:
        result = _select_from_record(data, patterns, matched)
    unmatched = [orig for orig, _h, _t in patterns if orig not in matched]
    if unmatched and isinstance(result, dict):  # arrays can't carry the marker
        result["_unmatched"] = unmatched
    return result


def select_output(data, args, shape):
    """Standard tail end of a command: honour --list-fields then --fields."""
    if getattr(args, "list_fields", False):
        return {"fields": _schema_paths(_representative(data, shape))}
    raw = getattr(args, "fields", None)
    return apply_fields(data, raw, shape) if raw else data


def _add_fields_arg(p):
    p.add_argument("--fields", "-f", nargs="+", default=None, metavar="FIELD",
                   help="field paths (exact, case-insensitive): x, y.z, *.z. Comma- or "
                        "space-separated; quote any path containing spaces")
    p.add_argument("--list-fields", action="store_true",
                   help="list selectable field paths and exit")


def emit(obj):
    json.dump(obj, sys.stdout, default=str, indent=2)
    sys.stdout.write("\n")


def fail(msg, code=1):
    json.dump({"error": str(msg)}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.exit(code)


# --- command registry --------------------------------------------------------

COMMANDS = {}


def command(name, help_text, add_args=None):
    def deco(fn):
        COMMANDS[name] = {"fn": fn, "help": help_text, "add_args": add_args}
        return fn
    return deco


# --- info (fundamentals / valuation) -----------------------------------------

# Curated, grouped subset of the ~184-key `info` dict. Stable schema: every key
# is emitted (null when Yahoo omits it) so the agent can rely on the shape.
INFO_GROUPS = {
    "identity": ["symbol", "shortName", "longName", "sector", "industry",
                 "country", "currency", "financialCurrency", "quoteType",
                 "exchange", "website"],
    "valuation": ["marketCap", "enterpriseValue", "trailingPE", "forwardPE",
                  "pegRatio", "trailingPegRatio", "priceToBook",
                  "priceToSalesTrailing12Months", "enterpriseToRevenue",
                  "enterpriseToEbitda"],
    "per_share": ["trailingEps", "forwardEps", "epsCurrentYear",
                  "revenuePerShare", "bookValue"],
    "profitability": ["profitMargins", "grossMargins", "operatingMargins",
                      "ebitdaMargins", "returnOnAssets", "returnOnEquity"],
    "growth": ["revenueGrowth", "earningsGrowth", "earningsQuarterlyGrowth"],
    "financials": ["totalRevenue", "grossProfits", "ebitda", "netIncomeToCommon",
                   "totalCash", "totalCashPerShare", "totalDebt", "debtToEquity",
                   "quickRatio", "currentRatio", "freeCashflow",
                   "operatingCashflow"],
    "dividends": ["dividendRate", "dividendYield", "fiveYearAvgDividendYield",
                  "payoutRatio", "exDividendDate"],
    "analyst": ["targetHighPrice", "targetLowPrice", "targetMeanPrice",
                "targetMedianPrice", "recommendationMean", "recommendationKey",
                "numberOfAnalystOpinions"],
    "ownership": ["sharesOutstanding", "floatShares", "heldPercentInsiders",
                  "heldPercentInstitutions", "shortPercentOfFloat",
                  "sharesShort", "shortRatio", "sharesShortPriorMonth"],
    "governance": ["overallRisk", "auditRisk", "boardRisk", "compensationRisk",
                   "shareHolderRightsRisk"],
    "price": ["currentPrice", "previousClose", "open", "dayLow", "dayHigh",
              "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "fiftyDayAverage",
              "twoHundredDayAverage", "52WeekChange", "SandP52WeekChange",
              "beta", "volume", "averageVolume"],
}


@command("info", "fundamentals, valuation, profitability, analyst targets and ownership", _add_fields_arg)
def cmd_info(t, args):
    info = t.info or {}
    grouped = {g: {k: info.get(k) for k in keys} for g, keys in INFO_GROUPS.items()}
    return select_output(grouped, args, "record")


# --- quote (price snapshot) --------------------------------------------------

@command("quote", "current price snapshot (price, change, ranges, market cap)", _add_fields_arg)
def cmd_quote(t, args):
    fast = t.fast_info
    try:
        info = t.info or {}
    except Exception:
        info = {}

    def g(*names):
        for n in names:
            try:
                v = fast.get(n) if hasattr(fast, "get") else getattr(fast, n, None)
            except Exception:
                v = None
            if v is None:
                v = info.get(n)
            if v is not None:
                return v
        return None

    last = g("lastPrice", "currentPrice")
    prev = g("previousClose", "regularMarketPreviousClose")
    change = change_pct = None
    if last is not None and prev:
        change = last - prev
        change_pct = change / prev * 100
    snapshot = {
        "symbol": (args.ticker or "").upper(),
        "currency": g("currency"),
        "price": _num(last),
        "previousClose": _num(prev),
        "change": _num(change),
        "changePercent": _num(change_pct),
        "dayLow": _num(g("dayLow")),
        "dayHigh": _num(g("dayHigh")),
        "fiftyTwoWeekLow": _num(g("yearLow", "fiftyTwoWeekLow")),
        "fiftyTwoWeekHigh": _num(g("yearHigh", "fiftyTwoWeekHigh")),
        "marketCap": _num(g("marketCap")),
    }
    return select_output(snapshot, args, "record")


# --- financial statements ----------------------------------------------------

_STATEMENT_ATTRS = {
    "income": {"annual": "income_stmt", "quarterly": "quarterly_income_stmt", "ttm": "ttm_income_stmt"},
    "balance": {"annual": "balance_sheet", "quarterly": "quarterly_balance_sheet"},
    "cashflow": {"annual": "cashflow", "quarterly": "quarterly_cashflow", "ttm": "ttm_cashflow"},
}


def _add_statement_args(p):
    p.add_argument("--period", "-p", default="annual",
                   choices=["annual", "quarterly", "ttm"],
                   help="annual (default), quarterly, or ttm (trailing twelve months; not available for balance)")
    p.add_argument("--last", "-n", type=int, default=None,
                   help="keep only the N most recent periods")
    _add_fields_arg(p)


def _make_statement_cmd(kind):
    @command(kind, f"{kind} statement (annual/quarterly/ttm) as {{period: {{line_item: value}}}}", _add_statement_args)
    def _cmd(t, args, _kind=kind):
        attrs = _STATEMENT_ATTRS[_kind]
        attr = attrs.get(args.period)
        if attr is None:
            fail(f"period '{args.period}' is not available for {_kind} (try: {', '.join(attrs)})")
        stmt = _limit_periods(_statement_to_dict(getattr(t, attr)), args.last)
        return select_output(stmt, args, "axis")
    return _cmd


for _k in _STATEMENT_ATTRS:
    _make_statement_cmd(_k)


# --- metrics (derived ratios, computed per period) ---------------------------
# These are NOT yfinance fields; they are computed here from the statements with
# one pinned definition each so a downstream agent never does the arithmetic.
# Each metric is (function(inc, bal, cf) -> value, human-readable definition),
# where inc/bal/cf are that period's {line_item: value} dicts (possibly empty).

def _safe_div(a, b):
    if a is None or b is None or b == 0:
        return None
    try:
        return a / b
    except (TypeError, ZeroDivisionError):
        return None


def _effective_tax_rate(inc):
    rate = inc.get("Tax Rate For Calcs")
    if rate is not None:
        return rate
    return _safe_div(inc.get("Tax Provision"), inc.get("Pretax Income"))


def _nopat(inc):
    ebit, rate = inc.get("EBIT"), _effective_tax_rate(inc)
    if ebit is None or rate is None:
        return None
    return ebit * (1 - rate)


def _invested_capital(bal):
    ic = bal.get("Invested Capital")
    if ic is not None:
        return ic
    debt, equity = bal.get("Total Debt"), bal.get("Common Stock Equity")
    if debt is None or equity is None:
        return None
    return debt + equity


METRICS = {
    "roic": (lambda inc, bal, cf: _safe_div(_nopat(inc), _invested_capital(bal)),
             "NOPAT / Invested Capital; NOPAT = EBIT x (1 - effective tax rate)"),
    "roce": (lambda inc, bal, cf: _safe_div(inc.get("EBIT"),
                _safe_div_sub(bal.get("Total Assets"), bal.get("Current Liabilities"))),
             "EBIT / (Total Assets - Current Liabilities)"),
    "roe": (lambda inc, bal, cf: _safe_div(inc.get("Net Income"), bal.get("Stockholders Equity")),
            "Net Income / Stockholders Equity"),
    "roa": (lambda inc, bal, cf: _safe_div(inc.get("Net Income"), bal.get("Total Assets")),
            "Net Income / Total Assets"),
    "gross_margin": (lambda inc, bal, cf: _safe_div(inc.get("Gross Profit"), inc.get("Total Revenue")),
                     "Gross Profit / Total Revenue"),
    "operating_margin": (lambda inc, bal, cf: _safe_div(inc.get("Operating Income"), inc.get("Total Revenue")),
                         "Operating Income / Total Revenue"),
    "net_margin": (lambda inc, bal, cf: _safe_div(inc.get("Net Income"), inc.get("Total Revenue")),
                   "Net Income / Total Revenue"),
    "fcf_margin": (lambda inc, bal, cf: _safe_div(cf.get("Free Cash Flow"), inc.get("Total Revenue")),
                   "Free Cash Flow / Total Revenue"),
    "fcf": (lambda inc, bal, cf: cf.get("Free Cash Flow"),
            "Free Cash Flow (cash flow statement)"),
    "debt_to_equity": (lambda inc, bal, cf: _safe_div(bal.get("Total Debt"), bal.get("Stockholders Equity")),
                       "Total Debt / Stockholders Equity"),
}


def _safe_div_sub(a, b):
    """Helper: a - b, or None if either is missing (used as a denominator)."""
    if a is None or b is None:
        return None
    return a - b


def _add_metrics_args(p):
    p.add_argument("--period", "-p", default="annual", choices=["annual", "quarterly"],
                   help="annual (default) or quarterly")
    p.add_argument("--last", "-n", type=int, default=None,
                   help="keep only the N most recent periods (e.g. -n 5 for 5 years)")
    _add_fields_arg(p)


@command("metrics", "derived per-period ratios (roic, roce, margins, ...) computed from the statements", _add_metrics_args)
def cmd_metrics(t, args):
    if args.list_fields:
        return {"metrics": {name: defn for name, (_fn, defn) in METRICS.items()}}

    q = args.period == "quarterly"
    inc = _statement_to_dict(t.quarterly_income_stmt if q else t.income_stmt)
    bal = _statement_to_dict(t.quarterly_balance_sheet if q else t.balance_sheet)
    cf = _statement_to_dict(t.quarterly_cashflow if q else t.cashflow)

    # Align on periods present in both income and balance (newest-first), cap to N.
    periods = [p for p in inc if p in bal]
    if args.last:
        periods = periods[:args.last]

    out = {}
    for p in periods:
        i, b, c = inc.get(p, {}), bal.get(p, {}), cf.get(p, {})
        out[p] = {name: _num(METRICS[name][0](i, b, c)) for name in METRICS}
    return apply_fields(out, args.fields, "axis") if args.fields else out


# --- corporate actions -------------------------------------------------------

def _add_last_arg(p, help_text="keep only the N most recent entries"):
    p.add_argument("--last", "-n", type=int, default=None, help=help_text)


@command("dividends", "dividend history as {date: amount}", _add_last_arg)
def cmd_dividends(t, args):
    s = t.dividends
    if args.last and s is not None and not s.empty:
        s = s.tail(args.last)
    return _series_to_dict(s)


@command("splits", "stock-split history as {date: ratio}", _add_last_arg)
def cmd_splits(t, args):
    s = t.splits
    if args.last and s is not None and not s.empty:
        s = s.tail(args.last)
    return _series_to_dict(s)


def _add_last_and_fields(p):
    _add_last_arg(p)
    _add_fields_arg(p)


@command("actions", "dividends and splits as {date: {Dividends, Stock Splits}}", _add_last_and_fields)
def cmd_actions(t, args):
    df = t.actions
    if args.last and df is not None and not df.empty:
        df = df.tail(args.last)
    return select_output(_df_by_index(df), args, "axis")


@command("calendar", "upcoming earnings/dividend dates and consensus ranges", _add_fields_arg)
def cmd_calendar(t, args):
    return select_output(_jsonify(t.calendar or {}), args, "record")


@command("sustain", "ESG / sustainability scores as {metric: value}", _add_fields_arg)
def cmd_sustain(t, args):
    return select_output(_df_by_index(t.sustainability), args, "record")


# --- holders & ownership -----------------------------------------------------

def _records(df, last):
    """A list of row dicts, optionally capped to the first N rows."""
    if last and df is not None and not getattr(df, "empty", True):
        df = df.head(last)
    return _df_records(df)


@command("ownership", "ownership summary: insider/institution percentages as {metric: value}", _add_fields_arg)
def cmd_ownership(t, args):
    return select_output(_df_by_index(t.major_holders), args, "record")


@command("holders", "institutional and mutual-fund holders combined, each row tagged with Type",
         _add_last_and_fields)
def cmd_holders(t, args):
    rows = []
    for label, attr in (("institutional", "institutional_holders"), ("mutual fund", "mutualfund_holders")):
        rows.extend({"Type": label, **rec} for rec in _records(getattr(t, attr), args.last))
    return select_output(rows, args, "list")


@command("insider-roster", "insider roster (current insider holdings) as a list of rows", _add_last_and_fields)
def cmd_insider_roster(t, args):
    return select_output(_records(t.insider_roster_holders, args.last), args, "list")


@command("insider-transactions", "insider buy/sell transactions as a list of rows", _add_last_and_fields)
def cmd_insider_transactions(t, args):
    return select_output(_records(t.insider_transactions, args.last), args, "list")


# --- analyst views -----------------------------------------------------------

@command("recommendations", "analyst buy/hold/sell counts as {period: {strongBuy, buy, hold, sell, strongSell}}",
         _add_fields_arg)
def cmd_recommendations(t, args):
    df = t.recommendations
    out = {}
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            d = {str(k): _scalar(v) for k, v in row.items()}
            out[str(d.pop("period", len(out)))] = d
    return select_output(out, args, "axis")


@command("upgrades", "recent analyst upgrades/downgrades (newest first)", _add_last_and_fields)
def cmd_upgrades(t, args):
    df = t.upgrades_downgrades
    if df is not None and not df.empty:
        df = df.sort_index(ascending=False)
        if args.last:
            df = df.head(args.last)
    return select_output(_df_records_dated(df, field="date"), args, "list")


_ESTIMATE_TABLES = {
    "earnings": "earnings_estimate",
    "revenue": "revenue_estimate",
    "eps_trend": "eps_trend",
    "growth": "growth_estimates",
}


def _add_estimates_args(p):
    _add_fields_arg(p)
    p.add_argument("--horizon", "-H", default=None,
                   help="comma-separated horizons (exact): 0q, +1q, 0y, +1y, LTG; default all")


@command("estimates", "forward analyst estimates (earnings, revenue, eps_trend, growth) by horizon", _add_estimates_args)
def cmd_estimates(t, args):
    if args.list_fields:
        return {"tables": list(_ESTIMATE_TABLES),
                "horizons": "0q=current qtr, +1q=next qtr, 0y=current yr, +1y=next yr, LTG=long-term"}
    # Fetch only the tables referenced by --fields heads (each is an HTTP call).
    raw = args.fields
    if raw:
        heads = {h.lower() for _o, h, _t in _parse_field_patterns(_split_fields(raw))}
        fetch = list(_ESTIMATE_TABLES) if "*" in heads else [n for n in _ESTIMATE_TABLES if n in heads]
    else:
        fetch = list(_ESTIMATE_TABLES)
    # Horizon is the axis shared by every table, so pivot it to the top level:
    # {horizon: {table: {field: value}}}. Tables that lack a horizon (only
    # `growth` has LTG) simply don't appear under it.
    out = {}
    for name in fetch:
        for horizon, fields in _df_by_index(getattr(t, _ESTIMATE_TABLES[name])).items():
            out.setdefault(horizon, {})[name] = fields
    # --horizon trims the (outer) axis; the shape stays {horizon: {table: ...}}.
    wanted = _split_fields(args.horizon)
    h_unmatched = []
    if wanted:
        keep, h_unmatched = _ci_exact(out, wanted)
        out = {h: out[h] for h in keep}
    # --fields then selects within each horizon record (table / table.field / *.field).
    result = apply_fields(out, raw, "axis") if raw else out
    if h_unmatched and isinstance(result, dict):
        result["_unmatched"] = result.get("_unmatched", []) + h_unmatched
    return result


# --- history -----------------------------------------------------------------

def _add_history_args(p):
    p.add_argument("--period", "-p", default="1mo", help="e.g. 1d,5d,1mo,1y,max (default 1mo)")
    p.add_argument("--interval", "-i", default="1d", help="e.g. 1m,1h,1d,1wk,1mo (default 1d)")
    p.add_argument("--start", "-s", default=None, help="YYYY-MM-DD")
    p.add_argument("--end", "-e", default=None, help="YYYY-MM-DD")
    _add_fields_arg(p)


@command("history", "OHLCV history as a list of records", _add_history_args)
def cmd_history(t, args):
    df = t.history(period=args.period, interval=args.interval,
                   start=args.start, end=args.end, auto_adjust=True)
    if df is None or df.empty:
        return select_output([], args, "list")
    df = df.reset_index()
    records = []
    for _, row in df.iterrows():
        rec = {}
        for k, v in row.items():
            k = str(k)
            if k.lower() in ("date", "datetime"):
                rec["date"] = v.isoformat() if hasattr(v, "isoformat") else str(v)
            else:
                rec[k] = _num(v)
        records.append(rec)
    return select_output(records, args, "list")


# --- entry point -------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(prog="yfin", description="JSON Yahoo Finance CLI (yfinance wrapper)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name, spec in COMMANDS.items():
        p = sub.add_parser(name, help=spec["help"])
        p.add_argument("ticker", help="ticker symbol, e.g. AAPL, CBA.AX, BTC-USD")
        if spec["add_args"]:
            spec["add_args"](p)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        t = yf.Ticker(args.ticker)
        result = COMMANDS[args.cmd]["fn"](t, args)
    except SystemExit:
        raise
    except Exception as e:  # surface as JSON rather than a traceback
        fail(f"{type(e).__name__}: {e}")
    emit(result)


if __name__ == "__main__":
    main()
