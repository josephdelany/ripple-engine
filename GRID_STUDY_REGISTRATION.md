# GRID STUDY — registration
*2026-09-03. Session B, on Joe's brief of the same date. A **new study**, not a change to the
event-triggered walk. Registered before anything under it is computed. Amendments are dated and appended.*

---

## Part 0 — standing, order of work, and what this does not touch

### 0.1 The order, and why it is this order
Joe's brief asks for two things whose order matters: *register the study fully before computing*, and
*compute the expected effective n for each multiplier before building, and publish that arithmetic first.*
These are reconciled in one sequence, and each step is committed before the next begins:

1. **Part I and Part II of this document** — the estimand and **the effective-n arithmetic registered as a
   method**, with its formulas, its data, its expected direction of error and its pre-declared drop rule.
   Committed before the code that computes it. *(this commit)*
2. **The arithmetic, as computed** — `src/engine/grid/power_arithmetic.py` → `data/grid/power_arithmetic.json`,
   published whatever it says, including for any multiplier that does not pay.
3. **Part III** — the study proper, registered in full **using** those numbers, with any multiplier the drop
   rule (§2.7) removes actually removed. Committed before the study's code.
4. The build.

Part III does not exist yet and must not be written before step 2 publishes. Nothing in steps 1–2 computes a
skill, a score or a forecast.

### 0.2 This is a different estimand, and the old results stand
The event-triggered walk asks: **given this event, what happens next?** Its unit is a corpus event; its
reads are triggered by something the corpus recorded.

This study asks: **given the world state on date t, what happens next?** Its unit is a **date** (and, for the
escalation side, a **dyad-date**). It is not a better version of the first question. It is a different
question, with a different sampling frame, a different base rate and a different set of things it can be
wrong about.

Consequently, and bindingly:
- **No number in `data/walk_forward/summary.json` is re-judged, re-scored or superseded by this study.**
  `WALK_FORWARD_PROTOCOL.md` §3 and §7 continue to govern it, and `engine:G` keeps whatever status the
  published run gave it.
- The grid study writes only to `data/grid/**`. It reads `data/walk_forward/**` and never writes there.
- Every surface that reports a grid number labels it `unit: date` (or `unit: dyad-date`), and every surface
  that reports an event-triggered number keeps `unit: event`. **The two are never pooled, never averaged and
  never compared as though they answered the same question.** A pointer from each to the other is required;
  a merged headline is forbidden.
- The protocol's information discipline (§1), sequential design (§2), proper scores (§3), inference (§6) and
  promotion rule (§7) are **inherited unchanged**, including Amendments E (size-corrected scores), F.1
  (the filtration audit), F.2 (block permutation), G (release lags), H (knowable-at situation fields) and
  I (determinism and the content digest). Where this document is silent, the protocol governs.

### 0.3 Ownership
Session B owns `GRID_STUDY_REGISTRATION.md`, `src/engine/grid/**`, `data/grid/**` and
`tests/test_grid_*.py`, added to its charter §1 block in the same commit as this document. It touches no
other session's tree; requests go to `data/handoffs/` as always.

### 0.4 Why the study is proposed at all — the two defects it addresses
Both are measured, not asserted, and both are facts about the published run rather than results of this study:

- **n.** 150 scored G reads and 253 scored P reads. The walk's own power block puts the minimum detectable
  Brier skill at n = 150 at **0.127** (G) and **0.085** (P), and the n required to detect skill +0.05 at 80 %
  power at roughly **1,200**. No component can be *fitted* at that n without overfitting, which is why every
  weight in the engine is a registered constant and why §5's learning loop is confined to a twelve-item menu.
- **Selection.** `data/walk_forward/big_moves_knew.json`: of the 43 registered Big Moves episodes,
  **15 carry zero reads — 34.9 %**. The engine is never scored on a third of the days the market actually
  moved, because no corpus event triggered a read there. A date grid removes the trigger and therefore the
  selection.

---

## Part I — the estimand

### 1.1 The unit
A **read** is issued at a **grid date** t. Two panels, never pooled:

- **P (price).** Unit = (grid date t, target a, horizon h). The engine issues a predictive distribution over
  the log return of target a from t to t + h trading days.
