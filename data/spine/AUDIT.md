# Spine audit — the honest baseline

*Generated 2026-09-03T00:45:20+00:00 by `src/spine_audit.py` from `data/oil.db` (read-only).
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
| carrying drafting scaffolding | 39 (12.5%) |
| with ≥ 2 distinct source domains | 22 (7.0%) |
| with exactly 1 source domain | 291 |
| with 0 source domains | 0 |
| whose `source_url` is a bare site root, not a document | 3 |
| whose `source_url` is an encyclopaedia (wikipedia and similar) | 28 |
| citing an encyclopaedia anywhere (incl. `sr_json`) | 31 |
| with **no citable domain at all** once encyclopaedias are set aside | 28 |
| description length, median / min / max (chars) | 150 / 53 / 794 |
| descriptions ≥ 700 chars (roughly a 120-word narrative) | 1 |
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
| 1990s | 16 | 4 (25.0%) | 10 (62.5%) | 1 | 0 | 198 | 1 | 13.8 | 22.5 | 63.8 | 2 | 9 | 7 |
| 2000s | 43 | 4 (9.3%) | 0 (0.0%) | 11 | 0 | 150 | 0 | 10.5 | 14.7 | 74.9 | 2 | 17 | 26 |
| 2010s | 85 | 11 (12.9%) | 0 (0.0%) | 5 | 0 | 148 | 0 | 11.4 | 27.2 | 61.4 | 2 | 55 | 30 |
| 2020s | 150 | 10 (6.7%) | 0 (0.0%) | 11 | 0 | 149 | 0 | 11.4 | 25.6 | 63.0 | 2 | 87 | 60 |

## By class

| class | n | placeholder | ≥2 domains | desc median | sr ext % | sr corpus % | sr null % | sr majority-null | IES-90 level | uncovered |
|---|---|---|---|---|---|---|---|---|---|---|
| chokepoint_disruption | 27 | 5 (18.5%) | 1 (3.7%) | 150 | 12.2 | 48.9 | 38.9 | 1 | 25 | 0 |
| conflict_escalation | 55 | 13 (23.6%) | 7 (12.7%) | 145 | 13.6 | 40.7 | 45.6 | 1 | 54 | 0 |
| demand_shock | 17 | 1 (5.9%) | 3 (17.6%) | 147 | 11.8 | 0.0 | 88.2 | 17 | 0 | 17 |
| infrastructure_attack | 48 | 5 (10.4%) | 2 (4.2%) | 154 | 11.5 | 41.5 | 47.1 | 0 | 48 | 0 |
| opec_decision | 52 | 1 (1.9%) | 2 (3.8%) | 149 | 10.2 | 0.0 | 89.8 | 52 | 0 | 52 |
| policy_response | 57 | 5 (8.8%) | 2 (3.5%) | 140 | 11.1 | 0.2 | 88.8 | 57 | 0 | 57 |
| sanctions | 57 | 9 (15.8%) | 5 (8.8%) | 160 | 13.0 | 39.5 | 47.5 | 1 | 57 | 0 |

## Every event still carrying drafting scaffolding (39)

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
| thai_baht_float_1997 | 1997-07-02 | demand_shock | draft coding | 632 | 2 | 2 | uncovered |
| operation_desert_fox_1998 | 1998-12-16 | conflict_escalation | draft coding | 794 | 1 | 4 | level |
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

<!-- APPENDED BELOW: hand-written, preserved across regeneration -->

# 2026-09-02 — the pre-2000 repair, before and after

*Session E. The tables above are regenerated from the database on every run of
`src/spine_audit.py`; this section is written by hand and preserved. It records what four
applied patches changed, what is still open, and what cannot be repaired at all.*

## What was done

All 35 pre-2000 records were taken to `SPINE_REGISTRATION.md`: a dossier each under
`data/dossiers/`, 31 of 35 passing `src/spine_check.py`, 4 honest partials, none claiming
more than it shows. Four patches were then applied on Joe's line
(`src/spine_apply.py --approved-by joe`), each backed up and applied in one transaction:
`pre1990_a` (29 rows), `pre1990_b` (13), `1990s_a` (7), `1990s_b` (17) — **66 field changes
applied, 13 rows flagged and left open**.

## Before and after, by decade

Baseline is the audit committed at `2dd291f`, before any record was rewritten.

| decade | n | ≥2 source domains | bare site-root URL | encyclopaedia-only | drafting scaffolding |
|---|---|---|---|---|---|
| 1970s | 8 | 0 → **7** | 3 → **1** | 0 → 0 | 8 → **5** |
| 1980s | 11 | 0 → **5** | 6 → **2** | 0 → 0 | 10 → **5** |
| 1990s | 16 | 0 → **10** | 0 → 0 | 4 → **1** | 6 → **4** |
| 2000s | 43 | 0 → 0 | 0 → 0 | 11 → 11 | 4 → 4 |
| 2010s | 85 | 0 → 0 | 0 → 0 | 5 → 5 | 11 → 11 |
| 2020s | 150 | 0 → 0 | 0 → 0 | 11 → 11 | 10 → 10 |
| **total** | **313** | **0 → 22** | **9 → 3** | **31 → 28** | **49 → 39** |

