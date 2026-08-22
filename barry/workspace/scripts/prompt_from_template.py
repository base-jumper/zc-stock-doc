#!/usr/bin/env python3
"""Render a ticker prompt template and optionally schedule it for an agent."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PLACEHOLDER = "{{TICKER}}"
QUEUE_ITEM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-]{0,95}$")


def read_ticker() -> str | None:
    """Read exactly one non-empty queue item from standard input."""
    items = [line.strip() for line in sys.stdin if line.strip()]
    if not items:
        return None
    if len(items) != 1:
        raise SystemExit(
            f"expected exactly one queue item on stdin, received {len(items)}; "
            "use one prompt dispatch per ticker"
        )

    item = items[0]
    if not QUEUE_ITEM_RE.fullmatch(item):
        raise SystemExit(f"invalid ticker or queue item: {item!r}")
    return item


def render_template(path: Path, ticker: str) -> str:
    try:
        template = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"could not read template {path}: {exc}") from exc

    if PLACEHOLDER not in template:
        raise SystemExit(f"template {path} does not contain {PLACEHOLDER}")
    return template.replace(PLACEHOLDER, ticker)


def resolve_executable(value: str) -> str:
    if "/" in value:
        return value
    executable = shutil.which(value)
    if executable:
        return executable
    raise SystemExit(
        f"could not find {value!r} on PATH; pass --zeroclaw with its absolute path"
    )


def schedule_prompt(prompt: str, agent: str, delay: str, zeroclaw: str) -> int:
    executable = resolve_executable(zeroclaw)
    command = [
        executable,
        "cron",
        "once",
        delay,
        prompt,
        "--agent",
        agent,
        "--prompt",
    ]
    try:
        result = subprocess.run(command, text=True, capture_output=True)
    except OSError as exc:
        raise SystemExit(f"could not run {executable}: {exc}") from exc

    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise SystemExit(
            f"zeroclaw cron once failed with exit code {result.returncode}"
            + (f": {detail}" if detail else "")
        )
    if result.stderr:
        sys.stderr.write(result.stderr)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a {{TICKER}} prompt template from one queue item on stdin. "
            "With --agent, schedule the rendered prompt as a one-shot agent job."
        )
    )
    parser.add_argument("template", type=Path, help="Markdown prompt template")
    parser.add_argument(
        "--agent",
        help="schedule the rendered prompt for this ZeroClaw agent alias",
    )
    parser.add_argument(
        "--delay",
        default="1s",
        help="delay for the one-shot agent job (default: %(default)s)",
    )
    parser.add_argument(
        "--zeroclaw",
        default=os.environ.get("ZEROCLAW_BIN", "zeroclaw"),
        help="ZeroClaw executable (default: ZEROCLAW_BIN or zeroclaw)",
    )
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="print the rendered prompt instead of scheduling it",
    )
    args = parser.parse_args()

    if args.render_only and args.agent:
        parser.error("--render-only cannot be combined with --agent")

    ticker = read_ticker()
    if ticker is None:
        return 0

    prompt = render_template(args.template, ticker)
    if args.agent is None:
        sys.stdout.write(prompt)
        if prompt and not prompt.endswith("\n"):
            sys.stdout.write("\n")
        return 0

    return schedule_prompt(prompt, args.agent, args.delay, args.zeroclaw)


if __name__ == "__main__":
    raise SystemExit(main())
