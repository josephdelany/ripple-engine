# METHOD — how the engine turns a geopolitical shock into a validated, priced consequence

> **SUPERSEDED — 2026-09-03.** This document dates from the project's v1 period (July
> 2026) and describes a "validated" portfolio that no longer exists. Every claim it calls
> validated has since been retracted or downgraded, each by a test registered before it
> ran: **H1** — geopolitical shocks amplifying ~5pp harder under volatility stress — did
> not survive a VIX-matched placebo (`docs/red_team_1.md`); **five of the six**
> stress-amplification propagation edges were retracted under a pre-registered re-test
> (`data/ripple/retraction_six.json`); the propagation chain is silent, with 21 of 477
> cells transmitting against 1–24 expected by chance (`docs/RIPPLE_FINDINGS.md`); and the
> walk-forward engine is significantly **worse** than the base rate on both targets once
> the vintage rule binds (`docs/PAPER_DRAFT.md` §8).
>
> Nothing below has been edited. This project annotates its record; it does not rewrite
> it. For the current state read `README.md`, `docs/PAPER_DRAFT.md` and `EDGE_PORTFOLIO.md`.


*The full framework, end to end. Written to be read and criticised — the opposite of a black box.
Every stage names its honesty guard, because the trustworthiness is the product.*

---

## Philosophy (one paragraph)

Incumbent tools measure **attention** (how much the world is talking about a risk) and emit a
**score**. This engine measures **consequence** — how a shock has historically rippled through the
energy complex, conditioned on the market state it lands in — and compares it to **what the market
has already priced** (the gap). Nothing is a claim until it survives out-of-sample validation with
multiple-testing correction; everything that fails is reported as a null; every number traces to a
source. It is a glass box by design, because the documented failures of the field — the conflict
"warning-response gap" and distrust of "proprietary algorithms" — are failures of *opacity*, and
opacity is the one thing a solo, honest engine can beat.

## The pipeline (each stage + its honesty guard)

1. **Event coding** (`EVENTS_CODEBOOK.md`, `load_events.py`). A curated corpus of dated,
   *sourced* geopolitical/energy shocks (currently 218, 1987–2025). *Guard:* severity/surprise are
   coded by **expected disruption and prior expectation, never the price reaction** — otherwise
   "big shocks move oil" is circular by construction. No `source_url`, not in the dataset.

2. **Point-in-time state** (`derive_signals.py`, bitemporal `observations.as_of`). The market state
   (VIX %ile, inventory σ, positioning, curve, dollar, realized vol) measured at **t−1**, the day
   before the shock. *Guard:* no lookahead — the amplifier must be observable before the event; macro
   vintages come from ALFRED (`fetch_fred_alfred.py`), not revised series.

3. **Event study** (`event_study.py`). Cumulative abnormal return (CAR) of a node around the shock,
   off a clean pre-event estimation window (t−130…t−11). *Guard:* abnormal = actual − own normal
   return; the run-up never contaminates the baseline.

4. **Conditioning** (`conditioned_study.py`, `robustness.py`). Split the ripple **magnitude**
   (|CAR|) by pre-event state (high vs low at the median). *Guard:* magnitude, not signed return, so
   opposite-signed event types don't cancel; overlapping episodes are **clustered** (a 5-week crisis
   is one observation, not three).

5. **The validation gate** (`validate.py`) — *nothing is an edge until it clears this:*
   permutation p (assumption-free at small N) · cluster-bootstrap CI (excludes zero or it's not a
   claim) · **Benjamini-Hochberg FDR + Bonferroni** (correct for testing many things) · purged
   Combinatorial CV + **PBO** (probability of backtest overfitting) · **Diebold-Mariano** (beat the
   benchmark, don't just look like it) · walk-forward (out-of-sample or it doesn't count).

6. **The propagation network** (`propagation_graph.py`). A directed graph of shock → node and
   node → node edges, each labelled **`validated | null | trap`**. *Guard:* the graph draws **only
   the edges that survive the gate**, and flags **traps** (nodes that co-move but where neither
   reliably leads — the link a naive map would sell and you'd lose on). Incumbents draw the map with
   no confidence; this one shows its own nulls.

7. **The gap** (`gaps.py`) — market-as-null. The engine's state-conditioned view vs the market's
   *implied* oil vol (OVX): under-priced-risk / over-priced-fear / aligned, resolved at +20 days and
   Brier-scored. *Guard:* no priceable anchor → descriptive only; the market is the null hypothesis.

8. **Cross-modal corroboration** (`corroborate.py`). Confidence comes from **convergence** across
   news + physical ship-transits (PortWatch) + thermal fires (FIRMS) + repricing prediction markets —
   not headline volume. *Guard:* correlated reprints collapse to one source; certainty is capped;
   "multi-modal" means confirmed beyond attention.

9. **The resolving ledger** (`resolve_reads.py`, `read_backtest.py`, `auto_forecast.py`). Every read
   and gap resolves at horizon and is Brier-scored, stratified by regime. *Guard:* the track record is
   public and includes the misses.

10. **The signal registry** (`signal_registry.py`). Each signal's status (live / experimental /
    rejected) is **derived from the validation runs, not asserted** — change the evidence and the
    label changes on the next build.

## What is validated today (the honest state)

- **H1 — VIX stress amplifies the ripple** (CI excludes 0, survives Bonferroni, holds walk-forward),
  and it **generalises down the energy spine**: crude, heating oil/diesel, and 5Y/10Y inflation
  breakevens all amplify under stress (FDR-corrected); gas, the dollar, and nominal yields are honest
  nulls. That validated backbone is the propagation network's core.
- **Suggestive, not yet validated:** the gap ledger's finding that the engine's *disagreements* with
  the market carry information (small-N, wide CIs).
- **Rejected nulls (reported, not buried):** H2 (inventories), H3 (positioning), the analogue
  forecaster, a kNN state-probability, a Kalman nowcast.

## What it does NOT do (the honest limits)

Not a supplier-mapping platform; not production trading alpha; not a forecaster of *whether* a shock
occurs. Small-N (~90 clustered episodes; some cells fewer), largely the energy channel. And the
qualitative geopolitical judgment — intent, novel scenarios, the narrative — stays the analyst's,
always. The engine is the quantitative research desk; the analyst is the analyst.

## Reproduce

`repro.sh` reproduces the pipeline; `python3 -m pytest -q` runs the hand-verifiable test suite
(89 tests); `python3 src/research.py vars` lists what you can interrogate; every artifact under
`data/*.json` carries its receipts. Free, local, deterministic, point-in-time.
