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
publication lag below is fixed *before* implementation, is capped at five years, is set
deliberately long, and may not be revised after any loss is computed. If a declared lag turns out
to be wrong, the correction is a dated amendment stating the documentary basis, made before
re-running, and the pre-correction result is published alongside. See the provenance note on the
lag table — they are conservative declarations awaiting confirmation, not figures read off
publisher documentation at registration time.

**This measures counterfactual availability, not demonstrated availability.** The claim it can
support is "had these variables been available on their sources' ordinary release schedules, structural
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

## Amendment 1 — 2026-09-03, before implementation or outcome computation

An independent executability audit found that the source-family lag design above is not defensible
from the frozen bundle. This amendment supersedes the conflicting provisions above. No forecast,
loss, CRPS, contrast, or outcome-conditioned quantity under either availability rule has been
computed. Only source strings, field coverage, stored dates, and loader semantics were inspected.

### Corrected estimand and name

This is the **schedule-imputed finalized-data sensitivity arm**, not a contemporaneous-availability
arm. It asks whether the registered equal-block similarity rule gains predictive accuracy when
finalized geopolitical data are aligned to the nominal availability dates already encoded by their
loaders. It cannot prove what an analyst actually knew, because modern finalized datasets may
contain later corrections or coding decisions. A favorable result supports only this representation
and weighting rule on this frozen record. An unfavorable result shows no demonstrated increment for
this operationalization; it does not establish that wider state contains no information.

### Corrected availability rule

The family-specific lag table and `obs_date + L(source)` rule above are withdrawn. Loaders already
encode nominal availability in `vintage` (for example annual COW/Polity at Y+1, SIPRI at Y+1 May,
WDI at Y+1 July, and event-derived rolling variables at their calculated as-of date). Adding another
lag would double-lag some sources. The frozen bundle also contains one selected row per
event/entity/field, so it cannot fall back to an earlier observation after a second lag rejects the
selected row.

A panel row is admitted exactly when:

1. `entity_id != "situation"`;
2. `retrospective == 0`;
3. `obs_date <= event_date`; and
4. `vintage <= event_date`.

`release` is recorded as provenance for the modern file actually parsed and is ignored in this
sensitivity. The claim that conservative under-admission cannot create a false positive is withdrawn:
missingness and selection can change rankings in either direction.

### Frozen field allowlist

Only the following non-market fields may enter. This list was frozen from the registered codebook
and bundle metadata before inspecting outcomes:

- Physical: `spare_capacity_opec`, `us_crude_stocks_xspr`, `us_spr_stock`,
  `us_refinery_utilization`.
- Actors: `cinc`, `milex_cow`, `milper_cow`, `milex_sipri`,
  `milex_gdp_share_sipri`, `polity2`, `polity_durable`, `leader_tenure_days`,
  `leader_change_last_365d`, `oil_rents_gdp`, `coup_last_5y`.
- Dyads: `atop_defense_pact`, `atop_any_obligation`, `mid_count_10y`,
  `mid_max_hostlev_10y`, `mid_last_date`, `icb_crisis_count`,
  `icb_last_outcome_form`, `icb_last_violence`, `icb_last_tension`,
  `unga_ideal_point_distance`.
- System: `ucdp_active_conflicts`, `ucdp_intensity_max`, `ucdp_battle_deaths`,
  `mepv_regional_war`.

Market, derived-market, narrative, retrospective, and corpus-derived OPEC fields are excluded from
the panel component. In particular, `wti_monthly`, `brent_daily`, `wti_daily`, `diesel_crack`,
`curve_m1_m4_spread`, `vix`, `ovx`, `cot_managed_money_net`, and `opec_decision_dated` may not enter
it. The four already-frozen market-vector fields remain the complete market block. Sentinel source
strings representing no MID, ICB crisis, or ATOP obligation are accepted only for their allowlisted
fields; there is no source-prefix inference and no source-lag map. Eligibility fails closed unless
the row's source is exactly one of:

