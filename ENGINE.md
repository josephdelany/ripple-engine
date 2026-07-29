# THE ENGINE — one system, honestly tiered
<!-- Canonical architecture. Resolves the "two engines" problem: there is ONE engine, the
Conditioned Ripple Engine, with a VALIDATED core, EXPERIMENTAL extensions (in the penalty box
until they earn skill), and DESCRIPTIVE context. Nothing surfaces as an edge until it is
scored. Written 2026-07-28 after closing #1 (registered study) and validating #2 (analogue). -->

## What it is (one sentence)
A **Conditioned Ripple Engine**: from decades of data it learns the *shape* of how a shock
type ripples through oil (Layer A), measures the *live state* that amplifies or dampens it
(Layer B), multiplies them into a **state-conditioned forecast**, compares that to **what the
market has priced** (the gap), and scores every claim it makes (the ledger). Stories are the
human view; the market is the null hypothesis.

## The "two engines" were one, mis-described. The real structure is one hierarchy:

```
  LAYER A — BASE RATES (the ripple)         event_study.py / cross_asset.py
     CAR by event type over 52 sourced shocks. METHOD: event study. STATUS: standard, sound.
        ×
  LAYER B — LIVE STATE (the amplifiers)     derive_signals.py / conditioned_study.py
     VIX %ile, inventory sigma, COT %ile, ... measured point-in-time at t-1.
        =
  A×B — THE CONDITIONED FORECAST            conditioned_study.py / engine_read.py / scenario.py
     state-dependent ripple magnitude. THIS IS THE VALIDATED CORE (see status table).
        |
  CANDIDATE METHODS (under validation)      analogue.py / gpr_signal.py / propagation.py
     alternative predictors racing the core; promoted only when they beat it OOS.
        |
  THE GAP                                    divergence.py / gpr_signal.py (source-aware)
     system read vs priced belief. DESCRIPTIVE until a scored gap backs it.
        |
  THE LEDGER (accountability)               auto_forecast.py / resolve_reads.py / calibrate.py
     every forecast -> resolve -> Brier. The spine that turns claims into a track record.
        |
  MEMORY + STORIES + SURFACE                situation.py / story.py / backend.py / mcp_server.py
     tracked narratives (view) + OpenBB widgets + natural-language query.
```

Data spine: one SQLite DB (`data/oil.db`, 10 tables), point-in-time (`as_of`/`retrieved_at`,
no lookahead). ~15 free feeds in; autonomous GitHub Actions loop; self-monitoring (heartbeat).

## VALIDATION STATUS — the honest core (a quant reads this first)
| Piece | Method | Status | Evidence |
|---|---|---|---|
| **H1 — stress amplifies (VIX)** | conditioned event study | ✅ **VALIDATED (robust)** | registered n=20 **+10.3pp**; expanded n=52 **+7.4pp**, 95% CI excludes 0, survives FDR@10% — holds as N grows |
| **H2 — tight inventories amplify** | conditioned event study | ⚠️ **SAMPLE-DEPENDENT** | registered n=20 **+5.4pp** (held); expanded n=52 **+2.9pp** — decays BELOW the +5pp bar, CI includes 0 → no longer a validated edge. See `REGISTERED_SAMPLE.md` |
| **H3 — crowded positioning amplifies** | conditioned event study | ❌ **REJECTED** | clustered **−6.8pp** (n=20) / **−6.9pp** (n=52), wrong direction — reported, not buried |
| **Analogue forecaster** (P oil turbulence) | kNN over 511-shock library | ⚠️ **NO OOS EDGE (null)** | raw Brier 0.40 / LOO-isotonic 0.29 vs base-rate 0.24 → skill still **−0.05** at N=42 |
| **Source-aware gap read** | rules (global vs country GPR sign) | 🟨 **DESCRIPTIVE** | agrees with reality (oil down while Gulf risk high) but unscored |
| **Propagation graph / criticality / OPEC stress** | sourced maps | 🟨 **DESCRIPTIVE** | context, not a scored edge |

**The rule this enforces:** the only thing the engine may present as *predictive edge* today is
the **A×B conditioning via H1 (VIX stress)** — the one hypothesis robust from n=20 to n=52.
H2 is now sample-dependent (below the bar at n=52). The analogue is in the **penalty box** — visible, honestly
labelled a null, promoted to the forecast only if it beats the base rate out-of-sample. Gap and
story layers **describe**; they do not claim edge. This is what keeps it from being Frontier Alpha.

## How an experimental method gets promoted (the discipline)
1. It makes a falsifiable, point-in-time forecast the ledger can score.
2. It is validated walk-forward (leave-one-out / purged CV) — `calibrate.py`, `backtest_analogue.py`.
3. It must beat the base rate (and ideally the A×B core) OOS, with PBO checked at scale.
4. Only then does it feed the surfaced forecast. Until then it is labelled null/experimental.

The analogue's honest path to promotion is **N** — the corpus work (GDELT/OSINT archives →
a much larger analogue library), then re-run `backtest_analogue.py` + `calibrate.py`. Not tuning.

## What #1 and #2 settled (2026-07-28)
- **#1 finished:** the registered study is closed (frozen at n=20, `REGISTERED_SAMPLE.md`). On the
  registered sample 2 of 3 held (H1, H2); H3 rejected. **Under expansion to n=52, only H1 remains
  an edge** — H2 decays below the +5pp bar (sample-dependent). H1 is the honest, robust core.
- **#2 proven — as a null:** the analogue forecaster has no OOS edge at current N. Rigorously
  shown (LOO isotonic). It stays experimental until the corpus makes it earn its place.

## The honest bottom line
The engine's **science is real** (H1/H2 conditioning survived pre-registration). Its **predictive
frontier is not yet proven** (the analogue is a null). The consolidated system is honest about
which is which — and that separation, not more features, is what makes it quant-grade.
