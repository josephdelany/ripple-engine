# Resume lines and application material

*2026-09-03. Every figure here is current as of run `walk_20260903T052633Z` and traceable to a
named file. Nothing is rounded in the project's favour.*

---

## The one-line version (resume, project header)

> **Ripple Engine** — pre-registered walk-forward test of whether historical analogy predicts
> geopolitical escalation and oil prices once hindsight is removed. Python · 27 academic and
> government datasets · [github.com/josephdelany/ripple-engine](https://github.com/josephdelany/ripple-engine)

## Bullets — pick three or four

**Research design**
- Designed and pre-registered a walk-forward forecasting test over **313 dated geopolitical and
  oil-policy shocks (1956–2026)**, with each forecast sealed by SHA-256 hash before its outcome
  was looked up, and a verdict rule fixed in writing before any result was computed.
- Derived the three conditions a state-conditioned analog forecaster requires — observability of
  state at the forecast date, density of the reference pool, non-degeneracy of the target — and
  **measured all three failing**, converting a null result into a specification of when the method
  class must fail.
- Established the study's central finding: enforcing a strict point-in-time information constraint
  revealed that **262 of 313 events had no state variable demonstrably available on the day**, and
  the apparent predictive skill disappeared with it — the signal had been hindsight.

**Data and engineering**
- Assembled a **352,000-row world-state panel from 27 academic and government sources** (Correlates
  of War, ICB, UCDP, ATOP, Polity, V-Dem, SIPRI, Archigos, UNGA ideal points, GPR, EIA, CFTC, World
  Bank, IMF, FRED, Energy Institute) joined to each event under a vintage rule, plus **772 price and
  macro series** back to 1946.
- Built the evaluation in Python with proper scoring rules (Brier, CRPS, RPS) and a full inference
  battery: Diebold–Mariano with small-sample correction, stationary block bootstrap, White Reality
  Check / Hansen SPA across a model family, label permutation, matched placebo, regime blocks, and a
  **162-specification curve** — negative in all 162 settings.
- Scaled the evaluation by an order of magnitude with a date-grid study (**10,857 scored cells**),
  computing *effective* rather than nominal sample size throughout — 50× the rows delivered 7.9× the
  power, and the study reports both.

**Integrity and review apparatus** *(the distinctive part — lead with this for consulting)*
- Ran the project as **seven parallel AI engineering sessions under a registration discipline**
  where every amendment was committed before the code it governed, and built the apparatus that
  makes AI-produced research auditable: a citation guard that fails when prose drifts from its
  source file, a filtration audit of **15,241 point-in-time checks**, an interval audit of every
  estimator in the project, and a test suite that refuses to report green when it has not run.
- **Published four retractions of the project's own positive findings**, three of them found by the
  component that had produced the finding while re-examining its own result — including a corrected
  *p*-value that moved a headline from 0.010 to 0.052 and cost the paper a claim.
- Wrote and published an **adversarial audit of the project's own weaknesses**, scoring each by
  exposure rather than by scientific interest.

---

## Cover-letter paragraph

> My main independent project tested a claim that geopolitical risk analysis relies on and rarely
> examines: that historical precedent predicts how a crisis will unfold. I built a forecasting
> system over 313 dated shocks and a world-state panel drawn from 27 academic and government
> datasets, then ran it forward through the record under a pre-registered protocol — each forecast
> sealed by hash before the outcome was looked up. The central result was negative and specific:
> enforcing a strict point-in-time constraint revealed that most of my events had no state
> information provably available on the day, and the apparent skill vanished with it. What I take
> from it is less about oil than about method — a model can look like it is extracting historical
> structure when it is really consuming variables built with later knowledge, and the only defence
> is an apparatus that checks you rather than a resolution to be careful. Building that apparatus,
> and publishing the four retractions it produced, is the part of the project I would most want to
> talk about.

---

## Every claim above, sourced

| claim | where it is verified |
|---|---|
| 313 events, 1956–2026 | `oil.db` `events`; `docs/PAPER_DRAFT.md` §3 |
| 27 sources; 352k-row panel; 772 series | §3; `WORLD_STATE_SOURCES.md` |
| 262 of 313 with no knowable state | `data/state/situation_knowable.json`; §8 |
| three conditions, all measured failing | §1.1, §13.1 |
| escalation skill −0.084, CI [−0.175, +0.004], *p* = 0.076, n = 100 | `summary.json` · `tiers.daily.G.engine_vs.climatology` |
| price CRPS +0.134 vs persistence, *p* < 0.001 | `tiers.daily.P.engine_vs.persistence` |
| 162 specifications, none positive | `spec_curve`; §9 |
| 10,857 grid cells; 50× rows → 7.9× power | `data/grid/price/summary.json`; `data/grid/power_arithmetic.json` |
| 15,241 filtration checks, 0 violations | `filtration_audit` |
| four retractions | §10, §12, §12.2 |
| interval audit | `docs/INTERVAL_AUDIT_2026-09-03.md` |
| adversarial audit | `docs/ADVERSARIAL_AUDIT.md` |

## Two things not to say

- **Not** "I proved historical analogy doesn't work." Say: *this implementation, under a strict
  point-in-time constraint, did not outperform simple baselines — and here are the three conditions
  that failed.*
- **Not** "I built it myself" if asked whether the code is yours. Say: *I directed it and own every
  registered decision; implementation was AI-assisted across parallel sessions, and the review
  apparatus is what makes that auditable.* The apparatus is the more transferable skill.
