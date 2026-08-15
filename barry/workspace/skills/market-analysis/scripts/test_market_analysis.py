#!/usr/bin/env python3
"""Tests for the dependency-aware market-doc refresh command."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import market_analysis as ma  # noqa: E402


TRAITS = (
    "network-effects",
    "data-scale-advantage",
    "brand-reputation",
    "capital-intensity",
    "scale-economies",
    "regulatory-barriers",
    "switching-costs",
)


class RefreshTests(unittest.TestCase):
    def build_doc(self, *, with_penetration: bool = False) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "test-market.md"
        penetration = ""
        if with_penetration:
            (path.parent / "adoption.csv").write_text(
                "year,value\n2025,0.1\n", encoding="utf-8"
            )
            penetration = """\
penetration:
  inputs:
    target-series: adoption.csv
    measure: stock
    ceiling: 0.8
    analogs: [analog-one, analog-two]
  model-estimate: {L: 0.7, t0: 2030.0, k: 0.3}
  method: logistic-blend
  date: 2026-01-01
"""
        traits = "\n".join(
            f"      {trait}: {{score: 0.5, confidence: 0.8}}" for trait in TRAITS
        )
        path.write_text(
            f"""\
---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 1.0
  maturity-market-value: 2.0
{penetration}concentration:
  inputs:
    traits:
{traits}
  model-estimate: {{s1: 0.1, r: 0.5}}
  hhi: 0.013333
  method: selected-direct-ridge
  date: 2026-01-01
players:
  inputs:
    current:
      - {{rank: 1, name: Alpha, ticker: AAA, share: 0.4}}
      - {{rank: 2, name: Beta, ticker: BBB, share: 0.25}}
  model-estimate:
    - {{rank: 1, name: Alpha, ticker: AAA, hold-position-capture: 0.1, mobility-adjusted-capture: 0.08, mobility-adjusted-revenue: 0.16}}
    - {{rank: 2, name: Beta, ticker: BBB, hold-position-capture: 0.05, mobility-adjusted-capture: 0.04, mobility-adjusted-revenue: 0.08}}
  gone-probability: 0.1
  method: share-gap-mobility-weighted-geometric-capture
  date: 2026-01-01
---
# Test Market

Body must be preserved.
""",
            encoding="utf-8",
        )
        return path

    @staticmethod
    def concentration_result() -> dict:
        return {
            "model-estimate": {"s1": 0.2, "r": 0.6},
            "selected": {"s1": 0.2, "r": 0.6},
            "selected-from": "model-estimate",
            "hhi": 0.0625,
            "method": "selected-direct-ridge",
        }

    @staticmethod
    def mobility_result(gone_probability: float = 0.1) -> dict:
        estimates = [
            {
                "rank": 1,
                "name": "Alpha",
                "ticker": "AAA",
                "hold-position-capture": 0.2,
                "mobility-adjusted-capture": 0.16,
                "mobility-adjusted-revenue": 0.32,
            },
            {
                "rank": 2,
                "name": "Beta",
                "ticker": "BBB",
                "hold-position-capture": 0.12,
                "mobility-adjusted-capture": 0.1,
                "mobility-adjusted-revenue": 0.2,
            },
        ]
        return {
            "model-estimate": estimates,
            "canonical": estimates,
            "maturity-market-value": 2.0,
            "gone-probability": gone_probability,
            "method": ma.mobility.PRODUCTION_METHOD,
            "concentration-source": "model-estimate",
        }

    @staticmethod
    def penetration_result() -> dict:
        estimate = {"L": 0.8, "t0": 2031.0, "k": 0.4}
        return {
            "model-estimate": estimate,
            "selected": estimate,
            "selected-from": "model-estimate",
            "w-fit": 0.5,
            "projection": {2026: 0.095362, 2036: 0.704638},
            "method": ma.penetration.PRODUCTION_METHOD,
        }

    def run_refresh(
        self,
        path: Path,
        *,
        dry_run: bool,
        mobility_result: dict | None = None,
    ) -> dict:
        expected = self.concentration_result()
        result = mobility_result or self.mobility_result()

        def calculate_mobility(front_matter: dict, _data_dir: Path) -> dict:
            self.assertEqual(
                front_matter["concentration"]["model-estimate"],
                expected["model-estimate"],
            )
            self.assertEqual(front_matter["concentration"]["hhi"], expected["hhi"])
            return result

        with (
            mock.patch.object(ma.concentration, "load_index", return_value={}),
            mock.patch.object(ma.concentration, "calibrate_models", return_value={}),
            mock.patch.object(
                ma.concentration, "concentration_doc_result", return_value=expected
            ),
            mock.patch.object(
                ma.penetration,
                "penetration_doc_result",
                return_value=self.penetration_result(),
            ),
            mock.patch.object(
                ma.mobility, "mobility_doc_result", side_effect=calculate_mobility
            ),
        ):
            return ma.refresh_market_doc(path, "2026-07-31", dry_run)

    def test_dry_run_feeds_new_concentration_to_mobility_without_writing(self) -> None:
        path = self.build_doc()
        original = path.read_text(encoding="utf-8")

        result = self.run_refresh(path, dry_run=True)

        self.assertEqual(result["steps"]["concentration"], "calculated")
        self.assertEqual(result["steps"]["penetration"], "skipped: no penetration.inputs")
        self.assertEqual(result["steps"]["mobility"], "calculated")
        self.assertEqual(result["validation-errors"], [])
        self.assertFalse(result["written"])
        self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_write_updates_all_outputs_together_and_preserves_body(self) -> None:
        path = self.build_doc(with_penetration=True)

        result = self.run_refresh(path, dry_run=False)

        _, front_matter = ma.concentration.split_front_matter(
            path.read_text(encoding="utf-8")
        )
        self.assertTrue(result["written"])
        self.assertEqual(result["steps"]["penetration"], "calculated")
        self.assertEqual(
            front_matter["concentration"]["model-estimate"], {"s1": 0.2, "r": 0.6}
        )
        self.assertEqual(
            front_matter["penetration"]["model-estimate"],
            {"L": 0.8, "t0": 2031.0, "k": 0.4},
        )
        self.assertEqual(
            front_matter["players"]["model-estimate"][0][
                "mobility-adjusted-capture"
            ],
            0.16,
        )
        self.assertEqual(
            front_matter["players"]["model-estimate"][0][
                "mobility-adjusted-revenue"
            ],
            0.32,
        )
        self.assertEqual(str(front_matter["players"]["date"]), "2026-07-31")
        self.assertIn("Body must be preserved.", path.read_text(encoding="utf-8"))
        self.assertEqual(ma.market_doc.validate_market_doc(path), [])

    def test_prospective_validation_failure_does_not_write(self) -> None:
        path = self.build_doc()
        original = path.read_text(encoding="utf-8")

        result = self.run_refresh(
            path, dry_run=False, mobility_result=self.mobility_result(gone_probability=2.0)
        )

        self.assertFalse(result["written"])
        self.assertTrue(result["validation-errors"])
        self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_writer_failure_does_not_partially_update_original(self) -> None:
        path = self.build_doc()
        original = path.read_text(encoding="utf-8")

        with mock.patch.object(
            ma.mobility,
            "write_mobility_outputs",
            side_effect=RuntimeError("simulated writer failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "simulated writer failure"):
                self.run_refresh(path, dry_run=False)

        self.assertEqual(path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
