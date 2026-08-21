#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("stock_announcements.py")
SPEC = importlib.util.spec_from_file_location("stock_announcements", SCRIPT)
assert SPEC and SPEC.loader
monitor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(monitor)


class AsxParserTests(unittest.TestCase):
    def test_parses_price_sensitive_announcement(self) -> None:
        fixture = """
        <table><tr><th>ASX Code</th></tr><tr>
          <td>WTC</td><td>31/07/2026 <span>7:20 pm</span></td>
          <td class="pricesens"><img title="price sensitive"></td>
          <td><a href="/asx/v2/statistics/displayAnnouncement.do?display=pdf&amp;idsId=03121043">
            FY26 Results<br><span class="page">12 pages</span><span class="filesize">1MB</span>
          </a></td>
        </tr></table>
        """
        parser = monitor.AsxParser()
        parser.feed(fixture)
        self.assertEqual(len(parser.rows), 1)
        event = parser.rows[0]
        self.assertEqual(event["event_id"], "asx:03121043")
        self.assertEqual(event["ticker"], "WTC.AX")
        self.assertEqual(event["date"], "2026-07-31")
        self.assertEqual(event["title"], "FY26 Results")
        self.assertTrue(event["price_sensitive"])


class UniverseTests(unittest.TestCase):
    def test_au_us_only_with_qv_scores(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "AAA.md").write_text(
                "---\nticker: AAA\noverall:\n  qv_score: 0.4\n---\n", encoding="utf-8")
            (root / "BBB.AX.md").write_text(
                "---\nticker: BBB.AX\noverall:\n  qv_score: 0.8\n---\n", encoding="utf-8")
            (root / "CCC.L.md").write_text(
                "---\nticker: CCC.L\noverall:\n  qv_score: 1.0\n---\n", encoding="utf-8")
            self.assertEqual(monitor.stock_universe(root), {"AAA": 0.4, "BBB.AX": 0.8})


class FilterTests(unittest.TestCase):
    def test_sec_form_filter(self) -> None:
        self.assertTrue(monitor.important_sec_form("8-K/A"))
        self.assertTrue(monitor.important_sec_form("424B5"))
        self.assertFalse(monitor.important_sec_form("4"))


