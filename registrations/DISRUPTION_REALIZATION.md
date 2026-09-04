# Physical impairment of maritime oil chokepoints — registration

**Registered 2026-09-04, before `src/disruption_episodes.py` existed and before any impairment
episode, linkage table or price quantity was computed under this design.** Changes after the first
detector run require a dated amendment appended below.

Attribution required by licence: **Sources: UN Global Platform; IMF PortWatch.**

## 24. Prior inspection, disclosed first because it conditions everything else

The following were viewed **before** this registration was written and are exploratory knowledge,
not blinded confirmation:

1. A preliminary "days more than 25% below a one-year trailing baseline" count by route and year.
   It showed Bab el-Mandeb 268 such days in 2024, Suez 210 in 2024, Hormuz 214 in 2026.
2. The timing of low-traffic days: all Hormuz days at ≤2 tankers fall in 2026 beginning 2026-03-02,
   and Suez's two such days are 2021-03-25/26. These were used in `docs/audit/V3_DATA_AUDIT.md` §3
   to establish that **zeros are genuine traffic rather than encoded missingness**, which is a
   data-quality question, not a hypothesis test.
3. The distribution of observed/baseline ratios per route (percentiles only, no event or price
   data), used to set the threshold in §8 below.

**Consequence, stated plainly: the detector's parameters were chosen by an author who had already
seen where the largest declines fall in time.** They were not chosen to maximise agreement with any
event, and no price data has been inspected at any point. The two-day lead in the linkage window
(§16) is the one parameter where prior observation could have influenced the choice, and it is
flagged there. A reader should treat this phase's outputs as **registered but not blind**, and
weight the sensitivity grid (§8) accordingly.

## 1. Research question

> Between 2020-01-31 and 2026-08-30, when did tanker transits through major maritime oil chokepoints
> fall materially below their own trailing norm, how large and how long were those declines, and can
> they be deterministically linked to events in the project's 313-event catalogue?

This phase is **descriptive and feasibility-establishing**. It makes no causal claim and runs no
confirmatory hypothesis test.

## 2. Observational unit

**Detection:** the route-day. Seven routes × 2,404 eligible days.
**Episode table:** the impairment episode — a maximal run of impaired route-days under §9–§11.
**Linkage (if valid):** the catalogue event, restricted to the eligible set defined in §15.

## 3. Exact series used

Primary: `portwatch.<route>.n_tanker` (tankers/day).
Registered secondary, reported but not primary: `portwatch.<route>.capacity_tanker` (metric
tons/day). `n_total` is not used — it includes non-tanker vessels.

**Impairment routes (6):** `hormuz`, `suez`, `bab_el_mandeb`, `bosporus`, `malacca`, `panama`.
**Diagnostic route (1):** `cape_of_good_hope`. It is a diversion destination; its expected sign is
opposite. **A decline at the Cape is never an impairment episode.** It is reported only as a
rerouting indicator alongside Suez and Bab el-Mandeb.

## 4. Coverage period

Input spans 2019-01-01 … 2026-08-30 (2,799 contiguous daily observations per series, 0 gaps, 0
nulls). The baseline in §6 requires 395 days of history, so **detection covers 2020-01-31 …
2026-08-30**, 2,404 route-days per route.

**Registered cost:** all of 2019 is outside the detection window. Three otherwise-eligible
catalogue events (2019-05-12, 2019-06-13, 2019-07-19) are excluded by this, reducing the linkage
denominator from 21 to **18**. This is accepted in advance rather than adjusted afterwards.

## 5. Missing-data treatment

The current snapshot has no missing observations. The detector nonetheless:

- fails loudly on any duplicate date, non-daily spacing, or null value;
- treats **zero as a valid observation**, never as missing (see `V3_DATA_AUDIT.md` §3);
- requires ≥300 non-missing observations inside the baseline window, else the route-day is
  ineligible and is counted as such rather than imputed.

## 6. Trailing baseline

For route *r* and date *t*:

> **B(t) = median of `n_tanker` over the 365 days [t−395, t−31] inclusive.**

Median, not mean, for robustness to single-day extremes. A 365-day window because daily tanker
traffic carries annual seasonality (monsoon, refinery turnaround, seasonal demand) and a full year
is the natural period. Uses **only observations strictly prior to t**.

## 7. Contamination-exclusion gap

The window ends **30 days before t**. A slow-onset disruption therefore cannot enter its own
baseline and mask itself. Thirty days is one month of shipping and is fixed a priori.

## 8. Impairment threshold

Ratio **R(t) = observed(t) / B(t)**. A route-day is **impaired when R(t) < 0.70**.

Justified from the input's own noise, with no event or price data: pooled across the six impairment
routes, **12.15%** of route-days fall below 0.70, 6.52% below 0.60, 3.44% below 0.50. A single day
30% below baseline is therefore *routine*. **The duration requirement in §9, not the threshold,
carries the identification.** 0.70 is deliberately permissive so that duration does the work.

