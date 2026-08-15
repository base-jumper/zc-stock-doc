from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_doc import (  # noqa: E402
    concentration_parameters,
    penetration_parameters,
    players_for,
    validate_market_doc,
)


TRAITS = {
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


class ConcentrationResolutionTests(unittest.TestCase):
    def test_override_wins_over_model_estimate(self) -> None:
        fm = {
            "concentration": {
                "model-estimate": {"s1": 0.2, "r": 0.7},
                "override": {"s1": 0.3, "r": 0.6, "reason": "Evidence"},
            }
        }

        self.assertEqual(concentration_parameters(fm), (0.3, 0.6, "override"))

    def test_model_estimate_is_default(self) -> None:
        fm = {"concentration": {"model-estimate": {"s1": 0.2, "r": 0.7}}}

        self.assertEqual(concentration_parameters(fm), (0.2, 0.7, "model-estimate"))


class PenetrationResolutionTests(unittest.TestCase):
    def test_override_wins_over_model_estimate(self) -> None:
        fm = {
            "penetration": {
                "model-estimate": {"L": 0.8, "t0": 2031, "k": 0.2},
                "override": {
                    "L": 0.7,
                    "t0": 2032,
                    "k": 0.15,
                    "reason": "Target evidence",
                },
            }
        }

        self.assertEqual(penetration_parameters(fm), (0.7, 2032.0, 0.15, "override"))

    def test_model_estimate_is_default(self) -> None:
        fm = {"penetration": {"model-estimate": {"L": 0.8, "t0": 2031, "k": 0.2}}}

        self.assertEqual(
            penetration_parameters(fm), (0.8, 2031.0, 0.2, "model-estimate")
        )


class PlayerResolutionTests(unittest.TestCase):
    def test_per_player_override_wins_and_can_add_an_outsider(self) -> None:
        fm = {
            "players": {
                "model-estimate": [
                    {"name": "Alpha", "ticker": "AAA", "mobility-adjusted-capture": 0.2},
                    {"name": "Beta", "ticker": "BBB", "mobility-adjusted-capture": 0.1},
                ],
                "override": [
                    {"name": "Beta", "capture": 0.15, "reason": "Evidence"},
                    {"name": "Entrant", "ticker": "NEW", "capture": 0.05,
                     "reason": "Outside contender"},
                ],
            }
        }

        players = {entry["name"]: entry for entry in players_for(fm)}

        self.assertEqual(players["Alpha"]["capture"], 0.2)
        self.assertEqual(players["Beta"]["capture"], 0.15)
        self.assertEqual(players["Beta"]["ticker"], "BBB")
        self.assertEqual(players["Entrant"]["capture"], 0.05)


class ValidationTests(unittest.TestCase):
    def write_doc(self, concentration: str, penetration: str = "", players: str = "") -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "market.md"
        path.write_text(
            "---\n"
            "base-year: 2026\n"
            "currency: USD\n"
            "maturity-duration: 10\n"
            "size: {current-market-value: 1.0, maturity-market-value: 100.0}\n"
            f"{penetration}"
            f"{concentration}"
            f"{players}"
            "---\n"
            "# Market\n",
            encoding="utf-8",
        )
        return path

    def test_valid_model_owned_concentration(self) -> None:
        trait_lines = "\n".join(
            f"      {name}: {{score: 0.5, confidence: 0.8}}" for name in TRAITS
        )
        path = self.write_doc(
            "concentration:\n"
            "  inputs:\n"
            "    traits:\n"
            f"{trait_lines}\n"
            "  model-estimate: {s1: 0.2, r: 0.6}\n"
            "  hhi: 0.0625\n"
            "  method: selected-direct-ridge\n"
            "  date: 2026-07-27\n"
        )

        self.assertEqual(validate_market_doc(path), [])

    def test_stale_hhi_and_missing_override_reason_fail(self) -> None:
        path = self.write_doc(
            "concentration:\n"
            "  model-estimate: {s1: 0.2, r: 0.6}\n"
            "  override: {s1: 0.3, r: 0.5}\n"
            "  hhi: 0.0625\n"
            "  method: legacy-manual\n"
            "  date: 2026-07-27\n"
        )

        errors = validate_market_doc(path)

        self.assertTrue(any("non-empty reason" in error for error in errors))
        self.assertTrue(any("does not match" in error for error in errors))

    def test_valid_penetration_contract(self) -> None:
        concentration = (
            "concentration:\n"
            "  model-estimate: {s1: 0.2, r: 0.6}\n"
            "  hhi: 0.0625\n"
            "  method: legacy-manual\n"
            "  date: 2026-07-28\n"
        )
        path = self.write_doc(
            concentration,
            "penetration:\n"
            "  inputs:\n"
            "    target-series: penetration.csv\n"
            "    measure: stock\n"
            "    ceiling: 0.8\n"
            "    analogs: [us-smartphones, us-color-tv]\n"
            "  model-estimate: {L: 0.8, t0: 2031, k: 0.2}\n"
            "  method: logistic-blend\n"
            "  date: 2026-07-28\n",
        )
        path.with_name("penetration.csv").write_text(
            "year,penetration\n2024,0.1\n", encoding="utf-8"
        )

        self.assertEqual(validate_market_doc(path), [])

    def test_penetration_override_and_inputs_are_validated(self) -> None:
        concentration = (
            "concentration:\n"
            "  model-estimate: {s1: 0.2, r: 0.6}\n"
            "  hhi: 0.0625\n"
            "  method: legacy-manual\n"
            "  date: 2026-07-28\n"
        )
        path = self.write_doc(
            concentration,
            "penetration:\n"
            "  inputs:\n"
            "    target-series: missing.csv\n"
            "    measure: sales\n"
            "    ceiling: 1.2\n"
            "    analogs: [one]\n"
            "  model-estimate: {L: 0.8, t0: 2031, k: 0.2}\n"
            "  override: {L: 0.7, t0: 2032, k: -0.1}\n"
            "  method: logistic-blend\n"
            "  date: 2026-07-28\n",
        )

        errors = validate_market_doc(path)

        self.assertTrue(any("non-empty reason" in error for error in errors))
        self.assertTrue(any(".k must be greater" in error for error in errors))
        self.assertTrue(any("target-series not found" in error for error in errors))
        self.assertTrue(any(".measure must be" in error for error in errors))
        self.assertTrue(any(".ceiling must be" in error for error in errors))
        self.assertTrue(any(".analogs must contain" in error for error in errors))

    def test_valid_mobility_backed_players(self) -> None:
        path = self.write_doc(
            "concentration:\n"
            "  model-estimate: {s1: 0.2, r: 0.6}\n"
            "  hhi: 0.0625\n"
            "  method: legacy-manual\n"
            "  date: 2026-07-31\n",
            players=(
                "players:\n"
                "  inputs:\n"
                "    current:\n"
                "      - {rank: 1, name: Alpha, ticker: AAA, share: 0.5}\n"
                "      - {rank: 2, name: Beta, ticker: BBB, share: 0.25}\n"
                "  model-estimate:\n"
                "    - {rank: 1, name: Alpha, ticker: AAA, hold-position-capture: 0.2, mobility-adjusted-capture: 0.16, mobility-adjusted-revenue: 16.0}\n"
                "    - {rank: 2, name: Beta, ticker: BBB, hold-position-capture: 0.12, mobility-adjusted-capture: 0.11, mobility-adjusted-revenue: 11.0}\n"
                "  gone-probability: 0.1\n"
                "  method: share-gap-mobility-weighted-geometric-capture\n"
                "  date: 2026-07-31\n"
            ),
        )

        self.assertEqual(validate_market_doc(path), [])

    def test_stale_mobility_outputs_and_bad_override_fail(self) -> None:
        path = self.write_doc(
            "concentration:\n"
            "  model-estimate: {s1: 0.2, r: 0.6}\n"
            "  hhi: 0.0625\n"
            "  method: legacy-manual\n"
            "  date: 2026-07-31\n",
            players=(
                "players:\n"
                "  inputs:\n"
                "    current:\n"
                "      - {rank: 1, name: Alpha, share: 0.4}\n"
                "      - {rank: 2, name: Beta, share: 0.5}\n"
                "  model-estimate:\n"
                "    - {rank: 1, name: Alpha, hold-position-capture: 0.3, mobility-adjusted-capture: 0.2, mobility-adjusted-revenue: 99.0}\n"
                "    - {rank: 2, name: Beta, hold-position-capture: 0.12, mobility-adjusted-capture: 0.1}\n"
                "  override:\n"
                "    - {name: Alpha, capture: 0.25}\n"
                "  gone-probability: 1.2\n"
                "  method: wrong\n"
                "  date: 2026-07-31\n"
            ),
        )

        errors = validate_market_doc(path)

        self.assertTrue(any("shares must be descending" in error for error in errors))
        self.assertTrue(any("does not match canonical concentration" in error for error in errors))
        self.assertTrue(any("override[1].reason" in error for error in errors))
        self.assertTrue(any("gone-probability" in error for error in errors))
        self.assertTrue(any("players.method" in error for error in errors))
        self.assertTrue(any("mobility-adjusted-revenue" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
