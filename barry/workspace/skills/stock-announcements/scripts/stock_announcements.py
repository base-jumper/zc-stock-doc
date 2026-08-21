#!/usr/bin/env python3
"""Queue new ASX announcements and SEC filings for AU/US stock-docs.

The script performs discovery, deterministic filtering, queue expiry, and bounded
batching. It never downloads filing bodies or edits stock-docs. Candidates remain
pending until explicitly acknowledged after review.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import html.parser
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml


WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STOCK_DIR = WORKSPACE / "investment" / "stock-docs"
DEFAULT_STATE = WORKSPACE / "tasks" / "stock-announcement-monitor-state.json"

ASX_URLS = (
    "https://www.asx.com.au/asx/v2/statistics/todayAnns.do",
    "https://www.asx.com.au/asx/v2/statistics/prevBusDayAnns.do",
)
SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_INDEX_ROOT = "https://www.sec.gov/Archives/edgar/daily-index"
DEFAULT_USER_AGENT = "openclaw-stock-analysis (nbuters@gmail.com)"
DEFAULT_MAX_AGE_DAYS = 30
DEFAULT_MAX_CANDIDATES = 4
DEFAULT_REFRESH_INTERVAL = dt.timedelta(hours=2)
DEFAULT_QV_FLOOR = 0.05
DEFAULT_URGENCY_TAU_DAYS = 10.0
URGENCY_FLOOR = 0.25

ASX_HEADLINE_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("financial-results", re.compile(
        r"\b(results?|annual report|half[ -]?year|quarterly (activities|report)|"
        r"cash flow report|trading update|earnings|guidance|outlook)\b", re.I)),
    ("capital-allocation", re.compile(
        r"\b(dividend|distribution|buy[ -]?back|capital return|capital rais|placement|"
        r"entitlement offer|share purchase plan|debt facilit|refinanc)\w*\b", re.I)),
    ("transaction", re.compile(
        r"\b(acquisition|acquire|disposal|divest|merger|takeover|scheme of arrangement|"
        r"change of control|strategic review)\w*\b", re.I)),
    ("operations", re.compile(
        r"\b(material contract|contract award|customer contract|clinical trial|trial results|"
        r"regulatory approval|fda|tga|investigation|litigation|cyber|data breach|"
        r"suspension from quotation|insolvency|administration)\w*\b", re.I)),
    ("leadership", re.compile(
        r"\b(ceo|chief executive|cfo|chief financial|managing director|chair)\b.*"
        r"\b(appoint|resign|retir|depart|succession|change)\w*\b|"
        r"\b(appoint|resign|retir|depart|succession|change)\w*\b.*"
        r"\b(ceo|chief executive|cfo|chief financial|managing director|chair)\b", re.I)),
)

# Forms whose contents can reasonably alter the durable stock view. Ownership
# forms are deliberately excluded: they are noisy and often filed under the
# holder's CIK rather than the issuer's CIK, so the daily index cannot map them
# reliably with a ticker-only universe.
SEC_FORMS = {
    "8-K", "10-K", "10-Q", "11-K", "20-F", "40-F", "6-K",
    "S-1", "S-4", "F-1", "F-4",
    "DEF 14A", "DEFM14A", "PREM14A", "SC 13E3",
}
# 424B2 (structured notes) and shelf registrations (S-3/F-3) are excluded:
# frequent bank issuance creates large, low-value review queues. A consequential
# takedown is normally visible through an 8-K and/or 424B5.
SEC_FORM_PREFIXES = ("424B4", "424B5", "424B7", "SC TO-")


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    value = yaml.safe_load(text[4:end]) or {}
    return value if isinstance(value, dict) else {}


def qv_value(fm: dict[str, Any]) -> float | None:
    overall = fm.get("overall")
    if not isinstance(overall, dict):
        return None
    try:
        return max(0.0, min(1.0, float(overall["qv_score"])))
    except (KeyError, TypeError, ValueError):
        return None


def stock_universe(stock_dir: Path) -> dict[str, float | None]:
    universe: dict[str, float | None] = {}
    for path in stock_dir.glob("*.md"):
        if path.name.upper() == "README.MD":
            continue
        fm = frontmatter(path)
        ticker = str(fm.get("ticker") or path.stem).upper()
        # AU is represented canonically by .AX. No suffix means a US-listed
        # security in this workspace; the SEC map is the final authority.
        if not (ticker.endswith(".AX") or "." not in ticker):
            continue
        universe[ticker] = qv_value(fm)
    return dict(sorted(universe.items()))


class AsxParser(html.parser.HTMLParser):
    """Parse the announcement table without treating the full HTML as model input."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict[str, Any]] = []
        self.in_row = False
        self.in_cell = False
        self.in_link = False
        self.ignore_link_text = False
        self.cells: list[str] = []
        self.cell_text: list[str] = []
        self.headline_text: list[str] = []
        self.href = ""
        self.price_sensitive = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = (attr.get("class") or "").split()
        if tag == "tr":
            self.in_row = True
            self.cells = []
            self.href = ""
            self.price_sensitive = False
        elif tag == "td" and self.in_row:
            self.in_cell = True
            self.cell_text = []
            if "pricesens" in classes:
                self.price_sensitive = True
        elif tag == "a" and self.in_cell:
            self.in_link = True
            self.href = attr.get("href") or self.href
        elif tag == "span" and self.in_link and ({"page", "filesize"} & set(classes)):
            self.ignore_link_text = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "span":
            self.ignore_link_text = False
        elif tag == "a":
            self.in_link = False
        elif tag == "td" and self.in_cell:
            self.cells.append(" ".join("".join(self.cell_text).split()))
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            self._finish_row()
            self.in_row = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_text.append(data)
        if self.in_link and not self.ignore_link_text:
            self.headline_text.append(data)

    def _finish_row(self) -> None:
        if len(self.cells) < 4 or not self.href:
            self.headline_text = []
            return
        code = self.cells[0].strip().upper()
        id_match = re.search(r"[?&]idsId=([^&]+)", self.href)
        if not code or not id_match:
            self.headline_text = []
            return
        title = " ".join("".join(self.headline_text).split())
        date_match = re.search(r"(\d{2})/(\d{2})/(\d{4})", self.cells[1])
        if not date_match:
            self.headline_text = []
            return
        day, month, year = date_match.groups()
        self.rows.append({
            "event_id": f"asx:{id_match.group(1)}",
            "ticker": f"{code}.AX",
            "market": "AU",
            "date": f"{year}-{month}-{day}",
            "published_at": self.cells[1],
            "title": title,
            "price_sensitive": self.price_sensitive,
            "url": urllib.parse.urljoin("https://www.asx.com.au", self.href),
        })
        self.headline_text = []


