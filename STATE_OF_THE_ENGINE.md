# STATE OF THE ENGINE — reconciliation inventory (VISION_ROADMAP Phase V0.1)

*Written 2026-08-03. A one-time snapshot of what the parallel workstreams
(WS0–WS-G, WS-S, UCDP, and the earlier Step/Pillar/Whole sprints) left behind:
what exists, what's registered, what's stale, what's orphaned. This is a map,
not a plan — the plan is `VISION_ROADMAP.md`.*

Baseline at write time: `python3 src/acceptance.py` → **COMMISSIONED**
(131 tests pass, framework_sound=true, engine_status=AMBER, cage present,
9 evidence packs). `engine_status` verdict **AMBER** for two reasons only
(1 dead feed + STALE series) — both diagnosed and fixed in slice V0.2.

---

## 1. What exists

### Canonical data store — ONE database
`data/oil.db`, the seven-table generic schema (`src/init_db.py`). Current size:

| table | rows | note |
|---|---|---|
| series | 361 | priceable + context series (incl. 267 predmkt contracts) |
| observations | 418,370 | point-in-time; `as_of`/`retrieved_at` on every row |
| events | 289 | the verified corpus (hand-coded + caged-LLM admissions) |
| forecasts | 4 | open forecast log (resolve → Brier) |
| edges | 6,844 | propagation-graph edges (measured pass-through/lag) |

No `nodes`/`claims` tables — nodes live in the graph artifacts, claims in
`data/evidence/*.json`. No parallel databases (guardrail held).

### Modules by function (`src/`, ~90 scripts)
- **Fetchers** (`fetch_*.py`, ~20): prices, EIA, FRED/ALFRED (point-in-time
  vintages), COT, GPR, GDELT tone, Wikipedia attention, FIRMS, PortWatch,
  Kalshi/Polymarket predmkt, OVX, breakevens, energy + wider priceable nodes,
  UCDP conflict-intensity. All keyless/free ($0 rule) except UCDP (token kept
  out of repo).
- **Corpus / living engine**: `extract_prepare.py` → `extract_events.py`
  (caged LLM extraction — the no-fabrication cage) → `admit_events.py` /
  `review_candidates.py` (admission + borderline queue) → `living_engine.py`.
- **Analysis (registered)**: `edge_battery.py` (the pre-registered amplification
  battery), `cross_asset.py` + `cross_asset_conditioned.py`, `derive_signals.py`
  (mechanism-string-gated), `conditioned_study.py`, `local_projections.py`,
  `nowcast.py`, `probability.py`, `discovery.py`, `robustness.py`, `validate.py`.
- **Confidence / accountability**: `corroborate.py`, `calibrate*.py`,
  `forecast_log.py`, `resolve_reads.py`, `read_backtest.py`, `evaluate.py`,
  `evidence.py`/`evidence_pack.py`.
- **Ops / health**: `heartbeat.py` (freshness smoke detector), `coverage.py`
  (feed/domain coverage), `status.py` (GREEN/AMBER/RED verdict),
  `acceptance.py` (COMMISSIONED/DEGRADED gate), `refresh.py`/`daily.py`
  (the run cycle), `restore_db.py` (tested restore), `notify.py`.
- **Surfaces / interface**: `backend.py` (Flask, port 5050), `mcp_server.py`
  (MCP query tools), `research.py` (the pull bench), `digest.py`/`orient.py`/
  `sowhat.py`/`daily.py` (reads), `watcher.py`/`watch_cycle.py` (live wire).

### Data feeds
- **RSS watch feeds** — `data/watch_feeds.txt`, 10 feeds across 6 domains
  (war, geopolitics, energy, macro, supply-chain/shipping, Middle-East).
- **Series feeds** — FRED/ALFRED, EIA, COT, GPR, GDELT, Polymarket, UCDP.

### Surfaces
Flask backend (5050) + OpenBB terminal design (6900), MCP server, the research
bench, the daily read, the live watcher. `SURFACES.md` is the map.

---

## 2. What's registered (the frozen scientific record)

- **`BRIEF_SKELETON.md`** — the pre-registered H1–H3 conditioned analysis +
  the fixed decision rule (+5pp clustered amplification).
- **`REGISTERED_SAMPLE.md`** — the frozen n=20 registered sample.
- **`PRE_REGISTRATION.md`** — the edge battery (10 amplification hypotheses,
  FDR-corrected), frozen before results, with dated amendments appended:
  - **Amendment 2026-07-30 (WS-S)** — credit/real-rate conditioners +
    clustering fix (commit `ded2419`, registered BEFORE results).
  - **Amendment 2026-07-30b (UCDP)** — verified-conflict conditioner
    (commit `4d5e1f3`, registered BEFORE results).
- **`EDGE_PORTFOLIO.md`** — the scored battery results (run 2026-07-30, N=289).

### Validated claims (9 evidence packs, `data/evidence/`)
`hyp.H1` (VIX-stress amplifies the oil ripple) · nodes: `brent_oil`,
`heating_oil`, `s&p_500`, `platinum`, `product_tankers`, `5y_breakeven` ·
edges: `copper_growth`, `hy_credit_stress`. Each pack is claim-addressable and
receipted. The UCDP verified-conflict conditioner (commit `5f540cf`) tested to
an **honest null** — reported, not buried.

