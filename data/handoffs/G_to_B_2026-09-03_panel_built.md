# G → B, 2026-09-03 — the panel is built: 15,740 dyad-date cells, 1987–2014, nothing filtered

Registered in `data/grid/g/G4_REGISTRATION.md` Amendment 3 (Joe's ruling), built by
`src/grid_labels.py --build`, published at `data/grid/g/PANEL.{parquet,json,md}`. G writes to
`data/grid/g/**` only; `data/grid/**` is yours and untouched. **Nothing is scored here** — this is
size and marginals before you score anything on it.

## 1. Size

| | |
|---|---|
| span | month-ends **1987-01-31 … 2014-09-30**, 333 grid dates |
| cells | **15,740** |
| distinct dyads | **156** (of 561 oil-relevant pairs) |
| active dyads per grid date (VR-3) | 17–124, **mean 47.3** |
| dyad-dates removed by VR-3 | **861** (selected on a record still running at t) |
| L defined | 14,997 (95.3 %) |
| **ΔIES defined** | **14,344 (91.1 %)** |

## 2. The ΔIES marginal

| ΔIES | −3 | −2 | −1 | **0** | +1 | +2 |
|---|---|---|---|---|---|---|
| cells | 8 | 266 | 323 | **13,184** | 363 | 200 |
| share | 0.0006 | 0.0185 | 0.0225 | **0.9191** | 0.0253 | 0.0139 |

**14,344 defined, 1,160 non-zero, 91.9 % zero.** L: `{0: 13548, 1: 579, 2: 851, 3: 19}`, 90.3 % zero.

Two notes you will want before modelling. **ΔIES = +3 never occurs and −3 occurs 8 times**: level 3
is reached on only 19 cells in 27 years, because Amendment 4's continuation rule refuses to date a
war that was already running, so level 3 marks *transitions into* war and not war itself. And the
distribution is **not symmetric** — 589 negative against 563 positive — but the negative mass sits
further out (266 at −2 against 200 at +2). De-escalation in this panel is larger and rarer than
escalation.

## 3. Evidence basis is a FIELD on every cell (A3.3), not a filter

| class | all cells | of the 1,160 non-zero ΔIES |
|---|---|---|
| `opposed_side` | **14,232** | **1,059** |
| `icb_co_actor` | 94 | 83 |
| `icb_co_actor_never_opposed` | 18 | 18 |
| `undefined` | 1,396 | — |

**The strict subset — `evidence_class == 'opposed_side'` — is 14,232 cells (90.4 % of the panel),
ΔIES defined on all of them, 1,059 non-zero, 92.6 % zero, on 156 dyads, running to 2014-09-30.**

This is the headline improvement from Joe's 1987–2014 ruling. On the probe's 2018 and 2024 years,
**zero** non-zero cells rested on sided evidence. On this span **91 %** of them do, because MID,
MIDI and COW War cover the whole panel. The strict subset is a selection you apply at scoring time
on a column that is already in the parquet — no rebuild, and the diagnostic runs on the full panel.

Every cell also carries `L_evidence` and `Lpre_evidence` separately, so you can require sided
evidence at one end and not the other if you have reason to.

## 4. The thing that most affects your effective-n arithmetic

**7,038 of the 15,740 cells — 44.7 % — fall in 1991–1995**, where the panel's density quadruples
(≈32 cells/date before, ≈100–122 in the window, ≈18–43 after). The cause is measured, not guessed:
at 1993-06-30, **108 of 120 active dyads** qualify on a record that began in the Gulf War window and
**89 of 120 qualify on ICB alone**. ICB's co-actor pairing does not only fabricate *levels* for ally
pairs — it fabricates **activity**: a crisis with k register actors makes up to k(k−1)/2 dyads
active for the whole five-year lookback. `crisis 393 GULF WAR` sets a level for 12 dyads including
`canada–usa`, `bhr–qatar` and `egypt–israel`.

The block is not wrong — 6,524 of its cells carry `opposed_side` evidence and real (mostly zero)
labels. It is **the panel's least informative half**:

| | cells | non-zero ΔIES | non-zero rate |
|---|---|---|---|
| 1991–1995 | 7,038 | 204 | **0.031** |
| all other years | 8,702 | 956 | **0.123** |

**45 % of the rows, 18 % of the signal, and 0 dyads that appear nowhere else.** Left in the panel
and flagged, never removed by G (A3.3). If your Part II weights cells equally, it weights this
accordingly — and a DEFF from two-way clustering on dyad and date will not see it, because these
are genuinely distinct dyads on genuinely distinct dates. The dependence is definitional.

## 5. Vintage, unchanged from the probe

VR-1 strict (dataset release ≤ t): **0 of 15,740**, as before, and an upper bound. VR-2 (session A's
registered convention, `WORLD_STATE_CODEBOOK` Amendment 1): 14,518 (92.2 %). **Every cell is
`retrospective = 1`.** Covering-source mix over the 333 grid dates: all five sided sources for 249
of them, `mid` without `midi` for the first 72 (MIDI starts 1993), and `war` drops out after
2007-10-02 for the last 84.

## 6. The three limits, registered before the panel existed

They are in `PANEL.json.limits` and at the head of `PANEL.md`, and they are properties of the
construction rather than caveats on a result:

1. **Never reaches the present** — it ends 2014-09-30 because its last sided source does. No number
   on it describes the world after 2014, and it cannot be the panel a live engine reads.
2. **Never carries VALIDATED** — every cell is retrospective; codebook Amendment 1 already rules
   that a retrospective field alone cannot. `n` does not touch this.
3. **Never scores onset** — R-ACT admits a dyad only after a recorded clash, so skill measured here
   is skill at continuation and de-escalation.

## 7. Two requests, and one thing G will not do

- **Cluster on the setter record, not the dyad-date.** Every cell carries `L_records` (the ICB
  `crisno` / MID `disno` / MIDI `incidnum` / COW `WarNum` that set its level) and `L_rules`. Your
  §2.5 two-way cluster on dyad and date cannot see that 12 dyads are one Gulf War row.
- **Read `data/grid/g/ICB_DYADIC_REPLICATION.md`** before Part III. ICB v16 ships a dyad-level file,
  it is already in the tree at `data/state/raw/icb/icb_dyads_v16.csv`, and
  `src/state/outcomes.py:load_icb` reads it and then flattens the pairs into an actor set on the
  next line. Fixing that removes the label limb and the activity limb at no data cost. It is
  **session A's file**; G reported it and did not patch it.
- **G will not filter the panel.** Joe ruled evidence basis is a field, not a filter, and the strict
  subset is yours to select. If you want a pre-filtered file, say so and G will write it as a
  derived view rather than by rebuilding.
