#!/usr/bin/env python3
"""Compute a stock-doc's overall valuation-and-confidence-aware scores.

This sits one layer above the per-strategy scorer and the valuation methods. It
combines three numbers already in the stock-doc front matter — a strategy's
quality score `q`, that strategy's confidence `c`, and the chosen valuation's
annualized ROI — into two ranking scores, written under an `overall:` block:

    overall:
      qv_score:    <geometric mean of q and V>     # where to focus research
      cqv_score:   <geometric mean of c*q and V>    # where to allocate dollars
      agent_score: <unchanged>                      # agent-owned, never written here

VALUE FROM ROI. The ROI is mapped onto a 0..1 value scale by a linear reference:

    V = clamp(roi / 0.30, 0, 1)

So 0%/yr -> 0, 15%/yr -> 0.5, >=30%/yr -> 1. (A non-positive ROI gives V=0, which
zeroes both geometric means — an idea with no expected return is not an opportunity
to rank.)

THE TWO SCORES.
    qv_score  = sqrt( q * V )           quality x value; confidence-blind
    cqv_score = sqrt( (c*q) * V )       confidence-adjusted quality x value  ( = sqrt(c) * qv_score )

`qv_score` says how good the opportunity looks on the visible merits — use it to
prioritize *research* effort. `cqv_score` discounts that by how much we trust the
quality read (confidence multiplies q directly) — use it to prioritize *capital*.
Both use an equal-weight geometric mean, so a name has to be good on BOTH quality
and value; a near-zero on either sinks it (see references/overall-score.md).

SELECTING q, c AND roi. A doc may carry several scored strategies and several
valuation blocks, so we pick the canonical pairing the same way ranking does:

  * strategy (-> q, c from strategies.<strategy>):
        1. `chosen.strategy` if set and present in the map
        2. else argmax over strategies.<s>.score * confidence
  * valuation method (-> roi from valuation.<method>.roi):
        1. `chosen.valuation` if set and present
        2. else the chosen strategy's canonical method (STRATEGY_VALUATION_METHODS)
        3. else the sole method present under `valuation:`

If no strategy is scored, or no usable ROI is found, qv/cqv cannot be computed —
they are left out (any stale ones cleared) and a present `agent_score` is preserved.

AGENT_SCORE is the agent's valuation-aware judgement call (0..1), confidence-blind
like qv_score. It is agent-owned — this script never writes or alters it, only
carries an existing value through when it re-renders the block. A large persistent
gap between `agent_score` and `qv_score` is the signal to review the methodology.

Use --dry-run to compute without writing. Requires PyYAML. No secrets, no network.
"""
from __future__ import annotations

import argparse
import json
import re
from math import sqrt
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# ROI reference: the annualized ROI that maps to a full value score of 1.0.
ROI_FULL_VALUE = 0.30

# Each strategy's canonical valuation method — the roi that ranking reads. Kept
# tiny and explicit, mirroring stock_doc.py (rule-breakers' weighted-average is a
# meta-method whose blended roi is canonical).
STRATEGY_VALUATION_METHODS = {
    "freeroll": "asymmetric-payoff",
    "rule-breakers": "weighted-average",
    "wonderful-and-fair": "exit-multiple",
}


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(msg)


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def split_front_matter(text: str) -> tuple[str, dict[str, Any]]:
    m = FM_RE.match(text)
    if not m:
        fail("Document has no YAML front matter (must start with a '---' block).")
    block = m.group(1)
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as e:
        fail(f"Could not parse front matter as YAML: {e}")
    if not isinstance(data, dict):
        fail("Front matter must be a YAML mapping.")
    return block, data


def resolve_stock_doc(arg: str, stock_dir: Path) -> Path:
    p = Path(arg)
    if p.suffix == ".md" or "/" in arg:
        return p
    return stock_dir / f"{arg.strip().lstrip('$').upper()}.md"


def value_from_roi(roi: float) -> float:
    """Map an annualized ROI onto a 0..1 value score: V = clamp(roi / 0.30, 0, 1)."""
    return max(0.0, min(roi / ROI_FULL_VALUE, 1.0))


def select_strategy(doc_fm: dict[str, Any]) -> tuple[str | None, dict[str, Any]]:
    """Pick (strategy_name, entry) per the canonical rule: an explicit
    `chosen.strategy` wins, else argmax over score*confidence. Returns (None, {})
    if nothing is usable."""
    strategies = doc_fm.get("strategies")
    if not isinstance(strategies, dict) or not strategies:
        return None, {}

    chosen = doc_fm.get("chosen")
    if isinstance(chosen, dict):
        name = chosen.get("strategy")
        if isinstance(name, str) and isinstance(strategies.get(name), dict):
            return name, strategies[name]

    best_name, best_entry, best_metric = None, {}, -1.0
    for name, entry in strategies.items():
        if not isinstance(entry, dict):
            continue
        s = as_float(entry.get("score"))
        c = as_float(entry.get("confidence"))
        if s is None:
            continue
        metric = s * (c if c is not None else 1.0)
        if metric > best_metric:
            best_name, best_entry, best_metric = name, entry, metric
    return best_name, best_entry


def select_roi(doc_fm: dict[str, Any], strategy: str | None) -> float | None:
    """Pick the canonical roi: `chosen.valuation` -> the strategy's mapped method
    -> the sole method present. Returns None if no usable roi is found."""
    valuation = doc_fm.get("valuation")
    if not isinstance(valuation, dict) or not valuation:
        return None

    def roi_of(method: str | None) -> float | None:
        block = valuation.get(method) if method else None
        return as_float(block.get("roi")) if isinstance(block, dict) else None

    chosen = doc_fm.get("chosen")
    if isinstance(chosen, dict):
        roi = roi_of(chosen.get("valuation"))
        if roi is not None:
            return roi

    roi = roi_of(STRATEGY_VALUATION_METHODS.get(strategy or ""))
    if roi is not None:
        return roi

    if len(valuation) == 1:
        return roi_of(next(iter(valuation)))
    return None


