"""
Tests for the Session E spine tools: src/spine_audit.py, src/spine_check.py,
src/spine_patch.py.

Everything here runs on fixtures written into a tmp_path, or on an in-memory sqlite
database. No test touches data/oil.db, data/events.csv or data/dossiers -- the audit's
own read of the real database is exercised only through its pure helper functions.
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import spine_audit as A        # noqa: E402
import spine_check as C        # noqa: E402
import spine_patch as P        # noqa: E402
import spine_apply as AP      # noqa: E402


# --------------------------------------------------------------------------- audit

def test_spine_audit_domain_strips_www_so_two_pages_of_one_site_are_one_source():
    assert A.domain_of("https://www.eia.gov/foo") == "eia.gov"
    assert A.domain_of("https://eia.gov/bar") == "eia.gov"
    assert A.domain_of("not a url") is None
    assert A.domain_of(None) is None


def test_spine_audit_flags_a_bare_site_root_as_not_a_document():
    assert A.is_generic_root("https://www.eia.gov") is True
    assert A.is_generic_root("https://www.eia.gov/") is True
    assert A.is_generic_root("https://www.eia.gov/petroleum/weekly") is False


def test_spine_audit_classifies_corpus_sources_as_self_referential_not_external():
    assert A.classify_source_slot("https://history.state.gov/d1") == "external"
    assert A.classify_source_slot("corpus:density") == "corpus"
    assert A.classify_source_slot("corpus:observed()") == "corpus"
    assert A.classify_source_slot(None) == "null"
    assert A.classify_source_slot("") == "null"
    assert A.classify_source_slot("unknown") == "null"
    # free text is not a checkable source
    assert A.classify_source_slot("Joe said so") == "null"


def test_spine_audit_does_not_count_an_encyclopaedia_as_a_citable_source(tmp_path):
    """The codebook requires a primary or major-wire source; an encyclopaedia is neither."""
    db = tmp_path / "w.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        "CREATE TABLE events (event_id TEXT PRIMARY KEY, event_date TEXT, "
        " date_precision TEXT, type TEXT, title TEXT, description TEXT, severity INT,"
        " confidence TEXT, source_url TEXT, sr_json TEXT);"
        "CREATE TABLE event_entities (event_id TEXT, entity_id TEXT, role TEXT);"
        "CREATE TABLE event_outcomes (event_id TEXT, source TEXT, field TEXT, value REAL);"
    )
    conn.execute(
        "INSERT INTO events VALUES ('w','1998-03-30','day','opec_decision','T','d',3,"
        "'medium','https://en.wikipedia.org/wiki/1998_world_oil_market_chronology',NULL)")
    conn.commit(); conn.close()
    ro = sqlite3.connect(f"file:{db}?mode=ro", uri=True); ro.row_factory = sqlite3.Row
    rows = A.load_events(ro); ro.close()
    r = rows[0]
    assert r["source_url_tertiary"] is True
    assert r["n_source_domains"] == 1        # it is a domain
    assert r["n_citable_domains"] == 0       # but not a citable one
    _, payload = A.build_report(rows)
    assert payload["overall"]["tertiary_source_url"] == 1
    assert payload["overall"]["zero_citable_domains"] == 1


def test_spine_audit_counts_placeholders_and_domains_on_a_synthetic_corpus(tmp_path):
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        "CREATE TABLE events (event_id TEXT PRIMARY KEY, event_date TEXT, "
        " date_precision TEXT, type TEXT, title TEXT, description TEXT, severity INT,"
        " confidence TEXT, source_url TEXT, sr_json TEXT);"
        "CREATE TABLE event_entities (event_id TEXT, entity_id TEXT, role TEXT);"
        "CREATE TABLE event_outcomes (event_id TEXT, source TEXT, field TEXT, value REAL);"
    )
    sr = json.dumps({"sources": {"a": "https://history.state.gov/d1",
                                 "b": "corpus:density", "c": None}})
    conn.executemany(
        "INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)",
        [("stub", "1973-10-17", "day", "sanctions", "T",
          "T [deep-history tier 1970-1989; events-only]", None, "medium",
          "https://www.eia.gov", sr),
         ("good", "1987-07-24", "day", "chokepoint_disruption", "T2",
          "x" * 800, 3, "high", "https://www.usni.org/magazines/proceedings/a", sr)],
    )
    conn.execute("INSERT INTO event_entities VALUES ('good','country.iran','actor')")
    conn.execute("INSERT INTO event_outcomes VALUES ('good','ies90','level',2)")
    conn.commit()
    conn.close()

    ro = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    ro.row_factory = sqlite3.Row
    rows = A.load_events(ro)
    ro.close()
    by = {r["event_id"]: r for r in rows}

    assert by["stub"]["placeholder"] is True
    assert by["stub"]["placeholder_marker"] == "deep-history tier"
    assert by["stub"]["source_url_generic_root"] is True
    assert by["good"]["placeholder"] is False
    # eia.gov + history.state.gov (from sr_json) = 2 for the stub
    assert by["stub"]["n_source_domains"] == 2
    assert by["stub"]["sr_slots_external"] == 1
    assert by["stub"]["sr_slots_corpus"] == 1
    assert by["stub"]["sr_slots_null"] == 1
    assert by["good"]["ies90"] == "level"
    assert by["stub"]["ies90"] == "uncovered"
    assert by["good"]["n_entities"] == 1

    md, payload = A.build_report(rows)
    assert payload["n_events"] == 2
    assert payload["overall"]["placeholder"] == 1
    assert "# Spine audit" in md


# --------------------------------------------------------------------------- check

COMPLETE = """# Test event   test_1973 · 1973-10-17 · day · sanctions

