#!/usr/bin/env python3
"""Fit the rank-mobility model from the panel corpus and predict transition rows.

Usage:
    mobility_fit.py windows [--json]     # derived windows, transitions, entrant composition
    mobility_fit.py fit [--json]         # fit stickiness kernel, LOO model comparison
    mobility_fit.py predict --coverage K --shares S1,S2,...,SK [--rank N] [--json]
    mobility_fit.py predict --market-doc MARKET [--dry-run] [--json]

Model (see ../references/mobility/calibration.md): a player at rank n transitions to destination
d in {1..K, fringe, gone}. Death/absorption hazard g is constant; conditional on surviving,
the destination-rank weight decays geometrically with rank distance:

    p(gone) = g
    p(i | alive)      ~ rho^|i - n|          for i = 1..K
    p(fringe | alive) ~ rho^(K+1-n) / (1-rho)   (the aggregated tail beyond K)

rho in (0,1) is the churn parameter: 0 freezes the ranking, higher values shuffle it. The
production share variant links rho to both origin rank and the origin's relative gap from its
nearest ranked neighbour. Fitting is maximum likelihood over pooled window transitions; model
comparison is leave-one-panel-out.
"""

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mobility_panels import (DATA_DIR, curve_position, derive_windows, load_index,
                             load_panel_csv)

# Fitting depth. Origins below this rank are excluded and deeper destinations collapse into the
# fringe: stickiness is rank-dependent (deep ranks churn more than the geometric kernel implies),
# and predictions are consumed for top-ranked players, so the fit is calibrated at that depth.
MAX_RANKS = 5
GONE_FATES = {"exited", "defunct", "acquired"}
EPS = 1e-12
WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_MARKET_DIR = WORKSPACE / "investment" / "market-docs"
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
PRODUCTION_METHOD = "share-gap-mobility-weighted-geometric-capture"


# ---------------------------------------------------------------- extraction

def extract(data_dir=DATA_DIR):
    """Return (observations, windows_meta). One observation per top-K origin per window."""
    observations, windows_meta = [], []
    for entry in load_index(data_dir):
        pid = entry["id"]
        players = entry.get("players") or {}
        k_eff = min(entry["coverage"], MAX_RANKS)
        logistic = (entry.get("penetration") or {}).get("logistic")
        rows = load_panel_csv(data_dir / "panels" / f"{pid}.csv")
        rank_by_year, share_by_year = {}, {}
        for year, rank, player, share in rows:
            rank_by_year.setdefault(year, {})[player] = rank
            share_by_year.setdefault(year, {})[rank] = share
        for start, end in derive_windows(sorted(rank_by_year)):
            curve = round(curve_position(logistic, start), 3) if logistic else None
            ranks_t, ranks_u = rank_by_year[start], rank_by_year[end]
            top_t = {p: r for p, r in ranks_t.items() if r <= k_eff}
            top_u = {p: r for p, r in ranks_u.items() if r <= k_eff}
            start_shares = [share_by_year[start].get(rank) for rank in range(1, k_eff + 1)]
            gaps = share_gaps(start_shares) if all(s is not None for s in start_shares) else None

            for player, n in sorted(top_t.items(), key=lambda pr: pr[1]):
                if player in top_u:
                    dest = top_u[player]
                elif player in ranks_u:
                    dest = "fringe"           # still ranked, below the modelled top K
                else:
                    facts = players.get(player) or {}
                    gone = facts.get("fate") in GONE_FATES and facts.get("fate-year", end + 1) <= end
                    dest = "gone" if gone else "fringe"
                observations.append({"panel": pid, "start": start, "end": end,
                                     "coverage": k_eff, "curve": curve,
                                     "player": player, "origin": n, "dest": dest,
                                     "share-gap": gaps[n - 1] if gaps else None})

            composition = {"held-topk": 0, "from-outside": 0, "new-to-market": 0, "not-yet-founded": 0}
            for player in top_u:
                if player in top_t:
                    composition["held-topk"] += 1
                elif player in ranks_t:
                    composition["from-outside"] += 1
                else:
                    facts = players.get(player) or {}
                    if facts.get("founded", 0) > start:
                        composition["not-yet-founded"] += 1
                    elif facts.get("entered-market", facts.get("founded", 0)) > start:
                        composition["new-to-market"] += 1
                    else:
                        composition["from-outside"] += 1
            windows_meta.append({"panel": pid, "start": start, "end": end, "coverage": k_eff,
                                 "curve": curve, "rank1-held": top_u.get(min(top_t, key=top_t.get)) == 1,
                                 "destination-origins": composition})
    return observations, windows_meta


