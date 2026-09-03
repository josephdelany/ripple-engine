# F → B, 2026-09-02 — the hostility precondition, and what it does to the published G run

## What you have to implement (v3, not now)
`OUTCOME_MAPPING.md` **Amendment 3** is committed (`bb697ac`). It adds a precondition to the
G target: an event is G-scorable only where the record shows a hostile act (H1) by a party
the record names at least to actor class (H2). Failing H1 → `no_independent_outcome`,
excluded and counted, exactly as `opec_decision` / `demand_shock` / `policy_response`
already are. H1-yes / H2-no → scored, flagged `hostility = 'hostile_unattributed'`.

What that means for `src/engine/**` and `src/walk.py`, all of which are yours:
- IES-90 gains a `hostility` value per geopolitical event; a `non_hostile` or `ambiguous`
  event returns `no_independent_outcome` **before** any source is consulted.
- `no_independent_outcome` already has a path through your code; this widens what feeds it.
  Nothing else changes — no window, no source, no precedence, no level mapping.
- The coding for the two classes audited is published event by event in
  `data/spine/CLASS_AUDIT.md` §3. `conflict_escalation` and `sanctions` are **not yet
  audited**; do not implement the precondition for those two until they are, or you will
  split the four geopolitical classes two ways.
- `tests/test_hostility.py::test_the_audit_applies_nothing` asserts there is no `hostility`
  field in `event_outcomes` today. When you implement, that test is the tripwire: it fails on
  purpose, and the fix is to re-state CLASS_AUDIT §6 against the new run, not to delete it.

## What you must NOT do
Amendment 3 §A3.5: **the published run is not re-scored.** `reads.jsonl` is sealed against
the target as it stood; re-scoring under a later definition breaks the seal and lets a
definition be chosen once its effect on the score is known. Run `walk_20260902T210135Z`
stands as published, with its n and its scores. Post-amendment runs are reported separately
and never pooled with it.

## The numbers, for your run notes and for the surfaces
Set: the 150 daily-tier scored G reads of `walk_20260902T210135Z`
(`summary.json` `/tiers/daily/G`, n = 150).

| | n | level-0 | share |
|---|---:|---:|---:|
| as published | 150 | 63 | 42.0% |
| less the 6 `non_hostile` | 144 | 59 | 41.0% |
| less the 3 `ambiguous` as well | 141 | 56 | 39.7% |
| less the 2 `hostile_unattributed` as well | 139 | 56 | 40.3% |

**9 of 150 affected (6.0%)**: `venezuela_blackout_2019` (0), `druzhba_contamination_2019`
(**2**), `suez_ever_given_2021` (0), `cpc_novorossiysk_storm_2022` (0),
`kurdistan_ceyhan_halt_2023` (**2**), `codelco_elteniente_2025` (0) — non-hostile; plus
`btc_pipeline_blast_2008` (0), `saudi_suspends_bab_el_mandeb_2018` (0),
`colonial_pipeline_shutdown_2021` (0) — ambiguous.

Five more affected events are already outside the 150 (monthly tier or burn-in):
`abqaiq_arabian_1977`, `iran_oilworkers_strike_1978`, `suez_tropic_brilliance_2004`,
`earnest_will_1987`, `libya_jathran_blockade_2013`. They are still **retrieved as
analogues**, which is the part that does not show up in the headline: an oil-workers'
strike sits in the precedent set carrying IES-90 level 3, war.

Surface note required by §A3.5 wherever this run's G results appear:
> scored before Amendment 3; includes 6 non-hostile events for which the G target is
> undefined (9 counting ambiguous) — `data/spine/CLASS_AUDIT.md` §6

Recomputation of every figure above is in `tests/test_hostility.py::
test_section_6_impact_recomputes_from_the_sealed_scores` — it reads your scores file and
never writes to it.

— Session F
