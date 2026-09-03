# The dyad-date escalation panel, 1987–2014 — size and marginals, before anything is scored
*Built by `src/grid_labels.py` under `data/grid/g/G4_REGISTRATION.md` Amendment 3, which was
committed first. Nothing here is a score, a forecast or a skill. No cell is filtered out.*

## The three limits, first, because they are properties of the construction and not caveats

> **1. It never reaches the present. The panel ends 2014-09-30 because its last sided source does (MID / MIDI / COW intra-state War end 2014-12-31 and ies90.covers needs t+90 <= that). No number computed on this panel describes the world after 2014, and it cannot be the panel a live engine reads.**

> **2. It can never carry VALIDATED. Every cell is retrospective = 1: a COW hostility level, an ICB violence code and a UCDP death estimate are later constructions, not contemporaneous records. WORLD_STATE_CODEBOOK.md Amendment 1 -- a retrospective field alone can never make a read VALIDATED. This is a property of the sources and n does not touch it.**

> **3. It never scores onset. R-ACT admits a dyad only after a recorded clash, so a dyad quiet for five years that goes to war is absent from the grid at every date before its first record. Skill measured here is skill at continuation and de-escalation, never at onset.**

## 1. Size

- **15,740 cells** over **333 month-ends** (1987-01-31 … 2014-09-30), on **156 distinct dyads** of 561 oil-relevant pairs.
- active dyads per grid date (VR-3): 17–124 (mean 47.3); under plain R-ACT the mean is 49.9, so **VR-3 removes 861 dyad-dates** that were selected on a record still running at t.
- L defined on 14,997 (0.9528) · ΔIES defined on 14,344 (0.9113)

## 2. The ΔIES marginal — the number B needs before scoring

| ΔIES | -3 | -2 | -1 | 0 | 1 | 2 |
|---|---|---|---|---|---|---|
| cells | 8 | 266 | 323 | 13,184 | 363 | 200 |
| share | 0.0006 | 0.0185 | 0.0225 | 0.9191 | 0.0253 | 0.0139 |

**14,344 defined, 1,160 non-zero, share zero 0.9191.** L: {"0": 13548, "1": 579, "2": 851, "3": 19}, share zero 0.9034.

## 3. Evidence class — a FIELD on every cell (A3.3), never a filter

| class | all cells | of the non-zero ΔIES cells |
|---|---|---|
| `opposed_side` | 14,232 | 1,059 |
| `icb_co_actor` | 94 | 83 |
| `icb_co_actor_never_opposed` | 18 | 18 |
| `ged_location` | 0 | 0 |
| `undefined` | 1,396 | 0 |

**The strict subset** (`evidence_class == opposed_side`): **14,232 cells** (0.9042 of the panel) on 156 dyads, last date 2014-09-30; ΔIES defined on 14,232, **1,059 non-zero**, share zero 0.9256. ΔIES: {"-3": 6, "-2": 258, "-1": 304, "0": 13173, "1": 295, "2": 196}

This is the subset the scored study runs on. It is a selection on a field that is already there; the diagnostic runs on the full panel. Nothing is rebuilt to move between them.

## 4. The ICB replication, measured over the whole panel (A3.6)

- ICB sets a level on **158 cells**, from **25 distinct crises**.
- dyads per crisis: max **12**, mean 2.24; distribution {"1": 14, "2": 3, "3": 6, "6": 1, "12": 1}
- A crisis with k register actors on the grid sets a level for up to k(k-1)/2 dyads, because ICB records crisis ACTORS and not sides. k=4 -> 6 dyads.

