# Market state versus event labels in historical analogy

When analysts choose historical precedents, does recent market state carry more useful information than a surface label such as “chokepoint disruption” or “sanctions”?

This repository’s authoritative result is a registered walk-forward experiment and a separately registered explanatory ablation on 313 dated geopolitical and oil-policy events. Every method receives exactly the same prior-event pool and forecasts Brent’s 20-trading-day abnormal return; only the weighting rule changes.

The catalogue spans 1973–2026, but the scored daily backtest does not: its 264 forecast dates run
from 2001-09-11 through 2026-06-17, and 147 (55.7%) fall in the 2020s. This is a recent-era daily
experiment, not a 53-year quantitative backtest.

## Result

Across 264 scored forecast dates, the registered combined-state weighting had mean CRPS **8.341**, versus **8.784** for surface-class weighting. The paired difference was **−0.444** (95% stationary-bootstrap interval **[−0.613, −0.269]**; Diebold–Mariano *p* = **8.65×10⁻⁷**).

That result has an essential qualification. Uniform pooling scored **8.390**. Combined-state weighting’s advantage over pooling was only **−0.049** (95% interval **[−0.112, +0.012]**; *p* = **0.140**). The original surface arm was also much more concentrated: median effective sample size 28.7 versus 130.2.

A registered follow-up matched market-state, combined-state, and event-class weights to the same effective sample size. Market-state matching scored **8.286** against **8.422** for class matching: difference **−0.136**, 95% interval **[−0.234, −0.038]**, Holm-adjusted *p* = **0.013**. Under the registered event-level aggregation, adding the sparse leadership/dyadic fields scored **+0.051** worse than market-only matching (interval **[−0.001, +0.118]**; Holm-adjusted *p* = **0.114**). That contrast does not test properly represented relational geopolitics: numeric values for multiple event entities were averaged before comparison.

> Recent oil-market state outperforms event class as an analogy rule at equal concentration. No arm establishes production forecasting skill, and the experiment does not determine whether role-preserving geopolitical structure adds value.

Note what that question is not. The project set out to ask whether correspondence across the wider geopolitical state beats matching on labels, and it cannot answer that. The registered file-release rule leaves the “combined-state” arm comparing four market fields on every one of its 41,997 target–candidate comparisons, two leadership fields on 50.2% of them, and one dyadic field on three. Alignment, regime and capability variables are in the catalogue and never reach the arithmetic. Multi-entity numeric values are also averaged into a single event value, erasing actor roles. So what was tested is market state, sometimes augmented by an event-level leadership aggregate, against event labels; full relational structural correspondence is untested rather than refuted. The measured composition is in [the paper](docs/PAPER.md), §3.

## Why it matters

The result separates three claims that commentary often conflates. A method can outperform
headline-category matching without demonstrating useful prediction; an apparent analogy advantage
can largely reflect how concentrated its weights are; and a model called “structural” tests only
the structure that its data representation actually preserves. The contribution is therefore both
substantive—market context beats event class in the matched comparison—and methodological: analogy
rules should be tested on identical support, at equal concentration, against unrestricted pooling.

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
- `src/reproduce_structural_component_ablation.py` — offline hash-checked ablation reproduction.
- `src/structural_surface_demo.py` — small instrument demonstration.
- `data/structural_surface/` — inputs, sealed reads, scores, summaries, ablation, and manifests.
- `tests/test_structural_surface_*.py` — scientific and reproduction invariants.
- `docs/audit/` — adversarial audit and claim corrections.
- `SUBMISSION_STATUS.md` — release scope, verified gates, and excluded local work.

The complete six-week research history and superseded analyses are preserved at recovery tag
`full-research-archive-2026-09-03`; they are intentionally absent from public HEAD.

`docs/audit/PUBLIC_PRODUCT_CLOSURE.md` records what was retained, what moved to the archive tag, and
the distinct verification receipts for the historical and public trees.

## Scope and integrity

The project originally attempted escalation forecasting, cross-asset propagation, physical exposure, autonomous feeds, and multiple interfaces. Audit found several cases where correct code computed a different quantity from the prose. Those outputs are evidence about measurement and research design, not additional validated product claims. The central result above was rebuilt to compare registered combined-state and surface-class weighting on identical support, with point-in-time eligibility and an abnormal-return target.

License: [LICENSE](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).

Before submission, run `make verify-submission`. It performs exact reproduction, the complete repository test suite,
semantic claim checks, local-link validation, and classification-ledger drift detection.
