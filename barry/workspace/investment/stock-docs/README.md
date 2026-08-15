# Stock Docs
This folder contains the latest notes for stocks that have been researched. These are living documents that are updated each time a stock is reviewed. Each file just contains a concise summary of our current view of the stock. To see how the view has evolved over time, refer to the git commit history.

## Skills
* `/stock-doc-show <TICKER>` pulls up the notes for the ticker. Also activated by asking to see our notes/docs/research for a stock.
* `/stock-doc-rank <N>` lists our current top `N` stocks by overall score, showing the ticker and score for each. Ranks by `cqv_score` (dollar-allocation priority) by default; pass `--by qv` or `--by agent` to rank by the research-priority or judgement-call score instead. `N` can be omitted to list all stocks. Also activated by asking something like "list our current top 10 stocks".
* `/stock-doc-watch` lists which stocks we are actively watching. Also activated by asking "which stocks are we watching?".
* Legacy `/stockinfo <TICKER>` maps to `/stock-doc-show <TICKER>` unless fresh research is requested.


## Implementation Notes
> Everything from this point onwards was used for initially creating the associated SKILLS and TASKS. Generally there is no need to re-read it.

Each time we research a stock we record findings and conclusions in the stock note. For new stocks that don't have an existing stock note, a deep-dive is done on the first pass. The template further down in this file is followed to generate the stock note. For subsequent passes where a stock note already exists, we first read our existing notes on the stock. The note could provide guidance on where to focus subsequent research so we can do a more targeted investigation. The stock note is then updated with any new findings. 

The stock note should always reflect our most up-to-date view on a stock. We do not need to maintain a record of prior views. A point in a stock note that has become irrelevant should be removed. Any data that is out of date should be replaced with new current data. We should perform house-keeping on teh stock note on every pass to ensure it remains concise, tidy and current. Stock notes are version controlled in git. Let git record the history rather than the file contents itself.

## Stock doc front-matter
Stocks are documented in markdown, with front-matter at the top for programmatic access to structured data. The front-matter is used for the skills. This allows the skills to be implemented programmatically so they can be run efficiently on a regular basis.

The front-matter should contain at least the following fields:
* ticker: stock ticker (eg. RPL.AX, GOOG, KKR)
* company: company name
* watching: true if we want to actively watch this stock.
* last-updated: last time this stock-doc was updated
* updated-by: who last performed the stock-doc update
* overall: the three 0–1 ranking scores — `qv_score` (quality×value, research priority) and `cqv_score` (confidence-adjusted, dollar-allocation priority) computed by `overall_score.py`, plus `agent_score`, the agent's valuation-aware judgement call (set by hand). See the stock-analysis overall-score reference.

## Schedules
A twice-daily cron task refreshes one watched stock per run. It runs `skills/stock-doc/scripts/stock_doc.py focus 1` to choose the stock where more research is currently most worthwhile, then reads that doc's `Watch` section first and updates the living document in place. It should replace stale data and interpretations rather than appending update logs, re-score the stock, and update `last-updated`.

## File Naming
The stock note for each ticker is stored in a separate file. Keep exchange suffixes in the names where useful. Some examples: `RPL.AX`, `HMC.AX`, `GOOG`, `KKR`

## Style
* Include sources and citations wherever possible (ideally as a link).
* Be explicit about uncertainty and source quality.
* Distinguish facts from interpretation.
* Prefer concise, decision-useful summaries over data dumps.
* You can assume that all information will be reviewed with a financial professional before acting on it. You do not need to provide cautionary notes or disclaimers.

## Contents
The content of the stock doc should include the following sections.

### Business Overview
A description of the business and how it generates it's revenue. The goal is to provide a concise overview of how the company makes its money and what are the most important drivers of profit. For big businesses with lots of moving parts just focus on the most important aspects (eg. focus on the segments that deliver 80% of the revenue and ignore items contributing the remaining 20%). Keep it to less than a page.

### Overall
Our overall view on the stock. 

### Improvements
Notes on what would need to improve for this stock to achieve a perfect score.

### Portfolio fit
An assessment of how well this into our portfolio, taking current holdings into account.

### Thesis Connections
Notes on any connections to an investment thesis (FIT).

### Key Positives
The things we like.

### Key Risks
The things we need to keep an eye on.

### Valuation
Note down any information or calculations that have been used when assessing current valuation or future earnings.

### Watch
A list of anything we need to keep tabs on. These will be things that could affect our rating of the stock. They could also be areas we want to research deeper at the next opportunity. Scheduled update run will read this section first before performing any research.
