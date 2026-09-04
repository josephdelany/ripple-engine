> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Working record of the pre-1973 admission and vintage work. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# G-3 — the situation fields' `knowable_at`, derived from dossier document dates
*Computed by `src/situation_vintage.py` under `docs/g/G3_REGISTRATION.md`, which was committed first.*
*Generated 2026-09-03T02:59:01+00:00. Nothing here is written to `events` or `situation_state`.*

## 0. The BEFORE column is recomputed, not copied

Session A's rules (a)–(d) are re-implemented in this script and run against the same database, so the
baseline can be checked rather than trusted. Against `data/state/situation_knowable.json`:

    published:  {"events": 313, "kept": 60, "dropped_after_t": 726, "events_with_no_situation_field_at_t": 262, "knowable_at_rules": {"c:coding_date(undated url)": 297, "c:coding_date(corpus-derived)": 413, "a:url_date": 76}, "values": 786}
    recomputed: {"events": 313, "kept": 60, "dropped_after_t": 726, "events_with_no_situation_field_at_t": 262, "values": 786, "knowable_at_rules": {"c:coding_date(undated url)": 297, "c:coding_date(corpus-derived)": 413, "a:url_date": 76}}
    agrees:     True

## 1. Before and after

| | situation values | kept at t | dropped at t | events with ≥1 field at t |
|---|---|---|---|---|
| Amendment A, as published | 786 | **60** | 726 | 51 of 313 |
| with rule (e) | 786 | **83** | 703 | 62 of 313 |
| *diagnostic, not registered:* min of (a)/(c) and (e) | 786 | *86* | 700 | 64 of 313 |

The diagnostic row is Amendment 2 and **gates nothing**: it prices the (e.0) choice to let a
transcribed document date override a date read out of a URL path, at +3 values.

Net **+23** values (26 gained, 3 lost); **+13** events gain a field at t, 2 lose their last one.

## 2. By field

| field | values | kept before | kept after | change |
|---|---|---|---|---|
| `actor` | 153 | 28 | 38 | +10 |
| `target` | 220 | 32 | 38 | +6 |
| `conflict_scope` | 184 | 0 | 0 | +0 |
| `tempo` | 187 | 0 | 7 | +7 |
| `asset_role` | 42 | 0 | 0 | +0 |

`conflict_scope`: 184 values reclassified by (e.8) from the coding
date to `event_date + 120 days`. This is a **correction, not a recovery** — it cannot raise the kept
count, and it says the field can never be a target-side feature of any read, at any level of sourcing.

## 3. Which rule dated each value

| rule | before | after |
|---|---|---|
| `a:url_date` | 76 | 73 |
| `c:coding_date(corpus-derived)` | 413 | 213 |
| `c:coding_date(undated url)` | 297 | 256 |
| `e.2:dossier_doc_date` | 0 | 44 |
| `e.3:dossier_dyad_date` | 0 | 16 |
| `e.8:forward_window(+120d)` | 0 | 184 |

## 4. Why rule (e) did not fire, where it did not

| count | clause and reason |
|---|---|
| 514 | (e.0) no dossier for this event |
| 9 | (e.3) a dyad member has no receipt -- |
| 3 | (e.2 iv) negation phrase present: 'gap' |
| 3 | (e.2 iii) the bullet cites no source marker |
| 2 | (e.2 iv) negation phrase present: 'not confirmed' |
| 2 | (e.2 iv) negation phrase present: 'no source retrieved' |
| 2 | (e.2 i) no bullet in the dossier names this entity_id |
| 1 | (e.2 iv) negation phrase present: 'not named' |
| 1 | (e.4) no chokepoint entity ['chokepoint.hormuz'] has a receipt: (e.2 iv) negation phrase present: 'no source r |
| 1 | (e.2 iv) negation phrase present: 'proposes reclassifying' |
| 1 | (e.4) no chokepoint entity ['chokepoint.hormuz'] has a receipt: (e.2 iv) negation phrase present: 'proposes re |
| 1 | (e.4) no chokepoint entity ['chokepoint.hormuz'] has a receipt: (e.2 iv) negation phrase present: 'gap' |
| 1 | (e.2 iv) negation phrase present: 'flags the role' |
| 1 | (e.2) no cited source has a parseable Doc. date |

## 5. Values rule (e) moved LATER than Amendment A gave them (the losses)

| event | field | value | before | after |
|---|---|---|---|---|
| `iran_eo12959_embargo_1995` | target | country.iran | 1995-05-06 (a:url_date) | 1995-05-09 (e.2:dossier_doc_date) |
| `korea_imf_bailout_1997` | actor | institution.imf | 1997-11-21 (a:url_date) | 1997-12-16 (e.2:dossier_doc_date) |
| `korea_imf_bailout_1997` | target | country.south_korea | 1997-11-21 (a:url_date) | 1997-12-16 (e.2:dossier_doc_date) |

## 6. Values rule (e) recovered

