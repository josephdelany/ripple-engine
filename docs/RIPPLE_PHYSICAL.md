# The physical half of the ripple study — Amendment C, as computed

*2026-09-03, session C. Registered in `RIPPLE_REGISTRATION.md` **Amendment C** (2026-09-02), which
fixed every sample size below **before anything was computed** and said so. All nine JODI counts and
all nine PortWatch counts reproduce exactly, including the counterintuitive one the amendment
recorded in advance so it could not later look like a bug. Estimates are read from
`data/ripple/physical.json`, written by `src/ripple_physical.py`, which **imports** its estimator
from `src/ripple_lp.py` rather than re-implementing it — a test asserts that. Verdict words are the
registered three: **TRANSMITTING / NULL / INSUFFICIENT**.*

---

## The one-sentence result

Physical quantities do not rescue the chain: across 954 JODI cells and 168 PortWatch cells the
corpus shocks move no barrels that this design can see — but the same code **does** find an
identified structural supply shock in the same production data, which turns the null from empty
into **bounded**, and the two chokepoint closures in the record show plainly why price and physics
came apart.

**Read section 0 before any estimate.** The physical record goes dark for the producers that
matter, and it goes dark because of the geopolitics.

---

## 0. Coverage first — the record goes dark, and not at random

This section conditions everything after it. JODI-Oil is a **voluntary** submission system: a
country reports because it chooses to. Six major producers stopped choosing to.

| reporter | production ends | exports ends | stocks ends | intake ends | demand ends |
|---|---|---|---|---|---|
| **Iran** | **2018-07** | 2018-07 | 2018-07 | 2018-07 | 2018-07 |
| **United Arab Emirates** | **2018-12** | 2018-12 | 2018-12 | 2018-12 | 2018-12 |
| **Qatar** | **2018-12** | 2018-12 | 2018-12 | 2018-12 | 2018-12 |
| Brazil | 2022-12 | 2022-12 | 2022-12 | 2022-12 | 2022-02 |
| **Russia** | **2023-03** | 2021-12 | **2009-12** | 2023-03 | — |
| **Iraq** | **2024-03** | 2024-03 | 2024-03 | 2024-03 | 2024-03 |
| India | 2026-03 | 2019-03 | 2026-03 | 2026-03 | 2026-03 |
| Kazakhstan | 2026-05 | 2026-05 | **2014-03** | — | — |
| Mexico | 2026-05 | 2026-05 | 2026-05 | 2026-05 | 2026-05 |

Iran's entire JODI record — production, exports, stocks, refinery intake, product demand — stops in
**July 2018**, the month US secondary sanctions were reimposed. The UAE and Qatar stop five months
later. Russian crude **stocks** stop in **2009**. These are not broken loaders: all six continue
publishing the barrels-per-tonne conversion factor, which a careless loader would mistake for a
volume (`RIPPLE_SOURCES.md` §5 records the trap).

**The consequence, stated as a selection problem with no correction available.** The panel is
structurally missing the OPEC core after 2018. Any post-2018 physical result is conditioned on the
states that kept reporting, and the states that kept reporting are the ones that were not
sanctioned, invaded, or at war. That is the opposite of a random sample, and no weighting fixes it,
because the missingness is caused by the treatment.

### 0.1 The selection problem, quantified

For each producer: de-overlapped corpus events naming it as actor or target, and how many fall
while it was still reporting production.

| producer | last production report | named events | within reporting span | **lost to the go-dark** |
|---|---|---|---|---|
| United States | still reporting | 23 | 22 | 1 |
| **Iran** | 2018-07 | 21 | **8** | **13** |
| **Russia** | 2023-03 | 20 | **14** | **6** |
| China | still reporting | 15 | 15 | 0 |
| Saudi Arabia | still reporting | 10 | 10 | 0 |
| Iraq | 2024-03 | 7 | 7 | 0 |
| Nigeria | still reporting | 7 | 7 | 0 |
| Venezuela | still reporting | 7 | 7 | 0 |
| United Arab Emirates | 2018-12 | 1 | **0** | **1** |

