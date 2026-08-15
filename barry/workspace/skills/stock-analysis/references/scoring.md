# Scoring mechanics

The canonical, **strategy-agnostic** description of how trait scores combine into a company score.
Every strategy uses this same machinery; they differ only in **which traits** they use, the
**floors** they assign, and how they **interpret** the resulting bands. Those three things are the
strategy's own — defined in each strategy doc. The math below is shared and lives only here.

## Two axes

Every trait is scored individually on **two separate axes**, each 0–1:

* **Score** — how well the company meets the trait criteria.
* **Confidence** — how firmly that score is grounded in evidence. High confidence means solid,
  indisputable facts; low confidence means sparse information, assumptions, or best-guesses.

**Confidence never alters the score.** A high score held with low confidence stays a high score — it
is just flagged as shaky. Use a low score with low confidence where evidence is thin; never omit a
trait the strategy requires.

Record `{score, confidence}` per trait in the **stock-doc front matter**, under a `traits:` mapping
keyed by trait id (see the [stock-doc skill](../../stock-doc/SKILL.md)).

## Documenting low confidence (the firm-up rule)

A confidence figure is only useful if it is *actionable*. So whenever a trait's **confidence is 0.8
or below**, the write-up for that trait must say what would raise it — exactly one of:

* **A specific, reviewable source** — named by document type and where to find it (e.g. "the FY2025
  annual report's business-combinations note", "the latest 4C quarterly cash-flow report"), never a
  vague "more research needed". If that source is cheap to obtain, also add it to the stock-doc
  **Watch** section so the next update actually closes the gap.
* **"Irreducible for now"** — a plain statement that no source can currently improve the score, plus
  the **future event** that would create the evidence (e.g. "no retention history exists until the
  first renewal cohorts report; revisit after FY2026 results"). That event is itself a Watch item.

The purpose is to force the distinction between *low confidence because the evidence was not gathered*
(a to-do) and *low confidence because the evidence does not yet exist* (a known limitation). One of
the two must be stated — never leave a sub-threshold confidence unexplained.

This is a **documentation discipline only**: it never changes the score or the confidence, and
confidence must not be nudged above the threshold to avoid writing the line.

## Eligibility gate (disqualifiers)

Before any traits are combined, the company is checked against the **disqualifiers** — thesis-breaking
facts that make it outright ineligible (a single universal set; see
[disqualifiers.md](disqualifiers.md)). This is a binary gate, deliberately kept *outside* the scoring
machinery: a disqualified company is **not scored at all**, rather than scored and then knocked down.
The verdict is recorded once in the stock-doc as a top-level `disqualified` boolean (absent =
unassessed, `false` = checked and clear, `true` = ineligible). When it is `true`, the scorer skips
**every** strategy and the leaderboard is empty.

Keeping disqualification out of the trait set is what lets every remaining term be a genuine 0–1
quality measure. An always-passes safety switch folded in as a trait does *not* behave like one: a term
that sits at its maximum almost every time still inflates the geometric mean (and only partially washes
out under normalization), by an amount that depends on the trait count — so it silently biases scores
upward and breaks cross-strategy comparability. The gate avoids this by construction.

## Combining traits

Both axes are aggregated with the **same** geometric mean of floor-adjusted terms. The score axis
produces the strategy's floor-adjusted score aggregate; the confidence axis produces its
floor-adjusted confidence aggregate:

```
term_i  = floor_i + (1 - floor_i) * value_i
overall = ( ∏_{i=1..n} term_i ) ^ (1/n)
```

Where `value_i` is the trait's score (for the score aggregate) or its confidence (for the confidence
aggregate), `floor_i` is the floor for trait *i* (read from the strategy front matter), and `n` is
the number of traits the strategy uses.

The floor lifts each trait's contribution from [0, 1] into [floor_i, 1]. **The floor encodes how
important a trait is, inversely: a LOWER floor makes the trait matter MORE.**

* **floor = 0** → the trait can *veto*. A zero value forces the whole aggregate to 0. Reserved for
  make-or-break traits.
* **floor near 1** → the trait barely moves the result, regardless of its value.

A geometric mean (rather than a plain average) is used deliberately: it punishes imbalance, so a
company that is weak on one real trait cannot fully paper over it with strengths elsewhere.

Running confidence through the identical formula means the confidence aggregate answers the right
question — *how well-grounded are the traits that actually drive the score?* Thin evidence on a
high-floor trait (which barely moves the score) barely dents confidence; thin evidence on a
make-or-break trait tanks it.

Because every term sits in [floor_i, 1], **both aggregates are compressed upward** (mediocre inputs
land above 0.50, not at it) and **both share the veto** (a 0 on any floor-0 trait drives the
aggregate to 0). Exactly where the bands fall depends on the strategy's floors and trait count, so
these raw aggregates are **not** comparable across strategies and are never read on a naïve 0–1
scale — which is why the scorer does not store them. It stores the *normalized* values instead (next
section), and those are read against a single shared table.

## Normalization

The raw floor-adjusted aggregates above are **not comparable across strategies** — each strategy's
floors compress and uplift them differently. So the scorer does not store them. Instead it
**normalizes both axes** and stores only those: each aggregate is converted back onto a comparable
[0, 1] underlying trait-quality scale.

The normalized value is the uniform trait value `q` that would reproduce the observed aggregate under
that strategy's floors:

```
aggregate = geometric_mean(floor_i + (1 - floor_i) * q)
```

The script solves `q` numerically by bisection — once with the score aggregate as the target (giving
the normalized **score**) and once with the confidence aggregate (giving the normalized
**confidence**). Because both axes share the identical floor machinery, both normalize the same way,
and a high-floor strategy and a low-floor strategy can be compared on the same implied
underlying-quality scale. The per-trait scores and the strategy floors remain the audit trail for
what drove the result.

The normalized pair is written into the stock-doc `strategies:` map, keyed by strategy name:

```yaml
strategies:
  rule-breakers:
    score:      0.72
    confidence: 0.79
```

The `strategies:` map is entirely scorer-owned. Eligibility lives elsewhere: a top-level, agent-owned
`disqualified` flag (see the *Eligibility gate* section above). When it is `true` the scorer writes no
strategies at all and clears any stale ones.

## Interpreting the normalized score

Because normalization removes each strategy's floor compression, the stored `score` sits directly on
the underlying **trait-quality** scale — the same scale the individual traits are scored on (0.70–1.00
clearly meets, 0.40–0.69 partial, 0.00–0.39 fails). So **one table reads every strategy**; there is
no per-strategy calibration to remember, and scores can be compared across strategies on sight:

| Normalized score | Reading |
|------------------|---------|
| ≥ 0.85 | Exceptional — equivalent to uniformly excellent traits across the board |
| 0.70 – 0.85 | Strong — solidly clears the bar, with one or two soft spots |
| 0.55 – 0.70 | Mixed — real positives but material gaps |
| 0.40 – 0.55 | Weak — several traits are unconvincing |
| < 0.40 | Poor / vetoed — a make-or-break (floor-0) trait is failing or absent, which drags the whole result down |

The veto still bites: a 0 on any floor-0 trait forces the raw aggregate to 0, and the normalized
score with it. Which traits can veto is the strategy's own (see each strategy's trait list).

