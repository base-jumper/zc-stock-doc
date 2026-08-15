#!/usr/bin/env python3
"""Estimate the expected annualized ROI of a stock over a holding period via an
exit-multiple terminal-value model (the reverse-engineered, Damodaran-style forward
return).

The model anchors on an *equity, per-share* fundamental (Earnings/share or FCF/share):

  1. Grow the fundamental at a *business-level* (aggregate) rate each year, then
     convert it to a per-share figure by netting off share-count change (dilution):

         fund_t = fund_0 * prod_{i<=t}(1 + g_i) / prod_{i<=t}(1 + d_i)

     g_i is aggregate growth; d_i is the signed dilution rate (a percentage of
     shares on issue). POSITIVE d = dilution (more shares, drags per-share down);
     NEGATIVE d = net buybacks (accretive). Defining g as business growth keeps
     growth and share-count orthogonal — never fold dilution into g as well, or it
     double-counts.

  2. Apply the expected EXIT MULTIPLE to the exit-year fundamental for the sale price:

         exit_price = exit_multiple * fund_N

     The *entry* multiple is implied by the inputs (entry_price / fund_0); the gap
     between entry and exit multiples is the re-rating.

  3. Pay a dividend each year as a payout fraction of that year's fundamental
     (a dividend YIELD input is just converted to an entry payout fraction).
     Dividends are ALWAYS reinvested — which is exactly what an IRR assumes about
     interim cash flows — so the expected return is the IRR of:

         t=0 : -entry_price
         t=1..N-1 : +dividend_t
         t=N : +dividend_N + exit_price

The headline output is that IRR (the expected annualized total return). It is also
decomposed, Damodaran-style, into the three sources of return — per-share growth
(business growth net of dilution), multiple re-rating, and income — which compose
multiplicatively to the price return and, with income, approximate the total.

============================================================================
Two ways to run it
============================================================================

This is the valuation counterpart of company_score.py and shares its interface.

  * STOCK-DOC mode (the integrated flow). Pass a stock-doc; the script reads the
    exit-multiple inputs from its front matter and writes the annualized ROI back:

        exit_multiple_valuation.py --stock-doc HUBB

    It reads `valuation.exit-multiple` from the front matter and writes the annualized
    ROI back as a `roi` child of that same block (surgical — only that line is touched),
    so you can hand-tweak the inputs and re-run to refresh the output.

    Stock-doc front matter (example):

        ---
        ticker: HUBB
        valuation:
          exit-multiple:
            price: 476.89
            entry-multiple: 24.36   # written by this script (price / fundamental)
            years: 5
            metric: Earnings        # Earnings or FCF
            fundamental: 19.575     # best estimate for TODAY's per-share fundamental
            growth: 8%              # aggregate business growth (scalar or per-year list)
            exit-multiple: 22
            dilution: -1.5%         # net buybacks are accretive
            dividend-yield: 1.2%    # or: payout: 30%
            roi: 0.0                # written by this script
            date: 2026-06-21        # written by this script (valuation as-of date)
        ---

    Alongside `roi` it stamps `date` (the as-of date of the run — today, or --as-of)
    and `entry-multiple` (price / fundamental, recorded next to `price` so the reader
    sees what multiple that price implied). Together they tell the next reader how
    stale the stored ROI is: how long ago it was computed, and against what price and
    entry multiple.

  * RAW mode (ad-hoc sanity check, no doc). Pass the inputs as flags:

        exit_multiple_valuation.py --price 100 --years 5 --fundamental 5 \
            --growth 10% --exit-multiple 18 --payout 30% --dilution 1.5%

Rates accept a trailing '%' ("10%" == 0.10) or a plain decimal (0.10). --growth and
--dilution take either one value (applied to every year) or a per-year list (a
comma-separated string on the CLI, or a YAML list in front matter) of length N.

Requires PyYAML for stock-doc mode. No secrets, no network.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

METHOD = "exit-multiple"  # front-matter block key, output prefix, and method id
WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"error: {msg}")


# --------------------------------------------------------------------------- #
# Parsing                                                                      #
# --------------------------------------------------------------------------- #
def parse_rate(s: Any, label: str) -> float:
    """Parse a rate: '10%' -> 0.10, '0.10' -> 0.10, 0.10 -> 0.10."""
    s = str(s).strip()
    try:
        return float(s[:-1]) / 100.0 if s.endswith("%") else float(s)
    except ValueError:
        fail(f"{label}: could not parse {s!r} as a rate (use e.g. 0.08 or 8%)")


def parse_rate_series(value: Any, years: int, label: str) -> list[float]:
    """Parse a scalar (broadcast to `years`) or a length-`years` series of rates.

    Accepts a YAML list ([0.12, 0.10]), a comma string ("0.12,0.10"), or a scalar.
    Every resulting growth/dilution factor (1 + rate) must be positive."""
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


def parse_metric(value: Any, *, required: bool, source: str) -> str | None:
    if value in (None, ""):
        if required:
            fail(f"{source}: missing required input 'metric' (use Earnings or FCF)")
        return None
    metric = str(value).strip().lower().replace("_", "-")
    aliases = {
        "earnings": "Earnings",
        "earning": "Earnings",
        "eps": "Earnings",
        "fcf": "FCF",
        "free-cash-flow": "FCF",
        "free cash flow": "FCF",
    }
    if metric not in aliases:
        fail(f"{source}: metric must be Earnings or FCF, got {value!r}")
    return aliases[metric]


# --------------------------------------------------------------------------- #
# The model                                                                    #
# --------------------------------------------------------------------------- #
def irr(cash_flows: list[float]) -> float:
    """IRR of a cash-flow series indexed by period (0..N) via bisection.

    Assumes the conventional one-sign-change pattern (an outflow at t=0, inflows
    after), so NPV is monotonic in the rate and the root is unique."""
    def npv(rate: float) -> float:
        return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cash_flows))

    lo, hi = -0.9999, 100.0
    f_lo, f_hi = npv(lo), npv(hi)
    if f_lo == 0.0:
        return lo
    if f_lo * f_hi > 0.0:
        fail("could not bracket an IRR (check the inputs — is any return possible?)")
    for _ in range(200):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid)
        if abs(f_mid) < 1e-10:
            return mid
        if f_lo * f_mid < 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def compute(
    price: float,
    years: int,
    fundamental: float,
    growth: list[float],
    dilution: list[float],
    exit_multiple: float,
    payout: float,
    metric: str | None = None,
) -> dict[str, Any]:
    if price <= 0:
        fail("price must be positive")
    if fundamental <= 0:
        fail("fundamental must be positive (needed to imply the entry multiple)")
    if exit_multiple <= 0:
        fail("exit-multiple must be positive")

    # Per-share fundamental path: business growth netted down by dilution.
    fund_path: list[float] = []
    g_cum = d_cum = 1.0
    for i in range(years):
        g_cum *= 1.0 + growth[i]
        d_cum *= 1.0 + dilution[i]
        fund_path.append(fundamental * g_cum / d_cum)

    fund_exit = fund_path[-1]
    exit_price = exit_multiple * fund_exit
    dividends = [payout * f for f in fund_path]  # year 1..N

    # Dividends reinvested == IRR's reinvestment assumption.
    cash_flows = [-price] + dividends[:-1] + [dividends[-1] + exit_price]
    total_return = irr(cash_flows)

    # Damodaran-style attribution (annualized). The first three compose
    # multiplicatively to the capital (price) return; income is the residual uplift.
    entry_multiple = price / fundamental
    n = float(years)
    business_cagr = g_cum ** (1.0 / n) - 1.0
    dilution_cagr = (1.0 / d_cum) ** (1.0 / n) - 1.0
    rerating_cagr = (exit_multiple / entry_multiple) ** (1.0 / n) - 1.0
    price_cagr = (exit_price / price) ** (1.0 / n) - 1.0
    income_cagr = total_return - price_cagr  # additive approximation

    result: dict[str, Any] = {
        "annualized_roi": round(total_return, 6),
        "return_multiple": round((1.0 + total_return) ** n, 4),
        "entry_price": round(price, 4),
        "exit_price": round(exit_price, 4),
        "entry_multiple": round(entry_multiple, 4),
        "exit_multiple": round(exit_multiple, 4),
        "metric": metric,
        "fundamental_now": round(fundamental, 6),
        "fundamental_exit": round(fund_exit, 6),
        "total_dividends": round(sum(dividends), 4),
        "holding_years": years,
        "attribution": {
            "business_growth": round(business_cagr, 6),
            "dilution": round(dilution_cagr, 6),
            "multiple_rerating": round(rerating_cagr, 6),
            "income": round(income_cagr, 6),
            "price_return": round(price_cagr, 6),
        },
    }
    return result


def resolve_inputs(
    raw: dict[str, Any],
    *,
    payout: Any,
    dividend_yield: Any,
    source: str,
) -> dict[str, Any]:
    """Turn a flat dict of raw inputs into validated arguments for compute()."""
    for req in ("price", "years", "fundamental", "growth", "exit-multiple"):
        if raw.get(req) in (None, ""):
            fail(f"{source}: missing required input {req!r}")

    years = require_int(raw["years"], "years")
    if payout not in (None, "") and dividend_yield not in (None, ""):
        fail(f"{source}: give only one of payout / dividend-yield, not both")

    price = require_float(raw["price"], "price")
    fundamental = require_float(raw["fundamental"], "fundamental")
    if dividend_yield not in (None, ""):
        payout_frac = parse_rate(dividend_yield, "dividend-yield") * price / fundamental
    elif payout not in (None, ""):
        payout_frac = parse_rate(payout, "payout")
    else:
        payout_frac = 0.0

    return dict(
        price=price,
        years=years,
        fundamental=fundamental,
        growth=parse_rate_series(raw["growth"], years, "growth"),
        dilution=parse_rate_series(raw.get("dilution", 0), years, "dilution"),
        exit_multiple=require_float(raw["exit-multiple"], "exit-multiple"),
        payout=payout_frac,
        metric=parse_metric(raw.get("metric"), required=source.startswith("valuation."), source=source),
    )


# --------------------------------------------------------------------------- #
# Front matter (stock-doc mode)                                                #
# --------------------------------------------------------------------------- #
def split_front_matter(text: str) -> tuple[str, dict[str, Any]]:
    import yaml

    m = FM_RE.match(text)
    if not m:
        fail("stock-doc has no YAML front matter (must start with a '---' block).")
    block = m.group(1)
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as e:
        fail(f"could not parse front matter as YAML: {e}")
    if not isinstance(data, dict):
        fail("front matter must be a YAML mapping.")
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
    of the method block. Everything else in the front matter is preserved. `value`
    is written verbatim, so the caller pre-formats it (a stringified number, an ISO
    date, etc.).
    """
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


