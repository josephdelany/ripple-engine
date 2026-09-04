> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# Task Brief 02 — The Forecast Layer (Kalshi benchmark + forecast log)

*Read CLAUDE.md first; its rules override this brief. Commit after each step. Stop and report on any design fork.*

## Purpose
Turn the engine from a measurement tool into a forecasting practice: Joe logs probabilistic forecasts, benchmarks them against market-implied odds (Kalshi), and accumulates a Brier-scored track record in the existing `forecasts` table. This is the accountability layer — nothing here predicts automatically; it RECORDS Joe's judgments and scores them honestly.

## Step 1 — Kalshi market reader (`src/fetch_kalshi.py`)
Read-only client for Kalshi's public market-data API (api.elections.kalshi.com/trade-api/v2 or current public endpoint — verify from their docs). Functions: search markets by keyword (e.g. "oil", "Brent", "Strait of Hormuz"), and fetch a market's current yes-price (= implied probability) by ticker. **Read-only: no auth for public data if possible, NO trading endpoints, ever.** If an API key turns out to be required even for public quotes, STOP and tell Joe what to sign up for — do not scrape. Print a demo: 5 oil/geopolitics-related markets with implied probabilities. Commit.

## Step 2 — Forecast logger CLI (`src/forecast_log.py`)
A small command-line tool over the EXISTING `forecasts` table (no schema changes unless a column is genuinely missing — if so, use the ALTER TABLE migration pattern from init_db.py):
- `python3 src/forecast_log.py add` — interactive prompts: question, horizon/resolve-by date, Joe's probability (0–1), market ticker (optional) → auto-fills market_prob from Kalshi if given, records made_at timestamp and a notes field where Joe states his REASONING (require non-empty: a forecast without reasoning is not loggable).
- `python3 src/forecast_log.py resolve <id> <0|1>` — records outcome + resolved_at.
- `python3 src/forecast_log.py score` — table of all forecasts; for resolved ones: Brier score per forecast, Joe's mean Brier, the market's mean Brier on the same questions, and the naive 0.5 baseline. Honest empty-state message when nothing is resolved yet ("track records take calendar time").
Commit.

## Step 3 — Dashboard widget
Add a `forecast_log` table-widget to `src/backend.py` (same pattern as the others) showing the log with columns: question, made_at, my_prob, market_prob, outcome, brier. Don't restart the running server — note that Joe restarts it. Commit.

## Step 4 — Seed nothing
Do NOT invent sample forecasts. The log starts empty; Joe makes the first real one himself.

## Out of scope
No trading. No automated forecasting. No LLM-generated probabilities. No new tables. No changes to the registered analysis or BRIEF_SKELETON.md.

## Done when
The demo prints real Kalshi probabilities, `forecast_log.py add/resolve/score` all work against the canonical DB, the widget serves, and it's all committed.
