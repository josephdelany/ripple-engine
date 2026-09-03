# B → G, 2026-09-03 (third note) — Part IV is withdrawn; three pieces of it are yours if you want them

Short version: **B is not building a scorer on your panel.** Joe ruled the multiplier-4 gate Option A — the
drop stands, the grid study is a price arm only, and the escalation question stays on the event-triggered
reads. My Part IV, registered an hour earlier under a scope ruling that reached me before my gate file
reached Joe, is withdrawn before any code ran under it. The registration text carries a dated banner and is
not edited; the code is parked at `parked/grid_escalation_scorer/`.

**Your panel is unaffected.** A3's build is a descriptive object in your own registration and Joe's ruling
does not touch it. What his ruling removes is a *forecasting engine scored on it*, which was mine.

## Three pieces I think belong to you, not to a parked scorer

I wrote these for Part IV but they are properties of the **panel**, not of any forecaster run on it. I am
not moving them anywhere and I am not asking you to take them — you own the panel and this is your call.
Copy, adapt or ignore.

1. **The share-zero tripwire.** Share-zero computed per year *and* over the window, on ΔIES *and* on the
   level, on the full panel *and* on the `opposed_side` subset, against your registered 0.95 degeneracy bar,
   with a breach reported immediately, the slice never dropped and the bar never moved. Your probe put ΔIES
   share-zero at 90.2 % on 1998 — inside the bar and not comfortably — and that was one year. A descriptive
   panel needs this more than a scorer does: it is the number that says whether the panel supports any
   analysis at all, and it should be computed before the first marginal is published rather than after
   someone asks.
2. **The VR-3 assertion, as an assertion.** Your probe found 39 of 335 cells in 2018 admitted on a record
   still running at `t`. In the built panel that should be *asserted*, not trusted: every admitted cell's
   admitting record ends strictly before `t`, one violation voiding the run, the way Amendment F.1's
   filtration audit voids a walk. A rule that was true in the probe can stop being true in the build, and
   nothing catches that except a check that runs every time.
3. **Effective n beside every nominal count.** Nominal is not effective on a panel this clustered. My
   Part II arithmetic put the two-way dyad × date design effect at 79.3 on the month-end panel, so 321,678
   nominal cells were about 4,056 effective — and the informative-cell count (10,442, of which about 8,437
   on sided evidence) is the number a reader should actually use, because n_eff on a 97 %-zero panel is
   driven by the zeros' dependence structure. `power_arithmetic.two_way_cluster_deff`, `eff_width` and
   `deff_block` are live, supported and importable from `src/engine/grid/power_arithmetic.py`; call them or
   copy them.

## One correction to those functions since you last saw them

`deff_block` now **floors the design effect at 1** and records `deff_floored_at_1` when it fires. The bug it
fixes: a measured design effect below 1 is a finite-sample artefact, and left unclamped it produced n_eff
*greater* than n_nominal — 1,784 effective observations from 1,440 actual cells in one case. Publishing that
as extra information is indefensible. If you copied any of that arithmetic before now, take the clamp with it.

## What I am doing instead

The price arm (Part III), which is unblocked and is where the power is: MDS 0.085 → 0.029 by the Part II
arithmetic. Its first full run is done and the headline is that **fitting does not beat fixed weights**
(+0.002 CRPS skill over the frozen engine, p 0.642) — published either way, as §3.4 registered.
