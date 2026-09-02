# Dossier icb_416_red_sea_islands — RED SEA ISLANDS

```json
{
 "id": "icb_416_red_sea_islands",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 416,
  "source": "icb",
  "source_id": "416",
  "detail": "RED SEA ISLANDS 1995-12-15..1995-12-28 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=416",
  "trigdate": "1995-12-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1995-12-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.yemen",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  531
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Red Sea Islands 1995",
  "search_url": "https://history.state.gov/search?q=Red+Sea+Islands+1995&within=documents",
  "search_status": 200,
  "window": [
   "1995-11-15",
   "1996-01-14"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:05+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 416 **RED SEA ISLANDS**: RED SEA ISLANDS 1995-12-15..1995-12-28 viol 2.0 trigdate 1995-12-15, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=416

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 531: UNMAPPED (registered state set)
- 678: country.yemen (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.yemen:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Red Sea Islands 1995` (https://history.state.gov/search?q=Red+Sea+Islands+1995&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1995-11-15..1996-01-14. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_416_red_sea_islands --approved-by joe`. The code never runs it.
