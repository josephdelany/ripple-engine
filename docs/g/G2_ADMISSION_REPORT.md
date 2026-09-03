# G-2 — the pre-1974 candidates against the SPINE_REGISTRATION bar, and what admitting them buys
*2026-09-03, Session G. Six dossiers, six verdicts, and the arithmetic of what each is worth.
Nothing here enters `events`. Admission is Joe's line (`SPINE_REGISTRATION.md` §3); this file
is the sheet he needs to sign it. Sources: `data/dossiers/*.md`, `docs/g/ROUTE_TESTS.md`,
`data/candidates/G1_GAP.json`.*

## 0. The one-paragraph answer

**All six pre-1974 candidates now reach the bar.** Two reached it in the first pass (Suez
1956, the Six-Day War 1967); four were `partial — fails (a)` and are now complete, because
the first pass hunted a second *primary* when clause (a) only ever needed a second
*independent domain of any role*, and two such domains — `ora.ox.ac.uk` and `merip.org` —
were already in Session E's tested set and had not been tried. **But admitting all six buys
zero scored monthly-tier reads**, and four of the six cannot be scored by this engine at all,
on either branch, for reasons that have nothing to do with how well they are sourced. Both
facts are below, with the numbers.

## 1. The verdicts, clause by clause

`SPINE_REGISTRATION.md` §1: (a) two independent domains, ≥1 primary · (b) 120–250-word
narrative, every claim marked · (c) `knowable_at` with its reason · (d) entities from the
register with roles · (e) a codebook class with the clause quoted · (f) an explicit
what-was-NOT-known.

| # | event_id | date | class | (a) | (b) | (c) | (d) | (e) | (f) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `suez_nationalisation_1956` | 1956-07-26 | chokepoint_disruption | ✅ 3 domains, 2 primary | ✅ 203 w | ✅ | ⚠ 2 register gaps reported | ✅ | ✅ | **complete** |
| 2 | `six_day_war_1967` | 1967-06-05 | conflict_escalation | ✅ 2 domains, both primary | ✅ 229 w | ✅ | ⚠ 3 register gaps reported | ✅ | ✅ | **complete** |
| 3 | `libya_posted_price_confrontation_1970` | 1970-09-23 | opec_decision | ✅ 2 domains (1 primary) | ✅ 250 w | ⚠ a **floor**, see §3 | ⚠ oil-company gap | ⚠ class by elimination | ✅ | **complete** |
| 4 | `tehran_agreement_1971` | 1971-02-14 | opec_decision | ✅ 2 domains (1 primary) | ✅ 236 w | ✅ | ⚠ 4 of 6 signatories inferred | ⚠ class by elimination | ✅ | **complete** |
| 5 | `tripoli_agreement_1971` | 1971-04-02 | opec_decision | ✅ 2 domains (1 primary) | ✅ 244 w | ✅ | ⚠ oil-company gap | ⚠ class by elimination | ✅ | **complete, narrowly** |
| 6 | `iraq_ipc_nationalisation_1972` | 1972-06-01 | opec_decision | ✅ 3 domains (1 primary) | ✅ 238 w | ✅ | ⚠ 3 register gaps | ⚠ class by elimination | ✅ | **complete** |

⚠ marks a clause that is **met** with a limitation stated in the dossier, not a clause that fails.

### Corroboration strength — read this before treating the six as equivalent

Clause (a) is binary and all six pass it. What the second source actually *says* is not binary,
and the six are not equal:

| event | second/third domain | what it corroborates | what it does NOT |
|---|---|---|---|
| Suez 1956 | `peacekeeping.un.org` (primary), `nber.org` | the nationalisation, the UN operation, 1.5 mb/d canal transit, −1.7 mb/d Nov 1956 | — |
| Six-Day War 1967 | `presidency.ucsb.edu` (primary) | the war, the Straits of Tiran as stated cause, the maritime interest | barrels; the delivery suspension rests on FRUS editorial apparatus |
| Libya 1970 | `ora.ox.ac.uk` (Fattouh, WPM 40, Jan 2011) | the September 1970 Occidental settlement, the mechanism, the other companies following | the 1.5 mb/d — S1's **conditional** estimate, alone |
| Tehran 1971 | `ora.ox.ac.uk` | the Tehran negotiation, its outcome in kind, its origin in Libya's terms | **every figure**; 30¢/50¢ and $1.4bn/$12bn rest on S1 alone and are 1971 projections |
| **Tripoli 1971** | `merip.org` (Renner, *MERIP Reports* 120, Jan 1984) | **one sentence**: that "the Tehran and Tripoli agreements of 1970-1971" happened | the date, the 63¢/bbl, the $3.446 vs $2.55 tax reference prices, the offers to Iraq and Saudi Arabia |
| Iraq/IPC 1972 | `ora.ox.ac.uk` + `merip.org` | the fact and the **year** | the **day** (1 June), which rests on S1 alone; and barrels |

