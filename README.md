# Ripple Engine

**A pre-registered, historically-conditioned engine for reading how geopolitical
shocks move the oil and petro-products economy — and a walk-forward test of
whether the record predicts anything at all.**

Built Spring–Summer 2026 by a history major (Middle East focus) directing AI
coding agents as architect and reviewer. Every number in this repo is one hop
from its receipt; every threshold was registered before it was computed; every
result is published as computed, nulls included.

## What it is

- **The spine.** 313 coded geopolitical and policy shocks, 1973–2026, human-gated
  under a codebook with per-field provenance ("sourced or unknown"). **The spine is
  the project's weakest layer and is under repair:** each event carries one primary
  source URL, not the two the codebook's admission rule requires (0 of 313 have two
  independent sources recorded), event descriptions average one sentence, and the
  coverage is badly skewed — 8 events in the 1970s, 11 in the 1980s, 16 in the
  1990s, against 150 in the 2020s. The engine's analog pool before 1990 is
  therefore thin by construction, which is visible in the 1990 demo. Repair is
  registered and in progress (`data/candidates/`, `DOSSIER_RULE.md`): dossiers with
  two verified sources per event, admitted only by the author.
  Also: a monthly price spine back to 1946, 598 series and
  467k observations, and ~8,000 measured price-transmission edges across crude,
  products, gas, LNG and fertilizer. A world-state panel (280k rows, 17 open
  academic and government datasets — COW, ATOP, ICB, UCDP, Polity, V-Dem, SIPRI,
  GPR, EIA, Energy Institute, Kilian, UNGA ideal points, WDI, Archigos) joined to
  every event with the **vintage rule**: the engine at date *t* sees only what was
  knowable at *t*.
- **Big Moves.** Significance defined by the market, not by us: every top-tail
  move in Brent, WTI and the diesel crack since 1986 (and monthly WTI since 1946),
  each attributed to what was knowable while it moved — or marked *no identified
  event*.
- **The engine.** Block-wise similarity over the state vector (physical, market,
  actors, dyads, system), analog retrieval with a registered threshold, reads as
  frequency distributions with *n*, propagation through the measured edges,
  then-vs-now differencing, and "no adequate precedent" as a first-class answer.
- **Independent outcomes.** Escalation at +90 days (IES-90: none / threat /
  force / war, + deal) is computed from dated records in ICB, COW MID, COW War and
  UCDP — not from our own corpus — after our self-coded labels tested at chance
  against them (κ ≈ 0).
- **The walk.** The engine forecasts the past in sequence: sealed reads (hashed
  before the outcome is looked up), strictly proper scores (Brier / log / RPS for
  escalation, CRPS / pinball / PIT for price), four baselines (climatology,
  persistence, random analogs, a frozen engine), Hedge learning over a registered
  menu, Diebold–Mariano with the HLN correction, stationary block bootstrap,
  White's Reality Check / Hansen SPA, label permutation, a VIX-matched placebo,
  regime-block leave-out, a specification curve, and a leakage test that breaks
  the filtration to prove it binds. `WALK_FORWARD_PROTOCOL.md`.
- **The desk.** `./go` → `http://127.0.0.1:5050/app`: Feed (market state, gated
  stream), Story (any development read in a desk's order, with a challenge loop),
  Big moves, Walk (open any sealed read and its score), Ledger (append-only
  claims that resolve from data).

## What it found

**On the record (Big Moves, Brent, 43 episodes 1987–2026):** 35% of the market's
largest moves have no identifiable event in the corpus; the market's extreme
preceded the catalyst in a third of the rest; demand shocks and OPEC decisions sit
inside big moves more often than any random day, while infrastructure attacks,
sanctions and chokepoint disruptions sit inside them *less* often on crude — and
2–3× more often on the diesel crack. Geopolitics moves products more than crude.

**On prediction (the walk, daily tier, ~250 scored reads; numbers from
`data/walk_forward/summary.json`, run 182828Z after Amendment 2):** with
independent escalation labels, the state-conditioned engine has **no skill
beyond the base rate** for escalation (Brier skill −0.01, 95% CI −0.08 … +0.06;
SPA p 0.79) or for price (CRPS skill −0.03 vs climatology). It beats persistence
(+0.16, p < 0.001) and is not reliably better than random analogs (+0.06 and
+0.04, neither significant). The VIX-matched placebo is null (−0.02, CI covers
zero); the specification curve is negative in 83% of 162 registered settings
(median −0.02); dropping 2008, 2020 or 2026 changes nothing; learning adds
nothing over a frozen engine. A label-permutation test rejects "the engine is
noise" (p 0.008) while the skill test says "not better than the base rate" —
the engine finds structure in the labels but not enough to forecast with.
**Verdict as computed: SUGGESTIVE / null on both targets.** An earlier run that
showed escalation skill of +0.12 (p < 0.001) was scored against our own
corpus-derived labels; it did not survive independent labels, exactly as the
first headline result (H1, volatility clustering) did not survive a matched
placebo. Both downgrades are in the record.

## The integrity record

Pre-registration with git timestamps (`BRIEF_SKELETON.md`, `PRE_REGISTRATION_V2.md`,
`BIG_MOVES_REGISTRATION.md`, `CLAIM_LEDGER_REGISTRATION.md`, `OUTCOME_MAPPING.md`,
`WALK_FORWARD_PROTOCOL.md`) — every amendment dated and appended, never edited.
An external adversarial review (`docs/red_team_1.md`) that falsified the original
headline result; the downgrade published. No fabricated field: sourced or
"unknown". Nothing enters the corpus without a human. Licence-restricted panels
are loaded locally and never committed. 300+ tests; `python3 src/acceptance_v2.py`.

## Run it

```
./go                      # refresh, rebuild, open http://127.0.0.1:5050/app
python3 src/walk.py       # re-run the walk; publishes data/walk_forward/summary.json as computed
python3 src/big_moves.py  # re-run market-defined significance
pytest -q
```

## Where it is going

`PATH.md` is the route: Amendment 2 to the outcome mapping (dyadic precedence),
the 30-event label audit, corpus completion before 1987, the 9/11 / 1990 / 2026
demos from sealed inputs, and a paper. `SESSION_CHARTER.md` governs every session.
The earlier README, with the v1 record and headline history, is at
`docs/README_v1_record.md`.
