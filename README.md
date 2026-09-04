# Market state versus event labels in historical analogy

When analysts choose historical precedents, does recent market state carry more useful information than a surface label such as “chokepoint disruption” or “sanctions”?

This repository’s authoritative result is a registered walk-forward experiment and a separately registered explanatory ablation on 313 dated geopolitical and oil-policy events. Every method receives exactly the same prior-event pool and forecasts Brent’s 20-return abnormal return; only the weighting rule changes.

## Result

Across 264 scored forecast dates, structural weighting had mean CRPS **8.341**, versus **8.784** for surface-class weighting. The paired difference was **−0.444** (95% stationary-bootstrap interval **[−0.613, −0.269]**; Diebold–Mariano *p* = **8.65×10⁻⁷**).

That result has an essential qualification. Uniform pooling scored **8.390**. Structural weighting’s advantage over pooling was only **−0.049** (95% interval **[−0.112, +0.012]**; *p* = **0.140**). The original surface arm was also much more concentrated: median effective sample size 28.7 versus 130.2.

A registered follow-up matched market-state, combined-state, and event-class weights to the same effective sample size. Market-state matching scored **8.286** against **8.422** for class matching: difference **−0.136**, 95% interval **[−0.234, −0.038]**, Holm-adjusted *p* = **0.013**. Adding the available leadership/dyadic fields did not improve on market-only matching: difference **+0.051**, interval **[−0.001, +0.118]**, Holm-adjusted *p* = **0.114**.

> Recent oil-market state outperforms event class as an analogy rule at equal concentration. The available non-market state does not add demonstrated value, and no arm establishes production forecasting skill.

Note what that question is not. The project set out to ask whether correspondence across the wider geopolitical state beats matching on labels, and it cannot answer that. The strict point-in-time rule leaves the “structural” arm comparing four market fields on every one of its 41,997 target–candidate comparisons, two leadership fields on 50.2% of them, and one dyadic field on three. Alignment, regime and capability variables are in the catalogue and never reach the arithmetic. So what was tested is a market-and-leadership state against event labels; full structural correspondence is untested rather than refuted. The measured composition is in [the paper](docs/PAPER.md), §3.

Read [the paper](docs/PAPER.md) for the design, limitations, and interpretation. The decisions are frozen in the [central registration](registrations/STRUCTURAL_SURFACE_EXPERIMENT.md) and [ablation registration](registrations/STRUCTURAL_COMPONENT_ABLATION.md).

For applications and interviews, use only [the verified résumé language](docs/RESUME.md).
The exact release decision and gates are in [SUBMISSION_STATUS.md](SUBMISSION_STATUS.md).

## Reproduce the central experiment

Requirements: Python 3.11+ and the packages in `requirements-public.txt`.

```bash
python3 -m pip install -r requirements-public.txt
make reproduce-central
make reproduce-ablation
make test-public
```

Both reproduction targets use only committed inputs, rebuild into temporary directories, and require SHA-256 hashes to match the frozen manifests. They do not require the uncommitted research database or network access.

That is a transparent input bundle, not a fully reproducible data pipeline. The bundle reproduces the experiment exactly; the bundle itself cannot be rebuilt and checked from its upstream sources, which are partly hand-obtained, key-gated or request-gated. Run `python3 src/bundle_provenance.py` for the checked status, and see [the provenance boundary](docs/audit/PROVENANCE_BOUNDARY.md).

## Instrument demonstration

```bash
python3 src/structural_surface_demo.py
```

The demo produces one sealed retrospective read for the 2026 Hormuz closure and shows the candidate pool, structural weights, surface weights, forecast distributions, and scores. It demonstrates mechanics; one event is not validation. Details are in [docs/DEMO.md](docs/DEMO.md).

## Public-product map

- `docs/PAPER.md` — authoritative methods-and-evidence paper.
- `docs/RESUME.md` — verified résumé bullets and interview explanation.
- `registrations/STRUCTURAL_SURFACE_EXPERIMENT.md` — decisions frozen before computation.
- `registrations/STRUCTURAL_COMPONENT_ABLATION.md` — concentration and component analysis frozen before computation.
- `src/structural_surface_experiment.py` — central experiment.
- `src/structural_component_ablation.py` — registered explanatory ablation.
- `src/reproduce_structural_surface.py` — offline hash-checked reproduction.
- `src/structural_surface_demo.py` — small instrument demonstration.
- `data/structural_surface/` — inputs, sealed reads, scores, summaries, ablation, and manifests.
- `tests/test_structural_surface_*.py` — scientific and reproduction invariants.
- `docs/audit/` — adversarial audit and claim corrections.
- `SUBMISSION_STATUS.md` — release scope, verified gates, and excluded local work.

The repository also preserves the six-week research history and superseded analyses. They are not part of the authoritative claim unless the paper cites them. Recovery tag `closure-core-frozen-2026-09-03` identifies the pre-closure frozen core.

`docs/audit/PUBLIC_PRODUCT_CLOSURE.md` records what was retained, what is archival, and the state of the historical test suite. “Archival” means preserved for auditability and recovery, not endorsed as a current result.

## Scope and integrity

The project originally attempted escalation forecasting, cross-asset propagation, physical exposure, autonomous feeds, and multiple interfaces. Audit found several cases where correct code computed a different quantity from the prose. Those outputs are evidence about measurement and research design, not additional validated product claims. The central result above was rebuilt to compare structural and surface analogy on identical support, with point-in-time eligibility and an abnormal-return target.

License: [LICENSE](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).

Before submission, run `make verify-submission`. It performs exact reproduction, the complete repository test suite,
semantic claim checks, local-link validation, and classification-ledger drift detection.
