> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Adversarial review findings, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# D1b — RIPPLE_REGISTRATION.md/RIPPLE_SOURCES.md audit + Amendment D verification at HEAD

Audited repo: `/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine`
(branch `v2-day1`). Prior audit was at `b7c8ec1`; HEAD at time of this review is
`d6a3bde` (`git log --oneline -8` reproduced below). READ-ONLY: no file in the repo
was edited, created or deleted; two disposable `git worktree` checkouts were made
under the scratchpad (at commits `07ed7a8` and `d6a3bde`) to test isolated,
uncommitted-change-free copies of the code, and both were removed with
`git worktree remove` before finishing (`git worktree list` now shows only the
original working copy).

```
d6a3bde Brief R (c, Amendment A): cluster window = 35 calendar days...
847cd44 Brief A-10: feed register data/feeds/REGISTER.md...
fc706ef Brief A-9: reader accuracy on an unaudited gold set...
49f96b1 Brief A-8: knowable_at on every situation field...
266b918 Brief A-7: world-state panel 34 -> 50 of 70 fields...
84bd102 Brief A-6: pre-1987 admission dossiers...
cbf4fdc Brief R (c, register): RIPPLE_REGISTRATION.md...
df66b3c Brief R (a+b): RIPPLE_SOURCES.md...
   ... (07ed7a8 Amendment D at 4 commits further back; b7c8ec1 the prior-audit commit, 4 back from that)
```

**Commit ordering, checked with `git log --oneline --all | grep -n`:** line numbers
(1 = HEAD, larger = older) put `cbf4fdc` at line 7, `df66b3c` at line 9, `07ed7a8`
at line 11, `b7c8ec1` at line 15. So chronologically: `df66b3c` (sources+loaders) →
`cbf4fdc` (registration) → ... → `d6a3bde` (current HEAD). `src/ripple_lp.py` does
**not exist** at HEAD (`ls` returns "No such file or directory") — the
"registered before the code" claim in `RIPPLE_REGISTRATION.md` line 3 still holds,
unchanged since `cbf4fdc`.

**IMPORTANT — this repo is a live shared tree.** `git status` at the start of this
review already showed uncommitted changes to `src/walk.py` and `src/acceptance_v2.py`,
and by the time Part 2 was investigated, `src/engine/read.py` and
`src/engine/similarity.py` had *also* become modified — uncommitted — mid-session,
which no command of mine touched. This matches the standing note that ripple-engine
"sessions A/B share one tree." Findings below distinguish **HEAD (committed)**,
which is what the task asked to verify, from the **live working tree**, which is a
moving target being edited by another session concurrently with this review.

---

## PART 1 — RIPPLE_REGISTRATION.md / RIPPLE_SOURCES.md / ripple_fetch.py