The normalized `confidence` lives on the **same** scale — read it as *how much to trust the score*
(solid evidence vs. thin), not as a plain average of the per-trait confidences. Always report a
strategy's `score` together with its `confidence`.

## Running the scorer

Do not compute aggregates by hand. Score the traits in the stock-doc front matter, then run
[`company_score.py`](../scripts/company_score.py). For each strategy it reads the trait scores from
the stock-doc and the floors from the strategy, computes the floor-adjusted aggregates, normalizes
both axes, and writes the normalized `score` and `confidence` into the stock-doc's `strategies:` map
under the strategy's name (surgically — other strategies' entries and the rest of the front matter are
left untouched). If the company's top-level `disqualified` flag is `true`, no strategy is scored and
any stale `strategies:` block is cleared. The raw floor-adjusted aggregates are shown in the run output
but not stored.

The stock-doc is the only positional argument — a bare ticker (resolved in the stock-docs dir) or a
path to a `.md`. Override dirs with `--stock-dir` / `--strategy-dir` if needed.

```bash
SCRIPT=skills/stock-analysis/scripts/company_score.py

# Default: score EVERY strategy whose trait set is complete, writing each back. Strategies still
# missing traits are skipped (reported, not an error). If the company is disqualified, nothing is scored.
"$SCRIPT" NVDA

# Score just one strategy (explicit-request case); fails if its trait set is incomplete:
"$SCRIPT" NVDA --only rule-breakers

# Preview without writing; --format json for a machine-readable result:
"$SCRIPT" NVDA --dry-run --format json
```

