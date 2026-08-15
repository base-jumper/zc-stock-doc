#!/usr/bin/env python3
"""Estimate the "it works" annualized ROI of an early-stage, growth-first
company from a market-analysis terminal-revenue estimate.

Unlike the exit-multiple method, this model does not anchor on today's per-share
fundamental. It reads the company's 10-year terminal annual revenue from a
market-doc at `players.model-estimate[].mobility-adjusted-revenue`, then builds
terminal value:

  1. A mature profit margin converts revenue to a terminal profit figure, and an
     exit multiple converts that to terminal ENTERPRISE value:

         terminal_ev = terminal_revenue * margin * exit_multiple

     `margin` and `exit_multiple` must reference the SAME profit line (see
     `margin-basis`): an EV/EBITDA multiple needs an EBITDA margin, an EV/EBIT
     multiple needs an operating (EBIT) margin. Pulling both from one real
     "role model" company (see below) keeps them consistent by construction.

  2. A net-debt bridge takes enterprise value to EQUITY value; a company funded by
     share issuance rather than debt plausibly ends near net-cash, so `net-debt`
     defaults to 0 (set it negative for net cash):

         terminal_equity = terminal_ev - net_debt

  3. Share issuance over the 10-year hold dilutes the per-share claim. Dilution compounds
     each year off today's diluted share count:

         shares_N = shares_0 * prod_{i<=N}(1 + d_i)
         terminal_price = terminal_equity / shares_N

  4. With no dividends to model (early-stage companies don't pay), the return is a
     pure price CAGR off today's price:

         annualized_roi = (terminal_price / price) ^ (1/years) - 1

The result is decomposed into the two sources of return, which compose exactly:

    value creation  — (terminal_equity / today's market cap) ^ (1/N) - 1
    dilution        — (1 / prod(1 + d_i)) ^ (1/N) - 1            (a drag, negative)

i.e. the business growing into a mature, fully-valued company, less the share-count
leakage on the way. Their product is the total annualized ROI.

============================================================================
The role model
============================================================================

The market-analysis model owns terminal market share and revenue. The remaining
`margin` and `exit-multiple` assumptions should be anchored on one mature "role
model" in a similar industry. Its history also calibrates dilution. Recording the
role-model ticker in `role-model` keeps those assumptions traceable.

NOTE: the role model is, by definition, a survivor. This method therefore estimates
the "it works" case, not a probability-weighted expectation — treat its ROI as the
base/bull case and pair it with the odds of getting there.

============================================================================
Two ways to run it
============================================================================

This is the valuation counterpart of company_score.py and shares its interface.

  * STOCK-DOC mode (the integrated flow). Pass a stock-doc; the script reads the
    tam-capture inputs from its front matter and writes the annualized ROI back:

        tam_capture_valuation.py --stock-doc NET

    It reads `valuation.tam-capture` from the front matter and writes the annualized
    ROI back as a `roi` child of that same block (surgical — only that line is
    touched), alongside the run's as-of `date`. Hand-tweak an input and re-run to
    refresh both — nothing else is touched.

    Stock-doc front matter (example):

        ---
        ticker: NET
        valuation:
          tam-capture:
            price: 18.40           # entry price per share (today) — the ROI denominator
            shares: 340e6          # today's diluted share count
            market-doc: cloud-security-platforms
            market-player: NET     # optional; defaults to the stock-doc ticker
            margin: 28%            # mature profit margin (role model)
            margin-basis: EBITDA   # EBITDA or EBIT — must match the exit multiple
            exit-multiple: 16      # EV/EBITDA (or EV/EBIT) at maturity (role model)
            dilution: 4%           # yearly share issuance (scalar or per-year list)
            net-debt: 0            # terminal net debt (subtracted from EV); negative = net cash
            role-model: ZS         # source of margin, multiple, and dilution calibration
            roi: 0.0               # written by this script
            date: 2026-06-23       # written by this script (valuation as-of date)
        ---

  * RAW mode (ad-hoc sanity check, no doc). Pass the inputs as flags:

        tam_capture_valuation.py --ticker NET --market-doc cloud-security-platforms \
            --price 18.40 --shares 340e6 --margin 28% --exit-multiple 16 \
            --dilution 4% --role-model ZS

Rates accept a trailing '%' ("9%" == 0.09) or a plain decimal (0.09). --dilution
takes either one value (applied to every year) or a per-year list (a comma-separated
string on the CLI, or a YAML list in front matter) of length 10 — useful to
front-load issuance during the cash-burn years and taper it later.

Requires PyYAML for stock-doc mode. No secrets, no network.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

METHOD = "tam-capture"  # front-matter block key, output prefix, and method id
WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"
DEFAULT_MARKET_DIR = WORKSPACE / "investment" / "market-docs"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"error: {msg}")


# --------------------------------------------------------------------------- #
# Parsing                                                                      #
# --------------------------------------------------------------------------- #
def parse_rate(s: Any, label: str) -> float:
    """Parse a rate: '9%' -> 0.09, '0.09' -> 0.09, 0.09 -> 0.09."""
    s = str(s).strip()
    try:
        return float(s[:-1]) / 100.0 if s.endswith("%") else float(s)
    except ValueError:
        fail(f"{label}: could not parse {s!r} as a rate (use e.g. 0.09 or 9%)")


def parse_rate_series(value: Any, years: int, label: str) -> list[float]:
    """Parse a scalar (broadcast to `years`) or a length-`years` series of rates.

    Accepts a YAML list ([0.06, 0.04]), a comma string ("0.06,0.04"), or a scalar.
    Every resulting factor (1 + rate) must be positive."""
    if isinstance(value, (list, tuple)):
        rates = [parse_rate(v, label) for v in value]
    else:
        parts = [p for p in str(value).split(",") if p.strip() != ""]
        rates = [parse_rate(p, label) for p in parts]
    if not rates:
        fail(f"{label}: no value provided")
    if len(rates) == 1:
        rates = rates * years
    if len(rates) != years:
        fail(f"{label}: expected 1 value or {years} values, got {len(rates)}")
    for r in rates:
        if 1.0 + r <= 0.0:
            fail(f"{label}: rate {r} implies a non-positive (1+rate) factor")
    return rates


def require_float(value: Any, label: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        fail(f"{label}: expected a number, got {value!r}")


def require_int(value: Any, label: str) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        fail(f"{label}: expected a whole number, got {value!r}")
    if n < 1:
        fail(f"{label}: must be at least 1")
    return n


def parse_basis(value: Any, source: str) -> str:
    """The profit line `margin` and `exit-multiple` both reference. Inert in the
    maths (profit = revenue * margin either way); recorded to keep the two
    consistent. Defaults to EBITDA, the usual mature multiple."""
    if value in (None, ""):
        return "EBITDA"
    basis = str(value).strip().upper().replace("_", "").replace("-", "")
    aliases = {"EBITDA": "EBITDA", "EBIT": "EBIT", "OPERATING": "EBIT", "OP": "EBIT"}
    if basis not in aliases:
        fail(f"{source}: margin-basis must be EBITDA or EBIT, got {value!r}")
    return aliases[basis]


# --------------------------------------------------------------------------- #
# The model                                                                    #
# --------------------------------------------------------------------------- #
def compute(
    price: float,
    shares: float,
    years: int,
    terminal_revenue: float,
    margin: float,
    exit_multiple: float,
    dilution: list[float],
    net_debt: float = 0.0,
    margin_basis: str = "EBITDA",
    role_model: str | None = None,
) -> dict[str, Any]:
    if price <= 0:
        fail("price must be positive (it is the ROI denominator)")
    if shares <= 0:
        fail("shares must be positive")
    if terminal_revenue <= 0:
        fail("terminal-revenue must be positive")
    if margin <= 0:
        fail("margin must be positive (a profitable mature business)")
    if exit_multiple <= 0:
        fail("exit-multiple must be positive")

    # 1-2: terminal whole-company value from market-analysis revenue.
    terminal_profit = terminal_revenue * margin
    terminal_ev = terminal_profit * exit_multiple
    terminal_equity = terminal_ev - net_debt
    if terminal_equity <= 0:
        fail("terminal equity is non-positive (net-debt exceeds enterprise value)")

    # 3: dilute today's share count over the hold; per-share exit price.
    d_cum = 1.0
    for d in dilution:
        d_cum *= 1.0 + d
    shares_exit = shares * d_cum
    terminal_price = terminal_equity / shares_exit

    # 4: pure price CAGR — no dividends for an early-stage company.
    n = float(years)
    total_return = (terminal_price / price) ** (1.0 / n) - 1.0

    # Attribution. value_creation and dilution compose EXACTLY to the total:
    #   (terminal_equity/mktcap0)^(1/N) * (1/d_cum)^(1/N) = (terminal_price/price)^(1/N)
    market_cap_now = price * shares
    value_creation_cagr = (terminal_equity / market_cap_now) ** (1.0 / n) - 1.0
    dilution_cagr = (1.0 / d_cum) ** (1.0 / n) - 1.0

    return {
        "annualized_roi": round(total_return, 6),
        "return_multiple": round(terminal_price / price, 4),
        "holding_years": years,
        "entry_price": round(price, 4),
        "terminal_price": round(terminal_price, 4),
        "shares_now": shares,
        "shares_exit": round(shares_exit, 2),
        "total_dilution": round(d_cum - 1.0, 6),
        "market_cap_now": round(market_cap_now, 2),
        "terminal_revenue": round(terminal_revenue, 2),
        "terminal_profit": round(terminal_profit, 2),
        "margin_basis": margin_basis,
        "terminal_ev": round(terminal_ev, 2),
        "net_debt": round(net_debt, 2),
        "terminal_equity": round(terminal_equity, 2),
        "value_creation_multiple": round(terminal_equity / market_cap_now, 4),
        "exit_multiple": round(exit_multiple, 4),
        "role_model": role_model,
        "attribution": {
            "value_creation": round(value_creation_cagr, 6),
            "dilution": round(dilution_cagr, 6),
        },
    }


def resolve_inputs(raw: dict[str, Any], *, source: str) -> dict[str, Any]:
    """Turn a flat dict of raw inputs into validated arguments for compute()."""
    for req in ("price", "shares", "years", "terminal-revenue", "margin", "exit-multiple"):
        if raw.get(req) in (None, ""):
            fail(f"{source}: missing required input {req!r}")

    years = require_int(raw["years"], "years")
    role_model = raw.get("role-model")
    role_model = str(role_model).strip() if role_model not in (None, "") else None
    return dict(
        price=require_float(raw["price"], "price"),
        shares=require_float(raw["shares"], "shares"),
        years=years,
        terminal_revenue=require_float(raw["terminal-revenue"], "terminal-revenue"),
        margin=parse_rate(raw["margin"], "margin"),
        exit_multiple=require_float(raw["exit-multiple"], "exit-multiple"),
        dilution=parse_rate_series(raw.get("dilution", 0), years, "dilution"),
        net_debt=require_float(raw.get("net-debt", 0) or 0, "net-debt"),
        margin_basis=parse_basis(raw.get("margin-basis"), source),
        role_model=role_model,
    )


def resolve_market_doc(arg: str, market_dir: Path) -> Path:
    """Resolve a market id or explicit Markdown path."""
    p = Path(arg)
    if p.suffix == ".md" or "/" in arg:
        return p
    return market_dir / f"{arg.strip()}.md"


def _selector(value: Any) -> str:
    return "" if value is None else str(value).strip().casefold().lstrip("$")


def load_market_revenue(
    market_doc: str,
    player: str,
    market_dir: Path = DEFAULT_MARKET_DIR,
) -> dict[str, Any]:
    """Read one player's canonical 10-year annual revenue.

    Market-doc revenue is stored in billions of the top-level currency. Return
    the whole-currency-unit value used by the valuation arithmetic. A matching
    analyst override is canonical and replaces the mobility model estimate; its
    revenue is capture multiplied by the market's maturity value.
    """
    path = resolve_market_doc(market_doc, market_dir)
    if not path.exists():
        fail(
            f"market-doc not found: {path}. Generate it with the market-analysis "
            "skill before running TAM-capture."
        )
    _, fm = split_front_matter(path.read_text(encoding="utf-8"), source=f"market-doc {path}")

    years = require_int(fm.get("maturity-duration"), "market-doc maturity-duration")
    if years != 10:
        fail(f"market-doc {path}: maturity-duration must be 10, got {years}")
    currency = fm.get("currency")
    if not isinstance(currency, str) or not currency.strip():
        fail(f"market-doc {path}: missing non-empty top-level currency")

    players = fm.get("players")
    overrides = players.get("override") if isinstance(players, dict) else None
    estimates = players.get("model-estimate") if isinstance(players, dict) else None

    wanted = _selector(player)
    override_matches = []
    if overrides is not None:
        if not isinstance(overrides, list):
            fail(f"market-doc {path}: players.override must be a list")
        for index, entry in enumerate(overrides, start=1):
            if not isinstance(entry, dict):
                fail(f"market-doc {path}: players.override[{index}] must be a mapping")
            name, ticker = entry.get("name"), entry.get("ticker")
            if wanted in {_selector(ticker), _selector(name)}:
                override_matches.append(entry)
    if len(override_matches) > 1:
        fail(f"market-doc {path}: player selector {player!r} is ambiguous in players.override")

    if override_matches:
        entry = override_matches[0]
        capture = require_float(entry.get("capture"), "players.override.capture")
        if capture <= 0:
            fail(f"market-doc {path}: players.override.capture must be positive")
        size = fm.get("size")
        maturity_value = require_float(
            size.get("maturity-market-value") if isinstance(size, dict) else None,
            "size.maturity-market-value",
        )
        if maturity_value <= 0:
            fail(f"market-doc {path}: size.maturity-market-value must be positive")
        revenue_bn = capture * maturity_value
        base_year = fm.get("base-year")
        projection_year = base_year + years if isinstance(base_year, int) else None
        return {
            "path": path,
            "market_id": path.stem,
            "player_name": entry.get("name"),
            "player_ticker": entry.get("ticker"),
            "terminal_revenue": revenue_bn * 1e9,
            "terminal_revenue_billions": revenue_bn,
            "currency": currency.strip(),
            "years": years,
            "base_year": base_year,
            "projection_year": projection_year,
            "source": "override",
        }

    if not isinstance(estimates, list) or not estimates:
        fail(f"market-doc {path}: missing players.model-estimate and no matching player override")

    matches = []
    available = []
    for index, entry in enumerate(estimates, start=1):
        if not isinstance(entry, dict):
            fail(f"market-doc {path}: players.model-estimate[{index}] must be a mapping")
        name, ticker = entry.get("name"), entry.get("ticker")
        available.append(str(ticker or name or f"entry {index}"))
        if wanted in {_selector(ticker), _selector(name)}:
            matches.append(entry)

    if not matches:
        fail(
            f"market-doc {path}: no players.model-estimate entry matches {player!r}; "
            f"available players: {', '.join(available)}"
        )
    if len(matches) > 1:
        fail(f"market-doc {path}: player selector {player!r} is ambiguous")

    entry = matches[0]
    revenue_bn = require_float(
        entry.get("mobility-adjusted-revenue"),
        "players.model-estimate.mobility-adjusted-revenue",
    )
    if revenue_bn <= 0:
        fail(
            f"market-doc {path}: players.model-estimate.mobility-adjusted-revenue "
            "must be positive"
        )
    base_year = fm.get("base-year")
    projection_year = base_year + years if isinstance(base_year, int) else None
    return {
        "path": path,
        "market_id": path.stem,
        "player_name": entry.get("name"),
        "player_ticker": entry.get("ticker"),
        "terminal_revenue": revenue_bn * 1e9,
        "terminal_revenue_billions": revenue_bn,
        "currency": currency.strip(),
        "years": years,
        "base_year": base_year,
        "projection_year": projection_year,
        "source": "model-estimate",
    }


# --------------------------------------------------------------------------- #
# Front matter (stock-doc mode)                                                #
# --------------------------------------------------------------------------- #
def split_front_matter(
    text: str, *, source: str = "stock-doc"
) -> tuple[str, dict[str, Any]]:
    import yaml

    m = FM_RE.match(text)
    if not m:
        fail(f"{source} has no YAML front matter (must start with a '---' block).")
    block = m.group(1)
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as e:
        fail(f"could not parse {source} front matter as YAML: {e}")
    if not isinstance(data, dict):
        fail(f"{source} front matter must be a YAML mapping.")
    return block, data


def resolve_stock_doc(arg: str, stock_dir: Path) -> Path:
    p = Path(arg)
    if p.suffix == ".md" or "/" in arg:
        return p
    return stock_dir / f"{arg.strip().lstrip('$').upper()}.md"


def upsert_valuation_child(
    block: str, method: str, key: str, value: str, after_key: str | None = None
) -> str:
    """Surgically set `<key>: <value>` inside the `valuation.<method>` mapping.

    Updates the child in place if present. When absent, it is inserted just after
    the `after_key` child (if given and found), otherwise appended as the last child
    of the method block. Everything else in the front matter is preserved."""
    def indent_of(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    lines = block.splitlines()

    val_i = next((i for i, l in enumerate(lines)
                  if re.match(r"[ ]*valuation:[ ]*$", l)), None)
    if val_i is None:
        fail("cannot write back: front matter has no 'valuation:' block.")
    val_indent = indent_of(lines[val_i])

    method_i = None
    for i in range(val_i + 1, len(lines)):
        if not lines[i].strip():
            continue
        if indent_of(lines[i]) <= val_indent:
            break  # left the valuation block
        if re.match(rf"[ ]*{re.escape(method)}:[ ]*$", lines[i]):
            method_i = i
            break
    if method_i is None:
        fail(f"cannot write back: front matter has no 'valuation.{method}' block.")
    method_indent = indent_of(lines[method_i])

    child_indent = None
    key_i = None
    after_i = None
    end_i = len(lines)
    for i in range(method_i + 1, len(lines)):
        if not lines[i].strip():
            continue
        ind = indent_of(lines[i])
        if ind <= method_indent:
            end_i = i
            break
        if child_indent is None:
            child_indent = ind
        if re.match(rf"[ ]*{re.escape(key)}:", lines[i]):
            key_i = i
        if after_key is not None and re.match(rf"[ ]*{re.escape(after_key)}:", lines[i]):
            after_i = i
    if child_indent is None:
        child_indent = method_indent + 2

    new_line = f"{' ' * child_indent}{key}: {value}"
    if key_i is not None:
        lines[key_i] = new_line
    elif after_i is not None:
        lines.insert(after_i + 1, new_line)
    else:
        insert_at = end_i
        while insert_at > method_i + 1 and not lines[insert_at - 1].strip():
            insert_at -= 1
        lines.insert(insert_at, new_line)
    return "\n".join(lines)


def write_outputs(path: Path, roi: float, as_of: str) -> None:
    """Stamp the computed `roi` and valuation `date` into the method block."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        fail(f"cannot write back: {path} has no front-matter block.")
    block = upsert_valuation_child(m.group(1), METHOD, "roi", str(round(roi, 6)))
    block = upsert_valuation_child(block, METHOD, "date", as_of)
    path.write_text(f"---\n{block}\n---\n" + text[m.end():], encoding="utf-8")


