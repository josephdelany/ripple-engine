# Release check — 2026-09-02, session B

Every line below was produced by running the thing, not by reading code. Commands are reproducible from
the repo root. Numbers quoted are verbatim from the files named. This file supersedes its first version
(1cddad2), which checked run 181720Z; session A rebuilt the IES-90 rows under Amendment 2 at 18:25:30Z,
eight minutes after that run read the database, so the walk was re-run and everything below re-checked.

## 1. `git pull --rebase` — PASS (after setting the upstream)

First attempt: `fatal: no upstream configured for branch 'v2-day1'`. The branch already existed on the
remote (`refs/heads/v2-day1` at 0a1c5ed, pushed by session A), so no push was needed:

```
git branch --set-upstream-to=origin/v2-day1 v2-day1
git pull --rebase --autostash      # "Current branch v2-day1 is up to date. Applied autostash."
```
`--autostash` because the launchd refresh keeps six tracked `data/` artifacts dirty in the shared tree
and plain `--rebase` refuses on unstaged changes; the stash held only those six files and re-applied
cleanly (six dirty before, six after; no other session's file touched). Remote head was an ancestor of
local HEAD (behind 0, ahead 2), so the rebase changed nothing. SESSION_CHARTER.md and PATH.md re-read
after the pull: unchanged since the commits this check was written against.

## 2. The walk, full registered draws — PASS

`python3 src/walk.py` (no `--fast`; n_boot 2000, n_spa_boot 1000, n_perm 1000, random_draws 25,
placebo_reps 5), 4 m 35 s, on the Amendment 2 rows (handoff `A_to_B_2026-09-02_amendment2.md`).

- `summary.json.run_id` = `walk_20260902T182828Z`
- `summary.json.registered.g_target` = "IES-90 level in (d, d+90] + DEAL flag (OUTCOME_MAPPING.md
  Amendment 1 and later amendments; event_outcomes source='ies90'; the label registration the run saw is
  recorded in data_state.ies90_registration); sr_outcome_90 retired"
- `summary.json.data_state.ies90_registration` = "OUTCOME_MAPPING.md Amendment 1 + 1.1 + 2 (2026-09-02)",
  generated 2026-09-02T18:25:31+00:00
- `data_state`: 187 geopolitical events, 184 with an IES-90 level (0: 76, 1: 6, 2: 48, 3: 54),
  3 `no_independent_outcome`, 95 with a DEAL flag.
- `seal_check`: 1565 / 1565 sealed records re-hash (five runs: 163321Z, 180646Z, 180821Z, 181720Z,
  182828Z; `reads.jsonl` is append-only, ~19 MB, +5 MB per run — Joe may want a retention rule).
- Run 181720Z (7903e66) on the Amendment 1+1.1 labels stays sealed in the file; its summary is superseded.

| daily tier, 253 of 299 reads scored | skill | 95% CI | DM/HLN p |
|---|---|---|---|
| G Brier engine vs climatology | −0.007 | −0.084..+0.065 | 0.847 |
| G Brier engine vs random analogs | +0.062 | −0.008..+0.130 | 0.068 |
| G Brier engine vs frozen | −0.003 | −0.006..+0.001 | 0.131 |
| G RPS engine vs climatology | +0.072 | −0.008..+0.151 | 0.076 |
| G RPS engine vs random analogs | +0.140 | +0.061..+0.219 | 0.001 |
| DEAL binary Brier vs climatology (n 66, base 0.061) | −0.218 | −0.857..+0.072 | — |
| P CRPS engine vs climatology | −0.028 | −0.062..+0.008 | 0.136 |
| P CRPS engine vs persistence | +0.163 | +0.121..+0.210 | <0.001 |
| P CRPS engine vs random analogs | +0.035 | −0.002..+0.077 | 0.053 |

G SPA p = 0.793 (best = M07_uniform_k12); label permutation p = 0.008 with observed Brier skill
+0.0005 (the permuted-label engines are strongly negative, so zero ranks high — the registered gate
`skill > 0` is still False); placebo, size-matched −0.024, CI −0.053..+0.007, `null_holds: true`
(vs climatology −0.081, CI −0.112..−0.048; size-corrected −0.008, CI −0.043..+0.028); leakage:
filtration is binding; spec curve median −0.023, share positive 0.17; regime blocks G −0.013 / −0.014 /
−0.007, P −0.028 / −0.011 / −0.028; power (minimum detectable skill at 80%) G 0.123, P 0.058.
Verdict `engine:G` SUGGESTIVE / null, `engine:P` SUGGESTIVE / null, audit flag false.
Monthly tier: 14 reads, 0 past burn-in (describes, does not validate).

Change from the Amendment 1+1.1 run (181720Z): G Brier vs climatology −0.045 → −0.007; RPS vs random
analogs +0.086 (p 0.065) → +0.140 (p 0.001); placebo `null_holds` false → true; scored reads 241 → 253
(the 24 chokepoint events now carry a location-based level). RPS vs random analogs is the only G
comparison that clears p < 0.05; it is not a registered gate (gate report Gate 1, A.2).

## 3. The whole suite — PASS

