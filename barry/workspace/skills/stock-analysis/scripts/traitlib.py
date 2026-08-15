#!/usr/bin/env python3
"""Shared helpers for the per-trait DATA scripts.

A trait data script gathers everything the agent needs to *score* one quantitative
trait — the targeted Yahoo pulls and the derived figures computed from them — and
nothing more. It is the executable form of a trait's "What to look at" metrics.

Division of labour (deliberate, see stock-analysis/SKILL.md):
  * yfin is the single source of Yahoo access; trait scripts shell out to it rather
    than importing yfinance, so the data layer stays in one place.
  * trait scripts stay on the FACTS side of the fact/judgement line: they fetch and
    compute, they never assign a score, a confidence, or a band. Which band a figure
    falls in depends on business-type judgement the script can't make — that read is
    the agent's, against the tables in the trait doc.

This module wraps the yfin invocation (so each trait script is thin and they all call
it identically) and carries the small numeric/formatting utilities they share.

No secrets, no network of its own — all network goes through yfin.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

# .../skills/stock-analysis/scripts/traitlib.py -> parents[3] == workspace root,
# where the data-tool wrappers live under scripts/bin/.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_REPO_YFIN = _REPO_ROOT / "scripts" / "bin" / "yfin"
_REPO_EDGAR = _REPO_ROOT / "scripts" / "bin" / "edgar"


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"error: {msg}")


def _tool_cmd(name: str, repo_path: Path) -> list[str]:
    """A data-tool invocation: the wrapper on PATH if present, else the repo copy."""
    exe = shutil.which(name)
    if exe:
        return [exe]
    if repo_path.exists():
        return [str(repo_path)]
    fail(f"cannot find the {name!r} CLI on PATH or at {repo_path} "
         "(run scripts/bin/install.sh to set it up).")


def _run_json(name: str, cmd: list[str], args: tuple) -> Any:
    """Run a data-tool subcommand and return its parsed JSON.

    Both yfin and edgar emit a single-key {"error": ...} object with a non-zero
    exit on failure; that is surfaced as a SystemExit carrying the tool's message."""
    full = cmd + [str(a) for a in args]
    try:
        proc = subprocess.run(full, capture_output=True, text=True)
    except OSError as e:
        fail(f"could not run {name}: {e}")
    if not proc.stdout.strip():
        fail(f"{name} produced no output (exit {proc.returncode}): {proc.stderr.strip()[:300]}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        fail(f"{name} returned non-JSON output:\n{proc.stdout[:500]}")
    if isinstance(data, dict) and set(data) == {"error"}:
        fail(f"{name} {' '.join(str(a) for a in args)}: {data['error']}")
    return data


def yfin(*args: str) -> Any:
    """Run a yfin (Yahoo Finance) subcommand and return its parsed JSON."""
    return _run_json("yfin", _tool_cmd("yfin", _REPO_YFIN), args)


def edgar(*args: str) -> Any:
    """Run an edgar (SEC EDGAR) subcommand and return its parsed JSON.

    The deep-history counterpart to yfin: use it for the long annual series (revenue,
    margins, share count over 15+ years) that Yahoo's 4-year cap can't supply. US
    filers only — it fails plainly for a non-US ticker."""
    return _run_json("edgar", _tool_cmd("edgar", _REPO_EDGAR), args)


# --- statement pulls / period alignment --------------------------------------

def pull(ticker: str, cmd: str, *, years: int | None = None, fields: str | None = None,
         period: str | None = None) -> dict:
    """Run one statement-style yfin command and return its {period: {...}} dict.

    Thin convenience over yfin() for the common case the trait scripts share:
    `pull("AAPL", "income", years=10, fields="Total Revenue,Net Income")`."""
    args: list[str] = [cmd, ticker]
    if period:
        args += ["--period", period]
    if years:
        args += ["-n", str(years)]
    if fields:
        args += ["--fields", fields]
    out = yfin(*args)
    return out if isinstance(out, dict) else {}


def aligned_periods(*stmts: dict, limit: int | None = None) -> list[str]:
    """The union of period keys across statements, newest first (statements are
    keyed by ISO fiscal-year-end), optionally capped to the N most recent."""
    keys: set[str] = set()
    for s in stmts:
        if isinstance(s, dict):
            keys |= set(s.keys())
    ordered = sorted(keys, reverse=True)
    return ordered[:limit] if limit else ordered


def ttm_row(ticker: str, cmd: str, fields: str | None = None) -> dict:
    """The single trailing-twelve-month record from `income`/`cashflow` (the only
    statements with a ttm period), or {} when unavailable."""
    raw = pull(ticker, cmd, period="ttm", fields=fields)
    return next(iter(raw.values()), {}) if raw else {}


# --- numeric / lookup helpers ------------------------------------------------

def safe_div(a: Any, b: Any) -> float | None:
    """a / b, or None if either is missing or the denominator is zero."""
    if a is None or b is None or b == 0:
        return None
    try:
        return a / b
    except (TypeError, ZeroDivisionError):
        return None


def first_present(d: dict[str, Any], *keys: str) -> tuple[Any, str | None]:
    """Return (value, key) for the first key present with a non-None value.

    yfinance line-item names drift (e.g. "Cash And Cash Equivalents" vs the broader
    "Cash Cash Equivalents And Short Term Investments"); list the preferred name
    first and the script records which one it actually used."""
    for k in keys:
        v = d.get(k)
        if v is not None:
            return v, k
    return None, None


def rnd(x: Any, n: int = 2) -> float | None:
    """Round numbers, pass None through (so missing data stays missing)."""
    return round(x, n) if isinstance(x, (int, float)) else None


def pct_change(new: Any, old: Any) -> float | None:
    """(new - old) / |old| as a fraction; None if either is missing or old is 0."""
    if new is None or old is None or old == 0:
        return None
    return (new - old) / abs(old)


def cagr(latest: Any, earliest: Any, years: int) -> float | None:
    """Compound annual growth from earliest to latest over `years`; None unless both
    are positive (a sign change makes a CAGR meaningless)."""
    if latest is None or earliest is None or earliest <= 0 or latest <= 0 or years <= 0:
        return None
    return (latest / earliest) ** (1.0 / years) - 1.0


def stdev(values: list[float]) -> float | None:
    """Population standard deviation of the present values, or None if < 2."""
    xs = [v for v in values if isinstance(v, (int, float))]
    if len(xs) < 2:
        return None
    mean = sum(xs) / len(xs)
    return (sum((x - mean) ** 2 for x in xs) / len(xs)) ** 0.5


def trend(latest: Any, earliest: Any, eps: float = 0.1) -> str:
    """A coarse direction label for a figure's move across the window."""
    if latest is None or earliest is None:
        return "—"
    delta = latest - earliest
    return "rising" if delta > eps else "falling" if delta < -eps else "flat"


def millions(x: Any) -> str:
    """Format a raw currency figure in millions for table output; '—' when absent."""
    if not isinstance(x, (int, float)):
        return "—"
    return f"{x / 1e6:,.0f}"


def pctf(x: Any, dp: int = 1) -> str:
    """A fraction (0.153) as a percent string ('15.3%') for table output; '—' if absent."""
    return f"{x * 100:.{dp}f}%" if isinstance(x, (int, float)) else "—"


def val(x: Any, suffix: str = "") -> str:
    """A bare figure for a table cell, em dash when missing."""
    return f"{x}{suffix}" if x is not None else "—"


# --- shared table scaffolding ------------------------------------------------
# Every trait script opens with the same title and closes with the same two blocks
# (what Yahoo can't see, and the reminder that scoring is the agent's call), so the
# scripts stay uniform and only their middle — the trait's own figures — differs.

def title(ticker: str, trait_name: str, currency: str | None, width: int = 66) -> list[str]:
    return [f"{ticker}  —  {trait_name}   [{currency or '?'}]", "=" * width]


def footer(trait_id: str, not_covered: list[str] | None = None) -> list[str]:
    out: list[str] = []
    if not_covered:
        out += ["", "  NOT covered by Yahoo — get from filings:"]
        out += [f"    • {n}" for n in not_covered]
    out += ["", f"  These are the facts only. Score against the bands in the {trait_id} trait doc —",
            "  the read depends on business-type and judgement the script doesn't make."]
    return out
