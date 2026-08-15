#!/usr/bin/env python3
"""Blend several valuation methods' ROIs into one expected annualized ROI.

`weighted-average` is a META-method: it does not value a company from scratch, it
combines the ROIs that the other methods have already written to the stock-doc. A
strategy whose thesis admits more than one valuation lens (e.g. rule-breakers, where
a profitless disruptor is valued top-down by tam-capture while a now-profitable one
can also be anchored bottom-up by exit-multiple) names this method; the components it
blends are listed as the keys of its `weights` map.

  blended_roi = Σ_i ( w_i / Σ w ) * valuation.<method_i>.roi

The component ROIs are read IN PLACE from their own front-matter blocks
(valuation.exit-multiple.roi, valuation.tam-capture.roi, …) — this method never
copies or restates them, so there is a single source of truth for each. Only the
methods the analyst judged applicable to this company appear in `weights`; an
inapplicable method is simply absent (its weight is not "zero", it is omitted).

Weights are RELATIVE and need not sum to 1 — the script normalizes them. Assign them
by how applicable each method is and how reliable its data is (this is, in effect,
inverse-variance weighting: trust the better-supported estimate more). Do NOT weight
toward whichever answer is more conservative.

The spread between the component ROIs is reported but NOT stored: wide divergence
means the methods disagree about the company's future and the blend is hiding model
risk, so it should pull the strategy's CONFIDENCE down; tight agreement supports it.
The headline is the point estimate; the spread is the honesty.

============================================================================
Two ways to run it
============================================================================

This is the valuation counterpart of company_score.py and shares its interface.

  * STOCK-DOC mode (the integrated flow). Run it AFTER the component methods, so
    their `roi` fields are populated:

        weighted_average_valuation.py --stock-doc NET

    It reads `valuation.weighted-average.weights`, pulls each listed method's `roi`
    from its sibling block, and writes the blended ROI back as
    `valuation.weighted-average.roi` (plus the run `date`). Surgical — only those
    lines are touched.

    Stock-doc front matter (example):

        ---
        ticker: NET
        valuation:
          exit-multiple:
            ...
            roi: 0.082            # written earlier by exit_multiple_valuation.py
          tam-capture:
            ...
            roi: 0.251            # written earlier by tam_capture_valuation.py
          weighted-average:
            weights: {exit-multiple: 0.4, tam-capture: 0.6}   # keys = methods to blend
            roi: 0.0              # written by this script
            date: 2026-06-24      # written by this script
        ---

  * RAW mode (ad-hoc sanity check, no doc). Pass the components as name:roi:weight:

        weighted_average_valuation.py \
            --component exit-multiple:0.082:0.4 \
            --component tam-capture:0.251:0.6

Component ROIs accept a trailing '%' ("8.2%" == 0.082) or a plain decimal.

Requires PyYAML for stock-doc mode. No secrets, no network.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

METHOD = "weighted-average"  # front-matter block key, output prefix, and method id
WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"error: {msg}")


# --------------------------------------------------------------------------- #
# Parsing                                                                      #
# --------------------------------------------------------------------------- #
def parse_rate(s: Any, label: str) -> float:
    """Parse a rate: '8.2%' -> 0.082, '0.082' -> 0.082, 0.082 -> 0.082."""
    s = str(s).strip()
    try:
        return float(s[:-1]) / 100.0 if s.endswith("%") else float(s)
    except ValueError:
        fail(f"{label}: could not parse {s!r} as a rate (use e.g. 0.082 or 8.2%)")


def require_weight(value: Any, label: str) -> float:
    try:
        w = float(str(value).strip())
    except (TypeError, ValueError):
        fail(f"{label}: weight must be a number, got {value!r}")
    if w < 0:
        fail(f"{label}: weight must be non-negative, got {w}")
    return w


# --------------------------------------------------------------------------- #
# The model                                                                    #
# --------------------------------------------------------------------------- #
def compute(components: list[tuple[str, float, float]]) -> dict[str, Any]:
    """components: list of (method_id, roi, weight). Weights are normalized here."""
    if not components:
        fail("no components to blend (weights map is empty)")
    total_w = sum(w for _, _, w in components)
    if total_w <= 0:
        fail("weights sum to zero — at least one must be positive")

    parts = []
    blended = 0.0
    for method, roi, w in components:
        nw = w / total_w
        contribution = nw * roi
        blended += contribution
        parts.append({
            "method": method,
            "roi": round(roi, 6),
            "weight": round(nw, 6),
            "contribution": round(contribution, 6),
        })

    rois = [roi for _, roi, _ in components]
    spread = max(rois) - min(rois)
    return {
        "annualized_roi": round(blended, 6),
        "components": parts,
        "roi_min": round(min(rois), 6),
        "roi_max": round(max(rois), 6),
        "roi_spread": round(spread, 6),
    }


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


def collect_components(valuation: dict[str, Any]) -> list[tuple[str, float, float]]:
    """Read the weights map, then pull each listed method's roi from its sibling
    block. Fails loudly if a component has not been computed yet — run it first."""
    block = valuation.get(METHOD)
    if not isinstance(block, dict):
        fail(f"stock-doc has no 'valuation.{METHOD}' block. Add one with a 'weights' map.")
    weights = block.get("weights")
    if not isinstance(weights, dict) or not weights:
        fail(f"valuation.{METHOD}.weights must be a non-empty mapping of method: weight.")

    components: list[tuple[str, float, float]] = []
    for method, weight in weights.items():
        method = str(method).strip()
        if method == METHOD:
            fail(f"valuation.{METHOD}.weights cannot include {METHOD} itself (circular).")
        w = require_weight(weight, f"weights.{method}")
        sibling = valuation.get(method)
        if not isinstance(sibling, dict):
            fail(f"weights lists {method!r} but there is no 'valuation.{method}' block — "
                 f"run that method first, or remove it from weights.")
        roi = sibling.get("roi")
        if roi in (None, ""):
            fail(f"valuation.{method}.roi is not set — run the {method} method first "
                 f"(weighted-average blends already-computed ROIs).")
        components.append((method, parse_rate(roi, f"valuation.{method}.roi"), w))
    return components


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
    """Stamp the blended `roi` and valuation `date` into the method block."""
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
    head = doc_path.stem if doc_path else "weighted-average valuation"
    out = [
        f"{head}  —  blended expected ROI  as of {as_of}",
        "=" * 56,
        "",
        "  Components (weight x roi)",
        "  " + "-" * 44,
    ]
    for c in r["components"]:
        out.append(
            f"    {c['method']:<18} {c['weight'] * 100:5.1f}%  x  {pct(c['roi'])}"
            f"  =  {pct(c['contribution'])}"
        )
    out += [
        "  " + "-" * 44,
        f"    BLENDED ROI       {pct(r['annualized_roi'])}  / yr",
        "",
        f"  Component spread  : {pct(r['roi_min'])} … {pct(r['roi_max'])}"
        f"   (range {r['roi_spread'] * 100:.2f} pts)",
        "  (wide spread = methods disagree → lower the strategy's confidence)",
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
    if not isinstance(valuation, dict):
        fail("stock-doc front matter has no 'valuation:' block.")
    components = collect_components(valuation)
    result = compute(components)
    as_of = resolve_as_of(args.as_of)

    wrote = not args.dry_run
    if wrote:
        write_outputs(doc_path, result["annualized_roi"], as_of)

    if args.format == "json":
        print(json.dumps({**result, "date": as_of, "stock_doc": str(doc_path), "written": wrote}, indent=2))
    else:
        print(render_table(result, doc_path, wrote, as_of))
    return 0


def parse_component_arg(s: str) -> tuple[str, float, float]:
    parts = s.split(":")
    if len(parts) != 3:
        fail(f"--component expects name:roi:weight, got {s!r}")
    name, roi, weight = parts
    if not name.strip():
        fail(f"--component has an empty method name in {s!r}")
    return name.strip(), parse_rate(roi, f"component {name} roi"), require_weight(weight, f"component {name} weight")


def run_cli_mode(args: argparse.Namespace) -> int:
    if not args.component:
        fail("raw mode needs at least one --component name:roi:weight (or pass --stock-doc)")
    components = [parse_component_arg(c) for c in args.component]
    names = [c[0] for c in components]
    if len(names) != len(set(names)):
        fail("duplicate method name across --component arguments")
    result = compute(components)
    as_of = resolve_as_of(args.as_of)
    print(json.dumps({**result, "date": as_of}, indent=2) if args.format == "json"
          else render_table(result, None, False, as_of))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Blend component valuation methods' ROIs into one weighted-average ROI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--stock-doc", help="Ticker (resolved in the stock dir) or path to a stock-doc .md. "
                                       "Reads valuation.weighted-average.weights + sibling rois, writes the blend back.")
    p.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    p.add_argument("--dry-run", action="store_true", help="Stock-doc mode: compute without writing back.")
    p.add_argument("--as-of", help="Valuation date stamped alongside roi (ISO YYYY-MM-DD). Default: today.")
    # Raw mode inputs (used only when --stock-doc is absent):
    p.add_argument("--component", action="append", metavar="NAME:ROI:WEIGHT",
                   help="A component to blend, e.g. exit-multiple:0.082:0.4. Repeatable.")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    return run_doc_mode(args) if args.stock_doc else run_cli_mode(args)


if __name__ == "__main__":
    raise SystemExit(main())
