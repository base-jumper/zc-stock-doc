from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from concentration_fit import (  # noqa: E402
    PRODUCTION_TRAITS,
    RidgeModel,
    concentration_doc_result,
    concentration_ratio,
    dominance_index,
    fit_calibration_entry,
    fit_geometric_moments,
    hhi,
    load_moments,
    predict_parameters,
    upsert_concentration_child,
    write_concentration_outputs,
)
from concentration_census import synthetic_share_rows  # noqa: E402


class AggregateMomentFitTests(unittest.TestCase):
    def test_production_model_predicts_s1_and_r_directly(self) -> None:
        models = {
            "s1_model": RidgeModel([0.0] * 3, [1.0] * 3, [0.20, 0.10, 0.05, -0.02]),
            "r_model": RidgeModel([0.0] * 3, [1.0] * 3, [0.80, -0.10, -0.05, 0.02]),
        }
        traits = dict(zip(PRODUCTION_TRAITS, (0.5, 0.6, 0.4)))

        s1, r = predict_parameters(models, traits)

        self.assertAlmostEqual(s1, 0.272)
        self.assertAlmostEqual(r, 0.728)

    def test_dominance_index_uses_noisy_or(self) -> None:
        traits = {
            "network-effects": 0.5,
            "data-scale-advantage": 0.2,
            "brand-reputation": 0.25,
        }

        self.assertAlmostEqual(dominance_index(traits), 0.7)

    def test_recovers_exact_geometric_parameters(self) -> None:
        s1, r = 0.24, 0.67
        moment = {
            "hhi": hhi(s1, r),
            **{
                f"cr{rank}": concentration_ratio(rank, s1, r)
                for rank in (4, 8, 20, 50)
            },
        }

        fit = fit_geometric_moments(moment)

        self.assertAlmostEqual(fit["s1"], s1, places=4)
        self.assertAlmostEqual(fit["r"], r, places=4)
        self.assertAlmostEqual(fit["hhi"], moment["hhi"], places=12)
        self.assertLess(fit["top_cr_rmse"], 1e-5)
        self.assertLess(fit["tail_cr_rmse"], 1e-5)

    def test_holds_tail_out_of_parameter_fit(self) -> None:
        s1, r = 0.20, 0.70
        moment = {
            "hhi": hhi(s1, r),
            "cr4": concentration_ratio(4, s1, r),
            "cr8": concentration_ratio(8, s1, r),
            "cr20": min(concentration_ratio(20, s1, r) + 0.10, 1.0),
            "cr50": min(concentration_ratio(50, s1, r) + 0.20, 1.0),
        }

        fit = fit_geometric_moments(moment)

        self.assertAlmostEqual(fit["s1"], s1, places=4)
        self.assertAlmostEqual(fit["r"], r, places=4)
        self.assertLess(fit["top_cr_rmse"], 1e-5)
        self.assertGreater(fit["tail_cr_rmse"], 0.05)

    def test_calibration_entry_loads_synthetic_shares(self) -> None:
        s1, r = 0.18, 0.75
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            shares_dir = data_dir / "shares"
            shares_dir.mkdir()
            path = shares_dir / "example.csv"
            with open(path, "w", newline="") as fh:
                fh.write("# synthetic-geometric-shares\n")
                writer = csv.writer(fh)
                writer.writerow(("rank", "share"))
                for rank in range(1, 80):
                    writer.writerow((rank, s1 * r ** (rank - 1)))
            entry = {
                "id": "example",
                "outcome-quality": "synthetic-geometric-shares",
            }

            fit = fit_calibration_entry(entry, data_dir)

            self.assertAlmostEqual(fit["s1"], s1, places=4)
            self.assertAlmostEqual(fit["r"], r, places=4)
            self.assertTrue(fit["synthetic"])
            self.assertFalse(fit["shape_validation_eligible"])

    def test_synthetic_shares_round_trip_moment_fit(self) -> None:
        s1, r = 0.20, 0.70
        moment = {
            "id": "example",
            "firm_count": 100,
            "hhi": hhi(s1, r),
            **{
                f"cr{rank}": concentration_ratio(rank, s1, r)
                for rank in (4, 8, 20, 50)
            },
        }

        rows, diagnostics = synthetic_share_rows(moment)
        round_trip = diagnostics["round_trip"]

        self.assertGreater(len(rows), 10)
        self.assertAlmostEqual(round_trip["s1"], s1, places=6)
        self.assertAlmostEqual(round_trip["r"], r, places=5)
        self.assertLess(diagnostics["omitted_hhi_fraction"], 1e-9)


