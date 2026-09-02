# Handoff E → A, 2026-09-02: three defects in how the 1970–1989 tier entered `events`

Session E (the history spine) is rewriting the pre-1990 records to the SPINE_REGISTRATION
standard. Before proposing any patch I traced how those rows got into the database. Three
things are wrong at the loader level, not at the record level, so patching the records
alone would leave the defects in place and the next load would reintroduce them.

`src/load_deep_history.py` and `data/deep_history_1970_1989.json` are corpus tooling and
therefore yours (charter §1). Session E has changed nothing in either file. Everything
below is executed, not read.

## 1. `date_precision` is hardcoded to `day` for every deep-history event

`src/load_deep_history.py`, in `run()`, inserts:

```
(e["event_id"], e["event_date"], "day", e["type"], e["title"], ...)
```

The seed JSON carries no `date_precision` field at all, so every one of its 18 events is
stamped `day` whatever the evidence supports. The codebook is explicit: *"`day` (exact) ·
`week` (known to the week) · `month` (only the month is known). Be honest — imprecision is
fine, false precision is not."*

The clearest casualty is `opec_price_collapse_1986`, dated **1986-01-01** with `day`
precision. New Year's Day is not a decision date; the shift it names is OPEC's move to a
market-share strategy, which the literature places in late 1985, and the collapse itself
ran through 1986. Hamilton (NBER w16790, retrieved and quoted in Session E's dossiers)
describes it as a process, not a day: *"The Saudis abandoned those efforts, beginning to
ramp production back up in 1986, causing the price of oil to collapse from $27/barrel in
1985 to $12/barrel at the low point in 1986."*

`tanker_war_1984` (1984-03-27) has the same shape: a multi-year campaign given a single
day. Session E's dossiers propose per-event precision from the evidence; the loader needs
to stop overriding it.

**Ask:** let the seed carry `date_precision` per event and have the loader use it,
defaulting to `month` rather than `day` when the seed is silent. A default of `day` makes
the false claim; a default of `month` makes the weaker true one.

## 2. Every description is generated, not written

The same insert builds the description as:

```
e["title"] + " [deep-history tier 1970-1989; events-only]"
```

That is why the spine audit finds these 17 rows with a median description of 85–94
characters and the scaffolding string still in the text. It is honest scaffolding — it
says what it is — but it means the historical tier carries no case narrative at all.
Session E is writing 120–250 word sourced narratives for them; when a patch lands, the
loader must not regenerate the stub over it.

**Ask:** have the loader write `e.get("description")` when the seed provides one, and only
fall back to the generated stub when it does not.

## 3. The loader cannot update, so a patch cannot be applied by re-running it

Both the events insert and the entity insert are `INSERT OR IGNORE`, and the `sr_json`
write is built from the seed each run. For a row that already exists, re-running
`load_deep_history.py` after editing the seed changes nothing at all. So the repair path
for these 17 rows is **not** "edit the seed and reload", and it is not the
`apply_review.py` + `load_events.py` path either, because — executed check —
`data/events.csv` holds 296 rows of which only **2** are pre-1990
(`bridgeton_mine_strike_1987`, `praying_mantis_1988`). The other 17 exist only in the
database and the seed JSON.

**Ask:** decide with Joe which is canonical for this tier. Session E's patches are written
as proposals (`data/spine/patches/<batch>.json`, built read-only by `src/spine_patch.py`)
precisely so that whoever owns the apply path can apply them; Session E will not write to
`events`.

## 4. A related provenance note (no action for you)

The seed's `_meta` names its anchor sources as *"Hamilton 2011, NBER w16790, Historical Oil
Shocks"* and *"EIA, U.S. Energy Information Administration energy chronology"*. Session E
tested the second on 2026-09-02: the EIA chronology page is gone, and the weekly petroleum
page that survives carries no timeline. That is the origin of the 9 corpus events whose
`source_url` is the bare root `https://www.eia.gov` — the document they were meant to cite
no longer exists. Those 9 are being re-sourced to retrievable documents by Session E, and
`SPINE_REGISTRATION.md` §4 records the route as unusable so nothing cites it again.

Separately, `data/events.csv` sources `iraq_invades_kuwait_1990` to
`https://digitallibrary.un.org/record/94220`; the UN Digital Library returns HTTP 403 to
scripts today, so that citation is currently unretrievable too. Flagged, not touched — it
is a 1990s record and Session E reaches it in step E-4.

— Session E
