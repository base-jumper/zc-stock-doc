#!/usr/bin/env python3
"""Compute a strategy's overall company score from per-trait scores.

This script is agnostic to what the traits mean. It reads two documents:

  * a STRATEGY doc — its front matter lists the traits the strategy uses, each
    with a `floor`, plus a `strategy` name that also prefixes where results are
    written; and
  * a STOCK-DOC — its front matter holds, per trait, a `score` and `confidence`
    in [0, 1].

For each trait the strategy requires, the value is mapped into [floor, 1] via the
floor transform, then the transformed terms are combined with a geometric mean:

    term_i  = floor_i + (1 - floor_i) * value_i
    overall = ( prod_{i=1..n} term_i ) ^ (1/n)

Floors encode trait importance (LOWER floor = MORE important):
  * floor 0    -> the trait can veto: a 0 forces the aggregate to 0 (make-or-break)
  * floor ~1   -> the trait barely moves the result

Score and confidence are two separate axes (confidence never alters the score),
but both run through the same formula and floors, so the combined confidence is
importance-weighted exactly like the score.

Both aggregates are then NORMALIZED — converted back onto a comparable [0, 1]
underlying trait-quality scale: the uniform trait value q that would reproduce
the floor-adjusted aggregate under this strategy's floors. Only the normalized
values are written back, into the stock-doc front matter under a per-strategy
`strategies:` map (several strategies can coexist, one entry each):

    strategies:
      <strategy>:
        score:      <normalized score>
        confidence: <normalized confidence>

ELIGIBILITY GATE. Disqualification is a property of the COMPANY, not a strategy:
a single top-level `disqualified: true` in the stock-doc marks it INELIGIBLE for
every strategy — all strategies are skipped (no scores written, any stale scores
cleared) and the leaderboard is empty. The flag is agent-owned: this script never
sets it, only reads it to decide whether to score. The `strategies:` map is
script-owned (score/confidence only).

The raw floor-adjusted aggregates are shown in the run output but not stored.
Use --dry-run to compute without writing.

Strategy front matter (example):

    ---
    strategy: rule-breakers
    traits:
      - {id: right-place-and-time, floor: 0.00}
      - {id: top-dog,              floor: 0.15}
    ---

Stock-doc front matter (example):

    ---
    ticker: NVDA
    traits:
      right-place-and-time: {score: 0.9, confidence: 0.8}
      top-dog:              {score: 0.9, confidence: 0.9}
    ---

Requires PyYAML. No secrets, no network.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from math import exp, log
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"
DEFAULT_STRATEGY_DIR = Path(__file__).resolve().parent.parent / "references" / "strategies"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# Near-tie margin on the score×confidence metric. When the leader is proven but a
# runner-up's optimistic bound sits within this of it, the margin is unknown and
# the runner-up should be resolved before crowning (see --leaderboard verdict).
EPSILON = 0.05


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(msg)


def coerce_unit(value: Any, label: str) -> float:
    """Coerce a value to a float in [0, 1], raising on anything outside."""
    try:
        num = float(value)
    except (TypeError, ValueError):
        fail(f"{label}: expected a number in [0, 1], got {value!r}")
    if not 0.0 <= num <= 1.0:
        fail(f"{label}: must be in [0, 1], got {num}")
    return num


def split_front_matter(text: str) -> tuple[str, dict[str, Any]]:
    """Return (front_matter_block_text, parsed_dict). Raises if absent/invalid."""
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


def load_strategy(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"Strategy doc not found: {path}")
    _, fm = split_front_matter(path.read_text(encoding="utf-8"))
    prefix = fm.get("strategy")
    if not isinstance(prefix, str) or not prefix.strip():
        fail("Strategy front matter must define a non-empty 'strategy'.")
    raw_traits = fm.get("traits")
    if not isinstance(raw_traits, list) or not raw_traits:
        fail("Strategy front matter must define a non-empty 'traits' list.")
    traits: list[tuple[str, float]] = []
    seen: set[str] = set()
    for i, entry in enumerate(raw_traits):
        if not isinstance(entry, dict) or "id" not in entry or "floor" not in entry:
            fail(f"Strategy trait #{i + 1} must be a mapping with 'id' and 'floor'.")
        tid = str(entry["id"])
        if tid in seen:
            fail(f"Strategy lists trait {tid!r} more than once.")
        seen.add(tid)
        traits.append((tid, coerce_unit(entry["floor"], f"floor for {tid}")))
    return {"prefix": prefix.strip(), "name": fm.get("name", fm.get("strategy")), "traits": traits}


def resolve_stock_doc(arg: str, stock_dir: Path) -> Path:
    p = Path(arg)
    if p.suffix == ".md" or "/" in arg:
        return p
    return stock_dir / f"{arg.strip().lstrip('$').upper()}.md"


def resolve_strategy(arg: str, strategy_dir: Path) -> Path:
    p = Path(arg)
    if p.suffix == ".md" or "/" in arg:
        return p
    return strategy_dir / f"{arg.strip()}.md"


def geometric_mean(values: list[float]) -> float:
    if not values:
        return 0.0
    if any(v <= 0.0 for v in values):
        return 0.0
    return exp(sum(log(v) for v in values) / len(values))


def equivalent_uniform(floors: list[float], target: float) -> float:
    """Return q where GM(floor_i + (1-floor_i) * q) == target.

    This converts a strategy-specific floor-adjusted aggregate (a score OR a
    confidence aggregate — the machinery is identical) back onto a comparable
    [0, 1] underlying trait-quality scale. It preserves the strategy's floor
    structure but removes the visual uplift/compression caused by floors.
    """
    if not floors:
        return 0.0
    if all(f == 1.0 for f in floors):
        # Degenerate strategy: every term is always 1, so q is not identifiable.
        # Return 1 because the observed aggregate can only be 1.
        return 1.0

    def aggregate(q: float) -> float:
        return geometric_mean([f + (1.0 - f) * q for f in floors])

    lo, hi = 0.0, 1.0
    floor_min = aggregate(lo)
    if target <= floor_min:
        return 0.0
    if target >= 1.0:
        return 1.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if aggregate(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def score(strategy: dict[str, Any], doc_fm: dict[str, Any]) -> dict[str, Any]:
    traits_in = doc_fm.get("traits")
    if not isinstance(traits_in, dict):
        fail("Stock-doc front matter must contain a 'traits' mapping.")

    rows: list[dict[str, Any]] = []
    score_terms: list[float] = []
    conf_terms: list[float] = []
    floors: list[float] = []
    missing: list[str] = []

    for tid, floor in strategy["traits"]:
        entry = traits_in.get(tid)
        if entry is None:
            missing.append(tid)
            continue
        if not isinstance(entry, dict) or "score" not in entry:
            fail(f"Trait {tid!r} must be a mapping with at least a 'score'.")
        s = coerce_unit(entry["score"], f"{tid} score")
        c = coerce_unit(entry.get("confidence", 0.0), f"{tid} confidence")
        score_terms.append(floor + (1.0 - floor) * s)
        conf_terms.append(floor + (1.0 - floor) * c)
        floors.append(floor)
        rows.append({"trait": tid, "score": round(s, 4), "confidence": round(c, 4), "floor": round(floor, 4)})

    if missing:
        fail(
            f"Stock-doc is missing trait(s) required by strategy {strategy['name']!r}: "
            f"{', '.join(missing)}.\nScore every required trait (use a low score with low "
            "confidence if there's no evidence)."
        )

    overall_score = geometric_mean(score_terms)
    combined_confidence = geometric_mean(conf_terms)
    return {
        "strategy": strategy["name"],
        "prefix": strategy["prefix"],
        "overall_score": round(overall_score, 4),
        "combined_confidence": round(combined_confidence, 4),
        "normalized_score": round(equivalent_uniform(floors, overall_score), 4),
        "normalized_confidence": round(equivalent_uniform(floors, combined_confidence), 4),
        "traits": rows,
    }


def missing_traits(strategy: dict[str, Any], traits_in: Any) -> list[str]:
    """Trait ids the strategy requires that are absent from the stock-doc."""
    if not isinstance(traits_in, dict):
        return [tid for tid, _ in strategy["traits"]]
    return [tid for tid, _ in strategy["traits"] if traits_in.get(tid) is None]


# --------------------------------------------------------------------------- #
# Leaderboard mode: optimistic, non-writing, all strategies at once.
#
# Every trait NOT present in the stock-doc's `traits:` map is assumed perfect
# ({score: 1, confidence: 1}). Because each term is monotonic in its value, this
# makes every strategy's normalized score and confidence — and therefore their
# product, the ranking metric — an OPTIMISTIC UPPER BOUND on the strategy's true
# result, descending toward the truth as traits are evaluated. A strategy that
# leads (highest metric) once it is FULLY evaluated is the proven winner: its
# true metric is >= every other strategy's bound, hence >= their true metrics.
# This is the stopping rule the verdict encodes. Nothing is written back.
# --------------------------------------------------------------------------- #


def load_all_strategies(strategy_dir: Path) -> list[dict[str, Any]]:
    paths = sorted(strategy_dir.glob("*.md"))
    if not paths:
        fail(f"No strategy docs found in {strategy_dir}")
    return [load_strategy(p) for p in paths]


def eval_optimistic(strategy: dict[str, Any], traits_in: dict[str, Any]) -> dict[str, Any]:
    """Score one strategy, treating any trait absent from the doc as {1, 1}."""
    score_terms: list[float] = []
    conf_terms: list[float] = []
    floors: list[float] = []
    evaluated: list[str] = []
    unevaluated: list[dict[str, Any]] = []

    for tid, floor in strategy["traits"]:
        entry = traits_in.get(tid) if isinstance(traits_in, dict) else None
        if entry is None:
            s, c = 1.0, 1.0
            unevaluated.append({"trait": tid, "floor": round(floor, 4)})
        else:
            if not isinstance(entry, dict) or "score" not in entry:
                fail(f"Trait {tid!r} must be a mapping with at least a 'score'.")
            s = coerce_unit(entry["score"], f"{tid} score")
            c = coerce_unit(entry.get("confidence", 0.0), f"{tid} confidence")
            evaluated.append(tid)
        score_terms.append(floor + (1.0 - floor) * s)
        conf_terms.append(floor + (1.0 - floor) * c)
        floors.append(floor)

    ns = round(equivalent_uniform(floors, geometric_mean(score_terms)), 4)
    nc = round(equivalent_uniform(floors, geometric_mean(conf_terms)), 4)
    return {
        "strategy": strategy["name"],
        "prefix": strategy["prefix"],
        "score": ns,
        "confidence": nc,
        "metric": round(ns * nc, 4),
        "evaluated": len(evaluated),
        "total": len(strategy["traits"]),
        "complete": not unevaluated,
        "unevaluated": sorted(unevaluated, key=lambda u: (u["floor"], u["trait"])),
    }


def compute_verdict(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply the branch-and-bound stopping rule to ranked rows (metric desc)."""
    leader = rows[0]
    runner = rows[1] if len(rows) > 1 else None

    if not leader["complete"]:
        nxt = leader["unevaluated"][0]
        return {
            "decided": False,
            "reason": (f"leader {leader['prefix']} still has "
                       f"{leader['total'] - leader['evaluated']} optimistic trait(s); its lead "
                       "may not survive evaluation"),
            "next": {"strategy": leader["prefix"], "trait": nxt["trait"], "floor": nxt["floor"]},
        }

    # Leader is fully evaluated -> its true metric >= every other bound -> winner.
    verdict: dict[str, Any] = {"decided": True, "winner": leader["prefix"], "metric": leader["metric"]}
    if runner is not None and (leader["metric"] - runner["metric"]) < EPSILON:
        if runner["complete"]:
            verdict["near_tie"] = True
            verdict["note"] = (
                f"genuine near-tie: {runner['prefix']} scores {runner['metric']} vs "
                f"{leader['metric']} (within {EPSILON}) — write up as a dual-fit")
        else:
            nxt = runner["unevaluated"][0]
            verdict["provisional"] = True
            verdict["note"] = (
                f"winner holds, but runner-up {runner['prefix']} bound {runner['metric']} is within "
                f"{EPSILON} and still optimistic — resolve it to confirm a clear win vs a dual-fit")
            verdict["next"] = {"strategy": runner["prefix"], "trait": nxt["trait"], "floor": nxt["floor"]}
    return verdict