# ---------------------------------------------------------------- model

def row_probs(n, coverage, rho, g):
    """Transition row for origin rank n: {1..K, 'fringe', 'gone'}, sums to 1."""
    rho = min(max(rho, 1e-6), 1 - 1e-6)
    weights = [rho ** abs(i - n) for i in range(1, coverage + 1)]
    w_fringe = rho ** (coverage + 1 - n) / (1 - rho)
    z = sum(weights) + w_fringe
    probs = {i + 1: (1 - g) * w / z for i, w in enumerate(weights)}
    probs["fringe"] = (1 - g) * w_fringe / z
    probs["gone"] = g
    return probs


def share_gaps(shares):
    """Relative gap from each ranked share to its nearest adjacent ranked neighbour."""
    gaps = []
    for index, share in enumerate(shares):
        adjacent = []
        if index:
            adjacent.append(shares[index - 1] - share)
        if index + 1 < len(shares):
            adjacent.append(share - shares[index + 1])
        gap = min(adjacent) if adjacent else 0.0
        gaps.append(max(0.0, gap) / max(share, EPS))
    return gaps


def validate_share_vector(shares, coverage):
    """Validate current whole-market shares ordered from rank 1 through K."""
    if not 1 <= coverage <= MAX_RANKS:
        raise ValueError(f"coverage must be between 1 and {MAX_RANKS}")
    if len(shares) != coverage:
        raise ValueError(f"shares needs exactly {coverage} values")
    if any(not math.isfinite(share) or share <= 0 or share > 1 for share in shares):
        raise ValueError("shares must be positive fractions no greater than 1")
    if any(left < right for left, right in zip(shares, shares[1:])):
        raise ValueError("shares must be ordered from current rank 1 to rank K")
    if sum(shares) > 1 + 1e-9:
        raise ValueError("shares cannot sum to more than 1")


def rho_of(a, b=0.0, curve=0.0, c=0.0, origin=1, d=0.0, share_gap=0.0):
    """Churn parameter: sigmoid(a + b*curve + c*(origin-1) + d*share_gap)."""
    linear = a + b * (curve or 0.0) + c * (origin - 1) + d * (share_gap or 0.0)
    return 1.0 / (1.0 + math.exp(-linear))


def nll(observations, a, b, c, d, g):
    total = 0.0
    for o in observations:
        rho = rho_of(a, b, o["curve"], c, o["origin"], d, o.get("share-gap"))
        probs = row_probs(o["origin"], o["coverage"], rho, g)
        total -= math.log(max(probs[o["dest"]], EPS))
    return total


def fit_kernel(observations, use_curve=False, use_rank=False, use_share=False):
    """Deterministic zooming grid search; inactive dimensions are pinned at 0."""
    spans = {"a": (-4.0, 4.0),
             "b": (-8.0, 8.0) if use_curve else (0.0, 0.0),
             "c": (-1.0, 3.0) if use_rank else (0.0, 0.0),
             "d": (-8.0, 8.0) if use_share else (0.0, 0.0),
             "g": (0.005, 0.4)}
    best = None
    for _ in range(4):
        grids = {k: ([lo] if lo == hi else [lo + (hi - lo) * s / 8 for s in range(9)])
                 for k, (lo, hi) in spans.items()}
        for a in grids["a"]:
            for b in grids["b"]:
                for c in grids["c"]:
                    for d in grids["d"]:
                        for g in grids["g"]:
                            score = nll(observations, a, b, c, d, g)
                            if best is None or score < best[0]:
                                best = (score, a, b, c, d, g)
        _, a0, b0, c0, d0, g0 = best
        spans = {k: (max(spans[k][0], v - (spans[k][1] - spans[k][0]) * 0.2),
                     min(spans[k][1], v + (spans[k][1] - spans[k][0]) * 0.2))
                 for k, v in (("a", a0), ("b", b0), ("c", c0), ("d", d0), ("g", g0))}
    score, a, b, c, d, g = best
    return {"a": round(a, 4), "b": round(b, 4), "c": round(c, 4), "d": round(d, 4),
            "g": round(g, 4), "nll": score}


