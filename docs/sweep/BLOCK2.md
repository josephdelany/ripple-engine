# Findings sweep — block 2

*2026-09-03, Session C. Same convention and evidence grades as `docs/OIL_FINDINGS.md`:
**[TESTED]** a hypothesis test with an interval, corrected where a family exists · **[DESCRIPTIVE]**
a measured count or rate with no test · **[NULL]** a test run and not rejected · **[CASE]** two or
three episodes, illustrative. Every figure traced to a named file. Report only — nothing outside
this file was edited.*

**Scope.** `data/big_moves/{wti,wti_monthly,diesel_crack}.json` · `data/propagation.json` ·
`data/propagation_graph.json` · `data/supply_chain.json` · `data/spec_curve.json` ·
`data/calibration_report.json`. Brent is read only as the published comparator.

**Headline.** The brief asked whether the anticipation structure differs by asset. **It does not.**
The apparent cross-asset differences in the published table are a composition artifact, and the
composition-free metric puts all four assets within 6.6 points of each other. Separately, one file
in scope carries a live stale claim of exactly the kind already retracted elsewhere, and one
published cell does not reproduce from any file.

---

## Part 1 — the big-moves files

### B2-1 [NULL] The anticipation structure does **not** differ by asset

`docs/OIL_FINDINGS.md` §3 tabulates, per asset, the share of attributed episodes where *every*
attributed event was already public and where *any* was. Those columns span a wide range and invite
a cross-asset reading:

| asset | "all anticipated" | "any anticipated" |
|---|---:|---:|
| Brent | 50% | 73% |
| WTI | 38% | **59%** |
| diesel crack | 31% | **86%** |
| WTI monthly | 29% | 76% |

**Both columns are mechanically driven by how many events an episode carries**, and that varies more
than three-fold across the files:

| asset | attributed episodes | events | **events per episode** | event-level anticipated |
|---|---:|---:|---:|---:|
| Brent | 30 | 77 | 2.57 | 68.8% |
| WTI | 34 | 79 | **2.32** | 67.1% |
| diesel crack | 29 | 111 | **3.83** | 63.1% |
| WTI monthly | 17 | 98 | **5.76** | 62.2% |

Hold the event-level anticipation rate **identical across all four assets** at a single common value
and resample each asset's own episode sizes 20,000 times. The spread reappears almost in full from
composition alone:

| asset | expected "all" | observed | expected "any" | observed |
|---|---:|---:|---:|---:|
| Brent | 33.3% | 50.0% | 74.9% | 73.3% |
| WTI | 37.5% | 38.2% | 71.1% | 58.8% |
| diesel crack | 23.7% | 31.0% | 83.0% | 86.2% |
| WTI monthly | 22.1% | 29.4% | 84.1% | 76.5% |

**The composition-free metric is the event-level share, and on it the four assets are
indistinguishable** — 68.8%, 67.1%, 63.1%, 62.2%, with Wilson 95% intervals
[57.8, 78.1], [56.1, 76.4], [53.8, 71.5] and [52.4, 71.2]. Every interval contains every other
point estimate.

**The answer to the brief's question is no**, and the published table should not be read as showing
an asset difference. This is a caution about the *presentation*, not a defect in the data: the
files are correct and §3's per-asset rows are individually reproducible (below).
`data/big_moves/{brent,wti,diesel_crack,wti_monthly}.json` · `episodes[].events[].anticipated`

### B2-2 [DESCRIPTIVE] Brent and WTI are very nearly the same evidence, and `anticipated` is asset-relative

| pair | shared event ids |
|---|---:|
| Brent ∩ WTI | **60** (of 70 and 72 distinct) |
| Brent ∩ diesel crack | 24 |
| WTI ∩ diesel crack | 25 |
| all three | 20 |

Of the 69 events scored by more than one asset, **26 disagree on `anticipated` and 60 disagree on
`lag_days`** — because lag is measured to each asset's own episode onset. Two consequences:
`anticipated` is a property of the **(event, asset) pair**, not of the event; and Brent and WTI are
**not independent samples**, so any test pooling them overstates its degrees of freedom. All tests
in B2-3 are reported with that caveat attached.
`data/big_moves/*.json` · `episodes[].events[].lag_days`