Across all reporters: **122** named de-overlapped events, **101** inside the producer's reporting
span, **21 lost**. Iran loses 62% of its own events. And the attrition compounds inside the
regression: Iran's 8 in-span events become **4** usable observations once the local projection needs
`y[t+3]` and `y[t-1]` and six own lags, so the country with the most sanctions events in the corpus
contributes four.

PortWatch, by contrast, is complete: 7 chokepoints × 3 fields × **2,799 calendar days**
(2019-01-01 → 2026-08-30), no missing day. Its limit is the other one — it begins in 2019, so it
cannot see any disruption before then.

---

## 1. The seal held

Amendment C fixed these before the estimator existed.

| shock set | JODI registered | computed | PortWatch registered | computed |
|---|---|---|---|---|
| chokepoint_disruption | 21 | **21** | 14 | **14** |
| infrastructure_attack | 21 | **21** | 14 | **14** |
| conflict_escalation | 34 | **34** | 17 | **17** |
| opec_decision | 38 | **38** | 15 | **15** |
| sanctions | 36 | **36** | 19 | **19** |
| demand_shock | 13 | **13** | 9 | **9** |
| policy_response | 36 | **36** | 22 | **22** |
| all (pooled) | 67 | **67** | 16 | **16** |
| tightening (pooled) | 51 | **51** | 24 | **24** |

Including the fact C.3 recorded in advance: in the 2019+ window the pooled `all` set de-overlaps to
**16** clusters, *fewer* than the `tightening` subset's **24**, because the 35-day chain rule merges
dense post-2019 events. C.3 registered the consequence — `all` is **not used** for PortWatch — and
this run obeys it. 294 months, 67 of them carrying an event; 21 production series with ≥200 months,
exactly as C.2 said.

---

## 2. JODI — country production

### 2.1 The registered primary test barely exists

C.2's primary is **the producer the event itself names**. Of 22 reporters, four clear the registered
minimum of 15 named de-overlapped events, and only on the pooled `all` set — **no country clears
n = 15 for any single class, and none clears it for `tightening`.**

| producer | named (all) | named (tightening) | usable in the regression |
|---|---|---|---|
| United States | 23 | 4 | 22 |
| Iran | 21 | 8 | **4** (record ends 2018-07) |
| Russia | 20 | 11 | **12** (record ends 2023-03) |
| China | 15 | 1 | 15 |
| Saudi Arabia | 10 | 8 | — below minimum |

Every estimable cell is NULL:

| cell | n | β(h=3) [95%] | verdict |
|---|---|---|---|
| `us.crude_production` × all | 22 | −0.076% [−3.115, +2.963] | NULL |
| `us.refinery_intake` × all | 22 | −1.135% [−3.655, +1.384] | NULL |
| `us.crude_stocks` × all | 22 | −0.795% [−2.743, +1.153] | NULL |
| `us.crude_exports` × all | 22 | −4.661% [−16.467, +7.145] | NULL |
| `us.products_demand` × all | 22 | −1.565% [−3.908, +0.777] | NULL |
| `cn.crude_production` × all | 15 | +0.087% [−1.018, +1.192] | NULL |
| `cn.refinery_intake` × all | 15 | −0.822% [−4.371, +2.728] | NULL |
| `cn.products_demand` × all | 15 | +0.404% [−3.477, +4.284] | NULL |

**The two countries that survive the registered primary test are the United States and China** —
a price-responsive shale producer and a country that appears in the corpus mostly as the *subject of
demand events*. Saudi Arabia, the one producer whose output is a genuine swing variable, is named ten
times. That is the whole test.

### 2.2 The pooled panel and the balanced aggregate

C.2's secondary. Ten reporters have a complete 294-month production record — **Canada, China,
Germany, United Kingdom, Japan, Nigeria, Norway, Saudi Arabia, United States, Venezuela**. Balancing
is not fastidiousness: if a country that *stops reporting* is allowed into an aggregate, it looks
exactly like a country that *stopped producing*, and since the stoppages cluster on sanctions dates
that would manufacture a causal effect out of nothing. A test asserts that no reporter in the
go-dark table is in the panel.

Panel: country fixed effects, standard errors clustered by month (the shock has no cross-sectional
variation, so time clustering binds). Headline h = 3 months.

