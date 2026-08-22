#!/usr/bin/env python3
"""FIFO stock ticker queue helper for Barry/ZeroClaw."""
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
DEFAULT_QUEUE = WORKSPACE / 'state' / 'stock-analysis-fifo-queue.txt'
DEFAULT_LOG = WORKSPACE / 'state' / 'stock-analysis-fifo-queue.log.jsonl'
DEFAULT_HOURS_PER_RUN = 3.0
TICKER_RE = re.compile(r'^[A-Z0-9][A-Z0-9.\-]{0,15}$')

DEFAULT_CRON_DIR = Path.home() / '.zeroclaw' / 'data' / 'cron'
WORKER_JOB_RE = re.compile(r'^stock-analysis$', re.IGNORECASE)
# Max input context per model-name prefix, used to estimate context window use.
CONTEXT_WINDOWS = [
    ('gpt-5', 272_000),
    ('claude', 200_000),
]
FALLBACK_CONTEXT_WINDOW = 200_000


def normalize(ticker: str) -> str:
    t = ticker.strip().upper()
    if not TICKER_RE.match(t):
        raise SystemExit(f'invalid ticker: {ticker!r}')
    return t


def ensure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [ln.strip().upper() for ln in path.read_text().splitlines() if ln.strip()]


def log_event(log_path: Path, event: str, ticker: str | None = None, **extra) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'event': event,
        **({'ticker': ticker} if ticker else {}),
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
    tickers = [normalize(t) for t in args.tickers]
    q = Path(args.queue)
    log = Path(args.log)
    with with_lock(q) as f:
        existing = [ln.strip().upper() for ln in f.read().splitlines() if ln.strip()]
        additions = []
        for t in tickers:
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
    print('\n'.join(additions) if additions else 'no new tickers queued')
    return 0


def cmd_peek(args) -> int:
    lines = read_lines(Path(args.queue))
    if lines:
        print(lines[0])
        return 0
    return 1


def cmd_list(args) -> int:
    lines = read_lines(Path(args.queue))
    for i, ticker in enumerate(lines, 1):
        print(f'{i}. {ticker}')
    if not lines:
        print('(empty)')
    return 0


def cmd_complete_first(args) -> int:
    ticker = normalize(args.ticker)
    q = Path(args.queue)
    log = Path(args.log)
    with with_lock(q) as f:
        lines = [ln.strip().upper() for ln in f.read().splitlines() if ln.strip()]
        if not lines:
            raise SystemExit('queue is empty')
        if lines[0] != ticker:
            raise SystemExit(f'first queued ticker is {lines[0]}, not {ticker}; refusing to remove')
        remaining = lines[1:]
        f.seek(0)
        f.truncate()
        if remaining:
            f.write('\n'.join(remaining) + '\n')
    log_event(log, 'completed', ticker)
    print(f'completed and removed {ticker}')
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
    print(f'cadence=1 ticker every {format_duration(args.hours_per_run)}')
    print(f'total={format_duration(total_hours)}')
    print(f'estimated-empty-at={finish.isoformat(timespec="minutes")}')
    if count:
        print(f'next={lines[0]}')
        print(f'last={lines[-1]}')
    return 0


def resolve_worker_job_id(cron_dir: Path) -> str:
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
    matches = [j for j in jobs if WORKER_JOB_RE.search(j.get('name', ''))]
    if not matches:
        raise SystemExit(f'no stock-analysis cron job found via {source}')
    if len(matches) > 1:
        names = ', '.join(f"{j['id']} ({j['name']})" for j in matches)
        raise SystemExit(f'multiple stock FIFO cron jobs found, pass --job-id: {names}')
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
        if d.get('event') == 'completed' and d.get('ticker'):
            ts = d['ts']
            if ts.endswith('Z'):
                ts = ts[:-1] + '+00:00'
            events.append((datetime.fromisoformat(ts).timestamp() * 1000, d['ticker']))
    return events


def cmd_token_burn(args) -> int:
    raise SystemExit("ZeroClaw 0.8.4 does not store per-run token usage in cron history")
    cron_dir = Path(args.cron_dir)
    job_id = args.job_id or resolve_worker_job_id(cron_dir)
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
    header = ('finished', 'ticker', 'status', 'model', 'input', 'output', 'total', 'ctx%')
    rows = []
    totals = {'input': 0, 'output': 0, 'total': 0}
    for run in runs:
        usage = run.get('usage', {})
        start = run.get('runAtMs', 0)
        end = run.get('ts', start)
        tickers = [t for ms, t in completions if start <= ms <= end]
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
            ','.join(tickers) or '-',
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
    p = argparse.ArgumentParser(description='Manage the stock analysis FIFO queue')
    p.add_argument('--queue', default=str(DEFAULT_QUEUE))
    p.add_argument('--log', default=str(DEFAULT_LOG))
    sub = p.add_subparsers(dest='cmd', required=True)

    add = sub.add_parser('add')
    add.add_argument('tickers', nargs='+')
    add.add_argument('--allow-duplicates', action='store_false', dest='unique', help='append even if ticker is already queued')
    add.set_defaults(func=cmd_add, unique=True)

    peek = sub.add_parser('peek')
    peek.set_defaults(func=cmd_peek)

    ls = sub.add_parser('list')
    ls.set_defaults(func=cmd_list)

    done = sub.add_parser('complete-first')
    done.add_argument('ticker')
    done.set_defaults(func=cmd_complete_first)

    estimate = sub.add_parser('estimate', help='Estimate time to drain the queue at the worker cadence')
    estimate.add_argument('--hours-per-run', type=float, default=DEFAULT_HOURS_PER_RUN,
                          help=f'Hours per completed ticker (default: {DEFAULT_HOURS_PER_RUN:g}, matching the cron cadence)')
    estimate.add_argument('--now', help='ISO timestamp to estimate from; default: current local time')
    estimate.set_defaults(func=cmd_estimate)

    burn = sub.add_parser('token-burn', help='Show token usage for recent FIFO worker cron runs')
    burn.add_argument('-n', '--runs', type=int, default=10, help='Number of most recent runs to show (default: 10)')
    burn.add_argument('--cron-dir', default=str(DEFAULT_CRON_DIR), help='OpenClaw cron directory (default: %(default)s)')
    burn.add_argument('--job-id', help='Cron job id; default: the cron job whose name contains both "stock" and "fifo"')
    burn.add_argument('--context-window', type=int,
                      help='Context window size in tokens; default: inferred from the run\'s model name')
    burn.set_defaults(func=cmd_token_burn)

    args = p.parse_args()
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
