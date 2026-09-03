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
    assert g["engine_vs"]["climatology"]["n"] == d["n_published"]   # binds at any n, not just 150
    assert s["verdict"]["rules"]["engine:G"]["status_code"] == "SUGGESTIVE / null"
    assert s["verdict"]["audit_passed"] is False


def test_k_the_exclusion_set_is_fs_registered_field():
    d = _s()["tiers"]["daily"]["G"]["diagnostic_hostile"]
    assert d["n_published"] == d["n_retained"] + d["n_dropped"]     # the partition must be exact
    assert d["n_retained"] > 0 and d["n_dropped"] > 0
    # A3.3 registers WHICH hostility values have an undefined G target, not how many events carry
    # them -- the counts move with the target rebuild, the exclusion set does not.
    assert set(d["dropped_by_hostility"]) <= {"non_hostile", "ambiguous"}
    assert set(d["dropped_by_hostility"]), "the exclusion set must not be silently empty"
    assert set(d["retained_by_hostility"]) <= {"hostile", "hostile_unattributed"}
    assert sum(d["retained_by_hostility"].values()) == d["n_retained"]
    assert sum(d["dropped_by_hostility"].values()) == d["n_dropped"]


def test_k_climatology_was_re_estimated_not_reused():
    """The point of the exercise: the baseline moves too. Its pool shrinks and its mean score changes."""
    s = _s(); g = s["tiers"]["daily"]["G"]; d = g["diagnostic_hostile"]
    assert d["climatology_pool"]["mean_size_reduced"] < d["climatology_pool"]["mean_size_published"]
    assert d["brier"]["climatology"]["ref_mean"] != g["engine_vs"]["climatology"]["ref_mean"]
    assert d["brier"]["climatology"]["engine_mean"] != g["engine_vs"]["climatology"]["engine_mean"]
    # the level-0 share moves, which is why climatology had to be re-estimated
    # the DIRECTION is the registered claim (K.2: removing undefined-target reads lowers the
    # level-0 share); the two literals were an artefact of the pre-Amendment-4 target
    assert 0.0 <= d["level0_share_retained"]["pct"] <= d["level0_share_published"]["pct"]


def test_k_every_baseline_is_reported_with_its_interval_on_both_scores():
    d = _s()["tiers"]["daily"]["G"]["diagnostic_hostile"]
    for score in ("brier", "rps"):
        assert set(d[score]) == {"climatology", "frozen", "random_analogs", "persistence"}
        for ref, b in d[score].items():
            assert b["n"] == d["n_retained"], (score, ref)
            assert b["skill"] is not None and b["ci95"][0] is not None and b["dm_p"] is not None
    assert f"n falls from {d['n_published']} to {d['n_retained']}" in d["limit"]