**Tripoli 1971 is the one to look at hardest.** It has the best primary of the four — a State
Department cable timed the day of the agreement, carrying exact posted prices — and the
thinnest corroboration: a single retrospective sentence naming the agreement. It passes §1(a)
by the letter. A reader wanting two substantive accounts of it does not have them.

## 2. What admitting all six buys: **zero scored reads**

The monthly tier's scoring predicate is registered in `G1_REGISTRATION.md` §1 and re-derived
from `walk.py:276` and `read.py:201`: **burn-in is per class**, a class needs ≥ 8 prior closed
members before any of its reads is scored, and the tier needs ≥ 30 scored reads to permit
validation. Applying the registered bound `S_c ≤ max(0, n_c − 8)`:

| class | now | after the six | short of burn-in | scored reads added |
|---|---|---|---|---|
| conflict_escalation | 5 | **6** (+1, Six-Day War) | 2 | 0 |
| infrastructure_attack | 4 | 4 | 4 | 0 |
| chokepoint_disruption | 1 | **2** (+1, Suez) | 6 | 0 |
| sanctions | 2 | 2 | 6 | 0 |
| policy_response | 1 | 1 | 7 | 0 |
| opec_decision | 1 | **5** (+4) | 3 | 0 |
| demand_shock | 0 | 0 | 8 | 0 |
| **tier** | **14** | **20** | — | **0 → 0** |

G-1 computed the minimum at **33** admissions (degenerate, one class) and **43** for a tier
§6's per-class blocks can be run on. Six is not close to either, and no subset of six could be:
every monthly class is below burn-in, so the first 8 − n_c admissions to any class score
nothing by construction. **Admitting these six is worth doing for the record, not for the
score, and it should be said in those words rather than presented as progress toward 30.**

What it *is* worth: the corpus's earliest event moves from 1973-10-06 to **1956-07-26**,
extending the monthly tier by seventeen years, and `opec_decision` goes from 1 member to 5 —
**three short of burn-in**, which is the smallest remaining distance of any class in the tier.

## 3. What cannot be done, by reason

These are stated as reasons rather than as failures, because none of them is closed by more
searching.

**R1 — Four of the six cannot be scored by this engine on either branch.**
`opec_decision` is not in `GEO_TYPES` (`similarity.py:46`: conflict_escalation,
infrastructure_attack, chokepoint_disruption, sanctions), so Libya 1970, Tehran 1971, Tripoli
1971 and IPC 1972 get **no G score** whatever their IES-90 coverage. Their P score is the
monthly WTI target, and G-1 diagnostic D2 measured what that target does before 1973: WTISPLC
takes **16 distinct values in the 324 months to 1972** and **83.5 % of its 3-month changes are
exactly zero** (IQR 0.0). So the four records Joe named as the most important pre-1974 oil
events are, under the rules as they stand, **unscoreable on both branches**. Suez 1956
(chokepoint_disruption) and the Six-Day War 1967 (conflict_escalation) are geopolitical
classes and do carry a G target. This is the sharpest thing G-2 found and it is not a sourcing
problem.

**R2 — The closed codebook has no class for a concession or ownership change.**
A posted-price confrontation, a participation demand and a nationalisation are all pushed into
`opec_decision` by elimination, and that class's own clause reads "production decision". Four
of the six records sit there for want of anywhere else. Recorded in every affected dossier as
a v3 codebook question for Joe and Session E; **not decided by G**, because changing a closed
codebook to fit records one has just written is the wrong order. It bears on R1: a
concession/ownership class placed in `GEO_TYPES` would give these four a scoreable target.

**R3 — The entity register cannot express the parties.**
There is **no entity type for an oil company** — Occidental, the Oasis partners, Shell, BP and
IPC are the counterparties in the retrieved primaries and cannot be coded — and no
`country.france`, `country.syria`, `country.jordan`, `country.algeria`, Qatar or the UAE, all
named in retrieved primaries. Reported to Session A (`docs/g/ROUTE_TESTS.md`), never invented.
Consequence for admission: the `actor`/`target` coding of records 3–6 will be one-sided (the
producer state, no counterparty) until the register grows.

