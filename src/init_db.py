"""
init_db.py -- creates the canonical database schema for the Ripple Engine.

THE BIG IDEA (this is the foundation, read it):
You do NOT build a separate database for every thing you measure.
You build ONE generic schema. Adding a new domain (rare earths, FX, shipping,
conflict) means adding ROWS, not new tables. That is what lets this project
scale from oil to everything else without ever being rewritten.

Seven tables cover the entire system:
  entities        - the things (countries, commodities, chokepoints, institutions)
  series          - the catalog of data series (one row per series)
  observations    - EVERY number ever measured, in "long format"
  events          - discrete dated shocks
  event_entities  - which entities each event involved (many-to-many)
  edges           - causal links between entities (the Chain Library, as data)
  forecasts       - your prediction log, scored against the market

Safe to run repeatedly (it only creates what's missing).

Run:  python3 src/init_db.py
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

# --- The schema. Note how nothing here mentions "oil" -- it's domain-agnostic. ---
SCHEMA = """
-- The THINGS: countries, commodities, chokepoints, institutions.
CREATE TABLE IF NOT EXISTS entities (
    entity_id   TEXT PRIMARY KEY,      -- e.g. 'commodity.brent', 'country.iran'
    type        TEXT NOT NULL,         -- commodity | country | chokepoint | institution
    name        TEXT NOT NULL,
    notes       TEXT
);

-- The CATALOG of data series. One row per series, not per data point.
CREATE TABLE IF NOT EXISTS series (
    series_id   TEXT PRIMARY KEY,      -- e.g. 'fred.DCOILBRENTEU'
    name        TEXT NOT NULL,
    entity_id   TEXT REFERENCES entities(entity_id),
    unit        TEXT,                  -- 'USD/bbl', 'thousand bbl', 'percent'
    frequency   TEXT,                  -- daily | weekly | monthly
    source      TEXT,                  -- 'FRED', 'EIA', 'CFTC'
    source_url  TEXT,                  -- provenance / receipt
    notes       TEXT
);

-- EVERY number ever measured lives here, in long format.
-- obs_date = the date the value refers to.
-- as_of    = the date you KNEW it (bitemporal -> prevents lookahead bias).
CREATE TABLE IF NOT EXISTS observations (
    series_id     TEXT NOT NULL REFERENCES series(series_id),
    obs_date      TEXT NOT NULL,
    value         REAL,
    as_of         TEXT,
    retrieved_at  TEXT,
    PRIMARY KEY (series_id, obs_date, as_of)
);
CREATE INDEX IF NOT EXISTS idx_obs ON observations(series_id, obs_date);

-- Discrete dated SHOCKS, any domain.
CREATE TABLE IF NOT EXISTS events (
    event_id       TEXT PRIMARY KEY,
    event_date     TEXT NOT NULL,
    date_precision TEXT,               -- day | week | month (be honest about it)
    type           TEXT NOT NULL,      -- chokepoint_disruption | opec_decision | sanctions | conflict
    title          TEXT NOT NULL,
    description    TEXT,
    severity       INTEGER,            -- 1-5, defined in your codebook
    surprise       INTEGER,            -- 1-5, how UNexpected (see codebook)
    confidence     TEXT,               -- high | medium | low
    source_url     TEXT NOT NULL,      -- every event MUST be sourced
    added_at       TEXT
);

-- Which entities an event involved (an event touches several at once).
CREATE TABLE IF NOT EXISTS event_entities (
    event_id   TEXT NOT NULL REFERENCES events(event_id),
    entity_id  TEXT NOT NULL REFERENCES entities(entity_id),
    role       TEXT,                   -- actor | target | affected_market | location
    PRIMARY KEY (event_id, entity_id, role)
);

-- The Chain Library as queryable data: mechanisms between entities.
CREATE TABLE IF NOT EXISTS edges (
    edge_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entity TEXT REFERENCES entities(entity_id),
    to_entity   TEXT REFERENCES entities(entity_id),
    polarity    TEXT,                  -- same | inverse
    lag         TEXT,                  -- hours | days | weeks | months
    strength    TEXT,                  -- load-bearing | contributing | marginal
    confidence  TEXT,                  -- textbook | consensus | contested
    mechanism   TEXT                   -- the plain-English why
);

-- Your forecast track record, scored against the market (Kalshi/Polymarket).
CREATE TABLE IF NOT EXISTS forecasts (
    forecast_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    made_at       TEXT NOT NULL,
    question      TEXT NOT NULL,
    horizon       TEXT,
    my_prob       REAL,
    market_prob   REAL,
    market_source TEXT,
    resolved_at   TEXT,
    outcome       INTEGER,             -- 1 = happened, 0 = didn't, NULL = pending
    notes         TEXT
);

