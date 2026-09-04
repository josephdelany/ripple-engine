"""Linkage must never touch detection, and must never overstate what it found.

The linkage rule was run once and declared unusable (`registrations/DISRUPTION_REALIZATION.md`
Amendment 3). These tests hold that conclusion in place: they pin the reported counts so the
numbers cannot drift silently, and they enforce the vocabulary rule that an unmatched episode is
"not matched to the current event catalogue" and never "silent" or "undeclared".
"""
import csv
import datetime as dt
import json
from pathlib import Path

import pytest

import disruption_linkage as L

ROOT = Path(__file__).resolve().parent.parent
V3 = ROOT / "data" / "v3"
EPISODES = V3 / "episodes_n_tanker.csv"
EVENTS = V3 / "event_routes.csv"


def available():
    return EPISODES.exists() and EVENTS.exists()


@pytest.fixture(scope="module")
def result():
    if not available():
        pytest.skip("v3 linkage inputs not present in this checkout")
    return L.link(EPISODES, EVENTS, L.WINDOW_PRIMARY)


def test_linkage_does_not_modify_the_frozen_episode_table(result):
    """Detection is upstream and immutable. Linkage reads it and writes nothing to it."""
    before = EPISODES.read_bytes()
    L.link(EPISODES, EVENTS, L.WINDOW_PRIMARY)
    assert EPISODES.read_bytes() == before


def test_reported_eligibility_chain_is_the_corrected_one(result):
    """Amendment 2: 313 → 28 route-mapped → 11 excluded → 17 eligible. Not the original 21/18."""
    assert result["n_catalogue_total"] == 313
    assert result["n_route_mapped"] == 28
    assert result["n_excluded_before_detection"] == 11
    assert result["n_eligible_events"] == 17


def test_reported_proportions_are_pinned(result):
    """If these move, the feasibility document is stale and must be rewritten, not quietly updated."""
    assert result["n_eligible_events_linked"] == 4
    assert result["n_episodes"] == 39
    assert result["n_episodes_linked"] == 4
    # Stored rounded to 4 dp, so compare at that precision rather than to machine epsilon.
    assert abs(result["proportion_A_events_linked"] - 4 / 17) < 1e-4
    assert abs(result["proportion_B_episodes_linked"] - 4 / 39) < 1e-4


def test_wilson_interval_is_correct_on_a_known_case():
    """Checked against the closed form rather than trusted."""
    lo, hi = L.wilson(0, 10)
    assert lo == 0.0 and 0.27 < hi < 0.32
    lo, hi = L.wilson(5, 10)
    assert abs((lo + hi) / 2 - 0.5) < 1e-6
    assert L.wilson(0, 0) == (None, None)


def test_the_registered_window_has_not_been_widened():
    """Amendment 3: the Hormuz closure misses by one day and the window stays as registered."""
    assert L.WINDOW_PRIMARY == (-2, 14)
    assert L.WINDOW_STRICT == (0, 14)


def test_hormuz_closure_remains_unlinked_by_three_days(result):
    """The single largest episode is excluded. That fact is the finding, so it is pinned."""
    unlinked = {e[0] for e in result["eligible_events_not_linked"]}
    assert any("hormuz" in e[2] and e[1] == "2026-03-04" for e in
               result["eligible_events_not_linked"]), "the Hormuz closure should be unlinked"
    episode_starts = {r["start_date"] for r in csv.DictReader(EPISODES.open(encoding="utf-8"))
                      if r["route"] == "hormuz"}
    assert "2026-03-01" in episode_starts
    offset = (dt.date(2026, 3, 1) - dt.date(2026, 3, 4)).days
    assert offset == -3 and offset < L.WINDOW_PRIMARY[0]


def test_geography_mapping_is_the_registered_one():
    """No route may be assigned to an event by hand after episodes became visible."""
    assert set(L.ENTITY_TO_ROUTE.values()) == {
        "hormuz", "bab_el_mandeb", "suez", "bosporus", "malacca", "panama"}
    assert L.ENTITY_TO_ROUTE["chokepoint.suez_canal"] == "suez"
    assert "chokepoint.cape_of_good_hope" not in L.ENTITY_TO_ROUTE


def test_unmatched_episodes_are_never_called_undeclared():
    """The catalogue is not a census, so the prohibited vocabulary must not appear anywhere."""
    prohibited = ("undeclared", "silent disruption", "nobody called", "ignored by analysts",
                  "unexpected disruption")
    for path in (ROOT / "src" / "disruption_linkage.py",
                 ROOT / "docs" / "audit" / "V3_LINKAGE_FEASIBILITY.md",
                 ROOT / "docs" / "V3_STATUS.md"):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        # Paragraph-scoped, not line-scoped: a prohibition and the word it forbids are often
        # separated by a line wrap, and a line-based check reports that as a violation.
        for para in text.split("\n\n"):
            for word in prohibited:
                if word in para:
                    assert any(g in para for g in ("not ", "never", "prohibit", "may not")), \
                        f"{path.name}: unguarded use of {word!r} in {para[:80]!r}"


def test_route_coverage_gap_is_rule_independent(result):
    """The one v3 result quoted on the résumé. It must hold under ANY temporal linkage rule.

    Linkage requires an event and an episode to share a route, so episodes on a route with no
    eligible catalogue event are unmatchable by construction. This pins that count.
    """
    import collections
    events = [e for e in csv.DictReader(EVENTS.open(encoding="utf-8"))
              if dt.date.fromisoformat(e["event_date"]) >= L.DETECTION_START]
    episodes = list(csv.DictReader(EPISODES.open(encoding="utf-8")))
    per_event = collections.Counter(e["route"] for e in events)
    zero_event_routes = {p["route"] for p in episodes if per_event[p["route"]] == 0}
    unmatchable = [p for p in episodes if p["route"] in zero_event_routes]

    assert zero_event_routes == {"panama", "bosporus"}
    assert len(unmatchable) == 13
    assert len(episodes) == 39
    assert max(int(p["duration_days"]) for p in unmatchable) == 51
    # And the résumé must state it, so the document cannot drift away from the data.
    resume = (ROOT / "docs" / "RESUME.md").read_text(encoding="utf-8")
    assert "13 of 39" in resume and "51-day Panama" in resume
