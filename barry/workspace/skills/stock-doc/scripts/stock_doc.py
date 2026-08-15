#!/usr/bin/env python3
"""Deterministic helpers for Nick's stock-doc markdown files.

Commands:
  show TICKER
  rank [N]
  latest [N]
  watch
  focus [N] [--today YYYY-MM-DD] [--tau DAYS] [--wq W] [--wc W] [--ws W]
  list-strategy STRATEGY
  frontmatter [TICKER]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"

# Keep this tiny and explicit. These are the stock-analysis strategies currently
# supported by Nick's workflow; each strategy writes its predicted annualized ROI
# to valuation.<method>.roi in stock-doc front matter. For a strategy whose method is
# a blend, this is the meta-method (weighted-average), whose roi is the canonical one.
STRATEGY_VALUATION_METHODS = {
    "freeroll": "asymmetric-payoff",
    "rule-breakers": "weighted-average",
    "wonderful-and-fair": "exit-multiple",
}

# The three overall scores `rank` can sort by (see the stock-analysis overall-score
# reference). Each maps to a key in the stock-doc's `overall:` block.
RANK_METRICS = {
    "cqv": "cqv_score",   # confidence-adjusted quality×value — where to allocate dollars (default)
    "qv": "qv_score",     # quality×value — where to focus research
    "agent": "agent_score",  # the agent's valuation-aware judgement call
}


def load_doc(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    try:
        fm = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}, text
    if not isinstance(fm, dict):
        return {}, text
    return fm, body


def iter_stock_docs(stock_dir: Path):
    for path in sorted(stock_dir.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        yield path


def normalize_ticker(ticker: str) -> str:
    return ticker.strip().lstrip("$").upper()


def doc_path(stock_dir: Path, ticker: str) -> Path:
    return stock_dir / f"{normalize_ticker(ticker)}.md"


def parse_date(value: Any) -> dt.date | None:
    if value is None:
        return None
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def format_age(value: Any, today: dt.date) -> str:
    """Format a date-only update age as an exact duration in days."""
    last_updated = parse_date(value)
    if last_updated is None:
        return "?"
    return f"{(today - last_updated).days}d"


def frontmatter_summary(path: Path) -> dict[str, Any]:
    fm, _ = load_doc(path)
    out = dict(fm)
    out["file"] = str(path)
    return out


def cmd_show(args: argparse.Namespace) -> int:
    path = doc_path(args.stock_dir, args.ticker)
    if not path.exists():
        print(f"No stock doc found for {normalize_ticker(args.ticker)} at {path}", file=sys.stderr)
        return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_rank(args: argparse.Namespace) -> int:
    today = dt.date.today()
    rows = []
    for path in iter_stock_docs(args.stock_dir):
        fm, _ = load_doc(path)
        scores = overall_scores(fm)
        if scores[args.by] is None:
            continue
        ticker = str(fm.get("ticker") or path.stem)
        rows.append(
            (
                ticker,
                winning_strategy(fm),
                scores,
                format_age(fm.get("last-updated"), today),
                str(fm.get("company") or ""),
            )
        )
    rows.sort(key=lambda r: (-r[2][args.by], r[0]))
    if args.n is not None:
        rows = rows[: args.n]

    def fmt(v: float | None) -> str:
        return "" if v is None else f"{v:g}"

    print(f"#\t{'ticker':<12}\t{'strategy':<20}\tqv\tcqv\tagent\tage\tcompany")
    for i, (ticker, strategy, scores, age, company) in enumerate(rows, start=1):
        print(f"{i}\t{ticker:<12}\t{strategy:<20}\t{fmt(scores['qv'])}\t{fmt(scores['cqv'])}\t{fmt(scores['agent'])}\t{age}\t{company}")
    return 0


def overall_scores(fm: dict[str, Any]) -> dict[str, float | None]:
    overall = fm.get("overall")
    if not isinstance(overall, dict):
        return {metric: None for metric in RANK_METRICS}
    return {metric: as_float(overall.get(key)) for metric, key in RANK_METRICS.items()}


def scoreboard_ranks(docs: list[tuple[Path, dict[str, Any]]]) -> dict[str, dict[str, int]]:
    """Return per-metric 1-based ordinal ranks, sorted like `rank`.

    Only docs carrying a score for that metric are ranked. Ties are broken by ticker,
    matching `cmd_rank`, so every ranked ticker gets a stable position.
    """
    ranks: dict[str, dict[str, int]] = {metric: {} for metric in RANK_METRICS}
    for metric in RANK_METRICS:
        rows = []
        for path, fm in docs:
            score = overall_scores(fm)[metric]
            if score is None:
                continue
            rows.append((score, str(fm.get("ticker") or path.stem)))
        rows.sort(key=lambda r: (-r[0], r[1]))
        ranks[metric] = {ticker: i for i, (_score, ticker) in enumerate(rows, start=1)}
    return ranks


def winning_strategy(fm: dict[str, Any]) -> str:
    chosen = fm.get("analysis-strategy")
    if chosen:
        return str(chosen)
    strategies = fm.get("strategies")
    if not isinstance(strategies, dict):
        return ""
    scored = []
    for strategy, entry in strategies.items():
        score = as_float(entry.get("score")) if isinstance(entry, dict) else None
        if score is not None:
            scored.append((score, str(strategy)))
    if not scored:
        return ""
    scored.sort(key=lambda r: (-r[0], r[1]))
    return scored[0][1]


def cmd_latest(args: argparse.Namespace) -> int:
    docs = []
    for path in iter_stock_docs(args.stock_dir):
        fm, _ = load_doc(path)
        docs.append((path, fm))

    ranks = scoreboard_ranks(docs)
    rows = []
    for path, fm in docs:
        last = parse_date(fm.get("last-updated"))
        ticker = str(fm.get("ticker") or path.stem)
        rows.append((last or dt.date.min, ticker, fm))
    rows.sort(key=lambda r: (-r[0].toordinal(), r[1]))
    rows = rows[: args.n]

    for last, ticker, fm in rows:
        last_s = "" if last == dt.date.min else last.isoformat()
        strategy = winning_strategy(fm)
        qv_rank = ranks["qv"].get(ticker)
        cqv_rank = ranks["cqv"].get(ticker)
        agent_rank = ranks["agent"].get(ticker)
        qv_s = "" if qv_rank is None else f"#{qv_rank}"
        cqv_s = "" if cqv_rank is None else f"#{cqv_rank}"
        agent_s = "" if agent_rank is None else f"#{agent_rank}"
        company = str(fm.get("company") or "")
        print(f"{ticker}\tlast={last_s}\tstrategy={strategy}\tqv={qv_s}\tcqv={cqv_s}\tagent={agent_s}\t{company}")
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    rows = []
    for path in iter_stock_docs(args.stock_dir):
        fm, _ = load_doc(path)
        if fm.get("watching") is True:
            rows.append((str(fm.get("ticker") or path.stem), str(fm.get("last-updated") or ""), str(fm.get("company") or "")))
    rows.sort(key=lambda r: (r[1] or "9999-12-31", r[0]))
    for ticker, last, company in rows:
        print(f"{ticker}\tlast={last}\t{company}")
    return 0


def clamp01(value: float) -> float:
    return 0.0 if value < 0.0 else 1.0 if value > 1.0 else value


def chosen_confidence(fm: dict[str, Any]) -> float | None:
    """Normalized confidence of the doc's chosen strategy (`analysis-strategy`).

    qv_score is derived from that same strategy, so its confidence is the right
    uncertainty to pair with it. Returns None if unavailable.
    """
    strategies = fm.get("strategies")
    chosen = fm.get("analysis-strategy")
    if isinstance(strategies, dict) and chosen:
        entry = strategies.get(chosen)
        if isinstance(entry, dict):
            return as_float(entry.get("confidence"))
    return None


def staleness(days: int | None, tau: float) -> float:
    """Saturating staleness in [0, 1] from raw days since last update.

    0 for a just-updated doc, ~0.63 at `tau` days, approaching 1 when far
    overdue. Unknown last-updated is treated as maximally stale.
    """
    if days is None:
        return 1.0
    if days <= 0 or tau <= 0:
        return 0.0
    return 1.0 - math.exp(-days / tau)


def cmd_focus(args: argparse.Namespace) -> int:
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    rows = []
    for path in iter_stock_docs(args.stock_dir):
        fm, _ = load_doc(path)
        if fm.get("watching") is not True:
            continue
        overall = fm.get("overall")
        qv = as_float(overall.get("qv_score")) if isinstance(overall, dict) else None
        if qv is None:
            continue
        qv = clamp01(qv)
        conf = chosen_confidence(fm)
        # Unknown confidence counts as maximal uncertainty (0.0) — an unscored doc
        # is exactly the kind we want to surface for research.
        conf_used = clamp01(conf) if conf is not None else 0.0
        last = parse_date(fm.get("last-updated"))
        days = (today - last).days if last else None
        stale = staleness(days, args.tau)
        priority = (qv ** args.wq) * ((1.0 - conf_used) ** args.wc) * (stale ** args.ws)
        rows.append((priority, qv, conf, days, str(fm.get("ticker") or path.stem), str(fm.get("company") or "")))
    rows.sort(key=lambda r: (-r[0], r[4]))
    if args.n is not None:
        rows = rows[: args.n]
    for priority, qv, conf, days, ticker, company in rows:
        conf_s = "" if conf is None else f"{conf:g}"
        age_s = "?" if days is None else str(days)
        print(f"{ticker}\t{priority:.4f}\tqv={qv:g}\tconf={conf_s}\tage={age_s}d\t{company}")
    return 0


def normalize_strategy(strategy: str) -> str:
    return strategy.strip().lower().replace("_", "-")


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def cmd_list_strategy(args: argparse.Namespace) -> int:
    strategy = normalize_strategy(args.strategy)
    method = STRATEGY_VALUATION_METHODS.get(strategy)

    rows = []
    for path in iter_stock_docs(args.stock_dir):
        fm, _ = load_doc(path)
        strategies = fm.get("strategies")
        entry = strategies.get(strategy) if isinstance(strategies, dict) else None
        if not isinstance(entry, dict):
            continue
        strategy_score = as_float(entry.get("score"))
        if strategy_score is None:
            continue
        confidence = as_float(entry.get("confidence"))
        roi = None
        if method:
            valuation = fm.get("valuation")
            block = valuation.get(method) if isinstance(valuation, dict) else None
            if isinstance(block, dict):
                roi = as_float(block.get("roi"))
        rows.append(
            (
                strategy_score,
                confidence,
                roi,
                str(fm.get("ticker") or path.stem),
                str(fm.get("company") or ""),
            )
        )

    rows.sort(key=lambda r: (-r[0], r[3]))
    for strategy_score, confidence, roi, ticker, company in rows:
        score_s = f"{strategy_score:g}"
        confidence_s = "" if confidence is None else f"{confidence:g}"
        roi_s = "" if roi is None else f"{roi:g}"
        print(f"{ticker}\t{score_s}\t{confidence_s}\t{roi_s}\t{company}")
    return 0


def cmd_frontmatter(args: argparse.Namespace) -> int:
    if args.ticker:
        paths = [doc_path(args.stock_dir, args.ticker)]
    else:
        paths = list(iter_stock_docs(args.stock_dir))
    data = [frontmatter_summary(p) for p in paths if p.exists()]
    # default=str so YAML-parsed dates (datetime.date) serialise as ISO strings.
    print(json.dumps(data[0] if args.ticker and data else data, indent=2, sort_keys=True, default=str))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Read stock-doc front matter and list stock-doc views.")
    p.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("show")
    s.add_argument("ticker")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("rank")
    s.add_argument("n", nargs="?", type=int)
    s.add_argument("--by", choices=tuple(RANK_METRICS), default="cqv",
                   help="Which overall score to rank by (default: cqv — where to allocate dollars).")
    s.set_defaults(func=cmd_rank)

    s = sub.add_parser("latest")
    s.add_argument("n", nargs="?", type=int, default=10, help="Limit to the latest N docs (default: 10).")
    s.set_defaults(func=cmd_latest)

    s = sub.add_parser("watch")
    s.set_defaults(func=cmd_watch)

    s = sub.add_parser(
        "focus",
        help="Rank watched docs by research-focus priority: high qv_score, low confidence, stale.",
    )
    s.add_argument("n", nargs="?", type=int, help="Limit to the top N (default: all).")
    s.add_argument("--today")
    s.add_argument("--tau", type=float, default=60.0,
                   help="Staleness time constant in days; staleness reaches ~63%% at this age (default: 60).")
    s.add_argument("--wq", type=float, default=1.0, help="qv_score exponent (default: 1.0; 0 disables).")
    s.add_argument("--wc", type=float, default=1.0, help="(1-confidence) exponent (default: 1.0; 0 disables).")
    s.add_argument("--ws", type=float, default=1.0, help="staleness exponent (default: 1.0; 0 disables).")
    s.set_defaults(func=cmd_focus)

    s = sub.add_parser("list-strategy")
    s.add_argument("strategy", help="Strategy id, e.g. rule-breakers or freeroll")
    s.set_defaults(func=cmd_list_strategy)

    s = sub.add_parser("frontmatter")
    s.add_argument("ticker", nargs="?")
    s.set_defaults(func=cmd_frontmatter)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