| event | field | value | before | after |
|---|---|---|---|---|
| `oapec_embargo_1973` | actor | country.saudi_arabia | 2026-09-02 (c:coding_date(undated url)) | 1973-10-17 |
| `embargo_lifted_1974` | target | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1974-03-18 |
| `iran_hostage_crisis_1979` | actor | country.iran | 2026-09-02 (c:coding_date(undated url)) | 1979-11-04 |
| `iran_hostage_crisis_1979` | target | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1979-11-04 |
| `iran_hostage_crisis_1979` | tempo | nth | 2026-09-02 (c:coding_date(corpus-derived)) | 1979-11-04 |
| `carter_doctrine_1980` | actor | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1980-01-23 |
| `earnest_will_1987` | actor | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1987-07-22 |
| `bridgeton_mine_strike_1987` | actor | country.iran | 2026-09-02 (c:coding_date(undated url)) | 1987-07-24 |
| `iran_air_655_1988` | actor | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1988-07-03 |
| `iraq_invades_kuwait_1990` | actor | country.iraq | 2026-09-02 (c:coding_date(undated url)) | 1990-08-02 |
| `iraq_invades_kuwait_1990` | target | country.kuwait | 2026-09-02 (c:coding_date(undated url)) | 1990-08-02 |
| `iraq_invades_kuwait_1990` | tempo | nth | 2026-09-02 (c:coding_date(corpus-derived)) | 1990-08-02 |
| `desert_storm_air_campaign_1991` | actor | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1991-01-17 |
| `desert_storm_air_campaign_1991` | target | country.iraq | 2026-09-02 (c:coding_date(undated url)) | 1991-01-17 |
| `desert_storm_air_campaign_1991` | tempo | nth | 2026-09-02 (c:coding_date(corpus-derived)) | 1991-01-17 |
| `kuwait_oil_fires_1991` | actor | country.iraq | 2026-09-02 (c:coding_date(undated url)) | 1991-02-22 |
| `kuwait_oil_fires_1991` | target | country.kuwait | 2026-09-02 (c:coding_date(undated url)) | 1991-02-22 |
| `kuwait_oil_fires_1991` | tempo | nth | 2026-09-02 (c:coding_date(corpus-derived)) | 1991-02-22 |
| `iraq_un_986_ofp_1995` | target | country.iraq | 2026-09-02 (c:coding_date(undated url)) | 1995-04-14 |
| `iraq_un_986_ofp_1995` | tempo | nth | 2026-09-02 (c:coding_date(corpus-derived)) | 1995-04-14 |
| `ilsa_sanctions_1996` | actor | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1996-08-05 |
| `ilsa_sanctions_1996` | target | country.iran | 2026-09-02 (c:coding_date(undated url)) | 1996-08-05 |
| `ilsa_sanctions_1996` | tempo | nth | 2026-09-02 (c:coding_date(corpus-derived)) | 1996-08-05 |
| `operation_desert_fox_1998` | actor | country.usa | 2026-09-02 (c:coding_date(undated url)) | 1998-12-16 |
| `operation_desert_fox_1998` | target | country.iraq | 2026-09-02 (c:coding_date(undated url)) | 1998-12-16 |
| `operation_desert_fox_1998` | tempo | nth | 2026-09-02 (c:coding_date(corpus-derived)) | 1998-12-16 |

## 7. The audit table — every decision, against the dossier text it came from

One row per field rule (e) was **considered** for, derived or not. Open
`data/dossiers/<event_id>.md`, find the quoted bullet, and check the decision follows.
Registration §6: finding nothing wrong here is not evidence that it is right.

### `yom_kippur_war_1973` · 1973-10-06 · `actor` = `country.egypt`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1973-10-07** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1973-10-06** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.egypt` — actor — named as an attacking party in [S1] ("Egyptians across the Canal") and [S2].`
  - S1: `Washington, October 7, 1973, 6:06–7:06 p.m.` → **1973-10-07** (form1)
  - S2: `February 2011` → **2011-02-28** (form3 (end of month))
- earliest cited document: **1973-10-07**

### `yom_kippur_war_1973` · 1973-10-06 · `target` = `country.israel`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1973-10-07** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1973-10-06** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.israel` — target — the attacked state, per [S1] ("the Israelis") and [S2].`
  - S1: `Washington, October 7, 1973, 6:06–7:06 p.m.` → **1973-10-07** (form1)
  - S2: `February 2011` → **2011-02-28** (form3 (end of month))
- earliest cited document: **1973-10-07**

### `yom_kippur_war_1973` · 1973-10-06 · `tempo` = `first`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1973-10-07** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1973-10-06** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.egypt`: earliest 1973-10-07
  - dyad member `country.israel`: earliest 1973-10-07

### `oapec_embargo_1973` · 1973-10-17 · `actor` = `country.saudi_arabia`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1973-10-17** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1973-10-17** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.saudi_arabia` — actor — Saudi Arabia is not individually named quoted in S1–S3's retrieved text, but is corroborated as a lead OAPEC actor by [S4] and by the broader FRUS record of Saudi Oil Minister Yamani's threats referenced in [S1] ("New York Times article by Edward Cowan mentioning .`
  - S1: `Washington, October 17, 1973, 3:05–4:04 p.m.` → **1973-10-17** (form1)
  - S3: `Washington, October 19, 1973` → **1973-10-19** (form1)
  - S4: `February 2011` → **2011-02-28** (form3 (end of month))
- earliest cited document: **1973-10-17**

### `oapec_embargo_1973` · 1973-10-17 · `target` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1973-10-19** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1973-10-17** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — target — named as the object of embargo threats in [S3] ("total embargo against the United States").`
  - S3: `Washington, October 19, 1973` → **1973-10-19** (form1)
- earliest cited document: **1973-10-19**

### `oapec_embargo_1973` · 1973-10-17 · `tempo` = `first`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1973-10-19** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1973-10-17** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.saudi_arabia`: earliest 1973-10-17
  - dyad member `country.usa`: earliest 1973-10-19

### `embargo_lifted_1974` · 1974-03-18 · `actor` = `country.saudi_arabia`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1974-03-18** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.saudi_arabia` — actor — Saudi Arabia is the lead intermediary pressing for the lift throughout [S2] and [S3], though not named as a signatory in the retrieved text of [S1] itself.`
- **not derived:** (e.2 iv) negation phrase present: 'not named'

