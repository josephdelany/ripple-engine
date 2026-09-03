
## Amendment O (2026-09-03) — the abnormal-return price target on the event walk, from the sealed run
*Registered BEFORE the code. Session B. Answers `docs/audit/01_TIER1_design_defects.md` A1 on the EVENT
walk, after the same test on the grid arm (`docs/ABNORMAL_RETURN_RESULT.md`) found the grid's decisive loss
to climatology was a property of the raw-return target. The event walk's price numbers are the ones the
paper reports and they still carry A1 in full.*

### O.1 Why this needs no re-run, and therefore disturbs nothing
Every sealed read carries the **identities** of the analogs whose outcomes form its P forecast
(`items[*].P_ids`, `engine.P.ids`) and the point-in-time climatology pool. Retrieval is label-free and was
already performed. So the abnormal-return target is computed by **substituting each analog's outcome value**
with its abnormal counterpart and re-scoring — exactly the Amendment K discipline. **No read is re-read, no
analog is re-retrieved, no Hedge weight is re-fitted, and `walk_20260903T052633Z` is not re-run or
re-judged.**

### O.2 The expected-return model, identical to the grid arm
For an event at `t` on the daily tier, whose registered P outcome is the percentage change of the tier's
price series over +20 trading days from `t−1`:

    AR_i = chg_pct_i − 20 · α̂_i · 100

with `α̂` the mean daily log return estimated on **250 trading days ending 21 trading days before `t`**
(a 20-day gap, so a read's own horizon can never enter its own benchmark), minimum **100** observations.
The **constant-mean-return model** is used because the daily tier's target is crude itself and there is no
exogenous oil-market factor distinct from the asset (Brown & Warner 1985, *JFE*). An event whose estimation
window is short is **dropped and counted**, never scored on a raw return as a silent fallback.

### O.3 What is recomputed and what is held fixed
Recomputed in abnormal space: the read's own outcome, every analog atom of every menu item, the
climatology pool's atoms, and the random-analog draws (same k, same sealed seed). Held **exactly as
sealed**: which analogs were retrieved, their weights, the Hedge weights, and the cluster structure.
Persistence stays a point mass at zero, which is no-change in either space.

### O.4 Inference, unchanged and fully guarded
CRPS as the registered gate score; the stationary block bootstrap at the tier's measured mean block; DM/HLN
at the tier's HAC lag; **SPA with climatology as benchmark over the model family, and BH-FDR across every
comparison reported.** Omitting the guards here while requiring them on the grid arm would be the double
standard this project exists to prevent.

### O.5 Standing and the three outcomes, fixed before the numbers
DIAGNOSTIC standing, like Amendment K: published beside the registered raw-return numbers, which are **not
withdrawn**, and it **cannot move any §7 verdict** on its own.
- **The raw loss persists on abnormal returns** → A1 is a real limitation but not the cause of the event
  walk's price null, and the published number stands with a stated caveat.
- **The raw loss disappears** → the event walk reproduces the grid finding, and **the paper's price section
  is reporting a target artefact and must be rewritten rather than annotated.**
- **The engine beats climatology on abnormal returns and it survives SPA and FDR** → a positive price
  result exists and the published null is wrong. This is the least likely and the most consequential, and
  it is the reason the guards in O.4 are mandatory rather than optional.
Published in `summary.json → tiers.daily.P.diagnostic_abnormal` with `registered: true`,
`derived_from_run`, and the dropped-window count.
