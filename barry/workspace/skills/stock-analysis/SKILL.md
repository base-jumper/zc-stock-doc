---
name: stock-analysis
description: Standards for researching a listed stock and producing the body of a stock-doc — strategy selection, trait scoring, ROI/valuation estimation, and the section-by-section write-up. Use when Nick asks for fresh stock research, a deep dive, valuation work, investment thesis assessment, or to estimate/update/refresh a stock's ROI, expected return, annualized return, or re-run a valuation method (exit-multiple, tam-capture, scenario-tam, weighted-average, asymmetric-payoff), or when stock-doc needs substantive content generation.
---

# Stock Analysis

How we research a listed stock and write up the findings. This skill owns the **methodology** and
the **body** of a stock-doc; the [stock-doc skill](../stock-doc/SKILL.md) owns the file name, the
front matter, and the tools for working with it. Produce the analysis here, then write it into the
stock-doc.

## Principles

- Prefer primary sources: company filings, investor presentations, earnings releases/transcripts,
  exchange announcements, and reputable data sources. See [references/sources.md](references/sources.md)
  for where we do and don't source information, ranked by trust.
- **Facts, not sentiment.** When reading any article, post, or report, deliberately discard the
  author's sentiment and keep only the hard information; we form our own conclusions from the facts
  rather than absorbing someone else's. This rule is spelled out in
  [references/sources.md](references/sources.md).
- Separate facts from interpretation.
- State uncertainty and source quality.
- Be concise and decision-useful — no data dumps.
- Do not add generic investment disclaimers unless Nick asks; assume notes will be reviewed with a
  financial professional before action.
- **Each stock-doc stands alone.** Analyze and write up the current company on its own merits, as if
  it were the only stock in the prompt. Do not carry over context from another company analyzed
  earlier in the same conversation — no cross-references, comparisons, or relative judgments like
  "a better X than TICKER". A reader opening this stock-doc has no knowledge of what else you looked
  at, and the doc must make complete sense to them. Compare only against the strategy's traits and
  floors, never against another stock you happened to run.

## Picking the strategy

Companies are scored against a **strategy** — a philosophy plus a set of traits, each with a floor.
Strategies live in [references/strategies/](references/strategies/).

The individual traits are defined, strategy-agnostically, in [references/traits/](references/traits/).
A trait's **score** is the same no matter which strategy reads it — strategies differ only in the
**floors** they assign and the subset of traits they use; the **same trait can be shared across
strategies** (cash-cow, for instance, reuses much of wonderful-and-fair's quality set and shares
[fundamental-stability](references/traits/fundamental-stability.md) with freeroll). The full set of
traits is the union across all strategies.

You do **not** pick the strategy upfront by judgement. You evaluate traits and let the scorer's
**leaderboard** categorize the company mechanically — the strategy whose traits the company best
satisfies wins. The one shortcut: **an explicit request wins.** If the prompt names a strategy —
*"analyze NVDA as a rule breaker"* — score that strategy's traits, commit it, and skip the contest.