### `embargo_lifted_1974` · 1974-03-18 · `target` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1974-03-18** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1974-03-18** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — target — the embargo's object throughout [S1][S2][S3].`
  - S1: `Washington, March 19, 1974` → **1974-03-19** (form1)
  - S2: `Jidda, January 22, 1974` → **1974-01-22** (form1)
  - S3: `Washington; forwarded Feb. 6, handed to Saudi Ambassador Feb. 7, 1974` → **1974-12-31** (form4 (end of year))
- earliest cited document: **1974-01-22** (before the event date; clamped to it by (e.6))

### `embargo_lifted_1974` · 1974-03-18 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1974-03-18** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.saudi_arabia`: (e.2 iv) negation phrase present: 'not named'
  - dyad member `country.usa`: earliest 1974-01-22
- **not derived:** (e.3) a dyad member has no receipt -- country.saudi_arabia: (e.2 iv) negation phrase present: 'not named'

### `abqaiq_arabian_1977` · 1977-05-11 · `actor` = `country.saudi_arabia`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1977-05-11** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.saudi_arabia` — actor and target (per the current `event_entities` rows) — **not confirmed by any source retrieved this session.** If the underlying event was an accidental pipeline failure (an unverified claim above), coding Saudi Arabia as `actor` is itself questionable — an accident ha`
- **not derived:** (e.2 iv) negation phrase present: 'not confirmed'

### `abqaiq_arabian_1977` · 1977-05-11 · `target` = `country.saudi_arabia`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1977-05-11** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.saudi_arabia` — actor and target (per the current `event_entities` rows) — **not confirmed by any source retrieved this session.** If the underlying event was an accidental pipeline failure (an unverified claim above), coding Saudi Arabia as `actor` is itself questionable — an accident ha`
- **not derived:** (e.2 iv) negation phrase present: 'not confirmed'

### `abqaiq_arabian_1977` · 1977-05-11 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1977-05-11** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.saudi_arabia`: (e.2 iv) negation phrase present: 'not confirmed'
- **not derived:** (e.3) a dyad member has no receipt -- country.saudi_arabia: (e.2 iv) negation phrase present: 'not confirmed'

### `iran_oilworkers_strike_1978` · 1978-10-31 · `actor` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1978-11-09** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1978-11-09** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — actor — per the existing `event_entities` rows; consistent with both sources, which discuss Iranian oil workers/strikers and the Iranian state as the locus of the disruption [S1][S2].`
  - S1: `Washington, November 9, 1978, 3–4:23 p.m.` → **1978-11-09** (form1)
  - S2: `February 2011` → **2011-02-28** (form3 (end of month))
- earliest cited document: **1978-11-09**

### `iran_oilworkers_strike_1978` · 1978-10-31 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1978-11-09** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — as currently recorded. This is a modeling oddity worth flagging to Session A rather than resolving here: coding Iran as both actor and target of its own workers' strike blurs who is doing what to whom. A strike is workers acting against employers/the state, not the state `
- **not derived:** (e.2 iv) negation phrase present: 'gap'

### `iran_oilworkers_strike_1978` · 1978-10-31 · `tempo` = `first`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1978-11-09** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: (A1.2) a second bullet for this entity carries a negation phrase: 'gap' -- - `country.iran` — target — as currently recorded. This is a modeling oddity worth flagging to Session A rather than resolving here: coding Iran as both actor a
- **not derived:** (e.3) a dyad member has no receipt -- country.iran: (A1.2) a second bullet for this entity carries a negation phrase: 'gap' -- - `country.iran` — target — as currently recorded. This is a modeling oddity worth flagging to Session A rather than resolving here: coding Iran as both actor a

### `shah_leaves_iran_1979` · 1979-01-16 · `actor` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1979-01-16** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — actor — per the existing `event_entities` rows.`
- **not derived:** (e.2 iii) the bullet cites no source marker

### `shah_leaves_iran_1979` · 1979-01-16 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1979-01-16** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — as currently recorded. As with the other events in this batch, this duplication is flagged rather than resolved: the Shah's own departure is a decision by (or affecting) a head of state, not evidently an act of the Iranian state "against" itself. No replacement entity exi`
- **not derived:** (e.2 iv) negation phrase present: 'gap'

### `shah_leaves_iran_1979` · 1979-01-16 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1979-01-16** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: (e.2 iii) the bullet cites no source marker
- **not derived:** (e.3) a dyad member has no receipt -- country.iran: (e.2 iii) the bullet cites no source marker

### `iran_revolution_1979` · 1979-02-11 · `actor` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1979-02-12** (e.2:dossier_doc_date)
- dossier bullet, verbatim: `- `country.iran` — actor — per the existing `event_entities` rows; consistent with both sources' focus on Iran as the locus of the shortfall/political change [S1][S2].`
  - S1: `Brussels, February 12, 1979, 1002Z` → **1979-02-12** (form1)
  - S2: `February 2011` → **2011-02-28** (form3 (end of month))
- earliest cited document: **1979-02-12**

### `iran_revolution_1979` · 1979-02-11 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- dossier bullet, verbatim: `- `country.iran` — target — as currently recorded, with the same duplication concern flagged in the companion dossiers `iran_oilworkers_strike_1978` and `shah_leaves_iran_1979`. Reported to Session A rather than resolved here.`
- **not derived:** (e.2 iii) the bullet cites no source marker