## Sources
| # | role | publisher | title | doc date | URL | retrieved_at | quote |
|---|---|---|---|---|---|---|---|
| S1 | primary | US Dept of State (FRUS) | Minutes of Washington Special Actions Group Meeting | 1973-10-19 | https://history.state.gov/historicaldocuments/frus1969-76v36/d221 | 2026-09-02T16:20:00Z | "SUBJECT: Middle East. PARTICIPANTS: Chairman: Henry A. Kissinger." |
| S2 | secondary | NBER | Historical Oil Shocks | 2011-02-01 | https://www.nber.org/papers/w16790 | 2026-09-02T16:24:00Z | "On October 17, the Arab members of the Organization of Petroleum Exporting Countries announced an embargo" |

## Narrative
%s [S1] %s [S2]

## Knowable at
1973-10-17, the announcement date [S2].

## Entities
country.saudi_arabia:actor [S1]

## Class
sanctions -- the codebook says "Sanctions imposed, tightened, or lifted on a producer" [S2].

## Not known at the time
The eventual magnitude of the cutback [S2].

## Proposed field changes
| field | current | proposed | source |
|---|---|---|---|
| description | T [deep-history tier] | A sourced narrative | [S1] |
| severity | NULL | 5 | [S2] |

## Status
complete
""" % (" ".join(["word"] * 100), " ".join(["word"] * 40))


def _write(tmp_path, name, text):
    d = tmp_path / "dossiers"
    d.mkdir(exist_ok=True)
    p = d / f"{name}.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_spine_check_passes_a_dossier_that_meets_the_registration(tmp_path):
    p = _write(tmp_path, "test_1973", COMPLETE)
    r = C.check_one(p)
    assert r["verdict"] == "PASS", r["problems"]
    assert r["claims"] == "complete"
    assert r["primary"] == [1]
    assert set(r["domains"]) == {"history.state.gov", "nber.org"}
    assert 120 <= r["narrative_words"] <= 250


def test_spine_check_fails_a_dossier_that_claims_complete_on_one_domain(tmp_path):
    # both sources on the same publisher: the two-source rule is not met
    text = COMPLETE.replace("https://www.nber.org/papers/w16790",
                            "https://history.state.gov/historicaldocuments/frus1969-76v36/d222")
    p = _write(tmp_path, "one_domain", text)
    r = C.check_one(p)
    assert r["verdict"] == "FAIL"
    assert any("2 distinct source domains" in x for x in r["problems"])


def test_spine_check_fails_when_complete_is_claimed_without_a_primary_source(tmp_path):
    text = COMPLETE.replace("| S1 | primary |", "| S1 | secondary |")
    p = _write(tmp_path, "no_primary", text)
    r = C.check_one(p)
    assert r["verdict"] == "FAIL"
    assert any("primary" in x for x in r["problems"])


def test_spine_check_accepts_an_honest_partial(tmp_path):
    text = COMPLETE.replace("https://www.nber.org/papers/w16790",
                            "https://history.state.gov/historicaldocuments/frus1969-76v36/d222")
    text = text.replace("## Status\ncomplete", "## Status\npartial -- fails (a)")
    p = _write(tmp_path, "honest_partial", text)
    r = C.check_one(p)
    assert r["verdict"] == "PARTIAL-OK"
    assert r["claims"] == "partial"


def test_spine_check_rejects_a_wikipedia_citation(tmp_path):
    text = COMPLETE.replace("https://www.nber.org/papers/w16790",
                            "https://en.wikipedia.org/wiki/1973_oil_crisis")
    p = _write(tmp_path, "wiki", text)
    r = C.check_one(p)
    assert r["verdict"] == "FAIL"
    assert any("wikipedia" in x for x in r["problems"])


def test_spine_check_catches_a_narrative_citing_a_source_that_does_not_exist(tmp_path):
    text = COMPLETE.replace("[S2]\n\n## Knowable", "[S7]\n\n## Knowable")
    p = _write(tmp_path, "dangling", text)
    r = C.check_one(p)
    assert r["verdict"] == "FAIL"
    assert any("not listed" in x for x in r["problems"])


def test_spine_check_catches_a_narrative_outside_120_to_250_words(tmp_path):
    text = COMPLETE.replace(" ".join(["word"] * 100), "too short")
    p = _write(tmp_path, "short", text)
    r = C.check_one(p)
    assert r["verdict"] == "FAIL"
    assert any("120-250" in x for x in r["problems"])


# --------------------------------------------------------------------------- patch

def test_spine_patch_parses_a_table_of_proposed_changes():
    block = (
        "| field | current | proposed | source |\n"
        "|---|---|---|---|\n"
        "| description | old text | \"a new sourced narrative long enough to be real prose\" | [S1] |\n"
        "| severity | NULL | 5 | [S2] |\n"
        "| date_precision | day | month | [S1] |\n"
    )
    rows = P.parse_changes(block)
    got = {r["field"]: r for r in rows}
    assert got["severity"]["dossier_current"] is None  # NULL -> None
    assert got["description"]["source"] == "[S1]"
    assert P.coerce("severity", got["severity"]["raw_proposed"])[:2] == (5, None)
    assert P.coerce("date_precision", got["date_precision"]["raw_proposed"])[0] == "month"


def test_spine_patch_parses_the_bullet_form_too():
    rows = P.parse_changes("- severity: NULL -> 4 [S1]\n- date_precision: day -> month [S2]\n")
    got = {r["field"]: P.coerce(r["field"], r["raw_proposed"])[0] for r in rows}
    assert got == {"severity": 4, "date_precision": "month"}


def test_spine_patch_extracts_a_value_from_a_cell_that_also_carries_reasoning():
    """The dossiers write '5 -- because X'. The column must get 5, not the sentence."""
    val, why, ok = P.coerce("severity", "5 \u2014 \"Systemic; a top producer\" because Saudi output fell")
    assert (val, ok) is not None and val == 5 and ok is True
    assert why and "Systemic" in why


def test_spine_patch_reads_the_proposed_n_phrasing_the_dossiers_use():
    assert P.coerce("severity", "Proposed 4 -- major producer affected")[0] == 4
    assert P.coerce("surprise", "Propose 2 because it was telegraphed")[0] == 2


def test_spine_patch_marks_a_proposal_it_cannot_reduce_as_needing_joe():
    val, why, ok = P.coerce("severity", "Not a number, just an argument about the scale")
    assert ok is False          # kept in the patch, flagged, never silently written


def test_spine_patch_treats_unchanged_and_leave_null_as_no_change():
    assert P.coerce("date_precision", "day (unchanged)")[2] is None
    assert P.coerce("severity", "Propose leaving NULL. Reasoning: no source")[2] is None
    assert P.coerce("surprise", "Not proposed. No day-before source found.")[2] is None


def test_spine_patch_never_lifts_a_date_out_of_prose_that_declines_to_propose_it():
    """Regression: a dossier wrote 'not changed here, but flagged: [S2] dates the start
    to 1991-01-16'. The parser proposed 1991-01-16. It must not."""
    cell = ("not changed here, but flagged: [S2] dates the physical start of well "
            "destruction to 1991-01-16, seven days before the February 22 date")
    assert P.coerce("event_date", cell)[2] is None      # recognised as 'no change'
    # and even without the no-change phrase, a date buried in prose is not a proposal
    assert P.coerce("event_date", "[S2] dates the start to 1991-01-16 which is earlier")[2] is False
    assert P.coerce("event_date", "1991-01-16 -- the day the fires began")[0] == "1991-01-16"


