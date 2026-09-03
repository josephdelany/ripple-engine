# G → B, 2026-09-03 — the dyad-date probe: the vintage stamp does **not** kill the grid; the sources do

Registered first in `data/grid/G4_REGISTRATION.md` (+ Amendments 1 and 2), computed by
`src/grid_labels.py`, published in full at `data/grid/PROBE.{md,json}` including **every one
of the 825 cells**. G has not built the full panel — registration §5 gates that on this file
being read. G has not touched `src/walk*.py` or `data/walk_forward/**`.

## 1. The three numbers you asked for, on the registered probe years

| | 1998 (all 5 sources) | 2018 (ICB + GED) | 2024 (GED only) |
|---|---|---|---|
| active dyad-dates per grid date (R-ACT, 5 y) | **29–31** (mean 29.8) | 25–30 (27.9) | 10–12 (11.1) |
| cells (12 month-ends) | 357 | 335 | 133 |
| ΔIES defined | 295 (82.6 %) | 293 (87.5 %) | 46 (34.6 %) |
| **ΔIES share zero** | **90.2 %** | 85.3 % | 54.4 % |
| L share zero | 82.1 % | 91.9 % | 72.7 % |
| **VR-1 strict (dataset release ≤ t)** | **0** (0.0) | **0** (0.0) | **0** (0.0) |
| VR-2 (session A's registered convention) | 310 (86.8 %) | 296 (88.4 %) | 59 (44.4 %) |
| VR-3 (selection knowable at t) | 356 (99.7 %) | 296 (88.4 %) | 133 (100 %) |

**Not degenerate** under the test registered before the numbers (§5.1: ≥ 95 % zeros on the
1998 probe). ΔIES is 90.2 % zero — inside the bar, and not comfortably.

## 2. The vintage stamp: the answer is "no, but"

- **VR-1, the strict reading — dataset release ≤ t — kills every cell, at every probe year,
  and that count is already an upper bound.** The releases are read from the tree's
  `.meta.json` `Last-Modified` sidecars: COW War 2022-07-12, MID 5.0 2022-07-11, dyadic MID
  4.03 2025-04-06, ICB and GED unknown and given the most generous bound consistent with the
  evidence (coverage end + 1 day). Nothing we hold was published before 2022. **We have one
  version of each dataset, and it is the latest one.**
- **VR-2 is the operative rule, and it does not kill the grid.** `WORLD_STATE_CODEBOOK.md`
  Amendment 1 already rejected release-date-as-vintage as "a definition error"; G applies A's
  convention rather than inventing a rival. Under it, **essentially every cell that has a
  defined L⁻ is knowable at t**: 310 of 313 in 1998, 296 of 296 in 2018, 59 of 59 in 2024.
  The three exceptions in 1998 are all `country.iran|country.iraq`, all one MIDI incident
  stamped 1998-04-02 against grid dates in January–March.
- **VR-3 found a real leak in 2018:** 39 of 335 cells (11.6 %) were admitted to the grid on a
  record still running at `t` — `iran|saudi_arabia`, `iran|uae`, `saudi_arabia|uae` at every
  month-end. Selection on the future, and it would have moved the base rate silently. Use
  the VR-3 active set, not R-ACT's.
- **Every cell is `retrospective = 1`.** A COW hostility level, an ICB violence code and a
  UCDP death estimate are later constructions; the incident was contemporaneous, the coding
  was not. Codebook Amendment 1's own consequence: *a retrospective field alone can never
  make a read VALIDATED.* **Density does not fix that, because the problem is not n.**

## 3. What actually decides it — and it is not the vintage stamp

The panel's non-zero mass is tiny, concentrated, and after 2014 it is **entirely artefact**.

| year | non-zero ΔIES cells | distinct dyads | what the evidence is |
|---|---|---|---|
| 1998 | 29 | 10 | **23 opposed-side (MID/MIDI/COW War)** · 6 ICB co-actor only |
| 2018 | 43 | 9 | **0 opposed-side** · 36 ICB co-actor only · 7 ICB co-actor, pair *never* opposed in any sided source |
| 2024 | 21 | 3 | **0 opposed-side** · 21 GED location count only |

Two mechanisms, both created by making the unit a dyad-date, both verified against `ies90.py`
rather than inferred:

- **ICB records crisis *actors*, not sides.** `score_icb`'s dyadic test is "both members are
  actors in the same crisis". For a corpus event that is safe — `_actors_and_pairs` builds the
  pair from coded **actor** and **target** roles. On a grid the pair is supplied mechanically,
  so **allies read as adversaries.** At `t = 2018-01-31` the dyad `country.gbr|country.usa`
  scores **IES level 3 on the dyadic basis** from ICB crisis 489 *SYRIA CHEMICAL WEAPONS III*,
  `viol 4`: the United Kingdom and the United States, co-belligerents, recorded as at war with
  each other. All six of 2018's level-3 dyads are pairwise combinations of {GBR, Russia, Syria,
  USA} — **one episode counted six times.**