| shock | n | β(h=3) [95%] | verdict |
|---|---|---|---|
| chokepoint_disruption | 20 | −0.383% [−2.350, +1.584] | NULL |
| infrastructure_attack | 21 | −0.291% [−1.955, +1.372] | NULL |
| conflict_escalation | 34 | −0.229% [−1.520, +1.061] | NULL |
| opec_decision | 38 | +0.147% [−1.068, +1.362] | NULL |
| sanctions | 35 | +0.180% [−1.284, +1.644] | NULL |
| policy_response | 35 | +0.631% [−0.588, +1.849] | NULL |
| all | 65 | +0.562% [−0.399, +1.523] | NULL |
| tightening | 51 | +0.085% [−0.943, +1.113] | NULL |
| *demand_shock* | *13* | *−3.789% [−6.856, −0.722]* | **INSUFFICIENT** |

**Note what the last row demonstrates.** The one panel band that excludes zero belongs to the one
class Amendment C.2 registered as INSUFFICIENT *in advance*, because 13 < 15. It is not read. Had
the amendment not been written first, that −3.8% would have been the headline of this document.

The balanced aggregate (a single series, so the placebo can score it) agrees: every cell NULL, at
every registered shock.

### 2.3 The check that decides how to read all of it

A null is worth nothing until you show the machinery can see something. v2's §4.1 did this with
Känzig's surprise on Brent. The physical analogue: does **Baumeister & Hamilton's identified
structural oil supply shock** move JODI aggregate production, using the same code that produced
every null above? Their shock is *defined* on global production, so if this data can show anything,
it can show this.

| horizon | on aggregate production | on the crude price |
|---|---|---|
| h = 0 | **+0.760 [+0.496, +1.023]** ✓ | **−3.756 [−4.829, −2.683]** ✓ |
| h = 1 | **+0.561 [+0.234, +0.889]** ✓ | **−5.245 [−7.166, −3.324]** ✓ |
| h = 2 | +0.320 [−0.105, +0.744] | **−5.450 [−7.654, −3.246]** ✓ |
| **h = 3 (registered headline)** | +0.200 [−0.236, +0.637] | **−4.646 [−7.074, −2.217]** ✓ |
| h = 6 | −0.062 [−0.498, +0.374] | **−6.042 [−8.120, −3.963]** ✓ |
| h = 9 | +0.024 [−0.595, +0.642] | **−6.022 [−8.313, −3.732]** ✓ |
| h = 12 | −0.245 [−0.791, +0.301] | **−5.434 [−8.208, −2.660]** ✓ |

(✓ = 95% EHW band excludes zero. n = 291 overlapping months. Känzig's monthly news shock behaves
the same way: −0.509 [−0.962, −0.055] on production at h = 0 — the correct sign for a contractionary
news shock — and +9.950% on the price, dying on production by h = 1 and persisting on the price.)

Two things follow, and they are the most useful sentences in this document.

1. **The data and the estimator work.** The JODI aggregate is not junk and the monthly local
   projection is not blind. So the nulls in 2.1 and 2.2 are about the **shocks**, exactly as v2
   concluded for prices — an unsigned dummy that weighs a coup and a communiqué alike.
2. **The registered headline horizon is wrong for a physical quantity.** Even for a *real,
   identified* supply shock the production response lives at h = 0–1 and is gone by h = 2, while
   the price response runs undiminished to h = 12. h = 3 was registered in advance and cannot be
   moved now — but it was registered where a physical response has already decayed. Physical
   quantities adjust fast and small; prices adjust slowly and large. That is a finding about the
   design, and it is the first thing v4 should fix.

**And it is not the horizon that is hiding the effect.** At h = 0 and h = 1 — where the identified
shock's own effect lives — the corpus dummies still find nothing on aggregate production
(`tightening` −0.279% [−0.877, +0.318] at h = 0; the only band excluding zero is `policy_response`
at +0.767%, one cell of 36).

### 2.4 So the null is bounded, not empty

One standard deviation of the B–H supply shock (SD = 1.734 over this window) moves aggregate
production **1.32%** at impact and the crude price **−6.51%**. Against that yardstick, at h = 0:

| shock | n | β(h=0) [95%] | largest production fall not excluded | as a share of a one-SD identified shock |
|---|---|---|---|---|
| **tightening** | 51 | −0.279% [−0.877, +0.318] | −0.88% | **0.67×** |
| all | 65 | +0.424% [−0.209, +1.058] | −0.21% | 0.16× |
| conflict_escalation | 34 | −0.009% [−0.775, +0.758] | −0.78% | 0.59× |
| chokepoint_disruption | 20 | −0.333% [−1.168, +0.503] | −1.17% | 0.89× |
| infrastructure_attack | 21 | −0.529% [−1.178, +0.120] | −1.18% | 0.89× |

**The pooled tightening result rules out that the average corpus tightening event carries as much
physical production impact as a one-standard-deviation identified supply shock.** That is a real
statement, not an absence of one. For the individual classes (n ≈ 20) the bound is 0.89× and rules
out almost nothing — those cells are underpowered, and saying "NULL" about them would be
overclaiming.

### 2.5 The exploratory family, against its own base rate

Every reporter × flow × shock, BH-controlled within each node's nine-shock family.

| verdict | all cells | cells on non-degenerate series |
|---|---|---|
| TRANSMITTING | 22 | **21** |
| NULL | 655 | 575 |
| INSUFFICIENT | 277 | 169 |
| **total** | **954** | **765** |
| **expected TRANSMITTING under a complete null** | **2–48** | **2–38** |

**The observed count sits inside its own null expectation on both counts. Nothing in this table is a
discovery**, and it is printed only so that nobody rediscovers a cell later and believes it was
hidden. The largest, `ae.refinery_intake × opec_decision` at −14.0%, belongs to a country whose
record ends in 2018 and is one cell of 954.

A **disclosed post-hoc screen** marks 21 of 106 series degenerate — more than 10% zero observations,
or a monthly log-change SD above 25. Germany reports zero crude exports in 208 of 294 months; Korea's
crude "production" has a median of 0.25 kb/d. The screen is computed **from the series alone, never
from a coefficient**, which is the least contaminated form a post-hoc screen can take, and both
tallies are published. It was written after the first run produced a "+47% Nigerian refinery-intake
response", which is a near-zero denominator and not a response. It removes exactly that one cell.

### 2.6 A defect in v2, recorded not repaired quietly

v2 ran every monthly node with `do_placebo=False`. Amendment B's TRANSMITTING verdict **requires**
the placebo. Therefore **every monthly cell in v2 was NULL-or-INSUFFICIENT by construction**, and
`docs/RIPPLE_FINDINGS.md` §1.2's striking "hop 4 fertilizer: zero transmitting cells out of 54" was
not a finding about fertilizer — it was arithmetic about a flag. Hop 3 is 3/5 affected the same way.
This run implements the registered daily placebo construction on the monthly grid so the verdict
means something.

It is weak, and the weakness is reported rather than buried: the pool is **108 non-event months**
across **58 state buckets**, and on average **26.4 buckets per cell** fall back to VIX-decile-only
matching. A monthly TRANSMITTING verdict therefore rests mainly on the two standard-error bands and
only weakly on the state match. See the erratum in §6.

---

## 3. PortWatch — chokepoint transits

### 3.1 The registered primary test is INSUFFICIENT at every chokepoint

C.3's primary is **the chokepoint the event names**.

| chokepoint | named de-overlapped events, 2019+ | clears n ≥ 15? |
|---|---|---|
| Strait of Hormuz | 8 | no |
| Bab el-Mandeb | 5 | no |
| Suez Canal | 1 | no |
| Cape of Good Hope | 0 | no (it is the reroute counter-node by design) |
| Malacca, Panama, Bosporus | 0 | no |

**All seven below the minimum.** The registered primary test returns INSUFFICIENT everywhere — and
this is knowable by counting, without estimating anything. The corpus simply does not contain
fifteen dated events naming any one strait since 2019.

### 3.2 The secondary: nothing transmits

Per-class and `tightening` shocks on all seven chokepoints × three fields, on the registered
2,799-day calendar sample:

| verdict | cells |
|---|---|
| **TRANSMITTING** | **0** |
| NULL | 105 |
| INSUFFICIENT | 63 |
| **total** | **168** |

