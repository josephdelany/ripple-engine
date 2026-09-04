> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Adversarial review findings, kept as evidence. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# D-2 Leakage Hunt — ripple-engine, branch v2-day1, HEAD b7c8ec1

Read-only audit. Working tree was dirty in `src/engine/read.py`, `scoring.py`,
`similarity.py`, `src/walk.py`, `tests/conftest.py` (another session mid-edit,
confirmed live during this audit — I observed its pytest processes and a live
edit to `tests/test_walk_recalibration.py` running in the real repo directory
while I worked). All findings below are against the **committed** code via
`git show HEAD:<path>`, from a scratch clone at `b7c8ec1`. Files actually read
at HEAD: `src/engine/read.py`, `src/engine/similarity.py`, `src/engine/scoring.py`
(header only), `src/walk.py`, `src/engine/learning.py`, `src/engine/persistence.py`
(referenced), `src/big_moves.py`, `src/derive_signals.py`, `src/fetch_cot.py`,
`src/fetch_eia.py`, `src/fetch_fred_alfred.py`, `src/admission_rule.py`,
`src/state/panel.py`, `src/state/situation_state.py`, `src/state/polity.py`,
`src/state/cow_nmc.py`, `src/state/ies90.py`, `data/candidates/REGISTRATION.md`,
`WALK_FORWARD_PROTOCOL.md`, `SESSION_CHARTER.md`, `README.md`,
`data/walk_forward/summary.json`, and `data/oil.db` (read-only SQL). The
untracked `src/engine/recalibrate.py` and `tests/test_walk_recalibration.py`
(Amendment C / M13) were read but are **not yet in the published run**
(`summary.json.menu` has 12 items, not 13) — noted, not scored below.

---

## Ranked table

