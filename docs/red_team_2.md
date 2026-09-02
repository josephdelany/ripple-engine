# Red team 2 — adversarial review and replication (Session D, 2026-09-02)

*Reviewer stance: the committee's external reviewer. Read everything; edited nobody's code or
data. The audit was taken against the committed state at `b7c8ec1` (branch `v2-day1`); by the time
this report was finished HEAD had moved to `4c989b0` through sessions A, B, C and Cowork, and where
a later commit changes a finding's status that is said in the "status at HEAD" column. Where a
finding touches a file that was dirty in the shared tree, the committed version was audited
(`git show HEAD:…`). Every number below was executed (python3 / sqlite3 read-only), never done by
eye; the arithmetic and the verbatim tool output live in the appendices under
`docs/red_team_2/`. No fixes are proposed. Findings are ranked by whether they change a published
sentence: first the README, then the paper draft, then the desk.*

**Owners** follow `SESSION_CHARTER.md` §1: **A** — `src/state/**`, `OUTCOME_MAPPING.md`,
`story_read.py`, `feed_build.py`, `api_v2.py`, `app.html`, corpus tooling; **B** — `src/engine/**`,
`walk.py`, `data/walk_forward/**`, `WALK_FORWARD_PROTOCOL.md` amendments,
`data/candidates/REGISTRATION.md`; **C** — the Ripple briefs (`RIPPLE_*`, `ripple_fetch.py`);
**Cowork** — `docs/PAPER_DRAFT.md`, `docs/demos/*`, PATH Steps 10/12. Files that predate the charter
(`big_moves.py`, `materiality.py`, `backend.py`, `digest.py`, `trace.html`, `backtest.html`,
`fetch_eia.py`, `fetch_cot.py`, `BIG_MOVES_REGISTRATION.md`, all from `594d2fa` or earlier) have no
session owner; they are marked **pre-charter → Joe to assign**.

**Files this session added (nothing else touched):** `docs/red_team_2.md`,
`docs/red_team_2/D1_registration_audit.md`, `D1b_ripple_and_amendmentD.md`, `D2_leakage_hunt.md`,
`D3_multiplicity.md`, `D4_labels.md`, `D5_reader.md`, `D6_replication.md`, `D8_paper.md`,
`D9_desk.md`; `Makefile` (target `reproduce`); `tests/test_reproduce.py`; `requirements.txt`
(pinned `==`, comments kept). Nothing under `data/` was written. The walk was never run in this
tree; replication ran in clean clones under the session scratch directory. One sub-review created
and removed two temporary `git worktree` checkouts to run a test at a fixed commit; `git worktree
list` shows only the main tree.

---

## The top three

**1. The published placebo sentence rests on an amendment Joe has not ratified, and the committed
walk implements amendment text that is not in the protocol.** README:62 *"The VIX-matched placebo
is null (−0.02, CI covers zero)"*; paper §9 *"the placebo is null, as required"*. The registered
protocol §6 says *"engine skill on placebos must be indistinguishable from zero"*; against
climatology, the reference every other skill number uses, the placebo skill in run 182828Z is
−0.081 (CI −0.112 … −0.048; `placebo.vs_climatology`), which is not zero. The −0.02 quoted is the
*size-matched* placebo, a reference defined only in "Amendment A", text that exists solely as a
proposal in `data/gates/step8_2026-09-02.md` under *"Gate 1 (Joe): ratify Amendment A"* and appears
nowhere in `WALK_FORWARD_PROTOCOL.md` (0 occurrences of "size-matched"; the protocol's amendments
are B–I). The gate file records that A.4–A.5 *"describe code written before the amendment"*.
README:78 *"every amendment dated and appended, never edited"* is therefore not true of the
amendment the headline depends on. Owner: **B** (protocol, walk), **Joe** (ratification).

