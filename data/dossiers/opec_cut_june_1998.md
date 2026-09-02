# A June 1998 OPEC cut is referenced only indirectly — this session could not source it          opec_cut_june_1998 · 1998-06-24 (unconfirmed) · day (unconfirmed) · opec_decision

## Sources

| # | Role | Publisher | Title | Doc. date | URL | Retrieved at (UTC) | Verbatim quote relied on |
|---|------|-----------|-------|-----------|-----|---------------------|---------------------------|
| S1 | press (contemporaneous wire report, independent domain) | RFE/RL (Radio Free Europe/Radio Liberty), Charles Recknagel | "World: OPEC States Approve Cut In Oil Output" | dateline Prague, 24 March 1999 | https://www.rferl.org/a/1090869.html | 2026-09-02T23:10Z (session) | "The new OPEC cutback agreement is the third in two years and comes after both previous accords were sabotaged by overproduction by individual members." |

**This is not a source for this event's specific facts.** [S1] is about the 23 March 1999 OPEC cut (see the `opec_cut_1999` dossier, where it is the primary source). It is included here only because it is the sole retrieved fact touching this event at all: an indirect, undated, unlocated reference to "the third [cutback agreement] in two years," implying two prior 1998 accords existed (consistent with, but not confirming, this database's `opec_cut_march_1998` and `opec_cut_june_1998` records). No source retrieved this session narrates a late-June 1998 OPEC decision specifically — no date, no meeting location, no barrels-per-day figure.

## Narrative

This dossier could not establish, from any source retrieved this session, the specific facts of a late-June 1998 OPEC decision: no source confirms a 24 June 1998 date, a meeting location, or a 1.355 million barrels-a-day cut. Genuine retrieval attempts were made across govinfo.gov, eia.gov, iea.org, imf.org, crsreports.congress.gov, upi.com, bis.org, federalreserve.gov, fraser.stlouisfed.org and presidency.ucsb.edu, documented below; none returned content narrating this event. The one relevant fact retrieved is indirect: RFE/RL's contemporaneous report on OPEC's subsequent 23 March 1999 cut describes that decision as "the third [cutback agreement] in two years," coming "after both previous accords were sabotaged by overproduction by individual members" [S1] — corroborating only that a second 1998 OPEC cut accord existed somewhere between the 30 March 1998 Vienna decision and the March 1999 decision, without dating, locating, or sizing it. What was physically at risk cannot be stated because the decision's content is unconfirmed. This gap is reported rather than filled: the database's existing figures may well be accurate, but this dossier did not retrieve a source establishing them, and none is invented here. (177 words)

## Knowable at

**Not established.** No source retrieved this session provides a date, or a reason to trust a date, for this event's specific facts. The current database value (1998-06-24, `date_precision = day`) is neither confirmed nor contradicted by evidence retrieved this session — its absence from this dossier's sourcing is a gap in retrieval, not a finding against it.

## Entities

No changes proposed. No source retrieved this session speaks to this specific event's actors, so current coding (`institution.opec:actor`, `commodity.brent:affected_market`) is left as-is — unconfirmed and uncontradicted alike.

## Class

Proposed class: `opec_decision`, as currently coded. Codebook clause: "`opec_decision` | OPEC/OPEC+ production decision or collapse of talks." Even without confirming this event's specific facts, [S1]'s general reference to "the third [cutback agreement] in two years" is consistent with this event being some form of OPEC production-cut decision, so the class itself is not challenged by the (thin) evidence available — only its specific date, location and magnitude are unconfirmed.

## Not known at the time

Cannot be meaningfully addressed. This dossier could not establish what the event was with enough specificity to separate contemporaneous knowledge from hindsight.

## Proposed field changes

| Field | Current | Proposed | Source |
|---|---|---|---|
| `source_url` | https://en.wikipedia.org/wiki/1998_world_oil_market_chronology | **No replacement could be retrieved this session.** Every route attempted (listed in Status) failed to produce a source narrating this specific event. Recommend removing the Wikipedia citation and leaving `source_url` `unknown`/NULL rather than retaining an encyclopaedia citation, pending a future session's retrieval — do not fabricate a replacement. | — |
| `event_date` | 1998-06-24 | unchanged — no source retrieved this session supports a change in either direction | — |
| `date_precision` | day | unchanged | — |
| `severity` | 3 | unchanged | — |
| `surprise` | 3 | unchanged | — |
| `description` | "At its 105th conference OPEC agreed a further 1.355 million bpd cut effective July 1, lifting cumulative 1998 reductions to 2.6 million bpd to arrest the price slide" | unchanged — this dossier neither confirms nor contradicts the figures already in the description; it records only that it could not independently verify them | — |
| `confidence` | high | leave for Joe to weigh: the existing `confidence = high` was presumably assigned on the strength of the now-disqualified Wikipedia source; this dossier retrieved nothing that would itself support "high" | — |

## Status

partial — fails clause (a) (no source at all, let alone two independent domains or a primary), clause (b) (the narrative above is a gap-report, not an account of what happened, who acted, and what was physically at risk — none of which could be sourced), and clause (c) (`knowable_at` not established). This is the weakest-sourced of the four events in this batch.

Routes tried and failed this session: opec.org — HTTP 402 (confirmed unusable per SPINE_REGISTRATION.md §4); oxfordenergy.org direct — HTTP 403 (x2; and Mabro's SP10 paper, retrieved via its ora.ox.ac.uk mirror for the other two 1998 dossiers in this batch, was written in April 1998 and predates a June 1998 decision, so it could not have covered this event even in principle); eia.gov (multiple report-archive pages) — HTTP 403; iea.org (root) — HTTP 403; imf.org / elibrary.imf.org — HTTP 403; crsreports.congress.gov (search) — HTTP 403; upi.com/Archives — HTTP 403; bis.org (Quarterly Review URL guesses) — HTTP 404; fraser.stlouisfed.org — no keyword-search endpoint found (404; browse-only navigation); federalreserve.gov — Beige Book archive URL guesses returned 404, and the one page that did load (Monetary Policy Report, 21 July 1998) contained no OPEC-specific content; govinfo.gov — the *Economic Report of the President 1999* (450pp) and the House *Congressional Record* for 25 June 1998 (186pp, the day after this event's putative date) both loaded successfully and were searched in full but contain zero mentions of OPEC, oil prices, or crude oil in a relevant context; api.govinfo.gov — HTTP 401 (requires an API key not obtained this session); web.archive.org — blocked to this tool ("Claude Code is unable to fetch from web.archive.org"), so a Wayback Machine mirror of the old (now-gone) EIA oil-market chronology page, found via Wikipedia's own external links, could not be checked; duckduckgo.com/html — returned a CAPTCHA challenge; bing.com/search — loaded but returned only generic, non-query-specific "OPEC" overview results regardless of query wording (multiple distinct queries returned an identical result set); presidency.ucsb.edu's advanced search — functional (a real, working full-text search, unlike most routes above), searched for "OPEC" in a June-July 1998 window and returned zero documents.

This is exactly the finding SPINE_REGISTRATION.md anticipates is possible: a whole event may be unsourceable within a session's retrievable routes. The honest record of that is this Status line, not a fabricated citation.
