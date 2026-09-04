> **SUPERSEDED — NOT A CURRENT CLAIM.** Demonstration pages built from the superseded event walk. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# Sealed reads, walked through

PATH Step 10. Each page below is written *from the sealed read and its score* in
`data/walk_forward/{reads,scores}.jsonl`, run **`walk_20260903T052633Z`** — the run
`summary.json` reports, on the escalation target rebuilt under `OUTCOME_MAPPING.md`
Amendment 4. Nothing is reconstructed from memory; where a number appears, the field it
came from is named. The reads were hashed and time-stamped before the outcome was looked
up (`sealed_at` < `outcome.looked_up_at` on every row; `tests/test_demo_911.py`
re-verifies the hash with `walk.verify_seal`).

| Page | Event | as_of | Prior events in pool | Scored for the gates? |
|---|---|---|---:|---|
| [1990.md](1990.md) | Iraq invades Kuwait | 1990-08-02 | 6 | **No** — below the registered burn-in of 8; published, not counted |
| [911.md](911.md) | September 11 attacks | 2001-09-11 | 9 | **Yes** |
| [2026.md](2026.md) | Iran declares Hormuz closed | 2026-03-04 | 26 | **Price only** — `no_independent_outcome`, so escalation is not scored at all |

How to read them: the engine's read is a frequency distribution over analogs it found
*before* the date, with *n*. "Climatology" is the base rate over every prior event. A
lower Brier / RPS / CRPS is better. The point of the pages is not that the engine was
right — on these three it mostly was not — but that you can see exactly what it knew,
what it said, and how it was scored, with nothing edited after the fact.

## What the Amendment 4 rebuild did to these three pages

Worth stating plainly, because the previous version of this file said the opposite.

Across runs `210135Z` and `003422Z` the numbers on these pages did **not** move: the
spine repair between them touched only provenance columns the engine does not read. The
Amendment 4 rebuild is not like that. It changed the escalation target itself — the
ongoing-conflict rule now reaches COW War and UCDP GED, and a missing covering record no
longer reads as level 0 — and **every number on all three pages moved with it**, along
with all three read hashes.

Three consequences, all visible above:

- **1990 fell further below burn-in**, 7 prior events to 6. It was never counted; it is
  now further from being countable.
- **9/11's pool fell** from 10 to 9, and its escalation scores moved.
- **2026 lost its escalation label entirely.** `hormuz_closure_2026` is now
  `no_independent_outcome`, its `scores` block contains a `P` and no `G`, and the page
  was **restructured rather than re-quoted**: it is a price walkthrough, and the sealed
  escalation read is shown as a non-result. Do not cite it for an escalation finding.

The superseded pages are in git history, and the superseded run is archived at
`data/walk_forward/runs/walk_20260903T003422Z/`. Every hash quoted on these pages stays
resolvable: `/api/walk/read` falls back to the gzipped run archive when a run is no
longer the live one, so a citation does not rot the next time the walk is re-run.

Open any read on the desk: `./go` → Walk → click the event.