**2. Both numbers in the Big Moves headline come from an unregistered rule, and one of them does
not reproduce from the published file.** README:49–51 *"(Big Moves, Brent, 43 episodes 1987–2026):
35% of the market's largest moves have no identifiable event in the corpus; the market's extreme
preceded the catalyst in a third of the rest"*; the same numbers in paper §4 and the Abstract.
(a) `BIG_MOVES_REGISTRATION.md:10–11` registers clustering *"within 60 trading days"* and no merge
step; `src/big_moves.py:33,40–41` clusters at 90 calendar days and merges same-sign clusters
within 60 days. No amendment covers either value (Amendment 3 sets 365/180 for the monthly tier
only); both constants were in `594d2fa`, the commit that also landed the registration and the
computed JSON, so git cannot show "registered before computed"; no test exercises them. (b) From
`data/big_moves/brent.json` (committed 10:21, before the README at 14:14): of the 28 Brent episodes
with an attributed event, 14 (50 %) have every event flagged `anticipated`, 20 (71 %) have at least
one, 14 (50 %) have the earliest-dated event anticipated. "A third" appears only by pooling Brent,
WTI and the diesel crack (33/89 = 37 %), and the sentence's own scope is Brent. Executed in
`D1_registration_audit.md` and re-executed by the synthesising reviewer. Owner: **pre-charter →
Joe to assign** (code and registration), **Cowork** (paper §4).

**3. Four in five "war" labels are wars that were already on before the event; a persistence
forecast built from the same sources beats both the engine and the base rate; and the README's
persistence sentence reads the other way.** README:30–33 *"Escalation at +90 days … is computed
from dated records in ICB, COW MID, COW War and UCDP"*; README:58 *"no skill beyond the base rate
for escalation"*; README:60 *"It beats persistence (+0.16, p < 0.001)"*. Blind re-derivation of 20
random IES-90 rows agrees 20/20 (κ = 1.0), so the code implements `OUTCOME_MAPPING.md` exactly; the
problem is the rule. All 54 level-3 rows come from COW War (16) or UCDP GED (38), the two sources
Amendment 1.1's "ongoing → no level" fix was not extended to. Executed on `event_outcomes`
(source `ies90`): 31 of the 38 GED war labels already had ≥ 250 deaths in the 90 days *before* the
event (`deaths_ged_pre90`, a field the mapping stores and does not use); 12 of the 16 COW spells
began at or before the event date. ≈ 43/54 ≈ 80 % of level 3 is a pre-existing war continuing
through the window. The replication then produced the executed consequence: in a clean clone of
`b7c8ec1` with the persistence sources present, the G-persistence baseline (Amendment B) scores
Brier 0.480 against the engine's 0.706 and climatology's 0.701; engine-vs-persistence skill
−0.469 (CI −1.036 … −0.138; DM/HLN p 0.002; BH q 0.019, survives); SPA with persistence as the
benchmark, best item M07, p 0.575. Session B's run 193022Z, published to the tree while this
report was being written (`d99b1ef`), gives −0.467. So for escalation the engine loses to
persistence, and the README's "beats persistence" is a price-tier number a reader will take as
general. The G/P null does not flip; what "escalation" and "beats persistence" mean does. Owner:
**A** (`OUTCOME_MAPPING.md`, `ies90.py`), **B** (walk publication), **Cowork** (paper §9–§10).

---

## Findings, ranked by whether they change a published sentence

### Tier A — README: the sentence as written is false, unsupported, or depends on something unratified