### `iran_revolution_1979` · 1979-02-11 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
  - dyad member `country.iran`: (A1.2) a second bullet for this entity cites no source marker -- - `country.iran` — target — as currently recorded, with the same duplication concern flagged in the companion dossiers `iran_oilworkers_strike_1978` and `shah_l
- **not derived:** (e.3) a dyad member has no receipt -- country.iran: (A1.2) a second bullet for this entity cites no source marker -- - `country.iran` — target — as currently recorded, with the same duplication concern flagged in the companion dossiers `iran_oilworkers_strike_1978` and `shah_l

### `iran_hostage_crisis_1979` · 1979-11-04 · `actor` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1979-11-04** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1979-11-04** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — actor — per the existing `event_entities` rows; the students are described throughout S1 as Iranian, and S2 addresses "the Government of Iran" directly as the entity whose property is blocked in response.`
  - S1: `Washington, November 4, 1979` → **1979-11-04** (form1)
  - S2: `November 14, 1979` → **1979-11-14** (form1)
- earliest cited document: **1979-11-04**

### `iran_hostage_crisis_1979` · 1979-11-04 · `target` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1979-11-04** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1979-11-04** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — target — per the existing `event_entities` rows; the U.S. Embassy and its personnel are the object of the action in S1, and S2 is a U.S. government emergency response protecting U.S. national security and economic interests.`
  - S1: `Washington, November 4, 1979` → **1979-11-04** (form1)
  - S2: `November 14, 1979` → **1979-11-14** (form1)
- earliest cited document: **1979-11-04**

### `iran_hostage_crisis_1979` · 1979-11-04 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1979-11-04** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1979-11-04** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: earliest 1979-11-04
  - dyad member `country.usa`: earliest 1979-11-04

### `carter_doctrine_1980` · 1980-01-23 · `actor` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1980-01-23** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1980-01-23** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — actor — the United States is the party making the commitment, per S1/S2 (matches the existing `event_entities` row).`
  - S1: `January 23, 1980, House Chamber, U.S. Capitol, Washington, D.C.` → **1980-01-23** (form1)
  - S2: `undated editorial note, positioned in the volume's record of events following January 23, 1980` → **None** (unparseable token 'undated')
- earliest cited document: **1980-01-23**

### `carter_doctrine_1980` · 1980-01-23 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1980-01-23** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — currently coded as `target` in `event_entities`, but no source retrieved this session names Iran as the object of the doctrine. S1 and S2 both identify the threat addressed as an "outside force" seeking to control the Gulf — read in context (Soviet invasion of Afghanistan, immedia`
- **not derived:** (e.2 iv) negation phrase present: 'no source retrieved'

### `iran_iraq_war_1980` · 1980-09-22 · `actor` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1980-11-05** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1980-09-22** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — actor — "war between Iran and Iraq commenced with ... attacks on Iranian territory by Iraqi forces" [S1]; "Iraq ... launched a war against the country" [S2]. Matches the existing `event_entities` row.`
  - S1: `Washington, November 5, 1980` → **1980-11-05** (form1)
  - S2: `February 2011` → **2011-02-28** (form3 (end of month))
- earliest cited document: **1980-11-05**

### `iran_iraq_war_1980` · 1980-09-22 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1980-11-05** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1980-09-22** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — the state whose territory was attacked, per both S1 and S2. Matches the existing `event_entities` row.`
  - S1: `Washington, November 5, 1980` → **1980-11-05** (form1)
  - S2: `February 2011` → **2011-02-28** (form3 (end of month))
- earliest cited document: **1980-11-05**

### `iran_iraq_war_1980` · 1980-09-22 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1980-11-05** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1980-09-22** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: earliest 1980-11-05
  - dyad member `country.iraq`: earliest 1980-11-05

### `tanker_war_1984` · 1984-03-27 · `actor` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1984-07-31** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1984-03-27** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — actor — the attacking party per S1 and S2. Matches the existing `event_entities` row.`
  - S1: `May 1990` → **1990-05-31** (form3 (end of month))
  - S2: `July 1984` → **1984-07-31** (form3 (end of month))
- earliest cited document: **1984-07-31**

### `tanker_war_1984` · 1984-03-27 · `target` = `chokepoint.hormuz`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1984-03-27** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `chokepoint.hormuz` — currently coded as `target` in `event_entities`. No source retrieved this session supports this: the attack was on two tankers "southwest of Kharg," inside the Gulf and well north of the Strait of Hormuz itself, and neither S1 nor S2 mentions Hormuz. This dossier flags `choke`
- **not derived:** (e.2 iv) negation phrase present: 'no source retrieved'

### `tanker_war_1984` · 1984-03-27 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1984-03-27** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `chokepoint.hormuz`: (e.2 iv) negation phrase present: 'no source retrieved'
  - dyad member `country.iraq`: earliest 1984-07-31
- **not derived:** (e.3) a dyad member has no receipt -- chokepoint.hormuz: (e.2 iv) negation phrase present: 'no source retrieved'

### `tanker_war_1984` · 1984-03-27 · `asset_role` = `chokepoint`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1984-03-27** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `chokepoint.hormuz` — currently coded as `target` in `event_entities`. No source retrieved this session supports this: the attack was on two tankers "southwest of Kharg," inside the Gulf and well north of the Strait of Hormuz itself, and neither S1 nor S2 mentions Hormuz. This dossier flags `choke`
- **not derived:** (e.4) no chokepoint entity ['chokepoint.hormuz'] has a receipt: (e.2 iv) negation phrase present: 'no source retrieved'

### `kharg_strikes_1985` · 1985-08-15 · `actor` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1990-05-31** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1985-08-15** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — actor — the attacking party per S1. Matches the existing `event_entities` row.`
  - S1: `May 1990` → **1990-05-31** (form3 (end of month))
