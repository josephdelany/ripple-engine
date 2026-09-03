"""OUTCOME_MAPPING.md Amendment 4.2: the label audit display is blind, and stays blind.

kappa is an inter-rater statistic. Before this amendment `audit_ies90.show()` printed
"ENGINE: level 3 (war) ... rule WAR.inter.pair" immediately above the prompt that asks Joe
for his level, so the number measured agreement with something he had just been shown.

These tests render every row of the LIVE sheet through the same function the tool uses and
fail if any engine-assigned level survives anywhere in it. That matters more than the
redaction patterns themselves: all 26 of the leaks inside `code_and_rule` came from strings
built in `src/state/ies90.py`, so the next one will be added there, by someone who has never
read `audit_ies90.py`. This is the test that stops it reaching Joe.

An absence-only test is passable by showing nothing at all, so the presence tests below are
load-bearing: the record must still be on the screen, or the audit is unanswerable.

Read-only. Renders in memory; writes nothing, answers nothing.
"""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import audit_ies90 as A  # noqa: E402


@pytest.fixture(scope="module")
def sheet():
    if not A.SHEET.exists():
        pytest.skip("run python3 src/state/ies90.py first")
    ev = A.load_sheet(A.SHEET)
    assert ev, "the sheet parsed to nothing"
    return ev


@pytest.fixture(scope="module")
def rendered(sheet):
    """{event_id: the exact text Joe sees before he is asked for his level}."""
    return {eid: "\n".join(A.render_row(item, i, len(sheet)))
            for i, (eid, item) in enumerate(sheet.items(), 1)}


# --------------------------------------------------------------- A4.2.2: nothing engine-derived reaches the screen

# every registered rule id (OUTCOME_MAPPING A2.3 + A4.2), each of which states a level on its face
RULE_ID = re.compile(r"\b(?:MIDI|WAR|ICB|MID|GED|NONE|UNCOVERED|UNDATED)\.[A-Za-z_]+(?:\.[A-Za-z0-9_]+)?\b")
LEVEL_CLAIM = re.compile(
    r"(?ix)"
    r" ENGINE:"                      # the anchoring line itself
    r"| ->\s*level\s*\d"             # per-source level_contributed
    r"| \blevel\s*[0-3]\b"           # any bare "level 2"
    r"| \bdelta_level\b"             # A4.4's diagnostic ladder
    r"| \bno\s+level\b"              # "(no level)"
    r"| \basserted from coverage\b"
    r"| \bundated-for-W\b"
    r"| \balready at level\b"
)


def test_A4_2_2_no_engine_level_appears_anywhere_before_the_prompt(rendered):
    bad = {eid: LEVEL_CLAIM.findall(t) for eid, t in rendered.items() if LEVEL_CLAIM.search(t)}
    assert not bad, f"the engine's level leaked into the blind display: {bad}"


def test_A4_2_2_no_registered_rule_id_appears_before_the_prompt(rendered):
    """GED.location.ge250 IS the statement "level 3"; NONE.covered IS "level 0"."""
    bad = {eid: RULE_ID.findall(t) for eid, t in rendered.items() if RULE_ID.search(t)}
    assert not bad, f"a rule id leaked into the blind display: {bad}"


def test_A4_2_2_the_event_id_is_not_shown(rendered):
    """`israel_hamas_war_2023` telegraphs the answer; session H measured that on 9 of 30 rows."""
    leaked = [eid for eid, t in rendered.items() if eid in t]
    assert not leaked, f"the event_id is on screen for: {leaked}"


def test_A4_2_2_the_engine_columns_are_not_reachable_from_the_render(sheet, rendered):
    """Belt and braces: the literal values of the withheld columns must not appear either."""
    bad = []
    for eid, item in sheet.items():
        e, t = item["event"], rendered[eid]
        # `ies90_level_meaning` is deliberately NOT checked as a literal: its values are the ordinary English words
        # "none / threat or display of force / use of force / war", and "war" is in the name of half the COW records
        # ("COW inter-state war 211 Gulf War") and in event titles. Matching it flags the record, not a leak. The
        # meaning string was only ever printed as part of the "ENGINE:" line, which LEVEL_CLAIM above forbids
        # outright and which no longer exists in the module at all (asserted in the reveal test).
        for col in ("rule_fired",):
            v = (e.get(col) or "").strip()
            if v and v in t:
                bad.append((eid, col, v))
        for s in item["sources"]:
            v = (s.get("record_rule") or "").strip()
            if v and v in t:
                bad.append((eid, "record_rule", v))
    assert not bad, bad