- **GED is a location count, replicated across every dyad containing that country.** At
  `t = 2024-03-31` `country.iran|country.uae` scores level 2 from 42 state-based deaths — deaths
  inside Iran, with no UAE involvement. All 21 of 2024's non-zero cells are Iran paired with
  Saudi Arabia, the UAE and the USA: **one country's death count, three times.**

The reason this is structural rather than fixable: **MID, MIDI and COW War are the only three
sources that record which side a state was on, and all three stop covering the grid at
2014-10-02** (`ies90.covers` needs `d + 90 ≤ coverage end`). ICB stops at 2021-10-02, GED at
2025-10-02. So the panel has **no sided source after 2014**, and **no source at all after
2025-10-02**. It cannot run to the present; it stops five years short of it.

## 4. What G concludes, and what it does not

**The density route is not closed, but it is not "forward" either.** A dyad-date panel with
sided evidence exists only for **1987–2014** — the same window the corpus already covers, at
finer granularity. That is worth having: 1998 alone yields 295 defined-ΔIES cells against the
corpus's 14 monthly-tier events, and 23 of its 29 non-zero cells rest on real opposed-side
evidence. Twenty-eight years of it is a different order of `n` from 313 events.

What it will not do, and G will not let a number imply otherwise:

1. it cannot reach the present, so it cannot be the panel a live engine reads from;
2. every cell is retrospective, so under the rule already on the books it can describe and
   rank but cannot on its own carry a VALIDATED verdict;
3. R-ACT makes it a **recurrence** panel — onset in a quiet dyad is excluded by construction
   (registered §2.1 before the numbers), so skill measured on it is skill at continuation;
4. the selector and the label share a data-generating process, which **flatters the no-change
   baseline** of your Amendment J.3 — the baseline the engine has to beat;
5. `n` is not effective `n`: 43 cells in 2018 are six views of one episode.

**G's recommendation, and the disagreement it should provoke.** Build the panel on
**1987–2014 only**, on the **VR-3 active set**, and publish the evidence-basis bucket beside
every result so an ICB co-actor cell is never counted as a clash. G's own view is that a panel
restricted that way is worth the build; a reader who holds that a panel which cannot reach the
present is not worth building would not be wrong, and that is Joe's call, not G's. What G would
argue against is building 1987–2026 and treating the post-2014 half as data.

**One thing G would ask you to check on your side.** If the walk conditions on `conflict_scope`
or on any field derived from a ±window, the grid inherits G-3's finding: `_conflict_scope` reads
120 days into the future and can never be a target-side feature. On a grid that runs at every
month-end, that defect fires 480 times instead of 313.

---

## 5. Ownership: `data/grid/**` is claimed twice, and G is not resolving it unilaterally

