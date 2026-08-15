---
name: stock-announcements
description: Discover, review, and process new ASX announcements and SEC filings for AU/US companies with stock-docs, updating only materially affected living research documents. Use when asked to "process stock announcements", "check stock announcements", "review new company filings", monitor company announcements, or perform the scheduled announcement-processing run.
---

# Stock Announcements

Process primary-source company disclosures without spending model tokens scanning
market-wide feeds. Use the bundled poller for discovery and deduplication; use agent
judgement only for the small set of matched candidates.

## Discover candidates

Run from any directory:

```bash
stock_announcements poll --max-candidates 4 --max-age-days 30
```

Monitor every AU/US stock-doc. Do not impose a rank cap.

The poller fetches exchange/regulator-wide metadata, intersects it with the selected
stock-doc universe, applies deterministic materiality filters, and maintains a durable
pending queue. It returns the four highest-priority candidates per run, retains deferred
candidates for later runs, and automatically discards candidates more than 30 days old.
It does not download filing bodies, edit stock-docs, or mark candidates handled.

Recalculate priority from the current stock-doc on every poll:

```text
interest = max(qv_score, 0.05)
urgency = 0.25 + 0.75 × (1 − exp(−filing_age_days / 10))
priority = interest × urgency
```

Treat a missing QV as the `0.05` interest floor. Rank by priority descending, then
filing age descending, ticker, and event ID. This lets older medium-QV filings overtake
newer ones while low-interest filings can expire during sustained overload. Use the
poll output's `priority`, `qv_score`, `interest_score`, `filing_age_days`, and `urgency`
fields to audit each selection.

- If `candidate_count` is zero, do no research.
- Never review more than the returned batch of four candidates in one invocation.
- Treat a non-empty `warnings` array as a source or coverage problem. Do not interpret
  a failed source as having no announcements.

## Review candidates

Group the returned candidates by ticker and process all candidates for one ticker
together.

1. Read the existing stock-doc and its `Watch` section.
2. Open each primary-source `url` and read the actual announcement or filing. Do not
   update from a headline, form type, search snippet, or generated summary alone.
3. Decide whether the contents materially change the current view: thesis, risks,
   positives, management assessment, financial or operating facts, valuation inputs,
   trait scores, confidence, or Watch items.
4. Leave the stock-doc untouched when a disclosure is immaterial or administrative.
5. For a material change, use the `stock-doc` and `stock-analysis` skills. Update the
   document as a living current view, replace stale content in place, and do not append
   a dated news log. Refresh affected scoring and valuation outputs, set
   `last-updated` to today, and set `updated-by: Nipa`.
6. Directly inspect the finished stock-doc before acknowledging its candidates.

Edit and re-score a ticker at most once per run.

## Acknowledge reviewed candidates

Run:

```bash
stock_announcements ack <EVENT_ID> [<EVENT_ID> ...]
```

Acknowledge an immaterial candidate after reviewing its source. Acknowledge a material
candidate only after the required stock-doc update succeeds and is verified. Never
acknowledge a candidate whose source could not be reviewed or whose update failed; it
must remain pending for the next run.

## Report

For an interactive request, report tickers reviewed, stock-docs updated, disclosures
judged immaterial, and any pending failures. For a scheduled run, remain silent when
nothing material changed and there are no warnings; surface blockers only in cron
output.

The deterministic implementation is
[`scripts/stock_announcements.py`](scripts/stock_announcements.py). Run its tests with
`test_stock_announcements`.
