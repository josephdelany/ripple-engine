# Ripple Engine

A personal, **pre-registered event-study engine** that measures how geopolitical
shocks ripple through oil prices — and, crucially, whether they ripple *bigger*
when markets are already stressed. It is a research instrument, not a newsreader:
every number is one hop from the evidence that produced it, failed hypotheses are
reported not buried, and the whole thing runs on **free, keyless data at $0**.

Flagship build for the News-to-Markets project. Single-user tool, held to a bar a
quant could inspect.

## The headline finding

Geopolitical-risk shocks are **not** systematically associated with higher oil
prices — the average ripple is close to null, and the negative-control placebo is
null too. This is an *honest null*, and it matches the frontier literature
(Caldara & Iacoviello's GPR work), found here independently. The engine's job now
is defending that result at frontier standard — see `PRE_REGISTRATION.md` and
`EVALUATION.md`.

Where the engine *does* find structure, it is receipted: the crude→products value
chain transmits strongly, and two cross-asset edges (supply→gasoline crack;
fertilizer→corn) validated against pre-registered nulls. See `EDGE_PORTFOLIO.md`.

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
