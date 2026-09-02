# Release check — 2026-09-02, session B

Every line was produced by running the thing, not by reading code. This file supersedes its earlier
versions (1cddad2, d3df9af): it covers the run published by Brief 2, `walk_20260902T210135Z`, and keeps the
record of what each earlier check found. Numbers are verbatim from `data/walk_forward/summary.json`.

## 1. `git pull --rebase` — PASS

Upstream was set to the existing `origin/v2-day1` (session A had pushed it); `git pull --rebase --autostash`
runs, `--autostash` because the launchd refresh keeps tracked `data/` artifacts dirty in the shared tree.
Branch pushed at 805dd8d and again after this brief.

## 2. The walk, full registered draws — PASS

`python3 src/walk.py` (no `--fast`), 28 minutes, run `walk_20260902T210135Z`, 313 sealed reads.

- G target: IES-90 level + DEAL, `data_state.ies90_registration` = "OUTCOME_MAPPING.md Amendment 1 + 1.1 + 2".
- Menu: 13 items (12 weightings + M13 recalibrated, Amendment C).
- Seal check 313/313; six earlier runs archived under `runs/<run_id>/` and each re-verified (Amendment D).
- **Filtration audit (Amendment F.1): 0 violations over 15,784 checks** — 4,438 analog dates, 2,515 branch
  windows, 4,115 price windows, 4,236 market values (293 of them from session A's state bridge, whose
  `obs_date` and `vintage` the audit checks), 187 persistence windows. Leakage: filtration is binding.
- **Determinism (Amendment I): two separate full runs, hours apart, produced the identical content digest**
  `2a90ff4a88f30f6f50433a2b5268dc1feaf9bc219b5ef2ec575ef15dce57f116`.

### Daily tier, 253 scored reads (150 with an IES-90 label)

| comparison | skill | 95% CI | DM/HLN p |
|---|---|---|---|
| G Brier vs climatology | −0.097 | −0.180..−0.018 | 0.022 |
| G Brier vs random analogs | −0.021 | −0.098..+0.052 | 0.583 |
| G Brier vs frozen | +0.007 | +0.000..+0.014 | 0.029 |
| G Brier vs persistence | −0.600 | −1.228..−0.230 | <0.001 |
| G RPS vs climatology | −0.013 | −0.100..+0.078 | 0.770 |
| G RPS vs random analogs | +0.062 | −0.022..+0.148 | 0.139 |
| P CRPS vs climatology | −0.071 | −0.136..−0.017 | 0.016 |
| P CRPS vs persistence | +0.128 | +0.070..+0.185 | <0.001 |
| P CRPS vs random analogs | −0.005 | −0.060..+0.049 | 0.852 |
| M13 recalibrated vs climatology | −0.699 | −0.940..−0.457 | <0.001 |

G SPA p 0.645 (best M03_market_only); P SPA p 0.961; RPS SPA p 0.979 (Amendment F.3). Block permutation
(Amendment F.2, the §7 condition): observed skill −0.066, **p 0.124**; i.i.d. p 0.092. Placebo, size-matched:
−0.047 (CI −0.083..−0.008), **null does not hold**. Spec curve: 0 % of specifications positive, median
−0.075. FDR family 34 comparisons, 31 survive — nearly all of them the engine or an item being *worse*.
Verdict: `engine:G` SUGGESTIVE / null, `engine:P` SUGGESTIVE / null, audit flag false.

**What changed and why it matters.** Amendment H (situation fields taken from `situation_state`'s
`knowable_at` rows, else unknown) is the largest single move in the project's published numbers: G skill vs
climatology went from −0.005 (p 0.884) to −0.097 (p 0.022), P from −0.030 to −0.071 (p 0.016), the spec
curve from 22 % positive to none, and the permutation's observed skill from +0.013 (p 0.002) to −0.066
(p 0.124). The engine's apparent parity with climatology depended on situation fields coded after the fact;
262 of 313 events have no situation field knowable at t, so retrieval runs on the market block alone and the
engine is significantly worse than climatology. Published as computed.

## 3. D4 — CLOSED

`tiers.daily.G.engine_vs` carries four references (climatology, frozen, random_analogs, persistence);
`G.spa_vs_persistence` and `n_persistence_fallback` (2 of 153 geopolitical reads) are published. P had four.

## 4. Power (Brief 2 B-6) — published

By simulation from the sealed score differentials, resampled with the tier's measured stationary block
(mean block 2.32, HAC lag 1), DM/HLN at α 0.05:

| target | n measured | minimum detectable skill at 80 % power | n needed for +0.05 |
|---|---|---|---|
| G (Brier) | 150 | **0.127** | **1,200** |
| P (CRPS) | 253 | **0.085** | **1,200** |

`figures/power.png`. At the corpus's present size the walk cannot detect a +0.05 improvement on either
target; a null here is "not detectable at this n", which is what §9 requires it to say.

## 5. The whole suite — PASS

`python3 -m pytest -q`: **366 passed, 15 skipped, 0 failed** (12 min) at e8b3517; re-run against the final
code after the audit fix. Skips are session A's licence- or key-gated loaders, each with its reason.

New test files this brief: `test_walk_baselines.py` (Amendment B), `test_walk_recalibration.py` (C),
`test_walk_archive.py` (D), `test_walk_filtration_audit.py` (F.1, G, H — including both of session D's
deliberate leaks, re-applied and caught), `test_walk_determinism.py` (I), `test_candidates_pre1987.py` (B-3).

## 6. The desk, end to end — PASS (checked at run 182828Z; endpoints unchanged since)

All seven endpoints 200 with every number traced: `/app`, `/api/walk/summary`, `/api/walk/list`,
`/api/walk/read`, `/api/engine_read`, `/api/story`, `/api/ledger`. Session A has since fixed the three
PARTIAL items this file previously carried (Brief A-1..A-3: the summary endpoint passes the file through
whole, the story trust block reads the current run, the retired branch rates carry the retired label).

## 7. Session D's red-team findings — answered

`data/handoffs/B_response_to_D.md`: D2 findings 1, 2, 3, 4 fixed by dated amendments (F.1, candidates
Amendment 1, G, H) with the code and tests behind them; D2's Big Moves threshold answered with a computation
(2 of 41 episodes would not clear their own point-in-time threshold) and registered as a v3 item; D3
findings 1, 3, 5 fixed (F.4, F.3, F.5), finding 2 fixed by the block permutation, finding 4 closed by the
193022Z run. **D was right that the leakage test was structurally blind**; the audit that replaces it caught
a genuine cross-session interaction on its first run.

## 8. Registered files and the events table

`OUTCOME_MAPPING.md`, `PATH.md`, `SESSION_CHARTER.md`, `events`: untouched by session B.
`WALK_FORWARD_PROTOCOL.md` carries dated appended Amendments B, C, D (Brief 1) and E, F, G, H, I (Brief 2),
each committed before its code. `data/candidates/REGISTRATION.md` carries Amendment 1.

## Summary

PASS: the walk (clean filtration audit, deterministic across two runs), D4 closed, power published, suite
366/0/15, seven endpoints traced, every red-team finding answered. FAIL: none. The engine, made
point-in-time, is worse than climatology on both targets, and the corpus is roughly 8× too small to detect
the effect size anyone would care about.
