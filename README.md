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
escalation reads; numbers from `data/walk_forward/summary.json`, run 193022Z with
the fourth baseline and recalibration):** with independent escalation labels, the
state-conditioned engine has **no skill beyond the base rate** for escalation
(Brier skill −0.005, 95% CI −0.083 … +0.067; SPA p 0.74 over 15 models) or for
price (CRPS skill −0.030, CI −0.064 … +0.006). Two results from this run are worse
than that, and both survive multiple-comparison control:

- **A dumb rule beats it on escalation.** "The dyad's escalation level over the
  last 90 days will persist" scores Brier **0.481** against the engine's **0.705**
  — skill −0.467, DM p 0.002. Escalation is strongly autocorrelated and the engine
  throws that away by averaging over analogs.
- **Recalibration made it worse, not better.** We predicted in writing that the
  engine's miscalibration was hiding real resolution, and registered M13
  (walk-forward isotonic) to test it. M13's Brier skill is **−0.590** (CI −0.834 …
  −0.357, p < 0.001) and its reliability terms rose rather than fell. **The
  hypothesis is falsified and published as such.**

It does beat persistence on price (+0.162, p < 0.001) and is not reliably better
than random analogs (+0.064 on escalation, +0.033 on price; neither significant).
**The placebo condition is unresolved, not passed:**
against the size-matched random-analog reference the VIX-matched placebo is −0.02
(CI covers zero), but that reference is defined in an amendment Joe has not
ratified; against climatology — the reference every other skill number here uses,
and the one the registered protocol §6 implies — it is −0.075 (CI −0.106 …
−0.043), which is not zero. Until the amendment is ratified or withdrawn, no
verdict may lean on "the placebo is null" (`docs/red_team_2.md` finding 1;
corrected 2026-09-02). The specification curve is negative in 78% of 162 registered
settings (median −0.017); dropping 2008, 2020 or 2026 changes nothing; learning
adds nothing over a frozen engine. A label-permutation test rejects "the engine is
noise" (p 0.002) while the skill test says "not better than the base rate" — the
engine finds structure in the labels but not enough to forecast with. **Power is
now measured, not asserted:** at n = 150 the walk can detect an escalation skill of
+0.12 with 96% power but only +0.043 with 41%, so "no skill" here means "no skill
larger than roughly a tenth", not "exactly zero".
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