- **G (escalation).** Unit = (grid date t, dyad D). The engine issues a distribution over dyad D's IES level
  over (t, t + 90 days], on the registered four-level scale of `OUTCOME_MAPPING.md` Amendment 1 and its
  amendments, and — per Amendment L, which found the level estimand mis-anchored — **also** over ΔIES
  = L − L⁻ with L⁻ the dyad's own pre-window level. Both are sealed; the Δ form is primary for G, and the
  level form is published beside it, for the reason Amendment L established: a G forecast that does not start
  from the dyad's own level starts behind.

### 1.2 The grid
Candidate grids, both registered, chosen between in Part III **on the arithmetic of Part II and on nothing
else**: **month-end** and **week-end**, over the daily tier's span (1987 onward; the monthly tier is out of
scope for this study). A grid date is admissible only if the state block is knowable at t under the
protocol's §1, Amendment G's release lags and Amendment H's knowable-at rule. Grid dates are **not** filtered
by whether anything happened — that filter is the defect being repaired.

### 1.3 The base rate moves, and the comparison moves with it
Grid dates are mostly uneventful. The class base rate on a date grid is **not** the base rate on an
event-triggered sample, and a skill number computed against the wrong climatology is meaningless.

**Registered:** climatology for both panels is re-estimated **on the grid**, point-in-time (from grid reads
strictly before t whose outcome had closed by t), and every skill number in this study is computed against
**that** climatology. The grid base rate and the event base rate are published side by side in
`data/grid/**` so the size of the shift is visible, and the shift is reported before any skill number is.

### 1.4 What the grid cannot repair
Stated now, not later: the grid removes *trigger* selection. It does not remove **source** selection. The
physical record still goes dark for the producers that matter (Iran from July 2018, UAE from December 2018,
Russian crude stocks 2009, Kazakh crude stocks 2014 — the JODI finding in `docs/PAPER_DRAFT.md` §3), and the
escalation label sources still end when they end (§2.5). A date grid over a period whose data are missing
manufactures rows, not evidence, and §2.6's availability cut is what stops it.

---

## Part II — the effective-n arithmetic, registered as a method before it is computed

*This part fixes **how** effective n is computed, on what data, with which estimator, and what would make a
multiplier fail — before the numbers exist. Nothing here is a result.*

### 2.1 The quantity that actually carries the power
Power is not a function of how many rows a table has. It is a function of the variance of the mean of the
**score-differential series** d_u = S_engine(u) − S_reference(u) over evaluation units u. Define

    n_eff  :=  n_nominal / DEFF,        DEFF := Var(mean d) / (σ²_d / n_nominal)

DEFF is the **design effect**: the factor by which dependence between units inflates the variance of the
mean relative to n_nominal independent draws. Every claim about a multiplier in this study is a claim about
n_eff and never about n_nominal. Where both appear, n_nominal is printed **beside** n_eff and never instead
of it.

### 2.2 Serial dependence on the time axis (multipliers 1 and 3)
Two estimators of DEFF_time, both computed, both published:

- **Bartlett / Newey–West closed form** at the protocol's registered HAC lag L:
  `DEFF_bartlett = 1 + 2 Σ_{k=1..L} (1 − k/(L+1)) ρ_k`, with ρ_k the lag-k autocorrelation of d.
- **The registered bootstrap ratio:** the variance of the mean under the **stationary block bootstrap**
  (Politis–Romano, the protocol's registered 2,000 draws, the tier's measured mean block from the registered
  35-day clustering rule) divided by its variance under an i.i.d. bootstrap at the same n and the same seed.

**Registered tie-break:** if the two differ by more than a factor of **1.5**, both are published and the
**larger** DEFF is used everywhere. A disagreement of that size is itself reported as a finding about the
dependence structure, not smoothed over.

### 2.3 Cross-sectional dependence across targets (multiplier 2)
For the mean of M series each with variance σ² and correlation matrix ρ,
`Var(mean) = (σ²/M²)·Σᵢ Σⱼ ρᵢⱼ`, so the effective number of independent targets is

    M_eff  =  M²  /  Σᵢ Σⱼ ρᵢⱼ

**Registered, including its known weakness.** ρ must be the correlation of the **score differentials**,
because that is what is being averaged. Before the engine exists there are no score differentials, so the
pre-build number uses the correlation of the **h-horizon log returns** of the targets as a proxy.