class QueueTests(unittest.TestCase):
    def event(self, event_id: str, date: str, ticker: str = "AAA") -> dict:
        return {"event_id": event_id, "date": date, "ticker": ticker, "title": event_id}

    def test_expires_old_items_and_limits_batch_without_losing_deferred(self) -> None:
        state = {
            "version": 2,
            "acknowledged": {"seen": "2026-08-01T00:00:00+00:00"},
            "pending": {
                "old": self.event("old", "2026-07-01"),
                "first": self.event("first", "2026-07-02"),
            },
        }
        discovered = [
            self.event("seen", "2026-07-28"),
            self.event("second", "2026-07-03"),
            self.event("third", "2026-07-04"),
            self.event("fourth", "2026-07-05"),
            self.event("fifth", "2026-07-06"),
        ]
        batch, expired, deferred = monitor.queue_candidates(
            state, discovered, {"AAA": 0.4}, dt.date(2026, 8, 1), 30, 4, 0.05, 10.0)
        self.assertEqual([event["event_id"] for event in batch],
                         ["first", "second", "third", "fourth"])
        self.assertEqual(expired, 1)
        self.assertEqual(deferred, 1)
        self.assertEqual(set(state["pending"]),
                         {"first", "second", "third", "fourth", "fifth"})

    def test_priority_combines_qv_and_filing_age(self) -> None:
        state = {"version": 2, "acknowledged": {}, "pending": {}}
        discovered = [
            self.event("high-new", "2026-08-01", "HIGH"),
            self.event("medium-week-old", "2026-07-25", "MED"),
            self.event("missing-old", "2026-07-02", "MISSING"),
        ]
        batch, expired, deferred = monitor.queue_candidates(
            state,
            discovered,
            {"HIGH": 0.8, "MED": 0.4, "MISSING": None},
            dt.date(2026, 8, 1),
            30,
            3,
            0.05,
            10.0,
        )
        self.assertEqual([event["event_id"] for event in batch],
                         ["medium-week-old", "high-new", "missing-old"])
        self.assertAlmostEqual(batch[0]["priority"], 0.251024, places=6)
        self.assertEqual(batch[0]["filing_age_days"], 7)
        self.assertEqual(batch[0]["qv_score"], 0.4)
        self.assertAlmostEqual(batch[0]["urgency"], 0.627561, places=6)
        self.assertEqual(batch[2]["interest_score"], 0.05)
        self.assertEqual(expired, 0)
        self.assertEqual(deferred, 0)

    def test_ack_removes_pending_item(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            state_path = Path(temp) / "state.json"
            state_path.write_text(
                json.dumps({
                    "version": 2,
                    "acknowledged": {},
                    "pending": {"x": {
                        "event_id": "x", "date": "2026-08-01", "ticker": "AAA",
                    }},
                    "last_downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "discovery_cache": [],
                    "discovery_cache_tickers": [],
                }),
                encoding="utf-8")
            args = type("Args", (), {
                "state": state_path, "stock_dir": Path(temp), "event_id": ["x"],
            })()
            with contextlib.redirect_stdout(io.StringIO()):
                monitor.cmd_ack(args)
            state = monitor.load_state(state_path)
            self.assertNotIn("x", state["pending"])
            self.assertIn("x", state["acknowledged"])


class DiscoveryCacheTests(unittest.TestCase):
    def test_cache_is_fresh_for_two_hours(self) -> None:
        now = dt.datetime(2026, 8, 21, 12, tzinfo=dt.timezone.utc)
        state = {
            "last_downloaded_at": "2026-08-21T10:00:01+00:00",
            "discovery_cache": [],
        }
        self.assertTrue(monitor.discovery_cache_is_fresh(
            state, now, dt.timedelta(hours=2)))
        state["last_downloaded_at"] = "2026-08-21T10:00:00+00:00"
        self.assertFalse(monitor.discovery_cache_is_fresh(
            state, now, dt.timedelta(hours=2)))

    def test_poll_skips_web_discovery_when_cache_is_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state_path = root / "state.json"
            now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
            state_path.write_text(json.dumps({
                "version": 2,
                "acknowledged": {},
                "pending": {},
                "last_downloaded_at": now,
                "discovery_cache": [],
                "discovery_cache_tickers": ["AAA"],
            }), encoding="utf-8")
            args = type("Args", (), {
                "stock_dir": root,
                "state": state_path,
                "force_refresh": False,
                "as_of": dt.date.today(),
                "sec_lookback_days": 7,
                "max_age_days": 30,
                "max_candidates": 4,
                "qv_floor": 0.05,
                "urgency_tau_days": 10.0,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={"AAA": 0.5}), \
                    mock.patch.object(monitor, "sec_candidates") as discover, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_poll(args), 0)
            discover.assert_not_called()
            output = json.loads(stdout.getvalue())
            self.assertTrue(output["using_cached_discovery"])
            self.assertFalse(output["downloaded"])

    def test_force_refresh_bypasses_fresh_cache(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state_path = root / "state.json"
            state_path.write_text(json.dumps({
                "version": 2,
                "acknowledged": {},
                "pending": {},
                "last_downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }), encoding="utf-8")
            args = type("Args", (), {
                "stock_dir": root,
                "state": state_path,
                "force_refresh": True,
                "as_of": dt.date.today(),
                "sec_lookback_days": 7,
                "max_age_days": 30,
                "max_candidates": 4,
                "qv_floor": 0.05,
                "urgency_tau_days": 10.0,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={"AAA": 0.5}), \
                    mock.patch.object(monitor, "sec_candidates", return_value=([], [])) as discover, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_poll(args), 0)
            discover.assert_called_once()
            output = json.loads(stdout.getvalue())
            self.assertFalse(output["using_cached_discovery"])
            self.assertTrue(output["downloaded"])


class PendingCommandTests(unittest.TestCase):
    def test_returns_all_ticker_counts_and_prunes_queue(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            as_of = dt.date.today()
            current = as_of.isoformat()
            expired = (as_of - dt.timedelta(days=31)).isoformat()
            events = {
                "a1": {"event_id": "a1", "ticker": "AAA", "date": current},
                "a2": {"event_id": "a2", "ticker": "AAA", "date": current},
                "old": {"event_id": "old", "ticker": "AAA", "date": expired},
                "out": {"event_id": "out", "ticker": "OUT", "date": current},
            }
            state_path = root / "state.json"
            state_path.write_text(json.dumps({
                "version": 2,
                "acknowledged": {},
                "pending": events,
                "last_downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "discovery_cache": [],
                "discovery_cache_tickers": ["AAA"],
            }), encoding="utf-8")
            args = type("Args", (), {
                "stock_dir": root,
                "state": state_path,
                "force_refresh": False,
                "cache_only": False,
                "as_of": as_of,
                "sec_lookback_days": 7,
                "max_age_days": 30,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={"AAA": 0.5}), \
                    mock.patch.object(monitor, "discover_candidates") as discover, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_pending(args), 0)
            discover.assert_not_called()
            output = json.loads(stdout.getvalue())
            self.assertEqual(output["tickers"], {"AAA": 2})
            self.assertEqual(output["pending_count"], 2)
            self.assertEqual(output["discarded_expired_count"], 1)
            self.assertEqual(output["discarded_out_of_scope_count"], 1)
            self.assertEqual(set(monitor.load_state(state_path)["pending"]), {"a1", "a2"})

    def test_refreshes_stale_cache_and_ingests_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            event = {
                "event_id": "new", "ticker": "AAA",
                "date": dt.date.today().isoformat(),
            }
            args = type("Args", (), {
                "stock_dir": root,
                "state": root / "state.json",
                "force_refresh": False,
                "cache_only": False,
                "as_of": dt.date.today(),
                "sec_lookback_days": 7,
                "max_age_days": 30,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={"AAA": 0.5}), \
                    mock.patch.object(
                        monitor, "discover_candidates", return_value=([event], [], True)
                    ) as discover, contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_pending(args), 0)
            discover.assert_called_once()
            output = json.loads(stdout.getvalue())
            self.assertTrue(output["downloaded"])
            self.assertFalse(output["cache_stale"])
            self.assertEqual(output["tickers"], {"AAA": 1})

    def test_cache_only_uses_stale_queue_without_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            event = {
                "event_id": "queued", "ticker": "AAA",
                "date": dt.date.today().isoformat(),
            }
            state_path = root / "state.json"
            state_path.write_text(json.dumps({
                "version": 2,
                "acknowledged": {},
                "pending": {"queued": event},
            }), encoding="utf-8")
            args = type("Args", (), {
                "stock_dir": root,
                "state": state_path,
                "force_refresh": False,
                "cache_only": True,
                "as_of": dt.date.today(),
                "sec_lookback_days": 7,
                "max_age_days": 30,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={"AAA": 0.5}), \
                    mock.patch.object(monitor, "discover_candidates") as discover, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_pending(args), 0)
            discover.assert_not_called()
            output = json.loads(stdout.getvalue())
            self.assertTrue(output["using_cached_discovery"])
            self.assertTrue(output["cache_stale"])
            self.assertEqual(output["tickers"], {"AAA": 1})
            self.assertTrue(output["warnings"])


class TickerCommandTests(unittest.TestCase):
    def test_returns_every_filtered_candidate_without_queue_limit(self) -> None:
        candidates = [
            {"event_id": f"asx:{number}", "ticker": "PLS.AX",
             "date": f"2026-08-{number:02d}", "title": str(number)}
            for number in range(1, 7)
        ]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = type("Args", (), {
                "ticker": "PLS.AX",
                "stock_dir": root,
                "state": root / "state.json",
                "force_refresh": False,
                "as_of": dt.date(2026, 8, 21),
                "sec_lookback_days": 7,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={}), \
                    mock.patch.object(monitor, "asx_candidates", return_value=candidates) as discover, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_ticker(args), 0)
            discover.assert_called_once_with({"PLS.AX"})
            output = json.loads(stdout.getvalue())
        self.assertEqual(output["candidate_count"], 6)
        self.assertEqual([item["event_id"] for item in output["candidates"]],
                         ["asx:6", "asx:5", "asx:4", "asx:3", "asx:2", "asx:1"])

    def test_uses_shared_cache_when_ticker_is_covered(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            event = {"event_id": "asx:1", "ticker": "PLS.AX",
                     "date": "2026-08-21", "title": "Results"}
            state_path = root / "state.json"
            state_path.write_text(json.dumps({
                "version": 2,
                "acknowledged": {},
                "pending": {},
                "last_downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "discovery_cache": [event],
                "discovery_cache_tickers": ["PLS.AX"],
            }), encoding="utf-8")
            args = type("Args", (), {
                "ticker": "PLS.AX",
                "stock_dir": root,
                "state": state_path,
                "force_refresh": False,
                "as_of": dt.date.today(),
                "sec_lookback_days": 7,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={"PLS.AX": 0.5}), \
                    mock.patch.object(monitor, "discover_candidates") as discover, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_ticker(args), 0)
            discover.assert_not_called()
            output = json.loads(stdout.getvalue())
            self.assertTrue(output["using_cached_discovery"])
            self.assertEqual(output["candidates"], [event])

    def test_includes_older_candidates_retained_in_pending_queue(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pending = {"event_id": "asx:old", "ticker": "CSL.AX",
                       "date": "2026-08-18", "title": "FY2026 Results"}
            state_path = root / "state.json"
            state_path.write_text(json.dumps({
                "version": 2,
                "acknowledged": {},
                "pending": {pending["event_id"]: pending},
                "last_downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "discovery_cache": [],
                "discovery_cache_tickers": ["CSL.AX"],
            }), encoding="utf-8")
            args = type("Args", (), {
                "ticker": "CSL.AX",
                "stock_dir": root,
                "state": state_path,
                "force_refresh": False,
                "as_of": dt.date.today(),
                "sec_lookback_days": 7,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={"CSL.AX": 0.5}), \
                    mock.patch.object(monitor, "discover_candidates") as discover, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(monitor.cmd_ticker(args), 0)
            discover.assert_not_called()
            output = json.loads(stdout.getvalue())
            self.assertEqual(output["candidates"], [pending])

    def test_ticker_argument_is_case_insensitive(self) -> None:
        args = monitor.parser().parse_args(["ticker", "pls.ax"])
        self.assertEqual(args.ticker, "PLS.AX")

    def test_ticker_refresh_ingests_candidates_into_pending(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            event = {"event_id": "asx:new", "ticker": "PLS.AX",
                     "date": "2026-08-21", "title": "Results"}
            args = type("Args", (), {
                "ticker": "PLS.AX",
                "stock_dir": root,
                "state": root / "state.json",
                "force_refresh": False,
                "as_of": dt.date.today(),
                "sec_lookback_days": 7,
            })()
            with mock.patch.object(monitor, "stock_universe", return_value={}), \
                    mock.patch.object(monitor, "discover_candidates",
                                      return_value=([event], [], True)), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(monitor.cmd_ticker(args), 0)
            state = monitor.load_state(args.state)
            self.assertEqual(state["pending"], {event["event_id"]: event})


if __name__ == "__main__":
    unittest.main()
