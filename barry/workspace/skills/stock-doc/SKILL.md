---
name: stock-doc
description: Maintain durable stock research documents and views. Use when asked to show stored stock notes, rank stocks by score, list latest/recently updated docs, list watched stocks, list stocks evaluated by strategy, pick which stock to focus research effort on, update/create stock docs, or invokes /stock-doc-show, /stock-doc-rank, /stock-doc-latest, /stock-doc-watch, /stock-doc-list-strategy, /stock_doc list-strategy, or /stock-doc-focus.
---

# Stock Doc

Maintain living stock research notes under `investment/stock-docs`.

This skill defines a common file name and format, metadata, and a set of tools for working with the metadata. The actual contents of the document itself is produced separately with the stock-analysis skill. 

## Core rules

- Store one Markdown file per ticker: `<TICKER>.md`; keep exchange suffixes (`RKN.AX`, `SRG.AX`, `GOOG`).
- Keep each file as the current view only. Remove stale points instead of preserving an in-file history; git records history.
- Always preserve and update front matter.
- Use the bundled script for list/rank/focus commands instead of hand-parsing files.
- If creating or substantively updating research content, use the `stock-analysis` skill if available; it defines the body sections and standards.
- Include sources/citations where possible. Be explicit about uncertainty and source quality. Distinguish facts from interpretation.

## Front matter

Each stock doc must start with:

```yaml
---
ticker: TICKER
company: Company Name
watching: true
last-updated: YYYY-MM-DD
updated-by: Nipa
# Best-fit strategy this doc is primarily framed under (the stock-analysis skill picks it). When
# several strategies are scored, set this to the best-fit one; all scored strategies appear under
# `strategies:` below, and this must name one of them.
analysis-strategy: rule-breakers
# Per-trait scores for strategy evaluation (optional; added when scored). Keyed by trait id;
# see the stock-analysis skill. Strategies share these scores and differ only in their floors.
traits:
  right-place-and-time:  {score: 0.0, confidence: 0.0}
  # … one line per trait the strategy requires …
# Normalized strategy results, written by company_score.py (do not hand-edit; re-run the scorer
# instead). One entry per scored strategy; both numbers are on a comparable [0, 1] underlying
# trait-quality scale, so they can be compared across strategies. The raw floor-adjusted aggregates
# are not stored.
strategies:
  rule-breakers:
    score:      0.0
    confidence: 0.0
# ROI valuation inputs (optional; added when the strategy has a `valuation:` method). Keyed by method
# id, like traits — the stock-analysis skill generates these. Hand-tweakable; re-run the method script.
valuation:
  exit-multiple:
    price: 0.0
    years: 5
    metric: Earnings # Earnings or FCF; must match `fundamental` and `exit-multiple`
    fundamental: 0.0 # best estimate for TODAY's per-share fundamental, not trailing or forward
    growth: 0.0
    exit-multiple: 0.0
    # … the method's inputs; see references/valuation/<method>.md …
    # Written by the method's script (do not hand-edit; re-run the script instead):
    roi: 0.0          # annualized ROI
    date: 2026-06-21  # the run's as-of date — used to judge staleness
# Overall ranking scores (0–1). qv_score and cqv_score are written by overall_score.py from the
# chosen strategy's score/confidence and the chosen valuation's roi (do not hand-edit; re-run it).
# agent_score is the agent's valuation-aware judgement call — agent-owned, set by hand.
overall:
  qv_score:    0.0   # quality × value — where to focus research
  cqv_score:   0.0   # confidence-adjusted — where to allocate dollars
  agent_score: 0.0   # valuation-aware judgement call (was the old 0–10 `score`, rescaled to 0–1)
---
```

- `overall` holds the three 0–1 ranking scores (see the stock-analysis
  [overall-score reference](../stock-analysis/references/overall-score.md)). `qv_score` (quality ×
  value) and `cqv_score` (confidence-adjusted) are computed by `overall_score.py`; `agent_score` is
  the agent's valuation-aware judgement call — a separate human judgement, **not** a strategy score,
  and agent-owned (set by hand). `rank` sorts on one of these (default `cqv_score`).
- `analysis-strategy` names the best-fit strategy this doc is primarily framed under, and must be
  one of the keys in `strategies:`.
