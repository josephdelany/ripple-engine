# SESSION CHARTER — standing orders for every Claude Code session on this repo
*Read this at the start of EVERY turn, before anything else. Then PATH.md. The
goal is NORTH_STAR.md; the route is PATH.md; the proof is
WALK_FORWARD_PROTOCOL.md. If your memory of the task and this file disagree,
this file wins.*

## 1. Who you are
- **Session A** owns: `src/state/**`, `WORLD_STATE_CODEBOOK.md`,
  `OUTCOME_MAPPING.md` (+ amendments), `src/story_read.py`, `src/feed_build.py`,
  `src/api_v2.py`, `src/app.html`, `src/acceptance_v2.py`, corpus tooling
  (`admit_events.py`, extractor runs), PATH Steps 1–5, 9, 11.
- **Session B** owns: `src/engine/**`, `src/walk.py`, `data/walk_forward/**`,
  PATH Steps 6–8, the walk figures.
- Neither edits the other's files. If you need a change there, write it as a
  request in `data/handoffs/<from>_to_<to>_<date>.md` and continue with what
  you can do. Both may add tests under `tests/` with a unique basename.
- Shared tree, one branch (`v2-day1`): `git pull --rebase` before every commit;
  commit small; never force-push; never `git stash` the other session's work.

## 2. What never changes
1. Sourced-or-unknown. Every field carries source + vintage. Nothing fabricated.
2. Registered before computed. Thresholds, mappings, menus are committed as a
   dated document BEFORE the code that uses them; changes are dated amendments.
3. Nothing enters `events` without Joe. Nothing is hand-resolved. The ledger,
   sealed reads and challenges are append-only.
4. Published as computed. A null is a result. VALIDATED only per protocol §7.
5. The engine at date t sees vintage ≤ t. Enforced in code, tested.
6. Every displayed number: n + receipt path. Every surface labels
   corpus-derived, monthly-resolution, thin, no-precedent, regex-fallback.
7. `pytest -q` green at every commit. A red test is a stop, not a note.

## 3. The current targets (update this section when they change)
- **Outcome for G:** IES-90 (0 none / 1 threat-display / 2 force / 3 war, +
  DEAL flag) from `event_outcomes` source='ies90', as rebuilt under
  OUTCOME_MAPPING Amendment 2 (dyadic precedence; littoral map as location).
  `sr_outcome_90` is RETIRED as an outcome. `no_independent_outcome` events are
  excluded from G-scoring and counted.
- **Outcome for P:** price/product/flow at +20/+60 td (daily tier), +3/+12 m
  (monthly tier), from series; never pooled across tiers.
- **State:** `state_panel` / `situation_state` (PATH Steps 2–3) when present;
  until then the existing fields, through the same interface.
- **Scores:** Brier + log + ranked probability score (ordinal) for G; CRPS +
  pinball + PIT for P; four baselines; Hedge menu in `data/walk_forward/menu.json`.

## 4. How to work a turn
1. Re-read this file and the PATH step you are on. State the step number.
2. Do the smallest slice that ends with a test. Commit it.
3. If a Joe gate blocks you, write the gate report to
   `data/gates/<step>_<date>.md` and MOVE ON to the next PATH step that is not
   blocked. Never idle waiting for Joe.
4. If you find a flaw in a registered definition, do not patch around it:
   write the dated amendment, then the code, and say in the commit that the
   amendment came first.
5. If you find a flaw in your own earlier work, fix it and record it; do not
   hide it in a later commit message.
6. End every turn with: step done, tests (passed/failed/skipped), commits,
   gates open, next step. Nothing else.

## 5. Definition of done for the whole build
PATH.md §3 (D1–D7). Until every one holds, the product is not finished and
no surface says it is.

## 6. What Joe does (so you don't)
Grants launchd access; requests GSDB; supplies keys in `tools/config.json`;
admits corpus candidates; checks audit sheets against sources; reviews demos.