- `EIA STEO Table 3d, surplus crude oil production capacity (STEO_m.xlsx)`
- `EIA https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCESTUS1&f=W (series eia.crude_stocks_xspr; bridge)`
- `EIA https://www.eia.gov/petroleum/ (series eia.spr_stocks; bridge)`
- `EIA https://www.eia.gov/petroleum/ (series eia.refinery_util; bridge)`
- `COW National Material Capabilities v7.0 (NMC-70-abridged.csv)`
- `Archigos v4.1 (Archigos_4.1_stata14.dta)`
- `Polity5 (p5v2018.xls, local file)`
- `SIPRI Military Expenditure Database (local file)`
- `World Bank WDI NY.GDP.PETR.RT.ZS (api.worldbank.org/v2)`
- `CSP Coups d'Etat 1946-2021 (CSPCoupsAnnualv2021.xls, local file)`
- `CSP Major Episodes of Political Violence 1946-2018 (MEPVv2018.xls, local file)`
- `UCDP/PRIO Armed Conflict v26.1 + UCDP Battle-Related Deaths v26.1`
- `COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)`
- `COW dyadic MID 4.03: no dispute listed (absent = none)`
- `ICB v16 system level + dyads (Duke)`
- `ICB v16: no crisis listed for the dyad (absent = none)`
- `ATOP 5.1 directed dyad-year (atop5_1ddyr.csv)`
- `ATOP 5.1: no obligation listed (absent = none)`
- `UNGA ideal points, Bailey-Strezhnev-Voeten (IdealpointestimatesAll_Jun2024.csv)`

### Frozen support and arms

Every scored date reuses the exact candidate IDs, outcome atoms, realized outcome, and date set from
the 264 frozen central reads. State availability cannot add, remove, or reorder candidates. Only
distances and weights are recomputed.

The comparison is symmetric: both the target and each historical analogue use the snapshot keyed
to their own event date. It does not reconstruct what the target-date analyst later knew about the
historical analogue; that alternative information set is outside this analysis.

The primary arms are market-only, availability-state (the market block plus every admitted
allowlisted non-market block), and event class, all matched to a common per-date effective sample
size using the already registered deterministic procedure. Uniform and unmatched arms are
descriptive. Non-market-only is an explicitly labeled diagnostic restricted to dates where it is
defined; it is not on identical date support and cannot enter the primary family.

The two primary contrasts and Holm correction remain, but their decision language is replaced:

- C1 tests whether the registered equal-block availability-state operationalization improves on
  market-only weighting on this frozen record.
- C2 tests whether that operationalization improves on event-class weighting on this frozen record.

C1 is favorable only when its interval excludes zero in the favorable direction and its
Holm-adjusted *p* is below 0.05. A null must be reported as “no demonstrated incremental forecast
improvement for this operationalization,” with realized sample size, field/block coverage, and
effective sample sizes. C2 cannot rescue a null C1. Neither contrast licenses a claim about actual
historical analyst knowledge or about every possible representation of wider state.

### Pre-outcome coverage and power correction

The statement above that at most 227 events carry non-market state is withdrawn. Before any outcome
inspection, metadata show UCDP fields for 294–313 events, actor fields for roughly 223–227, physical
fields for 37–114, and dyadic/alignment fields for roughly 34–42. These are row/event coverage counts,
not effective power: pairwise block availability on the exact frozen supports must be published by
the run. A null can reflect coverage, encoding, aggregation, scaling, missingness, or low power and
cannot be translated into “the underlying state contains no information.”

### Output correction

The output directory and files remain as registered, except `source_lag_map.json` is replaced by
`field_admission.json`, which records the exact allowlist, admitted/excluded row counts by field and
block, and exclusions by rule. Tests must additionally prove exact frozen support against all 264
central reads and prove that no field outside the allowlist enters a distance.
