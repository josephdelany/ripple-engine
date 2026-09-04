> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

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
  PATH Steps 6–8, the walk figures. Added by Joe's brief of 2026-09-03 (the grid
  study, a new estimand with the unit a date rather than an event):
  `GRID_STUDY_REGISTRATION.md`, `src/engine/grid/**`, `data/grid/**` and
  `tests/test_grid_*.py`. The grid study reads `data/walk_forward/**` and never
  writes there; no event-triggered number is re-judged by it, and the two units are
  never pooled (GRID_STUDY_REGISTRATION §0.2).
- **Session E** (the history spine) owns: `EVENTS_CODEBOOK.md`,
  `data/events*.csv`, `data/dossiers/**`, `data/spine/**`, `src/spine_audit.py`,
  `SPINE_REGISTRATION.md`, `docs/spine/**`; `src/dossier.py` is **shared with A**
  and changed only after a handoff note. Session E does not touch `src/engine/**`,
  `src/walk.py`, `src/state/**`, `src/api_v2.py`, `src/app.html` or `src/ripple_*`.
  It brings event *records* (description, sources, entities, class) up to the
  SPINE_REGISTRATION standard; it never writes to the `events` table itself —
  every change is a patch file Joe admits, per §2 rule 3.
- **Session F** (target definitions) owns: `OUTCOME_MAPPING.md` amendments
  concerning the G target, `data/spine/CLASS_AUDIT.md`, `tests/test_hostility.py`.
  It does **not** touch `src/engine/**`, `src/walk.py`, `data/walk_forward/**` (B),
  `src/state/**`, `src/api_v2.py`, `src/app.html`, `src/story_read.py` (A),
  `src/ripple_*` (C), `data/dossiers/**`, `data/spine/patches/**` (E). It reads
  those trees and reports numbers; it never edits them and never writes to the
  `events` table. Amendments are registered before anything is computed under them;
  implementation of an amendment is B's, in v3. `data/spine/CLASS_AUDIT.md` is
  carved out of Session E's `data/spine/**` by Joe's brief of 2026-09-02;
  `data/handoffs/F_to_E_2026-09-02_class_audit.md` records the carve-out.
- **Session H** (the claim loop) owns: `data/ledger/**`, `data/reader_eval/**`,
  `src/ledger_backfill.py`, `src/audit_reader.py`, `src/uncheckable_audit.py`,
  `tests/test_ledger_backfill.py`, `tests/test_audit_reader.py`,
  `tests/test_uncheckable_audit.py`, `tests/test_challenge_loop.py`. It is the
  session that makes the Ledger's core mechanic actually fire: a claim logged at
  its real knowable date and resolved from data at its horizon. `src/ledger.py`
  and `src/challenge.py` are **shared** — H may fix a resolver defect it can
  demonstrate with a failing test, and records the fix in an amendment; it never
  changes a threshold or a verdict rule to move a ratio (that is INV-6 /
  charter §2). Session H does **not** touch `src/engine/**`, `src/walk.py`,
  `data/walk_forward/**` (B), `src/story_read.py`, `src/api_v2.py`,
  `src/app.html`, `src/feed_build.py`, `src/reader.py` (A), `src/ripple_*` (C),
  `data/dossiers/**`, `data/spine/**` (E). Defects found in those trees are
  written to `data/handoffs/H_to_<who>_<date>.md` and reported, never patched
  in place.
- **Session G** (the pre-1973 tail) owns: the pre-1987 admission work under
  `data/candidates/**` (the sheet, its registration and amendments, the
  screen and the gap arithmetic), `data/dossiers/` for events dated **before
  1973-01-01**, `src/situation_vintage.py`, `src/g_monthly_gap.py`, and
  `docs/g/**`. It does **not** touch `src/engine/**`, `src/walk.py`,
  `data/walk_forward/**` (B), `src/app.html`, `src/story_read.py`,
  `src/api_v2.py`, `src/state/**` (A), `src/ripple_*` (C),
  `data/spine/CLASS_AUDIT.md` (F), or any dossier dated 1973-01-01 or later (E).
  It reads those trees and reports numbers; it never edits them and never
  writes to the `events` table. Its dossiers are built to SPINE_REGISTRATION.md
  and its patches go to Joe under §3 of that document, like E's. Registrations
  are dated and committed before the code that uses them.

