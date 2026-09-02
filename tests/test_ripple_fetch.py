"""R2/R3(b) ripple loaders: parsers reproduce published values from REAL fixture files (verbatim
copies or head-slices of the files downloaded 2026-09-02 and recorded in RIPPLE_SOURCES.md);
the seed manifest is hash-consistent; the DB writer is append-only and stamps as_of/retrieved_at.
No fixture row is invented -- every number asserted below was read off the source file."""
import json
import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

import ripple_fetch as R

FIX = Path(__file__).resolve().parent / "fixtures" / "ripple"


def test_r2_eia_xls_wdistus1_first_and_last_rows_match_workbook():
    raw = (FIX / "WDISTUS1w.xls").read_bytes()
    df = R.parse_eia_xls(raw, "WDISTUS1")
    assert R.eia_title(raw).startswith("Weekly U.S. Ending Stocks of Distillate Fuel Oil")
    assert df.iloc[0].tolist() == ["1982-08-20", 149415]          # first row of Data 1
    assert df.iloc[-1]["date"] == "2026-08-28" and df.iloc[-1]["value"] == 104187
    assert len(df) == 2292
    with pytest.raises(ValueError):                               # wrong sourcekey is refused
        R.parse_eia_xls(raw, "WGTSTUS1")


def test_r2_pink_sheet_columns_units_and_1960m01_values():
    tables = R.parse_pink((FIX / "CMO-Historical-Data-Monthly_head.xlsx").read_bytes())
    for key in [s["key"] for s in R.SPECS.values() if s["kind"] == "pink"]:
        assert key in tables, key
    crude = tables["Crude oil, average"]
    assert crude.iloc[0].tolist() == ["1960-01-01", 1.6]
    assert tables["Urea"].iloc[0].tolist() == ["1960-01-01", 42.3]
    assert tables["Potassium chloride"].iloc[0].tolist() == ["1960-01-01", 28.5]   # '**' footnote stripped
    assert len(crude) == 24                                        # the head fixture keeps 24 months


def test_r2_kanzig_daily_pc_and_monthly_sheets():
    t = R.parse_kanzig((FIX / "oilSupplyNewsShocks_2025M12.xlsx").read_bytes())
    d = t["daily_pc"]
    assert d.iloc[0]["date"] == "1983-07-19" and abs(d.iloc[0]["value"] - 0.200943) < 1e-5
    assert d.iloc[-1]["date"] == "2025-12-01" and len(d) == 169
    m = t["monthly_shock"]
    assert m.iloc[0]["date"] == "1975-01-01" and abs(m.iloc[0]["value"] + 0.410498) < 1e-5
    assert t["monthly_surprise"].iloc[0]["value"] == 0.0            # no futures before 1983
    assert len(m) == 612


def test_r2_fred_csv_parser_drops_dots_and_keeps_iso_dates():
    df = R.parse_fred_csv((FIX / "fredgraph_DJFUELUSGULF_head.csv").read_bytes())
    assert df.iloc[0].tolist() == ["1990-04-02", 0.55]
    assert df["date"].str.match(r"^\d{4}-\d{2}-\d{2}$").all()


def test_r2_portwatch_feature_parser_handles_epoch_and_string_dates():
    feats = [{"attributes": {"date": 1546300800000, "n_tanker": 10, "n_total": 20, "capacity_tanker": 1.5}},
             {"attributes": {"date": "2019-01-02", "n_tanker": 11, "n_total": None, "capacity_tanker": 1.6}}]
    out = R.parse_portwatch_features(feats)
    assert out["n_tanker"]["date"].tolist() == ["2019-01-01", "2019-01-02"]
    assert out["n_total"]["date"].tolist() == ["2019-01-01"]        # None dropped, not zero-filled


