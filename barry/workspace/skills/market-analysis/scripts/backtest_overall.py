#!/usr/bin/env python3
"""Generate the aggregate summary for a market-analysis back-test run."""
from __future__ import annotations

import argparse
import datetime as dt
import statistics
import sys
from pathlib import Path
from typing import Any

import yaml


EXPECTED_PROJECTION_DURATION = 10

METRICS = {
    "current-market-value": ("size", "current-market-value"),
    "maturity-market-value": ("size", "maturity-market-value"),
    "hhi": ("concentration", "hhi"),
}

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "references" / "back-test" / "data"


def load_doc(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} is missing front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path} has unterminated front matter")
    front_matter = yaml.safe_load(text[4:end]) or {}
    if not isinstance(front_matter, dict):
        raise ValueError(f"{path} front matter is not a mapping")
    return front_matter, text[end + 5 :]


def get_nested(mapping: dict[str, Any], keys: tuple[str, ...]) -> Any:
    value: Any = mapping
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def validate_projection_duration(path: Path, fm: dict[str, Any]) -> None:
    duration = as_int(fm.get("maturity-duration"))
    if duration != EXPECTED_PROJECTION_DURATION:
        raise ValueError(
            f"{path} must use maturity-duration: {EXPECTED_PROJECTION_DURATION}; got {duration!r}"
        )


def pct_error(generated: Any, benchmark: Any) -> float | None:
    gen = as_float(generated)
    bench = as_float(benchmark)
    if gen is None or bench in (None, 0):
        return None
    return (gen - bench) / bench * 100


def round1(value: float | None) -> float | None:
    return None if value is None else round(value, 1)


def fmt_num(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int) or float(value).is_integer():
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:+.1f}%"


