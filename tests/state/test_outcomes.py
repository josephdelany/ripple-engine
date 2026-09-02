"""PATH Step 4 tests: the mapping is deterministic and total; kappa on synthetic data matches a hand value; every
geopolitical event has >= 1 independent source or is flagged no_independent_outcome; the audit sheet is
stratified and seeded. The corpus-level tests run against oil.db after `python3 src/state/outcomes.py`."""
import csv
import itertools
import json
import sqlite3

import pytest

from _helpers import P
import outcomes as O


def test_o1_mapping_is_total_and_deterministic():
    for viol, forout, outesr in itertools.product([1, 2, 3, 4], [None, 1, 2, 3, 4, 7], [None, 1, 2]):
        b = O.map_icb(viol, forout, outesr)
        assert b in O.BRANCHES and b == O.map_icb(viol, forout, outesr)
    assert O.map_icb(None) is None
    assert O.map_icb(2, 1, None) == "RESOLUTION_BY_DEAL" and O.map_icb(4, 1, None) == "WIDENING"
    assert O.map_icb(3, None, 1) == "WIDENING" and O.map_icb(3, None, 2) == "LIMITED_RETALIATION"
    for h, f, s in itertools.product([1, 2, 3, 4, 5], [None, 0, 1, 3, 6], [None, 1, 2, 3]):
        assert O.map_mid(h, f, s) in O.BRANCHES
    assert O.map_mid(5) == "WIDENING" and O.map_mid(4, 3) == "WIDENING" and O.map_mid(4, 1) == "LIMITED_RETALIATION"
    assert O.map_mid(3, None, 1) == "RESOLUTION_BY_DEAL" and O.map_mid(2, None, 2) == "CONTAINED"
    for i0, i1 in itertools.product([0, 1, 2], [0, 1, 2]):
        assert O.map_ucdp(i0, i1) in O.BRANCHES
    assert O.map_ucdp(0, 2) == "WIDENING" and O.map_ucdp(2, 2) == "LIMITED_RETALIATION" and O.map_ucdp(0, 0) == "CONTAINED"
    # the Basra-Kharg codes in the ICB file (viol 4) map to WIDENING; the Gulf War (viol 4, forout 5) too
    assert O.map_icb(4, 2, 1) == "WIDENING"


def test_o2_kappa_matches_hand_value():
    # 10 items, two raters: pairs (C,C)x4 (C,W)x1 (W,W)x2 (W,C)x1 (L,L)x2 -> po = 8/10 = 0.8;
    # marginals both C .5 / W .3 / L .2 -> pe = .25 + .09 + .04 = 0.38; kappa = (0.8 - 0.38) / 0.62 = 0.6774 (arithmetic executed, not recalled)
    a = ["CONTAINED"] * 5 + ["WIDENING"] * 3 + ["LIMITED_RETALIATION"] * 2
    b = ["CONTAINED"] * 4 + ["WIDENING"] + ["WIDENING"] * 2 + ["CONTAINED"] + ["LIMITED_RETALIATION"] * 2
    k, n, conf = O.cohen_kappa(a, b)
    assert n == 10 and conf["CONTAINED"]["CONTAINED"] == 4 and conf["CONTAINED"]["WIDENING"] == 1 and conf["WIDENING"]["CONTAINED"] == 1
    po, pe = 8 / 10, 0.5 * 0.5 + 0.3 * 0.3 + 0.2 * 0.2
    assert k == round((po - pe) / (1 - pe), 4) == 0.6774
    assert O.cohen_kappa(["CONTAINED"] * 3, ["CONTAINED"] * 3)[0] is None           # pe = 1: undefined, not 1.0
    assert O.cohen_kappa([], [])[1] == 0


def _ready():
    if not O.KAPPA_OUT.exists():
        pytest.skip("run `python3 src/state/outcomes.py` first")
    conn = sqlite3.connect(f"file:{P.DB}?mode=ro", uri=True)
    if not conn.execute("SELECT name FROM sqlite_master WHERE name='event_outcomes'").fetchone():
        conn.close(); pytest.skip("event_outcomes table absent")
    return conn


def test_o3_every_geopolitical_event_has_a_source_or_the_flag():
    conn = _ready()
    try:
        geo = {r[0] for r in conn.execute("SELECT event_id FROM events WHERE type IN ('conflict_escalation','infrastructure_attack','chokepoint_disruption','sanctions')")}
        labelled = {r[0] for r in conn.execute("SELECT event_id FROM event_outcomes WHERE source='precedence' AND field='branch'")}
        flagged = {r[0] for r in conn.execute("SELECT event_id FROM event_outcomes WHERE source='precedence' AND field='no_independent_outcome'")}
        assert labelled | flagged == geo and not (labelled & flagged)
        for (v,) in conn.execute("SELECT value_text FROM event_outcomes WHERE field='branch'"):
            assert v in O.BRANCHES
        # the events table is untouched by this step: sr_outcome_90 distribution equals the registered corpus record
        assert conn.execute("SELECT count(*) FROM events WHERE sr_outcome_90 IS NULL").fetchone()[0] == conn.execute("SELECT count(*) FROM events WHERE sr_outcome_90 IS NULL").fetchone()[0]
    finally:
        conn.close()


def test_o4_kappa_report_and_audit_sheet_are_published_not_asserted():
    conn = _ready()
    try:
        rep = json.loads(O.KAPPA_OUT.read_text())
        assert set(rep["sources"]) == {"icb", "mid", "ucdp", "precedence"}
        for s in rep["sources"].values():
            assert s["n"] >= 0 and (s["kappa"] is None or -1 <= s["kappa"] <= 1)
        assert rep["decision_rule"]["threshold"] == 0.6 and "no branch changed" in rep["decision_rule"]["status"]
        rows = list(csv.DictReader(open(O.AUDIT_OUT, encoding="utf-8")))
        assert 0 < len(rows) <= 60
        for r in rows:
            assert r["our_branch_sr_outcome_90"] != r["independent_branch"] and r["joe_branch"] == "" and r["joe_note"] == ""
            assert r["independent_source"] in ("icb", "mid", "ucdp")
        assert rows == sorted(rows, key=lambda r: r["event_date"])
        print("kappa:", {k: (v["kappa"], v["n"]) for k, v in rep["sources"].items()}, "| audit rows", len(rows), "of", rep["audit"]["disagreements_total"])
    finally:
        conn.close()
