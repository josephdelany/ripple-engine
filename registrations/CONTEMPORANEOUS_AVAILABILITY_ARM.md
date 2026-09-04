# Contemporaneous-availability state arm — registration

**Registered 2026-09-03, before any implementation and before any loss, score or contrast under
this rule has been computed.** Nothing in this document may be changed after the first execution
except by a dated amendment appended below.

## Why this exists

The frozen central experiment admits a state value only when the *release date of the dataset
version* precedes the event (`src/structural_surface_experiment.py`, `strict_panel_rows`). Over the
11,029 panel rows in the committed bundle, that clause alone excludes 10,150, while observation
dates exclude 0 and vintages exclude 0
(`docs/audit/UNUSED_DATA_INVENTORY.md`, `tests/test_unused_data_inventory.py`).

The consequence is mechanical rather than substantive. Polity5 was released in 2018, COW NMC v7.0
and SIPRI and UCDP v26.1 later still, so for a 1990 event every modern compilation fails by
decades. Polity (227 events), CINC and military expenditure (227), UCDP conflict intensity
(294–313), alliance and alignment fields are all collected at real coverage and all reduced to
between 0 and 3 usable rows. Only the two Archigos leader fields survive, and only because their
release metadata happened to be recorded differently.

So the registered rule does not measure what an analyst could have known in 1990. It measures
whether *that particular file* existed in 1990. That is a defensible thing to have tested — it is
the strictest possible reading and it is why the paper's availability claim is conservative — but
it means the project's founding question, whether correspondence across the wider geopolitical
state beats matching on labels, is **untested rather than answered**. This registration defines
the analysis that would test it.

## What this is not

**This does not replace, reopen, or re-score the frozen experiment.** The central result and the
registered component ablation stand exactly as published. This is a separate arm answering a
different question, and it must be reported as such.

**This is not the strict rule loosened until something appears.** Relaxing a filter after seeing it
produce a null is the move `INV-6` exists to prevent. The guard against it is that every
publication lag below is fixed from source documentation *before* implementation, is capped, and
may not be revised after any loss is computed. If a declared lag turns out to be wrong, the
correction is a dated amendment stating the documentary basis, made before re-running, and the
pre-correction result is published alongside.

**This measures counterfactual availability, not demonstrated availability.** The claim it can
support is "had these variables been available on their sources' documented schedules, structural
correspondence would/would not have beaten event class". It can never support "analysts had this
information". The paper's §5 finding — that availability *could not be demonstrated* from the
recorded metadata — is unaffected and remains the honest statement about the historical record.

## Prior inspection, disclosed

Before writing this, the following were computed and are descriptive only: per-field row and event
counts, the four-way decomposition of exclusion reasons, and which fields survive the strict rule.
**No outcome, loss, CRPS, difference or contrast under any relaxed rule has been computed by
anyone.** The frozen experiment's own losses were read, but those are already published.

## Fixed design

Identical to the frozen experiment in every respect except the availability rule. Specifically
unchanged and not re-openable: the 313-event catalogue and committed input bundle; the 20-trading-day
abnormal Brent return and its constant-mean estimation window; the candidate-eligibility rule (prior,
outcome-closed, usable target, no same-class filter); `MIN_POOL = 8`; `MIN_FIELDS = 3`;
`MIN_SCALE_N = 30`; the equal-block distance; weighted CRPS; the `paired_block` inference with
`SEED = 19900802` and `n_boot = 2000`; and the seal-before-outcome order.

### The replacement availability rule

A state row is admissible when **all** of:

1. `entity_id != 'situation'` (unchanged).
2. `retrospective = 0` (unchanged). Retrospective reconstructions — historical GPR, Kilian IGREA,
   `diplomatic_representation`, `surplus_capacity_world` — are **permanently excluded**. They have
   no contemporaneous equivalent by construction, and admitting them would be the lookahead this
   project exists to avoid.
3. `obs_date <= event_date` (unchanged).
4. `obs_date + L(source) <= event_date`, where `L` is the declared publication lag below.

Clause 4 **replaces** `release <= event_date` and `vintage <= event_date`. Clauses 1–3 are the
frozen rule's other three clauses, unchanged.

### Declared publication lags

Fixed now, before implementation. **Provenance of these numbers, stated plainly: they are declared
from general knowledge of these sources' release cadence and were deliberately set long, not read
off the publishers' documentation during registration.** Each must be confirmed against the
source's own release history as the first step of implementation, and any correction made as a
dated amendment below **before** anything is computed — never after seeing a loss. Where confirmation
is impossible, the lag is set to the 5-year ceiling or the source is dropped, and which of the two
was chosen is published. A source not listed here is **not admissible**; the list may not be
extended after implementation except by dated amendment.

