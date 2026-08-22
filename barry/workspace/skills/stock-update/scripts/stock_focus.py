#!/usr/bin/env python3
"""Rank watched stocks by research-focus priority and update triggers.

Subcommands:
- ``list [N]`` -- print the ranked table (the previous default output).
- ``peek``    -- print exactly one bare ticker, the current top priority,
                 for the scheduled stock-update worker.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_ANNOUNCEMENT_WEIGHT = 0.20


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clamp01(value: float) -> float:
    return 0.0 if value < 0.0 else 1.0 if value > 1.0 else value


def parse_date(value: Any) -> dt.date | None:
    if value is None:
        return None
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def chosen_confidence(frontmatter: dict[str, Any]) -> float | None:
    strategies = frontmatter.get("strategies")
    chosen = frontmatter.get("analysis-strategy")
    if isinstance(strategies, dict) and chosen:
        entry = strategies.get(chosen)
        if isinstance(entry, dict):
            return as_float(entry.get("confidence"))
    return None


def staleness(days: int | None, tau: float) -> float:
    if days is None:
        return 1.0
    if days <= 0 or tau <= 0:
        return 0.0
    return 1.0 - math.exp(-days / tau)


def load_frontmatter(stock_dir: Path | None) -> list[dict[str, Any]]:
    command = ["stock_doc"]
    if stock_dir is not None:
        command.extend(["--stock-dir", str(stock_dir)])
    command.append("frontmatter")

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("stock_doc command not found") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or f"exit status {exc.returncode}"
        raise RuntimeError(f"stock_doc frontmatter failed: {detail}") from exc

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"stock_doc frontmatter returned invalid JSON: {exc}") from exc
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise RuntimeError("stock_doc frontmatter returned an unexpected JSON structure")
    return data


def load_pending_announcements(
    stock_dir: Path | None,
    state: Path | None,
    today: dt.date,
    *,
    cache_only: bool,
    force_refresh: bool,
) -> tuple[dict[str, int], list[str]]:
    command = ["stock_announcements"]
    if stock_dir is not None:
        command.extend(["--stock-dir", str(stock_dir)])
    if state is not None:
        command.extend(["--state", str(state)])
    command.extend(["pending", "--as-of", today.isoformat()])
    if cache_only:
        command.append("--cache-only")
    elif force_refresh:
        command.append("--force-refresh")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError("stock_announcements command not found") from exc

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        detail = result.stderr.strip() or str(exc)
        raise RuntimeError(f"stock_announcements pending returned invalid JSON: {detail}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("tickers"), dict):
        raise RuntimeError("stock_announcements pending returned an unexpected JSON structure")

    counts: dict[str, int] = {}
    for ticker, count in data["tickers"].items():
        if not isinstance(ticker, str) or not isinstance(count, int) or count < 1:
            raise RuntimeError("stock_announcements pending returned an invalid ticker count")
        counts[ticker.upper()] = count

    raw_warnings = data.get("warnings", [])
    if not isinstance(raw_warnings, list):
        raise RuntimeError("stock_announcements pending returned invalid warnings")
    warnings = [str(warning) for warning in raw_warnings]
    if result.returncode != 0:
        warnings.append(
            f"refresh exited with status {result.returncode}; using the returned pending queue"
        )
    return counts, warnings


def ticker_for(frontmatter: dict[str, Any]) -> str:
    ticker = frontmatter.get("ticker")
    if ticker:
        return str(ticker)
    return Path(str(frontmatter.get("file") or "")).stem


def focus_priority(
    qv: float,
    confidence: float,
    stale: float,
    *,
    wq: float,
    wc: float,
    ws: float,
    has_pending_announcement: bool,
    announcement_weight: float,
) -> float:
    base_attention = ((1.0 - confidence) ** wc) * (stale**ws)
    announcement_attention = announcement_weight if has_pending_announcement else 0.0
    combined_attention = 1.0 - (
        (1.0 - base_attention) * (1.0 - announcement_attention)
    )
    return (qv**wq) * combined_attention


def rank_documents(args) -> tuple[list[tuple[Any, ...]], list[str]]:
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    warnings: list[str] = []
    try:
        documents = load_frontmatter(args.stock_dir)
        if args.wa == 0.0:
            announcement_counts: dict[str, int] = {}
        else:
            announcement_counts, warnings = load_pending_announcements(
                args.stock_dir,
                args.announcement_state,
                today,
                cache_only=args.announcements_cache_only,
                force_refresh=args.announcements_force_refresh,
            )
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
    for warning in warnings:
        print(f"warning: stock_announcements: {warning}", file=sys.stderr)

    rows = []
    for frontmatter in documents:
        if frontmatter.get("watching") is not True:
            continue
        overall = frontmatter.get("overall")
        qv = as_float(overall.get("qv_score")) if isinstance(overall, dict) else None
        if qv is None:
            continue
        qv = clamp01(qv)
        confidence = chosen_confidence(frontmatter)
        confidence_used = clamp01(confidence) if confidence is not None else 0.0
        last_updated = parse_date(frontmatter.get("last-updated"))
        days = (today - last_updated).days if last_updated else None
        stale = staleness(days, args.tau)
        ticker = ticker_for(frontmatter)
        pending_count = announcement_counts.get(ticker.upper(), 0)
        priority = focus_priority(
            qv,
            confidence_used,
            stale,
            wq=args.wq,
            wc=args.wc,
            ws=args.ws,
            has_pending_announcement=pending_count > 0,
            announcement_weight=args.wa,
        )
        rows.append(
            (
                priority,
                qv,
                confidence,
                days,
                pending_count,
                ticker,
                str(frontmatter.get("company") or ""),
            )
        )

    rows.sort(key=lambda row: (-row[0], row[5]))
    return rows, warnings


def cmd_list(args) -> int:
    rows, _warnings = rank_documents(args)
    if args.n is not None:
        rows = rows[: args.n]
    for priority, qv, confidence, days, pending_count, ticker, company in rows:
        confidence_text = "" if confidence is None else f"{confidence:g}"
        age_text = "?" if days is None else str(days)
        print(
            f"{ticker}\t{priority:.4f}\tqv={qv:g}\tconf={confidence_text}"
            f"\tage={age_text}d\tpending={pending_count}\t{company}"
        )
    return 0


def cmd_peek(args) -> int:
    rows, _warnings = rank_documents(args)
    if not rows:
        # No eligible stock: print nothing so the dispatcher skips the job.
        return 1
    print(rows[0][5])
    return 0


def add_shared_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--stock-dir", type=Path)
    parser.add_argument("--today")
    parser.add_argument(
        "--tau",
        type=float,
        default=60.0,
        help="Staleness time constant in days; staleness reaches ~63%% at this age (default: 60).",
    )
    parser.add_argument("--wq", type=float, default=1.0, help="qv_score exponent (default: 1.0; 0 disables).")
    parser.add_argument(
        "--wc", type=float, default=1.0, help="(1-confidence) exponent (default: 1.0; 0 disables)."
    )
    parser.add_argument("--ws", type=float, default=1.0, help="staleness exponent (default: 1.0; 0 disables).")
    parser.add_argument(
        "--wa",
        type=float,
        default=DEFAULT_ANNOUNCEMENT_WEIGHT,
        help="pending-announcement attention weight (default: 0.20; 0 disables)",
    )
    parser.add_argument("--announcement-state", type=Path)
    announcement_refresh = parser.add_mutually_exclusive_group()
    announcement_refresh.add_argument(
        "--announcements-cache-only",
        action="store_true",
        help="use queued and cached announcement data without refreshing",
    )
    announcement_refresh.add_argument(
        "--announcements-force-refresh",
        action="store_true",
        help="refresh announcement discovery even when its cache is fresh",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Rank watched stocks by research-focus priority: high qv_score, "
            "low confidence, stale, and pending announcements."
        )
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    list_parser = sub.add_parser("list", help="print the ranked table")
    add_shared_args(list_parser)
    list_parser.add_argument("n", nargs="?", type=int, help="Limit to the top N (default: all).")
    list_parser.set_defaults(func=cmd_list)

    peek_parser = sub.add_parser(
        "peek", help="print exactly one bare ticker: the top-priority stock"
    )
    add_shared_args(peek_parser)
    peek_parser.set_defaults(func=cmd_peek)

    args = parser.parse_args()
    if not 0.0 <= args.wa <= 1.0:
        parser.error("--wa must be between 0 and 1")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())