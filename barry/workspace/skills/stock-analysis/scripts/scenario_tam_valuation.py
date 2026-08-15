#!/usr/bin/env python3
"""Estimate the EXPECTED annualized ROI of an early-stage company by
probability-weighting up to four outcome scenarios, each valued with the
tam-capture terminal build (see tam_capture_valuation.py, which this script
reuses for the per-scenario arithmetic and the stock-doc plumbing).

Scenarios (fixed names; `failure` and `it-works` are required):

    failure          the company dies; a direct residual `terminal-equity`
                     (cash less wind-down, or an IP/asset sale)
    niche-survivor   survives but never escapes sub-scale (its own role model)
    it-works         the tam-capture "it works" case, verbatim
    blue-sky         the same role model at its actually-achieved economics
                     (optional — omit when merged into it-works)

`price`, `shares`, `years`, and `net-debt` are shared across scenarios (same
company, same horizon). `tam` is the shared BASE boundary — the maturity-year
market at now + years, never today's — and a scenario may carry its own `tam`
where its ending implies a different market (blue-sky usually does: the market
a technology wins big in is rarely today's obvious one). Each scenario's
capture must be measured against its own TAM's boundary. A scenario carries
either the tam-capture inputs (capture / margin / margin-basis / exit-multiple /
dilution / role-model, plus an optional tam) or a direct `terminal-equity`; the
base `tam` may be omitted only when every TAM-built scenario has its own.

The expectation is taken in TERMINAL-VALUE space and annualized once:

    E[terminal_price] = sum_i p_i * terminal_price_i
    expected_roi      = (E[terminal_price] / price) ^ (1/years) - 1

Never average per-scenario ROIs: wealth compounds on terminal values, and
annualization is concave, so a probability-weighted average of CAGRs understates
the return on expected terminal wealth (Jensen).

`failure.probability` may be omitted, in which case it is the residual
1 - sum(other probabilities). If every probability is explicit they must sum
to 1.

Besides the headline ROI the script reports:

  * per-scenario terminal values, standalone ROIs, and contributions to the
    expectation (warning when a single sub-10% scenario contributes over half);
  * P(below entry) — total probability of ending under today's price;
  * the implied power-law tail exponent between it-works and blue-sky
    (alpha = ln(P(>=v_iw)/P(>=v_bs)) / ln(v_bs/v_iw)), warning outside
    ~1.5-3.0 — venture outcome research (Othman, AngelList 2019) puts the
    upper tail near alpha ~ 2;
  * the market-implied breakeven: the P(it-works) that, against the failure
    outcome alone, the current price needs to clear --hurdle (default 10%/yr).

Two ways to run it (mirrors the other valuation scripts):

  * STOCK-DOC mode — read `valuation.scenario-tam` from the front matter and
    write `roi` + `date` back surgically:

        scenario_tam_valuation.py --stock-doc BRN.AX
        scenario_tam_valuation.py --stock-doc BRN.AX --dry-run --format json

  * RAW mode — shared inputs as flags, one --scenario per outcome as
    "name,key=value,..." ('|' separates per-year dilution lists):

        scenario_tam_valuation.py --price 0.155 --shares 2419.8e6 --years 8 --tam 25e9 \
            --scenario "failure,terminal-equity=20e6" \
            --scenario "it-works,probability=13%,capture=2%,margin=25%,exit-multiple=18,dilution=6%,role-model=ARM"

See references/valuation/scenario-tam.md for the methodology (role models per
scenario, probability base rates, tail consistency).
"""
from __future__ import annotations

import argparse
import json
import math
from typing import Any

import tam_capture_valuation as tc

METHOD = "scenario-tam"  # front-matter block key, output prefix, and method id
SCENARIO_ORDER = ("failure", "niche-survivor", "it-works", "blue-sky")
REQUIRED_SCENARIOS = ("failure", "it-works")
ALPHA_BAND = (1.5, 3.0)
PROB_TOL = 1e-6

fail = tc.fail


