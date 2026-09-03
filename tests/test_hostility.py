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
MAPPING = ROOT / "docs" / "reference" / "OUTCOME_MAPPING.md"

GEO_CLASSES = ("infrastructure_attack", "chokepoint_disruption",
               "conflict_escalation", "sanctions")
# The vocabulary is fixed by OUTCOME_MAPPING Amendment 3 A3.3 -- not by this test.
VOCAB = ("hostile", "hostile_unattributed", "ambiguous", "non_hostile")
NOT_SCORABLE = ("non_hostile", "ambiguous")     # A3.3: these return no_independent_outcome
N_EVENTS = 187                                  # all four geopolitical classes

# a row of the section-3 tables:
# | `event_id` | date | **hostility**[ flags] | level (basis, `rule`) | evidence |
ROW = re.compile(
    r"^\|\s*`(?P<eid>[a-z0-9_]+)`\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2})\s*\|\s*"
    r"\*\*(?P<hostility>\w+)\*\*(?P<flags>[^|]*)\|\s*(?P<level>\d|—)\s*"
    r"\((?P<basis>[a-z]+),\s*`(?P<rule>[^`]+)`\)\s*\|(?P<evidence>.*?)\|\s*$")


def _published_run(scored):
    """Section 6 reports on the run the scores file currently holds, and the audit never
    names a run id. Session B re-runs the walk; a re-run must recompute this section, not
    quietly invalidate it. Latest run id wins (they sort by their embedded timestamp)."""
    return sorted({r["run_id"] for r in scored})[-1]


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
            "select event_id, event_date, type from events "
            f"where type in ({','.join('?' * len(GEO_CLASSES))})", GEO_CLASSES)}


def test_every_geo_event_is_coded_exactly_once(rows, events):
    """Completeness. An event that slips out of the audit is an event silently assumed hostile."""
    missing = sorted(set(events) - set(rows))
    extra = sorted(set(rows) - set(events))
    assert not missing, f"in the corpus, not in the audit: {missing}"
    assert not extra, f"in the audit, not in the corpus: {extra}"
    assert len(rows) == len(events) == N_EVENTS, \
        f"the four geopolitical classes hold {len(events)} events"


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
                    # A4.2: `basis` is stored only for a row that HAS a level. A no_independent_outcome row
                    # therefore has none, and the word the audit carries says which of the two reasons applies:
                    # `undated` (a source covers the window but cannot date a level in it) or `uncovered`
                    # (nothing covers it). Before Amendment 4 there was only the second, hence the old fallback.
                    rule = conn.execute(
                        "select value_text from event_outcomes where source='ies90' and field='rule_fired' "
                        "and event_id=?", (eid,)).fetchone()
                    default = "undated" if "UNDATED" in ((rule and rule[0]) or "") else "uncovered"
                    assert (got or default) == row["basis"], f"{eid} basis"
                else:
                    # rule_fired lists every rule that attained the level. Amendment 2 A2.3
                    # fixes the order *between* sources but not within one, and a re-run can
                    # flip two rules of the same source; the audit's claim is which rules
                    # fired, so compare as a set and let a genuine change still fail.
                    assert set((got or "").split(",")) == set(row["rule"].split(",")), \
                        f"{eid} rule_fired: db {got!r} vs audit {row['rule']!r}"


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
    assert "Amendment 3.2" in t, "the rules for conflict_escalation and sanctions are not registered"
    for v in VOCAB:
        assert f"`{v}`" in t, f"{v} is used in the audit but not registered in OUTCOME_MAPPING"
    assert "no_independent_outcome" in t
    # and the field itself is canon in the codebook, not only in the target document
    cb = (ROOT.parent / "EVENTS_CODEBOOK.md").read_text(encoding="utf-8")
    assert "`hostility`" in cb, "the hostility field is not registered in EVENTS_CODEBOOK"
    for v in ("hostile", "non-hostile", "ambiguous", "hostile-unattributed"):
        assert v in cb, f"{v} is not among the codebook's registered values"