def title_from_body(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback.replace("-", " ").title()


def benchmark_subjects(data_dir: Path) -> list[str]:
    benchmark_dir = data_dir / "benchmark"
    return sorted(path.stem for path in benchmark_dir.glob("*.md"))


def run_dirs(data_dir: Path) -> list[Path]:
    dirs: list[Path] = []
    for path in data_dir.iterdir():
        if not path.is_dir() or path.name == "benchmark":
            continue
        try:
            dt.date.fromisoformat(path.name)
        except ValueError:
            continue
        dirs.append(path)
    return sorted(dirs)


def run_uses_fixed_horizon(data_dir: Path, run_dir: Path) -> bool:
    try:
        for market_id in benchmark_subjects(data_dir):
            generated_path = run_dir / "market-docs" / f"{market_id}.md"
            if not generated_path.exists():
                return False
            gen_fm, _ = load_doc(generated_path)
            validate_projection_duration(generated_path, gen_fm)
    except (OSError, ValueError, yaml.YAMLError):
        return False
    return True


def find_previous_run(data_dir: Path, run_date: str) -> Path | None:
    previous = [
        path
        for path in run_dirs(data_dir)
        if path.name < run_date and run_uses_fixed_horizon(data_dir, path)
    ]
    return previous[-1] if previous else None


def subject_rows(data_dir: Path, run_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for market_id in benchmark_subjects(data_dir):
        generated_path = run_dir / "market-docs" / f"{market_id}.md"
        benchmark_path = data_dir / "benchmark" / f"{market_id}.md"
        if not generated_path.exists():
            raise FileNotFoundError(f"missing generated market doc: {generated_path}")
        gen_fm, gen_body = load_doc(generated_path)
        bench_fm, _ = load_doc(benchmark_path)
        validate_projection_duration(generated_path, gen_fm)
        validate_projection_duration(benchmark_path, bench_fm)

        errors = {
            metric: pct_error(
                get_nested(gen_fm, keys),
                get_nested(bench_fm, keys),
            )
            for metric, keys in METRICS.items()
        }
        comparable_errors = [abs(v) for v in errors.values() if v is not None]
        rows.append(
            {
                "market-id": market_id,
                "market": title_from_body(gen_body, market_id),
                "base-year": gen_fm.get("base-year"),
                "generated": {
                    metric: get_nested(gen_fm, keys) for metric, keys in METRICS.items()
                },
                "benchmark": {
                    metric: get_nested(bench_fm, keys) for metric, keys in METRICS.items()
                },
                "errors": errors,
                "mae": statistics.mean(comparable_errors) if comparable_errors else None,
            }
        )
    return rows


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metric_summary: dict[str, dict[str, float | None]] = {}
    for metric in METRICS:
        signed = [row["errors"][metric] for row in rows if row["errors"][metric] is not None]
        metric_summary[metric] = {
            "mean-signed-error-pct": statistics.mean(signed) if signed else None,
            "mean-absolute-error-pct": statistics.mean(abs(v) for v in signed) if signed else None,
            "median-absolute-error-pct": statistics.median(abs(v) for v in signed) if signed else None,
        }

    subject_maes = [row["mae"] for row in rows if row["mae"] is not None]
    return {
        "subject-count": len(rows),
        "mean-absolute-error-pct": statistics.mean(subject_maes) if subject_maes else None,
        "median-subject-mae-pct": statistics.median(subject_maes) if subject_maes else None,
        "metrics": metric_summary,
    }


def consistent_misses(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    misses: list[dict[str, Any]] = []
    for metric in METRICS:
        signed = [row["errors"][metric] for row in rows if row["errors"][metric] is not None]
        if not signed or len(signed) != len(rows):
            continue
        if all(value > 0 for value in signed) or all(value < 0 for value in signed):
            direction = "overestimated" if signed[0] > 0 else "underestimated"
            misses.append(
                {
                    "metric": metric,
                    "direction": direction,
                    "mean-signed-error-pct": statistics.mean(signed),
                    "mean-absolute-error-pct": statistics.mean(abs(v) for v in signed),
                }
            )
    return misses


def front_matter(
    run_date: str,
    summary: dict[str, Any],
    misses: list[dict[str, Any]],
    previous: dict[str, Any] | None,
) -> str:
    payload = {
        "run-date": run_date,
        "subject-count": summary["subject-count"],
        "mean-absolute-error-pct": round1(summary["mean-absolute-error-pct"]),
        "median-subject-mae-pct": round1(summary["median-subject-mae-pct"]),
        "metrics": {
            metric: {key: round1(value) for key, value in values.items()}
            for metric, values in summary["metrics"].items()
        },
        "consistent-misses": [
            {
                "metric": miss["metric"],
                "direction": miss["direction"],
                "mean-signed-error-pct": round1(miss["mean-signed-error-pct"]),
                "mean-absolute-error-pct": round1(miss["mean-absolute-error-pct"]),
            }
            for miss in misses
        ],
        "comparison": previous,
    }
    return "---\n" + yaml.safe_dump(payload, sort_keys=False) + "---\n"


def metric_label(metric: str) -> str:
    return {
        "current-market-value": "Current market value",
        "maturity-market-value": "10-year market value",
        "hhi": "HHI",
    }[metric]


def comparison_summary(current: dict[str, Any], previous: dict[str, Any] | None) -> str:
    if previous is None or previous.get("previous-run-date") is None:
        return "No prior dated run was found, so this is the baseline for future methodology checks."
    change = previous.get("mean-absolute-error-change-pct")
    if change is None:
        return f"Compared with {previous['previous-run-date']}, the aggregate MAE change is not available."
    direction = "improved" if change < 0 else "worsened" if change > 0 else "was unchanged"
    return (
        f"Compared with {previous['previous-run-date']}, aggregate MAE {direction} "
        f"by {abs(change):.1f} percentage points."
    )


def render_markdown(
    run_date: str,
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    misses: list[dict[str, Any]],
    previous: dict[str, Any] | None,
) -> str:
    lines = [
        "# Market Analysis Back-Test Overall",
        "",
        "## Summary",
        "",
        (
            f"This run covered {summary['subject-count']} subject markets. "
            f"Mean subject MAE was {summary['mean-absolute-error-pct']:.1f}% and "
            f"median subject MAE was {summary['median-subject-mae-pct']:.1f}%."
        ),
        "",
        comparison_summary(summary, previous),
        "",
        "## Comparison",
        "",
    ]

    if previous is None or previous.get("previous-run-date") is None:
        lines.append("| Run | Mean subject MAE | Change |")
        lines.append("|---|---:|---:|")
        lines.append(f"| {run_date} | {summary['mean-absolute-error-pct']:.1f}% | n/a |")
    else:
        change = previous.get("mean-absolute-error-change-pct")
        lines.append("| Run | Mean subject MAE | Change vs prior |")
        lines.append("|---|---:|---:|")
        lines.append(
            f"| {run_date} | {summary['mean-absolute-error-pct']:.1f}% | {fmt_pct(change)} pts |"
        )
        lines.append(
            f"| {previous['previous-run-date']} | {previous['previous-mean-absolute-error-pct']:.1f}% | n/a |"
        )

    lines.extend(
        [
            "",
            "## Metric Accuracy",
            "",
            "| Metric | Mean signed error | Mean absolute error | Median absolute error |",
            "|---|---:|---:|---:|",
        ]
    )
    for metric, values in summary["metrics"].items():
        lines.append(
            "| "
            + metric_label(metric)
            + f" | {fmt_pct(values['mean-signed-error-pct'])} | "
            + f"{fmt_pct(values['mean-absolute-error-pct']).replace('+', '')} | "
            + f"{fmt_pct(values['median-absolute-error-pct']).replace('+', '')} |"
        )

    lines.extend(
        [
            "",
            "## Subject Scorecard",
            "",
            "| Market | Base year | Subject MAE | Current market-value error | 10-year market-value error | HHI error |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['market']} | {row['base-year']} | "
            f"{fmt_pct(row['mae']).replace('+', '')} | "
            f"{fmt_pct(row['errors']['current-market-value'])} | "
            f"{fmt_pct(row['errors']['maturity-market-value'])} | "
            f"{fmt_pct(row['errors']['hhi'])} |"
        )

    lines.extend(["", "## Consistent Misses", ""])
    if misses:
        for miss in misses:
            lines.append(
                f"- {metric_label(miss['metric'])} was {miss['direction']} in every subject "
                f"(mean signed error {fmt_pct(miss['mean-signed-error-pct'])}; "
                f"MAE {miss['mean-absolute-error-pct']:.1f}%)."
            )
    else:
        lines.append("No top-level metric was missed in the same direction across every subject.")

    lines.extend(
        [
            "",
            "## Subject Details",
            "",
            "| Market | Projection year | Generated 10-year market value | Benchmark 10-year market value | Generated HHI | Benchmark HHI |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        gen = row["generated"]
        bench = row["benchmark"]
        projection_year = int(row["base-year"]) + 10
        lines.append(
            f"| {row['market']} | {projection_year} | "
            f"{fmt_num(gen['maturity-market-value'])} | {fmt_num(bench['maturity-market-value'])} | "
            f"{fmt_num(gen['hhi'])} | {fmt_num(bench['hhi'])} |"
        )

    lines.extend(
        [
            "",
            "## Recommendations",
            "",
            "Review the per-subject accuracy docs for qualitative misses. Treat consistent aggregate misses as candidates for methodology changes only when the same issue would plausibly improve live market work.",
            "",
        ]
    )
    return "\n".join(lines)


def previous_comparison(data_dir: Path, run_date: str, current: dict[str, Any]) -> dict[str, Any] | None:
    previous_run = find_previous_run(data_dir, run_date)
    if previous_run is None:
        return {
            "previous-run-date": None,
            "mean-absolute-error-change-pct": None,
            "metric-changes-pct": {},
        }

    previous_rows = subject_rows(data_dir, previous_run)
    previous_summary = aggregate(previous_rows)
    current_mae = current["mean-absolute-error-pct"]
    previous_mae = previous_summary["mean-absolute-error-pct"]
    metric_changes = {}
    for metric in METRICS:
        current_metric = current["metrics"][metric]["mean-absolute-error-pct"]
        previous_metric = previous_summary["metrics"][metric]["mean-absolute-error-pct"]
        metric_changes[metric] = (
            None
            if current_metric is None or previous_metric is None
            else round1(current_metric - previous_metric)
        )
    return {
        "previous-run-date": previous_run.name,
        "previous-mean-absolute-error-pct": round1(previous_mae),
        "mean-absolute-error-change-pct": (
            None if current_mae is None or previous_mae is None else round1(current_mae - previous_mae)
        ),
        "metric-changes-pct": metric_changes,
    }


def write_overall(data_dir: Path, run_date: str) -> Path:
    run_dir = data_dir / run_date
    if not run_dir.exists():
        raise FileNotFoundError(f"run directory does not exist: {run_dir}")
    rows = subject_rows(data_dir, run_dir)
    summary = aggregate(rows)
    misses = consistent_misses(rows)
    previous = previous_comparison(data_dir, run_date, summary)
    output = front_matter(run_date, summary, misses, previous)
    output += "\n" + render_markdown(run_date, rows, summary, misses, previous)
    path = run_dir / "overall.md"
    path.write_text(output, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate overall.md for a market-analysis back-test run.")
    parser.add_argument(
        "run_date",
        nargs="?",
        default=dt.date.today().isoformat(),
        help="Back-test run date folder, YYYY-MM-DD. Defaults to today.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Back-test data directory containing benchmark/ and run-date folders.",
    )
    args = parser.parse_args()

    try:
        path = write_overall(args.data_dir, args.run_date)
    except Exception as exc:
        print(f"backtest_overall: {exc}", file=sys.stderr)
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
