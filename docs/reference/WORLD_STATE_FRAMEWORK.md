# WORLD-STATE FRAMEWORK — the spine's memory of *how the world stood* at every shock
*2026-09-02. Registered before collection. This is the input the predictive engine
has been missing: a wide, sourced, vintage-stamped record of the state of the
world — physical, actors, dyads, system, market, narrative — at every date since
1946, so that "rhymes" are computed on the state and not on a label. The walk
(WALK_FORWARD_PROTOCOL.md) runs on top of this; without it, the walk has nothing
to condition on.*

## 1. The idea in one paragraph
History rhymes because the *state* recurs in pieces while the *event* never
repeats. An attack on a terminal in 1985 and one in 2019 are the same class and
different worlds: spare capacity 10 mb/d vs 2; a war economy vs peace; a
superpower escorting tankers vs one exporting crude; a coalition vs a truce.
The engine must hold, for every shock, the full state around it — not a
description of the event, but the world it landed in — and compute similarity
across that state with weights it learns from being scored. Then the read for
9/11, made standing on 2001-09-11 with only the 1946–2001 record, is a
comparison of *worlds*, and the outcome teaches the engine which parts of the
world mattered. That is the predictive engine. It is built from the state up.

## 2. Two layers of state
**Layer S (the panel).** Continuous variables for every month (and year where
only annual exists) from 1946 to today, for the world, the key regions, and
every actor the corpus names. Any date has a state; the engine can stand
anywhere, not only at events. Built by loaders from public panel datasets.
**Layer D (the dossier).** Per-event fields no panel carries: posture, stated
intent, capacity to respond, what the target exported that mattered, the prior
clash in the dyad, what the market was saying. Researched per event from dated
sources by the caged extractor and gated by the analyst; two-source rule;
"unknown" allowed and counted.
Every field in both layers carries: value, unit, **source**, **source date
(vintage)**, coding rule id, confidence. The engine at date t sees a field
only if its vintage ≤ t.

## 3. The schema (blocks → fields → source)
Resolution: m = monthly, a = annual, e = per event. Coverage is the dataset's.

### PHYSICAL (supply, capacity, flows)
| field | res | source | coverage |
|---|---|---|---|
| crude production by country; OPEC/non-OPEC | m | EIA International (monthly), EI Statistical Review (annual) | 1973→ (m), 1965→ (a) |
| OPEC spare capacity, total and Saudi | a→m | EIA *Global Surplus Crude Oil Production Capacity 1970–2021* + STEO 2003→ | 1970→ |
| consumption by country/region; net import dependence | a | EI Statistical Review | 1965→ |
| refinery capacity/throughput by region | a | EI Statistical Review | 1965→ |
| US crude + product inventories; days of cover | w→m | EIA weekly (1982→), monthly PSM | 1982→ |
| US SPR stock and releases | m | EIA | 1977→ |
| proven reserves by country | a | EI | 1980→ |
| chokepoint transit volumes | d | IMF PortWatch (2019→); EIA chokepoint factsheets (a, earlier) | 2019→ / episodic |
| tanker freight | d | Baltic Dirty/Clean Tanker Index | 1998→ |

### MARKET (what the price already says)
| field | res | source | coverage |
|---|---|---|---|
| WTI monthly spliced | m | FRED WTISPLC (loaded) | 1946→ |
| Brent, WTI daily; products; cracks | d | FRED/EIA (loaded) | 1986/87→ |
| **curve structure**: NYMEX contracts 1–4 → M1–M4 spread (backwardation/contango) | d | EIA NYMEX futures 1–4 | 1983→ |
| realized vol; implied vol (VXO/VIX, OVX) | d | CBOE via FRED (loaded) | 1986/1990/2007→ |
| positioning (COT managed money) | w | CFTC (loaded) | 1986/2006→ |
| macro: rates, curve, dollar, CPI, IP, recession dates | m | FRED/ALFRED vintages (partly loaded) | 1946→ |
| product PPI (fertilizer, plastics) | m | FRED | varies |

