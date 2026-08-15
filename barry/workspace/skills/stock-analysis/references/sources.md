---
id: sources
name: Sourcing Information
---

# Sourcing Information

Where we do and don't get information when researching a stock, and how to read it. The
[stock-analysis skill](../SKILL.md) leans on this doc whenever it gathers evidence — every fact in a
stock-doc should be traceable to a source that belongs on the "trusted" side of this page.

## The one rule that overrides everything: facts, not sentiment

When reading **any** article, post, transcript, or report, deliberately **discard the author's
sentiment** and keep only the hard information. We form our own predictions and conclusions from the
underlying facts — we do not absorb someone else's mood, conviction, or price target as if it were
data.

In practice:

- **Extract the verifiable.** Numbers, dates, named events, quoted guidance, contracts, product
  launches, management statements, regulatory actions. These are the raw material.
- **Drop the adjectives.** "Blockbuster quarter", "disappointing", "stock to buy now", "crushing it",
  "in trouble" — these are the author's feelings, not information. Strip them out before the
  information enters our notes.
- **Re-derive the conclusion yourself.** If an article says a company is a "screaming buy", ignore the
  verdict and ask: what facts did they cite, are those facts true, and what do *we* conclude from
  them? Often the facts support a more measured view than the headline.
- **Attribute opinion as opinion.** If another party's *view* is itself the fact worth recording (e.g.
  an analyst downgrade that moves the stock, a short-seller's thesis), record it as "X claims Y",
  noting it is a claim and who is making it — never restate it as established truth.
- **Watch for incentives.** Sell-side notes, company IR material, influencers, and anyone with a
  position have reasons to spin. The more someone wants you to feel something, the harder we separate
  their facts from their framing.

This rule is why the source hierarchy below matters: the closer we get to primary documents, the less
sentiment there is to strip in the first place.

## Source hierarchy

### Tier 1 — Primary sources (strongly preferred)

Go here first. These are the company's own words and the official record, with the least
interpretation layered on top.

- **Annual reports** (10-K / 20-F / annual report & accounts) — the most complete picture of the
  business, risks, and audited financials.
- **Quarterly reports** (10-Q / interim reports) — the freshest audited-ish financial detail.
- **Earnings releases** — the headline numbers and management's framing of the quarter.
- **Earnings call transcripts** — management's answers to unscripted analyst questions; often the
  richest source of forward-looking detail. (Strip the sentiment, keep the substance.)
- **Stock exchange announcements / regulatory filings** — material disclosures, contracts, director
  dealings, capital raises, M&A. The official, legally-accountable record.
- **Investor presentations & investor-day decks** — useful for strategy and segment detail; remember
  these are curated by IR, so they are primary *facts* wrapped in company *framing*.
- **Prospectuses / shareholder circulars** — for IPOs, rights issues, and major transactions.

### Tier 2 — Reputable data & reporting

Trusted for aggregated data, market prices, and factual reporting. Use to corroborate and to fill
gaps Tier 1 doesn't cover. Prefer them for *numbers and events*, not for their *opinions*.

- **Yahoo Finance via the `yf` CLI** — current and historical prices, dividends, corporate actions,
  calendar, and holders. See the [yahoo-finance skill](../../yahoo-finance/SKILL.md). This is our
  go-to for market data and ticker checks.
- **Company IR websites** — the canonical home for the Tier 1 documents above; reach them by web.
- **Official exchange sites and filings indexes** — e.g. SEC EDGAR, ASX announcements, company
  registries. The authoritative index of Tier 1 filings.
- **Established financial press** for factual reporting (not the op-eds): Reuters, Bloomberg, the
  Financial Times, the Wall Street Journal, The Economist. Read for the *what happened*, discard the
  *what to feel*.

### Tier 3 — Use with care

Can be valuable, but treat as leads to verify against Tier 1/2 — never as standalone evidence.

- **Sell-side analyst notes** — useful for the data and models they expose; their ratings and price
  targets are opinion and incentive-laden. Record as "analyst claims", not fact.
- **Reputable independent research / newsletters** — judge case by case; keep only the facts and
  re-derive conclusions.

### Tier 4 — Avoid as evidence

Do not base any score, valuation input, or thesis point on these. At most they are signals of what
the crowd is talking about — and even then, only the verifiable facts within them count.

- Anonymous forums, stock-promotion sites, and hype channels (Reddit/Stocktwits crowds, "hot stock"
  blasts, pump newsletters).
- Social media posts presented without primary backing.
- Anything whose primary purpose is to make you *feel* bullish or bearish rather than to inform.
- Generative summaries of unknown provenance, and content we cannot trace back to a real source.

## Customer-voice sources (for the Customer Devotion trait)

Gauging how much customers love a product (the [Customer Devotion](traits/customer-devotion.md)
trait) draws on a distinct family of sources. The hard *quantitative* signals — net revenue
retention, logo churn, renewal and expansion rates, reported NPS — come from the Tier 1 filings,
earnings calls, and investor decks above; look there first. The platforms below add the qualitative,
third-party customer voice that those documents lack. They are customer sentiment by nature, so the
[facts-not-sentiment rule](#the-one-rule-that-overrides-everything-facts-not-sentiment) applies
hard: keep the **aggregate rating and review volume** (and the trend in both), and discard
individual reviews' adjectives.

- **Verified B2B peer-review platforms** — G2, Gartner Peer Insights, TrustRadius, Capterra. Tier 2
  for the *aggregate* score and review count, because reviewers are identity-verified; the real
  signal is a high rating held across a *large, growing* review base, not a handful of glowing
  entries.
- **App-store ratings** — Apple App Store and Google Play. Tier 2 for the aggregate star rating and
  review volume of a consumer app; watch for rating resets after major releases.
- **Open consumer-review sites** — Trustpilot and similar. Tier 3 at best: largely unverified and
  readily gamed in both directions. Use only to corroborate a picture the verified sources already
  show.

Treat any single platform as one data point. Devotion is credible when *independent* sources agree —
e.g. high NRR in the filings *and* a strong, deep peer-review standing.

## Citing sources

- Record the source for every material fact, ideally as a link, with an **as-of date** where the
  fact, price, or valuation depends on timing.
- Name the document type (e.g. "FY2025 10-K", "Q3 FY2026 earnings call transcript") so the next
  update can find it again.
- When a claim is opinion, cite it as opinion and name who holds it.
- These citations land in the stock-doc's **Sources** section (see the [stock-analysis
  skill](../SKILL.md)).
