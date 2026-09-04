# Submission status

## Release decision

The maintained research product contains one qualified finding, one reproducible central experiment, one registered explanatory ablation, one methods paper, and one instrument demonstration. This revision is the verified v2.0.1 release.

## Defensible finding

On 264 walk-forward forecast dates from 2001-09-11 through 2026-06-17, the original combined-state arm scores mean CRPS 8.341 versus 8.784 for the concentrated event-class arm (difference −0.444; interval [−0.613, −0.269]), while remaining indistinguishable from uniform pooling at 8.390 (difference −0.049; interval [−0.112, +0.012]). Of those dates, 147 (55.7%) are in the 2020s. In the registered explanatory ablation, market-state matching and event-class matching were calibrated to the same effective sample size: CRPS 8.286 versus 8.422, paired difference −0.136, 95% interval [−0.234, −0.038], Holm-adjusted *p*=0.013. The registered event-level nonmarket aggregation scores +0.051 worse than market alone (interval [−0.001, +0.118]; Holm-adjusted *p*=0.114), but multi-entity numeric values were averaged and dyadic coverage was nearly absent. The finding is market context over headline category in this recent-era sample—not evidence against relational geopolitical structure, validation of full-state analogy, or production forecasting skill.

## Verified release gates

- `make verify-submission`: passed on the release candidate and in a detached clean worktree.
- Frozen central outputs reproduce byte-for-byte at their recorded SHA-256 hashes.
- Pre-separation archive receipt: the complete historical tree passed 1,038 tests, explicitly skipped 13 condition-dependent tests, recorded 1 expected failure, and had zero unexpected failures. It is preserved at `full-research-archive-2026-09-03`.
- Current public tree and detached clean worktree: all 57 retained tests pass with zero skips or expected failures.
- Public claims match the frozen central and ablation summaries.
- Local links in authoritative documents resolve.
- All tracked files are classified in `docs/audit/FILE_CLASSIFICATION.csv`.
- Autonomous feeds, dashboards, superseded papers, duplicate narratives, and their operational tests are absent from public HEAD and recoverable at the archive tag.

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

Earlier `submission-v1.0.0`, `submission-v1.0.1`, and `submission-v2.0.0` tags predate the final relational-aggregation correction and must not be submitted or cited as the current verified release.

## Human-use constraint

Use only `docs/RESUME.md` for applications. Do not claim prediction of oil prices, validation of structural analogy, superiority to pooling, or a live Hormuz forecast.
