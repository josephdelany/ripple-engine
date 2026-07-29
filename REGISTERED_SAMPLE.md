# The registered sample — frozen (do not edit)

`data/registered_sample_n20.csv` is the **immutable** 20-event sample the pre-registered
H1/H2/H3 study was run on, once, on 2026-07-21 (git `a3470ce6`). It is frozen here so the
registered result stays reproducible forever, independent of how large the live `events`
table grows.

## Why this exists
The pre-registration (`BRIEF_SKELETON.md` §4) is "run once" on a fixed sample. The live
`events` table has since grown (20 → 30 → 42 → 52, history loaded back to 1987) via the
human-gated corpus expansion. `robustness.py` reads the *current* table, so it recomputes on
the grown sample — which is legitimate as an EXPANDED, reported-alongside re-test, but is NOT
the registered run. Without this frozen copy the registered numbers were not reproducible.

## The honest record
- **n=20 (registered, frozen):** H1 HOLDS (+10.3pp), H2 HOLDS (+5.4pp), H3 REJECTED (-6.8pp).
- **n=52 (current, expanded re-test):** H1 HOLDS (+7.4pp, 95% CI excludes 0, survives FDR@10%),
  **H2 FAILS (+2.9pp)** — decays below the +5pp bar as N grows → the H2 result was partly
  sample-dependent. H3 still rejected (-6.9pp). See `data/validation_claims.json`.

## The rule going forward (Phase B)
Maximize N, but keep integrity: the fixed hypotheses/directions/windows do not change; each
newly added event is an OUT-OF-SAMPLE test the registered run never saw, tracked in the
ledger. We report expansions alongside the frozen n=20 anchor — we do not re-run the in-sample
split repeatedly and cherry-pick a look. "Re-baseline" means report on the bigger sample
honestly, not overwrite the pre-registration.
