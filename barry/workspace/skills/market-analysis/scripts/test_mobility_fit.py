#!/usr/bin/env python3
"""Tests for mobility_fit.py extraction and kernel fitting."""

import argparse
import contextlib
import io
import random
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mobility_fit as mf

INDEX = """\
panels:
  - id: test-market
    name: Test market
    market: Test market unit shipments worldwide
    region: Global
    basis: units
    coverage: 3
    tracker: test tracker
    quality: seed-approximate
    penetration:
      logistic: {t0: 2008.0, k: 0.5}
      provenance: estimated
    players:
      Alpha:   {founded: 1980}
      Beta:    {founded: 1980}
      Gamma:   {founded: 1980, fate: acquired, fate-year: 2016, acquirer: Alpha}
      Delta:   {founded: 2015}
      Epsilon: {founded: 1990}
    sources: ["test citation"]
"""

CSV = """\
year,rank,player,share
2010,1,Alpha,0.40
2010,2,Beta,0.30
2010,3,Gamma,0.10
2020,1,Alpha,0.35
2020,2,Delta,0.30
2020,3,Epsilon,0.20
"""


class ExtractionTests(unittest.TestCase):
    def build(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = Path(tmp.name)
        (data / "panels").mkdir()
        (data / "panels.yaml").write_text(INDEX)
        (data / "panels" / "test-market.csv").write_text(CSV)
        return data

    def test_destinations_classified(self):
        obs, meta = mf.extract(self.build())
        dests = {o["player"]: o["dest"] for o in obs}
        self.assertEqual(dests, {"Alpha": 1, "Beta": "fringe", "Gamma": "gone"})
        self.assertEqual(obs[0]["curve"], 0.731)
        self.assertAlmostEqual(obs[0]["share-gap"], 0.25)
        self.assertAlmostEqual(obs[1]["share-gap"], 1 / 3)
        self.assertAlmostEqual(obs[2]["share-gap"], 2.0)

    def test_destination_origin_composition(self):
        _, meta = mf.extract(self.build())
        self.assertEqual(meta[0]["destination-origins"],
                         {"held-topk": 1, "from-outside": 1, "new-to-market": 0,
                          "not-yet-founded": 1})
        self.assertTrue(meta[0]["rank1-held"])


class KernelTests(unittest.TestCase):
    def test_row_probs_sum_to_one(self):
        for n in (1, 3, 5):
            for rho in (0.2, 0.6, 0.9):
                probs = mf.row_probs(n, 5, rho, 0.1)
                self.assertAlmostEqual(sum(probs.values()), 1.0, places=9)
                self.assertAlmostEqual(probs["gone"], 0.1, places=9)

    def test_rank_effect_raises_rho_with_depth(self):
        self.assertLess(mf.rho_of(0.0, c=0.5, origin=1), mf.rho_of(0.0, c=0.5, origin=5))

    def test_larger_share_gap_can_make_a_leader_stickier(self):
        close_rho = mf.rho_of(0.0, d=-2.0, share_gap=0.05)
        dominant_rho = mf.rho_of(0.0, d=-2.0, share_gap=0.90)
        self.assertLess(dominant_rho, close_rho)
        self.assertGreater(mf.row_probs(1, 5, dominant_rho, 0.1)[1],
                           mf.row_probs(1, 5, close_rho, 0.1)[1])

    def test_share_gaps_are_relative_to_the_origins(self):
        gaps = mf.share_gaps([0.40, 0.30, 0.20])
        self.assertAlmostEqual(gaps[0], 0.25)
        self.assertAlmostEqual(gaps[1], 1 / 3)
        self.assertAlmostEqual(gaps[2], 0.50)

    def test_fit_recovers_synthetic_parameters(self):
        rng = random.Random(7)
        true_rho, true_g = 0.6, 0.1
        obs = []
        for i in range(600):
            n = i % 5 + 1
            probs = mf.row_probs(n, 5, true_rho, true_g)
            r, acc, dest = rng.random(), 0.0, "gone"
            for key, p in probs.items():
                acc += p
                if r < acc:
                    dest = key
                    break
            obs.append({"panel": f"p{i % 3}", "coverage": 5, "curve": 0.5,
                        "origin": n, "dest": dest})
        params = mf.fit_kernel(obs)
        self.assertAlmostEqual(mf.rho_of(params["a"]), true_rho, delta=0.05)
        self.assertAlmostEqual(params["g"], true_g, delta=0.03)


class MarketDocTests(unittest.TestCase):
    def front_matter(self):
        return {
            "currency": "USD",
            "size": {"maturity-market-value": 100.0},
            "concentration": {
                "model-estimate": {"s1": 0.25, "r": 0.6},
                "override": {"s1": 0.3, "r": 0.5, "reason": "Target evidence"},
            },
            "players": {
                "inputs": {
                    "current": [
                        {"rank": 1, "name": "Alpha", "ticker": "AAA", "share": 0.5},
                        {"rank": 2, "name": "Beta", "ticker": "BBB", "share": 0.25},
                    ]
                },
                "override": [
                    {"name": "Beta", "capture": 0.12, "reason": "Company evidence"},
                    {"name": "Entrant", "ticker": "NEW", "capture": 0.04,
                     "reason": "Credible outside contender"},
                ],
            },
        }

    def prediction(self):
        return {
            "model": "share",
            "starting-shares": [0.5, 0.25],
            "relative-share-gaps": [0.5, 1.0],
            "rho": {1: 0.5, 2: 0.5},
            "g": 0.1,
            "rows": {
                1: {1: 0.5, 2: 0.2, "fringe": 0.2, "gone": 0.1},
                2: {1: 0.2, 2: 0.4, "fringe": 0.3, "gone": 0.1},
            },
            "from-outside": {1: 0.3, 2: 0.4},
        }

    def test_fringe_has_geometric_tail_value_and_gone_is_zero(self):
        capture = mf.mobility_adjusted_capture(1, 0.3, 0.5, self.prediction())

        self.assertAlmostEqual(capture, 0.19)

    def test_doc_result_reads_canonical_concentration_and_resolves_overrides(self):
        with mock.patch.object(mf, "predict_share_model", return_value=self.prediction()):
            result = mf.mobility_doc_result(self.front_matter())

        self.assertEqual(result["concentration-source"], "override")
        self.assertAlmostEqual(result["model-estimate"][0]["hold-position-capture"], 0.3)
        self.assertAlmostEqual(
            result["model-estimate"][0]["mobility-adjusted-capture"], 0.19
        )
        self.assertAlmostEqual(
            result["model-estimate"][0]["mobility-adjusted-revenue"], 19.0
        )
        canonical = {entry["name"]: entry for entry in result["canonical"]}
        self.assertEqual(canonical["Alpha"]["source"], "model-estimate")
        self.assertEqual(canonical["Beta"]["capture"], 0.12)
        self.assertEqual(canonical["Entrant"]["capture"], 0.04)
        self.assertEqual(result["gone-probability"], 0.1)

    def test_doc_result_requires_projected_market_value(self):
        front_matter = self.front_matter()
        del front_matter["size"]

        with self.assertRaisesRegex(SystemExit, "size.maturity-market-value"):
            mf.mobility_doc_result(front_matter)

    def test_write_preserves_inputs_overrides_peers_and_body(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "market.md"
        path.write_text(
            "---\n"
            "base-year: 2026\n"
            "players:\n"
            "  inputs:\n"
            "    current:\n"
            "      - {rank: 1, name: Alpha, ticker: AAA, share: 0.5}\n"
            "      - {rank: 2, name: Beta, ticker: BBB, share: 0.25}\n"
            "  override:\n"
            "    - {name: Beta, capture: 0.12, reason: Company evidence}\n"
            "unrelated: keep-me\n"
            "---\n"
            "# Market\n\nBody stays byte-for-byte.\n",
            encoding="utf-8",
        )
        result = {
            "model-estimate": [
                {"rank": 1, "name": "Alpha", "ticker": "AAA",
                 "hold-position-capture": 0.3, "mobility-adjusted-capture": 0.19,
                 "mobility-adjusted-revenue": 19.0},
                {"rank": 2, "name": "Beta", "ticker": "BBB",
                 "hold-position-capture": 0.15, "mobility-adjusted-capture": 0.16,
                 "mobility-adjusted-revenue": 16.0},
            ],
            "maturity-market-value": 100.0,
            "gone-probability": 0.1,
            "method": mf.PRODUCTION_METHOD,
        }

        mf.write_mobility_outputs(path, result, "2026-07-31")
        updated = path.read_text(encoding="utf-8")

        self.assertIn("current:", updated)
        self.assertIn("reason: Company evidence", updated)
        self.assertIn("mobility-adjusted-capture: 0.19", updated)
        self.assertIn("mobility-adjusted-revenue: 19.0", updated)
        self.assertIn("gone-probability: 0.1", updated)
        self.assertIn(f"method: {mf.PRODUCTION_METHOD}", updated)
        self.assertIn("date: 2026-07-31", updated)
        self.assertIn("unrelated: keep-me", updated)
        self.assertTrue(updated.endswith("# Market\n\nBody stays byte-for-byte.\n"))

    def test_market_doc_dry_run_does_not_write(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "market.md"
        path.write_text(
            "---\n"
            "size: {maturity-market-value: 100.0}\n"
            "concentration:\n"
            "  override: {s1: 0.3, r: 0.5, reason: Target evidence}\n"
            "players:\n"
            "  inputs:\n"
            "    current:\n"
            "      - {rank: 1, name: Alpha, ticker: AAA, share: 0.5}\n"
            "      - {rank: 2, name: Beta, ticker: BBB, share: 0.25}\n"
            "---\n"
            "# Market\n",
            encoding="utf-8",
        )
        before = path.read_text(encoding="utf-8")
        args = argparse.Namespace(
            coverage=None,
            shares=None,
            rank=None,
            model="share",
            curve_position=None,
            t0=None,
            k=None,
            year=None,
            market_doc=str(path),
            market_dir=str(path.parent),
            data_dir=str(Path(tmp.name)),
            dry_run=True,
            as_of="2026-07-31",
            json=False,
        )

        with mock.patch.object(mf, "predict_share_model", return_value=self.prediction()):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(mf.cmd_predict_market_doc(args), 0)

        self.assertEqual(path.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
