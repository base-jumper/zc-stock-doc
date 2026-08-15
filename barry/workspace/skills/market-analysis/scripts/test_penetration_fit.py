from __future__ import annotations

import argparse
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from penetration_fit import (  # noqa: E402
    DATA_DIR,
    cmd_blend_market_doc,
    penetration_doc_result,
    write_penetration_outputs,
)


class PenetrationMarketDocTests(unittest.TestCase):
    def make_doc(self, override: str = "") -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        directory = Path(tmp.name)
        (directory / "penetration.csv").write_text(
            "year,penetration\n"
            "2022,0.10\n"
            "2023,0.14\n"
            "2024,0.19\n"
            "2025,0.25\n",
            encoding="utf-8",
        )
        path = directory / "market.md"
        path.write_text(
            "---\n"
            "base-year: 2026\n"
            "currency: USD\n"
            "maturity-duration: 10\n"
            "penetration:\n"
            "  inputs:\n"
            "    target-series: penetration.csv\n"
            "    measure: stock\n"
            "    ceiling: 0.85\n"
            "    analogs: [us-smartphones, us-color-tv]\n"
            "    w-fit: 0.5\n"
            f"{override}"
            "unrelated: keep-me\n"
            "---\n"
            "# Market\n\n"
            "Body stays byte-for-byte.\n",
            encoding="utf-8",
        )
        return path

    def test_model_estimate_and_base_year_projection(self) -> None:
        path = self.make_doc()
        import yaml

        front_matter = yaml.safe_load(path.read_text().split("---\n", 2)[1])
        result = penetration_doc_result(front_matter, path, DATA_DIR)

        self.assertEqual(result["selected-from"], "model-estimate")
        self.assertEqual(result["selected"], result["model-estimate"])
        self.assertEqual(result["projection"][0][0], 2026)
        self.assertEqual(result["projection"][-1][0], 2036)
        self.assertEqual(result["method"], "logistic-blend")

    def test_complete_override_controls_projection(self) -> None:
        path = self.make_doc(
            "  override:\n"
            "    L: 0.7\n"
            "    t0: 2032\n"
            "    k: 0.15\n"
            "    reason: Target-specific evidence.\n"
        )
        import yaml

        front_matter = yaml.safe_load(path.read_text().split("---\n", 2)[1])
        result = penetration_doc_result(front_matter, path, DATA_DIR)

        self.assertEqual(result["selected-from"], "override")
        self.assertEqual(result["selected"], {"L": 0.7, "t0": 2032.0, "k": 0.15})

    def test_surgical_write_preserves_inputs_override_peers_and_body(self) -> None:
        path = self.make_doc(
            "  override:\n"
            "    L: 0.7\n"
            "    t0: 2032\n"
            "    k: 0.15\n"
            "    reason: Target-specific evidence.\n"
        )
        before = path.read_text(encoding="utf-8")
        result = {
            "model-estimate": {"L": 0.85, "t0": 2030.1234567, "k": 0.2345678},
            "method": "logistic-blend",
        }

        write_penetration_outputs(path, result, "2026-07-28")
        after = path.read_text(encoding="utf-8")

        self.assertIn("target-series: penetration.csv", after)
        self.assertIn("reason: Target-specific evidence.", after)
        self.assertIn("unrelated: keep-me", after)
        self.assertIn("Body stays byte-for-byte.", after)
        self.assertIn("model-estimate:\n    L: 0.85", after)
        self.assertIn("t0: 2030.123457", after)
        self.assertIn("k: 0.234568", after)
        self.assertIn("method: logistic-blend", after)
        self.assertIn("date: 2026-07-28", after)
        self.assertEqual(before.split("---\n", 2)[2], after.split("---\n", 2)[2])

    def test_dry_run_does_not_write(self) -> None:
        path = self.make_doc()
        before = path.read_text(encoding="utf-8")
        args = argparse.Namespace(
            series=None,
            ceiling=None,
            analogs=None,
            market_doc=str(path),
            horizon_year=None,
            as_of=None,
            w_fit=None,
            data_dir=str(DATA_DIR),
            market_dir=str(path.parent),
            dry_run=True,
            stamp_date="2026-07-28",
            json=False,
        )

        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cmd_blend_market_doc(args), 0)

        self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_measure_mismatch_is_rejected(self) -> None:
        path = self.make_doc()
        text = path.read_text(encoding="utf-8").replace(
            "measure: stock", "measure: spend-share"
        )
        path.write_text(text, encoding="utf-8")
        import yaml

        front_matter = yaml.safe_load(path.read_text().split("---\n", 2)[1])
        with self.assertRaisesRegex(SystemExit, "analog measure must match"):
            penetration_doc_result(front_matter, path, DATA_DIR)


if __name__ == "__main__":
    unittest.main()
