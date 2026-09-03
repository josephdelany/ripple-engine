# Three sealed reads, walked through

PATH Step 10. Each page below is written *from the sealed read and its score* in
`data/walk_forward/{reads,scores}.jsonl`, run `walk_20260903T003422Z` — the run
`summary.json` and `docs/PAPER_DRAFT.md` report. Nothing is reconstructed from
memory; where a number appears, the field it came from is named. The reads were
hashed and time-stamped before the outcome was looked up (`sealed_at` <
`outcome.looked_up_at` on every row; `tests/test_demo_911.py` re-verifies the hash
with `walk.verify_seal`).

| Page | Event | as_of | Prior events in pool | Scored for the gates? |
|---|---|---|---|---|
| [1990.md](1990.md) | Iraq invades Kuwait | 1990-08-02 | 7 | No — below burn-in (8); shown as what the engine said, not evidence |
| [911.md](911.md) | September 11 attacks | 2001-09-11 | 10 | Yes |
| [2026.md](2026.md) | Iran declares Hormuz closed | 2026-03-04 | 25 | Price only — no independent escalation source covers 2026 yet |

How to read them: the engine's read is a frequency distribution over analogs it
found *before* the date, with *n*. "Climatology" is the base rate over every prior
event. A lower Brier / CRPS is better. The point of the pages is not that the
engine was right — on these three it mostly was not — but that you can see
exactly what it knew, what it said, and how it was scored, with nothing edited
after the fact.

Every hash quoted on these pages stays resolvable: `/api/walk/read` falls back to the
gzipped run archive when a run is no longer the live one, so a citation does not rot the
next time the walk is re-run. The numbers on these three pages are unchanged across runs
210135Z and 003422Z — the spine repair between them moved no forecast number.

Open any read on the desk: `./go` → Walk → click the event.
