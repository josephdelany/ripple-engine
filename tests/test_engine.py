"""
test_engine.py -- the engine proves itself.

Six small, hand-verifiable tests over the load-bearing maths and gates. Each one
has an expected value computed BY HAND in the comment, so the test documents the
behaviour, not just asserts it. Run:  python3 -m pytest -q
"""

import math
import sqlite3

import numpy as np
import pandas as pd


# t1 -- the CAR of a perfectly flat (constant-return) series must be exactly 0:
# abnormal return = actual - mean, and if every return is the same, every abnormal
# return is 0, so the cumulative is 0.
def test_t1_flat_series_car_is_zero():
    from event_study import car_for_event, PRE
    dates = pd.bdate_range("2000-01-03", periods=300)
    ret = pd.Series(0.001, index=dates)          # constant 0.1%/day
    car = car_for_event(ret, dates[200])
    assert car is not None
    assert abs(car[PRE + 20]) < 1e-12


# t2 -- clustering (35-day window): two events 10 days apart collapse into one
# episode; two events 40 days apart stay separate.
def test_t2_clustering_collapses_near_keeps_far():
    from robustness import assign_clusters
    def n_clusters(gap_days):
        base = pd.Timestamp("2010-01-01")
        df = pd.DataFrame({"date": [base.strftime("%Y-%m-%d"),
                                    (base + pd.Timedelta(days=gap_days)).strftime("%Y-%m-%d")]})
        return assign_clusters(df)["cluster"].nunique()
    assert n_clusters(10) == 1        # within 35 days -> one cluster
    assert n_clusters(40) == 2        # beyond 35 days -> two clusters


# t3 -- inv_sigma seasonal z reproduces a hand-computed value. Six years of the
# same week-of-year with values 100,110,120,130,140,200. The prior five
# (100..140) have mean 120 and sample std sqrt(250)=15.8114; the 6th year's z is
# (200-120)/15.8114 = 5.060.
def test_t3_inv_sigma_seasonal_z():
    from datetime import date
    from derive_signals import seasonal_sigma
    # Pin every point to ISO week 26 across years so they form ONE seasonal group
    # (calendar dates like 'June 15' drift across ISO weeks in 53-week years).
    idx = pd.to_datetime([date.fromisocalendar(y, 26, 3) for y in range(2001, 2007)])
    s = pd.Series([100, 110, 120, 130, 140, 200], index=idx, dtype=float)
    z = seasonal_sigma(s)
    assert abs(z.iloc[-1] - 5.060) < 0.02


# t4 -- inference standardization: with an estimation window of alternating
# +/-0.02 (sample std ~= 0.02) and a single +0.10 event-day shock, the
# standardized CAR+20 = car20 / (sigma * sqrt(26)) ~= 0.10 / (0.02 * 5.099) ~= 0.94.
def test_t4_standardization_matches_hand_sigma():
    from event_study import car_for_event, PRE
    from inference import sigma_for_event, CAR20_LEN
    dates = pd.bdate_range("2000-01-03", periods=400)
    ret = pd.Series([0.02 if i % 2 == 0 else -0.02 for i in range(400)],
                    index=dates, dtype=float)
    pos = 200
    ret.iloc[pos - 5: pos + 21] = 0.0            # clear the event window
    ret.iloc[pos] = 0.10                          # the shock
    sigma = sigma_for_event(ret, dates[pos])
    car20 = car_for_event(ret, dates[pos])[PRE + 20]
    std = car20 / (sigma * math.sqrt(CAR20_LEN))
    assert 0.019 < sigma < 0.021                  # hand: ~0.0201
    assert 0.85 < std < 1.00                       # hand: ~0.94


# t5 -- the loader flags an event with a missing source (codebook: no source, not
# in the dataset); a sourced row is not flagged.
def test_t5_loader_flags_unsourced():
    from load_events import check
    row = {"type": "sanctions", "date_precision": "day", "confidence": "high",
           "event_date": "2020-01-01", "severity": "3", "surprise": "3",
           "source_url": "https://example.com/doc"}
    assert not any(p.startswith("MISSING SOURCE") for p in check(row, 1))
    row["source_url"] = ""
    assert any(p.startswith("MISSING SOURCE") for p in check(row, 1))


# t6 -- the watcher dedups: the same story url is new once, then never again.
def test_t6_watcher_dedup():
    from watcher import is_new
    seen = sqlite3.connect(":memory:")
    seen.execute("CREATE TABLE seen (story_hash TEXT PRIMARY KEY, first_seen TEXT)")
    url = "http://example.com/a-story"
    assert is_new(seen, url) is True
    assert is_new(seen, url) is False
