#!/usr/bin/env python3
"""Tests for mobility_panels.py corpus validation."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mobility_panels as mp

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
      Alpha: {founded: 1980}
      Beta:  {founded: 1990}
      Gamma: {founded: 2000}
      Delta: {founded: 1970, fate: exited, fate-year: 2015}
    sources: ["test citation"]
"""

CSV = """\
year,rank,player,share
2010,1,Alpha,0.40
2010,2,Beta,0.30
2010,3,Delta,0.10
2020,1,Beta,0.35
2020,2,Alpha,0.30
2020,3,Gamma,0.20
"""


class CorpusValidationTests(unittest.TestCase):
    def build(self, index=INDEX, csv_text=CSV, csv_name="test-market.csv"):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = Path(tmp.name)
        (data / "panels").mkdir()
        (data / "panels.yaml").write_text(index)
        (data / "panels" / csv_name).write_text(csv_text)
        return data

    def test_valid_corpus_passes(self):
        errors, warnings, infos = mp.validate_corpus(self.build())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(infos[0]["windows"], 1)
        self.assertEqual(infos[0]["players"], 4)

    def test_rank_gap_is_error(self):
        bad = CSV.replace("2020,2,Alpha,0.30\n", "")
        errors, _, _ = mp.validate_corpus(self.build(csv_text=bad))
        self.assertTrue(any("contiguous" in e for e in errors))

    def test_unknown_player_is_error(self):
        bad = CSV.replace("2020,3,Gamma,0.20", "2020,3,Zeta,0.20")
        errors, _, _ = mp.validate_corpus(self.build(csv_text=bad))
        self.assertTrue(any("'Zeta' not in the panels.yaml players map" in e for e in errors))

    def test_share_sum_over_one_is_error(self):
        bad = CSV.replace("2020,1,Beta,0.35", "2020,1,Beta,0.95")
        errors, _, _ = mp.validate_corpus(self.build(csv_text=bad))
        self.assertTrue(any("sum to" in e for e in errors))

    def test_short_span_warns(self):
        csv_text = "\n".join(CSV.splitlines()[:4]) + "\n"
        errors, warnings, infos = mp.validate_corpus(self.build(csv_text=csv_text))
        self.assertEqual(errors, [])
        self.assertTrue(any("no usable window" in w for w in warnings))
        self.assertEqual(infos[0]["windows"], 0)

    def test_acquired_requires_acquirer(self):
        index = INDEX.replace("fate: exited, fate-year: 2015", "fate: acquired, fate-year: 2015")
        errors, _, _ = mp.validate_corpus(self.build(index=index))
        self.assertTrue(any("requires 'acquirer'" in e for e in errors))

    def test_orphan_csv_is_error(self):
        data = self.build()
        (data / "panels" / "orphan.csv").write_text(CSV)
        errors, _, _ = mp.validate_corpus(data)
        self.assertTrue(any("no panels.yaml entry" in e for e in errors))

    def test_curve_position_reported(self):
        _, _, infos = mp.validate_corpus(self.build())
        positions = infos[0]["curve-position"]
        self.assertAlmostEqual(positions[2010], 0.731, places=3)
        self.assertAlmostEqual(positions[2020], 0.998, places=3)

    def test_bad_penetration_provenance_is_error(self):
        index = INDEX.replace("provenance: estimated", "provenance: guessed")
        errors, _, _ = mp.validate_corpus(self.build(index=index))
        self.assertTrue(any("penetration.provenance" in e for e in errors))

    def test_nonpositive_k_is_error(self):
        index = INDEX.replace("k: 0.5", "k: -0.5")
        errors, _, infos = mp.validate_corpus(self.build(index=index))
        self.assertTrue(any("penetration.logistic.k" in e for e in errors))
        self.assertNotIn("curve-position", infos[0])

    def test_count_windows(self):
        self.assertEqual(mp.count_windows([2010, 2020]), 1)
        self.assertEqual(mp.count_windows([2015, 2020]), 0)
        self.assertEqual(mp.count_windows(list(range(1996, 2025))), 2)


if __name__ == "__main__":
    unittest.main()
