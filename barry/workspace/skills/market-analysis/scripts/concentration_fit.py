#!/usr/bin/env python3
"""Fit and project geometric rank-share concentration curves.

Methodology and workflow live in references/concentration/concentration.md. The model is a
two-parameter geometric rank-share law:

    share(i) = s1 * r**(i - 1)          i = 1, 2, 3, ... (rank, 1 = largest)

with s1 the leader's share and r in (0, 1) the rank-to-rank decay ratio. Realized calibration
shares are summarized by anchoring s1 to the observed leader share and choosing r to reproduce
the empirical HHI. The modeled players need not sum to 1: the remainder 1 - s1/(1 - r) is an
atomistic competitive fringe whose HHI contribution vanishes, so

    HHI               = s1**2 / (1 - r**2)
    effective players = 1 / HHI

are exact for the whole market. capture(i) = share(i) for each named player slotted into a rank.

Commands:
  fit      Summarize one rank,share CSV as s1, r, HHI / effective players / fit quality.
  fit-moments
           Summarize one aggregate concentration-moment row as s1, r / fit quality.
  params   Predict s1, r, HHI from CLI traits, or read inputs from a market doc and write back.
  project  Emit the HHI, effective-player count, and capture table for explicit s1, r.
  list     Summarise the calibration library (fit each entry's outcome).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "references" / "concentration" / "data"
WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_MARKET_DIR = WORKSPACE / "investment" / "market-docs"
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MIN_FIT_POINTS = 2
GEOM_RMSE_WARN = 0.03  # above this, a single geometric describes the shape poorly (flat top / detached tail)
MOMENT_TOP_RANKS = (4, 8)
MOMENT_TAIL_RANKS = (20, 50)
MOMENT_TOP_RMSE_WARN = 0.03
MOMENT_TAIL_RMSE_WARN = 0.08
SYNTHETIC_OUTCOME_QUALITY = "synthetic-geometric-shares"
SYNTHETIC_SHARE_MARKER = "# synthetic-geometric-shares"

# Candidate trait groups remain available to concentration_evaluate.py. Production uses the frozen,
# nested-CV-selected direct ridge specification below; feature selection and alpha tuning never run
# in this module.
DOMINANCE_TRAITS = ["network-effects", "data-scale-advantage", "brand-reputation"]
BARRIER_TRAITS = ["capital-intensity", "scale-economies", "regulatory-barriers", "switching-costs"]
PRODUCTION_TRAITS = ["network-effects", "scale-economies", "switching-costs"]
PRODUCTION_RIDGE_ALPHA = 1.0
PRODUCTION_MODEL = "selected-direct-ridge"
TRAIT_ALIASES = {
    "ne": "network-effects", "dsa": "data-scale-advantage", "br": "brand-reputation",
    "sc": "switching-costs", "ci": "capital-intensity", "se": "scale-economies",
    "rb": "regulatory-barriers",
}
S1_CLIP = (0.02, 0.99)
R_CLIP = (0.02, 0.98)
ALL_TRAITS = list(dict.fromkeys(DOMINANCE_TRAITS + BARRIER_TRAITS))


@dataclass
class RidgeModel:
    means: list[float]
    scales: list[float]
    coefficients: list[float]

    def predict(self, values: list[float]) -> float:
        if len(values) != len(self.means):
            raise ValueError(f"expected {len(self.means)} features, got {len(values)}")
        standardized = [
            (value - mean) / scale
            for value, mean, scale in zip(values, self.means, self.scales)
        ]
        return self.coefficients[0] + sum(
            coefficient * value
            for coefficient, value in zip(self.coefficients[1:], standardized)
        )


def _solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """Solve a small dense linear system with partial-pivot Gaussian elimination."""
    n = len(vector)
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("singular regression system")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            multiplier = augmented[row][column]
            if multiplier:
                augmented[row] = [
                    value - multiplier * pivot_value
                    for value, pivot_value in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(n)]


def fit_ridge(xs: list[list[float]], ys: list[float], alpha: float) -> RidgeModel:
    """Fit standardized ridge regression with an unpenalized intercept."""
    if not xs or len(xs) != len(ys):
        raise ValueError("ridge regression requires matched non-empty x/y rows")
    width = len(xs[0])
    if any(len(row) != width for row in xs):
        raise ValueError("ridge regression feature rows have inconsistent widths")
    means = [sum(row[j] for row in xs) / len(xs) for j in range(width)]
    scales = []
    for j, mean in enumerate(means):
        variance = sum((row[j] - mean) ** 2 for row in xs) / len(xs)
        scales.append(math.sqrt(variance) if variance > 1e-16 else 1.0)
    design = [
        [1.0] + [(row[j] - means[j]) / scales[j] for j in range(width)]
        for row in xs
    ]
    size = width + 1
    gram = [
        [sum(row[i] * row[j] for row in design) for j in range(size)]
        for i in range(size)
    ]
    rhs = [sum(row[i] * y for row, y in zip(design, ys)) for i in range(size)]
    for j in range(1, size):
        gram[j][j] += alpha + 1e-12
    return RidgeModel(means, scales, _solve(gram, rhs))


def geometric(rank: int, s1: float, r: float) -> float:
    return s1 * r ** (rank - 1)


def hhi(s1: float, r: float) -> float:
    """Whole-market HHI of the infinite geometric tail: s1**2 / (1 - r**2)."""
    return s1 * s1 / (1.0 - r * r)


def concentration_ratio(rank: int, s1: float, r: float) -> float:
    """Cumulative modeled share of ranks 1..rank."""
    return s1 * (1.0 - r ** rank) / (1.0 - r)


def load_shares(path: Path) -> tuple[list[tuple[int, float]], list[str]]:
    """Return [(rank, share)] sorted by rank, plus validation warnings."""
    warnings: list[str] = []
    rows: list[tuple[int, float]] = []
    with open(path, newline="") as fh:
        for i, row in enumerate(csv.reader(fh)):
            if not row or row[0].strip().startswith("#"):
                continue
            if row[0].strip().lower() == "rank":
                continue
            try:
                rank, share = int(row[0]), float(row[1])
            except (ValueError, IndexError):
                raise SystemExit(f"{path}: unparseable row {i + 1}: {row}")
            if not 0.0 < share <= 1.0:
                raise SystemExit(f"{path}: share {share} at rank {rank} outside (0, 1]")
            rows.append((rank, share))
    rows.sort()
    ranks = [i for i, _ in rows]
    if ranks != list(range(1, len(ranks) + 1)):
        raise SystemExit(f"{path}: ranks must be 1..N with no gaps, got {ranks}")
    total = sum(s for _, s in rows)
    if total > 1.02:
        raise SystemExit(f"{path}: shares sum to {total:.3f} > 1")
    for (r1, s1_), (r2, s2) in zip(rows, rows[1:]):
        if s2 > s1_ + 1e-9:
            warnings.append(
                f"share rises {s1_:.3f} -> {s2:.3f} from rank {r1} to {r2}; "
                "ranks must be ordered largest-first"
            )
    return rows, warnings


def fit_geometric(rows: list[tuple[int, float]]) -> dict:
    """Summarise a realized distribution as (s1, r), moment-matched not least-squares.

    s1 is anchored to the observed leader share (the most decision-relevant point and the bulk
    of HHI), and r is chosen so the geometric's whole-market HHI equals the empirical HHI:
    HHI = s1**2 / (1 - r**2)  =>  r = sqrt(1 - s1**2 / HHI). This reproduces exactly the two
    quantities the market-doc stores (leader capture and HHI) and, unlike log-OLS, does not let
    the long tail pull the leader's share around. geom_rmse then reports how well this single
    geometric reproduces the *other* ranks, flagging shapes it describes poorly (flat oligopoly
    tops, leaders detached above their tail).
    """
    n = len(rows)
    if n < MIN_FIT_POINTS:
        raise SystemExit(f"need >= {MIN_FIT_POINTS} ranks to fit, have {n}")
    s1 = rows[0][1]
    empirical_hhi = sum(share * share for _, share in rows)
    if empirical_hhi <= s1 * s1:
        raise SystemExit("leader share already accounts for all HHI; need a declining tail")
    r = math.sqrt(1.0 - s1 * s1 / empirical_hhi)
    geom_rmse = math.sqrt(
        sum((share - geometric(rank, s1, r)) ** 2 for rank, share in rows) / n
    )
    return {
        "s1": s1,
        "r": r,
        "n": n,
        "rank_range": [rows[0][0], rows[-1][0]],
        "hhi": empirical_hhi,
        "effective_players": 1.0 / empirical_hhi,
        "modeled_mass": min(s1 / (1.0 - r), 1.0),
        "geom_rmse": geom_rmse,
    }


def load_moments(path: Path) -> dict[str, dict]:
    """Load normalized aggregate moments keyed by id.

    Expected share fields (cr4/cr8/cr20/cr50 and hhi) are decimals in [0, 1].
    Extra source columns are retained for reporting.
    """
    out: dict[str, dict] = {}
    with open(path, newline="") as fh:
        for line_no, row in enumerate(csv.DictReader(fh), start=2):
            key = (row.get("id") or "").strip()
            if not key:
                raise SystemExit(f"{path}: row {line_no} has no id")
            if key in out:
                raise SystemExit(f"{path}: duplicate id '{key}'")
            try:
                parsed = dict(row)
                for field in ("cr4", "cr8", "cr20", "cr50", "hhi"):
                    parsed[field] = float(row[field])
                for field in ("year", "firm_count", "revenue_usd_thousands"):
                    if row.get(field):
                        parsed[field] = int(row[field])
            except (KeyError, ValueError) as exc:
                raise SystemExit(f"{path}: invalid row {line_no}: {exc}") from exc
            out[key] = parsed
    return out


def _moment_objective(r: float, empirical_hhi: float, moments: dict[int, float]) -> float:
    s1 = math.sqrt(empirical_hhi * (1.0 - r * r))
    return sum(
        (concentration_ratio(rank, s1, r) - moments[rank]) ** 2
        for rank in MOMENT_TOP_RANKS
    )


def fit_geometric_moments(moment: dict) -> dict:
    """Fit (s1, r) from aggregate HHI and concentration ratios.

    HHI is matched exactly. The remaining degree of freedom is chosen to minimize error on CR4 and
    CR8. CR20 and CR50 are held out as diagnostics: fitting them would let the observed competitive
    fringe distort the top-of-market shape this model is meant to summarize.
    """
    empirical_hhi = float(moment["hhi"])
    ratios = {
        4: float(moment["cr4"]),
        8: float(moment["cr8"]),
        20: float(moment["cr20"]),
        50: float(moment["cr50"]),
    }
    if not 0.0 < empirical_hhi <= 1.0:
        raise ValueError(f"HHI {empirical_hhi} outside (0, 1]")
    previous = 0.0
    for rank in (*MOMENT_TOP_RANKS, *MOMENT_TAIL_RANKS):
        value = ratios[rank]
        if not previous <= value <= 1.0:
            raise ValueError(f"CR{rank}={value} is outside [{previous}, 1]")
        previous = value

    # Coarse-to-fine deterministic search avoids another numerical dependency. Conditional on r,
    # exact HHI identifies s1 = sqrt(HHI * (1-r^2)).
    best_r = 0.0001
    best_error = math.inf
    coarse_step = 0.001
    for i in range(1, 1000):
        r = i * coarse_step
        error = _moment_objective(r, empirical_hhi, ratios)
        if error < best_error:
            best_r, best_error = r, error
    lo, hi = max(0.000001, best_r - coarse_step), min(0.999999, best_r + coarse_step)
    for i in range(1001):
        r = lo + (hi - lo) * i / 1000
        error = _moment_objective(r, empirical_hhi, ratios)
        if error < best_error:
            best_r, best_error = r, error

    s1 = math.sqrt(empirical_hhi * (1.0 - best_r * best_r))
    predicted = {
        rank: concentration_ratio(rank, s1, best_r)
        for rank in (*MOMENT_TOP_RANKS, *MOMENT_TAIL_RANKS)
    }
    residuals = {rank: predicted[rank] - ratios[rank] for rank in predicted}
    top_rmse = math.sqrt(
        sum(residuals[rank] ** 2 for rank in MOMENT_TOP_RANKS) / len(MOMENT_TOP_RANKS)
    )
    tail_rmse = math.sqrt(
        sum(residuals[rank] ** 2 for rank in MOMENT_TAIL_RANKS) / len(MOMENT_TAIL_RANKS)
    )
    return {
        "s1": s1,
        "r": best_r,
        "hhi": empirical_hhi,
        "effective_players": 1.0 / empirical_hhi,
        "modeled_mass": min(s1 / (1.0 - best_r), 1.0),
        "top_cr_rmse": top_rmse,
        "tail_cr_rmse": tail_rmse,
        "observed_cr": {str(rank): ratios[rank] for rank in predicted},
        "predicted_cr": {str(rank): predicted[rank] for rank in predicted},
        "cr_residuals": {str(rank): residuals[rank] for rank in predicted},
    }


def fit_calibration_entry(
    entry: dict,
    data_dir: Path,
) -> dict:
    """Fit one calibration entry from its canonical ranked-share outcome."""
    path = data_dir / "shares" / f"{entry['id']}.csv"
    declared_synthetic = entry.get("outcome-quality") == SYNTHETIC_OUTCOME_QUALITY
    with open(path) as fh:
        marked_synthetic = fh.readline().strip() == SYNTHETIC_SHARE_MARKER
    if declared_synthetic != marked_synthetic:
        raise SystemExit(
            f"{entry['id']}: outcome-quality and share-file synthetic marker disagree"
        )
    rows, _ = load_shares(path)
    fit = fit_geometric(rows)
    fit["synthetic"] = declared_synthetic
    fit["shape_validation_eligible"] = not fit["synthetic"]
    return fit


def capture_table(s1: float, r: float, names: list[str], min_share: float) -> list[dict]:
    """Ranked capture rows: named players first, then unnamed ranks until share < min_share."""
    rows, rank = [], 1
    while True:
        share = geometric(rank, s1, r)
        name = names[rank - 1] if rank - 1 < len(names) else None
        if name is None and share < min_share:
            break
        rows.append({"rank": rank, "name": name, "share": share})
        rank += 1
        if rank > 100:
            break
    return rows


def load_index(data_dir: Path) -> dict[str, dict]:
    with open(data_dir / "calibration.yaml") as fh:
        doc = yaml.safe_load(fh)
    return {e["id"]: e for e in doc["calibration"]}


def print_fit(fit: dict, label: str = "fit") -> None:
    flag = "  POORLY GEOMETRIC" if fit["geom_rmse"] > GEOM_RMSE_WARN else ""
    print(
        f"{label}: s1={fit['s1']:.3f}  r={fit['r']:.3f}  HHI={fit['hhi']:.3f}  "
        f"N_eff={fit['effective_players']:.1f}  n={fit['n']} "
        f"[rank {fit['rank_range'][0]}-{fit['rank_range'][1]}]  "
        f"geom_rmse={fit['geom_rmse']:.4f}{flag}"
    )


def print_moment_fit(fit: dict, label: str = "fit") -> None:
    flags = []
    if fit["top_cr_rmse"] > MOMENT_TOP_RMSE_WARN:
        flags.append("POOR TOP FIT")
    if fit["tail_cr_rmse"] > MOMENT_TAIL_RMSE_WARN:
        flags.append("POOR TAIL FIT")
    suffix = f"  {' / '.join(flags)}" if flags else ""
    print(
        f"{label}: s1={fit['s1']:.3f}  r={fit['r']:.3f}  HHI={fit['hhi']:.3f}  "
        f"N_eff={fit['effective_players']:.1f}  top_cr_rmse={fit['top_cr_rmse']:.4f}  "
        f"tail_cr_rmse={fit['tail_cr_rmse']:.4f}{suffix}"
    )


def cmd_fit(args: argparse.Namespace) -> int:
    rows, warnings = load_shares(Path(args.shares))
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    fit = fit_geometric(rows)
    if args.json:
        print(json.dumps(fit, indent=2))
    else:
        print_fit(fit)
    return 0


def cmd_fit_moments(args: argparse.Namespace) -> int:
    moments = load_moments(Path(args.moments))
    if args.id not in moments:
        raise SystemExit(f"moment id '{args.id}' not found in {args.moments}")
    fit = fit_geometric_moments(moments[args.id])
    if args.json:
        print(json.dumps(fit, indent=2))
    else:
        print_moment_fit(fit)
    return 0


def _ols(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Simple linear regression; returns (intercept, slope)."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - slope * mx, slope


def _clip(v: float, lo: float, hi: float) -> float:
    return min(max(v, lo), hi)


def dominance_index(traits: dict[str, float]) -> float:
    """OR-like dominance index: any strong mechanism can support leader dominance."""
    return 1.0 - math.prod(1.0 - traits[k] for k in DOMINANCE_TRAITS)


def barrier_index(traits: dict[str, float]) -> float:
    return sum(traits[k] for k in BARRIER_TRAITS) / len(BARRIER_TRAITS)


def _ridge_metadata(model: RidgeModel) -> dict:
    return {
        "intercept": model.coefficients[0],
        "means": dict(zip(PRODUCTION_TRAITS, model.means)),
        "scales": dict(zip(PRODUCTION_TRAITS, model.scales)),
        "standardized_coefficients": dict(
            zip(PRODUCTION_TRAITS, model.coefficients[1:])
        ),
    }


def calibrate_models(index: dict[str, dict], data_dir: Path) -> dict:
    """Refit the frozen direct-ridge production models and fixed-specification LOO diagnostics."""
    xs, s1s, rs = [], [], []
    for entry in index.values():
        outcome = fit_calibration_entry(entry, data_dir)
        xs.append([entry["traits"][trait]["score"] for trait in PRODUCTION_TRAITS])
        s1s.append(outcome["s1"])
        rs.append(outcome["r"])
    n = len(xs)
    s1_model = fit_ridge(xs, s1s, PRODUCTION_RIDGE_ALPHA)
    r_model = fit_ridge(xs, rs, PRODUCTION_RIDGE_ALPHA)
    es1, er = [], []
    for i in range(n):
        training = [j for j in range(n) if j != i]
        fold_xs = [xs[j] for j in training]
        s1_fold = fit_ridge(
            fold_xs, [s1s[j] for j in training], PRODUCTION_RIDGE_ALPHA
        )
        r_fold = fit_ridge(
            fold_xs, [rs[j] for j in training], PRODUCTION_RIDGE_ALPHA
        )
        s1_prediction = _clip(s1_fold.predict(xs[i]), *S1_CLIP)
        r_prediction = _clip(r_fold.predict(xs[i]), *R_CLIP)
        es1.append((s1s[i] - s1_prediction) ** 2)
        er.append((rs[i] - r_prediction) ** 2)
    return {
        "type": PRODUCTION_MODEL,
        "n": n,
        "features": list(PRODUCTION_TRAITS),
        "alpha": PRODUCTION_RIDGE_ALPHA,
        "s1_model": s1_model,
        "r_model": r_model,
        "loo_s1": math.sqrt(sum(es1) / n),
        "loo_r": math.sqrt(sum(er) / n),
    }


def predict_parameters(models: dict, traits: dict[str, float]) -> tuple[float, float]:
    values = [traits[trait] for trait in PRODUCTION_TRAITS]
    s1 = _clip(models["s1_model"].predict(values), *S1_CLIP)
    r = _clip(models["r_model"].predict(values), *R_CLIP)
    return s1, r


def parse_traits(spec: str) -> dict[str, float]:
    """Parse 'ne=0.6,dsa=0.4,br=0.5,...' (ids or aliases) into {trait-id: score}."""
    out = {}
    for pair in spec.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise SystemExit(f"bad trait spec '{pair}' (expected key=value)")
        key, val = pair.split("=", 1)
        key = key.strip()
        key = TRAIT_ALIASES.get(key, key)
        try:
            score = float(val)
        except ValueError:
            raise SystemExit(f"bad score '{val}' for {key}")
        if not 0.0 <= score <= 1.0:
            raise SystemExit(f"score {score} for {key} outside [0, 1]")
        out[key] = score
    return out


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


def market_doc_traits(front_matter: dict) -> dict[str, float]:
    """Read and validate analyst-owned concentration trait inputs."""
    concentration = front_matter.get("concentration")
    inputs = concentration.get("inputs") if isinstance(concentration, dict) else None
    traits = inputs.get("traits") if isinstance(inputs, dict) else None
    if not isinstance(traits, dict):
        raise SystemExit(
            "market-doc has no 'concentration.inputs.traits' mapping; "
            "add all seven concentration traits and re-run"
        )

    scores: dict[str, float] = {}
    for trait in ALL_TRAITS:
        value = traits.get(trait)
        if not isinstance(value, dict):
            raise SystemExit(
                f"concentration.inputs.traits.{trait} must be a "
                "{score, confidence} mapping"
            )
        for field in ("score", "confidence"):
            try:
                number = float(value[field])
            except (KeyError, TypeError, ValueError) as exc:
                raise SystemExit(
                    f"concentration.inputs.traits.{trait}.{field} must be a number"
                ) from exc
            if not 0.0 <= number <= 1.0:
                raise SystemExit(
                    f"concentration.inputs.traits.{trait}.{field}={number} outside [0, 1]"
                )
            if field == "score":
                scores[trait] = number
    return scores


def market_doc_override(front_matter: dict) -> tuple[float, float, str] | None:
    """Return the optional analyst-owned (s1, r, reason) override."""
    concentration = front_matter.get("concentration")
    override = concentration.get("override") if isinstance(concentration, dict) else None
    if override is None:
        return None
    if not isinstance(override, dict):
        raise SystemExit("concentration.override must be a mapping or be omitted")
    try:
        s1 = float(override["s1"])
        r = float(override["r"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit("concentration.override requires numeric s1 and r") from exc
    reason = override.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise SystemExit("concentration.override requires a non-empty reason")
    validate_parameters(s1, r, "concentration.override")
    return s1, r, reason.strip()


def validate_parameters(s1: float, r: float, source: str) -> None:
    if not 0.0 < s1 <= 1.0:
        raise SystemExit(f"{source}.s1 must be in (0, 1]")
    if not 0.0 < r < 1.0:
        raise SystemExit(f"{source}.r must be in (0, 1)")


def concentration_doc_result(models: dict, front_matter: dict) -> dict:
    """Compute the model estimate and the override-resolved concentration outputs."""
    traits = market_doc_traits(front_matter)
    model_s1, model_r = predict_parameters(models, traits)
    override = market_doc_override(front_matter)
    if override is None:
        selected_s1, selected_r = model_s1, model_r
        selected_from = "model-estimate"
    else:
        selected_s1, selected_r, _ = override
        selected_from = "override"
    selected_hhi = hhi(selected_s1, selected_r)
    return {
        "model-estimate": {"s1": model_s1, "r": model_r},
        "selected": {"s1": selected_s1, "r": selected_r},
        "selected-from": selected_from,
        "hhi": selected_hhi,
        "effective_players": 1.0 / selected_hhi,
        "method": models["type"],
        "corpus-size": models["n"],
    }


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def upsert_concentration_child(block: str, key: str, value: str | dict[str, float]) -> str:
    """Surgically replace or append one script-owned child of `concentration`."""
    lines = block.splitlines()
    parent_i = next(
        (i for i, line in enumerate(lines) if re.fullmatch(r"concentration:\s*", line)),
        None,
    )
    if parent_i is None:
        raise SystemExit("cannot write back: market-doc has no top-level 'concentration:' block")
    parent_indent = _indent(lines[parent_i])

    parent_end = len(lines)
    child_indent = parent_indent + 2
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


def resolve_as_of(arg: str | None) -> str:
    if arg is None:
        return date.today().isoformat()
    try:
        return date.fromisoformat(arg).isoformat()
    except ValueError as exc:
        raise SystemExit(f"--as-of must be YYYY-MM-DD, got {arg!r}") from exc


def write_concentration_outputs(path: Path, result: dict, as_of: str) -> None:
    """Write only script-owned concentration outputs; preserve inputs, override, body and peers."""
    text = path.read_text(encoding="utf-8")
    match = FM_RE.match(text)
    if not match:
        raise SystemExit(f"cannot write back: {path} has no front-matter block")
    block = match.group(1)
    block = upsert_concentration_child(block, "model-estimate", result["model-estimate"])
    block = upsert_concentration_child(block, "hhi", str(round(result["hhi"], 6)))
    block = upsert_concentration_child(block, "method", result["method"])
    block = upsert_concentration_child(block, "date", as_of)
    path.write_text(f"---\n{block}\n---\n" + text[match.end():], encoding="utf-8")


def cmd_params(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    models = calibrate_models(load_index(data_dir), data_dir)
    if args.market_doc:
        path = resolve_market_doc(args.market_doc, Path(args.market_dir))
        if not path.exists():
            raise SystemExit(f"market-doc not found: {path}")
        _, front_matter = split_front_matter(path.read_text(encoding="utf-8"))
        result = concentration_doc_result(models, front_matter)
        selected = result["selected"]
        if selected["s1"] > 1.0 - selected["r"] + 1e-9:
            print(
                f"warning: selected s1={selected['s1']:.3f} > "
                f"1-r={1 - selected['r']:.3f}; modeled ranks sum past 1 "
                "(hard-oligopoly regime; enumerate only real players)",
                file=sys.stderr,
            )
        as_of = resolve_as_of(args.as_of)
        wrote = not args.dry_run
        if wrote:
            write_concentration_outputs(path, result, as_of)
        result = {
            **result,
            "date": as_of,
            "market-doc": str(path),
            "written": wrote,
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            estimate = result["model-estimate"]
            selected = result["selected"]
            print(
                f"{path.stem}: model s1={estimate['s1']:.3f}, r={estimate['r']:.3f}; "
                f"selected from {result['selected-from']} s1={selected['s1']:.3f}, "
                f"r={selected['r']:.3f}; HHI={result['hhi']:.3f}"
            )
            print(f"{'written to ' + str(path) if wrote else 'dry run — not written'}")
        return 0

    traits = parse_traits(args.traits)
    missing = [k for k in PRODUCTION_TRAITS if k not in traits]
    if missing:
        raise SystemExit(
            f"missing production trait(s): {', '.join(missing)} "
            f"(need all of {', '.join(PRODUCTION_TRAITS)})"
        )
    s1, r = predict_parameters(models, traits)
    names = [s.strip() for s in args.names.split(",")] if args.names else []
    table = capture_table(s1, r, names, args.min_share)
    model_output = {
        "type": models["type"],
        "n": models["n"],
        "features": models["features"],
        "alpha": models["alpha"],
        "s1": _ridge_metadata(models["s1_model"]),
        "r": _ridge_metadata(models["r_model"]),
        "fixed_model_loo_rmse": {
            "s1": models["loo_s1"],
            "r": models["loo_r"],
        },
    }
    result = {
        "s1": s1,
        "r": r,
        "hhi": hhi(s1, r),
        "effective_players": 1.0 / hhi(s1, r),
        "model": model_output,
        "capture": table,
    }
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(
        f"{models['type']} (fresh from n={models['n']} corpus; alpha={models['alpha']:.1f})"
    )
    print(f"s1 = {s1:.3f}   r = {r:.3f}")
    print(f"HHI = {result['hhi']:.3f}   N_eff = {result['effective_players']:.1f}")
    for target in ("s1", "r"):
        metadata = model_output[target]
        coefficients = ", ".join(
            f"{trait}={coefficient:+.3f}"
            for trait, coefficient in metadata["standardized_coefficients"].items()
        )
        print(f"{target} standardized coefficients: {coefficients}")
    print(
        f"fixed-model LOO-RMSE: s1 {models['loo_s1']:.3f}, r {models['loo_r']:.3f}  "
        "(conditional diagnostic; method-selection benchmark is in concentration_evaluate.py)"
    )
    if s1 > 1.0 - r + 1e-9:
        print(
            f"warning: s1={s1:.3f} > 1-r={1 - r:.3f}; modeled players sum past 1 "
            "(hard-oligopoly regime; enumerate only real players).",
            file=sys.stderr,
        )
    if table:
        print("capture:")
        for row in table:
            print(f"  rank {row['rank']:>2}  {row['share']:.4f}  {row['name'] or ''}")
    return 0


def cmd_project(args: argparse.Namespace) -> int:
    if not 0.0 < args.r < 1.0:
        raise SystemExit("--r must be in (0, 1)")
    if not 0.0 < args.s1 <= 1.0:
        raise SystemExit("--s1 must be in (0, 1]")
    if args.s1 > 1.0 - args.r + 1e-9:
        print(
            f"warning: s1={args.s1:.3f} > 1-r={1 - args.r:.3f}; modeled players sum past 1 "
            "(no room for a fringe). Lower s1 or r.",
            file=sys.stderr,
        )
    names = [s.strip() for s in args.names.split(",")] if args.names else []
    table = capture_table(args.s1, args.r, names, args.min_share)
    modeled = args.s1 / (1.0 - args.r)
    result = {
        "s1": args.s1,
        "r": args.r,
        "hhi": hhi(args.s1, args.r),
        "effective_players": 1.0 / hhi(args.s1, args.r),
        "modeled_mass": min(modeled, 1.0),
        "fringe": max(0.0, 1.0 - modeled),
        "capture": table,
    }
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(
        f"s1={args.s1:.3f}  r={args.r:.3f}  HHI={result['hhi']:.3f}  "
        f"N_eff={result['effective_players']:.1f}  fringe={result['fringe']:.3f}"
    )
    print("capture:")
    for row in table:
        print(f"  rank {row['rank']:>2}  {row['share']:.4f}  {row['name'] or ''}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    index = load_index(data_dir)
    print(
        f"{'id':<28} {'outcome':<10} {'trait-quality':<16} {'basis':<12} {'matured':>7} "
        f"{'s1':>6} {'r':>6} {'HHI':>6} categories"
    )
    for entry in index.values():
        fit = fit_calibration_entry(entry, data_dir)
        outcome = "synthetic" if fit["synthetic"] else "observed"
        basis = entry.get("share-basis", "-")
        basis = basis if len(basis) <= 12 else f"{basis[:11]}~"
        print(
            f"{entry['id']:<28} {outcome:<10} {entry['quality']:<16} {basis:<12} "
            f"{str(entry.get('matured-year', '-')):>7} "
            f"{fit['s1']:>6.3f} {fit['r']:>6.3f} {fit['hhi']:>6.3f} "
            f"{','.join(entry.get('categories', []))}"
        )
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fit", help="summarise a rank,share CSV as (s1, r)")
    f.add_argument("shares", help="CSV of rank,share rows (rank 1 = largest)")
    f.add_argument("--json", action="store_true")
    f.set_defaults(func=cmd_fit)

    fm = sub.add_parser("fit-moments", help="summarise one aggregate-moment row as (s1, r)")
    fm.add_argument("moments", help="CSV with normalized cr4/cr8/cr20/cr50/hhi fields")
    fm.add_argument("--id", required=True, help="row id to fit")
    fm.add_argument("--json", action="store_true")
    fm.set_defaults(func=cmd_fit_moments)

    pm = sub.add_parser("params", help="predict s1, r, HHI with the corpus-fitted production model")
    source = pm.add_mutually_exclusive_group(required=True)
    source.add_argument("--traits",
                        help="comma-separated trait scores, ids or aliases, e.g. "
                             "'ne=0.6,se=0.7,sc=0.3' "
                             "(network effects, scale economies and switching costs required)")
    source.add_argument("--market-doc",
                        help="market id or Markdown path; read concentration.inputs.traits and "
                             "write model-estimate, resolved HHI, method and date")
    pm.add_argument("--names", help="comma-separated player names, rank order, for a capture table")
    pm.add_argument("--min-share", type=float, default=0.01)
    pm.add_argument("--data-dir", default=str(DATA_DIR))
    pm.add_argument("--market-dir", default=str(DEFAULT_MARKET_DIR))
    pm.add_argument("--dry-run", action="store_true",
                    help="market-doc mode: calculate without writing")
    pm.add_argument("--as-of", help="market-doc mode: output date, YYYY-MM-DD (default today)")
    pm.add_argument("--json", action="store_true")
    pm.set_defaults(func=cmd_params)

    pr = sub.add_parser("project", help="HHI and capture table for explicit s1, r")
    pr.add_argument("--s1", type=float, required=True, help="leader share s1 in (0, 1]")
    pr.add_argument("--r", type=float, required=True, help="rank decay ratio r in (0, 1)")
    pr.add_argument("--names", help="comma-separated player names, rank order (largest first)")
    pr.add_argument("--min-share", type=float, default=0.01,
                    help="stop listing unnamed ranks below this share (default 0.01)")
    pr.add_argument("--json", action="store_true")
    pr.set_defaults(func=cmd_project)

    ls = sub.add_parser("list", help="summarise the calibration library")
    ls.add_argument("--data-dir", default=str(DATA_DIR))
    ls.set_defaults(func=cmd_list)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