- earliest cited document: **1990-05-31**

### `kharg_strikes_1985` · 1985-08-15 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1990-05-31** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1985-08-15** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — Kharg Island is Iran's terminal, and Iran built the Sirri Shuttle specifically in response to the ongoing threat to Kharg [S1]. Matches the existing `event_entities` row.`
  - S1: `May 1990` → **1990-05-31** (form3 (end of month))
- earliest cited document: **1990-05-31**

### `kharg_strikes_1985` · 1985-08-15 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1990-05-31** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1985-08-15** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: earliest 1990-05-31
  - dyad member `country.iraq`: earliest 1990-05-31

### `opec_price_collapse_1986` · 1986-01-01 · `actor` = `country.saudi_arabia`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2015-05-31** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1985-12-10** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.saudi_arabia` — actor — Saudi Arabia, via Minister Yamani, is the party making the policy shift in both S1 and S4. Matches part of the existing `event_entities` row.`
  - S1: `May 2015` → **2015-05-31** (form3 (end of month))
  - S4: `May 8, 2020 (updated July 16, 2020)` → **2020-07-16** (form1)
- earliest cited document: **2015-05-31**

### `opec_price_collapse_1986` · 1986-01-01 · `target` = `country.saudi_arabia`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1985-12-10** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.saudi_arabia` as `target` (current coding) — not supported by any source retrieved this session; Saudi Arabia is the actor here, not a target of an outside action. Recommend removing the `target` role unless a source is found to justify it.`
- **not derived:** (e.2 iii) the bullet cites no source marker

### `iraq_kharg_1986` · 1986-08-12 · `actor` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1986-11-26** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1986-08-12** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — actor — the attacking party, per S1 ("Iraqi jets," in the context of Sirri and the companion Larak raid) and consistent with S2's account of Iraqi Exocet campaigns against Iran's export shuttle. Matches the existing `event_entities` row.`
  - S1: `November 26, 1986` → **1986-11-26** (form1)
  - S2: `May 1990` → **1990-05-31** (form3 (end of month))
- earliest cited document: **1986-11-26**

### `iraq_kharg_1986` · 1986-08-12 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1986-11-26** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1986-08-12** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — Sirri Island was Iran's alternate export terminal, per S1 and S2. Matches the existing `event_entities` row.`
  - S1: `November 26, 1986` → **1986-11-26** (form1)
  - S2: `May 1990` → **1990-05-31** (form3 (end of month))
- earliest cited document: **1986-11-26**

### `iraq_kharg_1986` · 1986-08-12 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1986-11-26** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1986-08-12** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: earliest 1986-11-26
  - dyad member `country.iraq`: earliest 1986-11-26

### `earnest_will_1987` · 1987-07-22 · `actor` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1987-07-22** (e.2:dossier_doc_date)
- dossier bullet, verbatim: `- `country.usa` — actor — confirmed: the U.S. Navy conducted the escort at presidential authorization [S1][S2]. Matches existing coding.`
  - S1: `May 29, 1987, Washington` → **1987-05-29** (form1)
  - S2: `filed July 22, 1987, dateline "Aboard the USS Fox in the Gulf of Oman"` → **1987-07-22** (form1)
- earliest cited document: **1987-05-29** (before the event date; clamped to it by (e.6))

### `earnest_will_1987` · 1987-07-22 · `target` = `chokepoint.hormuz`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- dossier bullet, verbatim: `- `chokepoint.hormuz` — currently coded `target` in `event_entities`. This dossier proposes reclassifying to `location`: nothing was attacking or threatening to seize the Strait of Hormuz on this date; the convoy transited it. "Target" does not fit any of the codebook's four defined roles (actor/tar`
- **not derived:** (e.2 iv) negation phrase present: 'proposes reclassifying'

### `earnest_will_1987` · 1987-07-22 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
  - dyad member `chokepoint.hormuz`: (e.2 iv) negation phrase present: 'proposes reclassifying'
  - dyad member `country.usa`: earliest 1987-05-29
- **not derived:** (e.3) a dyad member has no receipt -- chokepoint.hormuz: (e.2 iv) negation phrase present: 'proposes reclassifying'

### `earnest_will_1987` · 1987-07-22 · `asset_role` = `chokepoint`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- dossier bullet, verbatim: `- `chokepoint.hormuz` — currently coded `target` in `event_entities`. This dossier proposes reclassifying to `location`: nothing was attacking or threatening to seize the Strait of Hormuz on this date; the convoy transited it. "Target" does not fit any of the codebook's four defined roles (actor/tar`
- **not derived:** (e.4) no chokepoint entity ['chokepoint.hormuz'] has a receipt: (e.2 iv) negation phrase present: 'proposes reclassifying'

### `bridgeton_mine_strike_1987` · 1987-07-24 · `actor` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1987-07-24** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1987-07-24** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — coded `actor`. Supported only as a strong circumstantial attribution in both sources ("clearly point the finger to Iran" [S2]; Seitz's account that Farsi Island-based Iranians had "a very high chance of hitting us" [S1]) — not a confirmed claim of responsibility by Iran itself. Th`
  - S1: `May 1988, Vol. 114/5/1,023 (interview conducted "recently" before publication, i.e. roughly 10 months after the event)` → **1988-05-31** (form3 (end of month))
  - S2: `filed July 24, 1987, dateline "Aboard the USS Kidd in the Persian Gulf"` → **1987-07-24** (form1)
- earliest cited document: **1987-07-24**