| item | registered value (doc:line) | code (file:line) | status | note |
|---|---|---|---|---|
| Lag-augmented LP estimator (Montiel Olea–Plagborg-Møller) | RIPPLE_REGISTRATION.md:52-68, 211-229 | — | **UNIMPLEMENTED** | `src/ripple_lp.py` does not exist |
| EHW (HC1) primary SE vs Newey–West(h) diagnostic | RIPPLE_REGISTRATION.md:246-253 | — | **UNIMPLEMENTED** | no estimator code anywhere computes either |
| Fixed p, no pre-testing (p=5/4/6, robustness 2p) | RIPPLE_REGISTRATION.md:240-244 | — | **UNIMPLEMENTED** | |
| h/T check (≤0.6%/1.4%/2%) | RIPPLE_REGISTRATION.md:231-238 | — | **UNIMPLEMENTED** | arithmetic in the doc itself not re-derived by any script |
| Table M — class → Kilian/B&H mapping | RIPPLE_REGISTRATION.md:260-273 | — | **UNIMPLEMENTED** | declared as "not itself tested" (line 272-273) even once code exists |
| Table N — nodes (~35 rows) | RIPPLE_REGISTRATION.md:345-385 | src/ripple_fetch.py (raw series only) | **PARTIAL / UNIMPLEMENTED** | every *new* raw series Table N needs is loaded and seeded (see fetch table below); the LP-side node construction (transforms, sample starts, hop assembly) that Table N specifies does not exist |
| Horizons (daily 0..60, weekly 0..26, monthly 0..12) | RIPPLE_REGISTRATION.md:231-236 | — | **UNIMPLEMENTED** | |
| Min n = 15 de-overlapped events per class/node | RIPPLE_REGISTRATION.md:281-285 | — | **UNIMPLEMENTED** | |
| BH q = 0.10 (exploratory family) | RIPPLE_REGISTRATION.md:327-333 | — | **UNIMPLEMENTED** | repo already has a working `bh_fdr` (`engine/inference.py`, used by `walk.py`'s q=0.05 FDR family) but nothing wires it to the ripple family yet |
| Filtration lags table (declared publication lags) | RIPPLE_REGISTRATION.md:335-343 | src/ripple_fetch.py `load_into` (obs=as_of, no lag applied); src/derive_signals.py:286-288 (same convention for `derived.cot_pct`/`derived.inv_sigma`) | **MATCH (convention)** / UNIMPLEMENTED (LP use) | Confirmed by code and by `tests/test_ripple_fetch.py::test_r3b_load_into_is_append_only_and_stamps_as_of`, which asserts `as_of == obs_date` literally. §2.10's framing ("responses are measured on obs_date — a hindsight IRF, standard") is an accurate, disclosed description of existing repo behavior, not a hidden defect. See Finding 4. |
| Nine EXPECTATIONS (E-1…E-9) | RIPPLE_REGISTRATION.md:406-430 | — | **UNIMPLEMENTED** | `data/ripple/` output directory (§5, line 396) does not exist; nothing computed |
| Placebo (500 pseudo-event draws, seed 19900802) | RIPPLE_REGISTRATION.md:286-292, 403 | — | **UNIMPLEMENTED** | an *unrelated, older* placebo (`data/placebo_vixmatched.json`, `placebo_vixmatched.py`) exists and is explicitly cited/extended by §2.5 (line 289), but the ripple-specific 500-draw placebo is not built |
| Asymmetry test (crude→product hop, §2.6) | RIPPLE_REGISTRATION.md:294-305 | — | **UNIMPLEMENTED** | |
| 2009-02-06/02-13 gas regime split (Ramberg–Parsons) | RIPPLE_REGISTRATION.md:307-313 | — | **UNIMPLEMENTED** | no file references this date anywhere in `data/`, `src/`, or existing docs |
| Kilian–Vigfusson uncensored sign split (never censor) | RIPPLE_REGISTRATION.md:148-160, 297-298 | — | **UNIMPLEMENTED** | |
| Amendment A correction: CLUSTER_DAYS = 35 calendar days (not 20 trading days) | RIPPLE_REGISTRATION.md:444-448 | src/robustness.py:48, 62-67 | **MATCH** | `CLUSTER_DAYS = 35`; `assign_clusters` compares `(d - last_date).days <= CLUSTER_DAYS` — calendar days, confirmed |
| RIPPLE_SOURCES.md verification register | RIPPLE_SOURCES.md (whole file, 276 lines) | — | **MATCH** | every source line states how-verified/how-loaded; GAP lines present for unverifiable licences (Baltic indices, PortWatch terms, B&H licence, pre-2006 USD splice, etc.) |
| src/ripple_fetch.py loaders (FRED, EIA hist_xls, Pink Sheet, PortWatch, Kaenzig, B&H, yfinance) | RIPPLE_SOURCES.md #2-#7 | src/ripple_fetch.py:1-537 | **MATCH, tested** | `python3 -m pytest tests/test_ripple_fetch.py -q` → **7 passed** (executed) |
| data/seed/ripple sha256 manifest | RIPPLE_SOURCES.md "loader run... 54 series ok, 0 failed" | data/seed/ripple/MANIFEST.json (18 entries) | **MATCH, executed** | independent Python re-hash of every seeded CSV against `MANIFEST.json["sha256"]`: 18/18 match, 0 bad |
| "live run 54 ok / 0 failed" (commit message) | df66b3c commit message | 18 series are seeded (committable licence); the remaining ~36 (`bh.*`, `yf.*`, `portwatch.*`) are refresh-only by design | **UNTESTED here** | the 54/0 network claim could not be re-verified without a live `--refresh` fetch (out of scope for a read-only review; not attempted) |

**Publication-before-code check.** Grepped `data/`, `README.md`, `docs/PAPER_DRAFT.md`,
`src/app.html` for `ripple_lp`, `RIPPLE_REGISTRATION`, `beta_h`, `IRF`, `local_projection`:
the only hit is `docs/PAPER_DRAFT.md:342`, a forward reference — *"registered as the
next build (`RIPPLE_REGISTRATION.md`, forthcoming) and are not [yet computed]"* — not a
published number. `data/ripple/` does not exist. **No violation found**: nothing from
this registration has been computed or published anywhere in the repo.

**"Expectations written with knowledge of already-published results" check.** The
repo already has older, methodologically different (constant-mean event-study CAR,
not LP) results in `data/cross_asset_results.txt` / `data/chain_report.txt` /
`data/local_projections.json` (the last of these is an *unrelated* H1/VIX-amplification
study, not the chain-hop ripple study — different y-variable, different regressor).
See Finding 5 below for the one place this matters.

---

## PART 2 — WALK_FORWARD_PROTOCOL.md Amendment D vs. commit 07ed7a8, at HEAD

Amendment D text: WALK_FORWARD_PROTOCOL.md:219-226.

| item | Amendment D text (doc:line) | code (file:line) | status | note |
|---|---|---|---|---|
| Every earlier run's rows MOVED (never edited, never dropped) to `runs/<run_id>/*.jsonl.gz` | WALK_FORWARD_PROTOCOL.md:221-223 | src/walk.py:121-148 `archive_prior_runs` | **MATCH** | reads split by `run_id`, non-keep lines appended (gzip `"at"` mode) to the archive, keep-only lines rewritten to the tree file; verified end-to-end by `tests/test_walk_archive.py` (hash sets identical before/after: `{r["hash"] for r in ... run_A} == before`) |
| Append-only within each run's archive file | WALK_FORWARD_PROTOCOL.md:225 (§2 discipline) | src/walk.py:135-140 (`gzip.open(..., "at", ...)`) | **MATCH** | test archives run_A, then a third run archives run_B beside it and asserts run_A's archive is `len(...) == n` — "untouched by later archiving" |
| Each archive still verifies by `walk.verify_file` | WALK_FORWARD_PROTOCOL.md:224 | src/walk.py:109-117 `verify_file` (reads `gzip` via `_open_text`); called on `reads.jsonl.gz` only, src/walk.py:144-148 | **MATCH (reads) / caveat** | Only `reads.jsonl` records carry a content hash at all (WALK_FORWARD_PROTOCOL.md §2: *"Each read is sealed"* — scores/weights are not independently sealed; confirmed — `sf.write`/`wf.write` records have no `"hash"` key). So "each archive still verifies" can only be literally true for the reads archive; `manifest[run_id]` has no `scores_seal_ok`/`weights_seal_ok` keys. Not a functional gap, but the amendment's wording overstates what's checked. See Finding 2. |
| `summary.json.data_state.archived_runs` carries the manifest with each archive's run_ids, counts, seal checks | WALK_FORWARD_PROTOCOL.md:224 | src/walk.py:1282-1283 | **MATCH** | `summary["data_state"]["archived_runs"] = archive_prior_runs(out_dir, w.run_id)`; manifest shape `{run_id: {"reads.jsonl": n, "scores.jsonl": n, "weights.jsonl": n, "reads_seal_ok": bool, "reads_records_in_archive": n, "first_bad_line": None}}` |
| `runs/` git-ignored, kept on disk | WALK_FORWARD_PROTOCOL.md:223 | .gitignore:97-98 | **MATCH** | `data/walk_forward/runs/` present in `.gitignore` |
| Leakage test and seal check computed on the run in the tree | WALK_FORWARD_PROTOCOL.md:226 | src/walk.py: `leakage_test` call ≈ line 1252 (before archiving); `summary["seal_check"] = verify_file(out_dir / "reads.jsonl")` at line ≈1284 (after archiving, when the tree file holds only the current run) | **MATCH** | ordering is correct: leakage is computed against the full pre-archive `Walk` object in memory; the post-archive seal check re-reads the tree file, which by then correctly contains only `w.run_id` |
| `tests/test_walk_archive.py` (Amendment D's own evidence) | commit 07ed7a8 message | tests/test_walk_archive.py (43 lines) | **MATCH at HEAD, FAILS in the live working tree** | see Finding 1 — full detail below |

**Test execution, three ways (all `python3 -m pytest tests/test_walk_archive.py -q`):**
1. Isolated `git worktree` checkout **at commit `07ed7a8`** (Amendment D's own commit): **1 passed**.
2. Isolated `git worktree` checkout **at HEAD `d6a3bde`** (committed, no uncommitted changes): **1 passed**.
3. **Live working tree** (as it stands right now, with other in-flight uncommitted edits): **1 failed** — `assert W.leakage_test(w_c, w3)["asserted"]` → `AssertionError: assert False`.

So **"verified against the committed code at HEAD": PASS.** The failure only
reproduces in the uncommitted working tree — see Finding 1 for why, and why it is
not a defect in Amendment D.

**`data/walk_forward/summary.json` at HEAD — does it carry `archived_runs`?**
No. `python3 -c "json.load(open(...))['data_state']"` shows no `archived_runs` /
`archive_dir` key. The file's `run_id` is `walk_20260902T182828Z` — the same run
`docs/PAPER_DRAFT.md` cites — which predates commit `07ed7a8`. This is exactly the
expected state per the task: it should not carry `archived_runs` until the *next*
full pipeline run writes a new `summary.json`.

**Has the archive ever run in this tree?** `ls data/walk_forward/` shows no `runs/`
subdirectory — **the archive mechanism has never fired**, consistent with the
`summary.json` finding above. See Finding 3 for what this means given the tree's
current (uncommitted) state.

---

## Findings, ranked

**Finding 1 (moderate — evidentiary, Part 2).** The test cited as Amendment D's proof,
`tests/test_walk_archive.py`, passes cleanly against the *committed* code at both
`07ed7a8` and HEAD (`d6a3bde`), confirmed by running it in two disposable, isolated
`git worktree` checkouts. But it currently **fails** in the live working tree, and
not for an archive reason: `leakage_test(w_c, w3)` returns `asserted: False` because
uncommitted, in-flight changes to `src/engine/read.py` and `src/engine/similarity.py`
(unrelated "Amendment G"/"Amendment H" work — release lags and situation
`knowable_at` blanking, both dated 2026-09-02, apparently another session's live
edit) change analog retrieval enough that the synthetic test corpus's broken-filtration
run stops differing from its sealed run (`n_reads_with_different_analogs: 0`, `G`/`P`
scores both `null` — i.e. no scored reads at all). Diagnosed directly: re-running the
identical test body by hand in the working tree vs. the HEAD worktree checkout, with
everything else (seed=3, `MENU`, `FAST`) held fixed, reproduces the divergence.
**Risk if unqualified:** any claim that "tests are green" for this repo right now,
read without pinning to a commit, is not reliable — the tree is being edited by a
concurrent session mid-review. CLAUDE.md's own rule (*"I verify by running things,
reading outputs"*) means a `pytest` run in this tree today needs a commit hash
attached to be trustworthy evidence.

**Finding 2 (low — Part 2, wording).** Amendment D's text, *"each archive still
verifies by `walk.verify_file`"* (WALK_FORWARD_PROTOCOL.md:224), is only true for
the `reads.jsonl.gz` archive. `scores.jsonl` and `weights.jsonl` records carry no
`"hash"` field (only `reads.jsonl` records are sealed, per WALK_FORWARD_PROTOCOL.md
§2, *"Each read is sealed"*), so `verify_file` is never even called on their `.gz`
archives, and the manifest has no seal-check field for them. This is consistent
with the protocol's actual sealing design (there's nothing to verify on
scores/weights), but the amendment's own sentence overstates it. Not a functional
gap — no fix needed, just a note for anyone reading the amendment literally.

**Finding 3 (informational — Part 2, operational).** `data/walk_forward/runs/` does
not exist: the archive has never executed, anywhere, in this tree. Meanwhile the
*live, uncommitted* `data/walk_forward/{reads,scores,weights}.jsonl` currently hold
**7 distinct `run_id`s** (checked directly: `walk_20260902T180646Z`,
`walk_20260902T192906Z`, `walk_20260902T163321Z`, `walk_20260902T180821Z`,
`walk_20260902T193022Z`, plus 2 more), and `git diff --stat HEAD` shows exactly
+626 lines added to each of the three files with zero deletions — i.e. pure
appends, consistent with several `Walk(...).run_reads()` invocations against the
real `data/walk_forward/` directory (not the tmp-dir the test suite uses) that
never reached the full `run()` pipeline's archiving step. This is not a defect in
Amendment D — `archive_prior_runs` is only ever called from inside `run()`
(src/walk.py:1282), by design, "when a run completes" — but it does mean the next
full `run()` invocation will archive 6 runs' worth of rows in one shot, which is
worth Joe knowing about before it happens (and worth asking the other session
whether those 6 stray runs were intentional).

**Finding 4 (low — Part 1, disclosure check).** RIPPLE_REGISTRATION.md §2.10
(line 338) states FRED daily-spot responses are measured "on `obs_date` (a
hindsight IRF, standard)" with no as_of adjustment for the ~1-3 business day FRED
publication lag. Checked against code: `src/ripple_fetch.py`'s `load_into` writes
`as_of = obs_date` literally (line ≈487), and this is the *same* convention already
used by `derived.cot_pct` and `derived.inv_sigma` in `src/derive_signals.py`
(lines 286-288, `payload = [(sid, d.strftime(...), ..., d.strftime(...), now)]` —
both date fields identical). `tests/test_ripple_fetch.py`'s
`test_r3b_load_into_is_append_only_and_stamps_as_of` asserts this explicitly. So the
registration's framing is an *honest, accurate* disclosure of existing repo
behavior, not a hidden defect — it correctly names the convention it inherits.
One thing to flag for whoever eventually writes `ripple_lp.py`: the *uncommitted*
Amendment G work in `src/engine/similarity.py` (RELEASE_LAGS = {"cot_pct": 3,
"inv_sigma": 5}) is introducing a *second*, different lag mechanism — applied at
read time in `InfoSet`, not by changing `as_of` in storage — for exactly the two
series RIPPLE_REGISTRATION.md's §2.10 table also lists (EIA weekly, ≈ t+5 days).
When the LP code is written, it should either reuse that read-time mechanism for
its knowable-control lookups or explicitly say why it doesn't; right now there are
two lag conventions coexisting in the repo (raw storage un-lagged; some
consumers apply a lag at read time, others use `obs_date` directly), and
RIPPLE_REGISTRATION.md doesn't yet know Amendment G exists (it's newer,
uncommitted, uncorrelated work).

