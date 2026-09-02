"""WS-M05 EIA NYMEX curve: RCLC1 first print 1983-04-04 = 29.44 (the file; PATH cites 1983-03-30 -- the file is
the record), the series end 2024-04-05, and the M1-M4 spread on a known day."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import eia_nymex as M


def test_m05_fixture_first_print_and_spread():
    c1 = M.read_contract(FIX / "eia_nymex" / "RCLC1d.csv")
    assert str(c1.index[0].date()) == "1983-04-04" and c1.iloc[0] == 29.44
    rows = M.parse({"RCLC1": FIX / "eia_nymex" / "RCLC1d.csv", "RCLC4": FIX / "eia_nymex" / "RCLC4d.csv"}, release="2026-08-26")
    check_rows(rows, M.FIELDS)
    assert rows[-1]["obs_date"] == "2024-04-05"                               # EIA: no futures prices after 2024-04-05
    for r in rows:
        assert r["vintage"] == r["obs_date"]                                  # a daily print is knowable on its date
    c4 = M.read_contract(FIX / "eia_nymex" / "RCLC4d.csv")
    d = "2001-09-10"
    got = [r for r in rows if r["obs_date"] == d][0]["value"]
    assert abs(got - (float(c1[d]) - float(c4[d]))) < 1e-9


def test_m05_live_smoke():
    live_or_skip(*[P.raw_path("eia_nymex", f"{s}d.xls") for s in M.CONTRACTS])
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 9000
        v = P.value_at(conn, "world", "curve_m1_m4_spread", "2001-09-10")
        assert v and v["obs_date"] == "2001-09-10" and v["release"]
        assert P.value_at(conn, "world", "curve_m1_m4_spread", "2026-01-01")["obs_date"] == "2024-04-05"   # the series stopped; the last print carries, labelled by its date
    finally:
        conn.close(); os.remove(db)