def test_r3b_seed_manifest_is_hash_consistent_and_licence_gated():
    if not R.MANIFEST.exists():
        pytest.skip("no seeds yet (run src/ripple_fetch.py --refresh)")
    man = json.loads(R.MANIFEST.read_text())
    for sid, meta in man.items():
        assert R.SPECS[sid]["seed"], f"{sid} is refresh-only by licence and must not be seeded"
        path = R.SEED_DIR / f"{sid}.csv"
        assert path.exists() and R._sha256(path) == meta["sha256"]
        for k in ("source_url", "licence", "retrieved_at", "first", "last", "rows"):
            assert meta.get(k), (sid, k)
    for sid, s in R.SPECS.items():                                    # nothing refresh-only leaked
        if not s["seed"]:
            assert not (R.SEED_DIR / f"{sid}.csv").exists(), sid


def test_r3b_load_into_is_append_only_and_stamps_as_of():
    fd, path = tempfile.mkstemp(suffix=".db"); os.close(fd)
    conn = sqlite3.connect(path)
    conn.executescript("""
        CREATE TABLE entities (entity_id TEXT PRIMARY KEY, type TEXT, name TEXT, notes TEXT);
        CREATE TABLE series (series_id TEXT PRIMARY KEY, name TEXT, entity_id TEXT, unit TEXT,
                             frequency TEXT, source TEXT, source_url TEXT, notes TEXT);
        CREATE TABLE observations (series_id TEXT, obs_date TEXT, value REAL, as_of TEXT,
                                   retrieved_at TEXT, PRIMARY KEY (series_id, obs_date, as_of));""")
    try:
        df = R.parse_eia_xls((FIX / "WDISTUS1w.xls").read_bytes(), "WDISTUS1").head(5)
        n1 = R.load_into(conn, "eia.distillate_stocks", df, "2026-09-02T00:00:00+00:00")
        n2 = R.load_into(conn, "eia.distillate_stocks", df, "2026-09-03T00:00:00+00:00")
        assert n1 == 5 and n2 == 0                                   # second load adds nothing
        row = conn.execute("SELECT obs_date, value, as_of, retrieved_at FROM observations "
                           "ORDER BY obs_date LIMIT 1").fetchone()
        assert row == ("1982-08-20", 149415.0, "1982-08-20", "2026-09-02T00:00:00+00:00")
        assert conn.execute("SELECT COUNT(*) FROM observations WHERE as_of IS NULL").fetchone()[0] == 0
        assert conn.execute("SELECT entity_id FROM series").fetchone()[0] == "physical.us_stocks"
    finally:
        conn.close(); os.remove(path)


def test_c5_cftc_disagg_parser_tracks_contract_code_not_name():
    """The WTI contract was renamed (CRUDE OIL, LIGHT SWEET -> WTI-PHYSICAL) but code 067651 is stable;
    the fixture is the real 2026 file filtered to codes 067651 and 06765T."""
    raw = (FIX / "fut_disagg_txt_2026_wti_brent_rows.zip").read_bytes()
    df = R.parse_cftc_zip(raw, "disagg")
    assert set(df["code"]) == {"067651", "06765T"}
    assert "WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE" in set(df["Market_and_Exchange_Names"].str.strip())
    s = R.cftc_series([df], "067651", "M_Money_Positions_Long_All")
    assert s.iloc[0]["date"] == "2026-01-06" and s["date"].is_monotonic_increasing
    assert (s["value"] > 0).all() and len(s) == 34
    b = R.cftc_series([df], "06765T", "Open_Interest_All")
    assert len(b) == 34                                            # the NYMEX Brent proxy, weekly


def test_c5_cftc_legacy_parser_first_wti_report_1986_01_15():
    raw = (FIX / "deacot1986_wti_rows.zip").read_bytes()
    df = R.parse_cftc_zip(raw, "legacy")
    s = R.cftc_series([df], "067651", "Noncommercial Positions-Long (All)")
    assert s.iloc[0].tolist() == ["1986-01-15", 2560]
    oi = R.cftc_series([df], "067651", "Open Interest (All)")
    assert oi.iloc[0].tolist() == ["1986-01-15", 74334]
    assert R.cftc_series([df], "000000", "Open Interest (All)").empty     # unknown code -> empty, not zeros