| # | Sentence at risk (README line) | Finding | Evidence | Owner | Status at HEAD (4c989b0) |
|---|---|---|---|---|---|
| A1 | :62 "The VIX-matched placebo is null (−0.02, CI covers zero)" | Depends on unratified Amendment A.4; vs climatology −0.081 (CI −0.112 … −0.048). | `data/gates/step8_2026-09-02.md:6–47`; protocol §6; `summary.json.placebo` (run 182828Z, now only in git at `d3df9af`) | B; Joe | Amendment A still absent from the protocol; Amendment E (`9c5c9e8`) registers size-corrected scores as a *prospective* v3 gate, Joe's decision |
| A2 | :78 "every amendment dated and appended, never edited" | Amendment A is neither appended nor ratified; committed `walk.py` implements A.1–A.6 (IES-90 gate, RPS, size-matched placebo, `diagnostic_fair`, FAR_FUTURE). | `walk.py` HEAD:558–572, 943–947, 1217 | B | unchanged |
| A3 | :49 "43 episodes … 35% … no identifiable event" | `cluster_days=90` calendar + `MERGE_DAYS=60`; registered 60 trading days, no merge; untested; unamended; same commit as registration and output. | `BIG_MOVES_REGISTRATION.md:10–11`; `src/big_moves.py:33,40–41,88–98`; `git log -S"CLUSTER_DAYS = 90"` → `594d2fa` | pre-charter → Joe | unchanged |
| A4 | :51 "preceded the catalyst in a third of the rest" | Brent file gives 14/28 = 50 % (all anticipated), 20/28 = 71 % (any); "a third" only by pooling three assets (33/89). | `data/big_moves/brent.json`, executed | pre-charter → Joe | unchanged |
| A5 | :30–33 "computed from dated records … (κ ≈ 0)"; :58 "no skill … for escalation"; :60 "It beats persistence (+0.16, p < 0.001)" | 100 % of level-3 labels from the two sources with no ongoing/onset carve-out; ≈ 80 % pre-existing wars (GED 31/38; COW 12/16). κ ≈ 0 is accurate but describes the retired `sr_outcome_90` comparison. With the sources present, G-persistence beats the engine (skill −0.469, p 0.002) and climatology. | `event_outcomes` `level_source`, `deaths_ged_pre90`; `OUTCOME_MAPPING.md` A1.1 vs the COW War / GED rules; clone-b `summary.json`; `d99b1ef` | A; B; Cowork | Run 193022Z (`d99b1ef`) publishes −0.467; README still cites 182828Z; no amendment yet addresses the ongoing-war rule |
| A6 | :79–80 "An external adversarial review (`docs/red_team_1.md`) that falsified the original headline result; the downgrade published" | The downgrade is not applied to the desk. `docs/red_team_1.md` §"FINAL TIERS": *"Validated set under the single evidentiary bar: empty"*, signed off by Joe 2026-08-15. Live-rendered today (jsdom, scratch clone): `/digest` *"The validated edge"* / *"The one signal that passed the full validation gate"* (`src/digest.py:300–303`), *"4 validated"* (:332); `/backtest_view` *"the validated edge (H1) HOLDS"* (`src/backend.py:1059–1074`); `/trace_view` *"H1 — VIX stress (validated; …)"* (`backend.py:1137`), *"Validated transmission"* (`src/trace.html:120`); plus `/edge_portfolio` `verdict:"VALIDATED"` ×4 (`backend.py:845,865`), `/propagation_graph`, `/sowhat`, `/track_record`, `/h1_live_edge`, `/widgets.json`, `/openapi.json`. Charter §2 rule 4: VALIDATED only per protocol §7. | `D9_desk.md` §3, §5.1; `docs/red_team_1.md:200–225` | pre-charter → Joe (v1 surfaces) | unchanged |
| A7 | :9 "every threshold was registered before it was computed" | `eta`, `n_boot`, `n_spa_boot`, `n_perm`, `random_draws`, `k_max`, `placebo_reps`, `placebo_excl_days`, `pit_bins`, `reliability_bins` and all five spec-curve ranges exist only in `walk.py`'s `REGISTERED` dict, committed with the code; protocol §6 promises a "pre-declared range" it never declares; `summary.json.registered` is copied from that dict. Base `BIG_MOVES_REGISTRATION.md` and `CLAIM_LEDGER_REGISTRATION.md` landed with their code and output (`594d2fa`); every later amendment does show a clean gap. | `walk.py` HEAD:60–77; grep; `git log` | B; pre-charter → Joe | Amendment I (`9c5c9e8`) registers seeds and a content digest; the constants above remain in the dict |
| A8 | :20 "the engine at date t sees only what was knowable at t" | (i) `derived.cot_pct` and `derived.inv_sigma` have `as_of == obs_date` on 100 % of rows (7,030; 14,993) though CFTC releases ~3 d and EIA ~5 d after the reference date; `gpr.GPRD` in the same table has `as_of > obs_date` on all 15,219 rows. (ii) The seven `sr_*` fields in `similarity.py` `SR_MAP` (:88–90, :244–246) carry no vintage and are never blanked; the panel fields are gated by `apply_panel()` (:203–220). (iii) The Big Moves top-5 % threshold is a full-history quantile (`big_moves.py:39,68`) used at read time by `read.py` `in_big_move`/`m_read` (:159–165, :325–332). All three inflate skill; the null survives them, so the null is conservative. | executed SQL in `D2_leakage_hunt.md`; `fetch_eia.py:118`; `fetch_cot.py:107` | pre-charter → Joe (i, iii); A (ii, `knowable_at`) | Amendments G (lags 3 d / 5 d) and H (`knowable_at`) registered at `9c5c9e8`, before code; (iii) unaddressed |
| A9 | :65–67 "A label-permutation test rejects 'the engine is noise' (p 0.008)" | Not in the FDR family (`walk.py` HEAD:1093–1099 assemble it from per-tier `family_p`; the permutation is a separate path). Pooled with the 79 other reported p-values, BH at q 0.05 gives q 0.091. The null is i.i.d. within-class shuffling (:671–676) ignoring the registered 35-day clusters; label lag-1 autocorrelation +0.17 (executed from `scores.jsonl`), so the p is anti-conservative. Matches protocol §6 as written: a registration gap, not a code deviation. | `D3_multiplicity.md` §2, §3, §5 | B | Amendment F (`9c5c9e8`) registers block permutation, before code |
| A10 | :36 "four baselines (climatology, persistence, random analogs, a frozen engine)" | True for P; the G tier of the run the README cites has three. | `summary.json` at `d3df9af`, `tiers.daily.G.engine_vs` keys | B | Run 193022Z has four; README not updated |

