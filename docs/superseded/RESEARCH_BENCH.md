> **SUPERSEDED — NOT A CURRENT CLAIM.** Superseded design and status material for the legacy engine. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# The Research Bench — how to interrogate the engine

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


`src/research.py` is the pull interface: you bring a question, it returns a **deterministic,
receipted answer** — a number, a confidence interval, a verdict, the sources — and nothing else.
It does not write your analysis or offer opinions. You do the thinking and the writing; the bench
is your quantitative research desk. This is what lets a solo analyst falsify their own macro
hypotheses with the rigor that normally needs a quant team.

## The four modes

**1. Test a hypothesis** — *does STATE (high/low) amplify the ripple in ASSET?*
```
python3 src/research.py test --state derived.vix_pct --asset fred.DCOILBRENTEU --sign high
```
Runs the full gate — clustered median split + cluster-bootstrap 95% CI + permutation p — and
returns **HOLDS** (CI excludes zero, perm p<0.10) or **NO SIGNIFICANT EFFECT** (honest null).
Point it at *any* state variable, asset, direction, or horizon.

**2. Query history + analogues** — *how has ASSET moved after shocks of a TYPE?* (optionally split by a state)
```
python3 src/research.py query --type conflict_escalation --horizon 20 --state derived.vix_pct
```
Returns mean CAR + 95% CI + n, the high-vs-low split, and the **sourced events** behind it.

**3. Scan what's mispriced now** — *where does the engine's view diverge from the priced market?*
```
python3 src/research.py gaps
```
The live gap + the resolving scorecard (small-N, suggestive — raw material for *your* read).

**4. See what you can test**
```
python3 src/research.py vars
```
Lists the available state variables, assets, and event types.

## Add your OWN data, then test it immediately

The bench is only as good as the corpus. Three ways to extend it — all additive, no schema change:

**Add events** (the most common):
1. Append rows to `data/events.csv` following `EVENTS_CODEBOOK.md` (every row needs a real
   `source_url`; code severity/surprise by *expected disruption / prior expectation*, never the
   price reaction).
2. `python3 src/load_events.py` (validates + loads; rejects unsourced/mis-typed rows).
3. Re-run any `research.py query`/`test` — your events are now in the corpus.

**Add a state variable** (a new conditioning signal):
1. Add it to `src/derive_signals.py` with a **declared mechanism string** (no mechanism, no metric).
2. Rebuild signals (it writes `derived.<name>` into `observations`).
3. `python3 src/research.py test --state derived.<name> --asset ...` — test your new signal.

**Add an asset** (a new ripple target):
1. Add a `fetch_<asset>.py` adapter (copy `src/fetch_series.py`; keyless FRED/EIA where possible).
2. Add it to `ASSETS` in `src/cross_asset.py` (`kind`: price | yield | weekly).
3. `python3 src/research.py test --asset fred.<ID> --state ...` — test the ripple in the new asset.

## The rules that keep it honest (don't skip these)

- **Point-in-time:** state is measured at t-1; no lookahead. The bench enforces it.
- **Multiple testing:** a single `test` is one hypothesis. If you *scan* many state×asset combos,
  correct for it (`validate.bh_fdr`) — otherwise you'll find a "signal" by luck. The engine will
  not do this for you; it's on you to not p-hack.
- **Small N:** most cells are ~90 clustered episodes or fewer. Believe the wide CIs. "No
  significant effect" is a real, publishable result — report it, don't bury it.
- **The bench tests; you judge.** It can only speak to what's measurable and priced. The
  qualitative geopolitical judgment — intent, novel scenarios, narrative — is yours, always.
