# Overall scores

How a stock-doc's three headline numbers in the `overall:` block are produced and read. They sit one
layer above per-strategy scoring and valuation: they **combine** a strategy's quality score, its
confidence, and the chosen valuation's ROI into comparable ranking numbers. The strategy score and
confidence come from [scoring.md](scoring.md); the ROI from [valuation/](valuation/). This file owns
only how they fold together.

```yaml
overall:
  qv_score:    0.66   # quality × value      — where to focus research
  cqv_score:   0.58   # confidence-adjusted  — where to allocate dollars
  agent_score: 0.75   # the agent's valuation-aware judgement call (0–1)
```

`qv_score` and `cqv_score` are computed by [`overall_score.py`](../scripts/overall_score.py);
`agent_score` is agent-owned (see below). All three are on a 0–1 scale so they read together.

## The three inputs

* **`q` — quality.** The chosen strategy's normalized `score` (0–1). Pure business quality; it carries
  no price. Selected: `chosen.strategy` if set, else the strategy with the highest `score × confidence`
  (which is, by construction, the leaderboard winner the doc is framed under).
* **`c` — confidence.** The same strategy's normalized `confidence` (0–1) — how well-grounded `q` is.
* **`roi` — the only valuation-aware input.** The chosen valuation's annualized ROI, where price
  enters. Selected: `chosen.valuation` if set, else the chosen strategy's canonical method, else the
  sole method present. (The `chosen` defaults are spelled out in the
  [SKILL](../SKILL.md#estimating-roi).)

## Value from ROI

ROI is unbounded and on a different scale from quality, so it is mapped onto a 0–1 **value** score
against a single reference return:

```
V = clamp(roi / 0.30, 0, 1)
```

0%/yr → 0, 15%/yr → 0.5, ≥30%/yr → 1. The map is linear with no hurdle: lower returns score lower
rather than being cut off, so names stay rankable instead of bunching at zero. A non-positive ROI
gives `V = 0` (and so a zero overall score) — an idea you expect to lose money on is not an
opportunity to rank.

## The two computed scores

Both fold quality and value with an **equal-weight geometric mean**:

```
qv_score  = sqrt( q · V )
cqv_score = sqrt( (c · q) · V )      ( = sqrt(c) · qv_score )
```

The geometric mean is **conjunctive on purpose**: a name must be good on *both* quality and value, and
a near-zero on either sinks the result. That matches what prioritizing opportunities for capital
actually requires — a wonderful business with no expected return, or a steep "bargain" in a poor
business, should both rank low. A plain average would let one paper over the other.

The two scores differ only in confidence:

* **`qv_score`** is **confidence-blind** — it rates the opportunity on the visible merits. Use it to
  prioritize **research**: a high `qv_score` held at low confidence is exactly a high-potential idea
  worth digging into to firm up.
* **`cqv_score`** multiplies `q` by `c` before the mean, discounting the quality read by how much we
  trust it. Use it to prioritize **capital** — it is the conviction-weighted number. Because confidence
  enters as a clean multiplier, `cqv_score = sqrt(c) · qv_score`, so the two never cross and their
  ratio is a pure confidence readout.

Confidence discounts `q` only, not `V`: today's confidence figure measures trust in the *quality*
traits, and we have no separate confidence on the ROI estimate. A valuation confidence is a future
addition; until then `cqv_score` does not penalize ROI-model uncertainty.

## `agent_score` — the judgement call

`agent_score` is the agent's overall, **valuation-aware** rating of the stock on a 0–1 scale (the
basis for it is argued in the stock-doc's **Valuation** section). It is the successor to the old
top-level 0–10 `score`, rescaled (7.2/10 → 0.72) so it reads alongside the others.

It is **confidence-blind, like `qv_score`**: the agent rates the opportunity on its visible merits, not
on how much evidence backs them — two glowing sentences about a company earn a high `agent_score`,
even though confidence would be low. So the right comparison is **`agent_score` vs `qv_score`**, both
risk-blind. What the agent adds over the mechanical `qv_score` is the qualitative judgement the formula
cannot see: red flags, portfolio fit, catalysts, where the thesis is fragile.

`agent_score` is **agent-owned**. `overall_score.py` never writes or alters it — it only carries an
existing value through when it re-renders the block (exactly as the `disqualified` flag is agent-owned
and outside the scorer). Set it by hand as part of the write-up.

## Methodology-drift signal

A **large gap between `agent_score` and `qv_score`** is a hint to review the methodology — either the
agent is seeing something the formula misses, or the formula (trait scoring, the ROI, the value map) is
miscalibrated. Because the two scales have different distributions (the geometric mean compresses
toward the low-middle; the agent anchors higher by feel), judge **outlier** divergence — a name that
deviates far more than the book's typical gap — not the routine offset every name shares.

## Running it

Run after the strategy is scored ([`company_score.py`](../scripts/company_score.py)) and the chosen
valuation's ROI is written. One positional argument — a bare ticker (resolved in the stock-docs dir) or
a path to a `.md`:

```bash
SCRIPT=skills/stock-analysis/scripts/overall_score.py

"$SCRIPT" SDR.AX                 # compute and write overall.qv_score / overall.cqv_score
"$SCRIPT" SDR.AX --dry-run       # preview without writing; --format json for machine-readable
```

It reads `q`, `c`, and `roi` per the selection rules above, writes `qv_score` and `cqv_score` into the
`overall:` block (surgically — `agent_score` and the rest of the front matter are untouched), and
re-stamps nothing else. If no strategy is scored or no usable ROI exists, the two scores cannot be
computed: they are left out (any stale ones cleared) and `agent_score` is preserved. Re-run after any
change to the chosen strategy's score/confidence or the chosen ROI.
