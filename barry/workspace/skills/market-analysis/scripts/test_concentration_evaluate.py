from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from concentration_evaluate import (  # noqa: E402
    Candidate,
    Record,
    _power_mean,
    evaluate_candidate,
    fit_ridge,
)


class ConcentrationEvaluateTests(unittest.TestCase):
    def test_ridge_recovers_linear_relationship(self) -> None:
        xs = [[0.0, 1.0], [1.0, 0.0], [2.0, 1.0], [3.0, 2.0]]
        ys = [2.0 + 3.0 * row[0] - 0.5 * row[1] for row in xs]

        model = fit_ridge(xs, ys, alpha=0.0)

        self.assertAlmostEqual(model.predict([1.5, 0.5]), 6.25, places=8)

    def test_power_mean_special_cases(self) -> None:
        values = [0.2, 0.5, 0.8]

        self.assertAlmostEqual(_power_mean(values, 1.0), sum(values) / len(values))
        self.assertAlmostEqual(
            _power_mean(values, 0.0),
            (values[0] * values[1] * values[2]) ** (1 / 3),
        )
        self.assertGreater(_power_mean(values, 4.0), _power_mean(values, 1.0))
        self.assertLess(_power_mean(values, -4.0), _power_mean(values, 1.0))

    def test_outer_fold_never_trains_on_held_out_record(self) -> None:
        records = [
            Record(str(i), {"x": i / 10}, 0.1 + i / 20, 0.8 - i / 20)
            for i in range(5)
        ]

        def predict(training: list[Record], record: Record) -> tuple[float, float, dict]:
            self.assertNotIn(record, training)
            self.assertEqual(len(training), len(records) - 1)
            return (
                sum(item.s1 for item in training) / len(training),
                sum(item.r for item in training) / len(training),
                {},
            )

        candidate = Candidate("test", "test", predict, lambda _: {})
        result = evaluate_candidate(candidate, records)

        self.assertEqual(result["n"], len(records))
        self.assertEqual(len(result["residuals"]), len(records))
        self.assertGreater(result["metrics"]["s1_rmse"], 0)

    def test_sector_validation_holds_out_entire_group(self) -> None:
        records = [
            Record(
                str(i),
                {"x": i / 10},
                0.1 + i / 20,
                0.8 - i / 20,
                "source",
                ("a", "b", "c")[i // 2],
            )
            for i in range(6)
        ]

        def predict(training: list[Record], record: Record) -> tuple[float, float, dict]:
            self.assertTrue(all(item.sector != record.sector for item in training))
            self.assertEqual(len(training), 4)
            return (
                sum(item.s1 for item in training) / len(training),
                sum(item.r for item in training) / len(training),
                {},
            )

        candidate = Candidate("test", "test", predict, lambda _: {})
        result = evaluate_candidate(candidate, records, validation="sector")

        self.assertEqual(result["outer_groups"], 3)
        self.assertEqual(set(result["by_outer_group"]), {"a", "b", "c"})
        self.assertEqual(result["by_outcome_source"]["source"]["n"], 6)


if __name__ == "__main__":
    unittest.main()
