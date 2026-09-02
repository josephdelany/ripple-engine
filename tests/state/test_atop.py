"""WS-D01/D02 ATOP 5.1: USA-Japan carries a defense pact in 2000 (the 1960 treaty), USA-Iran no obligation;
directed rows fold to the undirected dyad."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import atop as M


def test_d01_fixture_usa_japan_defense_pact_2000():
    rows = M.parse(FIX / "atop" / "atop5_1ddyr.csv", release="2024-04-04")
    check_rows(rows, M.FIELDS)
    by = {(r["entity_id"], r["field"], r["obs_date"]): r["value"] for r in rows}
    assert by[("dyad.japan__usa", "atop_defense_pact", "2000-01-01")] == 1.0
    assert by[("dyad.japan__usa", "atop_any_obligation", "2000-01-01")] == 1.0
    # ATOP's dyad-year file lists only dyads with an obligation: USA-Iran has no row at all (absent = none,
    # within 1815-2018 -- the join fills 0 for this dataset's coverage; see situation_state.ZERO_IF_ABSENT)
    assert ("dyad.iran__usa", "atop_defense_pact", "2000-01-01") not in by
    assert {r["entity_id"] for r in rows} == {"dyad.japan__usa"}                     # both directions folded to one dyad


def test_d01_live_smoke():
    live_or_skip(P.raw_path("atop", "atop_5.1_csv.zip"))
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 30000
        v = P.value_at(conn, "dyad.japan__usa", "atop_defense_pact", "2001-09-11")
        assert v and v["value"] == 1.0 and v["obs_date"] == "2001-01-01"
        assert P.value_at(conn, "dyad.japan__usa", "atop_defense_pact", "2019-06-01")["obs_date"] == "2018-01-01"   # ATOP ends 2018; last value carries, dated
    finally:
        conn.close(); os.remove(db)
