> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# TASK_BRIEF_06 — Scenario Playbook ("if X happened today")

Read CLAUDE.md first. All guardrails apply.

## Outcome

A module `src/scenario.py` that answers, for any event type:
**"If an event of this type occurred TODAY, what does history + the current
state of the system imply?"** — as a "scenario card."

Each card must contain, computed from oil.db:

1. **Analogs** — every historical event of that type (clustered, same logic as
   robustness.py): event_id, date, CAR+5, CAR+20.
2. **Base rates** — clustered mean CAR+1/+5/+10/+20, plus min/max range and n.
   Small n must be printed loudly (e.g. "n=2 — anecdote, not statistics").
3. **Today's conditioning** — current amplifier states from the engine-read
   logic (H1 VIX, H2 inventories; H3 always FAILED/fenced off), and the
   historical amplification estimate for whichever amplifiers are ON, citing
   the registered numbers.
4. **A caveat line, always present:** the card is conditional on the event
   occurring; the engine does not forecast whether events occur.

## Interfaces

- CLI: `python3 src/scenario.py conflict_escalation` prints one card;
  `python3 src/scenario.py --all` prints all types and writes
  `data/playbook.md` (all cards, human-readable — the analyst's reference
  document).
- New `scenario_playbook` widget in backend.py (table: one row per event type,
  columns for n, base-rate CARs, range, and today's amplifier context).
- Wire `--all` into refresh.py after engine_read, so the playbook regenerates
  daily with current conditioning.

## Standard

- Import clustering/CAR/amplifier logic from existing modules — no forks,
  no re-implementation, no re-testing of hypotheses.
- Point-in-time: conditioning uses only latest available data at run time.
- Every number traceable to a query; prose limited to fixed templates.
- Teach-style comments.
- Receipts: commit `data/playbook_sample.txt` (console output of --all) and
  show refresh.py completing 8/8 OK.

## Bounds

- No new data sources, no scraping, no keys, no events added (human gate).
- No probabilities of event OCCURRENCE — ever. Market-consequence
  conditionals only.
- No trading logic.
- Do not modify event_study.py / robustness.py / conditioned_study.py.
- Ports 5050/6900 untouched. If something can't be computed honestly, print
  that instead of approximating.
