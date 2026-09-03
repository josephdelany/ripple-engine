"""MAGNITUDE_REGISTRATION.md section 5 -- the pre-registered re-test of severity_dose_response.

Every test names the registered section it covers. The point of these is that the verdict words were
fixed BEFORE the test ran (sealed 8cb9d3d), that the re-test builds the null the published claim
never did, and that edge_battery.json is reported on rather than edited."""
import json
from pathlib import Path

import numpy as np
import pytest

import ripple_lp as R
import magnitude_severity_retest as M

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "magnitude" / "severity_retest.json"


@pytest.fixture(scope="module")
def payload():
    if not OUT.exists():
        pytest.skip("run src/magnitude_severity_retest.py first")
    return json.loads(OUT.read_text())


def test_s5_the_published_claim_is_recorded_verbatim_before_being_re_tested(payload):
    p = payload["published_claim"]
    assert p["validated"] is True and p["amp"] == pytest.approx(5.0789)
    assert p["survives_fdr"] is True and p["survives_bonferroni"] is False
    assert p["n"] == 116 and p["n_high"] == 76 and p["n_low"] == 40


def test_s5_verdict_vocabulary_is_the_registered_mapping(payload):
    """RETAINED if TRANSMITTING, RETRACTED if NULL, INSUFFICIENT below n=15 -- fixed in advance."""
    a = payload["test_a_claim_as_published"]["all_events"]
    assert a["verdict"] in ("TRANSMITTING", "NULL", "INSUFFICIENT")
    mapping = {"TRANSMITTING": "RETAINED", "NULL": "RETRACTED", "INSUFFICIENT": "INSUFFICIENT"}
    assert payload["verdict"] == mapping[a["verdict"]]


def test_s5_the_retest_builds_a_non_event_comparison_which_the_published_test_lacked(payload):
    """The registered defect: the published gate never looks at a non-event day."""
    pl = payload["test_a_claim_as_published"]["all_events"]["placebo"]
    assert pl is not None and pl["n_draws"] >= 100
    assert "percentile" in pl and "beyond_state" in pl


def test_s5_severity_dose_response_is_retracted(payload):
    """The result, asserted so a later change of it is a visible test failure."""
    a = payload["test_a_claim_as_published"]["all_events"]
    assert a["welch"]["excludes_zero"] is False
    assert a["placebo"]["beyond_state"] is False
    assert payload["verdict"] == "RETRACTED"


def test_s5_both_severity_arms_are_null_as_ordinary_ripple_cells(payload):
    for r in payload["test_b_ripple_cells"]:
        assert r["verdict"] in ("NULL", "INSUFFICIENT"), r["shock"]


def test_s5_edge_battery_json_is_not_edited_by_this_brief(payload):
    """Amendment B's pattern: report the status, let the owning session act."""
    assert payload["meta"]["edge_battery_json_edited"] is False
    src = (ROOT / "src" / "magnitude_severity_retest.py").read_text()
    # no line may both name edge_battery and write anything
    for line in src.splitlines():
        if "edge_battery" in line:
            assert not any(w in line for w in ("write_text", "json.dump", "open(", "w\")", "'w'")), line
    # the only path this module writes to is its own output directory
    assert 'OUT = ROOT / "data" / "magnitude"' in src
    assert src.count("write_text") == 1 and 'OUT / "severity_retest.json"' in src


def test_s5_the_clustering_unit_defect_is_quantified(payload):
    """Clustering within TYPE does not de-overlap a comparison grouped by SEVERITY."""
    c = payload["clustering_unit_check"]["high_sev_ge_4"]
    assert c["clustered_within_type"] > c["clustered_within_severity_group"]
    assert c["raw"] >= c["clustered_within_type"]


def test_s5_provenance_resolves_the_upper_bound_i_published(payload):
    """MAGNITUDE_REGISTRATION.md section 5 reported 102 as an UPPER bound on class-imputed
    severities. Resolved: the auto-admit path never ran against this corpus."""
    p = payload["severity_provenance"]
    assert p["n_on_class_band"] == 102
    assert p["n_flagged_AUTO_ADMIT"] == 0
    assert p["n_demonstrably_class_imputed"] == 0
    assert p["admission_log_exists"] is False
    assert p["n_joe_approved"] == p["n_in_candidate_review_sheet"]


def test_s5_the_off_band_split_is_one_sided_and_must_not_be_read_as_cleaner():
    """SEV_BAND's values are {2,3}: 3 is in neither arm and 2 is in the LOW arm only, so excluding
    on-band events can only ever strip the low arm. A test, because the off-band number is larger
    and would otherwise look like the better estimate."""
    assert set(M.SEV_BAND.values()) == {2, 3}
    assert all(v > M.LO or v == M.LO for v in M.SEV_BAND.values())
    assert not any(v >= M.HI for v in M.SEV_BAND.values())   # nothing on-band can be in the HIGH arm


def test_s5_estimator_is_imported_from_ripple_lp_not_reimplemented():
    src = (ROOT / "src" / "magnitude_severity_retest.py").read_text()
    assert "import ripple_lp as R" in src
    for fn in ["def run_lp(", "def placebo(", "def verdict(", "def cluster_first_dates(", "def ols("]:
        assert fn not in src, f"{fn} is re-implemented; it must come from ripple_lp"


def test_s5_registered_constants_unchanged():
    assert R.MIN_N == 15 and R.CLUSTER_DAYS == 35 and R.N_PLACEBO == 500
    assert M.HORIZON == 20 and M.HI == 4 and M.LO == 2
