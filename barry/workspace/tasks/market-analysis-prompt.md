Analyze market `{{TICKER}}` using the `market-analysis` skill. Process only this market; do not alter stock docs.

Only after the analysis succeeds and the market-doc has been validated, remove it from the FIFO queue:

```bash
python3 skills/market-queue/scripts/market_queue.py complete-first {{TICKER}}
```

If blocked or validation fails, leave `{{TICKER}}` queued and report the blocker.
