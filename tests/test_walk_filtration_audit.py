"""WALK_FORWARD_PROTOCOL.md Amendments F.1 (the filtration audit), G (release lags) and H (knowable-at situation
fields), Brief 2 B-8. Session D's two deliberate leaks (docs/red_team_2/D2_leakage_hunt.md) are re-applied by
monkeypatching the SEALED path and must be caught by the audit -- which the old broken-vs-sealed comparison missed.
DB-free."""
import os
import sys

import numpy as np
import pandas as pd
import pytest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)
import engine.read as R
import engine.similarity as S
import walk as W
from test_read import _synthetic
from test_walk import MENU, FAST


def _run(c, out, **kw):
    return W.Walk(c, MENU, out_dir=out, params=FAST, quiet=True, **kw).run_reads()


def test_f1_clean_run_passes_the_audit(tmp_path):
    c = _synthetic(n=100, seed=3)
    w = _run(c, tmp_path / "s")
    a = W.filtration_audit(c, w.reads)
    assert a["clean"] and a["n_violations"] == 0
    assert a["checks"]["analog_date"] > 0 and a["checks"]["g_window"] > 0 and a["checks"]["p_window"] > 0 and a["checks"]["market_value"] > 0
    b = _run(c, tmp_path / "b", break_filtration=True)
    lk = W.leakage_test(w, b, None, a)
    assert lk["asserted"] and lk["filtration_audit_clean"]
    assert W.filtration_audit(c, b.reads)["n_violations"] > 0                   # the broken run fails its own audit, as it should


def test_f1_d2_leak_1_unclosed_window_is_caught(tmp_path, monkeypatch):
    # D2 "Leak 1": drop the branch-window-closed check from the analog pool -> an analog whose +90d window is still
    # open at as_of enters with g_closed = True. Reads ~55 days apart make this bite on nearly every read.
    monkeypatch.setattr(R.Corpus, "g_closed_by", lambda self, event_id, as_of: True)
    c = _synthetic(n=100, seed=3)
    w = _run(c, tmp_path / "s")
    a = W.filtration_audit(c, w.reads)
    assert not a["clean"] and a["violations"].get("g_window", 0) > 0, a
    assert a["first_violation"]["kind"] == "g_window"
    b = _run(c, tmp_path / "b", break_filtration=True)
    lk = W.leakage_test(w, b, None, a)
    assert lk["asserted"] is False and "VOID" in lk["verdict"]                    # the old comparison alone would have passed


def test_f1_d2_leak_2_same_day_market_value_is_caught(tmp_path, monkeypatch):
    # D2 "Leak 2": side="right" -- an observation dated exactly as_of becomes visible to the read at as_of
    def leaky(self, field, t):
        if field not in self._s:
            return None
        idx, v, _, _ = self._s[field]
        i = np.searchsorted(idx, np.datetime64(pd.Timestamp(t)), side="right") - 1
        return float(v[i]) if i >= 0 else None
    monkeypatch.setattr(S.InfoSet, "value_before", leaky)
    c = _synthetic(n=100, seed=3)
    w = _run(c, tmp_path / "s")
    a = W.filtration_audit(c, w.reads)
    assert not a["clean"] and a["violations"].get("market_value", 0) > 0, a


def test_g_release_lags_apply_to_value_and_standardization():
    idx = pd.bdate_range("2010-01-01", "2010-12-31")
    vals = pd.Series(np.arange(len(idx), dtype=float), index=idx)
    info = S.InfoSet({"cot_pct": vals, "vix_pct": vals})
    t = "2010-06-16"                                                   # a Wednesday
    v_cot = info.value_before("cot_pct", t); v_vix = info.value_before("vix_pct", t)
    last_cot = vals[vals.index < pd.Timestamp(t) - pd.Timedelta(days=S.RELEASE_LAGS["cot_pct"])].iloc[-1]
    last_vix = vals[vals.index < pd.Timestamp(t)].iloc[-1]
    assert v_cot == last_cot and v_vix == last_vix and v_cot < v_vix                  # 3 calendar days of COT withheld; VIX unlagged
    iv, d = info.independent_value_before("cot_pct", t)
    assert iv == v_cot and pd.Timestamp(d) + pd.Timedelta(days=3) < pd.Timestamp(t)   # the independent path agrees
    assert info.stats("cot_pct", t)[2] == int((vals.index < pd.Timestamp(t) - pd.Timedelta(days=3)).sum())   # n in the scale window


def test_h_situation_fields_follow_knowable_at():
    c = _synthetic(n=30, seed=3)
    v = c.vector("ev05")
    assert v["fields"]["actor"] is not None and "actor" in v["situation_known_at_t"]      # knowable on the event date (synthetic rows)
    d = c.by_id["ev05"]["event_date"]
    c2 = _synthetic(n=30, seed=3)
    c2.panel["ev05"] = [{"field": "sr_actor", "value": "country.zz", "vintage": str((pd.Timestamp(d) + pd.Timedelta(days=400)).date())}]
    v2 = c2.vector("ev05")
    assert v2["fields"]["actor"] is None and "actor" in v2["situation_blanked"] and "actor" in v2["unknown"]   # coded, not knowable at t
    c3 = _synthetic(n=30, seed=3)
    c3.panel["ev05"] = [{"field": "sr_actor", "value": "country.zz", "vintage": d}]
    assert c3.vector("ev05")["fields"]["actor"] == "country.zz"                          # the knowable row wins over the coded column
    assert c3.vector("ev05")["fields"]["prior_dyad"] == c.by_id["ev05"]["sr_prior_dyad"]  # H.1: corpus-derived field stays as coded
