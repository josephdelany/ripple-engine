"""WORLD_STATE_FRAMEWORK.md Amendment A: every situation field carries knowable_at by the registered rule; the join drops
fields with knowable_at > t and counts them. The corpus-level test copies ONE real event (no synthetic rows) into a
scratch DB and joins it there; the real situation_state is only read."""
import shutil
import sqlite3

import pytest

from _helpers import P
import situation_state as SS


def test_a8_knowable_at_rules_are_total_and_never_guess():
    assert SS.knowable_at("https://www.aljazeera.com/news/2019/09/14/x", "2019-09-14", "2026-09-02T00:00:00") == ("2019-09-14", "a:url_date")
    assert SS.knowable_at("https://x.org/report-2001-10-08.pdf", "2001-09-11", "2026-09-02") == ("2001-10-08", "a:url_date")
    assert SS.knowable_at("https://www.nber.org/papers/w16790", "1979-01-16", "2026-09-02T02:23:34+00:00") == ("2026-09-02", "c:coding_date(undated url)")
    assert SS.knowable_at("corpus:dyad", "1990-08-02", "2026-09-02") == ("2026-09-02", "c:coding_date(corpus-derived)")
    assert SS.knowable_at("corpus:observed()", "1990-08-02", "2026-09-02") == ("1990-10-31", "b:window_close")
    assert SS.knowable_at(None, "1990-08-02", "2026-09-02") == ("unknown", "d:null")
    assert SS.knowable_at("corpus:density", "1990-08-02", None) == ("unknown", "c:coding_date(corpus-derived)")


def test_a8_join_drops_fields_knowable_after_t_and_counts_them(tmp_path):
    if not P.DB.exists():
        pytest.skip("oil.db absent")
    real = sqlite3.connect(P.DB)
    eid = real.execute("SELECT event_id FROM events WHERE sr_json IS NOT NULL AND type='conflict_escalation' ORDER BY event_date LIMIT 1").fetchone()[0]
    fields = SS.situation_fields(real, eid)
    assert fields and all(f["knowable_at"] and f["rule"] for f in fields)
    kept, dropped, unknown = SS.situation_rows_at(real, eid, real.execute("SELECT event_date FROM events WHERE event_id=?", (eid,)).fetchone()[0])
    assert len(kept) + dropped + unknown == len(fields)
    assert all(f["knowable_at"] <= f["obs_date"] for f in kept)                           # nothing after t survives
    # far in the future everything dated is knowable
    kept2, dropped2, unknown2 = SS.situation_rows_at(real, eid, "2099-01-01")
    assert dropped2 == 0 and len(kept2) == len(fields) - unknown2
    # the join on a scratch DB holding only this real event writes only the kept rows under entity 'situation'
    db = tmp_path / "scratch.db"
    shutil.copy(P.DB, db)
    c = sqlite3.connect(db)
    c.execute("DELETE FROM events WHERE event_id != ?", (eid,)); c.execute("DELETE FROM situation_state"); c.commit()
    SS.join(c, [eid])
    n = c.execute("SELECT COUNT(*) FROM situation_state WHERE event_id=? AND entity_id='situation'", (eid,)).fetchone()[0]
    assert n == len(kept)
    assert c.execute("SELECT COUNT(*) FROM situation_state WHERE entity_id='situation' AND vintage > obs_date").fetchone()[0] == 0
    assert SS.KNOWABLE and SS.KNOWABLE[0]["dropped_after_t"] == dropped and SS.KNOWABLE[0]["unknown"] == unknown
    real.close(); c.close()
