# Structural versus surface historical analogy

Can a geopolitical forecasting instrument do better by comparing the full observable state around past events rather than matching a surface label such as “chokepoint disruption” or “sanctions”?

This repository’s authoritative result is a registered, walk-forward comparison on 313 dated geopolitical and oil-policy events. Both methods receive exactly the same prior-event pool and forecast the same outcome: Brent’s 20-trading-day abnormal return. The only intended difference is how they weight history.

## Result

Across 264 scored forecast dates, structural weighting had mean CRPS **8.337**, versus **8.782** for surface-class weighting. The paired difference was **−0.446** (95% stationary-bootstrap interval **[−0.623, −0.271]**; Diebold–Mariano *p* = **1.57×10⁻⁶**).

That result has an essential qualification. Uniform pooling scored **8.392**. Structural weighting’s advantage over pooling was only **−0.055** (95% interval **[−0.115, +0.006]**; *p* = **0.090**), while surface-class weighting was materially worse than pooling. The defensible conclusion is:

> Strict structural weighting beats surface-class matching, but at the registered 20-day horizon it does not distinguishably beat pooling. Most of the measured gap comes from surface selection doing harm.

This is professionally consequential without being a claim of production forecasting skill: an analyst should not narrow precedent by event label and assume the remaining cases are more informative.

Read [the paper](docs/PAPER.md) for the design, limitations, and interpretation. See [the registration](registrations/STRUCTURAL_SURFACE_EXPERIMENT.md) for the frozen decision rules.

For applications and interviews, use only [the verified résumé language](docs/RESUME.md).

## Reproduce the central experiment

Requirements: Python 3.11+ and the packages in `requirements.txt`.

```bash
python3 -m pip install -r requirements.txt
make reproduce-central
make test-public
```

`make reproduce-central` uses only the committed, transparent input bundle in `data/structural_surface/input/`. It rebuilds the sealed reads, scores, and summary in a temporary directory and requires their SHA-256 hashes to match the frozen manifest. It does not require the uncommitted research database or network access.

## Instrument demonstration

```bash
python3 src/structural_surface_demo.py
```

The demo produces one sealed retrospective read for the 2026 Hormuz closure and shows the candidate pool, structural weights, surface weights, forecast distributions, and scores. It demonstrates mechanics; one event is not validation. Details are in [docs/DEMO.md](docs/DEMO.md).

## Public-product map

- `docs/PAPER.md` — authoritative methods-and-evidence paper.
- `docs/RESUME.md` — verified résumé bullets and interview explanation.
- `registrations/STRUCTURAL_SURFACE_EXPERIMENT.md` — decisions frozen before computation.
- `src/structural_surface_experiment.py` — central experiment.
- `src/reproduce_structural_surface.py` — offline hash-checked reproduction.
- `src/structural_surface_demo.py` — small instrument demonstration.
- `data/structural_surface/` — inputs, sealed reads, scores, summary, and manifest.
- `tests/test_structural_surface_*.py` — scientific and reproduction invariants.
- `docs/audit/` — adversarial audit and claim corrections.

The repository also preserves the six-week research history and superseded analyses. They are not part of the authoritative claim unless the paper cites them. Recovery tag `closure-core-frozen-2026-09-03` identifies the pre-closure frozen core.

`docs/audit/PUBLIC_PRODUCT_CLOSURE.md` records what was retained, what is archival, and the state of the historical test suite. “Archival” means preserved for auditability and recovery, not endorsed as a current result.

## Scope and integrity

The project originally attempted escalation forecasting, cross-asset propagation, physical exposure, autonomous feeds, and multiple interfaces. Audit found several cases where correct code computed a different quantity from the prose. Those outputs are evidence about measurement and research design, not additional validated product claims. The central result above was rebuilt to compare structural and surface analogy on identical support, with point-in-time eligibility and an abnormal-return target.

License: [LICENSE](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).