Direction of the error, stated in advance so it cannot be chosen afterwards: a score differential contains
the forecast's own target-specific error in addition to the outcome, so we **expect** ρ_d ≤ ρ_return and
therefore expect the return-based M_eff to be a **floor**. That is an argument, not a proof. The realised
M_eff on actual score differentials is recomputed and published on the first run of the study; the pre-build
floor published here is never retro-fitted to it, and if the two differ the difference is reported.

### 2.4 Horizon nesting (multiplier 3)
The same formula applied across the H horizons at the same grid date: `H_eff = H² / Σᵢ Σⱼ ρᵢⱼ`.

**A pre-registered benchmark, so the empirical number can be judged rather than merely reported.** Under a
random walk, returns over nested windows from the same origin satisfy
`corr(r_{t,h₁}, r_{t,h₂}) = √(min(h₁,h₂) / max(h₁,h₂))`. For the registered h ∈ {5, 10, 20, 40, 60} this
gives an exact theoretical H_eff, computed in closed form and published **beside** the empirical one. The gap
between them is the extent to which oil returns are not a random walk over these horizons, and it is
published whichever way it goes.

Overlap across grid dates is a separate effect and is handled by §2.2 on the stacked series, not here.

### 2.5 Dyad dependence, and the coverage wall (multiplier 4)
Escalation on a dyad-date panel has dependence on **two** axes: a dyad's level persists across adjacent grid
dates (the 90-day windows of consecutive month-ends share two thirds of their span, and Amendment L
established that IES levels persist strongly), and dyads inside one conflict system move together.

**Registered estimator:** DEFF from a **two-way cluster** on dyad and on date — the ratio of the two-way
clustered variance of the mean (Cameron–Gelbach–Miller) to the i.i.d. variance — reported beside a
**block bootstrap over date blocks with all dyads at a date kept intact**, the same registered mean block.
As in §2.2, if they differ by more than 1.5× both are published and the larger is used.

**The coverage wall, established from the files in the tree before this document was written, and reported
here as a fact about the data rather than a result:**

| source | in the tree | span | dyad-resolved? |
|---|---|---|---|
| Dyadic MID 4.03 | **10,358 dyad-year rows** | 1816–**2014** | yes |
| MIDA 5.0 / MIDB 5.0 / MIDI 5.0 / MIDIP 5.0 | 2,436 / 5,883 / 4,483 / 9,619 | to **2014** | yes |
| ICB v16 (crises / actors / dyads) | 512 / 1,131 / **1,388** | 1918–**2021** (dyads to 2022) | yes |
| UCDP GED 26.1 | 417,968 events | 1989–2025 | **no — the cache has no dyad field; location only** |
| COW War v4 inter / intra | — | to 2007 / 2014 | yes |

**The brief's figure of "59,076 panel rows" for Dyadic MID 4.03 does not match the file in this tree, which
has 10,358 rows.** No file in `data/state/raw/` has 59,076 rows. This registration therefore uses 10,358 and
states the discrepancy rather than reconciling it silently; if Joe has a different Dyadic MID build in mind
it should be admitted through the normal route and this section amended.

The consequence is not cosmetic and is registered as a constraint on multiplier 4, before its arithmetic is
run: **a dyad-resolved IES label ends in 2014** for the MID family, is carried by ICB alone to 2021, and does
not exist after 2021. GED covers 1989–2025 but resolves a *location*, not a dyad, so it can raise a level for
a place and cannot attribute it to a pair. The number of grid dates at which a dyad-date label is knowable is
computed in §2.6 and published; a grid date with no covering source yields `no_independent_outcome` and is
**counted, never guessed** — the ies90 coverage rule, unchanged.

### 2.6 The availability cut, before any dependence at all
A multiplier supplies only the rows whose data exist. Computed and published **first**, as a plain table:

- **Per target and horizon:** the number of grid dates at which the state block is knowable at t (§1.2) *and*
  the outcome at t + h is observable and closed. Target spans already established in the tree, and the
  reason this cut is not decorative: Brent 1987-05-20 (9,963 obs), WTI 1986-01-02 (10,231), diesel crack
  1986-06-02 (10,103), gasoline crack 1986-06-02 (10,101), **Henry Hub 1997-01-07 (7,441)**, **propane
  1992-07-09 (8,554)**. Two of the six targets do not exist for the first decade of the grid.