**Preregistered sensitivity grid, symmetric about the primary, every cell reported and none
selected:** threshold ∈ {0.60, **0.70**, 0.80} × minimum duration ∈ {3, **5**, 7}, holding the
baseline at 365/30. Nine cells. The primary is (0.70, 5). No cell may be promoted after inspection.

## 9. Minimum episode duration

**5 consecutive impaired days.** Justified by cadence: maritime traffic has a strong weekly rhythm,
so any requirement of ≤2 days is dominated by weekend variation. Five days spans a business week.
This is not tuned to include or exclude any particular episode.

## 10. Allowed gap within an episode

Up to **2 consecutive non-impaired days** may fall inside an episode without ending it. A one- or
two-day rebound is within normal daily variation and should not fragment one disruption into many.

## 11. Recovery rule separating episodes

An episode ends on the last impaired day before **more than 2 consecutive non-impaired days**.
This is a **registered, bounded look-ahead of 3 days**: an episode's end date cannot be finalised
until 3 further observations exist. It is the only look-ahead in the detector, it affects only the
end boundary, and it can never create or delete an episode's start.

## 12. Magnitude and duration estimands

Per episode: `duration_days`; `trough_date` (minimum R, earliest on ties);
`fractional_impairment_at_trough` = 1 − R(trough); `mean_fractional_impairment` over impaired days;
`tanker_days_lost` = Σ over episode days of max(0, B(t) − observed(t)).

## 13. Overlapping route impairments

Episodes are detected **independently per (route, series)** and never merged across routes.
Simultaneity is reported descriptively as a co-occurrence table. Merging routes would impose a
network model this phase does not have.

## 14. Rerouting versus network impairment

Rerouting is reported as a descriptive diagnostic: Cape of Good Hope transits during Suez and Bab
el-Mandeb episodes, relative to the Cape's own baseline. **No test.** Rising Cape traffic during a
Red Sea decline is consistent with diversion; it does not establish it.

## 15. Event-to-route geography mapping

Fixed here, before linkage runs, from `event_entities.role='location'` joined to `entities`. This
mapping was created by earlier sessions for other purposes and **predates all v3 work**, so it is
exogenous to the detector.

| location entity | route |
|---|---|
| `chokepoint.hormuz` | `hormuz` |
| `chokepoint.bab_el_mandeb` | `bab_el_mandeb` |
| `chokepoint.suez`, `chokepoint.suez_canal` | `suez` |
| `chokepoint.bosporus` | `bosporus` |
| `chokepoint.malacca` | `malacca` |
| `chokepoint.panama` | `panama` |

Unmapped and therefore ineligible: `druzhba_pipeline`, `kirkuk_ceyhan_pipeline`,
`cpc_novorossiysk`, `libya_es_sider`, `gibraltar_strait`, `taiwan_strait`. **No event may be
assigned a route by hand after episodes are visible.**

Eligibility attrition, registered as the only permitted denominator chain:

> 313 catalogue events → 171 dated 2019-01-01 or later → 75 carrying a `location` entity → 21
> mapping to a PortWatch route → **18 inside the detection window (§4)**

## 16. Temporal linkage window

An eligible event dated *d* is **linked** if an episode on its mapped route has
`start_date ∈ [d − 2, d + 14]`.

The +14 reflects that a physical shipping response to a declared event should begin within two
weeks. **The −2 lead is flagged under §24:** vessels divert on warning rather than on
announcement, which is the a priori justification, but the author had already observed that Hormuz
transits fell on 2026-03-02 against an event dated 2026-03-04. A reader should treat the −2 as
potentially informed by that observation. Linkage counts under a strict [d, d+14] window are
reported alongside, so the choice is visible rather than load-bearing.

## 17. Primary descriptive estimands

1. Episode count by route and year, with duration and magnitude distributions.
2. **A.** Of eligible catalogue events, the proportion linked to a detected episode.
3. **B.** Of detected episodes, the proportion linked to an eligible catalogue event.
4. Co-occurrence of episodes across routes.
5. Cape of Good Hope behaviour during Suez / Bab el-Mandeb episodes.

Proportions carry Wilson intervals. **With an 18-event denominator these are descriptive; no
inference is claimed.**

## 18. Confirmatory tests

**None in this phase.** Registered now for the eventual full study, at most two:

- **C1:** conditional on a detected episode, does episode magnitude predict the sign and size of the
  subsequent oil-price response beyond event class?
- **C2:** among eligible events, does the presence of realized impairment predict a persistent price
  response where the event label does not?

Neither may be run until a separate registration fixes the price estimand, and neither may be run
on the 18-event denominator.

## 19. Multiplicity

C1 and C2 would be corrected by Holm at family α = 0.05, unadjusted and adjusted *p* both
published. The nine sensitivity cells are **not** hypothesis tests and are reported as a grid.

## 20. Uncertainty