| # | Path | Severity | Evidence | Verdict could change? |
|---|------|----------|----------|------------------------|
| 1 | **(g) Corpus admission sheet joins the outcome before Joe decides** | **CRITICAL** | `data/candidates/REGISTRATION.md:34-47`: the pre-1987 monthly-tier candidate sheet Joe reviews carries `inside_big_move`, `episode_id`, `monthly_move_pct`, `wti_chg_3m_pct` — the P outcome the walk would score — **as columns on the admission sheet**, "so Joe sees the outcome the walk would score whether or not the record sits in a Big Move." This is selection-on-outcome built into the registered process, not a code bug. | **Yes, for the monthly tier only**, prospectively. Doesn't touch the current daily-tier null (README's headline numbers are daily-tier only; monthly tier is 14 events, explicitly "can describe, not validate"). But it means any *future* monthly-tier skill or materiality claim built from this admission process is contaminated by construction — the corpus would be selected toward (or away from) big moves by a human who can see the outcome first. Direction: inflates apparent skill/materiality precision for whichever way Joe's judgment leans. |
| 2 | **(a) Materiality READ uses a full-history quantile as a feature, not just a label** | **MAJOR** | `src/big_moves.py:39,68`: `TOP_Q=0.95`, `thr = r.abs().quantile(TOP_Q)` computed once over the **entire 1987–2026 (or 1946–2026) series**, never re-run per `as_of`. `src/engine/read.py:159-165` (`in_big_move`) and `:325-332` (`m_read`) use this static, full-sample-derived episode list to flag **each analog** in the pool, and that flag feeds the read's own MATERIAL/NOT_MATERIAL call (`m_read`, called at read time, not just at scoring time). `src/walk.py:334` also uses the same `in_big_move` as the scoring "truth." The spec curve (`walk.py:768-769`) only varies the quantile (0.90/0.95/0.975); it never re-derives the threshold from data available at `as_of`. | Doesn't flip the README's G/P nulls (M isn't headlined). But it does mean every M call sealed in every read — and the persisted `tiers.daily.M.engine` precision/recall block in `summary.json` — is computed with a threshold informed by 2020–2026 volatility even for a read in 1990. Because the engine still shows no skill on G/P despite this unfair advantage embedded in a correlated feature, this makes the *null* more credible, not less — but the M numbers themselves are not point-in-time and the protocol's own §1 filtration promise doesn't cover this path at all. |
| 3 | **(i) Two similarity-feature series carry no release lag** | **MAJOR** | Executed check on `data/oil.db`: `derived.cot_pct` and `derived.inv_sigma` (and every other `derived.*` series) have `as_of == obs_date` for 100% of rows (14,993–7,030 rows each; see console output below). `src/fetch_cot.py:107` stores `as_of = Report_Date_as_YYYY-MM-DD` (CFTC's *positions-as-of-Tuesday* date), not the Friday release date (~3-day real lag). `src/fetch_eia.py:118` stores `as_of = obs_date` (week-ending Friday), asserting in a comment that this "IS the point-in-time the number refers to" — but EIA's Weekly Petroleum Status Report is released the **following Wednesday** (~4-5 day real lag), not on the Friday it describes. `gpr.GPRD`, by contrast, correctly has `as_of > obs_date` for all 15,219 rows — so the pipeline *can* do this correctly, and doesn't for these two. This directly contradicts protocol §1: "macro series use ALFRED vintages where they exist, otherwise the release lag is applied" — no lag is applied here. | Doesn't flip the daily-tier G/P null by itself (both features enter `similarity.py`'s market block alongside VIX etc., diluted across ~13 fields). Direction: **inflates** apparent skill for any read landing Wed–Fri of a COT week or the ~4 days after an EIA Friday reading, because the engine "sees" positioning/inventory data before it was actually public. Since skill is still null, this understates how much *worse* a truly point-in-time engine would do, i.e. makes the published null conservative rather than suspect — but it is a live, uncorrected violation of the engine's own stated filtration rule and would matter more once M13/recalibration or a positive-skill claim is built on these features. |
| 4 | **(b)/(d) `sr_*` situation fields carry no vintage at all** | **MAJOR** | `src/engine/similarity.py:88-90` (`SR_MAP`) and `:244-246` (`state_vector`): `actor`, `target`, `conflict_scope`, `tempo`, `prior_dyad`, `asset_role`, `propensity` are read straight off the `events` table with **no `as_of` check whatsoever** — contrast with `apply_panel()` (`similarity.py:203-220`), which correctly enforces `vintage <= as_of` for the 35 `situation_state` panel fields (verified: `state_panel`/`situation_state` in `data/oil.db` do carry real, mostly-non-event-date vintages, e.g. 8,239/8,564 rows have `vintage != event_date`). The `sr_*` columns have no such column to check against — they are static, coded once at corpus-admission time, and `tempo`/`conflict_scope` in particular describe how a crisis *unfolded*, which is knowable in full only after the fact. This is exactly protocol §1's stated LIMITATION ("situation fields are not vintage-stamped... fields whose source postdates t are set to unknown"), but the "set to unknown" mitigation is **not implemented** for `sr_*` — only for panel rows that have a vintage to compare. `sr_outcome_90` itself is correctly retired and unused (confirmed by grep: no reference in `engine/read.py`, `similarity.py`, or `walk.py` scoring paths). | Same both-sides argument as #2/#3: these fields feed the *analog retrieval itself* (the "situation" block of the distance metric), for both the target event and every candidate. If coded with hindsight, this inflates the apparent quality of retrieved analogs system-wide across the whole walk, for both the engine and its baselines that use the situation block (M02/M04/M10 in the menu). Since the engine still shows no skill, this again argues the null is conservative — but it means "the analog retrieval used ONLY information available at t" (similarity.py's own docstring, line 15-17) is not true for the `situation` block, and no test in the suite checks it (searched `tests/test_similarity.py`: the vintage test at line 119 is for panel fields only, never for `sr_*`). |
| 5 | (c) Analog pool: unclosed-outcome-window leakage | **none found at HEAD, but the guard is a single unguarded conditional (see deliberate-leak §1 below)** | `src/engine/read.py:184-192` (`Corpus.pool`): strict `event_date < as_of` (string comparison), and admission requires `g_closed_by(...)` (label window closed) or `closed_by(...)` (price window closed) — verified both by reading the code and by `tests/test_read.py:85-113` (`test_step7_filtration_excludes_unclosed_windows_and_break_leaks`), which passes at HEAD. `g_distribution`/`p_distribution` in `read.py` re-filter on the `g_closed`/`p_closed` flags returned by `pool()`. | No — correctly implemented at HEAD. Flagged only because a single-line deletion (§ deliberate-leak experiment below) reintroduces exactly this leakage and only one of ~24 relevant tests notices, and *not* the test the protocol calls "the leakage test." |
| 6 | (h)/(e) IES-90 label sources (ICB/MID/UCDP/COW War) reused, in a strictly-prior window, as the persistence baseline | **MINOR, disclosed** | `WALK_FORWARD_PROTOCOL.md` Amendment B.1: persistence uses `ies90.score_event` on `W⁻=[t-90,t-1]`, "records dated ≤ t−1 enter" only — correctly windowed against *incident date*. But the underlying datasets (ICB v16, UCDP GED 26.1, Dyadic MID 4.03, COW War v4) are themselves compiled/released **decades after** old incidents, in a single modern vintage — Amendment B.1 states this explicitly ("no vintages exist for these datasets — stated here as the same limitation the labels carry"). So persistence for a 1990 read draws on a 2020s-compiled, definitive historical record of 1990, not on what a person actually knew in 1990. | No — this is the *baseline* the engine is compared against, and the README reports the engine **beats** persistence (+0.16, p<0.001). If persistence is stronger than a fair point-in-time persistence would be (compiled-hindsight data usually resolves ambiguous/contested incidents better than 1990s wire reports could), beating it is if anything a *more* robust finding, not a spurious one. Same tables are not reused as G *features* at read time beyond this disclosed baseline (confirmed: `_ies90(conn)` in `read.py` is used only for pool labels/persistence, never merged into `state_vector`). |
| 7 | (j) Spec curve reuse of full-sample quantities | Same root cause as #2 | `walk.py:768-769`: `big_move_q` spec varies `[0.90, 0.95, 0.975]`, each still computed by re-running `big_moves.episodes_for` on the **full series** — no spec arm re-derives the threshold from `as_of`-truncated history. | No new direction beyond #2 — the 83%-negative spec curve (README) is for G/P skill, not M, so unaffected directly. |
| — | (f) Climatology / random-analogs baselines | **none found** | `read.py:325-332` and `walk.py` `_random_g`: climatology and random-analog draws are built from `pool()`'s already-point-in-time-filtered candidate set at each `as_of`, never from the full corpus. Verified by reading the call sites — both baselines run through the same `Corpus.pool` filtration as the engine. | No. |

---

## Deliberate-leak experiment (scratch clone only, real repo untouched)

Clone: `git clone --no-local "/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine" .../scratchpad/leak_clone`, checked out at `b7c8ec1` (confirmed clean, matching HEAD). All tests below are DB-free (`_synthetic()` fixtures in `tests/test_read.py`), so no copy of `data/oil.db` or `data/walk_forward` was needed — confirmed by reading `tests/test_walk.py:1-8` and `tests/test_read.py:18-38`.

**Baseline (unmodified clone):**
```
$ python3 -m pytest -q tests/test_read.py tests/test_walk.py tests/test_walk_baselines.py tests/test_engine.py
.....s..................                                                 [100%]
23 passed, 1 skipped in 116.03s (0:01:56)
```
(1 skip = `test_step7_abqaiq_read_uses_only_analogs_dated_before_it`, needs the real `oil.db`, not copied.)

### Leak 1 — drop the G-window-closed check from the analog pool

`src/engine/read.py`, in `Corpus.pool()`:
```diff
-            g_ok = e["type"] in GEO_TYPES and self.g_closed_by(e["event_id"], as_of) and e["event_id"] in self.ies90
+            g_ok = e["type"] in GEO_TYPES and e["event_id"] in self.ies90  # LEAK-1: dropped g_closed_by(...) check
```
This directly implements item (c): an analog whose 90-day label window has **not** closed at `as_of` now enters the pool with `g_closed=True`, and its (retrospectively fully-known, final) IES-90 label is used in `g_distribution()`'s frequency count for the read.

```
$ python3 -m pytest -q tests/test_read.py tests/test_walk.py tests/test_walk_baselines.py tests/test_engine.py
...F.s..................                                                 [100%]
=================================== FAILURES ===================================
_______ test_step7_filtration_excludes_unclosed_windows_and_break_leaks ________
    ...
>       assert "ev19" not in {a["event_id"] for a in r2["analogs"]}
E       AssertionError: assert 'ev19' not in {'ev00', 'ev01', 'ev02', 'ev03', 'ev04', 'ev05', ...}
tests/test_read.py:98: AssertionError
=========================== short test summary info ============================
FAILED tests/test_read.py::test_step7_filtration_excludes_unclosed_windows_and_break_leaks
1 failed, 22 passed, 1 skipped in 166.34s (0:02:46)
```

**Caught — but only by one narrow unit test, not by the walk's own leakage guard.** `tests/test_walk.py::test_step8_leakage_broken_filtration_must_differ` — the test named in `WALK_FORWARD_PROTOCOL.md` §1 and asserted in `summary.json.leakage_test`  — **passed** with this leak live. Reading `walk.py:891-906` (`leakage_test`) shows why: it only ever compares a **sealed** run against a `break_filtration=True` run (a hardcoded, maximal leak that admits every same-type event regardless of date at all). It has no independent reference for "correct" filtration — it can only detect the presence of a lot of leakage, never confirm the sealed path itself is leak-free. My leak lives entirely inside the "sealed" code path, so both runs it compares still differ hugely from each other (broken admits everything; my leak admits only unclosed-window same-type events) — `reads_differ` stays `True`, `asserted` stays `True`, `verdict` stays `"filtration is binding"`, and the published `summary.json` would look identical on this front.

Reverted cleanly (`git diff --stat` empty afterward).

### Leak 2 — same-day market data visible to standardization and retrieval

`src/engine/similarity.py`, `InfoSet.value_before` and `InfoSet.stats` (used for both the z-score scale and the "last known value" feed into every market-block similarity field):
```diff
-        i = np.searchsorted(idx, np.datetime64(pd.Timestamp(t))) - 1   # last index with date < t
+        i = np.searchsorted(idx, np.datetime64(pd.Timestamp(t)), side="right") - 1   # LEAK-2
...
-        n = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(t))))   # count of dates < t
+        n = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(t)), side="right"))   # LEAK-2
```
A one-word `side="right"` change (an easy, realistic typo) — now a market observation dated exactly `t` is visible to a read standing at `t`.

```
$ python3 -m pytest -q tests/test_read.py tests/test_walk.py tests/test_walk_baselines.py tests/test_engine.py tests/test_similarity.py
.....s.......F............F.....                                         [100%]
=================================== FAILURES ===================================
______ test_step8_placebo_skill_is_zero_within_ci_on_synthetic_null_data _______
    ...
>       assert pl["n"] >= 10 and pl["null_holds"] is True and pl["vs_random_analogs"]["covers_zero"]
E       assert (83 >= 10 and False is True)
______ test_step6_standardization_uses_only_data_before_t_future_outlier _______
    ...
>       assert spiked.value_before("vix_pct", "2012-01-01") != 1e6
E       AssertionError: assert 1000000.0 != 1000000.0
tests/test_similarity.py:82: AssertionError
2 failed, 29 passed, 1 skipped in 78.17s (0:01:18)
```

**Caught by two tests** — the direct unit test for this exact property (`test_similarity.py`, as its docstring promises), and, notably, the **placebo test** (`test_step8_placebo_skill_is_zero_within_ci_on_synthetic_null_data`) failed too: `pl["null_holds"]` flipped to `False` on VIX-matched pseudo-events, i.e. same-day market leakage manufactures spurious skill that the placebo diagnostic actually detects, even though placebo testing isn't described as a leakage check. **`test_step8_leakage_broken_filtration_must_differ` again passed** with this leak live, for the same structural reason as Leak 1 — it never touches `InfoSet`, only `Corpus.pool()`'s event-admission logic.

Reverted cleanly (`git diff` empty afterward, confirmed).

**Both leaks tried; both caught — but only by tests that happen to target that exact mechanism, never by the protocol's designated leakage test, which is structurally blind to anything short of total, no-date-filter breakage.**

---

## FINDINGS, ranked

**1. The published `leakage_test` cannot detect a real leak in the sealed path — only total absence of filtration.**
README states: *"Leakage guard: the walk is run twice, once with the filtration enforced and once with it deliberately broken... The two runs must differ; if they do not, the filtration is not doing anything and the result is void"* (`WALK_FORWARD_PROTOCOL.md` §1, mirrored in `summary.json.leakage_test.verdict: "filtration is binding"`). This sentence is true as written — the test does show the two runs differ — but it is being read (by the protocol, and implicitly by anyone citing `leakage_test.reads_differ: true` as evidence the engine is point-in-time-honest) as proof the *sealed* run itself has no leakage. It is not that: `leakage_test` compares sealed against a maximal `break_filtration=True` run, never against a corrected reference. Two concrete, independent leaks — one in the analog-pool window-closure gate, one in the market-data standardization cutoff — both survived it undetected, in the same test run that reported `"filtration is binding"`. **Both leaks would inflate skill in the direction the README needs to be null.** Since the daily-tier G/P verdict is already null, this specific gap does not currently overturn the headline sentence — but it means the README's confidence that "the filtration is binding" rests on a test that is, by construction, incapable of confirming that.

**2. Corpus admission for the monthly tier is designed to show Joe the outcome before he decides.**
`data/candidates/REGISTRATION.md` §"The join to the monthly Big Moves" is a dated, disclosed, *deliberate* design choice — not a bug — but it is exactly the selection-on-outcome the task flagged as item (g): the sheet Joe uses to admit pre-1987 events into the corpus he governs (`SESSION_CHARTER.md` §2 rule 3, "Nothing enters `events` without Joe") carries `inside_big_move`, `monthly_move_pct`, and `wti_chg_3m_pct` as columns next to each candidate. At risk: README's own claim that *"Pre-registration with git timestamps... every amendment dated and appended, never edited... No fabricated field: sourced or 'unknown'. Nothing enters the corpus without a human."* — true on its face, but the *human* step is the one with outcome-contaminated input. This affects the monthly tier prospectively (only 14 events exist there today; the sheet targets its expansion), not the currently-published daily-tier null.

**3. Two market-conditioning features (CFTC positioning, EIA inventories) violate the engine's own stated filtration rule, unflagged.**
`WALK_FORWARD_PROTOCOL.md` §1: *"Prices and series: observations dated ≤ t... macro series use ALFRED vintages where they exist... otherwise the release lag is applied."* Executed check on `data/oil.db` (below) shows `derived.cot_pct` and `derived.inv_sigma` never apply a release lag — `as_of == obs_date` for every row — contradicting this sentence directly, while `gpr.GPRD` in the same table correctly does apply one. Direction: inflates skill (features become knowable ~3-5 days early); the published null survives despite this advantage, which is reassuring for the null but means the "filtration" sentence in the protocol is not fully true of the code as committed.

**4. `sr_*` situation-coding fields — a full third of the similarity metric's blocks — carry no vintage, contradicting the disclosed limitation's own stated mitigation.**
`WALK_FORWARD_PROTOCOL.md` §1: *"the current situation fields are not vintage-stamped; until each field carries a source date, fields whose source postdates t are set to 'unknown' for that read (conservative), and the share of fields blanked is reported."* The "set to unknown" half of this sentence is implemented only for `situation_state` panel rows, which have a vintage to test; it is not implemented for the `sr_*` columns feeding the same "situation" block, because those columns carry no vintage to test against at all. The limitation is honestly named; the promised mitigation is not built for the columns that most need it.

**5. Persistence baseline draws on hindsight-compiled academic datasets for old events (disclosed, minor).**
Named directly in Amendment B.1; the README's *"It beats persistence (+0.16, p < 0.001)"* claim, if anything, gets more robust rather than less if persistence is stronger than a true point-in-time persistence would be.

---

## Executed evidence (verbatim console output)

```
$ python3 -c "
import sqlite3
conn = sqlite3.connect('data/oil.db')
for sid in ['gpr.GPRD','derived.vix_pct','derived.inv_sigma','derived.cot_pct','derived.credit_stress','derived.real_rate','derived.usd_z','derived.curve_2s10s','fred.DCOILBRENTEU']:
    r = conn.execute('SELECT count(*), sum(CASE WHEN obs_date=as_of THEN 1 ELSE 0 END), sum(CASE WHEN as_of>obs_date THEN 1 ELSE 0 END), sum(CASE WHEN as_of<obs_date THEN 1 ELSE 0 END) FROM observations WHERE series_id=?', (sid,)).fetchone()
    print(sid, 'total=',r[0],'as_of==obs_date=',r[1],'as_of>obs_date=',r[2],'as_of<obs_date=',r[3])
"
gpr.GPRD total= 15219 as_of==obs_date= 0 as_of>obs_date= 15219 as_of<obs_date= 0
derived.vix_pct total= 9013 as_of==obs_date= 9013 as_of>obs_date= 0 as_of<obs_date= 0
derived.inv_sigma total= 14993 as_of==obs_date= 14993 as_of>obs_date= 0 as_of<obs_date= 0
derived.cot_pct total= 7030 as_of==obs_date= 7030 as_of>obs_date= 0 as_of<obs_date= 0
derived.credit_stress total= 4504 as_of==obs_date= 4504 as_of>obs_date= 0 as_of<obs_date= 0
derived.real_rate total= 5669 as_of==obs_date= 5669 as_of>obs_date= 0 as_of<obs_date= 0
derived.usd_z total= 4928 as_of==obs_date= 4928 as_of>obs_date= 0 as_of<obs_date= 0
derived.curve_2s10s total= 12559 as_of==obs_date= 12559 as_of>obs_date= 0 as_of<obs_date= 0
fred.DCOILBRENTEU total= 9963 as_of==obs_date= 9963 as_of>obs_date= 0 as_of<obs_date= 0
```

```
$ python3 -c "
import sqlite3
conn = sqlite3.connect('data/oil.db')
r2 = conn.execute('''SELECT count(*) FROM situation_state s JOIN events e ON e.event_id=s.event_id WHERE s.vintage != e.event_date''').fetchone()
print(r2)   # (8239,)
r3 = conn.execute('SELECT count(*) FROM situation_state').fetchone()
print(r3)   # (8564,)
"
```

`data/walk_forward/summary.json`: `leakage_test = {"reads_differ": true, "n_reads_with_different_analogs": 313, "asserted": true, "verdict": "filtration is binding"}`; `seal_check = {"ok": true, "n_records": 1565}`; `registered.spec.big_move_q = [0.9, 0.95, 0.975]`; `menu` has 12 items (M13/Amendment C recalibration not yet live).

---

## What I did not do
- Did not audit `src/engine/scoring.py` line-by-line (only its header/role, referenced via callers in `walk.py`) — no leakage-relevant logic found there in the parts read (pure proper-scoring-rule arithmetic).
- Did not try a third leak (task allows stopping after two, both caught, both bypassing the named leakage test).
- Did not run the full `pytest -q` suite in the clone (only the four files named in the task plus `test_similarity.py`) — a concurrent session was running the full suite live in the real repo during this audit, competing for CPU; running it again in the clone was not needed to answer the task.
- Did not evaluate Amendment C / `recalibrate.py` (M13) in depth beyond confirming it is not yet in the published run — it is untracked, uncommitted work in progress by the other live session.
- Did not check every one of the ~35 `situation_state` panel fields' vintage conventions against their true publication dates (spot-checked `polity.py`/`cow_nmc.py`'s "knowable 1 Jan year+1" convention, which is disclosed and defensible, not verified against every source's real release calendar).