### ACTORS (who they were that year)
| field | res | source | coverage |
|---|---|---|---|
| material capability (CINC: military spend/personnel, energy, iron/steel, population) | a | COW National Material Capabilities v7 | 1816–2022 |
| military expenditure, arms imports | a | SIPRI MILEX (1949→), SIPRI Arms Transfers (1950→) | 1949→ |
| regime type (polity score, durability) | a | Polity5 (to 2018); V-Dem (to present) | 1800→ |
| leader tenure / recent change | e | Archigos (to 2015) + dossier | 1875→ |
| oil-export dependence (oil rents % GDP; share of exports) | a | World Bank WDI; EI | 1970→ |
| fiscal breakeven price | a | IMF (loaded, recent); dossier earlier | 2000s→ |

### DYADS (the pair that clashed)
| field | res | source | coverage |
|---|---|---|---|
| alliance ties and obligations | a | ATOP 5.1 | 1815–2018 |
| militarized disputes: count, hostility level, last date | a | COW MID 5.0 (to 2014) + UCDP (to present) | 1816→ |
| crises: trigger, gravity, violence, escalation, outcome | e | **ICB v16** (512 crises, 1918–2021) | 1918→ |
| sanctions in force between them; type; objective | a | GSDB R5 (1950–2025) | 1950→ |
| trade dependence, bilateral | a | IMF DOTS (1948→), UN Comtrade (1962→) | 1948→ |
| UN voting alignment (ideal-point distance) | a | Voeten UNGA ideal points | 1946→ |
| diplomatic representation | a | Diplometrics / COW Diplomatic Exchange | to 2005 / dossier |

### SYSTEM (the world around the pair)
| field | res | source | coverage |
|---|---|---|---|
| active interstate/intrastate wars, battle deaths | a | UCDP/PRIO (1946→), COW Wars | 1946→ |
| great-power posture in the Gulf (carrier presence, escort operations, bases) | e | dossier (sourced) | — |
| geopolitical risk, threats vs acts | m | Caldara–Iacoviello GPR (1985→ daily) and **GPRH (1900→ monthly)** | 1900→ |
| OPEC decisions and quota changes | e | OPEC conference record; Känzig announcement dataset | 1960→ |
| UN Security Council action on the crisis | e | UN records via dossier | — |

### NARRATIVE (what was being said then)
| field | res | source | coverage |
|---|---|---|---|
| coverage volume and tone on the actors/assets | m | GPRH newspaper counts; NYT Article Search (1851→, free key); GDELT (1979→) | 1900→ |
| contemporaneous claims (the narrative at the time) | e | source article of the event + NYT archive; claim-extracted point-in-time | per event |

## 4. Coding protocol (binding)
1. Panel fields are loaded by code from the named dataset with the dataset's
   own release/vintage date; no hand entry.
2. Dossier fields are proposed by the caged extractor from dated sources,
   quoted verbatim, and gated by the analyst; two independent sources for any
   field that conditions a read; else "unknown".
3. Never from outcomes: a field may not be coded using anything dated after
   the event (the vintage rule is enforced in code, not by promise).
4. A 60-event stratified audit of dossier fields against sources (κ ≥ 0.6)
   before any conditioner built on them is called more than SUGGESTIVE.
5. Every field has a one-line coding rule in `WORLD_STATE_CODEBOOK.md`,
   registered before its loader runs.

## 5. How the engine uses it ("rhymes, not repeats")
- Similarity between a live situation and each historical one is a weighted
  distance over the state vector, block by block (physical, market, actors,
  dyad, system, narrative), with continuous fields standardized *within the
  information set at t* (no future scaling) and categorical fields matched.
