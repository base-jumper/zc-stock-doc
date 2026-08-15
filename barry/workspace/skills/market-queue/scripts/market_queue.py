#!/usr/bin/env python3
"""FIFO market ID queue helper for Barry/ZeroClaw."""
from __future__ import annotations

import argparse
import fcntl
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_QUEUE = WORKSPACE / 'tasks' / 'market-analysis-fifo-queue.txt'
DEFAULT_LOG = WORKSPACE / 'tasks' / 'market-analysis-fifo-queue.log.jsonl'
DEFAULT_HOURS_PER_RUN = 3.0
MARKET_ID_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,95}$')

DEFAULT_CRON_DIR = Path.home() / '.zeroclaw' / 'data' / 'cron'
FIFO_JOB_RE = re.compile(r'(?=.*market)(?=.*fifo)', re.IGNORECASE)
# Max input context per model-name prefix, used to estimate context window use.
CONTEXT_WINDOWS = [
    ('gpt-5', 272_000),
    ('claude', 200_000),
]
FALLBACK_CONTEXT_WINDOW = 200_000


def normalize(market_id: str) -> str:
    t = market_id.strip().lower()
    if not MARKET_ID_RE.match(t):
        raise SystemExit(f'invalid market ID: {market_id!r}')
    return t


def ensure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [ln.strip().lower() for ln in path.read_text().splitlines() if ln.strip()]


def log_event(log_path: Path, event: str, market_id: str | None = None, **extra) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'event': event,
        **({'market_id': market_id} if market_id else {}),
        **extra,
    }
    with log_path.open('a') as f:
        f.write(json.dumps(payload, sort_keys=True) + '\n')


def with_lock(path: Path):
    ensure(path)
    f = path.open('r+')
    fcntl.flock(f, fcntl.LOCK_EX)
    return f


def cmd_add(args) -> int:
    market_ids = [normalize(t) for t in args.market_ids]
    q = Path(args.queue)
    log = Path(args.log)
    with with_lock(q) as f:
        existing = [ln.strip().lower() for ln in f.read().splitlines() if ln.strip()]
        additions = []
        for t in market_ids:
            if args.unique and t in existing:
                continue
            existing.append(t)
            additions.append(t)
        f.seek(0)
        f.truncate()
        if existing:
            f.write('\n'.join(existing) + '\n')
    for t in additions:
        log_event(log, 'queued', t)
    print('\n'.join(additions) if additions else 'no new markets queued')
    return 0


def cmd_peek(args) -> int:
    lines = read_lines(Path(args.queue))
    if lines:
        print(lines[0])
        return 0
    return 1


def cmd_list(args) -> int:
    lines = read_lines(Path(args.queue))
    for i, market_id in enumerate(lines, 1):
        print(f'{i}. {market_id}')
    if not lines:
        print('(empty)')
    return 0


def cmd_complete_first(args) -> int:
    market_id = normalize(args.market_id)
    q = Path(args.queue)
    log = Path(args.log)
    with with_lock(q) as f:
        lines = [ln.strip().lower() for ln in f.read().splitlines() if ln.strip()]
        if not lines:
            raise SystemExit('queue is empty')
        if lines[0] != market_id:
            raise SystemExit(f'first queued market_id is {lines[0]}, not {market_id}; refusing to remove')
        remaining = lines[1:]
        f.seek(0)
        f.truncate()
        if remaining:
            f.write('\n'.join(remaining) + '\n')
    log_event(log, 'completed', market_id)
    print(f'completed and removed {market_id}')
    return 0


def format_duration(hours: float) -> str:
    if hours <= 0:
        return '0h'
    whole_hours = int(hours)
    minutes = round((hours - whole_hours) * 60)
    if minutes == 60:
        whole_hours += 1
        minutes = 0
    days, rem_hours = divmod(whole_hours, 24)
    parts = []
    if days:
        parts.append(f'{days}d')
    if rem_hours:
        parts.append(f'{rem_hours}h')
    if minutes:
        parts.append(f'{minutes}m')
    return ' '.join(parts) if parts else '0h'


def parse_now(value: str | None) -> datetime:
    if not value:
        return datetime.now().astimezone()
    text = value.strip()
    if text.endswith('Z'):
        text = text[:-1] + '+00:00'
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        return parsed.astimezone()
    return parsed


def cmd_estimate(args) -> int:
    if args.hours_per_run <= 0:
        raise SystemExit('--hours-per-run must be > 0')
    lines = read_lines(Path(args.queue))
    count = len(lines)
    total_hours = count * args.hours_per_run
    now = parse_now(args.now)
    finish = now + timedelta(hours=total_hours)
    print(f'queued={count}')
    print(f'cadence=1 market every {format_duration(args.hours_per_run)}')
    print(f'total={format_duration(total_hours)}')
    print(f'estimated-empty-at={finish.isoformat(timespec="minutes")}')
    if count:
        print(f'next={lines[0]}')
        print(f'last={lines[-1]}')
    return 0