-- SITUATION MEMORY: the running per-conflict timeline (the "middle clock").
-- This is NOT the gated events table -- it is a memory of what appeared and is
-- relevant to an ongoing situation. Rows are auto-attached from the watcher
-- (deterministic) and, later, typed/summarised by the scoped agent. An item
-- becomes canon ONLY via the untouched human gate (which then backfills
-- promoted_event_id). Every atom is sourced; status is one value, never blended.
CREATE TABLE IF NOT EXISTS situation_log (
    log_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    situation_id      TEXT NOT NULL REFERENCES entities(entity_id),  -- 'situation.*'
    ts                TEXT NOT NULL,       -- when the item is dated (from the alert)
    kind              TEXT,                -- playbook vocab; 'unmapped' until typed
    actor_entity      TEXT REFERENCES entities(entity_id),
    headline          TEXT NOT NULL,
    detail            TEXT,                -- prose; meaning fixed by `status`
    source_url        TEXT NOT NULL,       -- every atom MUST be sourced
    retrieved_at      TEXT NOT NULL,
    status            TEXT NOT NULL,       -- observed | inferred | promoted (never blended)
    confidence        TEXT,                -- display-only; NEVER fed to math
    alert_url         TEXT,                -- provenance back to the alert_queue row
    promoted_event_id TEXT REFERENCES events(event_id),  -- set ONLY by the human-gate backfill
    -- re-running the attach step must add 0 rows: one atom per (situation, source).
    UNIQUE (situation_id, source_url)
);
"""

# Seed entities + series for what we already have.
ENTITIES = [
    ("commodity.wti",   "commodity", "WTI Crude Oil",   "US benchmark crude"),
    ("commodity.brent", "commodity", "Brent Crude Oil", "Global benchmark crude"),
    # Situation Memory identity row. type='situation' is invisible to the watcher's
    # entity net (it filters to country/chokepoint/commodity/institution), so this
    # never creates false alert matches. Membership lives in data/situations.yaml.
    ("situation.israel_iran_war_2025", "situation", "Israel-Iran War (2025- )",
     "Ongoing multi-front conflict; membership + config in data/situations.yaml."),
]
SERIES = [
    ("fred.DCOILWTICO",   "WTI Crude Oil Spot Price",   "commodity.wti",
     "USD/bbl", "daily", "FRED", "https://fred.stlouisfed.org/series/DCOILWTICO", None),
    ("fred.DCOILBRENTEU", "Brent Crude Oil Spot Price", "commodity.brent",
     "USD/bbl", "daily", "FRED", "https://fred.stlouisfed.org/series/DCOILBRENTEU", None),
]
# Map the old prices table's labels onto the new series ids.
LABEL_TO_SERIES = {"WTI": "fred.DCOILWTICO", "Brent": "fred.DCOILBRENTEU"}


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # 1. Create the seven tables (safe to re-run).
    cur.executescript(SCHEMA)

    # 1b. MIGRATION. CREATE TABLE IF NOT EXISTS won't add columns to a table that
    # already exists, so we check for missing columns and add them. This is how
    # real projects evolve a schema without wiping data.
    existing_cols = {r[1] for r in cur.execute("PRAGMA table_info(events)")}
    for col, coltype in [("surprise", "INTEGER")]:
        if col not in existing_cols:
            cur.execute(f"ALTER TABLE events ADD COLUMN {col} {coltype}")
            print(f"Migration: added column events.{col}")

    # 2. Register the entities and series we already have.
    cur.executemany("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)", ENTITIES)
    cur.executemany("INSERT OR IGNORE INTO series VALUES (?,?,?,?,?,?,?,?)", SERIES)

    # 3. Migrate the existing prices table into the generic observations table.
    # On a FRESH build there is no `prices` table yet (fetch_prices creates it and
    # now writes observations directly), so guard the migration -- otherwise a
    # from-zero rebuild (repro.sh) would crash here.
    have_prices = cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='prices'").fetchone()
    existing = cur.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    if existing == 0 and have_prices:
        rows = cur.execute("SELECT date, price, commodity FROM prices").fetchall()
        payload = [
            (LABEL_TO_SERIES[label], str(date)[:10], float(price), str(date)[:10], now)
            for date, price, label in rows
            if label in LABEL_TO_SERIES
        ]
        cur.executemany(
            "INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)", payload
        )
        print(f"Migrated {len(payload):,} price rows into observations.")
    else:
        print(f"observations already has {existing:,} rows - skipping migration.")

    conn.commit()

    # 4. Report what the database now looks like.
    print("\nCanonical schema in", DB)
    # NOTE: fetch the table list FIRST. Running a query on the same cursor
    # while looping over its results would reset it (a classic SQLite gotcha).
    tables = [
        row[0]
        for row in cur.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
    ]
    for name in tables:
        count = cur.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        print(f"  {name:<16} {count:>8,} rows")
    conn.close()


if __name__ == "__main__":
    main()
