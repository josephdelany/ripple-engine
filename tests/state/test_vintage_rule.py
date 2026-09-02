"""PATH Step 3 -- test_vintage_rule.py: a value with vintage > t is invisible at t, through every read path
(panel.value_at, panel.state_at, situation_state.state_at, and the join itself)."""
import os
import sqlite3

from _helpers import P, scratch_conn
import situation_state as SS


def _seed(conn):
    P.write(conn, [
        {"entity_id": "country.usa", "field": "cinc", "obs_date": "2000-01-01", "value": 0.14, "unit": "share", "source": "t", "vintage": "2001-01-01", "release": "2026-01-01"},
        {"entity_id": "country.usa", "field": "cinc", "obs_date": "2001-01-01", "value": 0.15, "unit": "share", "source": "t", "vintage": "2002-01-01", "release": "2026-01-01"},
        {"entity_id": "world", "field": "gpr_monthly", "obs_date": "2001-08-01", "value": 64.1, "unit": "index", "source": "t", "vintage": "2001-09-01", "release": "2026-01-01"},
        {"entity_id": "world", "field": "gpr_monthly", "obs_date": "2001-09-01", "value": 200.0, "unit": "index", "source": "t", "vintage": "2001-10-01", "release": "2026-01-01"},
        {"entity_id": "dyad.iraq__usa", "field": "atop_defense_pact", "obs_date": "2001-01-01", "value": 0.0, "unit": "0/1", "source": "t", "vintage": "2001-01-01", "release": "2026-01-01"},
    ])


def test_vr1_value_at_hides_later_vintage():
    conn, db = scratch_conn()
    try:
        _seed(conn)
        assert P.value_at(conn, "country.usa", "cinc", "2001-09-11")["value"] == 0.14          # 2001's value (vintage 2002) invisible
        assert P.value_at(conn, "country.usa", "cinc", "2002-01-01")["value"] == 0.15
        assert P.value_at(conn, "country.usa", "cinc", "2000-12-31") is None
        g = P.value_at(conn, "world", "gpr_monthly", "2001-09-11")
        assert g["obs_date"] == "2001-08-01" and g["value"] == 64.1                            # September's 200 not knowable on 11 Sept
    finally:
        conn.close(); os.remove(db)


def test_vr2_state_at_and_join_use_the_same_rule():
    conn, db = scratch_conn()
    try:
        _seed(conn)
        st = SS.state_at(conn, "2001-09-11", ["country.usa"], ["dyad.iraq__usa"])
        assert st["country.usa"]["cinc"]["value"] == 0.14 and st["world"]["gpr_monthly"]["value"] == 64.1
        assert st["dyad.iraq__usa"]["atop_defense_pact"]["value"] == 0.0
        # ZERO_IF_ABSENT: a dyad with no ATOP row inside 1815-2018 reads 0 with the rule stated as its source
        st2 = SS.state_at(conn, "2001-09-11", [], ["dyad.iran__usa"])
        assert st2["dyad.iran__usa"]["atop_defense_pact"]["value"] == 0.0 and "absent = none" in st2["dyad.iran__usa"]["atop_defense_pact"]["source"]
        # and outside the window (2019+) it is unknown, not 0
        assert "dyad.iran__usa" not in SS.state_at(conn, "2019-06-01", [], ["dyad.iran__usa"])
        # the join writes exactly what state_at sees
        conn.execute("CREATE TABLE events (event_id TEXT PRIMARY KEY, event_date TEXT, type TEXT, sr_actor TEXT, sr_target TEXT)")
        conn.execute("CREATE TABLE event_entities (event_id TEXT, entity_id TEXT, role TEXT)")
        conn.execute("INSERT INTO events VALUES ('e1','2001-09-11','conflict_escalation','country.usa','country.iraq')")
        conn.execute("INSERT INTO event_entities VALUES ('e1','country.usa','actor')")
        conn.commit()
        SS.join(conn)
        rows = {(e, f): (v, vin) for e, f, v, vin in conn.execute("SELECT entity_id, field, value, vintage FROM situation_state WHERE event_id='e1'")}
        assert rows[("country.usa", "cinc")] == (0.14, "2001-01-01")
        assert rows[("world", "gpr_monthly")] == (64.1, "2001-09-01")
        assert all(vin <= "2001-09-11" for (_e, _f), (_v, vin) in rows.items())                 # nothing with vintage > t
    finally:
        conn.close(); os.remove(db)
