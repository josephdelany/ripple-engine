"""Tests for src/situation_vintage.py (Session G, G-3).

Every test names the clause of docs/g/G3_REGISTRATION.md it covers, so a failing test says
which registered rule broke. Nothing here touches oil.db, events or situation_state; the
fixtures are strings written in the test.
"""
import datetime as dt
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import situation_vintage as SV  # noqa: E402


# ------------------------------------------------------------------ (e.1) parsing a Doc. date cell

@pytest.mark.parametrize("cell,expect", [
    ("Washington, October 7, 1973, 6:06–7:06 p.m.", "1973-10-07"),   # form 1, place prefix, time suffix
    ("filed July 24, 1987, dateline \"Aboard the USS Kidd\"", "1987-07-24"),
    ("4 December 1997", "1997-12-04"),                               # form 2
    ("February 2011", "2011-02-28"),                                 # form 3 -> END of the month
    ("May 1990", "1990-05-31"),
    ("1998 (writing dated \"at the time of writing\")", "1998-12-31"),  # form 4 -> END of the year
])
def test_e1_doc_date_forms(cell, expect):
    assert SV.parse_doc_date(cell)[0] == expect


def test_e1_latest_date_within_a_cell_is_taken():
    """(e.1) 'Signed May 6, 1995; published May 9, 1995' is established as a whole only on 9 May."""
    assert SV.parse_doc_date("Signed May 6, 1995; published May 9, 1995")[0] == "1995-05-09"
    assert SV.parse_doc_date("September 30, 1997 / November 12, 1997")[0] == "1997-11-12"


@pytest.mark.parametrize("cell", [
    "n/a (compiled)",
    "undated editorial note, positioned in the volume's record for 1980",
    "c. 2022 (retrospective; event described occurred 1997)",
    "archival description, collection covers 1985-1986 OPEC material",
    "case study text, undated; resolution quoted is dated August 6 1990",
])
def test_e1_unparseable_cells_yield_no_date(cell):
    """(e.1) a cell carrying an unparseable token is not parsed AT ALL, even where it holds a year."""
    assert SV.parse_doc_date(cell)[0] is None


def test_A1_1_circa_token_does_not_match_abbreviations():
    """(A1.1) 'c.' as a bare substring matched 'U.S.' and 'D.C.' and rejected a fully dated primary."""
    got, form = SV.parse_doc_date("January 23, 1980, House Chamber, U.S. Capitol, Washington, D.C.")
    assert got == "1980-01-23", form
    assert SV.parse_doc_date("c. 2022 (retrospective)")[0] is None       # circa still rejected


# ------------------------------------------------------------------ fixtures for the receipt clauses

def _doss(entities, sources):
    """A dossier dict of the shape read_dossier returns."""
    src = {}
    for mk, cell in sources.items():
        iso, form = SV.parse_doc_date(cell)
        src[mk] = {"marker": f"S{mk}", "role": "primary", "publisher": "p",
                   "doc_date_cell": cell, "doc_date": iso, "parse": form, "url": "http://x"}
    ents = []
    for text in entities:
        m = SV._LEAD_ENTITY.match(text)
        ents.append({"entity_id": m.group(1), "text": text,
                     "markers": sorted({mm.group(1) for mm in SV._MARKER.finditer(text)})})
    return {"sources": src, "entities": ents, "declared_knowable_at": None}


def test_e2_receipt_takes_the_earliest_cited_document():
    d = _doss(["- `country.usa` — actor — confirmed [S1][S2]."],
              {"1": "August 5, 1996", "2": "August 6, 1996"})
    ka, det = SV.receipt(d, "country.usa", "1996-08-05", role_words=("actor",))
    assert ka == "1996-08-05" and det["earliest_doc_date"] == "1996-08-05"


def test_e6_knowable_at_is_never_earlier_than_the_event_date():
    """(e.6) a document dated before the event cannot establish who acted on the day; it sets the floor."""
    d = _doss(["- `country.usa` — actor — confirmed [S1]."], {"1": "January 14, 1980"})
    ka, det = SV.receipt(d, "country.usa", "1980-01-23", role_words=("actor",))
    assert ka == "1980-01-23" and det["clamped"] is True


def test_e7_a_later_document_makes_the_field_later_not_the_assertion_earlier():
    """(e.7) the receipt is the document, not the dossier's own asserted knowable_at."""
    d = _doss(["- `country.egypt` — actor — confirmed [S1]."], {"1": "Washington, October 7, 1973"})
    ka, _ = SV.receipt(d, "country.egypt", "1973-10-06", role_words=("actor",))
    assert ka == "1973-10-07"                       # NOT the dossier's asserted 1973-10-06


def test_e2_iv_a_negated_bullet_yields_no_receipt():
    d = _doss(["- `country.iran` — currently coded as `actor`, but no source retrieved this session "
               "names Iran [S1]."], {"1": "August 5, 1996"})
    ka, det = SV.receipt(d, "country.iran", "1996-08-05", role_words=("actor",))
    assert ka is None and "e.2 iv" in det["reject"]


