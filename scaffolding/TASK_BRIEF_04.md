# Task Brief 04 — Automation & Reliability (the engine runs itself)

*Read CLAUDE.md first; its rules override this brief. Commit after each step. Goal: the engine stays current daily without Joe typing anything, and NOTHING can fail silently — silent failure is this project's historic killer.*

## Step 1 — One-command refresh (`src/refresh.py`)
A single orchestrator that runs, in order, with per-step error capture (one step failing must NOT stop the others): fetch_prices → fetch_series → fetch_eia → fetch_cot → derive_signals → load_events (idempotent sync). Each step logs: name, started, duration, rows written, OK/FAILED + the error text. Results append to `data/refresh_log.csv` (timestamp, step, status, detail). Print a clean end-of-run summary table. Commit.

## Step 2 — Heartbeat / staleness monitor (`src/heartbeat.py`)
Reads the canonical DB and reports, per series: last observation date, expected cadence (daily/weekly from the series table), and a status — OK / STALE (a fresh reading is overdue by >2× its cadence) / DEAD (>4×). Also checks: events table row count, forecast log pending count, and whether refresh_log shows failures in the last run. Writes `data/health_status.json` and prints a human-readable report. Exit code non-zero if anything is STALE/DEAD or the last refresh had failures (so wrappers can detect trouble). Commit.

## Step 3 — Health widget
Add a `system_health` table-widget to src/backend.py (same pattern as the others) reading health_status.json: series, last update, status. Do NOT restart the running server — Joe restarts it. Commit.

## Step 4 — Scheduling (macOS)
Create `ops/com.ripple.refresh.plist` — a launchd agent running `python3 src/refresh.py && python3 src/heartbeat.py` daily at 07:30 local — plus `ops/INSTALL.md` with the exact two commands Joe runs once to install it (cp to ~/Library/LaunchAgents + launchctl load), and how to uninstall. Do not install it yourself — Joe decides. Commit.

## Step 5 — Ops section in README
Short section: how to refresh manually, how to read the health report, what STALE means, where logs live. Commit.

## Out of scope
No new data sources. No analysis changes. No edits to registered/brief files. No touching the running servers.

## Done when
`python3 src/refresh.py` runs end-to-end with a summary, `python3 src/heartbeat.py` prints an honest health report, the widget serves, the plist + install doc exist, all committed.