def build_leaderboard(strategies: list[dict[str, Any]], doc_fm: dict[str, Any]) -> dict[str, Any]:
    if doc_disqualified(doc_fm):
        return {"rows": [], "verdict": {"decided": False,
                "reason": "company is disqualified — ineligible for all strategies"}}
    traits_in = doc_fm.get("traits")
    traits_in = traits_in if isinstance(traits_in, dict) else {}
    rows = [eval_optimistic(s, traits_in) for s in strategies]
    rows.sort(key=lambda r: (-r["metric"], r["prefix"]))  # metric desc, deterministic tie-break
    verdict = compute_verdict(rows)
    return {"rows": rows, "verdict": verdict}


def render_leaderboard(board: dict[str, Any], doc_path: Path) -> str:
    rows, verdict = board["rows"], board["verdict"]
    out = [f"LEADERBOARD  —  {doc_path.stem}", "=" * 60, ""]
    if not rows:
        out.append(f"VERDICT: not decided — {verdict['reason']}")
        return "\n".join(out)
    out.append(f"{'#':>2}  {'Strategy':<22}{'Score':>8}{'Conf':>8}{'S×C':>8}{'Eval':>8}  Status")
    out.append("-" * 64)
    for i, r in enumerate(rows, 1):
        opt = "*" if not r["complete"] else ""
        status = "COMPLETE" if r["complete"] else "optimistic"
        sc = f"{r['score']:.2f}{opt}"
        cf = f"{r['confidence']:.2f}{opt}"
        mt = f"{r['metric']:.2f}{opt}"
        ev = f"{r['evaluated']}/{r['total']}"
        out.append(f"{i:>2}  {r['prefix']:<22}{sc:>8}{cf:>8}{mt:>8}{ev:>8}  {status}")
    out.append("-" * 64)
    out.append("* optimistic bound — unevaluated traits assumed {score: 1, confidence: 1}")
    out.append("")

    if verdict["decided"]:
        out.append(f"VERDICT: DECIDED — winner: {verdict['winner']}  (S×C {verdict['metric']})")
        if verdict.get("note"):
            out.append(f"  ⚠ {verdict['note']}")
    else:
        out.append(f"VERDICT: not decided — {verdict['reason']}")
    nxt = verdict.get("next")
    if nxt:
        out.append(f"  → highest-leverage next: evaluate {nxt['strategy']} → "
                   f"{nxt['trait']} (floor {nxt['floor']})")
    out.append("")

    pending = [r for r in rows if not r["complete"]]
    if pending:
        out.append("Unevaluated traits (floor ascending — lower floor = higher leverage):")
        for r in pending:
            items = ", ".join(f"{u['trait']}({u['floor']})" for u in r["unevaluated"])
            out.append(f"  {r['prefix']}: {items}")
    return "\n".join(out)


