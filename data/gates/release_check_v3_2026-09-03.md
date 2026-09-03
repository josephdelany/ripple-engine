# Release check — what a `v3.0` tag would point at, 2026-09-03

Prepared by session B. **No tag is created here.** Joe cuts `v3.0` once the paper's final version lands
(PATH.md §3 D7). This file records what the tag would be pointing at on 2026-09-03, and what each item that
is not yet done is waiting on.

## The run

**`walk_20260903T003422Z`** — `data/walk_forward/summary.json`, committed at 1a587e5.

| | |
|---|---|
| draws | full registered (n_boot 2000, n_spa_boot 1000, n_perm 1000, random_draws 25, placebo_reps 5) |
| reads | 313 sealed; daily tier 299 (253 scored past burn-in, 150 with an IES-90 label), monthly 14 (0 scored) |
| filtration audit | **clean** — 0 violations over 15,784 checks (protocol Amendment F.1) |
| leakage | filtration is binding; the recalibration rule asserted too |
| determinism | content digest `2a90ff4a88f30f6f50433a2b5268dc1feaf9bc219b5ef2ec575ef15dce57f116`, reproduced by **three** separate full runs |
| G target | IES-90 level + DEAL, `OUTCOME_MAPPING.md` Amendment 1 + 1.1 + 2 |
| verdict | `engine:G` SUGGESTIVE / null; `engine:P` SUGGESTIVE / null; audit flag false |

Headline numbers: G Brier skill vs climatology −0.0966 (CI −0.180..−0.018, DM p 0.022); P CRPS −0.0705
(CI −0.136..−0.017, p 0.016); vs persistence G −0.6000 and P +0.1285; block permutation p 0.124; size-matched
placebo −0.0473, does not hold; specification curve 0 of 54 positive; minimum detectable skill at 80 % power
0.127 (G, n 150) and 0.085 (P, n 253), with n ≈ 1,200 needed for +0.05.

Two things sit beside the run and gate nothing: the Ferro size-corrected diagnostics (Amendment A.5) and the
hostility diagnostic (Amendment K) at `tiers.daily.G.diagnostic_hostile`, which shows the engine's negative
skill **widening** to −0.1316 on the 123 reads whose G target is defined.

## PATH.md §3 — the definition of done

| item | status | evidence | what it is waiting on |
|---|---|---|---|
| **D1** `pytest -q` green incl. every named test | **PASS** | `447 passed, 15 skipped, 1 xfailed, 0 failed` (6 m 52 s, exit 0) | Nothing. `acceptance_v2 --dod` prints FAIL because `_d1()` tests `"failed" not in summary` and the line contains `1 xfailed`; `returncode` is 0. One-line fix is session A's, reported in `data/handoffs/B_to_A_2026-09-02.md` §8. |
| **D2** `status.py` ≥ 12 loaders + coverage by block | PASS | `data/state/status.json` | Nothing. 27 loaders behind 49 loaded fields of 70 registered; coverage by block × decade present. |
| **D3** κ published; rule applied; audit file | PASS | `data/state/outcomes_kappa.json` | Nothing. The κ < 0.6 replacement rule is superseded by OUTCOME_MAPPING Amendment 1 (`sr_outcome_90` retired, IES-90 adopted). |
| **D3a** label audit recorded by Joe | **PARTIAL** | `data/audits/outcome_audit.json` | **Joe.** 1 of 30 rows coded; κ not computable at n = 1; `passed: false`. The §7 gate opens at 30 rows with κ ≥ 0.6. Sheet: `data/audits/ies90_audit_30.csv`; recorder: `src/audit_ies90.py`. |
| **D4** walk summary complete | PASS | `data/walk_forward/summary.json` | Nothing. Both tiers, four G baselines (climatology, frozen, random_analogs, persistence — closed by Brief 3 B-1), DM and SPA p-values, placebo, permutation, regime blocks, specification curve, power, leakage asserted. |
| **D5** 9/11, 1990, 2026 demos from sealed inputs | PASS | `data/walk_forward/reads.jsonl` | Nothing. All three sealed in this run; `/api/walk/read`; `tests/test_demo_911.py`. |
| **D6** VALIDATED only via protocol §7 | PASS | `data/walk_forward/summary.json` | Nothing. No §7 verdict is VALIDATED; no v2 surface prints VALIDATED without a §7 reference. Joe's Ruling 1 removed the last five `validated` rows from `propagation_edges` (2026-09-02). |
| **D6a** reader accuracy on the gold set | PASS | `data/reader_eval/score.json` | Nothing blocking. Class accuracy 0.84 against a 0.80 threshold, entity F1 0.935 — but the gold set is coded by session A and **unaudited by Joe**, which is worth one line in the paper. |
| **D7** tag v3.0; paper; one week in the Ledger | **PARTIAL** | git tags / `data/ledger/claims.jsonl` | **Three things.** (1) the tag — Joe's, and the point of this file; (2) the paper — `docs/PAPER_DRAFT.md` exists and its final version is the trigger; (3) **six more days of Ledger use** — 1 distinct day recorded, 7 required. |