The encyclopaedia column's baseline was measured when that check was added, a few commits
after `2dd291f`; every other baseline is from `2dd291f` itself. The post-2000 rows are
unchanged because they are Session A's half of the repair, not E's.

The first column is the one that matters. The codebook's two-source rule had been an
admission standard the corpus had never met in a single record. Twenty-two records now
meet it, all of them pre-2000.

## Still open: the 13 rows flagged `needs_joe`

None of these was decided by Session E. Each is a judgement, an unresolved conflict between
sources, or a value no source supports.

| # | batch | record and field | now | what the dossier says |
|---|---|---|---|---|
| 1 | pre1990_a | `iran_oilworkers_strike_1978`.type | `infrastructure_attack` | a labour strike is not a "direct strike" on infrastructure; no closed-set class fits |
| 2 | pre1990_b | `kharg_strikes_1985`.event_date | 1985-08-15 | the single retrieved source says 14 August; do not change on one source |
| 3 | pre1990_b | `kharg_strikes_1985`.date_precision | day | hangs on the one-day discrepancy above |
| 4 | pre1990_b | `opec_price_collapse_1986`.event_date | 1986-01-01 | do not set a single day; `1985-12` if a value is required |
| 5 | pre1990_b | `opec_price_collapse_1986`.date_precision | day | month: no day is pinnable in either the September or December 1985 window |
| 6 | pre1990_b | `bridgeton_mine_strike_1987`.surprise | 3 | borderline 2–3; do not change silently |
| 7 | pre1990_b | `praying_mantis_1988`.surprise | 3 | possibly overstated given the October 1987 precedent |
| 8 | pre1990_b | `iran_iraq_ceasefire_1988`.type | `policy_response` | unsupported by the evidence, and no closed-set class fits a de-escalation |
| 9 | 1990s_a | `iraq_invades_kuwait_1990`.surprise | 5 | the evidence supports the existing code |
| 10 | 1990s_a | `desert_storm_air_campaign_1991`.description | draft text | drop the "DRAFT coding" language; the substance is accurate |
| 11 | 1990s_a | `ilsa_sanctions_1996`.description | "$20M/yr" | the $20M/$40M split is not in the statute text; both sources give $40 million |
| 12 | 1990s_b | `opec_cut_june_1998`.source_url | Wikipedia | no replacement retrievable; the dossier recommends unsetting rather than keeping it |
| 13 | 1990s_b | `opec_cut_june_1998`.confidence | high | assigned on the strength of a now-disqualified source |

A fourteenth question is open without being a patch row: `iran_iraq_ceasefire_1988` is dated
1988-08-20, the day the ceasefire took effect, while the UN's own mission history records the
Secretary-General announcing it on 8 August "with effect from 0300 GMT on 20 August". The
codebook dates an event to the first day the market could have known. The dossier flagged
this rather than proposing it, so no change was applied.

## What cannot be repaired, and why

**Four records are blocked by declassification, not by effort.** `iran_revolution_1979`
needs *Foreign Relations of the United States* Volume X (Iran, January 1977 – November 1979);
`tanker_war_1984`, `kharg_strikes_1985` and `iraq_kharg_1986` need FRUS 1981–1988 Volumes XX
and XXI (Iran, Iraq). All three volumes were checked directly and are marked "Being Cleared":
they are not published. These records rest on scholarly secondary sources and will stay
`partial` until the United States declassifies the volumes. No route table, subscription or
further searching changes that.

**Twenty-eight records have no citable domain at all.** They cite an encyclopaedia and
nothing else, which the codebook's own inclusion criterion 2 — "a primary or major-wire
source exists. No source = not in the dataset" — does not admit. All 28 are post-2000 and
belong to Session A's half of the repair. Ten of them are OPEC decisions, which is the
hardest case: `opec.org` returns HTTP 402, the Oxford Institute for Energy Studies 403, the
Congressional Research Service 403, and the Associated Press refuses the client, so the
class that most needs re-sourcing is the class with no free route to a document
(`SPINE_REGISTRATION.md` Amendment 2).

**One record has now proved that constraint individually.** `opec_cut_june_1998` defeated
about twenty documented retrieval routes — OPEC, Oxford, the EIA, the IEA, the IMF, the
Congressional Research Service, UPI, the BIS, FRASER, the Federal Reserve, GovInfo including
a full Congressional Record day and the API, the Internet Archive, and three search engines.
None named a June 1998 OPEC decision. Its Wikipedia citation therefore stands, flagged, and
the dossier recommends unsetting the field rather than keeping a source the codebook does not
admit. It is the clearest single instance of the general problem: for OPEC decisions the
corpus cannot currently be repaired by any free route, and closing them needs an archive the
project does not have.

**One measure did not move and should not be explained away.** `descriptions ≥ 700 chars`
went from 0 to 1. The 120–250 word narratives live in the dossiers; what a patch writes into
`events.description` is a one-paragraph summary. Either the corpus row should carry the
narrative, which is a further patch, or `SPINE_REGISTRATION.md` §7 is counting the wrong
artifact. The measure was not redefined to make it pass.
