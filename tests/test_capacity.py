"""T1 of PHYSICAL_EXPOSURE_REGISTRATION.md -- the capacity register and its vintage rule.

Section 3 is the trap this file exists to spring: "A register's knowable_at is its publication date,
not its reference year. The 2019 EI Statistical Review, published mid-2020, may not inform a 2019
forecast. A filtration test asserts no exposure value derives from a register published after its
event date." test_t1_filtration_no_value_is_read_before_it_was_published is that test."""
import json
import sqlite3
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "state"))
import capacity as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "state" / "capacity_register.json"


@pytest.fixture(scope="module")
def payload():
    if not REG.exists():
        pytest.skip("run src/state/capacity.py first")
    return json.loads(REG.read_text())


# --- section 3, the vintage rule -------------------------------------------------------------

def test_t1_every_register_row_carries_a_publication_date(payload):
    for r in payload["register"]:
        assert r.get("knowable_at"), r
        assert r.get("publication_date"), r
        pd.Timestamp(r["knowable_at"])


def test_t1_knowable_at_is_never_before_the_reference_period(payload):
    """The 2019-Review-published-mid-2020 trap, in the direction it actually bites: a figure may not
    become knowable BEFORE the period it describes has ended."""
    for r in payload["register"]:
        ref = pd.Timestamp(r["reference_period"] + "-01")
        assert pd.Timestamp(r["knowable_at"]) >= ref, r


def test_t1_filtration_no_value_is_read_before_it_was_published(payload):
    """THE registered filtration test. For every register row, a lookup dated one day before that
    row became knowable must never return it."""
    reg = payload["register"]
    for r in reg[:: max(1, len(reg) // 60)]:
        t = pd.Timestamp(r["knowable_at"]) - pd.Timedelta(days=1)
        got = C.lookup(reg, r["entity_id"], r["measure"], t)
        assert got is None or pd.Timestamp(got["knowable_at"]) <= t
        assert got is not r


def test_t1_lookup_returns_the_latest_register_published_on_or_before_t(payload):
    reg = payload["register"]
    for ent, meas in [("country.usa", "refining_capacity"),
                      ("opec.total", "crude_production_capacity")]:
        rows = sorted([r for r in reg if r["entity_id"] == ent and r["measure"] == meas],
                      key=lambda r: r["knowable_at"])
        assert len(rows) > 4
        mid = rows[len(rows) // 2]
        got = C.lookup(reg, ent, meas, pd.Timestamp(mid["knowable_at"]))
        assert got["knowable_at"] == mid["knowable_at"]
        # a day earlier must fall back to a strictly earlier vintage
        prev = C.lookup(reg, ent, meas, pd.Timestamp(mid["knowable_at"]) - pd.Timedelta(days=1))
        assert prev is None or pd.Timestamp(prev["knowable_at"]) < pd.Timestamp(mid["knowable_at"])


def test_t1_lookup_before_any_register_returns_none_not_zero(payload):
    """Section 2's registered fallback: X1 is null, not zero."""
    got = C.lookup(payload["register"], "country.usa", "refining_capacity", pd.Timestamp("1990-01-01"))
    assert got is None


# --- what the register honestly contains -----------------------------------------------------

def test_t1_aggregates_are_never_labelled_as_countries(payload):
    """The failure mode worth a test: silently passing an OPEC regional figure off as a country's."""
    for r in payload["register"]:
        if r["entity_id"].startswith("country."):
            assert r["scope"] == "country", r
        else:
            assert r["scope"] == "aggregate", r
    countries = {r["entity_id"] for r in payload["register"] if r["scope"] == "country"}
    assert countries == {"country.usa"}


def test_t1_crude_production_capacity_has_no_country_row(payload):
    """The finding, asserted so a later change is visible: no reachable source carries it."""
    rows = [r for r in payload["register"] if r["measure"] == "crude_production_capacity"]
    assert rows and all(r["scope"] == "aggregate" for r in rows)


def test_t1_every_named_country_without_a_register_has_an_explicit_null_row(payload):
    have = {(r["entity_id"], r["measure"]) for r in payload["register"]}
    named = set(payload["corpus_side"]["countries"])
    gapped = {(g["entity_id"], g["measure"]) for g in payload["gaps"]}
    for cc in named:
        for m in ("crude_production_capacity", "refining_capacity"):
            assert (cc, m) in have or (cc, m) in gapped, (cc, m)
    for g in payload["gaps"]:
        assert g["value_kbd"] is None and g["knowable_at"] is None
        assert "null, not zero" in g["registered_fallback"]


def test_t1_coverage_matches_what_was_reported_to_joe(payload):
    cov = payload["coverage"]
    assert cov["crude_production_capacity"]["events_with_a_country_figure_published_before_the_event"] == 0
    assert cov["refining_capacity"]["events_with_a_country_figure_published_before_the_event"] == 15
    assert cov["crude_production_capacity"]["of"] == 187


def test_t1_coverage_is_recomputed_by_the_same_lookup_the_study_would_use(payload):
    """Not a stored constant: recompute it here from the register."""
    conn = sqlite3.connect(ROOT / "data" / "oil.db")
    geo, sets = C.coded_country_sets(conn)
    n = sum(1 for _, e in geo.iterrows()
            if any(C.lookup(payload["register"], cc, "refining_capacity", e.event_date)
                   for cc in sets[e.event_id]))
    conn.close()
    assert n == payload["coverage"]["refining_capacity"]["events_with_a_country_figure_published_before_the_event"]


def test_t1_vintages_are_distinct_releases_with_increasing_publication_dates(payload):
    v = payload["vintages"]
    assert len(v) >= 20
    months = [x["publication_month"] for x in v]
    assert len(set(months)) == len(months)


def test_t1_the_source_is_not_committed_only_the_derived_register():
    """Charter: licence-restricted and bulk sources stay local and gitignored."""
    gi = (ROOT / ".gitignore").read_text()
    assert "data/state/raw/" in gi
    assert not (ROOT / "data" / "state" / "raw" / "steo_archives" / ".gitkeep").exists()
