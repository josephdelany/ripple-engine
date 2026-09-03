"""Session F: the class audit is held to the database, not to itself.

`data/spine/CLASS_AUDIT.md` is a *hand* coding — a reading of each event's record, like the
codebook's own severity and surprise scales. A test cannot check a reading. What it can
check, and what these tests check, is that the reading is complete, that it is about the
events that actually exist, that its published totals are its own rows added up, and that
the impact figures in section 6 recompute from the sealed scores file. Anything that drifts
between the audit and `data/oil.db` is a failure here, not a footnote later.

Nothing in this file writes: it opens the DB read-only and reads two JSON/JSONL artefacts.
"""
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "spine" / "CLASS_AUDIT.md"
DB = ROOT / "data" / "oil.db"
SCORES = ROOT / "data" / "walk_forward" / "scores.jsonl"
MAPPING = ROOT / "OUTCOME_MAPPING.md"

GEO_CLASSES = ("infrastructure_attack", "chokepoint_disruption")
# The vocabulary is fixed by OUTCOME_MAPPING Amendment 3 A3.3 -- not by this test.
VOCAB = ("hostile", "hostile_unattributed", "ambiguous", "non_hostile")
NOT_SCORABLE = ("non_hostile", "ambiguous")     # A3.3: these return no_independent_outcome
RUN = "walk_20260902T210135Z"                   # the published run section 6 reports on

# a row of the section-3 tables: | `event_id` | date | **hostility** | level (basis, `rule`) | evidence |
ROW = re.compile(
    r"^\|\s*`(?P<eid>[a-z0-9_]+)`\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2})\s*\|\s*"
    r"\*\*(?P<hostility>\w+)\*\*\s*\|\s*(?P<level>\d|—)\s*\((?P<basis>[a-z]+),\s*`(?P<rule>[^`]+)`\)\s*\|"
    r"(?P<evidence>.*?)\|\s*$")


def _rows():
    out = {}
    for line in AUDIT.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            assert m["eid"] not in out, f"{m['eid']} appears twice in the audit"
            out[m["eid"]] = m.groupdict()
    return out


def _db():
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


@pytest.fixture(scope="module")
def rows():
    assert AUDIT.exists(), "the class audit must be published before it can be checked"
    r = _rows()
    assert r, "no event rows parsed out of CLASS_AUDIT.md -- the table format changed"
    return r


@pytest.fixture(scope="module")
def events():
    with _db() as conn:
        return {r["event_id"]: dict(r) for r in conn.execute(
            "select event_id, event_date, type from events where type in (?, ?)", GEO_CLASSES)}


def test_every_geo_event_is_coded_exactly_once(rows, events):
    """Completeness. An event that slips out of the audit is an event silently assumed hostile."""
    missing = sorted(set(events) - set(rows))
    extra = sorted(set(rows) - set(events))
    assert not missing, f"in the corpus, not in the audit: {missing}"
    assert not extra, f"in the audit, not in the corpus: {extra}"
    assert len(rows) == len(events) == 75, f"the two geo classes hold {len(events)} events"


def test_rows_match_the_database(rows, events):
    """Date and class come from the DB, never from the prose."""
    with _db() as conn:
        for eid, row in rows.items():
            assert row["date"] == events[eid]["event_date"], eid
            for f in ("level", "basis", "rule_fired"):
                x = conn.execute(
                    "select value, value_text from event_outcomes "
                    "where source='ies90' and field=? and event_id=?", (f, eid)).fetchone()
                got = (x[0] if x[0] is not None else x[1]) if x else None
                if f == "level":
                    want = None if row["level"] == "—" else int(row["level"])
                    assert (None if got is None else int(got)) == want, f"{eid} level"
                elif f == "basis":
                    assert (got or "uncovered") == row["basis"], f"{eid} basis"
                else:
                    assert got == row["rule"], f"{eid} rule_fired"


def test_coding_uses_only_the_registered_vocabulary(rows):
    """A5th value would be a definition change, and definition changes are amendments."""
    bad = {e: r["hostility"] for e, r in rows.items() if r["hostility"] not in VOCAB}
    assert not bad, f"values outside Amendment 3 A3.3: {bad}"
    for eid, r in rows.items():
        assert r["evidence"].strip(), f"{eid} is coded with no evidence"


def test_the_precondition_is_registered_before_the_audit_applies_it(rows):
    """SESSION_CHARTER 2.2: registered before computed. The audit may not invent its own rule."""
    t = MAPPING.read_text(encoding="utf-8")
    assert "Amendment 3" in t and "hostility precondition" in t
    for v in VOCAB:
        assert f"`{v}`" in t, f"{v} is used in the audit but not registered in OUTCOME_MAPPING"
    assert "no_independent_outcome" in t


