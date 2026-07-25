"""
integrity.py -- guard the database, and keep a week of backups.

Silent data loss is this project's historic failure mode, so this is the tripwire.
Each run it checks the canonical oil.db four ways and then takes a compressed,
rotated backup:

  1. PRAGMA integrity_check -- is the SQLite file structurally sound?
  2. Row-count deltas vs the last run -- and it shouts if ANY table SHRANK (a
     table losing rows is almost always a bug or a bad edit, never normal growth).
  3. Orphans -- event_entities / edges rows pointing at an event_id that no longer
     exists in events.
  4. Duplicate observation keys -- any (series_id, obs_date) carrying more than one
     row (would mean the same reading landed twice).

Then it writes a gzipped copy of oil.db into data/backups/ and keeps the 7 newest.

Exits non-zero if any check fails, so daily.py degrades the day and says look here.

Run:  python3 src/integrity.py
"""

import gzip
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
BACKUPS = ROOT / "data" / "backups"
STATE = ROOT / "data" / "integrity_state.json"
OUT = ROOT / "data" / "integrity_report.txt"
KEEP = 7                      # rotate: keep the 7 newest compressed backups


def take_backup():
    """A gzipped, timestamped copy of oil.db; keep only the KEEP newest."""
    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    dest = BACKUPS / f"oil_{stamp}.db.gz"
    with open(DB, "rb") as src, gzip.open(dest, "wb") as gz:
        shutil.copyfileobj(src, gz)
    backups = sorted(BACKUPS.glob("oil_*.db.gz"))
    for old in backups[:-KEEP]:
        old.unlink()
    return dest.name, len(backups) - len(backups[:-KEEP]) if len(backups) > KEEP else len(backups)


def main():
    conn = sqlite3.connect(DB)
    problems, lines = [], []
    w = lines.append
    w("=" * 70)
    w(f"INTEGRITY REPORT  --  {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    w("=" * 70)

    # 1. structural integrity
    ic = conn.execute("PRAGMA integrity_check").fetchone()[0]
    w(f"1. PRAGMA integrity_check: {ic}")
    if ic != "ok":
        problems.append("integrity_check failed")

    # 2. row counts + deltas (shrink = loud)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND "
        "name NOT LIKE 'sqlite_%' ORDER BY name")]
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
    last = json.loads(STATE.read_text()) if STATE.exists() else {}
    w("\n2. Row counts (delta vs last run):")
    for t in tables:
        prev = last.get(t)
        if prev is None:
            w(f"   {t:<18} {counts[t]:>8,}   (baseline, no prior run)")
        else:
            d = counts[t] - prev
            flag = "  <<< SHRANK" if d < 0 else ""
            w(f"   {t:<18} {counts[t]:>8,}   {d:+,}{flag}")
            if d < 0:
                problems.append(f"{t} shrank by {-d}")

    # 3. orphans
    orphan_ee = conn.execute(
        "SELECT COUNT(*) FROM event_entities WHERE event_id NOT IN "
        "(SELECT event_id FROM events)").fetchone()[0]
    orphan_edges = conn.execute(
        "SELECT COUNT(*) FROM edges WHERE event_id IS NOT NULL AND event_id NOT IN "
        "(SELECT event_id FROM events)").fetchone()[0]
    w(f"\n3. Orphans:  event_entities -> events: {orphan_ee}   "
      f"edges -> events: {orphan_edges}")
    if orphan_ee or orphan_edges:
        problems.append(f"orphans (ee={orphan_ee}, edges={orphan_edges})")

    # 4. duplicate observation keys
    dup = conn.execute(
        "SELECT COUNT(*) FROM (SELECT series_id, obs_date FROM observations "
        "GROUP BY series_id, obs_date HAVING COUNT(*) > 1)").fetchone()[0]
    w(f"4. Duplicate observation (series_id, obs_date) keys: {dup}")
    if dup:
        problems.append(f"{dup} duplicate observation keys")
    conn.close()

    # backup + persist state
    name, kept = take_backup()
    STATE.write_text(json.dumps(counts, indent=2))
    w(f"\nBackup: wrote data/backups/{name} (keeping {kept} of last {KEEP}).")
    w("=" * 70)
    if problems:
        w(f"STATUS: PROBLEMS -- {'; '.join(problems)}")
    else:
        w("STATUS: OK -- structure sound, no shrink, no orphans, no dup keys.")

    text = "\n".join(lines)
    OUT.write_text(text + "\n")
    print(text)
    raise SystemExit(1 if problems else 0)


if __name__ == "__main__":
    main()