def remove_fm_key(block: str, key: str) -> str:
    """Remove a top-level `key:` from a front-matter block, including any indented
    children if it is a block mapping (so `strategies:` and its nested entries go
    together). Leaves everything else untouched."""
    pat = re.compile(rf"(?m)^{re.escape(key)}:.*(?:\n[ \t]+.*)*\n?")
    return pat.sub("", block)


def render_strategies(strategies: dict[str, dict[str, Any]]) -> str:
    """Render the `strategies:` block (sorted by strategy name). Each entry carries
    a script-owned score+confidence pair; emit whichever keys are present."""
    lines = ["strategies:"]
    for name in sorted(strategies):
        entry = strategies[name]
        lines.append(f"  {name}:")
        if "score" in entry:
            lines.append(f"    score:      {entry['score']}")
        if "confidence" in entry:
            lines.append(f"    confidence: {entry['confidence']}")
    return "\n".join(lines)


def existing_strategies(doc_fm: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Deep-ish copy of the doc's current `strategies:` map (entries copied so we
    can rebuild without mutating the parsed front matter)."""
    raw = doc_fm.get("strategies")
    if not isinstance(raw, dict):
        return {}
    return {k: (dict(v) if isinstance(v, dict) else {}) for k, v in raw.items()}


def doc_disqualified(doc_fm: dict[str, Any]) -> bool:
    """Company-level eligibility gate: a top-level `disqualified: true` marks the
    stock ineligible for every strategy (see disqualifiers.md)."""
    return doc_fm.get("disqualified") is True


def scored_entry(result: dict[str, Any]) -> dict[str, Any]:
    """Build a strategy entry (script-owned score+confidence pair) from a result."""
    return {"score": result["normalized_score"], "confidence": result["normalized_confidence"]}


def write_strategies(path: Path, strategies: dict[str, dict[str, Any]]) -> None:
    """Replace the `strategies:` block with the given map, leaving the rest of the
    front matter untouched. An empty map removes the block entirely (used to clear
    scores when the company is disqualified). The caller owns merge/preservation
    policy; this just re-renders the whole block."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        fail(f"Cannot write back: {path} has no front-matter block.")
    block = m.group(1)

    # Drop the block (re-rendered below) and any legacy flat keys for these strategies.
    block = remove_fm_key(block, "strategies")
    block = remove_fm_key(block, "normalized-score")
    for prefix in strategies:
        block = remove_fm_key(block, f"{prefix}-score")
        block = remove_fm_key(block, f"{prefix}-confidence")

    if strategies:
        block = block.rstrip("\n") + "\n" + render_strategies(strategies)
    new_text = f"---\n{block.rstrip(chr(10))}\n---\n" + text[m.end():]
    path.write_text(new_text, encoding="utf-8")


