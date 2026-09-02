# Dossier icb_314_libya_threat_sadat — LIBYA THREAT-SADAT

```json
{
 "id": "icb_314_libya_threat_sadat",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:44+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 314,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=314",
  "trigdate": "1980-06-11",
  "termdate": "1980-06-28",
  "viol": 1,
  "forout": 7
 },
 "event_date": "1980-06-11",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "actor"
  },
  {
   "entity": "country.egypt",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Libya Threat Sadat 1980",
  "search_url": "https://history.state.gov/search?q=Libya+Threat+Sadat+1980&within=documents",
  "search_status": 200,
  "window": [
   "1980-05-12",
   "1980-07-28"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d6",
    "title": "6. Telegram From the Embassy in Egypt to the Department of State (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1977-04-16",
    "retrieved_at": "2026-09-02T19:18:40+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d210",
    "title": "210. Memorandum of Conversation (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1980-02-29",
    "retrieved_at": "2026-09-02T19:18:40+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v09Ed2/d354",
    "title": "354. Memorandum of Conversation (1977\u20131980, Volume IX, Arab-Israeli Dispute, August 1978\u2013December 1980, Second, Revised Edition)",
    "page_date": "1980-04-08",
    "retrieved_at": "2026-09-02T19:18:41+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d27",
    "title": "27. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-04-05",
    "retrieved_at": "2026-09-02T19:18:42+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v09Ed2/d24",
    "title": "24. Minutes of a National Security Council Meeting (1977\u20131980, Volume IX, Arab-Israeli Dispute, August 1978\u2013December 1980, Second, Revised Edition)",
    "page_date": "1978-09-01",
    "retrieved_at": "2026-09-02T19:18:42+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d172",
    "title": "172. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-12-12",
    "retrieved_at": "2026-09-02T19:18:43+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:39+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 314 **LIBYA THREAT-SADAT**: trigdate 1980-06-11, termdate 1980-06-28, viol 1, forout 7. Page: https://www.icb.umd.edu/dataviewer/?crisno=314

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 620: country.libya (registered state set)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.libya:actor, country.egypt:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Libya Threat Sadat 1980` (https://history.state.gov/search?q=Libya+Threat+Sadat+1980&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1980-05-12..1980-07-28.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 6. Telegram From the Embassy in Egypt to the Department of S (1977-04-16); 210. Memorandum of Conversation (1977–1980, Volume XVII, Par (1980-02-29); 354. Memorandum of Conversation (1977–1980, Volume IX, Arab- (1980-04-08); 27. Memorandum of Conversation (1977–1980, Volume VIII, Arab (1977-04-05); 24. Minutes of a National Security Council Meeting (1977–198 (1978-09-01); 172. Memorandum of Conversation (1977–1980, Volume VIII, Ara (1977-12-12)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_314_libya_threat_sadat --approved-by joe`. The code never runs it.
