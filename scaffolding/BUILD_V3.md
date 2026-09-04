> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# BUILD_V3 — making the predictive engine real
*2026-09-02. Supersedes BUILD_V2.md. Governed by NORTH_STAR.md (the goal),
WORLD_STATE_FRAMEWORK.md + WORLD_STATE_SOURCES.md (the spine),
WALK_FORWARD_PROTOCOL.md (the proof), CLAIM_LEDGER_REGISTRATION.md and
BIG_MOVES_REGISTRATION.md (the gate and the ledger). Read those first.*

## 0. What "real" means here
The engine measures **responses**, never perceptions: what production, flows,
inventories, the curve, crude, product margins and gas actually did after each
shock, given the state the shock landed in. Perceived risk (GPR, coverage, VIX)
is an *input* to the state and a *claim* to be scored — never an outcome.
"Prediction" means a calibrated distribution over outcomes with its n and its
walk-forward score beside it. Anything the walk has not passed is SUGGESTIVE.

## 1. Principles that do not bend
1. Sourced-or-unknown; vintage on every field; the engine at t sees only
   vintage ≤ t (enforced in code, tested).
2. Every threshold registered before computing; amendments dated, appended.
3. Outcomes come from data or from independent codings (ICB, UCDP, MID) —
   never from the corpus's own later entries without an audit against them.
4. Nothing enters the corpus without Joe. Nothing is hand-resolved.
5. Publish as computed. A null is a result.
6. One command shows the state of the system; one page shows the score.

## 2. Phases (dependencies run top to bottom)

### S1 — The state panel (code; ~5 working days)
Loaders, one per source, keyless, each with a test on a published value and
each writing `state_panel(entity_id, field, obs_date, value, unit, source,
vintage, retrieved_at)`:
- Physical: EIA spare capacity 1970–2021 (figure2.xlsx) + STEO country spare
  capacity 2003→; EIA international monthly production (API key, free);
  EI Statistical Review annual panel (2025 archive xlsx; 2026 when obtained);
  EIA US stocks/SPR; PortWatch (loaded).
- Market: NYMEX RCLC1–4 daily 1983–2024-04 → M1–M4 spreads; post-2024 curve
  from a delayed continuous feed, separate source tag; VXO/VIX/OVX; COT;
  ALFRED vintages; WTISPLC monthly (loaded); Kilian/IGREA index 1968→ and the
  exogenous OPEC supply-shock series 1971–2004.
- Actors: COW NMC v7 (CINC + components); SIPRI milex + arms transfers;
  Polity5 (local only) + V-Dem v16 (2019→); Archigos to 2015; WDI oil rents.