class MarketDocModeTests(unittest.TestCase):
    def models(self) -> dict:
        return {
            "type": "test-ridge",
            "n": 10,
            "s1_model": RidgeModel([0.0] * 3, [1.0] * 3, [0.20, 0.10, 0.05, -0.02]),
            "r_model": RidgeModel([0.0] * 3, [1.0] * 3, [0.80, -0.10, -0.05, 0.02]),
        }

    def front_matter(self, override: dict | None = None) -> dict:
        traits = {
            trait: {"score": 0.5, "confidence": 0.8}
            for trait in (
                "network-effects",
                "data-scale-advantage",
                "brand-reputation",
                "capital-intensity",
                "scale-economies",
                "regulatory-barriers",
                "switching-costs",
            )
        }
        concentration = {"inputs": {"traits": traits}}
        if override is not None:
            concentration["override"] = override
        return {"concentration": concentration}

    def test_model_estimate_is_canonical_without_override(self) -> None:
        result = concentration_doc_result(self.models(), self.front_matter())

        self.assertEqual(result["selected-from"], "model-estimate")
        self.assertEqual(result["selected"], result["model-estimate"])
        self.assertAlmostEqual(
            result["hhi"],
            hhi(result["selected"]["s1"], result["selected"]["r"]),
        )

    def test_override_is_canonical_and_model_estimate_is_preserved(self) -> None:
        result = concentration_doc_result(
            self.models(),
            self.front_matter({"s1": 0.32, "r": 0.60, "reason": "Target-specific evidence"}),
        )

        self.assertEqual(result["selected-from"], "override")
        self.assertEqual(result["selected"], {"s1": 0.32, "r": 0.60})
        self.assertNotEqual(result["selected"], result["model-estimate"])
        self.assertAlmostEqual(result["hhi"], hhi(0.32, 0.60))

    def test_surgical_upsert_preserves_inputs_and_override(self) -> None:
        block = """\
base-year: 2026
concentration:
  inputs:
    traits:
      network-effects: {score: 0.5, confidence: 0.8}
  override:
    s1: 0.32
    r: 0.60
    reason: Keep this analyst note
  hhi: 0.0
players:
  capture: []
"""
        updated = upsert_concentration_child(
            block, "model-estimate", {"s1": 0.28, "r": 0.64}
        )
        updated = upsert_concentration_child(updated, "hhi", "0.086")

        self.assertIn("reason: Keep this analyst note", updated)
        self.assertIn("network-effects: {score: 0.5, confidence: 0.8}", updated)
        self.assertIn("model-estimate:\n    s1: 0.28\n    r: 0.64", updated)
        self.assertIn("  hhi: 0.086", updated)
        self.assertEqual(updated.count("  hhi:"), 1)
        self.assertIn("players:\n  capture: []", updated)

    def test_write_outputs_preserves_body_and_analyst_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "market.md"
            path.write_text(
                "---\n"
                "base-year: 2026\n"
                "concentration:\n"
                "  inputs: {traits: keep}\n"
                "  override: {s1: 0.3, r: 0.6, reason: Keep}\n"
                "---\n"
                "# Market\n\nBody stays.\n"
            )
            result = {
                "model-estimate": {"s1": 0.28, "r": 0.64},
                "hhi": hhi(0.3, 0.6),
                "method": "test-ridge",
            }

            write_concentration_outputs(path, result, "2026-07-27")
            text = path.read_text()

            self.assertIn("inputs: {traits: keep}", text)
            self.assertIn("override: {s1: 0.3, r: 0.6, reason: Keep}", text)
            self.assertIn("model-estimate:\n    s1: 0.28\n    r: 0.64", text)
            self.assertIn("method: test-ridge", text)
            self.assertTrue(text.endswith("# Market\n\nBody stays.\n"))


if __name__ == "__main__":
    unittest.main()
