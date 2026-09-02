"""WS-D06..D09 ICB v16: 512 crises (PATH's named value); Basra-Kharg Island (crisno 348) coded viol 4, forout 2,
outesr 1 in the system file; a dyad's crisis fields are knowable the day after termination, not before."""
import os
from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import icb as M


def test_d06_fixture_kharg_codes_and_knowability():
    sysd = M.crises(FIX / "icb" / "icb1v16.csv")
    k = sysd[sysd.crisno == 348].iloc[0]
    assert k.crisname == "BASRA-KHARG ISLAND" and k.viol == 4 and k.forout == 2 and k.outesr == 1
    assert str(k.termdate.date()) == "1984-07-11"
    rows = M.parse({"system": FIX / "icb" / "icb1v16.csv", "dyads": FIX / "icb" / "icb_dyads_v16.csv"}, release="2025-01-01")
    check_rows(rows, M.FIELDS)
    ii = [r for r in rows if r["entity_id"] == "dyad.iran__iraq" and r["field"] == "icb_last_violence"]
    assert ii and ii[0]["obs_date"] == "1984-07-12" == ii[0]["vintage"] and ii[0]["value"] == 4.0


def test_d06_live_smoke_512_crises():
    live_or_skip(P.raw_path("icb", "icb1v16.csv"))
    assert len(M.crises()) == 512
    conn, db = scratch_conn()
    try:
        assert M.load(conn) > 1000
        assert P.value_at(conn, "dyad.iran__iraq", "icb_last_violence", "1984-07-11") is None or \
            P.value_at(conn, "dyad.iran__iraq", "icb_last_violence", "1984-07-11")["obs_date"] < "1984-07-12"   # not yet knowable during the crisis
        after = P.value_at(conn, "dyad.iran__iraq", "icb_last_violence", "1985-01-01")
        assert after and after["value"] == 4.0
    finally:
        conn.close(); os.remove(db)
