# A negative control: the spine repair moved zero forecast numbers

*Dated finding, session B, 2026-09-03. Evidence, not a claim of correctness — read §"What this does not
show" before citing it.*

## The finding

Session E repaired the corpus's sourcing: **66 field changes** across nineteen pre-1990 records and the
1990s pass (`data/spine/patches/{pre1990_a,pre1990_b,1990s_a,1990s_b}.json`, applied in commits eabfba9,
964d76c, dff8f8b, f25ae08). The walk was then re-run in full on the repaired corpus.

**Every published forecast number is identical.** Run `walk_20260903T003422Z` reproduces
`walk_20260902T210135Z` on every skill estimate, every confidence interval, every DM/HLN and SPA p-value,
the label permutation, the placebo, the specification curve, the power block, the Murphy decompositions and
the whole FDR family. The two runs' content digests are the same string:

```
2a90ff4a88f30f6f50433a2b5268dc1feaf9bc219b5ef2ec575ef15dce57f116
```

A whole-summary diff, ignoring only run identity and wall-clock stamps, is equal on every key except
`verdict.audit_record` — which is Joe's label audit beginning (1 of 30 rows), not a forecast number.

## Why, established by execution rather than argument

The 66 changes by column: `source_url` 24, `description` 17, `surprise` 12, `severity` 9, `confidence` 8,
`date_precision` 4, and proposals recorded for `event_date` 2 and `type` 2.

Only two of those columns can move a walk — `event_date`, which the filtration keys on and which sets the
IES-90 window `(d, d+90]`, and `type`, which decides the analog pool and whether an event is G-scored. So
the patch files were not taken on trust. The live corpus was diffed against **the sealed reads of the
earlier run**, which are the record of what the engine actually saw:

| check | result |
|---|---|
| events in the corpus vs sealed reads | 313 vs 313; none added, none removed |
| events whose `event_date` differs from the sealed read | **0** |
| events whose `type` differs from the sealed read | **0** |
| IES-90 labels differing from the sealed outcome | **0** of 184 |
| `severity`, `surprise`, `confidence`, `description`, `source_url`, `date_precision` references in `src/engine/*.py` and `src/walk.py` | **0 each** |

The two `event_date` and two `type` entries in the patch files are proposals that were not applied to those
columns, consistent with session E's own correction (commit b4a1f6d: "the Iran-Iraq ceasefire date did NOT
move; my previous commit message was wrong") and its handoff ("no date moved at all … only the
`date_precision` label changed").

The engine's inputs are: `event_date` and `type` from `events`; the seven situation fields, now via
`situation_state`'s knowable-at rows (protocol Amendment H); the market series from `observations`; the
label from `event_outcomes`; and the entity rows that `ies90.score_event` uses for the persistence baseline.
None of the six repaired columns is among them.

## What this shows

The published results **do not depend on which sources the corpus cites.** Session E's audit found that
**31 of 313 events cite Wikipedia as their `source_url` with no other citable domain** — by the codebook's
own inclusion criterion 2 ("No source = not in the dataset"), those records are not sourced, and that is the
largest single sourcing defect in the corpus. A reader entitled to ask whether the engine's numbers were
propped up by weakly-cited records now has a direct answer: a repair that rewrote 24 citations and 42 other
provenance and coding fields moved nothing, to the last decimal, because the forecast never reads those
fields.

This is a negative control in the proper sense. It was not run to produce a null; it was run because the
corpus changed, and the null is what came back. The instrument that establishes it — the content digest of
Amendment I — was registered before this repair existed, so the test could not have been shaped to pass.

## What this does not show

It does **not** show the corpus is well sourced, and it does not retire the 31 Wikipedia-only records. The
repair changed provenance columns; it did not change a single `event_date` or `type`. So this control says
nothing about whether the dates and classes those weak citations support are *correct* — only that the
published numbers are invariant to the citations themselves. If a future repair moves a date or a class,
the numbers can and should move, and that would be a different finding.

Nor is it evidence of skill. The run it validates is null on both targets: G Brier skill against
climatology −0.0966 (DM p 0.022, i.e. significantly *worse* than climatology), P CRPS −0.0705 (p 0.016),
the specification curve negative in all 54 specifications, the size-matched placebo not holding, and the
§7 label audit 1 of 30 rows in. A stable null is still a null.

## Receipts

`data/walk_forward/summary.json` (run `walk_20260903T003422Z`); the prior run archived and re-verified at
`data/walk_forward/runs/walk_20260902T210135Z/`; the full delta in
`data/handoffs/B_run_delta_spine.md`; session E's changes in `data/spine/PATCH_LOG.md` and
`data/handoffs/E_to_AB_2026-09-02_spine_changes.md`; the digest instrument in
`WALK_FORWARD_PROTOCOL.md` Amendment I and `tests/test_walk_determinism.py`.

One further check, run because another session regenerated the IES-90 rows at 2026-09-03T01:17:06Z, after
this walk sealed its reads at 00:34Z: comparing the database against the published run's sealed outcomes
gives **0 of 184 labels different**, with identical level counts (0: 76, 1: 6, 2: 48, 3: 54). The published
summary describes labels that still exist.
