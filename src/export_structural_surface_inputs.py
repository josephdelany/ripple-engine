"""Export the minimal, transparent input bundle for the central experiment."""
import argparse
import csv
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLES = {
    "events.csv": ("SELECT event_id,event_date,type,title,date_precision FROM events ORDER BY event_date,event_id",
                   ("event_id", "event_date", "type", "title", "date_precision")),
    "market_observations.csv": (
        "SELECT series_id,obs_date,value,as_of FROM observations WHERE series_id IN "
        "('fred.DCOILBRENTEU','fred.DCOILWTICO','fred.VIXCLS') ORDER BY series_id,obs_date,as_of",
        ("series_id", "obs_date", "value", "as_of")),
    "situation_state.csv": (
        "SELECT event_id,entity_id,field,obs_date,value,value_text,vintage,release,retrospective,source,joined_at "
        "FROM situation_state ORDER BY event_id,field,entity_id",
        ("event_id", "entity_id", "field", "obs_date", "value", "value_text", "vintage", "release",
         "retrospective", "source", "joined_at")),
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def export(db, out):
    out.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    manifest = {"source_database_sha256": sha(db), "files": {}}
    try:
        for name, (query, cols) in TABLES.items():
            path = out / name
            with path.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(cols)
                n = 0
                for row in conn.execute(query):
                    w.writerow(row); n += 1
            manifest["files"][name] = {"rows": n, "sha256": sha(path)}
    finally:
        conn.close()
    (out / "bundle_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "structural_surface" / "input")
    args = ap.parse_args()
    print(json.dumps(export(args.db, args.out), indent=2))


if __name__ == "__main__":
    main()
