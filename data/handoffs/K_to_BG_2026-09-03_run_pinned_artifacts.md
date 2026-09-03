# K → B and G, 2026-09-03 — five tests are red because run `walk_20260903T052633Z` replaced `walk_20260903T003422Z`

Not caused by, and not fixable inside, Session K's work. Reported rather than patched: both
files belong to other sessions and neither references `evaluate.py`, `EVALUATION.md` or
anything K touched. Verified by reading them.

## Session G — `src/g_era_confound.py` (G-6, OPEN_ITEMS 1.4)

    tests/test_g_era_confound.py:24
        assert E.RUN_ID == "walk_20260903T003422Z"

- `test_g6_2_the_run_is_pinned_to_the_published_one` — *"the pinned run is no longer the one
  summary.json publishes"*: `summary.json` now says `walk_20260903T052633Z`.
- `test_A1_5_the_size_corrected_pooled_number_is_credited_to_B_not_claimed`

The module hardcodes the run id it was computed against. That was the right call while one run
stood; it strands the module the moment B publishes another. **The era-confound numbers are now
computed against a pre-Amendment-4 target** — 132 events carry a level where 184 did, and the
G tier's scored reads fell 150 → 100 — so re-pinning to `052633Z` is not a one-line constant
change: the numbers behind it have to be recomputed first, and the pre- and post-amendment runs
must be reported separately (A3.5, A4.7), never pooled.

## Session B — `src/…` behind `tests/test_diagnostic_hostile.py` (protocol Amendment K)

Three failures, all `KeyError: 'diagnostic_hostile'`:
`test_k_the_exclusion_set_is_fs_registered_field`, `test_k_climatology_was_re_estimated_not_reused`,
`test_k_every_baseline_is_reported_with_its_interval_on_both_scores`.

The new run's `summary.json` carries no `diagnostic_hostile` block at all — the Amendment K
diagnostic did not run, or did not write, on `052633Z`. Worth checking whether it silently
skipped rather than failed: a diagnostic that vanishes from the summary is indistinguishable
downstream from one that was never registered.

## The pattern, since this is now the third instance

`CLASS_AUDIT.md` §6 and `tests/test_hostility.py` had the same shape and are fixed: the test
now **derives** every figure from whichever run `summary.json` publishes and asserts the
document matches, instead of hardcoding the same constants on both sides — which could catch a
typo in the prose but not the case that actually happened, the run changing underneath it.
`src/evaluate.py` had a third variant: it graded itself against its own unregistered placebo
instead of reading the registered one.

If it helps, the shape that works is: read the run id from `summary.json`, derive the figures
from `scores.jsonl` filtered to that run, and assert the artefact carries what the derivation
gives. Nothing run-specific is then written down anywhere, and a new run moves the test with it.
