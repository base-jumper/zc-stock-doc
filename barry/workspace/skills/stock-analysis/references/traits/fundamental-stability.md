---
id: fundamental-stability
name: Fundamental Stability / Secular Durability
---

# Trait: Fundamental Stability / Secular Durability

**What we're looking for:**
Confidence that the business's fundamentals are **durable** — that its earning power, and the assets
and cash flows behind it, is **not being structurally eroded**. The enemy is the **melting ice cube**:
a business in secular, permanent decline from obsolescence, disruption, substitution, or a lasting
loss of demand. We do **not** need growth — we need the fundamentals to *hold*. Stability fully meets
the trait; the only thing that fails it is structural decay.

The question reads the same regardless of where the business starts from:

* For a business whose fundamentals have **already fallen**, ask whether the decline has *arrested* and
  its cause is non-structural — so the floor holds rather than keeps sinking. (This is the classic
  **value trap** guard: cheap for a reason, and getting cheaper.)
* For a business whose fundamentals are **currently healthy**, ask whether they will *persist* —
  whether a structural threat is gathering that would erode them while we own it.

Both reduce to one diagnosis — classify the trajectory of the fundamentals as:

* **(a) cyclical / temporary / self-correcting** — a trough or wobble that mean-reverts;
* **(b) a one-off shock the market is over-extrapolating** — a single event priced as if permanent; or
* **(c) structural / secular decline** — underway or credibly impending: the melting ice cube.

We want **(a)** or **(b)** — or a healthy business with no structural threat in sight. We avoid
**(c)**, where the earning power keeps eroding no matter the price paid or the time allowed.

**Key questions:**

* Is the earning power currently stable, deteriorating, or recovering — and what does the recent trend
  in the operating fundamentals (volumes, margins, churn, occupancy, orders, leading indicators) show?
* If fundamentals have weakened, why? Is the cause cyclical, one-off, or structural?
* If fundamentals look healthy, what could structurally erode them — disruption, obsolescence,
  substitution, secular demand loss, regulation — and is there evidence that erosion has begun?
* Is there a credible path for the earning power (or NAV / dividend / cash stream) to keep falling over
  our horizon?
* What would have to be true for the fundamentals to persist (or recover), and is that credible?

**Scoring guidance:**

* **0.70–1.00** Durable fundamentals: currently stable or healthy with no structural threat in sight,
  **or** a decline that has clearly arrested for a cyclical/one-off reason. The earning power is not
  eroding.
* **0.40–0.69** Mixed — stabilising but unproven, continued softness with a credible but not-yet-
  visible recovery, or a healthy business facing a real but not-yet-biting structural threat.
* **0.00–0.39** Structural / secular decline underway or clearly impending — a melting ice cube whose
  earning power keeps eroding.

**Documentation:**

* The current trajectory of the fundamentals (stable / deteriorating / recovering), with the operating
  evidence behind it
* Where there is weakness: the diagnosed cause, classified cyclical / one-off / structural, with reasoning
* Where fundamentals are healthy: the main structural threats considered, and why they are (or aren't)
  a danger over the horizon
* The verdict — whether the earning power is judged durable, and what evidence would change that read

## Script

[`fundamental_stability.py`](../../scripts/fundamental_stability.py) lays out the one quantitative input
to this otherwise-diagnostic trait — the trajectory of the fundamentals — via
[`yfin`](../../../yahoo-finance/SKILL.md):

```bash
fundamental_stability INTC         # 5 annual years (default); --years N
fundamental_stability INTC --format json
```

The series shows revenue, gross / operating / net margin, diluted EPS and FCF year by year; the **erosion
read** then gives, for revenue, operating margin, EPS and FCF, how far the latest figure sits below its
window peak and the direction. A long way off peak on every line and still falling is the melting ice
cube; near peak and steady is stable. *Why* it is falling — cyclical, one-off, or structural — is the
agent's diagnosis from operating evidence Yahoo doesn't carry.