- **Per dyad-date:** the number of (dyad, grid date) cells with ≥ 1 covering label source over (t, t+90]
  under the ies90 coverage rule, and the count that would return `no_independent_outcome`.

### 2.7 The drop rule, pre-declared
For each multiplier m, define its **realisation ratio** on the joint panel:

    R_m  =  Δn_eff from adding m  /  Δn_nominal from adding m

Decided in advance, and applied mechanically:

- **R_m < 0.10 → the multiplier is DROPPED** from Part III, and the reason is published with the number.
- **Δn_eff from adding m < 30 effective units → DROPPED regardless of R_m** (30 is the protocol's registered
  `min_tier_n`: a contribution smaller than the smallest tier that may be reported at all is not a
  contribution).
- **0.10 ≤ R_m < 0.33 → KEPT but reported as marginal**, with R_m printed beside every number it contributes
  to, in every surface, permanently.
- **R_m ≥ 0.33 → KEPT.**

### 2.8 The joint number is computed jointly, never multiplied
The four multipliers are not independent — a week-end grid and a 60-day horizon overlap each other; two
targets that correlate at 0.99 do not become independent because they are observed at more dates.

**Registered:** the headline n_eff is computed on the **actual stacked evaluation matrix** — one row per
(grid date, target, horizon) for P and per (grid date, dyad) for G — with a single design effect estimated on
that stacked series by the estimators of §2.2–§2.5. The product of the separate factors is computed too, and
published **only** as a diagnostic explicitly labelled `naive_product`, beside the joint number, so the gap
between the two is visible in the file. **A nominal multiplier is never reported as a power multiplier**, and
any statement of the form "50× the data" must carry the joint n_eff ratio in the same sentence.

### 2.9 What the arithmetic decides
Two thresholds, registered before the numbers:

- **Is the study worth building?** The protocol's own power estimator (`INF.power_block`, registered seeds,
  the measured mean block and HAC lag of the stacked series) is run at the computed joint n_eff. The study is
  built iff it detects a Brier skill of **+0.05 at 80 % power** for at least one of the two panels. If it does
  not, that shortfall is published as the finding and Part III is written as a null design rather than as a
  study.
- **Is training legitimate?** The fitting stage of Part III (§3) is run **only if** each outer fold's inner
  training set carries at least **20 effective units per fitted parameter** — the conventional floor, fixed
  here before the parameter count is known. The count is published with the number of fitted parameters
  beside it. If the floor is not met, **the fit is not run**, the frozen registered-weight engine stands, and
  that is published as a result about the design rather than quietly skipped.

### 2.10 Outputs of Part II
`data/grid/power_arithmetic.json` — the availability table (§2.6), DEFF and n_eff per multiplier by both
estimators (§2.2–§2.5), the random-walk H_eff benchmark (§2.4), the joint n_eff and the `naive_product`
diagnostic (§2.8), R_m and the drop decision for each multiplier (§2.7), the two threshold verdicts (§2.9),
and the registered seeds. Tests: `tests/test_grid_power.py`, each name carrying its clause id.

---

## Part III — the study proper

**Not written.** Part III is registered only after Part II is computed and published, and it is registered
with any multiplier the §2.7 drop rule removed actually removed. It will fix: the grid choice (§1.2), the
retrieval and the state blocks, the scores, the baselines including grid-climatology (§1.3) and the frozen
registered-weight engine, the nested walk-forward CV design for the fitted block weights and the learned
similarity metric (inner folds strictly before each outer read, no exceptions), the comparison of the fitted
model against the frozen one — **with the finding published either way, because "fitting does not beat fixed
weights at this n" is a result about the design and not a failure to report** — and the promotion rule.

---

## Appendix — what was already in the tree when this was written
Established by reading the files, before any arithmetic:

- The published run `walk_20260903T003422Z`: 150 scored G reads, 253 scored P reads, measured MDS 0.127 (G)
  and 0.085 (P), n ≈ 1,200 required for skill +0.05.
- `data/walk_forward/big_moves_knew.json`: 43 Big Moves episodes, **15 with zero reads (34.9 %)**.
- Targets and spans as listed in §2.6; the six exist and are loaded.
- Conflict sources and spans as listed in §2.5, with the Dyadic MID row-count discrepancy stated.
- `state_panel` 352,295 rows, `observations` 678,280 rows, `situation_state` 11,089 rows, 772 series.
