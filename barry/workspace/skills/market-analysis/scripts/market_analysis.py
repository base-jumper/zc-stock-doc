#!/usr/bin/env python3
"""Refresh configured market-doc calculations in dependency order.

Usage:
    market_analysis.py refresh MARKET_ID [--dry-run] [--as-of YYYY-MM-DD] [--json]

The command calculates every configured deterministic sub-skill in memory, validates the
prospective combined state, then writes only after the whole refresh succeeds. Size remains an
analyst-owned research output.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import stat
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = SCRIPT_DIR.parent.parent
MARKET_DOC_SCRIPT_DIR = SKILLS_DIR / "market-doc" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(MARKET_DOC_SCRIPT_DIR))

import concentration_fit as concentration  # noqa: E402
import market_doc  # noqa: E402
import mobility_fit as mobility  # noqa: E402
import penetration_fit as penetration  # noqa: E402

WORKSPACE = SKILLS_DIR.parent
DEFAULT_MARKET_DIR = WORKSPACE / "investment" / "market-docs"


def resolve_as_of(value: str | None) -> str:
    if value is None:
        return date.today().isoformat()
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise SystemExit(f"--as-of must be YYYY-MM-DD, got {value!r}") from exc


def resolve_market_doc(value: str, market_dir: Path) -> Path:
    path = Path(value)
    if path.suffix == ".md" or "/" in value:
        return path
    market_id = value.strip().lower().replace("_", "-").replace(" ", "-")
    return market_dir / f"{market_id}.md"


def nested(mapping: dict[str, Any], *keys: str) -> Any:
    value: Any = mapping
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def configured(front_matter: dict[str, Any], *keys: str) -> bool:
    return isinstance(nested(front_matter, *keys), dict)


def round_mapping(mapping: dict[str, float]) -> dict[str, float]:
    return {key: round(value, 6) for key, value in mapping.items()}


def overlay_concentration(front_matter: dict[str, Any], result: dict, as_of: str) -> None:
    section = front_matter["concentration"]
    section["model-estimate"] = round_mapping(result["model-estimate"])
    section["hhi"] = round(result["hhi"], 6)
    section["method"] = result["method"]
    section["date"] = as_of


def overlay_penetration(front_matter: dict[str, Any], result: dict, as_of: str) -> None:
    section = front_matter["penetration"]
    section["model-estimate"] = round_mapping(result["model-estimate"])
    section["method"] = result["method"]
    section["date"] = as_of


def overlay_mobility(front_matter: dict[str, Any], result: dict, as_of: str) -> None:
    section = front_matter["players"]
    section["model-estimate"] = mobility.rounded_model_estimates(result)
    section["gone-probability"] = round(result["gone-probability"], 6)
    section["method"] = result["method"]
    section["date"] = as_of


def concentration_summary(result: dict) -> dict:
    return {
        "model-estimate": result["model-estimate"],
        "selected": result["selected"],
        "selected-from": result["selected-from"],
        "hhi": result["hhi"],
        "method": result["method"],
    }


def penetration_summary(result: dict) -> dict:
    return {
        "model-estimate": result["model-estimate"],
        "selected": result["selected"],
        "selected-from": result["selected-from"],
        "w-fit": result["w-fit"],
        "projection": result["projection"],
        "method": result["method"],
    }


def mobility_summary(result: dict) -> dict:
    return {
        "model-estimate": result["model-estimate"],
        "canonical": result["canonical"],
        "gone-probability": result["gone-probability"],
        "concentration-source": result["concentration-source"],
        "method": result["method"],
    }


def refresh_market_doc(
    path: Path,
    as_of: str,
    dry_run: bool,
    concentration_data_dir: Path = concentration.DATA_DIR,
    penetration_data_dir: Path = penetration.DATA_DIR,
    mobility_data_dir: Path = mobility.DATA_DIR,
) -> dict:
    """Calculate, jointly validate, then optionally write all configured calculations."""
    if not path.exists():
        raise SystemExit(f"market-doc not found: {path}")
    _, original = concentration.split_front_matter(path.read_text(encoding="utf-8"))
    prospective = copy.deepcopy(original)
    outputs: dict[str, dict] = {}
    steps: dict[str, str] = {}

    concentration_result = None
    if configured(prospective, "concentration", "inputs", "traits"):
        models = concentration.calibrate_models(
            concentration.load_index(concentration_data_dir), concentration_data_dir
        )
        concentration_result = concentration.concentration_doc_result(models, prospective)
        overlay_concentration(prospective, concentration_result, as_of)
        outputs["concentration"] = concentration_summary(concentration_result)
        steps["concentration"] = "calculated"
    else:
        steps["concentration"] = "skipped: no concentration.inputs.traits"

    penetration_result = None
    if configured(prospective, "penetration", "inputs"):
        penetration_result = penetration.penetration_doc_result(
            prospective, path, penetration_data_dir
        )
        overlay_penetration(prospective, penetration_result, as_of)
        outputs["penetration"] = penetration_summary(penetration_result)
        steps["penetration"] = "calculated"
    else:
        steps["penetration"] = "skipped: no penetration.inputs"

    mobility_result = None
    if isinstance(nested(prospective, "players", "inputs", "current"), list):
        mobility_result = mobility.mobility_doc_result(prospective, mobility_data_dir)
        overlay_mobility(prospective, mobility_result, as_of)
        outputs["mobility"] = mobility_summary(mobility_result)
        steps["mobility"] = "calculated"
    else:
        steps["mobility"] = "skipped: no players.inputs.current"

    errors = market_doc.validate_front_matter(prospective, path)
    if errors:
        return {
            "market-doc": str(path),
            "date": as_of,
            "dry-run": dry_run,
            "written": False,
            "steps": steps,
            "outputs": outputs,
            "validation-errors": errors,
        }

    wrote = False
    if not dry_run and outputs:
        descriptor, staged_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        os.close(descriptor)
        staged_path = Path(staged_name)
        try:
            staged_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            os.chmod(staged_path, stat.S_IMODE(path.stat().st_mode))
            if concentration_result is not None:
                concentration.write_concentration_outputs(
                    staged_path, concentration_result, as_of
                )
            if penetration_result is not None:
                penetration.write_penetration_outputs(staged_path, penetration_result, as_of)
            if mobility_result is not None:
                mobility.write_mobility_outputs(staged_path, mobility_result, as_of)
            disk_errors = market_doc.validate_market_doc(staged_path)
            if disk_errors:
                raise RuntimeError(
                    "staged market-doc validation failed: " + "; ".join(disk_errors)
                )
            staged_path.replace(path)
            wrote = True
        finally:
            staged_path.unlink(missing_ok=True)

    return {
        "market-doc": str(path),
        "date": as_of,
        "dry-run": dry_run,
        "written": wrote,
        "steps": steps,
        "outputs": outputs,
        "validation-errors": [],
    }


def print_result(result: dict) -> None:
    print(Path(result["market-doc"]).stem)
    for name in ("concentration", "penetration", "mobility"):
        print(f"  {name}: {result['steps'][name]}")
    if result["validation-errors"]:
        print("  validation: failed")
        for error in result["validation-errors"]:
            print(f"    - {error}")
        print("  not written")
        return
    print("  validation: passed")
    if result["written"]:
        print("  written")
    elif result["dry-run"]:
        print("  dry run — not written")
    else:
        print("  no configured calculations — not written")


def cmd_refresh(args: argparse.Namespace) -> int:
    path = resolve_market_doc(args.market_doc, Path(args.market_dir))
    result = refresh_market_doc(path, resolve_as_of(args.as_of), args.dry_run)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_result(result)
    return 1 if result["validation-errors"] else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    refresh = sub.add_parser("refresh", help="refresh configured market-doc calculations")
    refresh.add_argument("market_doc", help="market id or Markdown path")
    refresh.add_argument("--market-dir", default=str(DEFAULT_MARKET_DIR))
    refresh.add_argument("--as-of", help="output date, YYYY-MM-DD (default today)")
    refresh.add_argument("--dry-run", action="store_true", help="calculate without writing")
    refresh.add_argument("--json", action="store_true")
    refresh.set_defaults(func=cmd_refresh)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
