# SPINE REGISTRATION — what a complete event record is
*2026-09-02, Session E, step E-2. Registered BEFORE any event record is rewritten
(the spine audit, `data/spine/AUDIT.md`, was published first and is the baseline
this standard is measured against). Amendments are dated and appended, never
edited. Nothing in this document changes the `events` table; it defines what must
be true before Joe is asked to.*

## 0. Why this exists

The audit says the spine's condition precisely: 313 events, **0 with two independent
source domains**, description median 148 characters, 49 records still carrying drafting
scaffolding, 9 citing a bare site root rather than a document, and `sr_json` field
sources 11.9 % external / 25.0 % corpus-derived / 63.1 % null. The codebook's two-source
rule was written as an admission standard and has never been met by the corpus it
governs. This document fixes what "met" means, so that the repair is checkable and so
that no record is rewritten to a standard invented after the fact.

## 1. A COMPLETE event record

An event record is **complete** when all six hold. Anything less is `partial` and says
which clause it fails. No record is ever completed by inference, by memory, or by
plausible reconstruction: if a clause cannot be met from retrieved sources, the record
stays partial and the gap is written down.

**(a) Two independent sources, at least one primary.**
Independent means different publishers, not two pages of one site: domains are compared
with a leading `www.` stripped, exactly as `src/spine_audit.py` counts them. **Primary**
means a document produced by a participant or an official body at the time: a diplomatic
record, a presidential address or message, an executive order, a UN or OPEC resolution, a
court or legislative record, a company or agency statement of the day. For pre-1990
events the primary source must come from the routes in §4, which were tested on the date
of this registration and whose status is recorded there. Contemporaneous press is a
legitimate **second** source and never the only one. A scholarly secondary source
(a monograph, a peer-reviewed article, a working paper) may serve as the second source
and never as the primary. Wikipedia may be used to orient a search and is never cited.

**(b) A case narrative of 120–250 words** answering, in this order: what happened; who
acted and against whom; what was physically at risk, in the units the trade uses
(barrels per day, refining capacity, transit volumes, storage); and — kept separate —
**what was known on the day** versus what is known now. The narrative is prose, not a
field dump. Every factual claim in it carries its source inline as a bracketed marker
(`[S1]`, `[S2]`, …) resolving to the source table in the dossier. A claim that no
retrieved source supports does not go in the narrative.

