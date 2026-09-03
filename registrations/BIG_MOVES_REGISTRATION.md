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

## Amendment 4 — 2026-09-03, session H, on Joe's ruling: the code never implemented §3, and the registered rule becomes the primary result

Registered BEFORE the re-run. The reading in "How the two windows combine" below is fixed here so
it cannot be chosen after seeing which reading gives the nicer number.

### The discrepancy
`§3` (as revised by Amendments 1–2, which changed the onset/end definitions but never the cluster
window and never added a merge) registers, for the daily tier:

> consecutive qualifying dates within **60 trading days** of an episode's start belong to that
> episode

`src/big_moves.py` has, since its first line of history:

    CLUSTER_DAYS = 90    # compared with (d2 - d1).days -> CALENDAR days, not trading days
    MERGE_DAYS  = 60    # a same-sign merge step across the 20d and 60d windows

Three deviations, not one: the window is **90 not 60**, it is counted in **calendar not trading
days** (so 90 calendar ≈ 62 trading — the label `unit="trading days"` in `TIERS["daily"]` is simply
wrong), and there is a **merge step that §3 does not contain at all**. A same-sign merge *is*
registered — in Amendment 3, for the **monthly** tier only, at 180 days. It was never registered for
the daily tier.

### The history, stated plainly because git cannot
`BIG_MOVES_REGISTRATION.md` and `src/big_moves.py` both first appear in the same commit,
`594d2fa` ("v2 day-1"). There is therefore **no commit in which the registration exists and the code
does not**, and the project's central discipline — registered before computed — cannot be
demonstrated from history for this file. Worse, the code has *never* agreed with the registration:
the 90/merge values are present in that first commit. So this is not drift introduced later; either
the registration was written to describe an intent the code never had, or the code was written
without reading §3. Which of the two is unknowable now, and this amendment does not guess.

### How the two windows combine — the ambiguity, settled before computing
§1 computes returns over **both** a 20-day and a 60-day window and §2 thresholds each against its
own distribution, but §3 says only "consecutive qualifying dates" and never says whether the two
windows' qualifying dates are one set or two. The as-computed code resolved this with the merge step
— the original comment reads "20d and 60d episodes with onsets this close and same sign merge" —
i.e. the merge exists to solve a problem §3 leaves open, which is why it cannot simply be deleted.

The registered rule is therefore read **literally and in the only way that needs no unregistered
step**: the qualifying dates from both windows are pooled into one ordered set, and that set is
clustered once, within 60 trading days of the episode's start. No merge. Onset and end follow
Amendment 1 (end = date of maximal |trailing return| in the cluster; onset = the price extreme
within [end − W, end], W taken from the window of the maximal date). This reading is recorded here
before the re-run.

### The ruling (Joe, 2026-09-03)
1. The **REGISTERED** rule is the primary result. Every published figure is computed under it.
2. The **AS-COMPUTED** rule is published beside it, labelled, so the change is visible and the old
   numbers are not silently retracted.
3. Neither is chosen after the fact, and no threshold moves in either.

### What this is expected to move
The episode count and everything built on it: `no_identified_event` and the "15 of 43" figure
carried by `README.md`, `docs/BRIEF.md` and `docs/PAPER_DRAFT.md`; `p_class_given_big`;
`p_big_given_class` and `everyday_base_rate_pct`, which are the **materiality gate's inputs**
(CLAIM_LEDGER_REGISTRATION.md §1), so MATERIAL/IN LINE/NOISE calls may change too. Both sets are
published in `data/big_moves/<asset>.json` under `registered` and `as_computed`, and the surfaces
are updated by Joe once both are in hand. Nothing here changes a threshold, an attribution window or
the top-5% cut.
