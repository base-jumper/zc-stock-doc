#!/usr/bin/env python3
"""Score a penetration back-test run and write per-cell accuracy docs plus overall.md.

A run lives at references/penetration/back-test/data/<run-date>/ with one prediction per
(subject, base-year) cell in predictions/<subject>-<base-year>.md. Each prediction is scored
against the frozen benchmark series for its subject. All metrics are in penetration points
(pp), not the relative-% used by the market-value back-test — near-zero early penetrations make
relative error meaningless.

Every miss is decomposed against a hindsight-optimal logistic (the best logistic fit to the full
realized series):
  model-form floor = how far the best possible logistic sits from reality (irreducible; high only
                     when the market does not follow an S-curve at all)
  forecast gap     = how far the forecaster's base-year curve sits from that best logistic
                     (the judgment component: ceiling, analog choice, blend weight)

Usage:
  penetration_backtest.py score <run-date> [--data-dir DIR] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import statistics
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from penetration_fit import fit_free_ceiling, load_series, logistic  # noqa: E402

BACKTEST_DIR = (
    Path(__file__).resolve().parent.parent
    / "references" / "penetration" / "back-test" / "data"
)
HORIZON = 10


def read_front_matter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing front matter")
    _, fm, _ = text.split("---", 2)
    return yaml.safe_load(fm)


def interp(series: list[tuple[float, float]], year: float) -> float:
    if year <= series[0][0]:
        return series[0][1]
    if year >= series[-1][0]:
        return series[-1][1]
    for (t1, p1), (t2, p2) in zip(series, series[1:]):
        if t1 <= year <= t2:
            return p1 + (p2 - p1) * (year - t1) / (t2 - t1)
    return series[-1][1]


def actual_cross_year(series, target: float):
    """Year the realized series first reaches `target`, by linear interpolation."""
    for (t1, p1), (t2, p2) in zip(series, series[1:]):
        if p1 <= target <= p2 and p2 > p1:
            return t1 + (target - p1) * (t2 - t1) / (p2 - p1)
    return None


def pred_cross_year(ceiling, k, t0, target: float):
    import math
    if target >= ceiling:
        return None
    return t0 - math.log(ceiling / target - 1.0) / k


def score_cell(pred_fm: dict, benchmark_dir: Path) -> dict:
    subject = pred_fm["subject"]
    base = int(pred_fm["base-year"])
    logistic_params = pred_fm["penetration"]["logistic"]
    L = float(logistic_params["L"])
    k = float(logistic_params["k"])
    t0 = float(logistic_params["t0"])

    bench_fm = read_front_matter(benchmark_dir / f"{subject}.md")
    realized_ceiling = float(bench_fm["realized-ceiling"])
    series, _ = load_series(benchmark_dir / bench_fm["series"])

    horizon_year = base + HORIZON
    last = int(series[-1][0])
    window = [y for y in range(base + 1, min(horizon_year, last) + 1)]

    def pred(y):
        return logistic(y, L, k, t0)

    abs_errs = [abs(pred(y) - interp(series, y)) for y in window]
    path_mae = 100 * statistics.mean(abs_errs) if abs_errs else float("nan")
    hy = min(horizon_year, last)
    horizon_err = 100 * (pred(hy) - interp(series, hy))
    ceiling_err = 100 * (L - realized_ceiling)

    # Timing: years to half of realized ceiling.
    target = 0.5 * realized_ceiling
    ap, pp = actual_cross_year(series, target), pred_cross_year(L, k, t0, target)
    timing_err = (pp - ap) if (ap is not None and pp is not None) else None

    # Hindsight-optimal logistic on the full realized series -> model-form floor.
    hind = fit_free_ceiling(series)
    floor_errs = [abs(logistic(y, hind["ceiling"], hind["k"], hind["t0"]) - interp(series, y))
                  for y in window]
    floor_mae = 100 * statistics.mean(floor_errs) if floor_errs else float("nan")
    gap_errs = [abs(pred(y) - logistic(y, hind["ceiling"], hind["k"], hind["t0"]))
                for y in window]
    gap_mae = 100 * statistics.mean(gap_errs) if gap_errs else float("nan")

    return {
        "subject": subject,
        "base_year": base,
        "horizon_year": hy,
        "pred": {"ceiling": L, "k": k, "t0": t0},
        "path_mae_pp": path_mae,
        "horizon_error_pp": horizon_err,
        "ceiling_error_pp": ceiling_err,
        "timing_error_years": timing_err,
        "model_form_floor_pp": floor_mae,
        "forecast_gap_pp": gap_mae,
        "hindsight": {"ceiling": hind["ceiling"], "k": hind["k"], "t0": hind["t0"]},
        "realized_ceiling": realized_ceiling,
        "window": [window[0], window[-1]] if window else None,
        "analogs_used": pred_fm.get("analogs-used", []),
        "w_fit": pred_fm.get("w-fit"),
    }


def fmt(x, nd=1, unit=""):
    return "n/a" if x is None else f"{x:+.{nd}f}{unit}" if unit == "" else f"{x:.{nd}f}{unit}"


ACCURACY_FM_KEYS = [
    "path_mae_pp", "horizon_error_pp", "ceiling_error_pp",
    "timing_error_years", "model_form_floor_pp", "forecast_gap_pp",
]


def write_accuracy(cell: dict, out_dir: Path) -> Path:
    name = f"{cell['subject']}-{cell['base_year']}"
    fm = {
        "subject": cell["subject"],
        "base-year": cell["base_year"],
        "horizon-year": cell["horizon_year"],
        "metrics": {
            "path-mae-pp": round(cell["path_mae_pp"], 2),
            "horizon-error-pp": round(cell["horizon_error_pp"], 2),
            "ceiling-error-pp": round(cell["ceiling_error_pp"], 2),
            "timing-error-years": (None if cell["timing_error_years"] is None
                                   else round(cell["timing_error_years"], 2)),
            "model-form-floor-pp": round(cell["model_form_floor_pp"], 2),
            "forecast-gap-pp": round(cell["forecast_gap_pp"], 2),
        },
    }
    p = cell["pred"]
    body = f"""# {name} Back-Test Accuracy

