# Ripple Engine

**A pre-registered, historically-conditioned engine for reading how geopolitical
shocks move the oil and petro-products economy — and a walk-forward test of
whether the record predicts anything at all.**

Built Spring–Summer 2026 by a history major (Middle East focus) directing AI
coding agents as architect and reviewer. Every number in this repo is one hop
from its receipt; every threshold was registered before it was computed; every
result is published as computed, nulls included.

## What it is

- **The spine.** 313 coded geopolitical and policy shocks, 1973–2026 (two-source
  rule, human-gated codebook), a monthly price spine back to 1946, 598 series and
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

**On prediction (the walk, daily tier, 241 scored reads):** with independent
escalation labels, the state-conditioned engine has **no skill beyond the base
rate** for escalation (RPS skill +0.02, 95% CI −0.09 … +0.11) or for price
(CRPS skill −0.03 vs climatology); it beats persistence (+0.16, p < 0.001) and
is borderline against random analogs; the placebo is null; the specification
curve is negative across every registered setting; learning adds nothing over a
frozen engine; the filtration is binding. **Verdict as computed: SUGGESTIVE /
null on both targets.** An earlier run that showed escalation skill of +0.12
(p < 0.001) was scored against our own corpus-derived labels; it did not survive
independent labels, exactly as the first headline result (H1, volatility
clustering) did not survive a matched placebo. Both downgrades are in the
record.

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
