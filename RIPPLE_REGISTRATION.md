# RIPPLE REGISTRATION — the chain study, registered before computing
*2026-09-02. Brief R (R1 method, R2 nodes, R3c registration). Written after
RIPPLE_SOURCES.md and the loaders (commit df66b3c) and before `src/ripple_lp.py`
existed or any IRF was run. The git timestamp is the seal. Amendments are dated and
appended, never edited in place (WALK_FORWARD_PROTOCOL.md convention). Everything in
§6 is an EXPECTATION to be tested, not a finding.*

## 0. The object

A **ripple** is the dynamic response of a chain node to an identified oil-market shock:
the coefficient path β(h), h = 0…H, of the node's change from the last pre-shock close
to h periods after, attributable to the shock. The chain runs

    crude (hop 0) → refined products and cracks (hop 1)
                 → the physical system: refinery runs, stocks, imports, chokepoint transits (hop 2)
                 → gas and LNG (hop 3) → fertilizer (hop 4)
    with macro cross-checks (breakevens, dollar, VIX) and equity proxies beside, never inside.

Shocks are the corpus events (313, seven classes), with the Big Moves onsets as the
market-defined alternative and two external identified-shock series (Känzig 2021;
Baumeister & Hamilton 2019) as documented sanity checks, not gates.

## 1. Method (R1) — what was extracted from each paper and where it is used

Every paper below was opened; the version opened is stated. Where the published text
could not be opened, the register says so and the claim is sourced to what was read.
Full extraction notes (verbatim quotes with page numbers) are in the session record;
the sentences quoted here are the ones the design rests on.

### 1.1 Estimator — Jordà (2005), AER 95(1):161–182
Opened: AEA abstract page; Jordà's own slide deck "Impulse Responses by Local
Projections: Practical Issues" (UC Davis, hosted at UC3M); Jordà & Taylor (2024) NBER
WP 32822 "Local Projections" §2, §6. The 2005 full text is paywalled and was NOT
opened; nothing below is attributed to a page of it.
- Extracted: the LP idea — "estimating local projections at each period of interest
  rather than extrapolating into increasingly distant horizons from a given model"
  (abstract); one regression per horizon; advantages "(1) simple regression… (2) more
  robust to misspecification; (3) joint or point-wise analytic inference is simple;
  (4) easily accommodate… highly nonlinear and flexible specifications" (abstract).
  Slides: "The maximum lag p need not be common to all s projections"; "The lag
  length and the IR horizon impose degree-of-freedom constraints for very small
  samples"; "Monte Carlos show little loss of efficiency in estimating univariate
  local projections and using HAC robust standard errors (such as Newey-West)".
  Jordà & Taylor §6.1: the h-step residual is "a moving-average of order h or MA(h). A
  simple solution proposed by Jordà (2005) is to use a heteroskedasticity and
  autocorrelation consistent (HAC) covariance estimator, such as Newey-West"; §2:
  "use information criteria to determine the lag-length as usual for [h=1], and then
  use the same lag-length at subsequent horizons".
- Used for: the estimator (§2.1); the HAC diagnostic with bandwidth = h (§2.4); the
  one-lag-length-for-all-horizons rule (§2.3).

### 1.2 Inference — Montiel Olea & Plagborg-Møller (2021), Econometrica 89(4):1789–1823
Opened: full text (arXiv 2007.13888, Dec 2020 version; page numbers are the arXiv's).
- Extracted: lag-augmented LP (their eqs. 1–6); "contrary to conventional wisdom
  (e.g., Jordà, 2005, p. 166; Ramey, 2016, p. 84), HAR standard errors are not needed
  to conduct inference on lag-augmented LP… it suffices to use the usual
  heteroskedasticity-robust Eicker-Huber-White standard error" (p. 8); validity "uniform
  over the persistence in the data and for a wide range of horizons" provided h̄/T → 0
  (p. 10); "p should be chosen conservatively… there is no asymptotic efficiency cost
  of controlling for more than p₀ lags" and "Naive pre-testing for p causes uniformity
  issues" (pp. 27–28); recommendation: "lag-augmented local projections with
  heteroskedasticity-robust (Eicker-Huber-White) standard errors… standard normal
  critical values" (p. 27); the two cases where it is inferior (short horizons with
  known-stationary data; near-unit roots at horizons a substantial fraction of T).
- Used for: primary standard errors = EHW (HC1), normal critical values (§2.4); a
  fixed, conservative, pre-registered lag length instead of pre-testing (§2.3); the
  h/T check (§2.2: max h = 60 trading days against T ≈ 9,900; 26 weeks against
  ≈ 1,900; 12 months against ≈ 600–800).

