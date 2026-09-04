> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Operations runbook for the legacy autonomous feeds, which are archived and inert. Not part of the submitted product; see [`README.md`](../README.md).

# Ops — scheduling the daily refresh (macOS launchd)

This makes the engine refresh itself every morning without you typing anything.
It is **not installed automatically** — you run two commands, once. You stay in
control: nothing schedules itself.

## What it does
Every day at **07:30 local time**, macOS runs:

```
python3 src/daily.py
```

`daily.py` runs the whole pipeline in order — **refresh → heartbeat → watcher →
digest** — behind a lockfile (so two runs can never overlap), times each step, and
ends with a one-line **OK / DEGRADED** verdict that says what to look at. All
output is captured to `data/launchd_refresh.log`.

## Before you install — sanity-check the paths
The plist has two machine-specific absolute paths. Confirm they match your machine:

```bash
which python3
# expected: /usr/local/bin/python3   (edit the plist if yours differs)
```
The repo path in the plist is
`/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine`.
If you moved the repo, edit both paths in `ops/com.ripple.refresh.plist` first.

## Install (run once)
```bash
cp "ops/com.ripple.refresh.plist" ~/Library/LaunchAgents/com.ripple.refresh.plist
launchctl load ~/Library/LaunchAgents/com.ripple.refresh.plist
```

That's it — it will now run every day at 07:30.

## Test it now (optional, don't wait until tomorrow)
```bash
launchctl start com.ripple.refresh          # runs it immediately
cat data/launchd_refresh.log                 # see what happened
```

## Check it's registered
```bash
launchctl list | grep com.ripple.refresh     # shows the job (a PID or last exit code)
```

## Uninstall
```bash
launchctl unload ~/Library/LaunchAgents/com.ripple.refresh.plist
rm ~/Library/LaunchAgents/com.ripple.refresh.plist
```

## Keep the Intelligence Desk always-on (optional, run once)
The daily/hourly jobs above keep the DATA fresh. To keep the **Desk itself serving**
at `http://127.0.0.1:5050/workbench` without leaving a Terminal open — so it survives
logout, sleep, and reboot — install the keep-alive agent (`KeepAlive` restarts it if it
ever exits):

```bash
cp "ops/com.ripple.desk.plist" ~/Library/LaunchAgents/com.ripple.desk.plist
launchctl load ~/Library/LaunchAgents/com.ripple.desk.plist
launchctl list | grep com.ripple.desk        # confirm it's registered
```

Then open http://127.0.0.1:5050/workbench any time. To stop/uninstall:
```bash
launchctl unload ~/Library/LaunchAgents/com.ripple.desk.plist
rm ~/Library/LaunchAgents/com.ripple.desk.plist
```
If you'd rather not install it, just run `python3 src/backend.py` in a Terminal you
leave open — same result while that window lives.

## Notes
- If your Mac is asleep at 07:30, launchd runs the job at the next wake. That is
  expected launchd behaviour.
- `heartbeat.py` exits non-zero when something is STALE/DEAD or the last refresh
  failed. launchd records that exit code (see `launchctl list`); it does not pop
  an alert. To read the health at any time: `python3 src/heartbeat.py`.
- Logs: `data/launchd_refresh.log` (this run's console), `data/refresh_log.csv`
  (per-step history), `data/health_status.json` (latest freshness snapshot).
