# STATE OF THE ENGINE — generated 2026-09-02T19:54:11+00:00

> **SUPERSEDED, 2026-09-03.** Generated 2026-09-02T19:54Z, which is **two runs and two
> registered amendments ago**. Every escalation number here predates both `OUTCOME_MAPPING.md`
> Amendment 4 (which took the target from 184 labelled events to 132) and the re-run
> `walk_20260903T052633Z`. It is accurate as a receipt of the state at its own timestamp and
> should not be read as current. For current numbers see `README.md` and
> `docs/PAPER_DRAFT.md`; for what is outstanding, `OPEN_ITEMS.md`.

_Generated from the live `data/oil.db` and the published receipts by `src/state_of_engine.py` — not hand-typed. Every number names its receipt. The 2026-08-04 hand-written after-picture is kept at `docs/STATE_OF_THE_ENGINE_2026-08-04.md`._

HEAD: `5026731 2026-09-02 Brief 2 B-8 (D2 finding 2, code): the admission sheet is blind -- pre1987_candidates.csv carries no o`

## 1. Corpus (`events`, receipt: `data/events.csv`, `DATA_DICTIONARY.md`)

- 313 events; by type: sanctions 57, policy_response 57, conflict_escalation 55, opec_decision 52, infrastructure_attack 48, chokepoint_disruption 27, demand_shock 17
- geopolitical events by decade: 1970s 8, 1980s 8, 1990s 9, 2000s 17, 2010s 55, 2020s 90
- `sr_*` situation-record columns: corpus-derived; `sr_outcome_90` / `sr_outcome_30` RETIRED as outcomes (OUTCOME_MAPPING.md Amendment 1)

## 2. Data (`series`, `observations`; receipts: `data/engine_status.json`, `data/health_status.json`)

- 644 series, 624,740 observations; last obs 2026-09-02
- engine status **GREEN** at 2026-09-02T19:49: GREEN: fresh, covered, last run OK, framework sound
- freshness: 0 DEAD, 0 STALE (heartbeat); integrity findings: `data/integrity_report.txt`

## 3. World state (`state_panel`; receipt: `data/state/status.json`, `WORLD_STATE_CODEBOOK.md`)

- 352,295 panel rows from 27 loaders (status 2026-09-02); fields loaded 49 / registered 70; unloaded: 21
- licence-restricted inputs live in `data/state/local/` (never committed; README there); keyless raw downloads in `data/state/raw/` (gitignored, rebuilt by loaders)

## 4. Independent outcomes — IES-90 (`event_outcomes` source='ies90'; receipts: `data/state/ies90_distribution.json`, `OUTCOME_MAPPING.md`)

- registration: OUTCOME_MAPPING.md Amendment 1 + 1.1 + 2 (2026-09-02); 187 geopolitical events; level counts {'3': 54, '0': 76, '2': 48, '1': 6, 'null': 3}
- by basis (Amendment 2): {'None': {'null': 3}, 'dyadic': {'3': 8, '0': 14, '2': 5, '1': 2}, 'location': {'3': 46, '0': 62, '2': 43, '1': 4}}
- coverage by source: {'war': 61, 'icb': 95, 'mid': 57, 'ged': 168, 'midi': 37}; uncovered (no_independent_outcome): 3
- GED is location-only (no dyad field in the cache); 77 GED names unmapped (listed in the file)
- audit for Joe: `data/audits/ies90_audit_30.csv` — 30 events / 63 source rows; Joe's record: `data/audits/outcome_audit.json` ABSENT
- for the record: Step 4 kappa vs the retired label — precedence κ 0.0606 (n 184); `data/state/outcomes_kappa.json`, `data/audits/outcome_audit_60.csv`

## 5. The walk (receipt: `data/walk_forward/summary.json`, `WALK_FORWARD_PROTOCOL.md`)