| crisis | n dyads | the dyads |
|---|---|---|
| crisis 393 GULF WAR | **12** | bhr–iraq, bhr–qatar, canada–usa, egypt–israel, gbr–iraq, iraq–saudi_arabia, iraq–syr, iraq–turkey, iraq–usa, israel–syr, kuwait–saudi_arabia, syr–turkey |
| crisis 412 IRAQ DEPLOY./KUWAIT | **6** | iraq–kuwait, iraq–saudi_arabia, iraq–usa, kuwait–saudi_arabia, kuwait–usa, saudi_arabia–usa |
| crisis 448 IRAN NUCLEAR II | **3** | gbr–iran, gbr–usa, iran–usa |
| crisis 440 IRAQ REGIME CHANGE | **3** | gbr–iraq, gbr–usa, iraq–usa |
| crisis 429 UNSCOM II | **3** | gbr–iraq, gbr–usa, iraq–usa |
| crisis 422 UNSCOM I | **3** | gbr–iraq, gbr–usa, iraq–usa |
| crisis 418 OPRN GRAPES OF WRATH | **3** | israel–lebanon, israel–syr, lebanon–syr |
| crisis 406 IRAQ NO-FLY ZONE | **3** | gbr–iraq, gbr–usa, iraq–usa |

See `ICB_DYADIC_REPLICATION.md` for the write-up.

## 5. Vintage and coverage

