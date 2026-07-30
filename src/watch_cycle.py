"""
watch_cycle.py -- the light HOURLY news pass (separate from the heavy daily refresh).

Two clocks: the daily refresh (07:30, all the fetch/derive/analysis) and this cheap hourly cycle that
just pulls live news and pushes any high-signal alert to Joe's phone. It holds its OWN lock (watch.lock)
so it can never collide with -- or block -- the daily run, and it always exits 0 (a partial cycle is
fine; a hang is not). Scheduled by ops/com.ripple.watch.plist (StartInterval hourly + RunAtLoad, so it
catches up on wake).

Run:  python3 src/watch_cycle.py
"""

import subprocess
import sys
from pathlib import Path

from _lock import acquire, release

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
LOCK = ROOT / "data" / "watch.lock"
STEPS = ["watcher.py", "notify.py"]          # pull live news, then push high-signal alerts (idempotent)


def main():
    if not acquire(LOCK, stale_secs=1800):
        print("watch_cycle: another watch is active. Exiting.")
        return
    try:
        for s in STEPS:
            try:
                subprocess.run([PY, str(ROOT / "src" / s)], cwd=ROOT, timeout=300)
            except subprocess.TimeoutExpired:
                print(f"   ({s} timed out -- skipped; partial cycle is fine)")
            except Exception as e:               # noqa: BLE001
                print(f"   ({s} error {type(e).__name__} -- skipped)")
        print("watch_cycle: done.")
    finally:
        release(LOCK)


if __name__ == "__main__":
    main()
