> **SUPERSEDED — NOT A CURRENT CLAIM.** Superseded design and status material for the legacy engine. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# ACCEPTANCE — is the engine ready?

> **SUPERSEDED — 2026-09-03.** This document dates from the project's v1 period (July
> 2026) and describes a "validated" portfolio that no longer exists. Every claim it calls
> validated has since been retracted or downgraded, each by a test registered before it
> ran: **H1** — geopolitical shocks amplifying ~5pp harder under volatility stress — did
> not survive a VIX-matched placebo (`docs/red_team_1.md`); **five of the six**
> stress-amplification propagation edges were retracted under a pre-registered re-test
> (`data/ripple/retraction_six.json`); the propagation chain is silent, with 21 of 477
> cells transmitting against 1–24 expected by chance (`docs/RIPPLE_FINDINGS.md`); and the
> walk-forward engine is significantly **worse** than the base rate on both targets once
> the vintage rule binds (`docs/PAPER_DRAFT.md` §8).
>
> Nothing below has been edited. This project annotates its record; it does not rewrite
> it. For the current state read `README.md`, `docs/PAPER_DRAFT.md` and `EDGE_PORTFOLIO.md`.


**One command:** `python3 src/acceptance.py` → prints **COMMISSIONED** or **DEGRADED**.

It aggregates the checks that together mean "finished and sound":
1. **the test suite passes** (`pytest -q`, 120+ hand-verifiable tests);
2. **the evaluation framework is sound** — the negative-control placebo is null and every surface agrees
   on the headline number (`data/evaluation.json`);
3. **`engine_status` is not RED** — data fresh, coverage complete, last run OK (`data/engine_status.json`);
4. **the living-engine cage + no-fabrication tests are present** (auto-growth can't fabricate);
5. **evidence packs exist** — every validated claim is receipted (`data/evidence/`).

Use `--fast` to skip the nested pytest. Any hard failure prints the reason.

## The daily commissioning glance
- `python3 src/status.py` → GREEN / AMBER / RED with reasons (or the `engine_status` MCP tool).
- `./go --refresh` → rebuild the reads, open the digest, start the cockpit.
- AMBER on "no last-run record yet" clears after the first `python3 src/daily.py` (or the launchd run).

## What "ready" means here
Ready = **sound** (placebo null, surfaces consistent, claims robust), **living** (accretes codebook-valid
live events, gated, can't fabricate), **reliable** (scheduled, self-healing, tested restore, alerts),
**broad** (six domains covered), and **inspectable** (every number one hop from its evidence pack). It
stays a **single-user, $0/keyless** personal tool held to a quality bar an Ergo quant could inspect.

*This file supersedes the earlier 10-point manual checklist; the runner is `src/acceptance.py`.*
