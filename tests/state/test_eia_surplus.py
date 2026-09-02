"""WS-P01 EIA surplus capacity: 1985 = 11.3 mb/d (the page's stated peak); vintage never null."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import eia_surplus as M


def test_p01_fixture_reproduces_1985_peak_11_3():
    rows = M.parse(FIX / "eia_surplus" / "figure2.xlsx", release="2022-06-09")
    check_rows(rows, M.FIELDS)
    v85 = [r for r in rows if r["entity_id"] == "world" and r["obs_date"] == "1985-01-01"][0]
    assert round(v85["value"], 1) == 11.3
    assert v85["vintage"] == "1986-01-01" and v85["retrospective"] == 1     # knowable 1 Jan 1986; a 2022 reconstruction
    assert {r["entity_id"] for r in rows} == {"world", "opec", "region.non_opec"}
    assert min(r["obs_date"] for r in rows) == "1970-01-01" and max(r["obs_date"] for r in rows) == "2021-01-01"


def test_p01_live_smoke_point_in_time():
    live_or_skip(P.raw_path("eia_surplus", "figure2.xlsx"))
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 100
        at86 = P.value_at(conn, "world", "surplus_capacity_world", "1986-06-01")
        assert at86 and round(at86["value"], 1) == 11.3 and at86["release"]
        assert P.value_at(conn, "world", "surplus_capacity_world", "1969-12-31") is None     # nothing knowable before the series
    finally:
        conn.close(); os.remove(db)
