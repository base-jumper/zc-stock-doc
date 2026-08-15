Twice-daily focused stock-doc refresh

Run `skills/stock-doc/scripts/stock_doc.py focus 1`.

This prints the single watched stock where a refresh is most worthwhile, based on research-focus priority. If it prints no ticker, stop silently.

For the ticker printed:
1. Read `investment/stock-docs/<TICKER>.md` first.
2. Read the `Watch` section before researching. Use it to decide where to spend effort and what data/events need checking.
3. Follow the `stock-doc` and `stock-analysis` skill guidelines, but do **not** do a complete new analysis from scratch unless the existing document is unusable.
4. Check whether new material data is available since the stored view: filings, announcements, investor presentations, earnings updates, current quote/valuation inputs, major news, changed risks, changed positives, and watch-list items.
5. Refresh only what needs refreshing. The stock-doc is a living current-view document, not a log: replace stale facts, stale valuation assumptions, stale interpretations, and stale Watch items in place. Do not append a dated update section to the end.
6. Re-score the stock after the refresh:
   - Update any affected `traits`, `strategies`, and valuation inputs in front matter.
   - Re-run the relevant valuation script(s) if valuation inputs changed.
   - Re-run `skills/stock-analysis/scripts/overall_score.py <TICKER>` so `overall.qv_score` and `overall.cqv_score` are current.
   - Update `overall.agent_score` if the judgement call changed.
7. Update front matter: set `last-updated` to today's date and `updated-by: Nipa`.
8. Keep the doc concise, decision-useful, sourced where possible, and internally consistent.
9. Do not message Nick. The output of this task is the one updated stock-doc file only. If there is nothing material to update, still refresh the checked-as-of state where appropriate, update `last-updated`, and leave the file clean.

If research/update fails, leave the existing file intact where possible and do not send a message. Surface the blocker only in the cron run output.
