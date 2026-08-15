# Market Docs

This folder contains current notes for nascent or structurally changing markets we are researching. Each file reflects the latest view, not a dated update log. To see how the view evolved, use git history.

Each market doc starts with front matter: a compact summary of the assumptions most likely to feed stock-level valuation work. The prose below it explains the market definition, adoption path, structure, player assumptions, and key things to watch.

The main front matter fields are `base-year`, `maturity-duration`, `size.current-market-value`,
`size.maturity-market-value`, optional `penetration.inputs` and
`penetration.model-estimate`, `concentration.inputs.traits`,
`concentration.model-estimate`, its optional `concentration.override`, the derived
`concentration.hhi`, and canonical player capture resolved from `players.model-estimate` and
optional `players.override`. `maturity-duration` is fixed at `10`, so the projection
year is always `base-year + 10`.

## Terminology

**TAM** — total addressable market at full adoption: the addressable base times unit economics,
independent of how far adoption has progressed. Not currently a stored front matter field; its future
methodology belongs to the market-analysis size sub-skill.

**Market value** — expected actual market size in a given year, in billions of `currency`. Stored in `size.current-market-value` (base year) and `size.maturity-market-value` (the 10-year horizon, `base-year + 10`).

**Penetration** — adoption measured as `stock`, `new-sales-share`, or `spend-share`, always as a
decimal in `[0,1]`. Docs with adoption-curve work store analyst choices under `inputs` and the
script's logistic `{L, t0, k}` under `model-estimate`; a complete explained `override` is canonical
when present. The annual path is derived, not stored. Addressable units and unit economics belong
to market sizing, not penetration.

**Capture** — a player's expected decimal share of market value at the 10-year horizon. The
mobility model estimates it from the current ranking, current shares, and horizon concentration.
An explained per-player override is canonical when present; otherwise the mobility-adjusted model
estimate is canonical. The model also stores `mobility-adjusted-revenue`, equal to its adjusted
capture multiplied by `size.maturity-market-value`, in billions of `currency`; this field remains
the unoverridden model view.

## Interpreting HHI

The concentration model writes a geometric rank-share pair `{s1, r}` under `model-estimate`, where
rank `i` has share `s1 × r^(i−1)`. If an analyst-owned `override` is present, it is canonical;
otherwise `model-estimate` is canonical. HHI is script-owned and stored as the derived value
`s1² / (1 − r²)`, equivalent to the sum of squared decimal shares under that model. A `0.10` HHI
behaves like ten equally sized competitors; `0.25` behaves like four. Multiply by `10,000` to
compare with the common antitrust point scale, where `0.18` equals `1,800`.

These ranges are intuition pumps, not hard rules. HHI moves with the market definition, geography, and share basis used.

| Front matter HHI | Effective competitors | Read as | Rough industry anchors |
| --- | ---: | --- | --- |
| `< 0.03` | `33+` | Extremely fragmented | restaurants, local construction trades, independent professional services |
| `0.03-0.06` | `17-33` | Fragmented | apparel brands, ecommerce sellers, generic industrial components |
| `0.06-0.10` | `10-17` | Moderately fractured | global automakers, industrial automation, grid-scale battery storage |
| `0.10-0.18` | `6-10` | Moderately concentrated | smartphones, public cloud infrastructure, athletic footwear |
| `0.18-0.35` | `3-6` | Concentrated | U.S. wireless carriers, payment networks, major rating agencies |
| `> 0.35` | `< 3` | Dominant or duopoly-like | web search, mobile operating systems, large commercial aircraft |

Use the HHI as a consistency check: the player-capture table and market-structure prose should feel like they describe the same 10-year market.