def write_outputs(path: Path, roi: float, entry_multiple: float, as_of: str) -> None:
    """Stamp the computed `roi`, `entry-multiple`, and valuation `date` into the block.

    `entry-multiple` (price / fundamental) is recorded right after `price`; `roi` and
    `date` are kept together at the end of the method block."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        fail(f"cannot write back: {path} has no front-matter block.")
    block = upsert_valuation_child(m.group(1), METHOD, "entry-multiple",
                                   str(round(entry_multiple, 2)), after_key="price")
    block = upsert_valuation_child(block, METHOD, "roi", str(round(roi, 6)))
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


def render_table(r: dict[str, Any], doc_path: Path | None, wrote: bool, as_of: str) -> str:
    a = r["attribution"]
    head = doc_path.stem if doc_path else f"exit-multiple valuation"
    out = [
        f"{head}  —  expected ROI over {r['holding_years']}y (dividends reinvested)  as of {as_of}",
        "=" * 56,
        "",
        f"  Entry price       : {r['entry_price']:>12.4f}  @ {r['entry_multiple']:.2f}x",
        f"  Exit price        : {r['exit_price']:>12.4f}  @ {r['exit_multiple']:.2f}x",
        f"  Fundamental now   : {r['fundamental_now']:>12.4f}" + (f"  ({r['metric']})" if r.get("metric") else ""),
        f"  Fundamental exit  : {r['fundamental_exit']:>12.4f}" + (f"  ({r['metric']})" if r.get("metric") else ""),
        f"  Dividends (total) : {r['total_dividends']:>12.4f}",
        "",
        f"  ANNUALIZED ROI    : {pct(r['annualized_roi'])}  / yr",
        f"  Return multiple   : {r['return_multiple']:.2f}x  over {r['holding_years']}y",
        "",
        "  Return attribution (annualized)",
        "  " + "-" * 40,
        f"    business growth   {pct(a['business_growth'])}",
        f"    dilution          {pct(a['dilution'])}",
        f"    multiple re-rating{pct(a['multiple_rerating'])}",
        f"    income            {pct(a['income'])}",
        f"    = total           {pct(r['annualized_roi'])}",
    ]
    out += [
        "",
        f"  valuation.{METHOD}.entry-multiple : {round(r['entry_multiple'], 2)}",
        f"  valuation.{METHOD}.roi            : {r['annualized_roi']}",
        f"  valuation.{METHOD}.date           : {as_of}",
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
            f"front matter (see the exit-multiple reference) and re-run."
        )
    block = valuation[METHOD]
    kwargs = resolve_inputs(
        block,
        payout=block.get("payout"),
        dividend_yield=block.get("dividend-yield"),
        source=f"valuation.{METHOD}",
    )
    result = compute(**kwargs)
    as_of = resolve_as_of(args.as_of)

    wrote = not args.dry_run
    if wrote:
        write_outputs(doc_path, result["annualized_roi"], result["entry_multiple"], as_of)

    if args.format == "json":
        print(json.dumps({**result, "date": as_of, "stock_doc": str(doc_path), "written": wrote}, indent=2))
    else:
        print(render_table(result, doc_path, wrote, as_of))
    return 0


def run_cli_mode(args: argparse.Namespace) -> int:
    missing = [f for f in ("price", "years", "fundamental", "growth", "exit_multiple")
               if getattr(args, f) is None]
    if missing:
        fail("raw mode needs --" + ", --".join(m.replace("_", "-") for m in missing)
             + " (or pass --stock-doc instead)")
    raw = {
        "price": args.price, "years": args.years, "metric": args.metric, "fundamental": args.fundamental,
        "growth": args.growth, "exit-multiple": args.exit_multiple,
        "dilution": args.dilution,
    }
    kwargs = resolve_inputs(
        raw, payout=args.payout, dividend_yield=args.dividend_yield, source="arguments"
    )
    result = compute(**kwargs)
    as_of = resolve_as_of(args.as_of)
    print(json.dumps({**result, "date": as_of}, indent=2) if args.format == "json"
          else render_table(result, None, False, as_of))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Expected annualized ROI from an exit-multiple terminal-value model (equity basis).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--stock-doc", help="Ticker (resolved in the stock dir) or path to a stock-doc .md. "
                                       "Reads valuation.exit-multiple inputs and writes valuation.exit-multiple.roi back.")
    p.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    p.add_argument("--dry-run", action="store_true", help="Stock-doc mode: compute without writing back.")
    p.add_argument("--as-of", help="Valuation date stamped alongside roi (ISO YYYY-MM-DD). Default: today.")
    # Raw mode inputs (used only when --stock-doc is absent):
    p.add_argument("--price", type=float, help="Entry price per share (today).")
    p.add_argument("--years", type=int, help="Holding period in whole years.")
    p.add_argument("--metric", choices=("Earnings", "FCF"), help="Raw mode: fundamental metric used.")
    p.add_argument("--fundamental", type=float, help="Best estimate for today's per-share fundamental.")
    p.add_argument("--growth", help="Aggregate (business) growth: one rate or N comma-separated.")
    p.add_argument("--exit-multiple", type=float, help="Expected P/E or P/FCF applied at sale.")
    p.add_argument("--dilution", default="0", help="Signed share-count change: +dilution / -buyback.")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--payout", help="Dividend payout as a fraction of the fundamental (e.g. 40%% or 0.4).")
    g.add_argument("--dividend-yield", help="Entry dividend yield; converted to a payout fraction.")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    return run_doc_mode(args) if args.stock_doc else run_cli_mode(args)


if __name__ == "__main__":
    raise SystemExit(main())
