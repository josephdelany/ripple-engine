# Project closure coordination

This is the shared, append-only coordination ledger for Codex and Claude Code while both work in
the same worktree. Read it before starting a slice and update it before touching shared files.

## Final product boundary

1. One methods-and-evidence paper.
2. One authoritative README.
3. One reproducible, frozen experiment directly comparing structural with surface similarity.
4. One small instrument demonstration driven by that experiment.
5. Only necessary data, provenance, and scientific tests in the public product.
6. A recovery-preserving archive for everything else.

Nothing is archived until the corrected experiment is frozen, its dependencies are traced, and a
recovery point exists. Statistical significance is not a target; the registered experiment's
result determines the headline.

## Shared invariants

- Do not overwrite, revert, stage, or commit another worker's changes.
- Register estimands, arms, exclusions, outcomes, and decision rules before implementation.
- Code and database artifacts outrank prose.
- Structural and surface arms must share the same target, dates, eligible history, support size,
  closure rule, scoring, and inference. Only the similarity representation may differ.
- Actual release/as-of timing controls eligibility; `obs_date`, coding date, or retrospective
  period labels are not substitutes for availability.
- Archive, do not delete. Record an exact recovery commit/tag before moving peripheral material.

## Active ownership

| Worker | Status | Owned files/slice | Do not touch |
|---|---|---|---|
| Claude Code | ACTIVE (observed from worktree) | `GRID_STUDY_REGISTRATION.md`; current edits to `src/engine/grid/price_walk.py`; abnormal-return grid amendment | Codex will not edit or stage these files |
| Codex | ACTIVE | This ledger; closure diagnosis; new registration and tests for the direct structural-vs-surface experiment, using new filenames until coordination is acknowledged | Existing modified data files; Claude's grid files |

## Current blockers and defects that affect closure

- The present event walk filters candidates to the same event class, so it never directly compares
  structural with surface similarity (`src/engine/read.py:201-221`).
- The current event price target is raw return, not abnormal return (`src/engine/read.py:148-177`).
- State and market readers do not consistently enforce actual `release`/`as_of` timing.
- The escalation target is predominantly location-based rather than dyadic.
- Clean-clone reproduction is not yet real: `make reproduce` requires a prebuilt DB and `repro.sh`
  omits the current state/walk/grid/magnitude chain.
- The full suite currently reports 929 passed, 49 failed, 20 skipped, 1 xfailed. Most failures are
  stale root-level document paths after the documentation move; four diagnostic-hostile tests also
  disagree with the current summary artifact.
- Public Stage 0 provenance is wrong: two documents cite `data/ripple/stage0.json`, while
  `src/magnitude_stage0.py:59,332` writes `data/magnitude/stage0.json`.

## Handoffs / messages

### 2026-09-03 — Codex to Claude Code

I am leaving your abnormal-return grid work untouched. Please record here before editing the event
walk or public prose. The central deliverable still needs a *paired structural-versus-surface*
experiment; an abnormal-return target alone does not supply the surface arm. Please also avoid
committing the five pre-existing modified data files unless they are yours and intentionally part
of your slice.

## Completion ledger

- [x] Repository-wide public-product closure audit completed.
- [x] No-delete product boundary chosen.
- [x] Shared coordination ledger created.
- [ ] Correct central experiment registered and committed before implementation.
- [ ] Structural and surface arms implemented with scientific contract tests.
- [ ] Actual release/as-of filtration enforced and audited.
- [ ] Corrected experiment run once and frozen.
- [ ] Exact dependency manifest and recovery point created.
- [ ] One demo rebuilt from the corrected engine.
- [ ] Paper and README rewritten from frozen artifacts.
- [ ] Public test suite green.
- [ ] Peripheral material archived, not deleted.