# --------------------------------------------------------------------------- #
# Parsing                                                                      #
# --------------------------------------------------------------------------- #
def parse_probabilities(scenarios: dict[str, dict]) -> tuple[dict[str, float], bool]:
    """Per-scenario probabilities in [0, 1]. Only `failure` may omit its
    probability, in which case it becomes the residual 1 - sum(others)."""
    probs: dict[str, float | None] = {}
    for name, sc in scenarios.items():
        p = sc.get("probability")
        if p in (None, ""):
            if name != "failure":
                fail(f"{name}: probability is required (only failure may omit it "
                     "and take the residual)")
            probs[name] = None
        else:
            v = tc.parse_rate(p, f"{name}.probability")
            if not 0.0 <= v <= 1.0:
                fail(f"{name}.probability: must be in [0, 1], got {v}")
            probs[name] = v

    explicit = sum(v for v in probs.values() if v is not None)
    residual = probs.get("failure") is None
    if residual:
        if explicit > 1.0 + PROB_TOL:
            fail(f"scenario probabilities sum to {explicit:.4f} > 1 before the "
                 "failure residual — reduce them")
        probs["failure"] = max(1.0 - explicit, 0.0)
    elif abs(explicit - 1.0) > PROB_TOL:
        fail(f"scenario probabilities must sum to 1, got {explicit:.4f} "
             "(or omit failure.probability to make it the residual)")
    return {k: float(v) for k, v in probs.items()}, residual


def parse_scenario_flag(spec: str) -> tuple[str, dict[str, str]]:
    """RAW mode: 'name,key=value,...' -> (name, raw dict). '|' -> ',' in values
    so per-year dilution lists survive the comma split."""
    parts = [p.strip() for p in spec.split(",") if p.strip()]
    if not parts:
        fail("--scenario: empty spec")
    name, raw = parts[0], {}
    for part in parts[1:]:
        if "=" not in part:
            fail(f"--scenario {name}: expected key=value, got {part!r}")
        k, v = part.split("=", 1)
        raw[k.strip()] = v.strip().replace("|", ",")
    return name, raw


# --------------------------------------------------------------------------- #
# The model                                                                    #
# --------------------------------------------------------------------------- #
def scenario_terminal(
    name: str, sc: dict[str, Any],
    price: float, shares: float, years: int, tam: float | None, net_debt: float,
) -> dict[str, Any]:
    """One scenario's terminal equity / per-share value / standalone ROI, via a
    direct terminal-equity or the tam-capture build. A scenario-level `tam`
    overrides the shared base boundary."""
    src = f"scenarios.{name}"
    dilution = tc.parse_rate_series(sc.get("dilution", 0), years, f"{src}.dilution")
    role_model = sc.get("role-model")
    role_model = str(role_model).strip() if role_model not in (None, "") else None
    sc_tam = sc.get("tam")
    tam_i = tc.require_float(sc_tam, f"{src}.tam") if sc_tam not in (None, "") else tam

    if sc.get("terminal-equity") not in (None, ""):
        terminal_equity = tc.require_float(sc["terminal-equity"], f"{src}.terminal-equity")
        if terminal_equity < 0:
            fail(f"{src}.terminal-equity: must be >= 0")
        d_cum = 1.0
        for d in dilution:
            d_cum *= 1.0 + d
        terminal_price = terminal_equity / (shares * d_cum)
        margin_basis = None
        tam_used = None
    else:
        for req in ("capture", "margin", "exit-multiple"):
            if sc.get(req) in (None, ""):
                fail(f"{src}: needs either terminal-equity or the tam-capture "
                     f"inputs — missing {req!r}")
        if tam_i is None:
            fail(f"{src}: needs a tam — its own, or the shared base tam")
        r = tc.compute(
            price=price, shares=shares, years=years,
            terminal_revenue=tam_i * tc.parse_rate(sc["capture"], f"{src}.capture"),
            margin=tc.parse_rate(sc["margin"], f"{src}.margin"),
            exit_multiple=tc.require_float(sc["exit-multiple"], f"{src}.exit-multiple"),
            dilution=dilution, net_debt=net_debt,
            margin_basis=tc.parse_basis(sc.get("margin-basis"), src),
            role_model=role_model,
        )
        terminal_equity, terminal_price = r["terminal_equity"], r["terminal_price"]
        margin_basis = r["margin_basis"]
        tam_used = tam_i

    roi = (terminal_price / price) ** (1.0 / years) - 1.0 if terminal_price > 0 else -1.0
    return {
        "scenario": name,
        "role_model": role_model,
        "margin_basis": margin_basis,
        "tam": round(tam_used, 2) if tam_used is not None else None,
        "terminal_equity": round(terminal_equity, 2),
        "terminal_price": round(terminal_price, 6),
        "scenario_roi": round(roi, 6),
    }


