# B_run_delta_spine — the walk on the repaired corpus: `walk_20260903T003422Z` vs `walk_20260902T210135Z`

The run the paper's final version reports. Full registered draws (`python3 src/walk.py`, no `--fast`;
n_boot 2000, n_spa_boot 1000, n_perm 1000, random_draws 25, placebo_reps 5), 29 minutes, 313 sealed reads,
filtration audit clean (0 violations over 15,784 checks), leakage binding.

## The headline: nothing moved. Not one number.

| | 210135Z | 003422Z |
|---|---|---|
| content digest | `2a90ff4a88f30f6f50433a2b5268dc1feaf9bc219b5ef2ec575ef15dce57f116` | **identical** |

A whole-summary diff, ignoring only run identity and wall-clock stamps, returns **equal on every key**
except one (below). That covers every skill number, every confidence interval, every DM/HLN and SPA
p-value, the permutation, the placebo, the spec curve, the power block, the reliability decompositions and
the FDR family. This is the third separate full run to produce that digest (Amendment I).

## Why it did not move, established rather than assumed

Session E applied 66 field changes across four patch batches (`pre1990_a` 29, `pre1990_b` 13, `1990s_a` 7,
`1990s_b` 17). Distribution by column: `source_url` 24, `description` 17, `surprise` 12, `severity` 9,
`confidence` 8, `date_precision` 4, `event_date` 2, `type` 2.

Two of those columns can move a walk — `event_date` (the filtration keys on it; IES-90 windows are
`(d, d+90]`) and `type` (it decides the analog pool and whether an event is G-scored). So rather than trust
the patch files, I diffed the **live corpus against the sealed reads of 210135Z**:

- events in the corpus: 313; sealed reads: 313; **none added, none removed**
- events whose `event_date` or `type` differs from the sealed read: **0**
- IES-90 labels that differ from the sealed outcome: **0**

The `event_date` and `type` entries in the patch files are proposals that were not applied to those two
columns, consistent with session E's own correction (commit b4a1f6d: "the Iran-Iraq ceasefire date did NOT
move; my previous commit message was wrong") and its handoff ("no date moved at all... only the
`date_precision` label changed").

