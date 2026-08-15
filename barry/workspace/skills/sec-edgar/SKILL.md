---
name: sec-edgar
description: Deep annual financial history from SEC EDGAR via the `edgar` CLI (JSON output, no API key) — 15+ years of revenue, margins and share count for US-listed filers. Use when Yahoo's 4-year statement cap is too shallow, e.g. reading a mature role model's long ramp for the TAM-capture valuation.
---

# SEC EDGAR

All data comes from the **`edgar`** CLI: source [scripts/edgar.py](scripts/edgar.py),
run via the `edgar` wrapper installed by
scripts/bin/install.sh. It is stdlib-only (SEC XBRL
over `urllib`) — no virtualenv, unlike `yfin`.

This tool exists for the one job Yahoo can't do: **long history**. [yfin](../yahoo-finance/SKILL.md)
caps its statements at 4 annual periods; `edgar` reads the SEC's XBRL company-facts
API for ~15+ years. It is **US-only** (EDGAR covers US filers) and **annual only** in
this first pass — use it for the deep series, and `yfin` for everything else (quotes,
the current snapshot, non-US names).

```bash
edgar income ADBE                     # curated annual income series, ~15+ yrs, newest first
edgar income ADBE -n 12               # keep the 12 most recent fiscal years
edgar income ADBE --fields "Revenue,Operating Income,Diluted Shares"
edgar metrics ADBE -n 10              # derived per-period margins + YoY revenue growth
edgar concept AAPL ResearchAndDevelopmentExpense   # raw series for any us-gaap tag
edgar cik CRM                         # resolve a ticker to its SEC CIK
```

Every command takes a US ticker as its first argument and prints JSON to stdout.
A ticker with no SEC filer errors as `{"error": "..."}` with a non-zero exit,
naming the US-only limitation.

`income` returns `{ticker, cik, title, periods: {period_iso: {line_item: value}}, _tags}`,
mirroring `yfin`'s statement shape (period keyed by fiscal-year-end, newest first) so
a caller can treat the two identically. Line items: `Revenue`, `Cost Of Revenue`,
`Gross Profit`, `Operating Income`, `EBITDA`, `Net Income`, `D&A`, `Diluted Shares`,
`Basic Shares`. `Gross Profit` falls back to `Revenue − Cost Of Revenue` and `EBITDA`
is derived as `Operating Income + D&A` (both `null` when an input is absent).

`_tags` records which `us-gaap` XBRL tag each line item resolved to. Tag choice
drifts across filers and over time (e.g. `Revenues` vs
`RevenueFromContractWithCustomerExcludingAssessedTax`), so each canonical item maps
to an ordered list of candidate tags and the first that carries data wins — the same
`first_present` discipline the trait scripts use for Yahoo's shifting names.

`metrics` derives `gross_margin`, `operating_margin`, `ebitda_margin`, `net_margin`,
and `revenue_growth` per period; run `edgar metrics <ticker> --list-fields` for the
definitions. `concept` is the escape hatch for any `us-gaap` tag not in the curated
set.

### Trimming output

- `--last` / `-n N` — keep only the N most recent fiscal years.
- `--fields` / `-f` — line items to keep (exact, case-insensitive; comma- or
  space-separated). Quote any name containing spaces, e.g. `--fields "Operating Income"`.
  Unmatched names come back under `_unmatched`. Available on `income` and `metrics`.
- `--list-fields` — print the selectable line items (and, for `metrics`, their
  definitions) without values.

## Notes

- **Annual, US, 10-K only.** Quarterly and balance-sheet concepts are out of scope
  for now; add a concept to `CONCEPTS` in [scripts/edgar.py](scripts/edgar.py) when a
  caller needs one. One value per fiscal year, taking the most recently filed
  (restated) figure on collisions.
- **User-Agent.** The SEC asks for a descriptive agent with a contact address; the
  default is set in the script and overridable via `EDGAR_USER_AGENT`.
- **Caching.** The ticker→CIK map and each company's facts are cached under
  `~/.cache/edgar-cli` (30-day and 1-day TTL); `--refresh` bypasses it.
- Its first consumer is `tam_capture_inputs` (the TAM-capture valuation), which pairs
  this deep history with a `yfin` snapshot — see
  [tam-capture.md](../stock-analysis/references/valuation/tam-capture.md).