Otherwise, run this loop (the mechanic — optimistic bounds, the ranking metric, and the stopping
rule — is documented in [references/scoring.md](references/scoring.md#picking-the-strategy-leaderboard-mode)):

1. **Read all trait rubrics and the strategies' floors upfront.** They are short, and knowing the
   full question set lets you gather evidence once instead of re-reading sources per trait.
2. **Comprehend the business, then score the free traits.** Do your initial pass over the primary
   sources, and immediately score *and document* every trait that falls out of it. Don't defer the
   easy ones; set confidence honestly (a trait read quickly off the overview earns lower confidence
   than one you dug into). A trait counts as evaluated only once it is written into `traits:`. On this
   same pass, screen the [disqualifiers](references/disqualifiers.md) (fraud, insolvency, hidden
   liabilities, value-leaking control, a business-model kill-shot) — they are universal, so check them
   once. If one fires, set the top-level `disqualified: true` and stop: the company is ineligible for
   every strategy.
3. **Consult the leaderboard to choose what to research next.** Run
   `company_score.py <TICKER> --leaderboard`. It ranks every strategy on optimistic bounds and names
   the **highest-leverage** unevaluated trait — the current leader's lowest-floor trait (to confirm
   or dethrone it). Research it, or a batch of traits sharing a source, and write the results in.
4. **Refine earlier traits as new sources surface.** Source-first research means you score some
   traits on partial information; revise score/confidence when *new evidence* warrants — not to nudge
   a preferred strategy over the line. The leaderboard always reflects the latest `traits:`.
5. **Stop when the verdict is decided** — i.e. the rank-1 strategy is fully evaluated, so no remaining
   optimism can change the order. If the runner-up's bound is within ε, resolve it to confirm a clear
   win versus a genuine dual-fit. In the clear-cut case (one obvious fit, the rest vetoed on their
   gate traits or disqualified), the leaderboard craters the losers in a call or two and the loop ends
   fast.

Then **record the result.** Make sure the top-level `disqualified` flag is set (`false` once you have
screened the gate and it is clear), then run the committing scorer (see *Scoring*) with no strategy
argument — it writes a normalized `{score, confidence}` under `strategies:` for **every strategy whose
trait set you completed**, and skips the rest, so the strategies you resolved (the winner, plus any
runner-up) are committed and the ones you ruled out on their optimistic bound are left out by design.
(If the company is disqualified, the scorer writes nothing.) Set `analysis-strategy:` to the winner (it
must name an entry in the map), and note in the write-up which strategies were ruled out and why. For a
genuine dual-fit, both are committed; make `analysis-strategy` the primary and frame the write-up around
it while acknowledging the other.

## Scoring

Each trait gets two independent scores, both 0–1 — a **Score** (how well the company meets the trait)
and a **Confidence** (how well-grounded that score is in evidence). Record `{score, confidence}` per
trait in the **stock-doc front matter**, under a `traits:` mapping keyed by trait id (see the
[stock-doc skill](../stock-doc/SKILL.md)). Use a low score with low confidence where evidence is thin
— never omit a trait the chosen strategy requires. Eligibility is handled separately from scoring by
the [disqualifier gate](references/disqualifiers.md), not by any trait.

See each trait file for its scoring bands and documentation checklist. The mechanics shared by every
strategy — the two axes, the floor transform → geometric-mean formula, normalization, the
leaderboard, and running [`company_score.py`](scripts/company_score.py) to compute and write the
aggregates — live once in [references/scoring.md](references/scoring.md). Each strategy doc adds only
what is specific to it: its floors and how to read the resulting bands.

## Estimating ROI

Alongside the quality score, every strategy estimates an **expected annualized ROI** — a forward
return you can rank ideas by. This works exactly like scoring, one level
removed: the **strategy** names a valuation method, the **stock-doc** holds that method's inputs, and
a **script** reads the inputs and writes the ROI back.

* Each strategy's front matter carries a `valuation:` field naming its method — wonderful-and-fair and cash-cow both use
  `exit-multiple` (grow owner-earnings/FCF to an exit multiple; wonderful-and-fair on a growth-carried
  return, cash-cow on an income-and-buyback-carried one), freeroll uses `asymmetric-payoff`
  (probability-weight the floor against fair value), and rule-breakers uses `weighted-average`, a
  meta-method that blends the lenses that apply to a given company (`tam-capture` terminal "it works"
  build from market-analysis's 10-year company-revenue estimate, `exit-multiple` bottom-up once it is
  profitable). A strategy without a `valuation:` field has no ROI method wired up yet — skip the ROI
  step for it.
* **TAM-capture has a market-doc prerequisite.** Follow the dependency workflow in the
  [tam-capture reference](references/valuation/tam-capture.md#applicability) before generating or
  running its inputs. Use a suitable existing market doc unchanged. If none exists, spawn a
  sub-agent to use the `market-analysis` skill to create and save one, wait for it to finish, then
  pass that document's reference into `valuation.tam-capture.market-doc`. Do not begin the stock's
  TAM-capture valuation while that dependency is missing.
* **Blended valuations** (`weighted-average`) name their components as the keys of a `weights` map and
  must run *after* them — evaluate each applicable component method first (skip any the company doesn't
  fit, per the method's *Applicability*), then run the meta-method to combine their ROIs. It reads the
  component `roi`s in place rather than restating them. Let a wide spread between components lower the
  strategy's confidence.
* The methods are documented in [references/valuation/](references/valuation/), one file per method,
  each with its own input contract and script. Read the method's file before generating inputs.
* During the analysis, **generate the method's inputs** into the stock-doc front matter under a
  `valuation:` block keyed by method id — the same way you produce per-trait `{score, confidence}`
  under `traits:`. Base each input on the evidence and state the basis in the **Valuation** body
  section below.
* Then **run the method's script** with `--stock-doc <TICKER>`. It reads the input block and writes
  two children back surgically: the annualized ROI as `roi` (e.g. `valuation.exit-multiple.roi`) and
  the run's as-of date as `date` (defaulting to today, or `--as-of YYYY-MM-DD`). You can hand-tweak an
  input and re-run to refresh both — nothing else is touched.

The stamped `date`, read against today and against the `price` the valuation used versus the current
quote, is how we judge whether a stored ROI is **stale** and due a refresh. A scheduled update run can
sort by it to find the valuations that have drifted furthest out of date.

The inputs are deliberately exposed and editable: the ROI is only as good as the assumptions
(growth path, exit multiple, holding period) fed in, so make them defensible and cite their source in
the write-up.

**The canonical strategy and ROI (`chosen`).** A borderline company may be scored under more than one
strategy and carry several valuation blocks, so the front matter records which pairing is canonical for
downstream ranking:

```yaml
chosen:
  strategy: rule-breakers       # optional — default: argmax over strategies.<s>.score * confidence
  valuation: weighted-average   # optional — default: the chosen strategy's named valuation method
```

Both keys are **optional and default-driven**: omit `chosen` entirely and ranking uses the strategy
with the highest `score * confidence` and that strategy's own valuation method. Set a key only to
**override** the default — e.g. to rank a company under a strategy other than its top-scoring one. To
prefer one component lens over another, don't override `valuation` to a bare component; adjust the
`weighted-average` weights instead, so the canonical ROI stays the blend.

**Refreshing ROI on its own.** If Nick just asks to update/refresh a stock's ROI (not a full
re-research), this is a lightweight step: read the doc's `valuation:` block, update any inputs that
have moved — most often the current `price`, but also growth, fair value, or the catalyst's
probability/window if the thesis has shifted — then re-run the method's script with `--stock-doc
<TICKER>` to rewrite `valuation.<method>.roi` and re-stamp `valuation.<method>.date`. Update the
Valuation section to match (assumptions, the new ROI, attribution). Then re-run the overall-score step
below, since the ROI feeds it.

## Overall scores

Once the chosen strategy is scored and its ROI written, fold them into the doc's headline `overall:`
scores — the comparable numbers we rank and prioritize on. Run
[`overall_score.py`](scripts/overall_score.py) with the ticker; it reads the chosen strategy's quality
`score`, its `confidence`, and the chosen valuation's `roi`, and writes back `overall.qv_score`
(quality × value — where to research) and `overall.cqv_score` (confidence-adjusted — where to allocate
dollars). The value-from-ROI map, the geometric-mean formulas, and how to read the scores live in
[references/overall-score.md](references/overall-score.md).

The third number, `overall.agent_score`, is **yours**: the valuation-aware judgement call (0–1) you
argue in the **Valuation** section. The script never touches it — set it by hand. It is confidence-blind
(rate the visible merits, not how much evidence backs them), so a large gap between it and `qv_score`
is the signal that the methodology — or the judgement — needs a second look.

## Documenting the analysis

Write the findings into the stock-doc using these sections, in order. (The stock-doc skill owns the
file name and front matter; everything below is the body.)

### Business Overview

A description of the business and how it generates its revenue. The goal is a concise overview of
how the company makes its money and the most important drivers of profit. For big businesses with
many moving parts, focus on the most important aspects (e.g. the segments that deliver ~80% of
revenue; ignore the long tail). Keep it to less than a page.

### Trait Assessment

Write this in depth for the **winning strategy's** traits — one `###` subsection each. Each should:

* State the trait's **score** and **confidence**.
* Cover the **Documentation** checklist from that trait's file (see
  [references/traits/](references/traits/)) — the specific evidence behind the score.
* Distinguish facts from interpretation, and cite sources.
* For any trait whose **confidence is 0.8 or below**, note what would firm it up — a specific named
  source, or that it is irreducible for now and the future event that would resolve it. This is the
  [firm-up rule](references/scoring.md#documenting-low-confidence-the-firm-up-rule); cheap-to-obtain
  sources also go in **Watch**.

This is what makes a front-matter score auditable: the next update should be able to read here *why*
a trait scored what it did. Every trait you evaluated still carries its `{score, confidence}` in the
front matter (the full audit trail); this section just covers the winner's set in prose.

Close with a brief **why the other strategies lost** — a sentence or two each naming the trait(s)
that ruled them out (the cratered gate, or where the leaderboard left them). For a genuine dual-fit,
cover the runner-up's traits in depth too and explain why the primary was chosen.

### Overall

Our overall view on the stock. Call out the main strengths, as well as the main detractors that
prevent it from getting a perfect score.

### Valuation

Information and calculations used when assessing current valuation or future earnings. This is the
basis for the stock-doc's `overall.agent_score` (a valuation-aware judgement call on a 0–1 scale; see
*Overall scores*), so make the reasoning explicit. If the strategy has a `valuation:` method (see
*Estimating ROI*), state the inputs you fed it and their basis, the resulting annualized ROI, and the
return attribution — so the next update can re-run with refreshed numbers.

### Thesis Connections

Notes on any connections to an investment thesis (FIT).

### Watch

A list of anything we need to keep tabs on — things that could change our rating, or areas to
research deeper next time. A scheduled update run reads this section first before doing any
research, so keep it specific and actionable.

### Sources

References and citations, ideally as links, with as-of dates where facts, prices, or valuation
depend on timing.
