# v3 data and provenance audit — IMF PortWatch chokepoint transits

*2026-09-04. Written before any detector was implemented and before any impairment episode was
computed under a registered rule. Every number is a query against `data/oil.db`, reproducible with
the command printed beside it.*

Attribution required by licence: **Sources: UN Global Platform; IMF PortWatch.**

## Why this document exists

v2's reproducibility boundary (`docs/audit/PROVENANCE_BOUNDARY.md`) exists because its input bundle
could not be traced to a verifiable upstream. This audit answers the same questions *before*
building on PortWatch, so v3 does not inherit the same defect.

## 1. What series exist

Twenty-one series: seven chokepoints × three measures.

| chokepoint | series suffixes |
|---|---|
| `hormuz`, `suez`, `bab_el_mandeb`, `bosporus`, `malacca`, `panama`, `cape_of_good_hope` | `n_tanker`, `n_total`, `capacity_tanker` |

Units, from the `series` table (not inferred):

| measure | unit | meaning |
|---|---|---|
| `n_tanker` | **tankers/day** | daily count of tanker transits |
| `n_total` | **ships/day** | daily count of all vessel transits |
| `capacity_tanker` | **metric tons/day** | daily tanker cargo capacity transiting |

`n_tanker` is a **daily transit count**, not a unique-vessel count and not a volume. `capacity_tanker`
is the volumetric measure. The registered detector uses `n_tanker` as primary because it is the
least model-dependent of the three; `capacity_tanker` is a registered secondary.

```sql
SELECT series_id, unit, frequency, source FROM series WHERE series_id LIKE 'portwatch.%';
```

## 2. Coverage, spacing and completeness

| property | value |
|---|---|
| rows per series | **2,799** |
| span | **2019-01-01 … 2026-08-30** |
| expected days in span | **2,799** |
| date gaps | **0** |
| duplicate dates | **0** |
| null values | **0** |

Coverage is exactly contiguous daily with no missing observations in any of the 21 series. There is
therefore **no missing-day imputation problem** in the current snapshot. The detector still
validates spacing and fails loudly rather than assuming this holds for a future snapshot.

## 3. Are missing days zeros, or is zero real traffic?

**Zeros are genuine low traffic, not encoded missingness.** Evidence:

- `hormuz.n_tanker` has 39 zero days and 120 days at ≤2 tankers. **All 120 fall in 2026**, beginning
  **2026-03-02**. The catalogue's Hormuz closure event is dated **2026-03-04**.
- On those days `n_total` is frequently non-zero (2, 3, 7 ships) while `n_tanker` is 0 — the sensor
  is reporting, and tanker traffic specifically has stopped. A missingness artifact would zero all
  three series together.
- `suez.n_tanker` ≤2 on exactly **2021-03-25 and 2021-03-26**. The Ever Given grounded 2021-03-23.

Two independent corroborations against events the detector never sees. Zero is treated as a valid
observation; the detector must not silently drop or impute it.

## 4. Revisions and vintage

`as_of` equals `obs_date` on **all 58,779 PortWatch rows** (0 exceptions), and there are 2,799
distinct `as_of` values — one per day. **`as_of` therefore carries no revision information.** It is
a copy of the observation date, not a publication vintage.

Consequence, stated rather than hidden: these are values *as currently published*. If IMF PortWatch
revises history, this snapshot cannot detect it and the detector cannot be made vintage-aware from
this database. This is a **real-time-inference limitation** and is registered as such. It does not
affect the descriptive estimands, which are explicitly retrospective.

## 5. Redistribution rights

The `series.notes` field records the licence, verified for every PortWatch series:

> IMF Terms and Conditions, Copyright and Usage, special terms for statistical Data
> (imf.org/external/terms.htm, effective 2020-01-02): users may download, copy, publish and
> distribute Data from IMF Sites, with attribution "Source: International Monetary Fund" and no
> alteration of integrity. Published daily aggregates only — upstream AIS inputs are third-party.

**Conclusion: the daily aggregate slice may be committed**, with attribution and unaltered. The
upstream AIS vessel-level inputs are third-party and are neither held nor redistributable.

