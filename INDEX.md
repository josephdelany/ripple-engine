# What to read, in what order

*This repository has 59 documents at its root and about 880 in total. That is the residue
of a project that registered everything it did. This page is the map. Anything not listed
here is either the frozen record (never edited) or superseded working material (bannered,
never deleted).*

---

## If you have five minutes

1. **`README.md`** — what it is and what it found.
2. **`docs/PAPER_DRAFT.md`** — the full write-up: method, results, robustness, limitations,
   and Appendix A tracing every number to the file that produced it.

## If you have twenty

3. **`docs/demos/`** — three sealed reads walked through end to end: 9/11, Iraq–Kuwait
   1990, Hormuz 2026. What the engine knew, what it said, what happened, how it scored.
4. **`docs/RIPPLE_FINDINGS.md`** — the propagation study. 477 cells, 21 transmitting
   against 1–24 expected by chance.
5. **`NORTH_STAR.md`** — what the desk is for, in the analyst's terms.
6. Run it: `./go` → `http://127.0.0.1:5050/app`.

## The registered record — never edited, only appended

These are the pre-registrations and protocols. Amendments are dated and appended at the
bottom of each; nothing above an amendment is ever rewritten. Git timestamps establish
that each was committed before the code it governs.

| file | governs |
|---|---|
| `WALK_FORWARD_PROTOCOL.md` | the walk: scores, baselines, tests, and the §7 verdict rule (Amendments A–I) |
| `OUTCOME_MAPPING.md` | the escalation target IES-90 and the hostility precondition (Amendments 1–3.3) |
| `BIG_MOVES_REGISTRATION.md` | market-defined significance |
| `CLAIM_LEDGER_REGISTRATION.md` | claim typing, verdicts, the challenge loop |
| `RIPPLE_REGISTRATION.md` | the propagation study's design |
| `SPINE_REGISTRATION.md` | what a complete event record is |
| `PRE_REGISTRATION.md`, `PRE_REGISTRATION_V2.md`, `BRIEF_SKELETON.md`, `REGISTERED_SAMPLE.md` | the v1 hypotheses, frozen |
| `EVALUATION.md`, `RED_TEAM_1_RESPONSE.md` | the v1 evaluation bar and the first review's disposition |

## The integrity record

- **`docs/red_team_1.md`** — the first adversarial review, which falsified the headline.
- **`docs/red_team_2.md`** + `docs/red_team_2/` — the second, with nine appendices.
- **`data/gates/`** — release checks and the dated findings, including the negative control.
- **`data/spine/AUDIT.md`**, **`data/spine/CLASS_AUDIT.md`** — the corpus measured against
  its own standard, before and after repair.
- **`data/audits/`** — the label audit in progress.

## Current working documents

`PATH.md` (the route), `SESSION_CHARTER.md` (who owns what), `CLAUDE.md` (the guardrails),
`DESIGN.md` (the desk specification), `DATA_DICTIONARY.md`, `WORLD_STATE_FRAMEWORK.md`,
`WORLD_STATE_SOURCES.md`, `WORLD_STATE_CODEBOOK.md`, `SITUATION_CODEBOOK_V2.md`,
`RIPPLE_SOURCES.md`, `EDGE_PORTFOLIO.md`, `STATE_OF_THE_ENGINE.md`.

## Superseded — bannered, not deleted

`SURFACES.md`, `DIFFERENTIATION.md`, `TALKING_TO_IT.md`, `USAGE.md`, `ENGINE_STATUS.md`,
`ENGINE.md`, `ACCEPTANCE_TEST.md`, `METHOD.md`, `RESEARCH_BENCH.md` — all from July 2026,
all describing a validated portfolio that no longer exists. Each now opens with a dated
banner saying so and pointing at the current record. They are kept because a project that
deletes its wrong turns cannot be checked.

`TASK_BRIEF_01`–`11`, `BUILD_V2.md`, `BUILD_V3.md`, `MORNING_NOTE.md`, `DONE.md`,
`DECONSTRUCTION.md`, `PLATFORM_AUDIT.md`, `NEWS_LAYER.md`, `FRONTEND_SPEC.md`,
`STATE_OF_THE_ENGINE_V2.md` — build scaffolding, superseded by `PATH.md` and `DESIGN.md`.

## Reproducing it

`make reproduce` rebuilds `data/walk_forward/summary.json` from source with the full
registered draws. Read the Makefile's header first: it states honestly which sources a
clean clone can and cannot reach, and which are licence-gated. Two independent full runs
reproduce the same content digest.
