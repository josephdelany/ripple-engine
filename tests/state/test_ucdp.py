"""WS-S01..S03 UCDP v26.1: 40 active conflicts in 2000 (the conflict-year file), knowable 1 Jan 2001; battle deaths
by location country for 1991; nothing for a year before the data."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import ucdp as M


def test_s01_fixture_2000_active_conflicts_40():
    rows = M.parse({"acd": FIX / "ucdp" / "UcdpPrioConflict_v26_1.csv", "brd": FIX / "ucdp" / "BattleDeaths_v26_1_conf.csv"}, release="2026-06-08")
    check_rows(rows, M.FIELDS)
    w = [r for r in rows if r["entity_id"] == "world" and r["field"] == "ucdp_active_conflicts"][0]
    assert w["value"] == 40.0 and w["obs_date"] == "2001-01-01" == w["vintage"]
    bd = [r for r in rows if r["entity_id"] == "country.iraq" and r["field"] == "ucdp_battle_deaths"]
    assert bd and bd[0]["obs_date"] == "1992-01-01" and bd[0]["value"] > 0


def test_s01_live_smoke():
    live_or_skip(P.raw_path("ucdp", "ucdp-prio-acd-261-csv.zip"), P.raw_path("ucdp", "ucdp-brd-conf-261-csv.zip"))
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 3000
        v = P.value_at(conn, "world", "ucdp_active_conflicts", "2001-09-11")
        assert v and v["value"] == 40.0 and v["obs_date"] == "2001-01-01"
        assert P.value_at(conn, "world", "ucdp_active_conflicts", "1946-06-01") is None
    finally:
        conn.close(); os.remove(db)
