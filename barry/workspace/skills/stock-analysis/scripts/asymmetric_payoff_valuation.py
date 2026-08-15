#!/usr/bin/env python3
"""Estimate the expected annualized ROI of an asymmetric (freeroll) bet via a
probability-weighted two-outcome payoff model.

The freeroll thesis is binary: a stock bought near its valuation FLOOR either
re-rates to FAIR VALUE when its catalyst fires (probability p), or it fails and we
exit back at the floor (probability 1 - p). Both outcomes are assumed to resolve at
the catalyst horizon. The model blends them into an expected holding-period return
and annualizes it:

    downside_pct   = (price - floor)      / price        # loss if it falls to the floor
    upside_pct     = (fair_value - price) / price        # gain if it re-rates to fair value
    asymmetry      = upside_pct / downside_pct           # the headline risk/reward ratio
    expected_roi   = p * upside_pct - (1 - p) * downside_pct   # over the horizon
    annualized_roi = (1 + expected_roi) ** (1 / years) - 1

The three price inputs come straight from the freeroll traits: `floor` from
downside-support, `fair_value` from fair-value-upside (derived via the catalyst),
and `p` / `years` from the catalyst (its probability and window). Income earned
while waiting (dividends/carry) is NOT modelled here — the payoff is price-only.

============================================================================
Two ways to run it
============================================================================

This is a valuation method for the freeroll strategy and shares company_score.py's
interface (it is the asymmetric-payoff counterpart of exit_multiple_valuation.py).

  * STOCK-DOC mode (the integrated flow). Pass a stock-doc; the script reads the
    asymmetric-payoff inputs from its front matter and writes the annualized ROI back:

        asymmetric_payoff_valuation.py --stock-doc SRG.AX

    It reads `valuation.asymmetric-payoff` from the front matter and writes the
    annualized ROI back as a `roi` child of that same block (surgical — only that
    line is touched), so you can hand-tweak the inputs and re-run to refresh the output.

    Stock-doc front matter (example):

        ---
        ticker: SRG.AX
        valuation:
          asymmetric-payoff:
            price: 1.00            # entry price per share (today)
            floor: 0.85            # downside-support floor per share
            fair-value: 1.60       # fair value after the catalyst plays out
            probability: 60%       # catalyst's probability of success (p)
            years: 2               # catalyst window (whole or fractional years)
            roi: 0.0               # written by this script
            date: 2026-06-21       # written by this script (valuation as-of date)
        ---

    Alongside `roi` it stamps `date` — the as-of date of the run (today, or
    --as-of). Together they tell the next reader how stale the stored ROI is:
    how long ago it was computed, and against what `price`.

  * RAW mode (ad-hoc sanity check, no doc). Pass the inputs as flags:

        asymmetric_payoff_valuation.py --price 1.00 --floor 0.85 \
            --fair-value 1.60 --probability 60% --years 2

Rates (probability) accept a trailing '%' ("60%" == 0.60) or a plain decimal (0.60).
Requires PyYAML for stock-doc mode. No secrets, no network.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

METHOD = "asymmetric-payoff"  # front-matter block key, output prefix, and method id
WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"error: {msg}")


# --------------------------------------------------------------------------- #
# Parsing                                                                      #
# --------------------------------------------------------------------------- #
def parse_rate(s: Any, label: str) -> float:
    """Parse a rate: '60%' -> 0.60, '0.60' -> 0.60, 0.60 -> 0.60."""
    s = str(s).strip()
    try:
        return float(s[:-1]) / 100.0 if s.endswith("%") else float(s)
    except ValueError:
        fail(f"{label}: could not parse {s!r} as a rate (use e.g. 0.6 or 60%)")


def require_float(value: Any, label: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        fail(f"{label}: expected a number, got {value!r}")


# --------------------------------------------------------------------------- #
# The model                                                                    #
# --------------------------------------------------------------------------- #
def compute(
    price: float,
    floor: float,
    fair_value: float,
    probability: float,
    years: float,
) -> dict[str, Any]:
    if price <= 0:
        fail("price must be positive")
    if fair_value <= 0:
        fail("fair-value must be positive")
    if floor < 0:
        fail("floor must be non-negative")
    if floor >= price:
        fail("floor must be below price (there must be a real downside to measure against)")
    if not 0.0 <= probability <= 1.0:
        fail(f"probability must be in [0, 1], got {probability}")
    if years <= 0:
        fail("years must be positive")

    downside_pct = (price - floor) / price
    upside_pct = (fair_value - price) / price
    asymmetry = upside_pct / downside_pct  # downside_pct > 0 guaranteed above
    expected_roi = probability * upside_pct - (1.0 - probability) * downside_pct
    annualized_roi = (1.0 + expected_roi) ** (1.0 / years) - 1.0

    result: dict[str, Any] = {
        "annualized_roi": round(annualized_roi, 6),
        "expected_roi": round(expected_roi, 6),
        "return_multiple": round(1.0 + expected_roi, 4),
        "entry_price": round(price, 4),
        "floor": round(floor, 4),
        "fair_value": round(fair_value, 4),
        "downside_pct": round(downside_pct, 6),
        "upside_pct": round(upside_pct, 6),
        "asymmetry": round(asymmetry, 4),
        "probability": round(probability, 6),
        "holding_years": years,
    }
    return result


def resolve_inputs(raw: dict[str, Any], *, source: str) -> dict[str, Any]:
    """Turn a flat dict of raw inputs into validated arguments for compute()."""
    for req in ("price", "floor", "fair-value", "probability", "years"):
        if raw.get(req) in (None, ""):
            fail(f"{source}: missing required input {req!r}")
    return dict(
        price=require_float(raw["price"], "price"),
        floor=require_float(raw["floor"], "floor"),
        fair_value=require_float(raw["fair-value"], "fair-value"),
        probability=parse_rate(raw["probability"], "probability"),
        years=require_float(raw["years"], "years"),
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


def upsert_valuation_child(block: str, method: str, key: str, value: str) -> str:
    """Surgically set `<key>: <value>` inside the `valuation.<method>` mapping.

    Updates the child in place if present, otherwise appends it as the last child
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
    if child_indent is None:
        child_indent = method_indent + 2

    new_line = f"{' ' * child_indent}{key}: {value}"
    if key_i is not None:
        lines[key_i] = new_line
    else:
        insert_at = end_i
        while insert_at > method_i + 1 and not lines[insert_at - 1].strip():
            insert_at -= 1
        lines.insert(insert_at, new_line)
    return "\n".join(lines)


