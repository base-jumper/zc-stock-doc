Refresh the stock-doc for `{{TICKER}}` using the `stock-update` skill. Process only this ticker.

The stock-update skill owns ticker handling, research triage, valuation refresh, scoring, and
document reconciliation. Update `investment/stock-docs/{{TICKER}}.md` as a living current view and
report the update depth used, the refreshed valuation ROI, and any blockers.

If the update cannot succeed, report the blocker and leave the stock-doc unchanged.