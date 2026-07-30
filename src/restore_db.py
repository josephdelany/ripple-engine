"""
restore_db.py -- restore oil.db from the newest GOOD backup (the missing half of integrity.py).

integrity.py rotates 7 gzipped backups but there was no way to USE one, and no test that a backup is
actually loadable -- so recovery from a corrupt/locked DB was manual guesswork. This restores from the
newest backup that passes PRAGMA integrity_check, atomically, never overwriting the live DB with a
backup that itself fails the check (it falls back to the next-newest). tests/test_restore.py round-trips
a real corrupt->restore, so "restore_tested" can be asserted true, not hoped.

Run:  python3 src/restore_db.py            # restore from newest good backup
      python3 src/restore_db.py --verify   # just report which backups are loadable (no changes)
"""

import gzip
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
BACKUPS = ROOT / "data" / "backups"


def is_good(sqlite_path):
    """True if the SQLite file passes PRAGMA integrity_check."""
    try:
        c = sqlite3.connect(sqlite_path)
        ok = c.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        c.close()
        return ok
    except sqlite3.DatabaseError:
        return False


def newest_good_backup():
    """Return (path, decompressed_temp) for the newest backup that passes integrity_check, or (None,
    None). Caller owns the temp file."""
    for gz in sorted(BACKUPS.glob("oil_*.db.gz"), reverse=True):    # newest first (timestamped names)
        tmp = Path(tempfile.mkstemp(suffix=".db")[1])
        try:
            with gzip.open(gz, "rb") as src, open(tmp, "wb") as out:
                shutil.copyfileobj(src, out)
            if is_good(tmp):
                return gz, tmp
        except OSError:
            pass
        tmp.unlink(missing_ok=True)
    return None, None


def restore():
    gz, tmp = newest_good_backup()
    if not gz:
        return {"restored": False, "reason": "no loadable backup found in data/backups/"}
    shutil.move(str(tmp), str(DB))                 # atomic on the same filesystem
    return {"restored": True, "from": gz.name, "verified": True}


def main():
    if "--verify" in sys.argv:
        good = []
        for gz in sorted(BACKUPS.glob("oil_*.db.gz"), reverse=True):
            tmp = Path(_gunzip(gz))
            if is_good(tmp):
                good.append(gz.name)
            tmp.unlink(missing_ok=True)
        print(f"loadable backups ({len(good)}): {', '.join(good[:5]) or 'none'}")
        return
    res = restore()
    print(f"restore_db: {'restored from ' + res['from'] if res['restored'] else res['reason']}")
    if not res["restored"]:
        sys.exit(1)


def _gunzip(gz):
    tmp = tempfile.mkstemp(suffix=".db")[1]
    with gzip.open(gz, "rb") as src, open(tmp, "wb") as out:
        shutil.copyfileobj(src, out)
    return tmp


if __name__ == "__main__":
    main()
