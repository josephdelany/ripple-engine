"""
extract_prepare.py -- stage a READ-ONLY extraction bundle for the Cowork worker (living-engine step 1).

The watcher already pulls live news into data/alert_queue.csv (sourced, deduped, entity-matched). This
module bundles the alerts that (a) carry a real http source_url and (b) have not been extracted before,
into data/extract/inbox_<ts>.json -- a manifest the Cowork worker (Claude on Joe's subscription, NO API
key) reads to PROPOSE codebook-coded candidate events. It GENERATES nothing and SCORES nothing; it only
selects already-sourced alerts and stamps the allowed event vocabulary into the bundle for convenience.

Dedup uses a new `extract_seen` table in the watch_seen.db SIDECAR (keeps oil.db clean), keyed by the
SAME sha1(url) scheme watcher.is_new uses -- so "seen for alerting" and "seen for extraction" share a
key but are tracked independently.

Run:  python3 src/extract_prepare.py
"""

import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from load_events import VALID_TYPES

ROOT = Path(__file__).resolve().parent.parent
ALERT_QUEUE = ROOT / "data" / "alert_queue.csv"
SEEN_DB = ROOT / "data" / "watch_seen.db"
EXTRACT_DIR = ROOT / "data" / "extract"
SKIP_STATUS = {"dismissed"}          # everything else (new/seen/promoted) is eligible to extract once
MAX_BUNDLE = 40                      # keep a bundle small enough for one focused worker pass


def _hash(url):
    return hashlib.sha1((url or "").encode("utf-8", "replace")).hexdigest()


def open_seen():
    conn = sqlite3.connect(SEEN_DB)
    conn.execute("CREATE TABLE IF NOT EXISTS extract_seen "
                 "(url_hash TEXT PRIMARY KEY, first_seen TEXT)")
    conn.commit()
    return conn


def unextracted(alerts, seen):
    """Alerts with a real http source we haven't bundled before (does NOT mark them -- marking happens
    only after the worker's proposals are caged, so a lost bundle can be rebuilt)."""
    out = []
    for a in alerts:
        url = (a.get("url") or "").strip()
        if not url.startswith("http"):
            continue
        if (a.get("status") or "").strip().lower() in SKIP_STATUS:
            continue
        if seen.execute("SELECT 1 FROM extract_seen WHERE url_hash=?", (_hash(url),)).fetchone():
            continue
        out.append(a)
    return out


def build_bundle():
    if not ALERT_QUEUE.exists():
        return None, []
    with open(ALERT_QUEUE, newline="", encoding="utf-8") as f:
        alerts = list(csv.DictReader(f))
    seen = open_seen()
    fresh = unextracted(alerts, seen)[:MAX_BUNDLE]
    seen.close()
    if not fresh:
        return None, []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    bundle = {
        "batch_id": f"inbox_{now}",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "allowed_types": sorted(VALID_TYPES),          # closed vocab travels with the data
        "instructions_ref": "ops/extract_agent.md",
        "alerts": [{
            "alert_id": _hash(a.get("url", "")),
            "timestamp_utc": a.get("timestamp_utc", ""),
            "source": a.get("source", ""),
            "headline": a.get("headline", ""),
            "url": a.get("url", ""),
            "matched_entities": a.get("matched_entities", ""),
            "matched_keywords": a.get("matched_keywords", ""),
            "heuristic_type": a.get("heuristic_type", ""),
        } for a in fresh],
    }
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    path = EXTRACT_DIR / f"{bundle['batch_id']}.json"
    path.write_text(json.dumps(bundle, indent=2))
    return path, fresh


def main():
    path, fresh = build_bundle()
    if not path:
        print("extract_prepare: no un-extracted sourced alerts to bundle (no-op).")
        return
    print(f"extract_prepare: wrote {path.relative_to(ROOT)} with {len(fresh)} alert(s) for the worker.")
    print("  next: the Cowork worker reads it per ops/extract_agent.md and writes "
          f"data/extract/proposals_<batch>.json; then extract_events.py cages it.")


if __name__ == "__main__":
    main()
