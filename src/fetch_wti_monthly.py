"""fetch_wti_monthly.py -- the 1946+ monthly spine (FRED WTISPLC, keyless).

Daily Brent starts 1987-05; the corpus starts 1973-10. This loads FRED's spliced monthly
WTI (1946-01 ->) as `fred.WTISPLC` so the point-in-time read, Big Moves and the walk can
stand at 1973, 1979, 1985 -- at MONTHLY resolution, labelled as such on every surface.

Order: fetch from FRED (no key) -> on any failure, load data/seed/wtisplc_monthly.txt
(transcribed from the FRED table on 2026-09-02; the seed is overwritten by a successful
fetch so the two never diverge silently). Idempotent: rows are upserted by (series, date).

Run:  python3 src/fetch_wti_monthly.py
"""
import re
import sqlite3
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
SEED = ROOT / "data" / "seed" / "wtisplc_monthly.txt"
SID = "fred.WTISPLC"
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=WTISPLC"


def parse_seed(text):
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\s*(\d{4}):\s*(.+)$", line)
        if not m:
            continue
        y = int(m.group(1))
        for i, v in enumerate([x.strip() for x in m.group(2).split(",") if x.strip()]):
            rows.append((f"{y}-{i + 1:02d}-01", float(v)))
    return rows


def parse_fred_csv(text):
    rows = []
    for line in text.splitlines()[1:]:
        d, v = (line.split(",") + [""])[:2]
        if re.match(r"^\d{4}-\d{2}-\d{2}$", d) and v not in ("", "."):
            rows.append((d, float(v)))
    return rows


def fetch():
    try:
        with urllib.request.urlopen(URL, timeout=20) as r:
            rows = parse_fred_csv(r.read().decode("utf-8"))
        if len(rows) > 900:
            SEED.parent.mkdir(parents=True, exist_ok=True)
            by_year = {}
            for d, v in rows:
                by_year.setdefault(int(d[:4]), []).append(f"{v:g}")
            head = "\n".join(l for l in SEED.read_text().splitlines() if l.startswith("#")) if SEED.exists() else "# FRED WTISPLC monthly"
            SEED.write_text(head + "\n" + "\n".join(f"{y}: {','.join(vs)}" for y, vs in sorted(by_year.items())) + "\n")
            return rows, "fred"
    except Exception as e:                      # offline, blocked, or FRED down -> seed
        sys.stderr.write(f"fetch failed ({e.__class__.__name__}); using seed\n")
    return parse_seed(SEED.read_text()), "seed"


def load(rows, source):
    conn = sqlite3.connect(DB)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn.execute("INSERT OR REPLACE INTO series (series_id, name, entity_id, unit, frequency, source, source_url, notes) "
                 "VALUES (?,?,?,?,?,?,?,?)",
                 (SID, "WTI spot, monthly spliced (1946-)", "commodity.wti", "$/bbl", "monthly", "FRED",
                  "https://fred.stlouisfed.org/series/WTISPLC",
                  f"Monthly spine for the pre-1987 record; loaded from {source} {now[:10]}. Monthly resolution: "
                  "horizons on this series are months, and every surface says so."))
    n = 0
    for d, v in rows:
        conn.execute("INSERT OR REPLACE INTO observations (series_id, obs_date, value, as_of, retrieved_at) VALUES (?,?,?,?,?)",
                     (SID, d, v, d, now))
        n += 1
    conn.commit(); conn.close()
    return n


if __name__ == "__main__":
    rows, source = fetch()
    n = load(rows, source)
    print(f"{SID}: {n} monthly observations {rows[0][0]} -> {rows[-1][0]} (from {source})")
