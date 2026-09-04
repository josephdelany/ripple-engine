# Submission status

## Release decision

The maintained research product contains one qualified finding, one reproducible central experiment, one registered explanatory ablation, one methods paper, and one instrument demonstration. This revision is a release candidate until every gate below is rerun from a clean checkout and a replacement release tag is created.

## Defensible finding

On 264 walk-forward forecast dates, the original combined-state arm scores mean CRPS 8.341 versus 8.784 for the concentrated event-class arm (difference −0.444; interval [−0.613, −0.269]), while remaining indistinguishable from uniform pooling at 8.390 (difference −0.049; interval [−0.112, +0.012]). In the registered explanatory ablation, market-state matching and event-class matching were calibrated to the same effective sample size: CRPS 8.286 versus 8.422, paired difference −0.136, 95% interval [−0.234, −0.038], Holm-adjusted *p*=0.013. Adding the available leadership/dyadic state does not improve on market alone: +0.051, interval [−0.001, +0.118], Holm-adjusted *p*=0.114. The finding is market context over headline category—not validation of full-state analogy or production forecasting skill.

## Verified release gates

- `make verify-submission`: must be rerun on this release candidate.
- Frozen central outputs reproduce byte-for-byte at their recorded SHA-256 hashes.
- Populated research environment: default `pytest -q` passed 1,032 tests, explicitly skipped 13 condition-dependent tests, and recorded 1 expected monthly-tier failure, with zero unexpected failures.
- Clean committed checkout: exact reproduction passed; 348 deterministic tests passed, 619 database-dependent and 52 other condition-dependent tests were explicitly skipped, and zero tests failed. This is not presented as full integration coverage because the gitignored research database cannot be reconstructed from the repository alone.
- Public claims match the frozen central and ablation summaries.
- Local links in authoritative documents resolve.
- All tracked files are classified in `docs/audit/FILE_CLASSIFICATION.csv`.
- Former self-mutating GitHub Actions are inert under `archive/github-workflows/`.
- Superseded paper, brief, oil-findings, explanation, and résumé documents carry warnings.
- The run emitted four non-failing dependency/encoding warnings: three from legacy FastAPI/Starlette APIs and one from a Stata file decoded with its documented Latin-1 fallback.

## Submission contents

- `README.md`
- `docs/PAPER.md`
- `docs/RESUME.md`
- `docs/DEMO.md`
- `registrations/STRUCTURAL_SURFACE_EXPERIMENT.md`
- `registrations/STRUCTURAL_COMPONENT_ABLATION.md`
- `src/structural_surface_experiment.py`
- `src/structural_component_ablation.py`
- `src/reproduce_structural_surface.py`
- `src/reproduce_structural_component_ablation.py`
- `data/structural_surface/`

## Excluded local work

Ignored research databases, raw source distributions, caches, backups, and the legacy `data/walk_forward/unfiltered/` diagnostic are not release contents. They cannot alter the committed frozen results. Their role and the upstream reproducibility boundary are stated in `docs/audit/PROVENANCE_BOUNDARY.md`.

The earlier `submission-v1.0.0` tag was issued after only a 15-test scoped gate and is retracted. It must not be submitted or cited as a verified release.

## Human-use constraint

Use only `docs/RESUME.md` for applications. Do not claim prediction of oil prices, validation of structural analogy, superiority to pooling, or a live Hormuz forecast.
