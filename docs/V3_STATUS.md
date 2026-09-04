# v3 status — declared versus realized petroleum disruption

*2026-09-04. Branch `research/v3`, built from `submission-v2.0.1` (`f4dd795`), which is unchanged.*

Sources: UN Global Platform; IMF PortWatch.

## Résumé status

> **Not résumé-ready; research foundation only.**

There is a reproducible instrument and an honest feasibility conclusion. There is no defensible
quantitative finding with a usable denominator, so no v3 résumé bullet is drafted and the approved
v2 bullet in `docs/RESUME.md` stands unchanged.

## What was completed

| phase | outcome |
|---|---|
| **0 — provenance and identifiability audit** | complete (`docs/audit/V3_DATA_AUDIT.md`) |
| **0 — registration before implementation** | complete (`registrations/DISRUPTION_REALIZATION.md`, committed `0173ccb`, before the detector existed) |
| **1 — event-blind detector** | complete, tested, frozen, reproducible (`96035ed`) |
| **1 — preregistered sensitivity grid** | complete, all nine cells reported |
| **2 — linkage feasibility** | attempted, run once, **declared not usable** (`docs/audit/V3_LINKAGE_FEASIBILITY.md`) |
| **price analysis** | **not started, by design.** No price series has been inspected at any point. |

## Exact counts

**Input.** 21 PortWatch series (7 chokepoints × 3 measures), 2,799 contiguous daily observations
each, 2019-01-01 … 2026-08-30. Zero gaps, zero duplicates, zero nulls, no revision history.

**Detection.** 2020-01-31 … 2026-08-30, 2,404 eligible route-days per route, 6 impairment routes.
**39 episodes** at the registered specification (threshold 0.70, ≥5 impaired days, baseline 365/30):

| route | episodes | longest |
|---|---:|---|
| bab_el_mandeb | 9 | 242 days from 2023-12-28 |
| suez | 9 | 121 days from 2024-01-07 |
| hormuz | 8 | 183 days from 2026-03-01 |
| panama | 8 | 51 days from 2023-12-25 |
| bosporus | 5 | 10 days |
| malacca | **0** | — |

**Sensitivity (all nine registered cells, none selected).** Episode counts range **16 to 195**:

| threshold \ min days | 3 | 5 | 7 |
|---|---:|---:|---:|
| 0.60 | 44 | 24 | 16 |
| **0.70** | 106 | **39 (primary)** | 19 |
| 0.80 | 195 | 98 | 59 |

**Linkage.** 313 catalogue events → 28 route-mapped → 11 before the detection start → **17
eligible**. A = 4/17 = 0.235 (Wilson [0.096, 0.473]); B = 4/39 = 0.103 (Wilson [0.041, 0.236]).
Identical under the strict window.

## Is linkage identifiable?

**Geographically yes; temporally no.** The event→route mapping exists in `event_entities`, is
deterministic, and predates all v3 work, so it is exogenous. The registered *onset-window* rule is
not fit for purpose and its proportions are not findings. Three evidenced failure modes:

1. The largest episode in the record — Hormuz, 183 days at 100% impairment — is excluded **by one
   day**. Traffic collapsed 2026-03-01, three days before the 2026-03-04 declaration; the
   registered lead is two days.
2. Slow-onset disruptions fall outside the 14-day lag. Two of the three Red Sea declaring events
   sit 27 and 39 days ahead of sustained onset.
3. Events occurring *inside* a running episode can never link, because linkage keys on onset. Four
   Houthi events fall within one 242-day episode and none count.

**The window was not widened after seeing this.** Doing so would be the post-hoc tuning the design
exists to prevent. A corrected rule needs a new registration and a larger eligible set than 17.

## Claim classification

**Engineering validation** — the detector reproduces its frozen output byte-for-byte from a
committed input; 40 tests pass; blinding is machine-enforced over the dependency graph.

**Exploratory observation** — blind to the catalogue, the detector recovered Ever Given (Suez
2021-03-23, trough 03-25, against a 03-23 grounding), the Red Sea campaign at two chokepoints
simultaneously, the Panama Canal drought, and the Hormuz closure. This is corroboration that the
instrument measures something real. **It is not a result**: the comparison was made after the fact
and no hypothesis was tested by it.

**Registered confirmatory result** — none. This phase ran no hypothesis test.

**Unresolved hypothesis** — whether declared disruptions systematically differ from realized ones,
and whether realized impairment predicts price response. Neither is answerable from 17 events.

## Independently reproducible?

**Yes, for the first time in this project.** The IMF licence permits redistribution of the daily
aggregates with attribution, so `data/v3/portwatch_daily.csv` (58,779 rows) is committed with a
hash manifest and the episode table rebuilds from it offline with no database and no network. This
is strictly stronger than v2, whose bundle could not be traced upstream
(`docs/audit/PROVENANCE_BOUNDARY.md`).

Not reproducible: PortWatch's own aggregates from upstream AIS, which is third-party and not held.

## Known limitations

- **Episode counts are highly parameter-sensitive** (16–195 across nine cells). The *large*
  episodes are stable in every cell; the count is not. No count should be quoted without its
  specification.
- **`as_of` equals `obs_date` on every row**, so there is no revision history and the detector
  cannot be made vintage-aware. This phase is retrospective and claims no real-time availability.
- Transit **counts** are not delivered **volume**. `capacity_tanker` is nearer and is registered as
  a secondary measure; it has not been run.
- The 313-event catalogue is curated and is **not a census of declarations**. Unmatched episodes
  are **"not matched to the current event catalogue"** and nothing stronger. The catalogue has no
  entry at all for the Panama drought, which the detector found as 8 episodes.
- Malacca produced zero episodes. That is consistent with it being the most stable route in the
  input, but no test establishes it.
- Registration §24 records that the author had seen a preliminary below-baseline count by route and
  year before writing the registration. **This phase is registered but not blind.**

## Verification

```bash
cd "/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine"
git checkout research/v3
make verify-v3-foundation      # detector tests, rebuild, sensitivity grid, drift check
make verify-submission         # v2 must remain green on this branch
python3 src/disruption_episodes.py --help
python3 src/disruption_episodes.py --report
python3 src/disruption_linkage.py
git diff --check && git status --short
```

## Commits

| commit | contents |
|---|---|
| `0173ccb` | registration + data audit, **before any detector code existed** |
| `b67784f` | episode-duration ambiguity resolved before the first run |
| `96035ed` | blind detector, committed input slice, frozen output, 32 tests |
| *(this commit)* | sensitivity grid, linkage feasibility, amendments 2–3, status |

`submission-v2.0.1` still resolves to `f4dd795` and no existing tag was moved.

## Next highest-value task

**Code route geography for the rest of the catalogue, under a written rule, before any further
linkage.** Only 28 of 313 events carry a route-mapped `location` entity, and that — not the
detector, not the data — is what makes every linkage estimate uninformative. It is bounded,
mechanical work on data already held.

Second: register an **overlap-based** linkage rule with an asymmetric window justified from
shipping-response evidence independent of these episodes. Third: run the detector on
`capacity_tanker` as the registered secondary measure. A monthly JODI producer-level detector is
deferred and needs its own registration; daily and monthly results may never be pooled.
