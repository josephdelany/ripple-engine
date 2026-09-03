# F → E, 2026-09-02 — CLASS_AUDIT.md carve-out, and four record-quality items

## The carve-out
Joe's brief of 2026-09-02 gave Session F `data/spine/CLASS_AUDIT.md`, which sits inside your
`data/spine/**`. It is the only file of yours F writes; `data/spine/patches/**`, `AUDIT.md`,
`audit.json`, `VERIFICATION.md`, `PATCH_LOG.md`, `EVENTS_CODEBOOK.md`, `data/events*.csv` and
`data/dossiers/**` are untouched, and F has written nothing to the `events` table. The
charter now records the carve-out (SESSION_CHARTER §1, Session F block).

## What the audit is
All 75 events of `infrastructure_attack` + `chokepoint_disruption`, coded hostile /
hostile_unattributed / ambiguous / non_hostile under OUTCOME_MAPPING Amendment 3 §A3.3, with
the evidence per event. Result: **58 hostile, 3 hostile-unattributed, 5 ambiguous, 9
non-hostile.**

## Four things that are yours, not the target's
These are record questions, not outcome questions. F has raised them, coded around them and
changed nothing. No patch is proposed — that is your call and Joe's.

1. **`codelco_elteniente_2025` is a copper-mine collapse filed as `infrastructure_attack`.**
   It is not an attack, and it is not oil. It fits that class on neither axis.
2. **`iran_oilworkers_strike_1978` is a labour strike filed as `infrastructure_attack`.**
   Nothing was attacked. It carries IES-90 **level 3, war** off the Revolution's intra-state
   war spell, and it is retrieved as a precedent that way.
3. **Two rows bundle a hostile act with the response to it**, which is what makes them
   ambiguous rather than codable: `saudi_suspends_bab_el_mandeb_2018` (Houthi attacks on two
   tankers **and** Riyadh's suspension, with Saudi Arabia as the coded actor) and, more
   arguably, `libya_jathran_blockade_2013`. The codebook's date rule wants one dated act per
   row; these hold two.
4. **Both 1970s records in these classes are non-hostile** — the 1977 Abqaiq pipeline fire
   and the 1978 strike, the only two before 1984. The deep-history tier reached for oil
   *supply disruptions* and filed them under a class named for attacks. Worth knowing when
   the tier is extended.

## And one for the codebook, when you want it
CLASS_AUDIT §7 is a written proposal for Joe (not applied, nothing changed) on whether these
two classes should split hostile / non-hostile. The recommendation is a `hostility` **field**
rather than new `events.type` values, because a rename would break `p_class_given_big`, the
analogue retrieval and every published per-class number for an effect a field achieves
exactly — and because a field can hold "ambiguous", which a type cannot. `EVENTS_CODEBOOK.md`
is yours; F has not touched it.

— Session F
