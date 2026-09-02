# Dossier icb_281_egypt_libya_clashes — EGYPT/LIBYA CLASHES

```json
{
 "id": "icb_281_egypt_libya_clashes",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:43+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 281,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=281",
  "trigdate": "1977-07-14",
  "termdate": "1977-09-10",
  "viol": 3,
  "forout": 2
 },
 "event_date": "1977-07-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "target"
  },
  {
   "entity": "country.egypt",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Egypt Libya Clashes 1977",
  "search_url": "https://history.state.gov/search?q=Egypt+Libya+Clashes+1977&within=documents",
  "search_status": 200,
  "window": [
   "1977-06-14",
   "1977-10-10"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d77",
    "title": "77. Memorandum From Secretary of State Haig to President Reagan (1981\u20131988, Volume I, Foundations of Foreign Policy)",
    "page_date": "1982-01-11",
    "retrieved_at": "2026-09-02T19:17:42+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v27/d302",
    "title": "302. Memorandum of Conversation (1969\u20131976, Volume XXVII, Iran; Iraq, 1973\u20131976)",
    "page_date": "1975-12-17",
    "retrieved_at": "2026-09-02T19:17:42+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d32",
    "title": "32. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-05-09",
    "retrieved_at": "2026-09-02T19:17:43+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:17:41+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 281 **EGYPT/LIBYA CLASHES**: trigdate 1977-07-14, termdate 1977-09-10, viol 3, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=281

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 620: country.libya (registered state set)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.libya:target, country.egypt:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Egypt Libya Clashes 1977` (https://history.state.gov/search?q=Egypt+Libya+Clashes+1977&within=documents, HTTP 200) returned 3 document(s) opened, none dated inside 1977-06-14..1977-10-10.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 77. Memorandum From Secretary of State Haig to President Rea (1982-01-11); 302. Memorandum of Conversation (1969–1976, Volume XXVII, Ir (1975-12-17); 32. Memorandum of Conversation (1977–1980, Volume VIII, Arab (1977-05-09)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_281_egypt_libya_clashes --approved-by joe`. The code never runs it.