## Scorecard

| Metric | Value | Read as |
|---|---:|---|
| Path MAE | {cell['path_mae_pp']:.1f} pp | mean abs error over {cell['window'][0]}-{cell['window'][1]} |
| Horizon error ({cell['horizon_year']}) | {cell['horizon_error_pp']:+.1f} pp | +over / -under-predicted final penetration |
| Ceiling error | {cell['ceiling_error_pp']:+.1f} pp | asserted {p['ceiling']:.2f} vs realized {cell['realized_ceiling']:.2f} |
| Timing error | {fmt(cell['timing_error_years'])} yr | +late / -early to half of realized ceiling |
| Model-form floor | {cell['model_form_floor_pp']:.1f} pp | irreducible: best logistic vs reality |
| Forecast gap | {cell['forecast_gap_pp']:.1f} pp | judgment: forecast vs best logistic |

Predicted logistic L={p['ceiling']:.2f} k={p['k']:.3f} t0={p['t0']}; hindsight-optimal \
L={cell['hindsight']['ceiling']:.2f} k={cell['hindsight']['k']:.3f} t0={cell['hindsight']['t0']:.0f}. \
Analogs used: {', '.join(cell['analogs_used']) or 'n/a'}; w_fit={cell['w_fit']}.

## Attribution

<!-- Written after scoring. Is the miss model-form (floor high -> market is not an S-curve) or
     judgment (gap high -> ceiling / analog / weight choice)? Which lever dominated? -->

## Issues And Recommendations

<!-- Pull from the prediction's Issues section and the numbers above. Only propose skill changes
     that would also help live work. -->