**R4 — `severity` is `unknown` for all four commercial records, and stays unknown.**
No source retrieved by either pass gives barrels for Libya 1970, Tehran 1971, Tripoli 1971 or
IPC 1972. The figures that exist are *prices* (63¢/bbl, $3.446 vs $2.55) or *conditional
estimates* (the 1.5 mb/d Libya could shut in, written in the conditional and never realised in
that form). Coding severity from either would store an inference in a measured column. Under
the sourced-or-unknown rule the correct value is `unknown`, and it is a measurement.

**R5 — The pre-1990 US government record is public, free, and unreadable by this toolchain.**
Four `govinfo.gov` items were requested this pass — the 1974 Senate committee print on the
international petroleum cartel, the bound *Congressional Record* for September 1970, and two
committee prints — and **all four exceeded the fetch client's 10 MB limit**; the HTML
renderings do not exist for that era. This is a tool limit, not an access limit, and it is the
single change most likely to improve pre-1974 sourcing: the Senate's own 1974 hearings on the
Libya/Tehran/Tripoli negotiations are the obvious second primary for records 3–5 and we cannot
open them.

**R6 — The blind candidate sheet cannot grow the classes that own 1970–73.**
G-1 established this and it is unchanged: ICB, COW and MID are militarised-dispute registries,
so Libya 1970, Tehran/Tripoli 1971 and IPC 1972 are **absent from
`pre1987_candidates.csv` entirely**. The sheet's 39 Tier-A pre-1974 episodes are Cold War
crises (Korea, the Taiwan Strait, Cuba, Prague) that pass the screen because a superpower
counts as a `producer`; they are not oil events. `opec_decision`, `policy_response` and
`demand_shock` cannot be grown from this sheet at all, and they are three of the seven classes.

## 4. The admission sheet

If Joe admits, these are the values each dossier proposes. Every `unknown` is a measurement
under R4, not a blank to be filled.

| event_id | event_date | precision | type | source_url | severity | surprise | hostility |
|---|---|---|---|---|---|---|---|
| `suez_nationalisation_1956` | 1956-07-26 | day | chokepoint_disruption | history.state.gov/…/frus1955-57v16/d2 | unknown | unknown | — |
| `six_day_war_1967` | 1967-06-05 | day | conflict_escalation | history.state.gov/…/frus1964-68v19/d160 | unknown | unknown | hostile |
| `libya_posted_price_confrontation_1970` | 1970-09-23 | day | opec_decision | history.state.gov/…/frus1969-76v36/d55 | unknown | unknown | n/a |
| `tehran_agreement_1971` | 1971-02-14 | day | opec_decision | history.state.gov/…/frus1969-76v36/d86 | unknown | unknown | n/a |
| `tripoli_agreement_1971` | 1971-04-02 | day | opec_decision | history.state.gov/…/frus1969-76v36/d88 | unknown | unknown | n/a |
| `iraq_ipc_nationalisation_1972` | 1972-06-01 | day | opec_decision | history.state.gov/…/frus1969-76v36/d124 | unknown | unknown | n/a |

**One date carries a warning.** `libya_posted_price_confrontation_1970`'s 1970-09-23 is a
**floor, not the onset**: the telegram that establishes it describes a confrontation already
under way (the Occidental settlement in the past tense, the Shell export ban in force). The
true first-knowability is earlier and no retrieved source dates it. If admitted, that record's
`knowable_at` should be revisited when an earlier 1970 document is found. Admitting a floor as
an onset would put the event *later* than it happened, which for a filtration is the
conservative direction — but it is still wrong, and it is flagged rather than smoothed.

## 5. G's recommendation, and the disagreement it should provoke

Admit **1, 2, 4, 6** (Suez, the Six-Day War, Tehran, IPC) without reservation. Admit **3**
(Libya 1970) with the date recorded as a floor. On **5** (Tripoli 1971), G's own view is that
it should be admitted — the primary is the strongest of the four and is dated the day of the
event — but a reader who holds that clause (a) is about *corroboration* rather than about
counting domains would decline it, and that reader would not be wrong about the substance.
The registration counts domains; G reports the substance beside the count and does not resolve
the tension by adjusting either.

**The recommendation G would rather Joe act on is R1 and R2.** Admitting six records that
cannot be scored changes no number in any run. Deciding whether a concession/ownership class
exists — and whether it is a geopolitical class with a G target — decides whether the entire
1970–73 commercial history is data or decoration. That is a codebook decision, it is Joe's and
Session E's, and it is worth more than any further dossier G could write.
