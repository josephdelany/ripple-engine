# D-9 — Ripple Engine desk, read as a hostile reader

Repo under audit: `/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine` (untouched — see confirmation at the end).
All execution ran against a scratch clone: `/private/tmp/claude-502/-Users-default-PERSONAL-OS-V2/33693732-1ed6-49a9-aa2e-892d7ee3ffcf/scratchpad/desk_clone`, seeded with the real repo's `data/oil.db`, `data/cache`, `data/state/raw`, `data/state/local`, `data/reader`, and `data/digest.html` (this last one is gitignored/generated but is one of the screens in scope, so it was copied in separately). The clone's committed `data/walk_forward/summary.json` has `run_id = walk_20260902T182828Z`, matching the record this task defines.

**Note on rendering tooling:** the task pointed at `<repo>/tools/node_modules` for jsdom; that path does not exist in this repo (no `tools/` directory, no `package.json` anywhere in the tree). `node` (v24.14.0) is installed system-wide; jsdom (v29.1.1) was found in an unrelated local project (`/Users/default/econ-bootcamp/node_modules`) and loaded via `NODE_PATH`, exactly the fallback `tests/test_app_render.py` itself documents (`_node_path()` checks `NODE_PATH` first). Nothing was installed into the clone or the real repo.

All GET routes were called with FastAPI's `TestClient` against `backend.app` (which mounts `terminal_api` and `api_v2`), in-process, no port bound. POST routes were inspected, not called (per instructions).

---

## 1. Endpoint table

