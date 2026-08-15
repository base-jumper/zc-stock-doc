---
id: organic-growth
name: Organic Growth over Acquisitive Growth
---

# Trait: Organic Growth over Acquisitive Growth

**What we're looking for:**
Growth that the company *built* rather than *bought*. The best compounders expand by winning
customers, launching products, and taking share with their own engine — not by repeatedly buying
revenue. This trait rewards organic, internally-generated growth and penalises companies that lean
on large or overpriced acquisitions to manufacture the appearance of growth.

It is a **quality-of-growth** trait, distinct from [Durable Growth](durable-growth.md), which asks
*whether* the engine is compounding. This trait asks *how* that growth was achieved. All else equal,
a company that grew revenue organically should score higher than one that grew the same amount
through M&A.

**Why this matters:**
Acquisitive growth is lower quality and riskier than organic growth. It often masks a stalling core
business, dilutes shareholders or piles on debt, carries integration risk, and accumulates goodwill
that can later be written down. Large deals especially tend to destroy value — the acquirer
overpays, synergies disappoint, and management attention is consumed by integration rather than the
core. Serial overpayment is a capital-allocation failure, even when reported growth looks healthy.
Recent examples of value-eroding mega-acquisitions include Intuit (Credit Karma / Mailchimp) and CSL
(Vifor) — both large, richly-priced deals that strained the balance sheet and underwhelmed.

**Small, sensible bolt-ons are fine — and can be a plus:**
This is not a blanket anti-M&A trait. Modest, on-strategy acquisitions that fill a genuine gap
(a tuck-in product, a key team, a geography) at a sensible price are normal, healthy capital
allocation and should not be penalised. The target is *giant* deals and *overpriced* deals, and
companies whose growth is fundamentally **dependent** on a steady diet of acquisitions (roll-ups).

**What to look at:**

* **Organic vs total growth** — does the company disclose organic (constant-currency,
  ex-acquisition) revenue growth, and how much of headline growth is left once acquired revenue is
  stripped out? A wide gap is the tell.
* **Deal size relative to the acquirer** — a deal worth a large fraction of the company's market cap
  or revenue is a bet-the-company move; many small bolt-ons are not.
* **Price paid** — multiples paid versus the target's growth/margins; premium over the undisturbed
  price; goodwill and intangibles created relative to the purchase price.
* **Funding** — was the deal funded by cash flow, a lot of new debt, or share issuance (dilution)?
* **Track record** — subsequent goodwill impairments, divestitures of past acquisitions, or
  restructuring charges are evidence of prior overpayment.
* **Strategic fit and dependence** — do the deals fit a coherent strategy, or is the company buying
  growth because the core has stalled?

If it can be shown conclusively that the company has **never made any acquisitions**, then a score of 
1 and confidence of 1 is appropriate.

**Key questions:**

* Strip out acquired revenue — is the core business still growing well on its own?
* Are acquisitions small, sensible bolt-ons, or large bet-the-company deals?
* Did management pay a sensible price, or overpay (rich multiples, big premiums, large goodwill)?
* How were the deals funded — internal cash, debt, or dilution?
* Has the company written down or unwound past acquisitions?

**Scoring guidance:**

* **0.70–1.00** Growth is overwhelmingly organic; any acquisitions are small, on-strategy bolt-ons
  bought at sensible prices and funded conservatively
* **0.40–0.69** A mix — meaningful organic growth alongside acquisitions, or a sizeable deal that
  was reasonably priced and well-integrated; M&A is a contributor but not the whole story
* **0.00–0.39** Growth is substantially manufactured through acquisitions, and/or one or more giant
  or clearly overpriced deals (rich multiples, large premiums, heavy goodwill, debt-/dilution-funded),
  and/or a history of acquisition write-downs

**Documentation:**

* Organic vs total revenue growth over recent periods, with source (or a note that the company does
  not disclose organic growth, and your best estimate)
* Material acquisitions in recent years: size relative to the acquirer, price/multiple paid, premium,
  goodwill created, and how each was funded — with source
* Any goodwill impairments, divestitures, or restructuring tied to past deals
* The reason for the score — why the growth is judged primarily organic vs bought, and how the deal
  sizes and prices factored in

## Script

Yahoo doesn't disclose organic (ex-acquisition) revenue, so
[`organic_growth.py`](../../scripts/organic_growth.py) gives the **M&A fingerprint** — the tracks
acquisitive growth leaves — via [`yfin`](../../../yahoo-finance/SKILL.md):

```bash
organic_growth CSL.AX              # 5 annual years (default); --years N
organic_growth CSL.AX --format json
```

Per year it shows revenue and its growth, **goodwill** and goodwill / total assets, acquisition cash
spend, and the diluted share count; the summary gives revenue CAGR, the goodwill-as-share-of-assets
trend, cumulative acquisition spend, and the share-count change (deals funded with stock show as
dilution). A heavy fingerprint — goodwill climbing, big acquisition outflows, rising share count — under
healthy headline growth is the tell that growth was *bought*. The clean organic figure, the prices/
multiples paid, and goodwill impairments need the filings (flagged in the output).
