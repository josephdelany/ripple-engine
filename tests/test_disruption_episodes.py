"""Behavioural tests for the impairment detector, against synthetic series with known answers.

Nothing here uses real chokepoint data to decide whether the detector is correct — a synthetic
series is the only place the right answer is known independently of the thing being tested.
"""
import datetime as dt

import numpy as np
import pytest

import disruption_episodes as D


def series(values, start=dt.date(2019, 1, 1)):
    return [start + dt.timedelta(days=i) for i in range(len(values))], list(values)


def flat_then(drop_at, drop_len, level=20.0, low=5.0, n=900):
    """A long flat run so the baseline is well defined, then a drop of known length."""
    v = [level] * n
    for i in range(drop_at, drop_at + drop_len):
        v[i] = low
    return v


def test_baseline_uses_only_prior_observations():
    """A spike at t must never affect the baseline at t, or at any earlier date."""
    v = [10.0] * 900
    base_flat = D.baselines(v)
    v2 = list(v)
    v2[800] = 10_000.0
    base_spiked = D.baselines(v2)
    assert np.allclose(base_flat[:800], base_spiked[:800], equal_nan=True)
    assert base_flat[800] == base_spiked[800], "the spike leaked into its own baseline"


def test_baseline_respects_the_registered_gap():
    """Values inside the 30-day exclusion gap must not enter the baseline."""
    v = [10.0] * 900
    for i in range(870, 900):          # the 30 days immediately before index 899
        v[i] = 1000.0
    base = D.baselines(v)
    assert base[899] == 10.0, "the contamination gap did not exclude recent days"


def test_baseline_is_nan_before_enough_history():
    v = [10.0] * 900
    base = D.baselines(v)
    assert np.isnan(base[:D.BASELINE_WINDOW + D.BASELINE_GAP - 1]).all()
    assert np.isfinite(base[D.BASELINE_WINDOW + D.BASELINE_GAP])


def test_synthetic_episode_is_detected_with_correct_boundaries():
    v = flat_then(drop_at=600, drop_len=10)
    dates, values = series(v)
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert len(rows) == 1
    ep = rows[0]
    assert ep["start_date"] == dates[600].isoformat()
    assert ep["end_date"] == dates[609].isoformat()
    assert ep["n_impaired_days"] == 10
    assert ep["duration_days"] == 10
    assert ep["observed_at_trough"] == 5.0
    assert ep["baseline_at_trough"] == 20.0
    assert abs(ep["fractional_impairment"] - 0.75) < 1e-9
    assert ep["detector_version"] == D.DETECTOR_VERSION


def test_short_dip_below_the_minimum_is_not_an_episode():
    dates, values = series(flat_then(600, D.MIN_IMPAIRED_DAYS - 1))
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert rows == []


def test_shallow_dip_above_the_threshold_is_not_an_episode():
    """0.75 of baseline is above the 0.70 threshold, however long it lasts."""
    v = [20.0] * 900
    for i in range(600, 640):
        v[i] = 15.0                      # ratio 0.75
    dates, values = series(v)
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert rows == []


def test_short_rebound_does_not_split_one_episode():
    """A two-day recovery is inside the tolerated gap (§10)."""
    v = flat_then(600, 12)
    v[606] = v[607] = 20.0               # two clean days in the middle
    dates, values = series(v)
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert len(rows) == 1
    assert rows[0]["n_impaired_days"] == 10
    assert rows[0]["duration_days"] == 12, "calendar span should include the tolerated gap"


def test_long_rebound_splits_two_episodes():
    """Three clean days exceed MAX_GAP and close the episode (§11)."""
    v = flat_then(600, 16)
    for i in (606, 607, 608):
        v[i] = 20.0
    dates, values = series(v)
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert len(rows) == 2
    assert rows[0]["end_date"] == dates[605].isoformat()
    assert rows[1]["start_date"] == dates[609].isoformat()


def test_zero_is_a_real_observation_not_missing_data():
    """A total stoppage is the strongest possible signal and must never be dropped."""
    v = flat_then(600, 10, low=0.0)
    dates, values = series(v)
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert len(rows) == 1
    assert rows[0]["observed_at_trough"] == 0.0
    assert abs(rows[0]["fractional_impairment"] - 1.0) < 1e-9


def test_future_observations_cannot_change_a_completed_historical_episode():
    """Truncating the future must leave already-closed episodes byte-identical.

    The registered recovery rule (§11) needs at most 3 days beyond an episode's end, so an episode
    that closed well before the truncation point cannot move.
    """
    v = flat_then(600, 10)
    v[700:720] = [4.0] * 20              # a second, later disruption
    dates, values = series(v)
    full, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    trunc, _ = D.detect_route(dates[:650], values[:650], "synthetic", "n_tanker")
    assert len(full) == 2 and len(trunc) == 1
    assert full[0] == trunc[0], "a completed episode changed when future data was added"


def test_trough_tie_resolves_to_the_earliest_date():
    v = flat_then(600, 10)               # every impaired day has an identical ratio
    dates, values = series(v)
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert rows[0]["trough_date"] == dates[600].isoformat()


def test_tanker_days_lost_matches_a_hand_computation():
    v = flat_then(600, 10, level=20.0, low=5.0)
    dates, values = series(v)
    rows, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert abs(rows[0]["tanker_days_lost"] - 10 * (20.0 - 5.0)) < 1e-6


def test_detection_is_deterministic():
    v = flat_then(600, 10)
    dates, values = series(v)
    a, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    b, _ = D.detect_route(dates, values, "synthetic", "n_tanker")
    assert a == b


@pytest.mark.parametrize("bad,msg", [
    ("series_id,obs_date\nx,2020-01-01\n", "unexpected columns"),
    ("series_id,obs_date,value\nx,2020-01-01,abc\n", "unparseable"),
    ("series_id,obs_date,value\nx,2020-01-01,1\nx,2020-01-01,2\n", "duplicate"),
    ("series_id,obs_date,value\nx,2020-01-01,1\nx,2020-01-05,2\n", "non-daily"),
])
def test_malformed_input_fails_loudly(tmp_path, bad, msg):
    p = tmp_path / "bad.csv"
    p.write_text(bad, encoding="utf-8")
    with pytest.raises(D.InputError, match=msg):
        D.load_panel(p)


def test_missing_required_series_fails_rather_than_skipping(tmp_path):
    p = tmp_path / "partial.csv"
    rows = ["series_id,obs_date,value"]
    for i in range(500):
        d = dt.date(2020, 1, 1) + dt.timedelta(days=i)
        rows.append(f"portwatch.hormuz.n_tanker,{d.isoformat()},10")
    p.write_text("\n".join(rows) + "\n", encoding="utf-8")
    with pytest.raises(D.InputError, match="required series missing"):
        D.detect_all(D.load_panel(p))
