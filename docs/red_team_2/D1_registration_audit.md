> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Adversarial review findings, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# D-1 — Registration-vs-Code Audit

Repo: ripple-engine, branch `v2-day1`, HEAD `b7c8ec1` (2026-09-02 14:58:39 -0400).
Audited state: **committed (`git show HEAD:<path>`)** for every file listed as dirty in the
prompt. Working-tree edits (another session, mid-flight) are described only where they change
the interpretation of a finding; they are never treated as "the code."

`git diff --stat HEAD` (uncommitted, NOT audited as code):
```
 data/alert_queue.csv        | 4761 +------------------------------------------
 data/engine_read.json       |  116 +-
 data/engine_status.json     |    2 +-
 data/signal_registry.json   |    2 +-
 data/sowhat.json            |   86 +-
 data/walk_forward/menu.json |  204 +-
 data/watch_seen.db          |  Bin 643072 -> 32768 bytes
 src/engine/read.py          |    2 +-
 src/engine/scoring.py       |   20 +-
 src/engine/similarity.py    |    8 +-
 src/walk.py                 |  139 +-
 tests/conftest.py           |    1 +-
 12 files changed, 449 insertions(+), 4892 deletions(-)
```
Untracked, also not audited as committed code: `TASK_BRIEF_12/13/22.md`, `TASK_BRIEF_PLATFORM.md`,
`TASK_QUEUE_A.md`, `UNIFIED_PLATFORM_BRIEF.md`, `VISION_ROADMAP.md`, `data/audit_202609.md`,
`practice/`, **`src/engine/recalibrate.py`**, **`tests/test_walk_recalibration.py`**.

The dirty `src/walk.py` already wires WALK_FORWARD_PROTOCOL.md Amendment C (M13 recalibration)
against the uncommitted `engine.recalibrate` module and an uncommitted `menu.json` (13 items,
`M13_recalibrated` appended). At HEAD, none of that exists: the committed `menu.json` has 12
items and committed `walk.py` never imports `recalibrate`. That is the **correct** state per
Amendment C's own rule ("registered first, computed after") — noted here, not flagged as a
finding, because the committed record is internally consistent (see Amendment-timing table below).

---

## 0. Amendment-timing check (registration must precede the code that uses it)

For every dated amendment, the commit that added the amendment text vs. the commit that added
the code using it (`git log --format='%h %ci %s'`):

| Document | Amendment | Registered (commit, time) | Code (commit, time) | Order |
|---|---|---|---|---|
| BIG_MOVES_REGISTRATION.md | base doc + Amendments 1, 2 | `594d2fa` 00:12:55 | `src/big_moves.py` **same commit** `594d2fa` 00:12:55 | **SAME COMMIT — unverifiable** |
| BIG_MOVES_REGISTRATION.md | Amendment 3 (monthly tier) | `0abcc39` 10:21:30 | `src/big_moves.py` monthly-tier code, **same commit** `0abcc39` 10:21:30 | **SAME COMMIT — unverifiable** |
| CLAIM_LEDGER_REGISTRATION.md | base doc (§1-4) + Amendments 1, 2 | `594d2fa` 00:12:55 | `src/materiality.py`, `src/ledger.py` **same commit** `594d2fa` | **SAME COMMIT — unverifiable** |
| CLAIM_LEDGER_REGISTRATION.md | Amendment 3 (caged reader) | `11f3ecc` 00:45:19 | `src/reader.py` added `22a575a` 01:05:00 | OK (code after) |
| CLAIM_LEDGER_REGISTRATION.md | Amendment 4 (Challenge loop) | `cb0682d` 10:19:42 | `src/challenge.py`, `src/escalation.py` `f73fd73` 10:27:20 | OK (code after) |
| OUTCOME_MAPPING.md | base + Amendment 1 | `186d103` 11:39:53 / `dc96877`… (base `b17d760` 11:39:53) | `src/state/outcomes.py` PATH Step 4 `bf4b4e6` 11:48:15; `src/state/ies90.py` Amendment 1 code `6e06b60` 12:58:33 | OK |
| OUTCOME_MAPPING.md | Amendment 1.1 | `0af5cf5` 12:51:28 | `src/state/ies90.py` (same commit as 1+1.1 code) `6e06b60` 12:58:33 | OK |
| OUTCOME_MAPPING.md | Amendment 2 | `dc96877` 14:20:43 | `src/state/ies90.py` rebuild `6098539` 14:25:57 | OK |
| WALK_FORWARD_PROTOCOL.md | base doc | `3547559` 10:30:47 | `src/walk.py` `c2443a0` 12:37:55 | OK, **but** see §1 below — most of the numeric constants `walk.py` calls "REGISTERED" do not appear anywhere in this document, at any commit |
| WALK_FORWARD_PROTOCOL.md | Amendments B, C, D | `ae873b6` 14:53:20 | `src/engine/persistence.py` (Amendment B) `b7c8ec1` 14:58:39; Amendment C code (`recalibrate.py`) **not committed**; Amendment D (archive) code **not present anywhere** in the tree | OK for B; C correctly has no code yet; **D has never been implemented, in any commit** (see F-6) |
| data/candidates/REGISTRATION.md | — | committed with `src/dossier.py`'s partial re-use, no dedicated commit | the document's own deliverable (`pre1987_candidates.csv` + its generator) has **no code at all**, in any commit | UNIMPLEMENTED (see F-7) |
| data/walk_forward/menu.json | registered 2026-09-02 | `c4335ef` 11:19:41, "committed before Step 7 and before any walk runs" | `src/walk.py` reads it starting `c2443a0` 12:37:55 | OK |

**Reading:** the amendment-by-amendment discipline (each dated, each committed before the code
that consumes it) holds up everywhere it can be checked *except* the two base registrations
(BIG_MOVES_REGISTRATION.md, CLAIM_LEDGER_REGISTRATION.md) and BIG_MOVES Amendment 3, where the
registration text and the implementing code landed in **the same git commit**. Git history
cannot establish "registered before computed" for those — it can only establish that they were
never disclosed as separately timestamped. This is a process-integrity finding (F-1), not
necessarily a numeric one: see §1 for what the "same commit" pattern hides in this repo's most
important file (`walk.py`).

---

## 1. WALK_FORWARD_PROTOCOL.md vs `src/walk.py` (`REGISTERED` dict, committed, lines 60-77) and `data/walk_forward/summary.json`

`summary.json.registered` was compared field-by-field against `walk.py`'s committed `REGISTERED`
dict with a Python script (not by hand):

