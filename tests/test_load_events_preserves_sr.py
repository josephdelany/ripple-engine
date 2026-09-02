"""load_events must never blank the situation-record columns (sr_*) that events.csv does not carry.
Regression for the 2026-09-02 refresh, which wiped sr_* on every CSV-loaded event via INSERT OR REPLACE. DB-free."""
import sqlite3

import load_events as LE


def test_le1_upsert_keeps_sr_columns_and_added_at():
    conn = sqlite3.connect(":memory:"); cur = conn.cursor()
    cur.execute("CREATE TABLE events (event_id TEXT PRIMARY KEY, event_date TEXT, date_precision TEXT, type TEXT, title TEXT, "
                "description TEXT, severity INTEGER, surprise INTEGER, confidence TEXT, source_url TEXT, added_at TEXT, "
                "sr_actor TEXT, sr_outcome_90 TEXT)")
    row = {"event_id": "e1", "event_date": "2019-09-14", "date_precision": "day", "type": "infrastructure_attack", "title": "Abqaiq",
           "description": "d", "severity": "4", "surprise": "4", "confidence": "high", "source_url": "http://x"}
    LE.upsert_event(cur, row, "2026-01-01T00:00:00")
    cur.execute("UPDATE events SET sr_actor='country.iran', sr_outcome_90='CONTAINED' WHERE event_id='e1'")
    LE.upsert_event(cur, {**row, "title": "Abqaiq (edited)"}, "2026-09-02T00:00:00")          # a re-load with an edited title
    t, a, o, added = cur.execute("SELECT title, sr_actor, sr_outcome_90, added_at FROM events WHERE event_id='e1'").fetchone()
    assert t == "Abqaiq (edited)" and a == "country.iran" and o == "CONTAINED" and added == "2026-01-01T00:00:00"
    assert cur.execute("SELECT count(*) FROM events").fetchone()[0] == 1
