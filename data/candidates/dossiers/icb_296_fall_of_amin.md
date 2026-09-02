# Dossier icb_296_fall_of_amin — FALL OF AMIN

```json
{
 "id": "icb_296_fall_of_amin",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:10+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 296,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=296",
  "trigdate": "1978-10-28",
  "termdate": "1979-04-10",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1978-10-28",
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
  500,
  510
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Fall Of Amin 1978",
  "search_url": "https://history.state.gov/search?q=Fall+Of+Amin+1978&within=documents",
  "search_status": 200,
  "window": [
   "1978-09-28",
   "1979-05-10"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d88",
    "title": "88. Briefing Memorandum From the Acting Director of the Bureau of Intelligence and Research (Mark) to Secretary of State Vance (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": "1979-12-16",
    "retrieved_at": "2026-09-02T19:18:07+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d67",
    "title": "67. Interagency Intelligence Memorandum Prepared in the Central Intelligence Agency (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": "1979-09-28",
    "retrieved_at": "2026-09-02T19:18:07+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d104",
    "title": "104. Telegram From the Embassy in Pakistan to the Department of State (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": "1979-12-28",
    "retrieved_at": "2026-09-02T19:18:08+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d131",
    "title": "131. Intelligence Memorandum Prepared in the Central Intelligence Agency (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1980-05-16",
    "retrieved_at": "2026-09-02T19:18:09+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d56",
    "title": "56. Editorial Note (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": null,
    "retrieved_at": "2026-09-02T19:18:09+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p3/d100",
    "title": "100. Intelligence Memorandum Prepared in the Central Intelligence Agency (1977\u20131980, Volume XVII, Part 3, North Africa)",
    "page_date": "1979-06-01",
    "retrieved_at": "2026-09-02T19:17:51+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:06+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 296 **FALL OF AMIN**: trigdate 1978-10-28, termdate 1979-04-10, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=296

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 500: UNMAPPED
- 510: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.libya:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Fall Of Amin 1978` (https://history.state.gov/search?q=Fall+Of+Amin+1978&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1978-09-28..1979-05-10.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 88. Briefing Memorandum From the Acting Director of the Bure (1979-12-16); 67. Interagency Intelligence Memorandum Prepared in the Cent (1979-09-28); 104. Telegram From the Embassy in Pakistan to the Department (1979-12-28); 131. Intelligence Memorandum Prepared in the Central Intelli (1980-05-16); 56. Editorial Note (1977–1980, Volume XII, Afghanistan) (no date); 100. Intelligence Memorandum Prepared in the Central Intelli (1979-06-01)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_296_fall_of_amin --approved-by joe`. The code never runs it.