def resolve_fifo_job_id(cron_dir: Path) -> str:
    jobs_path = cron_dir / 'jobs.json'
    if jobs_path.exists():
        data = json.loads(jobs_path.read_text())
        source = str(jobs_path)
    else:
        # OpenClaw 2026.7 migrated cron job metadata out of jobs.json. Query the
        # gateway on current versions while retaining legacy-file support.
        try:
            result = subprocess.run(
                ['openclaw', 'cron', 'list', '--all', '--json'],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            data = json.loads(result.stdout)
            source = 'openclaw cron list --all --json'
        except (FileNotFoundError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
            raise SystemExit(
                f'cron jobs file not found: {jobs_path}; '
                f'could not query current cron metadata: {exc}'
            ) from exc
    jobs = data if isinstance(data, list) else data.get('jobs', [])
    matches = [j for j in jobs if FIFO_JOB_RE.search(j.get('name', ''))]
    if not matches:
        raise SystemExit(f'no market FIFO cron job found via {source}')
    if len(matches) > 1:
        names = ', '.join(f"{j['id']} ({j['name']})" for j in matches)
        raise SystemExit(f'multiple market FIFO cron jobs found, pass --job-id: {names}')
    return matches[0]['id']


def context_window_for(model: str) -> int:
    for prefix, window in CONTEXT_WINDOWS:
        if model.startswith(prefix):
            return window
    return FALLBACK_CONTEXT_WINDOW


def completed_events(log_path: Path) -> list[tuple[float, str]]:
    events = []
    if not log_path.exists():
        return events
    for line in log_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get('event') == 'completed' and d.get('market_id'):
            ts = d['ts']
            if ts.endswith('Z'):
                ts = ts[:-1] + '+00:00'
            events.append((datetime.fromisoformat(ts).timestamp() * 1000, d['market_id']))
    return events


def cmd_token_burn(args) -> int:
    raise SystemExit("ZeroClaw 0.8.4 does not store per-run token usage in cron history")
    cron_dir = Path(args.cron_dir)
    job_id = args.job_id or resolve_fifo_job_id(cron_dir)
    runs_path = cron_dir / 'runs' / f'{job_id}.jsonl'
    runs = []
    if runs_path.exists():
        records = []
        for line in runs_path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        runs = [d for d in records if d.get('action') == 'finished'][-args.runs:][::-1]
    else:
        try:
            result = subprocess.run(
                ['openclaw', 'cron', 'runs', '--id', job_id, '--limit', str(args.runs)],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            data = json.loads(result.stdout)
            runs = [d for d in data.get('entries', []) if d.get('action') == 'finished']
        except (FileNotFoundError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
            raise SystemExit(
                f'run log not found: {runs_path}; '
                f'could not query current cron run history: {exc}'
            ) from exc
    if not runs:
        print('no finished runs found')
        return 1

    completions = completed_events(Path(args.log))
    header = ('finished', 'market_id', 'status', 'model', 'input', 'output', 'total', 'ctx%')
    rows = []
    totals = {'input': 0, 'output': 0, 'total': 0}
    for run in runs:
        usage = run.get('usage', {})
        start = run.get('runAtMs', 0)
        end = run.get('ts', start)
        market_ids = [t for ms, t in completions if start <= ms <= end]
        model = run.get('model', '?')
        window = args.context_window or context_window_for(model)
        inp = usage.get('input_tokens', 0)
        out = usage.get('output_tokens', 0)
        tot = usage.get('total_tokens', 0)
        totals['input'] += inp
        totals['output'] += out
        totals['total'] += tot
        rows.append((
            datetime.fromtimestamp(end / 1000).astimezone().strftime('%Y-%m-%d %H:%M'),
            ','.join(market_ids) or '-',
            run.get('status', '?'),
            model,
            f'{inp:,}',
            f'{out:,}',
            f'{tot:,}',
            f'{100 * inp / window:.0f}%',
        ))
    rows.append(('TOTAL', '', '', '', f"{totals['input']:,}", f"{totals['output']:,}", f"{totals['total']:,}", ''))

    widths = [max(len(header[i]), *(len(r[i]) for r in rows)) for i in range(len(header))]
    def fmt(row):
        cells = [row[i].ljust(widths[i]) if i < 4 else row[i].rjust(widths[i]) for i in range(len(row))]
        return '  '.join(cells).rstrip()
    print(fmt(header))
    print(fmt(tuple('-' * w for w in widths)))
    for row in rows[:-1]:
        print(fmt(row))
    print(fmt(tuple('-' * w for w in widths)))
    print(fmt(rows[-1]))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description='Manage the market analysis FIFO queue')
    p.add_argument('--queue', default=str(DEFAULT_QUEUE))
    p.add_argument('--log', default=str(DEFAULT_LOG))
    sub = p.add_subparsers(dest='cmd', required=True)

    add = sub.add_parser('add')
    add.add_argument('market_ids', nargs='+')
    add.add_argument('--allow-duplicates', action='store_false', dest='unique', help='append even if market_id is already queued')
    add.set_defaults(func=cmd_add, unique=True)

    peek = sub.add_parser('peek')
    peek.set_defaults(func=cmd_peek)

    ls = sub.add_parser('list')
    ls.set_defaults(func=cmd_list)

    done = sub.add_parser('complete-first')
    done.add_argument('market_id')
    done.set_defaults(func=cmd_complete_first)

    estimate = sub.add_parser('estimate', help='Estimate time to drain the queue at the worker cadence')
    estimate.add_argument('--hours-per-run', type=float, default=DEFAULT_HOURS_PER_RUN,
                          help=f'Hours per completed market_id (default: {DEFAULT_HOURS_PER_RUN:g}, matching the cron cadence)')
    estimate.add_argument('--now', help='ISO timestamp to estimate from; default: current local time')
    estimate.set_defaults(func=cmd_estimate)

    burn = sub.add_parser('token-burn', help='Show token usage for recent FIFO worker cron runs')
    burn.add_argument('-n', '--runs', type=int, default=10, help='Number of most recent runs to show (default: 10)')
    burn.add_argument('--cron-dir', default=str(DEFAULT_CRON_DIR), help='OpenClaw cron directory (default: %(default)s)')
    burn.add_argument('--job-id', help='Cron job id; default: the cron job whose name contains both "market" and "fifo"')
    burn.add_argument('--context-window', type=int,
                      help='Context window size in tokens; default: inferred from the run\'s model name')
    burn.set_defaults(func=cmd_token_burn)

    args = p.parse_args()
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
