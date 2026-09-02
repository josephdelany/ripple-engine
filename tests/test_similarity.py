"""PATH Step 6 -- similarity on the state (src/engine/similarity.py). Every test named in PATH §1 Step 6
is here, plus the seam tests for the state panel (Steps 2-3). DB-free: synthetic vectors and series only."""
import json
import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import engine.similarity as S


def _info(extra_after_t=None, n=200, seed=1):
    """Two continuous market fields with daily history 2010-01-01.. ; optionally a future outlier."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2010-01-01", periods=n)
    vix = pd.Series(rng.normal(50, 10, n), index=idx)
    gpr = pd.Series(rng.normal(100, 30, n), index=idx)
    if extra_after_t is not None:
        d, v = extra_after_t
        vix = pd.concat([vix, pd.Series([v], index=[pd.Timestamp(d)])])
        gpr = pd.concat([gpr, pd.Series([v], index=[pd.Timestamp(d)])])
    return S.InfoSet({"vix_pct": vix, "gpr": gpr})


def _vec(eid, date, **fields):
    base = {"actor": "country.a", "target": "country.b", "conflict_scope": "isolated", "tempo": "first",
            "prior_dyad": "none", "asset_role": None, "propensity": None, "vix_pct": 50.0, "gpr": 100.0}
    base.update(fields)
    return {"event_id": eid, "date": date, "type": "conflict_escalation", "title": eid,
            "outcome": "CONTAINED", "fields": base}


T = "2011-01-03"     # ~260 business days after the start: enough prior observations for a scale


def test_step6_identical_states_distance_zero():
    info = _info()
    a, b = _vec("a", "2010-06-01"), _vec("b", "2010-07-01")
    d, detail = S.distance(a, b, info, t=T)
    assert d == 0.0 and detail["comparable"]
    s, _ = S.similarity(a, b, info, t=T)
    assert s == 1.0


def test_step6_unknown_field_on_either_side_does_not_change_distance():
    info = _info()
    a = _vec("a", "2010-06-01", actor="country.x")            # actor mismatch -> some distance
    b = _vec("b", "2010-07-01")
    d0, det0 = S.distance(a, b, info, t=T)
    assert d0 > 0
    # blank the same field on either side -> the field is excluded and counted, distance unchanged
    a_unk = _vec("a", "2010-06-01", actor="country.x", target="unknown")
    b_unk = _vec("b", "2010-07-01", target=None)
    d1, det1 = S.distance(a_unk, b, info, t=T)
    d2, det2 = S.distance(a, b_unk, info, t=T)
    # the remaining fields are a different set, so recompute the expected value by hand:
    # situation block has actor(1) + scope(0) + tempo(0) + prior_dyad(0) = 4 fields known (target dropped)
    assert det1["n_unknown"] == det0["n_unknown"] + 1 and det2["n_unknown"] == det0["n_unknown"] + 1
    assert d1 == d2                                            # symmetric: which side is unknown is irrelevant
    assert det1["blocks"]["situation"]["n_fields"] == det0["blocks"]["situation"]["n_fields"] - 1
    assert "target" not in det1["blocks"]["situation"]["fields"]
    # an unknown field NEVER contributes: a vector that only differs in an unknown field is at distance 0
    c = _vec("c", "2010-07-01", target="unknown")
    assert S.distance(b, c, info, t=T)[0] == 0.0


def test_step6_standardization_uses_only_data_before_t_future_outlier():
    clean = _info()
    spiked = _info(extra_after_t=("2012-01-01", 1e6))          # an outlier that arrives after t
    a = _vec("a", "2010-06-01", vix_pct=40.0, gpr=80.0)
    b = _vec("b", "2010-07-01", vix_pct=60.0, gpr=140.0)
    assert clean.stats("vix_pct", T) == spiked.stats("vix_pct", T)
    assert S.distance(a, b, clean, t=T) == S.distance(a, b, spiked, t=T)
    # ...but the same outlier BEFORE t does change the scale (so the test is not vacuous)
    early = _info(extra_after_t=("2010-03-01", 1e6))
    assert early.stats("vix_pct", T) != clean.stats("vix_pct", T)
    assert S.distance(a, b, early, t=T)[0] != S.distance(a, b, clean, t=T)[0]
    # and a value observed on/after t is invisible to value_before
    assert spiked.value_before("vix_pct", "2012-01-01") != 1e6
    assert spiked.value_before("vix_pct", "2012-01-02") == 1e6


def test_step6_threshold_fires_below_retrieve_min():
    info = _info()
    tgt = _vec("t", T, actor="country.q", target="country.r", conflict_scope="war", tempo="nth",
               prior_dyad="WIDENING", vix_pct=95.0, gpr=250.0)
    pool = [_vec(f"p{i}", "2010-06-01") for i in range(10)]
    r = S.retrieve(tgt, pool, info, t=T, weighting={"retrieve_min": 0.40, "k": 5})
    assert r["no_adequate_precedent"] is True and r["analogs"] == []
    assert r["max_similarity"] < 0.40
    # lower the registered threshold below the max similarity -> precedent found
    r2 = S.retrieve(tgt, pool, info, t=T, weighting={"retrieve_min": 0.0, "k": 5})
    assert r2["no_adequate_precedent"] is False and len(r2["analogs"]) == 5
    # a target with nothing comparable to anyone -> no precedent (never a number from zero evidence)
    blank = {"event_id": "z", "date": T, "type": "x", "fields": {f: None for f in tgt["fields"]}}
    assert S.retrieve(blank, pool, info, t=T)["no_adequate_precedent"] is True


def test_step6_per_block_contributions_and_weights():
    info = _info()
    a = _vec("a", "2010-06-01", actor="country.x")                # situation mismatch only
    b = _vec("b", "2010-07-01")
    d, det = S.distance(a, b, info, t=T)
    shares = [c["share_of_distance"] for c in det["blocks"].values()]
    assert abs(sum(shares) - 1.0) < 1e-6
    assert det["blocks"]["situation"]["share_of_distance"] == 1.0 and det["blocks"]["market"]["distance"] == 0.0
    # block weights: zeroing the situation block removes the only mismatch -> distance 0
    d0, _ = S.distance(a, b, info, t=T, block_weights={"situation": 0.0, "market": 1.0})
    assert d0 == 0.0
    # doubling it (relative to market) doubles its pull: exact formula check
    d2, _ = S.distance(a, b, info, t=T, block_weights={"situation": 2.0, "market": 1.0})
    sit = det["blocks"]["situation"]["distance"]
    assert abs(d2 - (2 * sit) / 3) < 1e-9 and abs(d - sit / 2) < 1e-9


def test_step6_panel_seam_vintage_rule_and_codebook(tmp_path):
    # rows shaped like situation_state(event_id, field, value, vintage, source); vintage > t invisible
    rows = [{"field": "cinc_actor", "value": 0.12, "vintage": "2010-01-01", "source": "COW NMC"},
            {"field": "cinc_actor_future", "value": 0.99, "vintage": "2011-06-01", "source": "COW NMC"},
            {"field": "regime_actor", "value": "autocracy", "vintage": "2010-01-01", "source": "Polity5"}]
    f = S.apply_panel({}, rows, as_of=T)
    assert f == {"cinc_actor": 0.12, "regime_actor": "autocracy"}
    # the codebook seam: block + kind parsed from the markdown table session A commits in Step 1
    cb = tmp_path / "WORLD_STATE_CODEBOOK.md"
    cb.write_text("# codebook\n\n| block | field | unit | resolution | source | coverage | licence | rule |\n"
                  "|---|---|---|---|---|---|---|---|\n"
                  "| actors | cinc_actor | share | a | COW NMC v7 | 1816-2022 | CC | R1 |\n"
                  "| actors | regime_actor | category | a | Polity5 | 1800- | local | R2 |\n")
    schema = S.codebook_schema(cb)
    assert schema == {"cinc_actor": ("actors", "num"), "regime_actor": ("actors", "cat")}
    assert S.codebook_schema(tmp_path / "missing.md") == {}
    # a panel field participates in the distance under its codebook block, standardized point-in-time
    info = S.InfoSet({"cinc_actor": pd.Series(np.linspace(0.05, 0.25, 60),
                                               index=pd.bdate_range("2009-01-01", periods=60))})
    a = {"event_id": "a", "date": "2010-06-01", "type": "x", "fields": {"cinc_actor": 0.10, "regime_actor": "autocracy"}}
    b = {"event_id": "b", "date": "2010-07-01", "type": "x", "fields": {"cinc_actor": 0.10, "regime_actor": "democracy"}}
    d, det = S.distance(a, b, info, t=T, schema_extra=schema)
    assert list(det["blocks"]) == ["actors"] and det["blocks"]["actors"]["n_fields"] == 2
    assert d == 0.5                                            # one match, one mismatch, equal field weights


def test_step6_menu_registered_and_capped():
    m = S.load_menu()
    ids = [i["id"] for i in m["items"]]
    assert 1 <= len(ids) <= 12 and len(set(ids)) == len(ids)
    for it in m["items"]:
        assert set(it["block_weights"]) >= set(S.BLOCKS)
        assert 0 <= it["retrieve_min"] <= 1 and it["k"] >= 1
    assert m["items"][0]["id"].startswith("M01")               # item 0 is the uniform prior (frozen engine)


def test_step6_too_few_comparable_fields_is_not_a_precedent():
    info = _info()
    tgt = _vec("t", T)
    # a candidate that shares only two known fields with the target (both matching) is excluded
    thin = {"event_id": "thin", "date": "2010-06-01", "type": "conflict_escalation", "title": "thin",
            "outcome": "CONTAINED", "fields": {"actor": "country.a", "target": "country.b"}}
    r = S.retrieve(tgt, [thin], info, t=T, weighting={"retrieve_min": 0.40, "k": 5})
    assert r["n_pool"] == 0 and r["no_adequate_precedent"] is True
    thin["fields"]["tempo"] = "first"                          # three comparable fields -> admissible
    r = S.retrieve(tgt, [thin], info, t=T, weighting={"retrieve_min": 0.40, "k": 5})
    assert r["n_pool"] == 1 and r["analogs"][0]["similarity"] == 1.0