def render_table(result: dict[str, Any], doc_path: Path, wrote: bool) -> str:
    lines = [f"{doc_path.stem}  —  strategy: {result['strategy']}", "=" * 48, ""]
    lines.append(f"{'Trait':<30}{'Score':>7}{'Conf':>7}{'Floor':>7}")
    lines.append("-" * 51)
    for r in result["traits"]:
        lines.append(f"{r['trait']:<30}{r['score']:>7.2f}{r['confidence']:>7.2f}{r['floor']:>7.2f}")
    lines.append("-" * 51)
    lines.append("")
    lines.append(f"strategies.{result['prefix']}.score      : {result['normalized_score']:.3f}   (normalized; written)")
    lines.append(f"strategies.{result['prefix']}.confidence : {result['normalized_confidence']:.3f}   (normalized; written)")
    lines.append("")
    lines.append(f"raw floor-adjusted aggregate  score: {result['overall_score']:.3f}  confidence: {result['combined_confidence']:.3f}  (not stored)")
    lines.append("")
    lines.append(f"({'written to ' + str(doc_path) if wrote else 'dry run — not written'})")
    return "\n".join(lines)


def commit_all(strategies: list[dict[str, Any]], doc_fm: dict[str, Any], doc_path: Path,
               dry_run: bool) -> dict[str, Any]:
    """Score and write back every strategy whose trait set is complete; skip (don't
    fail on) the rest. If the company is disqualified, no strategy is scored and any
    stale `strategies:` block is cleared. One write."""
    traits_in = doc_fm.get("traits")
    original = existing_strategies(doc_fm)

    if doc_disqualified(doc_fm):
        changed = original != {}
        if changed and not dry_run:
            write_strategies(doc_path, {})  # clear all scores — ineligible
        return {"scored": [], "skipped": [], "disqualified": True, "changed": changed}

    final = existing_strategies(doc_fm)
    scored: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for s in strategies:
        prefix = s["prefix"]
        miss = missing_traits(s, traits_in)
        if miss:
            skipped.append({"strategy": s["name"], "prefix": prefix, "missing": miss})
            continue  # leave any existing entry untouched
        res = score(s, doc_fm)
        final[prefix] = scored_entry(res)
        scored.append(res)
    changed = final != original
    if changed and not dry_run:
        write_strategies(doc_path, final)
    return {"scored": scored, "skipped": skipped, "disqualified": False, "changed": changed}