def implied_tail_alpha(results: dict[str, dict], probs: dict[str, float]) -> float | None:
    """Tail exponent implied by the two upper scenarios, from the survival
    function: P(V >= v_iw) = p_iw + p_bs, P(V >= v_bs) = p_bs."""
    if "blue-sky" not in results:
        return None
    v_iw, v_bs = results["it-works"]["terminal_equity"], results["blue-sky"]["terminal_equity"]
    p_iw, p_bs = probs["it-works"], probs["blue-sky"]
    if v_bs <= v_iw or p_bs <= 0.0 or p_iw <= 0.0:
        return None
    return math.log((p_iw + p_bs) / p_bs) / math.log(v_bs / v_iw)


def compute(
    price: float, shares: float, years: int, tam: float | None, net_debt: float,
    scenarios: dict[str, dict], hurdle: float,
) -> dict[str, Any]:
    unknown = sorted(set(scenarios) - set(SCENARIO_ORDER))
    if unknown:
        fail(f"unknown scenario(s) {unknown} — allowed: {list(SCENARIO_ORDER)}")
    for req in REQUIRED_SCENARIOS:
        if req not in scenarios:
            fail(f"missing required scenario {req!r}")
    if price <= 0:
        fail("price must be positive (it is the ROI denominator)")
    if shares <= 0:
        fail("shares must be positive")
    years = tc.require_int(years, "years")

    probs, failure_residual = parse_probabilities(scenarios)
    results = {name: scenario_terminal(name, sc, price, shares, years, tam, net_debt)
               for name, sc in scenarios.items()}

    expected_tp = sum(probs[n] * results[n]["terminal_price"] for n in results)
    if expected_tp <= 0:
        fail("expected terminal price is non-positive — check the scenario values")
    n = float(years)
    expected_roi = (expected_tp / price) ** (1.0 / n) - 1.0
    p_below_entry = sum(probs[n_] for n_ in results
                        if results[n_]["terminal_price"] < price)

    ordered = [n_ for n_ in SCENARIO_ORDER if n_ in results]
    table = []
    for name in ordered:
        r = results[name]
        table.append({
            **r,
            "probability": round(probs[name], 6),
            "contribution": round(probs[name] * r["terminal_price"] / expected_tp, 6),
        })

    warnings: list[str] = []
    alpha = implied_tail_alpha(results, probs)
    if alpha is not None and not ALPHA_BAND[0] <= alpha <= ALPHA_BAND[1]:
        direction = ("fatter tail than venture history supports (alpha ~ 2)"
                     if alpha < ALPHA_BAND[0] else
                     "blue-sky may be under-weighted relative to its value")
        warnings.append(
            f"implied tail alpha {alpha:.2f} outside {ALPHA_BAND[0]}-{ALPHA_BAND[1]}: {direction}")
    if "blue-sky" in results and results["blue-sky"]["terminal_equity"] <= results["it-works"]["terminal_equity"]:
        warnings.append("blue-sky terminal equity does not exceed it-works — "
                        "the scenarios are mis-ordered")
    top = max(table, key=lambda row: row["contribution"])
    if top["probability"] < 0.10 and top["contribution"] > 0.5:
        warnings.append(
            f"{top['scenario']} ({top['probability']:.0%} probable) contributes "
            f"{top['contribution']:.0%} of the expected value — the estimate is "
            "tail-dominated; the probability deserves extra scrutiny")

    # Market-implied breakeven: P(it-works) vs failure alone that clears the hurdle.
    target = price * (1.0 + hurdle) ** n
    tp_iw = results["it-works"]["terminal_price"]
    tp_fail = results["failure"]["terminal_price"]
    breakeven = ((target - tp_fail) / (tp_iw - tp_fail)) if tp_iw > tp_fail else None

    return {
        "expected_annualized_roi": round(expected_roi, 6),
        "expected_return_multiple": round(expected_tp / price, 4),
        "holding_years": years,
        "entry_price": round(price, 4),
        "expected_terminal_price": round(expected_tp, 6),
        "p_below_entry": round(p_below_entry, 6),
        "failure_probability_residual": failure_residual,
        "implied_tail_alpha": round(alpha, 4) if alpha is not None else None,
        "hurdle": hurdle,
        "breakeven_p_it_works": round(breakeven, 4) if breakeven is not None else None,
        "scenarios": table,
        "warnings": warnings,
    }


