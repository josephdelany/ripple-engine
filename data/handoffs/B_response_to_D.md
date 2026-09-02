# B_response_to_D — Session D's findings on src/engine, src/walk.py, data/walk_forward (Brief 2, B-8)

Each finding from `docs/red_team_2/D2_leakage_hunt.md` and `D3_multiplicity.md` that names session B's
files is either fixed by a dated amendment (WALK_FORWARD_PROTOCOL.md Amendments F, G, H, I; candidates
REGISTRATION.md Amendment 1) with the code behind it, or answered with a computation. Numbers marked "(final run)" are from the run published by this brief, `walk_20260902T210135Z` (daily tier, 253 scored
reads, 150 with an IES-90 label). Everything else was computed in the working tree on 2026-09-02.

## D2 finding 1 — the leakage test was structurally blind. FIXED (Amendment F.1). Session D was right.
D's two deliberate leaks passed the registered broken-vs-sealed comparison because that comparison can only
see a *large* leak. The fix is an audit inside the sealed run by an independent code path (raw dates and a
mask-based lookup, never the functions that built the read): every analog dated before `as_of`; every
`g_closed` analog's +90-day window closed by `as_of`; every `p_closed` analog's closing price observation
dated ≤ `as_of`; every market value in the read's state equal to the last observation dated < `as_of − lag`;
the persistence window ending before `as_of`. Published as `summary.json.filtration_audit`; one violation
voids the run (`leakage_test.asserted` false, verdict "VOID: the filtration audit found a violation").

Both of D's leaks are re-applied in `tests/test_walk_filtration_audit.py` by monkeypatching the sealed path:
- Leak 1 (drop the window-closed check in `Corpus.pool`): `g_window` violations on the synthetic corpus,
  `leakage_test.asserted` false — where the old comparison alone still said "filtration is binding".
- Leak 2 (`side="right"` in `InfoSet.value_before`): `market_value` violations (the read's market value
  differs from the last value dated before `as_of`).
- A clean run: 0 violations over every check kind (counts published).
Final run: **15,491 checks, 0 violations** — 4,438 analog dates, 2,515 branch windows, 4,115 price windows,
4,236 market values (293 of them supplied by session A's state bridge, see below), 187 persistence windows.

**The audit's first firing was a real catch, and it was not a leak.** On its first run it reported 293
`market_value` violations: the read's `diesel_crack` value did not equal the engine's own last-observation-
before-`as_of`. Cause: session A's `situation_state` bridge writes a `diesel_crack` row for 300 events, and
`apply_panel` prefers it. Checked before accepting it: those rows carry `obs_date` 4–7 days *before* the event
(median 4) and `vintage` never after it — strictly more conservative than the engine's own path, not less. The
audit now verifies the panel path's `obs_date` and `vintage` against `as_of` instead of assuming a single
source, and counts it separately (`checks.market_value_from_panel`). Reported to session A as a finding: two
independent point-in-time paths feed the same field name, and the panel one silently wins.

## D2 finding 2 — the admission sheet showed Joe the outcome. FIXED (candidates REGISTRATION.md Amendment 1).
`pre1987_candidates.csv` now carries `event_date, actors, source, source_id, source_detail,
suggested_title` and nothing else; the Big Moves / WTI join lives in `pre1987_candidates_outcomes.csv`,
keyed by `(source, source_id)`, for use after admission decisions are recorded. Same 624 records. The
test asserts the split and the one-to-one key match.

## D2 finding 3 — no release lag on `cot_pct` / `inv_sigma`. FIXED (Amendment G).
The engine's information set applies registered lags: `cot_pct` 3 calendar days (CFTC positions as of
Tuesday, released Friday), `inv_sigma` 5 days (EIA WPSR week ending Friday, released Wednesday). Value and
standardization window both obey `d + lag < t`; the audit checks it; `registered.release_lags_days` records
it. The other `derived.*` series D listed (vix_pct, credit_stress, real_rate, usd_z, curve_2s10s) are market
prices observed on their date; Brent likewise. Effect on the published numbers (final run vs 193022Z):
the lags are live in the published run (`registered.release_lags_days = {cot_pct: 3, inv_sigma: 5}`) and the
audit confirms every market value obeys them. Their isolated effect is not separable from Amendment H's, which
landed in the same run and is much larger; both are in the same direction (less information at t).