### B2-3 [NULL] Anticipation differs neither by event class nor by direction of the move

Pooled across the three daily assets (267 event×asset rows, 158 distinct event ids):

| test | statistic | *p* |
|---|---|---:|
| class × anticipated | χ² = 6.60, dof 6 | **0.360** |
| lag by class | Kruskal–Wallis H = 7.85 | **0.249** |
| direction × anticipated (up 62.7% vs down 68.2%) | χ² = 0.62 | **0.430** |

**A tempting contrast that must not be reported as a finding.** By class, `chokepoint_disruption`
looks distinct — 83.3% anticipated (15/18) and a 55-day median lag, against 57.8% and 26 days for
`infrastructure_attack` + `conflict_escalation` pooled (Mann–Whitney *p* = 0.0152 on the lag).
That is the extreme pair selected from seven classes **after** seeing the table, and its own omnibus
test is null at *p* = 0.249. Under the standard `OIL_FINDINGS.md` §1 already set for itself, this is
a hypothesis and not a result. Recorded here so it is not rediscovered and promoted.
`data/big_moves/{brent,wti,diesel_crack}.json`

### B2-4 [DESCRIPTIVE] The monthly tier's 94% attribution rate is an artifact, not a signal

`wti_monthly` attributes 17 of 18 episodes (94%) against 68–78% for the daily files. It is tempting
to read that as the monthly market being more explicable. It is not.

| asset | episodes | median episode length | **events per 100 episode-days** | attributed |
|---|---:|---:|---:|---:|
| Brent | 44 | 76 d | 2.96 | 68% |
| WTI | 48 | 78 d | 2.86 | 71% |
| diesel crack | 37 | 82 d | 4.20 | 78% |
| **WTI monthly** | **18** | 92 d | **2.75 — the lowest** | **94%** |

**Event density is flat across the four files; the monthly tier has the lowest of all.** Its high
attribution rate comes from partitioning the same event stream into fewer, longer episodes, which
raises the chance that any one episode contains at least one event.

And the single unattributed monthly episode is **1947-10**, while the corpus begins **1973-10-06**.
The monthly tier therefore attributes **100% of the episodes the corpus can reach**, which is a
statement about the corpus window rather than about the market.
`data/big_moves/wti_monthly.json` · `data/oil.db` `events`

### B2-5 [DESCRIPTIVE] What the monthly tier *does* uniquely show: the pre-1986 shocks

Five of 18 monthly episodes begin before **1986-01-02**, the earliest first date in any daily file,
and are structurally invisible to the daily tier:

| onset | change | length | attributed events |
|---|---:|---:|---|
| 1947-10 | +37.4% | 92 d | none — predates the corpus |
| **1973-01** | **+184.0%** | 365 d | Yom Kippur war, OAPEC embargo |
| 1973-10 | +134.6% | 92 d | Yom Kippur war, OAPEC embargo |
| **1979-04** | **+149.2%** | 366 d | Iran hostage crisis, Carter doctrine |
| 1985-11 | −62.4% | 242 d | 1986 OPEC price collapse |

Median |change| is **68.9%** monthly against 37.6% (Brent) and 37.3% (WTI) daily.

**One correction to the natural reading.** The monthly tier does *not* contain the largest move in
the record: that is **Brent 2020-04, +379.3%** in the daily file (WTI 2020-04, +357.2%), against a
monthly maximum of +184.0%. The monthly tier's contribution is **era coverage, not magnitude** — it
is the only file that contains the 1973 and 1979 shocks at all.

**Its lag figures are not comparable to the daily tier's** and should not be placed in the same
table: monthly `lag_days` runs median 72, 75th percentile 217, maximum 359, against Brent's median
31 and maximum 85, because lags are measured to an onset resolved only to the month.
`data/big_moves/wti_monthly.json`

---

## Part 2 — propagation, supply chain, specification curve, calibration

