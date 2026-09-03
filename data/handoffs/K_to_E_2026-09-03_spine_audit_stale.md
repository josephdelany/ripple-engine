# K → E, 2026-09-03 — `data/spine/audit.json` carries pre-Amendment-4 IES-90 counts

`event_outcomes` source `ies90` was rebuilt to OUTCOME_MAPPING Amendment 4 today on Joe's
ruling. `src/spine_audit.py` reads that table live, so **the code is fine**; only its last
published output is stale.

`data/spine/audit.json` currently records:

    ies90_level: 184   ies90_none: 3   ies90_uncovered: 126

The table now holds **132** events with a level and **55** `no_independent_outcome` (52
undated-for-W, 3 uncovered). Re-running `python3 src/spine_audit.py` refreshes it; K did not,
because `data/spine/**` and `src/spine_audit.py` are yours under SESSION_CHARTER §1.

One thing to know when you do: `no_independent_outcome` now has **two** reasons, carried in
`rule_fired` — `UNCOVERED` (no source covers the window, 3 events) and `UNDATED.continuation`
(a source covers it but records only a conflict it cannot date inside the window, 52 events).
`spine_audit.py`'s three-way `level / no_independent_outcome / uncovered` split reads the
`no_independent_outcome` row and will lump them together; splitting them would say something
useful about corpus coverage, but that is your call, not K's.

The pre-rebuild record is tagged `record-pre-amendment-4` (`5a2c58f` → `18561e2`).
Per-event before/after: `data/state/ies90_amendment4_counts.json` → `rows_changed.rows`.
