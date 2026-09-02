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

**On the record (Big Moves, Brent, 43 episodes 1987–2026):** 15 of 43 (35%) of the
market's largest moves have no identifiable event in the corpus. Of the 28 that do,
**20 (71%) have at least one event that was already knowable more than 20 trading
days before the move began, and in 14 (50%) every attributed event was** — the
market's extreme routinely precedes the catalyst, more often than an earlier
version of this sentence said ("a third", which was the pooled Brent+WTI+crack
figure, 33 of 89, quoted under a Brent-only heading; corrected 2026-09-02 after
`docs/red_team_2.md` finding 2). Demand shocks and OPEC decisions sit
inside big moves more often than any random day, while infrastructure attacks,
sanctions and chokepoint disruptions sit inside them *less* often on crude — and
2–3× more often on the diesel crack. Geopolitics moves products more than crude.

**On prediction (the walk, daily tier, 253 scored price reads and 150 labelled
escalation reads; numbers from `data/walk_forward/summary.json`, run 210135Z, the
first run in which the vintage rule binds on the per-event situation fields):**

**The engine is significantly *worse* than the base rate on both targets** —
escalation Brier skill **−0.097** (95% CI −0.180 … −0.018, DM p 0.022), price CRPS
**−0.071** (CI −0.136 … −0.017, p 0.016). Both survive multiple-comparison control.

The reason is the project's central finding. Earlier runs of the same code showed
parity with climatology (−0.005, −0.030). Those runs took the per-event situation
fields as *coded* rather than as *knowable*. Once the vintage rule is enforced on
them too — registered as Amendment H before the code — **262 of 313 events turn out
to have no situation field knowable on the day**, retrieval falls back to the
market block alone, and the parity disappears. The state conditioning that gave the
engine its edge was, to a first approximation, hindsight.

Three consequences, all published as computed:

- **A dumb rule beats it.** "The dyad's escalation level over the last 90 days will
  persist" scores Brier **0.480** against the engine's **0.769** — skill −0.600,
  p 0.0002. Escalation is autocorrelated; averaging over analogs from other dyads
  destroys that. The engine's one surviving win is against persistence on *price*
  (+0.129, p < 0.001).
- **Recalibration is falsified.** We predicted in writing that miscalibration was
  hiding real resolution and registered M13 (walk-forward isotonic) to test it.
  Skill **−0.700** (p < 0.001), reliability terms *higher*. Published as falsified.
- **The permutation test no longer rejects.** It gave p 0.002 before Amendment H;
  now p 0.124. The structure it had detected lived in the retrospective codings.

The specification curve is negative in **all 162** registered settings (0% positive,
median −0.075); dropping 2008, 2020 or 2026 changes nothing; the frozen mixture beats
the online one, so Hedge learning costs rather than helps; the placebo now fails
under two of three references. A standing filtration audit ran 15,784 point-in-time
checks with **0 violations**, and two independent full runs reproduce the same
content digest.

**Power, measured not asserted:** minimum detectable skill at 80% is 0.127
(escalation) and 0.085 (price); detecting +0.05 would take ~1,200 scored reads
against 150 today. So "worse than the base rate" is established; "no small positive
edge exists" is not, and the corpus is roughly eight times too small to settle it.

**Verdict as computed: SUGGESTIVE / null on both targets** — and the honest
description is worse than the label: significantly worse than the base rate,
point-in-time. Earlier positive headlines (H1 volatility-stress amplification;
escalation skill +0.12 on self-coded labels) did not survive a matched placebo and
independent labels respectively. Five of six "validated" propagation edges were
retracted under a pre-registered re-test. Every downgrade is in the record, with the
run that produced it.

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