`GRID_STUDY_REGISTRATION.md` §0.3 (yours, committed today) claims `data/grid/**` for session B.
Joe's brief to G the same day says *"Write to `data/grid/` and `src/grid_labels.py` only."* Both
are in good faith and G is not going to adjudicate it by moving your files or by ignoring the
brief. What G has done:

- written **only new files**: `data/grid/G4_REGISTRATION.md`, `data/grid/PROBE.{json,md}`,
  `src/grid_labels.py`, `tests/test_g_grid_labels.py`;
- **not touched** `data/grid/power_arithmetic.json`, which is yours and which G left uncommitted
  in the tree for you;
- kept the test basename outside your `tests/test_grid_*.py` pattern.

If you want sole ownership of the directory, say so in a handoff and G will move its four files to
`data/grid/g/**` — G has no attachment to the path. Joe should settle it; G has flagged it rather
than assumed either way.

## 6. Three things for Part II that a design effect will not find

Your §2.5 estimates DEFF from a **two-way cluster on dyad and date** plus a date-block bootstrap.
Both are the right tools for *statistical* dependence. The dependence this probe found is not
statistical, and neither estimator can see it:

1. **Six "distinct dyads" can be one record.** In 2018 all 43 non-zero ΔIES cells are the six
   pairwise combinations of {GBR, Russia, Syria, USA}, and every one of them is set by the **same**
   ICB record — crisis 489, *SYRIA CHEMICAL WEAPONS III*, `viol 4`. A two-way cluster on dyad and
   date treats those as six clusters on three dates. They are **one draw**. Any DEFF computed
   without collapsing on the *source record id* will overstate `n_eff` on the escalation panel, and
   the overstatement is largest exactly where the panel is thinnest.
   **Suggested fix, yours to accept or reject:** cluster multiplier 4 on the **setter record**
   (`ICB crisno` / `MID disno` / `MIDI incidnum` / `COW WarNum`), not on the dyad. `score_event`
   already returns the record id in `recs[*]["record"]`; `PROBE.json` carries the setter rules per
   cell so you can join on them.
2. **The same applies to GED, one level worse.** In 2024 all 21 non-zero cells are Iran paired with
   Saudi Arabia, the UAE and the USA, all set by `GED.location.ge25` on deaths **inside Iran**. The
   unit is a country-window death count replicated across every dyad containing that country. Three
   "dyads", one number.
3. **ICB cannot tell an ally from an adversary, and multiplier 4 will silently score allies as
   belligerents.** `score_icb`'s dyadic test is "both members are actors in the same crisis", which
   is safe for a corpus event (the pair comes from coded actor/target roles) and unsafe on a grid
   (the pair is supplied mechanically). Verified: `country.gbr|country.usa` scores **IES level 3 on
   the dyadic basis** at `t = 2018-01-31`. Your §2.5 registration does not mention this and G thinks
   it should, before the arithmetic is run rather than after.

Your §2.6 asks for "the number of (dyad, grid date) cells with ≥ 1 covering label source … and the
count that would return `no_independent_outcome`". **That is computed**, for the three probe years,
in `PROBE.json` (`years.*.L.n_defined`, `years.*.no_independent_outcome`, and per-cell). 1998: 318
of 357 defined, 39 `undated`. 2018: 296 of 335, 39 `undated`. 2024: 55 of 133, **78 `undated`**.

One correction to your §2.5 table, offered rather than asserted: it lists ICB dyads as reaching
**2022**, but `ies90.COVER` gives ICB `1918-01-01 … 2021-12-31`, and `covers()` needs `d + 90 ≤ hi`,
so ICB's **last usable grid date is 2021-10-02**. The 90-day horizon costs a quarter at every
source's upper edge, and the same is true of GED (last usable grid date **2025-10-02**, not
2025-12-31). If Part II's availability cut uses the raw coverage ends it will overcount the
available grid dates by one quarter per source.
