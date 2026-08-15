#!/usr/bin/env python3
"""Deterministic helpers for market-doc markdown files.

Commands:
  show MARKET_ID
  latest [N]
  companies
  frontmatter [MARKET_ID]
  validate [MARKET_ID]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_MARKET_DIR = WORKSPACE / "investment" / "market-docs"
CONCENTRATION_TRAITS = {
    "network-effects",
    "data-scale-advantage",
    "brand-reputation",
    "capital-intensity",
    "scale-economies",
    "regulatory-barriers",
    "switching-costs",
}
PENETRATION_MEASURES = {"stock", "new-sales-share", "spend-share"}
MOBILITY_METHOD = "share-gap-mobility-weighted-geometric-capture"
MAX_MOBILITY_RANKS = 5


def load_doc(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    try:
        fm = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}, text
    if not isinstance(fm, dict):
        return {}, text
    return fm, body


def iter_market_docs(market_dir: Path):
    for path in sorted(market_dir.glob("*.md")):
        if path.name.upper() == "README.MD" or path.name.startswith("_"):
            continue
        yield path


def normalize_market_id(market_id: str) -> str:
    return market_id.strip().lower().replace("_", "-").replace(" ", "-")


def doc_path(market_dir: Path, market_id: str) -> Path:
    return market_dir / f"{normalize_market_id(market_id)}.md"


def resolve_market_doc(market_dir: Path, market_id: str) -> Path | None:
    normalized = normalize_market_id(market_id)
    exact = doc_path(market_dir, normalized)
    if exact.exists():
        return exact

    paths = list(iter_market_docs(market_dir))
    prefix_matches = [p for p in paths if p.stem.startswith(normalized)]
    matches = prefix_matches or [p for p in paths if normalized in p.stem]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"Multiple market docs match '{market_id}':", file=sys.stderr)
        for path in matches:
            print(f"  {path.stem}", file=sys.stderr)
        return None

    print(f"No market doc found for '{market_id}'.", file=sys.stderr)
    return None


def nested(mapping: dict[str, Any], *keys: str) -> Any:
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


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def title_from_body(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
    return fallback


def market_id_for(path: Path) -> str:
    return path.stem


def market_name_for(path: Path, body: str) -> str:
    return title_from_body(body, path.stem.replace("-", " ").title())


def updated_date_for(path: Path) -> dt.date:
    return dt.datetime.fromtimestamp(path.stat().st_mtime).date()


def maturity_duration(fm: dict[str, Any]) -> int | None:
    return as_int(fm.get("maturity-duration"))


def maturity_year(fm: dict[str, Any]) -> int | None:
    base = as_int(fm.get("base-year"))
    duration = maturity_duration(fm)
    if base is not None and duration is not None:
        return base + duration
    return None


def currency_for(fm: dict[str, Any]) -> Any:
    return fm.get("currency")


def current_market_value(fm: dict[str, Any]) -> Any:
    return nested(fm, "size", "current-market-value")


def maturity_market_value(fm: dict[str, Any]) -> Any:
    return nested(fm, "size", "maturity-market-value")


def hhi_for(fm: dict[str, Any]) -> Any:
    return nested(fm, "concentration", "hhi")


def concentration_parameters(fm: dict[str, Any]) -> tuple[float, float, str] | None:
    """Resolve canonical s1/r: analyst override when present, else model estimate."""
    concentration = fm.get("concentration")
    if not isinstance(concentration, dict):
        return None
    source = "override" if "override" in concentration else "model-estimate"
    parameters = concentration.get(source)
    if not isinstance(parameters, dict):
        return None
    s1 = as_float(parameters.get("s1"))
    r = as_float(parameters.get("r"))
    if s1 is None or r is None:
        return None
    return s1, r, source


def penetration_parameters(fm: dict[str, Any]) -> tuple[float, float, float, str] | None:
    """Resolve canonical L/t0/k: analyst override when present, else model estimate."""
    penetration = fm.get("penetration")
    if not isinstance(penetration, dict):
        return None
    source = "override" if "override" in penetration else "model-estimate"
    parameters = penetration.get(source)
    if not isinstance(parameters, dict):
        return None
    L = as_float(parameters.get("L"))
    t0 = as_float(parameters.get("t0"))
    k = as_float(parameters.get("k"))
    if L is None or t0 is None or k is None:
        return None
    return L, t0, k, source


def players_for(fm: dict[str, Any]) -> list[Any]:
    """Resolve canonical player capture from per-player overrides, else mobility estimates."""
    players = fm.get("players")
    if not isinstance(players, dict):
        return []
    model = players.get("model-estimate")
    model = model if isinstance(model, list) else []
    overrides = players.get("override")
    overrides = overrides if isinstance(overrides, list) else []
    override_by_name = {
        entry.get("name"): entry
        for entry in overrides
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    out = []
    model_names = set()
    for estimate in model:
        if not isinstance(estimate, dict) or not isinstance(estimate.get("name"), str):
            continue
        name = estimate["name"]
        model_names.add(name)
        override = override_by_name.get(name)
        source = override or estimate
        capture = (
            source.get("capture")
            if override is not None
            else source.get("mobility-adjusted-capture")
        )
        out.append(
            {
                "name": name,
                "ticker": source.get("ticker") or estimate.get("ticker") or "",
                "capture": capture,
            }
        )
    for override in overrides:
        if (
            isinstance(override, dict)
            and isinstance(override.get("name"), str)
            and override["name"] not in model_names
        ):
            out.append(
                {
                    "name": override["name"],
                    "ticker": override.get("ticker") or "",
                    "capture": override.get("capture"),
                }
            )
    return out


def capture_for(entry: dict[str, Any]) -> float | None:
    return as_float(entry.get("capture"))


def player_name_for(entry: dict[str, Any]) -> str:
    return str(entry.get("name") or "")


def fmt_billions(value: Any, currency: Any) -> str:
    value_s = fmt(value)
    if not value_s:
        return ""
    return f"{fmt(currency)} {value_s}B" if currency else f"{value_s}B"


def frontmatter_summary(path: Path) -> dict[str, Any]:
    fm, _ = load_doc(path)
    out = dict(fm)
    out["file"] = str(path)
    return out


def cmd_show(args: argparse.Namespace) -> int:
    path = resolve_market_doc(args.market_dir, args.market_id)
    if path is None:
        return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_latest(args: argparse.Namespace) -> int:
    rows = []
    for path in iter_market_docs(args.market_dir):
        fm, body = load_doc(path)
        updated = updated_date_for(path)
        market_id = market_id_for(path)
        rows.append(
            (
                updated,
                market_id,
                maturity_year(fm),
                current_market_value(fm),
                maturity_market_value(fm),
                currency_for(fm),
                hhi_for(fm),
                market_name_for(path, body),
            )
        )
    rows.sort(key=lambda r: (-r[0].toordinal(), r[1]))
    rows = rows[: args.n]
    print(f"{'market-id':<32}  {'updated':<10}  {'projection':<10}  {'current-market-value':<20}  {'10yr-market-value':<17}  {'hhi':<7}  market")
    for updated, market_id, mat_year, cur_value, mat_value, currency, hhi, market in rows:
        print(
            f"{market_id:<32}  {updated.isoformat():<10}  {fmt(mat_year):<10}  "
            f"{fmt_billions(cur_value, currency):<20}  {fmt_billions(mat_value, currency):<17}  {fmt(hhi):<7}  {market}"
        )
    return 0


def cmd_companies(args: argparse.Namespace) -> int:
    rows = []
    for path in iter_market_docs(args.market_dir):
        fm, body = load_doc(path)
        players = players_for(fm)
        if not players:
            continue
        market_id = market_id_for(path)
        market = market_name_for(path, body)
        mat_value = maturity_market_value(fm)
        currency = currency_for(fm)
        mat_year = maturity_year(fm)
        for entry in players:
            if not isinstance(entry, dict):
                continue
            ticker = str(entry.get("ticker") or "")
            name = player_name_for(entry)
            rows.append(
                (
                    market_id,
                    ticker,
                    capture_for(entry),
                    name,
                    mat_year,
                    mat_value,
                    currency,
                    market,
                )
            )
    rows.sort(key=lambda r: (r[0], -(r[2] or -1), r[1]))
    print(f"{'market-id':<32}  {'ticker':<12}  {'projection':<10}  {'10yr-market-value':<17}  {'capture':<8}  {'player':<32}  market")
    for market_id, ticker, share, player, mat_year, mat_value, currency, market in rows:
        print(
            f"{market_id:<32}  {ticker:<12}  {fmt(mat_year):<10}  "
            f"{fmt_billions(mat_value, currency):<17}  {fmt(share):<8}  {player:<32}  {market}"
        )
    return 0


def cmd_frontmatter(args: argparse.Namespace) -> int:
    if args.market_id:
        path = resolve_market_doc(args.market_dir, args.market_id)
        if path is None:
            return 1
        paths = [path]
    else:
        paths = list(iter_market_docs(args.market_dir))
    data = [frontmatter_summary(p) for p in paths]
    print(json.dumps(data[0] if args.market_id and data else data, indent=2, sort_keys=True, default=str))
    return 0


def validate_players(fm: dict[str, Any], s1: float, r: float) -> list[str]:
    """Validate manual or mobility-backed canonical player capture."""
    errors: list[str] = []
    players = fm.get("players")
    if players is None:
        return errors
    if not isinstance(players, dict):
        return ["players must be a mapping"]
    if "capture" in players:
        errors.append("players.capture is obsolete; use model-estimate and/or override")

    overrides = players.get("override")
    parsed_overrides: list[dict[str, Any]] = []
    if overrides is not None:
        if not isinstance(overrides, list):
            errors.append("players.override must be a list")
        else:
            names = []
            for index, entry in enumerate(overrides, start=1):
                source = f"players.override[{index}]"
                if not isinstance(entry, dict):
                    errors.append(f"{source} must be a mapping")
                    continue
                name = entry.get("name")
                if not isinstance(name, str) or not name.strip():
                    errors.append(f"{source}.name must be non-empty")
                else:
                    names.append(name)
                ticker = entry.get("ticker")
                if ticker is not None and (
                    not isinstance(ticker, str) or not ticker.strip()
                ):
                    errors.append(f"{source}.ticker must be non-empty or omitted")
                capture = as_float(entry.get("capture"))
                if capture is None or not 0.0 <= capture <= 1.0:
                    errors.append(f"{source}.capture must be in [0, 1]")
                reason = entry.get("reason")
                if not isinstance(reason, str) or not reason.strip():
                    errors.append(f"{source}.reason must be non-empty")
                if isinstance(name, str) and name.strip() and capture is not None:
                    parsed_overrides.append({"name": name, "capture": capture})
            if len(set(names)) != len(names):
                errors.append("players.override names must be unique")

    inputs = players.get("inputs")
    estimates = players.get("model-estimate")
    model_mode = inputs is not None or estimates is not None
    parsed_estimates: list[dict[str, Any]] = []
    if model_mode:
        current = inputs.get("current") if isinstance(inputs, dict) else None
        if not isinstance(current, list) or not 2 <= len(current) <= MAX_MOBILITY_RANKS:
            errors.append(
                f"players.inputs.current must contain the current top 2..{MAX_MOBILITY_RANKS} players"
            )
            current = []
        current_names = []
        current_shares = []
        current_ranks = []
        for index, entry in enumerate(current, start=1):
            source = f"players.inputs.current[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{source} must be a mapping")
                continue
            rank = as_int(entry.get("rank"))
            name = entry.get("name")
            share = as_float(entry.get("share"))
            if rank is None:
                errors.append(f"{source}.rank must be an integer")
            else:
                current_ranks.append(rank)
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{source}.name must be non-empty")
            else:
                current_names.append(name)
            ticker = entry.get("ticker")
            if ticker is not None and (
                not isinstance(ticker, str) or not ticker.strip()
            ):
                errors.append(f"{source}.ticker must be non-empty or omitted")
            if share is None or not 0.0 < share <= 1.0:
                errors.append(f"{source}.share must be in (0, 1]")
            else:
                current_shares.append(share)
        if current_ranks and current_ranks != list(range(1, len(current) + 1)):
            errors.append("players.inputs.current ranks must be ordered and contiguous from 1")
        if len(set(current_names)) != len(current_names):
            errors.append("players.inputs.current names must be unique")
        if len(current_shares) == len(current):
            if any(left < right for left, right in zip(current_shares, current_shares[1:])):
                errors.append("players.inputs.current shares must be descending by rank")
            if sum(current_shares) > 1 + 1e-9:
                errors.append("players.inputs.current shares cannot sum above 1")

        if not isinstance(estimates, list) or len(estimates) != len(current):
            errors.append("players.model-estimate must contain one row per current player")
            estimates = []
        estimate_names = []
        estimate_ranks = []
        maturity_value = as_float(nested(fm, "size", "maturity-market-value"))
        if (
            maturity_value is None
            or not math.isfinite(maturity_value)
            or maturity_value < 0
        ):
            errors.append(
                "size.maturity-market-value must be a non-negative number for mobility revenue"
            )
        for index, entry in enumerate(estimates, start=1):
            source = f"players.model-estimate[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{source} must be a mapping")
                continue
            rank = as_int(entry.get("rank"))
            name = entry.get("name")
            hold = as_float(entry.get("hold-position-capture"))
            adjusted = as_float(entry.get("mobility-adjusted-capture"))
            revenue = as_float(entry.get("mobility-adjusted-revenue"))
            if rank is None:
                errors.append(f"{source}.rank must be an integer")
            else:
                estimate_ranks.append(rank)
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{source}.name must be non-empty")
            else:
                estimate_names.append(name)
            if hold is None or not 0.0 <= hold <= 1.0:
                errors.append(f"{source}.hold-position-capture must be in [0, 1]")
            elif rank is not None:
                expected_hold = s1 * r ** (rank - 1)
                if not math.isclose(hold, expected_hold, rel_tol=0.0, abs_tol=1e-6):
                    errors.append(
                        f"{source}.hold-position-capture={hold:g} does not match "
                        f"canonical concentration ({expected_hold:.6f})"
                    )
            if adjusted is None or not 0.0 <= adjusted <= 1.0:
                errors.append(f"{source}.mobility-adjusted-capture must be in [0, 1]")
            if revenue is None or not math.isfinite(revenue) or revenue < 0.0:
                errors.append(
                    f"{source}.mobility-adjusted-revenue must be non-negative"
                )
            elif adjusted is not None and maturity_value is not None and maturity_value >= 0:
                expected_revenue = adjusted * maturity_value
                if not math.isclose(
                    revenue,
                    expected_revenue,
                    rel_tol=0.0,
                    abs_tol=1e-6,
                ):
                    errors.append(
                        f"{source}.mobility-adjusted-revenue={revenue:g} does not match "
                        f"mobility-adjusted-capture × maturity-market-value "
                        f"({expected_revenue:.6f})"
                    )
            if isinstance(name, str) and name.strip() and adjusted is not None:
                parsed_estimates.append({"name": name, "capture": adjusted})
        if estimate_ranks and estimate_ranks != current_ranks:
            errors.append("players.model-estimate ranks must match players.inputs.current")
        if estimate_names and estimate_names != current_names:
            errors.append("players.model-estimate names must match players.inputs.current")
        gone = as_float(players.get("gone-probability"))
        if gone is None or not 0.0 <= gone <= 1.0:
            errors.append("players.gone-probability must be in [0, 1]")
        if players.get("method") != MOBILITY_METHOD:
            errors.append(f"players.method must be {MOBILITY_METHOD}")
        if not players.get("date"):
            errors.append("players.date is required")
        if s1 / (1 - r) > 1 + 1e-9:
            errors.append("mobility requires canonical concentration modeled mass <= 1")

    if not model_mode and overrides is None:
        errors.append("players requires model-estimate and/or override")

    canonical = {entry["name"]: entry["capture"] for entry in parsed_estimates}
    canonical.update({entry["name"]: entry["capture"] for entry in parsed_overrides})
    if sum(canonical.values()) > 1 + 1e-9:
        errors.append("canonical player captures cannot sum above 1")
    return errors


def validate_front_matter(fm: dict[str, Any], path: Path) -> list[str]:
    """Validate parsed market-doc state, including prospective in-memory outputs."""
    errors: list[str] = []
    if not fm:
        return ["missing or invalid YAML front matter"]
    if maturity_duration(fm) != 10:
        errors.append("maturity-duration must be 10")

    concentration = fm.get("concentration")
    parameters = concentration_parameters(fm)
    if not isinstance(concentration, dict):
        errors.append("missing concentration mapping")
        return errors
    if parameters is None:
        errors.append("concentration requires override or model-estimate with numeric s1 and r")
        return errors

    s1, r, source = parameters
    if not 0.0 < s1 <= 1.0:
        errors.append(f"concentration.{source}.s1 must be in (0, 1]")
    if not 0.0 < r < 1.0:
        errors.append(f"concentration.{source}.r must be in (0, 1)")
    if source == "override":
        reason = nested(concentration, "override", "reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("concentration.override requires a non-empty reason")

    if concentration.get("method") == "selected-direct-ridge":
        traits = nested(concentration, "inputs", "traits")
        if not isinstance(traits, dict):
            errors.append("selected-direct-ridge requires concentration.inputs.traits")
        else:
            missing = sorted(CONCENTRATION_TRAITS - set(traits))
            if missing:
                errors.append(f"concentration.inputs.traits missing: {', '.join(missing)}")
            for trait in sorted(CONCENTRATION_TRAITS & set(traits)):
                value = traits[trait]
                if not isinstance(value, dict):
                    errors.append(f"concentration.inputs.traits.{trait} must be a mapping")
                    continue
                for field in ("score", "confidence"):
                    number = as_float(value.get(field))
                    if number is None or not 0.0 <= number <= 1.0:
                        errors.append(
                            f"concentration.inputs.traits.{trait}.{field} must be in [0, 1]"
                        )

    stored_hhi = as_float(concentration.get("hhi"))
    if stored_hhi is None:
        errors.append("concentration.hhi must be numeric")
    elif 0.0 < r < 1.0:
        derived_hhi = s1 * s1 / (1.0 - r * r)
        if not math.isclose(stored_hhi, derived_hhi, rel_tol=0.0, abs_tol=1e-6):
            errors.append(
                f"concentration.hhi={stored_hhi:g} does not match "
                f"{source} parameters ({derived_hhi:.6f})"
            )
    if not concentration.get("method"):
        errors.append("concentration.method is required")
    if not concentration.get("date"):
        errors.append("concentration.date is required")

    penetration = fm.get("penetration")
    if penetration is None:
        errors.extend(validate_players(fm, s1, r))
        return errors
    if not isinstance(penetration, dict):
        errors.append("penetration must be a mapping")
        errors.extend(validate_players(fm, s1, r))
        return errors

    penetration_params = penetration_parameters(fm)
    if penetration_params is None:
        errors.append(
            "penetration requires override or model-estimate with numeric L, t0 and k"
        )
        errors.extend(validate_players(fm, s1, r))
        return errors
    L, t0, k, penetration_source = penetration_params
    if not 0.0 < L <= 1.0:
        errors.append(f"penetration.{penetration_source}.L must be in (0, 1]")
    if not math.isfinite(t0):
        errors.append(f"penetration.{penetration_source}.t0 must be finite")
    if not math.isfinite(k) or k <= 0.0:
        errors.append(f"penetration.{penetration_source}.k must be greater than zero")
    if penetration_source == "override":
        reason = nested(penetration, "override", "reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("penetration.override requires a non-empty reason")

    if penetration.get("method") == "logistic-blend":
        model_estimate = penetration.get("model-estimate")
        if not isinstance(model_estimate, dict) or any(
            as_float(model_estimate.get(field)) is None for field in ("L", "t0", "k")
        ):
            errors.append("logistic-blend requires penetration.model-estimate")
        inputs = penetration.get("inputs")
        if not isinstance(inputs, dict):
            errors.append("logistic-blend requires penetration.inputs")
        else:
            target_series = inputs.get("target-series")
            if not isinstance(target_series, str) or not target_series.strip():
                errors.append("penetration.inputs.target-series must be a non-empty path")
            else:
                target_path = Path(target_series)
                if not target_path.is_absolute():
                    target_path = path.parent / target_path
                if not target_path.exists():
                    errors.append(
                        f"penetration.inputs.target-series not found: {target_series}"
                    )
            if inputs.get("measure") not in PENETRATION_MEASURES:
                errors.append(
                    "penetration.inputs.measure must be stock, new-sales-share or spend-share"
                )
            ceiling = as_float(inputs.get("ceiling"))
            if ceiling is None or not 0.0 < ceiling <= 1.0:
                errors.append("penetration.inputs.ceiling must be in (0, 1]")
            analogs = inputs.get("analogs")
            if (
                not isinstance(analogs, list)
                or len(analogs) < 2
                or any(not isinstance(analog, str) or not analog.strip() for analog in analogs)
            ):
                errors.append(
                    "penetration.inputs.analogs must contain at least two analog ids"
                )
            elif len(set(analogs)) != len(analogs):
                errors.append("penetration.inputs.analogs must not contain duplicates")
            w_fit = inputs.get("w-fit")
            if w_fit is not None:
                weight = as_float(w_fit)
                if weight is None or not 0.0 <= weight <= 1.0:
                    errors.append("penetration.inputs.w-fit must be in [0, 1]")
            as_of_year = inputs.get("as-of-year")
            if as_of_year is not None and as_int(as_of_year) is None:
                errors.append("penetration.inputs.as-of-year must be an integer")
    if not penetration.get("method"):
        errors.append("penetration.method is required")
    if not penetration.get("date"):
        errors.append("penetration.date is required")
    errors.extend(validate_players(fm, s1, r))
    return errors


def validate_market_doc(path: Path) -> list[str]:
    """Validate a market doc from disk."""
    fm, _ = load_doc(path)
    return validate_front_matter(fm, path)


def cmd_validate(args: argparse.Namespace) -> int:
    if args.market_id:
        path = resolve_market_doc(args.market_dir, args.market_id)
        if path is None:
            return 1
        paths = [path]
    else:
        paths = list(iter_market_docs(args.market_dir))
    error_count = 0
    for path in paths:
        errors = validate_market_doc(path)
        error_count += len(errors)
        for error in errors:
            print(f"ERROR {path.stem}: {error}")
    print(f"{len(paths)} market doc(s) checked: {error_count} error(s)")
    return 1 if error_count else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Maintain, validate and list market-doc views.")
    p.add_argument("--market-dir", type=Path, default=DEFAULT_MARKET_DIR)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("show", help="Show one market doc; accepts exact or unique partial market ids.")
    s.add_argument("market_id")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("latest", help="List recently updated market docs with market-value and concentration assumptions.")
    s.add_argument("n", nargs="?", type=int, default=10, help="Limit to the latest N docs (default: 10).")
    s.set_defaults(func=cmd_latest)

    s = sub.add_parser("companies", help="Export player market-value capture assumptions across market docs.")
    s.set_defaults(func=cmd_companies)

    s = sub.add_parser("frontmatter", help="Print parsed market-doc front matter as JSON.")
    s.add_argument("market_id", nargs="?")
    s.set_defaults(func=cmd_frontmatter)

    s = sub.add_parser("validate", help="Validate market-doc front matter and derived outputs.")
    s.add_argument("market_id", nargs="?")
    s.set_defaults(func=cmd_validate)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
