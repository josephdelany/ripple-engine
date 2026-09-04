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
import time
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
    "test_figures_paper.py",         # Session I: the paper figures -- committed JSON/Markdown only
    # Session H, the claim loop. All four read committed artifacts (data/ledger/**, data/reader_eval/**);
    # every DB-dependent test in them carries its own skipif or takes a self-skipping `conn` fixture.
    # Verified to pass with no oil.db present. They are in the CI gate because two of their checks are
    # the ones least safe to lose silently: the fabrication guard (every backfill quote must appear
    # verbatim in its archived page) and the L-1 regression test (log_claims must persist entities).
    "test_ledger_backfill.py",
    "test_audit_reader.py",
    "test_uncheckable_audit.py",
    "test_challenge_loop.py",
    "test_antecedent.py",            # Amendments 9/9.1: the antecedent gate; its corpus tests self-skip
    "test_big_moves_variants.py",    # BIG_MOVES Amendment 4: registered vs as-computed clustering. The
                                     # series tests take a self-skipping fixture; the published-file tests
                                     # read committed data/big_moves/*.json and run without a DB.
    # The retraction guard: reads data/*.json + docs/PAPER_DRAFT.md, needs no database. It is in the CI
    # gate deliberately -- it exists to stop a retracted claim being carried live, and a guard that only
    # runs where the DB happens to exist would not have caught any of the six instances it was written for.
    "test_retraction_guard.py",
    "test_citation_guard.py",        # Session I: the citation guard over the five published documents --
                                     # committed JSON/Markdown only. In the CI gate on purpose: it is the
                                     # test that goes red when a re-run supersedes the numbers in the prose.
    "test_structural_component_ablation.py",
    "test_paper_field_composition.py",
    "test_public_claim_guard.py",
    "test_verify_submission.py",
    "test_structural_surface_experiment.py",
    "test_structural_surface_demo.py",
    "test_bundle_provenance.py",
    "test_doc_status_guard.py",
}


class DatabaseBusy(Exception):
    """The DB is present and populated but locked by another process.

    This is NOT the same condition as 'no DB here' and must never be silently converted into one.
    Session A, 2026-09-03: a concurrent write lock made _db_ready() return False, which skipped
    435 of 792 tests and still exited 0 printing a pass. Three silent-skip failures surfaced the
    same day (jsdom never installed; [T] tests reading the stylesheet; this). A suite that reports
    green while not running is worse than a red one, because charter S2.7 gates commits on green.
    """


def _db_ready(_retries=5, _wait=2.0):
    """True only if a POPULATED oil.db exists (has the events table with rows).

    A fresh sqlite connect would auto-create an empty file, so we check for real content rather
    than the file's existence. Absent -> False (a legitimate skip). LOCKED -> retry, then raise
    DatabaseBusy: a busy database is a reason to wait or fail, never a reason to report a pass.
    """
    if not DB.exists():
        return False
    last = None
    for attempt in range(_retries):
        try:
            con = sqlite3.connect(DB, timeout=_wait)
            try:
                return con.execute("SELECT COUNT(*) FROM events").fetchone()[0] > 0
            finally:
                con.close()
        except sqlite3.OperationalError as e:
            last = e
            if "locked" not in str(e).lower() and "busy" not in str(e).lower():
                return False          # genuinely malformed / unreadable -> treat as absent
            time.sleep(_wait)
        except sqlite3.DatabaseError:
            return False              # corrupt or not a database -> absent
    raise DatabaseBusy(
        f"data/oil.db is present but locked after {_retries} attempts ({last}). "
        "Refusing to skip the DB-integration suite and report a pass: another session is holding "
        "a write lock. Wait for it to finish and re-run.")


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
    config._ripple_skipped_for_db = n


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """A run that skipped most of itself may not exit green silently.

    The DB-free gate is a real, intended mode (CI checkout with no oil.db). What is not intended is
    a run that skips the majority of the suite for any *other* reason and still prints a pass. This
    prints the ratio on every run so 'green' can be read honestly, and fails the run when skips
    exceed the floor without the DB-free gate being the cause.
    """
    n_db = getattr(config, "_ripple_skipped_for_db", 0)
    stats = terminalreporter.stats
    passed, skipped = len(stats.get("passed", [])), len(stats.get("skipped", []))
    total = passed + skipped + len(stats.get("failed", [])) + len(stats.get("error", []))
    if not total:
        return
    unexplained = skipped - n_db
    terminalreporter.write_sep("-", f"ripple: {passed} passed, {skipped} skipped "
                                   f"({n_db} for the DB-free gate, {unexplained} otherwise) of {total}")
    if unexplained > total * 0.25:
        terminalreporter.write_sep("!", f"REFUSING TO REPORT GREEN: {unexplained} tests skipped for "
                                       f"reasons other than the DB-free gate ({unexplained/total:.0%} "
                                       f"of the suite). A silently-skipped suite is not a passing one.")
        terminalreporter._session.exitstatus = 1