- Dyads: ATOP 5.1 (state-year, dyad-year); COW MID 5 (dispute + dyadic);
  ICB v16 (system, actor, dyads); GSDB R5 (after Joe's request; local only);
  Voeten UNGA ideal points; IMF DOTS bilateral trade.
- System: UCDP/PRIO + BRD + External Support; CSP MEPV + Coups (local only);
  GPR monthly (Recent 1985→, Historical 1900→, 44 countries) **with the
  monthly vintage archive**.
- Narrative: GDELT (loaded); NYT Article Search (key; test on Joe's machine).
`WORLD_STATE_CODEBOOK.md` — one line per field (block, unit, resolution,
source, coverage, licence, rule id) — committed **before** any loader runs.
Gate: coverage report per block per decade; S1 acceptance = ≥12 of 15 loaders
green with tests.

### S2 — State-at-event join (code; ~1 day)
`situation_state(event_id, field, value, vintage, source)` = for every corpus
event, every panel field as of `event_date` with vintage ≤ date. Coverage per
block reported for 1946–86 and 1987→. Unit test: a later-vintage value is
invisible. Also `state_at(date)` for any date (the "stand anywhere" call).

### S3 — Outcomes from independent codings (code + Joe audit; ~3 days)
- Join each geopolitical corpus event to its ICB crisis (by dates/actors) →
  ICB `VIOL/SEVVIOSY`, `FOROUT`, `OUTESR`, great-power/UN involvement.
- Join to MID (hostility level, fatality level) and UCDP (intensity, BRD).
- Map to our four branches by a registered rule; compare to the existing
  corpus-derived `sr_outcome_90`; publish agreement (κ). **Joe audits 60**
  disagreements against sources. This decides whether the old "validated"
  label was ever earned.
- Price/flow outcomes stay data-derived (already true).

### S4 — Corpus completion, prioritized (research; Joe-gated; ~2–3 weeks, can overlap S5–S6)
Order: (1) the 61 Big Moves episodes — every "no identified event" gets a
sourced answer or a documented "no catalyst"; (2) ICB crises 1946–1987
touching oil states/chokepoints not yet in the corpus (the deep-history tier,
two-source rule, extractor proposes, Joe admits); (3) OPEC decisions 1960→
from the conference record; (4) dossier fields (posture, capacity, stated
intent) for the escalation classes, NYT/GDELT quotes verbatim with dates.
Target: ≥ 120 sourced events 1946–1986; every 1987→ event with ≥ 25
non-unknown state fields.

### S5 — The engine on the state (code; ~4 days)
`src/engine/similarity.py`: block-wise weighted distance over the state
vector; continuous fields standardized within the information set at t;
categorical matched; unknown fields excluded and counted; retrieval threshold
→ "no adequate precedent"; k analogs with per-block contributions shown.
`src/engine/read.py`: distributions with n for (G) branches, (P) price/product
/flow outcomes at +20/+60 td and +3/+12 m, (F) realized flow disruption;
propagation through the measured edges per branch; differencing table then vs
now over the state vector with evidence status. Weights: uniform prior; the
registered menu (≤12 weightings, `data/walk_forward/menu.json`) written now.

### S6 — The walk (code; ~5 days)
`src/walk.py` per WALK_FORWARD_PROTOCOL.md exactly: filtration-enforced
sequential reads over every event (both tiers, never pooled), sealed before
outcomes; Brier/log, CRPS/pinball/PIT, materiality precision/recall; four
baselines; Hedge updates from past sealed scores only, weights logged; DM with
HLN, stationary block bootstrap, Reality Check/SPA, BH-FDR, VIX-matched
placebo, 1,000 label permutations, regime-block leave-out, specification
curve, simulation power; leakage test (broken filtration must differ).
Outputs: `summary.json`, learning curve, reliability diagrams, PIT histograms,
"what the engine knew at each Big Move." VALIDATED only per §7 of the protocol
including the S3 audit flag. **Published whatever it says.**

### S7 — The desk on the engine (code; ~4 days)
Story page reads from S5 (state vector, block contributions, analogs with
then-vs-now); Challenge re-runs S5 under the analyst's conditions on any state
field, logged; Feed gate stays market-defined; Ledger's engine board reads
`summary.json`; a **Walk** page: pick any date, see the state, the read, the
outcome, the score, the learning curve. Terminal/Trace/Big moves remain.

### S8 — The 9/11 demo and the release (~2 days)
Stand on 2001-09-11 from sealed inputs (WORLD_STATE_SOURCES §7 list): state →
nearest states by block → read → challenge → outcome → score → learning
curve. Then the same for 1990-08-02 and 2026-03-04. Regenerate docs;
acceptance A1–A11 + S1–S6; tag v3.0. Then the paper (8–10 pages) and the
deployment to the family office.

## 3. Effort, honestly
Code: ~4 weeks of Claude Code sessions (S1, S2, S3-code, S5, S6, S7, S8).
Research: ~3 weeks of Joe-gated work (S3 audit, S4 corpus and dossiers),
overlapping the code. The two Claude sessions run in parallel: one on loaders
and engine, one on the walk; Cowork designs, reviews, and reads the numbers.
Elapsed: 6–8 weeks to v3.0 if the gates are cleared as they come.

## 4. What could still make it not work, and what we do then
- The state may carry little signal at n≈300 (skill ≈ 0 after SPA). Then the
  product is the honest measurement: which blocks carry nothing is itself the
  finding, and the tool remains the disciplined outside view with a score.
- ICB/MID/UCDP may disagree with our branches. Then our branches change to
  theirs; theirs are audited by forty years of scholarship, ours by a script.
- Data licences may block redistribution. Then the repo ships loaders, not
  files; the DB is built locally.
- The corpus may stay thin before 1987. Then the monthly tier describes and
  does not validate, and every surface says so.

## 5. Order of the next three pastes
1. S1 + S2 (loaders + join) — one Claude Code session.
2. S3 (independent outcomes + κ) — the same session, then Joe's 60-event audit.
3. S5 + S6 (engine + walk) — the second session, starting once S2's coverage
   report exists.
