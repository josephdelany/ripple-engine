> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Adversarial review findings, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# D-6 Replication — ripple-engine, branch v2-day1

Repo under review: `/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine`.
Clone commit (both clones): **b7c8ec1** (2026-09-02 14:58:39 -0400, "Brief B-1 (code): G-persistence,
the fourth G baseline (Amendment B)"). The real repo is a live, multi-session tree: by the time this
report was written its HEAD had moved to `d6a3bde` (two further sessions' commits, Amendments C and
D among them) and another session's `python3 src/walk.py` was running in it — none of that is this
review's work; the clones and everything below are pinned to b7c8ec1 as it stood at clone time.

Deliverables in the real repo (uncommitted, per the brief's hard rules — nothing else touched, no
`git add`/`commit`/`stash`): `Makefile` (new; none existed), `tests/test_reproduce.py` (new),
`requirements.txt` (pinned `==`, comments kept, `pytest` added).

Two clean clones were built and run to isolate two questions at once:
- **`ripple-clone`** (run `walk_20260902T191640Z`) — `make reproduce REPRO_DB=<real repo>/data/oil.db
  REPRO_FORCE=1`. First attempt at the `REPRO_DB` sibling-directory copy had a path bug (see §6) so
  `data/state/raw/` and `data/cache/` did **not** get copied in; this run is the honest "REPRO_DB
  alone" case.
- **`ripple-clone-b`** (run `walk_20260902T191744Z`) — same command, after the one-line fix, so
  `data/state/raw/` (42 MB) and `data/cache/` (38 MB) **were** copied in.
Running both, from the identical committed code and the identical copied `oil.db`, turns the bug into
a useful natural experiment: it isolates exactly what the G-persistence baseline needs at read time,
executed, not asserted (§4).

---

## 1. The dependency chain

**`data/oil.db` is not committed.** `.gitignore:4` — `data/*.db` — confirmed by
`git ls-files data | grep oil.db` (empty) and `git check-ignore -v data/oil.db` →
`.gitignore:4:data/*.db  data/oil.db`. It is 193–202 MB on disk in the working tree only.

**`repro.sh`** (22 steps, "rebuild `oil.db` FROM ZERO... against the committed inputs") needs, in
order: FRED (`fetch_prices.py`, `fetch_series.py`, `fetch_value_chain.py` — keyless but networked),
**EIA Open Data v2** (`fetch_eia.py` — networked *and* needs `EIA_API_KEY`), **CFTC** COT
(`fetch_cot.py` — networked), and the **GPR** `.xls` (`fetch_gpr.py` — networked file). None of that
is reachable from a bare `git clone`.

**`src/state/ies90.py`** — called live, at every read, by `src/engine/persistence.py`'s G-persistence
baseline (`load_sources()` → `load_war()`, `load_midi()`, `load_ged()`) — additionally needs
**correlatesofwar.org** (networked; `WAR_URLS` in `ies90.py:39`) and two gitignored directories that
are not part of `oil.db`: `data/state/raw/` (COW MID, ICB, GPR, EIA, etc. — 42 MB) and `data/cache/`
(`ucdp_ged_26.1.json`, UCDP GED — 38 MB). `engine/read.py:_persistence()` wraps the whole call in
`try/except Exception` — absent, every read falls back to climatology, **honestly counted**
(`n_persistence_fallback`), never silently wrong. This is executed, not inferred: see §4.

Per `data/gates/release_check_2026-09-02.md` §3, six more `src/state/*.py` loaders are keyed or
licence-gated (not on the walk's own path, but part of the same corpus): `ei_review` (EI xlsx, 403 to
scripts), `eia_intl` (`EIA_API_KEY`), `gsdb` (GSDB R5 by request), `nyt` (`NYT_API_KEY`), `vdem`
(V-Dem v16, form-served), `dots` (IMF DOTS refuses scripted pulls).

**What IS committed and offline-only:** `data/events.csv` (`src/load_events.py`), `data/state/*.csv`
— `situation_log.csv`, `reads.csv`, `forecasts.csv` (`src/import_state.py`, idempotent
`INSERT OR IGNORE`), `data/walk_forward/menu.json`, `data/seed/wtisplc_monthly.txt`,
`data/seed_library/*`. `src/init_db.py` is pure schema, no network. That is enough to refresh the
`events` table on top of an *already-built* `oil.db` — it is **not** enough to build `oil.db` itself,
and not enough to source the G-persistence baseline's raw inputs.

**Verdict:** the chain from a clean clone alone dead-ends at `oil.db`. The Makefile's `REPRO_DB=`
fallback (copy an already-built `oil.db`, plus its sibling `state/raw`/`cache`/`state/local` if
present) is the documented way to still time and exercise the walk stage — used for both runs below.

---

## 2. Makefile (`reproduce` target)

Single target, one shell (`set -euo pipefail`, backslash-continued so `$$T0`-style timers persist
across the whole recipe):

0. `python3 src/init_db.py` — schema, offline, idempotent.
1. **guard**: refuses if `data/walk_forward/reads.jsonl` is non-empty, unless `REPRO_FORCE=1`.
2. **db**: refuses with a precise message if `REPRO_DB` is unset; else `cp $(REPRO_DB) data/oil.db`,
   then copies sibling `state/raw`, `cache`, `state/local` from `REPRO_DB`'s own `data/` directory if
   present.
3. **events**: `python3 src/load_events.py && python3 src/import_state.py` (offline, committed CSVs).
4. **walk**: `python3 src/walk.py` — **no `--fast`**, the registered full draws.

Prints `date +%s`-based wall time per stage and a total. No dependency beyond `python3`/`bash`/`cp`.

---

## 3. Wall time

Both runs were launched **concurrently** on the same machine (deliberate, to get the raw/cache-copy
comparison without waiting twice) — CPU-contended, so absolute times overstate a solo run; they are
still valid for the *relative* / structural comparison this report needs, and are reported as
measured, not adjusted.

| stage | A (`ripple-clone`, REPRO_DB only) | B (`ripple-clone-b`, REPRO_DB + raw/cache) |
|---|---|---|
| 0 — `init_db.py` | 0s | 1s |
| 1 — `oil.db` copy (+raw/cache for B) | 1s (193M) | 1s (193M + 80M raw/cache) |
| 2 — `load_events.py` + `import_state.py` | 0s | 0s |
| 3 — the walk (`src/walk.py`) | see below | see below |
| **total** | **~1037s (17m17s)** | **~1003s (16m43s)** |

Stage 3 has no clean Makefile-level number: the `make` process itself received `Terminated: 15` partway
through (the tool session that launched it in the background ended its call before the child finished;
`python3 src/walk.py` — already forked, inheriting the log's file descriptor — kept running to
completion regardless, and both `summary.json` files exist, are well-formed, and their file `mtime`
matches the internal timing below exactly, so the run is complete and valid). `src/walk.py` prints its
own internal, `time.time()`-relative milestones, which are what the table above is built from:

| internal milestone | A | B |
|---|---|---|
| reads sealed (313) | 302s | 290s |
| inference phase done (BH-FDR, permutation, regime blocks, spec curve, placebo) | 636s (+334s) | 625s (+335s) |
| `summary.json` written (after the leakage re-run + figures) | **1036s** | **1001s** |

Cross-check against the file's own timestamps: A's `run_id` embeds `19:16:40Z`; `summary.json` `mtime`
is `2026-09-02T19:33:56Z` → 1036s elapsed, exact match. B's `run_id` is `19:17:44Z`, `mtime`
`19:34:24Z` → 1000s, matching the internal `1001s` to the second.

**`generated_at` is not the file's completion time.** `summary["generated_at"]` is stamped in
`run()` right after `run_reads()` returns (before `summarize_tier`, `permutation_test`,
`regime_blocks`, `spec_curve`, `placebo`, the second (leakage) walk, and `figures` all still run) — so
`generated_at − run_id` (A: 303.3s, B: 289.7s) measures only the **reads** sub-phase, not the walk
stage as a whole (1036s / 1001s). Anyone reading `run_id`→`generated_at` as "how long the walk took"
will understate it by roughly 3×. Worth a docstring note in `walk.py`, not fixed here (scope).

This run (Amendment B, G-persistence, present) is materially heavier than the release check's solo
**4 m 35 s** for the pre-Amendment-B `walk.py` (`data/gates/release_check_2026-09-02.md` §2) — expected,
given concurrency plus the added SPA-vs-persistence computation and a second full leakage walk; not
a discrepancy to chase.

---

## 4. Comparison: committed run 182828Z vs the reproductions

**Code-version note, executed:** `git log --format='%h %ci' -- data/walk_forward/summary.json` → the
committed file was produced by `d3df9af` (14:38:19). `git log --format='%h %ci' -- src/walk.py` →
HEAD's committed `src/walk.py` at clone time was `b7c8ec1` (14:58:39), **20 minutes later**, adding
Amendment B (the G-persistence baseline) — a change data-derived from the code, confirmed by
`git diff d3df9af b7c8ec1 -- src/walk.py`. **The reproduction target and the code that runs in a clean
clone are not the same code.** Every difference below traces to that one, named, dated change — this
was checked, not assumed.

### 4a. `walk.verify_seal` / how the seal hash is computed

```python
def seal(record):
    record["sealed_at"] = _now()
    record["hash"] = hashlib.sha256(_canon({k: v for k, v in record.items() if k != "hash"}).encode()).hexdigest()
    return record
```
The hash is over **the whole record except `hash` itself** — which includes `run_id` and `sealed_at`
(wall clock). **Run identity and time are not excluded.** So two separate runs, however identical
their inputs, can never produce an equal raw `hash` for "the same" read: confirmed by execution,
0/313 raw-hash matches in every pairing tried (A vs committed, B vs committed, A vs B — see §4c). This
contradicts the implicit premise "same read inputs should hash identically if the seal excludes
run_id/time" — it doesn't exclude them, so they don't.

### 4b. JSON diff, `registered` / `data_state` / `tiers` / `fdr` / `permutation` / `placebo` /
`spec_curve` / `verdict` — tolerance 0, then 1e-9 (executed: `deepdiff.py`, recursive, dict-keyed,
list-positional, numeric leaves compared with the stated tolerance)

**A (`191640Z`) vs committed (`182828Z`):** 163 differing leaves at **both** tolerance 0 and 1e-9 (no
diff resolved by the tolerance bump ⇒ every difference is structural/exact, none is float noise).
Broken down by top-level key:

| key | diffs | cause |
|---|---|---|
| `registered` | 1 | `g_baselines` key added (now lists `persistence`) — absent in the committed file |
| `data_state` | 0 | **identical** — same corpus, same IES-90 labels (187 geo events, 184 labelled, level counts 0:76/1:6/2:48/3:54, 95 with deal — byte for byte) |
| `fdr` | 92 | **one** new p-value (`daily:G:engine_vs_persistence`) inserted into the family at index 3; every later index shifts by one → the diff tool (positional) reports each shift as a "difference." The true content diff is 1 insertion, not 92. |
| `permutation` | 0 | **identical** (p 0.008, observed skill 0.000517, exact) |
| `placebo` | 0 | **identical** (`null_holds: true`, size-matched skill −0.0237, exact) |
| `spec_curve` | 0 | **identical** (162 specs, same distribution, `share_positive 0.1667`) |
| `verdict` | 0 | **identical** (`SUGGESTIVE / null` both targets — verdict logic only reads the `climatology` ref, untouched by Amendment B) |
| `tiers` | 70 | all six new keys Amendment B adds under `tiers.{monthly,daily}.G`: `engine_vs.persistence`, `n_persistence_fallback`, `n_persistence_known`, `rps.engine_vs.persistence`, `spa.benchmark` (new field on the existing SPA block), `spa_vs_persistence` (new block) — plus the `family_p.labels`/`family_p.p` index-shift cascade from the same one new comparison, same artifact as `fdr`. |

**Read as:** every quantity the *committed* code (`d3df9af`) computed reproduces **exactly** —
`data_state`, `permutation`, `placebo`, `spec_curve`, `verdict`, and (checked directly, not shown
above since it's inside `tiers`) the pre-existing `engine_vs.{climatology,frozen,random_analogs}`
blocks all match to the last decimal. The only differences are **additive**: fields Amendment B
introduced that the committed file never had, plus one cosmetic list-index cascade from inserting one
new named comparison into an ordered array. Zero evidence of nondeterminism in anything the committed
run itself measured.

**B (`191744Z`) vs committed:** same shape, same 163/163 diffs, same explanation (B differs from A
only in whether the persistence baseline had real data — see §4d — which doesn't touch anything the
committed file computed either).

### 4c. Read-by-read hash comparison, `reads.jsonl` (executed: `read_hash_compare.py`, matched by
`(tier, event_id)`, 313 keys in every file)

| comparison | own-record `verify_seal` | raw `hash` equal | content hash equal (`run_id`/`sealed_at`/`hash` stripped) |
|---|---|---|---|
| A vs committed 182828Z | 0/313 bad, 0/313 bad | **0/313** | **0/313** |
| B vs committed 182828Z | 0/313 bad, 0/313 bad | **0/313** | **0/313** |
| A vs B | 0/313 bad, 0/313 bad | **0/313** | **126/313** |

Every sealed record re-verifies against its own `hash` (the seal mechanism itself is sound). Raw
`hash` never matches across runs, anywhere — expected, per §4a. Content hash (the fairer determinism
test) is **0/313 for both reproductions against the committed run**, entirely because Amendment B
changed the `baselines.persistence` sub-object shape in **every** sealed read (committed:
`{"P": [0.0]}`; reproduced: the full `pers_blk` with `level_pre`/`covering_pre`/`fallback`/`G`) — a
schema change from code drift, not a nondeterminism finding; confirmed by diffing one example record
(`daily/abqaiq_attack_2019`): the only differing top-level fields are `baselines`, `hash`, `run_id`,
`sealed_at`.

**A vs B is the clean determinism test** (identical code, identical `oil.db`, identical seeds — the
*only* input difference is whether `data/state/raw`/`data/cache` were present): **126/313 reads have
an identical content hash**, and those 126 are *exactly* the non-geopolitical event types
(`demand_shock` 17 + `opec_decision` 52 + `policy_response` 57 = 126) — types for which
`engine/persistence.py`'s `pers_blk` is always the fixed no-op
`{"P": [0.0], "G": None, "fallback": None}` regardless of source availability. The 187 mismatches are
*exactly* the geopolitical types (`infrastructure_attack` 48, `chokepoint_disruption` 27, `sanctions`
57, `conflict_escalation` 55 = 187) — the only types the G-persistence baseline touches. Outside that
one subsystem, the walk is **fully deterministic**, confirmed at the individual sealed-read level, not
just in aggregate.

### 4d. A vs B — isolating run-to-run nondeterminism from code-version drift

Same executed diff, A vs B, top-level:

| key | diffs (tol 0 = tol 1e-9) |
|---|---|
| `registered` | 0 |
| `data_state` | 0 |
| `permutation` | 0 |
| `placebo` | 0 |
| `spec_curve` | 0 |
| `verdict` | 0 |
| `fdr` | 29 |
| `tiers` | 19 |

All 48 diffs are the G-persistence numbers themselves, changing exactly as expected between "no
source data" (A) and "source data present" (B):

| metric | A (fallback ≈ climatology) | B (real persistence) |
|---|---|---|
| `tiers.daily.G.n_persistence_fallback` / `n_persistence_known` | 153 / 0 | 2 / 151 |
| `tiers.daily.G.engine_vs.persistence.skill` (95% CI, DM p) | −0.0070 (−0.084…+0.065, p=0.847) | **−0.4693** (−1.036…−0.138, p=0.002) |
| `tiers.daily.G.rps.engine_vs.persistence.skill` (DM p) | +0.0718 (p=0.076) | **−0.6413** (p<0.001) |
| `tiers.daily.G.spa_vs_persistence.p_spa` | 0.793 | 0.575 |
| `fdr.family[3]` (`daily:G:engine_vs_persistence`), `p` / `q_value` / `survives` | 0.847 / 0.874 / False | **0.00204 / 0.01867 / True** |

With no real persistence signal, the engine trivially "beats" a baseline that degenerated to
climatology (skill ≈ 0, indistinguishable from `engine_vs.climatology`). With the real 90-day-prior
IES-90 level available, persistence is a **much sharper baseline than climatology** on this corpus —
the engine loses to it badly (skill −0.47, DM p = 0.002, now the only G comparison besides RPS-vs-
random-analogs to survive BH-FDR). This is a real, substantive finding for whoever reads the
G-persistence baseline once it is live: **whether `data/state/raw`/`data/cache` are present silently
changes a headline number from "beats persistence, not significant" to "loses to persistence,
p=0.002, survives FDR."** Every other block — `registered`, `data_state`, `permutation`, `placebo`,
`spec_curve`, `verdict` — is byte-identical between A and B, so this is not general nondeterminism;
it is entirely contained in the one subsystem that reads gitignored, non-`oil.db` files at run time.

---

## 5. `tests/test_reproduce.py` — pytest output, verbatim

**Skip mode (`REPRO_SUMMARY`/`REPRO_READS` absent — the state of the real repo, untouched):**
```
$ python3 -m pytest tests/test_reproduce.py -q
sssssss                                                                  [100%]
7 skipped in 1.25s
```

**Run against clone A** (`REPRO_SUMMARY`/`REPRO_READS` → `ripple-clone/data/walk_forward/{summary.json,reads.jsonl}`):
```
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0 -- /usr/local/bin/python3
rootdir: /Users/default/Documents/Claude/Projects/News to Markets/ripple-engine
collecting ... collected 7 items

tests/test_reproduce.py::test_reproduce_run_id_present PASSED            [ 14%]
tests/test_reproduce.py::test_reproduce_same_reads_covered PASSED        [ 28%]
tests/test_reproduce.py::test_reproduce_seal_hash_embeds_run_identity PASSED [ 42%]
tests/test_reproduce.py::test_reproduce_content_hash_matches_read_by_read FAILED [ 57%]
tests/test_reproduce.py::test_reproduce_registered_block_matches FAILED  [ 71%]
tests/test_reproduce.py::test_reproduce_verdict_block_matches PASSED     [ 85%]
tests/test_reproduce.py::test_reproduce_scored_numbers_match_to_1e9 FAILED [100%]

=================================== FAILURES ===================================
E   AssertionError: 313 / 313 reads have a different content hash (run_id/sealed_at/hash
    excluded) between committed run walk_20260902T182828Z and the reproduction; first 20:
    [('daily', 'abqaiq_attack_2019'), ('daily', 'amplats_loadshed_2022'), ...]

E   AssertionError: registered block differs:
      registered.g_baselines: committed='<MISSING>' reproduced=['climatology', 'frozen',
      'random_analogs', 'persistence']

E   AssertionError: 162 numeric/structural diffs (tol 1e-9) in tiers/fdr/permutation/
    placebo/spec_curve:
      tiers.daily.G.engine_vs.persistence: committed='<MISSING>' reproduced={'n': 150, ...}
      tiers.daily.G.n_persistence_fallback: committed='<MISSING>' reproduced=153
      ... (full list in §4b/§4d above)

========================= 3 failed, 4 passed in 3.22s ==========================
```
Run against clone B is identical in shape (3 failed, 4 passed, same three tests, same root cause).

**These three failures are correct, expected, and should not be "fixed" by loosening the test.** They
are the Amendment-B code-drift finding, executed and pinned to specific keys and values, exactly what
§4b/§4c document. The four passes (`run_id_present`, `same_reads_covered`, `seal_hash_embeds_run_
identity`, `verdict_block_matches`) are the parts of the reproducibility claim that genuinely hold:
same corpus coverage, the seal's run-identity property confirmed by execution rather than assumed, and
the verdict — the one number Joe would actually read — unchanged.

---

## 6. Two things recorded, not fixed (per instruction)

- **Makefile `REPRO_DB` sibling-copy path bug**, found and fixed during this session:
  `SRC_DATA=$(cd "$(dirname "$(REPRO_DB)")/.." && pwd)` went up one directory too far (to the repo
  root instead of `data/`), so the first run (`ripple-clone`) silently didn't copy `state/raw`/`cache`
  and fell back to climatology for the G-persistence baseline on every read
  (`[read] persistence baseline unavailable: [Errno 2] No such file or directory: '.../data/state/
  raw/icb/icb1v16.csv'`). Fixed to `SRC_DATA=$(cd "$(dirname "$(REPRO_DB)")" && pwd)` (one `cd`, not
  two) before the second run (`ripple-clone-b`), which copied both directories correctly (log line
  `also copying state/raw/ ...` / `also copying cache/ ...`, and no fallback warning). The fix is
  already in the committed-to-be `Makefile` in the real repo.
- **The reproduce-guard fires on every clean clone, not just the shared tree**, because
  `data/walk_forward/reads.jsonl` (append-only ledger) is itself a *committed* file carrying five
  sealed runs already. `git clone` brings all five along, so `[ -s data/walk_forward/reads.jsonl ]`
  is true from the moment of cloning — `REPRO_FORCE=1` was required for both runs here, on brand-new
  clones, not because either looked like the shared working tree. The guard does what its docstring
  says ("nobody runs it by accident in the main tree") but its *test* — file non-empty — can't
  distinguish "shared tree with runs from this repo's own history" from "a clean clone that inherited
  the same committed history," because they're the same file. Left as found, per instruction; a
  guard that instead checked for `run_id`s *not* already present, or diffed against a fresh clone's
  own baseline count, would tell the two cases apart.

---

## 7. Reproducibility findings, each against the README claim it bears on

> "Every number in this repo is one hop from its receipt" — README.md, top matter.

**Mostly holds, with one precise qualification.** `data_state`, `permutation`, `placebo`,
`spec_curve`, `verdict`, and every pre-Amendment-B `tiers` number reproduce **exactly** (tolerance 0)
from the committed `oil.db`-adjacent inputs plus the committed code that produced them (§4b). The
"receipt" is real for those numbers. The qualification: the **receipt itself — `hash` — is not a hop
to the data alone.** `seal()` hashes `run_id` and `sealed_at` into the same digest as the read content
(§4a), so the hash cannot be used, as literally written, to prove two runs produced "the same" read;
a reader has to know to strip those two fields first (which is what `verify_seal`-adjacent code in
this report, and now in `tests/test_reproduce.py`, does). Recommend documenting that in `walk.py`'s
`seal()` docstring: what the hash proves (tamper-evidence of a *given* run) vs what it doesn't (cross-
run equality of content).

