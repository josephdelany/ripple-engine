> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# The News Layer — comprehensive search, the database explorer, and the Ground-News question

This documents the "search any topic, get every article" feature and the engine-database
explorer added to the Desk, the research behind them, and — importantly — the honest limits
and the roadmap for the parts we deliberately did *not* build.

## What shipped

**1. Database explorer (`/wb_db_tables`, `/wb_db_rows`, `/wb_db_query`; `src/db_explore.py`).**
Browse and query the actual engine database (`data/oil.db`) from the Desk's **Database** view.
HARD read-only, four ways: a `mode=ro` connection, `PRAGMA query_only`, a statement authorizer
that permits only SELECT/READ, and single-statement + row-cap + wall-clock limits. Every write,
drop, ATTACH, PRAGMA, or multi-statement is **rejected, not run** (INV-2: the canonical DB is
append-only and never touched here). Tested in `tests/test_db_explore.py`.

**2. Comprehensive news search (`/wb_news_search`; `src/gdelt_search.py`).**
Search **any topic across the global press** via the **GDELT DOC 2.0 API** — free, **keyless**,
~65 languages, rolling ~3-month window, 15-minute fresh. Returns real deduped article URLs +
metadata and an honest **source-diversity coverage** view (how many articles, how many distinct
outlets, how many countries, over time). Click any result → the engine reads it (the brief) and
the source extract. Tested in `tests/test_gdelt_search.py`.

## Why GDELT (and why this is $0-safe forever)
Ground News aggregates ~50k sources via **commercial licensed feeds**. That is a paid moat we
cannot and should not buy. GDELT is the open equivalent for *discovery*: it already indexes the
global online press and the engine already uses it (`fetch_gdelt_tone.py`, `harvest_gdelt.py`,
`watcher.py`). Crucially for the **$0-forever, fails-not-bills** rule: GDELT has **no account and
no key**, so there is nothing to bill — the failure mode is a temporary IP throttle, never a
charge. (We deliberately avoid GDELT-on-BigQuery, which *does* bill on query bytes.)

Compliance built in: **attribution** ("Source: GDELT Project", shown on the coverage panel);
we store **metadata + links only**, never article bodies (GDELT licenses URLs, not full text);
and we detect GDELT's throttle — which arrives as **HTTP 200 + a plain-text body**, not a 429 —
by inspecting the body, so a rate-limit is surfaced honestly, never read as "no results".

## The Ground-News question, answered honestly
Research (see the build log) found Ground News is **~80% presentation of other people's labels**
plus one ML system (article clustering) and one AI-summary feature. Mapping their ideas to what
we can do at $0, keyless, no-fabrication:

| Ground News idea | Our status | How |
|---|---|---|
| Search any topic → all the articles | **SHIPPED** | GDELT DOC search + dedup |
| Coverage count / breadth | **SHIPPED** | distinct outlets + countries + time histogram (source diversity) |
| Cluster many articles into one story | **ROADMAP** | `scikit-learn` (already installed): TF-IDF cosine + connected-components in a time window — offline, keyless |
| Multi-article synthesis | **ROADMAP (extractive only)** | MMR over real sentences — verbatim, never generated (no hallucination) |
| Political bias bar (left/center/right) | **DEFERRED — licensing wall** | the label data (AllSides = CC BY-NC, MBFC = paid) can't be ingested cleanly; see below |
| Blindspot feed | **DEFERRED** | trivial arithmetic *once* bias labels exist |
| Ownership | **APPROXIMATE (future)** | Wikidata P127/P749 (CC0) — patchy but open |

## The one hard wall: political-bias labels
There is **no cleanly-licensed, open, source-level left/center/right dataset**. AllSides is
CC BY-**NC** (non-commercial, no redistribution); MBFC is proprietary/paid; every free GitHub
"bias CSV" is a licensing violation of the ratings underneath. So we do **not** ship a fabricated
or misattributed bias bar. The honest substitute we *do* ship is **source diversity** (outlets /
countries) from GDELT's own free metadata. A real political-bias bar is a deliberate future
decision: use AllSides under its non-commercial terms with attribution (fine for a single-user
personal tool), or train our own labels on a permissively-licensed corpus (MBIC, CC BY). Joe's
call, and it needs an ADR — it is not something to slip in.

## Open-source tools adopted / recommended (all permissive, keyless)
- **Adopted now:** `scikit-learn` (clustering/summary, already installed), the GDELT DOC API,
  a custom read-only SQLite explorer (chosen over embedding Datasette — fewer moving parts,
  same safety guarantees for a single-user tool).
- **Recommended next (needs a dependency add + ADR):** **`trafilatura`** (Apache-2.0, keyless,
  offline) for article extraction — F1 ~0.96, far better than the current regex `<p>` scrape,
  with reliable title/date. It would upgrade the source-extract quality across all sites.

## Honest limits to remember (don't overpromise)
GDELT counts **reports, not events**; it is English/Western-skewed; it does **no clustering or
dedup for you** (we dedup on URL + normalized title only); coverage is a rolling ~3 months (not
"every article ever"); and it is **metadata, not full text**. It is a superb $0 discovery layer —
not a licensed, deduplicated, bias-labeled event registry. The engine's differentiator remains
the **quant read**; the news layer is the intake that feeds it. The winning combination — *every
article on a story × its source diversity × the engine's measured market read* — is something no
news aggregator and no quant desk has, and it is now buildable end to end at $0.
