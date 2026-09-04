"""Export the IMF PortWatch daily chokepoint slice to a committed, redistributable CSV.

v2 could not commit its inputs, so its experiment reproduces only from a bundle whose own upstream
is unverifiable (`docs/audit/PROVENANCE_BOUNDARY.md`). PortWatch is different: the IMF terms permit
redistribution of the published daily aggregates with attribution, so v3's input can live in the
repository and the whole chain below it can be independently reproduced.

This is the only script in v3 that touches `data/oil.db`. Everything downstream reads the CSV.

Sources: UN Global Platform; IMF PortWatch.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "v3"

ATTRIBUTION = "Sources: UN Global Platform; IMF PortWatch."
LICENCE = (
    "IMF Terms and Conditions, Copyright and Usage, special terms for statistical Data "
    "(imf.org/external/terms.htm, effective 2020-01-02): users may download, copy, publish and "
    "distribute Data from IMF Sites, with attribution and no alteration of integrity. Published "
    "daily aggregates only; upstream AIS inputs are third-party and are not redistributed here."
)

QUERY = """
  SELECT series_id, obs_date, value
  FROM observations
  WHERE series_id LIKE 'portwatch.%' AND value IS NOT NULL
  ORDER BY series_id, obs_date
"""


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def export(db=DB, out_dir=OUT):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        rows = conn.execute(QUERY).fetchall()
        units = dict(conn.execute(
            "SELECT series_id, unit FROM series WHERE series_id LIKE 'portwatch.%'"))
    finally:
        conn.close()
    if not rows:
        raise SystemExit("no PortWatch rows found; refusing to write an empty slice")

    path = out_dir / "portwatch_daily.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(("series_id", "obs_date", "value"))
        w.writerows(rows)

    series = sorted({r[0] for r in rows})
    manifest = {
        "attribution": ATTRIBUTION,
        "licence": LICENCE,
        "source_url": "https://portwatch.imf.org/",
        "source_database_sha256": file_sha256(db) if Path(db).exists() else None,
        "n_rows": len(rows),
        "n_series": len(series),
        "series": {s: units.get(s) for s in series},
        "first_obs_date": min(r[1] for r in rows),
        "last_obs_date": max(r[1] for r in rows),
        "files": {path.name: {"sha256": file_sha256(path), "rows": len(rows)}},
    }
    (out_dir / "portwatch_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", type=Path, default=DB)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    m = export(args.db, args.out)
    print(json.dumps({k: v for k, v in m.items() if k != "licence"}, indent=2, sort_keys=True))
    print(ATTRIBUTION)


if __name__ == "__main__":
    main()
