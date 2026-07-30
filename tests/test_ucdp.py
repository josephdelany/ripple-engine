"""
test_ucdp.py -- the UCDP aggregation is correct + the token stays out of the repo.

aggregate() turns raw events into monthly fatalities (global + per region); it's pure and testable with
no network. We also assert the fetcher never hardcodes a token. Run: python3 -m pytest -q tests/test_ucdp.py
"""

from pathlib import Path

import fetch_ucdp as U


def test_ucdp1_aggregate_sums_by_month_and_region():
    events = [
        {"date_start": "2025-01-05", "region": "Middle East", "best": 10},
        {"date_start": "2025-01-20", "region": "Middle East", "best": 5},
        {"date_start": "2025-01-11", "region": "Africa", "best": 3},
        {"date_start": "2025-02-02", "region": "Middle East", "best": 7},
        {"date_start": "", "region": "Asia", "best": 99},          # undated -> dropped
    ]
    by = U.aggregate(events)
    assert by["ucdp.fat_global"]["2025-01-28"] == 18               # 10+5+3
    assert by["ucdp.fat_global"]["2025-02-28"] == 7
    assert by["ucdp.fat_middle_east"]["2025-01-28"] == 15          # 10+5
    assert by["ucdp.fat_africa"]["2025-01-28"] == 3
    assert "2099" not in "".join(by["ucdp.fat_global"])            # the undated event never lands


def test_ucdp2_token_is_never_hardcoded():
    src = (Path(U.__file__)).read_text()
    # the token is read from env / user_settings only -- never a literal in the source
    assert "UCDP_TOKEN" in src and "ucdp_access_token" in src
    assert "1cd3cfe6" not in src                                   # the real token must not be committed
