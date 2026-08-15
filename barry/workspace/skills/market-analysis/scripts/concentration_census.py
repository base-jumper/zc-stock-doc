#!/usr/bin/env python3
"""Extract and normalize concentration data from the U.S. Economic Census.

Input is the official EC2200SIZECONCEN .zip or pipe-delimited .dat file. The extract command
normalizes Census percentages and HHI points. The synthesize command converts a normalized
moment file into canonical synthetic rank-share outcomes for the calibration corpus.
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO

from concentration_fit import (
    SYNTHETIC_SHARE_MARKER,
    fit_geometric,
    fit_geometric_moments,
    geometric,
    load_moments,
)

CENSUS_SOURCE_URL = (
    "https://www2.census.gov/programs-surveys/economic-census/data/2022/"
    "sector00/EC2200SIZECONCEN.zip"
)
SYNTHETIC_HHI_TAIL_TOLERANCE = 1e-10
SYNTHETIC_ROUND_TRIP_R_TOLERANCE = 2e-4
REQUIRED_CODES = ("001", "604", "608", "620", "650")
OUTPUT_FIELDS = (
    "id",
    "naics",
    "name",
    "region",
    "year",
    "share_basis",
    "firm_count",
    "revenue_usd_thousands",
    "cr4",
    "cr8",
    "cr20",
    "cr50",
    "hhi",
    "source_url",
)


@contextmanager
def _open_census(path: Path) -> Iterator[TextIO]:
    if path.suffix.lower() != ".zip":
        with open(path, encoding="utf-8", newline="") as fh:
            yield fh
        return
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if name.lower().endswith(".dat")]
        if len(names) != 1:
            raise SystemExit(f"{path}: expected one .dat member, found {len(names)}")
        with archive.open(names[0]) as raw:
            with io.TextIOWrapper(raw, encoding="utf-8", newline="") as fh:
                yield fh


def load_census_observations(path: Path) -> dict[str, dict]:
    """Return complete six-digit, all-establishment observations keyed by NAICS."""
    grouped: dict[str, dict[str, dict]] = {}
    with _open_census(path) as fh:
        for row in csv.DictReader(fh, delimiter="|"):
            if row["INDLEVEL"] != "6" or row["TYPOP"] != "00":
                continue
            grouped.setdefault(row["NAICS2022"], {})[row["CONCENFI"]] = row

    observations: dict[str, dict] = {}
    for naics, rows in grouped.items():
        if any(code not in rows for code in REQUIRED_CODES):
            continue
        all_firms, cr4, cr8, cr20, cr50 = (rows[code] for code in REQUIRED_CODES)
        values = [cr4["VAL_PCT"], cr8["VAL_PCT"], cr20["VAL_PCT"], cr50["VAL_PCT"]]
        if any(value in ("", "0") for value in values) or cr50["HHI"] in ("", "0"):
            continue
        observation = {
            "id": f"us-naics-{naics}",
            "naics": naics,
            "name": all_firms["NAICS2022_LABEL"],
            "region": "US",
            "year": int(all_firms["YEAR"]),
            "share_basis": "sales-value-shipments-or-revenue",
            "firm_count": int(all_firms["FIRM"]),
            "revenue_usd_thousands": int(all_firms["RCPTOT"]),
            "cr4": float(cr4["VAL_PCT"]) / 100.0,
            "cr8": float(cr8["VAL_PCT"]) / 100.0,
            "cr20": float(cr20["VAL_PCT"]) / 100.0,
            "cr50": float(cr50["VAL_PCT"]) / 100.0,
            "hhi": float(cr50["HHI"]) / 10000.0,
            "source_url": CENSUS_SOURCE_URL,
        }
        try:
            fit_geometric_moments(observation)
        except ValueError:
            continue
        observations[naics] = observation
    return observations


def _parse_codes(args: argparse.Namespace) -> list[str]:
    codes: list[str] = []
    if args.codes:
        codes.extend(code.strip() for code in args.codes.split(",") if code.strip())
    if args.codes_file:
        with open(args.codes_file) as fh:
            codes.extend(
                line.strip()
                for line in fh
                if line.strip() and not line.lstrip().startswith("#")
            )
    if not codes:
        raise SystemExit("provide --codes or --codes-file")
    return list(dict.fromkeys(codes))


def cmd_list(args: argparse.Namespace) -> int:
    observations = load_census_observations(Path(args.source))
    fitted = []
    for observation in observations.values():
        fit = fit_geometric_moments(observation)
        if observation["firm_count"] < args.min_firms:
            continue
        if fit["top_cr_rmse"] > args.max_top_rmse:
            continue
        if fit["tail_cr_rmse"] > args.max_tail_rmse:
            continue
        fitted.append((observation, fit))
    sort_key = {
        "hhi": lambda item: item[0]["hhi"],
        "naics": lambda item: item[0]["naics"],
        "fit": lambda item: -(item[1]["top_cr_rmse"] + item[1]["tail_cr_rmse"]),
    }[args.sort]
    fitted.sort(key=sort_key, reverse=args.sort != "naics")
    print(
        f"{'NAICS':<6} {'HHI':>6} {'s1':>6} {'r':>6} {'top':>7} {'tail':>7} "
        f"{'firms':>7}  industry"
    )
    for observation, fit in fitted[: args.limit]:
        print(
            f"{observation['naics']:<6} {observation['hhi']:>6.3f} "
            f"{fit['s1']:>6.3f} {fit['r']:>6.3f} "
            f"{fit['top_cr_rmse']:>7.4f} {fit['tail_cr_rmse']:>7.4f} "
            f"{observation['firm_count']:>7}  {observation['name']}"
        )
    print(f"shown {min(len(fitted), args.limit)} of {len(fitted)} passing observations")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    observations = load_census_observations(Path(args.source))
    codes = _parse_codes(args)
    missing = [code for code in codes if code not in observations]
    if missing:
        raise SystemExit(f"no complete Census observation for: {', '.join(missing)}")
    output = open(args.output, "w", newline="") if args.output else sys.stdout
    try:
        writer = csv.DictWriter(output, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for code in codes:
            row = dict(observations[code])
            for field in ("cr4", "cr8", "cr20", "cr50", "hhi"):
                row[field] = f"{row[field]:.6f}".rstrip("0").rstrip(".")
            writer.writerow(row)
    finally:
        if output is not sys.stdout:
            output.close()
    return 0


def synthetic_share_rows(moment: dict) -> tuple[list[tuple[int, float]], dict]:
    """Materialize a finite geometric sequence that preserves the moment-estimated parameters.

    The sequence ends once omitted geometric-tail HHI is negligible. In the hard-oligopoly regime,
    where the infinite geometric mass exceeds one, it instead stops before cumulative share would
    exceed one. This can truncate mass without materially truncating HHI because tail shares enter
    HHI squared.
    """
    moment_fit = fit_geometric_moments(moment)
    s1, r = moment_fit["s1"], moment_fit["r"]
    firm_count = int(moment.get("firm_count") or 10000)
    rows: list[tuple[int, float]] = []
    cumulative = 0.0
    for rank in range(1, firm_count + 1):
        share = geometric(rank, s1, r)
        if cumulative + share > 1.0 + 1e-12:
            break
        rows.append((rank, share))
        cumulative += share
        if r ** (2 * rank) <= SYNTHETIC_HHI_TAIL_TOLERANCE:
            break
    if len(rows) < 2:
        raise ValueError(f"{moment.get('id', 'moment')}: cannot materialize at least two ranks")

    round_trip = fit_geometric(rows)
    if abs(round_trip["r"] - r) > SYNTHETIC_ROUND_TRIP_R_TOLERANCE:
        raise ValueError(
            f"{moment.get('id', 'moment')}: finite shares reproduce r={round_trip['r']:.8f}, "
            f"outside tolerance of moment fit r={r:.8f}"
        )
    diagnostics = {
        "moment_fit": moment_fit,
        "round_trip": round_trip,
        "cumulative_share": cumulative,
        "omitted_hhi_fraction": r ** (2 * len(rows)),
    }
    return rows, diagnostics


def _write_synthetic_shares(path: Path, moment: dict, rows: list[tuple[int, float]]) -> None:
    if path.exists():
        with open(path) as fh:
            if fh.readline().strip() != SYNTHETIC_SHARE_MARKER:
                raise SystemExit(f"{path}: refusing to overwrite a non-synthetic share file")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        fh.write(f"{SYNTHETIC_SHARE_MARKER}\n")
        fh.write(f"# Derived from aggregate moments for {moment['id']}; not observed firm shares.\n")
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(("rank", "share"))
        for rank, share in rows:
            writer.writerow((rank, f"{share:.12f}".rstrip("0").rstrip(".")))


def cmd_synthesize(args: argparse.Namespace) -> int:
    moments = load_moments(Path(args.moments))
    selected = args.ids.split(",") if args.ids else list(moments)
    selected = [item.strip() for item in selected if item.strip()]
    missing = [item for item in selected if item not in moments]
    if missing:
        raise SystemExit(f"moment id(s) not found: {', '.join(missing)}")

    output_dir = Path(args.output_dir)
    for key in selected:
        moment = moments[key]
        rows, diagnostics = synthetic_share_rows(moment)
        path = output_dir / f"{key}.csv"
        _write_synthetic_shares(path, moment, rows)
        moment_r = diagnostics["moment_fit"]["r"]
        round_trip_r = diagnostics["round_trip"]["r"]
        print(
            f"{key}: {len(rows)} ranks -> {path}  "
            f"r={moment_r:.6f} round-trip={round_trip_r:.6f}  "
            f"omitted-HHI={diagnostics['omitted_hhi_fraction']:.2e}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    ls = sub.add_parser("list", help="screen complete six-digit Census observations")
    ls.add_argument("source", help="EC2200SIZECONCEN .zip or .dat")
    ls.add_argument("--min-firms", type=int, default=10)
    ls.add_argument("--max-top-rmse", type=float, default=0.03)
    ls.add_argument("--max-tail-rmse", type=float, default=0.08)
    ls.add_argument("--sort", choices=("hhi", "naics", "fit"), default="hhi")
    ls.add_argument("--limit", type=int, default=50)
    ls.set_defaults(func=cmd_list)

    ex = sub.add_parser("extract", help="normalize selected NAICS observations to CSV")
    ex.add_argument("source", help="EC2200SIZECONCEN .zip or .dat")
    ex.add_argument("--codes", help="comma-separated six-digit NAICS codes")
    ex.add_argument("--codes-file", help="one six-digit NAICS code per line")
    ex.add_argument("--output", help="output CSV (default stdout)")
    ex.set_defaults(func=cmd_extract)

    sy = sub.add_parser(
        "synthesize",
        help="generate canonical synthetic rank-share CSVs from normalized moments",
    )
    sy.add_argument("moments", help="normalized aggregate-moment CSV")
    sy.add_argument("--output-dir", required=True, help="destination shares directory")
    sy.add_argument("--ids", help="optional comma-separated row ids (default all)")
    sy.set_defaults(func=cmd_synthesize)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
