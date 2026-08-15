# RF1.AX / LSF.AX entry monitor

Purpose: daily lightweight check for whether Nick should put money to work in RF1.AX or LSF.AX over the next 1-2 months. The attractiveness work is front-loaded here so the scheduled run mainly checks current price versus stored percentile thresholds.

## Run cadence

- Cron: weekdays 18:00 Australia/Perth.
- Normal output: silence / `NO_REPLY` when neither fund is attractive enough.
- Alert Nick only when the current premium/discount is in the **lowest/cheapest 35%** of the last six months of observed price-to-NAV/NTA gaps, or when source data is stale/broken enough to need attention.

## Source hierarchy

### Prices

Use `yfin quote RF1.AX` and `yfin quote LSF.AX` for current/delayed market prices. If yfin fails, use ASX pages:

- RF1 ASX: https://www.asx.com.au/markets/company/RF1
- LSF ASX: https://www.asx.com.au/markets/company/LSF

### NAV / NTA

Prefer primary fund-manager/ASX-announcement sources.

RF1:
- ASX announcements page: https://www.regalfm.com/regal-investment-fund-ASX-RF1/ASX-Announcements
- Fund page: https://www.regalfm.com/regal-investment-fund-ASX-RF1
- Current baseline source: RF1 weekly NAV estimate released 10 Aug 2026 for 7 Aug 2026: NAV per unit **$3.54**.
- Supporting monthly source: RF1 June 2026 newsletter: June NAV **$3.67**.

LSF:
- Primary daily source: ASX current-day announcements at https://www.asx.com.au/asx/v2/statistics/todayAnns.do; find the `LSF` row titled “Net Tangible Asset Backing”, follow its `displayAnnouncement.do` link, then read the direct ASX PDF URL from the `pdfURL` form field. On non-trading days or before the morning release appears, fall back to https://www.asx.com.au/asx/v2/statistics/prevBusDayAnns.do.
- Fund page/monthly reports (fallback only): https://www.l1.com.au/investments/l1-capital-long-short-fund/l1-long-short-fund-limited/
- Current baseline source: LSF ASX daily NTA announcement released 13 Aug 2026 for 10 Aug 2026: NTA before tax **$4.5367**, NTA after tax **$4.1508**.
- For entry monitoring, use **before-tax NTA** as the primary valuation anchor because it best reflects portfolio value before deferred tax on unrealised gains/losses; use after-tax NTA as the conservative floor in any alert.

## Historical premium/discount baseline

Built 2026-07-15 from six monthly primary-source samples, Jan-Jun 2026. Prices are `yfin history` closes on or before each month-end; NAV/NTA values are from fund-manager monthly reports. Detailed data is stored in `tasks/rf1-lsf-discount-history.json`.

Formula: `premium_discount = price / NAV_or_NTA - 1`. Lower is cheaper. The alert threshold is the **35th percentile** of the observed six-month distribution, i.e. current gap must be at or below that cutoff to be in the cheapest 35%.

### RF1.AX six-month gaps

| Month | Price date | Price | NAV | Premium/(discount) |
| --- | --- | ---: | ---: | ---: |
| 2026-01 | 2026-01-30 | $3.600 | $3.750 | -4.00% |
| 2026-02 | 2026-02-27 | $3.400 | $3.740 | -9.09% |
| 2026-03 | 2026-03-31 | $3.330 | $3.550 | -6.20% |
| 2026-04 | 2026-04-30 | $3.470 | $3.680 | -5.71% |
| 2026-05 | 2026-05-29 | $3.390 | $3.720 | -8.87% |
| 2026-06 | 2026-06-30 | $3.440 | $3.670 | -6.27% |

RF1 six-month stats: min **-9.09%**, average **-6.69%**, max **-4.00%**, 35th-percentile cutoff **-6.92%**.

### LSF.AX six-month gaps

