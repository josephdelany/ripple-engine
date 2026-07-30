"""
_db.py -- one place to open data/oil.db safely under concurrency.

THE PROBLEM (the biggest reliability risk the audit found): one oil.db is written by the daily/hourly
runs while the backend (:5050) and the MCP server read it live. A bare sqlite3.connect(DB) with no
busy timeout throws `database is locked` the moment a writer and a reader overlap -- surfacing as a
spurious FAILED step, or (worse) a reader seeing half-written state.

THE FIX: every connection goes through connect() here, which sets a 30s busy_timeout (wait, don't
throw) and WAL journal mode (readers never block the writer and vice-versa). Small, boring, and it
removes a whole class of intermittent failures.
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"


def connect(db_path=DB, *, read_only=False, timeout=30.0):
    """Open oil.db with a busy timeout + WAL. Use read_only=True for the backend/MCP so a reader can
    never accidentally take a write lock."""
    if read_only:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=timeout)
    else:
        conn = sqlite3.connect(db_path, timeout=timeout)
    conn.execute("PRAGMA busy_timeout=30000")     # wait up to 30s for a lock instead of erroring
    if not read_only:
        try:
            conn.execute("PRAGMA journal_mode=WAL")   # readers don't block the writer
        except sqlite3.OperationalError:
            pass                                      # WAL not available (rare); busy_timeout still helps
    return conn