The default scores all complete strategies in one pass — they coexist under `strategies:`. The
scorer is agnostic to what the traits mean: the floors are the strategy's single source of truth, the
per-trait scores are the stock-doc's. You can hand-edit a trait's score or confidence and re-run to
refresh every affected strategy's entry. Reserve `--only` for when a specific strategy is requested.

Always report a strategy's `score` **with** its `confidence` — a strong score on thin evidence is
not the same as a strong score on solid evidence.

## Picking the strategy: leaderboard mode

The committing run above needs *every* required trait scored. But you don't know upfront which
strategy a company belongs to, and you don't want to fully research all of them. `--leaderboard`
solves this: it scores **all** strategies at once, **optimistically** (any trait absent from
the stock-doc's `traits:` map is assumed perfect, `{score: 1, confidence: 1}`), and **never writes**.
If the company's top-level `disqualified` flag is `true`, the ranking is empty — it is ineligible for
everything. It exists to tell you which strategy is winning and which trait to evaluate next — the
workflow that uses it lives in the [SKILL](../SKILL.md#picking-the-strategy); the mechanic is here.

```bash
"$SCRIPT" NVDA --leaderboard            # ranked table + verdict
"$SCRIPT" NVDA --leaderboard --format json
```

**Why optimism is the right default.** Each term is monotonic in its value, so assuming `1` for an
unevaluated trait can only *overstate* a strategy's aggregate. Every strategy's leaderboard numbers
are therefore **upper bounds** that descend toward the truth as you evaluate its traits. Strategies
are ranked by the product **score × confidence** — an evidence-weighted quality, also an upper bound
(both factors descend from 1). The state contract is presence-based: **a trait counts as evaluated
only once it is written into `traits:`; everything absent is treated as optimistic.**

**The stopping rule (why a complete leader wins).** A strategy that is *fully evaluated* carries no
optimism — its leaderboard number is its true score×confidence. If such a strategy also **leads**
(top of the ranking), its true value is ≥ every other strategy's upper bound, hence ≥ their true
values: it is the proven winner, and you never had to finish evaluating the losers. So the verdict is
simply: **decided once the rank-1 strategy is COMPLETE.** While the leader still has optimistic
traits, its lead may evaporate — evaluate its lowest-floor (highest-leverage) unevaluated trait next.

**Near-ties.** Crowning proves the winner but not the *margin*: a ruled-out strategy is left with
only an upper bound, so you can't tell a comfortable win from a photo finish. When the runner-up's
bound sits within `EPSILON` (0.05) of the proven leader, the verdict flags it — `provisional` if the
runner-up is still optimistic (resolve its remaining traits to confirm a clear win vs a genuine
dual-fit), or `near_tie` if it too is complete (a real dual-fit — write up both, see the SKILL).

**Committing afterward.** The leaderboard is advisory and writes nothing. Once decided, run the
committing scorer (above) — its default writes a normalized `{score, confidence}` for **every
complete strategy** and skips the rest, which is exactly right: a strategy you ruled out on its
optimistic bound still has unevaluated traits, so it has no honest normalized score and is left out.
Record in the write-up that such a strategy was ruled out and why, rather than a fabricated number.
