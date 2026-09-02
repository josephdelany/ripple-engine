# Dossier icb_406_iraq_no_fly_zone — IRAQ NO-FLY ZONE

```json
{
 "id": "icb_406_iraq_no_fly_zone",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 406,
  "source": "icb",
  "source_id": "406",
  "detail": "IRAQ NO-FLY ZONE 1992-08-18..1992-09-08 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=406",
  "trigdate": "1992-08-18",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-08-18",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iraq",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Iraq No Fly Zone 1992",
  "search_url": "https://history.state.gov/search?q=Iraq+No+Fly+Zone+1992&within=documents",
  "search_status": 200,
  "window": [
   "1992-07-19",
   "1992-09-17"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:06+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 406 **IRAQ NO-FLY ZONE**: IRAQ NO-FLY ZONE 1992-08-18..1992-09-08 viol 1.0 trigdate 1992-08-18, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=406

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iraq:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Iraq No Fly Zone 1992` (https://history.state.gov/search?q=Iraq+No+Fly+Zone+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1992-07-19..1992-09-17. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_406_iraq_no_fly_zone --approved-by joe`. The code never runs it.