- VR-1 strict (dataset release ≤ t): **0** (0.0) — as on the probe, and an upper bound.
- VR-2 (session A's registered convention): 14,518 (0.9224).
- every cell `retrospective = 1`.
- covering-source mix over the 333 grid dates: `ged,icb,mid,midi,war,war_intra` ×177 · `ged,icb,mid,midi,war_intra` ×84 · `ged,icb,mid,war,war_intra` ×48 · `icb,mid,war,war_intra` ×24

- undefined, by reason: {"L:undated": 743, "Lpre:undated": 1080}

## 6. The panel's own n is not uniform, and one crisis supplies nearly half of it

Cells per grid date: 17–124 (mean 47.3). By year:

| year | 1987 | 1988 | 1989 | 1990 | 1991 | 1992 | 1993 | 1994 | 1995 | 1996 | 1997 | 1998 | 1999 | 2000 | 2001 | 2002 | 2003 | 2004 | 2005 | 2006 | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cells/date | 35.8 | 35.8 | 32.0 | 32.3 | 100.7 | 121.6 | 120.6 | 121.7 | 122.0 | 53.4 | 30.5 | 29.7 | 32.0 | 29.7 | 28.3 | 27.9 | 32.1 | 33.8 | 33.8 | 32.3 | 31.5 | 21.9 | 18.5 | 17.8 | 25.2 | 37.4 | 40.4 | 43.8 |

**7,038 of the panel's cells (44.7%) fall in 1991-1995**, where the density quadruples. The panel's own n is NOT uniform. The density quadruples 1991-1995 and falls back. That is the ICB co-actor rule acting on the ACTIVE SET, not on the label: a crisis with k register actors makes k(k-1)/2 dyads active for the full five-year lookback.

This is the **activity** limb of the ICB co-actor defect, and it is distinct from the **label** limb of §4: here ICB does not fabricate a level, it fabricates a dyad-date's *existence*. The labels in that block are mostly sided (6,524 `opposed_side`) and mostly zero:

| | cells | non-zero ΔIES | non-zero rate |
|---|---|---|---|
| 1991-1995 | 7,038 | 204 | **0.0311** |
| all other years | 8,702 | 956 | **0.1229** |

It adds rows, not coverage: every dyad active in the window is active elsewhere too. It supplies its share of the panel's rows and a far smaller share of its non-zero cells, so nominal n and informative n diverge here more than anywhere else. It adds **0** dyads that appear nowhere else.

**For whoever scores this panel:** the block is not wrong — the dyad-dates are real and their labels are sided — but it is a low-information half of the sample created by a selection rule, and any estimate that weights cells equally weights it accordingly. It is left in the panel, flagged, and never removed by G (A3.3: evidence basis is a field, not a filter).

## 7. The three checks the panel owes (Amendment 4 — session B's designs, adopted)

### 7.1 Share-zero tripwire — bar 0.95, never moved

| series | n defined | share zero | breach? |
|---|---|---|---|
| `full_panel.dIES` | 14,344 | **0.9191** | no |
| `full_panel.L` | 14,997 | **0.9034** | no |
| `opposed_side.dIES` | 14,232 | **0.9256** | no |
| `opposed_side.L` | 14,232 | **0.9188** | no |

**21 breach(es) of the 0.95 bar, reported and not dropped:**

| scope | field | year | n | share zero |
|---|---|---|---|---|
| full_panel | dIES | **1991** | 823 | **0.9733** |
| full_panel | dIES | **1992** | 1,431 | **0.9755** |
| full_panel | dIES | **1993** | 1,433 | **0.9714** |
| full_panel | dIES | **1995** | 1,433 | **0.9791** |
| full_panel | L | **1989** | 374 | **0.9733** |
| full_panel | L | **1991** | 1,151 | **0.9826** |
| full_panel | L | **1992** | 1,445 | **0.9765** |
| full_panel | L | **1993** | 1,439 | **0.9708** |
| full_panel | L | **1994** | 1,448 | **0.953** |
| full_panel | L | **1995** | 1,449 | **0.9655** |
| opposed_side | dIES | **1991** | 823 | **0.9733** |
| opposed_side | dIES | **1992** | 1,418 | **0.9824** |
| opposed_side | dIES | **1993** | 1,430 | **0.9734** |
| opposed_side | dIES | **1994** | 1,423 | **0.9606** |
| opposed_side | dIES | **1995** | 1,430 | **0.9811** |
| opposed_side | L | **1989** | 369 | **0.981** |
| opposed_side | L | **1991** | 823 | **0.9903** |
| opposed_side | L | **1992** | 1,418 | **0.9838** |
| opposed_side | L | **1993** | 1,430 | **0.9748** |
| opposed_side | L | **1994** | 1,423 | **0.9628** |
| opposed_side | L | **1995** | 1,430 | **0.9755** |

The slice stays in the panel and the bar stays at 0.95 (A4.1). A year that breaches is a fact about that year, published as one.

### 7.2 Admission audit — VR-3 asserted, not trusted

- cells checked: **15,740** · violations: **0** · `asserted`: **True**
- A4.2: every admitted cell's admitting record ends strictly before t. One violation voids the panel (WALK_FORWARD_PROTOCOL Amendment F.1 standing).

### 7.3 Effective n beside nominal

| scope | n nominal | non-zero | DEFF two-way (date × dyad) | n_eff two-way | DEFF block | n_eff block |
|---|---|---|---|---|---|---|
| `full_panel` | 14,344 | 1,160 | 1.4738 | **9732.7** | 1.0583 | **13553.8** |
| `opposed_side` | 14,232 | 1,059 | 1.1785 | **12076.4** | 1.0473 | **13589.2** |

**Limit, with its direction:** DEFF belongs to the score-differential series and this panel
has no scores, so it is computed on the OUTCOME. A score differential carries the forecaster's
own error too, so its correlations should be no larger -- the outcome-based DEFF is an UPPER
bound and the n_eff published here is a FLOOR.

Computed by calling `src/engine/grid/power_arithmetic.py (session B); functions called, never copied`.

**Reconciling with session B's DEFF of ~56–79 on *its* escalation panel** — a reader seeing 1.5 here and 56 there will assume one of us is wrong, so both are printed with their panels:

| | dyads | dyads with any variation | cells | share level 0 | DEFF | informative cells |
|---|---|---|---|---|---|---|
| B, full cross | 966 | 400 | 321,678 | 0.96754 | 56.417 | 10,442 |
| G, active set | 156 | 156 (all, by construction) | 15,740 | 0.90338 | 1.4738 | 1,160 |

They are different objects, not different answers. B's escalation panel is the FULL cross -- every register dyad at every grid date, no active rule -- so it carries dyads that are constant zero for the whole span, and a constant series is perfectly autocorrelated, which is what drives its DEFF up. B's own file records only 400 of 966 dyads with ANY variation. G's panel is the ACTIVE-SET panel (R-ACT + VR-3), which excludes those dyads by construction, so its DEFF is far lower and is the DEFF of the panel G actually built. Neither number transfers to the other panel.

**B's warning applies to G's panel too, at a smaller share: a cell whose outcome both a forecaster and its climatology get right carries no power to DISCRIMINATE between them. G's panel is 90.3 % zeros against B's 96.8 %, so the informative count -- the non-zero cells -- is the number to read, not n_eff.**