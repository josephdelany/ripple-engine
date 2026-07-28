"""
import_state.py -- load the committed memory CSVs back into a rebuilt oil.db.

Counterpart to export_state.py. After a from-zero rebuild (repro.sh / init_db +
fetch_*), the situation_log and reads tables are empty; this refills them from
data/state/*.csv so the accumulated memory survives the rebuild. Idempotent:
situation_log uses INSERT OR IGNORE against its UNIQUE(situation_id, source_url),
so running it twice (or after the live cycle re-attaches alerts) adds nothing.

Empty CSV cells are restored as SQL NULL (not ""), so numeric columns like a
pending read's realized_car stay properly null.

Run:  python3 src/import_state.py
"""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
STATE = ROOT / "data" / "state"
TABLES = ("situation_log", "reads", "forecasts")


def import_table(conn, table):
    path = STATE / f"{table}.csv"
    if not path.exists():
        return 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        if not cols:
            return 0
        placeholders = ",".join("?" for _ in cols)
        sql = (f"INSERT OR IGNORE INTO {table} ({','.join(cols)}) "
               f"VALUES ({placeholders})")
        before = conn.total_changes
        for row in reader:
            # "" -> NULL so numeric/nullable columns round-trip correctly.
            conn.execute(sql, [row[c] if row[c] != "" else None for c in cols])
    conn.commit()
    return conn.total_changes - before


def main():
    conn = sqlite3.connect(DB)
    print("import_state -- restoring durable memory:")
    for table in TABLES:
        n = import_table(conn, table)
        print(f"  {table:<16} {n:>5} rows loaded")
    conn.close()


if __name__ == "__main__":
    main()
