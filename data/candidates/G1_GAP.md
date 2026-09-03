# G-1 — THE MONTHLY-TIER GAP, AS COMPUTED
*2026-09-02, Session G. Registered first in `data/candidates/G1_REGISTRATION.md`
(+ Amendments 1 and 2), then computed by `src/g_monthly_gap.py`; the machine-readable
numbers are `data/candidates/G1_GAP.json`, the ranking is
`data/candidates/pre1987_ranked.csv`. Nothing here enters `events`. No threshold was
changed to make anything pass.*

## 0. The one-line answer

**33 more monthly-tier events is the arithmetic minimum, 43 for a tier that can be read,
and neither of them buys what the project wants**, because the price series the monthly
tier scores against does not move before 1973 and because the events that made 1970–73
are invisible to the sheet the candidates come from.

## 1. Where the tier stands (validation of the model first)

The predicate was re-implemented from `src/walk.py:276` and `src/engine/read.py:201` and
re-run on the real corpus. It returns **0 scored reads of 14**, which is exactly what the
published run `walk_20260903T003422Z` reports (`tiers.monthly.n_scored_burn_in = 0`). The
model is therefore the walk's rule and not a paraphrase of it.

| class | monthly events | best pool any read reached | scored reads | bound `max(0, n−8)` |
|---|---|---|---|---|
| conflict_escalation | 5 | 4 | 0 | 0 |
| infrastructure_attack | 4 | 3 | 0 | 0 |
| sanctions | 2 | 1 | 0 | 0 |
| chokepoint_disruption | 1 | 0 | 0 | 0 |
| policy_response | 1 | 0 | 0 | 0 |
| opec_decision | 1 | 0 | 0 | 0 |
| demand_shock | 0 | — | 0 | 0 |
| **tier** | **14** | **4** | **0** | **0** |

The single most useful number in that table is the third column. **Burn-in is per class,
not per tier** (`pool` requires `f.type == e.type`). The tier's best-supplied class has
reached a pool of four against a requirement of eight. The tier is not close; it is at
half of the entry requirement in its strongest class and at zero in four of seven.

## 2. What it would take (the registered arithmetic)

Activating a class costs `8 − n_c` events that score nothing, then one scored read per
event after that. Exact integer search over the seven classes:

| scenario | additional events | allocation | verdict |
|---|---|---|---|
| **minimum, concentrated** | **33** | all in `conflict_escalation` → n = 38 | arithmetically correct, **degenerate** |
| **balanced** (≥3 classes, none over half) | **43** | 10 scored each in `conflict_escalation`, `infrastructure_attack`, `sanctions` → n = 18 each | the smallest tier that can carry §6's per-class blocks |
| **all seven classes score** | **72** | 4–5 scored per class | what "the monthly tier works" actually costs |