Zero of 168. Three cells survive BH on the EHW p-value alone and none survives the placebo.

### 3.3 Erratum: v2's one transmitting physical cell does not survive

`docs/RIPPLE_FINDINGS.md` §1.4 reports **Cape of Good Hope transits × conflict_escalation, h = 5,
+20.659 [+8.772, +32.547], n = 16, BH survivor** — the only transmitting cell in the whole physical
hop, and one of only seven BH survivors in the study. v2 estimated it on the **Brent trading-day
index**, which discards weekends. Tanker transits happen at weekends. On the registered v3 sample —
the full 2,799 calendar days — the same cell is:

| index | h = 5 | band excludes zero? |
|---|---|---|
| Brent trading-day (v2) | **+18.04 [+5.85, +30.23]** | yes |
| **calendar, full record (registered)** | **+4.03 [−6.89, +14.96]** | **no** |

And it is not a horizon artefact. Trading-day h = 5 spans a mean of **7.2 calendar days**; the
matched calendar estimate at h = 7 is **+3.69 [−9.60, +16.99]**, covering zero. On the calendar
index this cell covers zero at **every one of nine horizons** (0, 1, 2, 5, 7, 10, 20, 40, 60). On the
trading-day index it excludes zero at exactly one of six — h = 5, which happens to be the registered
headline.

**Verdict on the full physical record: NULL.** Two further cells flip the same way — `bab_el_mandeb
× tightening` (+11.10 [+0.1, +22.1] trading-day, −0.74 [−10.7, +9.2] calendar) and `suez ×
chokepoint_disruption` (+18.68 [+5.5, +31.8] trading-day, −9.07 [−31.9, +13.8] calendar). Adding
day-of-week dummies to the calendar spec moves none of these three by more than 0.30 (across all 56
transit cells the largest shift is 1.74), so the difference between the indices is the discarded
third of the record, not a weekly cycle.

v2's §5.7 already hedged this cell as "a description of that episode, not an estimate of a general
response". That hedge was right and did not go far enough. The sealed v2 tables are **not edited**;
this erratum stands beside them.

### 3.4 The reroute counter-node

C.3 registered the falsification in advance: a real Red Sea closure should move Bab el-Mandeb **down**
and Cape of Good Hope **up**; both moving the same way is a common time trend, not a disruption.

| shock | Bab el-Mandeb β(h=5) | Cape of Good Hope β(h=5) | reading |
|---|---|---|---|
| chokepoint_disruption | +2.13 | +3.29 | **common time trend, not a reroute** |
| sanctions | −7.84 | −4.92 | **common time trend, not a reroute** |
| infrastructure_attack | −1.81 | +0.16 | consistent with a reroute |
| conflict_escalation | −5.30 | +4.03 | consistent with a reroute |
| tightening | −0.74 | +7.11 | consistent with a reroute |
| opec_decision, demand_shock, policy_response | — | — | opposite signs, wrong way round |

Three of eight point the registered right way; **not one of them excludes zero**, so the counter-node
neither confirms nor falsifies. The registered check fired on the class it was aimed at:
`chokepoint_disruption` moves *both* nodes up.

### 3.5 Leave-one-episode-out (mandatory under C.3)

Dropping the Red Sea window (2023-12-01 → 2024-12-31, 397 days) and the Hormuz window (2026-03-01 →
2026-08-30, 183 days), plus a jackknife over event clusters.

- C.3's registered worry was that the Cape of Good Hope result "is almost certainly that episode".
  On the calendar index it is not: dropping the Red Sea window makes it *larger* (+7.11 → +9.16 for
  `tightening`). But it never excluded zero on this sample either way, so this is a null being
  robust, not a result being robust.
- The Hormuz transit response to `chokepoint_disruption` **is** the 2026 closure: −12.15 with the
  window, **−4.32** without it.
- Cluster jackknife over 35 (node × shock) cells: **10 change sign** when a single de-overlapped
  event is removed. At n ≈ 20 these coefficients are one event wide.

---

## 4. The two episodes — described, never estimated

This is the part physical data buys that a price series cannot, and it is also the part no estimator
in this study is entitled to speak about: **n = 1 each**. They are levels.

