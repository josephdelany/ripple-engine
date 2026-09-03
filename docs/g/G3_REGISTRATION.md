# G-3 REGISTRATION — deriving `knowable_at` for the five source-coded situation fields from dossier document dates
*2026-09-03, Session G. Registered BEFORE the derivation is computed and BEFORE
`src/situation_vintage.py` is written (charter §2 rule 2). Nothing in this document
writes to `events`, `situation_state` or `data/events.csv` (SPINE_REGISTRATION §5);
nothing here re-judges any run. Amendments are dated and appended, never edited.*

## 0. What was read before this was written, and what was not

This registration could not be written without seeing the *shape* of the inputs, so the
following were opened first and are named here so the sequence is checkable:

- `src/state/situation_state.py` (session A's) — the `knowable_at()` function, its rules
  (a)–(d), and the join that publishes `data/state/situation_knowable.json`.
- `src/situation_record.py` — how each of the five fields is actually computed.
- `src/engine/read.py:104–128` (`_apply_knowable`) and `src/engine/similarity.py:88–90`
  — what the engine does with the five fields.
- `data/dossiers/*.md` — the **column layout** of the `## Sources` tables, the free-text
  form of the `Doc. date` cells, and the bullet form of the `## Entities` sections. The
  date strings and the entity bullets were read, because a parser cannot be specified for
  text nobody has looked at.
- `data/state/situation_knowable.json` — the **published starting position**, which is the
  baseline this work is measured against and is already in the tree: 313 events, 786
  situation values, **60 kept**, **726 dropped after t**, 0 unknown, 262 events with no
  situation field at t; rules `a:url_date` 76, `c:coding_date(undated url)` 297,
  `c:coding_date(corpus-derived)` 413.

**Not opened before this registration:** no count of how many fields the rule below would
recover was computed, printed or estimated. The before/after table in §7 is produced by
the code, after this file is committed.

## 1. The object

`WORLD_STATE_FRAMEWORK.md` Amendment A (session A) gives every situation field a
`knowable_at` by four rules: (a) a date read out of the cited URL's path; (b)
`corpus:observed` → window close; (c) corpus-derived or an undated URL → the **coding
date**; (d) null source → `unknown`. Amendment A rule 3 states the consequence in advance:
rule (c) dates almost every field to the 2026-09-02 coding run, so almost every field
vanishes at t. `WALK_FORWARD_PROTOCOL.md` Amendment H binds the engine to those dates for
exactly five fields:

    KNOWABLE_FIELDS = (actor, target, conflict_scope, tempo, asset_role)     read.py:109

Amendment A rule 3 also names the remedy — "a per-field contemporaneous source with its own
date (rule (a))" — and calls it coding work rather than a code change. **Session E's 35
dossiers and Session G's 6 are that coding work**, already done and already in the tree:
each carries a `## Sources` table with a transcribed document date and a `## Entities`
section naming each entity, its role, and which source names it, gated by
`SPINE_REGISTRATION.md` §1(a) and §1(d). This registration fixes how a document date in
that table becomes a `knowable_at`, before the mapping is run.

## 2. How each of the five fields is actually computed (read from the code, not from memory)

From `src/situation_record.py`:

| field | how it is coded | information horizon |
|---|---|---|
| `actor` | `sorted(A)[0]` where `A` = this event's `event_entities` rows with role `actor` (`_parties`) | this event only |
| `target` | `sorted(T)[0]` where `T` = role `target`, **falling back to role `location`** when no `target` row exists (`_parties`) | this event only |
| `asset_role` | `chokepoint` iff any entity id starts `chokepoint.`, **else** `chokepoint` iff `type == chokepoint_disruption`, else `unknown` (`_asset_role`) | this event only |
| `tempo` | `nth` iff some prior geopolitical event **strictly before** this event's date shares an entity with `A ∪ T`, else `first` | this event + strictly prior events |
| `conflict_scope` | `isolated`/`campaign`/`war` from the count of same-dyad geopolitical events with **`abs(days) <= 120`** (`_conflict_scope`) | **this event ± 120 days** |

Two of these are settled by the record of the event itself (`actor`, `target`,
`asset_role`); one is settled by the event plus the past (`tempo`); one reads 120 days into
the **future** (`conflict_scope`). The rules below follow that split and nothing else.

## 3. Rule (e) — the dossier document date (proposed; only session A can adopt it)

This is written as a proposed **rule (e)** for `WORLD_STATE_FRAMEWORK.md` Amendment A.
`WORLD_STATE_FRAMEWORK.md` is session A's document and Session G does not edit it. Until A
adopts rule (e), `situation_state` is unchanged and this work is a **computed proposal plus
a handoff**, exactly as Session E's dossiers are proposals until Joe admits them.

**(e.0) Scope.** Rule (e) applies to a situation field of an event that has a dossier at
`data/dossiers/<event_id>.md` and a row in `events`. Where it does not apply, the field
keeps the date Amendment A gives it. Rule (e) takes precedence over rules (a), (c) and (d)
where it applies, **in both directions** — if the document date is later than the URL-path
date of rule (a), the later date stands and the loss is published. A rule that could only
ever move a date earlier would not be a measurement.

**(e.1) Parsing a `Doc. date` cell.** The cell is free text ("Washington, October 7, 1973,
6:06–7:06 p.m."; "February 2011"; "n/a (compiled)"). Exactly four forms are recognised, and
nothing else:

1. `Month D, YYYY` — e.g. "October 7, 1973", "filed July 24, 1987";
2. `D Month YYYY` — e.g. "4 December 1997";
3. `Month YYYY` — e.g. "February 2011" → the **last day** of that month;
4. `YYYY` alone → **31 December** of that year.

Forms 3 and 4 resolve late because a cell that names only a month or a year does not
establish anything earlier than its end. **Within one cell, the LATEST parseable date is
taken** — a cell reading "Signed May 6, 1995; published May 9, 1995" is established as a
whole only on 9 May. A cell containing any of the tokens `n/a`, `undated`, `c.`,
`archival description`, `case study text` is **not parsed at all**, even where it also
contains a year. No date is ever read out of the URL under rule (e); that is rule (a)'s
job and the two stay separate, so their disagreements are visible.

**(e.2) The receipt for `actor` and `target`.** A field's coded value is an `entity_id`.
The receipt is a bullet in the dossier's `## Entities` section, and all four clauses must
hold:

  i.   the bullet's leading backticked token is **exactly** the coded `entity_id`;
  ii.  the role word matches within the bullet's first 160 characters — `actor` for the
       `actor` field; `target` for `target`, **or** `location` where the DB's own
       `event_entities` gave no `target` row (matching `_parties`' fallback);
  iii. the bullet cites at least one source marker, `[Sn]` or a bare `Sn` (`n` a digit run,
       optionally followed by a letter, as in `S1b`);
  iv.  the bullet contains **none** of the registered negation phrases of (e.5).

Then `knowable_at = max(event_date, min{ doc_date(S) : S cited in the bullet and its cell
parses })`. If no cited source's cell parses, there is no receipt and the field keeps its
Amendment A date.

**(e.3) The receipt for `tempo`.** `tempo` is settled by this event's dyad plus strictly
prior corpus events. Prior corpus events are knowable at their own `event_date`, which is
strictly earlier, so they never bind. The receipt is therefore the dyad: **every** entity
in `A ∪ T` (as `_parties` builds it from `event_entities`) must satisfy (e.2) i, iii and
iv, with any role. Then `knowable_at = max(event_date, max over dyad members of that
member's min doc_date)` — the whole dyad must be known before `first`/`nth` can be
evaluated, so the dyad's *latest* member governs. If any dyad member has no receipt, there
is no derivation.

**Limitation, stated with the rule:** `tempo` is corpus-relative. "first" means first in
this corpus, not first in the world, and the corpus is a sample. Rule (e) dates the field;
it does not repair the sample, and no claim about the world's first clash is made from it.

**(e.4) The receipt for `asset_role`.** The value is `chokepoint` or `unknown`. A receipt
exists **only** where the event's own `event_entities` carries a `chokepoint.*` entity and
that entity has a bullet satisfying (e.2) i, iii and iv. Where the value rests on the class
alone (`type == chokepoint_disruption`, no chokepoint entity), **there is no receipt** and
the field keeps its Amendment A date: the class is a coding decision about the event, not a
document about the asset, and rule (e) will not manufacture one.

**(e.5) The negation list (closed).** A bullet matching any of these, case-insensitively,
is rejected and its field keeps its Amendment A date:

    not confirmed · no source retrieved · not independently confirmed · does not propose ·
    not proposing · proposed addition · proposes reclassifying · missing, not invented ·
    gap · not named · no source · cannot be confirmed · not usable · never opened ·
    not asserted · flags the role · not confirmed by any source

The list runs **only in the direction of exclusion**: a phrase on it loses coverage and can
never invent it. The residual risk is the opposite — a bullet expressing doubt in words not
on this list would be admitted — and §6 exists to expose exactly that.

**(e.6) The clamp.** `knowable_at` is never earlier than `event_date`. A field describing an
event cannot be knowable before the event exists; `WALK_FORWARD_PROTOCOL.md` §1 already
takes `event_date` as the event's first knowability. A dossier may cite a document dated
before the event (background, or the prior state of the dyad); such a document cannot
establish who acted on the day, so it sets the floor and not the date.

**(e.7) The direction of the bound, stated.** A document dated D proves the fact was known
**by** D. It is an upper bound on knowability, not the knowability date itself. Rule (e)
uses the upper bound as the date. That is the conservative direction: it hides a field for
longer than the truth, never shorter. Where a dossier's own `## Knowable at` section asserts
an earlier date than any document it cites — `yom_kippur_war_1973` asserts 1973-10-06 and
its earliest document is dated 1973-10-07 — **rule (e) does not use the assertion.** The
assertion is a historian's inference; the document is the receipt. Both are published in
§6 so the size of the gap between them is visible.

## 4. `conflict_scope` — a correction, not a recovery

`_conflict_scope` counts same-dyad events with `abs(days) <= 120`. **Half of its input
postdates t.** No document date can make it knowable at t, and no dossier is asked to:

> **Rule (e.8).** `conflict_scope.knowable_at = event_date + 120 days`, for **every**
> event in the corpus, dossier or not. This replaces rule (c)'s coding date with the
> field's own information horizon.

Three things follow and are registered before the count:

1. `conflict_scope` **cannot be a target-side feature of any read, ever**, at any level of
   sourcing. It is available only as an analog-side feature, and only 120 days after the
   analog's own date.
2. The correction **cannot increase** the number of fields kept at t: `event_date + 120 >
   event_date` always. It moves values from "dropped, reason: coding date" to "dropped,
   reason: forward window". It is reported in its own row of §7 and is never added to the
   coverage gain.
3. `events.sr_conflict_scope` still holds the look-ahead value, and any surface reading the
   column directly rather than through the vintage-filtered join is reading a field
   contaminated by the following 120 days. Whether such a surface exists is a question for
   sessions A and B, not a change Session G makes. It is written into the handoff.

## 5. What is published

- `docs/g/SITUATION_VINTAGE.json` — machine-readable: per event, per field, the Amendment A
  date and rule, the rule-(e) date and receipt, the decision, and the reason for every
  non-derivation.
- `docs/g/SITUATION_VINTAGE.md` — the before/after table of §7 and the audit table of §6.
- `data/handoffs/G_to_B_2026-09-03_situation_vintage.md` — the numbers for session B, and
  the two structural findings (§4 clause 3, and §8).
- `src/situation_vintage.py` — the code. It opens the database **read-only** and writes
  no table. `tests/test_g_situation_vintage.py` covers it.

## 6. The audit table — how Joe checks this without reading code

Every field for which rule (e) was *considered* gets one row, whether it was derived or
not, carrying: `event_id`, field, coded value, the **verbatim** dossier bullet (truncated
to 300 characters), the source markers found, each marker's raw `Doc. date` cell and the
date it parsed to, the decision, and — where rejected — which clause of §3 rejected it.
A reader who has never opened a Python file can take any row, open
`data/dossiers/<event_id>.md`, and check that the quoted bullet is really there and that
the decision follows. That is the proof this works. **Finding nothing wrong in that table
is not evidence that it is right; the table exists so that something wrong can be found.**

## 7. The before/after that will be published (shape fixed now, numbers later)

| | values | events with ≥1 field at t |
|---|---|---|
| baseline (`data/state/situation_knowable.json`, in the tree) | 786 total, 60 kept, 726 dropped | 51 of 313 |
| after rule (e), dossier events only (≤ 35 events) | — | — |
| after rule (e), whole corpus | — | — |
| of which: `conflict_scope` reclassified by (e.8) | — | — (never a gain) |

Broken out by field and by rule, plus: values that rule (e) moved **later** than Amendment A
gave them (the losses), and the count of dossier events where rule (e) recovered nothing,
with the clause that blocked each.

## 8. The one-way loss in the join, reported not patched

`src/state/situation_state.py:join()` computes `situation_rows_at(conn, eid, edate)` and
inserts **only the kept rows**. A field not knowable at the event's own date therefore never
reaches `situation_state` at all — so it is invisible not only to the read standing at that
event, but to every later read that retrieves that event as an **analog**, where the field
would be legitimately visible. `src/engine/read.py:_load_panel` selects all vintages and
`_apply_knowable` filters them by `as_of`, so the engine is built to handle rows it never
receives. This is session A's file and Session G does not touch it. It is stated here
because it changes what the numbers in §7 mean: the 726 are lost twice, and a rule-(e) gain
is worth more than the count alone suggests.

## 9. What this registration does not do

It does not write to `events` or `situation_state`; it does not change Amendment A, which is
session A's to change; it does not change `read.py`'s `KNOWABLE_FIELDS` or any threshold; it
does not admit any event; it does not re-score any run; and it makes no claim that a field it
dates is *correct* — only that a dated document establishes when it could have been known.
