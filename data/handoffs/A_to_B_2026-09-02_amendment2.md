# Handoff A -> B, 2026-09-02: IES-90 rebuilt under Amendment 2 — the walk should re-run

`event_outcomes` source='ies90' was rebuilt (commit 6098539) under OUTCOME_MAPPING.md Amendment 2
(dc96877): dyadic precedence, chokepoint littoral map as location only, `basis` + `rule_fired` on every
level row. The fields the walk reads (`level`, `deal`, `no_independent_outcome`) are unchanged in name.
What changed in the labels:
- uncovered events 27 -> 3 (the littoral map gives the 24 chokepoint-only events a location set);
- level counts now war 54 / force 48 / threat 6 / none 76; basis dyadic 29 / location 155;
- the earlier run's labels stay in the sealed reads (reads.jsonl is append-only).

Per data/gates/step8_2026-09-02.md Gate 3: `python3 src/walk.py` re-runs on the new labels and the §7
audit flag stays false until Joe records the 30-event audit (`data/audits/ies90_audit_30.csv`,
regenerated with `basis` / `rule_fired` columns). Nothing for A to do on the walk itself.

Also for B's information: `src/acceptance_v2.py --dod` now prints PATH §3 D1–D7. D4 reads PARTIAL only
because the daily G tier carries three baselines (climatology, frozen, random_analogs) where §3 says four.
