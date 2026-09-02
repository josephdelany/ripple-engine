# Morning note — what was built overnight (2026-09-02), what to open, what needs you

## Open it
```
cd "News to Markets/ripple-engine"
git checkout v2-day1          # everything is on this branch; main and workbench-platform untouched
./go                          # rebuilds, then opens http://127.0.0.1:5050/app
```
If `./go` complains about data freshness, the watcher and refresh simply haven't run
since Aug 31 — the front door still works on the data in the DB.

## What exists now (all real numbers; nothing placeholder)
1. **Feed** (`/app`) — market-state strip (8 assets vs their own history) and today's
   watcher items through the market-defined gate, ranked; in-line and noise shelves.
2. **Story** — paste anything in the top bar, click any Feed row, or search a corpus
   event ("Open a corpus event" at the bottom of the Feed). Corpus events are read
   point-in-time. Try: `abqaiq_attack_2019`, `hormuz_closure_2026`, then paste a
   paragraph about Kharg and watch it retrieve the 1985–86 Kharg/Sirri strikes.
3. **Big moves** — 43 Brent / 46 WTI / 36 diesel-crack episodes since 1986–87 with
   attribution, anticipation lags, and the two-way rates that drive the gate.
4. **Ledger** — three boards; young and says so. Every story you read from now on logs
   its checkable claims; "Resolve claims past horizon" runs the data-only resolver
   (also runs in the daily loop).

Modules, tests and docs: `src/big_moves.py`, `materiality.py`, `ledger.py`,
`story_read.py`, `feed_build.py`, `api_v2.py`, `app.html`; tests in
`tests/test_v2_gate_ledger.py`, `tests/test_v2_story_api.py` (20 new, all green);
`README.md` v2 section; `acceptance_v2.py` now checks A1–A11 (8 PASS, 3 PARTIAL).

Registered before computing, amendments dated and disclosed:
`BIG_MOVES_REGISTRATION.md` (2 amendments), `CLAIM_LEDGER_REGISTRATION.md` (2).
Read the amendments — they are the honest part.

## What needs your decision (I did not decide these)
- **14 pre-1987 events were loaded into `events` at 02:23 UTC by the Claude Code
  session (B6).** Nothing enters the corpus without you. Approve or remove.
- **Walk-forward "VALIDATED"** (Claude Code, B5): outcome labels are derived from the
  corpus (situation records observe subsequent corpus events), not source-audited.
  Every surface now labels them "corpus-derived". Decide whether a source audit
  of the +90d outcomes happens before anyone outside sees the word "validated".
- `tests/test_status.py::test_st2` fails in my sandbox only because engine_status
  goes RED on stale series (last refresh Aug 31). Run `./go` and it clears.

## What is NOT there yet (be straight about it)
- Deep history to 1970 beyond the 14/17 B6 events; conditioned situation fields for
  *live* stories (they are read on class + target only, and the page says so).
- The corpus-article pilot (record vs narrative on the 313 source articles) — the
  Ledger's middle board is seeding, not lying.
- Entity-level materiality (which asset, what volume) — the gate is class-level.
- Fresh data: nothing fetched overnight (no network side effects from my side).

## Commit
One commit on `v2-day1`: "v2 day-1: Big Moves, materiality gate, claim ledger, Story
read, Feed, /app front door (NORTH_STAR)". Only my files are in it; your modified
`data/*` files from earlier runs are left uncommitted as they were.
