# T2 — the chokepoint flow register, and what the corpus can actually carry
*Built by `src/g_chokepoint_register.py` under `docs/g/G7_CHOKEPOINT_REGISTER_REGISTRATION.md`,
which was committed first. Generated 2026-09-03T16:14:10+00:00.*

> **Every value in this study is read through `src/g_vintage.py`, which will not return a
> number without the date you are claiming to be at.** There is no `.value` accessor and no
> default `t`. A capacity or flow value that could be read without its publication date would
> be a schema error, not a documentation lapse.

## 0. The filtration audit — Amendment F.1's standing

- terms checked **48** over **30** rows · violations **0** · `asserted`: **True** · study voided: **False**
- G7 §3, in WALK_FORWARD_PROTOCOL Amendment F.1's standing: a single violation voids the study.

## 1. The finding, before the register: T2 is a 25-event variable in a 313-event corpus

| | events |
|---|---|
| corpus | **313** (1973-10-06 … 2026-06-17) |
| predate the first EIA release (2011-03-02) — no T2 term possible | 82 (26.2%) |
| name any chokepoint entity | 37 |
| …of which name an entity EIA does not quantify | 7 |
| …of which predate the first release | 5 |
| **T2 constructible** | **25** |

And the chokepoints the corpus actually names: {"chokepoint.bab_el_mandeb": 13, "chokepoint.cpc_novorossiysk": 1, "chokepoint.druzhba_pipeline": 1, "chokepoint.gibraltar_strait": 1, "chokepoint.hormuz": 13, "chokepoint.kirkuk_ceyhan_pipeline": 1, "chokepoint.libya_es_sider": 2, "chokepoint.suez": 1, "chokepoint.suez_canal": 3, "chokepoint.taiwan_strait": 1}.
**4 of the seven** — cape_of_good_hope, malacca, panama, turkish_straits — are named by **zero**
corpus events, so their register entries exist for future use and contribute nothing today.

Whatever T2 shows, it cannot carry a corpus-wide claim. This is a design fact, established
before any estimate, and it belongs beside §5's verdict words rather than after them.

## 2. The register — four EIA releases, each figure with the sentence it was read from

| chokepoint | published | ref | value (million b/d) | source |
|---|---|---|---|---|
| `bab_el_mandeb` | 2011-03-02 | 2009 | 3.2 | EIA Today in Energy #330 |
| `bab_el_mandeb` | 2017-08-04 | 2016 | 4.8 | EIA Today in Energy #32352 |
| `cape_of_good_hope` | 2011-03-02 | 2009 | **gap — no figure** | EIA Today in Energy #330 |
| `danish_straits` | 2011-03-02 | 2009 | 3.3 | EIA Today in Energy #330 |
| `hormuz` | 2011-03-02 | 2009 | 15.5 | EIA Today in Energy #330 |
| `hormuz` | 2014-12-01 | 2013 | 17.0 | EIA Today in Energy #18991 |
| `hormuz` | 2017-08-04 | 2016 | 18.5 | EIA Today in Energy #32352 |
| `hormuz` | 2025-06-16 | 2024 | 20.0 | EIA Today in Energy #65504 |
| `malacca` | 2011-03-02 | 2009 | 13.6 | EIA Today in Energy #330 |
| `malacca` | 2014-12-01 | 2013 | 15.2 | EIA Today in Energy #18991 |
| `panama` | 2011-03-02 | 2009 | 0.8 | EIA Today in Energy #330 |
| `suez` | 2011-03-02 | 2009 | 1.8 | EIA Today in Energy #330 |
| `suez` | 2017-08-04 | 2016 | 3.9 | EIA Today in Energy #32352 |
| `sumed` | 2011-03-02 | 2009 | 1.1 | EIA Today in Energy #330 |
| `sumed` | 2017-08-04 | 2016 | 1.6 | EIA Today in Energy #32352 |
| `turkish_straits` | 2011-03-02 | 2009 | 2.9 | EIA Today in Energy #330 |
| `world_seaborne` | 2014-12-01 | 2013 | 56.5 | EIA Today in Energy #18991 |
| `world_seaborne` | 2017-08-04 | 2015 | 59.0 | EIA Today in Energy #32352 |

`cape_of_good_hope` is quantified by **no** release retrieved. It is a registered gap, never
a zero (§4). No figure is carried forward from one release to another, and no denominator is
back-derived from a rounded share (§4.1).

## 3. T2 per event

