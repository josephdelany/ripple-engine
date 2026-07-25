"""
data_dictionary.py -- write DATA_DICTIONARY.md from the LIVE schema of oil.db.

The dictionary is GENERATED, never hand-typed, so it can never drift from the
actual database: every table, every column, and every series (with its unit,
cadence and source) is read straight out of the file. Read-only.

Run:  python3 src/data_dictionary.py
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "DATA_DICTIONARY.md"


def main():
    conn = sqlite3.connect(DB)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND "
        "name NOT LIKE 'sqlite_%' ORDER BY name")]

    L = ["# Data dictionary", "",
         "_Generated from the live schema of `data/oil.db` by "
         "`src/data_dictionary.py` — not hand-typed, so it cannot drift from the "
         "actual database._", ""]

    for t in tables:
        cols = conn.execute(f"PRAGMA table_info({t})").fetchall()  # cid,name,type,notnull,dflt,pk
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        L += [f"## `{t}` — {n:,} rows", "",
              "| column | type | not null | pk |", "|---|---|---|---|"]
        for c in cols:
            L.append(f"| {c[1]} | {c[2] or ''} | {'yes' if c[3] else ''} "
                     f"| {'yes' if c[5] else ''} |")
        L.append("")

    # The series catalogue: every series_id with its provenance.
    L += ["## Series catalogue (`series_id` → unit, cadence, source)", "",
          "| series_id | unit | frequency | source |", "|---|---|---|---|"]
    for sid, unit, freq, src in conn.execute(
            "SELECT series_id, unit, frequency, source FROM series ORDER BY series_id"):
        L.append(f"| `{sid}` | {unit or ''} | {freq or ''} | {src or ''} |")
    conn.close()

    OUT.write_text("\n".join(L) + "\n")
    print(f"Wrote {OUT} ({len(tables)} tables).")


if __name__ == "__main__":
    main()
