# Ripple Engine

A personal, **pre-registered event-study engine** — a **measurement and grounding
instrument** for how geopolitical shocks move oil prices. It documents *what
happened* (a sourced, point-in-time event corpus), *what history says* about events
of that class (conditioned event-study distributions with honest CIs), and *what
state the market is in*. It **does not claim predictive edge** — the calibration
record is published and is near baseline (see `EVALUATION.md`). It is a research
instrument, not a newsreader: every number is one hop from the evidence that produced
it, and failed hypotheses are reported, not buried. It runs on free, keyless,
reproducible data — a **provenance/integrity guarantee (sourced, reproducible, no
fabrication), not evidence that any finding is correct**.

Flagship build for the News-to-Markets project. Single-user tool, held to a bar a
quant could inspect.

## The headline finding

**No conditioning effect survives standardized, regime-robust testing; the raw
amplification result was volatility clustering, exposed by a matched placebo.
Descriptive findings stand: conflict events average near-zero with large dispersion;
SPR releases show the strongest measured effect; the 289-event two-source dataset and
full adversarial review are published.**

This is the settled result of the first external adversarial review (red-team-1). The
"VIX-stress amplifies the oil ripple" (H1) headline had been computed on raw `|CAR|`,
a volatility quantity split by a volatility index. Under BMP-standardized abnormal
returns (SAR — the correct metric) the amplification does not survive at any tier, and
a VIX-matched **non-event** placebo reproduces the raw number — so it was
vol-clustering. Under one consistent evidentiary bar (`EVALUATION.md` §0) **no edge in
the portfolio is `validated`; all are SUGGESTIVE**, reported with their nulls
(including the gasoline-crack edge CC2: +1.16 $/bbl [−0.22, +2.56] under the strictest
cut). The H1 number, shown as a ranked block — SAR is the metric; raw `|CAR|` is a
secondary, vol-clustering-prone line:

| tier | corpus | raw `\|CAR\|` amp | SAR amp (metric) |
|---|---|---|---|
| **1. frozen registered** | N=289 (frozen 2026-07-30) | +5.00pp [0.86, 8.95] | **+0.16σ [−0.25, +0.52]** — incl. 0 |
| **2. out-of-sample** (frozen pre-2019 threshold) | 2019+ (n=16) | +2.92pp [−12.34, 18.92] | **+0.60σ [−0.32, +1.62]** — incl. 0 |
| **3. current tracking** | N=296 (grows) | +6.07pp [0.99, 9.87] | **+0.30σ [−0.21, +0.67]** — incl. 0 |

The genuinely-immutable registered-sample headline (n=20) was +10.3pp on raw `|CAR|`.
That a "validated" flagship did not survive adversarial standardization — and that the
downgrade is published — is the integrity result. Full disposition and every number:
`docs/red_team_1.md`, `data/NUMBERS.md`, `EDGE_PORTFOLIO.md`, `EVALUATION.md`.

## Is it sound? One command

```
python3 src/acceptance.py        # prints COMMISSIONED or DEGRADED
```

It aggregates the checks that together mean "finished and sound": the test suite
passes, the evaluation framework is sound (placebo null + every surface agrees on
the headline number), `engine_status` is not RED, the no-fabrication cage tests
are present, and every validated claim has an evidence pack. See
`ACCEPTANCE_TEST.md` for what each check means.

## The daily glance

```
python3 src/status.py            # GREEN / AMBER / RED, with reasons
./go --refresh                   # rebuild the reads, open the digest, start the cockpit
python3 src/backend.py           # the OpenBB cockpit surface on http://127.0.0.1:5050
```

## Reproduce every number from zero

```
bash repro.sh                    # 23 steps: schema -> free fetches -> corpus -> signals -> analyses
```

From a fresh clone this rebuilds `data/oil.db` in the one order that works —
schema, every free data fetch (FRED prices & macro, EIA inventories, CFTC COT,
GPR), the human-approved event corpus, the derived signals, and the analyses.
Every paper's numbers are reproducible against the committed inputs;
`data/repro_log.txt` is the receipt. `data/oil.db` itself is a derived artifact
(gitignored) — never hand-edited, always rebuilt.

## What's inside

- **The corpus** — 296 verified geopolitical/energy events across six domains
  (energy, macro, commodities, Middle-East risk, conflict, geopolitics), each
  carrying a real `source_url` + `retrieved_at`. Grows only via a caged LLM
  extractor that **cannot fabricate** (`extract_events.py` → `admit_events.py`);
  the registration sample stays frozen at N=289 so growth never contaminates the
  pre-registered test. Coding rules: `../EVENTS_CODEBOOK.md`.
- **The analysis** — event study + state-conditioned study (VIX / EIA inventories
  / COT, measured point-in-time at t−1) + robustness, run once against a binding
  pre-registration (H1–H3, fixed decision rule). `src/event_study.py`,
  `src/conditioned_study.py`, `src/robustness.py`.
- **The value chain** — keyless crude→products→petchem/fertilizer nodes and
  mechanism-gated derived cracks; the CHAIN VIEW reports what transmits and what
  is honestly decoupled.
- **The living layer** — an always-on RSS watcher (10 feeds, 6 domains) that
  *curates and never concludes*, a record-keeper that logs → resolves → scores
  its own reads, and phone alerts for high-signal items. All caged.
- **One canonical database** — `data/oil.db`, a seven-table generic schema
  (`src/init_db.py`). New data = new rows via small `src/fetch_*.py` adapters;
  no parallel databases, ever.

## Keeping it current (free, always-on)

- **Locally:** `python3 src/refresh.py` pulls every series in isolation (one
  failing never stops the others) and ends with a summary; `python3 src/heartbeat.py`
  reports freshness and exits non-zero if anything is STALE/DEAD.
- **In the cloud ($0):** `.github/workflows/track.yml` runs the whole
  deterministic engine daily on GitHub Actions, rebuilds the DB from free
  sources, pushes alerts, and publishes The Daily to Pages;
  `.github/workflows/watch.yml` is the frequent news watcher. The deterministic
  pytest gate runs first, so a broken build never reaches prod. Setup:
  `ops/GITHUB_ACTIONS.md`.

## Scientific-integrity rules (non-negotiable)

1. **Pre-registration is binding** — H1–H3 and the decision rule are fixed in
   `PRE_REGISTRATION.md`; windows/splits/metrics are never changed after seeing a
   result.
2. **Never fabricate data or sources** — every observation is sourced and
   timestamped; unfetchable data is reported as missing, never filled in.
3. **Point-in-time discipline** — state variables are read at t−1, no lookahead.
4. **Honest reporting** — nulls and failed hypotheses are results.

Full working rules: `CLAUDE.md`. Vision & current place: `../NORTH_STAR.md`.
State of the build: `STATE_OF_THE_ENGINE.md`.

## Setup

```
pip install -r requirements.txt   # numpy/scipy/statsmodels/fastapi/uvicorn, all free
```

Python 3.12+ (CI runs 3.12). No API keys required for the core; optional secrets
(`EIA_API_KEY`, `NTFY_TOPIC`, `FIRMS_KEY`) only enable extra data/alerts.