### `bridgeton_mine_strike_1987` · 1987-07-24 · `target` = `chokepoint.hormuz`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1987-07-24** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `chokepoint.hormuz` — coded `location`. This dossier flags a geographic precision concern rather than proposing a change: the mine strike occurred near Farsi Island, roughly 120 miles southeast of Kuwait and well inside the Gulf proper [S2] — not at the Strait of Hormuz itself, which lies at the G`
- **not derived:** (e.2 iv) negation phrase present: 'gap'

### `bridgeton_mine_strike_1987` · 1987-07-24 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1987-07-24** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `chokepoint.hormuz`: (e.2 iv) negation phrase present: 'gap'
  - dyad member `country.iran`: earliest 1987-07-24
- **not derived:** (e.3) a dyad member has no receipt -- chokepoint.hormuz: (e.2 iv) negation phrase present: 'gap'

### `bridgeton_mine_strike_1987` · 1987-07-24 · `asset_role` = `chokepoint`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1987-07-24** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `chokepoint.hormuz` — coded `location`. This dossier flags a geographic precision concern rather than proposing a change: the mine strike occurred near Farsi Island, roughly 120 miles southeast of Kuwait and well inside the Gulf proper [S2] — not at the Strait of Hormuz itself, which lies at the G`
- **not derived:** (e.4) no chokepoint entity ['chokepoint.hormuz'] has a receipt: (e.2 iv) negation phrase present: 'gap'

### `praying_mantis_1988` · 1988-04-18 · `actor` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1988-04-19** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1988-04-18** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — actor — confirmed [S1].`
  - S1: `April 19, 1988` → **1988-04-19** (form1)
- earliest cited document: **1988-04-19**

### `praying_mantis_1988` · 1988-04-18 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1988-04-19** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1988-04-18** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — confirmed; platforms and naval vessels were the objects of the U.S. strike [S1][S2].`
  - S1: `April 19, 1988` → **1988-04-19** (form1)
  - S2: `published November 11, 2003` → **2003-11-11** (form1)
- earliest cited document: **1988-04-19**

### `praying_mantis_1988` · 1988-04-18 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1988-04-19** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1988-04-18** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: earliest 1988-04-19
  - dyad member `country.usa`: earliest 1988-04-19

### `iran_air_655_1988` · 1988-07-03 · `actor` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1988-07-03** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1988-07-03** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — actor — confirmed [S1][S3].`
  - S1: `July 3, 1988` → **1988-07-03** (form1)
  - S3: `July 4, 1988` → **1988-07-04** (form1)
- earliest cited document: **1988-07-03**

### `iran_air_655_1988` · 1988-07-03 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1988-07-03** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — coded `target`. This dossier flags the role as only loosely fitting: the aircraft and its passengers, not the Iranian state, were the immediate object of Vincennes's fire, and both S1 and S3 characterize the shootdown as a defensive misidentification during an engagement with Iran`
- **not derived:** (e.2 iv) negation phrase present: 'flags the role'

### `iran_air_655_1988` · 1988-07-03 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **2026-09-02** (c:coding_date(corpus-derived))
- the dossier's own `## Knowable at` asserts **1988-07-03** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: (e.2 iv) negation phrase present: 'flags the role'
  - dyad member `country.usa`: earliest 1988-07-03
- **not derived:** (e.3) a dyad member has no receipt -- country.iran: (e.2 iv) negation phrase present: 'flags the role'

### `iran_iraq_ceasefire_1988` · 1988-08-20 · `actor` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1988-08-20** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — coded `actor`; `country.iraq` — coded `target`. This dossier flags the pairing as an imperfect fit: a mutual, UN-brokered ceasefire is not a unilateral action by one country against another, and "target" implies an adversarial object of action that neither retrieved source support`
  - S1: `undated official mission-history page, describing events of August 1988` → **None** (unparseable token 'undated')
- **not derived:** (e.2) no cited source has a parseable Doc. date

### `iran_iraq_ceasefire_1988` · 1988-08-20 · `target` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1988-08-20** (an inference; rule (e.7) uses the document, not the assertion)
- **not derived:** (e.2 i) no bullet in the dossier names this entity_id

### `iraq_invades_kuwait_1990` · 1990-08-02 · `actor` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1990-08-02** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1990-08-02** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — actor — Iraq is named as the invading party in both S1 ("Iraqi military invasion of Kuwait") and S2 ("Iraq invaded and occupied Kuwait").`
  - S1: `August 2, 1990` → **1990-08-02** (form1)
  - S2: `undated official mission-history page, describing events from August 1990` → **None** (unparseable token 'undated')
- earliest cited document: **1990-08-02**

### `iraq_invades_kuwait_1990` · 1990-08-02 · `target` = `country.kuwait`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1990-08-02** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1990-08-02** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.kuwait` — target — Kuwait is named as the invaded and occupied state in S2, and as the state whose assets Bush froze "to ensure that those assets are not interfered with by the illegitimate authority that is now occupying Kuwait" [S1].`
  - S1: `August 2, 1990` → **1990-08-02** (form1)
  - S2: `undated official mission-history page, describing events from August 1990` → **None** (unparseable token 'undated')
- earliest cited document: **1990-08-02**

### `iraq_invades_kuwait_1990` · 1990-08-02 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1990-08-02** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1990-08-02** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iraq`: earliest 1990-08-02
  - dyad member `country.kuwait`: earliest 1990-08-02

### `iraq_un_661_embargo_1990` · 1990-08-06 · `target` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1990-08-09** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1990-08-06** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — target — corroborated as the object of the embargo in [S1] ("Prohibiting Transactions With Iraq") and [S2] ("originating in Iraq or Kuwait").`
  - S1: `August 9, 1990` → **1990-08-09** (form1)
  - S2: `case study text, undated; resolution quoted is dated August 6, 1990` → **None** (unparseable token 'undated')
