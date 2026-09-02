"""WALK_FORWARD_PROTOCOL.md Amendment B (G-persistence, Brief B-1): the persistence level for a read at t uses
nothing dated >= t; the 0.9/0.1 smoothing sums to 1; the climatology fallback is counted. DB-free: a synthetic
MID table drives session A's scorer (ies90.score_event, called through engine.persistence, never copied)."""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)
import engine.persistence as PS
import walk as W
from test_read import _synthetic
from test_walk import MENU, FAST


def _src(mid_rows):
    """A source bundle with only a Dyadic-MID table; the other sources are empty but well-formed."""
    mid = pd.DataFrame(mid_rows, columns=["disno", "namea", "nameb", "ea", "eb", "pair", "start", "end", "hihost", "settlmnt", "war"])
    midi = pd.DataFrame(columns=["incidnum", "dispnum", "start", "end", "hostlev", "fatality", "action"])
    icb = pd.DataFrame(columns=["crisno", "crisname", "trigdate", "termdate", "viol", "forout"])
    return {"mid": mid, "midi": midi, "midip": {}, "war": {"inter": [], "intra": []}, "icb": icb, "icb_members": {}, "ged": {}}


def _dispute(start, end, hihost=4):
    return {"disno": 1, "namea": "A", "nameb": "B", "ea": "country.a", "eb": "country.b", "pair": frozenset(("country.a", "country.b")),
            "start": pd.Timestamp(start), "end": pd.Timestamp(end), "hihost": hihost, "settlmnt": 3, "war": 0}


def test_amendment_b_smoothing_sums_to_one_and_spreads_to_neighbours():
    for l in PS.LEVELS:
        p = PS.smooth(l)
        assert abs(sum(p.values()) - 1.0) < 1e-12 and p[l] == 0.9
    assert PS.smooth("0") == {"0": 0.9, "1": 0.1, "2": 0.0, "3": 0.0}                # one neighbour takes the 0.1
    assert PS.smooth("3") == {"0": 0.0, "1": 0.0, "2": 0.1, "3": 0.9}
    assert PS.smooth("2") == {"0": 0.0, "1": 0.05, "2": 0.9, "3": 0.05}


def test_amendment_b_persistence_uses_nothing_dated_on_or_after_as_of():
    t = "2000-06-01"
    A, pairs, L = {"country.a", "country.b"}, {frozenset(("country.a", "country.b"))}, set()
    # a use-of-force dispute wholly inside W- = [t-90, t-1] -> level 2
    r = PS.pre_window_level(t, A, pairs, L, _src([_dispute("2000-04-01", "2000-04-20")]))
    assert r["level_pre"] == "2" and r["window_pre"] == ["2000-03-03", "2000-05-31"]
    # the same dispute dated ON as_of (or later) is invisible to the read at as_of: covered, nothing in W- -> level 0
    for st, en in (("2000-06-01", "2000-06-20"), ("2000-07-01", "2000-07-20")):
        r2 = PS.pre_window_level(t, A, pairs, L, _src([_dispute(st, en)]))
        assert r2["level_pre"] == "0" and "mid" in r2["covering_pre"], r2
    # a dispute that begins inside W- and is still open at t contributes its dated onset only (level 1), not its peak
    r3 = PS.pre_window_level(t, A, pairs, L, _src([_dispute("2000-05-20", "2000-09-01", hihost=5)]))
    assert r3["level_pre"] == "1"
    # adding a future record to a knowable past leaves the forecast unchanged
    r4 = PS.pre_window_level(t, A, pairs, L, _src([_dispute("2000-04-01", "2000-04-20"), _dispute("2000-06-01", "2000-08-01", hihost=5)]))
    assert r4["level_pre"] == "2"
    # no covering source (every source's period ends before 2026) -> no level -> the walk falls back
    r5 = PS.pre_window_level("2026-06-01", A, pairs, L, _src([]))
    assert r5["level_pre"] is None and r5["covering_pre"] == []


def test_amendment_b_walk_seals_persistence_and_counts_the_fallback(tmp_path):
    p = dict(W.REGISTERED) | FAST
    # no persistence levels at all -> every geopolitical read falls back to climatology, and says so
    c = _synthetic(n=60, seed=3)
    assert c.persistence == {}
    w = W.Walk(c, MENU, out_dir=tmp_path / "fb", params=p, quiet=True).run_reads()
    tier = W.summarize_tier(w.reads, w.scores, p, "daily", n_boot=100, n_spa=50)
    n_geo = sum(1 for r in w.reads if r["burn_in_ok"] and r["type"] in W.GEO)
    assert tier["G"]["n_persistence_fallback"] == n_geo and tier["G"]["n_persistence_known"] == 0
    for r in w.reads:
        assert r["baselines"]["persistence"]["fallback"] is True and r["baselines"]["persistence"]["G"] == r["baselines"]["climatology"]["G"]
    pc, pp = tier["G"]["engine_vs"]["climatology"], tier["G"]["engine_vs"]["persistence"]
    assert pc["n"] == pp["n"] and abs(pc["skill"] - pp["skill"]) < 1e-12               # identical forecasts, identical skill
    assert "persistence" in tier["G"]["engine_vs"] and "persistence" in tier["G"]["rps"]["engine_vs"]
    assert tier["G"]["spa_vs_persistence"].get("benchmark") == "persistence"
    # levels known -> the sealed baseline is the smoothed point mass and nothing falls back
    c2 = _synthetic(n=60, seed=3)
    c2.persistence = {e["event_id"]: {"level_pre": "3", "covering_pre": ["mid"], "window_pre": None, "basis_pre": "dyadic"} for e in c2.events}
    w2 = W.Walk(c2, MENU, out_dir=tmp_path / "kn", params=p, quiet=True).run_reads()
    tier2 = W.summarize_tier(w2.reads, w2.scores, p, "daily", n_boot=100, n_spa=50)
    assert tier2["G"]["n_persistence_fallback"] == 0
    for r in w2.reads:
        b = r["baselines"]["persistence"]
        assert b["fallback"] is False and b["G"] == PS.smooth("3") and b["level_pre"] == "3"
    for s_ in w2.scores:
        if s_["outcome"]["level"]:
            assert s_["scores"]["persistence"]["G"]["brier"] is not None
    assert W.verify_file(tmp_path / "kn" / "reads.jsonl")[0]
