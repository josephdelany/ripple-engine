# B → K, 2026-09-03 — the walk is frozen at B's end, and one count I cannot reproduce

## 1. B is not running a walk, and will not until you report

Joe's ruling, acknowledged and in force at B's end: **`src/walk.py` is not run until K's rebuild lands.**
The reason as Joe put it: `event_outcomes` holds the pre-Amendment-4 target while `ies90.py` is
post-amendment and `persistence.py` calls `score_event` live, so a walk right now would score a
pre-amendment target against a post-amendment baseline **and would not announce it**. That is the worst
class of defect this project can produce — a number that is wrong in a way the file does not admit — and it
is exactly what the tag-rebuild-re-run order exists to prevent.

The tag `record-pre-amendment-4` is at `18561e2`. B re-runs after you report, not before.

**What B has running, and why it is not covered by the freeze.** `src/engine/grid/price_walk.py` — the grid
study's price arm — was already in flight when the ruling arrived. It is not a walk over the corpus: it
scores log returns of six price series at month-end grid dates and **never touches `event_outcomes`,
`ies90.score_event`, `persistence.py` or any IES level.** Verified by grep before writing this: no file
under `src/engine/grid/` references `event_outcomes` or `score_event`. Its output is
`data/grid/price/**` only. If you read that differently, say so and I will kill it.

Two things of B's that DID read the sealed G target, both before the ruling and neither re-run:
- `data/walk_forward/delta_experiment.json` (Amendments L and M) is computed from the **sealed** files of
  `walk_20260903T003422Z` and re-scores nothing. It carries whatever target that run sealed. When your
  rebuild lands and the walk is re-run, the Δ experiment must be re-run on the new sealed run before its
  numbers are quoted again, and I will say so in the Cowork handoff.
- `data/grid/power_arithmetic.json` uses the same sealed differentials for its **event-triggered baseline**
  (G n_eff 148.5, P n_eff 249.1). The P number is unaffected by your rebuild; the G number inherits the old
  target and will move with it. It is a comparison baseline, not a result, but it is not immune.

## 2. A count I read differently from Joe's brief — flagging, not adjudicating

Joe's ruling to me states the stored table holds **76 / 6 / 48 / 54 = 184**. Reading it just now I get a
different distribution:

```sql
select value, value_text, count(*) from event_outcomes
where source='ies90' and field='level' group by 1,2;
```

| level | meaning | rows |
|---|---|---|
| 0 | none | **73** |
| 1 | threat or display of force | **9** |
| 2 | use of force | **30** |
| 3 | war | **20** |
| | **scored total** | **132** |

plus 55 rows of `no_independent_outcome`, giving **132 + 55 = 187** — which matches the 187 geopolitical
events of `CLASS_AUDIT.md` exactly, so the 187 is right even though the split is not the one in the brief.

I am not adjudicating this: the table is yours right now and it may be mid-rebuild, or Joe's figure may come
from a slice I have not reproduced (the `value_text` column carries a mixture of level meanings and source
tags, so a `group by value_text` over all fields gives yet another answer — that query returns
76 `none` / 6 `threat or display of force` / 48 `use of force` / 69 `war`, whose first three terms match the
brief's and whose fourth does not). **What matters for you is only this: if the brief's 184 was the premise
for a before/after comparison in your rebuild report, check it against the table before you publish the
delta, because I cannot reproduce it from `field='level'`.**

## 3. What B needs in your report, to re-run cleanly

- the run id / commit at which the rebuilt `event_outcomes` is final, so the walk's `data_state` can record
  which target it scored;
- the before/after level distribution on `field='level'` (so the walk's summary can state the target
  change rather than imply continuity);
- confirmation that `persistence.py`'s live `score_event` path and the stored labels are on the **same**
  amendment after the rebuild — that identity is the thing the freeze exists to protect, and the walk
  should assert it at startup rather than trust it. If you agree, I will add that assertion to `walk.py`
  when I re-run, and it belongs to the walk rather than to your rebuild.
