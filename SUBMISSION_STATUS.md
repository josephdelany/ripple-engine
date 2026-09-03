# Submission status

## Release decision

The maintained research product contains one qualified finding, one reproducible experiment, one methods paper, and one instrument demonstration. It is not release-ready until every gate below passes on the same committed revision and a new release tag is created.

## Defensible finding

On 264 walk-forward forecast dates, structural weighting scores mean CRPS 8.337 versus 8.782 for surface-class matching. The paired difference is −0.446 with 95% stationary-bootstrap interval [−0.623, −0.271]. Uniform pooling scores 8.392; structure’s −0.055 advantage over it has interval [−0.115, +0.006]. Therefore the result is that event-label filtering can discard useful precedents—not that the structural instrument has established forecasting skill beyond pooling.

## Verified release gates

- `make verify-submission`: passes.
- Frozen central outputs reproduce byte-for-byte at their recorded SHA-256 hashes.
- Default `pytest -q`: latest unscoped run passed 1,000 tests, skipped 13 environment-dependent tests, and recorded 1 expected failure, with zero unexpected failures.
- Public claims match `data/structural_surface/summary.json`.
- Local links in authoritative documents resolve.
- All tracked files are classified in `docs/audit/FILE_CLASSIFICATION.csv`.
- Former self-mutating GitHub Actions are inert under `archive/github-workflows/`.
- Superseded paper, brief, oil-findings, explanation, and résumé documents carry warnings.

## Submission contents

- `README.md`
- `docs/PAPER.md`
- `docs/RESUME.md`
- `docs/DEMO.md`
- `registrations/STRUCTURAL_SURFACE_EXPERIMENT.md`
- `src/structural_surface_experiment.py`
- `src/reproduce_structural_surface.py`
- `data/structural_surface/`

## Excluded local work

Five pre-existing modified data files and the untracked `data/walk_forward/unfiltered/` diagnostic are not part of the submission commit. They were deliberately neither staged nor discarded. The unfiltered event-walk diagnostic is legacy work and cannot alter the frozen central result.

The earlier `submission-v1.0.0` tag was issued after only a 15-test scoped gate and is retracted. It must not be submitted or cited as a verified release.

## Human-use constraint

Use only `docs/RESUME.md` for applications. Do not claim prediction of oil prices, validation of structural analogy, superiority to pooling, or a live Hormuz forecast.