- run `walk_20260902T193022Z` generated 2026-09-02T19:34; G target: IES-90 level in (d, d+90] + DEAL flag (OUTCOME_MAPPING.md Amendment 1 and later amendments; event_outcomes source='ies90'; the label registration the run saw is recorded in data_state.ies90_registration); sr_outcome_90 retired
- monthly tier: 14 reads, 0 scored after burn-in, horizon 3 months; G skill vs climatology None (dm_p None); permits validation: False
- daily tier: 299 reads, 253 scored after burn-in, horizon 20 trading days; G skill vs climatology -0.0053315237127760096 (dm_p 0.8837017777161833); permits validation: True
- engine:G verdict: SUGGESTIVE / null; engine:P: SUGGESTIVE / null; audit flag: False
- leakage test asserted: True (filtration is binding); placebo skill -0.018083318942162085; permutation p 0.001998001998001998

## 6. Definition of done — PATH.md §3 D1–D7 (receipt: `data/acceptance_dod.json`, `python3 src/acceptance_v2.py --dod`)

_recorded 2026-09-02T19:53_

| item | status | evidence | note |
|---|---|---|---|
| D1 pytest green incl. every named test | **PASS** | `tests/` | 354 passed, 13 skipped, 4 warnings in 544.75s (0:09:04) |
| D2 status.py >=12 loaders + coverage by block | **PASS** | `data/state/status.json` | 27 loaders (distinct sources behind 49 loaded fields, status 2026-09-02); coverage by block x decade present=True; fields loaded 49 / registered 70 |
| D3 kappa published; rule applied; audit file | **PARTIAL** | `data/audits/ies90_audit_30.csv` | kappa published (data/state/outcomes_kappa.json); the kappa<0.6 replacement rule is superseded by OUTCOME_MAPPING.md Amendment 1 (labels retired, not replaced); 30-event IES-90 audit sheet present; Joe's audit NOT recorded (data/audits/outcome_audit.json absent) |
| D3a label audit recorded by Joe (auditor joe, all rows, kappa) | **FAIL** | `data/audits/outcome_audit.json` | absent -- Joe records it with python3 src/audit_ies90.py (never the code) |
| D4 walk summary: tiers, baselines, DM/SPA, placebo, permutation, regimes, spec curve, power, leakage | **PARTIAL** | `data/walk_forward/summary.json` | run walk_20260902T182828Z; present: ['both tiers', 'DM p-values', 'SPA p-value', 'placebo', 'permutation', 'regime blocks', 'specification curve', 'power', 'leakage test asserted']; missing: ["four baselines (daily G has 3: ['climatology', 'frozen', 'random_analogs'])"] |
| D5 9/11, 1990, 2026 demos from sealed inputs on /walk | **PASS** | `data/walk_forward/reads.jsonl` | sealed reads {'september_11_attacks_2001': 7, 'iraq_invades_kuwait_1990': 7, 'hormuz_closure_2026': 7}; /api/walk/read route; tests/test_demo_911.py |
| D6 VALIDATED only via protocol §7 | **PASS** | `data/walk_forward/summary.json` | protocol §7 verdicts VALIDATED: none (all SUGGESTIVE / null); v2 surfaces printing VALIDATED without a §7/verdict reference: none |
| D6a reader accuracy measured on the gold set (model mode) | **PASS** | `data/reader_eval/score.json` | class accuracy 0.84 (threshold 0.8), entity F1 0.9348, modes {'llm': 100}; gold: coded by session A, unaudited by Joe |
| D7 tag v3.0; paper; one week in the Ledger | **FAIL** | `git tag / data/ledger/claims.jsonl` | tag v3.0=False (tags: ['v2.0', 'v2.5']); paper drafted=False; ledger use on 1 distinct days (needs 7) |

5/7 PASS, 2 PARTIAL, 2 FAIL. The product is finished only when all seven PASS (SESSION_CHARTER.md §5); no surface says it is.