**(c) `knowable_at` with its reason.** The timestamp at which a reasonably attentive
market participant could first have known the fact that defines the event, with one
sentence saying how that is established (wire report, official announcement time, the
document's own date). Where only a date is establishable, `date_precision` says `day`,
`week` or `month` and the reason says why. This is the field the engine's filtration
depends on; a guess here is worse than an admission of ignorance.

**(d) Entities from the register**, with roles (`actor`, `target`, `affected_market`,
`location`) drawn only from `entities.entity_id`. An entity that should exist and does
not is reported to Session A in a handoff, never invented.

**(e) A class under the codebook** (`EVENTS_CODEBOOK.md`, closed set) **with the rule
that fired** — the specific codebook clause that puts this event in this class, quoted.
Where two classes are defensible, both are named and the tie-break is stated. Where the
scholarship disagrees with our class, the disagreement is recorded in the dossier and in
the decade essay; the class is not changed silently.

**(f) An explicit "what was NOT known at the time".** The facts that make hindsight
coding easy and contemporaneous forecasting hard: the magnitude that was only established
later, the intent that was disputed, the outcome that had not yet happened. This clause
exists because the whole engine is a claim about what was knowable at *t*, and a record
that does not separate the two is evidence for nothing.

## 2. The dossier

One file per event: `data/dossiers/<event_id>.md`, built by Session E, read by Joe.
Fixed section order, so a reader can diff two dossiers:

```
# <title>            event_id · event_date · date_precision · class
## Sources           numbered S1..Sn: role (primary/secondary/press), publisher,
                     exact title, document date, URL, retrieved_at, and the
                     verbatim quote relied on (never a paraphrase in this table)
## Narrative         120-250 words, every claim carrying [Sn]
## Knowable at       timestamp + reason + what fixes the precision
## Entities          entity_id, role, and which source names it
## Class             proposed class, the codebook clause quoted, alternatives considered
## Not known at the time
## Proposed field changes   one row per field: current value -> proposed value -> [Sn]
## Status            complete | partial (with the clause it fails)
```

A dossier records only what was retrieved. `retrieved_at` is the fetch timestamp, and a
quote in the source table is copied from the fetched text, never reconstructed.

## 3. How a record changes (nothing enters `events` without Joe)

1. Session E writes the dossier.
2. `src/spine_patch.py` turns the dossier's **Proposed field changes** into a patch file
   under `data/spine/patches/<batch>.json`, one row per field change carrying the
   event_id, field, current value, proposed value, and the source marker. The script
   reads the database read-only and **never writes to it**.
3. Joe reviews the dossier and the patch, and applies it himself with the admit line.
   The code never runs that line and refuses without it.
4. Every applied patch is appended to `data/spine/PATCH_LOG.md`: what changed, when,
   under which source, approved by whom.

A field that no source supports is never proposed. Where the audit shows a value is
wrong but no source establishes the right one, the patch proposes `unknown` — the
sourced-or-unknown rule (charter §2.1) resolves ties toward the admission of ignorance.

## 4. Retrieval routes, tested 2026-09-02

Every route below was requested on the registration date; the status is what came back,
not what is supposed to come back. A route marked unusable is not cited by any dossier
unless a later dated amendment records it working.

| route | status 2026-09-02 | use |
|---|---|---|
| **FRUS** — `history.state.gov/historicaldocuments/…` | **works**: volume and document pages return full text with an exact place-and-date line (verified on `frus1969-76v36/d221`, "Minutes of Washington Special Actions Group Meeting, Washington, October 19, 1973, 10:04–10:57 a.m.") | primary, 1945 → early 1990s |
| **American Presidency Project** — `presidency.ucsb.edu/documents/…` | **works**: verified on Nixon, "Address to the Nation About Policies To Deal With the Energy Shortages", November 7, 1973 | primary: addresses, messages, proclamations |
| **Federal Register codification** — `archives.gov/federal-register/codification/executive-order/…` | **works**: verified on EO 12170, "Blocking Iranian Government property", November 14, 1979 | primary: executive orders, sanctions |
| **NBER working papers** — `nber.org/system/files/working_papers/…pdf` | **works**: PDF retrieved and text extracted (Hamilton, *Historical Oil Shocks*, WP 16790, February 2011, 52 pp.) | secondary, scholarly. The paper states on its cover that NBER working papers are not peer-reviewed; it is cited as a working paper, and never as the primary source |
| UN Digital Library — `digitallibrary.un.org` | **HTTP 403** to scripts | not cited by code; Joe may cite a resolution by hand |
| Security Council Report — `securitycouncilreport.org` | **HTTP 403** | unusable |
| OPEC press room — `opec.org/press-room/…` | **HTTP 402** | unusable; OPEC decisions must be sourced elsewhere |
| CIA FOIA reading room search — `cia.gov/readingroom/search/site/…` | returns the site homepage, no results | unusable in this form |
| EIA petroleum chronology | the chronology page is gone; the weekly report page carries no timeline | unusable — and the 9 events citing `https://www.eia.gov` cite a site root, not a document (audit) |

## 5. What is never done

Never cite a source that was not retrieved in this session's own fetch log — including
standard works everyone knows. If a monograph is named in a decade essay for context, the
essay says explicitly that it was **not opened**, and no claim rests on it. Never convert
a paraphrase into a quotation. Never fill `severity`, `surprise` or a `sr_*` field to
remove a null: a null is a measurement. Never change an `event_date` to fit a price move.
Never write to `events`, `data/events.csv` or `situation_state`. Never edit another
session's files.

## 6. Order of work

Oldest first, because the historical tail is where the audit is worst and where the
engine has the fewest precedents: the 1970–1989 tier (19 events, 18 of them carrying
scaffolding), then the 1990s (16 events, 6 carrying scaffolding), then any 2000s+ record
whose `sr_json` field sources are majority null. One commit per batch of ten events,
each commit naming the events, the sources added, and any class the scholarship
challenges.

## 7. How completion is measured

`src/spine_audit.py` is re-run after every batch. The number that matters is events with
**≥ 2 independent source domains, at least one primary** and a narrative ≥ 700
characters — both zero at registration. The audit's own table is the scoreboard; no
other claim of progress is made.
