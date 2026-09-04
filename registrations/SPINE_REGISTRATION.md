> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A registration for a superseded study, kept so its pre-commitments stay auditable. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

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
3. Joe reviews the dossier and the patch, and applies it himself with the admit line:
   `python3 src/spine_apply.py --batch <name> --approved-by joe` (add `--dry-run` to see
   the change and write nothing). `src/spine_apply.py` is the only file in this toolchain
   that writes to the database; it refuses without `--approved-by joe`, refuses any row
   flagged `needs_joe`, refuses a column outside the patch whitelist, refuses a row whose
   live value has moved since the patch was built, refuses a value that fails its column's
   own range, and refuses to write an encyclopaedia URL. It gzips a backup of `oil.db`
   first, runs the whole batch in one transaction, and records the audit scoreboard before
   and after. The code never runs that line itself.
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

---

## Amendment 1 (2026-09-02) — three route corrections, from the pre-1990 batch

*Dated and appended, never edited. §4's table records routes as tested; running the
1970–1989 batch tested more of them, and three entries need correcting. Nothing else in
this registration changes.*

- **A.1 UN Peacekeeping is usable, and the UN Digital Library still is not.**
  `https://peacekeeping.un.org/sites/default/files/past/…` serves official mission
  histories and was verified by the reviewer on the UNIIMOG background page, which states
  "On 8 August, when he announced the agreement of both Iran and Iraq to a ceasefire with
  effect from 0300 GMT on 20 August", "The ceasefire came into effect at 0300 GMT on
  20 August 1988", and "In its resolution 619 (1988) of 9 August, the Security Council
  approved the Secretary-General's report and decided to establish UNIIMOG immediately for
  a period of six months." §4's row for the UN said only that `digitallibrary.un.org`
  returns 403, which is still true and is a different host. UN mission histories are
  **primary** for the facts of a UN operation and its dates.

- **A.2 FRUS is not available for the Reagan-era Gulf events.** §4 says FRUS runs "1945 →
  early 1990s", which is true of the series but not of the volumes this batch needed:
  FRUS 1981–1988 Volumes XX and XXI (Iran, Iraq) are marked **"Being Cleared"** and are not
  published, and FRUS 1969–1976 Volume X (Iran, January 1977 – November 1979) is likewise
  unpublished. Checked, not assumed. The consequence is recorded rather than worked
  around: the 1984–1988 dossiers rest on scholarly secondary sources and contemporaneous
  press, and say so in their status lines. FRUS 1981–1988 Volume I is published and did
  yield a primary document for the 1987 reflagging.

- **A.3 A press wire archive is usable where it serves the article text.**
  `https://www.upi.com/Archives/…` returned dated wire copy for July 1987 and August 1988
  and is cited with role `press`. Under §1(a) press is a legitimate second source and
  never the only one; every dossier using it also carries a non-press source.

**Standing note on scholarly monographs.** Where no primary document exists for an event,
a dossier may rest on a scholarly secondary source, and its status is then `partial —
fails (a)`, because clause (a) requires a primary. This batch has several such records and
they are not rounded up. The rule is unchanged; this note only makes the consequence
explicit, since a reader may otherwise read a well-sourced partial as a failure of effort
rather than of the archive.

---

## Amendment 2 (2026-09-02) — OPEC decisions cannot be sourced by any free route tested

*Dated and appended. §4 recorded `opec.org` as HTTP 402. Working the 1990s and 2000s tiers
showed the problem is wider than one host, and the consequence is structural rather than a
matter of effort, so it is registered rather than left in a session report.*

`opec_decision` is the second-largest class in the corpus (52 records) and the most heavily
represented in the encyclopaedia-sourced set the audit found. Routes tested by the reviewer
on the registration date, each requested directly:

| route | result |
|---|---|
| `opec.org` press room and conference resolutions | HTTP 402 |
| `oxfordenergy.org` (Oxford Institute for Energy Studies) | HTTP 403 |
| `crsreports.congress.gov` (Congressional Research Service PDFs) | HTTP 403 |
| `apnews.com` | refused by the fetch client |
| `eia.gov/finance/markets/crudeoil/supply-opec.php` | reachable, but describes how OPEC sets targets in general and names no meeting, decision or quota change with a date |
| `upi.com/Archives` | worked for 1987 and 1988 wire copy in one run and returned 403 in another; treat as intermittent |

Some OPEC decisions **are** sourceable, and the pre-1990 and 1990s dossiers show how: through
a document that reports the decision in passing (the Oxford Energy Forum piece used for the
1985 shift, an NYU archival finding aid, an institutional review). That is opportunistic, not
a route, and it will not scale to fifty records.

**What this registers.** A dossier for an OPEC decision that cannot reach two independent
citable domains is `partial — fails (a)`, and that is the expected outcome for this class
rather than a sign of a poor search. No dossier may substitute an encyclopaedia, and none may
assert a quota figure or a meeting date that was not retrieved. If the corpus is to carry
sourced OPEC decisions at scale, that requires an archive this project does not currently
have access to — a subscription news archive or OPEC's own paid materials — and that is a
decision about money and licensing, which is Joe's, not a research task.
