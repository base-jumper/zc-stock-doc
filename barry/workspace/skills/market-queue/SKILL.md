---
name: "market-queue"
description: "Replace malformed helper with clean generated script."
---

# Market Queue

Manage the plain-text FIFO queue for scheduled market-analysis jobs.

## Locations

- Queue: `tasks/market-analysis-fifo-queue.txt`
- Audit log: `tasks/market-analysis-fifo-queue.log.jsonl`
- Helper: `skills/market-queue/scripts/market_queue.py`
- Worker prompt: `tasks/market-analysis-fifo-worker.md`

Store one lowercase market ID per line. Treat the first non-empty line as next.

## Manage the queue

```bash
python3 skills/market-queue/scripts/market_queue.py add global-long-read-sequencing
python3 skills/market-queue/scripts/market_queue.py list
python3 skills/market-queue/scripts/market_queue.py peek
python3 skills/market-queue/scripts/market_queue.py estimate
```

Normalize IDs to lowercase kebab-case and reject invalid IDs. Avoid duplicates unless `--allow-duplicates` is explicit. The default drain estimate matches the three-hour worker cadence.

Inspect recent worker token usage with:

```bash
python3 skills/market-queue/scripts/market_queue.py token-burn -n 10
```

## Worker behavior

The cron worker runs every three hours and follows `tasks/market-analysis-fifo-worker.md`. It must use the `market-analysis` and `market-doc` skills, analyze exactly the first market, validate the saved market-doc, and only then remove the head:

```bash
python3 skills/market-queue/scripts/market_queue.py complete-first MARKET_ID
```

If blocked, leave the market in place and report the blocker.