The other six columns are provenance and coding metadata that the engine never reads. Executed check:
`severity`, `surprise`, `confidence`, `description`, `source_url` and `date_precision` each appear **zero
times** in `src/engine/*.py` and `src/walk.py`. The state vector takes only the seven `SR_MAP` fields (now
via `situation_state`'s knowable-at rows, Amendment H) plus the market series; the label comes from
`event_outcomes`; persistence comes from `event_entities` through `ies90.score_event`.

So the repair improved the corpus's sourcing without touching anything the forecast depends on. That is the
honest reading, and the digest is the proof rather than the argument.

## The four numbers the brief asked for, on the repaired corpus

| | value | vs 210135Z |
|---|---|---|
| G Brier skill vs climatology | −0.0966 (CI −0.180..−0.018, DM p 0.022, n 150) | unchanged |
| G Brier vs random analogs / frozen / persistence | −0.0212 (p 0.583) / +0.0074 (p 0.029) / −0.6000 (p <0.001) | unchanged |
| G RPS vs climatology / random analogs / persistence | −0.0127 (p 0.770) / +0.0616 (p 0.139) / −0.7906 (p <0.001) | unchanged |
| P CRPS vs climatology / persistence / random analogs / frozen | −0.0705 (p 0.016) / +0.1285 (p <0.001) / −0.0051 (p 0.852) / +0.0070 (p <0.001) | unchanged |
| M13 recalibrated vs climatology | −0.6995 (p <0.001) | unchanged |
| DEAL binary Brier vs climatology | −0.1781 (n 66, base rate 0.0606) | unchanged |
| **permutation (G)** | observed skill −0.0664; **block p 0.1239** (the §7 condition), i.i.d. p 0.0919 | unchanged |
| **placebo (P), size-matched** | −0.0473 (CI −0.0828..−0.0082), **`null_holds: false`**; vs climatology −0.1058; size-corrected +0.0172 | unchanged |
| **spec curve** (54 specifications) | min −0.1499, median −0.0754, max −0.0411, **share positive 0.000** | unchanged |
| SPA | G 0.645, P 0.961, RPS 0.979; best model M03_market_only on both | unchanged |
| power | MDS at 80 %: G 0.1268 (n 150), P 0.0850 (n 253); n ≈ 1,200 for +0.05 | unchanged |
| verdict | `engine:G` SUGGESTIVE / null; `engine:P` SUGGESTIVE / null | unchanged |

## 262 of 313 — has it moved? **No.**

`data_state.situation_knowable` is byte-identical: **51** events carry at least one situation field
knowable at t, **262** carry none, 726 coded values are blanked, 60 survive. Session E's patches added no
`situation_state` knowable-at rows, so Amendment H blanks exactly what it blanked before. The number moves
only when fields gain contemporaneous sources — session A's `knowable_at` work, or Joe's coding — not when
an event's citation or severity is repaired.

Corpus totals also unchanged: 313 events, 184 with an IES-90 level (Amendment 1 + 1.1 + 2 rows, generated
2026-09-02T18:25:31Z), 3 `no_independent_outcome`, 95 with a DEAL flag.

## The one thing that did change: Joe's label audit has begun

`verdict.audit_record` is the only block that differs, and it is not a forecast number.
`data/audits/outcome_audit.json` now exists and records the §1/§7 label audit in progress:

| field | value |
|---|---|
| auditor | joe |
| sheet | `data/audits/ies90_audit_30.csv` |
| started / dated | 2026-09-02T23:39:35Z / 2026-09-03T00:11:17Z |
| rows done | **1 of 30** |
| kappa | null (not computable at n = 1) |
| passed | **false** |
| agreement so far | one row, engine level 3 and Joe level 3; DEAL agrees 1 of 1 |

So `verdict.audit_passed` stays **false** and every §7 status stays SUGGESTIVE, which is correct: the gate
is not open until 30 rows are coded and κ ≥ 0.6. This is the first time the audit record has appeared in a
published summary at all, and the walk picked it up automatically.

## Suite, and two transient failures worth naming

`python3 -m pytest -q` twice after publishing: **435 passed, 15 skipped, 1 xfailed** with one failure each
time, in a different test of `tests/test_hostility.py` each time, and **all 10 of that file pass in
isolation both times**. Cause, not guessed: the tree is shared by four sessions. The first run overlapped my
`git pull --rebase --autostash`, which briefly restores tracked `data/` files mid-test; the second
overlapped another session re-running `src/state/ies90.py`, which deletes and re-inserts every `ies90` row
(that session was committing a fix for exactly this at 21:21, "rule_fired tie order is not stable across
runs"). Neither failure touches session B's code or the published artefacts. The single xfail is B-12's
monthly-tier smoke.

**The check that matters, run because of it:** the IES-90 rows were regenerated by that other session at
2026-09-03T01:17:06Z, *after* this walk sealed its reads at 00:34Z. Comparing the database now against the
published run's sealed outcomes: **0 of 184 labels differ**, and the level counts are identical
(0: 76, 1: 6, 2: 48, 3: 54). The rebuild reproduced the labels exactly, so the published summary describes
labels that still exist. Had it not, this run would have been superseded rather than reported.

## Diagnostic (Amendment K): the G block on the 123 G-scorable reads only

Registered before computing (protocol Amendment K, commit 79c7490). Session F's `hostility` field
(OUTCOME_MAPPING Amendment 3 §A3.3) was coded for all 187 events of the four geopolitical classes before any
count under it; `non_hostile` and `ambiguous` make the G target **undefined**, so removing them repairs the
estimand rather than searching subsets. Computed from the sealed files — the published run is not re-scored
(§A3.5). Engine, frozen and persistence forecasts are taken as sealed; **climatology is re-estimated** on
each read's own point-in-time pool minus its non-scorable members (mean pool 27.7 → 23.6), and random
analogs are re-drawn from that reduced pool at the same k and per-event seed.

Set: 150 published → **123 retained** (121 `hostile`, 2 `hostile_unattributed`), 27 dropped (17
`non_hostile`, 10 `ambiguous`). Level-0 share **42.0 % → 32.5 %**.

| comparison | published (n 150) | diagnostic (n 123) | direction |
|---|---|---|---|
| Brier vs climatology | −0.0966 (CI −0.180..−0.018, p 0.022) | **−0.1316 (CI −0.234..−0.028, p 0.012)** | **widens** |
| Brier vs random analogs | −0.0212 (p 0.583) | −0.0574 (CI −0.151..+0.034, p 0.222) | widens |
| Brier vs frozen | +0.0074 (p 0.029) | +0.0080 (CI +0.001..+0.016, p 0.033) | holds |
| Brier vs persistence | −0.6000 (p <0.001) | −0.4871 (CI −1.101..−0.117, p 0.004) | narrows, still decisive |
| RPS vs climatology | −0.0127 (p 0.770) | −0.0664 (CI −0.186..+0.044, p 0.251) | widens, still not significant |
| RPS vs persistence | −0.7906 (p <0.001) | −0.5840 (CI −1.340..−0.169, p 0.002) | narrows, still decisive |

**The answer to the question the diagnostic was set: the engine's negative skill widens.** Removing the
reads whose target is undefined does not rescue it. Both sides get harder — climatology's mean Brier rises
0.7011 → 0.7078 and the engine's 0.7687 → 0.8010 — but the engine loses ground faster, so the gap grows by
about three and a half points and stays significant. Read plainly: the engine was doing relatively *better*
on the reads that should never have been scored, which are disproportionately level-0 "none" and easy to
call; on the events where the escalation question is actually well posed it does worse, not better. The one
number that improves is the gap to persistence, and persistence still beats the engine by a wide margin on
both scores.

**The limit.** n falls 150 → 123, so every interval widens; `min_tier_n` 30 is still met but the measured
minimum detectable skill at n = 150 was already 0.127. This is a diagnostic on a sealed run, not a new run:
it gates nothing, changes no published number, and leaves `engine:G` SUGGESTIVE / null under §7. Published
in `summary.json` at `tiers.daily.G.diagnostic_hostile` with `registered: false`.

**One number in the instruction, corrected.** The brief said the level-0 share moves 42.0 % → 36.8 %. On the
123-read set it is **32.5 %**; 36.8 % is the 133-read set that drops the 17 `non_hostile` but keeps the 10
`ambiguous` (session F's table gives both). The diagnostic uses the 123 set as instructed, so 32.5 % is the
figure that belongs beside it.

## For the paper

The run to cite is **`walk_20260903T003422Z`** (`data/walk_forward/summary.json`, committed). Its numbers
are the same as 210135Z's, and the reason is worth one sentence in the data section: the corpus repair
changed provenance, not evidence, and the walk is demonstrably invariant to it — same content digest,
computed independently, three runs apart. The §7 label audit is 1 of 30 rows in, so no result is
VALIDATED and none is claimed to be.

The prior run's sealed records are archived at `data/walk_forward/runs/walk_20260902T210135Z/` and
re-verify (Amendment D).
