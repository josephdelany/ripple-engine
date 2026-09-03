# Flag to B, 2026-09-03: the live walk files hold two runs at once — not fixed by A, they are yours

`data/walk_forward/reads.jsonl` and `scores.jsonl` each currently hold **two complete runs**, 313 rows apiece:

| run | in reads.jsonl | in scores.jsonl |
|---|---|---|
| `walk_20260902T210135Z` | 313 | 313 |
| `walk_20260903T003422Z` | 313 | 313 |

`data/walk_forward/summary.json` publishes **`walk_20260902T210135Z`**, the older of the two.

The desk keys rows by `event_id` and the last row wins, so `/api/walk/read` serves **003422Z** while the summary
beside it is **210135Z**. The two disagree about which run the reader is looking at. Nothing is wrong with either
run's rows; the archive step simply has not run since 003422Z was written, so it was never moved into
`data/walk_forward/runs/`.

Not touched by session A: `walk.py`, the archive step and these files are yours, and your next re-run lands on top
of this anyway. It only needs to end with **exactly one live run** — archive 210135Z (or publish 003422Z's summary)
so the served read and the published summary name the same run.

Unrelated and already handled on A's side: `/api/walk/read` and `/api/walk/list` now fall back to
`data/walk_forward/runs/<run_id>/*.jsonl.gz`, so archiving a run no longer breaks published hashes. That change is
in `src/api_v2.py` with `tests/test_walk_read_archive.py`; it needs nothing from you.
