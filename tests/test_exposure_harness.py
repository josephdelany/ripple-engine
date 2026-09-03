"""
tests/test_exposure_harness.py -- PHYSICAL_EXPOSURE_REGISTRATION.md §4, the estimation harness.

Every test name carries the clause it covers. All synthetic data is in-memory or under tmp_path and never
touches a real table (CLAUDE.md's fixture exception).

THE TWO THAT MATTER MOST are the calibration pair: a harness that cannot detect a PLANTED exposure effect
is worthless, and one that reports an effect on NOISE is worse than worthless. Both are asserted here,
before K's exposure file lands, so that whatever the real data says we already know the instrument works.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from exposure_harness import (  # noqa: E402
    SCHEMA, SPECS, HORIZONS, HEADLINE_H, TARGETS, CRACK_TARGETS, CRUDE_TARGETS,
    schema_doc, load_exposure, filtration_test, design, spec_mask, estimate, verdict,
    cluster_boot_idx, exposure_path, _ols,
)

CLASSES = ["sanctions", "policy_response", "conflict_escalation", "opec_decision",
           "infrastructure_attack", "chokepoint_disruption", "demand_shock"]


def synth_df(n=210, seed=0, n_per_cluster=3, x3_null=0, bad_pub=0):
    """An event panel in the shape build_panel() produces: date, type, cluster, X1_kbd, X3_share."""
    rng = np.random.default_rng(seed)
    dates = pd.to_datetime("2004-01-05") + pd.to_timedelta(
        np.repeat(np.arange(n // n_per_cluster) * 90, n_per_cluster)[:n] + rng.integers(0, 10, n), unit="D")
    df = pd.DataFrame({
        "event_id": [f"e{i:04d}" for i in range(n)],
        "date": dates,
        "type": rng.choice(CLASSES, n),
        "cluster": np.repeat(np.arange(n // n_per_cluster) + 1, n_per_cluster)[:n],
        "X1_kbd": rng.gamma(2.0, 900.0, n),
        "register_pub": dates - pd.to_timedelta(rng.integers(40, 700, n), unit="D"),
    })
    df["X3_share"] = df["X1_kbd"] / rng.uniform(1500, 4000, n)
    if x3_null:
        df.loc[df.index[:x3_null], "X3_share"] = np.nan
    if bad_pub:
        df.loc[df.index[:bad_pub], "register_pub"] = df.loc[df.index[:bad_pub], "date"]
    return df


def synth_Y(df, beta=0.0, noise=1.0, seed=1):
    """Responses with a PLANTED coefficient on X3. beta=0 is the null."""
    rng = np.random.default_rng(seed)
    x3 = df["X3_share"].to_numpy(float)
    Y = {}
    for t in TARGETS:
        Y[t] = {h: beta * np.nan_to_num(x3) + rng.normal(0, noise, len(df)) for h in HORIZONS}
    return Y


# ---------------------------------------------------------------- §2 the declared schema

def test_2_the_schema_is_declared_and_names_what_each_column_means():
    d = schema_doc()
    assert {"event_id", "X1_kbd", "X3_share", "register_pub"} <= set(d)
    for k, v in d.items():
        assert v["accepted_columns"] and v["meaning"]
    assert d["X3_share"]["required"] and d["register_pub"]["required"]
    assert "null, not zero" in d["X1_kbd"]["meaning"]


def test_2_the_harness_constructs_no_exposure_value_and_says_so_when_the_file_is_absent():
    if exposure_path() is not None:
        pytest.skip("K's exposure file has landed")
    with pytest.raises(FileNotFoundError) as e:
        load_exposure()
    assert "constructs no exposure value" in str(e.value)


def test_2_a_missing_required_column_is_named_exactly(tmp_path):
    df = synth_df(30).drop(columns=["X3_share"])
    p = tmp_path / "exposure.csv"
    df.to_csv(p, index=False)
    with pytest.raises(KeyError) as e:
        load_exposure(p)
    assert "X3_share" in str(e.value) and "do not rename K's file" in str(e.value)


# ---------------------------------------------------------------- §3 the filtration test

def test_3_a_register_published_on_or_after_the_event_date_voids_the_run():
    clean = filtration_test(synth_df(60))
    assert clean["asserted"] is True and clean["n_violations"] == 0
    bad = filtration_test(synth_df(60, bad_pub=4))
    assert bad["asserted"] is False and bad["n_violations"] == 4
    assert bad["first_violation"]["event_id"] == "e0000"


def test_3_a_missing_publication_date_is_a_violation_not_a_pass():
    df = synth_df(60)
    df.loc[df.index[0], "register_pub"] = pd.NaT
    r = filtration_test(df)
    assert r["asserted"] is False, "sourced-or-unknown: an unknown vintage cannot clear a filtration test"


# ---------------------------------------------------------------- §4 the four specifications

def test_4_the_four_registered_specifications_are_exactly_A_B_C_D():
    assert SPECS == ("A_dummy", "B_X3", "C_both", "D_X1")


def test_4_R1_spec_A_is_estimable_because_the_dummy_is_the_class_indicator_set():
    """On an event-date-only sample 'an event occurred' has no variance. R1 reads §4's dummy as the class
    indicators, which is the only reading under which A can be estimated at all."""
    df = synth_df(90)
    Y = synth_Y(df)
    m = spec_mask(df, "A_dummy", Y["brent"][20])
    X, names = design(df, "A_dummy", m)
    assert names[0] == "const" and sum(n.startswith("class[") for n in names) == len(CLASSES) - 1
    assert np.linalg.matrix_rank(X) == X.shape[1], "spec A must be full rank, i.e. actually estimable"


def test_4_each_spec_carries_exactly_the_registered_regressors():
    df = synth_df(90); Y = synth_Y(df)
    got = {}
    for spec in SPECS:
        m = spec_mask(df, spec, Y["brent"][20])
        got[spec] = set(design(df, spec, m)[1])
    assert "X3" in got["B_X3"] and not any(n.startswith("class[") for n in got["B_X3"])
    assert "X3" in got["C_both"] and any(n.startswith("class[") for n in got["C_both"])
    assert "X1" in got["D_X1"] and "X3" not in got["D_X1"]
    assert "X3" not in got["A_dummy"] and "X1" not in got["A_dummy"]


# ---------------------------------------------------------------- the unit of dependence

def test_INTERVAL_AUDIT_the_inferential_n_is_the_cluster_not_the_event():
    df = synth_df(210, n_per_cluster=3); Y = synth_Y(df, beta=2.0)
    e = estimate(df, Y, "brent", HEADLINE_H, n_boot=300)
    b = e["specs"]["B_X3"]
    assert b["n_clusters"] < b["n_events"], "3 events per cluster: clusters must be fewer"
    assert "n_clusters is the inferential n" in b["unit_of_dependence"]


def test_INTERVAL_AUDIT_the_cluster_bootstrap_keeps_a_cluster_intact():
    cl = np.repeat(np.arange(20), 5)
    rng = np.random.default_rng(0)
    ix = cluster_boot_idx(cl, rng)
    drawn = cl[ix]
    counts = pd.Series(drawn).value_counts()
    assert all(c % 5 == 0 for c in counts), "every drawn cluster must bring all five of its events"


def test_INTERVAL_AUDIT_a_cluster_bootstrap_is_not_narrower_than_an_event_bootstrap():
    """The defect this guards: resampling events instead of clusters would report a tighter band than the
    data supports.

    The dependence has to be modelled where it actually lives. A cluster-level shock on the INTERCEPT alone
    barely moves a slope's variance -- the first version of this test made that mistake and measured a ratio
    of 1.10. In this study the REGRESSOR is what clusters: events inside one 35-day window involve the same
    countries, so their capacity exposures are near-identical. With a clustered regressor and a clustered
    error, resampling events instead of clusters understates the band badly."""
    rng = np.random.default_rng(3)
    n_cl, per = 40, 5
    cl = np.repeat(np.arange(n_cl), per)
    shock = rng.normal(0, 1, n_cl)                       # a cluster-level common shock in the error
    x_cl = rng.normal(0, 1, n_cl)                        # and the regressor is itself a cluster property
    x = np.repeat(x_cl, per) + 0.05 * rng.normal(0, 1, n_cl * per)
    y = 0.5 * x + np.repeat(shock, per) + 0.05 * rng.normal(0, 1, n_cl * per)
    X = np.column_stack([np.ones_like(x), x])
    def band(resample_clusters):
        r = np.random.default_rng(7); out = []
        for _ in range(600):
            ix = cluster_boot_idx(cl, r) if resample_clusters else r.integers(0, len(y), len(y))
            out.append(_ols(X[ix], y[ix])[0][1])
        lo, hi = np.percentile(out, [2.5, 97.5]); return hi - lo
    assert band(True) > band(False) * 1.2, "the cluster band must be materially wider under clustering"


# ---------------------------------------------------------------- CALIBRATION: the pair that matters

def test_CALIBRATION_a_planted_exposure_effect_is_DETECTED_and_reads_MAGNITUDE_CARRIES():
    """If the harness cannot see an effect that is really there, no result it produces means anything."""
    df = synth_df(210, n_per_cluster=3, seed=5)
    Y = synth_Y(df, beta=4.0, noise=1.0, seed=6)          # a large, real X3 effect
    res = {"estimates": {}}
    for t in TARGETS:
        res["estimates"][f"{t}|h{HEADLINE_H}"] = estimate(df, Y, t, HEADLINE_H, n_boot=400)
    b = res["estimates"][f"brent|h{HEADLINE_H}"]
    assert b["specs"]["B_X3"]["coefficients"]["X3"]["excludes_zero"] is True
    assert b["r2_diff_B_minus_A"]["excludes_zero"] is True, "the R2 gain must be detected too (R2)"
    v = verdict(res)
    assert v["per_target"]["brent"]["verdict"] == "MAGNITUDE CARRIES", v["per_target"]["brent"]


def test_CALIBRATION_pure_noise_reads_NO_ADDITION_which_is_a_permitted_outcome():
    df = synth_df(210, n_per_cluster=3, seed=8)
    Y = synth_Y(df, beta=0.0, noise=1.0, seed=9)          # X3 carries nothing
    res = {"estimates": {}}
    for t in TARGETS:
        res["estimates"][f"{t}|h{HEADLINE_H}"] = estimate(df, Y, t, HEADLINE_H, n_boot=400)
    v = verdict(res)
    got = v["per_target"]["brent"]
    assert got["verdict"] == "NO ADDITION", got
    assert "permitted outcome" in (got["note"] or ""), "§5: NO ADDITION is not a failure of the study"


def test_CALIBRATION_the_verdict_distinguishes_normalised_from_unnormalised_BUFFER_MATTERS():
    """§5's second, separately falsifiable claim: B (normalised) beating D (unnormalised) is the thesis."""
    df = synth_df(210, n_per_cluster=3, seed=11)
    x3 = df["X3_share"].to_numpy(float)
    rng = np.random.default_rng(12)
    Y = {t: {h: 4.0 * x3 + rng.normal(0, 1, len(df)) for h in HORIZONS} for t in TARGETS}
    res = {"estimates": {f"{t}|h{HEADLINE_H}": estimate(df, Y, t, HEADLINE_H, n_boot=400) for t in TARGETS}}
    v = verdict(res)["per_target"]["brent"]
    assert v["B_X3_excludes_zero"] is True
    assert v["BUFFER_MATTERS"] in (True, False)
    if not v["D_X1_excludes_zero"]:
        assert v["BUFFER_MATTERS"] is True, "X3 works, X1 does not -> the normalisation is doing the work"


