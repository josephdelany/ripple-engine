"""Batch-2 loaders (PATH Step 2): each reproduces one published value offline and never leaves vintage/release null.
Licence-restricted loaders (SIPRI, Polity, CSP) run only when the local file is present; otherwise they
are SKIPPED with the placement instructions -- never faked. Stubs (EI, EIA International, GSDB, NYT, V-Dem,
DOTS) must stop with instructions while their input is absent."""
import os

import pytest

from _helpers import FIX, P, check_rows, live_or_skip, scratch_conn
import archigos
import csp
import eia_steo
import kilian
import polity
import sipri
import voeten
import wdi


# ----------------------------------------------------------------------------- Kilian / IGREA (WS-M12)

def test_m12_igrea_1968_01_is_minus_12_327322_and_knowable_two_months_on():
    rows = kilian.parse(FIX / "kilian" / "IGREA.csv", release="2026-09-02")
    check_rows(rows, kilian.FIELDS)
    r = [x for x in rows if x["obs_date"] == "1968-01-01"][0]
    assert r["value"] == -12.327322 and r["vintage"] == "1968-03-01" and r["retrospective"] == 1


# ----------------------------------------------------------------------------- Archigos (WS-A10/A11)

def test_a10_archigos_usa_leader_on_2001_09_11_is_gw_bush_since_2001_01_21():
    rows = archigos.parse(FIX / "archigos" / "archigos_4.1_slice.csv", release="2016-02-29")
    check_rows(rows, archigos.FIELDS)
    conn, db = scratch_conn()
    try:
        P.write(conn, rows)
        t = archigos.tenure_at(conn, "country.usa", "2001-09-11")
        assert t["leader"] == "G.W. Bush" and t["since"] == "2001-01-21" and t["tenure_days"] == 233 and t["change_last_365d"] == 1
        t2 = archigos.tenure_at(conn, "country.usa", "2003-09-11")
        assert t2["leader"] == "G.W. Bush" and t2["change_last_365d"] == 0
        assert archigos.tenure_at(conn, "country.usa", "1800-01-01") is None
    finally:
        conn.close(); os.remove(db)


# ----------------------------------------------------------------------------- Voeten (WS-D12)

def test_d12_usa_russia_ideal_point_distance_session_1():
    rows = voeten.parse(FIX / "voeten" / "ideal_points_slice.csv", release="2026-02-17")
    check_rows(rows, voeten.FIELDS)
    r = [x for x in rows if x["entity_id"] == "dyad.russia__usa" and x["obs_date"] == "1946-01-01"][0]
    assert r["value"] == round(abs(1.67635 - (-2.055966)), 6) and r["vintage"] == "1947-01-01"     # the two published points


# ----------------------------------------------------------------------------- WDI (WS-A12)

def test_a12_wdi_saudi_oil_rents_2000():
    rows = wdi.parse_one(FIX / "wdi" / "SAU_NY.GDP.PETR.RT.ZS.json", "country.saudi_arabia")
    check_rows(rows, wdi.FIELDS)
    r = [x for x in rows if x["obs_date"] == "2000-01-01"][0]
    assert round(r["value"], 4) == 41.6692 and r["vintage"] == "2001-07-01" and r["release"] == "2026-07-13"


# ----------------------------------------------------------------------------- EIA STEO (WS-P02)

def test_p02_steo_opec_surplus_jan_2022_and_no_forecast_months():
    rows = eia_steo.parse(FIX / "eia_steo" / "3dtab.csv", release="2026-08-07")
    check_rows(rows, eia_steo.FIELDS)
    r = [x for x in rows if x["entity_id"] == "opec" and x["obs_date"] == "2022-01-01"][0]
    assert r["value"] == 2.31 and r["vintage"] == "2022-03-01"
    assert max(x["obs_date"] for x in rows) < eia_steo.parse.forecast_date[:7] + "-01"       # nothing at or after the forecast month


# ----------------------------------------------------------------------------- licence-restricted: local file or skip

