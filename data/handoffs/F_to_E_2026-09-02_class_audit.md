# F → E, 2026-09-02 — CLASS_AUDIT.md carve-out, and eight record-quality items
*Supersedes the first version: the audit now covers all four geopolitical classes (187
events), and the second pass found four more record questions that are yours.*

## The carve-out
Joe's brief of 2026-09-02 gave Session F `data/spine/CLASS_AUDIT.md`, which sits inside your
`data/spine/**`, and — with his approval on the same day — the `hostility` field amendment in
`EVENTS_CODEBOOK.md`, which is otherwise entirely yours. Those two files are all F has
written in your trees. `data/spine/patches/**`, `AUDIT.md`, `audit.json`, `VERIFICATION.md`,
`PATCH_LOG.md`, `data/events*.csv` and `data/dossiers/**` are untouched, and F has written
nothing to the `events` table. SESSION_CHARTER §1 records the carve-out.

## What the audit is
All 187 events of the four geopolitical classes, coded `hostile` / `hostile_unattributed` /
`ambiguous` / `non_hostile` with the evidence per event. **151 hostile, 3
hostile-unattributed, 13 ambiguous, 20 non-hostile — 33 of 187 (18%) not G-scorable.**

## Eight things that are yours, not the target's
Record questions, not outcome questions. F raised them, coded around them, and changed
nothing. No patch is proposed — that is your call and Joe's.

**From the first pass:**
1. **`codelco_elteniente_2025` is a copper-mine collapse filed as `infrastructure_attack`.**
   Not an attack, and not oil.
2. **`iran_oilworkers_strike_1978` is a labour strike filed as `infrastructure_attack`.**
   Nothing was attacked. It carries IES-90 **level 3, war**, and is retrieved as a precedent
   that way.
3. **Two rows bundle a hostile act with the response to it** —
   `saudi_suspends_bab_el_mandeb_2018` (Houthi attacks on two tankers **and** Riyadh's
   suspension, with Saudi Arabia as the coded actor) and `libya_jathran_blockade_2013`. The
   date rule wants one dated act per row; these hold two. `marikana_strike_2012` is a third
   (a wage strike **and** the police killing of 34 strikers).
4. **Both 1970s records in those two classes are non-hostile.** Across all four classes the
   1970s are 8 events of which 3 are not G-scorable — the thinnest decade and the worst.

**From the second pass:**
5. **Five China export-control rows name no counterparty, two do.** `chn_gage_2023`,
   `chn_graphite_2023`, `chn_re_tech_2023`, `chn_antimony_2024`, `chn_re_magnets_2025` carry
   no target state in the description or the coded entities, while `chn_ban_us_2024` and
   `chn_5minerals_2025` do. The same programme is half coded as statecraft and half not, and
   that is the only reason five of them are `ambiguous`. **One record fix settles all five**:
   name the counterparty where the measure names one, or state on the row that the measure
   names none (MOFCOM's July 2023 statement gives "national security and interests" and no
   country — that is a fact worth carrying on the row).
6. **Two records materially understate their own event.** `kazakhstan_unrest_2022` reads
   "nationwide unrest over fuel prices"; the event killed 227 including 19 police, injured
   4,353, and drew a CSTO military deployment. `egypt_revolution_2011` reads "mass unrest
   threatening Suez transit"; it was a rising that removed a head of state, with roughly 850
   killed. Both are coded `hostile` on the wider record, but a coder working only from the
   description would not get there.
7. **Eight mining strikes and community blockades are filed as `conflict_escalation`** —
   `escondida_strike_2011/2017/2024`, `sa_platinum_strike_2014`, `lasbambas_blockade_2019`,
   `lasbambas_halt_2021`, `cuajone_shutdown_2022`, `peru_lasbambas_2022`. They belong in the
   corpus (they move metal prices) and in no existing class.
8. **Three producer price-management export bans are filed as `sanctions`** —
   `indonesia_nickel_ban_2019`, `indonesia_palm_ban_2022`, `drc_cobalt_ban_2025`. Each is
   functionally an `opec_decision`: a producer restricting its own output to move a price.
   `drc_cobalt_ban_2025` carries **IES-90 level 3, war**, the worst single case in the corpus.

Items 7 and 8 are class placements, not record errors, and CLASS_AUDIT §7.3 says explicitly
that the field already prevents the harm (neither group is G-scored under Amendment 3) and
that moving them is a separate registration affecting `p_class_given_big` and the analogue
retrieval. Nothing is moved.

## The codebook
`EVENTS_CODEBOOK.md` now carries the `hostility` field (amendment 2026-09-02, approved by
Joe): four values, five coding rules, the four tie-breaks, and an explicit statement that the
field is **not** a data-quality flag — `non-hostile` says the escalation question does not
apply, not that the event is doubtful. The `type` enum is unchanged at seven values and no
event's class, severity, entities or sources were altered. If you would rather that amendment
lived in your hand, say so in a handoff and F will not touch the file again.

— Session F
