# Dossier icb_391_invasion_of_panama — INVASION OF PANAMA

```json
{
 "id": "icb_391_invasion_of_panama",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 391,
  "source": "icb",
  "source_id": "391",
  "detail": "INVASION OF PANAMA 1989-12-15..1990-01-03 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=391",
  "trigdate": "1989-12-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1989-12-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.panama",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Invasion Of Panama 1989",
  "search_url": "https://history.state.gov/search?q=Invasion+Of+Panama+1989&within=documents",
  "search_status": 200,
  "window": [
   "1989-11-15",
   "1990-01-14"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1940v01/d789",
    "title": "The Minister in Uruguay (Wilson) to the Secretary of State (1940, Volume I, General)",
    "page_date": "1940-05-11",
    "retrieved_at": "2026-09-02T19:53:14+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:53:14+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 391 **INVASION OF PANAMA**: INVASION OF PANAMA 1989-12-15..1990-01-03 viol 3.0 trigdate 1989-12-15, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=391

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 95: country.panama (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.panama:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Invasion Of Panama 1989` (https://history.state.gov/search?q=Invasion+Of+Panama+1989&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1989-11-15..1990-01-14. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: The Minister in Uruguay (Wilson) to the Secretary of State ( (1940-05-11)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_391_invasion_of_panama --approved-by joe`. The code never runs it.
