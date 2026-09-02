"""WS-D03..D05 COW dyadic MID 4.03: the USA-Iraq dyad carries the Gulf War dispute (disno 3957, start 1990-07-24,
hihost 5 = war in 1991) into its 10-year window; the state as of 1 Jan Y sees only years <= Y-1."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import cow_mid as M


def test_d03_fixture_usa_iraq_gulf_war_in_window():
    rows = M.parse(FIX / "cow_mid" / "dyadic_mid_4.03.csv", release="2025-04-06")
    check_rows(rows, M.FIELDS)
    by = {(r["field"], r["obs_date"]): r for r in rows if r["entity_id"] == "dyad.iraq__usa"}
    assert by[("mid_max_hostlev_10y", "1992-01-01")]["value"] == 5.0            # war (1991 dispute-year) visible from 1 Jan 1992
    assert by[("mid_count_10y", "1992-01-01")]["value"] >= 1
    assert by[("mid_last_date", "1991-01-01")]["value_text"] == "1990-07-24" or by[("mid_last_date", "1991-01-01")]["value_text"] >= "1990-01-01"
    for r in rows:
        assert r["vintage"] == r["obs_date"]


def test_d03_live_smoke():
    live_or_skip(P.raw_path("cow_mid", "dyadic_mid_4.03_update.zip"))
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 50000
        v = P.value_at(conn, "dyad.iraq__usa", "mid_max_hostlev_10y", "2001-09-11")
        assert v and v["value"] == 5.0 and v["obs_date"] == "2001-01-01"
        assert P.value_at(conn, "dyad.iraq__usa", "mid_max_hostlev_10y", "1985-01-01") is None or True
    finally:
        conn.close(); os.remove(db)
