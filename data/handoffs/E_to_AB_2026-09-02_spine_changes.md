# Handoff E → A and B, 2026-09-02: which pre-1990 records may move, and what moves with them

Session E has taken all nineteen pre-1990 records to the `SPINE_REGISTRATION.md` standard.
**Nothing has changed in `events`.** Every proposal sits in `data/spine/patches/pre1990_a.json`
and `pre1990_b.json`, unapplied, for Joe. This note is the advance warning: if he applies
them, analog pools and IES-90 labels move, and both of you own code that depends on them.

## For B (`src/engine/**`, `src/walk.py`, `data/walk_forward/**`)

**Three dates are proposed to change or lose precision.** Analog retrieval and the
filtration key on `event_date`, and IES-90 windows are `(d, d+90]`, so each of these moves
a label window:

| event | now | proposed | why |
|---|---|---|---|
| `iran_iraq_ceasefire_1988` | 1988-08-20, day | **1988-08-08**, day | The UN's own UNIIMOG history: the Secretary-General "announced the agreement of both Iran and Iraq to a ceasefire with effect from 0300 GMT on 20 August" on 8 August. The codebook's date rule is the first day the market could have known. Verified by the reviewer against the UN page. |
| `iran_oilworkers_strike_1978` | 1978-10-31, day | 1978-10, **month** | No retrieved source pins the day. |
| `iran_revolution_1979` | 1979-02-11, day | 1979-02, **month** | Same. FRUS Volume X, which would settle it, is unpublished ("Being Cleared") — checked. |
| `opec_price_collapse_1986` | 1986-01-01, day | **unresolved**, at least month | Two defensible anchors were found (Yamani at the Oxford Energy Seminar, September 1985; OPEC's 71st Conference, Vienna, 10–11 December 1985) and neither could be adjudicated from retrieved sources. Both fall in **1985**. Put to Joe rather than manufactured. |

If `date_precision` becomes `month` for any record, please say what the walk does with a
month-precision event on the daily tier. I could not find that rule written down, and it
decides whether these records stay in the pool, enter at month granularity, or drop out.
That is a question for you, not a change I should make.

**A structural note that may matter more than the dates.** Session E's researchers found
that all four Iran-only records — `iran_oilworkers_strike_1978`, `shah_leaves_iran_1979`,
`iran_revolution_1979`, and the 1977 Abqaiq fire — code the *same* entity as both `actor`
and `target`. A dyad cannot form from a single entity, so `OUTCOME_MAPPING` Amendment 2's
dyadic precedence cannot fire on them and they fall through to location basis. That is the
same defect the label audit reached from the other end. Recorded here, not fixed: the
entity rows are corpus data and the mapping is A's.

## For A (`src/state/**`, `OUTCOME_MAPPING.md`, corpus tooling)

**Four entities are missing from the register and were reported rather than invented:**
`country.syria` (a named co-actor in the 1973 war), `country.algeria` (named in the 1974
embargo lift), `institution.oapec` (the actual actor in the 1973 embargo — OAPEC is a
distinct body from OPEC, and `institution.opec` is not a substitute), and `institution.un`
(needed for the 1988 ceasefire). Correction to an earlier report: **`country.libya` does
exist** — the reviewer checked the table directly.

**Two class challenges affect IES-90 indirectly**, because class decides which events are
"geopolitical" for G-scoring: `iran_oilworkers_strike_1978` is filed as
`infrastructure_attack` though a labour strike is not a direct strike on infrastructure,
and `carter_doctrine_1980` and `iran_iraq_ceasefire_1988` are filed as `policy_response`
though neither is a market intervention. No class has been changed. The full set of gaps is
in `docs/spine/CODEBOOK_AMENDMENT_PROPOSED.md`, written as proposed text because the
canonical `EVENTS_CODEBOOK.md` lives in the parent repository, outside this repo's history.

**A live citation in the corpus is dead.** `praying_mantis_1988`'s `source_url` no longer
serves the article it cites (403 to the reviewer; a researcher reported it redirecting to
an unrelated 2004 article). A working replacement URL is in the dossier. Separately,
`iraq_invades_kuwait_1990` cites `digitallibrary.un.org`, which returns 403 to scripts
today.

**One record does not meet the codebook's own inclusion rule.** `abqaiq_arabian_1977`
returned zero sources after eleven documented retrieval routes. Criterion 2 says "No source
= not in the dataset". Its dossier proposes no field changes at all, because proposing any
value would mean inventing one. Whether it stays is Joe's call, and the honest options are
to source it from a subscription newspaper archive or to remove it.

## The corpus-wide finding you should both know about

`src/spine_audit.py` now measures encyclopaedia sourcing. **31 of 313 events cite Wikipedia
as their `source_url`, and all 31 have no other citable domain** — 1990s 4, 2000s 11,
2010s 5, 2020s 11, most of them OPEC decisions sourced to Wikipedia's "world oil market
chronology" pages. By the codebook's inclusion criterion 2 those records are not sourced.
This is the largest single sourcing defect in the corpus and it is not confined to the
historical tail.

— Session E
