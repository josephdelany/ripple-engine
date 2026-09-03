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
| `iran_iraq_ceasefire_1988` | 1988-08-20, day | **flagged, NOT proposed** — see correction below | The UN's own UNIIMOG history: the Secretary-General "announced the agreement of both Iran and Iraq to a ceasefire with effect from 0300 GMT on 20 August" on 8 August. The codebook's date rule is the first day the market could have known. Verified by the reviewer against the UN page. The dossier nevertheless writes "not changed here, but flagged", so no change was proposed and none was applied: the record still reads 1988-08-20. The decision is Joe's. |
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
(needed for the 1988 ceasefire). **`country.mexico`** is a fifth, added after the 1990s
pass: Mexico is a central sourced party to the March 1998 production agreement and has no
entity row. Correction to an earlier report: **`country.libya` does exist** — the reviewer
checked the table directly.

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

---

## Added after the decade essays (E-5), 2026-09-02

### For A (corpus tooling): a missing event the literature names

The Venezuelan general strike of December 2002 – January 2003 is **not in the corpus**.
Hamilton (NBER 16790, retrieved and read) records: "A general strike eliminated 2.1 mb/d of
oil production from Venezuela in December of 2002 and January of 2003", and adds that
"Kilian (2008) argued they should be included in the list of postwar oil shocks."

Executed check against `events`: no record exists. The episode survives in our data only
inside the *title* of another event, `opec_hike_jan_2003` — "OPEC raises quota 6.5% amid
Venezuela strike". A 2.1 mb/d supply loss that a leading authority argues belongs on the
list of postwar oil shocks is therefore visible in our corpus only as background to somebody
else's meeting.

This is a candidate for admission, not an admission: nothing enters `events` without Joe.
Session E has not built a dossier for it because it is not an existing record and the
session's scope is repairing records that exist. If Joe wants it, the same dossier standard
applies and the sourcing looks tractable.

Hamilton is careful not to overstate the case, which is worth quoting alongside it: "the
affected supply was a much smaller share of the global market than many of the other events
discussed here, and the disruptions had little apparent effect on global oil supplies."

### For B (the walk): two structural notes from the essays

**The largest price move of the 2000s has no event behind it, by the literature's own
account.** Hamilton on 2007–08: "Unlike many other historical oil shocks, there was no
dramatic geopolitical event associated with this." His explanation is field maturity and a
residual supplier declining to be residual — North Sea production down more than 2 mb/d by
end-2007, Cantarell down 1 mb/d between 2005 and 2008, Saudi production "850,000 barrels a
day lower in 2007 than it had been in 2005". None of that is a dated event, so an
event-keyed corpus cannot carry it. This is the same gap the Big Moves census measures from
the other side when it finds 35% of large Brent moves have no corpus event. Worth stating
plainly in the walk's limits section rather than leaving a reader to infer it.

**Sanctions programmes and the 35-day cluster rule.** The 2010s hold 21 sanctions records,
most of them designations, waivers and expiries inside long-running programmes against Iran,
Russia and Venezuela. The protocol's registered clustering rule treats reads within 35 days
as one cluster, which is the only thing preventing the engine from treating a tightening
programme as a sequence of independent draws. Whether 35 days is right for a sanctions
programme, as against a war or a hurricane, is a protocol question and yours. Session E
raises it, does not answer it.

### For Cowork: two sentences for the paper's data section

Both are computed and quotable: the corpus's class mix inverts across decades (18 of 43
records in the 2000s are OPEC decisions; `sanctions` is the largest class in the 2010s;
`policy_response` is the largest in the 2020s at 36 of 150), and the 2020s instruments —
notably the Russian oil price cap — have no class in the closed set at all.

— Session E

---

## Added 2026-09-02 after applying `pre1990_a`: the month-precision question, answered from the code

E's earlier note asked B what the walk does with a month-precision event on the daily tier.
**Answered by reading the code rather than waiting**, and the answer removes the concern:

- `Corpus.tier_of` (`src/engine/read.py:133`) is
  `return "daily" if pd.Timestamp(date) >= self.daily_start else "monthly"`. Tier is decided
  by the date alone.
- `self.daily_start` (`read.py:98`) is the first index of the daily price series, not a
  constant. Executed: `fred.DCOILBRENTEU` runs 1987-05-20 → 2026-08-25.
- **`date_precision` appears zero times in `src/walk.py` and `src/engine/`** (grep). The
  engine never reads the field.

So the ten records in `pre1990_a` (1973–1980) were already on the monthly tier and stay
there; changing `day` → `month` changed no tier assignment, no analog pool and no score.

**And no date moved at all.** There is no `event_date` row anywhere in `pre1990_a` — only
the `date_precision` label changed, on `iran_oilworkers_strike_1978` and
`iran_revolution_1979`. Their dates are still 1978-10-31 and 1979-02-11.

### A registrable v3 item for B, not something to fix now

The corpus carries a precision field the walk ignores, so **a month-precision event is
currently treated by the filtration as though its date were exact**. For
`iran_revolution_1979` the engine will treat 1979-02-11 as the knowable instant when the
evidence only supports "February 1979". The honest fix is to widen the filtration window to
the stated precision, which is a protocol change and B's to register. Flagged, not built.

### A measurement caveat on E's own scoreboard

`SPINE_REGISTRATION.md` §7 counts events with "a narrative ≥ 700 characters", and after
applying `pre1990_a` that count is **still 0**. That is correct and should not be explained
away: the 120–250 word narratives live in the dossiers, and what a patch writes into
`events.description` is a one-paragraph summary (the ten patched records now run 59–396
characters, median about 184). If the intention was for the corpus row itself to carry the
narrative, that is a further patch and a bigger `description` column of prose; if it was for
the dossier to hold it, §7's measure is counting the wrong artifact. E is not redefining the
measure to make it pass. Recorded for Joe.

— Session E
