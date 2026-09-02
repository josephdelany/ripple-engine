# Registration — pre-1987 candidate sheet for the monthly tier (Brief B-3, 2026-09-02)

Written before the sheet is computed. The sheet is Joe's admission list (PATH Step 5): NOTHING here
enters `events`; every row is a source record he can check, with a blank `suggested_title`.

## Why
The monthly tier (WTI spliced, 1946–1987, horizons in months) has 14 corpus events and 0 scored reads
(burn-in 8 per class, `min_tier_n` 30). It cannot describe, let alone validate, without pre-1987 events.

## What is listed (all of it — no judgment applied by the code)
Every record dated 1946-01-01 .. 1986-12-31 from the three sources session A already holds in
`data/state/raw/` (read only; the loaders in `src/state/ies90.py` / `outcomes.py` are called, not copied):

| source | record | date used | actors listed |
|---|---|---|---|
| ICB v16 (`icb1v16` system-level + `icb2v16` actors) | one row per crisis (`crisno`) | `trigdate` | crisis actors (`cracid`), plus `viol` and `forout` |
| COW War v4.0 inter-state and v4.1 intra-state | one row per war (`WarNum`) | earliest participant start | participants with sides (inter) / state parties A, B (intra) |
| Dyadic MID 4.03 | one row per dispute (`disno`) with `hihost` ≥ 4 (use of force = 4, war = 5) | earliest dyad start | every state in any of the dispute's dyads |

A record is listed when **at least one** of its actors is in the registered state set below. The
match is on COW country codes, so states the corpus does not yet name as `country.*` are not lost.

## The registered state set (COW ccode)
- **Producers**: USA 2, Canada 20, Mexico 70, Colombia 100, Venezuela 101, Ecuador 130, Brazil 140,
  Argentina 160, Trinidad & Tobago 52, UK 200, Norway 385, USSR/Russia 365, Romania 360, Algeria 615,
  Libya 620, Nigeria 475, Gabon 481, Angola 540, Egypt 651, Iran 630, Iraq 645, Saudi Arabia 670,
  Kuwait 690, Bahrain 692, Qatar 694, UAE 696, Oman 698, China 710, Indonesia 850, Malaysia 820,
  Brunei 835.
- **Transit** (Suez/SUMED, Bosporus, Hormuz, Bab el-Mandeb, Malacca, Panama, the Levant pipelines):
  Egypt 651, Syria 652, Lebanon 660, Jordan 663, Israel 666, Turkey 640, Iran 630, Oman 698, UAE 696,
  Bahrain 692, Yemen (YAR 678, PDR 680, unified 679), Djibouti 522, Somalia 520, Ethiopia 530,
  Eritrea 531, Panama 95, Malaysia 820, Singapore 830, Indonesia 850, Denmark 390.
- **Major consumers**: USA 2, Japan 740, West Germany 260 / Germany 255, France 220, UK 200,
  Italy 325, USSR 365, China 710, India 750, South Korea 732.

## The join to the monthly Big Moves (registered, `data/big_moves/wti_monthly.json`)
- `inside_big_move`: the record's date lies in [onset − 31 days, end] of any WTI monthly episode —
  the same window the walk's materiality call uses (`read.TIERS["monthly"]["before_days"]` = 31).
- `episode_id`: `wti_<onset>` of the matched episode (earliest if several); blank otherwise.
- `monthly_move_pct`: the matched episode's registered `change` (% onset→end); blank otherwise.
- `wti_chg_3m_pct`: WTI (`fred.WTISPLC`) percent change from the record's month to three months
  later — the monthly tier's registered P horizon — for every row, so Joe sees the outcome the walk
  would score whether or not the record sits in a Big Move.

## Columns
`event_date, actors, source, source_id, source_detail, inside_big_move, episode_id, monthly_move_pct,
wti_chg_3m_pct, suggested_title` (blank), sorted by `event_date`. Output:
`data/candidates/pre1987_candidates.csv`; counts by decade and by source in
`data/candidates/pre1987_candidates_summary.json`.

## What this is not
Not a coding. Not a filter for "oil-relevant". Not an entry in any registered table. Duplicates across
sources (the same war in ICB, COW and MID) are listed once per source, by design — Joe sees each
source's own record and decides.
