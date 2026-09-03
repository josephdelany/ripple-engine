# G-4 probe — the dyad-date escalation panel, three years, before anything is built
*Computed by `src/grid_labels.py` under `data/grid/G4_REGISTRATION.md`, which was committed first.*
*Generated 2026-09-03T03:44:46+00:00. The full panel is NOT built: registration §5 gates it on this file.*

## 0. The answer, in three numbers

- **Active dyad-dates per grid date (1998, R-ACT):** 29–31 (mean 29.8) out of 561 oil-relevant dyads.
- **Degeneracy (§5.1):** not degenerate — ΔIES zero share 0.9017, L zero share 0.8208, threshold 0.95.
- **Cells surviving the vintage stamp (1998):** VR-1 strict **0** (0.0) · VR-2 registered convention **310** (0.8683) · VR-3 selection **356** (0.9972). Every cell is `retrospective = 1`.

## 1. Active set, by probe year

| year | grid dates | oil dyads | active/date (min–max, mean) | VR-3 active/date | cells |
|---|---|---|---|---|---|
| 1998 | 12 | 561 | 29–31 (29.8) | 29–31 | 357 |
| 2018 | 12 | 561 | 25–30 (27.9) | 22–26 | 335 |
| 2024 | 12 | 561 | 10–12 (11.1) | 10–12 | 133 |

**Lookback sensitivity** (§2.1, pre-declared; five years stays primary) — mean active dyads per grid date:

| year | 1 y | 2 y | 5 y (primary) | 10 y | R-ACT-0 (no recency) |
|---|---|---|---|---|---|
| 1998 | 12.2 | 17.6 | **29.8** | 127.3 | 561 |
| 2018 | 10.2 | 12.9 | **27.9** | 50.0 | 561 |
| 2024 | 0.0 | 0.0 | **11.1** | 25.7 | 561 |

## 2. The marginal distributions

### 1998

- cells: **357** · L defined on 318 (0.8908) · L⁻ defined on 313 (0.8768) · ΔIES defined on 295 (0.8263)
- **L**: {"0": 261, "1": 24, "2": 33} — share zero **0.8208**
- **L⁻**: {"0": 256, "1": 25, "2": 32} — share zero 0.8179
- **ΔIES**: {"-2": 7, "-1": 5, "0": 266, "1": 16, "2": 1} — share zero **0.9017**
- undefined, by reason: {"L:undated": 39, "Lpre:undated": 44}

### 2018

- cells: **335** · L defined on 296 (0.8836) · L⁻ defined on 296 (0.8836) · ΔIES defined on 293 (0.8746)
- **L**: {"0": 272, "1": 2, "2": 4, "3": 18} — share zero **0.9189**
- **L⁻**: {"0": 274, "1": 4, "3": 18} — share zero 0.9257
- **ΔIES**: {"-3": 18, "-1": 1, "0": 250, "1": 2, "2": 4, "3": 18} — share zero **0.8532**
- undefined, by reason: {"L:undated": 39, "Lpre:undated": 39}

### 2024

- cells: **133** · L defined on 55 (0.4135) · L⁻ defined on 59 (0.4436) · ΔIES defined on 46 (0.3459)
- **L**: {"0": 40, "2": 12, "3": 3} — share zero **0.7273**
- **L⁻**: {"0": 37, "2": 18, "3": 4} — share zero 0.6271
- **ΔIES**: {"-2": 9, "0": 25, "2": 12} — share zero **0.5435**
- undefined, by reason: {"L:undated": 78, "Lpre:undated": 74}

## 3. Covering-source mix per grid date (§3, the regime table)

| year | mix (grid dates) |
|---|---|
| 1998 | `ged,icb,mid,midi,war,war_intra` ×12 |
| 2018 | `ged,icb` ×12 |
| 2024 | `ged` ×12 |

## 4. The vintage stamp

| year | cells | VR-1 strict (release ≤ t) | VR-2 event knowability | VR-3 selection knowable |
|---|---|---|---|---|
| 1998 | 357 | 0 (0.0) | 310 (0.8683) | 356 (0.9972) |
| 2018 | 335 | 0 (0.0) | 296 (0.8836) | 296 (0.8836) |
| 2024 | 133 | 0 (0.0) | 59 (0.4436) | 133 (1.0) |

**Release dates, read from the tree's `.meta.json` sidecars (§4.1), never from memory:**

| source | release | how | lower bound used by VR-1 |
|---|---|---|---|
| `war` | 2022-07-12 | HTTP Last-Modified of cow_war/Inter-StateWarData_v4.0.csv | 2022-07-12 |
| `war_intra` | 2022-07-12 | HTTP Last-Modified of cow_war/Intra-StateWarData_v4.1.csv | 2022-07-12 |
| `midi` | 2022-07-11 | HTTP Last-Modified of cow_mid/MID-5-Data-and-Supporting-Materials.zip | 2022-07-11 |
| `mid` | 2025-04-06 | HTTP Last-Modified of cow_mid/dyadic_mid_4.03_update.zip | 2025-04-06 |
| `icb` | **unknown** | icb/icb_dyads_v16.csv: host serves no Last-Modified | 2022-01-01 (bound, not a release date) |
| `ged` | **unknown** | no sidecar in the tree | 2026-01-01 (bound, not a release date) |

VR-1 uses a **lower bound** on release where the host serves none, which makes its count an **upper bound** on survival: the most favourable number consistent with the evidence.

**Every cell carries `retrospective = 1`** (§4.2). A COW hostility level, an ICB violence code and a UCDP death estimate are later constructions, not contemporaneous records. `WORLD_STATE_CODEBOOK.md` Amendment 1: *a retrospective field alone can never make a read VALIDATED.* That is a property of the sources, not of `n`, and density does not change it.

## 5. What the non-zero cells actually rest on (Amendment 2 — a diagnostic; gates nothing)

| year | non-zero ΔIES cells | distinct dyads | evidence basis |
|---|---|---|---|
| 1998 | 29 | 10 | **23** opposed-side evidence (MID / MIDI / COW War) · **6** ICB co-actor only (may be allies) |
| 2018 | 43 | 9 | **36** ICB co-actor only (may be allies) · **7** ICB co-actor only, pair NEVER opposed in MID/MIDI/COW |
| 2024 | 21 | 3 | **21** GED location count only (not a statement about the pair) |

Only the first bucket is evidence *about the dyad*. MID, MIDI and COW War are the three sources
that record which side a state was on, and they stop covering the grid at **2014-10-02**. After that
date the panel has no sided source at all, so a dyad-date label cannot distinguish an ally from an
adversary, and a location death-count is replicated across every dyad containing that country.

## 6. Verdict under the registered test (§5.1)

```
{
 "degenerate": false,
 "on": [],
 "share_zero_dIES": 0.9017,
 "share_zero_L": 0.8208,
 "threshold": 0.95,
 "rule": "G4_REGISTRATION \u00a75.1, fixed before the numbers were computed"
}
```