# Release check — 2026-09-02, session B

Every line below was produced by running the thing, not by reading code. Commands are reproducible from
the repo root. Numbers quoted are verbatim from the files named.

## 1. `git pull --rebase` — FAIL (cannot run)

```
fatal: no upstream configured for branch 'v2-day1'
```
`origin` has only `main`. Sessions A, B and Cowork commit to the same working tree, so there is nothing
to pull; the charter's "pull before every commit" cannot be executed until `v2-day1` is pushed and
tracked. Recorded, not worked around.

## 2. The walk, full registered draws — PASS

`python3 src/walk.py` (no `--fast`; n_boot 2000, n_spa_boot 1000, n_perm 1000, random_draws 25,
placebo_reps 5), 3 m 38 s. Committed as 7903e66 (`data/walk_forward/*` only).

- `summary.json.run_id` = `walk_20260902T181720Z`
- `summary.json.registered.g_target` = "IES-90 level in (d, d+90] + DEAL flag (OUTCOME_MAPPING.md
  Amendment 1+1.1; event_outcomes source='ies90'); sr_outcome_90 retired"
- `summary.json.data_state`: 187 geopolitical events, 160 with an IES-90 level
  (0: 60, 1: 7, 2: 42, 3: 51), 27 `no_independent_outcome`, 95 with a DEAL flag.
- `seal_check`: 1252 / 1252 sealed records re-hash (four runs: 163321Z, 180646Z, 180821Z, 181720Z;
  `reads.jsonl` is append-only, 15 MB and grows ~5 MB per run).
- Results reproduce bdfc815 (run 180821Z) to every printed digit — the seeds are registered.

| daily tier, 241 of 299 reads scored | skill | 95% CI | DM/HLN p |
|---|---|---|---|
| G Brier engine vs climatology | −0.045 | −0.136..+0.039 | 0.283 |
| G Brier engine vs random analogs | +0.020 | −0.064..+0.102 | 0.618 |
| G RPS engine vs climatology | +0.022 | −0.078..+0.117 | 0.638 |
| G RPS engine vs random analogs | +0.086 | −0.012..+0.176 | 0.065 |
| DEAL binary Brier vs climatology (n 62, base 0.065) | −0.215 | −0.895..+0.069 | — |
| P CRPS engine vs climatology | −0.028 | −0.066..+0.012 | 0.146 |
| P CRPS engine vs persistence | +0.164 | +0.119..+0.215 | <0.001 |
| P CRPS engine vs random analogs | +0.036 | −0.006..+0.083 | 0.058 |

G SPA p = 0.945 (best = frozen); permutation p = 0.128; placebo (size-matched) −0.066, CI
−0.115..−0.022, `null_holds: false`; leakage: filtration is binding; spec curve all negative
(median −0.040); verdict `engine:G` SUGGESTIVE / null, `engine:P` SUGGESTIVE / null, audit flag false.
Monthly tier: 14 reads, 0 past burn-in (describes, does not validate).

## 3. The whole suite — PASS

`python3 -m pytest -q`: **316 passed, 6 skipped, 0 failed** (4 m 29 s). Nothing fixed. The six skips
are session A's batch-2 loader tests waiting on licence-restricted or keyed inputs, each with its
instruction in the skip reason: `ei_review` (EI xlsx absent, 403 to scripts), `eia_intl`
(`EIA_API_KEY` unset), `gsdb` (GSDB R5 by request), `nyt` (`NYT_API_KEY` unset), `vdem` (V-Dem v16
form-served), `dots` (IMF DOTS refuses scripted pulls). Not failures; Joe-side inputs (charter §6).

## 4. The desk, end to end (FastAPI `TestClient(backend.app)`)

Script: session B scratch `desk_check.py`; each check re-reads the file the endpoint claims to serve.