The bias is deliberate and one-directional: every lag is long enough to be conservative, so an
error makes the arm admit *less* data than a contemporaneous analyst would have had, never more.
An arm that under-admits can produce a false null but cannot manufacture a false positive.

| source family | lag `L` | basis |
|---|---:|---|
| Archigos (leader tenure, leader change) | 0 days | event-dated at occurrence; matches the frozen rule, which already admits it |
| COW Dyadic MID, COW National Material Capabilities | 5 years | quinquennial-to-irregular release; deliberately conservative |
| UCDP/PRIO Armed Conflict, UCDP Battle-Related Deaths | 1 year | annual release in the year following the observation year |
| Polity (regime, durability) | 2 years | annual update published with roughly a one-to-two-year lag |
| SIPRI military expenditure | 1 year | annual April release covering the prior year |
| CSP Coups d'État, CSP Major Episodes of Political Violence | 2 years | annual update, irregular publication |
| ATOP (alliance obligations) | 5 years | periodic version releases |
| ICB (crisis counts and outcomes) | 5 years | periodic version releases |
| UNGA ideal-point distance | 2 years | annual session-based estimates, published after the session |
| World Bank oil rents (`oil_rents_gdp`) | 2 years | WDI annual release lag |
| market series already in the vector | unchanged | governed by stored `as_of`, not by this rule |

Where a source appears under several `source` strings in `situation_state`, the mapping from string
to family is by exact prefix match, resolved and committed in code **before** the first run, and
published as a table in the outputs. Any row whose source string matches no declared family is
excluded and counted.

**Ceiling.** No lag exceeds 5 years. Any future proposal to exceed it requires a dated amendment
with the documentary citation, made before re-running.

## Arms

All on identical support, identical atoms, identical outcomes.

1. **Uniform** — equal weight over the frozen candidate pool.
2. **Market-only** — the market block alone.
3. **Availability-state** — the equal-block distance over every field admissible under the rule
   above, market included.
4. **Non-market-only** — the equal-block distance over admissible non-market blocks alone, on the
   dates where at least one exists.
5. **Event class** — the frozen surface rule.

Arms 2–5 are additionally reported at a **common effective sample size**, matched per date by the
procedure registered in `registrations/STRUCTURAL_COMPONENT_ABLATION.md` Amendment 1, so
representation is never confounded with concentration. The ESS-matched contrasts are primary; the
unmatched ones are descriptive.

## Primary contrasts and decision rules

Two, and only two, with Holm correction across their DM *p*-values at family alpha 0.05:

- **C1: ESS-matched availability-state minus ESS-matched market-only.** Does the wider
  geopolitical state add information beyond market conditioning?
- **C2: ESS-matched availability-state minus ESS-matched event class.** Does it beat labels?

Declared before computation:

- The full-state question is **answered affirmatively** only if C1's 95% interval excludes zero in
  the favourable direction **and** its Holm-adjusted *p* < 0.05. Nothing else counts, including a
  favourable point estimate with an interval crossing zero.
- If C1 is null, the registered conclusion is that **the wider state adds no demonstrated
  information even when availability is granted counterfactually** — which is a materially stronger
  and more interesting negative result than the present "untested", and it must be published as the
  headline of this arm rather than buried.
- C2 cannot rescue C1. If C2 is favourable and C1 is null, the finding remains that market context
  drives the advantage, matching the frozen ablation.
- No subgroup, horizon, bandwidth, lag revision or field subset may change these readings.

## Power, stated in advance

At most 227 events carry any non-market field, and the pool minimum of 8 and field minimum of 3
will reduce that further. **A null on C1 will therefore be ambiguous between "no information" and
"insufficient power", and the report must say so with the realised n and effective sample sizes
rather than claiming an absence of effect.** The realised n is published whatever the outcome.

## Outputs and tests

Write only under `data/structural_surface/availability/`: `scores.jsonl`, `summary.json`,
`manifest.json`, plus `source_lag_map.json` recording the source-string-to-family resolution and
the count of rows excluded for matching no family. The manifest hashes the frozen input bundle and
every output, and records this registration's commit separately from the implementation and
execution commits.

Tests must: reconstruct weights and CRPS for fixed examples independently; prove identical support,
atoms and outcomes across all arms and against the frozen experiment; prove the lag map is read
from this document's table and not computed from data; prove no admissibility decision reads an
outcome; prove `retrospective = 1` rows are never admitted; verify the ESS matching numerically;
publish the realised admissible-field counts; and reproduce every output byte-for-byte from a clean
checkout.

## Status

**Registered and not run.** No implementation exists at the time of registration. Whoever executes
this must do so under the rules above without modification, and must publish the result whichever
way it falls.
