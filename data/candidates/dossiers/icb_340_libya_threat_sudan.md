# Dossier icb_340_libya_threat_sudan — LIBYA THREAT/SUDAN

```json
{
 "id": "icb_340_libya_threat_sudan",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:23+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 340,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=340",
  "trigdate": "1983-02-11",
  "termdate": "1983-02-22",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1983-02-11",
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
   "entity": "country.sudan",
   "role": "target"
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
  "query": "Libya Threat Sudan 1983",
  "search_url": "https://history.state.gov/search?q=Libya+Threat+Sudan+1983&within=documents",
  "search_status": 200,
  "window": [
   "1983-01-12",
   "1983-03-24"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d290",
    "title": "290. Minutes of a Meeting of the Joint Military Commission (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1981-11-09",
    "retrieved_at": "2026-09-02T19:19:21+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d27",
    "title": "27. Telegram From the Embassy in Yugoslavia to the Department of State and the White House (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1983-09-17",
    "retrieved_at": "2026-09-02T19:19:21+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v08/d31",
    "title": "31. Memorandum of Conversation (1977\u20131980, Volume VIII, Arab-Israeli Dispute, January 1977\u2013August 1978)",
    "page_date": "1977-04-26",
    "retrieved_at": "2026-09-02T19:19:22+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:19:20+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 340 **LIBYA THREAT/SUDAN**: trigdate 1983-02-11, termdate 1983-02-22, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=340

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 620: country.libya (registered state set)
- 625: country.sudan
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.libya:actor, country.sudan:target, country.egypt:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Libya Threat Sudan 1983` (https://history.state.gov/search?q=Libya+Threat+Sudan+1983&within=documents, HTTP 200) returned 3 document(s) opened, none dated inside 1983-01-12..1983-03-24.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 290. Minutes of a Meeting of the Joint Military Commission ( (1981-11-09); 27. Telegram From the Embassy in Yugoslavia to the Departmen (1983-09-17); 31. Memorandum of Conversation (1977–1980, Volume VIII, Arab (1977-04-26)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_340_libya_threat_sudan --approved-by joe`. The code never runs it.