| episode | measure | before | after | change |
|---|---|---|---|---|
| **Red Sea 2024** | Bab el-Mandeb, tankers/day | 26.32 | 11.42 | **−56.6%** |
| | Cape of Good Hope, tankers/day | 9.50 | 19.18 | **+101.8%** |
| | Brent, $/bbl | 84.69 | 80.56 | **−4.9%** |
| **Hormuz 2026** | Hormuz, tankers/day | 40.36 | 3.09 | **−92.3%** |
| | Cape of Good Hope, tankers/day | 16.63 | 20.07 | **+20.7%** |
| | Brent, $/bbl | 66.03 | 98.06 | **+48.5%** |

(Red Sea: 2023-06→11 vs 2024-02→12. Hormuz: 2025-09→2026-02 vs 2026-03-05→2026-08-30. The corpus
records both: `hormuz_closure_2026`, 2026-03-04, chokepoint_disruption, severity 5, target
`chokepoint.hormuz`.)

**Put side by side, these two are the study's real content.** Two chokepoint closures of comparable
severity, opposite price outcomes, and the physical data showing exactly why:

- The Red Sea closure was **reroutable**. Traffic halved at Bab el-Mandeb and *doubled* round the
  Cape. The barrels still arrived, later and dearer in freight, and **Brent did not move** — it was
  4.9% *lower* afterwards. A price-only study sees nothing here and concludes nothing happened. A
  physical study sees a 56.6% flow collapse and a textbook reroute.
- The Hormuz closure is **not reroutable**. There is no way out of the Gulf. Cape traffic rose only
  20.7% — refills from elsewhere, not Gulf cargoes — and **Brent rose 48.5%**.

That contrast is the mechanism behind v2's headline null. The corpus's tightening classes are
dominated by disruptions that are *reroutable*, and a reroutable disruption is a freight event, not a
price event. This is the first evidence in the project that can distinguish "the shock was not real"
from "the shock was real and the market correctly ignored it", and it says the latter, at least for
the Red Sea.

### 4.1 The reopening that reopened nothing

The corpus records `us_iran_hormuz_mou_2026` on 2026-06-17: a policy_response that "reopens the
Strait of Hormuz".

| month | Brent $/bbl | Hormuz tankers/day |
|---|---|---|
| 2025-12 | 62.54 | 30.42 |
| 2026-01 | 66.60 | 31.13 |
| 2026-02 | 70.89 | 43.46 |
| 2026-03 | 103.13 | **0.94** |
| 2026-04 | **117.29** | 2.60 |
| 2026-05 | 107.14 | 1.71 |
| 2026-06 *(MOU on the 17th)* | 85.40 | 5.67 |
| 2026-07 | 83.76 | 5.74 |
| 2026-08 | 91.40 | 1.77 |

**Brent has given back 55.8% of its spike. Hormuz tanker traffic has recovered 2.0% of its
collapse.** The market priced the reopening; the barrels have not moved. As of the last day of data
(2026-08-30) the strait is carrying about 4% of its February throughput.

This is stated as **description, not inference** — it is one episode, still in progress, and the
last observation is three days old. But it is the sharpest illustration available of why Amendment C
was written: a price is a belief about barrels, and here the belief and the barrels disagree by an
order of magnitude. It is also a live risk to anything in this repo that treats the price as the
outcome.

---

## 5. What this adds that v2 could not have

1. v2's nulls could always be read as "the market had already priced it". §4 shows a case where the
   market priced **nothing** and the disruption was enormous (Red Sea), and a case where the price
   moved and the disruption persists past the price's retracement (Hormuz). Neither reading is
   available from a price series alone.
2. §2.3 gives the physical analogue of v2's Känzig check: identified shocks are visible in this data
   at h = 0–1; corpus dummies are not visible at any horizon. The weakness is the shock design, on
   both halves of the study, and it is now shown twice with different outcome types.
3. §2.4 converts a null into a bound. The pooled tightening shock carries less physical production
   impact than a one-SD identified supply shock.
4. §3.3 retracts v2's only transmitting physical cell.

---

## 6. Limits, at full strength

