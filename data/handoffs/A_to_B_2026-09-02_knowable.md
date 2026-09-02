# Handoff A -> B, 2026-09-02: situation fields now carry knowable_at (WORLD_STATE_FRAMEWORK.md Amendment A)

`situation_state` now holds the situation-record fields (`sr_actor`, `sr_target`, `sr_conflict_scope`, `sr_tempo`,
`sr_alliance`, `sr_diplomatic`, `sr_target_capacity`, `sr_asset_role`) under entity `situation`, each with
`vintage = knowable_at` by the registered rule, and the join DROPS a field whose knowable_at is after the event date.
Counts as computed (data/state/situation_knowable.json, 2026-09-02T19:22Z):

| | count |
|---|---|
| situation fields on the 313 records | 786 |
| kept at t (source URL carries its own date) | 60 |
| dropped: knowable only at the coding run (2026-09-02) | 726 |
| unknown | 0 |
| events with NO situation field at t | 262 of 313 |

Rule breakdown: 76 fields dated from the cited URL's path, 297 from an undated URL (coding date), 413 corpus-derived
(coding date). The engine's similarity fields (src/engine, session B) still read `events.sr_*` directly; under §1 they
remain "taken as coded". The next walk can either read situation fields from `situation_state` (then 262 events
have none at t) or keep the §1 limitation and quote the count above. The remedy is per-field contemporaneous
sources (Joe's coding work), not a code change.