def _skip_unless(fn):
    try:
        return fn()
    except P.MissingInput as e:
        pytest.skip(str(e))


def test_a07_polity_saudi_2000_is_minus_10_durable_74():
    path = _skip_unless(polity.local_file)
    rows = polity.parse(path, release="2023-03-31")
    check_rows(rows, polity.FIELDS)
    by = {(r["entity_id"], r["field"], r["obs_date"]): r for r in rows}
    assert by[("country.saudi_arabia", "polity2", "2000-01-01")]["value"] == -10.0
    assert by[("country.saudi_arabia", "polity_durable", "2000-01-01")]["value"] == 74.0
    assert by[("country.saudi_arabia", "polity2", "2000-01-01")]["vintage"] == "2001-01-01"


def test_a14_csp_iraq_coups_1963_and_mepv_region_1991():
    paths = _skip_unless(csp.local_files)
    rows = csp.parse(paths, release="2022-01-07")
    check_rows(rows, csp.FIELDS)
    by = {(r["entity_id"], r["field"], r["obs_date"]): r["value"] for r in rows}
    assert by[("country.iraq", "coup_last_5y", "1964-01-01")] >= 2.0            # 1963: two successful coups in the file
    assert by[("country.iraq", "mepv_regional_war", "1991-01-01")] == 20.0        # nregion, as coded in MEPVv2018


def test_a04_sipri_saudi_2000_share_of_gdp_about_ten_percent():
    path = _skip_unless(sipri.local_file)
    rows = sipri.parse(path, release="2026-04-27")
    check_rows(rows, sipri.FIELDS)
    by = {(r["entity_id"], r["field"], r["obs_date"]): r for r in rows}
    s = by[("country.saudi_arabia", "milex_gdp_share_sipri", "2000-01-01")]
    assert 0.08 <= s["value"] <= 0.13 or 8 <= s["value"] <= 13                 # SIPRI reports ~10.6% (the sheet may store a fraction or a percent)
    assert by[("country.usa", "milex_sipri", "2000-01-01")]["value"] > 100000     # constant-2024 US$ m
    assert s["vintage"] == "2001-05-01"


# ----------------------------------------------------------------------------- stubs stop with instructions

@pytest.mark.parametrize("name", ["ei_review", "eia_intl", "gsdb", "nyt", "vdem", "dots"])
def test_stub_loaders_stop_with_instructions_when_input_is_absent(name):
    import importlib
    m = importlib.import_module(name)
    conn, db = scratch_conn()
    try:
        try:
            n = m.load(conn)
        except P.MissingInput as e:
            assert "data/state/local" in str(e) or "API_KEY" in str(e)
            pytest.skip(f"{name}: {str(e)[:120]}")
        assert n >= 0                                                             # input present on this machine: it loaded
        assert conn.execute("SELECT count(*) FROM state_panel WHERE vintage IS NULL OR release IS NULL").fetchone()[0] == 0
    finally:
        conn.close(); os.remove(db)


# ----------------------------------------------------------------------------- live smokes (cached download or network)

def test_live_batch2_point_in_time():
    live_or_skip(P.raw_path("kilian", "IGREA.csv"), P.raw_path("archigos", "Archigos_4.1_stata14.dta"), P.raw_path("voeten", "IdealpointestimatesAll_Jun2024.csv"))
    conn, db = scratch_conn()
    try:
        assert kilian.load(conn) > 600 and archigos.load(conn) > 500 and voeten.load(conn) > 10000
        k = P.value_at(conn, "world", "kilian_igrea", "2001-09-11")
        assert k and k["obs_date"] == "2001-07-01"                                 # August not yet knowable on 11 Sept under the m+2 rule
        assert archigos.tenure_at(conn, "country.saudi_arabia", "2001-09-11")["leader"]
        d = P.value_at(conn, "dyad.saudi_arabia__usa", "unga_ideal_point_distance", "2001-09-11")
        assert d and d["obs_date"] == "2000-01-01"
    finally:
        conn.close(); os.remove(db)
