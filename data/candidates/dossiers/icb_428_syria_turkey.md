# Dossier icb_428_syria_turkey — SYRIA/TURKEY

```json
{
 "id": "icb_428_syria_turkey",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 428,
  "source": "icb",
  "source_id": "428",
  "detail": "SYRIA/TURKEY 1998-10-01..1998-10-20 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=428",
  "trigdate": "1998-10-01",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-10-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.syr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Syria Turkey 1998",
  "search_url": "https://history.state.gov/search?q=Syria+Turkey+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-09-01",
   "1998-10-31"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:50+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 428 **SYRIA/TURKEY**: SYRIA/TURKEY 1998-10-01..1998-10-20 viol 1.0 trigdate 1998-10-01, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=428

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.syr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Syria Turkey 1998` (https://history.state.gov/search?q=Syria+Turkey+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-09-01..1998-10-31. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_428_syria_turkey --approved-by joe`. The code never runs it.