**Frozen-record rule:** the registered H1–H3/H5 record is history. New claims
come ONLY from new dated amendments (register-then-run, git-proven). V0 does not
touch it.

---

## 3. What's stale / dead (the AMBER — diagnosed honestly)

At write time `engine_status` = AMBER: **1 dead feed + STALE series**. Verified
against source, each labelled by true cause (fixed in slice V0.2):

### Dead feed (1) — BREAKAGE (external block)
- **`mining_com`** (`https://www.mining.com/feed/`) — returns HTTP 403
  (Cloudflare anti-bot), 0 entries via feedparser. Not our bug; the publisher
  blocks automated fetches. → **Replaced** with a live metals/mining wire
  (verified to parse). No silent keep.

### Stale series — THREE distinct causes (not one)
1. **FRED H.10 FX (4): `DEXCHUS`, `DEXJPUS`, `DEXUSEU`, `DTWEXBGS`** —
   **PUBLICATION LAG, not breakage.** Verified against FRED's own keyless CSV:
   FRED itself only has data through 2026-07-24 for these — our DB matches
   exactly. The H.10 daily-FX release publishes in weekly batches with a ~1-week
   lag; the generic `fred.*` 3-day lag override is simply too short. → Fixed
   with an honest per-series `publish_lag_days` that matches the real release
   cadence (still trips STALE on a genuine multi-week break).
2. **FRED weekly retail gasoline: `GASREGW`** — **MIS-CADENCED override.**
   It's a weekly series, but the `fred.*` glob forced it to daily cadence, so a
   normal 7-day gap read as STALE. → Fixed with a weekly cadence override.
3. **~18 Polymarket contracts (`predmkt.polymarket.wti-…`, `…ng-…`)** —
   **EXPIRED / RESOLVED CONTRACTS, a third category (neither lag nor breakage).**
   They reference past dates (July 27–29, March 26 2026); the `notes` field
   already records `ends <date>; DISPLAY/context only`. The contract resolved and
   will never update again. The fetcher is healthy (267 predmkt series, most
   fresh to today). Flagging a resolved contract as STALE is a false alarm. →
   Fixed by teaching `heartbeat` a **CLOSED** status: a dated contract past its
   `ends` date is terminal, excluded from the STALE/DEAD trouble rollup.

The `last_run` verdict shows DEGRADED **only** because `health_trouble=true`
(the STALE above) — `failed_steps` is empty, so nothing actually crashed. It
clears when the staleness is honestly resolved.

---

## 4. What's orphaned / superseded

### Competing roadmap & vision docs → folded into `VISION_ROADMAP.md` (slice V0.3)
These were earlier, parallel planning documents. `VISION_ROADMAP.md` is now the
single active plan ("other Claude Code sessions retire from this repo"). Moved to
`docs/superseded/` with a pointer, not deleted (history preserved):
- `ENRICHMENT_ROADMAP.md` → subsumed by roadmap V1/V2 (feeds → pipeline).
- `ANALYST_TERMINAL_BLUEPRINT.md` → subsumed by roadmap V5 (surfaces).
- `GULF_RISK_VISION.md` → subsumed by the roadmap's Vision section + `NORTH_STAR.md`.
- `STORIES_HUB_PLAN.md` → subsumed by roadmap V5 (surfaces / The Daily).
- `OPENBB_TERMINAL_DESIGN.md` → subsumed by roadmap V5 (surfaces).

`TASK_BRIEF_*.md` and `TASK_QUEUE_A.md` are NOT archived — they are historical
per-sprint execution records (closed tickets, like git history), not competing
roadmaps, so they stay in root untouched.

### Kept as canonical (NOT roadmaps — specs, results, method)
`CLAUDE.md`, `VISION_ROADMAP.md`, `BRIEF_SKELETON.md`, `PRE_REGISTRATION.md`,
`REGISTERED_SAMPLE.md`, `EDGE_PORTFOLIO.md`, `METHOD.md`, `ENGINE.md`,
`DIFFERENTIATION.md`, `EVIDENCE.md`, `EVALUATION.md`, `DATA_DICTIONARY.md`,
`ACCEPTANCE_TEST.md`, `ENGINE_STATUS.md`, `USAGE.md`, `README.md`,
`RESEARCH_BENCH.md`, `SURFACES.md`, `TALKING_TO_IT.md`.

### Open TODOs carried into the roadmap
- Value-chain breadth (products/petchem/fertilizer/food, metals, credit) → V1.
- Corpus to 500+ with a formal admission rule + monthly audit → V2.
- Cross-chain registered hypotheses on the grown corpus → V3.
- `triage(text_or_url)` live "throw anything at it" card → V4.
- Surfaces catch-up (chain view, triage queue) → V5.
- Bulletproofing lenses (spec curve, influence, holdout, vintages) → V-Q.

---

## 5. Guardrails held (verified this pass)
$0 / keyless (UCDP token out of repo) · ONE database, no new tables · frozen
registered record untouched · no fabrication (cage + tests present) · no naked
decimals at the surface (typed buckets) · nulls reported, not buried.