**6 of 9 PASS, 2 PARTIAL, 1 reported FAIL that is a green suite mis-read.**

### D1, run clean and shown to be clean

`python3 -m pytest -q` at 2026-09-02 22:04:07–22:11:01, HEAD 9f2d649: **447 passed, 15 skipped, 1 xfailed,
0 failed**, exit code 0. The one xfail is `tests/test_monthly_tier.py::test_b12_real_monthly_tier_smoke`,
which expects-fail today because the monthly tier holds 14 events and passes on its own when Joe admits a
batch. The 15 skips are session A's licence- or key-gated loaders, each with its instruction in the skip
reason.

Two earlier full runs each hit a single failure in a different test, and every one of those tests passed in
isolation — a shared tree with four sessions committing. So this run was stamped rather than asserted:
sessions A and F had not committed for nine minutes when it started, and across the run
`data/audits/outcome_audit.json` (which Joe is writing interactively, and which
`tests/test_audit_ies90.py` reads) and `data/oil.db` both kept their exact mtimes — no concurrent write
touched either. One unrelated documentation commit landed at 22:10:34, in the last twenty seconds. **This is
the D1 figure to carry.**

## Open gates, and who each is waiting on

**Joe**
- The IES-90 label audit, 1 of 30 rows. Everything §7 stays SUGGESTIVE until it passes at κ ≥ 0.6.
- Admitting pre-1987 events. 181 dossiers built, 97 admissible, **0 admitted**; nothing enters `events`
  without him. This is the only route to a decisive answer: power says n ≈ 1,200 scored reads to detect
  +0.05 skill, against 150 today. The blind admission sheet is `data/candidates/pre1987_candidates.csv`
  (outcomes held separately, per candidates REGISTRATION.md Amendment 1).
- Ruling 2 (the JODI licence) and Ruling 3, in `data/gates/ripple_2026-09-02.md` — still unruled.
- The two open questions in `data/gates/step8_2026-09-02.md`: ratifying protocol Amendment A, and whether
  §3 adopts the size-corrected scores (Amendment E already registers that prospectively for v3).
- Six more days of Ledger use for D7.

**Session A**
- The `_d1()` substring fix above.
- 13 `ambiguous` hostility events await adjudication (session F's handoff) — they can only move events into
  `hostile`, raising n, never out.

**Session B (me) — nothing blocking, three things registered and waiting for their trigger**
- Protocol Amendment E / J.1: the Ferro size-corrected scores become the primary gate **from the first v3
  run**, i.e. the first run after the pre-1987 corpus is admitted. Every v2 run keeps §3.
- Amendment J.2: the read-time materiality threshold becomes point-in-time at v3 (measured: 2 of 41
  episodes fail their own point-in-time threshold).
- Amendment J.3: the change-in-level estimand (ΔIES on {−3..+3}), registered with its scores, its four
  baselines including no-change, and its gate. Nothing computed.
- The monthly tier is ready the moment a batch is admitted: `tests/test_monthly_tier.py` proves the walk
  scores a filled tier at n = 40 today, and the real-corpus smoke flips from xfail to pass on its own.
  A publication run is then one command, `python3 src/walk.py`.

## What the tag would honestly say

That the engine is **null on both targets and worse than climatology on each**, that the result is
reproducible to a byte across three runs, that it survives a filtration audit that catches deliberately
planted leaks, that removing the reads whose target is undefined makes it worse rather than better, and that
the corpus is roughly eight times too small to detect an effect anyone would care about. Not one number on
any surface says VALIDATED, and the §7 gate that could say it is 1 of 30 rows into its audit.