def baseline_nll(observations, kind):
    total = 0.0
    for o in observations:
        k = o["coverage"]
        if kind == "uniform":
            p = 1.0 / (k + 2)
        else:  # frozen: rank preserved with prob 0.95
            p = 0.95 if o["dest"] == o["origin"] else 0.05 / (k + 1)
        total -= math.log(max(p, EPS))
    return total


def loo_by_panel(observations, use_curve=False, use_rank=False, use_share=False):
    """Leave-one-panel-out: refit without each panel, sum held-out NLL."""
    panels = sorted({o["panel"] for o in observations})
    total = 0.0
    for pid in panels:
        train = [o for o in observations if o["panel"] != pid]
        held = [o for o in observations if o["panel"] == pid]
        params = fit_kernel(train, use_curve=use_curve, use_rank=use_rank, use_share=use_share)
        total += nll(held, params["a"], params["b"], params["c"], params["d"], params["g"])
    return total


def predict_share_model(shares, data_dir=DATA_DIR):
    """Fit the production share-gap model and return unrounded transition diagnostics."""
    coverage = len(shares)
    validate_share_vector(shares, coverage)
    observations, _ = extract(data_dir)
    usable = [
        observation
        for observation in observations
        if observation["curve"] is not None and observation["share-gap"] is not None
    ]
    if not usable:
        raise ValueError("mobility corpus has no observations usable by the share model")
    params = fit_kernel(usable, use_rank=True, use_share=True)
    gaps = share_gaps(shares)
    rhos = {
        rank: rho_of(
            params["a"],
            params["b"],
            c=params["c"],
            origin=rank,
            d=params["d"],
            share_gap=gaps[rank - 1],
        )
        for rank in range(1, coverage + 1)
    }
    rows = {
        rank: row_probs(rank, coverage, rhos[rank], params["g"])
        for rank in range(1, coverage + 1)
    }
    return {
        "model": "share",
        "starting-shares": list(shares),
        "relative-share-gaps": gaps,
        "rho": rhos,
        "g": params["g"],
        "rows": rows,
        "from-outside": {
            destination: 1 - sum(rows[rank][destination] for rank in rows)
            for destination in range(1, coverage + 1)
        },
    }


def mobility_adjusted_capture(rank, s1, r, prediction):
    """Expected geometric capture across all surviving destinations; gone contributes zero."""
    coverage = len(prediction["rows"])
    row = prediction["rows"][rank]
    rho = prediction["rho"][rank]
    top_capture = sum(
        row[destination] * s1 * r ** (destination - 1)
        for destination in range(1, coverage + 1)
    )
    # `fringe` aggregates ranks K+1 onward with geometric mobility weights. Its conditional
    # expected concentration share has this closed form; gone is already absent from both terms.
    fringe_share = s1 * r**coverage * (1 - rho) / (1 - rho * r)
    return top_capture + row["fringe"] * fringe_share


# ---------------------------------------------------------------- market-doc interface

def split_front_matter(text):
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


def resolve_market_doc(arg, market_dir):
    """Resolve a market id or explicit Markdown path."""
    path = Path(arg)
    if path.suffix == ".md" or "/" in arg:
        return path
    market_id = arg.strip().lower().replace("_", "-").replace(" ", "-")
    return market_dir / f"{market_id}.md"