| check | status | evidence |
|---|---|---|
| GET /app | PASS | 200, 51,485 bytes |
| GET /api/walk/summary | PASS | 200; `run_id`, `verdict`, `placebo`, `permutation`, `tiers.daily.G/P.engine_vs` equal to `data/walk_forward/summary.json` |
| — carries G.rps, leakage_test, M | **PARTIAL** | endpoint reads keys `rps_vs` and `leakage` (file has `rps`, `leakage_test`) and copies `precision`/`recall`/`base` from `tiers.*.M` whose shape is `{engine: {precision 0.348, recall 0.554, base_rate 0.232}, ...}`; those three blocks come out empty. Handoff item 1. |
| GET /api/walk/list | PASS | 200; 313 rows = the LAST sealed read per event (4 runs in the file); every row's `hash`/`sealed_at` equal that record; `G_brier` equals `scores.jsonl` |
| GET /api/walk/read?id=september_11_attacks_2001 | PASS | 200; the read re-hashes to its seal; `score.read_hash` equals it; `sealed_at` < `outcome.looked_up_at`; outcome level 3 (war), deal 0; engine G {0: .133, 1: 0, 2: .143, 3: .724} |
| GET /api/engine_read?id=september_11_attacks_2001 | PASS | 200; `as_of` 2001-09-11; all 7 analogs dated before it; G counts over IES-90 levels {0: 1, 1: 0, 2: 1, 3: 5}, deal rate .143 (n 7) |
| GET /api/story?id=september_11_attacks_2001 | PASS | 200; `engine` block = the same read (G n 7), labelled "G = IES-90 levels (independent dated codings)"; `trust.walk_forward.verdict` = the summary's verdict object |
| — story `branches` block | **PARTIAL** | still shows the retired `sr_outcome_90` rates (CONTAINED .688 / LIMITED_RETALIATION .125 / WIDENING .125 / RESOLUTION_BY_DEAL .062, n 16) labelled "corpus-derived (subsequent corpus events), not source-audited" — Amendment 1 requires "corpus-derived, retired 2026-09-02". Handoff item 2. |
| — story `trust.walk_forward` rows/label | **PARTIAL** | `rows: []` (old `windows` shape) and label "as computed by src/walk_forward.py"; the verdict itself is current. Handoff item 3. |
| GET /api/ledger | PASS | 200; `engine.walk` carries `run_id walk_20260902T181720Z`, the verdict and per-tier skill from `summary.json`; legacy `engine.rows` is empty by design |

Every number on every surface above traces to `data/walk_forward/summary.json`, `reads.jsonl` or
`scores.jsonl` of run 181720Z, or to the live corpus read (`engine.read`) which reads
`events`, `observations` and `event_outcomes` and writes nothing.

## 5. Claims on surfaces vs the file

- `README.md` line 60: "the placebo is null" — **FAIL** as written. `summary.json.placebo`:
  `vs_random_analogs.skill −0.0662, ci95 [−0.1146, −0.0222], null_holds false`;
  `vs_climatology −0.1117 [−0.163, −0.065]`; `fair_vs_climatology −0.0385 [−0.078, +0.003]`. The engine at
  VIX-matched non-event dates is worse than random analogs, not indistinguishable. Handoff item 4.
- `README.md` "RPS skill +0.02, 95% CI −0.09 … +0.11": file says +0.022, [−0.078, +0.117] — PASS (rounded).
- `README.md` "beats persistence (+0.16, p < 0.001)", "specification curve negative across every
  registered setting", "learning adds nothing over a frozen engine", "filtration is binding",
  "SUGGESTIVE / null on both targets" — PASS, each equals the file.

## 6. Registered files and the events table

Untouched: `WALK_FORWARD_PROTOCOL.md`, `OUTCOME_MAPPING.md`, `PATH.md`, `menu.json`, `events`.
Session B wrote only `data/walk_forward/*`, `data/gates/*`, `data/handoffs/B_to_A_2026-09-02.md`.

## Summary

PASS: walk re-run and committed; G target and run_id recorded; suite 316/0/6; all seven endpoints 200
with every number traced. PARTIAL (session A's files, handoff written): `/api/walk/summary` drops RPS,
leakage and materiality by key mismatch; story `branches` shows the retired label without the required
"retired" wording; story trust label stale. FAIL: `git pull --rebase` has no upstream; README's "the
placebo is null" contradicts the published placebo.
