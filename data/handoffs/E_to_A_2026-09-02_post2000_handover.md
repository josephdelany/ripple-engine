# Handoff E → A, 2026-09-02: the post-2000 half of the three cohorts, and what to reuse

Joe has split the spine repair. **A takes the source-repair tooling and the post-2000 half
of the three cohorts. E keeps the dossier standard and the pre-2000 half**, continuing the
primary-document method. E will use A's route table when it lands rather than building its
own fetchers, so this note hands over the measured facts rather than any code that fetches.

## What A now owns, measured

The three cohorts split like this (computed by `src/spine_audit.py`, re-runnable):

| cohort | post-2000 (**A**) | pre-2000 (**E**) |
|---|---|---|
| encyclopaedia-only source_url | **27** | 4 |
| bare site-root `source_url` (all `https://www.eia.gov`) | **0** | 9 |
| draft scaffolding in the description | **25** | 24 |

The bare-root cohort is entirely pre-2000 and stays with E; it comes from the deep-history
seed naming the EIA energy chronology, which no longer exists.

**A's encyclopaedia-only 27, by class:** `opec_decision` 10, `conflict_escalation` 8,
`chokepoint_disruption` 4, `infrastructure_attack` 4, `sanctions` 1.
**A's draft-scaffolding 25, by decade:** 2000s 4, 2010s 11, 2020s 10.

Per-event membership is in `data/spine/audit.json` under `events`, with the flags
`source_url_tertiary`, `source_url_generic_root` and `placeholder`. No list needs to be
maintained by hand.

## Reuse rather than rebuild

- **The standard.** `SPINE_REGISTRATION.md` — six clauses for a complete record, the dossier
  template in §2, the retrieval-route table in §4, and two dated amendments. E keeps
  ownership of the standard; if A needs it changed, a dated amendment is the mechanism and E
  will write it on request.
- **The checker.** `python3 src/spine_check.py [event_id ...]` decides mechanically whether
  a dossier meets the standard, and reports FAIL when a dossier claims "complete" while
  failing any check. It exits non-zero on a FAIL, so it can gate a commit.
- **The patch builder.** `python3 src/spine_patch.py --batch <name> --events ...` reads the
  dossiers and the live values read-only and writes `data/spine/patches/<name>.json`. It
  never writes to the database. Two parser rules matter and were learned the hard way: a
  proposed `event_date` must LEAD its cell, and a proposed description must OPEN with a
  quotation, because a dossier that wrote "not changed here, but flagged: [S2] dates the
  start to 1991-01-16" had that date lifted out of its prose and proposed as a change the
  dossier had explicitly declined to make. Anything not reducible to a clean value is
  flagged `needs_joe` rather than written.
- **The audit.** `python3 src/spine_audit.py` is the scoreboard, and §7 of the registration
  fixes what counts as progress: events with two independent citable domains and a narrative
  of 700+ characters. Both were zero at registration and are still zero, because no patch has
  been applied.
- **The log.** `data/spine/PATCH_LOG.md` is append-only, with an empty "Applied" section.

If A extends `spine_audit.py` with new measures, please keep the existing keys stable —
`data/spine/audit.json` is the file the paper's §3 numbers are being drawn from.

## The one route finding A most needs before starting

**OPEC decisions cannot be sourced by any free route tested.** This is registered as
`SPINE_REGISTRATION.md` Amendment 2 with the evidence, and it matters disproportionately to
A because 10 of A's 27 encyclopaedia-only records are OPEC decisions, and `opec_decision` is
52 records corpus-wide. Tested directly, each request made: `opec.org` 402;
`oxfordenergy.org` 403; `crsreports.congress.gov` 403; `apnews.com` refused by the fetch
client; the EIA OPEC supply page reachable but naming no meeting, decision or quota change
with a date; `upi.com/Archives` intermittent, working in one run and 403 in another.

Some OPEC decisions are sourceable opportunistically, through a document that reports one in
passing — that is how the 1985 shift was reached, via an Oxford Energy Forum piece and an NYU
archival finding aid. That is not a route and will not scale to fifty records. The registered
consequence: `partial` is the expected status for this class, an encyclopaedia is never
substituted, and sourcing OPEC at scale needs an archive the project does not have, which is
a money and licensing decision for Joe.

## Routes E has confirmed working, for A's table

Each verified by fetching and quoting: `history.state.gov` (FRUS, primary, with exact
place-and-date lines); `presidency.ucsb.edu`; `archives.gov/federal-register/codification/
executive-order/`; `govinfo.gov` (the Public Papers of the Presidents resolve there);
`peacekeeping.un.org/sites/default/files/past/`; `press.un.org`; `ofac.treasury.gov`;
`nber.org` and `bis.org` PDFs, which extract cleanly with `pypdf`. Confirmed blocked:
`digitallibrary.un.org` 403, `securitycouncilreport.org` 403, `imf.org` 403,
`cia.gov/readingroom` search, `nytimes.com` and `washingtonpost.com`.

**Please send E the route table when it lands** (`data/handoffs/A_to_E_<date>.md` is fine).
E will use it for the remaining pre-2000 records rather than testing hosts again.

## What E is still doing

The pre-2000 half: 35 records, 28 with dossiers as of this note, 7 in progress. E will report
by decade in three categories — closed, partial, and blocked-by-declassification — the last
being records that cannot close at any effort because the primary record is unpublished. The
Reagan-era Gulf events are in that category: FRUS 1981–1988 Volumes XX and XXI (Iran, Iraq)
and FRUS 1969–76 Volume X (Iran 1977–79) are all marked "Being Cleared". That is a fact about
the declassification queue, and no route table will change it.

— Session E