def test_published_counts_are_the_rows_added_up(rows, events):
    """The tables in section 5 must be arithmetic on section 3, not a second opinion."""
    text = AUDIT.read_text(encoding="utf-8")
    def row(label, cc):
        # last column is the not-G-scorable count: ambiguous + non_hostile, the events
        # Amendment 3 removes from the target. It is arithmetic, not a second opinion.
        n = sum(cc.values()); out = cc["ambiguous"] + cc["non_hostile"]
        return (f"| {label} | {cc['hostile']} | {cc['hostile_unattributed']} | {cc['ambiguous']} | "
                f"{cc['non_hostile']} | {n} | {out} ({out / n:.0%}) |")

    for cl in GEO_CLASSES:
        cc = Counter(rows[e]["hostility"] for e in events if events[e]["type"] == cl)
        line = row(f"`{cl}`", cc)
        assert line in text, f"class count row disagrees with the coded rows: expected {line}"
    dec = {}
    for e, r in rows.items():
        dec.setdefault(r["date"][:3] + "0s", Counter())[r["hostility"]] += 1
    for d, cc in dec.items():
        line = row(d, cc)
        assert line in text, f"decade row disagrees with the coded rows: expected {line}"
    # the bolded totals rows carry ** markers, so they are checked as literals against the
    # coded rows rather than through row()
    total = Counter(r["hostility"] for r in rows.values())
    n = sum(total.values()); out = total["ambiguous"] + total["non_hostile"]
    for label in ("**all four**", "**all**"):
        line = (f"| {label} | **{total['hostile']}** | **{total['hostile_unattributed']}** | "
                f"**{total['ambiguous']}** | **{total['non_hostile']}** | **{n}** | "
                f"**{out} ({out / n:.0%})** |")
        assert line in text, f"totals row disagrees with the coded rows: expected {line}"


def test_all_non_hostile_events_currently_carry_a_level(rows):
    """The defect itself, asserted so it cannot quietly disappear from the record: every event
    the precondition removes is scored today, so removal changes n."""
    nh = [e for e, r in rows.items() if r["hostility"] == "non_hostile"]
    assert len(nh) == 20, f"the audit found 20 non-hostile events, now {len(nh)}: {sorted(nh)}"
    # Until 2026-09-03 every one of the 20 carried a level, so Amendment 3's removal changed n by 20.
    # OUTCOME_MAPPING Amendment 4 has since removed two of them by a different route -- their GED deaths were
    # already at the same level across the pre-window -- so Amendment 3's MARGINAL effect on the non-hostile
    # class is now 18, not 20. The pair is named rather than tolerated: a third one appearing means the two
    # rules are converging and the "orthogonal" claim in A4.9 needs re-checking, so this must fail.
    already = sorted(e for e in nh if rows[e]["level"] == "—")
    assert already == ["drc_cobalt_ban_2025", "druzhba_contamination_2019"], \
        f"non-hostile and already no_independent_outcome under Amendment 4: {already}"
    assert len(nh) - len(already) == 18


@pytest.mark.skipif(not SCORES.exists(), reason="walk scores not present")
def _section6(scored, rows):
    """The §6 set and every figure in it, DERIVED from the sealed scores of the published run.
    Nothing run-specific is written down here: when B publishes a new run these move with it,
    and the test's job is to check the document moved too. Before 2026-09-03 both sides of that
    comparison were hardcoded to the same constants, so the test could only catch a typo in the
    document -- never the case that actually happened, which was the run changing underneath it."""
    run = _published_run(scored)
    sel = [r for r in scored
           if r["run_id"] == run and r["tier"] == "daily" and r.get("burn_in_ok")
           and (r["scores"].get("engine") or {}).get("G")
           and (r["scores"].get("climatology") or {}).get("G")]
    nh = {e for e, r in rows.items() if r["hostility"] == "non_hostile"}
    amb = {e for e, r in rows.items() if r["hostility"] == "ambiguous"}
    hu = {e for e, r in rows.items() if r["hostility"] == "hostile_unattributed"}

    def share(drop):
        rs = [r for r in sel if r["event_id"] not in drop]
        k = sum(1 for r in rs if int(r["outcome"]["level"]) == 0)
        return len(rs), k, round(k / len(rs) * 100, 1)

    in_set = {r["event_id"] for r in sel}
    return {"run": run, "sel": sel, "n": len(sel), "in_set": in_set,
            "nh": in_set & nh, "amb": in_set & amb, "hu": in_set & hu,
            "published": share(set()), "no_nh": share(nh),
            "no_nh_amb": share(nh | amb), "strictest": share(nh | amb | hu)}


