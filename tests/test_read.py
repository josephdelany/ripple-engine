"""PATH Step 7 -- the read (src/engine/read.py). The four tests named in PATH §1 Step 7 plus the
filtration tests. Synthetic-corpus tests are DB-free; the abqaiq test needs the built oil.db."""
import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import engine.similarity as S
import engine.read as R

ROOT = os.path.join(os.path.dirname(__file__), "..")
DB = os.path.join(ROOT, "data", "oil.db")


# ----------------------------------------------------------------------------- synthetic corpus

def _synthetic(n=30, seed=3):
    """30 conflict_escalation events 2001-2015, a synthetic Brent series, two market fields, edges, and IES-90
    labels that FOLLOW THE ACTOR by construction (country.c -> level 0; country.a -> 3 or 1): a P-null (Brent is
    a seeded random walk) but not a G-null. The DEAL flag is null for every fifth event, 1 only at level 1."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("1999-01-01", "2017-12-31")
    brent = pd.Series(50 * np.exp(np.cumsum(rng.normal(0, 0.01, len(idx)))), index=idx)
    vix = pd.Series(rng.normal(50, 10, len(idx)), index=idx)
    events, edges, ies90, panel = [], {}, {}, {}
    dates = pd.date_range("2001-01-15", "2015-12-15", periods=n)
    for i, d in enumerate(dates):
        eid = f"ev{i:02d}"
        events.append({"event_id": eid, "event_date": str(d.date()), "type": "conflict_escalation", "title": eid,
                       "sr_actor": "country.a" if i % 2 else "country.c", "sr_target": "country.b",
                       "sr_conflict_scope": "isolated", "sr_tempo": "nth", "sr_prior_dyad": "none",
                       "sr_asset_role": "unknown", "sr_actor_propensity": None})
        level = "0" if i % 2 == 0 else ("3" if i % 4 == 1 else "1")
        ies90[eid] = {"level": level, "deal": (None if i % 5 == 0 else (1 if level == "1" else 0))}
        # Amendment H: the situation fields are taken from knowable_at rows (vintage <= as_of); here every coded field is
        # knowable on the event date, so the synthetic corpus keeps its situation block (labels follow the actor)
        d_ = str(d.date())
        panel[eid] = [{"field": "sr_actor", "value": events[-1]["sr_actor"], "vintage": d_}, {"field": "sr_target", "value": "country.b", "vintage": d_},
                      {"field": "sr_conflict_scope", "value": "isolated", "vintage": d_}, {"field": "sr_tempo", "value": "nth", "vintage": d_}]
        edges[(eid, "fred.DCOILBRENTEU")] = float(rng.normal(0, 8))
        edges[(eid, "yf.sp500")] = float(rng.normal(0, 3))
    info = S.InfoSet({"vix_pct": vix})
    big = {"daily": {"windows": [("2008-09-01", "2008-12-31"), ("2014-10-01", "2015-01-31")], "base_pct": 18.3}}
    return R.Corpus(events, info, {"daily": brent}, edges=edges, big_moves=big, ies90=ies90, panel=panel)


def test_step7_branch_counts_sum_to_n_synthetic():
    c = _synthetic()
    tgt = c.by_id["ev25"]
    r = R.read(c, tgt, weighting={"id": "u", "retrieve_min": 0.4, "k": 8})
    assert r["no_adequate_precedent"] is False
    assert sum(r["G"]["counts"].values()) == r["G"]["n"] == len([a for a in r["analogs"] if a["g_closed"]])
    assert abs(sum(r["G"]["rates"].values()) - 1.0) < 1e-9
    assert abs(sum(r["G"]["probs_for_log_score"].values()) - 1.0) < 1e-3
    assert r["P"]["n"] == len(r["P"]["values"]) and r["F"]["n"] == r["P"]["n"]


def test_step7_every_hop_carries_n_synthetic():
    c = _synthetic()
    r = R.read(c, c.by_id["ev25"], weighting={"id": "u", "retrieve_min": 0.4, "k": 8})
    prop = r["propagation"]
    assert prop["ALL"]["contributing_n"] >= 1
    for key, blk in prop.items():
        if key == "caveat":
            continue
        assert blk["hops"], key
        for h in blk["hops"]:
            assert isinstance(h["n"], int) and h["n"] >= 1
            assert h["n"] <= blk["contributing_n"]


def test_step7_no_adequate_precedent_returns_no_numbers():
    c = _synthetic()
    far = {"event_id": "live", "event_date": "2016-06-01", "type": "conflict_escalation", "title": "live",
           "sr_actor": "country.zz", "sr_target": "country.yy", "sr_conflict_scope": "war", "sr_tempo": "first",
           "sr_prior_dyad": "WIDENING", "sr_asset_role": "chokepoint", "sr_actor_propensity": None}
    r = R.read(c, far, weighting={"id": "u", "retrieve_min": 0.95, "k": 8})
    assert r["no_adequate_precedent"] is True
    assert r["G"] is None and r["P"] is None and r["F"] is None and r["M"] is None
    assert r["propagation"] is None and r["differencing"] is None and r["analogs"] == []
    # nothing numeric about the outcome leaks into the envelope: only retrieval diagnostics remain
    assert set(r) <= {"event_id", "date", "as_of", "type", "tier", "weighting", "k", "threshold", "filtration", "state",
                      "max_similarity", "conditioned_n", "no_adequate_precedent", "analogs", "G", "P", "F", "M",
                      "propagation", "differencing", "note"}


def test_step7_filtration_excludes_unclosed_windows_and_break_leaks():
    c = _synthetic()
    tgt = c.by_id["ev20"]
    t = tgt["event_date"]
    r = R.read(c, tgt, weighting={"id": "u", "retrieve_min": 0.0, "k": 30})
    for a in r["analogs"]:
        assert a["date"] < t                                                     # knowable
        assert pd.Timestamp(a["date"]) + pd.Timedelta(days=90) <= pd.Timestamp(t)  # branch label had closed
        o = c.outcome(a["event_id"])
        assert o is not None and o["closed_on"] <= t                              # price window had closed
    # ev19 is ~185 days before ev20 -> closed; read ev20 as of one day after ev19: ev19 must vanish
    r2 = R.read(c, tgt, as_of=str((pd.Timestamp(c.by_id["ev19"]["event_date"]) + pd.Timedelta(days=1)).date()),
                weighting={"id": "u", "retrieve_min": 0.0, "k": 30})
    assert "ev19" not in {a["event_id"] for a in r2["analogs"]}
    assert "ev19" in {a["event_id"] for a in r["analogs"]}
    # the deliberate leak admits future events (used only by the walk's leakage test)
    rb = R.read(c, tgt, weighting={"id": "u", "retrieve_min": 0.0, "k": 30}, break_filtration=True)
    assert rb["filtration"]["broken"] is True
    assert any(a["date"] > t for a in rb["analogs"])


def test_step7_materiality_call_uses_registered_ratio():
    c = _synthetic()
    r = R.read(c, c.by_id["ev29"], weighting={"id": "u", "retrieve_min": 0.0, "k": 30})
    m = r["M"]
    assert m["n"] >= 1 and m["base_pct"] == 18.3
    expected = "MATERIAL" if m["rate_pct"] / m["base_pct"] >= R.MATERIAL_RATIO else "NOT_MATERIAL"
    assert m["call"] == expected


@pytest.mark.skipif(not os.path.exists(DB), reason="needs the built oil.db")
def test_step7_abqaiq_read_uses_only_analogs_dated_before_it():
    from _db import connect
    conn = connect(read_only=True)
    c = R.Corpus.from_db(conn)
    r = R.read(c, c.by_id["abqaiq_attack_2019"], weighting=S.load_menu()["items"][0])
    assert r["date"] == "2019-09-14" and r["no_adequate_precedent"] is False
    assert r["analogs"], "abqaiq must have precedents"
    for a in r["analogs"]:
        assert a["date"] < "2019-09-14"
        if a["g_closed"]:
            assert pd.Timestamp(a["date"]) + pd.Timedelta(days=90) <= pd.Timestamp("2019-09-14")
        if a["p_closed"]:
            assert c.outcome(a["event_id"])["closed_on"] <= "2019-09-14"
    for pid in r["P"]["analog_ids"]:
        assert c.by_id[pid]["event_date"] < "2019-09-14"
    assert sum(r["G"]["counts"].values()) == r["G"]["n"]
    for key, blk in r["propagation"].items():
        if key != "caveat":
            for h in blk["hops"]:
                assert h["n"] >= 1
    # the event's own outcome is never among its evidence
    assert "abqaiq_attack_2019" not in {a["event_id"] for a in r["analogs"]}