def get_bytes(url: str, *, allow_404: bool = False) -> bytes | None:
    user_agent = os.environ.get("EDGAR_USER_AGENT") or DEFAULT_USER_AGENT
    headers = {"User-Agent": user_agent}
    if urllib.parse.urlparse(url).hostname in {"sec.gov", "www.sec.gov", "data.sec.gov"}:
        headers.update({
            "Accept-Encoding": "gzip, deflate",
            "Host": urllib.parse.urlparse(url).hostname or "www.sec.gov",
        })
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            if response.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return raw
    except urllib.error.HTTPError as error:
        if allow_404 and error.code == 404:
            return None
        raise


def get_json(url: str) -> Any:
    raw = get_bytes(url)
    assert raw is not None
    return json.loads(raw)


def asx_candidates(universe: set[str]) -> list[dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    for url in ASX_URLS:
        raw = get_bytes(url)
        assert raw is not None
        parser = AsxParser()
        parser.feed(raw.decode("utf-8", "replace"))
        for event in parser.rows:
            if event["ticker"] not in universe:
                continue
            reason = None
            if event["price_sensitive"]:
                reason = "ASX price-sensitive"
            else:
                for rule_name, pattern in ASX_HEADLINE_RULES:
                    if pattern.search(event["title"]):
                        reason = f"ASX headline rule: {rule_name}"
                        break
            if reason:
                event["reason"] = reason
                candidates[event["event_id"]] = event
    return list(candidates.values())


def sec_ticker_map(universe: set[str]) -> tuple[dict[int, list[str]], list[str]]:
    data = get_json(SEC_TICKERS_URL)
    by_cik: dict[int, list[str]] = {}
    mapped: set[str] = set()
    for entry in data.values():
        ticker = str(entry.get("ticker") or "").upper()
        if ticker not in universe:
            continue
        cik = int(entry["cik_str"])
        by_cik.setdefault(cik, []).append(ticker)
        mapped.add(ticker)
    return by_cik, sorted(universe - mapped)


def important_sec_form(form: str) -> bool:
    base = form.removesuffix("/A")
    return base in SEC_FORMS or base.startswith(SEC_FORM_PREFIXES)


def sec_index_url(day: dt.date) -> str:
    quarter = (day.month - 1) // 3 + 1
    return f"{SEC_INDEX_ROOT}/{day.year}/QTR{quarter}/master.{day:%Y%m%d}.idx"


def sec_candidates(
    universe: set[str], as_of: dt.date, lookback_days: int
) -> tuple[list[dict[str, Any]], list[str]]:
    by_cik, unmapped = sec_ticker_map(universe)
    candidates: dict[str, dict[str, Any]] = {}
    indexes_read = 0
    for offset in range(lookback_days):
        day = as_of - dt.timedelta(days=offset)
        try:
            raw = get_bytes(sec_index_url(day), allow_404=True)
        except urllib.error.HTTPError as error:
            # SEC returns 403, rather than 404, for a current/weekend/holiday
            # daily-index path that has not been published. Do not let one
            # expected missing date hide a broader outage: at least one index
            # in the lookback window must still be readable below.
            if error.code == 403:
                continue
            raise
        if raw is None:
            continue
        indexes_read += 1
        for line in raw.decode("latin-1").splitlines():
            parts = line.split("|", 4)
            if len(parts) != 5 or not parts[0].isdigit():
                continue
            cik_s, company, form, filed, filename = parts
            tickers = by_cik.get(int(cik_s))
            if not tickers or not important_sec_form(form):
                continue
            accession = Path(filename).name.removesuffix(".txt")
            filing_url = "https://www.sec.gov/Archives/" + filename.removesuffix(".txt") + "-index.html"
            for ticker in tickers:
                event_id = f"sec:{accession}:{ticker}"
                candidates[event_id] = {
                    "event_id": event_id,
                    "ticker": ticker,
                    "market": "US",
                    "date": dt.datetime.strptime(filed, "%Y%m%d").date().isoformat(),
                    "title": f"Form {form} — {company}",
                    "form": form,
                    "reason": f"SEC form {form}",
                    "url": filing_url,
                }
    if indexes_read == 0:
        raise RuntimeError(f"no readable SEC daily index in {lookback_days}-day window")
    return list(candidates.values()), unmapped


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 2, "acknowledged": {}, "pending": {}}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("acknowledged"), dict):
        raise ValueError(f"invalid state file: {path}")
    pending = value.setdefault("pending", {})
    if not isinstance(pending, dict):
        raise ValueError(f"invalid pending queue in state file: {path}")
    value["version"] = 2
    return value


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def discovery_cache_is_fresh(
    state: dict[str, Any], now: dt.datetime, interval: dt.timedelta
) -> bool:
    if not isinstance(state.get("discovery_cache"), list):
        return False
    stamp = state.get("last_downloaded_at")
    if not isinstance(stamp, str):
        return False
    try:
        downloaded_at = dt.datetime.fromisoformat(stamp)
    except ValueError:
        return False
    if downloaded_at.tzinfo is None:
        downloaded_at = downloaded_at.replace(tzinfo=dt.timezone.utc)
    return dt.timedelta(0) <= now - downloaded_at < interval


