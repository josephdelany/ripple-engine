# Spine audit — the honest baseline

*Generated 2026-09-03T00:01:26+00:00 by `src/spine_audit.py` from `data/oil.db` (read-only).
Session E, step E-1: published before any record is rewritten, so the repair can be
scored against a number rather than an impression. Every figure below is computed;
none is asserted. Re-run the script to regenerate this file.*

## What is measured

Per event: the number of distinct source domains (across `source_url` and every URL in
`sr_json.sources`), the description length, the provenance mix of the `sr_json` field
sources (external URL / corpus-derived / null), whether the description still carries
drafting scaffolding, the entity count, and whether an independent IES-90 level exists.
A "domain" strips a leading `www.`, so `eia.gov` and `www.eia.gov` are one source — the
conservative reading of the two-source rule. A `corpus:` source is self-referential: it
is derived from this corpus and so cannot corroborate it. An **encyclopaedia** domain
(wikipedia and similar) is counted separately and excluded from "citable domains": the
codebook requires "a primary or major-wire source", and an encyclopaedia is a tertiary
summary of sources it does not itself constitute.

## Overall (313 events)

| measure | value |
|---|---|
| events | 313 |
| carrying drafting scaffolding | 41 (13.1%) |
| with ≥ 2 distinct source domains | 17 (5.4%) |
| with exactly 1 source domain | 296 |
| with 0 source domains | 0 |
| whose `source_url` is a bare site root, not a document | 3 |
| whose `source_url` is an encyclopaedia (wikipedia and similar) | 30 |
| citing an encyclopaedia anywhere (incl. `sr_json`) | 31 |
| with **no citable domain at all** once encyclopaedias are set aside | 30 |
| description length, median / min / max (chars) | 150 / 53 / 487 |
| descriptions ≥ 700 chars (roughly a 120-word narrative) | 0 |
| `sr_json` field-source slots | 3130 |
| — external URL | 11.9% |
| — corpus-derived | 25.0% |
| — null | 63.1% |
| events whose field sources are majority null | 129 |
| entities per event, median | 2 |
| events with 0 entities | 0 |
| IES-90 level present | 184 |
| flagged `no_independent_outcome` | 3 |
| neither (uncovered) | 126 |
| `severity` null | 8 |

## By decade

| decade | n | placeholder | ≥2 domains | encyclopaedia url | generic-root url | desc median | desc ≥700 | sr ext % | sr corpus % | sr null % | entities median | IES-90 level | uncovered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1970s | 8 | 5 (62.5%) | 7 (87.5%) | 0 | 1 | 100 | 0 | 20.0 | 40.0 | 40.0 | 2 | 8 | 0 |
| 1980s | 11 | 5 (45.5%) | 5 (45.5%) | 0 | 2 | 265 | 0 | 20.0 | 31.8 | 48.2 | 2 | 8 | 3 |
| 1990s | 16 | 6 (37.5%) | 5 (31.2%) | 3 | 0 | 175 | 0 | 13.8 | 22.5 | 63.8 | 2 | 9 | 7 |
| 2000s | 43 | 4 (9.3%) | 0 (0.0%) | 11 | 0 | 150 | 0 | 10.5 | 14.7 | 74.9 | 2 | 17 | 26 |
| 2010s | 85 | 11 (12.9%) | 0 (0.0%) | 5 | 0 | 148 | 0 | 11.4 | 27.2 | 61.4 | 2 | 55 | 30 |
| 2020s | 150 | 10 (6.7%) | 0 (0.0%) | 11 | 0 | 149 | 0 | 11.4 | 25.6 | 63.0 | 2 | 87 | 60 |

## By class