`python3 -m pytest -q` after the re-run: **318 passed, 6 skipped, 0 failed** (3 m 44 s; the count rose
from 316 with session A's two new tests). Nothing fixed. The six skips are session A's batch-2 loader
tests waiting on licence-restricted or keyed inputs, each with its instruction in the skip reason:
`ei_review` (EI xlsx absent, 403 to scripts), `eia_intl` (`EIA_API_KEY` unset), `gsdb` (GSDB R5 by
request), `nyt` (`NYT_API_KEY` unset), `vdem` (V-Dem v16 form-served), `dots` (IMF DOTS refuses scripted
pulls). Not failures; Joe-side inputs (charter §6).

## 4. The desk, end to end (FastAPI `TestClient(backend.app)`), on run 182828Z

Each check re-reads the file the endpoint claims to serve.

| check | status | evidence |
|---|---|---|
| GET /app | PASS | 200, 51,485 bytes |
| GET /api/walk/summary | PASS | 200; `run_id`, `verdict`, `placebo`, `permutation`, `tiers.daily.G/P.engine_vs` equal to `data/walk_forward/summary.json` |
| — carries G.rps, leakage_test, M | **PARTIAL** | endpoint reads keys `rps_vs` and `leakage` (file has `rps`, `leakage_test`) and copies `precision`/`recall`/`base` from `tiers.*.M` whose shape is `{engine: {precision 0.337, recall 0.544, base_rate 0.225}, ...}`; those three blocks come out empty. Handoff item 1. |
| GET /api/walk/list | PASS | 200; 313 rows = the LAST sealed read per event (5 runs in the file); every row's `hash`/`sealed_at` equal that record; `G_brier` equals `scores.jsonl` |
| GET /api/walk/read?id=september_11_attacks_2001 | PASS | 200; the read re-hashes to its seal; `score.read_hash` equals it; `sealed_at` < `outcome.looked_up_at`; outcome level 3 (war), deal 0; engine G {0: .261, 1: 0, 2: .287, 3: .453} |
| GET /api/engine_read?id=september_11_attacks_2001 | PASS | 200; `as_of` 2001-09-11; all 7 analogs dated before it; G counts over IES-90 levels {0: 2, 1: 0, 2: 2, 3: 3}, deal rate .143 (n 7) |
| GET /api/story?id=september_11_attacks_2001 | PASS | 200; `engine` block = the same read (G n 7), labelled "G = IES-90 levels (independent dated codings)"; `trust.walk_forward.verdict` = the summary's verdict object |
| — story `branches` block | **PARTIAL** | still shows the retired `sr_outcome_90` rates (CONTAINED .688 / LIMITED_RETALIATION .125 / WIDENING .125 / RESOLUTION_BY_DEAL .062, n 16) labelled "corpus-derived (subsequent corpus events), not source-audited" — Amendment 1 requires "corpus-derived, retired 2026-09-02". Handoff item 2. |
| — story `trust.walk_forward` rows/label | **PARTIAL** | `rows: []` (old `windows` shape) and label "as computed by src/walk_forward.py"; the verdict itself is current. Handoff item 3. |
| GET /api/ledger | PASS | 200; `engine.walk` carries `run_id walk_20260902T182828Z`, the verdict and per-tier skill from `summary.json`; legacy `engine.rows` is empty by design |

Every number on every surface above traces to `data/walk_forward/summary.json`, `reads.jsonl` or
`scores.jsonl` of run 182828Z, or to the live corpus read (`engine.read`), which reads `events`,
`observations` and `event_outcomes` and writes nothing.

## 5. Claims on surfaces vs the file

- `README.md` lines 56–63 describe run 181720Z ("241 scored reads", "RPS skill +0.02, 95% CI −0.09 …
  +0.11", "borderline against random analogs", "the placebo is null"). Against run 182828Z: scored reads
  are 253; RPS vs climatology is +0.072 (CI −0.008..+0.151); RPS vs random analogs is +0.140 (CI
  +0.061..+0.219, p 0.001) — no longer borderline; the size-matched placebo now holds (−0.024, CI
  −0.053..+0.007) while the climatology-referenced one is −0.081 (CI −0.112..−0.048). **PARTIAL**: stale
  by one run; no sentence is false as of 181720Z except "the placebo is null", which that run's
  `null_holds: false` contradicted and this run's `true` now supports. Handoff item 4 amended.
- README "beats persistence (+0.16, p < 0.001)", "learning adds nothing over a frozen engine", "the
  filtration is binding", "SUGGESTIVE / null on both targets" — PASS, each equals the file. "specification
  curve is negative across every registered setting" — PARTIAL: now 9 of 54 specifications are positive
  (`share_positive 0.167`, max +0.015).
- `acceptance_v2 --dod` D4 "four baselines" reads PARTIAL for G (three). Protocol §4 lists persistence as
  a P baseline only ("Persistence / no-change for P"); a categorical +90d level has no no-change forecast.
  G's three and P's four are as registered. Not a walk defect; a reading of D4 for session A / Joe.

## 6. Registered files and the events table

Untouched: `WALK_FORWARD_PROTOCOL.md`, `OUTCOME_MAPPING.md`, `PATH.md`, `menu.json`, `events`.
Session B wrote `src/walk.py` (the summary now records the IES-90 registration it read; the uncovered
count in `limits` is computed, not typed), `data/walk_forward/*`, `data/gates/*`,
`data/handoffs/B_to_A_2026-09-02.md`.

## Summary

PASS: walk re-run on the Amendment 2 labels and committed; G target, label registration and run_id
recorded; suite 318 / 0 / 6; all seven endpoints 200 with every number traced. PARTIAL (session A's
files, handoff written): `/api/walk/summary` drops RPS, leakage and materiality by key mismatch; story
`branches` shows the retired label without the required "retired" wording; story trust label stale;
README described the previous run (session A has since updated it, 0e31cd0). FAIL: none.
The one FAIL of the first pass (`git pull --rebase`, no upstream) is resolved above.