def write_outputs(path: Path, roi: float, as_of: str) -> None:
    """Stamp the computed `roi` and the valuation `date` back into the method block."""
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


def render_table(r: dict[str, Any], doc_path: Path | None, wrote: bool, as_of: str) -> str:
    head = doc_path.stem if doc_path else "asymmetric-payoff valuation"
    out = [
        f"{head}  —  expected ROI over {r['holding_years']:g}y (probability-weighted)  as of {as_of}",
        "=" * 56,
        "",
        f"  Entry price       : {r['entry_price']:>12.4f}",
        f"  Floor (downside)  : {r['floor']:>12.4f}   {pct(-r['downside_pct'])}",
        f"  Fair value (up)   : {r['fair_value']:>12.4f}   {pct(r['upside_pct'])}",
        f"  Asymmetry (up:dn) : {r['asymmetry']:>11.2f}x",
        f"  Catalyst p        : {r['probability'] * 100:>11.1f}%",
        "",
        f"  Expected return   : {pct(r['expected_roi'])}  over {r['holding_years']:g}y",
        f"  ANNUALIZED ROI    : {pct(r['annualized_roi'])}  / yr",
        f"  Return multiple   : {r['return_multiple']:.2f}x",
    ]
    out += [
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
            f"front matter (see the asymmetric-payoff reference) and re-run."
        )
    kwargs = resolve_inputs(valuation[METHOD], source=f"valuation.{METHOD}")
    result = compute(**kwargs)
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
    missing = [f for f in ("price", "floor", "fair_value", "probability", "years")
               if getattr(args, f) is None]
    if missing:
        fail("raw mode needs --" + ", --".join(m.replace("_", "-") for m in missing)
             + " (or pass --stock-doc instead)")
    raw = {
        "price": args.price, "floor": args.floor, "fair-value": args.fair_value,
        "probability": args.probability, "years": args.years,
    }
    result = compute(**resolve_inputs(raw, source="arguments"))
    as_of = resolve_as_of(args.as_of)
    print(json.dumps({**result, "date": as_of}, indent=2) if args.format == "json"
          else render_table(result, None, False, as_of))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Expected annualized ROI from a probability-weighted asymmetric (freeroll) payoff.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--stock-doc", help="Ticker (resolved in the stock dir) or path to a stock-doc .md. "
                                       "Reads valuation.asymmetric-payoff inputs and writes valuation.asymmetric-payoff.roi back.")
    p.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    p.add_argument("--dry-run", action="store_true", help="Stock-doc mode: compute without writing back.")
    p.add_argument("--as-of", help="Valuation date stamped alongside roi (ISO YYYY-MM-DD). Default: today.")
    # Raw mode inputs (used only when --stock-doc is absent):
    p.add_argument("--price", type=float, help="Entry price per share (today).")
    p.add_argument("--floor", type=float, help="Downside-support floor per share.")
    p.add_argument("--fair-value", type=float, help="Fair value per share after the catalyst.")
    p.add_argument("--probability", help="Catalyst probability of success p (e.g. 60%% or 0.6).")
    p.add_argument("--years", type=float, help="Catalyst window in years (whole or fractional).")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    return run_doc_mode(args) if args.stock_doc else run_cli_mode(args)


if __name__ == "__main__":
    raise SystemExit(main())
