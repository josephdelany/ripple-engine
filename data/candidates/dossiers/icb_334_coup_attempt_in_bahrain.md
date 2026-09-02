# Dossier icb_334_coup_attempt_in_bahrain — COUP ATTEMPT IN BAHRAIN

```json
{
 "id": "icb_334_coup_attempt_in_bahrain",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:13+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 334,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=334",
  "trigdate": "1981-12-13",
  "termdate": "1982-01-08",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1981-12-13",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.bhr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Coup Attempt In Bahrain 1981",
  "search_url": "https://history.state.gov/search?q=Coup+Attempt+In+Bahrain+1981&within=documents",
  "search_status": 200,
  "window": [
   "1981-11-13",
   "1982-02-07"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v03/d221",
    "title": "221. Memorandum of Conversation (1981\u20131988, Volume III, Soviet Union, January 1981\u2013January 1983)",
    "page_date": "1982-10-04",
    "retrieved_at": "2026-09-02T19:19:13+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:19:12+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 334 **COUP ATTEMPT IN BAHRAIN**: trigdate 1981-12-13, termdate 1982-01-08, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=334

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 670: country.saudi_arabia (registered state set)
- 692: country.bhr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.saudi_arabia:unknown, country.bhr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Coup Attempt In Bahrain 1981` (https://history.state.gov/search?q=Coup+Attempt+In+Bahrain+1981&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1981-11-13..1982-02-07.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 221. Memorandum of Conversation (1981–1988, Volume III, Sovi (1982-10-04)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_334_coup_attempt_in_bahrain --approved-by joe`. The code never runs it.
