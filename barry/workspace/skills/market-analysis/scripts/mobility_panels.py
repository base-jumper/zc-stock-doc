#!/usr/bin/env python3
"""Validate and summarise the rank-mobility panel corpus.

Usage:
    mobility_panels.py validate [--json]
    mobility_panels.py summary  [--json]

The corpus contract lives in ../references/mobility/calibration.md. `validate` enforces it and exits
non-zero on errors (warnings are advisory). `summary` reports per-panel coverage and the count of
usable non-overlapping >=10-year windows.
"""

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "references" / "mobility" / "data"
WINDOW_YEARS = 10
SHARE_SUM_TOL = 1.005
FATES = {"fringe", "exited", "defunct", "acquired"}
PENETRATION_PROVENANCE = {"fitted", "estimated"}
QUALITIES = {"seed-approximate", "verified"}
REQUIRED_FIELDS = ("id", "name", "market", "region", "basis", "coverage", "tracker", "quality",
                   "players", "sources")
CSV_COLUMNS = ["year", "rank", "player", "share"]


def load_index(data_dir):
    with open(data_dir / "panels.yaml") as f:
        doc = yaml.safe_load(f) or {}
    return doc.get("panels") or []


def load_panel_csv(path):
    """Return rows as (year, rank, player, share-or-None)."""
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != CSV_COLUMNS:
            raise ValueError(f"columns must be {','.join(CSV_COLUMNS)}, got {reader.fieldnames}")
        for lineno, row in enumerate(reader, start=2):
            try:
                year, rank = int(row["year"]), int(row["rank"])
            except (TypeError, ValueError):
                raise ValueError(f"line {lineno}: year and rank must be integers")
            player = (row["player"] or "").strip()
            if not player:
                raise ValueError(f"line {lineno}: empty player")
            raw = (row["share"] or "").strip()
            try:
                share = float(raw) if raw else None
            except ValueError:
                raise ValueError(f"line {lineno}: bad share {raw!r}")
            rows.append((year, rank, player, share))
    if not rows:
        raise ValueError("no data rows")
    return rows


def curve_position(logistic, year):
    """F(t) = 1 / (1 + exp(-k (t - t0))) with L normalized to 1."""
    return 1.0 / (1.0 + math.exp(-logistic["k"] * (year - logistic["t0"])))


def derive_windows(years):
    """Greedy non-overlapping (start, end) year pairs >= WINDOW_YEARS apart."""
    years = sorted(years)
    windows, i = [], 0
    while i < len(years):
        j = next((k for k in range(i + 1, len(years)) if years[k] - years[i] >= WINDOW_YEARS), None)
        if j is None:
            break
        windows.append((years[i], years[j]))
        i = j + 1
    return windows


def count_windows(years):
    return len(derive_windows(years))


