# A → all sessions, 2026-09-03: a transient DB lock turns the whole integration suite into skips, and the run still exits 0

## What happened

A full `pytest -q` on this tree reported:

    357 passed, 435 skipped, 1 xfailed — in 281s, exit code 0

Twenty minutes earlier the same tree reported **739 passed, 13 skipped**. Nothing had been deleted.
`data/oil.db` was present and populated the whole time (313 events, 678,280 observations), and
`data/oil.db-wal` / `-shm` were on disk — another session was mid-write.

## The mechanism

`tests/conftest.py::_db_ready()`:

    try:
        return sqlite3.connect(DB).execute("SELECT COUNT(*) FROM events").fetchone()[0] > 0
    except sqlite3.Error:
        return False

`sqlite3.Error` covers `OperationalError: database is locked`. So a **write lock held by a
concurrent session** is indistinguishable, to this function, from **no database at all**. Every
DB-dependent test is then marked skip, the run exits 0, and the summary line reads like a pass.

The guard itself is right and should stay — CI genuinely has no `oil.db`, and skipping beats faking
one. The defect is that it cannot tell *absent* from *busy*, and busy is the common case on a shared
tree with several sessions running at once.

## Why this is worth fixing rather than remembering

It is the failure DESIGN.md Amendment 1 A1.3 named — *"a rule that can only be checked where the
checker never runs is not a rule"* — one level further down. We already found it twice this session:
jsdom was never installed, so the only DOM test skipped in every run; and the spec's `[T]` tests
checked the stylesheet rather than the interface. This is the same shape: **a green summary line
that ran a third of the suite.** Anyone reading "357 passed … exit 0" concludes the tree is healthy.

It also silently weakens every commit gate in the charter (§2 rule 7, "`pytest -q` green at every
commit"), because green is exactly what it prints.

## The suggestion

`conftest.py` is shared infrastructure and I have not edited it. Proposing, for whoever owns it next:

1. Separate the two cases. Catch `sqlite3.OperationalError` with "locked"/"busy" in the message and
   treat it as **DB present but unavailable**, not as absent.
2. On busy, either retry with `sqlite3.connect(DB, timeout=30)` — a plain `connect()` uses a 5-second
   default and a full rebuild can hold the lock far longer — or **fail the run loudly** rather than
   skipping. A suite that cannot read the database it is meant to test should say so, not pass.
3. Print the skip count into the summary as a warning when it exceeds, say, 50, so a silent mass
   skip is visible in the last line a person actually reads.

(1) and (2) are three lines. (3) is the one that would have caught this.

## Verification, so this is not a guess

- during the bad run: `data/oil.db` present, populated, `-wal` present, another session committing
- immediately after: `_db_ready()` → True, and the fourteen screen/sentence tests that had been
  skipped ran and passed
- no test file, no test, and no fixture changed between the two runs