- earliest cited document: **1990-08-09**

### `iraq_un_661_embargo_1990` · 1990-08-06 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1990-08-09** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1990-08-06** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iraq`: earliest 1990-08-09

### `desert_storm_air_campaign_1991` · 1991-01-17 · `actor` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1991-01-17** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1991-01-16** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — actor — confirmed: Bush states the attack was launched by "allied air forces" under U.S. presidential authority and with "the consent of the United States Congress" [S1].`
  - S1: `January 16, 1991, 9:01 p.m.` → **1991-01-16** (form1)
- earliest cited document: **1991-01-16** (before the event date; clamped to it by (e.6))

### `desert_storm_air_campaign_1991` · 1991-01-17 · `target` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1991-01-17** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1991-01-16** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — target — confirmed: "attack on military targets in Iraq" [S1].`
  - S1: `January 16, 1991, 9:01 p.m.` → **1991-01-16** (form1)
- earliest cited document: **1991-01-16** (before the event date; clamped to it by (e.6))

### `desert_storm_air_campaign_1991` · 1991-01-17 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1991-01-17** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1991-01-16** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iraq`: earliest 1991-01-16
  - dyad member `country.usa`: earliest 1991-01-16

### `kuwait_oil_fires_1991` · 1991-02-22 · `actor` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1991-02-22** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1991-02-22** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — actor — matches current coding; supported by [S1] ("Saddam has now launched...He is wantonly setting fires").`
  - S1: `February 22, 1991, 10:43 a.m.` → **1991-02-22** (form1)
- earliest cited document: **1991-02-22**

### `kuwait_oil_fires_1991` · 1991-02-22 · `target` = `country.kuwait`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1991-02-22** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1991-02-22** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.kuwait` — target — matches current coding; supported by [S1] ("against Kuwait") and [S2] (Kuwait's wells).`
  - S1: `February 22, 1991, 10:43 a.m.` → **1991-02-22** (form1)
  - S2: `originally published November 1998; this version "Last Update: August 2, 2000" (retrospective, not contemporaneous)` → **2000-08-02** (form1)
- earliest cited document: **1991-02-22**

### `kuwait_oil_fires_1991` · 1991-02-22 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1991-02-22** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1991-02-22** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iraq`: earliest 1991-02-22
  - dyad member `country.kuwait`: earliest 1991-02-22

### `iraq_un_986_ofp_1995` · 1995-04-14 · `target` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1995-04-14** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1995-04-14** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — coded `target` in `event_entities`. Supported: Iraq is the subject of the sanctions-committee-monitored export authorization and the intended, though not immediate, beneficiary of the humanitarian mechanism [S1][S3].`
  - S1: `Adopted by the Security Council at its 3519th meeting, on 14 April 1995` → **1995-04-14** (form2)
  - S3: `undated CRS report (post-2003, reviewing 1991–2003 history)` → **None** (unparseable token 'undated')
- earliest cited document: **1995-04-14**

### `iraq_un_986_ofp_1995` · 1995-04-14 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1995-04-14** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1995-04-14** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iraq`: earliest 1995-04-14

### `iran_eo12959_embargo_1995` · 1995-05-06 · `target` = `country.iran`
- before: **1995-05-06** (a:url_date) → after: **1995-05-09** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1995-05-06** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — per existing `event_entities` rows; S1's Section 1 prohibitions run against "Iran," "the Government of Iran," and entities it owns or controls throughout.`
  - S1: `Signed May 6, 1995; published May 9, 1995` → **1995-05-09** (form1)
- earliest cited document: **1995-05-09**

### `iran_eo12959_embargo_1995` · 1995-05-06 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1995-05-09** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1995-05-06** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: earliest 1995-05-09

### `ilsa_sanctions_1996` · 1996-08-05 · `actor` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1996-08-05** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1996-08-05** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — actor — the President and Congress acting to impose the sanction regime; corroborated by [S1][S2][S3][S4].`
  - S1: `August 5, 1996` → **1996-08-05** (form1)
  - S2: `August 5, 1996` → **1996-08-05** (form1)
  - S3: `August 5, 1996, 9:42 a.m., Oval Office` → **1996-08-05** (form1)
  - S4: `August 6, 1996` → **1996-08-06** (form1)
- earliest cited document: **1996-08-05**

### `ilsa_sanctions_1996` · 1996-08-05 · `target` = `country.iran`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1996-08-05** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1996-08-05** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iran` — target — named as a covered country in the statute's thresholds [S1][S2][S4].`
  - S1: `August 5, 1996` → **1996-08-05** (form1)
  - S2: `August 5, 1996` → **1996-08-05** (form1)
  - S4: `August 6, 1996` → **1996-08-06** (form1)
- earliest cited document: **1996-08-05**

### `ilsa_sanctions_1996` · 1996-08-05 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1996-08-05** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1996-08-05** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iran`: earliest 1996-08-05
  - dyad member `country.libya`: earliest 1996-08-05
  - dyad member `country.usa`: earliest 1996-08-05

### `iraq_ofp_exports_begin_1996` · 1996-12-10 · `target` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1997-12-04** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1996-12-10** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — coded `target`, matching the existing assignment; supported by S1/S2/S3, which frame Iraq as the subject of the UN sanctions-and-oil-for-food regime whose implementation it "delayed... for a year and a half" [S2].`
  - S1: `4 December 1997` → **1997-12-04** (form2)
  - S2: `February 3, 1998` → **1998-02-03** (form1)
  - S3: `June 16, 2004` → **2004-06-16** (form1)
