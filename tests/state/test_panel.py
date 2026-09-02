"""The panel itself (PATH Step 2/3): the schema, the writer's refusals, and the vintage rule --
a value with vintage > t is invisible at t (WORLD_STATE_FRAMEWORK §4.3, Amendment 1)."""
import os

import pytest

from _helpers import P, scratch_conn


def _row(**kw):
    base = {"entity_id": "country.usa", "field": "cinc", "obs_date": "2000-01-01", "value": 0.14, "unit": "share",
            "source": "test", "vintage": "2001-01-01", "release": "2026-06-03"}
    return {**base, **kw}


def test_vintage_rule_later_vintage_is_invisible():
    conn, db = scratch_conn()
    try:
        P.write(conn, [_row(), _row(value=0.15, vintage="2003-01-01")])         # a revision, knowable only from 2003
        assert P.value_at(conn, "country.usa", "cinc", "2000-06-01") is None      # before the first vintage
        assert P.value_at(conn, "country.usa", "cinc", "2001-06-01")["value"] == 0.14
        assert P.value_at(conn, "country.usa", "cinc", "2003-06-01")["value"] == 0.15
        assert P.state_at(conn, "2000-06-01") == {}
    finally:
        conn.close(); os.remove(db)


def test_writer_refuses_null_vintage_release_and_unregistered_field():
    conn, db = scratch_conn()
    try:
        with pytest.raises(ValueError):
            P.write(conn, [_row(vintage=None)])
        with pytest.raises(ValueError):
            P.write(conn, [_row(release=None)])
        with pytest.raises(ValueError):
            P.write(conn, [_row(field="not_in_codebook")])
        assert P.write(conn, [_row(value=None, value_text=None)]) == 0            # missing = absent row (WS-R3)
        assert P.write(conn, [_row(value=float("nan"))]) == 0
    finally:
        conn.close(); os.remove(db)


def test_coverage_reports_blocks_by_decade():
    conn, db = scratch_conn()
    try:
        P.write(conn, [_row(), _row(obs_date="1985-01-01", vintage="1986-01-01")])
        c = P.coverage(conn)
        assert c["n_rows"] == 2 and c["blocks"]["ACTORS"]["1980s"] == 1 and c["blocks"]["ACTORS"]["2000s"] == 1
        assert c["fields"]["cinc"]["entities"] == 1
    finally:
        conn.close(); os.remove(db)