- **Session I** (the figures, the citation guard, and the demo pages) owns:
  `docs/figures/**`, `docs/demos/**`, `src/figures_paper.py`,
  `src/citation_guard.py`, `docs/citation_inventory.json` and
  `docs/CITATION_INVENTORY.md`. `docs/demos/**` is assigned by Joe's brief of
  2026-09-03, after the Amendment 4 re-run left all three pages superseded; they
  are regenerated from `data/walk_forward/{reads,scores}.jsonl` of the live run
  and from nothing else, and a page whose read the current target excludes is
  restructured rather than re-quoted.
  It draws the paper figures and nothing else. It **computes nothing**: every
  number on every figure is read out of a committed file, each figure carries the
  path it was read from, and `tests/test_figures_paper.py` re-reads the sources and
  fails if a figure and its source disagree or if a result is typed into the drawing
  code. Where a figure needs a number that is not in `data/walk_forward/summary.json`
  — the before/after panel needs the run before Amendment H, and that file publishes
  one run — the figure names the other committed files it read on its own face rather
  than carrying the number silently. Session I does **not** touch `src/engine/**`,
  `src/walk.py`, `data/walk_forward/**` (B), `src/state/**`, `src/app.html`,
  `src/api_v2.py`, `src/story_read.py` (A), `src/ripple_*` (C), `data/dossiers/**`,
  `data/spine/**` (E), or `data/ledger/**` (H). It adds figures and their captions to
  `README.md` and `docs/BRIEF.md` and edits nothing else in those pages. It never
  re-runs the walk: if `summary.json` moves, the figures are redrawn from it, never
  the other way round. Defects it finds while reading another session's tree go to
  `data/handoffs/I_to_<who>_<date>.md`.
  The **citation guard** is the same discipline applied to the prose: every numeric
  claim in `README.md`, `docs/BRIEF.md`, `docs/PAPER_DRAFT.md`, `docs/EXPLAIN.md`
  and `OPEN_ITEMS.md` is inventoried against a declared registry of run objects,
  and `tests/test_citation_guard.py` goes **red when the run those numbers came
  from is superseded**. Session I READS those five documents and never edits them:
  the guard reports what cannot be traced, it never repairs a sentence. UNSOURCED
  is published and left standing — the guard never guesses at a source, and a
  registered exception or derived formula is added only when it can be *evaluated*
  against the record, never inferred to shorten the list.
- **Session K** (the ongoing-war defect in the G target) owns: `OUTCOME_MAPPING.md`
  **amendments** and `src/state/ies90.py`. Both are carved out of Session A's block by
  Joe's brief of 2026-09-02; A keeps the rest of `src/state/**`,
  `WORLD_STATE_CODEBOOK.md`, and the body of `OUTCOME_MAPPING.md` §1-§6 (Session F keeps
  its amendments on the hostility precondition, and K does not reopen them). K exists
  because red team 2 finding 3 is a defect in the *rule*, not in the code that implements
  it: Amendment 1.1's "ongoing -> no level" carve-out was never extended to COW War or
  UCDP GED, and 34 of 54 level-3 "war" labels are wars that were already running.
  It does **not** touch `src/app.html`, `src/story_read.py`, `src/api_v2.py` or the desk
  (A, in flight), `src/engine/**`, `src/walk.py`, `data/walk_forward/**` (B),
  `data/dossiers/**`, `data/spine/**` (E, F), `docs/g/**` (G), `data/ledger/**` (H),
  `docs/figures/**` (I). It may add tests under `tests/` with a unique basename.
  Three working rules that follow from where it sits:
  1. **Amendment first, then code**, in separate commits, so the gap is visible in
     `git log`. The expected effect on n and on the level distribution is written down
     *before* the number is computed.
  2. **It does not rewrite `event_outcomes` while another session holds an experiment
     open on it.** `ies90.run(conn, write=False)` computes every count without touching
     the table; the counts are published as a document and a JSON file, and the rebuild
     is a separate, announced step Joe schedules with B. Changing the target under a
     running experiment is the failure the seal exists to prevent.
  3. **It commits by explicit path**, never `git add -A`: the shared tree carries other
     sessions' staged and unstaged work at all times.

- No session edits another's files. If you need a change there, write it as a
  request in `data/handoffs/<from>_to_<to>_<date>.md` and continue with what
  you can do. All may add tests under `tests/` with a unique basename.
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
