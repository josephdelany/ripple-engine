"""
daily.py -- the one-command day. The autonomous loop, made ready, not switched on.

It runs the whole daily pipeline in order -- refresh -> heartbeat -> watcher cycle
-> digest -- behind a LOCKFILE so two runs can never overlap and corrupt each
other, times every step, and ends with a single honest verdict line
(OK / DEGRADED) that says exactly what to look at. Nothing schedules this; a human
or (once Joe chooses) a launchd agent runs it.

refresh.py always exits 0 (its own step failures live in the log); heartbeat.py
exits non-zero when data is STALE/DEAD or the last refresh failed -- that is the
health signal daily.py reports, not a crash. A step other than heartbeat exiting
non-zero IS a crash and degrades the day.

Run:  python3 src/daily.py
"""

import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
LOCK = ROOT / "data" / "daily.lock"
STALE_LOCK_SECS = 2 * 3600          # a lock older than this is treated as abandoned
STEP_TIMEOUT = 1200                 # generous; refresh pulls ~20 COT archives

# (name, argv-after-python, is_health_gate). heartbeat's non-zero exit is health,
# not a crash; every other step's non-zero exit is a crash.
STEPS = [
    ("refresh",   ["src/refresh.py"],   False),
    ("integrity", ["src/integrity.py"], False),   # right after refresh: guard + backup
    ("heartbeat", ["src/heartbeat.py"], True),
    ("watcher",   ["src/watcher.py"],   False),
    ("notify",    ["src/notify.py"],    False),   # push high-signal alerts (idempotent; dry-run w/o NTFY_TOPIC)
    ("digest",    ["src/digest.py"],    False),
]
LAST_RUN = ROOT / "data" / "last_run.json"


def acquire_lock():
    """Atomic lockfile. Returns True if we hold it, False if another run is active."""
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        age = time.time() - LOCK.stat().st_mtime
        if age < STALE_LOCK_SECS:
            print(f"daily.py: another run is active (lock held {age:.0f}s). Exiting.")
            return False
        print(f"daily.py: stale lock ({age:.0f}s old) -- reclaiming.")
        LOCK.unlink(missing_ok=True)
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, f"{os.getpid()} {datetime.now(timezone.utc).isoformat()}\n".encode())
    os.close(fd)
    return True


def run_step(argv):
    t0 = time.perf_counter()
    try:
        p = subprocess.run([PY, *argv], cwd=ROOT, capture_output=True, text=True,
                           timeout=STEP_TIMEOUT)
        rc, tail = p.returncode, (p.stderr or p.stdout or "").strip().splitlines()
    except subprocess.TimeoutExpired:
        return 124, time.perf_counter() - t0, f"timeout after {STEP_TIMEOUT}s"
    except Exception as e:
        return 1, time.perf_counter() - t0, f"{type(e).__name__}: {e}"
    return rc, time.perf_counter() - t0, (tail[-1] if tail else "")


def main():
    if not acquire_lock():
        sys.exit(0)
    try:
        run_id = datetime.now(timezone.utc).isoformat(timespec="seconds")
        print(f"Daily run {run_id}\n" + "=" * 60)
        crashes, health_trouble = [], False
        t_start = time.perf_counter()
        for name, argv, is_health in STEPS:
            rc, dur, note = run_step(argv)
            ok = (rc == 0)
            state = "OK" if ok else ("HEALTH" if is_health else "FAILED")
            print(f"  {name:<11} {state:<7} {dur:>6.1f}s   {note[:70]}")
            if is_health and not ok:
                health_trouble = True
            elif not ok:
                crashes.append(name)

        # --- One honest verdict line ---
        print("=" * 60)
        verdict = "OK" if not (crashes or health_trouble) else "DEGRADED"
        if crashes:
            print(f"VERDICT: DEGRADED -- step(s) failed: {', '.join(crashes)}. "
                  f"Look at data/refresh_log.csv and rerun that step.")
        elif health_trouble:
            print("VERDICT: DEGRADED -- data is stale/dead or the last refresh had "
                  "failures. Run: python3 src/heartbeat.py (see the STALE/DEAD rows).")
        else:
            print("VERDICT: OK -- pipeline fresh. Read it at "
                  "http://127.0.0.1:5050/digest")

        # --- Machine-readable verdict for the monitoring surface + conversational layer ---
        import json
        LAST_RUN.write_text(json.dumps({
            "run_id": run_id, "verdict": verdict, "duration_s": round(time.perf_counter() - t_start, 1),
            "failed_steps": crashes, "health_trouble": health_trouble,
        }, indent=2))
        sys.exit(1 if (crashes or health_trouble) else 0)
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