### Tier B — README: the sentence stands, but its evidential basis is weaker than it reads

| # | Sentence at risk | Finding | Evidence | Owner | Status at HEAD |
|---|---|---|---|---|---|
| B1 | :40 "a leakage test that breaks the filtration to prove it binds" | The test compares the sealed run to a maximal `break_filtration=True` run. Two deliberate one-line leaks in a scratch clone (dropping `g_closed_by` in `Corpus.pool`, `read.py:184–192`; a `side="right"` off-by-one in `InfoSet.value_before`/`stats`) both left `test_step8_leakage_broken_filtration_must_differ` passing and `verdict: "filtration is binding"` unchanged. Each was caught by a narrow unit test (`test_read.py:98`; `test_similarity.py:82`, plus the placebo test flipping `null_holds`). The leakage test proves total breakage differs; it cannot certify the sealed path. Not the headline because the leaks were caught. | verbatim pytest in `D2_leakage_hunt.md` | B | Amendment F registers a filtration audit inside the sealed run |
| B2 | :60 "It beats persistence (+0.16, p < 0.001)" (P tier) | Survives BH, Holm, Bonferroni over the registered 31 and the reported 80 comparisons. But persistence is a single-atom point mass CRPS-scored against a k-atom distribution; the size correction the walk applies to climatology (`diagnostic_fair`, Ferro 2014) has no persistence variant. | `scores.jsonl` `n_atoms: 1`; `diagnostic_fair` keys | B | Amendment F registers fair-vs-persistence |
| B3 | :9 "Every number in this repo is one hop from its receipt" | `data/oil.db` is git-ignored; rebuilding it needs FRED, EIA (keyed), CFTC, the GPR file; the persistence baseline needs correlatesofwar.org plus git-ignored `data/state/raw/` and `data/cache/`. A clean clone dead-ends at `oil.db`. The seal hashes `run_id` and `sealed_at` into the digest, so it proves tamper-evidence of one run, not cross-run equality of content; `walk.py` does not say so. The run the README and paper cite (182828Z) is no longer at `data/walk_forward/summary.json` (overwritten by 192906Z then 193022Z during this review); its `reads/scores/weights.jsonl.gz` are archived, its `summary.json` is not archived by the pipeline and survives only in git (`d3df9af`). | `D6_replication.md` §1, §4a; `D8_paper.md` finding 6; `data/walk_forward/runs/` | B | Amendment D implemented (`07ed7a8`) and fired; `summary.json` per run still not archived |
| B4 | :81 "Nothing enters the corpus without a human" | Latent bypass: `src/admit_events.py:91` sets `joe_decision = "approve"` in code for the AUTO_ADMIT tier, indistinguishable downstream from Joe's approval. Executed: no `data/extract/admission_log.csv`; 0 of 633 `candidate_review.csv` rows carry the tag; all 32 approvals are `candidate_source=manual`. True in fact today; false as a guarantee. | `admit_events.py:85–91`; counts executed | A | unchanged |
| B5 | :81 same sentence, monthly tier, prospective | `data/candidates/REGISTRATION.md:34–47` registered an admission sheet carrying `inside_big_move`, `monthly_move_pct`, `wti_chg_3m_pct` *"so Joe sees the outcome the walk would score"*: selection on outcome by design. | quoted from the registration | B | Answered: Amendment 1 to that registration (`9c5c9e8`) and code (`5026731`) split the outcome join into a separate file; the sheet is blind |
| B6 | :56–68 the prediction paragraph | The release check's "only G comparison that clears p < 0.05" (RPS vs random analogs, p 0.001) is outside the family and has no SPA over the 12-item RPS family, unlike Brier (best M07, p 0.793). | `release_check_2026-09-02.md`; `summary.json.tiers.daily.G.rps` | B | Amendment F registers an RPS SPA |
| B7 | :42 "Feed (market state, gated stream)"; :23 "each attributed to what was knowable while it moved" | `reader.py` emits no event date and no confidence (`STORY_SCHEMA` :228–256; `cage()` :422–456); the Feed's displayed time is the capture timestamp (`feed_build.py:132`, `app.html:125`), unlabeled. On 30 stored headlines the regex fallback agreed with a human read on class 24/30 (geopolitical bucket 6/10), entity 19/30; "pause attacks" → `infrastructure_attack`; Red Sea headlines missed `chokepoint_disruption`; "war" in opinion copy → `conflict_escalation`. No template renders the `reader` mode field, so a `regex_fallback` classification would show unlabeled (charter rule 6). Big Moves attribution does not use the reader, so :23 holds. | `D5_reader.md` §2–§4; `D9_desk.md` §5.3–5.4 | A | unchanged |