89 GET routes resolved 200 after supplying the required query params (11 needed a param the first pass didn't guess — `id=`, `event=`, `table=`, `entity=` — all re-run with corrected params, see full raw dumps in `/private/tmp/.../scratchpad/responses/*.txt`). One GET route (`/event_detail`) 500s. 9 routes are POST/mutating and were not called.

| route | method | status | writes? | notes |
|---|---|---|---|---|
| `/` | GET | 200 | no | landing text |
| `/agents.json`, `/apps.json`, `/widgets.json` | GET | 200 | no | OpenBB widget catalog; `widgets.json` descriptions carry "VALIDATED" language, see §3 |
| `/openapi.json`, `/docs`, `/docs/oauth2-redirect`, `/redoc` | GET | 200 | no | FastAPI auto-docs; `openapi.json` route *descriptions* (from docstrings) also carry "VALIDATED"/"validated" language, publicly visible at `/docs` |
| `/app` | GET | 200 | no | the 4-screen app (Feed/Story/Big moves/Walk/Ledger) |
| `/big_moves` | GET | 200 | no | static page, pre-rendered by `big_moves_page.py` from `data/big_moves/*.json` |
| `/digest` | GET | 200 | no | re-rendered per request from `src/digest.py`; **the "VALIDATED edge" section, see §3/Finding 1** |
| `/desk.css` | GET | 200 | no | stylesheet |
| `/api/market_state`, `/api/feed` | GET | 200 | no | Feed data |
| `/api/story?id=` | GET | 200 | no | Story object |
| `/api/story` | **POST** | not called | writes `data/ledger/claims.jsonl` (via `story_read.read(..., log=True)`) when the input is a pasted headline/URL | logs every checkable claim it extracts |
| `/api/big_moves?asset=` | GET | 200 | no | |
| `/api/ledger` | GET | 200 | no | 3 scoreboards + recent claims |
| `/api/ledger/resolve` | **POST** | not called | resolves every claim past its horizon from data and appends to `data/ledger/resolutions.jsonl` | |
| `/api/events?q=` | GET | 200 | no | corpus search |
| `/api/challenge/vocab`, `/api/challenges` | GET | 200 | no | |
| `/api/challenge` | **POST** | not called | logs a challenge run (re-read Layer G under conditions) to the challenge ledger; refusals are also logged | |
| `/api/engine_read?id=` | GET | 200 | no | |
| `/api/walk/summary` | GET | 200 | no | passes `data/walk_forward/summary.json` through **whole** except each tier's `items_vs_climatology` (api_v2.py:209-223) |
| `/api/walk/audit` | GET | 200 | no | IES-90 label audit status (0/30 done) |
| `/api/walk/list`, `/api/walk/read?id=` | GET | 200 | no | per-event sealed reads |
| `/api/rebuild` | **POST** | not called | regenerates `data/market_state.json` + `data/feed.json` in place (`feed_build.FB.run()`) | the only POST that rewrites core desk data files |
| `/event_detail` | GET | **500** | no | **crashes** — see Finding 6. Ignores any `event_id` query param; always computes over all events |
| `/event_database`, `/state_of_system`, `/ripple_by_type` | GET | 200 | no | |
| `/engine_read`, `/engine_status`, `/domain_lens`, `/domain_conditioning` | GET | 200 | no | `/domain_lens` and `/domain_conditioning` carry "VALIDATED" verdicts, see §3 |
| `/edge_portfolio` | GET | 200 | no | raw `data/edge_battery.json`-derived table with literal `"verdict":"VALIDATED"` × 4, see §3 |
| `/supply_chain`, `/propagation_graph` | GET | 200 | no | `/propagation_graph` layers are literally named `"BACKBONE (validated)"`, see §3 |
| `/ripple_map`, `/corroboration_convergence`, `/gap_board` | GET | 200 | no | `/gap_board` mixes "not yet a validated edge" (honest) with the pervasive validated framing elsewhere |
| `/track_record` | GET | 200 | no | markdown page titled around "the validated edge (H1)", see §3 |
| `/signal_registry`, `/h1_live_edge` | GET | 200 | no | `/h1_live_edge` = "THE READ for the one validated edge (H1)" |
| `/scenario_playbook`, `/propagation_map`, `/alert_queue`, `/corroborated_events`, `/prediction_markets`, `/chokepoint_transits`, `/attention`, `/supply_fundamentals`, `/story_opec`, `/opec_stress`, `/commodity_exposure`, `/conflict_intensity`, `/analogue_backtest`, `/analogue_forecast`, `/transmission_chains`, `/risk_gauge`, `/risk_vs_priced`, `/where_we_stand` | GET | 200 | no | mostly empty/null placeholders in this data snapshot |
| `/chart_*` (11 routes) | GET | 200 | no | chart data for OpenBB widgets |
| `/chain_view`, `/triage_queue`, `/forecast_log` | GET | 200 | no | |
| `/situation?event=`, `/situation_events`, `/situation_view` | GET | 200 | no | `/situation_view` renders "Verified analog set" — see Finding 2 |
| `/trace?entity=`, `/trace_entities`, `/trace_view` | GET | 200 | no | `/trace_view` renders "Validated transmission" live — see Finding 1 |
| `/backtest`, `/backtest_view` | GET | 200 | no | `/backtest_view` renders "the validated edge (H1) HOLDS" live — see Finding 1 |
| `/question_view` | GET | 200 | no | static shell, POSTs to `/wb_deconstruct` |
| `/terminal`, `/term_catalog`, `/term_series?id=`, `/term_ripples?id=` | GET | 200 | no | |
| `/workbench`, `/wb_today`, `/wb_articles`, `/wb_daily_brief`, `/wb_history`, `/wb_db_tables`, `/wb_db_rows?table=`, `/wb_event?id=`, `/wb_extract?url=`, `/wb_news_search?q=`, `/wb_pulse`, `/wb_series?series_id=`, `/wb_note` (GET) | GET | 200 | no | `/wb_daily_brief` carries "H1 validated" text, reachable from the workbench's Daily Brief button |
| `/wb_note` | **POST** | not called | writes `data/notes/current.md` | autosave |
| `/wb_export` | **POST** | not called | writes `data/notes/draft_<UTC ts>.md` | |
| `/wb_analyze`, `/wb_brief`, `/wb_deconstruct` | **POST** | not called | no disk writes (compute-only, per source read) | |
| `/wb_db_query` | **POST** | not called | read-only SQL only (enforced: `mode=ro` + `query_only` + authorizer + row cap + wall-clock interrupt, `db_explore.py`) | |

---

## 2. Screen table

| screen | rendered how | hits (validated/retired-label issues) |
|---|---|---|
| `src/app.html` `#s-feed`, `#s-story`, `#s-walk`, `#s-ledger` | **jsdom**, `runScripts:'outside-only'`, `w.eval`'d the page script (per `tests/test_app_render.py` pattern), `w.fetch` mocked to the real captured `/api/*` responses, called `loadFeed()`, `renderStory(story)`, `loadWalk()`, `loadLedger()`, dumped `#s-*` `.textContent` | **0** occurrences of `VALIDATED` in any of the four rendered screens (confirms the existing `test_a3_section5_renders_trust_from_the_api_under_jsdom` assertion). `SUGGESTIVE / null` appears verbatim, correctly, throughout Walk and Ledger. `#s-big` is an `<iframe src="/big_moves">`, not followed — see `/big_moves` row above |
| `src/situation.html` (`/situation_view`) | jsdom, mocked `/situation_events` + `/situation?event=september_11_attacks_2001` | **Finding 2**: "Verified analog set" renders bare `outcome_90` codes (`CONTAINED`, `LIMITED_RETALIATION`, …) with **zero** occurrences of "retired" anywhere on the rendered page |
| `src/trace.html` (`/trace_view`) | jsdom, mocked `/trace_entities` + `/trace?entity=country.iran` | **Finding 1**: renders live "H1 — VIX stress (**validated**; H2 inventories & H3 positioning rejected)" and a section literally titled "**Validated transmission** — how a shock propagates under stress" with 6 rows |
| `src/backtest.html` (`/backtest_view`) | jsdom, mocked `/backtest` | **Finding 1**: renders live "Temporal hold-out — the **validated edge** (H1) HOLDS" and "**Validated edges** and nulls are shown side by side" |
| `data/digest.html` (`/digest`) | direct HTTP response (server re-renders per request from committed artifacts; also diffed byte-for-byte against the static file, identical except the `as of` timestamp) | **Finding 1**: "The **validated edge**" section header, "passed the full **validation gate**", "**4 validated**" hypotheses |
| `src/terminal.html`, `src/question.html`, `src/workbench.html`, `src/big_moves.html` | **not fully jsdom-rendered** (time-boxed); static template + inline JS string literals grepped directly, cross-checked against the live API responses those pages fetch | `big_moves.html`/`terminal.html`/`question.html` own templates: 0 "VALIDATED"/"validated" literals. `workbench.html`'s "Daily Brief" button (`loadDaily()` → `/wb_daily_brief`, confirmed by source read at `workbench.html:413-414`) pulls in "H1 validated; see validation_claims.json" from `src/brief.py`'s output — not rendered under jsdom, but the data path is real and traced |

---

## 3. Hit list — stronger-than-record language

Record for this audit: verdict **SUGGESTIVE / null** on both targets (protocol §7); **no VALIDATED anywhere**; no occurrence probabilities; `sr_outcome_90` RETIRED and must be labelled so wherever shown.

**`VALIDATED` (upper-case, literal) — 62 raw hits, deduplicated to distinct emitters below.** This is overwhelmingly the dominant finding. It does **not** come from the walk-forward/IES-90 pipeline (`WALK_FORWARD_PROTOCOL.md` §7) that produced the SUGGESTIVE/null record — it comes from a separate, older, also-pre-registered program (`PRE_REGISTRATION.md` v1, frozen; `data/edge_battery.json`, FDR/Bonferroni-corrected) governing an "H1 amplifier" / "Edge Portfolio" claim system. Both are legitimate under their own protocols, but nothing on any of these pages tells a reader which protocol governs which number, and `SESSION_CHARTER.md` rule 4 says plainly: **"VALIDATED only per protocol §7."**

| exact string | file:line (source) | endpoint/screen | stronger than record? | record value |
|---|---|---|---|---|
| `"The validated edge"` / `"passed the full validation gate"` / `"4 validated"` | `src/digest.py:300,303,332` | `/digest` (rendered, confirmed) | **YES** | no VALIDATED anywhere |
| `"the validated edge (H1)"` / `"HOLDS"` / `"Validated edges and nulls are shown side by side"` | `src/backend.py:1059,1074` (panel built inline) | `/backtest`, `/backtest_view` (rendered under jsdom, confirmed) | **YES** | no VALIDATED anywhere |
| `(v.G_conditioning||'').startsWith('VALIDATED')` | `src/backtest.html:33` | `/backtest_view` (JS logic — dead in today's data since `G_conditioning` is `"SUGGESTIVE / null"`, but the template explicitly anticipates and styles a VALIDATED state) | **YES** (structural) | n/a |
| `"H1 — VIX stress (validated; ...)"` | `src/backend.py:1137` (`h1_live_edge`) | `/h1_live_edge`, and rendered live into `/trace_view` (confirmed) | **YES** | no VALIDATED anywhere |
| `"Validated transmission — how a shock propagates under stress"` | `src/trace.html:120` | `/trace_view` (rendered under jsdom, confirmed) | **YES** | no VALIDATED anywhere |
| `"BACKBONE (validated)"` × 6 edges | `src/propagation_graph.py:148,175,200,218,221,232` | `/propagation_graph` | **YES** | no VALIDATED anywhere |
| `"row":"VALIDATED node"` × 2 (Brent oil, Heating oil) | `src/backend.py:910` | `/domain_lens` | **YES** | no VALIDATED anywhere |
| `"verdict":"VALIDATED"` × 4 hypotheses (curve_2s10s, palladium_supply, hy_credit_stress, severity_dose_response) | `src/domain_conditioning.py:83` → `data/domain_conditioning.json` | `/domain_conditioning` | **YES** | no VALIDATED anywhere |
| `"verdict":"VALIDATED"` × 4 (copper_growth, palladium_supply, hy_credit_stress, severity_dose_response) with perm_p/fdr_q | `src/backend.py:845,865` → `data/edge_battery.json` | `/edge_portfolio` | **YES** | no VALIDATED anywhere |
| `"the validated edge (H1)"` / `"6 validated edges"` | `src/backend.py:1059,1074` | `/track_record` | **YES** | no VALIDATED anywhere |
| `"the VALIDATED propagation"` / `"validated backbone"` / `"Each asset validated through the SAME gate"` | `src/backend.py:168,196,197,210,212,218,219,229` | `/widgets.json` (OpenBB widget catalog copy) | **YES** | no VALIDATED anywhere |
| `"VALIDATED requires: skill > 0 vs climatology..."` | `data/walk_forward/summary.json` `verdict.note` (walk.py-authored) | `/api/walk/summary`, `/api/story`, `/api/ledger`, `/backtest` | NO — this is the honest promotion-rule text explaining *why* the current verdict is SUGGESTIVE, not a claim of validation | n/a (compliant) |
| `"VALIDATED graph only"` / `"the VALIDATED propagation"` | `src/sowhat.py:7,75,96` | `/sowhat` | **YES** | no VALIDATED anywhere |
| Route *descriptions* using "validated"/"VALIDATED" (Domain Lens, Supply Chain, Propagation Graph, H1 Live Edge, wb_db_rows) | `src/backend.py:196,210,218-219,1109`, docstrings | `/openapi.json`, visible at `/docs` and `/redoc` | **YES** (documentation-level, publicly reachable) | no VALIDATED anywhere |
| `"H1 validated; see validation_claims.json"` / `"not yet a validated edge"` | `src/brief.py` (build_brief) | `/wb_daily_brief`, reachable from Workbench "Daily Brief" | **YES** (mixed with an honest null a sentence later) | no VALIDATED anywhere |

**`SUGGESTIVE` without `/ null` — the specific item the task named.** Confirmed: `data/walk_forward/summary.json` → `verdict.rules["M07_uniform_k12:G"].status == "SUGGESTIVE"` (no suffix). Reachable verbatim through `/api/walk/summary`, and also embedded (same object) in `/api/story`, `/api/ledger`, `/backtest`. **Not rendered by any of the 8 screens checked** — `grep -n "verdict.rules\|\.rules\[" src/*.html` returns zero hits across `app.html`, `backtest.html`, `situation.html`, `trace.html`, `terminal.html`, `workbench.html`, `big_moves.html`. So this is an **API-surface** finding (any external consumer of the JSON gets a bare "SUGGESTIVE" for that one internal model-selection candidate), not a UI-visible one today.

**`sr_outcome_90` / `outcome_90` / RETIRED labeling.** `branches.outcome_label` (the governing disclaimer: `"retired: sr_outcome_90, κ≈0 vs ICB/MID/UCDP (OUTCOME_MAPPING.md Amendment 1, 2026-09-02) — corpus-derived, not an outcome"`) is present and correctly rendered next to the analog table on **`app.html` `#s-story`** (`app.html:194,249`) and next to the conditioned subset. It is **absent** from **`situation.html`** — see Finding 2. The literal column name `sr_outcome_90` (with sibling `sr_outcome_30`) appears only in the raw DB-schema/rows dump behind `/wb_db_tables` and `/wb_db_rows?table=events` (Workbench's read-only SQL browser) — unlabeled, but this is a raw-column browser by design, not a narrative surface; flagged as low-severity/informational, not a hard violation.

**Other patterns checked, no findings:** `predict*` (23 hits — all in disclaimers like "predict · score vs what actually happened", never a forward probability claim), `will ` (15 — all headline text or "the strait declared closed", not forecast language), `probability of` (1 hit, in `/wb_daily_brief`: `"NOT the probability of any outcome"` — this is the desk *disclaiming* probability, compliant), `chance of`/`% likely`/`likely to`/`expected to`/`forecasts that`/`causes`/`escalation skill`/`+0.12` (0 hits each), `confirmed`/`proven`/`shows that` (benign — news headlines, or "what's proven, how sure" page titles paired with disclaimers), `0.043`/`0.143` (hits exist but are unrelated coincidental values — a `pass_through_beta` in `/chain_view` and an `actor_response_propensity` in a raw situation-record row — not the retired v2.0 numbers named in the task), `Brier skill` (1 hit, `/api/story` trust row label — compliant, matches the record's own vocabulary), `best` (12 — all "SPA p ... (best M07_uniform_k12)", a statistical-test artifact naming the winning baseline, not a marketing claim).

---

## 4. 25-number trace (seed 20260902)

Pool of 38 numbers drawn from the Walk screen, Story trust rows, Ledger board, and Big moves (brent), each independently re-derived from the **committed file on disk** (`data/walk_forward/summary.json`, `data/big_moves/brent.json`) or the live corpus query path (`data/oil.db`, `src/story_read.py`, `src/ledger.py`), then compared byte-for-byte against the value shown in the captured API/render output. `random.seed(20260902); random.sample(pool, 25)`.

**Result: 25/25 traced, 0 mismatches.**

| screen | number | shown | source file | key/path |
|---|---|---|---|---|
| Walk | verdict.rules['engine:G'].status | `SUGGESTIVE / null` | data/walk_forward/summary.json | verdict.rules['engine:G'].status |
| Story trust | ies90.rates['3'] (war) | 0.4286 | live corpus read (event_outcomes source=ies90) | branches.ies90.rates.3 |
| Walk | daily n_scored_burn_in | 253 | data/walk_forward/summary.json | tiers.daily.n_scored_burn_in |
| Walk | daily G random_analogs skill | 0.06224193204100159 | data/walk_forward/summary.json | tiers.daily.G.engine_vs.random_analogs.skill |
| Story trust | ies90.n (analogs) | 7 | live corpus read | branches.ies90.n |
| Big moves | brent episodes[0].onset | 1988-11-17 | data/big_moves/brent.json | episodes[0].onset |
| Ledger | counts.checkable | 1 | src/ledger.py claims.jsonl (live) | counts.checkable |
| Story trust | statuses engine:P | `SUGGESTIVE / null` | data/walk_forward/summary.json | verdict.rules['engine:P'].status |
| Walk | run_id | walk_20260902T182828Z | data/walk_forward/summary.json | run_id |
| Walk | verdict.P_conditioning | `SUGGESTIVE / null (protocol §7; audit passed: False)` | data/walk_forward/summary.json | verdict.P_conditioning |
| Big moves | brent.everyday_base_rate_pct | 18.3 | data/big_moves/brent.json | everyday_base_rate_pct |
| Big moves | brent episodes[0].change | 50.6 | data/big_moves/brent.json | episodes[0].change |
| Ledger | engine.walk.run_id (mirrored) | walk_20260902T182828Z | data/walk_forward/summary.json | run_id |
| Walk | daily P persistence skill | 0.16323358351931772 | data/walk_forward/summary.json | tiers.daily.P.engine_vs.persistence.skill |
| Big moves | brent episodes[0].days | 64 | data/big_moves/brent.json | episodes[0].days |
| Walk | daily G climatology dm_p | 0.8470800466541546 | data/walk_forward/summary.json | tiers.daily.G.engine_vs.climatology.dm_p |
| Ledger | record_vs_narrative.resolved | 0 | src/ledger.py resolutions.jsonl | record_vs_narrative.resolved |
| Story trust | statuses engine:G | `SUGGESTIVE / null` | data/walk_forward/summary.json | verdict.rules['engine:G'].status |
| Walk | verdict.audit_passed | False | data/walk_forward/summary.json | verdict.audit_passed |
| Big moves | brent.no_identified_event | 15 | data/big_moves/brent.json | no_identified_event |
| Walk | verdict.rules['M07_uniform_k12:G'].status | `SUGGESTIVE` (bare, no "/ null") | data/walk_forward/summary.json | verdict.rules['M07_uniform_k12:G'].status |
| Walk | daily G climatology skill | -0.006989649941596232 | data/walk_forward/summary.json | tiers.daily.G.engine_vs.climatology.skill |
| Walk | daily G climatology n | 150 | data/walk_forward/summary.json | tiers.daily.G.engine_vs.climatology.n |
| Walk | daily n_reads | 299 | data/walk_forward/summary.json | tiers.daily.n_reads |
| Story trust | outcome_label carries "retired" + "sr_outcome_90" | True | OUTCOME_MAPPING.md Amendment 1 (hardcoded in story_read.py) | branches.outcome_label |

No untraceable or stale numbers among the 25 sampled. (Full pool of 38 candidates and the selection script are in the scratch directory: `trace25.py`, `trace25_chosen.json`.)

---

## 5. FINDINGS, ranked by severity

**1. CRITICAL — "VALIDATED" is pervasive across the desk, on live-rendered screens, contradicting the record's "no VALIDATED anywhere" and SESSION_CHARTER.md rule 4 ("VALIDATED only per protocol §7").**
Confirmed **actually rendered** (not just present in JSON) on three screens via jsdom:
- `/digest`: `"<h2 class=sec>The validated edge</h2>"` — `src/digest.py:300`; `"The one signal that passed the full validation gate"` — `src/digest.py:303`; `"<b>4 validated</b>"` — `src/digest.py:332`.
- `/backtest_view`: `"the validated edge (H1) HOLDS"` and `"Validated edges and nulls are shown side by side"` — built in `src/backend.py:1059-1074` (the `/backtest` payload), rendered by `src/backtest.html`.
- `/trace_view`: `"H1 — VIX stress (validated; H2 inventories & H3 positioning rejected)"` — `src/backend.py:1137`; `"Validated transmission — how a shock propagates under stress"` — `src/trace.html:120`.
Also present, unrendered-but-reachable, on: `/sowhat` (`src/sowhat.py:7,75,96`), `/track_record` (`src/backend.py:1059,1074`), `/propagation_graph` (`src/propagation_graph.py:148,175,200,218,221,232`), `/domain_lens` (`src/backend.py:910`), `/domain_conditioning` (`src/domain_conditioning.py:83`), `/edge_portfolio` (`src/backend.py:845,865`, literal `verdict:"VALIDATED"` × 4 with perm_p/fdr_q), `/h1_live_edge` (`src/backend.py:1109,1137,1191`), `/widgets.json` and `/openapi.json` (publicly visible at `/docs`, `src/backend.py:168,196-229`), and `/wb_daily_brief` (reachable from the Workbench's "Daily Brief" button, `src/brief.py`).
This is a genuinely different, separately pre-registered claim system (`PRE_REGISTRATION.md` v1, FDR/Bonferroni-corrected `data/edge_battery.json` — not fabrication), but nothing on any of these pages tells a hostile reader that "VALIDATED" here means something other than the walk-forward protocol §7 gate that is honestly SUGGESTIVE/null a click away on the Walk screen. A reader who lands on `/digest`, `/track_record`, `/trace_view`, or `/backtest_view` first — all realistic entry points — sees a confidently "validated" engine.

**2. HIGH — `situation.html` (`/situation_view`) shows the retired `outcome_90` taxonomy with zero "retired" disclosure, unlike `app.html`.**
`app.html`'s `#s-story` screen correctly renders `br.outcome_label` (`"retired: sr_outcome_90, κ≈0 vs ICB/MID/UCDP..."`) directly above and below its analog table (`app.html:194,249`). `situation.html`'s "Verified analog set" section (`situation.html:87`) renders the same per-analog `outcome_90` field (`CONTAINED`, `LIMITED_RETALIATION`, `WIDENING`, ...) with **no occurrence of "retired" anywhere on the rendered page** (confirmed via jsdom render of the live `/situation?event=september_11_attacks_2001` response). The section header itself — "**Verified** analog set" — compounds this.

**3. HIGH — Feed and Story screens never render the classification-mode field (`reader`: "llm" vs "regex_fallback"), violating SESSION_CHARTER.md rule 6 ("every surface labels ... regex-fallback").**
Every feed item (`/api/feed`) and the Story object (`/api/story`) carries a top-level `reader` field (`reader.py` sets `mode="regex_fallback"` at `reader.py:292,309,313,316,517,556,573` whenever the LLM path is unavailable/times out/errors). `grep -n "\.reader\b" src/app.html src/situation.html src/trace.html src/backtest.html src/big_moves.html src/workbench.html` returns **zero matches** across all six templates — the field is structurally never displayed. In today's data snapshot all 75 feed items happen to be `reader:"llm"`, so there is no live mislabeled headline right now, but the code path that would need the label (`regex_fallback`) exists and the template has no mechanism to show it if it fires.

**4. MEDIUM — Feed's displayed date is a capture timestamp, not an event date, and is unlabeled.**
`feed_build.py:132` sets `"when": (r.get("timestamp_utc") or "")[:16]` — the alert's ingestion/capture time. `app.html:125` renders it inline, unlabeled, immediately after the classification (`"conflict escalation · rss:timesofisrael · 2026-08-31T20:25 · ..."`), reading exactly like an event timestamp to a casual reader. `reader.py` (confirmed by grep) never assigns a `date` field — corroborating the task's premise.

**5. MEDIUM — `M07_uniform_k12:G` carries a bare `"SUGGESTIVE"` status (no "/ null") in the committed `summary.json`, reachable through `/api/walk/summary` (and mirrored into `/api/story`, `/api/ledger`, `/backtest`), but not rendered by any screen today.**
`verdict.rules["M07_uniform_k12:G"].status == "SUGGESTIVE"` exactly, vs. the top-level `verdict.G_conditioning`/`P_conditioning` which correctly append `"/ null (protocol §7; audit passed: False)"`. No screen (`app.html`, `backtest.html`, `situation.html`, `trace.html`, `terminal.html`, `workbench.html`, `big_moves.html`) references `verdict.rules` at all, so this is an API-only exposure today — but any future template (or an external OpenBB/API consumer) that iterates `verdict.rules` and displays `.status` verbatim would show a bare, un-suffixed SUGGESTIVE with no null qualifier.

**6. MEDIUM — `/event_detail` 500s on a real production bug (NaN JSON-serialization), not a claims issue but a hostile-reader-visible crash.**
`GET /event_detail` (ignores its own would-be `event_id` param, per `backend.py:675-706`, and always computes over every event) throws `ValueError: Out of range float values are not JSON compliant: nan` when a row's `severity` column is NaN. Any OpenBB widget or direct hit on this endpoint gets a raw 500.

**7. LOW/INFORMATIONAL — the literal retired column name `sr_outcome_90` is shown unlabeled in the Workbench's raw SQL/DB browser (`/wb_db_tables`, `/wb_db_rows?table=events`).**
This is a generic, read-only column/row dump (`db_explore.py`) by design — not a narrative surface — so it's flagged for completeness rather than as a hard violation.

---

## Confirmation: real repo unchanged

No write, create, or delete operation was ever issued against `/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine`. Every file operation into that path was a **read** (`cat`/`grep`/`Read`); every copy went **from** the real repo **into** the scratch clone (`cp`), never the reverse; `git clone --no-local` only reads from it. All app execution, jsdom rendering, and the 25-number trace ran against the scratch clone.

```
$ git -C "/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine" status --porcelain
```
returns a non-empty diff (modified/untracked files: `RIPPLE_SOURCES.md`, several `data/*.json`, `src/api_v2.py`, `src/app.html`, `src/walk.py`, `src/engine/*`, a large batch of new `data/candidates/dossiers/*.md`, `data/seed/ripple/*.csv`, new test files, etc.). **None of this is from this session** — this session performed zero writes there. The dirty state is pre-existing / from other concurrent work on the repo (the scratchpad already contained sibling scratch clones — `ripple-clone`, `ripple-clone-b`, `leak_clone` — and prior audit reports `D1_registration_audit.md` … `D5_reader.md` from earlier sessions in this same task series, consistent with other sessions actively committing to this tree). Full porcelain output is reproducible by re-running the command above.

## WHAT I DID NOT DO

- Did not call any POST/mutating endpoint (`/api/story`, `/api/ledger/resolve`, `/api/rebuild`, `/wb_analyze`, `/wb_brief`, `/wb_db_query`, `/wb_deconstruct`, `/wb_export`, `/wb_note`, `/api/challenge`) — listed with what they write in §1 instead, from source inspection only.
- Did not fully jsdom-render `terminal.html`, `question.html`, `workbench.html`, or `big_moves.html` (time-boxed at 4 full renders: `app.html`, `situation.html`, `trace.html`, `backtest.html`); the other four were checked via static-template + JS-literal grep and cross-referenced against their live API responses, as the task permits.
- Did not exhaustively enumerate every one of the 671 raw pattern hits individually in the report; grouped by distinct emitter/source-line, with representative counts, and explicitly called out the patterns that produced zero or only-benign hits.
- Did not resolve whether `PRE_REGISTRATION.md` v1's VALIDATED promotion rule is itself sound (Bonferroni/FDR correctness, family definition, etc.) — out of scope for D-9, which is about what's *shown* vs. the stated record, not re-auditing the underlying stats (that's D-3's job, per the `D3_multiplicity.md` report already in the scratchpad from an earlier session).