1. **The missingness is caused by the treatment.** §0. The producers the corpus names are the
   producers that stopped reporting. There is no correction for this and none is offered.
2. **The registered headline h = 3 is the wrong horizon for a quantity** (§2.3). Registered in
   advance, so it stands for this study; it should not stand for the next.
3. **The primary tests barely exist.** JODI: two countries, one shock set. PortWatch: nothing above
   the minimum at any chokepoint. Most of what is reported here is secondary or exploratory.
4. **The monthly placebo is thin** (§2.6): 108 pool months, 58 buckets, heavy fallback to
   VIX-only matching.
5. **Erratum to v2** (§2.6, §3.3): v2 ran no monthly placebo, so its monthly hops could not
   transmit by construction; and v2's Cape of Good Hope cell does not survive the full calendar
   record. `docs/RIPPLE_FINDINGS.md` is not edited — this document stands beside it.
6. **21 of 106 JODI series are degenerate** (§2.5). The screen is post-hoc and labelled.
7. **The corpus dummies carry no magnitude**, unchanged from v2 §5.1 and now demonstrated on
   physical outcomes too.
8. **PortWatch begins in 2019**, so six of the seven chokepoint nodes have never seen a disruption
   in sample, and the two that have are the two episodes of §4.
9. **The pooled `all` shock is unusable in the PortWatch window** (16 clusters < 24 for the subset),
   registered in advance and obeyed.
10. **At n ≈ 20, 10 of 35 jackknifed transit cells flip sign on removing one event** (§3.5).
11. **The two episodes are n = 1.** Nothing in §4 is an estimate, and the Hormuz episode is
    unfinished.
12. **JODI is refresh-only by licence** (`RIPPLE_SOURCES.md` §5): access was read as access, not as
    redistribution rights, so a fresh clone cannot rebuild those 106 series offline. PortWatch is
    seeded and reproducible; JODI is not.

---

## Appendix — provenance

Run `2026-09-03T03:25:09Z`, seed 19900802, runtime 130.6 s. Estimator: `src/ripple_lp.py`, imported.
Driver: `src/ripple_physical.py`. Output: `data/ripple/physical.json`, summary
`data/ripple/PHYSICAL_SUMMARY.md`. Tests: `tests/test_ripple_physical.py`, 20 passed.

| numbers | path in `data/ripple/physical.json` |
|---|---|
| the go-dark table, months-per-year matrix | `jodi_coverage.went_dark`, `.production_months_per_year` |
| the selection table (§0.1) | `jodi.named_producer_counts[]` |
| registered-n reconciliation (§1) | `jodi.shock_counts_deoverlapped`, `portwatch.shock_counts_deoverlapped` |
| named-producer cells (§2.1) | `jodi.named_producer_primary[]` |
| the pooled panel (§2.2) | `jodi.pooled_panel[]`; members in `jodi.balanced_panel_members` |
| B–H and Känzig checks (§2.3) | `jodi.external_check` |
| the bound (§2.4) | `jodi.bounded_null.h0` |
| exploratory tallies and base rate (§2.5) | `jodi.exploratory_tally`, `.exploratory_tally_clean` |
| degeneracy screen | `degeneracy_screen` |
| monthly placebo diagnostics (§2.6) | `jodi.monthly_placebo_diagnostics` |
| named-chokepoint counts (§3.1) | `portwatch.named_chokepoint_primary[]` |
| the 168-cell tally (§3.2) | `portwatch.secondary_tally` |
| the erratum's two indices (§3.3) | `portwatch.secondary_calendar[]` vs `.robustness_trading_day_index[]`; day-of-week in `.robustness_day_of_week[]` |
| reroute counter-node (§3.4) | `portwatch.reroute_counter_node[]` |
| leave-one-episode-out (§3.5) | `portwatch.leave_one_episode_out` |
| both episodes and the disconnect (§4, §4.1) | `episodes.red_sea_2024`, `episodes.hormuz_2026`, `.the_disconnect` |
| PortWatch source, licence, attribution | `RIPPLE_SOURCES.md` §5; `series.notes` |

Sources: UN Global Platform; IMF PortWatch (portwatch.imf.org). JODI-Oil (jodidata.org), refresh-only.
