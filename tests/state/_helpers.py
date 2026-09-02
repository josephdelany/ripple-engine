"""Shared helpers for the state-panel loader tests (PATH Step 2).

Every loader test: (1) reproduces a published value OFFLINE from a fixture sliced from the real file
(tests/fixtures/state/<source>/), (2) asserts vintage and release are never null, (3) runs a live smoke
against the cached raw download when it exists (or the network does) -- skipped, never faked, otherwise.
"""
import os
import socket
import sqlite3
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "state"))
import panel as P  # noqa: E402

FIX = ROOT / "tests" / "fixtures" / "state"


def scratch_conn():
    db = tempfile.mktemp(suffix=".db")
    return P.connect(db), db


def check_rows(rows, fields):
    """Amendment 1: every row carries a non-null vintage AND release; fields registered; obs_date ISO."""
    assert rows, "loader produced no rows"
    cb = P.codebook()
    for r in rows:
        assert r.get("vintage") and r.get("release"), r
        assert len(str(r["vintage"])) == 10 and len(str(r["release"])) == 10, r
        assert r["field"] in cb and r["field"] in fields, r["field"]
        assert len(str(r["obs_date"])) == 10, r["obs_date"]
        assert r.get("value") is not None or r.get("value_text") is not None, r


def network():
    try:
        socket.create_connection(("ucdp.uu.se", 443), timeout=5).close()
        return True
    except OSError:
        return False


def live_or_skip(*raw_files):
    """The live smoke runs against the cached download; if it is absent and there is no network, skip."""
    missing = [p for p in raw_files if not Path(p).exists()]
    if missing and (os.environ.get("RIPPLE_OFFLINE") or not network()):
        pytest.skip(f"no cached download and no network: {[str(m) for m in missing]}")
