# Public-product closure record

## Decision

Public HEAD is a deliberately small methods-and-evidence product: one paper, one README, one
registered central comparison, one registered explanatory ablation, one instrument demonstration,
the frozen transparent bundle, exact reproducers, audit receipts, and scientific/release tests.

The complete six-week research system is preserved at annotated tag
`full-research-archive-2026-09-03`. Before removal, every one of the 1,700 archival paths was checked
to exist at that tag. Public HEAD removed 971 planning/narrative files, 302 legacy generated-data
files, 226 legacy scientific-code files, 147 historical tests, 48 interface/operations files, and
6 already-archived files. This was separation, not erasure.

Five legacy source files remain because the paper cites their exact lines when explaining withdrawn
claims: `src/engine/read.py`, `src/walk.py`, `src/situation_vintage.py`, `src/state/ies90.py`, and
`src/engine/persistence.py`. They are audit evidence, not maintained product code.

## What was verified before separation

Immediately before slimming, the populated historical repository completed with **1,038 passed,
13 explicitly skipped, 1 expected failure, and zero unexpected failures**. Both frozen public
analyses reproduced exactly, and all claim/link/provenance guards passed. That receipt describes the
archive tag, not the smaller suite now collected by public HEAD.

An earlier release reported a scoped 15-test result as if it were repository verification. That
statement is retracted. The previously excluded failures were repaired, full collection was
restored, and test writers that mutated committed outputs were redirected to temporary files.

## Public release gate

`make verify-submission` is the complete public-HEAD gate. It:

1. reproduces the central and ablation artifacts byte-for-byte;
2. runs every test retained in public HEAD;
3. checks every quantitative public claim against the frozen JSON;
4. verifies citation metadata and local links;
5. checks document status and the complete retained-file classification; and
6. fails if verification changes the checkout.

This gate does not pretend to rerun the archived autonomous engine or reconstruct `data/oil.db`.
Those capabilities and their historical tests exist at the archive tag. The public bundle itself is
exactly reproducible; its upstream database/source chain is only auditable, as documented in
[`PROVENANCE_BOUNDARY.md`](PROVENANCE_BOUNDARY.md).

## Confirmed legacy provenance defect

At the archive tag, `docs/OIL_FINDINGS.md` and `docs/RESUME_AND_APPLICATION.md` cite
`data/ripple/stage0.json`, while their generator writes `data/magnitude/stage0.json`
(`src/magnitude_stage0.py:42,332` in that revision). Those documents and outputs are not public
claims.

## Do not claim

- Do not say the maintained method beats uniform pooling at 20 trading days.
- Do not present the 2026 Hormuz demonstration as validation or a live forecast.
- Do not describe modern dataset-release dates as historical information availability.
- Do not describe legacy same-class reranking as structural-versus-surface analogy.
- Do not claim that full geopolitical structural correspondence was tested.
- Do not import archived escalation, propagation, or physical-exposure results into the headline.