- `traits` and the `strategies:` map are produced by the stock-analysis scoring workflow (0–1,
  quality-only). `traits` holds the per-trait `{score, confidence}` inputs; `strategies:` holds, per
  scored strategy, the **normalized** `score` and `confidence` — the strategy-specific floor-adjusted
  aggregates converted back onto a comparable underlying trait-quality scale, so entries can be
  compared across strategies. A doc may carry several strategies side by side. The raw floor-adjusted
  aggregates are not stored.
- `valuation` is produced by the stock-analysis ROI workflow: the `valuation.<method>` block holds a
  method's inputs (hand-tweakable), and the method's script writes back the annualized ROI as a `roi`
  child and the run's as-of `date` (which, against today and the `price` used, flags a stale ROI).
  They appear only on docs scored under a strategy that names a `valuation:` method. For
  `exit-multiple`, include `metric: Earnings` or `metric: FCF` and use a best-estimate current
  per-share `fundamental`, not a raw trailing or forward-only figure.
- Set `watching: false` for archived/non-active docs.

## Commands

Use:

```bash
skills/stock-doc/scripts/stock_doc.py <command>
```

### `/stock-doc-show <TICKER>`

Run `stock_doc.py show <TICKER>`, then answer with the stored note or a concise summary if Nick did not ask for the full file. Legacy `/stockinfo <TICKER>` maps to this unless Nick asks for fresh research.

### `/stock-doc-rank <N>`

Run `stock_doc.py rank [N] [--by cqv|qv|agent]`. Returns a headed table: position, ticker, winning
strategy, all three scores (qv, cqv, agent), age since `last-updated` as a duration in days, and
company. `--by` selects which `overall` score orders the rows — `cqv` (default, where to allocate
dollars), `qv` (where to research), or `agent` (the agent's judgement). Docs missing the `--by`
score are omitted. If `N` is omitted, list all such docs.

### `/stock-doc-latest [N]`

Run `stock_doc.py latest [N]`. Return the most recently updated docs first; default `N` is 10. Include
ticker, `last-updated`, winning strategy, rank on the QV scoreboard, rank on the CQV scoreboard, rank
on the agent scoreboard, and company.

### `/stock-doc-watch`

Run `stock_doc.py watch`. Return watched tickers with last updated date and company.

### `/stock-doc-focus [N]`

Run `stock_doc.py focus [N] [--tau DAYS] [--wq W] [--wc W] [--ws W]`. Ranks watched docs by
**research-focus priority** — where extra analysis effort is most worthwhile — and prints ticker,
priority, `qv`, `conf`, `age` (days since last update), and company, highest first. Return the top
ticker(s); for interval use, act on the first row.

Priority multiplies three factors so a doc must earn all three to rank high:

```
priority = qv_score^wq · (1 − confidence)^wc · staleness^ws
staleness = 1 − exp(−days_since_update / τ)
```

`qv_score` is `overall.qv_score` (quality×value). `confidence` is the chosen strategy's normalized
confidence (`strategies[analysis-strategy].confidence`), which is what `qv_score` is derived from; an
unscored doc counts as fully uncertain. `staleness` rises from 0 for a just-updated doc to ~0.63 at
`τ` days (default 60), so a freshly-updated or high-confidence or low-qv doc drops out sharply. The
exponents `wq`/`wc`/`ws` (default 1.0) tune each factor's pull; set one to 0 to disable it. This is
distinct from `rank --by qv`, which orders on qv alone and ignores confidence and staleness.

### `/stock-doc-list-strategy <STRATEGY>` / `/stock_doc list-strategy <STRATEGY>`

Run `stock_doc.py list-strategy <STRATEGY>`. Return companies evaluated with that strategy, with ticker, normalized strategy score, normalized confidence, strategy ROI prediction, and company. The script reads the per-strategy entry from the `strategies:` map and sorts by normalized score descending.

## Updating docs

For a new or refreshed stock doc:

1. Read the existing stock doc first if it exists.
2. Read the `Watch` section before researching; use it to focus the update.
3. Use current sources where facts, prices, filings, or valuation matter.
4. Replace stale data and stale interpretations.
5. Keep the file concise and decision-useful.
6. Update front matter: `last-updated`, `updated-by`, `analysis-strategy`, `overall.agent_score`
   (your judgement call), and watch settings if needed. Re-run `overall_score.py` to refresh
   `overall.qv_score`/`overall.cqv_score`.

## Document body

This skill does not define the body. The sections and the standards for producing them live in the
[stock-analysis skill](../stock-analysis/SKILL.md) (*Documenting the analysis*). The body always
starts with an `# TICKER — Company Name` heading, immediately after the front matter.