# ---------------------------------------------------------------- §8 the registered prediction

def test_8_cowork_s_prediction_is_evaluated_mechanically_and_can_come_out_false():
    """Cracks carry, crude does not. The harness reports whether that held, without being able to tune it."""
    df = synth_df(210, n_per_cluster=3, seed=13)
    x3 = df["X3_share"].to_numpy(float)
    rng = np.random.default_rng(14)
    Y = {}
    for t in TARGETS:
        beta = 5.0 if t in CRACK_TARGETS else 0.0        # exactly the predicted pattern
        Y[t] = {h: beta * x3 + rng.normal(0, 1, len(df)) for h in HORIZONS}
    res = {"estimates": {f"{t}|h{HEADLINE_H}": estimate(df, Y, t, HEADLINE_H, n_boot=400) for t in TARGETS}}
    p = verdict(res)["cowork_prediction_section_8"]
    assert p["registered_before_the_numbers"] is True
    assert p["cracks_carry"] is True and p["crude_carries"] is False
    assert p["prediction_held"] is True
    # and the reverse pattern must report the prediction FAILING
    Y2 = {t: {h: (0.0 if t in CRACK_TARGETS else 5.0) * x3 + rng.normal(0, 1, len(df)) for h in HORIZONS}
          for t in TARGETS}
    res2 = {"estimates": {f"{t}|h{HEADLINE_H}": estimate(df, Y2, t, HEADLINE_H, n_boot=400) for t in TARGETS}}
    assert verdict(res2)["cowork_prediction_section_8"]["prediction_held"] is False