def discovery_cache_covers(state: dict[str, Any], tickers: set[str]) -> bool:
    covered = state.get("discovery_cache_tickers")
    return isinstance(covered, list) and tickers <= set(covered)


def discover_candidates(
    universe: set[str], as_of: dt.date, sec_lookback_days: int
) -> tuple[list[dict[str, Any]], list[str], bool]:
    warnings: list[str] = []
    candidates: list[dict[str, Any]] = []
    successful_sources = 0
    au = {ticker for ticker in universe if ticker.endswith(".AX")}
    us = universe - au
    if au:
        try:
            candidates.extend(asx_candidates(au))
            successful_sources += 1
        except Exception as error:
            warnings.append(f"ASX discovery failed: {error}")
    if us:
        try:
            sec_events, unmapped = sec_candidates(us, as_of, sec_lookback_days)
            candidates.extend(sec_events)
            successful_sources += 1
            if unmapped:
                warnings.append("No SEC ticker/CIK mapping: " + ", ".join(unmapped))
        except Exception as error:
            warnings.append(f"SEC discovery failed: {error}")
    expected_sources = int(bool(au)) + int(bool(us))
    return candidates, warnings, successful_sources == expected_sources


def update_discovery_cache(
    state: dict[str, Any], candidates: list[dict[str, Any]],
    tickers: set[str], now: dt.datetime,
) -> None:
    downloaded_at = now.isoformat(timespec="seconds")
    state["discovery_cache"] = candidates
    state["discovery_cache_tickers"] = sorted(tickers)
    state["last_downloaded_at"] = downloaded_at
    state["last_discovered_at"] = downloaded_at


