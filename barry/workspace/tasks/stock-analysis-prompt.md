Analyze `{{TICKER}}` using the `stock-analysis` skill. Process only this ticker.

Only after the analysis succeeds and the stock-doc has been checked, remove it from the FIFO queue:

```bash
python3 skills/stock-queue/scripts/stock_queue.py complete-first {{TICKER}}
```

If blocked or the document check fails, leave `{{TICKER}}` queued and report the blocker.