| event | date | chokepoint | flow | world seaborne | **T2 share** | if null, why |
|---|---|---|---|---|---|---|
| `tanker_war_1984` | 1984-03-27 | hormuz | — | — | — | no release published on or before t quantifies this chokepoint |
| `earnest_will_1987` | 1987-07-22 | hormuz | — | — | — | no release published on or before t quantifies this chokepoint |
| `bridgeton_mine_strike_1987` | 1987-07-24 | hormuz | — | — | — | no release published on or before t quantifies this chokepoint |
| `suez_tropic_brilliance_2004` | 2004-11-08 | suez | — | — | — | no release published on or before t quantifies this chokepoint |
| `egypt_revolution_2011` | 2011-01-25 | suez | — | — | — | no release published on or before t quantifies this chokepoint |
| `hormuz_iran_threat_2011` | 2011-12-27 | hormuz | 15.5 | — | — | no world seaborne denominator published on or before t (§4.1: null, not imputed) |
| `egypt_coup_suez_2013` | 2013-07-03 | suez | 1.8 | — | — | no world seaborne denominator published on or before t (§4.1: null, not imputed) |
| `bab_el_mandeb_houthi_tanker_2018` | 2018-04-03 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `saudi_suspends_bab_el_mandeb_2018` | 2018-07-25 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `fujairah_tanker_sabotage_2019` | 2019-05-12 | hormuz | 18.5 | 59.0 | **0.3136** |  |
| `gulf_of_oman_tanker_attacks_2019` | 2019-06-13 | hormuz | 18.5 | 59.0 | **0.3136** |  |
| `stena_impero_seizure_2019` | 2019-07-19 | hormuz | 18.5 | 59.0 | **0.3136** |  |
| `soleimani_strike_2020` | 2020-01-03 | hormuz | 18.5 | 59.0 | **0.3136** |  |
| `hankuk_chemi_seizure_2021` | 2021-01-04 | hormuz | 18.5 | 59.0 | **0.3136** |  |
| `suez_ever_given_2021` | 2021-03-23 | suez | 3.9 | 59.0 | **0.0661** |  |
| `mercer_street_2021` | 2021-07-29 | hormuz | 18.5 | 59.0 | **0.3136** |  |
| `me_galaxy_leader_2023` | 2023-11-19 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `red_sea_attacks_2023` | 2023-12-01 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_maersk_diversions_2023` | 2023-12-15 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_us_uk_strikes_2024` | 2024-01-11 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_marlin_luanda_2024` | 2024-01-26 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_rubymar_2024` | 2024-02-18 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_mv_tutor_2024` | 2024-06-12 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_chios_lion_2024` | 2024-07-15 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_sounion_2024` | 2024-08-21 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_rough_rider_2025` | 2025-03-15 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `me_midnight_hammer_2025` | 2025-06-22 | hormuz | 20.0 | 59.0 | **0.3390** |  |
| `redsea_houthi_resume_2025` | 2025-07-06 | bab_el_mandeb | 4.8 | 59.0 | **0.0814** |  |
| `hormuz_closure_2026` | 2026-03-04 | hormuz | 20.0 | 59.0 | **0.3390** |  |
| `us_iran_hormuz_mou_2026` | 2026-06-17 | hormuz | 20.0 | 59.0 | **0.3390** |  |

**23 of 30 event-chokepoint rows carry a T2 share.**

## 4. PortWatch cross-check (§6) — shares, never levels; gates nothing

| date | n chokepoints | Spearman rank (EIA vs PortWatch) |
|---|---|---|
| 2019-05-12 | 6 | +0.943 |
| 2019-06-13 | 6 | +0.943 |
| 2019-07-19 | 6 | +0.943 |
| 2020-01-03 | 6 | +0.943 |
| 2021-01-04 | 6 | +0.943 |
| 2021-03-23 | 6 | +0.943 |
| 2021-07-29 | 6 | +0.943 |
| 2023-11-19 | 6 | +0.943 |
| 2023-12-01 | 6 | +0.943 |
| 2023-12-15 | 6 | +0.943 |
| 2024-01-11 | 6 | +0.943 |
| 2024-01-26 | 6 | +0.943 |
| 2024-02-18 | 6 | +0.943 |
| 2024-06-12 | 6 | +0.886 |
| 2024-07-15 | 6 | +0.886 |
| 2024-08-21 | 6 | +0.886 |
| 2025-03-15 | 6 | +0.886 |
| 2025-06-22 | 6 | +0.886 |
| 2025-07-06 | 6 | +0.886 |
| 2026-03-04 | 6 | +0.886 |
| 2026-06-17 | 6 | +0.143 |

PortWatch measures transiting tanker capacity (AIS); EIA measures barrels of oil. Shares only, never levels; no conversion is asserted.

`cape_of_good_hope` is excluded from the rank statistic by registration (§6): it is a route,
not a strait, and a transit count there is not comparable to a chokepoint flow.