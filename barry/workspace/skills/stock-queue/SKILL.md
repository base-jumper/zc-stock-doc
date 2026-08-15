---
name: stock-queue
description: Manage Nick's FIFO stock analysis queue. Use when Nick asks to queue/enqueue/add a ticker for stock analysis (e.g. "queue WDS.AX"), list/show the stock queue, estimate how long the queue will take to drain, peek the next ticker, remove/complete the first queued ticker, or asks about the stock-analysis FIFO queue location or worker.
---

# Stock Queue

Use this skill to manage Nick's plain-text FIFO queue for stock-analysis jobs.

## Locations

- Queue file: `tasks/stock-analysis-fifo-queue.txt`
- Audit log: `tasks/stock-analysis-fifo-queue.log.jsonl`
- Helper script: `skills/stock-queue/scripts/stock_queue.py`
- Worker prompt: `tasks/stock-analysis-fifo-worker.md`

The queue is one ticker per line. The first non-empty line is the next ticker.

## Queue a ticker

For requests like “queue WDS.AX”, append the ticker to the queue with the helper script:

```bash
python3 skills/stock-queue/scripts/stock_queue.py add WDS.AX
```

- Normalize tickers to uppercase.
- By default, the helper avoids duplicate tickers already waiting in the queue.
- To intentionally allow duplicates, pass `--allow-duplicates`.
- Reply with the ticker queued and its position if useful. To see positions, run `list` after adding.

## Inspect the queue

```bash
python3 skills/stock-queue/scripts/stock_queue.py list
python3 skills/stock-queue/scripts/stock_queue.py peek
```

## Estimate queue drain time

```bash
python3 skills/stock-queue/scripts/stock_queue.py estimate
```

The estimate uses the worker cadence: one completed ticker every 3 hours by default. Override if the
cron frequency changes:

```bash
python3 skills/stock-queue/scripts/stock_queue.py estimate --hours-per-run 2
```

Return queue length, cadence, total estimated time, estimated empty timestamp, next ticker, and last
ticker. This is a throughput estimate only: blocked analyses remain in the queue and will extend the
actual completion time.

## Token usage of worker runs

ZeroClaw 0.8.4 does not store per-run token counts in cron history, so the migrated `token-burn` command exits with an explicit unsupported-version message. Queue operations and the scheduled worker are unaffected.

## Worker behavior

A cron job runs every 3 hours and follows `tasks/stock-analysis-fifo-worker.md`.

The worker must:

1. Use the `stock-analysis` and `stock-doc` skills for the research/update work.
2. Analyze exactly one ticker per run: the first line in the FIFO queue.
3. Not remove the ticker until the stock doc is updated and verified.
4. Remove only the first line using:

```bash
python3 skills/stock-queue/scripts/stock_queue.py complete-first TICKER
```

If blocked, leave the ticker in the queue and report the blocker.
