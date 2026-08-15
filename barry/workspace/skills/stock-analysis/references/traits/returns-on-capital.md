---
id: returns-on-capital
name: High, Durable Returns on Capital
---

# Trait: High, Durable Returns on Capital

**What we're looking for:**
The business earns a **high return on the capital it employs**, and has **kept earning it** year
after year. This is the single best quantitative signal of a wonderful business: a company that
earns, say, 20%+ on capital employed and sustains it is creating value with every dollar it
retains, and — given somewhere to reinvest — compounds intrinsic value at roughly that rate. It is
Terry Smith's first screen ("buy good companies" *means* high-return-on-capital companies) and the
arithmetic behind Buffett's preference for businesses that "earn good returns on capital while
employing little of it."

Two things must both be true:

| Dimension | What it means | Why it matters |
|---|---|---|
| **High** | Return on capital well above the cost of capital — not merely positive (see *Putting numbers on "high"* for the thresholds) | Below the cost of capital, growth *destroys* value; only a wide spread above it compounds wealth |
| **Durable** | That return has persisted across years and a cycle — stable or rising, not eroding | A high return that fades is a moat leaking; a high return that holds is the fingerprint of a real one |

**The quantitative fingerprint of a moat.**
This trait is the *measurable evidence* for the moat that the [Pricing Power](pricing-power.md) trait
describes *qualitatively*. Capitalism's default is that high returns attract competition and get
competed away; a business that earns high returns **and keeps them for years** is telling you,
in numbers, that something is defending it — pricing power, scale, switching costs, brand. The moat
trait asks *why* the returns persist; this trait checks *that* they do.

**Pick the right metric for the business:**

| Business type | Primary metric | Note |
|---|---|---|
| **Most operating companies** | **ROIC** or **ROCE** | Return on *all* capital (debt + equity), so leverage can't flatter it |
| **Capital-light (software, brands, services)** | ROIC / ROE, judged qualitatively | Capital employed can be tiny or negative — read the economics, not just the ratio |
| **Capital-intensive (industrial, utility)** | ROCE including the full asset base | The whole point is whether heavy capital earns its keep |
| **Banks / insurers / financials** | **ROE / ROTE** (return on tangible equity) | Here capital *is* the product; use tangible equity to strip goodwill |

**Putting numbers on "high":**
Use these as **default anchors for a typical operating company** (ROIC/ROCE). They are a practical
starting point, not a mechanical rule — the real test is always the **spread over the company's own
cost of capital**, and two business types read off a different scale (see below).

| Reading | ROIC / ROCE (operating co.) | Spread over cost of capital |
|---|---|---|
| **High** (0.70–1.00) | **≥ ~20%** sustained | wide — roughly ≥ 8–10 pts above WACC |
| **Decent / mixed** (0.40–0.69) | **~12–20%** | positive but modest |
| **Poor** (0.00–0.39) | **< ~12%**, or fading toward WACC | ≤ 0 — at or below the cost of capital |

* **The spread is the backbone, not the absolute number.** A 15% ROIC is excellent for a stable
  utility funded at 6%, but mediocre for a volatile business whose cost of capital is 12%. When the
  absolute figure and the spread disagree, lead with the spread.
* **Financials read off their own scale.** Judge a bank/insurer on **ROTE**, where roughly **≥ 15%**
  is strong — do not hold it to the 20% operating-company bar.
* **Capital-light businesses can break the ratio.** Where invested capital is tiny or negative the
  percentage explodes and stops being meaningful; fall back to the qualitative read and the cash
  economics rather than a literal number.

**Watch for the two classic distortions:**

* **Leverage flattering ROE** — a mediocre operating business can post a high *return on equity*
  simply by piling on debt. Always check the unlevered picture (ROIC/ROCE); a high ROE built on a
  thin, heavily-geared equity base is not the quality signal it looks like.
* **Goodwill from acquisitions** — a serial acquirer can show low ROIC *including* goodwill yet high
  returns *excluding* it (or vice versa). Look at both: returns on tangible operating capital reveal
  the underlying economics; returns including goodwill reveal whether management *overpaid* for them.

**Average vs incremental:**
The historical average tells you the quality of the capital already in the ground. What the business
earns on **incremental** capital — the recent, marginal dollars — is the forward-looking signal of
whether reinvestment is *still* high-return. A company whose incremental returns are falling is
maturing even if its average still looks pristine. (Whether there is *room* to keep reinvesting at
these returns is a separate question — the reinvestment-runway trait — this trait is about the *rate*
earned, not the runway.)

**Key questions:**

* What does the business earn on capital (ROIC/ROCE, or ROTE for financials), and is it comfortably
  above its cost of capital?
* Has that return persisted across the last 5–10 years and through a downturn — stable, rising, or
  eroding?
* Are these genuine operating returns, or is ROE flattered by leverage?
* Does acquisition goodwill distort the picture — and what is the underlying return on tangible
  operating capital?
* What is the business earning on *incremental* capital lately — is reinvestment still high-return?

**Scoring guidance:**

(What counts as **high** / **decent** / **poor** is defined once in *Putting numbers on "high"*
above — those thresholds carry the numbers; the bands below describe the *quality* read.)

* **0.70–1.00** **High** returns on capital that are durable — stable or rising across the cycle;
  genuine operating returns, not leverage-driven; incremental returns still high.
* **0.40–0.69** **Decent** returns that create some value but are unspectacular, **or** high returns
  that are visibly eroding, **or** a picture muddied by leverage or goodwill where the true return is
  ambiguous.
* **0.00–0.39** **Poor** returns — at or below the cost of capital, so the business doesn't create
  value per dollar reinvested — or apparent high returns that are an accounting illusion (leverage,
  distortions) masking poor underlying economics.

**Documentation:**

* The metric(s) chosen (ROIC / ROCE / ROTE) and why they fit this business type
* The level over 5–10 years versus the cost of capital, with source — and the trend (stable / rising /
  eroding) across a cycle
* Any leverage adjustment (ROE vs ROIC) and any goodwill adjustment (returns including vs excluding
  goodwill), with what each reveals
* Evidence on incremental / recent returns on capital, where available
* The reason for the score — why the returns are judged high and durable (or not), and how the
  distortions were handled

## Script

[`returns_on_capital.py`](../../scripts/returns_on_capital.py) pulls the per-period ROIC / ROCE / ROE /
ROA that [`yfin metrics`](../../../yahoo-finance/SKILL.md) computes and layers on the trait's reads:

```bash
returns_on_capital MSFT            # 10 annual years requested (Yahoo serves ~4); --years N
returns_on_capital MSFT --format json
```

Per year it shows the four return ratios, the **ROE-minus-ROIC gap** (the leverage-distortion check — a
wide positive gap means debt is flattering ROE, not operating quality) and **goodwill / invested
capital** (the acquisition-distortion flag). The summary adds the window-average ROIC, its trend, and
**incremental ROIC** (ΔNOPAT / ΔinvestedCapital — whether recent capital still earns the headline rate).
It does not judge whether the level is *high*: that is the spread over this company's cost of capital,
which Yahoo doesn't carry — read the level against WACC and the bands above yourself.