def _number(mapping, key, source):
    try:
        value = float(mapping[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"{source}.{key} must be a number") from exc
    if not math.isfinite(value):
        raise SystemExit(f"{source}.{key} must be finite")
    return value


def market_doc_concentration(front_matter):
    """Read the canonical geometric concentration parameters."""
    concentration = front_matter.get("concentration")
    if not isinstance(concentration, dict):
        raise SystemExit("market-doc has no concentration mapping")
    source = "override" if "override" in concentration else "model-estimate"
    parameters = concentration.get(source)
    if not isinstance(parameters, dict):
        raise SystemExit(
            "concentration requires override or model-estimate before running mobility"
        )
    s1 = _number(parameters, "s1", f"concentration.{source}")
    r = _number(parameters, "r", f"concentration.{source}")
    if not 0 < s1 <= 1:
        raise SystemExit(f"concentration.{source}.s1 must be in (0, 1]")
    if not 0 < r < 1:
        raise SystemExit(f"concentration.{source}.r must be in (0, 1)")
    if s1 / (1 - r) > 1 + 1e-9:
        raise SystemExit(
            f"canonical concentration curve has modeled mass {s1 / (1 - r):.3f} > 1; "
            "mobility requires a valid whole-market rank-share vector"
        )
    return s1, r, source


def market_doc_current_players(front_matter):
    """Read the analyst-owned current top-K ranking and whole-market shares."""
    players = front_matter.get("players")
    inputs = players.get("inputs") if isinstance(players, dict) else None
    current = inputs.get("current") if isinstance(inputs, dict) else None
    if not isinstance(current, list) or not 2 <= len(current) <= MAX_RANKS:
        raise SystemExit(
            f"players.inputs.current must contain the current top 2..{MAX_RANKS} players"
        )

    parsed = []
    for index, entry in enumerate(current, start=1):
        source = f"players.inputs.current[{index}]"
        if not isinstance(entry, dict):
            raise SystemExit(f"{source} must be a mapping")
        try:
            rank = int(entry["rank"])
        except (KeyError, TypeError, ValueError) as exc:
            raise SystemExit(f"{source}.rank must be an integer") from exc
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SystemExit(f"{source}.name must be non-empty")
        ticker = entry.get("ticker")
        if ticker is not None and (not isinstance(ticker, str) or not ticker.strip()):
            raise SystemExit(f"{source}.ticker must be a non-empty string or omitted")
        share = _number(entry, "share", source)
        parsed.append(
            {
                "rank": rank,
                "name": name.strip(),
                **({"ticker": ticker.strip()} if ticker is not None else {}),
                "share": share,
            }
        )

    ranks = [entry["rank"] for entry in parsed]
    if ranks != list(range(1, len(parsed) + 1)):
        raise SystemExit("players.inputs.current ranks must be ordered and contiguous from 1")
    names = [entry["name"] for entry in parsed]
    if len(set(names)) != len(names):
        raise SystemExit("players.inputs.current names must be unique")
    try:
        validate_share_vector([entry["share"] for entry in parsed], len(parsed))
    except ValueError as exc:
        raise SystemExit(f"players.inputs.current: {exc}") from exc
    return parsed


def market_doc_maturity_value(front_matter):
    """Read the projected market value used to convert capture into revenue."""
    size = front_matter.get("size")
    if not isinstance(size, dict):
        raise SystemExit("market-doc requires size.maturity-market-value for mobility revenue")
    value = _number(size, "maturity-market-value", "size")
    if value < 0:
        raise SystemExit("size.maturity-market-value must be non-negative")
    return value


def market_doc_player_overrides(front_matter):
    """Read optional per-player analyst capture replacements."""
    players = front_matter.get("players")
    overrides = players.get("override") if isinstance(players, dict) else None
    if overrides is None:
        return []
    if not isinstance(overrides, list):
        raise SystemExit("players.override must be a list or be omitted")
    parsed = []
    for index, entry in enumerate(overrides, start=1):
        source = f"players.override[{index}]"
        if not isinstance(entry, dict):
            raise SystemExit(f"{source} must be a mapping")
        name = entry.get("name")
        reason = entry.get("reason")
        if not isinstance(name, str) or not name.strip():
            raise SystemExit(f"{source}.name must be non-empty")
        if not isinstance(reason, str) or not reason.strip():
            raise SystemExit(f"{source}.reason must be non-empty")
        capture = _number(entry, "capture", source)
        if not 0 <= capture <= 1:
            raise SystemExit(f"{source}.capture must be in [0, 1]")
        ticker = entry.get("ticker")
        if ticker is not None and (not isinstance(ticker, str) or not ticker.strip()):
            raise SystemExit(f"{source}.ticker must be a non-empty string or omitted")
        parsed.append(
            {
                "name": name.strip(),
                **({"ticker": ticker.strip()} if ticker is not None else {}),
                "capture": capture,
                "reason": reason.strip(),
            }
        )
    names = [entry["name"] for entry in parsed]
    if len(set(names)) != len(names):
        raise SystemExit("players.override names must be unique")
    return parsed


def resolve_player_captures(model_estimate, overrides):
    """Resolve per-player canonical capture, with overrides also able to add outsiders."""
    override_by_name = {entry["name"]: entry for entry in overrides}
    canonical = []
    model_names = set()
    for estimate in model_estimate:
        name = estimate["name"]
        model_names.add(name)
        override = override_by_name.get(name)
        if override is None:
            canonical.append(
                {
                    "name": name,
                    **({"ticker": estimate["ticker"]} if estimate.get("ticker") else {}),
                    "capture": estimate["mobility-adjusted-capture"],
                    "source": "model-estimate",
                }
            )
        else:
            canonical.append(
                {
                    "name": name,
                    **(
                        {"ticker": override.get("ticker") or estimate.get("ticker")}
                        if override.get("ticker") or estimate.get("ticker")
                        else {}
                    ),
                    "capture": override["capture"],
                    "source": "override",
                }
            )
    for override in overrides:
        if override["name"] not in model_names:
            canonical.append(
                {
                    "name": override["name"],
                    **({"ticker": override["ticker"]} if override.get("ticker") else {}),
                    "capture": override["capture"],
                    "source": "override",
                }
            )
    total = sum(entry["capture"] for entry in canonical)
    if total > 1 + 1e-9:
        raise SystemExit(f"canonical player captures sum to {total:.3f} > 1")
    return canonical


def mobility_doc_result(front_matter, data_dir=DATA_DIR):
    """Calculate mobility-adjusted capture and revenue from the market-doc inputs."""
    current = market_doc_current_players(front_matter)
    s1, r, concentration_source = market_doc_concentration(front_matter)
    maturity_value = market_doc_maturity_value(front_matter)
    shares = [entry["share"] for entry in current]
    try:
        prediction = predict_share_model(shares, data_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    estimates = []
    for player in current:
        rank = player["rank"]
        adjusted_capture = mobility_adjusted_capture(rank, s1, r, prediction)
        estimates.append(
            {
                "rank": rank,
                "name": player["name"],
                **({"ticker": player["ticker"]} if player.get("ticker") else {}),
                "hold-position-capture": s1 * r ** (rank - 1),
                "mobility-adjusted-capture": adjusted_capture,
                "mobility-adjusted-revenue": adjusted_capture * maturity_value,
            }
        )
    overrides = market_doc_player_overrides(front_matter)
    return {
        "model-estimate": estimates,
        "canonical": resolve_player_captures(estimates, overrides),
        "maturity-market-value": maturity_value,
        "gone-probability": prediction["g"],
        "method": PRODUCTION_METHOD,
        "concentration-source": concentration_source,
        "diagnostics": prediction,
    }


def _indent(line):
    return len(line) - len(line.lstrip(" "))


class _IndentedSafeDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _render_yaml_child(key, value, indent):
    if isinstance(value, str):
        return [f"{' ' * indent}{key}: {value}"]
    dumped = yaml.dump(
        {key: value},
        Dumper=_IndentedSafeDumper,
        sort_keys=False,
        default_flow_style=False,
    ).rstrip()
    return [" " * indent + line for line in dumped.splitlines()]


def rounded_model_estimates(result):
    """Round stored estimates and derive revenue from the stored capture precision."""
    estimates = [
        {
            key: round(value, 6) if isinstance(value, float) else value
            for key, value in estimate.items()
        }
        for estimate in result["model-estimate"]
    ]
    maturity_value = result["maturity-market-value"]
    for estimate in estimates:
        estimate["mobility-adjusted-revenue"] = round(
            estimate["mobility-adjusted-capture"] * maturity_value, 6
        )
    return estimates


def upsert_players_child(block, key, value):
    """Surgically replace or append one script-owned child of `players`."""
    lines = block.splitlines()
    parent_i = next(
        (i for i, line in enumerate(lines) if re.fullmatch(r"players:\s*", line)),
        None,
    )
    if parent_i is None:
        raise SystemExit("cannot write back: market-doc has no top-level 'players:' block")
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
    replacement = _render_yaml_child(key, value, child_indent)
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


def resolve_as_of(arg):
    if arg is None:
        return date.today().isoformat()
    try:
        return date.fromisoformat(arg).isoformat()
    except ValueError as exc:
        raise SystemExit(f"--as-of must be YYYY-MM-DD, got {arg!r}") from exc


def write_mobility_outputs(path, result, as_of):
    """Write only script-owned player outputs; preserve inputs, overrides, peers and body."""
    text = path.read_text(encoding="utf-8")
    match = FM_RE.match(text)
    if not match:
        raise SystemExit(f"cannot write back: {path} has no front-matter block")
    block = match.group(1)
    estimates = rounded_model_estimates(result)
    block = upsert_players_child(block, "model-estimate", estimates)
    block = upsert_players_child(
        block, "gone-probability", round(result["gone-probability"], 6)
    )
    block = upsert_players_child(block, "method", result["method"])
    block = upsert_players_child(block, "date", as_of)
    path.write_text(f"---\n{block}\n---\n" + text[match.end():], encoding="utf-8")


def cmd_predict_market_doc(args):
    raw_options = (
        args.coverage is not None
        or args.shares is not None
        or args.rank is not None
        or args.model != "share"
        or args.curve_position is not None
        or args.t0 is not None
        or args.k is not None
        or args.year is not None
    )
    if raw_options:
        raise SystemExit(
            "--market-doc reads the current ranking and production model inputs from front matter; "
            "do not also pass raw prediction options"
        )
    path = resolve_market_doc(args.market_doc, Path(args.market_dir))
    if not path.exists():
        raise SystemExit(f"market-doc not found: {path}")
    _, front_matter = split_front_matter(path.read_text(encoding="utf-8"))
    result = mobility_doc_result(front_matter, Path(args.data_dir))
    as_of = resolve_as_of(args.as_of)
    wrote = not args.dry_run
    if wrote:
        write_mobility_outputs(path, result, as_of)
    output = {**result, "date": as_of, "market-doc": str(path), "written": wrote}
    if args.json:
        print(json.dumps(output, indent=2))
        return 0
    print(
        f"{path.stem}: share-gap mobility × canonical concentration "
        f"({result['concentration-source']})"
    )
    for estimate in result["model-estimate"]:
        print(
            f"  #{estimate['rank']} {estimate['name']}: "
            f"hold {estimate['hold-position-capture']:.3f} -> "
            f"mobility-adjusted {estimate['mobility-adjusted-capture']:.3f}, "
            f"revenue {estimate['mobility-adjusted-revenue']:.3f}bn "
            f"{front_matter.get('currency', '')}".rstrip()
        )
    print(f"gone probability {result['gone-probability']:.3f} (already included)")
    print(f"{'written to ' + str(path) if wrote else 'dry run — not written'}")
    return 0


# ---------------------------------------------------------------- commands

def cmd_windows(args):
    observations, windows_meta = extract()
    if args.json:
        print(json.dumps({"windows": windows_meta, "observations": observations}, indent=2))
        return 0
    print(f"{'panel':<36} {'window':>11} {'K':>2} {'F':>5}  rank1-held  destination origins")
    for w in windows_meta:
        comp = w["destination-origins"]
        comp_txt = ", ".join(f"{k}={v}" for k, v in comp.items() if v)
        curve = f"{w['curve']:.2f}" if w["curve"] is not None else "-"
        print(f"{w['panel']:<36} {w['start']}-{w['end']} {w['coverage']:>2} {curve:>5}"
              f"  {'yes' if w['rank1-held'] else 'NO':>10}  {comp_txt}")
    pooled = {}
    for w in windows_meta:
        for k, v in w["destination-origins"].items():
            pooled[k] = pooled.get(k, 0) + v
    slots = sum(pooled.values())
    print(f"\n{len(observations)} transitions from {len(windows_meta)} windows; "
          f"destination top-K slots: " +
          ", ".join(f"{k} {v} ({v / slots:.0%})" for k, v in pooled.items()))
    return 0


def cmd_fit(args):
    observations, windows_meta = extract()
    usable = [o for o in observations if o["curve"] is not None and o["share-gap"] is not None]
    skipped = len(observations) - len(usable)
    n = len(usable)
    variants = {"constant": {}, "maturity": {"use_curve": True}, "rank": {"use_rank": True},
                "share": {"use_rank": True, "use_share": True}}
    result = {"observations": n, "windows": len(windows_meta),
              "panels": len({o["panel"] for o in usable}), "skipped-no-curve-or-shares": skipped,
              "models": {}, "baselines": {
                  "uniform-nll-per-obs": round(baseline_nll(usable, "uniform") / n, 4),
                  "frozen-nll-per-obs": round(baseline_nll(usable, "frozen") / n, 4)}}
    for name, flags in variants.items():
        params = fit_kernel(usable, **flags)
        result["models"][name] = {
            **params,
            "nll-per-obs": round(params["nll"] / n, 4),
            "loo-nll-per-obs": round(loo_by_panel(usable, **flags) / n, 4)}
    result["loo-winner"] = min(result["models"], key=lambda k: result["models"][k]["loo-nll-per-obs"])
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"{n} transitions, {result['windows']} windows, {result['panels']} panels"
          + (f" ({skipped} obs skipped: no curve position or complete start shares)"
             if skipped else ""))
    forms = {"constant": lambda p: f"rho={rho_of(p['a']):.3f}",
             "maturity": lambda p: f"rho(F)=sigmoid({p['a']} + {p['b']}*F)",
             "rank": lambda p: "rho(n)=" + ", ".join(
                 f"#{i}: {rho_of(p['a'], c=p['c'], origin=i):.3f}" for i in range(1, 6)),
             "share": lambda p: f"rho(n,gap)=sigmoid({p['a']} + {p['c']}*(n-1)"
                                       f" + {p['d']}*gap)"}
    print()
    for name, m in result["models"].items():
        print(f"{name:<9} g={m['g']}  {forms[name](m)}"
              f"\n{'':<9} NLL/obs in-sample {m['nll-per-obs']}, LOO {m['loo-nll-per-obs']}")
    b = result["baselines"]
    print(f"baselines: uniform {b['uniform-nll-per-obs']}, frozen-ranking {b['frozen-nll-per-obs']}")
    print(f"\nLOO winner: {result['loo-winner']}. Treat as coarse; the corpus is small and most "
          f"penetration parameters are provenance=estimated.")
    return 0


def cmd_predict(args):
    if args.market_doc:
        return cmd_predict_market_doc(args)
    if args.coverage is None:
        print("predict requires --coverage or --market-doc", file=sys.stderr)
        return 2
    data_dir = Path(args.data_dir)
    usable = None
    curve = None
    if not 1 <= args.coverage <= MAX_RANKS:
        print(f"--coverage must be between 1 and {MAX_RANKS}", file=sys.stderr)
        return 2
    if args.rank is not None and not 1 <= args.rank <= args.coverage:
        print("--rank must be between 1 and --coverage", file=sys.stderr)
        return 2
    shares, gaps = None, None
    if args.shares is not None:
        shares = args.shares
        try:
            validate_share_vector(shares, args.coverage)
        except ValueError as exc:
            print(f"--{exc}", file=sys.stderr)
            return 2
        gaps = share_gaps(shares)
    if args.model == "share":
        if shares is None:
            print("--model share needs --shares S1,S2,...,SK", file=sys.stderr)
            return 2
        try:
            prediction = predict_share_model(shares, data_dir)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        gaps = prediction["relative-share-gaps"]
        rhos = prediction["rho"]
        rows = prediction["rows"]
        g = prediction["g"]
    elif args.model == "maturity":
        observations, _ = extract(data_dir)
        usable = [o for o in observations if o["curve"] is not None]
        if args.curve_position is not None:
            curve = args.curve_position
        elif args.t0 is not None and args.k is not None and args.year is not None:
            curve = curve_position({"t0": args.t0, "k": args.k}, args.year)
        else:
            print("--model maturity needs --curve-position or all of --t0/--k/--year", file=sys.stderr)
            return 2
        params = fit_kernel(usable, use_curve=True)
        g = params["g"]
    else:
        observations, _ = extract(data_dir)
        usable = [o for o in observations if o["curve"] is not None]
        params = fit_kernel(usable, use_rank=(args.model == "rank"))
        g = params["g"]
    coverage = args.coverage
    ranks = [args.rank] if args.rank else list(range(1, coverage + 1))
    if args.model != "share":
        rhos = {n: rho_of(params["a"], params["b"], curve, params["c"], n, params["d"],
                          gaps[n - 1] if gaps else 0.0) for n in ranks}
        rows = {n: row_probs(n, coverage, rhos[n], g) for n in ranks}
    elif args.rank:
        rhos = {args.rank: rhos[args.rank]}
        rows = {args.rank: rows[args.rank]}
    if args.json:
        out = {"model": args.model,
               "curve-position": round(curve, 3) if curve is not None else None,
               "starting-shares": shares,
               "relative-share-gaps": ([round(gap, 4) for gap in gaps] if gaps else None),
               "rho": {n: round(r, 4) for n, r in rhos.items()}, "g": g,
               "rows": {n: {str(k): round(v, 4) for k, v in r.items()} for n, r in rows.items()}}
        if not args.rank:
            out["from-outside"] = {i: round(1 - sum(rows[n][i] for n in ranks), 4)
                                   for i in range(1, coverage + 1)}
        print(json.dumps(out, indent=2))
        return 0
    label = f"maturity model, F={curve:.3f}" if curve is not None else f"{args.model} model"
    rho_txt = ", ".join(f"#{n}: {r:.3f}" for n, r in rhos.items()) if args.model in {"rank", "share"} \
        else f"{next(iter(rhos.values())):.3f}"
    print(f"{label} -> rho {rho_txt}, gone hazard g={g}")
    header = "  ".join(f"{('#' + str(i)):>6}" for i in range(1, coverage + 1))
    print(f"{'origin':<8} {header}  {'fringe':>7} {'gone':>6}")
    for n in ranks:
        r = rows[n]
        cells = "  ".join(f"{r[i]:>6.3f}" for i in range(1, coverage + 1))
        print(f"rank {n:<3} {cells}  {r['fringe']:>7.3f} {r['gone']:>6.3f}")
    if not args.rank:
        outside = "  ".join(f"{1 - sum(rows[n][i] for n in ranks):>6.3f}"
                            for i in range(1, coverage + 1))
        print(f"{'outside':<8} {outside}   <- share of each future rank won from outside today's top {coverage}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fit/predict rank mobility from the panel corpus")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("windows", "fit"):
        p = sub.add_parser(name)
        p.add_argument("--json", action="store_true")
    p = sub.add_parser("predict")
    p.add_argument("--coverage", type=int, help="raw mode: number of named ranks to model")
    p.add_argument("--shares", type=lambda value: [float(v) for v in value.split(",")],
                   help="current whole-market shares ordered from rank 1 to K (fractions)")
    p.add_argument("--rank", type=int, help="origin rank (default: all)")
    p.add_argument("--model", choices=["share", "rank", "constant", "maturity"], default="share",
                   help="rank + current-share-gap model (default), or a diagnostic fallback")
    p.add_argument("--curve-position", type=float, help="adoption-curve position F at present")
    p.add_argument("--t0", type=float, help="logistic inflection year")
    p.add_argument("--k", type=float, help="logistic steepness per year")
    p.add_argument("--year", type=float, help="year to evaluate the curve at")
    p.add_argument("--market-doc",
                   help="market id or Markdown path; read current shares and concentration, then "
                        "write mobility-adjusted capture")
    p.add_argument("--market-dir", default=str(DEFAULT_MARKET_DIR))
    p.add_argument("--data-dir", default=str(DATA_DIR))
    p.add_argument("--dry-run", action="store_true",
                   help="market-doc mode: calculate without writing")
    p.add_argument("--as-of", help="market-doc mode: output date, YYYY-MM-DD (default today)")
    p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return {"windows": cmd_windows, "fit": cmd_fit, "predict": cmd_predict}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