def validate_entry(entry, data_dir):
    errors, warnings = [], []
    pid = str(entry.get("id") or "<missing-id>")

    for field in REQUIRED_FIELDS:
        if not entry.get(field):
            errors.append(f"{pid}: missing field '{field}'")
    if entry.get("quality") and entry["quality"] not in QUALITIES:
        errors.append(f"{pid}: quality must be one of {sorted(QUALITIES)}")
    coverage = entry.get("coverage")
    if not isinstance(coverage, int) or coverage < 2:
        errors.append(f"{pid}: coverage must be an integer >= 2")
        coverage = None

    players = entry.get("players") or {}
    for name, facts in players.items():
        facts = facts or {}
        if not isinstance(facts.get("founded"), int):
            errors.append(f"{pid}: player '{name}' needs an integer 'founded'")
        fate = facts.get("fate")
        if fate is None:
            if "fate-year" in facts or "acquirer" in facts:
                warnings.append(f"{pid}: player '{name}' has fate-year/acquirer without 'fate'")
        else:
            if fate not in FATES:
                errors.append(f"{pid}: player '{name}' fate must be one of {sorted(FATES)}")
            if not isinstance(facts.get("fate-year"), int):
                errors.append(f"{pid}: player '{name}' fate requires an integer 'fate-year'")
            if fate == "acquired" and not facts.get("acquirer"):
                errors.append(f"{pid}: player '{name}' fate 'acquired' requires 'acquirer'")

    csv_path = data_dir / "panels" / f"{pid}.csv"
    if not csv_path.exists():
        errors.append(f"{pid}: missing panels/{pid}.csv")
        return errors, warnings, None
    try:
        rows = load_panel_csv(csv_path)
    except ValueError as exc:
        errors.append(f"{pid}: {exc}")
        return errors, warnings, None

    by_year = {}
    for year, rank, player, share in rows:
        by_year.setdefault(year, []).append((rank, player, share))

    for year in sorted(by_year):
        year_rows = sorted(by_year[year])
        ranks = [r for r, _, _ in year_rows]
        if ranks != list(range(1, len(ranks) + 1)):
            errors.append(f"{pid}: {year}: ranks must be unique and contiguous from 1, got {ranks}")
        if coverage is not None:
            if len(ranks) > coverage:
                errors.append(f"{pid}: {year}: {len(ranks)} ranks exceeds coverage {coverage}")
            elif len(ranks) < coverage:
                warnings.append(f"{pid}: {year}: only {len(ranks)} of coverage {coverage} ranks present")
        total, prev_share = 0.0, None
        for rank, player, share in year_rows:
            if player not in players:
                errors.append(f"{pid}: {year}: player '{player}' not in the panels.yaml players map")
            if share is not None:
                if not 0.0 < share <= 1.0:
                    errors.append(f"{pid}: {year}: share {share} for '{player}' outside (0, 1]")
                if prev_share is not None and share > prev_share + 1e-9:
                    warnings.append(f"{pid}: {year}: shares not non-increasing at rank {rank}")
                total += share
                prev_share = share
        if total > SHARE_SUM_TOL:
            errors.append(f"{pid}: {year}: shares sum to {total:.3f} > 1")

    penetration = entry.get("penetration")
    logistic = None
    if penetration is not None:
        logistic = (penetration or {}).get("logistic") or {}
        if not isinstance(logistic.get("t0"), (int, float)):
            errors.append(f"{pid}: penetration.logistic.t0 must be a number (inflection year)")
            logistic = None
        elif not isinstance(logistic.get("k"), (int, float)) or logistic["k"] <= 0:
            errors.append(f"{pid}: penetration.logistic.k must be a positive number")
            logistic = None
        if penetration.get("provenance") not in PENETRATION_PROVENANCE:
            errors.append(f"{pid}: penetration.provenance must be one of {sorted(PENETRATION_PROVENANCE)}")

    seen = {player for _, _, player, _ in rows}
    for name in players:
        if name not in seen:
            warnings.append(f"{pid}: player '{name}' listed in panels.yaml but never appears in the CSV")

    years = sorted(by_year)
    span = years[-1] - years[0]
    if span < WINDOW_YEARS:
        warnings.append(f"{pid}: span {years[0]}-{years[-1]} is under {WINDOW_YEARS} years — no usable window yet")
    info = {
        "id": pid,
        "quality": entry.get("quality"),
        "years": years,
        "span": span,
        "windows": count_windows(years),
        "players": len(seen),
        "rows": len(rows),
        "rows_with_share": sum(1 for _, _, _, s in rows if s is not None),
    }
    if logistic:
        info["curve-position"] = {y: round(curve_position(logistic, y), 3) for y in (years[0], years[-1])}
    return errors, warnings, info


def validate_corpus(data_dir):
    try:
        index = load_index(data_dir)
    except (OSError, yaml.YAMLError) as exc:
        return [f"panels.yaml: {exc}"], [], []
    errors, warnings, infos = [], [], []
    ids = [str(e.get("id")) for e in index]
    for pid in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate id '{pid}' in panels.yaml")
    for entry in index:
        e, w, info = validate_entry(entry, data_dir)
        errors += e
        warnings += w
        if info:
            infos.append(info)
    panels_dir = data_dir / "panels"
    if panels_dir.is_dir():
        for path in sorted(panels_dir.glob("*.csv")):
            if path.stem not in ids:
                errors.append(f"{path.name}: CSV has no panels.yaml entry")
    return errors, warnings, infos


def cmd_validate(args):
    errors, warnings, infos = validate_corpus(DATA_DIR)
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "panels": infos}, indent=2))
    else:
        for msg in errors:
            print(f"ERROR   {msg}")
        for msg in warnings:
            print(f"WARNING {msg}")
        print(f"{len(infos)} panel(s) checked: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def cmd_summary(args):
    errors, warnings, infos = validate_corpus(DATA_DIR)
    totals = {
        "panels": len(infos),
        "windows": sum(i["windows"] for i in infos),
        "verified": sum(1 for i in infos if i["quality"] == "verified"),
        "errors": len(errors),
    }
    if args.json:
        print(json.dumps({"panels": infos, "totals": totals}, indent=2))
        return 1 if errors else 0
    fmt = "{:<36} {:>9} {:>4} {:>4} {:>7} {:>7}  {}"
    print(fmt.format("panel", "years", "span", "win", "players", "shares", "quality"))
    for i in infos:
        years = f"{i['years'][0]}-{i['years'][-1]}" if len(i["years"]) > 1 else str(i["years"][0])
        print(fmt.format(i["id"], years, i["span"], i["windows"], i["players"],
                         f"{i['rows_with_share']}/{i['rows']}", i["quality"]))
    print(f"\n{totals['panels']} panel(s), {totals['windows']} usable window(s), "
          f"{totals['verified']} verified; {totals['errors']} validation error(s)")
    return 1 if errors else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate/summarise the rank-mobility panel corpus")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "summary"):
        p = sub.add_parser(name)
        p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return {"validate": cmd_validate, "summary": cmd_summary}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
