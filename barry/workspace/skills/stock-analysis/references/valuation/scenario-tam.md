---
id: scenario-tam
name: Scenario-TAM Valuation (probability-weighted)
script: ../../scripts/scenario_tam_valuation.py
---

# Valuation method: Scenario-TAM

Estimates the **expected annualized ROI** of an early-stage company by probability-weighting **up to
four outcome scenarios** — `failure`, `niche-survivor`, `it-works`, `blue-sky` — each valued with the
[tam-capture](tam-capture.md) terminal build. It exists because tam-capture alone prices only the
survivor's path: its role model made it, so its ROI is the *"it works" case*, not an expectation. This
method keeps that case as one scenario and surrounds it with the outcomes the survivor's cohort
actually experienced, most of which end near zero. The result is an honest expected return, comparable
across risk levels with the other methods' ROIs.

The weighting happens in **terminal-value space, then annualizes once**:

```
E[terminal_price] = Σ pᵢ · terminal_priceᵢ
expected ROI      = (E[terminal_price] ÷ price)^(1/years) − 1
```

Never average the per-scenario ROIs — wealth compounds on terminal values, and rates don't mix
linearly: a −100% outcome can never drag a rate average below −100%/yr no matter how much
probability sits on it, and because annualization is concave, `Σ pᵢ·roiᵢ` understates the return on
expected wealth (Jensen's inequality). A −100% outcome and a +18%/yr outcome must be combined as
terminal wealth, not as rates.

## Applicability

Applies wherever [tam-capture](tam-capture.md) applies — the early-stage, growth-first profile valued
on a future market rather than today's earnings — and **supersedes it as the headline lens** there,
because it prices the downside tam-capture explicitly excludes. It additionally needs a credible read
on the *failure* and *niche* outcomes (see below), which is rarely the binding constraint: every
industry has more sub-scale survivors than giants. Use bare tam-capture only as the single-scenario
engine inside this method, or for a quick "what does the bull case pay" sanity check.

## How it plugs in

Standard contract (see the [SKILL](../../SKILL.md), *Estimating ROI*): the **stock-doc holds the
inputs**, the **script writes `roi` and `date` back** into `valuation.scenario-tam`. It is an
available method but is not currently wired into any strategy — [rule-breakers](../strategies/rule-breakers.md)
values its candidates with [tam-capture](tam-capture.md) directly (via
[weighted-average](weighted-average.md)). To use this method for a company, add it as a
`weighted-average` component in that stock-doc.

### Front-matter contract

```yaml
valuation:
  scenario-tam:
    price: 0.155             # entry price per share (today) — the ROI denominator
    shares: 2419.8e6         # today's diluted share count
    years: 8                 # holding period to maturity — one horizon for all scenarios
    tam: 25e9                # base maturity-year TAM (at now+years) — scenarios may override
    net-debt: 0              # terminal net debt (negative = net cash). Default 0
    scenarios:
      failure:               # probability omitted -> residual: 1 − Σ(other probabilities)
        terminal-equity: 20e6      # residual value: cash less wind-down, or an IP/asset sale
      niche-survivor:
        probability: 30%
        capture: 0.4%
        margin: 10%
        margin-basis: EBIT
        exit-multiple: 20
        dilution: 10%              # scalar or per-year list, like tam-capture
        role-model: CEVA
      it-works:
        probability: 7%
        capture: 2%
        margin: 42%
        margin-basis: EBIT
        exit-multiple: 20
        dilution: 6%
        role-model: RMBS
      blue-sky:              # optional — omit when merged into it-works (see below)
        probability: 0.5%
        tam: 40e9                  # boundary override: the expanded market this ending implies
        capture: 4%                # measured against this scenario's own tam
        margin: 43%
        margin-basis: EBIT
        exit-multiple: 20
        dilution: 6%
        role-model: ARM
    roi: 0.0                 # written by the script — do not hand-edit; re-run instead
    date: 2026-07-08         # written by the script — the valuation's as-of date
```

`price`, `shares`, `years`, and `net-debt` are shared: every scenario is the same company over the
same horizon. `tam` is the **base boundary** every scenario defaults to; a scenario may override it
with its own `tam` where its ending implies a different market (see *Scenario TAMs* below). Each
scenario then carries either the tam-capture inputs (`capture`, `margin`, `margin-basis`,
`exit-multiple`, `dilution`, `role-model`, optionally `tam`) or a direct `terminal-equity` (the usual
form for `failure`). Scenario names are fixed to the four above; `failure` and `it-works` are
required, and the base `tam` may be omitted only when every TAM-built scenario carries its own.

## The scenarios and their role models

A scenario is a reference-class question — *which real company does the subject resemble in this
ending?* — so each gets its **own role model** where a real analogue exists, rather than one
survivor's numbers scaled up or down. Economics are not scale-invariant: a sub-scale company doesn't
have "the giant's margin, but less", it has a structurally different margin (fixed costs barely
amortized) and multiple (no growth premium). Read those off a real sub-scale company instead of
guessing. Everything [tam-capture](tam-capture.md) says about reading a role model — stage alignment, the
own-TAM `capture` rule (its revenue over its *own* TAM, never the subject's), margin/multiple
consistency — applies per scenario.

- **failure** — no role model, no TAM arithmetic: a direct `terminal-equity` anchored on what failed
  peers actually fetched (asset/IP sale, acqui-hire, or liquidation ≈ cash minus wind-down). Per
  share it usually rounds to near zero, because the path to failure runs through a final desperate
  raise first.
- **niche-survivor** — the mature company in the same industry that survived but never escaped
  sub-scale. Because every industry produces far more of these than giants, this is often the
  best-evidenced scenario in the set.
- **it-works** — the thesis case: the subject becomes a **successful, established mid-scale player**.
  Role model: a real company that made it comfortably past sub-scale without becoming the category
  giant, read at its real economics.
- **blue-sky** — the subject becomes the **category giant** — a distinct role model, again read at its
  actually-achieved economics. The ceiling must be a *real* company, never a hypothetical grander one
  (that is the door narrative inflation walks through); capping the top scenario at what a real
  company demonstrably did truncates the power-law tail at a defensible height. This is also the
  scenario that usually earns a `tam` override — see *Scenario TAMs* below.

**Merged fallback:** if the industry offers no two distinct upper anchors — no real mid-scale success
separate from the giant — omit `blue-sky` and give `it-works` a single role model that **sits between
the two**, carrying their **combined** probability. The tail is then truncated at that scenario — make
sure its probability reflects the merged mass.

### Scenario TAMs

TAM is **conditional on the outcome**, not a fact about the industry: each scenario's market is
really *the TAM given that ending*, and the endings differ. The world in which the technology
matures, gets cheap, and goes mainstream is largely the same world in which the company wins big —
market size and outcome are correlated, not independent. So a scenario may carry its own `tam`. In
practice `failure` needs none, `niche-survivor` and `it-works` usually share the base boundary, and
**blue-sky is the usual override**: don't size it from the currently obvious market, but from what
that market could become through the two channels that actually produce category giants — the market
itself **growing as the technology matures** and gets affordable, and the **adjacent markets** the
company could expand into from its initial niche.

The existing disciplines carry over per boundary. Every `tam` — base or override — is the
**maturity-year** market at now + `years`, sized per [tam-capture](tam-capture.md)'s rule (today's
market is only the starting point of that projection). Each scenario's `capture` must be measured
against *its own* `tam`, and an expanded boundary must be anchored on something real — the natural
anchor is the market the scenario's role model actually came to address, which for a category giant
is rarely the niche it started in — never a market invented for the thesis. State in the write-up
which lever each override turns: a bigger market, a bigger share, or both. A blue-sky that cranks
both at once is where narrative inflation now enters and deserves extra scrutiny; the tail-α check
operates on terminal equity, so it polices the *combined* effect however it is split.

**Dilution: role model as anchor, runway math as floor.** Destination economics are read off the role
model, but dilution is partly a *path* property — a subject burning cash today will issue shares in
every scenario, and in the niche path it issues from weakness for years. Start from the role model's
historical share-count growth, check it against the subject's own runway arithmetic (cash ÷ burn →
raises forced before breakeven), and take the **more dilutive** of the two. Expect the asymmetry
`niche-survivor > it-works ≥ blue-sky`; getting it right is a big part of why surviving-but-sub-scale
can still lose shareholders money.