### Tier C — no README sentence at risk; registered-vs-built gaps the committee should know

| # | Finding | Evidence | Owner | Status at HEAD |
|---|---|---|---|---|
| C1 | Amendment C (M13) was registered *from* run 182828Z's Murphy decomposition: a post-hoc item, dated and disclosed; §7 unchanged. | protocol Amendment C preamble | B | Run 193022Z: M13 worse than climatology (−0.590), published as computed |
| C2 | `data/candidates/REGISTRATION.md`'s deliverable (the pre-1987 sheet) was unbuilt at `b7c8ec1`; only the 53-code state set reached `src/dossier.py` (exact set match). | grep `pre1987_candidates` | B | code at `5026731` |
| C3 | Materiality: thin classes and `policy_response` can emit NOISE where the registration says "IN LINE … never MATERIAL" / "capped at IN LINE"; ratio < 0.8 branch untested. | `CLAIM_LEDGER_REGISTRATION.md:16–18`; `materiality.py:66,71` | pre-charter → Joe | unchanged |
| C4 | Hypothetical claims can never resolve: `ledger.py:263` skips `modality=="hypothetical"` unconditionally. | `CLAIM_LEDGER_REGISTRATION.md:34–36` | pre-charter → Joe | unchanged |
| C5 | Flow-claim verdicts use raw `abs(chg_pct) >= 10`, not `propagate.py`'s realized-disruption fraction the registration names. | `ledger.py:192,280` | pre-charter → Joe | unchanged |
| C6 | `M07_uniform_k12:G` status "SUGGESTIVE" without "/ null" in `verdict.rules`; served raw by `/api/walk/summary` and mirrored into `/api/story`, `/api/ledger`, `/backtest`; no screen renders it. | `summary.json.verdict.rules`; `api_v2.py` | B; A | Amendment F registers item-status wording |
| C7 | Location-basis contamination where the corpus names no counterparty: `sanc_2013_11_24` (JPOA, a de-escalation) is level 2 from Iran–Pakistan border incidents; `qatar_gulf_blockade_2017`, `rus_druzhba_strike_2025a` likewise; dyadic precedence cannot fire when P is empty. | `event_outcomes` `basis`, `rule_fired` | A | unchanged |
| C8 | Persistence (Amendment B) and the labels draw on datasets compiled decades after the incidents in one vintage; disclosed in B.1. Direction: makes persistence stronger, so the G result in A5 is if anything robust to it. | Amendment B.1 | B | — |
| C9 | `RIPPLE_REGISTRATION.md` (`cbf4fdc`, C) is genuinely pre-code: `src/ripple_lp.py` does not exist; every LP item, Table M/N, horizons, min n 15, BH q 0.10, the nine EXPECTATIONS, placebo, asymmetry, the 2009-02-06 split and the K-V split are UNIMPLEMENTED; nothing computed or published. Loaders and the 18-file sha256 seed manifest verify. E-1's expectation contradicts the sign of 2 of 3 tightening classes in the older `cross_asset_results.txt`, evidence against post-hoc expectations. Registered filtration lags will meet the same `as_of == obs_date` pattern as A8(i) unless the loaders apply them. | `D1b_ripple_and_amendmentD.md` §1 | C | Amendments A, B to that registration (`d6a3bde`, `60058f9`) appended before computing |
| C10 | Amendment D (sealed-run archive): implemented at `07ed7a8`; `archive_prior_runs` (`walk.py:121–148`) matches D's text; `tests/test_walk_archive.py` passes at `07ed7a8` and at HEAD in isolated checkouts but **fails in the live shared tree** because of uncommitted in-flight edits to `src/engine/read.py` / `similarity.py`. Minor wording overstatement in D ("each archive still verifies"). | `D1b…` §2 | B | archive has fired (seven run directories under `data/walk_forward/runs/`) |
| C11 | `/event_detail` returns 500 (`ValueError: Out of range float values are not JSON compliant: nan` on a NaN `severity`); `situation.html:87` renders retired `outcome_90` analog codes with no "retired" label under the header "Verified analog set" (`app.html:194,249` labels them correctly). | `D9_desk.md` §5.2, §5.6 | pre-charter → Joe (`backend.py:675–706`); A (`situation.html`) | unchanged |
| C12 | Process observation: during this review a concurrent session loosened a weight-sum tolerance in `tests/test_walk_recalibration.py` from 1e-6 to 1e-5 ("weights logged at 6 decimals"). Arithmetically defensible; noted because the fix chosen was the tolerance rather than the logging precision. | process list 15:15 | B | — |

