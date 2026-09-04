> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A registration for a superseded study, kept so its pre-commitments stay auditable. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

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

## The honest record (updated as N grew via the human-gated corpus expansion)
- **n=20 (registered, frozen):** H1 HOLDS (+10.3pp), H2 HOLDS (+5.4pp), H3 REJECTED (-6.8pp).
- **n=52 (expanded re-test):** H1 HOLDS (+7.4pp, CI excludes 0, survives FDR@10%);
  **H2 FAILS (+2.9pp)** — decays below the +5pp bar; H3 rejected (-6.9pp).
- **n=161 (expanded re-test, 2026-07-29):** **H1 HOLDS (+5.0pp, 95% CI [+1.1,+9.0] excludes 0,
  perm p=0.005, survives BOTH FDR@10% AND Bonferroni@5%)** — the effect STRENGTHENED under
  more data + multiple-testing correction, the hallmark of a real edge. **H2 FAILS (-0.8pp,
  now wrong-signed, CI includes 0)** — the n=20 "HOLDS" was small-sample noise. H3 REJECTED
  (-3.9pp). See `data/validation_claims.json`.
- **Analogue forecaster at big-N:** the OOS null SURVIVED the corpus growth (N scored 42→105):
  CPCV skill -0.14 (7% of paths beat base), PBO 0.0, Diebold-Mariano p=0.0002 (base rate
  significantly better). More N did NOT manufacture an edge — a genuine absence of signal, not
  a small-sample artifact. See `data/validation_analogue.json`.

**Bottom line:** the one conditioning edge (H1 — geopolitical shocks ripple harder when VIX
stress is already elevated) is now validated at N=161 to the strictest bar; the two candidate
edges that failed (H2, the analogue) failed harder with more data. Rigor + N did its job.

## The rule going forward (Phase B)
Maximize N, but keep integrity: the fixed hypotheses/directions/windows do not change; each
newly added event is an OUT-OF-SAMPLE test the registered run never saw, tracked in the
ledger. We report expansions alongside the frozen n=20 anchor — we do not re-run the in-sample
split repeatedly and cherry-pick a look. "Re-baseline" means report on the bigger sample
honestly, not overwrite the pre-registration.