> "every result is published as computed, nulls included" — README.md, top matter.

**Holds**, and this review is itself evidence for it: `verdict` reproduces byte-identical
(`SUGGESTIVE / null` on both targets), and the one place a null flips to a positive result — the
G-persistence comparison, when its source data is present (B: p=0.002, survives FDR) vs absent (A:
p=0.847) — is a difference this review *found by running the code*, not something the repo's own
narrative currently states anywhere (Amendment B is not yet in `README.md`'s numbers, correctly, since
`README.md` still describes run 182828Z, which predates it). Once Amendment B is registered and run
live (with `data/state/raw`/`data/cache` actually present, as session B's real working tree has), that
number — engine loses to persistence, p=0.002 — is a real result and should be published as computed,
same as everything else. Flagging it here so it doesn't quietly become the version that gets missed.

> "the walk... four baselines (climatology, persistence, random analogs, a frozen engine)" —
> README.md, "What it is."

**Not yet true of the committed `summary.json` (run 182828Z)**, and the repo already half-documents
this itself: `data/gates/step8_2026-09-02.md` §"Gate 3" and its own commit history show the G-side
persistence baseline (`{"P": [0.0]}` placeholder for G) only became real code in `b7c8ec1`, one commit
after 182828Z was produced. §4b's diff makes this precise: `registered.g_baselines` is entirely absent
from the committed file. Not a defect — the README's "Run it" section already tells the reader
`python3 src/walk.py` "re-run[s] the walk; publishes `data/walk_forward/summary.json` as computed" —
but a reader comparing the README's baseline count against the currently-committed `summary.json`
would be off by one baseline until the walk is re-run and re-committed.

---

## WHAT I DID NOT DO

- Did not run `repro.sh`, any `src/fetch_*.py`, `src/state/ies90.py`'s network path, or anything
  requiring `EIA_API_KEY`/`NYT_API_KEY` — none of that is reachable offline, confirmed and reported
  (§1), not attempted.
- Did not run anything in the real repo beyond read-only inspection (`git log`, `git diff`, `git
  status`, `git ls-files`, `git check-ignore`, `cat`/`grep`/`python3 -c` reads) and `python3 -m pytest
  tests/test_reproduce.py` (safe: skips cleanly with no env vars, and even with env vars set it never
  writes under `data/` — verified by reading the test file's own docstring guarantee before running
  it against the real repo).
- Did not touch `src/walk.py`, `src/engine/*`, `tests/conftest.py`, or any other dirty/tracked file in
  the real repo — confirmed clean (`git status --short` before finishing shows only `Makefile`
  (untracked), `tests/test_reproduce.py` (untracked), `requirements.txt` (modified) as this review's
  changes).
- Did not `git add`, `commit`, or `stash` anything, in the real repo or the clones.
- Did not fix the Makefile guard's false-positive-on-clean-clone behavior (§6) — recorded per
  instruction, left for the synthesizing reviewer's call.
- Did not attempt to make `tests/test_reproduce.py`'s three failing assertions pass by loosening
  them — they are correct as written; the failures are the finding (§5).
- Did not re-run either clone's walk a third time; both runs already completed and were compared
  as-is. `A` (`ripple-clone`, REPRO_DB-only, persistence unavailable) was kept rather than discarded
  after the bug was found, because it turned into the control side of the §4d comparison.
- Did not investigate the other, concurrent session's activity in the real repo (Amendments C/D,
  commits `17a489d`/`07ed7a8`/`d6a3bde`) beyond noting HEAD had moved — out of scope for D-6.
