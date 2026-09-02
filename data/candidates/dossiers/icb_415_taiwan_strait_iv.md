# Dossier icb_415_taiwan_strait_iv — TAIWAN STRAIT IV

```json
{
 "id": "icb_415_taiwan_strait_iv",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 415,
  "source": "icb",
  "source_id": "415",
  "detail": "TAIWAN STRAIT IV 1995-05-22..1996-03-25 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=415",
  "trigdate": "1995-05-22",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1995-05-22",
 "date_precision": "day",
 "proposed_class": "chokepoint_disruption",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "unknown"
  },
  {
   "entity": "country.taiwan",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Taiwan Strait Iv 1995",
  "search_url": "https://history.state.gov/search?q=Taiwan+Strait+Iv+1995&within=documents",
  "search_status": 200,
  "window": [
   "1995-04-22",
   "1995-06-21"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:02+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 415 **TAIWAN STRAIT IV**: TAIWAN STRAIT IV 1995-05-22..1996-03-25 viol 1.0 trigdate 1995-05-22, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=415

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 713: country.taiwan

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `chokepoint_disruption`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.china:unknown, country.taiwan:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Taiwan Strait Iv 1995` (https://history.state.gov/search?q=Taiwan+Strait+Iv+1995&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1995-04-22..1995-06-21. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_415_taiwan_strait_iv --approved-by joe`. The code never runs it.
