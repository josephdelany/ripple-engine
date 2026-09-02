"""Brief A-7: the bridge stamps already-held series into the panel with publish-lag vintages (never null), derives the
two event fields, loads COW Diplomatic Exchange, and writes every unloaded registered field as a stated gap. The
corpus-level tests run against oil.db after `python3 src/state/bridge.py` (skip, never fake, otherwise)."""
import re
import sqlite3

import pandas as pd
import pytest

from _helpers import P
import bridge as B


def _conn():
    if not P.DB.exists():
        pytest.skip("oil.db absent")
    c = sqlite3.connect(P.DB)
    if not c.execute("SELECT 1 FROM state_panel WHERE field='brent_daily' LIMIT 1").fetchone():
        pytest.skip("run python3 src/state/bridge.py first")
    return c


def test_a7_vintage_is_obs_plus_registered_lag_and_never_null():
    c = _conn()
    for f, lag in (("brent_daily", 7), ("vix", 3), ("us_spr_stock", 5), ("cot_managed_money_net", 3)):
        rows = c.execute("SELECT obs_date, vintage, release FROM state_panel WHERE field=? ORDER BY obs_date DESC LIMIT 5", (f,)).fetchall()
        assert rows, f
        for obs, vin, rel in rows:
            assert vin and rel and (pd.Timestamp(vin) - pd.Timestamp(obs)).days == lag, (f, obs, vin)
    obs, vin = c.execute("SELECT obs_date, vintage FROM state_panel WHERE field='wti_monthly' ORDER BY obs_date DESC LIMIT 1").fetchone()
    assert (pd.Timestamp(vin) - (pd.Timestamp(obs) + pd.offsets.MonthBegin(1))).days == 20     # the following month + 20 d
    assert c.execute("SELECT COUNT(*) FROM state_panel WHERE vintage IS NULL OR release IS NULL").fetchone()[0] == 0


def test_a7_derived_fields_and_dipex():
    c = _conn()
    assert c.execute("SELECT COUNT(*) FROM state_panel WHERE field='leader_change_last_365d'").fetchone()[0] == 0   # read-time field, never stored
    n_ev = c.execute("SELECT COUNT(*) FROM events WHERE type='opec_decision'").fetchone()[0]
    n_pf = c.execute("SELECT COUNT(*) FROM state_panel WHERE field='opec_decision_dated'").fetchone()[0]
    assert n_pf == n_ev and n_ev > 0
    lv = {v for (v,) in c.execute("SELECT DISTINCT value FROM state_panel WHERE field='diplomatic_representation'")}
    assert lv <= {0.0, 1.0, 2.0, 3.0} and c.execute("SELECT MIN(obs_date), MAX(obs_date) FROM state_panel WHERE field='diplomatic_representation'").fetchone() == ("1817-01-01", "2005-01-01")
    assert c.execute("SELECT COUNT(*) FROM state_panel WHERE field='diplomatic_representation' AND retrospective=1").fetchone()[0] > 0


def test_a7_every_unloaded_registered_field_is_a_stated_gap():
    c = _conn()
    cb = P.codebook()
    loaded = {f for (f,) in c.execute("SELECT DISTINCT field FROM state_panel")}
    unloaded = set(cb) - loaded
    assert unloaded <= set(B.GAPS) | set(B.READ_TIME), unloaded - set(B.GAPS) - set(B.READ_TIME)   # every missing field has a written reason
    text = B.GAPS_OUT.read_text()
    for f in unloaded:
        assert f"`{f}`" in text
    # the coverage table names a gap or a count for every block x decade 1940s-2020s
    assert "## Coverage" in text and all(f"{d}s" in text for d in range(1940, 2030, 10))
