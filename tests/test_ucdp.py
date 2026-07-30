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


def test_ucdp3_verified_conflict_modality_logic():
    import corroborate as C
    from datetime import date
    idx = {"Iran": [date(2025, 6, 13), date(2025, 7, 20)], "Israel": [date(2025, 3, 10)]}
    # a news cluster near a UCDP Iran event -> corroborated (only Iran is in-window here)
    hit = C._ucdp_hit([{"ts": "2025-06-15", "headline": "x"}], {"Iran", "Israel"}, idx)
    assert hit and hit.startswith("Iran:")
    # out of window -> no match
    assert C._ucdp_hit([{"ts": "2025-01-01", "headline": "x"}], {"Iran", "Israel"}, idx) is None
    # out of the situation's countries -> no match
    assert C._ucdp_hit([{"ts": "2025-06-15", "headline": "x"}], {"Yemen (North Yemen)"}, idx) is None


def test_ucdp4_country_map_covers_every_situation():
    """A new situation must never silently miss UCDP corroboration: every country.* in situations.yaml
    has a frozen ENTITY_TO_UCDP entry."""
    import re
    import corroborate as C
    yaml_text = (Path(C.__file__).resolve().parent.parent / "data" / "situations.yaml").read_text()
    countries = {m.split(".", 1)[1] for m in re.findall(r"country\.[a-z_]+", yaml_text)}
    missing = [c for c in countries if c not in C.ENTITY_TO_UCDP]
    assert not missing, f"situations.yaml countries missing from ENTITY_TO_UCDP: {missing}"


def test_ucdp5_conditioner_is_point_in_time_declared():
    """The conflict-intensity conditioner exists and its mechanism declares the t-1 / no-lookahead rule."""
    import derive_signals as D
    m = D.MECHANISMS.get("derived.conflict_intensity_pct")
    assert m is not None
    assert "t-1" in m[2].lower() and "lookahead" in m[2].lower()
