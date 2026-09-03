
---

## Amendment 2 to Part III (2026-09-03) — the abnormal-return target, answering Tier-1 A1
*Registered before the code. Session B. `docs/audit/01_TIER1_design_defects.md` A1 finds that the price
target is a raw return with no market model, so climatology is approximately the unconditional distribution
of 20-day oil returns and beating it requires forecasting oil. If that is right, **the price null follows
from the target definition and not from the phenomenon**. This amendment makes the question answerable
instead of arguable: the same engine, the same analogs, the same baselines, scored on an abnormal return.*

### A2.1 The expected-return model, fixed before any number
For a read at grid date `t` on target `a`, the expected return is estimated on an **estimation window of
250 trading days ending 21 trading days before `t`** — a 20-day gap so the event's own horizon can never
enter its own benchmark — with a minimum of **100** usable observations; below that the read is dropped and
counted, never scored on a raw return as a silent fallback.

Two registered model forms, by asset class, following the event-study convention (Brown & Warner 1985,
*JFE*, who show the constant-mean-return model performs comparably to market models):

| asset class | model | reason |
|---|---|---|
| crude — brent, wti | **constant mean**: `r = α + ε` | there is no exogenous oil-market factor distinct from the asset itself |
| cracks — diesel, gasoline | **market model**: `r = α + β·r_brent + ε` | a crack is a margin; its expected move **given crude** is exactly what must be removed |
| gas — henry hub, propane | **constant mean** | no registered factor; stated rather than assumed |

`α` and `β` are estimated on the estimation window only, by OLS on daily log returns, and are therefore
knowable at `t`. The abnormal cumulative return over horizon `h` is

    AR(t,h) = [ log P(t+h) − log P(t−1) ] − h · α̂ − β̂ · [ log F(t+h) − log F(t−1) ]

with `β̂ = 0` for the constant-mean assets. Everything else — retrieval, k, τ, the four specifications,
the baselines, the cluster structure, the inference — is **unchanged**, so any movement is attributable to
the target and to nothing else.

### A2.2 Both targets are published, and the raw one is not withdrawn
The run publishes the raw-return result and the abnormal-return result **side by side**. The raw result is
the one the paper reported and it stays on the record. This is a test of A1's claim, not a replacement of
the evidence.

### A2.3 What each outcome means, written before the numbers
- **The null holds on abnormal returns too** → A1 is a real design criticism but not the *cause* of the
  null. The price arm was measuring the right thing badly, and it still finds nothing. The finding
  survives and is **strengthened**, because the most obvious alternative explanation is now closed.
- **The engine beats climatology on abnormal returns** → **A1 was fatal and the published price null is an
  artefact of the target.** The paper's price section would be wrong and must be rewritten, not annotated.
- **The engine gets worse** → the market model removed signal the engine was using, which would say the
  engine's apparent competence on raw returns was tracking the oil market rather than the event.

All three are publishable. The registered gate score is unchanged (CRPS); `n_dropped_short_estimation_window`
is published beside every block.