def compute(doc_fm: dict[str, Any]) -> dict[str, Any]:
    """Resolve inputs and compute qv_score / cqv_score. Always returns a dict with
    the inputs used (for reporting) and the two scores when computable (else None)."""
    strategy, entry = select_strategy(doc_fm)
    q = as_float(entry.get("score")) if entry else None
    c = as_float(entry.get("confidence")) if entry else None
    roi = select_roi(doc_fm, strategy)

    result: dict[str, Any] = {
        "strategy": strategy, "q": q, "c": c, "roi": roi,
        "value": None, "qv_score": None, "cqv_score": None,
    }
    if q is None or roi is None:
        return result

    V = value_from_roi(roi)
    cq = q * (c if c is not None else 1.0)
    result["value"] = round(V, 4)
    result["qv_score"] = round(sqrt(q * V), 3)
    result["cqv_score"] = round(sqrt(cq * V), 3)
    return result


# --------------------------------------------------------------------------- #
# Write-back: the `overall:` block. qv_score/cqv_score are script-owned (computed
# or cleared); agent_score is agent-owned (carried through untouched).
# --------------------------------------------------------------------------- #


def remove_fm_key(block: str, key: str) -> str:
    pat = re.compile(rf"(?m)^{re.escape(key)}:.*(?:\n[ \t]+.*)*\n?")
    return pat.sub("", block)


def existing_agent_score(doc_fm: dict[str, Any]) -> float | None:
    overall = doc_fm.get("overall")
    return as_float(overall.get("agent_score")) if isinstance(overall, dict) else None


def render_overall(qv: float | None, cqv: float | None, agent: float | None) -> str | None:
    """Render the `overall:` block in the canonical key order, emitting only the
    keys that are present. Returns None when there is nothing to write."""
    lines = ["overall:"]
    if qv is not None:
        lines.append(f"  qv_score:    {qv}")
    if cqv is not None:
        lines.append(f"  cqv_score:   {cqv}")
    if agent is not None:
        lines.append(f"  agent_score: {agent}")
    return "\n".join(lines) if len(lines) > 1 else None


def write_overall(path: Path, qv: float | None, cqv: float | None, agent: float | None) -> None:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        fail(f"Cannot write back: {path} has no front-matter block.")
    block = remove_fm_key(m.group(1), "overall")
    rendered = render_overall(qv, cqv, agent)
    if rendered is not None:
        block = block.rstrip("\n") + "\n" + rendered
    new_text = f"---\n{block.rstrip(chr(10))}\n---\n" + text[m.end():]
    path.write_text(new_text, encoding="utf-8")


def render_table(res: dict[str, Any], doc_path: Path, agent: float | None, wrote: bool) -> str:
    out = [f"{doc_path.stem}  —  overall scores", "=" * 40, ""]
    strat = res["strategy"] or "(none scored)"
    q = "—" if res["q"] is None else f"{res['q']:.3f}"
    c = "—" if res["c"] is None else f"{res['c']:.3f}"
    roi = "—" if res["roi"] is None else f"{res['roi'] * 100:.2f}%/yr"
    val = "—" if res["value"] is None else f"{res['value']:.3f}"
    out.append(f"strategy : {strat}")
    out.append(f"q (score): {q}     c (confidence): {c}")
    out.append(f"roi      : {roi}     V = clamp(roi/0.30): {val}")
    out.append("")
    if res["qv_score"] is None:
        why = "no strategy scored" if res["q"] is None else "no usable ROI"
        out.append(f"qv_score / cqv_score : not computable ({why})")
    else:
        out.append(f"qv_score  : {res['qv_score']:.3f}   (sqrt(q·V) — where to research)")
        out.append(f"cqv_score : {res['cqv_score']:.3f}   (sqrt(c·q·V) — where to allocate $)")
    out.append(f"agent_score: {'—' if agent is None else f'{agent:.3f}'}   (agent-owned; preserved)")
    out.append("")
    out.append(f"({'written to ' + str(doc_path) if wrote else 'dry run — not written'})")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Compute a stock-doc's overall qv_score and cqv_score from its strategy score, "
                    "confidence, and chosen-valuation ROI.",
        epilog="Example: overall_score.py SDR.AX",
    )
    p.add_argument("stock_doc", metavar="STOCK-DOC",
                   help="Ticker (resolved in the stock dir) or path to a stock-doc .md")
    p.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    p.add_argument("--dry-run", action="store_true", help="Compute and print without writing back.")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    doc_path = resolve_stock_doc(args.stock_doc, args.stock_dir)
    if not doc_path.exists():
        fail(f"Stock-doc not found: {doc_path}")
    _, doc_fm = split_front_matter(doc_path.read_text(encoding="utf-8"))

    res = compute(doc_fm)
    agent = existing_agent_score(doc_fm)
    wrote = not args.dry_run
    if wrote:
        write_overall(doc_path, res["qv_score"], res["cqv_score"], agent)

    if args.format == "json":
        print(json.dumps({**res, "agent_score": agent, "stock_doc": str(doc_path),
                          "written": wrote}, indent=2))
    else:
        print(render_table(res, doc_path, agent, wrote))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