- earliest cited document: **1997-12-04**

### `iraq_ofp_exports_begin_1996` · 1996-12-10 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1997-12-04** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1996-12-10** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iraq`: earliest 1997-12-04

### `thai_baht_float_1997` · 1997-07-02 · `actor` = `country.thailand`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1997-11-30** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1997-07-02** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.thailand` — actor — per existing `event_entities` rows; both S1 and S4 identify "the Thai authorities" / "the BOT" as the actor abandoning the peg.`
  - S1: `Basle, November 1997` → **1997-11-30** (form3 (end of month))
  - S4: `c. 2022 (retrospective; event described occurred 1997)` → **None** (unparseable token 'c. <year>' (circa))
- earliest cited document: **1997-11-30**

### `korea_imf_bailout_1997` · 1997-11-21 · `actor` = `institution.imf`
- before: **1997-11-21** (a:url_date) → after: **1997-12-16** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1997-11-21** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `institution.imf` — actor — per existing `event_entities` rows; both S1 and S2 identify the IMF as the body running the rescue/support programme for Korea.`
  - S1: `Basle, February 1998` → **1998-02-28** (form3 (end of month))
  - S2: `December 16, 1997` → **1997-12-16** (form1)
- earliest cited document: **1997-12-16**

### `korea_imf_bailout_1997` · 1997-11-21 · `target` = `country.south_korea`
- before: **1997-11-21** (a:url_date) → after: **1997-12-16** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1997-11-21** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.south_korea` — location — per existing `event_entities` rows; consistent with both S1 and S2, which discuss Korea as the country in crisis and subject to the IMF program.`
  - S1: `Basle, February 1998` → **1998-02-28** (form3 (end of month))
  - S2: `December 16, 1997` → **1997-12-16** (form1)
- earliest cited document: **1997-12-16**

### `opec_jakarta_quota_increase_1997` · 1997-12-01 · `actor` = `institution.opec`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1998-12-31** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1997-12-01** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `institution.opec` — actor — [S1][S2] both describe a formal OPEC Conference of oil ministers deciding the quota change. Matches current coding.`
  - S1: `May 2009` → **2009-05-31** (form3 (end of month))
  - S2: `1998` → **1998-12-31** (form4 (end of year))
- earliest cited document: **1998-12-31**

### `opec_cut_march_1998` · 1998-03-30 · `actor` = `institution.opec`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1998-04-21** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1998-03-30** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `institution.opec` — actor — unchanged, well supported [S1].`
  - S1: `1998 (writing dated "at the time of writing (21 April 1998)" internally)` → **1998-04-21** (form2)
- earliest cited document: **1998-04-21**

### `opec_cut_june_1998` · 1998-06-24 · `actor` = `institution.opec`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **2026-09-02** (c:coding_date(undated url))
- the dossier's own `## Knowable at` asserts **1998-06-24** (an inference; rule (e.7) uses the document, not the assertion)
- **not derived:** (e.2 i) no bullet in the dossier names this entity_id

### `russia_default_ltcm_1998` · 1998-08-17 · `target` = `country.russia`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1998-11-30** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1998-08-17** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.russia` — per existing `event_entities` rows, coded `location`. Retrieved evidence (S1: "the decision by the Russian authorities... to float the rouble and declare a moratorium") indicates the Russian government was the acting party, not merely the location of the event — this dossier fla`
  - S1: `Basle, November 1998` → **1998-11-30** (form3 (end of month))
- earliest cited document: **1998-11-30**

### `operation_desert_fox_1998` · 1998-12-16 · `actor` = `country.usa`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1998-12-16** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1998-12-16** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.usa` — actor — per existing `event_entities` rows; S1 is the U.S. President's own order, and S2's U.S. representative defends the action as taken by "coalition forces."`
  - S1: `December 16, 1998` → **1998-12-16** (form1)
  - S2: `16 December 1998` → **1998-12-16** (form2)
- earliest cited document: **1998-12-16**

### `operation_desert_fox_1998` · 1998-12-16 · `target` = `country.iraq`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1998-12-16** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1998-12-16** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `country.iraq` — target — per existing `event_entities` rows; both S1 and S2 identify Iraq as the object of the strikes and the subject of the UNSCOM dispute.`
  - S1: `December 16, 1998` → **1998-12-16** (form1)
  - S2: `16 December 1998` → **1998-12-16** (form2)
- earliest cited document: **1998-12-16**

### `operation_desert_fox_1998` · 1998-12-16 · `tempo` = `nth`
- before: **2026-09-02** (c:coding_date(corpus-derived)) → after: **1998-12-16** (e.3:dossier_dyad_date)
- the dossier's own `## Knowable at` asserts **1998-12-16** (an inference; rule (e.7) uses the document, not the assertion)
  - dyad member `country.iraq`: earliest 1998-12-16
  - dyad member `country.usa`: earliest 1998-12-16

### `opec_cut_1999` · 1999-03-23 · `actor` = `institution.opec`
- before: **2026-09-02** (c:coding_date(undated url)) → after: **1999-03-24** (e.2:dossier_doc_date)
- the dossier's own `## Knowable at` asserts **1999-03-23** (an inference; rule (e.7) uses the document, not the assertion)
- dossier bullet, verbatim: `- `institution.opec` — actor — unchanged, well supported: [S1] states "the oil ministers of the 11 member states of ... OPEC ... voted."`
  - S1: `dateline Prague, 24 March 1999` → **1999-03-24** (form2)
- earliest cited document: **1999-03-24**
