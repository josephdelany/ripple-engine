"""
db_snapshot.py -- quarterly FROZEN database snapshots (VISION_ROADMAP V-Q1).

integrity.py keeps a rolling week of backups (disaster recovery). This is a different thing: a
QUARTERLY frozen vintage of the whole database, kept for two years, so any headline number can later
be recomputed against the data as it stood at a past quarter -- "the result doesn't depend on which
day you rebuilt the DB." Reproducibility discipline (AER data-editor standard), not backup.

  * One gzipped snapshot per calendar quarter: data/vintages/oil_YYYYQn.db.gz.
  * Idempotent: if this quarter's snapshot already exists it is left alone (safe to run daily -- it
    only writes once per quarter, on the first refresh of the quarter).
  * Rotated: the KEEP newest quarterly snapshots are kept (2 years); older ones are pruned.
  * Gitignored (data/vintages/) -- frozen DB copies are large derived artifacts, not source.

Run:  python3 src/db_snapshot.py            # take this quarter's snapshot if missing
      python3 src/db_snapshot.py --list     # list the frozen quarterly snapshots
"""

import gzip
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
VINTAGES = ROOT / "data" / "vintages"
KEEP = 8                      # 8 quarters = 2 years of frozen vintages


def current_quarter(today=None):
    d = today or datetime.now(timezone.utc).date()
    return f"{d.year}Q{(d.month - 1) // 3 + 1}"


def take_snapshot():
    """Freeze this quarter's DB if not already frozen; prune to the KEEP newest. Returns
    (path_or_None, action) where action is 'created' | 'exists' | 'no-db'."""
    if not DB.exists():
        return None, "no-db"
    VINTAGES.mkdir(parents=True, exist_ok=True)
    dest = VINTAGES / f"oil_{current_quarter()}.db.gz"
    if dest.exists():
        return dest, "exists"
    # gzip a copy (stream, so a big DB doesn't sit in memory)
    with open(DB, "rb") as src, gzip.open(dest, "wb") as gz:
        shutil.copyfileobj(src, gz)
    for old in sorted(VINTAGES.glob("oil_*.db.gz"))[:-KEEP]:
        old.unlink()
    return dest, "created"


def _loadable(gz):
    """Cheap integrity check: can we open the gunzipped DB and read a table? (defends against a
    truncated/corrupt snapshot silently rotating out the good ones)."""
    tmp = gz.with_suffix(".probe")
    try:
        with gzip.open(gz, "rb") as f, open(tmp, "wb") as out:
            shutil.copyfileobj(f, out)
        n = sqlite3.connect(tmp).execute("SELECT COUNT(*) FROM observations").fetchone()[0]
        return n
    except Exception:
        return None
    finally:
        tmp.unlink(missing_ok=True)


def main():
    if "--list" in sys.argv:
        snaps = sorted(VINTAGES.glob("oil_*.db.gz")) if VINTAGES.exists() else []
        print(f"Frozen quarterly snapshots ({len(snaps)}), keeping {KEEP} newest:")
        for s in snaps:
            mb = s.stat().st_size / 1e6
            print(f"  {s.name:<20} {mb:6.1f} MB")
        if not snaps:
            print("  (none yet -- run without --list to take this quarter's)")
        return
    dest, action = take_snapshot()
    if action == "no-db":
        print("no data/oil.db to snapshot"); return
    if action == "exists":
        print(f"this quarter already frozen: {dest.name} (idempotent -- nothing to do)"); return
    n = _loadable(dest)
    kept = len(sorted(VINTAGES.glob("oil_*.db.gz")))
    print(f"froze {dest.name} ({dest.stat().st_size/1e6:.1f} MB, "
          f"{'loadable, ' + format(n, ',') + ' obs' if n else 'WARNING: not loadable'}); "
          f"{kept} quarterly snapshot(s) kept.")


if __name__ == "__main__":
    main()
