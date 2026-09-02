# BIG MOVES — registered definition (written before computing)
*2026-09-01. Fixes the rule for "the market actually changed" so the set is
not chosen after seeing it. Amendments must be dated and appended, never edited.*

## Episodes (per asset; Brent first, WTI, cracks next)
1. Windowed change: log return over 20 trading days and over 60 trading days,
   computed at every date t (t → t+20, t → t+60).
2. Threshold: |return| in the top 5% of that asset's own full-sample
   distribution of that window (two-sided; the sign is recorded).
3. Clustering: consecutive qualifying dates within 60 trading days of an
   episode's start belong to that episode; the episode's start = first
   qualifying date; its peak = the date of maximal |return| in the cluster.
4. Additional episode types (registered, computed when series exist): curve
   flip (Brent M1–M12 sign change persisting 20 days), volatility break
   (20-day realized vol crossing its 95th percentile), product-spread
   blowout (crack in its top 5%), flow drop (production/transit series
   −10% vs 30-day mean).

## Attribution
- A corpus event is attributed to an episode if its `event_date` (first
  knowability) falls within −5..+20 trading days of the episode start.
- Several events may attribute; all are listed. None → NO IDENTIFIED EVENT.
- Attribution says "knowable in the window," not "caused." Causation is
  never asserted by the machine.

## Outputs
- `data/big_moves/<asset>.json`: episodes with start, peak, window, return,
  sign, attributed events.
- P(class | big move): share of episodes with ≥1 event of that class.
- P(big move | class): share of that class's events whose −5..+20d window
  contains an episode start — the materiality gate's input.
- Published as computed. The expected finding that demand collapses and
  policy turns dominate and most conflict headlines are absent is stated
  here in advance so it cannot be read as post hoc.

## Amendment 1 — 2026-09-01, after a first exploratory run (disclosed)
The first run dated episodes by the start of the forward return window, which
stamps a March-2020 collapse "2019-12-12" and attributes it to events of that
week. Seen and rejected as a definition error, not a result. Replaced by:
- Detection uses trailing returns (t−W → t). Episode END = date of maximal
  |trailing return| in the cluster.
- Episode ONSET = the price extreme (min for an up-move, max for a down-move)
  within [end − W, end].
- Attribution window = onset −7 .. +28 calendar days.
- Display uses simple % change, not log return.
Numbers from the first run are discarded; nothing from it is published.

## Amendment 2 — 2026-09-01, after the second run (disclosed)
The −7..+28-day window from onset missed Lehman (onset −9d), the Nov-2014 OPEC
meeting (+29d) and the Feb-2026 strikes (+50d): the market's extreme often
precedes the catalyst. Replaced by: attribution = any corpus event knowable
within [onset − 7 days, episode end]; each attributed event carries its LAG
from onset; lag > 20 days is displayed as ANTICIPATED (the market moved
first) — an F5 finding shown, not smoothed. This is a definitional choice made
after seeing two runs; it is descriptive, not a tested hypothesis, and the
Big Moves table must say so.

## Amendment 3 — 2026-09-02, the monthly tier (registered before computing)
Daily Brent begins 1987-05. To let the record stand at 1973, 1979 and 1985, a
MONTHLY tier is added on FRED WTISPLC (spliced WTI spot, 1946-01 →, keyless),
loaded by `src/fetch_wti_monthly.py`. Same rule, monthly units: episodes = top
5% of trailing 3-month and 12-month log changes over the series' own history;
cluster window 365 days; same-sign merge within 180 days; onset = the extreme
within [end − W months, end]; attribution = corpus events knowable within
[onset − 31 days, end], lag from onset, ANTICIPATED if lag > 60 days. Every
monthly number is labelled "monthly resolution"; the two tiers are never pooled.
