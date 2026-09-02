"""WS-A01..A03 COW NMC v7: CINC USA 2000 = 0.14289317 (PATH's named value), knowable 1 Jan 2001; an unmapped ccode is
reported; the hand country table agrees with the file's own stateabb column (WS-R4)."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import cow_nmc as M
import countries as C


def test_a01_fixture_cinc_usa_2000():
    rows = M.parse(FIX / "cow_nmc" / "NMC-70-abridged.csv", release="2026-06-03")
    check_rows(rows, M.FIELDS)
    usa = [r for r in rows if r["entity_id"] == "country.usa" and r["field"] == "cinc" and r["obs_date"] == "2000-01-01"][0]
    assert usa["value"] == 0.14289317 and usa["vintage"] == "2001-01-01"
    assert M.parse.unmapped == [999]
    for cc, abb in M.parse.stateabb.items():
        ent = C.from_ccode(cc)
        if ent and cc not in C.ALIASES_CCODE:
            assert C.ALL[ent][1] == abb, (ent, abb)


def test_a01_live_smoke_and_country_table_agrees_with_the_data():
    live_or_skip(P.raw_path("cow_nmc", "NMCv7.zip"))
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 15000
        v = P.value_at(conn, "country.usa", "cinc", "2001-09-11")
        assert v and v["obs_date"] == "2000-01-01" and v["value"] == 0.14289317
        assert P.value_at(conn, "country.usa", "cinc", "2000-06-01")["obs_date"] == "1999-01-01"      # 2000 not yet knowable mid-2000
        mism = [(cc, abb, C.ALL[C.from_ccode(cc)][1]) for cc, abb in M.parse.stateabb.items()
                if C.from_ccode(cc) and cc not in C.ALIASES_CCODE and C.ALL[C.from_ccode(cc)][1] != abb]   # 678 YAR -> yemen is a declared alias
        assert not mism, mism
    finally:
        conn.close(); os.remove(db)
