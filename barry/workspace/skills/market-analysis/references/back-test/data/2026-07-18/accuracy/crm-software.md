---
market-id: crm-software
run-date: 2026-07-18
base-year: 2004
errors:
  mean-absolute-error-pct: 38.7
  maturity-duration-error-pct: -14.3
  current-market-value-error-pct: -4.7
  maturity-market-value-error-pct: -50.2
  hhi-error-pct: 85.7
  player-capture:
    - name: Salesforce.com
      ticker: CRM
      error-pct: -28.2
    - name: SAP
      ticker: SAP
      error-pct: 104.8
    - name: Oracle / PeopleSoft
      ticker: ORCL
      error-pct: 190.9
    - name: Adobe
      ticker: ADBE
      error-pct: -100.0
    - name: Microsoft
      ticker: MSFT
      error-pct: 196.3
    - name: Siebel Systems
      ticker: SEBL
      error-pct: null
---
# Customer Relationship Management Software Back-Test Accuracy

## Summary

The generated 2004 doc matched the benchmark's base-year market boundary reasonably well and nearly matched current TAM, but it materially underestimated category expansion and overestimated mature concentration. It identified Salesforce as the highest-upside delivery-model challenger, but capped its mature share too low and expected incumbent suites to retain much more share than they did.

Headline MAE is `38.7%`. The most useful part of the forecast was the adoption-path diagnosis: SaaS attacked CRM's cost, deployment, usability, and access problems. The weakest part was mature-market calibration: the generated doc treated CRM as a suite-consolidation market rather than a broader SaaS-led customer-experience category with durable fragmentation.

## Scorecard

| Field | Generated | Benchmark | Error | Directional quality |
|---|---:|---:|---:|---|
| Maturity duration | 12 years | 14 years | -14.3% | Close; slightly early on SaaS becoming dominant. |
| Current TAM | `$8.2B` | `$8.6B` | -4.7% | Good base-year sizing. |
| Maturity TAM | `$24.0B` | `$48.23B` | -50.2% | Too low; missed CRM/CX expansion. |
| Mature HHI | 0.13 | 0.07 | 85.7% | Too concentrated. |
| Salesforce capture | 14.0% | 19.5% | -28.2% | Right winner, undersized share. |
| SAP capture | 17.0% | 8.3% | 104.8% | Overweighted ERP-suite pull. |
| Oracle capture | 16.0% | 5.5% | 190.9% | Overweighted consolidation. |
| Adobe capture | 0.0% | 5.1% | -100.0% | Missed marketing/CX adjacency. |
| Microsoft capture | 8.0% | 2.7% | 196.3% | Overweighted Office/channel leverage. |

Siebel's generated `18.0%` standalone capture is not directly comparable because the benchmark treats Siebel as absorbed into Oracle rather than a mature independent vendor. Qualitatively, it was an incumbent-overweight error.

## Largest Errors

The largest top-level miss was HHI. The generated doc forecast an oligopoly with stronger incumbent consolidation, while the benchmark shows one clear leader and a large fragmented tail. CRM's function breadth, vertical workflows, marketing/commerce/customer-experience expansion, and SMB products kept the market less concentrated than the 2004 suite logic implied.

The second-largest miss was maturity TAM. The generated `$24.0B` estimate captured growth from 2004 CRM applications but not the category broadening into marketing automation, commerce, analytics, and customer-experience software that the benchmark includes in the mature CRM/CX definition.

The largest player miss was Adobe. The simulated 2004 view did not include a digital marketing or analytics vendor as a plausible mature CRM/CX share-taker, which reveals a boundary problem: it understood CRM as sales/service/marketing automation, but not as a future customer-data and digital-experience control point.

## What The Skill Missed

The forecast overweighted installed enterprise-suite distribution and underweighted product-led delivery-model change. SAP, Oracle, Microsoft, and Siebel all had rational 2004 advantages, but the benchmark suggests those advantages preserved participation rather than leadership.

The forecast also used a mature-market boundary that was directionally similar but economically narrower. It included marketing automation and analytics in definition, yet the TAM estimate did not model those adjacencies becoming central enough to double the mature revenue pool.

## What The Skill Got Right

The base-year TAM was strong: `$8.2B` versus the benchmark's `$8.6B`. The doc also correctly identified Salesforce as the highest-upside challenger, named the core SaaS adoption advantages, and treated security, integration, customization, and enterprise trust as the right adoption bottlenecks.

The maturity timing was useful. A 2016 maturity year versus the benchmark's 2018 would still have put a live investor in the right decade and avoided treating the 2007 IDC on-demand forecast as full market maturity.

## Recommendations

Add an explicit adjacency-expansion check when a market is defined around enterprise workflows. Ask whether the control point could broaden from the initial module into adjacent data, analytics, commerce, marketing, payments, or platform revenue.

When incumbents have distribution but a challenger has a structurally different delivery model, separate "will remain a participant" from "will retain mature share." The player table should penalize incumbents when their advantage depends on the old profit model being disrupted.

For mature HHI, avoid translating early enterprise software consolidation directly into mature concentration. If the market contains several buyer segments, workflows, and deployment modes, model a larger fragmented tail even when the top-five set is easy to name.