| Month | Price date | Price | NTA before tax | NTA after tax | Premium/(discount) vs before-tax NTA |
| --- | --- | ---: | ---: | ---: | ---: |
| 2026-01 | 2026-01-30 | $4.151 | $4.390 | $3.940 | -5.44% |
| 2026-02 | 2026-02-27 | $4.348 | $4.330 | $3.910 | +0.41% |
| 2026-03 | 2026-03-31 | $3.917 | $3.860 | $3.640 | +1.49% |
| 2026-04 | 2026-04-30 | $4.086 | $4.110 | $3.810 | -0.58% |
| 2026-05 | 2026-05-29 | $4.453 | $4.380 | $4.010 | +1.67% |
| 2026-06 | 2026-06-30 | $4.720 | $4.320 | $3.950 | +9.26% |

LSF six-month stats: min **-5.44%**, average **+1.13%**, max **+9.26%**, 35th-percentile cutoff **+0.16%**.

## Entry thresholds

### RF1.AX

- **Alert / buy-zone threshold:** current premium/discount must be **<= -6.92%** versus latest NAV.
- Using latest weekly NAV **$3.54**, that implies a current-price trigger of about **$3.30 or lower**.
- If a newer NAV is found, recompute trigger as `latest_NAV * (1 - 0.0692)`.
- Do **not** alert merely because RF1 trades at a small discount; the historical six-month cutoff is much cheaper than the current small discount.

### LSF.AX

- **Alert / buy-zone threshold:** current premium/discount must be **<= +0.16%** versus latest before-tax NTA.
- Using latest daily before-tax NTA **$4.5367**, that implies a current-price trigger of about **$4.54 or lower**.
- If a newer before-tax NTA is found, recompute trigger as `latest_before_tax_NTA * (1 + 0.0016)`.
- In any alert, also show premium/discount versus after-tax NTA as the conservative view.

## Daily run instructions

1. Fetch current prices:
   - `yfin quote RF1.AX`
   - `yfin quote LSF.AX`
   - Run these as two separate commands; `yfin quote` accepts only one ticker per invocation.
2. Check for a newer NAV/NTA source than the baseline:
   - RF1: open the Regal ASX announcements page and look for the latest “Weekly NAV Estimate” or latest monthly newsletter.
   - LSF: check the ASX current-day announcements endpoint for the morning “Net Tangible Asset Backing” release. Use the latest daily NTA announcement, not the monthly fund report. Fall back to the previous-business-day endpoint if today's release is not yet available.
3. If a newer NAV/NTA is available, use it for today’s calculation and update this file’s baseline values after the run if practical.
4. Compute premium/discount versus the relevant anchor:
   - RF1: latest NAV per unit.
   - LSF: latest before-tax NTA; also calculate after-tax NTA premium/discount if alerting.
5. Alert Nick only if the current premium/discount is at or below the stored 35th-percentile cutoff:
   - RF1: `gap <= -6.92%`
   - LSF: `gap <= +0.16%`
6. If alerting, send a concise Telegram/current-chat message:
   - ticker
   - current price
   - NAV/NTA used and source/date
   - premium/discount
   - 35th-percentile threshold hit
   - suggested action: e.g. “worth considering a starter buy” or “stronger entry”.
7. If neither threshold is hit, reply exactly `NO_REPLY`.

## Staleness / maintenance rules

- RF1 weekly NAV estimate older than 10 calendar days: still run the price check, but mention stale NAV only if a threshold is close/hit or the source appears broken.
- LSF daily NTA release older than 3 business days: still run the price check, but alert only if price is attractive on the stale NTA **and** note that fresh NTA should be checked before acting.
- Recompute the six-month percentile baseline monthly, or after a major distribution, capital raise/buyback, material strategy change, or if Nick’s deployment window changes.

## Current judgement as of 2026-08-13

- RF1 is **not** currently in the six-month cheapest 35% buy zone. Current price **$3.67** versus weekly NAV **$3.54** is about **+3.67%**, versus the buy-zone cutoff **-6.92%** / about **$3.30**.
- LSF is **not** currently in the six-month cheapest 35% buy zone. Current price **$4.62** versus daily before-tax NTA **$4.5367** is about **+1.84%**, versus the buy-zone cutoff **+0.16%** / about **$4.54**. Versus after-tax NTA **$4.1508**, the premium is about **+11.30%**.
