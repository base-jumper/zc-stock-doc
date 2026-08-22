---
name: "market-queue"
description: "Replace malformed helper with clean generated script."
---

# Market Queue

Manage the plain-text FIFO queue for scheduled market-analysis jobs.

## Locations

- Queue: `state/market-analysis-fifo-queue.txt`
- Audit log: `state/market-analysis-fifo-queue.log.jsonl`
- Helper: `skills/market-queue/scripts/market_queue.py`
- Worker prompt template: `tasks/market-analysis-prompt.md`

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

## Worker dispatch

The shell cron worker runs every three hours. It pipes the queue head into the worker prompt
template and schedules a one-shot Barry agent job only when a market ID is present:

```bash
market_queue peek | prompt-from-template --agent barry tasks/market-analysis-prompt.md
```

The template uses `{{TICKER}}`. The `market-analysis` skill owns the market-doc
documentation workflow; the template owns FIFO completion and worker guardrails.

The worker must analyze exactly the supplied market ID, validate the saved market-doc, and only then remove the head:

```bash
python3 skills/market-queue/scripts/market_queue.py complete-first MARKET_ID
```

If blocked, leave the market in place and report the blocker.
