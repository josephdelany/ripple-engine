# PARKED — the Part IV escalation scorer, withdrawn 2026-09-03

**Not part of the grid study. Not collected by pytest. Not imported by anything.**

## Why it is here

Joe ruled the multiplier-4 gate (`data/gates/grid_multiplier4_2026-09-03.md`) **Option A: the drop stands
as registered.** The grid study has a **price arm only**, and the escalation question stays on the
event-triggered reads.

That ruling arrived after a scope ruling that had told B to build the escalation arm for 1987–2014. The
order of the two was an accident of sequencing, not a reversal by Joe: the scope ruling was given before
B's own gate file reached him. The reading that makes both coherent, and which B agrees with:

> G's 1987–2014 sided-evidence panel remains a **descriptive** object in its own registration. **Nothing
> scores a forecasting engine on it.** Part IV was the scorer. It is the piece that goes.

That is a real distinction and not a face-saving one. Describing a panel — its marginals, its evidence
classes, its base rates, the ICB dyadic-replication finding — is a different act from running a forecaster
on it and reporting skill. Multiplier 4 was about whether the dyad-date panel supplies *evaluation units*
to the grid study. Joe said no. G's panel is unaffected and is still worth building.

## What is in here

- `escalation_walk.py` — the scorer: G's PANEL read through a declared schema contract, the VR-3 assertion,
  the share-zero tripwire, the two-way dyad × date effective-n accounting, the three limits carried in
  every summary object.
- `test_grid_escalation.py` — 16 tests, each named for its clause. One (`..._floored_and_the_floor_is_
  recorded`) was still failing when the stop order arrived and is left failing rather than quietly fixed,
  so that anyone resurrecting this knows exactly where it was.

## What should NOT stay parked — B's one disagreement, recorded

Three pieces of Part IV are **not scorer-specific** and are worth having wherever G's descriptive panel is
registered, because they are properties of the panel rather than of any forecaster run on it:

1. **The share-zero tripwire** (§4.7) — share-zero computed per year and over the window, on ΔIES and on
   the level, on the full panel and on the `opposed_side` subset, against G's registered 0.95 degeneracy
   bar, with a breach reported immediately and the slice neither dropped nor the bar moved. A descriptive
   panel needs this more than a scorer does: it is the number that says whether the panel can support any
   analysis at all.
2. **The VR-3 assertion** (§4.8) — every admitted cell's admitting record ends strictly before `t`, asserted
   rather than trusted, one violation voiding the run. G's own probe found 39 of 335 cells in 2018 admitted
   on a record still running at `t`; an assertion is what stops that recurring silently in the built panel.
3. **The effective-n accounting** (§4.6) — nominal is not effective on a panel this clustered, and the
   informative-cell count belongs beside any marginal G publishes.

B is not moving these anywhere: they are offered to G in
`data/handoffs/B_to_G_2026-09-03c_part_iv_withdrawn.md`, and G decides. The functions are importable from
this directory or copyable; `power_arithmetic.two_way_cluster_deff`, `eff_width` and `deff_block` remain
live and supported in `src/engine/grid/power_arithmetic.py`.

## If this is ever resurrected

It is written against G's `data/grid/g/PANEL.{parquet,csv.gz,csv}` through `SCHEMA` in `escalation_walk.py`,
which lists the column names it will accept per concept and fails loudly naming exactly what is missing.
It never reads `event_outcomes` or `ies90.score_event` — asserted by an AST test, not by grep — so it was
safe under the 2026-09-03 walk freeze and would be again.