"""
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False).strip() + "\n---\n" + body
    out_path = out_dir / f"{name}.md"
    out_path.write_text(text)
    return out_path


def write_overall(cells: list[dict], run_date: str, out_dir: Path) -> Path:
    maes = [c["path_mae_pp"] for c in cells]
    fm = {
        "run-date": run_date,
        "cell-count": len(cells),
        "mean-path-mae-pp": round(statistics.mean(maes), 2),
        "median-path-mae-pp": round(statistics.median(maes), 2),
        "mean-ceiling-error-pp": round(
            statistics.mean(c["ceiling_error_pp"] for c in cells), 2),
        "mean-model-form-floor-pp": round(
            statistics.mean(c["model_form_floor_pp"] for c in cells), 2),
        "mean-forecast-gap-pp": round(
            statistics.mean(c["forecast_gap_pp"] for c in cells), 2),
    }

    # Per subject, show error vs base-year to check the blend claim (more history -> less error).
    subjects: dict[str, list[dict]] = {}
    for c in cells:
        subjects.setdefault(c["subject"], []).append(c)
    regime_rows = []
    for subj, cs in sorted(subjects.items()):
        for c in sorted(cs, key=lambda x: x["base_year"]):
            regime_rows.append(
                f"| {subj} | {c['base_year']} | {c['path_mae_pp']:.1f} | "
                f"{c['horizon_error_pp']:+.1f} | {c['ceiling_error_pp']:+.1f} | "
                f"{c['model_form_floor_pp']:.1f} | {c['forecast_gap_pp']:.1f} |"
            )

    body = f"""# Penetration Back-Test Overall

## Summary

{len(cells)} cells across {len(subjects)} subjects. Mean path MAE {fm['mean-path-mae-pp']:.1f} pp,
median {fm['median-path-mae-pp']:.1f} pp. Mean model-form floor {fm['mean-model-form-floor-pp']:.1f} pp
(irreducible); mean forecast gap {fm['mean-forecast-gap-pp']:.1f} pp (judgment).

## Cells

| Subject | Base year | Path MAE (pp) | Horizon err (pp) | Ceiling err (pp) | Floor (pp) | Gap (pp) |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(regime_rows)}

## Reading This Run

- Within a subject, path MAE should fall as the base-year advances — that is the blend claim
  (priors early, fit late) working. Where it does not, inspect the cell.
- A high model-form floor flags a market the logistic cannot represent; a high forecast gap with a
  low floor flags a judgment miss (usually ceiling).
- Ceiling error is the leakage-sensitive lever: a suspiciously small ceiling error at an early
  base-year may indicate hindsight crept into the ceiling assertion.

## Recommendations

<!-- Orchestrator synthesis: consistent misses across cells, and concrete skill changes. -->
"""
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False).strip() + "\n---\n" + body
    out_path = out_dir / "overall.md"
    out_path.write_text(text)
    return out_path


def cmd_score(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    run_dir = data_dir / args.run_date
    pred_dir = run_dir / "predictions"
    if not pred_dir.is_dir():
        raise SystemExit(f"no predictions folder at {pred_dir}")
    benchmark_dir = data_dir / "benchmark"
    acc_dir = run_dir / "accuracy"
    acc_dir.mkdir(exist_ok=True)

    cells = []
    for pred_path in sorted(pred_dir.glob("*.md")):
        cell = score_cell(read_front_matter(pred_path), benchmark_dir)
        cells.append(cell)
        print(
            f"{cell['subject']}-{cell['base_year']}: "
            f"MAE {cell['path_mae_pp']:.1f}pp  horizon {cell['horizon_error_pp']:+.1f}pp  "
            f"ceiling {cell['ceiling_error_pp']:+.1f}pp  floor {cell['model_form_floor_pp']:.1f}pp  "
            f"gap {cell['forecast_gap_pp']:.1f}pp"
        )
    if not cells:
        raise SystemExit("no predictions found to score")
    if args.dry_run:
        return 0
    for cell in cells:
        write_accuracy(cell, acc_dir)
    overall = write_overall(cells, args.run_date, run_dir)
    print(f"wrote {len(cells)} accuracy docs and {overall}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score", help="score a run and write accuracy + overall docs")
    s.add_argument("run_date", nargs="?", default=dt.date.today().isoformat())
    s.add_argument("--data-dir", default=str(BACKTEST_DIR))
    s.add_argument("--dry-run", action="store_true", help="print metrics without writing docs")
    s.set_defaults(func=cmd_score)
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
