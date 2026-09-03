# K → B, D and the G_accident session, 2026-09-03 — five §2 hard failures, four of them the same missing flag

`src/exposure_schema.py` now validates `data/exposure/blocks/*.json` against
EXPOSURE_REGISTRATION §2. It found five hard failures. **All five are cheap to fix and none needs
re-research** — no figure is wrong, the provenance is incomplete.

Run it yourself: `python3 src/exposure_schema.py` (or `--strict` to exit non-zero on any hard
failure). Published table: `data/exposure/COVERAGE.md`, `data/exposure/coverage.json`.

## The four

| block | event | failure |
|---|---|---|
| B | `saudi_abqaiq_foiled_2006` | nameplate from a source dated **2006-02-27**, three days after the event, without `retrospective: true` |
| B | `nigeria_mend_bonga_2008` | nameplate from **2008-06-20**, one day after the event, without `retrospective: true` |
| B | `kirkuk_ceyhan_isis_2014` | `days_to_full_restore: "ongoing"` with no `ongoing_stamp_date` |
| D | `colonial_pipeline_shutdown_2021` | nameplate from **2021-05-11**, four days after the event, without `retrospective: true` |
| G_accident | `pes_philadelphia_fire_2019` | nameplate from **2019-07-03**, twelve days after the event, without `retrospective: true` |

**The four vintage ones are a flag, not a figure.** §3 of PHYSICAL_EXPOSURE and §2 of this
registration both say a register's `knowable_at` is its publication date, and §2 says in terms
that where only a later source gives the figure "the value is flagged `retrospective: true`" and
"a test asserts the flag is carried". These are one, three and four days late — trivially
post-event — but the flag is what tells Stage 2 the value is inadmissible for any claim about
what was knowable at *t*, and a three-day-late source and a three-year-late source are
indistinguishable downstream without it. Add `"retrospective": true` to the nameplate provenance
and they pass.

**The `ongoing` one needs a date.** §2 permits `ongoing` for `days_to_full_restore` "with a stamp
date", because "ongoing" is only meaningful relative to when it was checked. Add
`ongoing_stamp_date` and it passes. (Block F uses `ongoing` once, for the Hormuz closure, stamped
`2026-08-05` on a Lloyd's List brief.)

## This is a schema problem, not four separate slips

Four different sessions, working independently, filled a nameplate from a post-event source and
did not set `retrospective`. That is not four people being careless — **the block template has no
`retrospective` key at all**, so there is nothing on the form to leave blank and nothing to
prompt you. §2 requires the flag and says "a test asserts the flag is carried"; until now no test
did. Worth adding the key to the template as an explicit `"retrospective": "unknown"` so it has
to be answered rather than remembered. That is a change to the block schema and therefore Joe's
or the schema owner's call, not K's.

## Two of them are currently declared COMPLETE

`saudi_abqaiq_foiled_2006` and `kirkuk_ceyhan_isis_2014` carry `status: COMPLETE` and compute as
`INVALID`. That is not a criticism of the research — both look well sourced — it is why the
validator **computes** status from the fields and never reads the `status` a block declares.
A session marking its own work COMPLETE is not evidence that it is, and the disagreements are
listed in `COVERAGE.md` with the computed value governing.

## One thing that is NOT a failure, so nobody "fixes" it

`saudi_abqaiq_foiled_2006` has `capacity_affected_kbd: 0`, `days_to_partial_restore: 0`,
`days_to_full_restore: 0`. **That is correct and the validator treats 0 as a value, not a
missing field.** The attack was foiled; nothing went offline; zero is the measurement. Only the
registered unknown markers count as missing, and `test_a_measured_zero_is_a_value_not_a_missing_field`
pins it — because treating a real zero as absent is `max(default=0)` run backwards, and it would
silently drop the cleanest observations in the corpus.

## Where coverage stands (snapshot; A–E are still being filled)

80 events in 7 blocks: **COMPLETE 5, PARTIAL 47, EMPTY 23, INVALID 5.**

`G_accident` declares `counts_toward_gate: false` under Amendment 1, and the validator honours
that rather than overriding it: the gate is counted over A–F only — **5 COMPLETE of the 75** — and
a block that says its rows do not count cannot carry the gate over the line. `n_complete_including_excluded_blocks`
is published beside it so the exclusion is visible rather than silent.

One number to reconcile: `G_accident`'s own `gate_note` says "the attack attempt closed at 8 of
75". The validator computes **5**. The difference is that some events declaring `COMPLETE` do not
compute as COMPLETE — three of them are the hard failures above. Not a criticism of that
session's count; it is the reason the validator computes rather than sums declarations. §5's gate is 30 COMPLETE,
so on today's numbers Stage 1 is **descriptive only and no verdict is issued** — registered in
advance so it cannot be waived now the number is known. Fixing these four moves 2 of them into
COMPLETE and takes the total to 7. The gate is a long way off and the honest thing is that it may
not be reachable: a large share of the partials across every block are *unit* problems, not
research gaps — operators publish refinery capacity in tonnes per year, and converting to kb/d
needs a barrels-per-tonne factor no source states. At least three sessions independently hit that
and all three correctly declined to convert. It is worth someone registering a decision on it,
because it is currently the single largest cause of PARTIAL in the corpus.
