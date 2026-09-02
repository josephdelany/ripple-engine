# Dossier icb_288_chad_libya_ii — CHAD/LIBYA II

```json
{
 "id": "icb_288_chad_libya_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:54+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 288,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=288",
  "trigdate": "1978-01-22",
  "termdate": "1978-03-27",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1978-01-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Chad Libya Ii 1978",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+Ii+1978&within=documents",
  "search_status": 200,
  "window": [
   "1977-12-23",
   "1978-04-26"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d100",
    "title": "100. Intelligence Memorandum Prepared in the Central Intelligence Agency (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1979-06-01",
    "retrieved_at": "2026-09-02T19:17:51+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v09Ed2/d30",
    "title": "30. Memorandum of Conversation (1977\u20131980, Volume IX, Arab-Israeli Dispute, August 1978\u2013December 1980, Second, Revised Edition)",
    "page_date": "1978-09-06",
    "retrieved_at": "2026-09-02T19:17:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d35",
    "title": "35. Memorandum of Conversation (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
    "page_date": "1978-06-08",
    "retrieved_at": "2026-09-02T19:17:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d161",
    "title": "161. Memorandum of Conversation (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1978-11-15",
    "retrieved_at": "2026-09-02T19:17:53+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v09Ed2/d384",
    "title": "384. Memorandum of Conversation (1977\u20131980, Volume IX, Arab-Israeli Dispute, August 1978\u2013December 1980, Second, Revised Edition)",
    "page_date": "1980-06-17",
    "retrieved_at": "2026-09-02T19:17:54+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:17:50+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 288 **CHAD/LIBYA II**: trigdate 1978-01-22, termdate 1978-03-27, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=288

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.libya:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chad Libya Ii 1978` (https://history.state.gov/search?q=Chad+Libya+Ii+1978&within=documents, HTTP 200) returned 5 document(s) opened, none dated inside 1977-12-23..1978-04-26.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 100. Intelligence Memorandum Prepared in the Central Intelli (1979-06-01); 30. Memorandum of Conversation (1977–1980, Volume IX, Arab-I (1978-09-06); 35. Memorandum of Conversation (1977–1980, Volume XVII, Part (1978-06-08); 161. Memorandum of Conversation (1977–1980, Volume XVII, Par (1978-11-15); 384. Memorandum of Conversation (1977–1980, Volume IX, Arab- (1980-06-17)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_288_chad_libya_ii --approved-by joe`. The code never runs it.
