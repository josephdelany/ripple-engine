# STATE OF THE ENGINE — generated 2026-09-02T18:31:53+00:00

_Generated from the live `data/oil.db` and the published receipts by `src/state_of_engine.py` — not hand-typed. Every number names its receipt. The 2026-08-04 hand-written after-picture is kept at `docs/STATE_OF_THE_ENGINE_2026-08-04.md`._

HEAD: `1cddad2 2026-09-02 Release check 2026-09-02 (session B): walk re-run 181720Z committed; suite 316 passed / 6 skipped; de`

## 1. Corpus (`events`, receipt: `data/events.csv`, `DATA_DICTIONARY.md`)

- 313 events; by type: sanctions 57, policy_response 57, conflict_escalation 55, opec_decision 52, infrastructure_attack 48, chokepoint_disruption 27, demand_shock 17
- geopolitical events by decade: 1970s 8, 1980s 8, 1990s 9, 2000s 17, 2010s 55, 2020s 90
- `sr_*` situation-record columns: corpus-derived; `sr_outcome_90` / `sr_outcome_30` RETIRED as outcomes (OUTCOME_MAPPING.md Amendment 1)

## 2. Data (`series`, `observations`; receipts: `data/engine_status.json`, `data/health_status.json`)

- 598 series, 467,436 observations; last obs 2026-09-02
- engine status **GREEN** at 2026-09-02T18:30: GREEN: fresh, covered, last run OK, framework sound
- freshness: 0 DEAD, 0 STALE (heartbeat); integrity findings: `data/integrity_report.txt`

## 3. World state (`state_panel`; receipt: `data/state/status.json`, `WORLD_STATE_CODEBOOK.md`)

- 280,208 panel rows from 17 loaders (status 2026-09-02); fields loaded 34 / registered 70; unloaded: 36
- licence-restricted inputs live in `data/state/local/` (never committed; README there); keyless raw downloads in `data/state/raw/` (gitignored, rebuilt by loaders)

## 4. Independent outcomes — IES-90 (`event_outcomes` source='ies90'; receipts: `data/state/ies90_distribution.json`, `OUTCOME_MAPPING.md`)

- registration: OUTCOME_MAPPING.md Amendment 1 + 1.1 + 2 (2026-09-02); 187 geopolitical events; level counts {'3': 54, '0': 76, '2': 48, '1': 6, 'null': 3}
- by basis (Amendment 2): {'None': {'null': 3}, 'dyadic': {'3': 8, '0': 14, '2': 5, '1': 2}, 'location': {'3': 46, '0': 62, '2': 43, '1': 4}}
- coverage by source: {'war': 61, 'icb': 95, 'mid': 57, 'ged': 168, 'midi': 37}; uncovered (no_independent_outcome): 3
- GED is location-only (no dyad field in the cache); 77 GED names unmapped (listed in the file)
- audit for Joe: `data/audits/ies90_audit_30.csv` — 30 events / 63 source rows; Joe's record: `data/audits/outcome_audit.json` ABSENT
- for the record: Step 4 kappa vs the retired label — precedence κ 0.0606 (n 184); `data/state/outcomes_kappa.json`, `data/audits/outcome_audit_60.csv`

## 5. The walk (receipt: `data/walk_forward/summary.json`, `WALK_FORWARD_PROTOCOL.md`)

- run `walk_20260902T181720Z` generated 2026-09-02T18:18; G target: IES-90 level in (d, d+90] + DEAL flag (OUTCOME_MAPPING.md Amendment 1+1.1; event_outcomes source='ies90'); sr_outcome_90 retired
- monthly tier: 14 reads, 0 scored after burn-in, horizon 3 months; G skill vs climatology None (dm_p None); permits validation: False
- daily tier: 299 reads, 241 scored after burn-in, horizon 20 trading days; G skill vs climatology -0.04526627835037411 (dm_p 0.2828930199687061); permits validation: True
- engine:G verdict: SUGGESTIVE / null; engine:P: SUGGESTIVE / null; audit flag: False
- leakage test asserted: True (filtration is binding); placebo skill -0.06621959628456775; permutation p 0.12787212787212787

## 6. Definition of done — PATH.md §3 D1–D7 (receipt: `data/acceptance_dod.json`, `python3 src/acceptance_v2.py --dod`)

_recorded 2026-09-02T18:31_

| item | status | evidence | note |
|---|---|---|---|
| D1 pytest green incl. every named test | **PARTIAL** | `tests/` | 318 passed, 6 skipped, 4 warnings in 298.47s (0:04:58); PATH-named tests absent: ['tests/test_demo_911.py'] |
| D2 status.py >=12 loaders + coverage by block | **PASS** | `data/state/status.json` | 17 loaders (distinct sources behind 34 loaded fields, status 2026-09-02); coverage by block x decade present=True; fields loaded 34 / registered 70 |
| D3 kappa published; rule applied; audit file | **PARTIAL** | `data/audits/ies90_audit_30.csv` | kappa published (data/state/outcomes_kappa.json); the kappa<0.6 replacement rule is superseded by OUTCOME_MAPPING.md Amendment 1 (labels retired, not replaced); 30-event IES-90 audit sheet present; Joe's audit NOT recorded (data/audits/outcome_audit.json absent) |
| D4 walk summary: tiers, baselines, DM/SPA, placebo, permutation, regimes, spec curve, power, leakage | **PARTIAL** | `data/walk_forward/summary.json` | run walk_20260902T181720Z; present: ['both tiers', 'DM p-values', 'SPA p-value', 'placebo', 'permutation', 'regime blocks', 'specification curve', 'power', 'leakage test asserted']; missing: ["four baselines (daily G has 3: ['climatology', 'frozen', 'random_analogs'])"] |
| D5 9/11, 1990, 2026 demos from sealed inputs on /walk | **PARTIAL** | `data/walk_forward/reads.jsonl` | sealed reads {'september_11_attacks_2001': 5, 'iraq_invades_kuwait_1990': 5, 'hormuz_closure_2026': 5}; walk read route=True; tests/test_demo_911.py present=False (PATH Step 10 is Cowork + Joe) |
| D6 VALIDATED only via protocol §7 | **PASS** | `data/walk_forward/summary.json` | protocol §7 verdicts VALIDATED: none (all SUGGESTIVE / null); v2 surfaces printing VALIDATED without a §7/verdict reference: none |
| D7 tag v3.0; paper; one week in the Ledger | **FAIL** | `git tag / data/ledger/claims.jsonl` | tag v3.0=False (tags: ['v2.0']); paper drafted=False; ledger use on 1 distinct days (needs 7) |

2/7 PASS, 4 PARTIAL, 1 FAIL. The product is finished only when all seven PASS (SESSION_CHARTER.md §5); no surface says it is.

