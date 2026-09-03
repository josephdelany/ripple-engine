# K → B, 2026-09-02 — the ongoing-war rule (OUTCOME_MAPPING Amendment 4), and what it does to your persistence experiment

Registered first in `OUTCOME_MAPPING.md` **Amendment 4** (commit `c74ccd6`, before a line of
code), implemented in `src/state/ies90.py`, computed with **`write=False`**. Receipts:
`data/state/ies90_amendment4_counts.json`,
`data/state/ies90_amendment4_persistence_overlap.json`. Tests:
`tests/test_ies90_continuation.py`.

**Session K has not written one row to `event_outcomes` and has not touched
`src/engine/**`, `src/walk.py` or `data/walk_forward/**`.** The table still holds the
pre-amendment labels and runs 182828Z and 193022Z remain reproducible. Amendment 4 governs
the **next** rebuild, which is Joe's to schedule with you — it is not a side effect of this
handoff. **But the code change does reach your persistence baseline without a rebuild —
read §0 before you run anything.**

## 0. READ THIS FIRST — the code change reaches your baseline **without** a database rebuild

`src/engine/persistence.py` calls `ies90.score_event` **live** ("called, never copied", its own
docstring). The labels come from `event_outcomes`, which Session K has not touched — but the
G-persistence forecast is *computed at run time by the function K just changed.*

**So from commit of the code until the `event_outcomes` rebuild, a walk run scores the
pre-Amendment-4 target against a post-Amendment-4 baseline.** That mixture is not a valid
comparison and is not what either amendment registers. It also does not announce itself:
`walk.py` records `data_state.ies90_registration` from
`data/state/ies90_distribution.json`, which K deliberately did **not** regenerate, so it
still reads *"Amendment 1 + 1.1 + 2"* while `ies90.REGISTRATION` in the code now reads
*"Amendment 1 + 1.1 + 2 + 4"*. A run made in this window would record a provenance string
that is true of its labels and false of its baseline.

Check before any run:

```
python3 -c "import sys; sys.path.insert(0,'src/state'); import ies90; import json; \
print('code:', ies90.REGISTRATION); \
print('labels:', json.load(open('data/state/ies90_distribution.json'))['registration'])"
```

If those two strings disagree, the target and the baseline are on different rules. **This is
Joe's call, not K's**, and it is the reason §6.1 asks you not to rebuild unilaterally. The
two coherent states are: everything pre-Amendment-4 (revert `src/state/ies90.py` to
`c74ccd6` for the duration), or everything post (rebuild the `ies90` rows, then run). K has
not chosen for you.

## 1. What changed in the rule

Amendment 1.1 gave ICB and Dyadic MID an "ongoing at d → no level" carve-out and never
extended it to COW War or UCDP GED. All 54 level-3 labels came from exactly those two
sources. Amendment 4 extends it with one predicate across all five sources —
`B = [d−90, d−1]`, the scale's own 90 days run backwards, so no new constant — and fixes
the mirror-image defect: "no level" was falling through `max(default=0)` to **level 0 =
"none"**. An event with no dated record and at least one undated-for-W record is now
`no_independent_outcome`, never 0.

## 2. The numbers you need