### B2-6 [CONTRADICTION — a live stale claim] `propagation_graph.json` retracts five edges and still labels those same five `"validated"`

The file states `backbone_validated: []` (zero) and lists five edges under
`backbone_retracted_2026_09_02`: **Brent oil, Heating oil, 5Y breakeven, S&P 500, Platinum.**

Its `amplification` array contains 25 entries, of which exactly **five carry `"status": "validated"`**
— and they are **the same five**:

| from | to | strength | CI | status in file |
|---|---|---:|---|---|
| geopolitical shock (VIX-stress regime) | **Brent oil** | +6.041% | [1.557, 10.087] | `validated` |
| " | **Heating oil** | +5.030% | [1.527, 9.230] | `validated` |
| " | **5Y breakeven** | +16.247 bps | [4.470, 31.022] | `validated` |
| " | **S&P 500** | +1.894% | [0.342, 3.448] | `validated` |
| " | **Platinum** | +7.425% | [1.958, 14.647] | `validated` |

Any consumer filtering `amplification[].status == "validated"` **recovers precisely the retracted
backbone**. This is the same defect class as the `severity_dose_response` entry in
`data/edge_battery.json` (OPEN_ITEMS 1.5): a machine-readable claim that other surfaces read as
current, contradicted by prose in its own file. These five are the edges retracted in
`docs/RIPPLE_FINDINGS.md` §3 after the VIX+GPR-matched re-test.

**Recommended treatment, the one already used in `src/propagation_graph.py`:** carry the status as
an explicit retraction rather than leaving `"validated"` in the record. Not actioned here — this is
a report.
`data/propagation_graph.json`

### B2-7 [NULL] No event→node edge in the propagation graph survives multiple-testing correction

The file reports `event_to_node_n_ci_excludes_zero: 13`. Of the eight strongest listed, every one
whose CI excludes zero carries an FDR *q* between **0.7699 and 0.8198**; the two that do not exclude
zero carry *q* = 0.9418.

| from | to | n | strength | CI excludes zero | **FDR q** |
|---|---|---:|---:|---|---:|
| demand_shock | 5Y breakeven | 13 | −21.49 bps | yes | 0.820 |
| demand_shock | Dry-bulk freight | 10 | −12.96% | yes | 0.770 |
| demand_shock | 10Y breakeven | 13 | −12.02 bps | yes | 0.820 |
| policy_response | 5Y breakeven | 36 | −8.36 bps | yes | 0.820 |
| demand_shock | Palladium | 14 | −7.82% | yes | 0.820 |
| policy_response | 10Y breakeven | 36 | −7.13 bps | yes | 0.820 |

**Nothing survives.** The file is honest about this — it carries `fdr_q` and its own `what` field
says the layer is "mostly null at this N — reported, not hidden". The count of 13 is a count of
uncorrected hits and must never be quoted without the *q* column beside it.
`data/propagation_graph.json` · `event_to_node_strongest[]`

### B2-8 [DESCRIPTIVE] Crude co-moves with its neighbours; it does not lead them

Six `node_to_node` edges are classified `trap`, all from Brent:

| to | lag | lead corr | contemporaneous corr |
|---|---:|---:|---:|
| Heating oil | 4 d | +0.042 | **+0.531** |
| 10Y breakeven | 1 d | +0.038 | +0.307 |
| Copper miners | 2 d | +0.036 | +0.281 |
| 5Y breakeven | 4 d | +0.035 | +0.278 |
| Broad USD | 1 d | −0.025 | −0.249 |
| Copper | 1 d | −0.016 | +0.242 |

Lead correlations are an order of magnitude smaller than contemporaneous ones. **Any product built
on "crude leads X by N days" at daily frequency is trading a correlation of about 0.03.** The
remaining 18 `node_to_node` edges are `null`. Naming these `trap` rather than dropping them is the
right call and worth keeping.
`data/propagation_graph.json` · `node_to_node[]`

### B2-9 [NULL] The producer-conflict → commodity channel is empty, and a third of it was never testable