### 1.3 Why LP and not a VAR here — Plagborg-Møller & Wolf (2021), Econometrica 89(2):955–980
Opened: full text (author's site, Oct 2020 version).
- Extracted: "the LP and VAR impulse response functions are equal, up to a constant of
  proportionality" in population (Proposition 1, p. 8); with finite lags they "agree
  at all horizons h ≤ p, although generally not at horizons h > p" (Prop. 2, p. 12);
  "the choice between the procedures at long horizons requires navigating a
  bias-variance trade-off" (pp. 14–15); identification schemes "can equivalently be
  carried out using LPs" (p. 15); the list of mistaken assertions, including that
  "local projections are generally more robust to misspecification than VARs" (p. 28).
- Statement (why LP): the estimand is the same, so this is a finite-sample choice, not
  an identification choice. We choose LP because (i) the shocks are dated event
  dummies and external surprise series, which enter an LP directly; (ii) the
  registered horizons (60 trading days, 26 weeks, 12 months) far exceed any lag length
  we would fit, so a VAR would be extrapolating from short-run autocorrelations — we
  prefer bias over variance at those horizons; (iii) the sign-split and regime
  specifications (§2.6–2.7) are single-regression changes in an LP. The costs are
  accepted and shown: wider bands and "sometimes erratic" long-horizon paths (Ramey),
  which is why every IRF ships with both standard errors and a placebo band.

### 1.4 Shock identification standards — Ramey (2016), Handbook of Macroeconomics ch. 2
Opened: full text (NBER WP 21978; page numbers are the paper's own).
- Extracted (p. 5): a shock should be "(1) exogenous with respect to the other current
  and lagged endogenous variables in the model; (2) uncorrelated with other exogenous
  shocks…; and (3) either unanticipated movements in exogenous variables or news about
  future movements". On narrative series (p. 11): "the narrative alone provides
  exogeneity. It does not." On high-frequency identification (pp. 11–12): timing
  assumptions "are more plausible" at daily frequency but "the unanticipated shock is
  not necessarily exogenous". On LP (p. 18): "the estimates are often less precisely
  estimated and are sometimes erratic. Nevertheless, this procedure is more robust".
  On oil (pp. 80–81): Kilian (2009) as "a critique of standard identification
  methods"; asymmetry "not strong evidence" (Kilian & Vigfusson 2011); on p. 23 the
  bias from censoring on increases only.
- Checklist applied to each shock series (§2.5): exogenous (the event is not a response
  to the node's own past moves — checked by the pre-event window t−5…t−1 being flat
  on average, published as a diagnostic); unanticipated (surprise code; Big Moves
  "ANTICIPATED" flag; GPR-threat level at t−1); not contaminated (de-overlapped
  clusters; same-day multi-class events counted in each class and flagged).

### 1.5 The closest template — Känzig (2021), AER 111(4):1092–1125
Opened: full text (author's site, Nov 2020 working paper); data repo and the
2025M12 workbook.
- Extracted: 119 OPEC press-release dates 1983–2017; surprise = log change of WTI
  futures settlement, announcement day vs. the prior trading day, daily window because
  "OPEC does not communicate as clearly as a central bank"; composite = first
  principal component of the 1M–12M maturities; monthly = sum within month, zero
  otherwise; external instrument in a 6-variable monthly VAR, 12 lags, 1974M1–2017M12
  with instrument sample 1983M4–2017M12; first-stage F = 22.7 (robust 10.55); an LP
  version "yield[s] comparable results… At longer horizons, the local projection
  responses are less persistent and less precisely estimated"; the signature of a
  supply-news shock: price up on impact, production falls only with a lag,
  inventories RISE; pitfalls named: invertibility, background noise, weak instruments,
  information channel (purged with OPEC demand-forecast revisions).
- Used for: the external check (§2.8): our `opec_decision` dummy IRF beside an LP on
  `kanzig.surprise_daily_pc`; and the expectation that OPEC-class shocks move
  inventories UP (§6, E-7), which the weekly stock nodes can test.

### 1.6 Shock classes — Kilian (2009), AER 99(3):1053–1069; Baumeister & Hamilton (2019), AER 109(5):1873–1910
Opened: Kilian — the June 2008 working-paper draft (sample stated 1973.1–2006.10; the
published sample may differ; not verified); Baumeister & Hamilton — the July 2018
working-paper draft; both shock datasets.
- Extracted (Kilian): three shocks — "shocks to the current physical availability of
  crude oil ('oil supply shocks')", "shocks to the current demand for crude oil driven
  by fluctuations in the global business cycle ('aggregate demand shocks')", "shifts in
  the precautionary demand for oil"; recursive ordering production → activity → real
  price; wild bootstrap; "unanticipated oil supply disruptions have only a small
  positive effect on the real price of oil"; 1990/91 "almost entirely due to an
  increase in precautionary demand"; 1979 = precautionary demand on top of aggregate
  demand; the precautionary shock "could in principle capture any number of omitted
  factors".
- Extracted (B&H): four shocks (oil supply; economic activity; oil consumption demand;
  oil inventory demand); prior on the short-run supply elasticity Student-t mode 0.1,
  posterior median 0.15; "supply shocks were more important in accounting for
  historical oil price movements than was found in studies that assumed very precise
  prior information about the size of the supply elasticity"; "considerable error in
  measuring world inventories".
- Used for: the registered class mapping (§2.5, Table M) and the monthly external
  check on `bh.*` (§2.8).

### 1.7 Asymmetry — Kilian & Vigfusson (2011), Quantitative Economics 2(3):419–453
Opened: full text (EconStor copy of the published article).
- Extracted: censored ("net increase") regressions "asymptotically overestimate the true
  response… regardless of whether the true data generating process is symmetric or
  asymmetric"; the encompassing model that nests both; the impulse-response-based
  symmetry test (simulate paths conditional on history, shocks of 1 and 2 sd, 500
  reps, integrate over histories); slope-based tests are "not informative about the
  degree of asymmetry of the response functions"; the verdict "very little, if any,
  evidence of asymmetric responses".
- Used for: §2.6 — we never censor; both signs of the crude change enter the same
  regression; the symmetry test we can run in an LP is a slope-based Wald test and is
  LABELLED as such with K&V's caveat; the IRF-based simulation test is deferred to a
  later brief and named as the stronger test.

### 1.8 Placebo-matching and anticipation — Caldara & Iacoviello (2022), AER 112(4):1194–1225
Opened: full text (Fed IFDP 1222r1, March 2022); replication page; the daily file.
- Extracted: eight search categories, threats (1–5) vs. acts (6–8) sub-indexes; daily
  index "noisier than its monthly counterpart but provides a detailed view"; VAR with
  GPR ordered first, two-sd shock lowers investment −1.5% after a year; LP at the
  firm level; caveat that slowly unfolding episodes may be mis-measured.
- Used for: the placebo (§2.5) matches pseudo-dates on GPR as well as VIX; the
  "anticipated vs surprise" control is the 30-day mean of `gpr.GPRD_THREAT` at t−8
  (the file updates weekly, so t−1 is not knowable; t−8 is).

### 1.9 Pass-through — Borenstein, Cameron & Gilbert (1997) QJE; Bachmeier & Griffin (2003) REStat
Opened: BCG — the 1992 NBER WP 4138 predecessor, full text (the QJE PDF is an image
scan without a text layer; OCR did not complete); B&G — NOT OPENED (every copy 403/404);
what is used is what Chesnes (2010, FTC WP 302, opened) attributes to them.
- Extracted (BCG WP): asymmetric distributed-lag ECM, ΔC⁺ = max(ΔC,0), ΔC⁻ = min(ΔC,0),
  10-week lags, cumulative asymmetry tested at weeks 5 and 10; weekly crude and spot,
  semi-monthly retail, 1986–1990; crude→terminal asymmetry "0.13¢ over the five weeks
  and statistically insignificant"; terminal→retail asymmetry "1.67¢ at five weeks…
  (significant at 1%)"; "Nearly all of the response to a crude oil price increase shows
  up in the pump price within 4 weeks, while decreases are passed along gradually over 8
  weeks". Chesnes on B&G: "find no evidence of asymmetry in the crude oil to gasoline
  spot price transmission" on daily data.
- Used for: §2.6 (the registered asymmetric pass-through test at the crude→product
  hop, with horizons 5 and 10 weeks for the weekly retail leg and 5/10/20 trading days
  for the daily spot leg) and expectation E-3 (no asymmetry at the spot hop; asymmetry,
  if any, at the retail leg).
- Kilian (2010), Energy Journal 31(2): NOT OPENED (SAGE/CEPR/SSRN all 403; the archived
  manuscript is on a domain the fetch tool refuses). **Not cited anywhere in this
  design.** Listed so the omission is visible.

### 1.10 Gas — Brown & Yücel (2008), Energy Journal 29(2):45–60; Ramberg & Parsons (2012), Energy Journal 33(2):13–36
Opened: Brown & Yücel — the Dallas Fed WP 0703 (Feb 2007) version, full text;
Ramberg & Parsons — full text (MIT copy).
- Extracted (B&Y): ECM of weekly Henry Hub on WTI with HDD/CDD deviations, storage
  deviation and Gulf shut-ins, 1997-06-13 → 2006-07-14 (1994 → for the two-variable
  model); rules of thumb 10-to-1 ("consistently under-forecasts"), 6-to-1 ("consistently
  over-forecasts"), burner-tip parity; long-run coefficient 0.14 ($ per mmbtu per $/bbl);
  error-correction speed −0.08/week without controls, −0.18/week with ("90 percent
  adjustment in less than 12 weeks"); "causality from oil to natural gas prices"; no
  formal break test. (R&P): Gregory–Hansen breaks at 2006-03-10 and 2009-02-06; the
  cointegrating slope falls from 0.7261 to 0.4621 (log-log) across the first break; after
  2009-02-13 "neither series displays sufficient evidence of non-stationarity for the
  tests of cointegration to be meaningful"; decouplings "not very long lasting".
- Used for: the registered regime split (§2.7): pre 2009-02-06 vs post 2009-02-13 as
  primary (the only break date in the opened literature from a formal test), with the
  2006-03-10 break as a secondary split; expectation E-4.

## 2. Design

### 2.1 The regression (one per node × shock × horizon)
For node y (transformed as in Table N), horizon h, shock series S:

    y_{t+h} − y_{t−1} = α_h + β_h · S_t + Σ_{l=1}^{p+1} γ_{h,l} · (y_{t−l} − y_{t−l−1}) + δ_h' X_{t−1} + u_{t+h}

- β_h is the IRF at h. The base is the close at t−1, so nothing dated t or later enters
  the base (the INV-4 discipline of this repo).
- The p+1 lags of the node's own change are the lag augmentation (one more than p;
  §1.2). Controls X_{t−1}: for daily nodes, the change in log VIX over t−6…t−1 and the
  30-day mean of GPRD_THREAT at t−8 (§1.8); for weekly nodes the same at the last
  knowable date; for monthly nodes, the prior month's Δlog crude (so a monthly node's
  response is conditional on crude's own last move — the "beyond crude" reading) and
  Δlog GPR monthly. For equity proxies, the S&P 500 change over the same window
  (y_{t+h} − y_{t−1} of `yf.sp500`) is added as a regressor, and the coefficient on S
  is read as the sector-specific response.
- Two specifications for every non-crude node: TOTAL (as above) and CRUDE-CONDITIONED
  (adds Brent's own change over t−1…t+h as a regressor). The first is the ripple; the
  second isolates what the shock does to the node beyond what crude explains. Both are
  published; the TOTAL is primary.

### 2.2 Horizons (fixed) and the h/T check
- Daily nodes: h ∈ {0, 1, 2, 5, 10, 20, 40, 60} trading days. Headline h = 5 for crude,
  20 for products/gas/cracks, 20 for macro.
- Weekly nodes (EIA): h ∈ {0, 1, 2, 4, 8, 13, 26} weeks. Headline h = 4.
- Monthly nodes (Pink Sheet, PPI, external shocks): h ∈ {0, 1, 2, 3, 6, 9, 12} months.
  Headline h = 3.
- h̄/T ≤ 60/9,900 ≈ 0.6% (daily), 26/1,900 ≈ 1.4% (weekly), 12/600 = 2% (monthly): all
  well inside the regime where lag-augmented LP inference is valid (§1.2).

### 2.3 Lag length (fixed in advance; no pre-testing)
p = 5 (daily), 4 (weekly), 6 (monthly); lag augmentation adds one. Robustness: 2p.
Rationale: §1.2 (conservative, no efficiency cost, no pre-test uniformity problem) and
§1.1 (one length for all horizons). A run at 2p that flips a headline sign is reported
as FRAGILE, not chosen.

### 2.4 Standard errors and bands
Primary: Eicker–Huber–White HC1 with standard-normal critical values; 90% and 95%
bands (§1.2). Diagnostic beside it: Newey–West (Bartlett) with bandwidth = h (the MA(h)
structure, §1.1). Rule: if the two disagree on whether the 95% band covers zero at the
headline horizon, the result is labelled FRAGILE. Sample for daily class IRFs is
de-overlapped: events of the same class within 20 trading days form one cluster and
the first date carries the dummy (`robustness.assign_clusters`, CLUSTER_DAYS as
registered there); the overlapping version is published beside as a diagnostic.

### 2.5 Shock series, exogeneity checks, minimum n, placebo
- **Primary S:** class dummies S^c_t = 1 on the knowability date of a class-c event (day
  precision only for daily/weekly nodes; week/month precision events enter monthly
  nodes only, dated to their month). Same-day events of different classes count in
  each class and are flagged `multi_class`.
- **Table M — registered mapping of our classes to Kilian (2009) / B&H (2019):**

| class | Kilian (2009) | B&H (2019) | expected crude impact sign | note |
|---|---|---|---|---|
| chokepoint_disruption | supply (physical availability) + precautionary demand | supply (+ inventory demand) | + | transit threatened; realised loss may be nil |
| infrastructure_attack | supply | supply | + | direct capacity loss |
| conflict_escalation | precautionary demand (Kilian: 1990/91 "almost entirely") | inventory demand / supply if output lost | + | |
| opec_decision | oil-specific (expectational) demand; Känzig: supply NEWS | supply news | ambiguous (cut + / raise −) | direction not coded in the corpus; unsigned pooled IRF, plus the Känzig continuous surprise beside |
| sanctions | supply news / expected availability | supply | ambiguous (imposed + / lifted −) | as above |
| demand_shock | aggregate demand | economic activity / consumption demand | − | |
| policy_response | supply (SPR release) / expectations | supply (+) | − (typically loosening) | |

  The mapping is a declared interpretation, registered so the results cannot be
  re-labelled after the fact; it is not itself tested.
- **Alternative S:** Big Moves onsets (`data/big_moves/brent.json`, sign carried), as a
  market-defined shock: the IRFs of every node to a Brent onset ± are published as a
  descriptive comparison (they condition on crude's own move, so they are not causal
  and are labelled so).
- **Exogeneity diagnostic (Ramey §1.4):** the mean pre-window change y_{t−1} − y_{t−6}
  by class, with its EHW band. A class whose pre-window is not flat is labelled
  ANTICIPATED-IN-PRICE and its IRFs carry that label.
- **Minimum n:** a class IRF is estimated for a node only if ≥ 15 de-overlapped events
  of that class fall inside the node's sample (with room for h̄); below that the class
  is pooled into "all events" for that node and reported as pooled. Same rule per
  regime (§2.7). PortWatch nodes (2019 →) will fail this for every class; they are
  therefore registered as EXPLORATORY (pooled, all events since 2019, labelled n).
- **Placebo:** for each (node, class), 500 pseudo-event sets drawn from non-event dates
  ≥ 30 calendar days from any corpus event, matched one-for-one to the class's events
  on the VIX 5-year-percentile decile and the GPRD 30-day-mean 5-year-percentile decile
  at t−1 (extends `placebo_vixmatched.py`; §1.8). The real β_h at the headline horizon
  is reported with its percentile in the pseudo distribution. A ripple is "beyond the
  state" only if outside the central 95% of the pseudo distribution; otherwise it is a
  property of turbulent times, and is said to be.

### 2.6 Asymmetry at the crude→product hop (registered test)
Two legs, both weekly-and-daily where the data allow:
- Daily spot leg (crude → DHOILNYH, DGASUSGULF, DGASNYH, DJFUELUSGULF, DPROPANEMBTX):
  LP of the product's log change on Δ⁺ = max(Δlog Brent_t, 0) and Δ⁻ = min(Δlog Brent_t, 0)
  entered TOGETHER (never censored; §1.7), same lags/controls as §2.1. Symmetry
  statistic: W_h = β⁺_h − β⁻_h with EHW Wald, at h = 5, 10, 20 trading days.
- Weekly retail leg (crude → `fred.GASREGW`, US regular retail, 1990-08 →): the same
  regression at weekly frequency, tested at h = 4 and h = 8 weeks (BCG's "4 weeks vs
  8 weeks"). The DB series is existing; its FRED page is EIA-sourced (public domain).
- Both tests are slope-based; per §1.7 they are informative about the slopes, not
  about the shape of the full nonlinear response. They are reported with that sentence
  attached. The IRF-based simulation test is a later brief.

### 2.7 Regimes
- Gas link (Henry Hub on crude; Pink Sheet gas US/EU and LNG Japan on crude monthly):
  primary split at **2009-02-06 / 2009-02-13** (Ramberg & Parsons' second break);
  secondary split at 2006-03-10. The pre-shale regime for the daily Henry Hub node is
  1997-01-07 → 2009-02-06. Estimated only if each regime holds ≥ 15 events of the class
  (else pooled across classes within the regime).
- No other regime split is registered. A split found interesting later is an amendment.

### 2.8 External checks (documented, never gates)
- Känzig: LP of Brent (daily) on `kanzig.surprise_daily_pc` (continuous, announcement
  days only, 1983-07 → 2025-12) over the same horizons; beside it our `opec_decision`
  dummy IRF. Expected: same sign for a tightening announcement; scales differ (his is
  a futures-surprise unit; ours a dummy). Also the correlation between our monthly
  count of opec_decision events and |kanzig.surprise_monthly|.
- Baumeister & Hamilton: monthly LP of `wb.crude_avg` (log) on `bh.supply_shock` and on
  `bh.inventory_demand_shock`; and the monthly correlation of the class-count series
  (chokepoint + infrastructure + conflict) with `bh.supply_shock`. Expected: a negative
  supply shock (production down) raises the price; our tightening classes should
  co-move with it weakly. Reported as numbers with n; no threshold is attached.

### 2.9 Multiple testing
Primary tests are the expectations in §6, each at its registered node, class and
headline horizon — nine tests, uncorrected, reported one by one. Everything else
(every other node × class × horizon) is exploratory and, within each node's family at
the headline horizon, controlled with Benjamini–Hochberg at q = 0.10; exploratory
results are printed with their BH-adjusted status and never promoted to a finding in
this brief.

### 2.10 Filtration (knowability) — declared publication lags
| source | value dated t is knowable at | consequence |
|---|---|---|
| FRED daily spots (EIA) | t + 1…3 business days | responses are measured on obs_date (a hindsight IRF, standard); CONTROLS use t−1 values only through series that are themselves knowable at t−1: VIX (same-day close) yes; Brent own lags: use t−4 and earlier for the "crude-conditioned" spec's lag block (declared, applied) |
| EIA weekly | Wednesday after the week (≈ t + 5 days) | weekly IRFs are on obs_date; not used as a control |
| Pink Sheet monthly | ≈ 4 days after month end | monthly IRFs on obs_date; monthly crude control at t−1 month is knowable |
| PortWatch daily | published with a lag of days (not stated on the item page) | exploratory only |
| GPR daily | file updates weekly | control uses t−8 |
| Känzig / B&H | vintages (6-monthly / semi-annual) | external checks only; never a control |

## 3. Nodes (R2) — Table N

Transform: `log` = 100·log level (responses in %); `lvl` = level (responses in the
series' unit); `pp` = percentage points. "sample" = first date usable.

| hop | node | series_id | freq | transform | sample | role |
|---|---|---|---|---|---|---|
| 0 | Brent | fred.DCOILBRENTEU | daily | log | 1987-05 | primary crude |
| 0 | WTI | fred.DCOILWTICO | daily | log | 1986-01 | secondary crude |
| 0 | Brent–WTI spread | derived.brent_wti_spread | daily | lvl | 1987-05 | locational |
| 1 | heating oil / diesel NYH | fred.DHOILNYH | daily | log | 1986-06 | product |
| 1 | gasoline Gulf | fred.DGASUSGULF | daily | log | 1986-06 | product |
| 1 | gasoline NYH | fred.DGASNYH | daily | log | 1986-06 | product (new) |
| 1 | jet fuel Gulf | fred.DJFUELUSGULF | daily | log | 1990-04 | product (new) |
| 1 | propane Mont Belvieu | fred.DPROPANEMBTX | daily | log | 1992-07 | NGL/petchem |
| 1 | diesel crack | derived.diesel_crack | daily | lvl (USD/bbl) | 1986-06 | margin |
| 1 | gasoline crack | derived.gasoline_crack | daily | lvl | 1986-06 | margin |
| 1 | retail gasoline (asymmetry leg only) | fred.GASREGW | weekly | log | 1990-08 | §2.6 |
| 2 | refinery utilization | eia.refinery_util | weekly | pp | 1990-11 | physical |
| 2 | crude stocks ex-SPR | eia.crude_stocks_xspr | weekly | log | 1982-08 | physical |
| 2 | distillate stocks | eia.distillate_stocks | weekly | log | 1982-08 | physical (new) |
| 2 | gasoline stocks | eia.gasoline_stocks | weekly | log | 1990-01 | physical (new) |
| 2 | crude imports | eia.crude_imports | weekly | log | 1990-01 | physical (new) |
| 2 | Hormuz / Bab el-Mandeb / Suez / Cape / Malacca / Panama / Bosporus tanker transits | portwatch.<slug>.n_tanker | daily | log(1+n) | 2019-01 | EXPLORATORY (n) |
| 3 | Henry Hub | fred.DHHNGSP | daily | log | 1997-01 | gas; regime split §2.7 |
| 3 | TTF (regime check only) | yf.ttf | daily | log | 2017-10 | unit inferred; descriptive |
| 3 | gas US / gas Europe / LNG Japan | wb.ngas_us, wb.ngas_eu, wb.lng_japan | monthly | log | 1960 / 1960 / 1977 | gas & LNG spine |
| 4 | nitrogen fertilizer PPI | fred.PCU325311325311 | monthly | log | 1975-12 | fertilizer |
| 4 | urea / DAP / TSP / potash | wb.urea, wb.dap, wb.tsp, wb.potash | monthly | log | 1960 / 1967 / 1960 / 1960 | fertilizer |
| 4 | coal Australia | wb.coal_aus | monthly | log | 1970 | substitute fuel (cross-check) |
| x | 5-year breakeven | fred.T5YIE | daily | pp | 2003-01 | macro |
| x | broad USD | fred.DTWEXBGS | daily | log | 2006-01 | macro (starts 2006; no splice) |
| x | VIX | fred.VIXCLS | daily | log | 1990-01 | macro (as a response; also a control at t−1 elsewhere) |
| x | HY credit ETF (proxy) | yf.hyg | daily | log | 2007-04 | labelled proxy (HY OAS window is 3 years) |
| e | tanker equities (FRO, DHT, TNK, INSW, STNG) | yf.eq_*, yf.tankers | daily | log, with S&P control | 2001 → | EQUITY PROXY |
| e | refiners (VLO, MPC, PSX) | yf.eq_* | daily | log, with S&P control | 1982 → | EQUITY PROXY |
| e | fertilizer (CF, NTR, MOS) | yf.eq_* | daily | log, with S&P control | 1988 → | EQUITY PROXY |
| e | LNG (Cheniere) | yf.eq_lng | daily | log, with S&P control | 1994 → | EQUITY PROXY |

Not nodes (RIPPLE_SOURCES.md §9): JKM, Baltic freight, JODI, OPEC MOMR, Suez monthly,
pre-2019 chokepoint flows.

## 4. Sample and units
- Daily study window: 1987-05-20 → last common date of the node and Brent; each node
  starts at its own first date (Table N). Events before a node's start do not enter
  that node's regression.
- Responses are in % (log nodes), pp (utilization, breakevens) or USD/bbl (cracks).
- Monthly shocks: the class dummies are aggregated to a monthly COUNT (number of
  de-overlapped events of the class in the month), so β_h is "per event in the month".

## 5. Outputs (all published as computed)
- `data/ripple/irf.json` — every (node, spec, shock, horizon): β, se_EHW, se_NW, n,
  bands, FRAGILE flag, placebo percentile at the headline horizon, BH status.
- `data/ripple/asymmetry.json` — §2.6 tests. `data/ripple/regimes.json` — §2.7.
- `data/ripple/external_checks.json` — §2.8. `data/ripple/exogeneity.json` — §2.5.
- `data/ripple/SUMMARY.md` — the nine expectations of §6, each with the number, the
  band, the placebo percentile and one of: CONSISTENT / INCONSISTENT / INDETERMINATE
  (band covers both the expected and the null), stated in that vocabulary and no other.
- Run: `python3 src/ripple_lp.py` (deterministic; seed 19900802 for the placebo draw).

## 6. Pre-stated EXPECTATIONS (to be tested, not findings)
E-1 (crude, h=5): tightening classes (chokepoint, infrastructure, conflict) raise Brent
    at h=5; demand_shock lowers it. (Replicates the event-study result in LP form.)
E-2 (pass-through completeness, h=20): heating oil and gasoline spot respond with the
    same sign as crude and a cumulative response at h=20 of similar size (ratio of
    product β to crude β in [0.5, 1.5]); the cracks' response is transitory (h=20 band
    covers zero).
E-3 (asymmetry, §2.6): NO asymmetry at the daily spot hop (BCG: terminal asymmetry
    "0.13¢… insignificant"; B&G via Chesnes: none crude→spot on daily data); asymmetry,
    if anywhere, at the weekly retail leg (increases faster: BCG "4 weeks vs 8 weeks").
E-4 (gas, §2.7): the Henry Hub response to a crude-moving shock is positive and larger
    pre-2009-02-06 than post; post-2009 the h=20 band covers zero. (B&Y long-run 0.14;
    R&P: cointegration not confirmable after 2009-02.)
E-5 (fertilizer lag): urea and DAP (monthly) respond to a tightening month with a peak
    at h=3–6 months, not h=0 (our expectation from the gas→ammonia→urea production
    chain; no opened paper states the lag — this is ours, labelled ours).
E-6 (physical, weekly): crude stocks ex-SPR do NOT fall within 4 weeks of a tightening
    event on average (Känzig: inventories RISE after supply news; Kilian: supply
    disruptions have small price effects); refinery utilization's h=4 band covers zero.
E-7 (OPEC, external): the sign of Brent's h=5 response to a positive Känzig surprise
    (supply tightening) is positive, and our opec_decision pooled IRF is small and
    indeterminate because the class mixes cuts and raises.
E-8 (placebo): at least one of E-1's classes is "beyond the state" (outside the 95%
    pseudo band) at h=5; products at h=20 may not be.
E-9 (equity proxies): tanker equities rise on chokepoint_disruption at h=5 after the
    S&P control; refiners' sign is indeterminate.

## 7. Known limits, stated now
Dummies carry no magnitude (a coup and a footnote weigh the same) — Känzig's
continuous surprise is the only magnitude-bearing shock here, and only for OPEC.
Seven classes × ~35 nodes × 8 horizons is a large family; §2.9 governs it. Monthly
nodes see 313 events collapsed into ≈ 600 months, most with zero events. PortWatch
covers 2019 → only. Equity proxies are confounded by everything else in the equity
market beyond the S&P control. The gas regime split leaves few events per class in
the pre-shale window for Henry Hub (1997–2009). None of these is fixed by more code;
they are stated so the results are read at their true weight.

## Amendment A — 2026-09-02, before any computation (disclosed)
Two defects found on re-reading the sealed text, fixed here rather than edited in place:
1. §2.4 says same-class events "within 20 trading days form one cluster" and in the
   same sentence cites `robustness.assign_clusters` "CLUSTER_DAYS as registered
   there". That constant is **35 calendar days**. The code value governs: clusters are
   formed by the chain rule over 35 calendar days, per class (and over the pooled set
   for the pooled shocks). The overlapping version stays a diagnostic.
2. E-1, E-5 and E-6 speak of "tightening classes" as one shock. Defined: the pooled
   shock **tightening** = chokepoint_disruption ∪ infrastructure_attack ∪
   conflict_escalation (the three classes with an unambiguous "+" in Table M),
   de-overlapped over their union. The pooled shock **all** = every day-precision
   event, de-overlapped over the whole corpus. Both are estimated for every node beside
   the per-class IRFs. Controls that require VIX (from 1990-01-02) or GPR (from
   1985-01-01) restrict every daily regression to dates where they exist; the effective
   daily sample therefore starts 1990-01-09 (five trading days of VIX for the control),
   which is stated here so it is not read as a choice made after seeing results.
No number had been computed when this was written.

## Amendment B — 2026-09-02, before any computation (disclosed): verdict vocabulary, the retraction check, three added nodes, output file names
Session C's brief (received after the seal) asks for counts of *transmitting / null /
insufficient* and for the retraction status of the six `propagation_edges` rows
currently labelled `validated` ("geopolitical shock (VIX-stress regime)" → Brent oil,
Heating oil, 5Y breakeven, Palladium, S&P 500, Platinum; lag 20d). Registered now,
before running:
1. **Verdict per (node, shock) at the headline horizon:** TRANSMITTING = the 95% EHW
   band excludes zero AND the real β lies outside the central 95% of the VIX+GPR-
   matched pseudo distribution (§2.5) AND the Newey–West band agrees on zero-coverage
   (else FRAGILE, which counts as null for the tally); NULL = n ≥ 15 and not
   transmitting; INSUFFICIENT = n < 15 de-overlapped events in the node's sample.
   These three words are the only verdict vocabulary; §5's CONSISTENT/INCONSISTENT/
   INDETERMINATE remains the vocabulary for the nine expectations.
2. **Retraction check of the six:** shock = `all` (every day-precision event,
   de-overlapped), restricted to events whose `derived.vix_pct` at t−1 is ≥ the
   in-sample median (the "VIX-stress regime" the edges claim), node = the six, h = 20.
   RETAINED if TRANSMITTING; RETRACTED if NULL; INSUFFICIENT otherwise. The
   `propagation_edges` table is not edited by this brief; the status is reported in
   `data/ripple/SUMMARY.md` for Session A/B to act on.
3. **Nodes added** for that check only: `yf.palladium`, `yf.platinum`, `yf.sp500`
   (daily, log; S&P without an S&P control, obviously). They are not in the chain.
4. **File names:** the §2.6 output is `data/ripple/passthrough.json` (the brief's
   name), contents exactly as registered under "asymmetry.json"; the summary file is
   `data/ripple/SUMMARY.md` and is mirrored to `RIPPLE_SUMMARY.md` at the repo root for
   the "who moved first" section the brief adds (C-6, descriptive, no test).
No number had been computed when this was written.

## Amendment C — 2026-09-02, REGISTRATION ONLY: two physical-quantity target families for v3
*Nothing in this amendment has been computed. It is written now, before any run, because Joe's
Rulings 2 and 3 made both sources loadable today and the sample sizes below are already fixed by
the corpus — registering after seeing a first estimate is exactly what the seal forbids. Neither
family is part of the v2 study reported in `docs/RIPPLE_FINDINGS.md`; that study's Table N is
closed.*

### C.1 Why these two, and what they add that v2 could not have
Every outcome in v2 is a **price**. A price response conflates the size of a disruption with the
market's belief about it, and §4.2 of the findings shows our tightening classes have almost no
relationship with the identified structural supply shock (r = −0.023 over 614 months). Physical
quantities break that conflation: a chokepoint either carries fewer tankers or it does not, and a
country either produces fewer barrels or it does not. These are the first outcomes in this
project that can falsify a "the shock was real but the market had already priced it" reading, so
they are registered as **outcome nodes**, not as controls or conditioners.

### C.2 Target family 1 — JODI-Oil monthly country production
- **Nodes.** `jodi.<cc>.crude_production` (thousand bbl/day, pinned unit KBD), and as secondary
  outcomes `jodi.<cc>.refinery_intake`, `jodi.<cc>.crude_stocks` (KBBL), `jodi.<cc>.crude_exports`,
  `jodi.<cc>.products_demand`. 106 series are loaded; **21 production series carry ≥ 200 months.**
- **Transform** 100·log for volumes; the registered horizons are the monthly set already in §2.2,
  h ∈ {0, 1, 2, 3, 6, 9, 12} months, headline **h = 3**, lag p = 6 (+1 augmentation), controls as
  §2.1 monthly.
- **Sample and n, fixed now.** Window **2002-01 → 2026-06, 294 months.** De-overlapped corpus
  events in that window: **all 67, tightening 51**; by class chokepoint 21, infrastructure 21,
  conflict 34, OPEC 38, sanctions 36, demand 13, policy 36. Months containing at least one
  de-overlapped event: **67 of 294**. So every class except demand_shock clears the registered
  minimum of 15, and demand_shock (13) does not and is registered as INSUFFICIENT in advance.
- **The registered restriction that makes this a test rather than a fishing trip.** A production
  response is only interpretable where the shock plausibly reaches the producer. Registered now:
  the primary test is **the producer named in the event's own actor/target fields** (a strike on
  Saudi infrastructure tests Saudi production), with the pooled cross-country panel as the
  secondary. Any country×class pair not named by the corpus is exploratory and BH-controlled.
- **The coverage limit, registered before it can be discovered as a surprise.** Six reporters
  stopped publishing production volumes: Iran 2018-07, UAE 2018-12, Qatar 2018-12, Brazil
  2022-12, Russia 2023-03, Iraq 2024-03. Four are major OPEC producers. **The panel is
  structurally missing the OPEC core after 2018**, so any post-2018 producer test is registered
  as running on non-OPEC reporters only, and this must be said wherever a result appears.
- **Expected direction, stated in advance:** a tightening event naming a producer lowers that
  producer's crude production at h = 1–3 months, or the "disruption" was to expectations only.

### C.3 Target family 2 — IMF PortWatch daily chokepoint transits
- **Nodes.** `portwatch.<slug>.n_tanker` (headline), with `n_total` and `capacity_tanker` as
  secondary, for the seven chokepoints already loaded and now seeded.
- **Transform** 100·log(1+n) as in v2 Table N; daily horizons h ∈ {0, 1, 2, 5, 10, 20, 40, 60},
  headline **h = 5**, lag p = 5 (+1), controls as §2.1 daily.
- **Sample and n, fixed now.** Window **2019-01-01 → 2026-08-30, 2,799 days.** De-overlapped
  events in that window by class: chokepoint 14, infrastructure 14, conflict 17, OPEC 15,
  sanctions 19, demand 9, policy 22; **tightening 24**.
- **A counterintuitive fact recorded now so it is not mistaken for a bug later.** The pooled
  **all** shock de-overlaps to **16** clusters in this window — *fewer than the tightening
  subset's 24* — because post-2019 events are dense enough that the 35-day chain rule merges
  almost everything into a few long clusters. Registered consequence: in this window the pooled
  `all` shock is **not** used; `tightening` and the per-class shocks are, and any v3 code that
  assumes pooling raises n is wrong here.
- **Registered restriction.** The primary test is **the chokepoint named by the event** (a Hormuz
  event tests Hormuz), with Cape of Good Hope registered as the **reroute counter-node**: a real
  Red Sea or Bab el-Mandeb closure should move Bab el-Mandeb down and Cape of Good Hope up, and a
  result that moves both the same way is evidence of a common time trend, not a disruption.
- **The confound registered in advance.** The 2024 Red Sea rerouting dominates this window. The
  one transmitting transit cell in v2 (Cape of Good Hope, conflict escalation, +20.7%, n = 16) is
  almost certainly that episode. v3 must report the leave-one-episode-out estimate beside the
  full-sample one, and if the result rests on that episode it is reported as an episode
  description, not a response.
- **Expected direction, stated in advance:** a chokepoint disruption naming a strait lowers that
  strait's tanker transits within 5 trading days and raises Cape of Good Hope transits.

### C.4 What is *not* registered here
No new shock series, no change to the v2 nodes, horizons, lag lengths, minimum n, placebo
construction, verdict vocabulary or multiple-testing rule — all of those carry over unchanged
from §2. No magnitude-bearing shock for the non-OPEC classes, which the findings name as the
study's principal weakness, is registered here because none exists yet; building one is its own
brief and needs its own registration before it is used.

## Amendment C — addendum, 2026-09-03, AFTER computing: what was run, and the three disclosed departures
*Amendment C above was registration only. This addendum records what the run actually did, written
after the fact and labelled as such. It changes no registered parameter; C.4 still holds. Results are
in `docs/RIPPLE_PHYSICAL.md`, data in `data/ripple/physical.json`, code in `src/ripple_physical.py`,
tests in `tests/test_ripple_physical.py` (20 passed).*

**The seal held.** All nine JODI counts (C.2) and all nine PortWatch counts (C.3) reproduce exactly,
including the counterintuitive `all` (16) < `tightening` (24) that C.3 recorded in advance; 294
months, 67 event months, 21 production series ≥200 months, 2,799 calendar days. A test asserts each.

**Three departures, all disclosed, none of them a change to a registered constant:**

1. **A monthly placebo now exists.** v2 ran every monthly node with `do_placebo=False`, which made
   Amendment B's TRANSMITTING verdict unreachable for monthly nodes *by construction*. That is a
   defect in v2, recorded as erratum E-2 in `docs/RIPPLE_FINDINGS.md` rather than repaired silently.
   The monthly buckets are §2.5's daily construction evaluated on the monthly grid. It is weak (108
   pool months, 58 buckets, mean 26.4 buckets per cell falling back to VIX-only matching) and every
   monthly verdict is qualified by that.
2. **PortWatch runs on the calendar-daily index**, the registered 2,799 days, rather than v2's Brent
   trading-day index. Tanker transits happen at weekends and the trading-day index discards 28% of
   the physical record. The trading-day version is reported beside it, and the two disagree on three
   cells — including v2's only transmitting physical cell (erratum E-1). C.3 fixed the sample at
   2,799 days, so the calendar index is the registered reading; the disagreement is reported either
   way.
3. **A post-hoc degeneracy screen**, written after the first run produced a "+47% Nigerian
   refinery-intake response" that is a near-zero denominator. It is computed from the series alone
   (>10% zero observations, or monthly log-change SD > 25) and never from a coefficient, it is
   labelled post-hoc wherever it appears, and **both tallies are published** (22/954 unscreened,
   21/765 screened; null-expected 2–48 and 2–38 respectively).

**One thing registered wrongly, recorded for v4 and not changed now.** C.2 set the JODI headline at
h = 3 months. The external check (`bh.supply_shock`, the identified structural supply shock, on JODI
aggregate production, same code) shows the production response lives at h = 0–1 and is gone by h = 2,
while the same shock's price response runs undiminished to h = 12. **h = 3 was registered where a
physical response has already decayed.** The headline stands for this study because it was sealed;
v4 should register h = 0–1 for quantity outcomes. The corpus dummies find nothing at h = 0 or h = 1
either, so this did not hide a result — but it would have.

**What was NOT done.** No new shock series (the magnitude-bearing shock for non-OPEC classes remains
unbuilt and remains the study's principal weakness); no change to v2 nodes, horizons, lag lengths,
minimum n, verdict vocabulary or the BH rule; `propagation_edges` was not touched; nothing outside
`src/ripple_*`, `tests/test_ripple_*`, `data/ripple/**` and this session's own docs was edited.