The date-aware recount agrees with the bound rather than beating it: taking the real dates
of the screened Tier A episodes in order, 33 admissions give exactly 30 scored reads in the
concentrated case and 43 give exactly 30 in the balanced case (round-robin). Class
assignment is Joe's at admission, so it was priced rather than assumed: 200 seeded random
allocations across the three classes (seed 19900802, the walk's registered seed) need
**43 (median 43, max 45)**. Window collisions cost nothing here because the candidate dates
are spread; that is measured, not assumed.

**The minimum is degenerate and should not be taken.** Thirty scored reads all in one class
cannot be read: protocol §6's per-class blocks have one cell, the specification curve varies
thresholds against a single class, and §7's promotion rule would be deciding whether the
engine can forecast `conflict_escalation` in the 1970s and 80s, which is not the claim the
project makes. 43 is the honest floor.

## 3. Which candidates are strong (the screen, run blind)

`data/candidates/pre1987_candidates.csv`, 624 rows, collapsed by the registered ±31-day
shared-actor rule into **461 episodes**:

| tier | rule | episodes | of which pre-1973 | 1973–1986 |
|---|---|---|---|---|
| **A** — strong | producer actor **and** high severity **and** ≥2 of {ICB, COW, MID} | **59** | 37 | 22 |
| **B** | (producer or transit) and high severity, single source | 286 | 180 | 106 |
| **C** | everything else | 116 | 65 | 51 |

Amendment 1 (intra-state war in a producer state counts as severity, registered before the
run because the corpus's own Iranian-revolution events are that shape) moves **30** episodes
into A or B that the unamended rule would have dropped.

The screen never opened `pre1987_candidates_outcomes.csv`. No column of
`pre1987_ranked.csv` derives from the realized price move.

**Sourceability is not in that table on purpose.** `route_predicted` and `route_tested` are
separate columns in the ranked CSV and only `route_tested = retrieved` is evidence. Tested
routes are reported in G-2's dossier work; the Tier A count is a count of episodes that pass
the *strength* screen, not of episodes proven primary-sourceable.

## 4. D2 — the finding that changes the question

Registered before the numbers were seen: *is the monthly tier's P target a traded price
before 1973?* `fred.WTISPLC`, 3-month percent changes, by era:

| era | months | **distinct price levels** | share of 3-m changes **exactly 0** | IQR of 3-m change | mean abs 3-m change | share \|Δ\| ≥ 10 % |
|---|---|---|---|---|---|---|
| 1946-01 – 1972-12 | 324 | **16** | **83.5 %** | **0.0 pp** | 1.25 % | 3.4 % |
| 1973-01 – 1986-12 | 168 | 82 | 34.5 % | 6.7 pp | 9.03 % | 25.0 % |
| 1987-01 – 2026-07 | 475 | 463 | 0.0 % | 20.0 pp | 13.37 % | 48.6 % |

Twenty-seven years of monthly observations take **sixteen distinct values**, and five
3-month windows in six close at exactly the price they opened. This is a step function: the
US wellhead posted price under Texas Railroad Commission prorationing, an administered
number, not a market clearing. A P read standing at 1971 would be issuing a predictive
distribution over an outcome that is zero five times in six, and its CRPS would be
measuring how well the engine has learned that an administered price does not move.

**D1 says the same thing from the other side.** The registered monthly WTI Big Moves inside
1946–1986 number **five**: 1947-10, 1973-01, 1973-10, 1979-04, 1985-11. Between **1949 and
1972 there is not one** — a 24-year run, 33 of the 41 years uncovered. So "prioritise
candidates inside a monthly WTI Big Move" is not merely methodologically risky (registration
§6); for the pre-1974 episodes it is **empty**. Suez, the Six-Day War, Libya, Tehran/Tripoli
and the IPC nationalisation are, every one of them, outside every registered monthly Big
Move, because the price they moved was not this one.

Scenario 5 (Amendment 2) prices the consequence. Confining admission to 1973-01 onwards,
where the P target moves: Tier A alone (22 episodes) **cannot** reach 30 scored reads — it
tops out at 19 concentrated and 9 balanced. Tier A **and** B (128 episodes) reaches 30 at
35 admissions concentrated, 46 balanced (seeded random allocation 43–48). A scorable
monthly tier is reachable only by admitting the B tier — single-sourced militarised
disputes — inside a fourteen-year window.

## 5. The other structural finding: the sheet cannot see 1970–73

Three of the five episodes the brief names are **absent from the candidate sheet entirely**.
Probe: any sheet row within ±45 days whose registered actors intersect the episode's states.

| episode | rows found |
|---|---|
| Suez nationalisation and closure, 1956-07-26 | 1 (ICB crisno 152, SUEZ NATN.-WAR, viol 4) |
| Six-Day War and canal closure, 1967-06-05 | 5 (ICB 222, COW WarNum 169, three MIDs) |
| **Libya posted-price confrontation, 1970** | **0** |
| **Tehran and Tripoli agreements, 1971** | **0** |
| **Iraq Petroleum Company nationalisation, 1972** | **0** |

Libya appears in the sheet 35 times — Chad, Egypt, the Gulf of Sirte, the 1986 raid — and
not once for the confrontation that broke the posted-price system. The reason is structural,
not an oversight in the sheet's construction: ICB, COW and Dyadic MID are **militarised-
dispute registries**. A nationalisation, a posted-price ultimatum and a producers' agreement
are not militarised disputes and are coded by none of them. The classes that carry the
commercial history — `opec_decision` (n = 1), `policy_response` (n = 1), `demand_shock`
(n = 0) — therefore **cannot be grown from this sheet at all**, and those are exactly the
classes that own 1970–73.

## 6. What follows (recommendation, Joe's call)

1. **Do not close the gap by lowering `burn_in` or `min_tier_n`.** That is INV-6 / charter
   §2.7 territory and it would not help: 14 events over seven classes cannot support a
   per-class analog retrieval at any burn-in above about 3, and at 3 the "analogs" are the
   same two Iranian events retrieved for everything.
2. **Split the question the tier is being asked.** G (escalation) is scorable before 1973 —
   ICB (1918→), COW (1816→) and MID (1816→) all cover the period and **all 624 sheet rows
   fall inside a covering window** (D3). P is not scorable before 1973 on this series. The
   monthly tier currently scores both against one `min_tier_n`; they should be reported
   separately, because the honest answer is "G yes, P no", not one number.
3. **If the P tier is wanted before 1973, the instrument has to change** — a posted-price
   series with the tanker-rate and product spreads that actually moved in 1956 and 1967
   (Suez-era freight rates moved violently while WTI did not), or the tier is declared
   G-only before 1973 and says so on every surface. Either is a registration and an
   instrument decision, not a research task, and it is Joe's.
4. **A second candidate source is needed for the commercial classes.** The sheet's three
   registries cannot produce a single `opec_decision` or `policy_response` candidate. Without
   one, "balanced" means balanced over three militarised classes, which is a tier about wars
   near oil states rather than a tier about oil.
5. **The cheapest real target is 43 admissions across three classes**, and the archive can
   support it only by reaching into Tier B. That is the number to plan against, and it is
   roughly three times the corpus the tier has today.

## 7. Receipts
- code `src/g_monthly_gap.py` (opens `data/oil.db` read-only; never opens the outcomes file)
- numbers `data/candidates/G1_GAP.json`
- ranking `data/candidates/pre1987_ranked.csv` (461 episodes, `route_tested` blank until a
  retrieval is attempted)
- registration `data/candidates/G1_REGISTRATION.md` + Amendments 1, 2
- validation: the model reproduces `summary.json.tiers.monthly.n_scored_burn_in = 0`