def test_published_counts_are_the_rows_added_up(rows, events):
    """The tables in section 5 must be arithmetic on section 3, not a second opinion."""
    text = AUDIT.read_text(encoding="utf-8")
    by_class = {cl: Counter(rows[e]["hostility"] for e in events if events[e]["type"] == cl)
                for cl in GEO_CLASSES}
    for cl, cc in by_class.items():
        line = f"| `{cl}` | {cc['hostile']} | {cc['hostile_unattributed']} | " \
               f"{cc['ambiguous']} | {cc['non_hostile']} | {sum(cc.values())} |"
        assert line in text, f"class count row disagrees with the coded rows: expected {line}"
    dec = {}
    for e, r in rows.items():
        dec.setdefault(r["date"][:3] + "0s", Counter())[r["hostility"]] += 1
    for d, cc in dec.items():
        n = sum(cc.values())
        line = f"| {d} | {cc['hostile']} | {cc['hostile_unattributed']} | {cc['ambiguous']} | " \
               f"{cc['non_hostile']} | {n} | {cc['non_hostile'] / n:.0%} |"
        assert line in text, f"decade row disagrees with the coded rows: expected {line}"


def test_all_non_hostile_events_currently_carry_a_level(rows):
    """The defect itself, asserted so it cannot quietly disappear from the record: every event
    the precondition removes is scored today, so removal changes n."""
    nh = [e for e, r in rows.items() if r["hostility"] == "non_hostile"]
    assert len(nh) == 9, f"the audit found 9 non-hostile events, now {len(nh)}: {sorted(nh)}"
    uncovered = [e for e in nh if rows[e]["level"] == "—"]
    assert not uncovered, f"non-hostile but already no_independent_outcome: {uncovered}"


@pytest.mark.skipif(not SCORES.exists(), reason="walk scores not present")
def test_section_6_impact_recomputes_from_the_sealed_scores(rows):
    """The published-run figures are read out of B's scores file, never retyped by hand.
    This test recomputes them; it does not re-score anything and never writes."""
    scored = [json.loads(l) for l in SCORES.open(encoding="utf-8")]
    sel = [r for r in scored
           if r["run_id"] == RUN and r["tier"] == "daily" and r.get("burn_in_ok")
           and (r["scores"].get("engine") or {}).get("G")
           and (r["scores"].get("climatology") or {}).get("G")]
    assert len(sel) == 150, f"the section-6 set is 150 scored G reads, got {len(sel)}"
    lvl = lambda r: int(r["outcome"]["level"])
    share = lambda rs: (sum(1 for r in rs if lvl(r) == 0), len(rs))

    k, n = share(sel)
    assert (k, n) == (63, 150) and round(k / n * 100, 1) == 42.0

    affected = {e for e, r in rows.items() if r["hostility"] in NOT_SCORABLE}
    nh = {e for e, r in rows.items() if r["hostility"] == "non_hostile"}
    in150 = {r["event_id"] for r in sel}
    assert len(in150 & affected) == 9, sorted(in150 & affected)
    assert len(in150 & nh) == 6, sorted(in150 & nh)

    k1, n1 = share([r for r in sel if r["event_id"] not in nh])
    assert (k1, n1) == (59, 144) and round(k1 / n1 * 100, 1) == 41.0
    k2, n2 = share([r for r in sel if r["event_id"] not in affected])
    assert (k2, n2) == (56, 141) and round(k2 / n2 * 100, 1) == 39.7

    text = AUDIT.read_text(encoding="utf-8")
    for s in ("| **as published** | 150 | 63 | **42.0%** |",
              "| excluding the 6 `non_hostile` (the Amendment 3 rule as registered) | 144 | 59 | **41.0%** |",
              "| also excluding the 3 `ambiguous` | 141 | 56 | **39.7%** |"):
        assert s in text, f"section 6 table drifted from the scores file: {s}"


def test_the_audit_applies_nothing(rows):
    """Amendment 3 A3.5 and the brief: this session reports, it does not fix. If the
    precondition ever gets implemented, it lands in event_outcomes as B's work -- and this
    test is the tripwire that says the audit is no longer merely a reading."""
    with _db() as conn:
        n = conn.execute(
            "select count(*) from event_outcomes where source='ies90' and field='hostility'").fetchone()[0]
    assert n == 0, ("a hostility field exists in event_outcomes: Amendment 3 has been "
                    "implemented, so CLASS_AUDIT section 6 must be re-stated against the new run "
                    "rather than describing the pre-amendment one")
