import copy
import sqlite3

import numpy as np

import structural_surface_experiment as M


def test_weighted_crps_matches_hand_formula():
    x = np.array([0.0, 2.0]); w = np.array([0.25, 0.75]); y = 1.0
    # E|X-y| = 1; .5 E|X-X'| = .5 * (2 * .25 * .75 * 2) = .375
    assert abs(M.weighted_crps(x, w, y) - 0.625) < 1e-12


def test_surface_arm_is_class_only_and_keeps_cross_class_support():
    d = M.surface_distances("sanctions", ["sanctions", "conflict_escalation", "sanctions"])
    assert d.tolist() == [0.0, 1.0, 0.0]
    w = M.kernel_weights(d)
    assert np.all(w > 0)
    assert abs(w.sum() - 1) < 1e-12
    assert w[0] == w[2] and w[0] > w[1]


def test_strict_panel_rows_enforces_release_vintage_and_retrospective():
    c = sqlite3.connect(":memory:")
    c.executescript("""
      CREATE TABLE events(event_id TEXT,event_date TEXT);
      CREATE TABLE situation_state(event_id TEXT,entity_id TEXT,field TEXT,obs_date TEXT,value REAL,
        value_text TEXT,vintage TEXT,release TEXT,retrospective INTEGER,source TEXT,joined_at TEXT);
      INSERT INTO events VALUES('e','2000-01-10');
      INSERT INTO situation_state VALUES('e','world','keep','2000-01-01',1,NULL,'2000-01-02','2000-01-03',0,'x','x');
      INSERT INTO situation_state VALUES('e','world','late_release','2000-01-01',2,NULL,'2000-01-02','2000-02-01',0,'x','x');
      INSERT INTO situation_state VALUES('e','world','retro','2000-01-01',3,NULL,'2000-01-02','2000-01-03',1,'x','x');
      INSERT INTO situation_state VALUES('e','situation','coded','2000-01-01',NULL,'x','2000-01-02','2000-01-03',0,'x','x');
    """)
    rows = M.strict_panel_rows(c)
    assert [r[1] for r in rows] == ["keep"]


def test_panel_reduction_is_registered_and_deterministic():
    rows = [("e", "power", 2.0, None, "country.b"), ("e", "power", 4.0, None, "country.a"),
            ("e", "regime", None, "z", "country.b"), ("e", "regime", None, "a", "country.a")]
    v, meta = M.reduce_panel(rows, {"power": "actors", "regime": "actors"})
    assert v["e"]["panel:power"] == 3.0
    assert v["e"]["panel:regime"] == "a|z"
    assert meta["e"]["panel:power"]["n_entities"] == 2


def test_seal_precedes_outcome_and_detects_tampering():
    r = M.seal({"event_id": "e", "candidate_ids": ["a"], "forecasts": {"20": {"abnormal_atoms": [1.0]}},
                "structural": {"weights": [1.0]}, "surface": {"weights": [1.0]}})
    assert "outcome" not in r
    assert M.verify_seal(r)
    bad = copy.deepcopy(r); bad["forecasts"]["20"]["abnormal_atoms"][0] = 2.0
    assert not M.verify_seal(bad)


def test_outcome_design_does_not_need_the_post_event_value():
    idx = np.arange(400, dtype=float)
    s = __import__("pandas").Series(np.exp(idx / 1000), index=__import__("pandas").date_range("2000-01-01", periods=400))
    event = s.index[300]
    before = M.outcome_design(s, event)
    s.iloc[320] = np.nan
    after = M.outcome_design(s, event)
    assert before == after


def test_structural_distance_never_uses_event_class():
    target = {"market:x": 1.0, "market:y": 2.0, "market:z": 3.0}
    cand = {"market:x": 1.0, "market:y": 2.0, "market:z": 3.0}
    meta = {k: {"block": "market", "kind": "num"} for k in target}
    history = [(f"1999-01-{i+1:02d}", {k: float(i) for k in target}) for i in range(30)]
    r = M.structural_distance(target, cand, history, "2000-01-01", meta, meta)
    assert r["distance"] == 0.0
    assert r["n_fields"] == 3
    assert all("type" not in x and "class" not in x for x in r["fields"])