## Choosing the probabilities

Probabilities are per-outcome-at-the-horizon: mutually exclusive, exhaustive. Two disciplines keep
them from becoming vibes: start from the **outside view** (research base rates), then adjust with a
**stage-gate decomposition** the write-up can defend.

### Base-rate starting points

The empirical outcome distribution for young companies is brutally skewed:

- **65% of 21,000+ venture financings (2004–13) returned less than 1×; only ~10% returned ≥5× and ~4%
  ≥10×** — Correlation Ventures data, via [Seth Levine, *Venture Outcomes are Even More Skewed Than
  You Think* (2014)](https://sethlevine.com/archives/2014/08/venture-outcomes-are-even-more-skewed-than-you-think.html).
- The skew survives listing: **~57% of all US stocks since 1926 have lifetime returns below one-month
  T-bills** (the median lifetime return is negative), and **the best-performing 4% account for the
  entire net wealth creation of the market** — [Bessembinder, *Do Stocks Outperform Treasury Bills?*,
  JFE 2018](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2900447).

Synthesized into starting bands by maturity (derived anchors, not quotes from the studies). These are
starting points, not limits: the final probabilities are a judgement call, and the specific case may
warrant landing outside a band in either direction. When it does, say why in the write-up — the
deviation should be a conscious, recorded decision, not a silent one:

| Stage at entry                                        | failure | niche-survivor | it-works | blue-sky |
| ----------------------------------------------------- | ------- | -------------- | -------- | -------- |
| Listed, pre-meaningful-revenue, loss-making           | 45–70%  | 20–35%         | 5–15%    | 1–3%     |
| Commercial traction (revenue scaling, still burning)  | 30–50%  | 25–40%         | 10–25%   | 2–5%     |
| Profitable, growth-stage                              | 15–35%  | 30–45%         | 20–35%   | 3–8%     |

The trait scores already in the stock-doc should point the same direction — weak
[downside-support](../traits/downside-support.md) and
[fundamental-stability](../traits/fundamental-stability.md) argue for the top of the failure band, a
proven [durable-growth](../traits/durable-growth.md) engine for a lower one. A contradiction between
the probabilities and the traits is a sign one of them is wrong.

### Stage-gate decomposition

Estimate `P(it-works)` as a product of conditional gates the analysis has already researched — e.g.
*technology proven in production* × *design wins convert to volume* × *revenue reaches the terminal
build before cash runs out* × *holds share against incumbents*. Multiplying three or four honest
40–70% conditionals lands in the single digits to low teens naturally, and each factor is citable.
Then let **failure be the residual**: reason about the positive outcomes explicitly and omit
`failure.probability`, and the script computes `1 − Σ(others)`.

### Tail consistency

Large-outcome frequencies follow a power law with tail exponent **α ≈ 2** ([Othman, *Startup Growth
and Venture Returns*, AngelList 2019](https://angel.co/pdf/growth.pdf) finds winning early-stage
investments draw from an α < 2 tail). Under `P(V ≥ x) ∝ x^−α`, a scenario at k× the terminal value
should be roughly k² less probable: blue-sky at ~3× it-works' terminal equity should carry around a
ninth of its cumulative probability. The script computes the implied α from your scenarios and warns
outside ~1.5–3.0 — below it you are assuming a fatter tail than venture history supports; justify it
explicitly or fix the probabilities.

## Running the script

Do the maths with the script — never by hand. It mirrors the other valuation scripts' interface.

```bash
SCRIPT=skills/stock-analysis/scripts/scenario_tam_valuation.py

# Stock-doc mode: read valuation.scenario-tam inputs, write valuation.scenario-tam.roi back.
"$SCRIPT" --stock-doc BRN.AX
"$SCRIPT" --stock-doc BRN.AX --dry-run --format json    # preview without writing

# Raw mode: shared inputs as flags, one --scenario per outcome (key=value pairs;
# use '|' for per-year dilution lists, e.g. dilution=8%|6%|4%).
"$SCRIPT" --price 0.155 --shares 2419.8e6 --years 8 --tam 25e9 \
    --scenario "failure,terminal-equity=20e6" \
    --scenario "niche-survivor,probability=30%,capture=0.4%,margin=10%,margin-basis=EBIT,exit-multiple=20,dilution=10%,role-model=CEVA" \
    --scenario "it-works,probability=13%,capture=2%,margin=25%,margin-basis=EBIT,exit-multiple=18,dilution=6%,role-model=ARM" \
    --scenario "blue-sky,probability=2%,tam=40e9,capture=4%,margin=35%,margin-basis=EBIT,exit-multiple=20,dilution=6%,role-model=ARM"
```

`--hurdle` (default 10%) sets the required return used by the breakeven output below.

## Reading the output

- **Expected annualized ROI** (`valuation.scenario-tam.roi`) — the headline. Because it is a true
  expectation it runs structurally lower than tam-capture's "it works" ROI; that is the point, and it
  is what makes it comparable with the other strategies' methods.
- **Scenario table** — each outcome's probability, TAM boundary, terminal equity, per-share value,
  standalone ROI, and **contribution to the expectation**. Expect most of the expected value to sit in low-probability
  scenarios; the script warns when a single sub-10% scenario contributes over half.
- **P(below entry)** — total probability of ending under today's price. For an early-stage company
  this is usually well over half even when the expected ROI is attractive; state it in the write-up.
- **Implied tail α** — the tail-consistency check above.
- **Market-implied breakeven** — the `P(it-works)` that, against the failure outcome alone, the
  current price needs to clear the hurdle. Comparing "the market needs X%" with "our stage-gates say
  Y%" is the single most decision-useful line: it turns the valuation into a disagreement you can
  argue about.

Feed the result into the stock-doc **Valuation** section: the scenario table with each role model and
why it fits, the probability reasoning (stage-gates, the band used and why), the expected ROI,
P(below entry), and the breakeven comparison. The probabilities are the load-bearing inputs — cite
their basis.
