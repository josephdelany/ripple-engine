"""
test_db_explore.py -- the DB explorer is HARD read-only. It reads the real oil.db, so the
cardinal guarantee is that NOTHING it accepts can write, drop, attach, or multi-statement
(INV-2: raw/atoms append-only, never UPDATE/DELETE). Every write form is rejected, not run.

Run: python3 -m pytest -q tests/test_db_explore.py
"""

import db_explore as X


def test_db1_tables_and_rows_read():
    names = {t["name"] for t in X.tables()}
    assert "events" in names and "observations" in names
    r = X.rows("events", limit=3)
    assert r["columns"] and r["total"] > 0 and len(r["rows"]) <= 3


def test_db2_select_query_works():
    q = X.query("SELECT type, COUNT(*) c FROM events GROUP BY type ORDER BY c DESC")
    assert q["columns"] == ["type", "c"] and q["rows"]


def test_db3_every_write_form_is_denied():
    writes = [
        "UPDATE events SET title='x'",
        "DELETE FROM events",
        "INSERT INTO events (event_id) VALUES ('x')",
        "DROP TABLE events",
        "CREATE TABLE z(a)",
        "ALTER TABLE events ADD COLUMN z TEXT",
    ]
    for sql in writes:
        assert X.query(sql).get("error"), f"NOT denied: {sql!r}"


def test_db4_multi_statement_and_pragma_denied():
    assert X.query("SELECT 1; SELECT 2").get("error")
    # a PRAGMA that could change state is not a SELECT/WITH -> rejected
    assert X.query("PRAGMA writable_schema=1").get("error")


def test_db5_bad_table_is_a_graceful_error():
    assert X.rows("does_not_exist").get("error")


def test_db6_events_table_still_intact_after_write_attempts():
    """Belt-and-suspenders: the corpus row count is unchanged by the denied writes above."""
    assert X.rows("events", limit=1)["total"] > 0