- Weights are not hand-set: they come from the registered menu and the Hedge
  update in the walk protocol §5, so the engine learns which blocks carried
  information — and publishes that as a result ("spare capacity mattered;
  regime type did not").
- The differencing table is the state vector side by side: every field where
  then ≠ now, tagged measured (the walk has scored it) or unmeasured.
- "No adequate precedent" fires on state distance, not on class, which is what
  makes an unprecedented situation legible as *partially* precedented.

## 6. Research and build pipeline (order)
**A. Panel loaders (code, keyless, days).** A1 FRED/ALFRED macro vintages;
A2 EIA international monthly production + spare-capacity series + NYMEX
contracts 1–4 (curve) + SPR + inventories; A3 EI Statistical Review annual
panel; A4 COW NMC v7 + MID 5 + COW wars; A5 ATOP 5.1; A6 ICB v16 (crisis and
actor files); A7 Polity5 + V-Dem; A8 SIPRI MILEX + arms transfers; A9 GSDB
(request by email; dyadic file); A10 UCDP/PRIO; A11 GPRH monthly; A12 Voeten
ideal points; A13 IMF DOTS. Each loader writes to `state_panel`
(entity, field, date, value, source, vintage) and is tested on a known value.
**B. State-at-event join (code, hours).** For every corpus event, the panel
value of every field as of the event date (last vintage ≤ t) → `situation_state`.
**C. Dossiers (research, weeks; prioritized).** Order: every event attributed
to a Big Move (43 daily + 18 monthly episodes), then every event in the
escalation classes, then the rest. The caged extractor proposes from the
event's sources plus NYT archive queries for the week of the event; Joe gates.
**D. The 9/11 acceptance demo.** Stand at 2001-09-11 with vintages ≤ that day:
show the state vector (spare capacity, inventories, curve, GPR, US posture,
Saudi/Iraq/Iran fields, alliances), the nearest states by block, the read, and
then the realized outcome and the score. If the demo cannot be produced with
every field either sourced or "unknown", the framework is not done.
**E. Then the walk** (WALK_FORWARD_PROTOCOL.md) runs on the state.

## 7. Acceptance
S1 `state_panel` populated for ≥ 12 of the 13 loaders with vintages;
S2 every corpus event has a `situation_state` row with ≥ 25 non-unknown fields
for 1987+ and ≥ 12 for 1946–86, coverage reported per block;
S3 vintage rule unit-tested (a field with vintage > t is invisible at t);
S4 dossier audit κ ≥ 0.6 on 60 events;
S5 the 9/11 demo renders end to end from sealed inputs;
S6 the codebook lists every field with source, rule, coverage, and licence.

## 8. Licences and access, stated
All named panels are free for research use; GSDB is by email request; NYT
Article Search needs a free key (never committed); EI Statistical Review is a
public good; COW/ATOP/ICB/Polity/SIPRI/UCDP are open academic datasets with
citation requirements — cited in `WORLD_STATE_CODEBOOK.md`.

---

## Amendment A (2026-09-02, registered before the code) — `knowable_at` on every situation field
WALK_FORWARD_PROTOCOL.md §1 states the limitation: the situation-record fields (`events.sr_*`, coded by
`situation_record.py` under SITUATION_CODEBOOK_V2.md) are taken as coded, not vintage-filtered, so a read
at date t may use a field whose evidence did not exist at t. This amendment closes it for the join.
1. **Every situation field carries `knowable_at`**, the date its evidence became knowable, taken in this
   order from the record's own per-field `sources` map: (a) the source's publication date when the cited
   URL carries one in its path (`/YYYY/MM/DD/` or `/YYYY-MM-DD` — read from the URL, never fetched or
   guessed); (b) for fields sourced `corpus:observed` (the retired outcome branches) the day the window
   closed, `event_date + 30 / + 90`; (c) for fields sourced from the corpus itself (`corpus:dyad`,
   `corpus:density`, `corpus:entities`) or from an undated URL, the **coding date** (`events.added_at`,
   the record's coding run); (d) `unknown` when the source is null. The field's `sources` entry is kept
   beside it as the receipt.
2. **The join drops a situation field with `knowable_at > t`** (t = the event date for the corpus
   join; the read date for a live read) and one with `knowable_at = unknown`; both are counted per
   event in `situation_state`'s coverage report as `sr_dropped_after_t` and `sr_unknown`, published as
   computed. Nothing in `events` changes; the columns stay; only the vintage-aware join filters.
3. **Consequence, stated now:** because every current record was coded on 2026-09-02 from sources that
   are mostly undated URLs or the corpus itself, rule (c) dates almost every situation field to the coding
   run, so almost every situation field vanishes at t for every corpus event. That is the honest reading
   of §1, not a bug. The remedy is a per-field contemporaneous source with its own date (rule (a)),
   which is Joe's coding work on the borderline queue, not a code change. Session B receives the count
   of vanishing fields so the next walk can say what the engine saw at t.
4. The walk's similarity fields are session B's (`src/engine`); this amendment binds `situation_state`
   (session A) and what it publishes; the engine may switch to reading situation fields from
   `situation_state` at its own registration.