def resolve_as_of(arg: str | None) -> str:
    """Today's ISO date, or a validated --as-of override."""
    if not arg:
        return date.today().isoformat()
    try:
        return date.fromisoformat(arg).isoformat()
    except ValueError:
        fail(f"--as-of: expected an ISO date (YYYY-MM-DD), got {arg!r}")


# --------------------------------------------------------------------------- #
# Output                                                                       #
# --------------------------------------------------------------------------- #
def pct(x: float) -> str:
    return f"{x * 100:+.2f}%"


def human(x: float) -> str:
    """Compact magnitude for the big terminal figures (revenue, EV, market cap)."""
    for unit, scale in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(x) >= scale:
            return f"{x / scale:,.2f}{unit}"
    return f"{x:,.2f}"


def render_table(r: dict[str, Any], doc_path: Path | None, wrote: bool, as_of: str) -> str:
    a = r["attribution"]
    head = doc_path.stem if doc_path else "tam-capture valuation"
    out = [
        f"{head}  —  'it works' ROI over {r['holding_years']}y (TAM-capture, terminal-anchored)  as of {as_of}",
        "=" * 64,
    ]
    if r.get("role_model"):
        out.append(f"  role model: {r['role_model']}")
    out += [
        "",
        f"  Revenue source       : {r['market_doc']} -> {r['market_player']} "
        f"({r['market_currency']}, {r.get('projection_year') or '10-year horizon'})",
        "  Terminal build-up (at maturity)",
        "  " + "-" * 44,
        f"    annual revenue          : {human(r['terminal_revenue']):>14}",
        f"    profit  (x margin)      : {human(r['terminal_profit']):>14}  ({r['margin_basis']})",
        f"    enterprise value        : {human(r['terminal_ev']):>14}  @ {r['exit_multiple']:.2f}x",
        f"    - net debt              : {human(r['net_debt']):>14}",
        f"    = equity value          : {human(r['terminal_equity']):>14}",
        "",
        f"  Market cap now      : {human(r['market_cap_now']):>14}",
        f"  Shares now -> exit  : {human(r['shares_now']):>14} -> {human(r['shares_exit'])}  (+{r['total_dilution'] * 100:.1f}% total)",
        f"  Entry price         : {r['entry_price']:>14.4f}",
        f"  Terminal price      : {r['terminal_price']:>14.4f}",
        "",
        f"  ANNUALIZED ROI      : {pct(r['annualized_roi'])}  / yr",
        f"  Return multiple     : {r['return_multiple']:.2f}x  over {r['holding_years']}y",
        "",
        "  Return attribution (annualized)",
        "  " + "-" * 44,
        f"    value creation    {pct(a['value_creation'])}   ({r['value_creation_multiple']:.2f}x today's mkt cap)",
        f"    dilution          {pct(a['dilution'])}",
        f"    = total           {pct(r['annualized_roi'])}",
        "",
        f"  valuation.{METHOD}.roi  : {r['annualized_roi']}",
        f"  valuation.{METHOD}.date : {as_of}",
    ]
    if doc_path is not None:
        out.append(f"  ({'written to ' + str(doc_path) if wrote else 'dry run — not written'})")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Entry points                                                                 #