def test_section_6_impact_recomputes_from_the_sealed_scores(rows):
    """The published-run figures are read out of B's scores file, never retyped by hand.
    This test recomputes them and asserts the DOCUMENT carries what the recomputation gives;
    it does not re-score anything and never writes."""
    scored = [json.loads(l) for l in SCORES.open(encoding="utf-8")]
    s6 = _section6(scored, rows)
    text = AUDIT.read_text(encoding="utf-8")
    sec6 = text[text.index("## 6."):text.index("## 7.")]

    n, k, pct = s6["published"]
    assert f"| **as published** | {n} | {k} | **{pct}%** |" in sec6, \
        f"the as-published row must read {n} / {k} / {pct}% for run {s6['run']}"
    n1, k1, p1 = s6["no_nh"]
    assert (f"| excluding the {len(s6['nh'])} `non_hostile` (the Amendment 3 rule as registered) "
            f"| {n1} | {k1} | **{p1}%** |") in sec6
    n2, k2, p2 = s6["no_nh_amb"]
    assert f"| also excluding the {len(s6['amb'])} `ambiguous` | {n2} | {k2} | **{p2}%** |" in sec6
    n3, k3, p3 = s6["strictest"]
    assert (f"| also excluding the {len(s6['hu'])} `hostile_unattributed` (the strictest reading) "
            f"| {n3} | {k3} | **{p3}%** |") in sec6

    aff = len(s6["nh"]) + len(s6["amb"])
    assert f"**Affected: {aff} of the {s6['n']} reads ({round(100*aff/s6['n'],1)}%)**" in sec6
    assert (f"| **all** | **{s6['n']}** | **{len(s6['nh'])}** | **{len(s6['amb'])}** "
            f"| **{aff} ({round(100*aff/s6['n'])}%)** |") in sec6

    # the by-class table, also derived
    with _db() as conn:
        cls = dict(conn.execute("select event_id, type from events").fetchall())
    for c in GEO_CLASSES:
        ids = {r["event_id"] for r in s6["sel"] if cls.get(r["event_id"]) == c}
        a = len(ids & s6["nh"]) + len(ids & s6["amb"])
        row = (f"| `{c}` | {len(ids)} | {len(ids & s6['nh'])} | {len(ids & s6['amb'])} "
               f"| {a} ({round(100*a/len(ids)) if ids else 0}%) |")
        assert row in sec6, f"by-class row drifted from the scores file: {row}"

    # the run this section was computed from must be named in it
    assert s6["run"] in sec6, f"section 6 must name the run it was recomputed from ({s6['run']})"


@pytest.mark.skipif(not SCORES.exists(), reason="walk scores not present")
def test_section_6_set_matches_the_published_summary(rows):
    """The 150 is not this test's own construction: it must equal the n Session B publishes."""
    summary = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text(encoding="utf-8"))
    published = summary["tiers"]["daily"]["G"]["engine_vs"]["climatology"]["n"]
    scored = [json.loads(l) for l in SCORES.open(encoding="utf-8")]
    run = _published_run(scored)
    sel = [r for r in scored
           if r["run_id"] == run and r["tier"] == "daily" and r.get("burn_in_ok")
           and (r["scores"].get("engine") or {}).get("G")
           and (r["scores"].get("climatology") or {}).get("G")]
    assert len(sel) == published, (
        f"the audit's section-6 set ({len(sel)}) is not the published G n ({published}); "
        "section 6 must be re-stated against the run summary.json describes")


@pytest.mark.skipif(not SCORES.exists(), reason="walk scores not present")
def test_de_escalatory_rows_are_still_scorable_and_marked(rows):
    """Amendment 3.2(b): a sanction lifted or a deal signed stays G-scorable, and carries the
    marker so a de-escalatory act is never read as a hostile one. Excluding these would bias
    the corpus toward escalation by construction, which is the error the marker prevents."""
    de = {e for e, r in rows.items() if "de-escalatory" in r["flags"]}
    assert len(de) == 9, f"expected the 9 relief/settlement rows, got {sorted(de)}"
    assert all(rows[e]["hostility"] == "hostile" for e in de), \
        "a de-escalatory row that is not G-scorable defeats the purpose of Amendment 3.2(b)"


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