def test_e2_iii_a_bullet_with_no_marker_yields_no_receipt():
    d = _doss(["- `country.iran` — actor — per the existing `event_entities` rows."], {"1": "May 6, 1995"})
    ka, det = SV.receipt(d, "country.iran", "1995-05-06", role_words=("actor",))
    assert ka is None and "e.2 iii" in det["reject"]


def test_e2_a_retrospective_only_dossier_yields_a_date_after_the_event():
    """A dossier resting on 2011 and 2015 scholarship dates the field to 2011, so it still drops at t."""
    d = _doss(["- `country.saudi_arabia` — actor — the party making the shift [S1][S2]."],
              {"1": "May 2015", "2": "February 2011"})
    ka, _ = SV.receipt(d, "country.saudi_arabia", "1986-01-01", role_words=("actor",))
    assert ka == "2011-02-28" > "1986-01-01"


def test_A1_2_the_role_word_selects_among_two_bullets_for_one_entity():
    """(A1.2) four dossiers give an entity two bullets, one per role."""
    d = _doss(["- `country.iran` — actor — confirmed [S1].",
               "- `country.iran` — target — as currently recorded; reported as a gap, not changed."],
              {"1": "November 4, 1979"})
    assert SV.bullet_for(d, "country.iran", ("actor",))["text"].startswith("- `country.iran` — actor")
    assert "target" in SV.bullet_for(d, "country.iran", ("target",))["text"][:40]
    ka, det = SV.receipt(d, "country.iran", "1979-11-04", role_words=("target",))
    assert ka is None and "e.2 iv" in det["reject"]              # the TARGET bullet's own reason


def test_A1_2_without_a_role_word_every_bullet_must_pass():
    """(A1.2) tempo and asset_role have no role word, so a second negated bullet rejects the entity."""
    d = _doss(["- `country.iran` — actor — confirmed [S1].",
               "- `country.iran` — target — reported as a gap, not silently changed."],
              {"1": "November 4, 1979"})
    ka, det = SV.receipt(d, "country.iran", "1979-11-04", require_role=False)
    assert ka is None and "A1.2" in det["reject"]


def test_A1_2_without_a_role_word_the_latest_bullet_governs():
    d = _doss(["- `chokepoint.hormuz` — location — named [S1].",
               "- `chokepoint.hormuz` — also discussed [S2]."],
              {"1": "July 22, 1987", "2": "September 1, 1987"})
    ka, _ = SV.receipt(d, "chokepoint.hormuz", "1987-07-22", require_role=False)
    assert ka == "1987-09-01"                       # max of the per-bullet earliest dates, not min


# ------------------------------------------------------------------ (e.8) conflict_scope

def test_e8_conflict_scope_window_is_symmetric_and_reaches_120_days_forward():
    """(e.8) situation_record._conflict_scope counts abs(days) <= 120, so half its input postdates t.
    The constant here must match that code; if that code changes, this test is the alarm."""
    src = (ROOT / "src" / "situation_record.py").read_text()
    assert "abs(_days(e[\"event_date\"], o[\"event_date\"])) <= 120" in src
    assert SV.CONFLICT_SCOPE_WINDOW_DAYS == 120


def test_e8_conflict_scope_can_never_be_knowable_at_t():
    """(e.8) whatever the sourcing, event_date + 120 > event_date, so the field always drops at t."""
    out = json.loads((ROOT / "docs" / "g" / "SITUATION_VINTAGE.json").read_text())
    cs = [r for r in out["rows"] if r["field"] == "conflict_scope"]
    assert cs, "no conflict_scope rows in the published output"
    for r in cs:
        assert r["after_rule"].startswith("e.8")
        assert r["after"] == (dt.date.fromisoformat(r["event_date"]) + dt.timedelta(days=120)).isoformat()
        assert r["after"] > r["event_date"]
    assert out["by_field"]["conflict_scope"]["kept_after"] == 0


# ------------------------------------------------------------------ the published run

def test_g3_before_column_reproduces_session_As_published_file():
    """The BEFORE column is recomputed from Amendment A's rules, not copied, and must agree with
    data/state/situation_knowable.json. This is the check that makes the AFTER number meaningful."""
    out = json.loads((ROOT / "docs" / "g" / "SITUATION_VINTAGE.json").read_text())
    b = out["baseline_check"]
    assert b["checked"] and b["agrees"], json.dumps(b, indent=1)


def test_g3_rule_e_never_invents_a_date_without_a_receipt():
    """Every value dated by rule (e) carries a receipt naming the documents it rests on."""
    out = json.loads((ROOT / "docs" / "g" / "SITUATION_VINTAGE.json").read_text())
    for r in out["rows"]:
        if r["after_rule"].startswith(("e.2", "e.3", "e.4")):
            det = r["detail"] or {}
            assert det.get("earliest_doc_date") or det.get("per_member"), r
            assert r["has_dossier"], r


def test_g3_the_output_never_writes_to_events_or_situation_state():
    """SPINE_REGISTRATION §5. The script opens the database read-only and issues no write."""
    src = (ROOT / "src" / "situation_vintage.py").read_text()
    assert "mode=ro" in src
    for bad in ("INSERT", "UPDATE ", "DELETE", "CREATE TABLE", "conn.commit"):
        assert bad not in src, f"situation_vintage.py contains {bad!r}"
