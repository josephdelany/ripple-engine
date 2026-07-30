"""
test_restore.py -- the backup-restore path actually works (round-trips a corrupt->restore).

This is what makes engine_status' `restore_tested` true rather than hoped: build a tiny DB, back it up
gzipped, corrupt it, and assert restore_db picks the good backup and integrity_check passes with the
rows intact. Run: python3 -m pytest -q tests/test_restore.py
"""

import gzip
import sqlite3
from pathlib import Path

import restore_db as R


def _make_db(path):
    c = sqlite3.connect(path)
    c.execute("CREATE TABLE t (id INTEGER, v TEXT)")
    c.executemany("INSERT INTO t VALUES (?,?)", [(1, "a"), (2, "b"), (3, "c")])
    c.commit(); c.close()


def test_r1_is_good_detects_corruption(tmp_path):
    good = tmp_path / "good.db"
    _make_db(good)
    assert R.is_good(good) is True
    bad = tmp_path / "bad.db"
    bad.write_bytes(b"this is not a sqlite file at all")
    assert R.is_good(bad) is False


def test_r2_restore_from_newest_good(tmp_path, monkeypatch):
    db = tmp_path / "oil.db"
    backups = tmp_path / "backups"
    backups.mkdir()
    monkeypatch.setattr(R, "DB", db)
    monkeypatch.setattr(R, "BACKUPS", backups)
    _make_db(db)
    # back it up gzipped (as integrity.py does), with an older name and a newer name
    for stamp in ("oil_20260101T000000.db.gz", "oil_20260201T000000.db.gz"):
        with open(db, "rb") as src, gzip.open(backups / stamp, "wb") as gz:
            gz.write(src.read())
    # now corrupt the live DB
    db.write_bytes(b"corrupted")
    assert R.is_good(db) is False
    res = R.restore()
    assert res["restored"] is True and res["from"] == "oil_20260201T000000.db.gz"   # newest chosen
    assert R.is_good(db) is True
    rows = sqlite3.connect(db).execute("SELECT COUNT(*) FROM t").fetchone()[0]
    assert rows == 3                                                                # data intact


def test_r3_skips_a_corrupt_backup(tmp_path, monkeypatch):
    db = tmp_path / "oil.db"
    backups = tmp_path / "backups"
    backups.mkdir()
    monkeypatch.setattr(R, "DB", db)
    monkeypatch.setattr(R, "BACKUPS", backups)
    _make_db(db)
    # newest backup is garbage; older one is good -> restore must fall back to the good one
    (backups / "oil_20260301T000000.db.gz").write_bytes(gzip.compress(b"not a db"))
    with open(db, "rb") as src, gzip.open(backups / "oil_20260101T000000.db.gz", "wb") as gz:
        gz.write(src.read())
    db.write_bytes(b"corrupted")
    res = R.restore()
    assert res["restored"] is True and res["from"] == "oil_20260101T000000.db.gz"
    assert R.is_good(db) is True