| class | n | placeholder | ≥2 domains | desc median | sr ext % | sr corpus % | sr null % | sr majority-null | IES-90 level | uncovered |
|---|---|---|---|---|---|---|---|---|---|---|
| chokepoint_disruption | 27 | 5 (18.5%) | 1 (3.7%) | 150 | 12.2 | 48.9 | 38.9 | 1 | 25 | 0 |
| conflict_escalation | 55 | 13 (23.6%) | 7 (12.7%) | 145 | 13.6 | 40.7 | 45.6 | 1 | 54 | 0 |
| demand_shock | 17 | 1 (5.9%) | 0 (0.0%) | 147 | 11.8 | 0.0 | 88.2 | 17 | 0 | 17 |
| infrastructure_attack | 48 | 5 (10.4%) | 2 (4.2%) | 154 | 11.5 | 41.5 | 47.1 | 0 | 48 | 0 |
| opec_decision | 52 | 3 (5.8%) | 0 (0.0%) | 149 | 10.2 | 0.0 | 89.8 | 52 | 0 | 52 |
| policy_response | 57 | 5 (8.8%) | 2 (3.5%) | 140 | 11.1 | 0.2 | 88.8 | 57 | 0 | 57 |
| sanctions | 57 | 9 (15.8%) | 5 (8.8%) | 159 | 13.0 | 39.5 | 47.5 | 1 | 57 | 0 |

## Every event still carrying drafting scaffolding (41)

