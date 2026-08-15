#!/usr/bin/env python3
"""Tests for the market-doc-backed TAM-capture valuation."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import tam_capture_valuation as tc


class TamCaptureValuationTests(unittest.TestCase):
    def write_market_doc(
        self,
        directory: Path,
        *,
        years: int = 10,
        revenue: float | None = 1.25,
    ) -> Path:
        revenue_line = (
            f"      mobility-adjusted-revenue: {revenue}\n" if revenue is not None else ""
        )
        path = directory / "test-market.md"
        path.write_text(
            "---\n"
            "base-year: 2026\n"
            "currency: USD\n"
            f"maturity-duration: {years}\n"
            "players:\n"
            "  model-estimate:\n"
            "    - rank: 1\n"
            "      name: Alpha Corp\n"
            "      ticker: AAA\n"
            "      mobility-adjusted-capture: 0.25\n"
            f"{revenue_line}"
            "---\n"
            "# Test Market\n",
            encoding="utf-8",
        )
        return path

    def test_compute_uses_terminal_revenue_directly(self) -> None:
        result = tc.compute(
            price=10,
            shares=100,
            years=10,
            terminal_revenue=1000,
            margin=0.2,
            exit_multiple=10,
            dilution=[0.0] * 10,
        )
        self.assertEqual(result["terminal_revenue"], 1000)
        self.assertEqual(result["terminal_equity"], 2000)
        self.assertAlmostEqual(result["annualized_roi"], 2 ** (1 / 10) - 1, places=6)

    def test_loads_ticker_revenue_and_converts_billions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.write_market_doc(directory)
            result = tc.load_market_revenue("test-market", "aaa", directory)

        self.assertEqual(result["years"], 10)
        self.assertEqual(result["projection_year"], 2036)
        self.assertEqual(result["currency"], "USD")
        self.assertEqual(result["player_name"], "Alpha Corp")
        self.assertEqual(result["terminal_revenue"], 1.25e9)

    def test_loads_player_by_exact_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.write_market_doc(directory)
            result = tc.load_market_revenue("test-market", "Alpha Corp", directory)
        self.assertEqual(result["player_ticker"], "AAA")

    def test_matching_override_is_canonical_and_can_add_outside_player(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            path = self.write_market_doc(directory)
            text = path.read_text(encoding="utf-8").replace(
                "players:\n",
                "size:\n"
                "  maturity-market-value: 410\n"
                "players:\n"
                "  override:\n"
                "    - name: Ivanhoe Mines\n"
                "      ticker: IVN.TO\n"
                "      capture: 0.008\n"
                "      reason: Outside contender\n",
            )
            path.write_text(text, encoding="utf-8")
            result = tc.load_market_revenue("test-market", "ivn.to", directory)

        self.assertEqual(result["player_name"], "Ivanhoe Mines")
        self.assertAlmostEqual(result["terminal_revenue"] / 1e9, 3.28)
        self.assertEqual(result["source"], "override")

    def test_matching_override_does_not_require_model_estimate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            path = directory / "override-only.md"
            path.write_text(
                "---\n"
                "base-year: 2026\n"
                "currency: USD\n"
                "maturity-duration: 10\n"
                "size:\n"
                "  maturity-market-value: 42\n"
                "players:\n"
                "  override:\n"
                "    - name: NGEx Minerals\n"
                "      ticker: NGEX.TO\n"
                "      capture: 0.019\n"
                "      reason: Outside contender\n"
                "---\n"
                "# Override-only market\n",
                encoding="utf-8",
            )
            result = tc.load_market_revenue("override-only", "NGEX.TO", directory)

        self.assertAlmostEqual(result["terminal_revenue"] / 1e9, 0.798)
        self.assertEqual(result["source"], "override")

    def test_rejects_non_ten_year_market_doc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.write_market_doc(directory, years=8)
            with self.assertRaisesRegex(SystemExit, "maturity-duration must be 10"):
                tc.load_market_revenue("test-market", "AAA", directory)

    def test_rejects_missing_revenue_instead_of_falling_back(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.write_market_doc(directory, revenue=None)
            with self.assertRaisesRegex(SystemExit, "mobility-adjusted-revenue"):
                tc.load_market_revenue("test-market", "AAA", directory)

    def test_rejects_legacy_tam_capture_inputs(self) -> None:
        legacy = {
            "price": 10,
            "shares": 100,
            "years": 8,
            "tam": 1000,
            "capture": 0.1,
            "margin": 0.2,
            "exit-multiple": 10,
        }
        with self.assertRaisesRegex(SystemExit, "terminal-revenue"):
            tc.resolve_inputs(legacy, source="test")

    def test_stock_doc_mode_resolves_market_doc_and_ticker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market_dir = root / "markets"
            stock_dir = root / "stocks"
            market_dir.mkdir()
            stock_dir.mkdir()
            self.write_market_doc(market_dir)
            stock_path = stock_dir / "AAA.md"
            original = (
                "---\n"
                "ticker: AAA\n"
                "valuation:\n"
                "  tam-capture:\n"
                "    market-doc: test-market\n"
                "    price: 10\n"
                "    shares: 100000000\n"
                "    margin: 20%\n"
                "    margin-basis: EBIT\n"
                "    exit-multiple: 10\n"
                "    dilution: 0\n"
                "---\n"
                "# AAA\n"
            )
            stock_path.write_text(original, encoding="utf-8")
            args = argparse.Namespace(
                stock_doc="AAA",
                stock_dir=stock_dir,
                market_dir=market_dir,
                dry_run=True,
                as_of="2026-08-01",
                format="json",
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                tc.run_doc_mode(args)

            result = json.loads(output.getvalue())
            self.assertEqual(result["holding_years"], 10)
            self.assertEqual(result["terminal_revenue"], 1.25e9)
            self.assertEqual(result["market_player"], "AAA")
            self.assertFalse(result["written"])
            self.assertEqual(stock_path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
