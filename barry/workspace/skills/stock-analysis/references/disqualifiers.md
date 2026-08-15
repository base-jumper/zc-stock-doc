# Disqualifiers

A **disqualifier** is a thesis-breaking fact that makes a company **ineligible** outright — no score
is computed for any strategy. It is not a trait: traits grade *how good* a company is on a continuous
0–1 scale and combine into the score, whereas a disqualifier is a binary **eligibility gate** checked
*before* and *separately from* scoring. This split exists because a safety switch that is "passed"
almost every time does not belong inside the geometric mean — folding an always-satisfied term into
the average distorts it (see [scoring.md](scoring.md)).

Disqualifiers are reserved for kill-shots that **no scored trait already captures**. A company that is
simply a poor *fit* for a strategy is not disqualified — it scores low on that strategy's traits and
loses on the leaderboard. Likewise a weakness that a trait already grades (decelerating growth, a lost
lead, a stretched-but-survivable balance sheet) is handled by marking that trait down, not by
disqualifying. Disqualify only when the fact would void the thesis regardless of how strong the traits
look.

Disqualification is therefore a property of the **company**, not of any one strategy: every
disqualifier is universal. There are no strategy-specific disqualifiers — a strategy-specific
weakness either belongs to a trait (and is graded by it) or, if it breaks the floor or the catalyst, is
already vetoed by that trait's floor of 0. So the gate is checked **once**, and a fired disqualifier
makes the company ineligible for *all* strategies at once.

## Universal disqualifiers

These break the thesis under any strategy:

* **Accounting integrity** — irregularities, restatements, or credible fraud allegations; financials
  that cannot be trusted enough to underwrite anything built on them.
* **Solvency / liquidity** — debt maturities, covenant breaches, or cash burn that could wipe out the
  equity or force a heavily dilutive raise before the thesis can play out.
* **Hidden or understated liabilities** — pension deficits, major litigation, decommissioning, or
  off-balance-sheet exposure large enough to threaten the equity.
* **Value-leaking control** — a controlling shareholder or related-party dealings structured so value
  is siphoned to insiders at minority holders' expense. (The non-egregious end of governance and pay
  is graded by the relevant traits; this is the abusive extreme that voids the case outright.)
* **Business-model kill-shot** — a regulatory or legal action that would imminently and fundamentally
  void the way the company makes money. Not the ordinary regulatory or legal overhang a business
  faces (that is the relevant fit/quality trait's judgement, and the score handles it), but a concrete
  action that voids the business model outright — distinct from a *liability quantum* large enough to
  threaten the equity, which the hidden-liabilities item above already covers.

## Recording the verdict

The gate is checked once, upfront (see
[SKILL — Picking the strategy](../SKILL.md#picking-the-strategy)). Record the result as a single
**top-level** `disqualified` boolean in the stock-doc front matter, with a three-state reading by
presence:

* **absent** — disqualifiers have not been assessed for this stock yet.
* **`false`** — disqualifiers were checked and none were triggered; the company is eligible.
* **`true`** — at least one disqualifier was triggered; the company is ineligible. The scorer skips
  every strategy (writing no `score`/`confidence`) and the leaderboard is empty.

The field is **agent-owned**: the scorer reads it to decide whether to score and clears any stale
scores when it is `true`, but never sets it itself. Document the reason for a `true` in the write-up's
**Trait Assessment** prose (which disqualifier, the evidence, the source) — the boolean carries the
verdict, the prose carries the why.
