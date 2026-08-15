---
name: market-doc
description: Maintain durable market research documents and extract standardized market outputs. Use when asked to show stored market notes, list latest/recently updated market docs, export company market-value capture assumptions, update/create market docs, or invoke /market-doc-show, /market-doc-latest, /market-doc-companies, or /market_doc companies.
---

# Market Doc

Maintain living market research notes under `investment/market-docs`.

Market docs track nascent or structurally changing markets where the useful output is a durable
10-year view: current market value, projected market value, expected concentration, and major-player
market-value capture at a common horizon. These assumptions can later feed stock-level valuation
work. See the market-docs README at investment/market-docs/README.md for the terminology
distinction between market value and TAM.

This skill defines the file name, front matter schema, and tools for working with stored market docs.
The actual research methodology and document body live in the [market-analysis skill](../market-analysis/SKILL.md).

## Core Rules

- Store one Markdown file per market: `<market-id>.md`, using a short lowercase slug such as `humanoid-robots.md` or `grid-scale-battery-storage.md`.
- Treat the file stem as the market id. Do not duplicate it in front matter.
- Keep each file as the current view only. Remove stale points instead of preserving an in-file history; git records history.
- Always preserve and update front matter.
- Use the bundled script for list/export commands instead of hand-parsing files.
- If creating or substantively updating research content, use the `market-analysis` skill if available; it defines the body sections and standards.

## Script-Owned Calculations

When a market-analysis sub-skill has a deterministic script, the market doc is its durable
input/output interface:

- `inputs` contains analyst-owned assumptions. Edit these when evidence or judgment changes.
- `model-estimate` contains the script's unadjusted estimate.
- `override` is optional and analyst-owned. When present, it must contain the complete replacement
  parameter set and a non-empty `reason`.
- For collection outputs such as players, completeness applies per overridden member; members
  without an override continue to resolve from `model-estimate`.
- Derived fields and the calculation's `method` and `date` are script-owned. Do not hand-edit them;
  change `inputs` or `override` and rerun the script.
- The canonical parameter set is `override` when present, otherwise `model-estimate`. Do not store a
  third copy of the resolved parameters.

Scripts must support a dry run and must update only their own script-owned fields, preserving
analyst inputs, overrides, unrelated front matter, and the document body. The prose must explain
the inputs, any override, and the resolved output.