def render_commit_summary(summary: dict[str, Any], doc_path: Path, dry_run: bool) -> str:
    out = [f"{doc_path.stem}  —  scoring complete strategies", "=" * 52, ""]
    if summary.get("disqualified"):
        out.append("  DISQUALIFIED — company ineligible for all strategies; no scores written.")
        out.append("")
        if summary.get("changed"):
            verb = "would clear" if dry_run else "cleared"
            out.append(f"{verb} stale strategy scores in {'(dry run)' if dry_run else doc_path}")
        else:
            out.append("Nothing to clear — no strategy scores were present.")
        return "\n".join(out)
    for r in summary["scored"]:
        out.append(f"  {r['prefix']:<22} score {r['normalized_score']:.3f}   "
                   f"confidence {r['normalized_confidence']:.3f}")
    for sk in summary["skipped"]:
        out.append(f"  {sk['prefix']:<22} skipped — missing: {', '.join(sk['missing'])}")
    out.append("")
    n = len(summary["scored"])
    if not summary.get("changed"):
        out.append("Nothing to write — no complete strategy produced a new result. "
                   "Run --leaderboard to see what to evaluate next.")
    else:
        verb = "would write" if dry_run else "wrote"
        out.append(f"{verb} {n} strateg{'y' if n == 1 else 'ies'} to "
                   f"{'(dry run)' if dry_run else doc_path}")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Score a stock-doc against the strategies' traits and floors.",
        epilog="Examples: company_score.py NVDA  |  company_score.py NVDA --only rule-breakers",
    )
    p.add_argument("stock_doc", metavar="STOCK-DOC",
                   help="Ticker (resolved in the stock dir) or path to a stock-doc .md")
    p.add_argument("--only", metavar="STRATEGY",
                   help="Score just this one strategy (name or path), and fail if its trait set is "
                        "incomplete. Default (omit) scores every strategy with a complete trait set.")
    p.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    p.add_argument("--strategy-dir", type=Path, default=DEFAULT_STRATEGY_DIR)
    p.add_argument("--leaderboard", action="store_true",
                   help="Advisory mode: score ALL strategies optimistically (unevaluated traits "
                        "assumed perfect) and print the ranking + winner verdict. Never writes.")
    p.add_argument("--dry-run", action="store_true", help="Compute and print without writing back.")
    p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args()

    doc_path = resolve_stock_doc(args.stock_doc, args.stock_dir)
    if not doc_path.exists():
        fail(f"Stock-doc not found: {doc_path}")
    _, doc_fm = split_front_matter(doc_path.read_text(encoding="utf-8"))

    if args.leaderboard:
        board = build_leaderboard(load_all_strategies(args.strategy_dir), doc_fm)
        if args.format == "json":
            print(json.dumps({**board, "stock_doc": str(doc_path)}, indent=2))
        else:
            print(render_leaderboard(board, doc_path))
        return 0

    wrote = not args.dry_run

    # --only: score exactly one strategy, strictly (fail on missing traits).
    if args.only:
        strategy = load_strategy(resolve_strategy(args.only, args.strategy_dir))
        prefix = strategy["prefix"]
        if doc_disqualified(doc_fm):
            fail(f"{doc_path.name} is marked disqualified; not scoring. "
                 "Clear the top-level disqualified flag to score it.")
        final = existing_strategies(doc_fm)
        result = score(strategy, doc_fm)
        if wrote:
            final[prefix] = scored_entry(result)
            write_strategies(doc_path, final)
        if args.format == "json":
            print(json.dumps({**result, "stock_doc": str(doc_path), "written": wrote}, indent=2))
        else:
            print(render_table(result, doc_path, wrote))
        return 0

    # Default: score every strategy that has a complete trait set; skip the rest.
    summary = commit_all(load_all_strategies(args.strategy_dir), doc_fm, doc_path, args.dry_run)
    if args.format == "json":
        print(json.dumps({**summary, "stock_doc": str(doc_path), "written": wrote}, indent=2))
    else:
        print(render_commit_summary(summary, doc_path, args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
