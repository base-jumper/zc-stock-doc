# Market Size Estimation

Estimate current and 10-year annual market value under the parent
[market contract](../../SKILL.md#market-contract). Accept the evaluated annual adoption path from
the parent workflow; do not invoke or reproduce penetration methodology. Own addressable-base
projections, billable activity, unit economics, TAM, and the bridge from adoption to market value.

## Contents

- [Outputs and Definitions](#outputs-and-definitions)
- [General Revenue Bridge](#general-revenue-bridge)
- [Revenue Archetypes](#revenue-archetypes)
- [Workflow](#workflow)
- [Addressable Base](#addressable-base)
- [Price and Revenue Intensity](#price-and-revenue-intensity)
- [Recurring Revenue and Adjacencies](#recurring-revenue-and-adjacencies)
- [Uncertainty and Validation](#uncertainty-and-validation)
- [Market-Doc Write-Up](#market-doc-write-up)
- [Back-Testing](#back-testing)

## Outputs and Definitions

Write the expected annual market values, in billions of the contract currency, to:

```yaml
size:
  current-market-value: 0.0
  maturity-market-value: 0.0
```

`maturity-market-value` means expected market value at `base-year + 10`, not value at an estimated
maturity date. Market value is annual recognized revenue at the contract's revenue boundary; it is
neither cumulative revenue nor customer spend unless the contract explicitly defines it that way.
Use nominal currency in each stated year by default because the output feeds future company revenue
estimates. If the task requires constant base-year currency, say so and remove general inflation
from the projection.

Keep these concepts distinct:

- **Addressable base** is the quantity of the contract denominator that could structurally adopt.
- **Adopted base or flow** is the addressable quantity multiplied by the supplied penetration rate.
- **Billable activity** is the annual quantity that generates revenue; it can differ from both.
- **Full-adoption TAM** is the annual revenue pool at 100% penetration under that year's base and
  unit economics. It is a diagnostic, not the projected market value.
- **Saturation revenue pool** applies the penetration ceiling `L`; do not confuse it with either
  full-adoption TAM or expected horizon market value.

For durable products, full-adoption TAM means sustainable annual replacement and attached revenue,
not the installed base multiplied by the equipment price every year.

## General Revenue Bridge

Model each economically distinct segment `s` and revenue stream `r`:

```text
D(s,t) = addressable denominator
p(s,t) = supplied penetration
A(s,t) = D(s,t) × p(s,t)
Q(s,r,t) = annual billable activity derived from A(s,t)
P(s,r,t) = net recognized revenue per billable unit

M(t) = Σ_s Σ_r Q(s,r,t) × P(s,r,t)
```

`A` inherits the penetration measure:

- For `stock`, it is the active or installed base. Convert that stock into annual subscriptions,
  usage, new installations, replacements, and attached revenue as applicable.
- For `new-sales-share`, `D` is the annual eligible sales flow and `A` is annual adopted sales.
- For `spend-share`, `D` is annual eligible spend or activity and `A` is the migrated share. Apply
  a take-rate or revenue conversion when the revenue boundary is narrower than that spend.

Do not multiply by an eligibility, adoption, or attachment factor twice. State where every material
conversion enters the bridge.

## Revenue Archetypes

Select one or combine several archetypes. Use separate streams when their volumes or prices follow
different drivers.

| Archetype | Annual billable activity |
|---|---|
| Subscription or service | Active accounts, seats, or users × annual revenue per active unit |
| Consumable or repeat purchase | Active base × purchase frequency × units per purchase |
| Durable equipment | New installations + replacement shipments |
| Installed-base ecosystem | Equipment shipments plus active base × consumables, service, or software attach |
| Healthcare | Treated patients × courses, procedures, doses, or patient-years |
| Marketplace or payments | Transacted activity or value × net take-rate |
| Project or capacity market | Annual projects or capacity additions plus installed-base service revenue |

For a `stock` durable, calculate the installed base annually:

```text
installed(t) = D(t) × p(t)
shipments(t) = max(installed(t) - installed(t-1) + retirements(t), 0)
```

Estimate retirements from installation cohorts and a survival curve when the data matters. A simple
`installed ÷ useful life` approximation is acceptable for an early pass if the installed base is
reasonably mature; state the limitation. Add recurring streams separately:

```text
ecosystem revenue(t) =
    shipments(t) × net equipment ASP(t)
    + installed(t) × annual attached revenue per active unit(t)
```

This installed-base check is mandatory for durable products. State whether initial equipment,
replacement, consumables, or service is expected to dominate horizon revenue.

## Workflow

1. **Apply the contract and segment the market.** Reuse its scope, revenue boundary, units,
   penetration measure, time/value basis, and segments. Add a segment only when separate modeling
   avoids a materially misleading blended volume or price.
2. **Reconstruct the current market.** Prefer a direct market-revenue source with a matching
   boundary. Also build a bottom-up bridge from current denominator, penetration, billable activity,
   and net price. Where direct totals are unavailable, gross up disclosed supplier revenue using a
   defensible share estimate. Resolve material disagreement rather than averaging incompatible
   definitions.
3. **Project the addressable denominator.** Use demographic, epidemiological, business, installed
   asset, capacity, or activity forecasts appropriate to the contract. Separate ordinary base
   growth from changes in structural eligibility caused by product capability, regulation, or
   economics. Do not hide adoption inside the addressable-base forecast.
4. **Apply the supplied adoption path.** Evaluate adopted quantities for every year needed by the
   revenue archetype. Use the whole annual path for stock-to-flow calculations; use the horizon
   point directly for subscriptions, eligible-sales shares, and spend shares when no intermediate
   year is needed.
5. **Calculate billable activity.** Model frequency, seats per customer, utilization, dosage,
   replacement life, attachments, and take-rates explicitly where material. If penetration already
   measures the active base, do not apply churn or retention again except to convert a year-end
   stock into average active unit-years or to estimate gross additions.
6. **Project net revenue per unit.** Start from realized revenue, forecast inflation and real price
   separately, and model mix by segment or stream rather than burying it in one unexplained ASP.
7. **Check recurring revenue and category expansion.** Test equipment replacement, consumables,
   service, software, payments, and adjacent modules. Include them only if they fall within the
   contract; otherwise exclude them or revise the contract before continuing.
8. **Triangulate and stress-test.** Compare the result with current supplier revenue, analogous
   market revenue intensity, customer or substitute spend, and physical supply capacity. Resolve
   impossible implications.
9. **Set the expected values.** Construct coherent downside, reference, and upside cases around the
   few uncertain drivers that matter. Store the probability-weighted expected value when risks are
   asymmetric; report the plausible range and principal sensitivities in prose.

## Addressable Base

Define the denominator independently of present adoption. Structural eligibility belongs in
`D(t)`; the supplied `p(t)` owns actual adoption. Affordability, access, diagnosis, customer
willingness, and similar constraints belong in one side of that boundary only. Use an explicit
funnel to check them, but do not multiply them into both the denominator and penetration.

Prefer primary population, prevalence, shipment, installed-base, business-count, and capacity
sources. Forecast the smallest number of drivers needed to explain `D(t)`. When using geographic
segments, project each in its natural units and translate revenue consistently to the contract
currency; disclose any constant-FX assumption.

## Price and Revenue Intensity

Use net recognized revenue per billable unit, not list price or end-customer expenditure, unless
those match the revenue boundary. Derive the current value from disclosed revenue and volume where
possible. Project:

```text
future net price =
    current net price
    × general inflation
    × real same-product price change
    × mix and net-realization change
```

Prefer explicit segmentation to a large mix adjustment. Anchor the real-price forecast to the
market's actual pricing mechanism: reimbursement or regulation, contracts and renewal behavior,
customer value and substitute cost, competitive intensity, or production economics.

For manufactured products, a cumulative-volume learning curve can constrain the cost forecast:

```text
unit cost(t) = unit cost(0) × (cumulative volume(t) / cumulative volume(0))^b
b = log2(1 - learning rate)
```

Do not pass cost decline through to price automatically. State the assumed pass-through, competitive
response, sustainable margin, and price floor. In software and services, cost per unit is rarely the
primary price anchor; seats, usage, modules, discounts, retention, and customer value usually matter
more.

## Recurring Revenue and Adjacencies

For every durable or workflow product, check whether the horizon revenue pool includes replacement,
consumables, maintenance, software, data, financing, payments, or other attached revenue. Show each
material stream separately to prevent the initial sale from dominating the model by default.

Perform one explicit category-expansion check. Include an adjacency only when it was allowed by the
market contract and is expected to become part of the same product, buying decision, or competitive
control point. Do not silently enlarge the category at the horizon. Conversely, do not describe an
included adjacency in the market definition and then omit it from the arithmetic.

## Uncertainty and Validation

Vary correlated drivers coherently: faster adoption may accelerate learning and lower price while
requiring more capacity; greater competition may lower both price and supplier concentration.
Identify the two or three drivers with the largest effect rather than varying every input.
When adoption uncertainty is material, have the parent workflow supply coherent alternative
adoption paths; do not alter penetration assumptions inside this sub-skill.

Before saving, verify:

- The bottom-up current estimate reconciles with the best boundary-matched current evidence.
- Units cancel correctly and every revenue stream is annual.
- Addressable-base filters and penetration are not double-counted.
- Durable shipments include both new installations and replacement.
- Net prices match the contract's revenue boundary and value basis.
- Recurring streams and included adjacencies appear exactly once.
- Implied unit volumes are feasible given supply, labor, capital, and channel constraints.
- Implied spending is plausible relative to customer budgets and substitutes.
- The current-to-horizon CAGR is consistent with the underlying volume and price bridge.

Round stored market values to sensible precision, normally two significant figures. A precise
calculation with uncertain inputs is not a precise forecast.

## Market-Doc Write-Up

Do not add size intermediates to front matter. In *Market Definition*, state the contract. In
*Current View*, explain the current anchor and bottom-up reconciliation. In *Adoption Path*, show
the horizon revenue bridge and uncertainty alongside the penetration forecast.

For each material segment or revenue stream, provide a compact current-versus-horizon table:

| Driver | Current | 10-year | Basis |
|---|---:|---:|---|
| Addressable denominator | | | |
| Penetration | | | |
| Adopted base or flow | | | |
| Annual billable activity | | | |
| Net revenue per billable unit | | | |
| Annual market value | | | |

State the expected value, plausible range, dominant revenue stream, and largest sensitivities.
Reconcile the table totals to `size.current-market-value` and `size.maturity-market-value`.

## Back-Testing

Use the normal market-analysis back-test. When size misses, classify the error as market boundary,
addressable base, penetration handoff, billable activity, price/mix, recurring revenue, adjacency,
or currency translation. Change this methodology only when a failure mode plausibly generalizes
beyond one historical market.