# --------------------------------------------------------------- the redaction must not blind the record itself

def test_A4_2_3_the_source_record_survives_redaction(sheet, rendered):
    """An absence-only test passes trivially if the screen is blank. The coded fields Joe reasons from -- and the
    dates, and the record identifier -- must still be there."""
    for eid, item in sheet.items():
        t = rendered[eid]
        assert item["event"]["title"] in t, eid
        assert item["event"]["event_date"] in t, eid
        for s in item["sources"]:
            if s["record"].strip():
                assert s["record"].strip()[:24] in t, (eid, "record missing", s["record"])
            if s["record_dates"].strip():
                assert s["record_dates"].strip() in t, (eid, "dates missing")


def test_A4_2_3_redaction_keeps_the_coded_fields_and_drops_only_the_mapping():
    """The exact strings the sheet actually carries, from src/state/ies90.py."""
    cases = [
        ("hihost 5 settlmnt 2 (ongoing at d, force undated in W (no level))",
         ["hihost 5", "settlmnt 2", "ongoing at d"], ["no level"]),
        ("viol 4 forout 5 (ongoing at d, violence undated in W (no level))",
         ["viol 4", "forout 5"], ["no level"]),
        ("hihost 4 settlmnt 3 (starts in W, ends after (onset dated -> 1; hihost 4 is the undated peak))",
         ["hihost 4", "settlmnt 3", "starts in W"], ["-> 1"]),
        ("best 258 in W (B [1996-09-11..1996-12-09] 70; on d 0; delta +188 -> delta_level 2; one-sided/non-state 0)",
         ["best 258 in W", "70", "on d 0", "delta +188"], ["delta_level"]),
        ("war spell covers all of B -> undated-for-W (A4.2, no level)",
         ["war spell covers all of B"], ["no level", "undated-for-W"]),
        ("level 0 asserted from coverage", ["no record in W"], ["level 0", "asserted from coverage"]),
    ]
    for raw, keep, drop in cases:
        got = A.redact(raw)
        for k in keep:
            assert k in got, f"redaction ate a source field: {k!r} gone from {got!r}"
        for d in drop:
            assert d not in got, f"redaction left the mapping: {d!r} still in {got!r}"


# --------------------------------------------------------------- A4.2.4 / A4.2.5: the reveal and superseded rows

def test_A4_2_4_the_reveal_is_off_by_default_and_never_renders_inside_the_row():
    src = (ROOT / "src" / "audit_ies90.py").read_text()
    assert "def run(sheet=SHEET, out_path=OUT, ask=input, echo=print, reveal=False)" in src, \
        "blind must be the default signature"
    body = src[src.index("def run("):src.index("\ndef status(")]
    assert body.index("ans = ask_row(ask)") < body.index("engine_answer_lines"), \
        "the engine's answer must not be rendered before the answer is taken"
    assert "ENGINE: level" not in src.split("def engine_answer_lines")[0], \
        "the unblinded renderer must not survive anywhere else in the module"


def test_A4_2_5_a_superseded_row_never_enters_kappa_or_n_done():
    rows = [{"event_id": "a", "joe_level": 3, "engine_level": 3, "hostility": "hostile",
             "superseded": True, "superseded_reason": "answered under the unblinded display"},
            {"event_id": "b", "joe_level": 2, "engine_level": 2, "hostility": "hostile"}]
    k, n, _ = A.kappa(rows)
    assert n == 1, "the superseded row was counted"
    out = {"rows": rows}
    A.finalize(out, n_rows=30)
    assert out["n_done"] == 1 and out["passed"] is False


def test_A4_2_5_joes_contaminated_row_is_marked_and_not_deleted():
    """The evidence that the audit once ran contaminated must survive in the file."""
    import json
    p = ROOT / "data" / "audits" / "outcome_audit.json"
    if not p.exists():
        pytest.skip("no audit file yet")
    o = json.loads(p.read_text())
    row = next((r for r in o["rows"] if r["event_id"] == "iran_iraq_war_1980"), None)
    if row is None:
        pytest.skip("the pre-Amendment-4.2 row is not in this file")
    assert row.get("superseded") is True
    assert "Amendment 4.2" in (row.get("superseded_by") or "")
    assert row["joe_level"] == 3 and row["answered_at"].startswith("2026-09-03")   # his answer itself is untouched
    assert o["n_done"] == 0 and o["kappa"] is None and o["passed"] is False