`supply_chain.json`: 14 edges tested, **`validated: []`**, and **0 of 14 confidence intervals exclude
zero**. Five of the 14 return `car: null` because n falls below the file's own
`min_producer_events: 6` — South Africa/palladium (n = 4), Canada/wheat (1), Australia/wheat (0),
Ukraine/wheat (5), Australia/natural gas (0), Qatar/natural gas (1).

The widest intervals are enormous: Saudi Arabia → crude oil, n = 10, CAR **−3.401% [−23.245,
+12.538]**. **This is a complete null, correctly labelled as one by the file**, and its more useful
reading is a power statement: at these sample sizes the design could not have detected anything
short of a very large effect.
`data/supply_chain.json`

### B2-10 [DESCRIPTIVE] The specification curve is robust, and its registered spec is not cherry-picked

108 specifications, **105 positive (97.2%)**. The registered specification returns
**amp = 5.0003 at n = 86**.

**One caution on the headline.** The 108 specs pool two incompatible scales, and the summary's
"97.2% positive" mixes them:

| scale | n | median amp | range | positive |
|---|---:|---:|---|---:|
| `raw` | 54 | **+5.880** | [+3.791, +11.459] | 54/54 |
| `std` | 54 | **+0.200** | [−0.037, +0.326] | 51/54 |

Compared within its own scale group, **the registered spec sits at the 28th percentile** of the raw
distribution — below its median, not above. That is the favourable direction: the registered choice
was not the flattering one. The three negative specs are all in the `std` group and all tiny
(minimum −0.037).
`data/spec_curve.json`

### B2-11 [NULL, and a metric that should not be aggregated] The forecaster has no skill over its base rate, and the quarterly series cannot be read as skill

Pooled: **n = 247, base rate 0.522, Brier 0.245 against a base-rate Brier of 0.2495 —
`skill_vs_base` = +0.0045.** That is 1.8% of the base-rate Brier. **No skill.**

Reliability has only two bands and both sit next to the base rate:

| band | n | mean forecast | observed |
|---|---:|---:|---:|
| 0.4–0.6 | 107 | 0.400 | 0.439 |
| 0.6–0.8 | 140 | 0.600 | 0.586 |

**The forecaster never leaves the neighbourhood of the base rate**, so there is little for a
calibration curve to discriminate.

**The quarterly field is a trap and the apparent contradiction is not real.** `quarters[].skill_vs_base`
is negative in **63 of 67 quarters** (median −0.1378, positive in 4), which looks like it contradicts
the pooled +0.0045. It does not:

- **30 of 67 quarters have a within-quarter base rate of exactly 0 or 1.** That forces
  `base_rate_brier` to 0 and therefore `skill_vs_base = −brier`, **negative by construction whatever
  the forecast did.** Example, 2007Q3: `n = 1, base_rate = 0.0, brier = 0.36, base_rate_brier = 0.0,
  skill_vs_base = −0.36`.
- **57 of 67 quarters are flagged `thin`**, median n = 2 (minimum 1, maximum 13).

So the quarterly median is not a skill measure and should not be averaged or plotted as one. The
honest statement is the pooled one: **no skill, on n = 247.** The file's own `thin` flag is what
protects a reader here, and it should be respected downstream.
`data/calibration_report.json`

### B2-12 [DESCRIPTIVE] `propagation.json` is a sourced hypothesis map, not a result

13 chains, 12 live, 9 of them chokepoint-triggered, across 10 active-situation countries, each with
`triggered_by`, `choke`, `downstream`, `lag`, `observe` and `source`. **Nothing in the file is
tested** — there is no interval or *p*-value anywhere in it, and its `note` describes live chains as
transmission paths whose trigger condition is currently met. It should be cited as a registered map
of *what to watch*, never as evidence that the chains transmit. B2-7 and B2-9, which do test
adjacent propositions, are both null.
`data/propagation.json`

---

## Part 3 — contradictions with published claims

**C-1 — one published cell does not reproduce from any file.** `docs/OIL_FINDINGS.md` §4 gives
`OPEC decision | 17/51 (31%)` in its crude column. Every other cell in that column matches Brent's
registered values exactly. No file and no variant yields 17:

| asset | registered | `as_computed` |
|---|---:|---:|
| Brent | **16/51** | 15/51 |
| WTI | 14/51 | 15/51 |
| diesel crack | 13/51 | 12/51 |

16/51 = 31.4%, and §4 prints **31%** — so the printed percentage is consistent with 16 and the
numerator 17 appears to be a transcription slip. **The 0.8× ratio and the conclusion are unaffected**,
but the count is wrong as printed.
`data/big_moves/{brent,wti,diesel_crack}.json` · `p_big_given_class`

**C-2 — §4's open inconsistency is resolved.** §4 flags "`infrastructure_attack` shows 44 against
crude and 45 against the crack" as something to resolve. The cause is the series start dates:
**`iraq_kharg_1986` (1986-08-12)** falls after WTI's first date (1986-01-02) and after the diesel
crack's (1986-06-02) but **before Brent's (1987-05-20)**. It is scoreable for two assets and not for
the third. The corpus holds 48 `infrastructure_attack` events; three predate every file
(1977, 1978, 1985-08), giving 45 for WTI and the crack, and 44 for Brent. **No defect — a window
effect, and it should be recorded as such rather than left open.**
`data/oil.db` `events` · `data/big_moves/*.json` `first`

**C-3 — a stale machine-readable claim, live now.** B2-6: `propagation_graph.json` labels the five
retracted backbone edges `"status": "validated"` in the same file that reports
`backbone_validated: []`. Same class as OPEN_ITEMS 1.5.

**C-4 — a presentational contradiction, not a data error.** B2-1: `OIL_FINDINGS.md` §3's cross-asset
table is individually reproducible but invites an asset comparison the data does not support, because
both of its summary columns are functions of events-per-episode. Every per-asset row I could check
reproduces exactly, including the "all/any" counts and the median lags.

**Not a contradiction — a convention worth recording.** §3's 75th-percentile lags are **54 / 59 / 57**
for Brent / WTI / diesel. Nearest-rank gives 54 / 58 / 56. The published figures correspond to
`numpy.percentile(..., method="higher")`, which is a legitimate convention consistently applied.
Flagged only so a future re-computation does not read it as an error.

---

## Grades at a glance

| # | claim | grade |
|---|---|---|
| B2-1 | anticipation does not differ by asset; the published spread is composition | **NULL** |
| B2-2 | Brent and WTI share 60 events; `anticipated` is asset-relative | DESCRIPTIVE |
| B2-3 | anticipation differs by neither class nor direction | **NULL** |
| B2-4 | the monthly tier's 94% attribution is a partitioning and corpus-window artifact | DESCRIPTIVE |
| B2-5 | the monthly tier uniquely covers 1973 and 1979; it does not hold the largest move | DESCRIPTIVE |
| B2-6 | five retracted edges still labelled `validated` in the same file | **CONTRADICTION** |
| B2-7 | no event→node edge survives FDR (q = 0.77–0.94) | **NULL** |
| B2-8 | crude co-moves, does not lead; lead corr ≈ 0.03 vs contemporaneous ≈ 0.3 | DESCRIPTIVE |
| B2-9 | producer-conflict → commodity: 0 of 14, 5 never testable | **NULL** |
| B2-10 | spec curve robust; registered spec at the 28th percentile of its own scale | DESCRIPTIVE |
| B2-11 | no forecast skill (+0.0045 on n = 247); quarterly skill uninterpretable in 30 of 67 | **NULL** |
| B2-12 | `propagation.json` is an untested map | DESCRIPTIVE |
| C-1 | §4's OPEC numerator 17/51 does not reproduce (16/51) | **CONTRADICTION** |
| C-2 | §4's 44-vs-45 inconsistency explained by series start dates | resolved |

**Nothing in this block reaches [TESTED].** Every test run here returned null, and the two
non-null-looking results — the chokepoint lag contrast and the 13 CI-excluding-zero propagation
edges — fail their own omnibus and FDR corrections respectively. That is consistent with
`OIL_FINDINGS.md` §9 and §2: what these files mostly establish is where the effects are *not*.
