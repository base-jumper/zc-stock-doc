#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


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
                '{"version": 2, "acknowledged": {}, "pending": '
                '{"x": {"event_id": "x", "date": "2026-08-01", "ticker": "AAA"}}}',
                encoding="utf-8")
            args = type("Args", (), {"state": state_path, "event_id": ["x"]})()
            with contextlib.redirect_stdout(io.StringIO()):
                monitor.cmd_ack(args)
            state = monitor.load_state(state_path)
            self.assertNotIn("x", state["pending"])
            self.assertIn("x", state["acknowledged"])


if __name__ == "__main__":
    unittest.main()
