---
name: stock-update
description: Refresh an existing stock-doc for a supplied ticker by starting from its Watch items, checking company announcements and current evidence, choosing a minimal, targeted, or full re-analysis, and rerunning valuation and scores. Use when asked to update, refresh, revisit, or perform the scheduled update of one stock already covered in investment/stock-docs.
---

# Stock Update

Update one existing stock-doc as a living current view. The caller supplies the ticker; ticker
selection is outside this workflow. Automation may use `stock_focus` upstream to choose a ticker.

## Load the governing methods

Before editing, read:

- [the stock-doc skill](../stock-doc/SKILL.md) for the file contract and front matter;
- [the stock-analysis skill](../stock-analysis/SKILL.md) for research, strategy selection, traits,
  valuation, scoring, body sections, and sourcing; and
- [the stock-announcements skill](../stock-announcements/SKILL.md) for disclosure review and
  acknowledgement rules.

Treat those skills as the source of truth. This skill defines only how to triage and execute an
update.

## 1. Establish the stored view

1. Normalize the supplied ticker and open `investment/stock-docs/<TICKER>.md`. If it does not
   exist, stop and ask for a fresh `stock-analysis`; do not silently create a partial stock-doc.
2. Read the entire document before researching. Read **Watch** especially closely.
3. Extract the claims, dates, valuation inputs, trait evidence, uncertainties, and concrete Watch
   questions that could be confirmed, refuted, or made stale.
4. Preserve the existing file until enough evidence has been gathered to make a coherent update.

## 2. Gather only decision-relevant new evidence

Check disclosures first for tickers supported by the announcement tool (ASX `.AX` and US tickers):

```bash
stock_announcements ticker <TICKER>
```

Use `--force-refresh` when explicitly requested or when a fresh discovery check is necessary. Treat
any warning or failed refresh as incomplete coverage, never as evidence that no announcement exists.
Open and read each candidate's primary-source document; do not update from its headline, form type,
search snippet, or generated summary.

For unsupported exchanges, the announcement tool provides no coverage. Check the issuer's investor
relations site and the primary exchange announcement feed instead, and surface the coverage gap if
the run is expected to report blockers.

Then check:

- every actionable Watch item against the most relevant primary source;
- the current share price and the effective date/currency of the quote;
- filings, results, presentations, guidance, capital actions, or major news published since the
  stored view; and
- inputs whose freshness affects the valuation, including the current per-share fundamental,
  diluted shares, net debt, distributions, growth path, catalyst odds, or market-doc estimates as
  applicable.

Prefer source-led, targeted research. Do not broaden a small update into a new deep dive unless the
evidence calls the stored thesis or category into question.

## 3. Choose the update depth

Use the smallest scope that leaves the document current and internally consistent.

### Minimal update

Use when disclosures are immaterial, price movement is modest, and Watch evidence does not change
the thesis. Recheck the Watch items, refresh the valuation and overall scores, update time-sensitive
facts or source as-of dates where needed, and leave sound analysis intact. Do not add filler merely
to demonstrate activity.

### Targeted update

Use when new evidence affects identifiable facts, Watch items, risks, positives, valuation inputs,
or traits without challenging the business classification. Replace the affected passages in place,
update the corresponding trait scores and confidence, and refresh every derived score.

### Full re-analysis

Re-enter the complete `stock-analysis` workflow when new evidence could change the disqualifier
gate, business model, earnings profile, balance-sheet risk, durable growth or advantage, management
or control, valuation-method applicability, or winning strategy. Also do so when the current
strategy no longer appears to fit or another strategy could plausibly overtake it. Rerun leaderboard
mode and apply its stopping rule rather than switching categories by intuition.

## 4. Refresh valuation on every run

Always obtain a current quote and rerun the canonical valuation, even when nothing else is material.
Read the applicable method under
[`stock-analysis/references/valuation/`](../stock-analysis/references/valuation/) before changing
its inputs.

1. Update `price` and any other inputs made stale by the latest evidence. Keep price, per-share
   fundamentals, shares, currency, and corporate-action basis consistent.
2. Run each applicable component valuation script. For `weighted-average`, run every component named
   in `weights` first, then run `weighted_average_valuation.py` last.
3. Ensure the script writes the new `roi`, `date`, and any method-specific derived fields.
4. Update the **Valuation** section so its assumptions, result, attribution, and
   `overall.agent_score` judgement agree with the front matter.

Do not preserve an inapplicable method merely for continuity. If applicability changes, follow the
strategy and valuation-selection rules in `stock-analysis`.

## 5. Recompute scoring

- If any trait score or confidence changes, run:

  ```bash
  skills/stock-analysis/scripts/company_score.py <TICKER>
  ```

- If category fit may have changed, use `company_score.py <TICKER> --leaderboard`, complete the
  strategy-selection workflow, then run the committing scorer and update `analysis-strategy` and
  any justified `chosen` overrides.
- After valuation and strategy scoring are current, always run:

  ```bash
  skills/stock-analysis/scripts/overall_score.py <TICKER>
  ```

- Reconsider `overall.agent_score`; change it only when the valuation-aware judgement changes.

Never hand-calculate or directly edit script-owned strategy, ROI, QV, or CQV outputs.

## 6. Reconcile the document

Edit the stock-doc as a current view, not an update log:

- replace stale facts, interpretations, assumptions, and citations in place;
- keep unaffected high-quality analysis;
- make the body and front-matter trait scores agree;
- resolve or remove completed Watch items, rewrite partially answered ones, and add new specific
  triggers or evidence gaps;
- keep unresolved low-confidence traits actionable under the `stock-analysis` firm-up rule; and
- retain the canonical body order and concise, decision-useful style.

After all substantive edits and scripts succeed, set `last-updated` to today's date and
`updated-by: Barry`.

## 7. Verify, then acknowledge announcements

Read the finished file end to end. Confirm:

- strategy, traits, valuation, overall scores, prose, dates, and sources are mutually consistent;
- all valuation components and the final method were rerun in dependency order;
- Watch reflects the remaining forward questions rather than completed work; and
- no stale conclusion survived elsewhere in the document.

For each announcement candidate whose primary source was read, acknowledge an immaterial event after
review and a material event only after the updated stock-doc passes verification:

```bash
stock_announcements ack <EVENT_ID> [<EVENT_ID> ...]
```

Never acknowledge an inaccessible source, unresolved disclosure, failed update, or unverified file;
leave it pending for retry. If the update fails, keep the existing document intact where possible and
report the blocker according to the caller's interactive or scheduled-run policy.