# --------------------------------------------------------------------------- #
def run_doc_mode(args: argparse.Namespace) -> int:
    doc_path = resolve_stock_doc(args.stock_doc, args.stock_dir)
    if not doc_path.exists():
        fail(f"stock-doc not found: {doc_path}")
    _, fm = split_front_matter(doc_path.read_text(encoding="utf-8"))
    valuation = fm.get("valuation")
    if not isinstance(valuation, dict) or not isinstance(valuation.get(METHOD), dict):
        fail(
            f"stock-doc has no 'valuation.{METHOD}' input block. Add one under the "
            f"front matter (see the tam-capture reference) and re-run."
        )
    raw = valuation[METHOD]
    legacy = sorted(key for key in ("years", "tam", "capture", "terminal-revenue") if key in raw)
    if legacy:
        fail(
            f"valuation.{METHOD}: remove legacy input(s) {', '.join(legacy)}; "
            "the market-doc now owns the horizon and terminal revenue"
        )
    market_doc = raw.get("market-doc")
    if not isinstance(market_doc, str) or not market_doc.strip():
        fail(f"valuation.{METHOD}: missing required input 'market-doc'")
    player = raw.get("market-player") or fm.get("ticker") or fm.get("company")
    if not isinstance(player, str) or not player.strip():
        fail(
            f"valuation.{METHOD}: add 'market-player' because the stock-doc has "
            "no ticker or company selector"
        )
    market = load_market_revenue(market_doc, player, args.market_dir)
    kwargs = resolve_inputs(
        {**raw, "years": market["years"], "terminal-revenue": market["terminal_revenue"]},
        source=f"valuation.{METHOD}",
    )
    result = compute(**kwargs)
    result.update({
        "market_doc": market["market_id"],
        "market_doc_path": str(market["path"]),
        "market_player": market["player_ticker"] or market["player_name"],
        "market_player_name": market["player_name"],
        "market_currency": market["currency"],
        "terminal_revenue_billions": market["terminal_revenue_billions"],
        "projection_year": market["projection_year"],
    })
    as_of = resolve_as_of(args.as_of)

    wrote = not args.dry_run
    if wrote:
        write_outputs(doc_path, result["annualized_roi"], as_of)

    if args.format == "json":
        print(json.dumps({**result, "date": as_of, "stock_doc": str(doc_path), "written": wrote}, indent=2))
    else:
        print(render_table(result, doc_path, wrote, as_of))
    return 0


