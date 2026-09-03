"""WALK_FORWARD_PROTOCOL.md Amendment K: the hostility diagnostic is a DIAGNOSTIC -- it recomputes from the
sealed files, it re-estimates climatology on the reduced pool, and it changes no published number and no
verdict. Reads the committed artefacts; writes nothing."""
import json
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

SUMMARY = os.path.join(ROOT, "data", "walk_forward", "summary.json")


def _s():
    return json.load(open(SUMMARY))


def test_k_diagnostic_is_present_labelled_and_gates_nothing():
    s = _s()
    g = s["tiers"]["daily"]["G"]
    d = g["diagnostic_hostile"]
    assert d["registered"] is False and d["gates"].startswith("nothing") and "§7 are untouched" in d["gates"]
    assert d["derived_from_run"] == s["run_id"]                      # derived from the run in the tree
    assert "Amendment K" in d["amendment"] and "A3.3" in d["amendment"]
    # the registered numbers beside it are untouched by the diagnostic
    assert g["engine_vs"]["climatology"]["n"] == d["n_published"] == 150
    assert s["verdict"]["rules"]["engine:G"]["status_code"] == "SUGGESTIVE / null"
    assert s["verdict"]["audit_passed"] is False


def test_k_the_exclusion_set_is_fs_registered_field():
    d = _s()["tiers"]["daily"]["G"]["diagnostic_hostile"]
    assert d["n_published"] == d["n_retained"] + d["n_dropped"] == 150
    assert d["n_retained"] == 123 and d["n_dropped"] == 27
    assert d["dropped_by_hostility"] == {"ambiguous": 10, "non_hostile": 17}       # A3.3: target undefined
    assert set(d["retained_by_hostility"]) <= {"hostile", "hostile_unattributed"}
    assert sum(d["retained_by_hostility"].values()) == 123


def test_k_climatology_was_re_estimated_not_reused():
    """The point of the exercise: the baseline moves too. Its pool shrinks and its mean score changes."""
    s = _s(); g = s["tiers"]["daily"]["G"]; d = g["diagnostic_hostile"]
    assert d["climatology_pool"]["mean_size_reduced"] < d["climatology_pool"]["mean_size_published"]
    assert d["brier"]["climatology"]["ref_mean"] != g["engine_vs"]["climatology"]["ref_mean"]
    assert d["brier"]["climatology"]["engine_mean"] != g["engine_vs"]["climatology"]["engine_mean"]
    # the level-0 share moves, which is why climatology had to be re-estimated
    assert d["level0_share_published"]["pct"] == 42.0 and d["level0_share_retained"]["pct"] == 32.5


def test_k_every_baseline_is_reported_with_its_interval_on_both_scores():
    d = _s()["tiers"]["daily"]["G"]["diagnostic_hostile"]
    for score in ("brier", "rps"):
        assert set(d[score]) == {"climatology", "frozen", "random_analogs", "persistence"}
        for ref, b in d[score].items():
            assert b["n"] == 123, (score, ref)
            assert b["skill"] is not None and b["ci95"][0] is not None and b["dm_p"] is not None
    assert "n falls from 150 to 123" in d["limit"]
