"""WS-S05..S09, N01 GPR: GPRH exists for 1914-08 (PATH's named value), knowable on 1914-09-01; country
columns map through the country table; an unknown country column is reported, not dropped silently."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import gpr as M


def test_s08_fixture_gprh_1914_08_exists_and_is_knowable_next_month():
    rows = M.parse(FIX / "gpr" / "data_gpr_export.csv", release="2026-09-02")
    check_rows(rows, M.FIELDS)
    h = [r for r in rows if r["field"] == "gprh_monthly" and r["obs_date"] == "1914-08-01"]
    assert len(h) == 1 and h[0]["value"] > 400 and h[0]["vintage"] == "1914-09-01" and h[0]["retrospective"] == 1
    assert not [r for r in rows if r["field"] == "gpr_monthly" and r["obs_date"] == "1914-08-01"]      # Recent GPR starts 1985: no row, no fill
    usa = [r for r in rows if r["field"] == "gpr_country_monthly" and r["entity_id"] == "country.usa"]
    assert usa and all(r["vintage"] > r["obs_date"] for r in usa)
    assert M.parse.unmapped == ["XXX"]


def test_s08_live_smoke():
    live_or_skip(P.raw_path("gpr", "data_gpr_export.xls"))
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 10000
        v = P.value_at(conn, "world", "gprh_monthly", "1914-09-01")
        assert v and v["obs_date"] == "1914-08-01" and round(v["value"], 1) == 472.3
        assert P.value_at(conn, "world", "gprh_monthly", "1914-08-15")["obs_date"] == "1914-07-01"          # August not yet knowable mid-August
        g = P.value_at(conn, "world", "gpr_monthly", "2001-09-11")
        assert g and g["obs_date"] == "2001-08-01"
    finally:
        conn.close(); os.remove(db)