### Tier P — `docs/PAPER_DRAFT.md` (Cowork; v0.1 from run 182828Z)

Every score, skill, CI and p-value in §8–§9 matches its source JSON to stated rounding; all
three demos reproduce (hashes, `sealed_at < looked_up_at`, every analog date, every score).
The paper's problems are unstated dependencies and where it allows confident language. Full
sentence-by-sentence table in `docs/red_team_2/D8_paper.md`.

| # | Paper sentence at risk | Finding | Owner |
|---|---|---|---|
| P1 | §9 "the placebo is null, as required"; Abstract "under a pre-registered walk-forward protocol … a rule written before any number was computed" | = A1/A2: licensed only by unratified Amendment A.4. | Cowork; B |
| P2 | §4 table and Abstract "35%" (43/46/36/18 episodes; every P(big \| class) ratio) | = A3/A4: computed under 90/60, not the registration §4 cites. | Cowork; pre-charter |
| P3 | Abstract and §13 "escalation skill +0.12 (p < 0.001) against self-coded labels" | No Appendix A row; nearest source is the gate report's run 180821Z (+0.116, p 0.001), not the paper's stated run 182828Z; the README at least says "an earlier run". | Cowork |
| P4 | §3 "Seventeen loaders populate 34 of 70 registered fields"; §13 "322 tests" | Both accurate at commit `0a2f9ed` (15:39) and overwritten minutes later (`266b918` 15:43: 50/70; `86282ec` 15:54: 354 passed); Appendix A cites mutable files without a commit. | Cowork; A |
| P5 | §13 "Pre-registration files with git timestamps (… `BIG_MOVES_REGISTRATION.md`, `CLAIM_LEDGER_REGISTRATION.md` …)" | = A7: for those two, git timestamps show registration, code and output in one commit. | Cowork |
| P6 | Appendix A's path `data/walk_forward/summary.json` | The cited run is no longer at that path (B3); its `summary.json` is not archived. | Cowork; B |
| P7 | §9 "The engine's analog selection carries information about the labels"; §10 "The engine knows something about which situations stay quiet and is over-confident about which ones burn" | = A5: already-at-war dyads cluster together and stay level 3 by construction; the simpler explanation is unmentioned, and the permutation p these sentences lean on carries A9's three caveats. | Cowork |
| P8 | Abstract "compared to four baselines" | = A10 for G in this run; §7 discloses it, the Abstract does not. | Cowork |
| P9 | `docs/demos/2026.md` "The largest atom was Ever Given at +12%" | The +12.011 % atom is `hankuk_chemi_seizure_2021`; Ever Given's is +8.522 %. | Cowork |

