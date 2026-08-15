#!/usr/bin/env python3
"""Fetch an up-to-date Sharesight holdings snapshot with minimal API calls.

Secrets are read from environment variables if present, otherwise from Bitwarden.
Nothing secret is stored here.

Credential sources, in order:
  1. SHARESIGHT_CLIENT_ID + SHARESIGHT_CLIENT_SECRET (CLIENT_ID + SECRET also accepted)
  2. Bitwarden item named by SHARESIGHT_BW_ITEM, default: "Nick's sharesight API key"

Default API calls: 1 token request + 1 valuation request per configured portfolio.
For the default portfolios below, that is 4 HTTP requests total.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

TOKEN_URL = os.environ.get("SHARESIGHT_TOKEN_URL", "https://api.sharesight.com/oauth2/token")
API_BASE = os.environ.get("SHARESIGHT_API_BASE", "https://api.sharesight.com/api/v2")
DEFAULT_BW_ITEM = os.environ.get("SHARESIGHT_BW_ITEM", "Nick's sharesight API key")

# Portfolio IDs are not secrets. Keeping them here avoids a discovery call every run.
DEFAULT_PORTFOLIOS = {
    "Erika": 1231212,
    "Nick": 1231095,
    "GrumpyFund": 1259505,
}


def optional_env(name: str, *aliases: str) -> str | None:
    for key in (name, *aliases):
        value = os.environ.get(key)
        if value:
            return value
    return None


def parse_notes(notes: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in notes.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip().lower()] = value.strip()
    return result


def run_bw(args: list[str]) -> str:
    bw = shutil.which("bw")
    if not bw:
        raise SystemExit("Missing credentials and Bitwarden CLI (`bw`) is not installed or not on PATH.")

    try:
        proc = subprocess.run([bw, *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
    except subprocess.TimeoutExpired as e:
        raise SystemExit(f"Bitwarden command timed out: bw {' '.join(args)}") from e

    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout).strip()
        raise SystemExit(f"Bitwarden command failed: bw {' '.join(args)}\n{msg}")
    return proc.stdout


def bitwarden_credentials(item_name: str) -> tuple[str, str]:
    bw_session = os.environ.get("BW_SESSION")
    get_args = ["get", "item", item_name]
    if bw_session:
        # `bw status` still reports "locked" when only BW_SESSION is exported,
        # but `bw get ... --session <key>` is valid. Treat BW_SESSION as the
        # explicit unlock mechanism and avoid interactive prompts.
        get_args.extend(["--session", bw_session])
    else:
        try:
            status = json.loads(run_bw(["status"]))
        except json.JSONDecodeError as e:
            raise SystemExit("Could not parse `bw status` output as JSON.") from e

        if status.get("status") != "unlocked":
            raise SystemExit(
                "Missing Sharesight credentials in env and Bitwarden is not unlocked.\n"
                "Unlock it first, e.g. `export BW_SESSION=$(bw unlock --raw)`, then rerun."
            )

    raw_item = run_bw(get_args)
    try:
        item = json.loads(raw_item)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Could not parse Bitwarden item {item_name!r} as JSON.") from e

    notes = parse_notes(item.get("notes") or "")
    client_id = notes.get("client id") or notes.get("client_id") or notes.get("api key")
    client_secret = notes.get("client secret") or notes.get("client_secret") or item.get("login", {}).get("password")
    if not client_id or not client_secret:
        raise SystemExit(
            f"Bitwarden item {item_name!r} did not contain Client Id and Client Secret in notes/login."
        )
    return client_id, client_secret


def get_credentials(bw_item: str) -> tuple[str, str]:
    client_id = optional_env("SHARESIGHT_CLIENT_ID", "CLIENT_ID")
    client_secret = optional_env("SHARESIGHT_CLIENT_SECRET", "SECRET")
    if client_id and client_secret:
        return client_id, client_secret
    if client_id or client_secret:
        raise SystemExit(
            "Incomplete environment credentials: provide both client id and client secret, "
            "or neither so the script can read Bitwarden."
        )
    return bitwarden_credentials(bw_item)


def request_json(url: str, *, method: str = "GET", data: dict[str, str] | None = None, token: str | None = None) -> Any:
    headers = {"Accept": "application/json", "User-Agent": "openclaw-sharesight-holdings/1.0"}
    body = None
    if data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"HTTP {e.code} for {url}: {detail}") from e


def get_access_token(bw_item: str) -> str:
    client_id, client_secret = get_credentials(bw_item)
    payload = request_json(
        TOKEN_URL,
        method="POST",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"Token response did not include access_token; keys={sorted(payload.keys())}")
    return token


def parse_portfolio_arg(values: list[str] | None) -> dict[str, int]:
    if not values:
        return dict(DEFAULT_PORTFOLIOS)
    result: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit("--portfolio must be NAME=ID, e.g. --portfolio Nick=1231095")
        name, raw_id = value.split("=", 1)
        name = name.strip()
        if not name:
            raise SystemExit("Portfolio name cannot be empty")
        result[name] = int(raw_id)
    return result


def fetch_valuation(token: str, portfolio_name: str, portfolio_id: int, balance_date: str | None) -> list[dict[str, Any]]:
    params = {"consolidated": "false", "grouping": "market", "include_sales": "false"}
    if balance_date:
        params["balance_date"] = balance_date
    url = f"{API_BASE}/portfolios/{portfolio_id}/valuation.json?{urllib.parse.urlencode(params)}"
    report = request_json(url, token=token)
    rows = []
    for holding in report.get("holdings", []):
        rows.append(
            {
                "portfolio": portfolio_name,
                "portfolio_id": portfolio_id,
                "balance_date": report.get("balance_date"),
                "symbol": holding.get("symbol"),
                "market": holding.get("market"),
                "name": holding.get("name"),
                "quantity": holding.get("quantity"),
                "value_aud": holding.get("value"),
                "holding_id": holding.get("id"),
                "instrument_id": holding.get("instrument_id"),
            }
        )
    return rows


def write_csv(rows: list[dict[str, Any]], path: str | None) -> None:
    fields = [
        "portfolio",
        "symbol",
        "market",
        "name",
        "quantity",
        "value_aud",
        "balance_date",
        "holding_id",
        "instrument_id",
        "portfolio_id",
    ]
    out = open(path, "w", newline="") if path else sys.stdout
    try:
        writer = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if path:
            out.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Sharesight holdings for Erika, Nick, and GrumpyFund.")
    parser.add_argument("--format", choices=("csv", "json"), default="csv")
    parser.add_argument("--output", "-o", help="Write to file instead of stdout")
    parser.add_argument("--balance-date", help="YYYY-MM-DD; defaults to Sharesight's current valuation date")
    parser.add_argument(
        "--bw-item",
        default=DEFAULT_BW_ITEM,
        help="Bitwarden item name/id to read credentials from when env credentials are absent.",
    )
    parser.add_argument(
        "--portfolio",
        action="append",
        help="Portfolio to fetch as NAME=ID. Repeat to override defaults.",
    )
    args = parser.parse_args()

    portfolios = parse_portfolio_arg(args.portfolio)
    token = get_access_token(args.bw_item)

    rows: list[dict[str, Any]] = []
    for name, portfolio_id in portfolios.items():
        rows.extend(fetch_valuation(token, name, portfolio_id, args.balance_date))

    rows.sort(key=lambda r: (str(r["portfolio"]), -(float(r["value_aud"] or 0)), str(r["symbol"] or "")))

    if args.format == "json":
        payload = {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "api_base": API_BASE,
            "portfolio_count": len(portfolios),
            "holding_count": len(rows),
            "holdings": rows,
        }
        text = json.dumps(payload, indent=2, sort_keys=True)
        if args.output:
            with open(args.output, "w") as f:
                f.write(text + "\n")
        else:
            print(text)
    else:
        write_csv(rows, args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
