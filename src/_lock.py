"""
_lock.py -- a shared atomic lockfile (extracted from daily.py so watch_cycle.py can reuse it).

WHY: two schedulers now run against one repo -- the heavy daily refresh and the light hourly news
watch. Each needs its OWN lock so they never collide, but both want the same proven mechanic: an
atomic O_EXCL create (only one process can win), with a stale-lock reclaim so a crashed run doesn't
wedge the pipeline forever. This is the identical logic daily.py used inline; it now lives in one
place, parameterized by lock path + stale age.
"""

import os
from datetime import datetime, timezone
from pathlib import Path


def acquire(lock_path, stale_secs=2 * 3600):
    """Atomic lockfile at `lock_path`. Returns True if we hold it, False if another run is active.
    A lock older than `stale_secs` is treated as abandoned and reclaimed (a crashed run)."""
    lock = Path(lock_path)
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        age = _age(lock)
        if age is not None and age < stale_secs:
            return False
        lock.unlink(missing_ok=True)
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return False                      # someone else reclaimed it in the race; yield
    os.write(fd, f"{os.getpid()} {datetime.now(timezone.utc).isoformat()}\n".encode())
    os.close(fd)
    return True


def release(lock_path):
    """Release the lock (best-effort; safe to call even if we never held it)."""
    Path(lock_path).unlink(missing_ok=True)


def _age(lock):
    try:
        import time
        return time.time() - lock.stat().st_mtime
    except OSError:
        return None
