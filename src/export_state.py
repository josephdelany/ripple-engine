"""
export_state.py -- snapshot the accumulating in-DB memory to committed CSVs.

The big oil.db (~36 MB) is a DERIVED artifact -- it is rebuilt from free sources
on every run (locally or in GitHub Actions), so it is gitignored. But two tables
hold state that CANNOT be re-fetched from any public source: `situation_log` (the
running conflict timeline, incl. the agent's typings and gate promotions) and
`reads` (the calibration ledger). This dumps them to small CSVs under data/state/
which ARE committed -- the durable source of truth. import_state.py loads them back
after a rebuild. Same philosophy the repo already uses for events.csv -> events.

The autoincrement id column is intentionally NOT exported: identities regenerate on
rebuild, and situation_log's UNIQUE(situation_id, source_url) is the real key.

Run:  python3 src/export_state.py
"""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
STATE = ROOT / "data" / "state"
TABLES = ("situation_log", "reads")


def exportable_columns(conn, table):
    """Every column except the autoincrement primary key (pk flag == 1)."""
    return [r[1] for r in conn.execute(f"PRAGMA table_info({table})") if not r[5]]


def export_table(conn, table):
    cols = exportable_columns(conn, table)
    rows = conn.execute(f"SELECT {','.join(cols)} FROM {table} "
                        f"ORDER BY 1").fetchall()
    path = STATE / f"{table}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
    return len(rows), path


def main():
    STATE.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    print("export_state -- durable memory snapshot:")
    for table in TABLES:
        n, path = export_table(conn, table)
        print(f"  {table:<16} {n:>5} rows -> {path.relative_to(ROOT)}")
    conn.close()


if __name__ == "__main__":
    main()