Proportions: Wilson score intervals. Episode-level summaries: empirical distributions with
quartiles, not parametric intervals. Any future paired comparison reuses the existing
`paired_block` stationary-bootstrap machinery with `SEED = 19900802`.

## 21. Null interpretations, fixed in advance

- **Few eligible events link to impairment** → declaration and physical realization diverge in this
  catalogue. Reported as a property of *these 18 events*, never generalised to declarations at
  large.
- **Most eligible events link** → declaration tracks realization for route-mapped events.
- **Many episodes are unmatched** → reported strictly as **"not matched to the current event
  catalogue"**. The catalogue is not a declaration census (`V3_DATA_AUDIT.md` §10), so the words
  *silent*, *undeclared*, *unexpected* and *ignored* are prohibited.
- **Too few eligible events** → the honest outcome is that linkage is identifiable but underpowered,
  and that is a complete result for this phase.

## 22. Data and provenance limitations

- `as_of` equals `obs_date` on all PortWatch rows, so **no revision history exists**. Values are as
  currently published, and the detector cannot be made vintage-aware. This phase is retrospective
  and does not claim real-time availability.
- Transit **counts** are not delivered **volume**; `capacity_tanker` is nearer and is secondary.
- Upstream AIS inputs are third-party, not held, and not reproducible here. The committed daily
  aggregate slice is redistributable under IMF terms with attribution.
- The 313-event catalogue is curated and not a comprehensive census of declarations.

## 23. Tested versus not tested

**Tested in this phase:** whether transit declines meeting a fixed, preregistered rule exist; their
count, size and duration; whether deterministic linkage to the catalogue is identifiable; and the
two proportions in §17.

**Not tested:** anything causal; whether an event *caused* a decline; whether a decline moved any
price; whether declarations outside this catalogue exist; whether counts track volumes; whether
these routes represent global oil transport; whether the result generalises beyond 2020–2026.

---

## Amendment 1 — episode-duration reading (2026-09-04, before the first detector run)

**No episode, linkage or price quantity has been computed under this registration at the time of
this amendment.**

§9 says "5 consecutive impaired days" while §10 permits up to 2 non-impaired days inside an
episode. Read strictly together these conflict: a run containing a tolerated gap has no 5
*consecutive* impaired days. The ambiguity is resolved now, before any output exists, rather than
after seeing which reading gives more episodes.

**Registered reading.** An episode is a maximal run of route-days bounded by more than `MAX_GAP`
consecutive non-impaired days (§11). It **qualifies** when it contains **at least 5 impaired days
in total**, whether or not those days are strictly contiguous. Both counts are published for every
episode: `n_impaired_days` (the qualifying count) and `duration_days` (the calendar span from first
to last impaired day).

This is the more permissive of the two readings and is chosen for that reason: it cannot suppress a
real disruption that briefly rebounded, and the stricter reading is recoverable from the published
columns by filtering on `n_impaired_days == duration_days`. The nine-cell sensitivity grid in §8
varies the minimum against this same definition.

## Amendment 2 — corrected eligibility arithmetic (2026-09-04, after the linkage run)

§15's attrition chain (313 → 171 → 75 → 21 → 18) was **arithmetically wrong**. It applied the
2019 date filter at the route-mapping step, then subtracted only the three 2019 events. It
therefore omitted seven pre-2019 route-mapped events and the 2020-01-03 Soleimani event, which
falls before the 2020-01-31 detection start.

The correct chain, computed by `src/disruption_linkage.py`:

> 313 catalogue events → **28** carrying a `location` entity mapped to a PortWatch route → 11
> dated before 2020-01-31 → **17 eligible**

This is recorded as a correction rather than a silent restatement. It changes the denominator of
estimand A from 18 to 17 and does not change any detector parameter, any episode, or the reported
count of linked events. `docs/audit/V3_LINKAGE_FEASIBILITY.md` uses the corrected chain throughout.

## Amendment 3 — linkage rule declared unusable (2026-09-04, after the linkage run)

The §16 onset-window rule was run once, exactly as registered, and its output is published. It is
now declared **not fit for purpose**, and its proportions may not be quoted as findings. Three
failure modes, evidenced in `docs/audit/V3_LINKAGE_FEASIBILITY.md`:

1. The largest episode in the record (Hormuz, 183 days at full impairment) is excluded by a
   one-day margin, because traffic collapsed three days before the declaration and the registered
   lead is two.
2. Slow-onset disruptions fall outside the 14-day lag; the Red Sea campaign's declaring events sit
   27 and 39 days ahead of sustained onset.
3. Events occurring *inside* an ongoing episode can never link, because linkage keys on episode
   onset. Four Houthi events fall within one 242-day episode and none count.

**The window has not been widened.** Changing it now, having seen that a wider lead would capture
the Hormuz closure, is the post-hoc tuning this registration exists to prevent. A corrected rule —
overlap-based rather than onset-based, with an asymmetric window justified independently of these
episodes — requires a new registration written before it is run, and a larger eligible set than 17.
