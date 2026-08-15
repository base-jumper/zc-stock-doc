# Mobility Corpus Collection

Build up the rank-mobility panel corpus: historical named market-share rankings used to calibrate
rank-transition probabilities. The contract is
[skills/market-analysis/references/mobility/mobility.md](../skills/market-analysis/references/mobility/mobility.md)
— read it fully before touching data; it defines the CSV/YAML format, the fate vocabulary, the
acquisition rule, and the citation/quality rules. This file only sets the work order and
boundaries.

## Rules

- **Never invent a number, rank, year, or founding date.** Every figure must come from a page you
  actually fetched this session; record the URL (Wayback Machine archive URLs are fine) in the
  entry's `sources`. If you can only verify the ordering, leave `share` blank.
- One panel at a time, verified as you go: create or extend the CSV and its `panels.yaml` entry,
  run `skills/market-analysis/scripts/mobility_panels.py validate`, fix errors, then move on.
- Set `quality: verified` only when every covered year is cited. If a session ends with uncited
  years, leave the panel `seed-approximate` and say so in your report.
- Secure two years ≥ 10 apart first so the panel has a usable window, then fill in every year the
  source covers — full annual series are the target.
- Leave the `penetration` block alone: S-curve parameter scoring is analyst work done before
  fitting, not part of collection.
- Touch nothing outside `skills/market-analysis/references/mobility/` for this task.

## Work Queue

Work in order; 1–2 panels per session is a good pace. Quality over quantity.

1. **Verify the seed.** `worldwide-smartphone-units` was seeded from memory. Re-derive both years
   from archived IDC full-year press releases (2013 and 2023 top-5 vendor tables), correct any
   figure that differs, cite each year, verify the player facts (founded/fate years), then flip
   it to `verified`.
2. **Worldwide PC shipments** — IDC full-year top-5 press releases; aim 1996 → latest for several
   non-overlapping windows. Do not mix IDC and Gartner numbers in one panel.
3. **US domestic airlines by passengers** — DOT/BTS carrier data; top ~8, 1995 → latest.
4. **US bank deposits** — FDIC Summary of Deposits, top 10 institutions, 1994 → latest.
5. **Worldwide semiconductor revenue** — Gartner annual press releases, 2000 → latest.
6. **US carbonated soft drinks** — Beverage Digest company shares.
7. **Global auto sales by group** — OICA or Ward's, top 10.
8. **US web browsers or worldwide mobile OS** — StatCounter usage share, 2009 → latest.
9. **US wireless subscribers** — FCC reports / carrier filings, top 4–6.
10. **US P&C insurance premiums** — NAIC market-share reports, top 10.

If a market's boundary proves unstable over the window (definition redraws, tracker splices you
cannot isolate), skip it and note why rather than forcing it.

## Report

End each session with `mobility_panels.py summary` output plus: panels added or extended, which
are `verified`, any figure you could not verify, and anything in the contract that proved
ambiguous — format friction is a finding, not a failure.
