> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# Task Brief 01 — Inventories adapter + the registered H1–H3 run

*Read CLAUDE.md first. Its rules override anything here. Work top to bottom; commit after each numbered step; stop and report if anything forces a design change.*

## Precondition (Joe does this part first)
The EIA API key is stored in `~/.openbb_platform/user_settings.json` under `credentials.eia_api_key`. If it's missing, STOP and tell Joe — do not proceed with a workaround, do not scrape.

## Step 1 — EIA inventories adapter (`src/fetch_eia.py`)
Fetch **Weekly US Ending Stocks of Crude Oil excluding SPR** (EIA series WCESTUS1) via the EIA v2 API, full history, using the key read from `~/.openbb_platform/user_settings.json`. Follow the exact pattern of `src/fetch_cot.py`: write a `series` row (entity `commodity.wti`, unit "thousand bbl", frequency weekly, source EIA, real source_url, and a mechanism note: "H2 conditioning input: thin physical buffers cannot absorb supply risk, so price must") and insert observations as `eia.crude_stocks_xspr` with provenance timestamps. Print row count and date range. Commit.

## Step 2 — Inventory tightness signal (in `src/derive_signals.py`)
Add `derived.inv_sigma`: the deviation of current stocks from their **seasonal norm**, in standard deviations — i.e., for each week-of-year, compare the latest reading against the mean/std of the same week-of-year over the trailing 5 years. Negative = tighter than normal. Register it in MECHANISMS with the H2 mechanism string. Forward-fill onto the daily index the same way cot_pct does. Add `"derived.inv_sigma": "Inv σ"` to STATE_VARS in `src/conditioned_study.py`. Run `derive_signals.py`; confirm the new signal appears with a sane current value (typically between −3 and +3). Commit.

## Step 3 — THE REGISTERED RUN (this is the moment; do it exactly once, cleanly)
Run, in order: `python3 src/load_events.py`, `python3 src/derive_signals.py`, `python3 src/conditioned_study.py`, `python3 src/robustness.py`.
Then extend `src/robustness.py` so its clustered/no-outlier comparison runs for ALL THREE registered variables (vix_pct, inv_sigma, cot_pct), not just VIX, and run it again.
Save the complete output (event-level table + all three conditioning splits, raw AND clustered) to `data/registered_run_results.txt`. Apply the pre-registered decision rule from BRIEF_SKELETON.md §4 (+5pp clustered = holds) and append a three-line verdict: H1 holds/fails, H2 holds/fails, H3 holds/fails. **Report verdicts exactly as computed — no reframing, no softening.** Commit with message "Registered run: H1–H3 results".

## Step 4 — Refresh outputs
Re-run `src/event_study.py` and `src/conditioned_study.py` so ripple.png and conditioned_ripple.png reflect the final data. Verify `src/backend.py` still serves all widgets (curl localhost:5050/state_of_system returns the new signals). Commit.

## Explicitly OUT of scope
No new tables. No new hypotheses. No GDELT, no automation, no dashboard changes beyond verifying it still works. No edits to BRIEF_SKELETON.md — Joe and his architect write the Results section themselves, from data/registered_run_results.txt.

## Done when
`data/registered_run_results.txt` exists with the three verdicts, everything is committed, and both servers still answer.
