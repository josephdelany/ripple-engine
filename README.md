# Ripple Engine (energy + chokepoint flagship)

Measures how geopolitical shocks ripple through crude-oil prices — an **event study** over decades of daily data. Flagship build for the News-to-Markets project.

## Structure
- `src/fetch_prices.py` — pulls daily Brent & WTI prices from FRED (free, no key), cleans them, saves to a local SQLite database, and charts them.
- `data/` — the SQLite database (`oil.db`) and output charts.

## How to run
```
pip install -r requirements.txt
python3 src/fetch_prices.py
```
Then open `data/oil_prices.png`.

## Operations (keeping the engine current)

The engine can refresh itself daily, and it is built so **nothing fails silently**.

**Refresh manually** — pull fresh data for every series in one command:
```
python3 src/refresh.py
```
Each step (prices, macro series, EIA inventories, COT, derived signals, events)
runs in isolation — one failing never stops the others — and the run ends with a
summary table. Per-step history is appended to `data/refresh_log.csv`.

**Read the health report** — is the data actually current?
```
python3 src/heartbeat.py
```
It prints every series with its last observation and a status, writes
`data/health_status.json`, and **exits non-zero** if anything is wrong (so a
scheduler can tell). The same panel shows in the dashboard as the *System Health*
widget.

- **OK** — up to date for its cadence.
- **STALE** — a fresh reading is overdue by more than **2×** the series' cadence
  (daily series are judged on business days, so weekends aren't counted).
- **DEAD** — overdue by more than **4×** — something is broken, not just late.

**Schedule it** (optional, runs 07:30 daily): see [`ops/INSTALL.md`](ops/INSTALL.md)
for the two commands to install the launchd agent (and how to uninstall).

**Where logs live** (all under `data/`, all gitignored runtime artifacts):
- `refresh_log.csv` — one row per step per run (timestamp, step, status, detail).
- `health_status.json` — latest freshness snapshot (what the widget reads).
- `launchd_refresh.log` — console output of scheduled runs.

## Roadmap (this repo)
1. ✅ Price data pipeline → SQLite
2. ⬜ Geopolitical event database (energy/chokepoint shocks, hand-curated + sourced)
3. ⬜ Event study — measure the average price ripple around each event type
4. ⬜ Visualize the ripple + write the finding
