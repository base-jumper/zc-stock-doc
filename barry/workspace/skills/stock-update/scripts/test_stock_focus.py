#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("stock_focus.py")
SPEC = importlib.util.spec_from_file_location("stock_focus", SCRIPT)
assert SPEC and SPEC.loader
focus = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(focus)


class PriorityTests(unittest.TestCase):
    def test_no_announcement_matches_original_formula(self) -> None:
        qv = 0.4
        confidence = 0.7
        stale = 0.6
        expected = (qv**1.2) * ((1.0 - confidence) ** 0.8) * (stale**1.1)
        actual = focus.focus_priority(
            qv,
            confidence,
            stale,
            wq=1.2,
            wc=0.8,
            ws=1.1,
            has_pending_announcement=False,
            announcement_weight=0.2,
        )
        self.assertAlmostEqual(actual, expected)

    def test_announcement_consumes_attention_headroom(self) -> None:
        actual = focus.focus_priority(
            0.4,
            0.7,
            0.5,
            wq=1.0,
            wc=1.0,
            ws=1.0,
            has_pending_announcement=True,
            announcement_weight=0.2,
        )
        self.assertAlmostEqual(actual, 0.4 * (1.0 - (1.0 - 0.15) * 0.8))


class AnnouncementCommandTests(unittest.TestCase):
    def test_uses_valid_queue_when_refresh_returns_nonzero(self) -> None:
        payload = {
            "tickers": {"AAA": 2},
            "warnings": ["SEC discovery failed"],
        }
        completed = subprocess.CompletedProcess(
            ["stock_announcements"], 1, stdout=json.dumps(payload), stderr=""
        )
        with mock.patch.object(focus.subprocess, "run", return_value=completed) as run:
            counts, warnings = focus.load_pending_announcements(
                Path("stocks"),
                Path("state.json"),
                dt.date(2026, 8, 21),
                cache_only=False,
                force_refresh=False,
            )
        self.assertEqual(counts, {"AAA": 2})
        self.assertEqual(len(warnings), 2)
        self.assertEqual(
            run.call_args.args[0],
            [
                "stock_announcements",
                "--stock-dir", "stocks",
                "--state", "state.json",
                "pending", "--as-of", "2026-08-21",
            ],
        )


class MainTests(unittest.TestCase):
    def test_pending_announcement_promotes_stock_and_is_displayed(self) -> None:
        documents = [
            {
                "ticker": "AAA",
                "company": "Alpha",
                "watching": True,
                "last-updated": "2026-08-21",
                "analysis-strategy": "chosen",
                "strategies": {"chosen": {"confidence": 0.8}},
                "overall": {"qv_score": 0.4},
            },
            {
                "ticker": "BBB",
                "company": "Beta",
                "watching": True,
                "last-updated": "2026-08-20",
                "analysis-strategy": "chosen",
                "strategies": {"chosen": {"confidence": 0.5}},
                "overall": {"qv_score": 0.8},
            },
        ]
        argv = ["stock_focus.py", "list", "--today", "2026-08-21"]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(focus, "load_frontmatter", return_value=documents), \
                mock.patch.object(
                    focus, "load_pending_announcements", return_value=({"AAA": 1}, [])
                ), contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(focus.main(), 0)
        lines = stdout.getvalue().splitlines()
        self.assertTrue(lines[0].startswith("AAA\t"))
        self.assertIn("pending=1", lines[0])
        self.assertIn("pending=0", lines[1])

    def test_zero_weight_skips_announcement_command(self) -> None:
        argv = ["stock_focus.py", "list", "--today", "2026-08-21", "--wa", "0"]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(focus, "load_frontmatter", return_value=[]), \
                mock.patch.object(focus, "load_pending_announcements") as pending, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(focus.main(), 0)
        pending.assert_not_called()

    def test_peek_prints_exactly_the_top_ticker(self) -> None:
        documents = [
            {
                "ticker": "AAA",
                "company": "Alpha",
                "watching": True,
                "last-updated": "2026-08-21",
                "analysis-strategy": "chosen",
                "strategies": {"chosen": {"confidence": 0.8}},
                "overall": {"qv_score": 0.4},
            },
            {
                "ticker": "BBB",
                "company": "Beta",
                "watching": True,
                "last-updated": "2026-08-20",
                "analysis-strategy": "chosen",
                "strategies": {"chosen": {"confidence": 0.5}},
                "overall": {"qv_score": 0.8},
            },
        ]
        argv = ["stock_focus.py", "peek", "--today", "2026-08-21"]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(focus, "load_frontmatter", return_value=documents), \
                mock.patch.object(
                    focus, "load_pending_announcements", return_value=({}, [])
                ), contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(focus.main(), 0)
        self.assertEqual(stdout.getvalue().splitlines(), ["BBB"])

    def test_peek_prints_nothing_when_no_stock_eligible(self) -> None:
        argv = ["stock_focus.py", "peek", "--today", "2026-08-21", "--wa", "0"]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(focus, "load_frontmatter", return_value=[]), \
                mock.patch.object(focus, "load_pending_announcements") as pending, \
                contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(focus.main(), 1)
        self.assertEqual(stdout.getvalue(), "")
        pending.assert_not_called()


if __name__ == "__main__":
    unittest.main()