# ---------------------------------------------------------------- §1 / §6 coverage of the complex

def test_1_all_eight_complex_targets_are_registered_not_crude_alone():
    assert set(TARGETS) == {"brent", "wti", "diesel_crack", "gasoline_crack", "henry_hub",
                            "propane", "fertilizer", "reroute"}
    assert CRACK_TARGETS == ("diesel_crack", "gasoline_crack")
    assert CRUDE_TARGETS == ("brent", "wti")
    assert HEADLINE_H == 20 and HORIZONS == (0, 1, 2, 5, 10, 20, 40, 60)


def test_6_R3_the_reroute_proxy_declares_its_construction_and_its_2019_start():
    r = TARGETS["reroute"]
    assert r["kind"] == "freight" and r["available_from"] == "2019-01-01"
    assert "cape_of_good_hope" in r["construction"] and "bab_el_mandeb" in r["construction"]


def test_6_R4_fertilizer_is_labelled_an_equity_proxy_not_a_price():
    assert TARGETS["fertilizer"]["proxy"] == "equity"
    assert TARGETS["fertilizer"]["series"].startswith("yf.eq_")


def test_2_X3_null_events_are_excluded_and_counted_never_zeroed():
    df = synth_df(120, x3_null=20)
    Y = synth_Y(df, beta=2.0)
    e = estimate(df, Y, "brent", HEADLINE_H, n_boot=200)
    assert e["specs"]["B_X3"]["n_events"] == 100, "the 20 null-X3 events must be dropped, not zero-filled"
    assert e["specs"]["A_dummy"]["n_events"] == 120, "spec A does not need X3, so it keeps all 120"