For normal refreshes, use the dependency-aware command documented under market-analysis
[Refreshing Stored Calculations](../market-analysis/SKILL.md#refreshing-stored-calculations).
Individual calculation scripts are diagnostic and maintainer interfaces.

This convention applies only where a stable calculation contract exists. Do not force large,
market-specific research bridges into front matter merely to make them script-readable.

## Front Matter

Each market doc must start with this front matter. This is the canonical schema; do not maintain a separate template file.

```yaml
---
base-year: 2026
currency: USD
maturity-duration: 10
size:
  current-market-value: 0.0
  maturity-market-value: 0.0
penetration:
  inputs:
    target-series: data/example/penetration.csv
    measure: stock              # stock | new-sales-share | spend-share
    ceiling: 0.0
    analogs: [analog-id-1, analog-id-2]
    # w-fit: 0.5                # optional analyst cap/override of computed fit weight
    # as-of-year: 2026          # optional information cutoff
  model-estimate:               # written by penetration_fit.py
    L: 0.0
    t0: 2031.0
    k: 0.0
  # Optional analyst-owned replacement for all three parameters:
  # override:
  #   L: 0.0
  #   t0: 2031.0
  #   k: 0.0
  #   reason: "Target-specific evidence the blended model does not capture."
  method: logistic-blend
  date: YYYY-MM-DD
concentration:
  inputs:
    traits:
      network-effects:       {score: 0.0, confidence: 0.0}
      data-scale-advantage:  {score: 0.0, confidence: 0.0}
      brand-reputation:      {score: 0.0, confidence: 0.0}
      capital-intensity:     {score: 0.0, confidence: 0.0}
      scale-economies:       {score: 0.0, confidence: 0.0}
      regulatory-barriers:   {score: 0.0, confidence: 0.0}
      switching-costs:       {score: 0.0, confidence: 0.0}
  model-estimate:             # written by concentration_fit.py
    s1: 0.0
    r: 0.0
  # Optional analyst-owned replacement for both parameters:
  # override:
  #   s1: 0.0
  #   r: 0.0
  #   reason: "Target-specific evidence the pooled model does not capture."
  hhi: 0.0                    # written from override-or-model-estimate
  method: selected-direct-ridge
  date: YYYY-MM-DD
players:
  inputs:
    current:
      - rank: 1
        name: Current Leader
        ticker: TICKER
        share: 0.0
      - rank: 2
        name: Current Number Two
        ticker: TICKER2
        share: 0.0
  model-estimate:             # written by mobility_fit.py
    - rank: 1
      name: Current Leader
      ticker: TICKER
      hold-position-capture: 0.0
      mobility-adjusted-capture: 0.0
      mobility-adjusted-revenue: 0.0
    - rank: 2
      name: Current Number Two
      ticker: TICKER2
      hold-position-capture: 0.0
      mobility-adjusted-capture: 0.0
      mobility-adjusted-revenue: 0.0
  # Optional per-player replacement or additional outside contender:
  # override:
  #   - name: Current Leader
  #     ticker: TICKER
  #     capture: 0.0
  #     reason: "Company-specific evidence the pooled mobility model does not capture."
  gone-probability: 0.0       # written by mobility_fit.py; already included in adjusted capture
  method: share-gap-mobility-weighted-geometric-capture
  date: YYYY-MM-DD
---
```

`base-year` is the starting year for the market view. `maturity-duration` is fixed at `10`; the
implied projection year is `base-year + 10`. The field name is retained for compatibility with
stock-analysis handoff scripts, but the process no longer estimates a market maturity date.

`currency` is the single currency used throughout the front matter and prose unless explicitly stated
otherwise. `size.current-market-value` and `size.maturity-market-value` are expected actual market
size in billions of `currency`; `size.maturity-market-value` is the expected market value at the
10-year horizon. These are market values, not TAMs (full-adoption addressable market). Sizing
methodology belongs to the market-analysis [size sub-skill](../market-analysis/references/size/size.md).

`penetration` is optional and present once adoption-curve work has been done.
`penetration.inputs` holds the analyst-owned target-series path, measure type, asserted ceiling,
analog selection, and optional fit-weight or information-cutoff judgment. Relative target-series
paths resolve from the market doc's directory. The script writes the blended logistic parameters
to `penetration.model-estimate`; an optional complete `penetration.override` replaces all three and
must explain why. The canonical parameters are therefore `override` when present, otherwise
`model-estimate`. Penetration at year `t` is `L / (1 + exp(-k × (t - t0)))`, where `L` is the
saturation ceiling, `t0` the midpoint year, and `k` the steepness. The annual path is derived on
demand and is not stored. Addressable units and unit economics do not belong in this block. The
methodology and parameter derivation live in the market-analysis
[penetration sub-skill](../market-analysis/references/penetration/penetration.md).

`concentration.inputs.traits` holds the seven analyst-scored structural inputs. The script writes
its predicted geometric rank-share parameters to `concentration.model-estimate`. An optional
`concentration.override` replaces both parameters and must explain why. The canonical parameters
are therefore:

```text
override if present, otherwise model-estimate
```

They model share at rank `i` as `s1 × r^(i−1)`, where `s1` is the leader's decimal share and `r` is
the rank-to-rank decay ratio. `concentration.hhi` is script-owned and derived from the canonical
parameters as `s1² / (1 − r²)`; never estimate or adjust it independently. HHI ranges from near `0`
for a highly fractured market to `1` for a monopoly. Approximate effective competitor count is
`1 / HHI`. The derivation and validity limits live in the market-analysis
[concentration sub-skill](../market-analysis/references/concentration/concentration.md).

`players.inputs.current` holds the defensible current top two to five ranking and each player's
share of the whole defined market. Ranks must be contiguous and shares descending on the same
boundary and basis as concentration. `mobility_fit.py predict --market-doc <MARKET_ID>` reads these
shares plus canonical concentration and writes `players.model-estimate`. `hold-position-capture`
is the horizon share at the player's current rank; `mobility-adjusted-capture` weights the complete
geometric horizon share curve by its fitted rank-transition distribution. The `fringe` state
receives its modeled geometric-tail value; `gone` receives zero, so `gone-probability` must not be
applied again. `mobility-adjusted-revenue` is `mobility-adjusted-capture ×
size.maturity-market-value`, expressed in billions of the top-level `currency`. It is a script-owned
model output; it does not incorporate `players.override`.

An optional `players.override` replaces the model capture for a matching name or adds an explicitly
judged outside contender. Every override supplies `capture` and a non-empty `reason`. Canonical
capture is the per-player override when present, otherwise `mobility-adjusted-capture`. Capture is
a decimal share of the whole projected market value. The canonical player list need not sum to
`1.0`, but cannot exceed it; unlisted private companies and the long tail belong in prose.

## Commands

Use:

```bash
skills/market-doc/scripts/market_doc.py <command>
```

### `/market-doc-show <MARKET_ID>`

Run `market_doc.py show <MARKET_ID>`, then answer with the stored note or a concise summary if Nick did not ask for the full file.

### `/market-doc-latest [N]`

Run `market_doc.py latest [N]`. Return the most recently updated docs first. The script reads the new front matter and reports market id, file update date, base year, projection year, current market value, projected market value, HHI, and market name.

### `/market-doc-companies`

Run `market_doc.py companies`. Return one row per canonical player capture, including market id,
ticker, 10-year capture, projection year, projected market value, player, and market name. This is
the handoff surface for stock-level TAM-capture valuation work.

### `/market-doc-frontmatter [MARKET_ID]`

Run `market_doc.py frontmatter [MARKET_ID]`. Return parsed front matter as JSON.

### `/market-doc-validate [MARKET_ID]`

Run `market_doc.py validate [MARKET_ID]` after changing front matter or running a script-owned
calculation. It checks the fixed horizon; penetration inputs and canonical parameters;
concentration inputs, canonical parameters, and derived HHI; and player current-share inputs,
mobility capture and revenue outputs, overrides, and canonical capture.

## Updating Docs

For a new or refreshed market doc:

1. Read the existing market doc first if it exists.
2. Read the `Watch` section before researching; use it to focus the update.
3. Use the `market-analysis` skill to generate substantive research content.
4. Update every front matter field affected by the refresh.
5. Preview and save script-owned outputs with the market-analysis
   [refresh command](../market-analysis/SKILL.md#refreshing-stored-calculations). It validates the
   prospective and saved document as part of the run.

## Document Body

The body starts with an `# Market Name` heading immediately after the front matter. That heading is the market name used by the script when no legacy `market` field exists.

This skill does not define the body. The sections and standards for producing them live in the
[market-analysis skill](../market-analysis/SKILL.md) (*Documenting The Analysis*).
