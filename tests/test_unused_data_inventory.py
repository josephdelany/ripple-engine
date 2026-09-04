"""The availability finding rests on one filter clause. That claim must be checked, not asserted.

`docs/audit/UNUSED_DATA_INVENTORY.md` says the strict point-in-time rule excludes almost every
geopolitical field through `release <= event_date` alone, and that the other three clauses do
essentially nothing. That is a load-bearing statement — it is why `docs/PAPER.md` §6 says the
full-state question is untested rather than failed — so it is recomputed here.

Everything is recomputed from the committed input bundle, not from `data/oil.db`, so this runs in
a clean checkout where the database is absent.
"""
import collections
import csv
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "data" / "structural_surface" / "input"
SUMMARY = ROOT / "data" / "structural_surface" / "summary.json"
INVENTORY = ROOT / "docs" / "audit" / "UNUSED_DATA_INVENTORY.md"


@pytest.fixture(scope="module")
def rows():
    events = {r["event_id"]: r["event_date"]
              for r in csv.DictReader((BUNDLE / "events.csv").open(encoding="utf-8"))}
    out = []
    for r in csv.DictReader((BUNDLE / "situation_state.csv").open(encoding="utf-8")):
        d = events.get(r["event_id"])
        if d:
            out.append((r, d))
    return out


@pytest.fixture(scope="module")
def panel(rows):
    """The base the experiment's own availability audit uses: 60 `situation`-coded rows dropped."""
    return [(r, d) for r, d in rows if r["entity_id"] != "situation"]


def test_release_clause_is_what_excludes_the_state_data(rows, panel):
    """The inventory's central claim: one clause does all the excluding."""
    n = len(panel)
    obs_after = sum(1 for r, d in panel if r["obs_date"] > d)
    vintage_after = sum(1 for r, d in panel if r["vintage"] > d)
    release_after = sum(1 for r, d in panel if r["release"] > d)
    retrospective = sum(1 for r, _ in panel if r["retrospective"] == "1")

    assert len(rows) == 11089
    assert n == 11029
    assert obs_after == 0, "the inventory says observation dates exclude nothing"
    assert vintage_after == 0, "the inventory says vintages exclude nothing"
    assert release_after == 10150
    assert retrospective == 2682
    # The point of the finding: release alone accounts for the overwhelming majority.
    assert release_after / n > 0.9


def test_decomposition_matches_the_experiments_own_availability_audit(rows, panel):
    """The frozen experiment publishes the same counts; the two must not drift apart."""
    audit = json.loads(SUMMARY.read_text(encoding="utf-8"))["availability_audit"]
    assert audit["all_rows"] == len(rows)
    assert audit["panel_rows"] == len(panel)
    assert audit["situation_coded_rows"] == len(rows) - len(panel) == 60
    assert audit["vintage_after_event_rows"] == 0
    assert audit["release_after_event_rows"] == sum(1 for r, d in panel if r["release"] > d)
    assert audit["retrospective_rows"] == sum(1 for r, _ in panel if r["retrospective"] == "1")


def test_the_state_fields_are_collected_at_real_coverage(rows):
    """'Missing data' would be a different problem with a different remedy. It is not missing."""
    events = collections.Counter()
    for r, _ in rows:
        events[r["field"]] += 0  # ensure key exists
    per_field = collections.defaultdict(set)
    for r, _ in rows:
        per_field[r["field"]].add(r["event_id"])
    # Fields the inventory names as well covered but unusable under the strict rule.
    for field, at_least in (("polity2", 200), ("cinc", 200), ("milex_cow", 200),
                            ("coup_last_5y", 200), ("ucdp_active_conflicts", 300),
                            ("ucdp_battle_deaths", 250)):
        assert len(per_field[field]) >= at_least, \
            f"{field} covers {len(per_field[field])} events, inventory claims >= {at_least}"


def test_only_the_two_leader_fields_survive_the_strict_rule(rows):
    """If a third field ever survives, the inventory and the paper both need rewriting."""
    survivors = collections.Counter()
    for r, d in rows:
        if (r["entity_id"] != "situation" and r["obs_date"] <= d and r["vintage"] <= d
                and r["release"] <= d and r["retrospective"] == "0"):
            survivors[r["field"]] += 1
    top = [f for f, n in survivors.items() if n >= 100]
    assert sorted(top) == ["leader_change_last_365d", "leader_tenure_days"], \
        f"fields surviving at scale changed: {survivors.most_common(6)}"


def test_inventory_publishes_the_decomposition(rows):
    """The document must carry the numbers, so a reader is not taking this on trust."""
    text = INVENTORY.read_text(encoding="utf-8")
    for value in ("11,089", "11,029", "10,150", "10,210", "2,682", "678,280", "648,822", "4.3%"):
        assert value in text, f"docs/audit/UNUSED_DATA_INVENTORY.md no longer states {value}"
