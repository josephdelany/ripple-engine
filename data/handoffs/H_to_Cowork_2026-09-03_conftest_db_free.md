# H → whoever next touches `tests/conftest.py`, 2026-09-03: four new test files should be DB-free

`tests/conftest.py` is shared and currently carries another session's uncommitted changes, so I have
not edited it — committing it would drag that work in with mine (charter §1). This is the request.

## Ask

Add these four basenames to `DB_FREE_FILES`:

    "test_ledger_backfill.py",     # session H: committed ledger rows + manifest; the two DB tests
                                   # in it carry their own skipif on data/oil.db
    "test_audit_reader.py",        # session H: committed gold, blind sheet and codings only
    "test_uncheckable_audit.py",   # session H: committed claims + the audit JSON only
    "test_challenge_loop.py",      # session H: the committed challenge log; its live-corpus tests
                                   # take a `conn` fixture that skips itself when the DB is absent

## Why it matters

Verified: all four pass on a checkout with no `data/oil.db` — every DB-dependent test in them either
carries `@pytest.mark.skipif(not DB.exists())` or takes the self-skipping `conn` fixture. Until they
are in the list they are skipped wholesale in CI, so the invariants they hold are not gating
anything. Those invariants include the two I would least like to lose silently:

- `test_H2_every_backfill_quote_appears_verbatim_in_the_archived_page` — the fabrication guard,
  re-run offline against the committed page receipts. It is the check that says the 98 backfill
  claims are quotes and not inventions.
- `test_L1_log_claims_persists_entities` — the regression test for defect L-1. It fails on the
  pre-fix `ledger.py` (verified by reverting the fix in a scratch copy and re-running), which is the
  failing test the charter requires before a shared-file fix.

Nothing else in conftest needs to change.