| level | before | after |
|---|---:|---:|
| 0 | 76 | 73 |
| 1 | 6 | 9 |
| 2 | 48 | 30 |
| 3 | **54** | **20** |
| `no_independent_outcome` | 3 | **55** (3 uncovered + 52 undated-for-W) |
| **events with a level** | **184** | **132** (−52, 28 % of G's n) |

59 of 187 labels move: 3 → NI 27, 2 → NI 22, 3 → 2 four, 3 → 1 three, 0 → NI three.
Surviving level 3 by source: GED 11, COW War 8, MIDI+War 1. Full per-event rows, with the
rule that fired and the `from`/`to`, are in `rows_changed` in the counts JSON.

## 3. **The thing to read before you run anything**

`WALK_FORWARD_PROTOCOL.md` **Amendment B.1 defines the G-persistence forecast as this same
function on a shifted window** — `ies90.score_event(t − 91, A, P, L, sources)`. So
Amendment 4 changes **your baseline as well as the target**. Two consequences:

1. **B.3's climatology fallback fires far more often: 2 corpus events → 58.** After
   Amendment 4 the persistence forecast is `no_independent_outcome` for a large minority of
   reads, and B.3 sends those to climatology. "Engine vs persistence" then partly *is*
   "engine vs climatology". `n_persistence_fallback` per tier must be published beside the
   comparison (B.4 already requires it) or the number will be read as something it is not.
2. **The comparison is materially less powerful** than the one that produced −0.469: fewer
   scored reads, and a baseline that is climatology on a chunk of them.

Neither is an argument against the amendment. Both are facts to price into the design
before the run, not after.

## 4. The answer to "is the persistence result mechanical?" — measured, not asserted

Both target and persistence recomputed under both rule sets (old code taken from git at
`c74ccd6`), read at `t = d`. Corpus-level diagnostics; **not** your walk's numbers.

| | before | after |
|---|---:|---:|
| n with both | 184 | 120 |
| exact agreement | 75.0 % | 73.3 % |
| Spearman ρ | 0.800 | 0.638 |
| **ρ² shared rank variance** | **0.640** | **0.407** |

Holding the sample fixed at the 120 events scorable under both rules: ρ² **0.484 → 0.407**.
So of the 0.23 headline fall, **about 0.08 is the rule and the rest is selection** — the
events removed were the ones where target and persistence agreed most.

**Partly mechanical, not only mechanical.** 41 % of the target's rank variance is still
shared with persistence and 73 % of labels are still exactly what persistence would say.
That residual is real autocorrelation in conflict, not an artefact, and the amendment does
not try to remove it. The engine still has to beat a strong baseline. Whether it does is
yours to run and publish either way — §A4.3 and §A4.5 both say in terms that the direction
of the effect on the engine's score was not a consideration in adopting the rule.

## 5. A second target, registered before either was computed

`delta_level` (§A4.4): the same registered ladder applied to `max(0, D(W) − D(B))` for GED,
stored beside `level` and **never inside it**. Distribution: 0 → 119, 2 → 28, 3 → 21, n/a
→ 19. **The number that prices the choice for you:** of the 52 events Amendment 4 removes from
the G target, `delta_level` is non-zero on **21** (2 on 13, 3 on 8). Those are events where
UCDP records a real increase over the baseline. If you score the change target, that is the
n you get back, and it is the strongest argument against §A4.3's choice — stated here so it
is in front of you rather than buried.

It is a **published diagnostic, not the G target** — no score is computed against it
under Amendment 4, and promoting it needs a further amendment registered before that score
exists.

It is handed to you now for one reason: "does the engine beat persistence once the target
stops encoding the pre-existing state?" has two defensible operationalisations — drop the
contaminated events (§A4.2) or measure the increment (§A4.4). Both are registered before
either is computed, so the choice cannot be made afterwards by whoever prefers the answer.
If you score both, publish both.

## 6. Requests

1. **Do not rebuild the `ies90` rows mid-experiment.** When you and Joe are ready, the
   command is `python3 src/state/ies90.py` (the default path still writes); `--counts`
   recomputes everything and writes nothing.
2. **Report pre- and post-amendment G runs separately** — never pooled, never as a
   correction to the published numbers (§A4.7).
3. **A4.7's surface note** for any G result from a pre-amendment run: *"scored before
   Amendment 4; 59 of 187 labels change under it, 52 of them to `no_independent_outcome`"*,
   receipt `data/state/ies90_amendment4_counts.json`.
4. Amendment 4 is **orthogonal to Amendment 3** (F's hostility precondition). An event can
   be dropped by either. Keep the two exclusion counts separate and never merge them into
   one "excluded" figure.

---

# ADDENDUM, 2026-09-03 — the rebuild has landed; §0's hazard is closed, and here is what is stale

Joe ruled tag-rebuild-re-run. `event_outcomes` source `ies90` is now on Amendment 4 and the
pre-rebuild record is tagged **`record-pre-amendment-4`** (`5a2c58f` → `18561e2`). §0's
incoherent window is **closed**: target and baseline are both post-amendment, and
`data/state/ies90_distribution.json` now reads *"Amendment 1 + 1.1 + 2 + 4"*, so
`data_state.ies90_registration` in your next run will record the right thing. The check in §0
now agrees on both sides.

**Level distribution as written:** 0 → 73, 1 → 9, 2 → 30, 3 → 20, `no_independent_outcome`
→ 55 (52 undated + 3 uncovered). 132 events carry a level. Identical to the `write=False`
projection, so the rebuild is deterministic. **1,198 `event_outcomes` rows touched**: 724
added, 209 removed, 265 changed. Rows of other sources (`icb` 308, `mid` 75, `ucdp` 561,
`precedence` 187) are untouched.

## What is now stale for you, measured not guessed

Against the sealed run `walk_20260903T003422Z` — 172 scored daily G reads carrying 11,385
analog slots (Amendment L's own filters retain 150 reads / 10,885 slots; the direction is the
same):

| | |
|---|---:|
| scored events that now leave the G target entirely | **49 of 172 (28 %)** |
| scored events keeping a level that changed | 6 |
| scored events with an unchanged label | 117 |
| scored events that now have **no knowable L⁻** → B.3 climatology fallback | **53** (the sealed run recorded `n_persistence_fallback` = **2**) |
| analog slots whose analog leaves the G pool (`read.py:217`) | **2,661 (23.4 %)** |
| analog slots whose analog keeps a level that changed | 618 (5.4 %) |
| analog slots whose analog has **no knowable L⁻_a** → Amendment L.2 drops it | **2,379 (20.9 %)** |

**Amendment L.2's structural fact will not survive the next run.** L.2 states, as a fact about
the data, *"0 of the 10,885 analog slots carried by the 150 scored reads lack L⁻_a"*, and
`delta_experiment.json` records `analogs.delta_dropped: 0`. On the rebuilt target that becomes
roughly 21 % of slots. `n_analog_delta_dropped` stops being decorative and becomes a number
that has to be published, and items will abstain more often.

**`data/walk_forward/delta_experiment.json` does not name the target it was computed on.** It
carries `derived_from_run: walk_20260903T003422Z` and the Amendment L citation, but no
`ies90_registration`. It is therefore one hop from its provenance — that run's `summary.json`
does record *"Amendment 1 + 1.1 + 2"* — and zero hops from being misread. Consider copying the
registration string into the delta output when you next regenerate it; a file whose headline
is "NO ADDITION" and whose target definition has since changed is exactly the number that
looks fine.

## Stale by design, and protected by the tag — do not regenerate to "fix" them

`reads.jsonl`, `scores.jsonl`, `weights.jsonl`, `summary.json`, `per_event.json`,
`delta_experiment.json`, `delta_experiment_reads.json`, `data/walk_forward/runs/**`,
`docs/PAPER_DRAFT.md` §8–§11 and the gate reports in `data/gates/` were all computed against
the pre-Amendment-4 target. **They stand as published** (A4.7). The next run is reported
separately and never pooled with them.

## Fresh, verified

- `engine/read.py::_ies90` selects only `field IN ('level','deal')`, so Amendment 4's new
  fields (`delta_level`, `delta_basis`, `deaths_ged_on_d`, `deaths_ged_delta`) do **not** leak
  into the walk's target. `delta_level` reaches you only if you go and read it deliberately,
  which is what A4.4 intends.
- `engine/persistence.py::precompute` is live and now post-amendment: 129 of 187 events have a
  knowable L⁻, 58 do not.
- `src/grid_labels.py` / `data/grid/g/PROBE.json` (Session G) are **already on Amendment 4** —
  its cells carry `L_ni: "undated"`, which only exists post-amendment. Not stale.