## D2 finding 4 — `sr_*` fields carried no vintage. FIXED (Amendment H; session A's knowable_at).
The five source-coded situation fields (actor, target, conflict_scope, tempo, asset_role) now come from
`situation_state`'s knowable_at rows with `vintage ≤ as_of`; a field with no such row is unknown, for the
target and every candidate. H.1: `prior_dyad` and `propensity` are derived by `situation_record.py` from
dated prior corpus events and stay as coded. Counts, as computed on the corpus: 51 of 313 events have at
least one situation field knowable at t (session A's count, reproduced exactly); 726 coded field values
are blanked. The engine's situation block is therefore mostly empty at t; retrieval runs on the market
block for 262 events. Published per run in `data_state.situation_knowable`. Effect (final run vs 193022Z):
**this is the largest single change in the project's published numbers.** G Brier skill vs climatology moved
from −0.005 (DM p 0.884) to **−0.097 (CI −0.180..−0.018, p 0.022)**; P CRPS skill from −0.030 (p 0.111) to
**−0.071 (CI −0.136..−0.017, p 0.016)**; the spec curve went from 22 % positive to **0 % positive** (median
−0.075); the size-matched placebo stopped holding (−0.047, CI −0.083..−0.008); the label permutation's
observed skill went from +0.013 (p 0.002) to −0.066 (block p 0.124). Read plainly: **the engine's apparent
parity with climatology depended on situation fields coded after the fact.** Deprived of them, retrieval runs
on the market block alone for 262 of 313 events and the engine is significantly *worse* than climatology.
That is the point-in-time engine, published as computed.

## D2 findings 2 (table row) and 7 — the Big Moves threshold is full-sample. ANSWERED with a computation.
The materiality label and the analogs' `in_big_move` flags use the registered full-history top-5 %
threshold (BIG_MOVES_REGISTRATION). Computed on `fred.DCOILBRENTEU` with `big_moves.episodes_for` on
history truncated at each `as_of` year:

| as_of | obs | point-in-time threshold | episodes to date |
|---|---|---|---|
| 1992 | 1,182 | 0.229 | 3 |
| 1996 | 2,196 | 0.165 | 10 |
| 2000 | 3,200 | 0.183 | 18 |
| 2004 | 4,223 | 0.207 | 20 |
| 2008 | 5,246 | 0.196 | 28 |
| 2014 | 6,752 | 0.198 | 31 |
| 2020 | 8,281 | 0.202 | 39 |
| 2026 | 9,799 | 0.205 | 45 |
| full sample | 9,963 | 0.212 | 43 |

Of the 41 registered episodes with ≥ 500 prior observations, **2** would not clear the threshold computed
from history before their own onset. The label is stable; the read-time M call is the exposure D names.
Not changed in this brief (M is not a §7 gate and not headlined); registered as a v3 item: the M call at
read time should use the threshold from history before `as_of`. Recorded here, dated, for the next
amendment round.

## D2 findings 5 and 6 — the persistence baseline's hindsight-compiled sources. ANSWERED, disclosed.
Amendment B.1 states it. The final run shows what it means in practice: persistence built from those
sources beats the engine on G (Brier skill −0.467, RPS −0.634 in run 193022Z). A weaker, contemporaneous
persistence would make the engine look better, not worse; the comparison as published is the harder one.

## D3 finding 1 — "beats persistence" without the size correction. FIXED (Amendment F.4).
`diagnostic_fair.engine_vs_persistence` is published for P and G. A point forecast has no within-forecast
spread, so its fair CRPS equals its registered CRPS; the engine's fair CRPS is lower than its registered
one, so the correction can only raise the engine's measured advantage. Final run: P `engine_vs_persistence` registered skill +0.128 (CI +0.070..+0.185, p 3e-5); size-corrected
**+0.243 (CI +0.192..+0.303, p <1e-15)** — the correction raises the engine's advantage, as derived. G:
registered −0.600, size-corrected −0.367 (CI −0.921..−0.046, p 0.022): persistence still wins on G.

## D3 finding 2 (and §5) — the permutation test ignored the 35-day clustering. FIXED (Amendment F.2).
The block permutation (intact clusters permuted as units) is computed beside the registered i.i.d. one and
decides the §7 condition from this amendment on. Final run: 57 clusters over the 150 scored G reads (mean size 2.63). Observed skill −0.066; **block p 0.124**
(the §7 condition), i.i.d. p 0.092. Both fail to reject; the block p is the larger, in the direction D
predicted. D3's concern about the 0.008 was well founded: that p-value did not survive either the block
permutation or the point-in-time situation rule.

## D3 finding 3 — no SPA over the RPS item family. FIXED (Amendment F.3).
`G.rps.spa` runs Hansen's SPA over the RPS item family against climatology. Final run: `G.rps.spa` p_spa 0.979 (RC 1.000), best model M05_market_2x over T = 137 — the post-hoc best RPS
item is not distinguishable from chance, the same guard the Brier family had.

## D3 finding 4 — the published summary predated the persistence code. CLOSED by run 193022Z (B-5).
Four G baselines on the file; the FDR family is re-derived by the code at every run (34 comparisons in
193022Z; the count is `len(summary.json.fdr.family)`, never typed).

## D3 finding 5 — a bare "SUGGESTIVE" one JSON fetch away. FIXED (Amendment F.5).
Every item's `verdict.rules[...]["status"]` now carries its skill, DM p and the family SPA p in the string;
`status_code` keeps the bare word for programs.

## D3 §3 — the FDR family and what "survives" means.
The family covers engine-vs-each-baseline and each item-vs-climatology on the registered score; BH is
two-sided, so a survivor can be a comparison the engine *loses* (in 193022Z, three of eight). The RPS
comparisons, the permutation, the placebo and the spec curve are reported outside the family by design
(§6 lists them as separate tests of the test); D's pooled BH over all 80 p-values is the honest reader's
check and is quoted in the release check.

## Determinism (Amendment I), as evidence for D-6
Run `walk_20260902T200654Z` (the one the audit voided) and run `walk_20260902T210135Z` (this one) were two
separate full walks on the same inputs, hours apart, with only the audit's own code changed between them.
Both produced content digest `2a90ff4a88f30f6f50433a2b5268dc1feaf9bc219b5ef2ec575ef15dce57f116` and every
published number identical to the printed digit. `python3 src/walk.py --digest` prints the digest of the run
in the tree; `tests/test_walk_determinism.py` asserts the property on the synthetic corpus.

## Open (not session B's files, or Joe's)
- The M-call threshold at read time (above), v3.
- D4 (labels) and D5 (reader) are session A's.
- D2's `derived.*` series with `as_of = obs_date` in the observations table are the pipeline's
  (`fetch_*.py`); the engine-side lag of Amendment G covers the two series D showed have a real release lag.
