# ACCEPTANCE — is the engine ready?

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