def resolve_shared(raw: dict[str, Any], *, source: str) -> dict[str, Any]:
    for req in ("price", "shares", "years"):
        if raw.get(req) in (None, ""):
            fail(f"{source}: missing required input {req!r}")
    scenarios = raw.get("scenarios")
    if not isinstance(scenarios, dict) or not scenarios:
        fail(f"{source}: missing 'scenarios' mapping")
    for name, sc in scenarios.items():
        if not isinstance(sc, dict):
            fail(f"{source}.scenarios.{name}: expected a mapping of inputs")
    base_tam = raw.get("tam")
    return dict(
        price=tc.require_float(raw["price"], "price"),
        shares=tc.require_float(raw["shares"], "shares"),
        years=tc.require_int(raw["years"], "years"),
        tam=tc.require_float(base_tam, "tam") if base_tam not in (None, "") else None,
        net_debt=tc.require_float(raw.get("net-debt", 0) or 0, "net-debt"),
        scenarios=scenarios,
    )


# --------------------------------------------------------------------------- #
# Output                                                                       #
# --------------------------------------------------------------------------- #
def write_outputs(path, roi: float, as_of: str) -> None:
    """Stamp `roi` and `date` into the scenario-tam block (surgical)."""
    text = path.read_text(encoding="utf-8")
    m = tc.FM_RE.match(text)
    if not m:
        fail(f"cannot write back: {path} has no front-matter block.")
    block = tc.upsert_valuation_child(m.group(1), METHOD, "roi", str(round(roi, 6)))
    block = tc.upsert_valuation_child(block, METHOD, "date", as_of)
    path.write_text(f"---\n{block}\n---\n" + text[m.end():], encoding="utf-8")


def render_table(r: dict[str, Any], doc_path, wrote: bool, as_of: str) -> str:
    head = doc_path.stem if doc_path else "scenario-tam valuation"
    out = [
        f"{head}  —  expected ROI over {r['holding_years']}y (scenario-TAM, probability-weighted)  as of {as_of}",
        "=" * 78,
        "",
        f"  {'Scenario':<15}{'p':>7}  {'tam':>10}  {'terminal eq':>12}  {'/share':>10}  {'ROI/yr':>8}  {'contrib':>8}  role model",
        "  " + "-" * 86,
    ]
    for row in r["scenarios"]:
        tam_s = tc.human(row["tam"]) if row.get("tam") is not None else "—"
        out.append(
            f"  {row['scenario']:<15}{row['probability'] * 100:>6.1f}%  "
            f"{tam_s:>10}  "
            f"{tc.human(row['terminal_equity']):>12}  {row['terminal_price']:>10.4f}  "
            f"{row['scenario_roi'] * 100:>+7.1f}%  {row['contribution'] * 100:>7.1f}%  "
            f"{row['role_model'] or '—'}"
        )
    residual = "  (residual)" if r["failure_probability_residual"] else ""
    out += [
        "",
        f"  Entry price             : {r['entry_price']:.4f}",
        f"  Expected terminal price : {r['expected_terminal_price']:.4f}",
        f"  EXPECTED ANNUALIZED ROI : {tc.pct(r['expected_annualized_roi'])}  / yr",
        f"  Expected multiple       : {r['expected_return_multiple']:.2f}x  over {r['holding_years']}y",
        f"  P(below entry)          : {r['p_below_entry'] * 100:.1f}%",
        f"  Failure probability     : {r['scenarios'][0]['probability'] * 100:.1f}%{residual}",
    ]
    if r["implied_tail_alpha"] is not None:
        lo, hi = ALPHA_BAND
        out.append(f"  Implied tail alpha      : {r['implied_tail_alpha']:.2f}  (plausible band {lo}-{hi})")
    if r["breakeven_p_it_works"] is not None:
        be = r["breakeven_p_it_works"]
        be_s = f"{be * 100:.1f}%" if 0 <= be <= 1 else f"{be * 100:.0f}% (unreachable)"
        out.append(f"  Breakeven P(it-works)   : {be_s}  vs failure alone, at a {r['hurdle'] * 100:.0f}%/yr hurdle")
    for w in r["warnings"]:
        out.append(f"  WARNING: {w}")
    out += [
        "",
        f"  valuation.{METHOD}.roi  : {r['expected_annualized_roi']}",
        f"  valuation.{METHOD}.date : {as_of}",
    ]
    if doc_path is not None:
        out.append(f"  ({'written to ' + str(doc_path) if wrote else 'dry run — not written'})")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Entry points                                                                 #
