---
id: weighted-average
name: Weighted-Average Valuation
script: ../../scripts/weighted_average_valuation.py
---

# Valuation method: Weighted-Average

A **meta-method**: it does not value a company from scratch, it **blends the ROIs of other methods**
that have already run. Use it for a strategy whose thesis legitimately admits more than one valuation
lens, where the best lens depends on the company. [Rule Breakers](../strategies/rule-breakers.md) is
the case in point — a profitless disruptor is valued top-down by [tam-capture](tam-capture.md),
while one that has tipped into profitability can *also* be anchored bottom-up by
[exit-multiple](exit-multiple.md) — and rather than pick one, this method weights whichever apply.

```
blended_roi = Σ_i ( w_i / Σ w ) · valuation.<method_i>.roi
```

## How it plugs in

Wired in like every method (see the [SKILL](../../SKILL.md), *Estimating ROI*), with one difference:
its inputs are **other methods' outputs**, so it runs **last**. The component ROIs are read in place
from their own blocks (`valuation.exit-multiple.roi`, `valuation.tam-capture.roi`, …) — this method
never copies them, keeping a single source of truth per component. It writes the blend back as
`valuation.weighted-average.roi`, stamped with `date`.

### Front-matter contract

```yaml
valuation:
  exit-multiple:                       # a component — produced by its own method
    ...
    roi: 0.082                         #   (written earlier by exit_multiple_valuation.py)
  tam-capture:                         # a component — produced by its own method
    ...
    roi: 0.251                         #   (written earlier by tam_capture_valuation.py)
  weighted-average:
    weights: {exit-multiple: 0.4, tam-capture: 0.6}  # keys = the methods to blend
    roi: 0.0                           # written by this script — do not hand-edit
    date: 2026-06-24                   # written by this script — the run's as-of date
```

The **keys of `weights` are the component list** — there is no separate `methods` field, so the two
can't drift apart. Weights are **relative** and need not sum to 1; the script normalizes them.

### Choosing the components and weights

- **Only include applicable methods.** A method the company doesn't fit (see each method's
  *Applicability*) is **omitted from `weights` entirely** — not given weight 0. If only one method
  applies, list just that one; the blend degenerates to it at weight 1.
- **Weight by reliability, not by answer.** Assign weight by how applicable each method is and how
  trustworthy its data is — in effect, trust the better-supported estimate more (inverse-variance
  weighting). **Do not** tilt the weights toward whichever result is more conservative; that biases
  the estimate under cover of caution.

### Spread drives confidence, not the ROI

The script reports the **spread** between the component ROIs but does not store it. A wide spread
means the lenses genuinely disagree about the company's future and the blend is averaging away real
model risk — so it should pull the strategy's **confidence** down (see [scoring.md](../scoring.md)).
Tight agreement supports confidence. The blended ROI is the point estimate; the spread is the honesty
that stops it from looking more certain than it is.

## Running the script

Run it **after** the component methods, so their `roi` fields exist. It mirrors `company_score.py`.

```bash
SCRIPT=skills/stock-analysis/scripts/weighted_average_valuation.py

# Stock-doc mode: read the weights map + sibling rois, write the blend back.
"$SCRIPT" --stock-doc NET
"$SCRIPT" --stock-doc NET --dry-run --format json     # preview without writing

# Raw mode: an ad-hoc blend, name:roi:weight per component.
"$SCRIPT" --component exit-multiple:0.082:0.4 --component tam-capture:0.251:0.6
```

It **fails loudly** if a method listed in `weights` has no block or no `roi` yet — run that component
first, or drop it from the weights.

## Reading the output

- **Blended ROI** (`valuation.weighted-average.roi`) — the headline, and the strategy's canonical ROI
  whenever `weighted-average` is the [chosen](../../SKILL.md) valuation method.
- **Component table** — each method's normalized weight, its ROI, and its contribution to the blend,
  so you can see which lens is driving the result.
- **Component spread** — the min–max range of the component ROIs. Feed it into the confidence call as
  above, and record the components, weights, and your weighting rationale in the **Valuation** section.
