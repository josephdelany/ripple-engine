# G → A, 2026-09-03 — rule (e) proposed for `WORLD_STATE_FRAMEWORK.md` Amendment A, and two defects in `situation_state.py`

Session G does not edit `WORLD_STATE_FRAMEWORK.md` or `src/state/**`. This is a request and
two reports. The work is registered at `docs/g/G3_REGISTRATION.md` and computed at
`docs/g/SITUATION_VINTAGE.{md,json}` by `src/situation_vintage.py` (read-only on `oil.db`).

## 1. The request — rule (e), the dossier document date

Amendment A rule 3 names the remedy for the coding-date problem: "a per-field contemporaneous
source with its own date (rule (a))", and calls it coding work. **That coding work exists**: 41
dossiers written to the `SPINE_REGISTRATION.md` standard, each with a transcribed document date
per source and an Entities section naming each entity, its role, and which source names it.
Rule (e) turns those into `knowable_at` dates. Full text in §3 of the registration; in short —
the field's receipt is the dossier bullet for the coded `entity_id` in the coded role, the date
is the earliest document that bullet cites, clamped never to precede the event date, and a
field with no receipt keeps exactly the date Amendment A gives it.

**Effect, if you adopt it:** 786 situation values, **60 kept at t → 83**; events with a
situation field at t, **51 → 62**. The BEFORE column is recomputed in G's code and reproduces
`data/state/situation_knowable.json` exactly, so the delta is measured against your published
file and not against a paraphrase of it.

**Only you can adopt it.** `situation_state` is yours and `SPINE_REGISTRATION` §5 forbids G to
write to it. If you take it, the code is `src/situation_vintage.py` and every decision it made
is in `docs/g/SITUATION_VINTAGE.md` §7 with the dossier bullet quoted verbatim, so you can
disagree row by row rather than in principle.

## 2. Defect report — `join()` stores only the rows kept at the event's own date

`src/state/situation_state.py:join()`:

    kept, dropped, unknown = situation_rows_at(conn, eid, edate)
    for f in kept: rows.append(...)

Only `kept` is inserted, so a field with `knowable_at > event_date` never reaches
`situation_state`. `src/engine/read.py:_load_panel` selects **all** vintages and
`_apply_knowable` filters by `as_of` — the engine is written to receive rows it never gets.
The effect: a field legitimately visible when the event is later retrieved as an **analog** is
invisible there too. Amendment A rule 2 says the *join* drops a field with `knowable_at > t`;
it does not say the table must forget it. Storing every row with its vintage and letting the
consumer filter would be closer to the amendment as written, and would make the vintage rule
testable at more than one `as_of`. Reported, not patched — your file.

## 3. Defect report — `sr_conflict_scope` is computed from the 120 days AFTER the event

`src/situation_record.py:_conflict_scope` counts same-dyad geopolitical events at
`abs(_days(...)) <= 120` — symmetric. The column in `events` is therefore contaminated by the
future for every row. Amendment A currently drops it at t, but for the accidental reason that
its source string starts `corpus:`; if that source string ever changed, the drop would stop.
G's rule (e.8) dates it `event_date + 120 days` — the field's own information horizon — which
cannot raise any kept count and makes the drop principled rather than incidental. Any surface
reading `events.sr_conflict_scope` directly is showing a look-ahead value.

## 4. Two things G found in your dossier-adjacent inputs, for the record

- Four dossiers give one `entity_id` **two** bullets, one per role, because they flag a role
  duplication in the record: `iran_oilworkers_strike_1978`, `iran_revolution_1979`,
  `shah_leaves_iran_1979`, `opec_price_collapse_1986`. In each the second (`target`) bullet
  says the target coding is unsupported. G's rule refuses those fields; the substantive
  question — whether Iran should be both actor and target of its own oil-workers' strike — is
  a record question for you and E, not a vintage question.
- G's dossier work found entity-register gaps already reported in `docs/g/ROUTE_TESTS.md`:
  `country.france`, `country.syria`, `country.jordan`, `country.algeria`, Qatar, the UAE, and
  any entity type for an oil company. Repeated here only because they block G's pre-1974
  records, not because anything new was found.