### Tier S — the desk (`docs/red_team_2/D9_desk.md`; 89 GET routes via TestClient, four screens jsdom-rendered, 25 seeded numbers traced with 0 mismatches)

| # | Exact string | Where | Stronger than the record? | Owner |
|---|---|---|---|---|
| S1 | "The validated edge" / "The one signal that passed the full validation gate" / "4 validated" | `src/digest.py:300,303,332`, rendered at `/digest` | Yes: red team 1's validated set is empty (A6) | pre-charter → Joe |
| S2 | "the validated edge (H1) HOLDS"; "Validated edges and nulls are shown side by side" | `src/backend.py:1059–1074`, rendered by `backtest.html` | Yes (A6) | pre-charter → Joe |
| S3 | "H1 — VIX stress (validated; H2 inventories & H3 positioning rejected)"; "Validated transmission — how a shock propagates under stress" | `backend.py:1137`; `trace.html:120` | Yes (A6) | pre-charter → Joe |
| S4 | `verdict:"VALIDATED"` ×4 | `/edge_portfolio` (`backend.py:845,865`), `/propagation_graph`, `/sowhat`, `/track_record`, `/h1_live_edge`, `/widgets.json`, `/openapi.json` | Yes, API-visible | pre-charter → Joe |
| S5 | `outcome_90` analog codes (CONTAINED, LIMITED_RETALIATION, WIDENING…) under "Verified analog set", no "retired" | `situation.html:87`, rendered at `/situation_view` | Yes: retired label without "retired" | A |
| S6 | Feed date `2026-08-31T20:25` style, inline after the class | `feed_build.py:132`; `app.html:125` | Capture timestamp shown as if an event time | A |
| S7 | `"SUGGESTIVE"` for `M07_uniform_k12:G` | `/api/walk/summary` and mirrors; not rendered | API-only (C6) | B; A |
| S8 | `/event_detail` → 500 | `backend.py:675–706` | Crash, not a claim | pre-charter → Joe |

No screen renders "predicts", "will", an occurrence probability, or the retired +0.043/+0.143
numbers; the Walk, Story trust rows, Ledger board and Big moves pages trace every sampled number
to its committed file.

---

## Method summaries and appendices

**D-1 Registration-vs-code** (`D1_registration_audit.md`, `D1b_ripple_and_amendmentD.md`): every
registered item in seven documents plus `menu.json`, with doc:line, file:line and status; the
amendment-timing table from `git log`. `OUTCOME_MAPPING.md` is the best-matched document
(near-exact, including the 10-entry littoral map by set-diff). Deviations uncovered by any
amendment: A3 (cluster/merge), C3 (thin-class NOISE), C5 (flow statistic), A2 (Amendment A
implemented, unregistered).

**D-2 Leakage hunt** (`D2_leakage_hunt.md`): ten paths ranked with direction. Found: A8(i)(ii)(iii),
B5. Not found: analog-pool window-closure leakage at HEAD (`read.py:184–192` strict and tested),
baseline contamination (climatology and random analogs draw from the same point-in-time pool),
`sr_outcome_90` reuse (absent from every read/score path). Deliberate leaks: B1.

**D-3 Multiplicity** (`D3_multiplicity.md`): reportable space 12 items × 2 tiers × 10 score
variants × ≤ 4 baselines × 3 regime blocks × 162 spec cells × 3 placebo variants; registered FDR
family as the code assembles it: 31 comparisons, daily tier only; p-values actually printed: 80,
or 242 with spec cells. BH/Holm/Bonferroni recomputed over each set: P vs persistence survives
all; G RPS vs random analogs survives all pooled sets but was never eligible; permutation p 0.008
survives nothing once pooled.

**D-4 Labels** (`D4_labels.md`): seed 20260902, 20 rows derived from raw ICB/MID/COW War/GED under
the mapping as written before reading the engine's level: 20/20, κ = 1.0. The three
`no_independent_outcome` events are genuinely uncovered (2025–2026); level-0 events have a
covering source that recorded nothing. κ ≈ 0 for the retired labels reproduces exactly (ICB −0.001
n 43; MID −0.234 n 15; UCDP 0.104 n 184; precedence 0.061 n 184). `data/audit_202609.md` untouched.

**D-5 Reader** (`D5_reader.md`): 30 stored headlines from `data/alert_queue.csv`, seed 20260902,
10/10/10, human-read first, regex fallback with `RIPPLE_READER=off` (a live LLM hit writes a
cache). Class 24/30, entity 19/30, date not emitted; every disagreement verbatim in §4.