def ingest_candidates(state: dict[str, Any], candidates: list[dict[str, Any]]) -> None:
    """Merge discoveries into the durable queue without ranking or expiry."""
    acknowledged = state["acknowledged"]
    pending = state["pending"]
    for event in candidates:
        if event["event_id"] not in acknowledged:
            pending[event["event_id"]] = event


def ensure_discovery(
    args: argparse.Namespace, extra_tickers: set[str] | None = None
) -> tuple[
    dict[str, Any], dict[str, float | None], list[dict[str, Any]],
    list[str], bool, bool,
]:
    """Refresh the shared cache when needed and always ingest it into pending."""
    universe = stock_universe(args.stock_dir)
    requested = set(universe) | (extra_tickers or set())
    state = load_state(args.state)
    now = dt.datetime.now(dt.timezone.utc)
    cache_is_usable = (
        discovery_cache_is_fresh(state, now, DEFAULT_REFRESH_INTERVAL)
        and discovery_cache_covers(state, requested)
    )
    refresh = getattr(args, "force_refresh", False) or (
        not getattr(args, "cache_only", False) and not cache_is_usable
    )
    if refresh:
        candidates, warnings, refresh_completed = discover_candidates(
            requested,
            getattr(args, "as_of", dt.date.today()),
            getattr(args, "sec_lookback_days", 7),
        )
        if refresh_completed:
            update_discovery_cache(state, candidates, requested, now)
    else:
        candidates = state.get("discovery_cache", [])
        warnings = (
            ["Discovery cache is stale; --cache-only prevented refresh"]
            if getattr(args, "cache_only", False) and not cache_is_usable
            else []
        )
        refresh_completed = False
    ingest_candidates(state, candidates)
    write_state(args.state, state)
    return state, universe, candidates, warnings, refresh, refresh_completed


def prune_pending(
    state: dict[str, Any],
    universe: dict[str, float | None],
    as_of: dt.date,
    max_age_days: int,
) -> tuple[int, int]:
    """Remove invalid, expired, and out-of-scope events from the pending queue."""
    cutoff = as_of - dt.timedelta(days=max_age_days)
    expired: list[str] = []
    out_of_scope: list[str] = []
    for event_id, event in state["pending"].items():
        try:
            event_date = dt.date.fromisoformat(str(event["date"]))
        except (KeyError, TypeError, ValueError):
            expired.append(event_id)
            continue
        if event_date < cutoff:
            expired.append(event_id)
        elif event.get("ticker") not in universe:
            out_of_scope.append(event_id)

    for event_id in expired + out_of_scope:
        state["pending"].pop(event_id, None)
    return len(expired), len(out_of_scope)


def queue_candidates(
    state: dict[str, Any],
    discovered: list[dict[str, Any]],
    universe: dict[str, float | None],
    as_of: dt.date,
    max_age_days: int,
    max_candidates: int,
    qv_floor: float,
    urgency_tau_days: float,
) -> tuple[list[dict[str, Any]], int, int]:
    """Merge discoveries, expire stale items, and return the highest-priority batch."""
    acknowledged = state["acknowledged"]
    pending = state["pending"]
    for event in discovered:
        event_id = event["event_id"]
        if event_id not in acknowledged:
            pending[event_id] = event

    expired_count, _out_of_scope_count = prune_pending(
        state, universe, as_of, max_age_days
    )

    ranked = []
    for event in pending.values():
        event_date = dt.date.fromisoformat(str(event["date"]))
        age_days = max(0, (as_of - event_date).days)
        qv_score = universe[event["ticker"]]
        interest = max(qv_floor, qv_score if qv_score is not None else qv_floor)
        urgency = URGENCY_FLOOR + (1.0 - URGENCY_FLOOR) * (
            1.0 - math.exp(-age_days / urgency_tau_days)
        )
        enriched = dict(event)
        enriched.update({
            "priority": round(interest * urgency, 6),
            "qv_score": qv_score,
            "interest_score": round(interest, 6),
            "filing_age_days": age_days,
            "urgency": round(urgency, 6),
        })
        ranked.append(enriched)

    ordered = sorted(
        ranked,
        key=lambda event: (
            -event["priority"],
            -event["filing_age_days"],
            event["ticker"],
            event["event_id"],
        ),
    )
    return ordered[:max_candidates], expired_count, max(0, len(ordered) - max_candidates)