**Finding 5 (informational, positive — Part 1, "written with knowledge of results"
check).** E-1 (RIPPLE_REGISTRATION.md:406-407) predicts *"tightening classes
(chokepoint, infrastructure, conflict) raise Brent at h=5."* The repo's older,
already-published, different-methodology event study
(`data/cross_asset_results.txt`, "CLUSTERED MEAN CAR+5 by event type x asset,"
Brent oil column) actually shows: chokepoint_disruption **−8.1%**, conflict_escalation
**+3.8%**, infrastructure_attack **−1.0%**. Two of the three "tightening" classes have
the *opposite* sign from what E-1 predicts, in a file that was sitting in the repo
before the registration was written. This is evidence the expectation was **not**
copy-pasted or reverse-engineered from the already-published number — a
post-hoc-informed author would have matched the known sign, not contradicted it.
Reported per instructions ("quote any expectation that restates an already-published
number") even though the answer here is *no restatement found* — the opposite, in
fact, which is worth Joe seeing since it's the kind of blind-spot check that could
have gone the other way.

---

## Arithmetic executed (python3)

- `18/18` seed manifest sha256 hashes match (`hashlib.sha256` re-computed per file,
  compared to `MANIFEST.json`).
- `7 passed` — `pytest tests/test_ripple_fetch.py -q`.
- `1 passed` (×2, isolated worktrees at `07ed7a8` and `d6a3bde`) / `1 failed`
  (live working tree) — `pytest tests/test_walk_archive.py -q`.
- Commit recency ordering derived from `git log --oneline --all | grep -n`
  line numbers (1 = HEAD-most-recent): `cbf4fdc`=7, `df66b3c`=9, `07ed7a8`=11,
  `b7c8ec1`=15.
- `626 × 3 = 1878` uncommitted lines added across the three `data/walk_forward/*.jsonl`
  files (`git diff --stat HEAD`).
- `7` distinct `run_id`s currently present in the live (uncommitted)
  `data/walk_forward/reads.jsonl` (counted with a `set()` over parsed JSON lines).

## WHAT I DID NOT DO

- Did not run `src/ripple_fetch.py --refresh` (would touch live network + write
  under `data/` — out of scope/forbidden for a read-only review); the "54 series
  ok / 0 failed" live-fetch claim in RIPPLE_SOURCES.md was therefore left
  UNTESTED here, not verified.
- Did not run the full `src/walk.py` pipeline (`run()`) to force
  `archive_prior_runs` to actually fire on the 7 stray run_ids — would write under
  `data/walk_forward/`, explicitly forbidden by the task.
- Did not attempt to diagnose or fix the `leakage_test` regression in
  `src/engine/read.py`/`similarity.py` — out of scope (uncommitted, another
  session's in-flight work) and this review is read-only.
- Did not re-open or re-verify the twelve academic sources RIPPLE_REGISTRATION.md
  cites (Jordà, Montiel Olea–Plagborg-Møller, etc.) — took the document's own
  "opened"/"not opened" disclosures at face value, since that's the standard the
  document itself sets (e.g. explicitly flags Kilian 2010 and B&G as NOT OPENED,
  not cited).