def test_spine_patch_only_takes_a_quoted_description_that_opens_the_cell():
    buried = ('strip the "DRAFT coding" language once Joe reviews this dossier; '
              'substantively the current description is accurate enough to keep')
    # "...accurate enough to keep" is a no-change (None). The invariant that matters is
    # that commentary is NEVER returned as a value to write (ok is never True).
    assert P.coerce("description", buried)[2] is not True
    # commentary carrying no no-change phrase is flagged for Joe instead
    commentary = ('the $20M/$40M split in the current description is not supported by the '
                  'retrieved text of the Act and should be re-examined')
    assert P.coerce("description", commentary)[2] is False
    leading = '"Iraqi forces invaded Kuwait on 2 August 1990, putting Kuwaiti and Iraqi crude at risk."'
    assert P.coerce("description", leading)[0].startswith("Iraqi forces invaded")


def test_spine_patch_treats_keep_and_retain_as_no_change():
    assert P.coerce("severity", "keep -- the evidence supports the existing code")[2] is None
    assert P.coerce("surprise", "supported")[2] is False   # not a value; flagged for Joe


def test_spine_patch_rejects_an_out_of_range_severity():
    assert P.coerce("severity", "9 -- off the codebook scale")[2] is False
    assert P.coerce("confidence", "extremely high")[2] is False


