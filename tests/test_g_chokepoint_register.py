"""Tests for src/g_chokepoint_register.py -- PHYSICAL_EXPOSURE §2 T2 (G-7 §§4-6)."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import g_chokepoint_register as C  # noqa: E402
import g_vintage as V  # noqa: E402

OUT = ROOT / "docs" / "g" / "CHOKEPOINT_T2.json"
REG = C.build_register()


# ------------------------------------------------------------------ §4 the register

def test_G7_4_every_entry_is_stamped_and_carries_its_verbatim_quote():
    for key, entries in REG.items():
        for e in entries:
            assert V.is_stamped(e), key
            assert e["quote"].strip(), f"{key} @ {e['published']} has no quote"
            assert e["source_url"].startswith("https://www.eia.gov/"), key


def test_G7_4_the_four_release_dates_are_the_retrieved_ones():
    pubs = sorted({e["published"] for entries in REG.values() for e in entries})
    assert pubs == ["2011-03-02", "2014-12-01", "2017-08-04", "2025-06-16"]


def test_G7_4_published_is_the_release_date_never_the_reference_year():
    """§3's trap: a register's knowable_at is its publication date, not its reference year."""
    for entries in REG.values():
        for e in entries:
            ref = e["reference_period"]
            if ref.isdigit():
                assert int(e["published"][:4]) > int(ref), (
                    f"{e['source_id']} claims to be knowable in its own reference year")


def test_G7_4_cape_of_good_hope_is_a_gap_in_every_release_never_a_zero():
    entries = REG["cape_of_good_hope"]
    assert entries and all(e["value"] is None for e in entries)
    _s, v = V.latest_value(REG, "cape_of_good_hope", "2026-01-01")
    assert v is None


def test_G7_4_a_chokepoint_a_release_omits_is_absent_from_it_not_carried_forward():
    """Malacca is quantified in 2011 and 2014 and in neither 2017 nor 2025. The 2017 release must
    not silently inherit the 2014 figure as its own."""
    mal = {e["published"] for e in REG["malacca"]}
    assert mal == {"2011-03-02", "2014-12-01"}
    s, v = V.latest_value(REG, "malacca", "2020-01-01")
    assert v == 15.2 and s["published"] == "2014-12-01"      # read forward, but stamped with ITS date


def test_G7_4_1_no_denominator_before_the_first_release_that_states_one():
    """§4.1: never back-derived from a rounded share. The 2011 release states no world figure."""
    assert V.latest(REG, "world_seaborne", "2013-01-01") is None
    s, v = V.latest_value(REG, "world_seaborne", "2015-01-01")
    assert v == 56.5 and s["published"] == "2014-12-01"


# ------------------------------------------------------------------ §2 T2 construction

@pytest.mark.skipif(not OUT.exists(), reason="T2 not built in this tree")
def test_G7_3_the_published_run_passes_its_filtration_audit():
    o = json.loads(OUT.read_text())
    a = o["filtration_audit"]
    assert a["asserted"] is True and a["voided"] is False and a["violations"] == 0
    assert a["terms_checked"] > 0


@pytest.mark.skipif(not OUT.exists(), reason="T2 not built in this tree")
def test_G7_2_a_null_T2_always_says_why_and_is_never_zero():
    o = json.loads(OUT.read_text())
    for r in o["t2"]:
        if r["T2_share"] is None:
            assert r["null_reason"], r["event_id"]
        else:
            assert r["T2_share"] > 0
        assert r["zeroed_nulls"] is False


@pytest.mark.skipif(not OUT.exists(), reason="T2 not built in this tree")
def test_G7_5_the_coverage_finding_is_published():
    """T2 is a 25-event variable in a 313-event corpus. If the corpus changes this must move."""
    o = json.loads(OUT.read_text())
    c = o["coverage"]
    assert c["n_events"] == 313
    assert c["first_release"] == "2011-03-02"
    assert c["n_t2_constructible"] == 25
    assert c["n_before_first_release"] == 82
    assert set(c["never_named"]) == {"cape_of_good_hope", "malacca", "panama", "turkish_straits"}


@pytest.mark.skipif(not OUT.exists(), reason="T2 not built in this tree")
def test_G7_events_before_the_first_release_carry_no_T2_term():
    o = json.loads(OUT.read_text())
    for r in o["t2"]:
        if r["event_date"] < "2011-03-02":
            assert r["T2_share"] is None and r["flow_mbd"] is None


@pytest.mark.skipif(not OUT.exists(), reason="T2 not built in this tree")
def test_G7_the_2011_egypt_revolution_is_null_by_five_weeks():
    """The rule biting where it is not obvious: 2011-01-25 precedes the first release by five weeks."""
    o = json.loads(OUT.read_text())
    rows = [r for r in o["t2"] if r["event_id"] == "egypt_revolution_2011"]
    assert rows and all(r["T2_share"] is None for r in rows)
    assert all("no release published on or before t" in r["null_reason"] for r in rows)


# ------------------------------------------------------------------ §6 the cross-check

@pytest.mark.skipif(not OUT.exists(), reason="T2 not built in this tree")
def test_G7_6_crosscheck_excludes_cape_by_registration_and_says_so():
    o = json.loads(OUT.read_text())
    for c in o["crosscheck"]:
        assert "cape_of_good_hope" not in c["chokepoints"]
        assert c["excluded_from_rank"] == ["cape_of_good_hope"]


@pytest.mark.skipif(not OUT.exists(), reason="T2 not built in this tree")
def test_G7_6_crosscheck_obeys_the_portwatch_publication_lag():
    """§6: PortWatch's own ~1-week tail lag is applied, so the cross-check obeys the same filtration."""
    o = json.loads(OUT.read_text())
    assert C.PW_LAG_DAYS == 7
    for c in o["crosscheck"]:
        hi = c["meta"]["window"][1]
        assert hi < c["date"], (c["date"], hi)


def test_G7_writes_no_table():
    src = (ROOT / "src" / "g_chokepoint_register.py").read_text()
    assert "mode=ro" in src
    for bad in ("INSERT", "UPDATE ", "DELETE", "CREATE TABLE", "conn.commit"):
        assert bad not in src, f"g_chokepoint_register.py contains {bad!r}"