def run_cli_mode(args: argparse.Namespace) -> int:
    missing = [f for f in ("price", "shares", "market_doc", "margin", "exit_multiple")
               if getattr(args, f) is None]
    if missing:
        fail("raw mode needs --" + ", --".join(m.replace("_", "-") for m in missing)
             + " (or pass --stock-doc instead)")
    player = args.market_player or args.ticker
    if not player:
        fail("raw mode needs --ticker or --market-player to select the company in the market-doc")
    market = load_market_revenue(args.market_doc, player, args.market_dir)
    raw = {
        "price": args.price, "shares": args.shares, "years": market["years"],
        "terminal-revenue": market["terminal_revenue"],
        "margin": args.margin, "exit-multiple": args.exit_multiple,
        "dilution": args.dilution, "net-debt": args.net_debt, "margin-basis": args.margin_basis,
        "role-model": args.role_model,
    }
    kwargs = resolve_inputs(raw, source="arguments")
    result = compute(**kwargs)
    result.update({
        "market_doc": market["market_id"],
        "market_doc_path": str(market["path"]),
        "market_player": market["player_ticker"] or market["player_name"],
        "market_player_name": market["player_name"],
        "market_currency": market["currency"],
        "terminal_revenue_billions": market["terminal_revenue_billions"],
        "projection_year": market["projection_year"],
    })
    as_of = resolve_as_of(args.as_of)
    print(json.dumps({**result, "date": as_of}, indent=2) if args.format == "json"
          else render_table(result, None, False, as_of))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="'It works' annualized ROI from a market-doc 10-year company-revenue estimate.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--stock-doc", help="Ticker (resolved in the stock dir) or path to a stock-doc .md. "
                                       "Reads valuation.tam-capture inputs and writes valuation.tam-capture.roi back.")
    p.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    p.add_argument("--market-dir", type=Path, default=DEFAULT_MARKET_DIR)
    p.add_argument("--dry-run", action="store_true", help="Stock-doc mode: compute without writing back.")
    p.add_argument("--as-of", help="Valuation date stamped alongside roi (ISO YYYY-MM-DD). Default: today.")
    # Raw mode inputs (used only when --stock-doc is absent):
    p.add_argument("--ticker", help="Subject ticker; selects players.model-estimate in raw mode.")
    p.add_argument("--market-doc", help="Market id or path containing the terminal revenue estimate.")
    p.add_argument("--market-player", help="Exact market-doc player ticker or name; overrides --ticker.")
    p.add_argument("--price", type=float, help="Entry price per share (today).")
    p.add_argument("--shares", type=float, help="Today's diluted share count.")
    p.add_argument("--margin", help="Mature profit margin (e.g. 28%% or 0.28); matches --margin-basis.")
    p.add_argument("--margin-basis", choices=("EBITDA", "EBIT"), default="EBITDA",
                   help="Profit line the margin and exit multiple reference.")
    p.add_argument("--exit-multiple", type=float, help="EV/EBITDA (or EV/EBIT) expected at maturity.")
    p.add_argument("--dilution", default="0", help="Yearly share issuance: one rate or 10 comma-separated.")
    p.add_argument("--net-debt", type=float, default=0.0, help="Terminal net debt (negative = net cash).")
    p.add_argument("--role-model", help="Ticker used to calibrate margin, multiple, and dilution.")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    return run_doc_mode(args) if args.stock_doc else run_cli_mode(args)


if __name__ == "__main__":
    raise SystemExit(main())
