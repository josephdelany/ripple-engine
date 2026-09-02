# Dossier icb_139_invasion_of_laos_i — INVASION OF LAOS I

```json
{
 "id": "icb_139_invasion_of_laos_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:36+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 139,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=139",
  "trigdate": "1953-03-24",
  "termdate": "1953-01-01",
  "viol": 3,
  "forout": 7
 },
 "event_date": "1953-03-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  812
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Invasion Of Laos I 1953",
  "search_url": "https://history.state.gov/search?q=Invasion+Of+Laos+I+1953&within=documents",
  "search_status": 200,
  "window": [
   "1953-02-22",
   "1953-01-31"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v13p1/d484",
    "title": "The Charg\u00e9 at Saigon (McClintock) to the Department of State (1952\u20131954, Volume XIII, Part 1, Indochina)",
    "page_date": "1953-12-17",
    "retrieved_at": "2026-09-02T19:13:33+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v13p1/d223",
    "title": "Memorandum of Conversation, by the Director of the Office of Philippine and Southeast Asian Affairs (Bonsal) (1952\u20131954, Volume XIII, Part 1, Indochina)",
    "page_date": "1953-04-16",
    "retrieved_at": "2026-09-02T19:13:33+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v13p1/d257",
    "title": "The Ambassador in Thailand (Stanton) to the Department of State (1952\u20131954, Volume XIII, Part 1, Indochina)",
    "page_date": "1953-04-30",
    "retrieved_at": "2026-09-02T19:13:34+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v13p1/d251",
    "title": "The Secretary of State to the Embassy in France (1952\u20131954, Volume XIII, Part 1, Indochina)",
    "page_date": "1953-04-29",
    "retrieved_at": "2026-09-02T19:13:34+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v13p1/d266",
    "title": "The Secretary of State to the Embassy in France (1952\u20131954, Volume XIII, Part 1, Indochina)",
    "page_date": "1953-05-06",
    "retrieved_at": "2026-09-02T19:13:35+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1952-54v13p1/d233",
    "title": "The Charg\u00e9 at Saigon (McClintock) to the Department of State (1952\u20131954, Volume XIII, Part 1, Indochina)",
    "page_date": "1953-04-24",
    "retrieved_at": "2026-09-02T19:13:36+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:13:32+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 139 **INVASION OF LAOS I**: trigdate 1953-03-24, termdate 1953-01-01, viol 3, forout 7. Page: https://www.icb.umd.edu/dataviewer/?crisno=139

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 812: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.fra:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Invasion Of Laos I 1953` (https://history.state.gov/search?q=Invasion+Of+Laos+I+1953&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1953-02-22..1953-01-31.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: The Chargé at Saigon (McClintock) to the Department of State (1953-12-17); Memorandum of Conversation, by the Director of the Office of (1953-04-16); The Ambassador in Thailand (Stanton) to the Department of St (1953-04-30); The Secretary of State to the Embassy in France (1952–1954,  (1953-04-29); The Secretary of State to the Embassy in France (1952–1954,  (1953-05-06); The Chargé at Saigon (McClintock) to the Department of State (1953-04-24)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_139_invasion_of_laos_i --approved-by joe`. The code never runs it.