def cmd_poll(args: argparse.Namespace) -> int:
    state, universe, candidates, warnings, refresh, refresh_completed = ensure_discovery(args)

    au = {ticker for ticker in universe if ticker.endswith(".AX")}
    us = set(universe) - au

    batch, expired_count, deferred_count = queue_candidates(
        state,
        candidates,
        universe,
        args.as_of,
        args.max_age_days,
        args.max_candidates,
        args.qv_floor,
        args.urgency_tau_days,
    )
    write_state(args.state, state)
    output = {
        "as_of": args.as_of.isoformat(),
        "downloaded": refresh_completed,
        "using_cached_discovery": not refresh,
        "last_downloaded_at": state.get("last_downloaded_at"),
        "universe": {
            "count": len(universe),
            "au": len(au),
            "us": len(us),
            "missing_qv": sum(score is None for score in universe.values()),
        },
        "candidate_count": len(batch),
        "pending_count": len(state["pending"]),
        "deferred_count": deferred_count,
        "discarded_expired_count": expired_count,
        "max_candidates": args.max_candidates,
        "max_age_days": args.max_age_days,
        "priority_model": {
            "qv_floor": args.qv_floor,
            "urgency_floor": URGENCY_FLOOR,
            "urgency_tau_days": args.urgency_tau_days,
        },
        "candidates": batch,
        "warnings": warnings,
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not refresh or refresh_completed else 1


def cmd_pending(args: argparse.Namespace) -> int:
    """Refresh when needed and return complete pending counts by ticker."""
    state, universe, _, warnings, refresh, refresh_completed = ensure_discovery(args)
    expired_count, out_of_scope_count = prune_pending(
        state, universe, args.as_of, args.max_age_days
    )
    write_state(args.state, state)

    ticker_counts: dict[str, int] = {}
    for event in state["pending"].values():
        ticker = str(event["ticker"])
        ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1

    requested = set(universe)
    now = dt.datetime.now(dt.timezone.utc)
    cache_stale = not (
        discovery_cache_is_fresh(state, now, DEFAULT_REFRESH_INTERVAL)
        and discovery_cache_covers(state, requested)
    )
    output = {
        "as_of": args.as_of.isoformat(),
        "downloaded": refresh_completed,
        "using_cached_discovery": not refresh,
        "cache_stale": cache_stale,
        "last_downloaded_at": state.get("last_downloaded_at"),
        "pending_count": sum(ticker_counts.values()),
        "ticker_count": len(ticker_counts),
        "tickers": dict(sorted(ticker_counts.items())),
        "discarded_expired_count": expired_count,
        "discarded_out_of_scope_count": out_of_scope_count,
        "warnings": warnings,
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not refresh or refresh_completed else 1


def ticker_value(value: str) -> str:
    ticker = value.strip().upper()
    if not ticker or ("." in ticker and not ticker.endswith(".AX")):
        raise argparse.ArgumentTypeError(
            "ticker must be an ASX ticker ending in .AX or a US ticker without a suffix"
        )
    return ticker


def cmd_ticker(args: argparse.Namespace) -> int:
    """Return every filtered announcement currently exposed by the source feeds."""
    state, _, discovered, warnings, refresh, refresh_completed = ensure_discovery(
        args, {args.ticker}
    )
    # The source snapshot is intentionally short (ASX today/previous business day;
    # SEC lookback window), while poll retains unacknowledged discoveries for up to
    # 30 days. Merge both so ticker can return everything currently visible to poll.
    ticker_candidates = {
        event["event_id"]: event
        for event in discovered
        if event["ticker"] == args.ticker
    }
    ticker_candidates.update({
        event["event_id"]: event
        for event in state["pending"].values()
        if event.get("ticker") == args.ticker
    })
    candidates = list(ticker_candidates.values())

    candidates.sort(
        key=lambda event: (event["date"], event["event_id"]), reverse=True
    )
    output = {
        "as_of": args.as_of.isoformat(),
        "ticker": args.ticker,
        "downloaded": refresh_completed,
        "using_cached_discovery": not refresh,
        "last_downloaded_at": state.get("last_downloaded_at"),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "warnings": warnings,
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not refresh or refresh_completed else 1


def cmd_ack(args: argparse.Namespace) -> int:
    state, _, _, warnings, _, _ = ensure_discovery(args)
    acknowledged = state["acknowledged"]
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    for event_id in args.event_id:
        acknowledged[event_id] = now
        state["pending"].pop(event_id, None)

    # Bound state growth while retaining ample retry/dedup history.
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=400)
    state["acknowledged"] = {
        event_id: stamp
        for event_id, stamp in acknowledged.items()
        if dt.datetime.fromisoformat(stamp) >= cutoff
    }
    state["last_acknowledged_at"] = now
    write_state(args.state, state)
    print(json.dumps({
        "acknowledged": args.event_id,
        "state": str(args.state),
        "warnings": warnings,
    }))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--stock-dir", type=Path, default=DEFAULT_STOCK_DIR)
    result.add_argument("--state", type=Path, default=DEFAULT_STATE)
    subparsers = result.add_subparsers(dest="command", required=True)

    poll = subparsers.add_parser("poll", help="print unseen candidate metadata as JSON")
    poll.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today())
    poll.add_argument("--force-refresh", action="store_true",
                      help="download announcement metadata even when the cache is fresh")
    poll.add_argument("--sec-lookback-days", type=int, default=7)
    poll.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS,
                      help="discard queued candidates older than this many days")
    poll.add_argument("--max-candidates", type=int, default=DEFAULT_MAX_CANDIDATES,
                      help="maximum candidates returned for processing in one run")
    poll.add_argument("--qv-floor", type=float, default=DEFAULT_QV_FLOOR,
                      help="minimum interest score for missing or very low QV")
    poll.add_argument("--urgency-tau-days", type=float, default=DEFAULT_URGENCY_TAU_DAYS,
                      help="filing-age urgency time constant in days")
    poll.set_defaults(func=cmd_poll)

    pending = subparsers.add_parser(
        "pending", help="refresh when stale and print all pending ticker counts as JSON"
    )
    pending.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today())
    refresh_group = pending.add_mutually_exclusive_group()
    refresh_group.add_argument("--force-refresh", action="store_true")
    refresh_group.add_argument(
        "--cache-only", action="store_true",
        help="use queued and cached data without contacting ASX or SEC",
    )
    pending.add_argument("--sec-lookback-days", type=int, default=7)
    pending.add_argument(
        "--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS,
        help="discard queued candidates older than this many days",
    )
    pending.set_defaults(func=cmd_pending)

    ticker = subparsers.add_parser(
        "ticker", help="print all filtered announcements for one AU/US ticker"
    )
    ticker.add_argument("ticker", type=ticker_value)
    ticker.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today())
    ticker.add_argument("--force-refresh", action="store_true")
    ticker.add_argument("--sec-lookback-days", type=int, default=7)
    ticker.set_defaults(func=cmd_ticker)

    ack = subparsers.add_parser("ack", help="acknowledge candidates only after review")
    ack.add_argument("event_id", nargs="+")
    ack.set_defaults(func=cmd_ack)
    return result


def main() -> int:
    args = parser().parse_args()
    if getattr(args, "sec_lookback_days", 1) < 1:
        raise SystemExit("--sec-lookback-days must be positive")
    if getattr(args, "max_age_days", 1) < 1:
        raise SystemExit("--max-age-days must be positive")
    if getattr(args, "max_candidates", 1) < 1:
        raise SystemExit("--max-candidates must be positive")
    if not 0.0 <= getattr(args, "qv_floor", 0.0) <= 1.0:
        raise SystemExit("--qv-floor must be between 0 and 1")
    if getattr(args, "urgency_tau_days", 1.0) <= 0:
        raise SystemExit("--urgency-tau-days must be positive")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