This is a material improvement on v2: **v3's inputs can be committed, so v3 can be independently
reproducible where v2 was not.** The committed slice is written to `data/v3/portwatch_daily.csv`
with a hash manifest.

## 6. Is `cape_of_good_hope` measured the same way?

Yes — same three measures, same units, same 2,799-day contiguous coverage, same source and licence.
It is included as the **rerouting** indicator: Cape of Good Hope transits *rising* while Suez and
Bab el-Mandeb fall is the diversion. Because the expected sign is opposite, the registration treats
it as a diagnostic, **not** as an impairment route. A fall at the Cape is not an impairment event.

## 7. Does the event catalogue support deterministic linkage?

The committed `data/structural_surface/input/events.csv` has columns
`event_id, event_date, type, title, date_precision` — **no route or geography field**. Geography
lives in `oil.db` in `event_entities`, which has `role ∈ {actor, target, location, affected_market,
source}` and 111 `location` rows, and in `entities`, which contains 13 `chokepoint.*` entities.

**This mapping was created by earlier sessions for other purposes and predates all v3 work.** It is
therefore exogenous to the detector and usable without post-hoc coding, which is the condition the
brief sets. The mapping used is fixed here, before any linkage is run:

| location entity | PortWatch route |
|---|---|
| `chokepoint.hormuz` | `hormuz` |
| `chokepoint.bab_el_mandeb` | `bab_el_mandeb` |
| `chokepoint.suez`, `chokepoint.suez_canal` | `suez` |
| `chokepoint.bosporus` | `bosporus` |
| `chokepoint.malacca` | `malacca` |
| `chokepoint.panama` | `panama` |

Entities with no PortWatch counterpart — `druzhba_pipeline`, `kirkuk_ceyhan_pipeline`,
`cpc_novorossiysk`, `libya_es_sider`, `gibraltar_strait`, `taiwan_strait` — are **not** mapped and
their events are ineligible. `cape_of_good_hope` has no event counterpart, correctly, since it is a
diversion destination rather than an event location.

### Eligibility attrition

| stage | events |
|---|---:|
| catalogue total | 313 |
| dated 2019-01-01 or later (PortWatch coverage) | 171 |
| carrying a `role='location'` entity | 75 |
| **mapping to one of the seven PortWatch routes** | **21** |

By route: Bab el-Mandeb 11, Hormuz 9, Suez 1.

**21 is the honest denominator and it is small.** It is large enough for descriptive reporting and
**too small for confirmatory inference**; the registration says so in advance rather than after
seeing the answer. Nothing in this project may use 313, 171 or 75 as the denominator for a
realization proportion.

## 8. Is JODI needed in this phase?

**No — deferred.** JODI is 106 series, 22 countries × 5 measures, **monthly**, 2002-01 … 2026-06. A
monthly producer-level detector needs its own baseline definition, its own missingness treatment
and its own revision analysis, none of which may borrow parameters from a daily transit detector,
and daily and monthly results may never be pooled. Deferring it keeps this phase honest and
finishable. It is the strongest candidate for the next phase.

## 9. Reproducibility boundary for v3

| layer | status |
|---|---|
| PortWatch daily slice → committed CSV | **redistributable and committed**; hash-manifested |
| committed CSV → episode table | **fully reproducible**, offline, deterministic |
| upstream AIS → PortWatch aggregates | **not reproducible**; third-party, not held |
| `data/oil.db` → committed CSV | one-time export, recorded with input hashes |

So v3 can claim: *the episode table reproduces byte-for-byte from a committed, redistributable
input.* It may **not** claim that PortWatch's own aggregates are independently verifiable.

## 10. What this audit does not establish

- It does not establish that the 313-event catalogue is a comprehensive census of declarations. It
  is not, and no v3 output may describe an unmatched episode as "undeclared", "silent" or "ignored".
  The only permitted phrase is **"not matched to the current event catalogue"**.
- It does not establish that transit counts measure delivered volume. `capacity_tanker` is closer,
  and is registered as a secondary measure.
- It does not establish that a transit decline is caused by any event.
