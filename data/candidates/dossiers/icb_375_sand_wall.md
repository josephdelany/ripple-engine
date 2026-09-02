# Dossier icb_375_sand_wall — SAND WALL

```json
{
 "id": "icb_375_sand_wall",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 375,
  "source": "icb",
  "source_id": "375",
  "detail": "SAND WALL 1987-02-25..1987-05-04 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=375",
  "trigdate": "1987-02-25",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-02-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.dza",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  435,
  600
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Sand Wall 1987",
  "search_url": "https://history.state.gov/search?q=Sand+Wall+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-01-26",
   "1987-03-27"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d326",
    "title": "326. Remarks by President Reagan (1981\u20131988, Volume I, Foundations of Foreign Policy)",
    "page_date": "1988-05-31",
    "retrieved_at": "2026-09-02T19:52:22+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:52:22+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 375 **SAND WALL**: SAND WALL 1987-02-25..1987-05-04 viol 3.0 trigdate 1987-02-25, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=375

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 435: UNMAPPED
- 600: UNMAPPED
- 615: country.dza (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.dza:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Sand Wall 1987` (https://history.state.gov/search?q=Sand+Wall+1987&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1987-01-26..1987-03-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 326. Remarks by President Reagan (1981–1988, Volume I, Found (1988-05-31)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_375_sand_wall --approved-by joe`. The code never runs it.