def test_ambiguous_is_recorded_as_terminal_not_as_a_to_do(rows):
    """Joe's ruling of 2026-09-02, registered as OUTCOME_MAPPING Amendment 3.3: ambiguous is
    a terminal value under the sourced-or-unknown rule. The risk this guards is a later
    session reading thirteen awkward values as a backlog and 'resolving' them -- which would
    settle a target definition by judgement, after the results are in view. The audit must
    say so where a reader meets the thirteen, and the amendment must exist."""
    mapping = MAPPING.read_text(encoding="utf-8")
    assert "Amendment 3.3" in mapping, "the ruling is not registered in OUTCOME_MAPPING"
    assert "terminal" in mapping and "not a pending decision" in mapping

    text = AUDIT.read_text(encoding="utf-8")
    sec4 = text[text.index("## 4."):text.index("## 5.")]
    assert "terminal state" in sec4 and "not a to-do" in sec4.lower(), \
        "section 4 must tell a reader meeting the thirteen that the value is terminal"
    assert len([e for e, r in rows.items() if r["hostility"] == "ambiguous"]) == 13


def test_the_ambiguous_diagnostic_is_published_both_ways():
    """Amendment 3.3 section 2: because the value is terminal, whether to count the ambiguous
    events can never be settled by evidence, so the level-0 share is published with AND
    without them. A single-figure report of this target is incomplete."""
    text = AUDIT.read_text(encoding="utf-8")
    sec6 = text[text.index("## 6."):text.index("## 7.")]
    # derived, not hardcoded: the requirement is that BOTH bounds are present for whatever run
    # is published, not that they equal any particular pair of numbers.
    scored = [json.loads(l) for l in SCORES.open(encoding="utf-8")]
    s6 = _section6(scored, _rows())
    n1, k1, p1 = s6["no_nh"]
    assert (f"| excluding the {len(s6['nh'])} `non_hostile` (the Amendment 3 rule as registered) "
            f"| {n1} | {k1} | **{p1}%** |") in sec6, \
        "the share under the registered rule (ambiguous still excluded from scoring) is missing"
    n2, k2, p2 = s6["no_nh_amb"]
    assert f"| also excluding the {len(s6['amb'])} `ambiguous` | {n2} | {k2} | **{p2}%** |" in sec6, \
        "the other bound (ambiguous also out of the denominator) is missing"
    n, k, pct = s6["published"]
    assert f"| **as published** | {n} | {k} | **{pct}%** |" in sec6
    assert "both with and without" in sec6, "section 6 must state the both-ways requirement"


def test_the_eleven_misplaced_events_keep_their_classes(events, rows):
    """Joe's ruling 2: the placements stay as coded, and the correct placement is a v3
    codebook item applied prospectively only. This test is the guard on 'prospectively only'
    -- it fails the moment someone re-classes one of the eleven, which would rewrite
    p_class_given_big and the analogue retrieval with the old numbers already in view."""
    MINING = ("escondida_strike_2011", "escondida_strike_2017", "escondida_strike_2024",
              "sa_platinum_strike_2014", "lasbambas_blockade_2019", "lasbambas_halt_2021",
              "cuajone_shutdown_2022", "peru_lasbambas_2022")
    BANS = ("indonesia_nickel_ban_2019", "indonesia_palm_ban_2022", "drc_cobalt_ban_2025")
    for e in MINING:
        assert events[e]["type"] == "conflict_escalation", f"{e} was re-classed"
    for e in BANS:
        assert events[e]["type"] == "sanctions", f"{e} was re-classed"
    # all eleven are non_hostile, which is what actually removes the harm
    for e in MINING + BANS:
        assert rows[e]["hostility"] == "non_hostile", f"{e} is no longer non_hostile"
    # and the prospective rule is registered in the codebook, not merely described in the audit
    cb = (ROOT.parent / "EVENTS_CODEBOOK.md").read_text(encoding="utf-8")
    assert "PROSPECTIVELY ONLY" in cb, "the v3 placement item is not registered"
    assert "do not move, now or ever" in cb
