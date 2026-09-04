> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# TASK_BRIEF_10 — Cross-asset ripples (the edges layer)

Read CLAUDE.md first. All guardrails apply. Purpose: the same 42 registered
shocks, measured in markets beyond oil — the first step from oil engine to
general reaction engine. FRONTIER_AUDIT.md F7.

## Outcome

1. **Target series.** Use what the DB already holds where possible; add ONLY
   these if missing, all FRED, keyless: Henry Hub natgas spot (DHHNGSP),
   broad dollar (DTWEXBGS, already present), 5-Year Treasury constant
   maturity (DGS5), 10-Year (DGS10, if already present reuse). Register in
   `series`, wire into refresh/heartbeat like every other series.
2. **`src/cross_asset.py`** (import-only reuse of event_study logic): for
   each event and each target asset, run the same constant-mean event study
   (same windows, t−130..−11 / t−5..+20). For YIELDS, "returns" are daily
   CHANGES in the level (basis points), not log returns — CAR becomes
   cumulative abnormal change in bps; label it clearly as such.
3. **Populate `edges`.** One row per (event, asset): event_id, target
   series, CAR+5, CAR+20 (units in the row), n-days used. This is the
   edges table finally earning its place in the schema.
4. **Output `data/cross_asset_results.txt`:** per event type × asset,
   clustered mean reaction at +5/+20 with n — the "propagation map." Include
   the September 11 row explicitly in a per-event appendix (it is the
   flight-to-safety canary: oil, yields, and dollar should react in
   different directions).
5. **Widget** `propagation_map` in backend.py (table: event type × asset
   grid). Wire cross_asset into refresh.py after scenario.

## Standard

- DESCRIPTIVE ONLY. No hypotheses, no verdicts, no amplifiers — this is a
  measurement layer. Any conditioning of cross-asset ripples requires a
  future registered hypothesis (Joe's gate).
- Same clustering discipline in the summary table as robustness.py.
- Units stated on every number (% for prices, bps for yields).
- Small-n cells shouted, same as the playbook ("n=2 — ANECDOTE").
- Teach-style comments; receipts: commit cross_asset_results.txt; refresh
  ends N/N OK.

## Bounds

- No new hypotheses or verdict language. No events touched.
- Do not modify existing analysis modules (import only); refresh/heartbeat
  wiring excepted.
- Keyless FRED only — no new keys, no scraping. Ports untouched.
- If a series can't be fetched, report and continue with the others.