# --------------------------------------------------------------------------- #
def run_doc_mode(args: argparse.Namespace) -> int:
    doc_path = tc.resolve_stock_doc(args.stock_doc, args.stock_dir)
    if not doc_path.exists():
        fail(f"stock-doc not found: {doc_path}")
    _, fm = tc.split_front_matter(doc_path.read_text(encoding="utf-8"))
    valuation = fm.get("valuation")
    if not isinstance(valuation, dict) or not isinstance(valuation.get(METHOD), dict):
        fail(f"stock-doc has no 'valuation.{METHOD}' input block. Add one under the "
             f"front matter (see the scenario-tam reference) and re-run.")
    kwargs = resolve_shared(valuation[METHOD], source=f"valuation.{METHOD}")
    result = compute(**kwargs, hurdle=tc.parse_rate(args.hurdle, "hurdle"))
    as_of = tc.resolve_as_of(args.as_of)

    wrote = not args.dry_run
    if wrote:
        write_outputs(doc_path, result["expected_annualized_roi"], as_of)

    if args.format == "json":
        print(json.dumps({**result, "date": as_of, "stock_doc": str(doc_path), "written": wrote}, indent=2))
    else:
        print(render_table(result, doc_path, wrote, as_of))
    return 0


def run_cli_mode(args: argparse.Namespace) -> int:
    missing = [f for f in ("price", "shares", "years") if getattr(args, f) is None]
    if missing:
        fail("raw mode needs --" + ", --".join(missing) + " (or pass --stock-doc instead)")
    if not args.scenario:
        fail("raw mode needs at least one --scenario 'name,key=value,...'")
    scenarios: dict[str, dict] = {}
    for spec in args.scenario:
        name, raw = parse_scenario_flag(spec)
        if name in scenarios:
            fail(f"--scenario {name}: given more than once")
        scenarios[name] = raw
    kwargs = resolve_shared(
        {"price": args.price, "shares": args.shares, "years": args.years,
         "tam": args.tam, "net-debt": args.net_debt, "scenarios": scenarios},
        source="arguments")
    result = compute(**kwargs, hurdle=tc.parse_rate(args.hurdle, "hurdle"))
    as_of = tc.resolve_as_of(args.as_of)
    print(json.dumps({**result, "date": as_of}, indent=2) if args.format == "json"
          else render_table(result, None, False, as_of))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Expected annualized ROI from probability-weighted TAM-capture scenarios (early-stage).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--stock-doc", help="Ticker (resolved in the stock dir) or path to a stock-doc .md. "
                                       "Reads valuation.scenario-tam inputs and writes valuation.scenario-tam.roi back.")
    p.add_argument("--stock-dir", type=tc.Path, default=tc.DEFAULT_STOCK_DIR)
    p.add_argument("--dry-run", action="store_true", help="Stock-doc mode: compute without writing back.")
    p.add_argument("--as-of", help="Valuation date stamped alongside roi (ISO YYYY-MM-DD). Default: today.")
    p.add_argument("--hurdle", default="10%", help="Required annual return for the breakeven P(it-works) output.")
    # Raw mode inputs (used only when --stock-doc is absent):
    p.add_argument("--price", type=float, help="Entry price per share (today).")
    p.add_argument("--shares", type=float, help="Today's diluted share count.")
    p.add_argument("--years", type=int, help="Holding period to maturity, whole years (shared).")
    p.add_argument("--tam", type=float, help="Base addressable-market revenue at now + years; a scenario "
                                             "may override it with its own tam=... key.")
    p.add_argument("--net-debt", type=float, default=0.0, help="Terminal net debt (negative = net cash).")
    p.add_argument("--scenario", action="append",
                   help="One scenario as 'name,key=value,...' — repeat per scenario. "
                        "Names: failure, niche-survivor, it-works, blue-sky.")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    return run_doc_mode(args) if args.stock_doc else run_cli_mode(args)


if __name__ == "__main__":
    raise SystemExit(main())
