#!/usr/bin/env python3
"""Compare trait-to-concentration models with nested leave-one-out validation.

The production model remains in concentration_fit.py. This script evaluates candidate aggregation,
feature, and link structures without changing live predictions. Any hyperparameter or feature
selection is repeated inside each outer fold so the reported errors remain out of sample.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import concentration_fit as fit
from concentration_fit import RidgeModel, fit_ridge

ALL_TRAITS = fit.DOMINANCE_TRAITS + fit.BARRIER_TRAITS
POWER_GRID = (-4.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 4.0, 8.0)
RIDGE_GRID = (0.0, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0)
MAX_SELECTED_FEATURES = 3
OBSERVED_SECTORS = {
    "us-web-search": "information",
    "us-cloud-infrastructure": "information",
    "us-ridesharing": "transport",
    "us-domestic-airlines": "transport",
    "global-mobile-os": "information",
    "discrete-gpus": "manufacturing",
    "us-carbonated-soft-drinks": "manufacturing",
    "credit-rating-agencies": "finance",
    "large-commercial-aircraft": "manufacturing",
    "us-card-payment-networks": "finance",
    "x86-cpus": "manufacturing",
    "us-restaurants": "food-services",
}
NAICS_SECTORS = {
    "21": "energy",
    "31": "manufacturing",
    "32": "manufacturing",
    "33": "manufacturing",
    "42": "wholesale",
    "44": "retail",
    "45": "retail",
    "48": "transport",
    "49": "transport",
    "51": "information",
    "52": "finance",
    "53": "real-estate-rental",
    "54": "professional-services",
    "56": "administrative-services",
    "61": "education",
    "71": "arts-recreation",
    "72": "food-services",
    "81": "personal-services",
}


@dataclass(frozen=True)
class Record:
    id: str
    traits: dict[str, float]
    s1: float
    r: float
    outcome_source: str = "unknown"
    sector: str = "unknown"


Predictor = Callable[[list[Record], Record], tuple[float, float, dict]]
FinalMetadata = Callable[[list[Record]], dict]


@dataclass(frozen=True)
class Candidate:
    name: str
    description: str
    predict: Predictor
    final_metadata: FinalMetadata


def load_records(data_dir: Path, quality: str) -> list[Record]:
    records = []
    for entry in fit.load_index(data_dir).values():
        if quality != "all" and entry["quality"] != quality:
            continue
        outcome = fit.fit_calibration_entry(entry, data_dir)
        synthetic = entry.get("outcome-quality") == fit.SYNTHETIC_OUTCOME_QUALITY
        if entry["id"].startswith("us-naics-"):
            naics_prefix = entry["id"].removeprefix("us-naics-")[:2]
            sector = NAICS_SECTORS.get(naics_prefix)
        else:
            sector = OBSERVED_SECTORS.get(entry["id"])
        if sector is None:
            raise SystemExit(f"{entry['id']}: no broad validation sector configured")
        records.append(
            Record(
                id=entry["id"],
                traits={trait: entry["traits"][trait]["score"] for trait in ALL_TRAITS},
                s1=outcome["s1"],
                r=outcome["r"],
                outcome_source="census-synthetic" if synthetic else "observed-shares",
                sector=sector,
            )
        )
    if len(records) < 4:
        raise SystemExit(f"need at least four calibration entries, found {len(records)}")
    return records


def _features(record: Record, names: tuple[str, ...] | list[str]) -> list[float]:
    return [record.traits[name] for name in names]


def _target(record: Record, name: str) -> float:
    return getattr(record, name)


def _error(actual: list[float], predicted: list[float]) -> tuple[float, float]:
    squared = [(a - p) ** 2 for a, p in zip(actual, predicted)]
    absolute = [abs(a - p) for a, p in zip(actual, predicted)]
    return math.sqrt(sum(squared) / len(squared)), sum(absolute) / len(absolute)


def _metrics(rows: list[dict]) -> dict:
    s1_rmse, s1_mae = _error(
        [item["actual_s1"] for item in rows],
        [item["predicted_s1"] for item in rows],
    )
    r_rmse, r_mae = _error(
        [item["actual_r"] for item in rows],
        [item["predicted_r"] for item in rows],
    )
    return {
        "s1_rmse": s1_rmse,
        "s1_mae": s1_mae,
        "r_rmse": r_rmse,
        "r_mae": r_mae,
    }


def _breakdown(rows: list[dict], field: str) -> dict[str, dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row[field], []).append(row)
    return {
        key: {"n": len(items), **_metrics(items)}
        for key, items in sorted(grouped.items())
    }


def _outer_groups(records: list[Record], validation: str) -> list[tuple[str, list[int]]]:
    if validation == "loo":
        return [(record.id, [i]) for i, record in enumerate(records)]
    attribute = "outcome_source" if validation == "source" else "sector"
    grouped: dict[str, list[int]] = {}
    for i, record in enumerate(records):
        grouped.setdefault(getattr(record, attribute), []).append(i)
    return sorted(grouped.items())


def _ridge_loo_rmse(
    records: list[Record],
    feature_names: tuple[str, ...],
    target_name: str,
    alpha: float,
) -> float:
    errors = []
    for i, record in enumerate(records):
        training = records[:i] + records[i + 1 :]
        model = fit_ridge(
            [_features(item, feature_names) for item in training],
            [_target(item, target_name) for item in training],
            alpha,
        )
        bounds = fit.S1_CLIP if target_name == "s1" else fit.R_CLIP
        prediction = fit._clip(model.predict(_features(record, feature_names)), *bounds)
        errors.append((_target(record, target_name) - prediction) ** 2)
    return math.sqrt(sum(errors) / len(errors))


def select_ridge_alpha(
    records: list[Record],
    feature_names: tuple[str, ...],
    target_name: str,
) -> float:
    scored = [
        (_ridge_loo_rmse(records, feature_names, target_name, alpha), alpha)
        for alpha in RIDGE_GRID
    ]
    return min(scored)[1]


def _power_mean(values: list[float], power: float) -> float:
    if power == 0.0:
        if any(value == 0.0 for value in values):
            return 0.0
        return math.exp(sum(math.log(value) for value in values) / len(values))
    if power < 0.0 and any(value == 0.0 for value in values):
        return 0.0
    return (sum(value**power for value in values) / len(values)) ** (1.0 / power)


def _index_prediction(
    training: list[Record],
    record: Record,
    index_fn: Callable[[Record], float],
) -> tuple[float, float]:
    indices = [index_fn(item) for item in training]
    a1, b1 = fit._ols(indices, [item.s1 for item in training])
    s1_prediction = fit._clip(a1 + b1 * index_fn(record), *fit.S1_CLIP)
    a2, b2 = fit._ols([item.s1 for item in training], [item.r for item in training])
    r_prediction = fit._clip(a2 + b2 * s1_prediction, *fit.R_CLIP)
    return s1_prediction, r_prediction


def _index_loo_rmse(records: list[Record], index_fn: Callable[[Record], float]) -> float:
    actual, predicted = [], []
    for i, record in enumerate(records):
        training = records[:i] + records[i + 1 :]
        s1_prediction, _ = _index_prediction(training, record, index_fn)
        actual.append(record.s1)
        predicted.append(s1_prediction)
    return _error(actual, predicted)[0]


def _dominance_noisy_or(record: Record) -> float:
    return fit.dominance_index(record.traits)


def _dominance_mean(record: Record) -> float:
    return sum(record.traits[name] for name in fit.DOMINANCE_TRAITS) / len(
        fit.DOMINANCE_TRAITS
    )


def _all_trait_mean(record: Record) -> float:
    return sum(record.traits[name] for name in ALL_TRAITS) / len(ALL_TRAITS)


def _select_power(records: list[Record]) -> float:
    scored = []
    for power in POWER_GRID:
        index_fn = lambda record, p=power: _power_mean(
            _features(record, fit.DOMINANCE_TRAITS), p
        )
        scored.append((_index_loo_rmse(records, index_fn), power))
    return min(scored)[1]


def _fixed_index_candidate(
    name: str,
    description: str,
    index_fn: Callable[[Record], float],
) -> Candidate:
    def predict(training: list[Record], record: Record) -> tuple[float, float, dict]:
        s1_prediction, r_prediction = _index_prediction(training, record, index_fn)
        return s1_prediction, r_prediction, {}

    return Candidate(name, description, predict, lambda records: {})


def _power_predict(training: list[Record], record: Record) -> tuple[float, float, dict]:
    power = _select_power(training)
    index_fn = lambda item: _power_mean(_features(item, fit.DOMINANCE_TRAITS), power)
    s1_prediction, r_prediction = _index_prediction(training, record, index_fn)
    return s1_prediction, r_prediction, {"power": power}


def _power_metadata(records: list[Record]) -> dict:
    return {"power": _select_power(records)}


def _predict_ridge_target(
    training: list[Record],
    record: Record,
    feature_names: tuple[str, ...],
    target_name: str,
    alpha: float,
) -> float:
    model = fit_ridge(
        [_features(item, feature_names) for item in training],
        [_target(item, target_name) for item in training],
        alpha,
    )
    return model.predict(_features(record, feature_names))


def _pipeline_r_loo_rmse(
    records: list[Record],
    stage1_predict: Callable[[list[Record], Record], float],
    r_trait_names: tuple[str, ...],
    alpha: float,
) -> float:
    errors = []
    for i, record in enumerate(records):
        training = records[:i] + records[i + 1 :]
        s1_prediction = stage1_predict(training, record)
        xs = [[item.s1] + _features(item, r_trait_names) for item in training]
        model = fit_ridge(xs, [item.r for item in training], alpha)
        prediction = fit._clip(
            model.predict([s1_prediction] + _features(record, r_trait_names)),
            *fit.R_CLIP,
        )
        errors.append((record.r - prediction) ** 2)
    return math.sqrt(sum(errors) / len(errors))


def _select_pipeline_r_alpha(
    records: list[Record],
    stage1_predict: Callable[[list[Record], Record], float],
    r_trait_names: tuple[str, ...],
) -> float:
    scored = [
        (_pipeline_r_loo_rmse(records, stage1_predict, r_trait_names, alpha), alpha)
        for alpha in RIDGE_GRID
    ]
    return min(scored)[1]


def _all_ridge_configuration(records: list[Record]) -> dict:
    names = tuple(ALL_TRAITS)
    alpha_s1 = select_ridge_alpha(records, names, "s1")

    def stage1(training: list[Record], record: Record) -> float:
        return fit._clip(
            _predict_ridge_target(training, record, names, "s1", alpha_s1),
            *fit.S1_CLIP,
        )

    alpha_r = _select_pipeline_r_alpha(records, stage1, names)
    return {"alpha_s1": alpha_s1, "alpha_r": alpha_r}


def _coefficient_metadata(
    records: list[Record],
    feature_names: tuple[str, ...],
    target_name: str,
    alpha: float,
    xs: list[list[float]] | None = None,
) -> dict:
    model = fit_ridge(
        xs if xs is not None else [_features(item, feature_names) for item in records],
        [_target(item, target_name) for item in records],
        alpha,
    )
    return {
        "intercept": model.coefficients[0],
        "standardized": dict(zip(feature_names, model.coefficients[1:])),
    }


def _all_ridge_metadata(records: list[Record]) -> dict:
    config = _all_ridge_configuration(records)
    names = tuple(ALL_TRAITS)
    return {
        **config,
        "s1_model": _coefficient_metadata(records, names, "s1", config["alpha_s1"]),
        "r_model": _coefficient_metadata(
            records,
            ("s1", *names),
            "r",
            config["alpha_r"],
            [[item.s1] + _features(item, names) for item in records],
        ),
    }


def _all_ridge_pipeline_predict(
    training: list[Record],
    record: Record,
) -> tuple[float, float, dict]:
    config = _all_ridge_configuration(training)
    names = tuple(ALL_TRAITS)
    s1_model = fit_ridge(
        [_features(item, names) for item in training],
        [item.s1 for item in training],
        config["alpha_s1"],
    )
    s1_prediction = fit._clip(s1_model.predict(_features(record, names)), *fit.S1_CLIP)
    r_model = fit_ridge(
        [[item.s1] + _features(item, names) for item in training],
        [item.r for item in training],
        config["alpha_r"],
    )
    r_prediction = fit._clip(
        r_model.predict([s1_prediction] + _features(record, names)),
        *fit.R_CLIP,
    )
    return s1_prediction, r_prediction, config


def _hybrid_configuration(records: list[Record]) -> dict:
    barrier_names = tuple(fit.BARRIER_TRAITS)

    def stage1(training: list[Record], record: Record) -> float:
        return _index_prediction(training, record, _dominance_noisy_or)[0]

    return {
        "alpha_r": _select_pipeline_r_alpha(records, stage1, barrier_names),
        "r_traits": list(barrier_names),
    }


def _hybrid_metadata(records: list[Record]) -> dict:
    config = _hybrid_configuration(records)
    names = tuple(fit.BARRIER_TRAITS)
    return {
        **config,
        "r_model": _coefficient_metadata(
            records,
            ("s1", *names),
            "r",
            config["alpha_r"],
            [[item.s1] + _features(item, names) for item in records],
        ),
    }


def _hybrid_predict(
    training: list[Record],
    record: Record,
) -> tuple[float, float, dict]:
    config = _hybrid_configuration(training)
    barrier_names = tuple(fit.BARRIER_TRAITS)
    s1_prediction, _ = _index_prediction(training, record, _dominance_noisy_or)
    r_model = fit_ridge(
        [[item.s1] + _features(item, barrier_names) for item in training],
        [item.r for item in training],
        config["alpha_r"],
    )
    r_prediction = fit._clip(
        r_model.predict([s1_prediction] + _features(record, barrier_names)),
        *fit.R_CLIP,
    )
    return s1_prediction, r_prediction, config


def _direct_configuration(records: list[Record]) -> dict:
    names = tuple(ALL_TRAITS)
    return {
        "alpha_s1": select_ridge_alpha(records, names, "s1"),
        "alpha_r": select_ridge_alpha(records, names, "r"),
    }


def _direct_metadata(records: list[Record]) -> dict:
    config = _direct_configuration(records)
    names = tuple(ALL_TRAITS)
    return {
        **config,
        "s1_model": _coefficient_metadata(records, names, "s1", config["alpha_s1"]),
        "r_model": _coefficient_metadata(records, names, "r", config["alpha_r"]),
    }


def _direct_ridge_predict(
    training: list[Record],
    record: Record,
) -> tuple[float, float, dict]:
    config = _direct_configuration(training)
    names = tuple(ALL_TRAITS)
    s1_prediction = fit._clip(
        _predict_ridge_target(training, record, names, "s1", config["alpha_s1"]),
        *fit.S1_CLIP,
    )
    r_prediction = fit._clip(
        _predict_ridge_target(training, record, names, "r", config["alpha_r"]),
        *fit.R_CLIP,
    )
    return s1_prediction, r_prediction, config


def _select_features(records: list[Record], target_name: str) -> tuple[tuple[str, ...], float]:
    """Greedy forward selection; every feature/penalty decision uses inner LOO error."""
    selected: tuple[str, ...] = ()
    selected_alpha = RIDGE_GRID[0]
    selected_error = math.inf
    for _ in range(MAX_SELECTED_FEATURES):
        candidates = []
        for trait in ALL_TRAITS:
            if trait in selected:
                continue
            names = selected + (trait,)
            for alpha in RIDGE_GRID:
                error = _ridge_loo_rmse(records, names, target_name, alpha)
                candidates.append((error, len(names), names, alpha))
        best_error, _, best_names, best_alpha = min(candidates)
        if best_error >= selected_error - 1e-9:
            break
        selected = best_names
        selected_alpha = best_alpha
        selected_error = best_error
    return selected, selected_alpha


def _selected_configuration(records: list[Record]) -> dict:
    s1_names, alpha_s1 = _select_features(records, "s1")
    r_names, alpha_r = _select_features(records, "r")
    return {
        "s1_traits": list(s1_names),
        "alpha_s1": alpha_s1,
        "r_traits": list(r_names),
        "alpha_r": alpha_r,
    }


def _selected_metadata(records: list[Record]) -> dict:
    config = _selected_configuration(records)
    s1_names = tuple(config["s1_traits"])
    r_names = tuple(config["r_traits"])
    return {
        **config,
        "s1_model": _coefficient_metadata(
            records, s1_names, "s1", config["alpha_s1"]
        ),
        "r_model": _coefficient_metadata(records, r_names, "r", config["alpha_r"]),
    }


def _selected_ridge_predict(
    training: list[Record],
    record: Record,
) -> tuple[float, float, dict]:
    config = _selected_configuration(training)
    s1_names = tuple(config["s1_traits"])
    r_names = tuple(config["r_traits"])
    s1_prediction = fit._clip(
        _predict_ridge_target(training, record, s1_names, "s1", config["alpha_s1"]),
        *fit.S1_CLIP,
    )
    r_prediction = fit._clip(
        _predict_ridge_target(training, record, r_names, "r", config["alpha_r"]),
        *fit.R_CLIP,
    )
    return s1_prediction, r_prediction, config


def candidates() -> list[Candidate]:
    return [
        _fixed_index_candidate(
            "dominance-noisy-or",
            "Former production dominance noisy-OR -> s1 -> r",
            _dominance_noisy_or,
        ),
        _fixed_index_candidate(
            "dominance-mean",
            "Arithmetic mean of dominance traits -> s1 -> r",
            _dominance_mean,
        ),
        Candidate(
            "dominance-power",
            "Nested-tuned power mean of dominance traits -> s1 -> r",
            _power_predict,
            _power_metadata,
        ),
        _fixed_index_candidate(
            "all-trait-mean",
            "Arithmetic mean of all seven traits -> s1 -> r",
            _all_trait_mean,
        ),
        Candidate(
            "all-trait-ridge-pipeline",
            "All traits -> ridge s1; predicted s1 + all traits -> ridge r",
            _all_ridge_pipeline_predict,
            _all_ridge_metadata,
        ),
        Candidate(
            "dominance-barrier-hybrid",
            "Dominance noisy-OR -> s1; predicted s1 + barriers -> ridge r",
            _hybrid_predict,
            _hybrid_metadata,
        ),
        Candidate(
            "all-trait-direct-ridge",
            "All traits independently predict s1 and r with ridge",
            _direct_ridge_predict,
            _direct_metadata,
        ),
        Candidate(
            "selected-direct-ridge",
            "Nested forward-selected traits independently predict s1 and r",
            _selected_ridge_predict,
            _selected_metadata,
        ),
    ]


def _metadata_summary(metadata: list[dict]) -> dict:
    keys = sorted({key for item in metadata for key in item})
    summary = {}
    for key in keys:
        values = [json.dumps(item[key], sort_keys=True) for item in metadata if key in item]
        summary[key] = [
            {"value": json.loads(value), "folds": count}
            for value, count in Counter(values).most_common()
        ]
    return summary


def evaluate_candidate(
    candidate: Candidate,
    records: list[Record],
    validation: str = "loo",
) -> dict:
    residuals = []
    fold_metadata = []
    outer_groups = _outer_groups(records, validation)
    for group, held_out in outer_groups:
        held_out_set = set(held_out)
        training = [record for i, record in enumerate(records) if i not in held_out_set]
        if len(training) < 4:
            raise SystemExit(
                f"{validation} group '{group}' leaves only {len(training)} training entries"
            )
        group_metadata = None
        for i in held_out:
            record = records[i]
            s1_prediction, r_prediction, metadata = candidate.predict(training, record)
            if group_metadata is None:
                group_metadata = metadata
            residuals.append(
                {
                    "id": record.id,
                    "outcome_source": record.outcome_source,
                    "sector": record.sector,
                    "outer_group": group,
                    "actual_s1": record.s1,
                    "predicted_s1": s1_prediction,
                    "s1_error": s1_prediction - record.s1,
                    "actual_r": record.r,
                    "predicted_r": r_prediction,
                    "r_error": r_prediction - record.r,
                }
            )
        fold_metadata.append(group_metadata or {})
    metrics = _metrics(residuals)
    by_outer_group = _breakdown(residuals, "outer_group")
    macro_group_metrics = {
        metric: sum(group[metric] for group in by_outer_group.values()) / len(by_outer_group)
        for metric in ("s1_rmse", "s1_mae", "r_rmse", "r_mae")
    }
    return {
        "name": candidate.name,
        "description": candidate.description,
        "n": len(records),
        "validation": validation,
        "outer_groups": len(outer_groups),
        "metrics": metrics,
        "macro_group_metrics": macro_group_metrics,
        "by_outcome_source": _breakdown(residuals, "outcome_source"),
        "by_sector": _breakdown(residuals, "sector"),
        "by_outer_group": by_outer_group,
        "full_corpus_selection": candidate.final_metadata(records),
        "outer_fold_selection": _metadata_summary(fold_metadata),
        "residuals": residuals,
    }


def _print_results(results: list[dict], details: bool) -> None:
    validation = results[0]["validation"]
    if validation != "loo":
        print(
            f"{'method':<29} {'s1 RMSE':>9} {'r RMSE':>9} "
            f"{'macro s1':>9} {'macro r':>9}"
        )
        minima = (
            min(result["metrics"]["s1_rmse"] for result in results),
            min(result["metrics"]["r_rmse"] for result in results),
            min(result["macro_group_metrics"]["s1_rmse"] for result in results),
            min(result["macro_group_metrics"]["r_rmse"] for result in results),
        )
        for result in results:
            values = (
                result["metrics"]["s1_rmse"],
                result["metrics"]["r_rmse"],
                result["macro_group_metrics"]["s1_rmse"],
                result["macro_group_metrics"]["r_rmse"],
            )
            markers = [
                "*" if abs(value - minimum) < 1e-12 else " "
                for value, minimum in zip(values, minima)
            ]
            rendered = [f"{value:.4f}{marker}" for value, marker in zip(values, markers)]
            print(
                f"{result['name']:<29} {rendered[0]:>9} {rendered[1]:>9} "
                f"{rendered[2]:>9} {rendered[3]:>9}"
            )
        print("* best column; hyperparameters/features selected inside each outer training set")
    else:
        best = {
            metric: min(result["metrics"][metric] for result in results)
            for metric in ("s1_rmse", "s1_mae", "r_rmse", "r_mae")
        }
        print(f"{'method':<29} {'s1 RMSE':>9} {'s1 MAE':>9} {'r RMSE':>9} {'r MAE':>9}")
        for result in results:
            metrics = result["metrics"]
            values = []
            for metric in ("s1_rmse", "s1_mae", "r_rmse", "r_mae"):
                marker = "*" if abs(metrics[metric] - best[metric]) < 1e-12 else " "
                values.append(f"{metrics[metric]:.4f}{marker}")
            print(
                f"{result['name']:<29} {values[0]:>9} {values[1]:>9} "
                f"{values[2]:>9} {values[3]:>9}"
            )
        print("* best column; all metrics are nested leave-one-out")
    print("\nFull-corpus selections (descriptive; not used for reported errors):")
    for result in results:
        metadata = result["full_corpus_selection"]
        if metadata:
            compact = {
                key: value
                for key, value in metadata.items()
                if key not in ("s1_model", "r_model")
            }
            print(f"  {result['name']}: {json.dumps(compact, sort_keys=True)}")
            for target in ("s1_model", "r_model"):
                if target in metadata:
                    coefficients = metadata[target]["standardized"]
                    formatted = ", ".join(
                        f"{name}={coefficient:+.3f}"
                        for name, coefficient in coefficients.items()
                    )
                    print(f"    {target.removesuffix('_model')}: {formatted}")
    if details:
        for result in results:
            breakdown = (
                result["by_outcome_source"]
                if validation == "loo"
                else result["by_outer_group"]
            )
            label = "outcome-source" if validation == "loo" else "outer-group"
            print(f"\n{result['name']} {label} metrics:")
            print(f"{'group':<28} {'n':>4} {'s1 RMSE':>9} {'r RMSE':>9}")
            for group, metrics in breakdown.items():
                print(
                    f"{group:<28} {metrics['n']:>4} "
                    f"{metrics['s1_rmse']:>9.4f} {metrics['r_rmse']:>9.4f}"
                )
            print(f"\n{result['name']} residuals:")
            print(f"{'id':<28} {'s1 actual':>9} {'s1 pred':>9} {'s1 err':>9} "
                  f"{'r actual':>9} {'r pred':>9} {'r err':>9}")
            for row in result["residuals"]:
                print(
                    f"{row['id']:<28} {row['actual_s1']:>9.4f} "
                    f"{row['predicted_s1']:>9.4f} {row['s1_error']:>+9.4f} "
                    f"{row['actual_r']:>9.4f} {row['predicted_r']:>9.4f} "
                    f"{row['r_error']:>+9.4f}"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-dir", default=str(fit.DATA_DIR))
    parser.add_argument(
        "--quality",
        choices=("all", "verified"),
        default="all",
        help="trait-quality filter (default all)",
    )
    parser.add_argument(
        "--validation",
        choices=("loo", "source", "sector"),
        default="loo",
        help="outer validation split: market LOO, outcome source, or broad sector",
    )
    parser.add_argument(
        "--methods",
        help="comma-separated candidate names (default all)",
    )
    parser.add_argument("--details", action="store_true", help="print per-market residuals")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    available = {candidate.name: candidate for candidate in candidates()}
    names = (
        [name.strip() for name in args.methods.split(",") if name.strip()]
        if args.methods
        else list(available)
    )
    unknown = [name for name in names if name not in available]
    if unknown:
        raise SystemExit(
            f"unknown method(s): {', '.join(unknown)}; choose from {', '.join(available)}"
        )
    records = load_records(Path(args.data_dir), args.quality)
    results = [
        evaluate_candidate(available[name], records, args.validation)
        for name in names
    ]
    payload = {
        "validation": args.validation,
        "quality": args.quality,
        "n": len(records),
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"Corpus: n={len(records)} ({args.quality} trait quality); "
            f"validation={args.validation}\n"
        )
        _print_results(results, args.details)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
