#!/usr/bin/env python3
"""Fit, blend, and project logistic penetration curves.

Methodology and workflow live in references/penetration/penetration.md. The model is
p(t) = L / (1 + exp(-k * (t - t0))) with ceiling L asserted (not fitted) in the standard
workflow: with L fixed, logit(p/L) is linear in t, so k and t0 come from ordinary least
squares with proper standard errors and no dependencies beyond the stdlib (plus PyYAML
for the analog index).

Commands:
  fit      Fit one series CSV (fixed ceiling, or grid-search the ceiling for mature series).
  blend    Fit/blend/project from raw arguments, or read inputs from and write a market doc.
  project  Print the annual path for explicitly supplied parameters.
  list     Summarise the analog library.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "references" / "penetration" / "data"
WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_MARKET_DIR = WORKSPACE / "investment" / "market-docs"
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MIN_FIT_POINTS = 4
MIN_FREE_CEILING_POINTS = 6
MIN_ANALOGS = 2
MEASURES = {"stock", "new-sales-share", "spend-share"}
PRODUCTION_METHOD = "logistic-blend"


def logistic(t: float, ceiling: float, k: float, t0: float) -> float:
    return ceiling / (1.0 + math.exp(-k * (t - t0)))


def load_series(path: Path) -> tuple[list[tuple[float, float]], list[str]]:
    """Return [(year, penetration)] sorted by year, plus validation warnings."""
    warnings: list[str] = []
    rows: list[tuple[float, float]] = []
    with open(path, newline="") as fh:
        for i, row in enumerate(csv.reader(fh)):
            if not row or row[0].strip().startswith("#"):
                continue
            try:
                year, p = float(row[0]), float(row[1])
            except (ValueError, IndexError):
                if i == 0:
                    continue  # header
                raise SystemExit(f"{path}: unparseable row {i + 1}: {row}")
            if not 0.0 <= p < 1.0:
                raise SystemExit(f"{path}: penetration {p} at {year:g} outside [0, 1)")
            rows.append((year, p))
    rows.sort()
    years = [y for y, _ in rows]
    if len(set(years)) != len(years):
        raise SystemExit(f"{path}: duplicate years")
    for (y1, p1), (y2, p2) in zip(rows, rows[1:]):
        if p2 < p1 - 0.02:
            warnings.append(
                f"penetration falls {p1:.3f} -> {p2:.3f} between {y1:g} and {y2:g}; "
                "check the series is a stock measure, not noisy flow data"
            )
    return rows, warnings


def fit_fixed_ceiling(rows: list[tuple[float, float]], ceiling: float) -> dict:
    """OLS of logit(p / ceiling) on year. Returns params, standard errors, diagnostics."""
    usable = [(t, p) for t, p in rows if p > 0.0]
    dropped = len(rows) - len(usable)
    for t, p in usable:
        if p >= ceiling:
            raise SystemExit(
                f"observation {p:g} at {t:g} >= ceiling {ceiling:g}; raise --ceiling"
            )
    n = len(usable)
    if n < MIN_FIT_POINTS:
        raise SystemExit(f"need >= {MIN_FIT_POINTS} usable points, have {n}")
    ts = [t for t, _ in usable]
    ys = [math.log(p / (ceiling - p)) for _, p in usable]
    tbar, ybar = sum(ts) / n, sum(ys) / n
    sxx = sum((t - tbar) ** 2 for t in ts)
    sxy = sum((t - tbar) * (y - ybar) for t, y in zip(ts, ys))
    k = sxy / sxx
    a = ybar - k * tbar
    if k <= 0:
        raise SystemExit("fitted steepness k <= 0; series is not growing toward the ceiling")
    t0 = -a / k
    resid = [y - (a + k * t) for t, y in zip(ts, ys)]
    sse_logit = sum(r * r for r in resid)
    syy = sum((y - ybar) ** 2 for y in ys)
    r2 = 1.0 - sse_logit / syy if syy > 0 else float("nan")
    s2 = sse_logit / (n - 2)
    var_k = s2 / sxx
    # Delta method on the centered form t0 = tbar - ybar/k, where cov(ybar, k) = 0.
    var_t0 = (s2 / n) / k**2 + (ybar**2 / k**4) * var_k
    rmse_p = math.sqrt(
        sum((p - logistic(t, ceiling, k, t0)) ** 2 for t, p in usable) / n
    )
    return {
        "ceiling": ceiling,
        "k": k,
        "t0": t0,
        "se_k": math.sqrt(var_k),
        "se_t0": math.sqrt(max(var_t0, 0.0)),
        "n": n,
        "dropped_zero_points": dropped,
        "year_range": [ts[0], ts[-1]],
        "r2_logit": r2,
        "rmse_p": rmse_p,
    }


def fit_free_ceiling(rows: list[tuple[float, float]]) -> dict:
    """Grid-search the ceiling, OLS inside; pick minimum SSE in penetration space.

    Only meaningful for mature (post-inflection) series; the caller enforces the point
    minimum. Pre-inflection data cannot identify the ceiling — assert it instead.
    """
    max_p = max(p for _, p in rows)
    lo = min(max_p + 0.01, 0.999)
    best = None
    grid = [lo + i * 0.005 for i in range(int((1.0 - lo) / 0.005) + 1)]
    for ceiling in grid:
        fit = fit_fixed_ceiling(rows, ceiling)
        usable = [(t, p) for t, p in rows if p > 0.0]
        sse = sum((p - logistic(t, ceiling, fit["k"], fit["t0"])) ** 2 for t, p in usable)
        if best is None or sse < best[0]:
            best = (sse, fit)
    best[1]["ceiling_mode"] = "grid-search"
    return best[1]


def project(ceiling: float, k: float, t0: float, from_year: int, to_year: int) -> list[tuple[int, float]]:
    return [(y, logistic(y, ceiling, k, t0)) for y in range(from_year, to_year + 1)]


PLATEAU_FRAC = 0.9  # an analog's ceiling is only "observable" once it reaches this fraction of it


def truncate(rows: list[tuple[float, float]], as_of: int) -> list[tuple[float, float]]:
    return [(t, p) for t, p in rows if t <= as_of]


def maturity_year(rows: list[tuple[float, float]], ceiling: float, frac: float = PLATEAU_FRAC):
    """First year the series reaches `frac` of its ceiling, else None."""
    for t, p in rows:
        if p >= frac * ceiling:
            return int(t)
    return None


def load_index(data_dir: Path) -> dict[str, dict]:
    index_path = data_dir / "analogs.yaml"
    with open(index_path) as fh:
        doc = yaml.safe_load(fh)
    return {a["id"]: a for a in doc["analogs"]}


def prepare_analog(analog: dict, data_dir: Path, as_of: int | None = None):
    """Fit one analog. With `as_of` set (back-testing), truncate the series there and
    require the analog to have reached its plateau by then — otherwise its ceiling was
    not observable at the base year and borrowing it would leak the future. Returns
    (fit, None) when admissible, else (None, reason)."""
    rows, warnings = load_series(data_dir / "series" / f"{analog['id']}.csv")
    ceiling = float(analog["ceiling-estimate"])
    if as_of is not None:
        rows = truncate(rows, as_of)
        usable = [(t, p) for t, p in rows if p > 0.0]
        if len(usable) < MIN_FIT_POINTS:
            return None, f"only {len(usable)} points by {as_of}"
        if maturity_year(rows, ceiling) is None:
            top = max((p for _, p in rows), default=0.0)
            return None, f"only {top / ceiling:.0%} of ceiling by {as_of}, not yet plateaued"
    fit = fit_fixed_ceiling(rows, ceiling)
    fit["id"] = analog["id"]
    fit["warnings"] = warnings
    return fit, None


def print_fit(fit: dict, label: str = "fit") -> None:
    print(
        f"{label}: L={fit['ceiling']:.3f}  k={fit['k']:.4f} (se {fit['se_k']:.4f})  "
        f"t0={fit['t0']:.1f} (se {fit['se_t0']:.1f})  n={fit['n']} "
        f"[{fit['year_range'][0]:g}-{fit['year_range'][1]:g}]  "
        f"r2(logit)={fit['r2_logit']:.3f}  rmse(p)={fit['rmse_p']:.4f}"
    )


def print_path(path: list[tuple[int, float]]) -> None:
    for year, p in path:
        print(f"  {year}  {p:.4f}")


def cmd_fit(args: argparse.Namespace) -> int:
    rows, warnings = load_series(Path(args.series))
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if args.ceiling is not None:
        fit = fit_fixed_ceiling(rows, args.ceiling)
    else:
        if len(rows) < MIN_FREE_CEILING_POINTS:
            raise SystemExit(
                f"free-ceiling fit needs >= {MIN_FREE_CEILING_POINTS} points; "
                "pass --ceiling for short or pre-inflection series"
            )
        fit = fit_free_ceiling(rows)
    if args.json:
        print(json.dumps(fit, indent=2))
    else:
        print_fit(fit)
        if args.project_to:
            print_path(project(fit["ceiling"], fit["k"], fit["t0"],
                               int(rows[-1][0]), args.project_to))
    return 0


def blend_curve(
    series: Path,
    ceiling: float,
    analog_ids: list[str],
    horizon_year: int,
    data_dir: Path = DATA_DIR,
    as_of: int | None = None,
    w_fit_override: float | None = None,
    expected_measure: str | None = None,
) -> dict:
    """Blend a target fit with analog priors and return diagnostics plus a projection."""
    if not 0.0 < ceiling <= 1.0:
        raise SystemExit(f"ceiling must be in (0, 1], got {ceiling:g}")
    index = load_index(data_dir)
    unknown = [i for i in analog_ids if i not in index]
    if unknown:
        raise SystemExit(f"unknown analogs: {', '.join(unknown)} (see `list`)")
    if len(analog_ids) < MIN_ANALOGS:
        raise SystemExit(f"need >= {MIN_ANALOGS} analogs to form a prior")
    if expected_measure is not None:
        mismatched = [
            f"{analog_id} ({index[analog_id].get('measure', 'unspecified')})"
            for analog_id in analog_ids
            if index[analog_id].get("measure") != expected_measure
        ]
        if mismatched:
            raise SystemExit(
                f"analog measure must match target measure '{expected_measure}': "
                + ", ".join(mismatched)
            )

    analog_fits, excluded = [], []
    for i in analog_ids:
        fit, reason = prepare_analog(index[i], data_dir, as_of)
        (analog_fits if fit else excluded).append(fit or (i, reason))
    if len(analog_fits) < MIN_ANALOGS:
        detail = "; ".join(f"{i} ({r})" for i, r in excluded)
        raise SystemExit(
            f"only {len(analog_fits)} admissible analogs (need >= {MIN_ANALOGS}). "
            f"excluded: {detail}"
        )
    ks = [f["k"] for f in analog_fits]
    prior_k = sum(ks) / len(ks)
    prior_var = sum((k - prior_k) ** 2 for k in ks) / (len(ks) - 1)

    rows, warnings = load_series(series)
    if as_of is not None:
        rows = truncate(rows, as_of)
        if len(rows) < 1:
            raise SystemExit(f"no target data on or before {as_of}")
    if not rows:
        raise SystemExit(f"{series}: no target observations")
    t_last, p_last = rows[-1]
    if horizon_year < int(t_last):
        raise SystemExit(
            f"horizon year {horizon_year} is before latest target observation {t_last:g}"
        )
    if p_last >= ceiling:
        raise SystemExit(f"latest observation {p_last:g} >= ceiling {ceiling:g}")
    if p_last <= 0.0:
        raise SystemExit("latest target observation must be greater than zero to anchor the curve")

    usable = [(t, p) for t, p in rows if p > 0.0]
    target_fit = None
    if len(usable) >= MIN_FIT_POINTS:
        target_fit = fit_fixed_ceiling(rows, ceiling)
        w_fit = prior_var / (prior_var + target_fit["se_k"] ** 2) if prior_var > 0 else 1.0
    else:
        w_fit = 0.0
    if w_fit_override is not None:
        if not 0.0 <= w_fit_override <= 1.0:
            raise SystemExit(f"w-fit must be in [0, 1], got {w_fit_override:g}")
        if target_fit is None and w_fit_override > 0:
            raise SystemExit("--w-fit > 0 requires enough data points to fit the target")
        w_fit = w_fit_override

    # Prior curve: analog-mean steepness anchored through the latest observation.
    t0_prior = t_last - math.log(p_last / (ceiling - p_last)) / prior_k
    if target_fit:
        k_blend = w_fit * target_fit["k"] + (1 - w_fit) * prior_k
        t0_blend = w_fit * target_fit["t0"] + (1 - w_fit) * t0_prior
    else:
        k_blend, t0_blend = prior_k, t0_prior

    path = project(ceiling, k_blend, t0_blend, int(t_last), horizon_year)

    return {
        "analogs": analog_fits,
        "prior": {"k": prior_k, "sd_k": math.sqrt(prior_var), "t0_anchored": t0_prior},
        "target_fit": target_fit,
        "w_fit": w_fit,
        "blended": {"ceiling": ceiling, "k": k_blend, "t0": t0_blend},
        "projection": path,
        "excluded_analogs": [{"id": i, "reason": r} for i, r in excluded],
        "warnings": warnings,
        "target_points": len(usable),
    }


def _print_blend_result(result: dict, as_of: int | None, horizon: int) -> None:
    for warning in result["warnings"]:
        print(f"warning: {warning}", file=sys.stderr)
    if as_of is not None:
        print(f"as-of {as_of}: series and analogs truncated; only pre-{as_of} information used")
    for excluded in result["excluded_analogs"]:
        print(f"excluded analog {excluded['id']}: {excluded['reason']}")
    print("analog fits:")
    for fit in result["analogs"]:
        print_fit(fit, f"  {fit['id']}")
    prior = result["prior"]
    print(
        f"prior:   k={prior['k']:.4f} "
        f"(sd {prior['sd_k']:.4f} across {len(result['analogs'])} analogs)"
    )
    if result["target_fit"]:
        print_fit(result["target_fit"], "target ")
    else:
        print(
            f"target : too few usable points ({result['target_points']}) "
            "to fit; using prior only"
        )
    w_fit = result["w_fit"]
    blended = result["blended"]
    print(f"weight : w_fit={w_fit:.2f} (fit) / {1 - w_fit:.2f} (prior)")
    print(
        f"blended: L={blended['ceiling']:.3f}  "
        f"k={blended['k']:.4f}  t0={blended['t0']:.1f}"
    )
    print(f"projection to {horizon}:")
    print_path(result["projection"])


def split_front_matter(text: str) -> tuple[str, dict]:
    """Parse a market-doc front-matter block while retaining its original text."""
    match = FM_RE.match(text)
    if not match:
        raise SystemExit("market-doc has no YAML front matter (must start with a '---' block)")
    block = match.group(1)
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as exc:
        raise SystemExit(f"could not parse market-doc front matter as YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("market-doc front matter must be a YAML mapping")
    return block, data


def resolve_market_doc(arg: str, market_dir: Path) -> Path:
    """Resolve a market id or explicit Markdown path."""
    path = Path(arg)
    if path.suffix == ".md" or "/" in arg:
        return path
    market_id = arg.strip().lower().replace("_", "-").replace(" ", "-")
    return market_dir / f"{market_id}.md"


def _number(mapping: dict, key: str, source: str) -> float:
    try:
        return float(mapping[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"{source}.{key} must be a number") from exc


def validate_logistic_parameters(L: float, t0: float, k: float, source: str) -> None:
    if not 0.0 < L <= 1.0:
        raise SystemExit(f"{source}.L must be in (0, 1]")
    if not math.isfinite(t0):
        raise SystemExit(f"{source}.t0 must be finite")
    if not math.isfinite(k) or k <= 0.0:
        raise SystemExit(f"{source}.k must be greater than zero")


def market_doc_penetration_inputs(
    front_matter: dict, market_doc: Path
) -> tuple[Path, str, float, list[str], float | None, int | None]:
    """Read and validate analyst-owned penetration inputs."""
    penetration = front_matter.get("penetration")
    inputs = penetration.get("inputs") if isinstance(penetration, dict) else None
    if not isinstance(inputs, dict):
        raise SystemExit("market-doc has no 'penetration.inputs' mapping")

    target_value = inputs.get("target-series")
    if not isinstance(target_value, str) or not target_value.strip():
        raise SystemExit("penetration.inputs.target-series must be a non-empty path")
    target_series = Path(target_value)
    if not target_series.is_absolute():
        target_series = market_doc.parent / target_series
    if not target_series.exists():
        raise SystemExit(f"penetration target series not found: {target_series}")

    measure = inputs.get("measure")
    if measure not in MEASURES:
        raise SystemExit(
            "penetration.inputs.measure must be one of: " + ", ".join(sorted(MEASURES))
        )
    ceiling = _number(inputs, "ceiling", "penetration.inputs")
    if not 0.0 < ceiling <= 1.0:
        raise SystemExit("penetration.inputs.ceiling must be in (0, 1]")

    analogs = inputs.get("analogs")
    if (
        not isinstance(analogs, list)
        or len(analogs) < MIN_ANALOGS
        or any(not isinstance(value, str) or not value.strip() for value in analogs)
    ):
        raise SystemExit(
            f"penetration.inputs.analogs must contain at least {MIN_ANALOGS} analog ids"
        )
    analog_ids = [value.strip() for value in analogs]
    if len(set(analog_ids)) != len(analog_ids):
        raise SystemExit("penetration.inputs.analogs must not contain duplicates")

    w_fit = inputs.get("w-fit")
    if w_fit is not None:
        try:
            w_fit = float(w_fit)
        except (TypeError, ValueError) as exc:
            raise SystemExit("penetration.inputs.w-fit must be a number in [0, 1]") from exc
        if not 0.0 <= w_fit <= 1.0:
            raise SystemExit("penetration.inputs.w-fit must be in [0, 1]")

    as_of = inputs.get("as-of-year")
    if as_of is not None:
        try:
            as_of = int(as_of)
        except (TypeError, ValueError) as exc:
            raise SystemExit("penetration.inputs.as-of-year must be an integer year") from exc
    return target_series, measure, ceiling, analog_ids, w_fit, as_of


def market_doc_penetration_override(
    front_matter: dict,
) -> tuple[float, float, float, str] | None:
    """Return the optional analyst-owned (L, t0, k, reason) override."""
    penetration = front_matter.get("penetration")
    override = penetration.get("override") if isinstance(penetration, dict) else None
    if override is None:
        return None
    if not isinstance(override, dict):
        raise SystemExit("penetration.override must be a mapping or be omitted")
    L = _number(override, "L", "penetration.override")
    t0 = _number(override, "t0", "penetration.override")
    k = _number(override, "k", "penetration.override")
    reason = override.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise SystemExit("penetration.override requires a non-empty reason")
    validate_logistic_parameters(L, t0, k, "penetration.override")
    return L, t0, k, reason.strip()


def penetration_doc_result(
    front_matter: dict,
    market_doc: Path,
    data_dir: Path = DATA_DIR,
) -> dict:
    """Fit the model estimate and resolve the optional analyst override."""
    try:
        base_year = int(front_matter["base-year"])
        duration = int(front_matter["maturity-duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit("market-doc requires integer base-year and maturity-duration") from exc
    if duration <= 0:
        raise SystemExit("maturity-duration must be greater than zero")
    horizon = base_year + duration

    series, measure, ceiling, analogs, w_fit, as_of = market_doc_penetration_inputs(
        front_matter, market_doc
    )
    fitted = blend_curve(
        series,
        ceiling,
        analogs,
        horizon,
        data_dir,
        as_of,
        w_fit,
        expected_measure=measure,
    )
    blended = fitted["blended"]
    estimate = {
        "L": blended["ceiling"],
        "t0": blended["t0"],
        "k": blended["k"],
    }
    override = market_doc_penetration_override(front_matter)
    if override is None:
        selected = dict(estimate)
        selected_from = "model-estimate"
    else:
        L, t0, k, _ = override
        selected = {"L": L, "t0": t0, "k": k}
        selected_from = "override"

    return {
        "model-estimate": estimate,
        "selected": selected,
        "selected-from": selected_from,
        "w-fit": fitted["w_fit"],
        "projection": project(
            selected["L"], selected["k"], selected["t0"], base_year, horizon
        ),
        "method": PRODUCTION_METHOD,
        "diagnostics": fitted,
    }


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def upsert_penetration_child(block: str, key: str, value: str | dict[str, float]) -> str:
    """Surgically replace or append one script-owned child of `penetration`."""
    lines = block.splitlines()
    parent_i = next(
        (i for i, line in enumerate(lines) if re.fullmatch(r"penetration:\s*", line)),
        None,
    )
    if parent_i is None:
        raise SystemExit("cannot write back: market-doc has no top-level 'penetration:' block")
    parent_indent = _indent(lines[parent_i])
    child_indent = parent_indent + 2
    parent_end = len(lines)
    for i in range(parent_i + 1, len(lines)):
        if not lines[i].strip():
            continue
        indent = _indent(lines[i])
        if indent <= parent_indent:
            parent_end = i
            break
        child_indent = min(child_indent, indent)

    child_i = None
    for i in range(parent_i + 1, parent_end):
        if not lines[i].strip() or _indent(lines[i]) != child_indent:
            continue
        if re.match(rf"{' ' * child_indent}{re.escape(key)}:\s*", lines[i]):
            child_i = i
            break

    if isinstance(value, dict):
        replacement = [f"{' ' * child_indent}{key}:"]
        replacement.extend(
            f"{' ' * (child_indent + 2)}{child}: {round(number, 6)}"
            for child, number in value.items()
        )
    else:
        replacement = [f"{' ' * child_indent}{key}: {value}"]

    if child_i is None:
        lines[parent_end:parent_end] = replacement
        return "\n".join(lines)
    child_end = parent_end
    for i in range(child_i + 1, parent_end):
        if lines[i].strip() and _indent(lines[i]) <= child_indent:
            child_end = i
            break
    lines[child_i:child_end] = replacement
    return "\n".join(lines)


def resolve_stamp_date(arg: str | None) -> str:
    if arg is None:
        return date.today().isoformat()
    try:
        return date.fromisoformat(arg).isoformat()
    except ValueError as exc:
        raise SystemExit(f"--stamp-date must be YYYY-MM-DD, got {arg!r}") from exc


def write_penetration_outputs(path: Path, result: dict, stamp_date: str) -> None:
    """Write only script-owned penetration outputs; preserve inputs, override and body."""
    text = path.read_text(encoding="utf-8")
    match = FM_RE.match(text)
    if not match:
        raise SystemExit(f"cannot write back: {path} has no front-matter block")
    block = match.group(1)
    block = upsert_penetration_child(block, "model-estimate", result["model-estimate"])
    block = upsert_penetration_child(block, "method", result["method"])
    block = upsert_penetration_child(block, "date", stamp_date)
    path.write_text(f"---\n{block}\n---\n" + text[match.end():], encoding="utf-8")


def cmd_blend_market_doc(args: argparse.Namespace) -> int:
    if args.series or args.ceiling is not None or args.analogs:
        raise SystemExit(
            "--market-doc reads series, ceiling and analogs from penetration.inputs; "
            "do not also pass raw blend inputs"
        )
    if args.horizon_year is not None or args.as_of is not None or args.w_fit is not None:
        raise SystemExit(
            "--market-doc derives its horizon and reads as-of-year/w-fit from "
            "penetration.inputs"
        )
    path = resolve_market_doc(args.market_doc, Path(args.market_dir))
    if not path.exists():
        raise SystemExit(f"market-doc not found: {path}")
    _, front_matter = split_front_matter(path.read_text(encoding="utf-8"))
    result = penetration_doc_result(front_matter, path, Path(args.data_dir))
    stamp_date = resolve_stamp_date(args.stamp_date)
    wrote = not args.dry_run
    if wrote:
        write_penetration_outputs(path, result, stamp_date)
    output = {
        **result,
        "date": stamp_date,
        "market-doc": str(path),
        "written": wrote,
    }
    for warning in result["diagnostics"]["warnings"]:
        print(f"warning: {warning}", file=sys.stderr)
    for excluded in result["diagnostics"]["excluded_analogs"]:
        print(
            f"excluded analog {excluded['id']}: {excluded['reason']}",
            file=sys.stderr,
        )
    if args.json:
        print(json.dumps(output, indent=2))
        return 0

    estimate = result["model-estimate"]
    selected = result["selected"]
    print(
        f"{path.stem}: model L={estimate['L']:.3f}, k={estimate['k']:.4f}, "
        f"t0={estimate['t0']:.1f}; selected from {result['selected-from']} "
        f"L={selected['L']:.3f}, k={selected['k']:.4f}, t0={selected['t0']:.1f}"
    )
    print(f"weight: w_fit={result['w-fit']:.2f}")
    print("annual penetration path:")
    print_path(result["projection"])
    print(f"{'written to ' + str(path) if wrote else 'dry run — not written'}")
    return 0


def cmd_blend(args: argparse.Namespace) -> int:
    if args.market_doc:
        return cmd_blend_market_doc(args)
    if not args.series:
        raise SystemExit("blend requires SERIES or --market-doc")
    if args.ceiling is None:
        raise SystemExit("raw blend mode requires --ceiling")
    if not args.analogs:
        raise SystemExit("raw blend mode requires --analogs")

    ids = [value.strip() for value in args.analogs.split(",") if value.strip()]
    rows, _ = load_series(Path(args.series))
    if args.as_of is not None:
        rows = truncate(rows, args.as_of)
    if not rows:
        raise SystemExit(f"{args.series}: no target observations")
    horizon = args.horizon_year or int(rows[-1][0]) + 10
    result = blend_curve(
        Path(args.series),
        args.ceiling,
        ids,
        horizon,
        Path(args.data_dir),
        args.as_of,
        args.w_fit,
    )
    if args.json:
        for warning in result["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
        print(json.dumps(result, indent=2))
        return 0

    _print_blend_result(result, args.as_of, horizon)
    return 0


def cmd_project(args: argparse.Namespace) -> int:
    print_path(project(args.ceiling, args.k, args.t0, args.from_year, args.to_year))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    index = load_index(data_dir)
    print(f"{'id':<28} {'measure':<16} {'ceiling':>7} {'matured':>7} {'years':<11} categories")
    for analog in index.values():
        rows, _ = load_series(data_dir / "series" / f"{analog['id']}.csv")
        years = f"{rows[0][0]:g}-{rows[-1][0]:g}"
        my = maturity_year(rows, float(analog["ceiling-estimate"]))
        print(
            f"{analog['id']:<28} {analog['measure']:<16} "
            f"{analog['ceiling-estimate']:>7.2f} {str(my or '-'):>7} {years:<11} "
            f"{','.join(analog.get('categories', []))}"
        )
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fit", help="fit a logistic to one series CSV")
    f.add_argument("series", help="CSV of year,penetration rows")
    f.add_argument("--ceiling", type=float, help="fixed saturation ceiling L (recommended)")
    f.add_argument("--project-to", type=int, help="also print the annual path to this year")
    f.add_argument("--json", action="store_true")
    f.set_defaults(func=cmd_fit)

    b = sub.add_parser(
        "blend",
        help="blend a target fit with analog priors; optionally read/write a market doc",
    )
    b.add_argument("series", nargs="?", help="raw mode: target CSV of year,penetration rows")
    b.add_argument("--ceiling", type=float, help="raw mode: target saturation ceiling L")
    b.add_argument("--analogs", help="raw mode: comma-separated analog ids")
    b.add_argument(
        "--market-doc",
        help="market id or Markdown path; read penetration.inputs and write model outputs",
    )
    b.add_argument("--horizon-year", type=int, help="default: last data year + 10")
    b.add_argument("--as-of", type=int,
                   help="back-test cutoff: truncate target and analogs at this year and drop "
                        "analogs not yet plateaued by then (see penetration/back-test)")
    b.add_argument("--w-fit", type=float,
                   help="override the computed fit weight (0-1); see penetration.md guidance")
    b.add_argument("--data-dir", default=str(DATA_DIR))
    b.add_argument("--market-dir", default=str(DEFAULT_MARKET_DIR))
    b.add_argument(
        "--dry-run",
        action="store_true",
        help="market-doc mode: calculate without writing",
    )
    b.add_argument(
        "--stamp-date",
        help="market-doc mode: output date, YYYY-MM-DD (default today)",
    )
    b.add_argument("--json", action="store_true")
    b.set_defaults(func=cmd_blend)

    pr = sub.add_parser("project", help="annual path for explicit parameters")
    pr.add_argument("--ceiling", type=float, required=True)
    pr.add_argument("--k", type=float, required=True)
    pr.add_argument("--t0", type=float, required=True)
    pr.add_argument("--from-year", type=int, required=True)
    pr.add_argument("--to-year", type=int, required=True)
    pr.set_defaults(func=cmd_project)

    ls = sub.add_parser("list", help="summarise the analog library")
    ls.add_argument("--data-dir", default=str(DATA_DIR))
    ls.set_defaults(func=cmd_list)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
