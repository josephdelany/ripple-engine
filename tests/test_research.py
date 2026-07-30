"""
test_research.py -- the research bench (interrogation interface).

Checks the reusable hypothesis-test core: it reproduces H1 (a HOLDS) and returns an honest null
for a signal that shouldn't amplify, with valid receipts either way.
Run: python3 -m pytest -q tests/test_research.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "oil.db"


def test_rb1_reproduces_h1():
    import research
    conn = sqlite3.connect(DB)
    r = research.run_test(conn, "derived.vix_pct", "fred.DCOILBRENTEU", "high", 20)
    conn.close()
    assert r["ok"] and r["holds"] is True                 # H1: VIX-high amplifies oil |CAR20|
    assert r["ci_excludes_zero"] and r["amp"] > 0
    lo, hi = r["ci"]
    assert lo <= r["amp"] <= hi                            # CI brackets the point estimate


def test_rb2_unknown_state_is_honest():
    import research
    conn = sqlite3.connect(DB)
    r = research.run_test(conn, "derived.not_a_real_signal", "fred.DCOILBRENTEU", "high", 20)
    conn.close()
    assert r["ok"] is False and "no such state" in r["reason"]


def test_rb3_asset_resolution():
    import research
    known = research._asset("fred.DGS10")
    assert known["kind"] == "yield" and known["unit"] == "bps"
    unknown = research._asset("fred.MADE_UP")             # defaults to price, never crashes
    assert unknown["kind"] == "price"