def test_spine_patch_never_proposes_a_field_outside_the_allowed_set():
    rows = P.parse_changes("| sr_actor | x | country.iran | [S1] |\n"
                           "| event_id | a | b | [S1] |\n"
                           "| severity | NULL | 2 | [S1] |\n")
    assert [r["field"] for r in rows] == ["severity"]


def test_spine_patch_module_never_opens_the_database_for_writing():
    src = (ROOT / "src" / "spine_patch.py").read_text(encoding="utf-8")
    assert "mode=ro" in src
    for forbidden in ("INSERT", "UPDATE ", "DELETE", "commit()"):
        assert forbidden not in src, f"spine_patch.py must not contain {forbidden}"


def test_spine_audit_module_never_opens_the_database_for_writing():
    src = (ROOT / "src" / "spine_audit.py").read_text(encoding="utf-8")
    assert "mode=ro" in src
    for forbidden in ("INSERT", "UPDATE ", "DELETE", "commit()"):
        assert forbidden not in src, f"spine_audit.py must not contain {forbidden}"


# --------------------------------------------------------------------------- apply

def test_spine_apply_validates_against_the_codebook_ranges():
    assert AP.validate("severity", 5) == 5
    assert AP.validate("date_precision", "month") == "month"
    assert AP.validate("confidence", "high") == "high"
    assert AP.validate("event_date", "1988-08-08") == "1988-08-08"
    for bad in [("severity", 9), ("severity", "5"), ("surprise", 0),
                ("date_precision", "daily"), ("confidence", "very high"),
                ("event_date", "8 August 1988"), ("type", "price_collapse"),
                ("source_url", "ftp://x"), ("title", "  ")]:
        with pytest.raises(AP.Refused):
            AP.validate(*bad)


def test_spine_apply_refuses_to_write_an_encyclopaedia_url():
    """The whole point of the repair: a patch may never put Wikipedia back."""
    with pytest.raises(AP.Refused):
        AP.validate("source_url", "https://en.wikipedia.org/wiki/1998_world_oil_market_chronology")
    assert AP.validate("source_url", "https://history.state.gov/d1").startswith("https://")


def test_spine_apply_refuses_a_field_outside_the_whitelist():
    for f in ("sr_actor", "event_id", "sr_json"):
        assert f not in AP.PATCHABLE
        with pytest.raises(AP.Refused):
            AP.validate(f, "x")


def test_spine_apply_is_the_only_session_e_module_that_writes():
    """spine_patch and spine_audit must stay read-only; the writer is one small file."""
    for name in ("spine_patch", "spine_audit", "spine_check"):
        src = (ROOT / "src" / f"{name}.py").read_text(encoding="utf-8")
        assert "UPDATE " not in src and "INSERT" not in src, f"{name}.py must not write"
    writer = (ROOT / "src" / "spine_apply.py").read_text(encoding="utf-8")
    assert "UPDATE events SET" in writer
    # and it must gate on Joe
    assert 'approved_by != "joe"' in writer
