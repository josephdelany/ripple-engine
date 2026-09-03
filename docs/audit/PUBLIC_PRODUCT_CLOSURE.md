# Public-product closure record

## Decision

The maintained product is one methods-and-evidence paper, one README, one registered structural-versus-surface experiment, one small demonstration, its transparent input bundle, and its scientific tests. Everything else is retained as an archive of the six-week research process, not as an additional public claim.

This is a logical archive rather than a destructive file purge. It preserves provenance, avoids breaking paths while another coding session is active, and keeps every prior artifact recoverable. The git tag `closure-core-frozen-2026-09-03` is the recovery point. The authoritative surface is enumerated in `README.md`; files outside that map are historical unless the paper cites them.

## Repository-wide classification

Every tracked file was classified during closure by path and role. The exhaustive ledger is
`docs/audit/FILE_CLASSIFICATION.csv`; regenerate it with `python3 src/classify_public_product.py`.

- **Maintained core:** registration, central implementation, reproducer, demonstration, frozen transparent inputs/outputs, README, paper, codebook, and central tests.
- **Required dependency:** inference/scoring code and the world-state codebook directly read by the central implementation.
- **Evidence/audit:** audit reports and the abnormal-return comparison cited to explain corrected design choices.
- **Archive—scientific:** prior experiments, outputs, registrations, and tests not used by the central claim.
- **Archive—interface/operations:** dashboards, APIs, feeds, agents, launch configuration, and operational documentation.
- **Archive—planning/narrative:** scaffolding, handoffs, duplicate papers, briefs, application prose, and historical plans.
- **Archive—generated/data:** generated ledgers and datasets not present in the committed central input bundle.

Generated artifacts, repetitive dossiers, tests, interfaces, and planning files were classified mechanically. Claim-producing code and the files capable of affecting the paper, central experiment, retained measurement evidence, demonstration, provenance, or reproduction received the substantive audit described in `docs/audit/00_INDEX.md` and the closure work.

## Frozen evidence

`make reproduce-central` was run after the final diagnostics. It reproduced `reads.jsonl`, `scores.jsonl`, and `summary.json` exactly at the SHA-256 values in `data/structural_surface/manifest.json`. The maintained test gate is `make test-public`: 11 tests pass.

The complete historical suite was also run at closure: **991 passed, 13 skipped, 1 expected failure, and 5 failed** out of 1,009. None of the five affects the central experiment. One is a networked ICB loader test that attempts a Duke download in an offline environment. Four are guards tied to the superseded README/figure/citation publication system. They remain visible rather than being weakened to create a cosmetically green historical suite.

## Confirmed provenance defect

The superseded `docs/OIL_FINDINGS.md` and `docs/RESUME_AND_APPLICATION.md` cite `data/ripple/stage0.json`, but the generator writes `data/magnitude/stage0.json` (`src/magnitude_stage0.py:42,332` in the audited revision). Therefore those documents do not point to their generating artifact. Neither document is part of the authoritative public claim.

## Do not claim

- Do not say the structural method beats pooling at 20 trading days.
- Do not present the 2026 Hormuz demonstration as validation.
- Do not describe coding dates as historical information-availability dates.
- Do not describe legacy same-class reranking as a test of structural versus surface analogy.
- Do not import escalation or propagation results into the central headline without a new claim-level audit.