| event_id | date | class | marker | desc len | domains | entities | IES-90 |
|---|---|---|---|---|---|---|---|
| abqaiq_arabian_1977 | 1977-05-11 | infrastructure_attack | deep-history tier | 99 | 1 | 2 | level |
| iran_oilworkers_strike_1978 | 1978-10-31 | infrastructure_attack | deep-history tier | 102 | 2 | 2 | level |
| shah_leaves_iran_1979 | 1979-01-16 | conflict_escalation | deep-history tier | 59 | 2 | 2 | level |
| iran_revolution_1979 | 1979-02-11 | conflict_escalation | deep-history tier | 72 | 2 | 2 | level |
| iran_hostage_crisis_1979 | 1979-11-04 | conflict_escalation | deep-history tier | 85 | 2 | 2 | level |
| tanker_war_1984 | 1984-03-27 | chokepoint_disruption | deep-history tier | 88 | 1 | 2 | level |
| earnest_will_1987 | 1987-07-22 | chokepoint_disruption | deep-history tier | 94 | 2 | 2 | level |
| bridgeton_mine_strike_1987 | 1987-07-24 | chokepoint_disruption | draft coding | 269 | 1 | 3 | level |
| iran_air_655_1988 | 1988-07-03 | conflict_escalation | deep-history tier | 75 | 2 | 2 | level |
| iran_iraq_ceasefire_1988 | 1988-08-20 | policy_response | deep-history tier | 82 | 2 | 2 | uncovered |
| desert_storm_air_campaign_1991 | 1991-01-17 | conflict_escalation | draft coding | 191 | 1 | 5 | level |
| ilsa_sanctions_1996 | 1996-08-05 | sanctions | draft coding | 205 | 1 | 4 | level |
| thai_baht_float_1997 | 1997-07-02 | demand_shock | draft coding | 179 | 1 | 2 | uncovered |
| opec_jakarta_quota_increase_1997 | 1997-12-01 | opec_decision | draft coding | 211 | 1 | 2 | uncovered |
| operation_desert_fox_1998 | 1998-12-16 | conflict_escalation | draft coding | 201 | 1 | 4 | level |
| opec_cut_1999 | 1999-03-23 | opec_decision | draft coding | 177 | 1 | 2 | uncovered |
| september_11_attacks_2001 | 2001-09-11 | conflict_escalation | draft coding | 207 | 1 | 3 | level |
| iea_release_katrina_2005 | 2005-09-02 | policy_response | draft coding | 145 | 1 | 2 | uncovered |
| israel_hezbollah_war_2006 | 2006-07-12 | conflict_escalation | draft coding | 225 | 1 | 3 | level |
| russia_georgia_war_2008 | 2008-08-08 | conflict_escalation | draft coding | 185 | 1 | 3 | level |
| iea_release_libya_2011 | 2011-06-23 | policy_response | draft coding | 129 | 1 | 2 | uncovered |
| ndaa_cbi_sanctions_2011 | 2011-12-31 | sanctions | draft coding | 236 | 1 | 3 | level |
| eu_iran_oil_embargo_2012 | 2012-01-23 | sanctions | draft coding | 175 | 1 | 3 | level |
| swift_cutoff_iran_2012 | 2012-03-15 | sanctions | draft coding | 166 | 1 | 3 | level |
| saudi_intervention_yemen_2015 | 2015-03-26 | conflict_escalation | draft coding | 187 | 1 | 3 | level |
| venezuela_financial_sanctions_2017 | 2017-08-25 | sanctions | draft coding | 172 | 1 | 3 | level |
| saudi_suspends_bab_el_mandeb_2018 | 2018-07-25 | chokepoint_disruption | draft coding | 147 | 1 | 4 | level |
| us_ends_iran_waivers_2019 | 2019-04-22 | sanctions | draft coding | 163 | 1 | 3 | level |
| gulf_of_oman_tanker_attacks_2019 | 2019-06-13 | infrastructure_attack | draft coding | 208 | 1 | 3 | level |
| stena_impero_seizure_2019 | 2019-07-19 | chokepoint_disruption | draft coding | 177 | 1 | 3 | level |
| venezuela_asset_freeze_2019 | 2019-08-05 | sanctions | draft coding | 141 | 1 | 3 | level |
| ras_tanura_attack_2021 | 2021-03-07 | infrastructure_attack | draft coding | 200 | 1 | 3 | level |
| colonial_pipeline_shutdown_2021 | 2021-05-07 | infrastructure_attack | draft coding | 172 | 1 | 2 | level |
| spr_release_2021 | 2021-11-23 | policy_response | draft coding | 140 | 1 | 2 | uncovered |
| spr_release_2022 | 2022-03-31 | policy_response | draft coding | 183 | 1 | 3 | uncovered |
| opec_plus_cut_2022 | 2022-10-05 | opec_decision | draft coding | 180 | 1 | 4 | uncovered |
| products_price_cap_2023 | 2023-02-05 | sanctions | draft coding | 153 | 1 | 3 | level |
| iran_strikes_israel_apr_2024 | 2024-04-13 | conflict_escalation | draft coding | 199 | 1 | 3 | level |
| iran_strikes_israel_oct_2024 | 2024-10-01 | conflict_escalation | draft coding | 187 | 1 | 3 | level |
| russia_shadow_fleet_sanctions_2025 | 2025-01-10 | sanctions | draft coding | 169 | 1 | 3 | level |
| israel_iran_war_2025 | 2025-06-13 | conflict_escalation | draft coding | 189 | 1 | 4 | level |

## Source domains, most common first (top 20)

| domain | events citing it |
|---|---|
| en.wikipedia.org | 31 |
| aljazeera.com | 21 |
| eia.gov | 17 |
| cnbc.com | 16 |
| home.treasury.gov | 10 |
| globalsecurity.org | 10 |
| nber.org | 9 |
| presidency.ucsb.edu | 9 |
| opec.org | 8 |
| history.state.gov | 7 |
| mining.com | 6 |
| cnn.com | 6 |
| spglobal.com | 6 |
| themoscowtimes.com | 6 |
| energy.gov | 5 |
| iea.org | 5 |
| npr.org | 5 |
| govinfo.gov | 4 |
| congress.gov | 4 |
| washingtonpost.com | 4 |

## How to read this

The two-source admission rule in the codebook is a standard for future admissions, not a
property of the present corpus: the `≥2 domains` column is the measurement of that gap.
A bare site root (`https://www.eia.gov`) satisfies "every event MUST be sourced" while
citing nothing a reader can check, so it is counted separately rather than treated as a
source. The `sr corpus %` column matters for the same reason a self-citation does: those
field values were derived from this corpus, so they cannot be evidence about it.

`data/spine/audit.json` carries the same numbers per event for later runs to diff.
