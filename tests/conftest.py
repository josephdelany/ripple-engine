"""Test bootstrap.

1. Put src/ on the import path so tests can import the engine modules.
2. CI GUARD: many tests are INTEGRATION tests that read the built data/oil.db. That DB is a derived
   artifact (gitignored -- rebuilt from free sources by repro.sh / src/refresh.py), so it is ABSENT in
   a fresh GitHub-Actions checkout. Rather than fake a database or let those tests error with "no such
   table", we SKIP the DB-dependent tests when no built DB is present, with a clear reason, and still
   run the deterministic logic tests as the CI gate. The full integration suite runs locally (where the
   DB exists) via `python3 src/acceptance.py`, and the daily workflow's own `refresh.py` + `heartbeat.py`
   prove the engine actually rebuilds and runs end-to-end. Nothing is faked; the skip is logged.
"""
import os
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
DB = ROOT / "data" / "oil.db"
# 3. The caged reader (src/reader.py) must never call the claude CLI from the test suite: model output is
#    replayed from recorded fixtures (tests/fixtures/reader); everything else takes the labelled regex fallback.
os.environ.setdefault("RIPPLE_READER", "off")

# Test files that run WITHOUT a built oil.db (pure logic / committed-artifact reads). Verified: these
# pass on a fresh checkout with no database. They are the deterministic CI gate.
DB_FREE_FILES = {
    "test_admission_rule.py", "test_corroboration.py", "test_edge_battery.py", "test_engine.py",
    "test_enrichment.py", "test_evaluate.py", "test_living_engine.py", "test_restore.py",
    "test_ripple_fetch.py", "test_ripple_lp.py",
    "test_sowhat.py", "test_status.py", "test_two_source.py", "test_ucdp.py", "test_validate.py",
    "test_kappa.py", "test_gdelt_search.py",
    "test_design_spec.py",           # DESIGN.md Amendment 1 A1.3: static rules, no browser and no DB, so CI enforces them
    "test_similarity.py",            # PATH Step 6: synthetic vectors + series only
    "test_read.py",                  # PATH Step 7: synthetic corpus; its one DB test carries its own skipif
    "test_walk.py",                  # PATH Step 8: synthetic corpus only
    "test_walk_baselines.py",        # Amendment B: synthetic corpus + a synthetic MID table
    "test_walk_recalibration.py",    # Amendment C: synthetic corpus only
    "test_candidates_pre1987.py",    # Brief B-3: reads the committed candidate sheet only
    "test_walk_archive.py",          # Amendment D: synthetic corpus, temp dirs
    "test_walk_filtration_audit.py", # Amendments F.1, G, H: synthetic corpus, monkeypatched leaks
    "test_walk_determinism.py",      # Amendment I: two synthetic runs
    "test_ruling1_retraction.py",    # Joe's Ruling 1: rows + committed artifacts; the DB branch self-guards
    "test_monthly_tier.py",          # B-12: synthetic monthly corpus; the real-corpus smoke carries its own skipif
    "test_diagnostic_hostile.py",    # Amendment K: reads the committed summary.json only
    "test_travel_irf.py",            # DESIGN.md Amendment 1: an ast scan of src/ + the committed
                                     # data/ripple/irf.json; its two Story tests carry their own skipif
}


def _db_ready():
    """True only if a POPULATED oil.db exists (has the events table with rows). A fresh sqlite connect
    would auto-create an empty file, so we check for real content, not just the file's existence."""
    if not DB.exists():
        return False
    try:
        return sqlite3.connect(DB).execute("SELECT COUNT(*) FROM events").fetchone()[0] > 0
    except sqlite3.Error:
        return False


def pytest_collection_modifyitems(config, items):
    if _db_ready():
        return                       # local / built DB -> run the whole suite unchanged
    skip = pytest.mark.skip(reason="needs a built data/oil.db (gitignored; rebuild via repro.sh / "
                            "src/refresh.py). Skipped where the DB isn't present (e.g. CI checkout); "
                            "runs locally via src/acceptance.py, and the daily refresh proves the engine runs.")
    n = 0
    for item in items:
        if "/tests/state/" in str(item.fspath).replace("\\", "/"):
            continue                 # PATH Step 2/3 loader tests use fixtures + a scratch DB: DB-free by construction
        if Path(str(item.fspath)).name not in DB_FREE_FILES:
            item.add_marker(skip); n += 1
    if n:
        print(f"\n[conftest] no built oil.db -> skipping {n} DB-integration test(s); "
              f"running the {len(items) - n} deterministic logic test(s) as the gate.")
