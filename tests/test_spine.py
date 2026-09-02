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
        "| description | old text | a new sourced narrative | [S1] |\n"
        "| severity | NULL | 5 | [S2] |\n"
        "| date_precision | day | month | [S1] |\n"
    )
    rows = P.parse_changes(block)
    got = {r["field"]: r for r in rows}
    assert got["severity"]["proposed"] == 5          # numeric coercion
    assert got["severity"]["dossier_current"] is None  # NULL -> None
    assert got["date_precision"]["proposed"] == "month"
    assert got["description"]["source"] == "[S1]"


def test_spine_patch_parses_the_bullet_form_too():
    rows = P.parse_changes("- severity: NULL -> 4 [S1]\n- title: old -> new [S2]\n")
    got = {r["field"]: r["proposed"] for r in rows}
    assert got == {"severity": 4, "title": "new"}


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