```
burn_in 8==8  k_max 12==12  cluster_days 35==35  eta 0.25==0.25  g_scale 2.0==2.0  p_scale 30.0==30.0
random_draws 25==25  n_boot 2000==2000  n_spa_boot 1000==1000  n_perm 1000==1000  min_tier_n 30==30
regime_blocks [2008,2020,2026]==same  placebo_reps 5==5  placebo_excl_days 30==30
spec {...}==same  pit_bins 10==10  reliability_bins 5==5   -> 0 mismatches
```
`summary.json`'s registered block is **byte-for-byte the same dict** `walk.py` writes into it —
it is not an independent check, it is a copy. So item 5 of the task ("does summary.json's
registered block match the protocol values exactly") resolves to: it matches `walk.py`
**exactly** (trivially — same source), and the real question is whether `walk.py`'s
`REGISTERED` dict matches **WALK_FORWARD_PROTOCOL.md**. It mostly does not:

| item | registered value (doc:line) | code (walk.py:line, committed) | status | note |
|---|---|---|---|---|
| burn-in ≥8 prior members | WALK_FORWARD_PROTOCOL.md:43 | `"burn_in": 8` (walk.py:64) | MATCH | |
| reads within 35 days = one cluster | WALK_FORWARD_PROTOCOL.md:102 | `"cluster_days": 35` (walk.py:66) | MATCH | |
| label permutation 1,000 times | WALK_FORWARD_PROTOCOL.md:111 | `"n_perm": 1000` (walk.py:72) | MATCH | |
| regime blocks 2008, 2020, 2026 | WALK_FORWARD_PROTOCOL.md:114-115 | `"regime_blocks": [2008,2020,2026]` (walk.py:70) | MATCH | |
| min_tier_n 30 ("describes, does not validate") | data/candidates/REGISTRATION.md:8 (cross-doc; WALK_FORWARD_PROTOCOL.md:140 states the *fact* n≈300/14 but not the literal cutoff "30") | `"min_tier_n": 30` (walk.py:73) | MATCH (sourced from a different registered doc) | |
| horizon +20 trading days / +3 months | WALK_FORWARD_PROTOCOL.md:11-12; CLAIM_LEDGER_REGISTRATION.md:29-30 | `TIERS["daily"]["horizon"]=20`, `TIERS["monthly"]["horizon"]=3` (engine/read.py:52-56, committed) | MATCH | |
| **Hedge η (eta)** | *not stated anywhere in WALK_FORWARD_PROTOCOL.md* | `"eta": LN.ETA` = 0.25 (walk.py:67; `src/engine/learning.py:21`) | **UNREGISTERED** | learning.py's own docstring calls it "Registered: ETA = 0.25 (~ sqrt(8 ln 12 / 300))" — verified `sqrt(8·ln12/300) = 0.2574` (python) — a reasoned choice, but the word "Registered" here means only "present in this source file," not "stated in a dated document before the code." Same commit as the code (`c2443a0`). |
| **k_max = 12** | WALK_FORWARD_PROTOCOL.md:83-84 says only "k" is adjustable via the menu; no fixed cap is registered as a scoring parameter (menu.json's per-item k values are registered, but "keep 12 analogs per item so the spec curve can slice k" is a walk.py-only choice) | `"k_max": 12` (walk.py:65) | **UNREGISTERED** (derivable from menu.json's max k=12, but not itself stated) | |
| **g_scale = 2.0, p_scale = 30.0** (Hedge loss normalizers) | not in WALK_FORWARD_PROTOCOL.md | walk.py:68-69 | **UNREGISTERED** | |
| **random_draws = 25** (baseline-3 seeded draws) | WALK_FORWARD_PROTOCOL.md:75-76 registers *that* random analogs are a baseline, not a draw count | walk.py:71 | **UNREGISTERED** | |
| **n_boot=2000, n_spa_boot=1000** (bootstrap/SPA replications) | not in WALK_FORWARD_PROTOCOL.md §6 | walk.py:72 | **UNREGISTERED** | |
| **placebo_reps=5, placebo_excl_days=30** | WALK_FORWARD_PROTOCOL.md:109 registers the placebo *mechanism* ("VIX/vol-matched pseudo-events... already built"), not a rep count or exclusion window | walk.py:75 | **UNREGISTERED** | |
| **pit_bins=10, reliability_bins=5** | WALK_FORWARD_PROTOCOL.md:64 (PIT), :57-58 (reliability diagrams) register the *diagnostics*, not bin counts | walk.py:78 | **UNREGISTERED** | |
| **spec curve ranges** `burn_in:[6,8,10] k:[5,8,12] horizon_daily:[15,20,25] cluster_days:[25,35,45] big_move_q:[0.90,0.95,0.975]` | WALK_FORWARD_PROTOCOL.md:116-118: "every registered threshold... varied across its **pre-declared range**" — the range itself is never written down anywhere in the document | walk.py:76-77 | **UNREGISTERED** (the doc promises a "pre-declared range" and never declares it) | k range [5,8,12] does at least trace to menu.json's own registered per-item k values (M06 k=5, M01 k=8, M07/M10 k=12) — the only one of the five spec dimensions with a paper trail |

**Computed:** `data/walk_forward/summary.json.spec_curve.rows` has **162** entries (python: `len(json.load(...)['spec_curve']['rows'])==162`), matching README's "negative in 83% of 162 registered settings" exactly. The word "registered" in that README sentence is carrying weight the audit trail does not support — see F-2.

Test coverage for these constants: `tests/test_walk.py` and `tests/test_walk_baselines.py` test
*mechanisms* (Hedge regret bound, DM/HLN textbook case, leakage, placebo-null-on-synthetic-data,
permutation positive control) — none asserts `REGISTERED["eta"] == 0.25`, or any of the other
values in this table, against an independent source. **UNTESTED** as registered values (the
mechanisms they parameterize are tested; the specific numbers are not).

---

## 2. BIG_MOVES_REGISTRATION.md vs `src/big_moves.py` (committed)

| item | registered value (doc:line) | code (big_moves.py:line) | status | note |
|---|---|---|---|---|
| windows: 20 and 60 trading days | BIG_MOVES_REGISTRATION.md:8 | `TIERS["daily"]["windows"]=(20,60)` (big_moves.py:33) | MATCH | |
| threshold: top 5% (two-sided) of own history | BIG_MOVES_REGISTRATION.md:8-9 | `TOP_Q = 0.95` (big_moves.py:39), `r.abs().quantile(TOP_Q)` | MATCH | |
| **clustering: within 60 trading days of episode start** | BIG_MOVES_REGISTRATION.md:10-11 (never revised by Amendment 1 or 2 — neither touches the cluster window) | `TIERS["daily"]["cluster_days"]=90` / module const `CLUSTER_DAYS=90` (big_moves.py:33,40), calendar days not trading days | **DEVIATION, uncovered** | see F-3 |
| episode start/peak (pre-Amendment-1 wording) | BIG_MOVES_REGISTRATION.md:11-12 | superseded by Amendment 1 (onset/end) — code follows Amendment 1 | MATCH (via amendment) | |
| Amendment 1: trailing returns; END = date of max \|trailing return\|; ONSET = price extreme in [end−W, end] | BIG_MOVES_REGISTRATION.md:40-43 | `episodes_for()` big_moves.py:64-86 (`end = clus.abs().idxmax()`; `onset = win.idxmin()/idxmax()` over `s.loc[:end].iloc[-(W+1):]`) | MATCH | |
| Amendment 1: display uses simple % change, not log return | BIG_MOVES_REGISTRATION.md:45 | `chg = (s.loc[end]/s.loc[onset]-1)*100` (big_moves.py:81) | MATCH | |
| Amendment 2: attribution window = [onset−7d, episode end]; lag from onset; lag>20d ⇒ ANTICIPATED | BIG_MOVES_REGISTRATION.md:51-54 | `attribute()` big_moves.py:104-114; `ATTR_BEFORE_DAYS=7`, `ANTICIPATED_LAG=20` (big_moves.py:42-43) | MATCH | |
| **no "merge" step registered anywhere for the daily tier** | absent from base doc, Amendment 1, Amendment 2 | `MERGE_DAYS=60` (big_moves.py:41) merges same-sign clusters within 60 days for **both** tiers via the generic `episodes_for()` (big_moves.py:88-98) | **UNREGISTERED for daily** (the concept exists only in Amendment 3, and only for monthly) | see F-3 |
| Amendment 3 (monthly): windows 3 & 12 months | BIG_MOVES_REGISTRATION.md:61-62 | `TIERS["monthly"]["windows"]=(3,12)` (big_moves.py:35) | MATCH | |
| Amendment 3: cluster window 365 days | BIG_MOVES_REGISTRATION.md:63 | `TIERS["monthly"]["cluster_days"]=365` (big_moves.py:35) | MATCH | |
| Amendment 3: same-sign merge within 180 days | BIG_MOVES_REGISTRATION.md:63 | `TIERS["monthly"]["merge_days"]=180` (big_moves.py:35) | MATCH | |
| Amendment 3: attribution [onset−31d, end]; ANTICIPATED if lag>60d | BIG_MOVES_REGISTRATION.md:64-65 | `TIERS["monthly"]["attr_before_days"]=31`, `anticipated_lag"]=60` (big_moves.py:35-36) | MATCH | |
| Amendment 3: monthly labelled "monthly resolution", tiers never pooled | BIG_MOVES_REGISTRATION.md:66 | `res["registration"]` string tags tier (big_moves.py:151); `TIER_ORDER`/tier fields separate outputs | MATCH | |
| Additional episode types: curve flip, volatility break, product-spread blowout, flow drop | BIG_MOVES_REGISTRATION.md:13-17, "computed when series exist" (conditional, disclosed) | **absent** — `grep -rn "curve flip\|curve_flip\|volatility break\|vol_break\|blowout\|flow drop\|flow_drop" src/*.py` returns nothing | UNIMPLEMENTED (disclosed as conditional, so not a violation on its own) | |

**Git-history confirmation for F-3:** `CLUSTER_DAYS = 90` and `MERGE_DAYS = 60` were both present
in the **very first** v2 commit (`594d2fa`, 2026-09-02 00:12:55), the same commit that landed
BIG_MOVES_REGISTRATION.md with Amendments 1 and 2 already included. `git log -S"CLUSTER_DAYS = 90"`
and `git log -S"MERGE_DAYS = 60"` both return only that commit for their introduction (90/60→90
was later reformatted, not changed, at `0abcc39`). So this is not drift from a later edit — the
very first working implementation of Big Moves used a clustering/merge rule the registration
document never states, and the code's own module docstring (big_moves.py:6) claims "this module
implements Amendment 2 **exactly**" — Amendment 2 says nothing about cluster or merge windows.

**Test coverage:** no `test_big_moves*.py` file exists. The only test touching `episodes_for()`
is `tests/test_v2_gate_ledger.py::test_big_moves_detects_a_planted_shock_and_dates_onset`
(lines 44-56), a single clean 30-day shock — it cannot distinguish a 60-day from a 90-day cluster
window or exercise the merge step at all. **UNTESTED** for both CLUSTER_DAYS and MERGE_DAYS.

**Downstream number check (executed in python against `data/big_moves/brent.json` /
`summary.json`):**
- `n_episodes=43`, `no_identified_event=15` → 15/43 = **34.9%** ≈ README's "35%" — MATCH, but this
  number is a direct product of the undocumented 90-day/60-day clustering-and-merge rule (F-3),
  not of the registered 60-trading-day rule with no merge step. A rerun under the literally
  registered rule would very likely produce a different episode count and a different
  no-identified-event share; nobody has published what that alternate run gives.
- "the market's extreme preceded the catalyst in a third of the rest" (README, "What it found"):
  I could not reconstruct this figure from `data/big_moves/brent.json`'s `anticipated` flags
  under any of four plausible readings, each computed in python:
  - episodes (Brent only) where **every** attributed event is anticipated: 14/28 = **50.0%**
  - episodes (Brent only) where **any** attributed event is anticipated: 20/28 = **71.4%**
  - the closest-lag event per episode (Brent only) anticipated: 14/28 = **50.0%**
  - pooling all three daily assets (brent+wti+diesel_crack), "every event anticipated": 33/89 =
    **37.1%** — the closest of the four to "a third," but it requires abandoning the sentence's
    own stated scope ("Big Moves, **Brent**, 43 episodes") to pool in WTI and the diesel crack.
  This is a **thin, unresolved** finding (F-4): not proven wrong, not reproduced. The evidence is
  that no formula I tried against the published Big Moves JSON, executed exactly, lands on "a
  third" while also staying inside the sentence's own stated Brent-only scope.

---

## 3. CLAIM_LEDGER_REGISTRATION.md vs `src/materiality.py`, `src/ledger.py`, `src/reader.py`, `src/challenge.py`, `src/escalation.py` (committed)

*(materiality.py, reader.py, challenge.py, escalation.py, deconstruct.py are not in the task's
suggested file list but are the actual implementations of this document's §1 and Amendments
3-4; ledger.py alone does not cover the gate or the caged reader, so they are included here for
completeness — the task calls for an exhaustive, committee-grade audit.)*

| item | registered value (doc:line) | code | status | note |
|---|---|---|---|---|
| MATERIAL: max ratio ≥ 1.2 and n≥8 | CLAIM_LEDGER_REGISTRATION.md:13 | `MATERIAL_RATIO=1.2`, `MIN_N=8` (materiality.py:15,17) | MATCH | |
| IN LINE: 0.8 ≤ max ratio < 1.2 | CLAIM_LEDGER_REGISTRATION.md:14 | `INLINE_RATIO=0.8` (materiality.py:16) | MATCH | |
| NOISE: ratio<0.8, or no class | CLAIM_LEDGER_REGISTRATION.md:15 | materiality.py:82-85 (`else: sig="NOISE"`), :55-57 (no etype) | MATCH | |
| **Thin (n<8): "IN LINE... never MATERIAL"** | CLAIM_LEDGER_REGISTRATION.md:16 | materiality.py:70-73: `sig = "IN_LINE" if ratio>=INLINE_RATIO else "NOISE"` | **DEVIATION** | can emit NOISE for a thin class with ratio<0.8; registration reads as unconditional IN LINE. See F-5. |
| **policy_response endogenous: "capped at IN LINE... regardless of its ratio"** | CLAIM_LEDGER_REGISTRATION.md:17-18 | materiality.py:65-69: same conditional pattern | **DEVIATION** | "regardless of its ratio" is the strongest wording in the document against a ratio-conditional branch; code has one anyway. See F-5. |
| LOUD/QUIET: attention top 20% (GPR pctile ≥80 or wiki ≥2×median) | CLAIM_LEDGER_REGISTRATION.md:19-21 | `LOUD_PCT=80` (materiality.py:20), used `flags_for()` :112 | MATCH for the GPR half; the wiki 2×-median half is not implemented in materiality.py — it only reads a precomputed `flag=="spike"` from `data/wiki_attention.json` (materiality.py:92-106), a file whose generator is outside the audited file set | UNVERIFIED (out of scope) for the wiki half |
| QUIET/LOUD: bottom 40% (GPR pctile ≤40) | CLAIM_LEDGER_REGISTRATION.md:21-23 | `QUIET_PCT=40` (materiality.py:21), :114 | MATCH | |
| §2 checkable = asset + direction/level + horizon; defaults +20td price / +90cd escalation | CLAIM_LEDGER_REGISTRATION.md:27-31 | `PRICE_HORIZON_TD=20`, `ESCALATION_HORIZON_CD=90` (ledger.py:35-36); `type_claim()` ledger.py:76-107 | MATCH | |
| §2 claim types: direction/level/flow/escalation/policy | CLAIM_LEDGER_REGISTRATION.md:32-33 | `type_claim()` kinds: escalation/flow/level/direction/policy/uncheckable (ledger.py:84-107) | MATCH | |
| §2 hypotheticals: modality=hypothetical, "resolve only if the antecedent event enters the corpus" | CLAIM_LEDGER_REGISTRATION.md:34-36 | `resolve()` **permanently skips** any claim with `modality=="hypothetical"` (ledger.py:263) — no code path anywhere re-checks a hypothetical claim once a matching event enters the corpus (`grep -rn hypothetical src/*.py` shows only classification, never conditional resolution) | **UNIMPLEMENTED** | see F-8: hypothetical claims are logged and displayed "if it occurs," but the registered conditional-resolution mechanism does not exist; they can never resolve. |
| §3 verdict cutoffs SUPPORTED r≥0.60&n≥8 / MIXED 0.40<r<0.60 / UNSUPPORTED r≤0.40 / THIN n<8 | CLAIM_LEDGER_REGISTRATION.md:42-44 | `SUPPORTED=0.60, MIXED=0.40, UNSUPPORTED=0.40, MIN_N=8`; `_cut()` (ledger.py:33-34,149-156) | MATCH | |
| §3 level claims: r = share reaching implied % distance | CLAIM_LEDGER_REGISTRATION.md:45-46 | `verdict_for()` kind=="level" (ledger.py:184-190) using `max_pct`/`min_pct` (path extrema) | MATCH (reasonable reading of "reached") | |
| §3 escalation claims: r over conditioned subset, LIMITED_RETALIATION+WIDENING | CLAIM_LEDGER_REGISTRATION.md:47-49 | `verdict_for()` kind=="escalation" (ledger.py:167-176): `r=rates[LIMITED_RETALIATION]+rates[WIDENING]` | MATCH | |
| **§3 flow claims: "r = ... the realized-disruption fraction from `propagate.py`"** | CLAIM_LEDGER_REGISTRATION.md:50-52 | `verdict_for()` kind=="flow" (ledger.py:191-192) and `resolve()` (ledger.py:280): `abs(o["chg_pct"]) >= 10` computed **directly in `ledger.py`** from raw price % change; `ledger.py` never imports `propagate` (`grep -n propagate src/ledger.py` → no hits) | **DEVIATION** | see F-9: `propagate.py`'s `realized_disruption_fraction` is defined over `car20` (event-study **cumulative abnormal return**, t−5..t+20, net of an estimation-window baseline — `src/inference.py:60-99`), a materially different, more careful statistic than `chg_pct` (raw % change, t→t+20, no baseline adjustment). Only the `10` threshold value is shared (`propagate.py:38 DISRUPTION_MIN=10.0`); the underlying quantity is not. |
| §3 policy claims: checkable only against a dated action, PENDING until corpus | CLAIM_LEDGER_REGISTRATION.md:53-54 | `type_claim()` kind=="policy" → `checkable: False`, "PENDING" (ledger.py:101-104) | MATCH | |
| §4 append-only claims.jsonl, idempotent per (story, sentence) | CLAIM_LEDGER_REGISTRATION.md:57-58 | `log_claims()` (ledger.py:224-246): sha1(story_id|text), skip if seen | MATCH | |
| §4 "nothing edited after written; corrections are new rows" | CLAIM_LEDGER_REGISTRATION.md:66 | `resolve()` only appends to `resolutions.jsonl` (ledger.py:255-300), never rewrites `claims.jsonl` | MATCH | |
| Amendment 1 (display-only, thresholds unchanged): per-side chips, Feed ranks by ratio | CLAIM_LEDGER_REGISTRATION.md:68-77 | not directly checked (frontend/API layer, out of scope files) | not audited | |
| Amendment 2: `no_entity` flag, entity match required to show MATERIAL | CLAIM_LEDGER_REGISTRATION.md:79-86 | superseded by Amendment 3's entity-aware gate (registration text says so itself) | see Amendment 3 row | |
| Amendment 3.1: event class ∈ 7 registered types or null | CLAIM_LEDGER_REGISTRATION.md:96-97 | reader.py cage schema (not line-verified in depth; out of primary scope) | not fully audited | |
| Amendment 3.3: claim quote must be verbatim substring of article text; fabricated quote dropped | CLAIM_LEDGER_REGISTRATION.md:101-103 | `reader.py` — referenced by module docstring ("proposals are cached by content hash"); substring check not traced line-by-line | not fully audited | |
| Amendment 3.3: escalation claim with no actor/target entity ⇒ UNCHECKABLE | CLAIM_LEDGER_REGISTRATION.md:109-110 | `reader.py:397`: `why.append("escalation claim with no actor/target entity in the story"); kind="uncheckable"` | MATCH | |
| Amendment 3.6: fallback labelled `regex_fallback`, never presented as a model read | CLAIM_LEDGER_REGISTRATION.md:123-126 | `reader.py` uses `mode="regex_fallback"` consistently (lines 221, 292, 309, 313, 316, 517, 556, 573) | MATCH | |
| Amendment 4.1: condition fields = actor, target, conflict_scope, tempo, alliance, diplomatic, target_capacity; refused values logged, nothing runs | CLAIM_LEDGER_REGISTRATION.md:139-142 | `challenge.py:38` `FIELDS=(...)` exact 7-tuple match; `challenge.py:170-175` `status="REFUSED"`, appended before short-circuit | MATCH | |
| Amendment 4.2: same engine, RETRIEVE_MIN 0.40, COND_SIM 0.50, COND_MIN_N 8 | CLAIM_LEDGER_REGISTRATION.md:144-146 | `src/escalation.py:26-28`: `RETRIEVE_MIN=0.40, COND_SIM=0.50, COND_MIN_N=8`; `challenge.py:213` echoes them into every response | MATCH (exact) | |
| Amendment 4.3: NO PRECEDENT vs THIN(n<8) states | CLAIM_LEDGER_REGISTRATION.md:147-150 | `challenge.py:188-190` | MATCH | |
| Amendment 4.5: `field_uncoded` flag | CLAIM_LEDGER_REGISTRATION.md:155-158 | `challenge.py:185` | MATCH | |
| Amendment 4.6: append-only `challenges.jsonl`, refused ones included | CLAIM_LEDGER_REGISTRATION.md:159-161 | `challenge.py:31 CHALLENGES = LEDGER_DIR / "challenges.jsonl"`; refused rows appended (:172) | MATCH | |

---

## 4. OUTCOME_MAPPING.md vs `src/state/outcomes.py`, `src/state/ies90.py` (committed)

*(`src/state/icb.py`, `src/state/cow_mid.py`, `src/state/ucdp.py` — named in the task's suggested
file list — turn out to implement WORLD_STATE panel fields (`icb_crisis_count`,
`mid_count_10y`, `ucdp_active_conflicts`, etc., i.e. WS-D03..D09/WS-S01..S03), a different feature
pipeline than OUTCOME_MAPPING.md. The matching/branch-mapping rules audited here live in
`outcomes.py`'s and `ies90.py`'s own `load_icb`/`load_mid`/`load_ucdp`/`load_midi`/`load_war`
loaders, which are separate code from those three state-panel files. Noted so the committee does
not read this as a skipped location — it is a scoping correction, not a gap.)*

| item | registered value (doc:line) | code | status | note |
|---|---|---|---|---|
| §2 ICB match: d ∈ [trigdate−30d, termdate]; tie-break latest trigdate≤d+30d else nearest | OUTCOME_MAPPING.md:22-24 | `outcomes.py:161` (`c.trigdate - 30d <= d <= c.termdate`), :168-169 (tie-break) | MATCH | |
| §2 MID match: dyad in P (or both states in A), d ∈ [start−30d, end+90d]; prefer nearest start | OUTCOME_MAPPING.md:27-29 | `outcomes.py:186` (`start-30d <= d <= end+90d`) | MATCH | |
| §2 UCDP: year(d) and year(d)+1 rows, max intensity, sum bd_best | OUTCOME_MAPPING.md:30-32 | `match_ucdp()` outcomes.py:201-212 | MATCH | |
| §3 ICB table (forout∈{1,2}&viol≤2→DEAL; viol=4→WIDENING; viol=3→WIDENING if outesr=1 else LIMITED_RETALIATION; viol=2→LIMITED_RETALIATION; viol=1→CONTAINED) | OUTCOME_MAPPING.md:40-45 | `map_icb()` outcomes.py:54-66 | MATCH (line-for-line) | |
| §3 MID table (hihost=5→WIDENING; hihost=4&fatlev≥3→WIDENING; hihost=4→LIMITED_RETALIATION; hihost∈{2,3}&settlmnt=1→DEAL; hihost∈{1,2,3}→CONTAINED) | OUTCOME_MAPPING.md:50-54 | `map_mid()` outcomes.py:69-79 | MATCH (line-for-line) | |
| §3 UCDP table (i1=2&i0<2→WIDENING; i1=2&i0=2→LIMITED_RETALIATION; i1=1→LIMITED_RETALIATION; i1=0→CONTAINED) | OUTCOME_MAPPING.md:59-63 | `map_ucdp()` outcomes.py:82-88 | MATCH | |
| §4 precedence ICB>MID>UCDP; per-source labels all stored | OUTCOME_MAPPING.md:68-71 | `outcomes.py:265-267` (`per`, `prec`) | MATCH | |
| §5 κ; decision rule κ<0.6 ⇒ replace | OUTCOME_MAPPING.md:74-78 | computed as `data/state/outcomes_kappa.json` (superseded — see Amendment 1) | MATCH (superseded per registration's own text) | |
| §6 audit sheet 60 disagreements, stratified, seed | OUTCOME_MAPPING.md:80-85 | `outcomes.py:33 SEED=20260902` and downstream audit writer | MATCH | |
| **A1.1 what the record shows**: κ figures (−0.001 ICB n43, −0.234 MID n15, 0.104 UCDP n184, 0.061 precedence n184, 114 disagreements, 60 in sheet) | OUTCOME_MAPPING.md:96-97 | `data/state/outcomes_kappa.json` (not re-verified numerically in this pass — would require re-running the κ computation; treated as the historical record per the amendment's own framing) | not independently recomputed | out of the code-vs-doc scope of this task; flagged only if the committee wants it separately re-derived |
| A1.2 IES-90 window W=(d,d+90] | OUTCOME_MAPPING.md:115 | `WINDOW=90`, `window(d)` (ies90.py:29,80-83) | MATCH | |
| A1.2 level table (0 none/1 threat/2 force/3 war) | OUTCOME_MAPPING.md:119-126 | `LEVEL_MEANING` (ies90.py:38) | MATCH | |
| A1.2 MIDI hostlev→level (1→0,2→1,3→1,4→2,5→3) | OUTCOME_MAPPING.md:136 | `HOSTLEV_TO_LEVEL` (ies90.py:36) | MATCH | |
| A1.2 GED thresholds D≥250→3, 25≤D<250→2, D<25→0 (1000×90/365=246.6→250) | OUTCOME_MAPPING.md:140 | `GED_WAR=250, GED_FORCE=25`; comment reproduces the 246.6→250 derivation (ies90.py:37) | MATCH | 246.6 verified in python: `1000*90/365=246.575...` ≈246.6, matches doc |
| A1.2 coverage periods (MIDI 1993-2014, ICB 1918-2021, MID —, GED 1989-2025) | OUTCOME_MAPPING.md:136-140 | `COVER` dict (ies90.py:34) | MATCH (MID lower bound 1816 sourced from Amendment 1.1's coverage summary, not the A1.2 table itself — see next row) | |
| A1.2 precedence tie order MIDI,ICB,MID,GED | OUTCOME_MAPPING.md:148-149 (superseded, see A1.1) | `SOURCES=("midi","war","icb","mid","ged")` (ies90.py:32) reflects the **A1.1** tie order (MIDI, war, ICB, MID, GED), not the pre-1.1 order | MATCH (via amendment) | |
| A1.1.1 COW War v4 loaded; inter-state pair/opposite-side, intra-state via L; level 3 | OUTCOME_MAPPING.md:185-190 | `score_war()` ies90.py:243-267 | MATCH | |
| A1.1.2 ICB dates only what it can date (wholly-in-W→peak; onset-in-W→1; ongoing→none) | OUTCOME_MAPPING.md:191-195 | `score_icb()` (not fully quoted above but consistent with `score_mid()`'s identical pattern, ies90.py) | MATCH by inspection of the analogous, more fully quoted `score_mid()` | |
| A1.1.3 Dyadic MID same pattern; de-duplicated to one row per (dispute,dyad), max hihost, last year's settlmnt/end | OUTCOME_MAPPING.md:196-200 | `dedupe_mid()` ies90.py:136-146; `score_mid()` ies90.py:271-296 | MATCH | |
| A2.1 dyadic precedence: dyadic-capable source + P non-empty ⇒ level from dyadic records only; else location | OUTCOME_MAPPING.md:221-227 | `score_event()` ies90.py:377-393 (`dy_cov`, `basis`) | MATCH | |
| A2.2 littoral map (10 chokepoints → L only) | OUTCOME_MAPPING.md:238-248 | `LITTORAL` dict ies90.py:41-51 — **all 10 entries compared programmatically, exact match** (hormuz/bab_el_mandeb/suez/suez_canal/gibraltar_strait/malacca/taiwan_strait/libya_es_sider/kirkuk_ceyhan_pipeline/druzhba_pipeline/cpc_novorossiysk, with the same "unmapped" states omitted) | MATCH (exact, python-diffed) | |
| A2.3 rule_fired identifiers, UNCOVERED, tie order | OUTCOME_MAPPING.md:253-259 | `score_event()` ies90.py:396-401, `"NONE.covered"`/`"UNCOVERED"` literals present | MATCH | |
| A1.3/A2.3 audit sheet: 30 events, level×decade, largest remainder, seed 20260902 | OUTCOME_MAPPING.md:166-169, 259 | `audit_pick(n=30, seed=SEED)` ies90.py:508-509, docstring "largest remainder" ies90.py:509 | MATCH | |

**Test coverage:** `tests/state/test_ies90.py` (8 tests, `test_i1`..`test_i8b`) covers totality/
dating/precedence/dyadic-precedence/littoral-map/coverage/distribution-consistency/audit-sheet
shape on synthetic data — this is the strongest-tested registered document in the repo. No
requirement-ID naming convention (`REQ-…`) is used, only informal `i1`-`i8b` labels tied to the
document's own subsection numbers — a minor deviation from CLAUDE.md's "test names must contain
the requirement ID they cover," not a numeric finding, noted for completeness.

**Overall:** OUTCOME_MAPPING.md is, by a wide margin, the best-matched document in this audit —
extensive, exact, line-level correspondence between the registered rules and the code, including
a fully-diffed exact match on the 10-entry littoral map. No FINDING is raised against this
document's core scoring logic.

---

## 5. data/candidates/REGISTRATION.md vs code

| item | registered value (doc:line) | code | status | note |
|---|---|---|---|---|
| Registered state set (COW ccodes, 53 states across producers/transit/consumers) | data/candidates/REGISTRATION.md:24-34 | `STATE_SET` in `src/dossier.py:37-39` | MATCH (exact — python set-diff of the registered 53 codes against `STATE_SET` returns empty on both sides) | this is the **only** piece of this document implemented anywhere |
| Sources: ICB (trigdate), COW War v4 (earliest participant start), Dyadic MID hihost≥4 (earliest dyad start) | data/candidates/REGISTRATION.md:15-19 | **no code** builds this candidate list — `grep -rln "pre1987_candidates" src/*.py` finds only `src/dossier.py`, which *consumes* `data/candidates/pre1987_candidates.csv` as an input ("session B's sheet when it lands") — the file does not exist (`data/candidates/` has no `pre1987_candidates.csv` or `_summary.json`) | **UNIMPLEMENTED** | |
| Join to monthly Big Moves (`inside_big_move`, `episode_id`, `monthly_move_pct`, `wti_chg_3m_pct`) | data/candidates/REGISTRATION.md:37-43 | no code | **UNIMPLEMENTED** | |
| Output columns / files (`pre1987_candidates.csv`, `_summary.json`) | data/candidates/REGISTRATION.md:45-49 | absent | **UNIMPLEMENTED** | |

This document's entire stated deliverable — the pre-1987 candidate sheet that the monthly tier's
own limitation note depends on ("It cannot describe, let alone validate, without pre-1987
events") — does not exist in code, beyond one incidentally-reused constant.

---

## 6. `data/walk_forward/menu.json` (registered Hedge menu, committed = HEAD) vs code

Committed `menu.json` has **12** items (M01–M12); this matches WALK_FORWARD_PROTOCOL.md §5's
"≤ 12" cap **as it stood at HEAD** (before Amendment C raised the cap to ≤13, which is registered
but has no committed code — correct per Amendment C's own "registered first, computed after"
rule). Field-by-field:

| item | registered (menu.json, committed) | protocol requirement | status |
|---|---|---|---|
| `"registered": "2026-09-02"` | header field | WALK_FORWARD_PROTOCOL.md §5: "a finite, registered menu... written before the run" | MATCH — `menu.json` committed `c4335ef` 11:19:41, before `walk.py`'s first run-producing commit `c2443a0` 12:37:55 |
| 12 items, ≤12 cap | menu.json items[] | WALK_FORWARD_PROTOCOL.md:83 "≤ 12" | MATCH |
| block_weights uniform within a block (not adjustable) | every item's weights are 0/1/2 integers, uniform within a block | menu.json header: `"field_weights": "uniform within a block (registered; not adjustable)"` | MATCH (self-consistent; not independently re-derived against `similarity.py`'s implementation in this pass) |
| retrieve_min values used: 0.30 (M08), 0.40 (all others), 0.50 (M09) | menu.json | WALK_FORWARD_PROTOCOL §5 registers *that* the retrieval threshold is adjustable via the menu, not specific values — the values themselves are only ever stated in menu.json | MATCH (menu.json is itself the registration for these numbers, and it predates the walk run) |
| k values used: 5 (M06), 8 (default), 12 (M07, M10) | menu.json | same | MATCH |
| M01 = frozen-engine baseline (uniform weights, never updated) | menu.json M01_uniform_k8 | WALK_FORWARD_PROTOCOL §4 baseline 4 | MATCH — `menu.json` header states this explicitly and `walk.py`'s `frozen` mixture (committed, uses `np.full(N, 1/N)`) matches |

No deviation found for the menu itself — it is well-formed and its own contents are the true
"pre-declared" source for the k/retrieve_min values used elsewhere (the one place in this audit
where "registered" and "used in code" trace back to the same, separately-dated document).

---

## 7. Unregistered magic constants (no registration anywhere, found by inspection/grep)

| constant | file:line | comment/purpose | registered? |
|---|---|---|---|
| `LN.ETA = 0.25` | src/engine/learning.py:21 | Hedge learning rate | No — see §1 |
| `g_scale=2.0, p_scale=30.0` | src/walk.py:68-69 | Hedge loss normalizers | No |
| `random_draws=25` | src/walk.py:71 | baseline-3 draw count | No |
| `n_boot=2000, n_spa_boot=1000, n_perm=1000` (n_perm only is registered) | src/walk.py:72 | bootstrap/SPA/permutation replication counts | Partial (n_perm only) |
| `k_max=12` | src/walk.py:65 | analogs kept per item | No (derivable from menu.json, not itself stated) |
| `placebo_reps=5, placebo_excl_days=30` | src/walk.py:75 | placebo mechanics | No |
| `pit_bins=10, reliability_bins=5` | src/walk.py:78 | diagnostic bin counts | No |
| spec-curve ranges (5 dimensions) | src/walk.py:76-77 | robustness sweep | No (k range only, derivable from menu.json) |
| `CLUSTER_DAYS=90` (daily) | src/big_moves.py:33,40 | episode clustering window | **Contradicts** the registered value (60 trading days) — see F-3 |
| `MERGE_DAYS=60` (daily) | src/big_moves.py:33,41 | same-sign episode merge | No basis for the daily tier at all — see F-3 |

---

## FINDINGS (ranked by severity)

**F-1 (HIGH) — Two base registrations, and one amendment, were committed in the same commit as
their implementing code, so "registered before computed" cannot be verified from the record for
them.**
`BIG_MOVES_REGISTRATION.md` (+ Amendments 1, 2) and `src/big_moves.py` both landed in `594d2fa`
(2026-09-02 00:12:55). `CLAIM_LEDGER_REGISTRATION.md` §1-4 (+ Amendments 1, 2) and
`src/materiality.py`/`src/ledger.py` also landed in `594d2fa`. `BIG_MOVES_REGISTRATION.md`
Amendment 3 and its `big_moves.py` code landed together in `0abcc39`. Git — the only mechanism
this repo uses to prove "before" — cannot distinguish "registered, then implemented, then
committed together" from "implemented, then written up as if it had been registered first, then
committed together." Every *later* amendment across all four documents (BIG_MOVES 3 already
counted above; CLAIM_LEDGER 3/4; OUTCOME_MAPPING 1/1.1/2; WALK_FORWARD B/C/D) does show a clean
registration-commit-before-code-commit gap, often by minutes to hours — so the discipline is
real and demonstrated everywhere it *can* be demonstrated. The exception is exactly the two
documents whose numbers most directly drive the flagship "What it found" paragraph.
**At risk:** README.md:8-9 — "every threshold was registered before it was computed" — is not
falsified, but for the base Big Moves and Claim Ledger rules it is also not verifiable, which a
"committee reads this" audit should not wave through as verified.

**F-2 (HIGH) — Most of the walk's own numeric machinery is not in WALK_FORWARD_PROTOCOL.md at
any point, including the amendments; it exists only in `walk.py`'s `REGISTERED` dict, committed
simultaneously with the code that reads it.**
`eta`, `g_scale`, `p_scale`, `random_draws`, `n_boot`, `n_spa_boot`, `k_max`, `placebo_reps`,
`placebo_excl_days`, `pit_bins`, `reliability_bins`, and all five specification-curve ranges
(`burn_in`, `k`, `horizon_daily`, `cluster_days`, `big_move_q`) are absent from
`WALK_FORWARD_PROTOCOL.md`'s text (confirmed by grep across the full document, all sections and
amendments). The document explicitly promises, for the specification curve, that thresholds are
"varied across its pre-declared range" (§6) — the range is never declared. `summary.json`'s
`registered` block matches `walk.py`'s dict exactly, but that is because `summary.json` is
generated *from* that dict, not because it was checked against an independent source.
**At risk:** README.md:56-67, the entire "On prediction" paragraph — Diebold-Mariano CIs, SPA
p-values, the 162-setting specification curve, and the permutation p-value all depend on these
constants. README.md:9's "every threshold was registered before it was computed" is the specific
sentence this finding weighs against; the walk's own thresholds mostly were not, in the sense the
sentence's own surrounding language (a *document*, dated, disclosed) implies.

**F-3 (HIGH) — Big Moves' clustering and merge rule silently diverged from the registered value
on day one, and the divergence has never been disclosed as an amendment; the "43 episodes"
headline number is a direct product of it.**
BIG_MOVES_REGISTRATION.md's undamended text (item 3) registers a 60-**trading-day** clustering
rule. `src/big_moves.py` has used `CLUSTER_DAYS=90` (**calendar** days, per the `.days`
arithmetic on `pd.Timestamp` diffs) since the very first commit (`594d2fa`), and additionally
merges same-sign clusters within `MERGE_DAYS=60` days — a mechanism the base document and
Amendments 1-2 never mention at all (it first appears, and only for the *monthly* tier, in
Amendment 3, four commits later). The code's own module docstring claims "this module implements
Amendment 2 exactly," which is not accurate for the daily-tier clustering/merge parameters.
No test exercises either constant's specific value. **At risk:** README.md:49-54 — "35% of the
market's largest moves have no identifiable event," "43 episodes," and the crude-vs-diesel-crack
ratio claims are all downstream of this undisclosed rule change; a run against the literally
registered 60-trading-day/no-merge rule has never been published for comparison.

**F-4 (MEDIUM, thin evidence — disclosed as such) — "the market's extreme preceded the catalyst
in a third of the rest" could not be reproduced from the published Big Moves data.**
Four plausible readings of "anticipated," computed in python against `data/big_moves/brent.json`
and (pooled) the other two daily assets, gave 50.0%, 71.4%, 50.0%, and 37.1% — none is "a third"
(33.3%), and the closest (37.1%) requires pooling brent+wti+diesel_crack, which contradicts the
sentence's own explicit Brent-only scope. This is not a claim that the number is wrong — it is a
claim that I could not verify it from the artifacts and code this audit had access to, and the
committee should ask for the exact query. **At risk:** README.md:50-51.

**F-5 (MEDIUM) — The materiality gate's two "capped" branches (thin classes, `policy_response`)
can still emit NOISE, contradicting the registration's plain-reading "unconditional cap"
language, and the contradicting branch is untested.**
CLAIM_LEDGER_REGISTRATION.md:16 ("Thin classes... are IN LINE... never MATERIAL") and :17-18
("`policy_response`... capped at IN LINE... regardless of its ratio") both read as unconditional
assignments. `src/materiality.py:66,71` implement both as `"IN_LINE" if ratio>=INLINE_RATIO else
"NOISE"` — i.e., a thin or endogenous class with ratio<0.8 shows NOISE. Neither test in
`test_v2_gate_ledger.py` exercises a ratio below 0.8 for either branch. No amendment revisits this
rule. **At risk:** the "materiality gate" description in README's "What it is" bullet (line 27:
"analog retrieval with a registered threshold") and any story shown with a low-ratio thin or
policy_response class would display a stronger-sounding NOISE chip than the registration
promises.

**F-6 (MEDIUM) — WALK_FORWARD_PROTOCOL.md Amendment D (the sealed-run archive) is registered but
has never been implemented, in any commit, and there is no uncommitted code for it either
(unlike Amendment C, which at least has uncommitted code in flight).**
Amendment D (WALK_FORWARD_PROTOCOL.md:219-226) describes moving completed runs' `reads.jsonl` /
`scores.jsonl` / `weights.jsonl` to `data/walk_forward/runs/<run_id>/*.gz` and publishing
`summary.json.data_state.archived_runs`. `grep -rn "archived_runs\|runs/<run_id>\|def archive"
src/*.py` (and the working tree) finds nothing; `data/walk_forward/runs/` does not exist. This is
disclosed as registered-not-yet-computed by its own header, so it is not a violation of the
"registered before computed" rule — but it is worth flagging because the append-only claim in
WALK_FORWARD_PROTOCOL §2 ("The file is append-only") is only true today because there is exactly
one run in the tree; Amendment D exists specifically because that stops being true at the second
run, and the second run has apparently already happened (the tree shows only one `run_id` in
`summary.json`, `walk_20260902T182828Z`, but `reads.jsonl` would grow unboundedly without
Amendment D once re-runs resume). Worth a status check before the next `python3 src/walk.py`.

**F-7 (MEDIUM) — data/candidates/REGISTRATION.md's entire stated deliverable (the pre-1987
candidate sheet) is unimplemented; only one incidental constant (the state set) made it into
code, for an unrelated tool.**
No code builds `pre1987_candidates.csv` or `_summary.json`; the ICB/COW-War/MID loader, the
"at least one actor in the state set" filter, and the join to `wti_monthly` big moves described in
the document do not exist anywhere. `src/dossier.py` (a later-stage admission-dossier writer,
Brief A-6, unrelated in purpose) happens to reuse the same 53-code state set — verified an
**exact** match against the registered list by python set-diff — but `dossier.py` itself expects
`pre1987_candidates.csv` as an input file that does not exist ("session B's sheet when it
lands"). The monthly tier's own stated limitation (WALK_FORWARD_PROTOCOL.md §9: "n ≈ 14 monthly-
tier events... can describe, not validate") is exactly the problem this unbuilt sheet exists to
address.

**F-8 (LOW-MEDIUM) — Hypothetical claims are logged and typed as registered, but the registered
conditional-resolution mechanism for them does not exist; they can never resolve.**
CLAIM_LEDGER_REGISTRATION.md:34-36: hypotheticals "resolve only if the antecedent event enters
the corpus." `src/ledger.py:263`'s `resolve()` unconditionally skips every claim with
`modality=="hypothetical"`, permanently. No other code path re-evaluates a hypothetical claim
against newly-entered corpus events. This under-builds rather than over-claims (a hypothetical
claim is never wrongly marked true or false — it simply never resolves), so it is lower severity
than F-3/F-5, but it means the registered "if it occurs" mechanism is currently vaporware.

**F-9 (LOW-MEDIUM) — Flow-claim verdicts cite `propagate.py`'s realized-disruption fraction but
are computed from a different, simpler statistic that only shares the numeric threshold.**
CLAIM_LEDGER_REGISTRATION.md:50-52 names `propagate.py`'s realized-disruption fraction (defined
over `car20`, an event-study cumulative abnormal return net of an estimation-window baseline,
`src/inference.py:60-99`, `propagate.py:38 DISRUPTION_MIN=10.0`) as the source of the flow-claim
statistic. `src/ledger.py` never imports `propagate`; both `verdict_for()` (line 192) and
`resolve()` (line 280) compute `abs(chg_pct)>=10` directly from `class_outcomes()`'s raw,
non-abnormal % price change. Only the `10` threshold is shared; the underlying quantity (raw
change vs. abnormal/excess return) is not what is named in the registration.

**F-10 (LOW, documentation hygiene) — WALK_FORWARD_PROTOCOL.md's amendments are lettered B, C, D
with no "Amendment A."** The task brief that generated this audit assumed "Amendments A-D" exist;
they do not — only B, C, D are present (`grep -n "^## Amendment"` confirms). Their corresponding
Briefs are B-1 (→Amendment B), B-2 (→Amendment C), and B-4 (→Amendment D); Brief B-3 corresponds
to `data/candidates/REGISTRATION.md`, a different document entirely, and there is no
`Amendment A`. Not a code deviation; flagged only so the committee does not read this as an
omission in the audit rather than a fact about the document.

---

## What was NOT re-verified in this pass (explicitly out of scope / budget)

- OUTCOME_MAPPING.md Amendment 1.1's reported κ figures (−0.001 / −0.234 / 0.104 / 0.061) were
  not recomputed from `data/state/outcomes_kappa.json` against a hand-built confusion table —
  treated as historical record per the amendment's own framing ("What the record shows").
- CLAIM_LEDGER Amendment 3 rules 1, 4 (event-class enum enforcement; title extraction) and the
  verbatim-substring fabrication check (rule 3) were located in `reader.py` but not traced
  line-by-line to full certainty — `reader.py` is outside the task's suggested file list and was
  audited at reduced depth relative to `big_moves.py`/`ledger.py`/`ies90.py`/`outcomes.py`/
  `walk.py`.
- `src/engine/similarity.py`, `src/engine/scoring.py`'s exact mathematical formulas (CRPS,
  Murphy decomposition identity, pinball loss) were confirmed present and correctly labelled
  registered-vs-diagnostic by their own docstrings, but not independently re-derived
  formula-by-formula against the cited literature (Gneiting & Raftery 2007, Murphy 1973).
- `src/state/icb.py`, `src/state/cow_mid.py`, `src/state/ucdp.py` were confirmed to be a
  *different* pipeline (WORLD_STATE panel features) from OUTCOME_MAPPING.md's matching logic and
  were not further audited against OUTCOME_MAPPING.md, since they do not implement it.