**D-6 Replication** (`D6_replication.md`): chain, Makefile, timings, diffs, verbatim pytest.

| run (clean clone of `b7c8ec1`, concurrent) | inputs | walk wall time |
|---|---|---|
| A `walk_20260902T191640Z` | `oil.db` only (sibling copy skipped by a path bug in the first Makefile draft, fixed before run B) | 1036 s (reads 302 s; inference 636 s; leakage re-run + figures to 1036 s) |
| B `walk_20260902T191744Z` | `oil.db` + `state/raw` + `cache` | 1001 s |

Determinism (executed JSON diff, tolerance 0 then 1e-9): clone A vs committed 182828Z:
`data_state`, `permutation`, `placebo`, `spec_curve`, `verdict` byte-identical; all 163
differences are Amendment-B keys absent from the committed file; no floating-point drift. Clone A
vs B: 48 differences, all in the persistence subsystem (A fell back to climatology on 153 reads, B
on 2). Content hashes with `run_id`/`sealed_at`/`hash` stripped: 126/313 match A vs B (the
non-geopolitical reads, which carry no persistence block), 0/313 vs the committed run.
`generated_at` is stamped after the reads seal, so `generated_at − run_id` understates the walk
by ~3×. `tests/test_reproduce.py` (7 tests): skips cleanly without `REPRO_SUMMARY`/`REPRO_READS`
(`7 skipped in 1.25s`); against clone A, 4 passed and 3 failed on exactly the Amendment-B drift
(`registered.g_baselines` absent from the committed file; 313/313 content hashes; 162 keys); they
pass once the committed run is produced by the committed code and must not be loosened.
`requirements.txt` pinned (pandas 2.3.3, numpy 2.4.3, requests 2.34.2, matplotlib 3.11.1,
pyyaml 6.0.3, feedparser 6.0.11, rapidfuzz 3.14.5, xlrd 2.0.2, yfinance 1.5.1, pytest 9.0.3;
Python 3.14.3). Makefile guard: refuses when the tree has uncommitted changes to tracked files
(shared tree: 25; fresh clone: 0), `REPRO_FORCE=1` overrides; the first draft refused on any
non-empty `reads.jsonl`, which every clone has since the ledger is committed.

**D-8 Paper** (`D8_paper.md`): 254 sentences numbered with a line map; every numeric sentence
against its source key; every causal/epistemic word judged; 26 Appendix A rows re-read; three
demos re-derived from `reads.jsonl`/`scores.jsonl`.

**D-9 Desk** (`D9_desk.md`): 89 GET routes, POST routes listed with what they write and not
called; jsdom renders of `app.html`, `situation.html`, `trace.html`, `backtest.html`; static grep
of the other four; 671 raw pattern hits grouped by emitter.

---

## What I did not do

- Did not run the walk, `./go`, `refresh.py`, the watcher or any POST endpoint in the shared tree;
  did not write under `data/`; did not write to `data/audit_202609.md` or `data/audits/`.
- Did not audit the dirty working-tree versions of `src/engine/*`, `src/walk.py`, `api_v2.py`,
  `app.html`, `situation_state.py`, `tests/conftest.py`; findings are against `b7c8ec1`, with the
  status column noting later commits I read but did not re-audit (`9c5c9e8`, `5026731`, `d99b1ef`,
  `07ed7a8`, `cbf4fdc`, `0a2f9ed`).
- Did not recompute Big Moves under the registered rule (60 trading days, no merge) to say what
  43 / 35 % / "a third" become; that is a fix.
- Did not test the reader's live LLM path (writes a cache; needs a key).
- Did not jsdom-render `terminal.html`, `question.html`, `workbench.html`, `big_moves.html`
  (static grep only); did not re-audit `PRE_REGISTRATION.md` v1's own promotion rule behind the
  v1 "VALIDATED" strings, only whether the desk shows them against red team 1's record.
- Did not re-derive κ for OUTCOME_MAPPING Amendment 1.1 from a hand-built confusion table beyond
  the four stored comparisons.
- Did not verify that Amendments E–I (`9c5c9e8`), registered against the appendices of this review
  while it was in progress, are implemented; at HEAD only B-8 (`5026731`) has code.
