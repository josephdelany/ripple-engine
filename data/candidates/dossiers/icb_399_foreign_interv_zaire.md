# Dossier icb_399_foreign_interv_zaire — FOREIGN INTERV.-ZAIRE

```json
{
 "id": "icb_399_foreign_interv_zaire",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 399,
  "source": "icb",
  "source_id": "399",
  "detail": "FOREIGN INTERV.-ZAIRE 1991-09-23..1991-11-04 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=399",
  "trigdate": "1991-09-23",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1991-09-23",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.congo_drc",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  211
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Foreign Interv Zaire 1991",
  "search_url": "https://history.state.gov/search?q=Foreign+Interv+Zaire+1991&within=documents",
  "search_status": 200,
  "window": [
   "1991-08-24",
   "1991-10-23"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:48+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 399 **FOREIGN INTERV.-ZAIRE**: FOREIGN INTERV.-ZAIRE 1991-09-23..1991-11-04 viol 3.0 trigdate 1991-09-23, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=399

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 211: UNMAPPED
- 220: country.fra (registered state set)
- 490: country.congo_drc

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.fra:unknown, country.congo_drc:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Foreign Interv Zaire 1991` (https://history.state.gov/search?q=Foreign+Interv+Zaire+1991&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1991-08-24..1991-10-23. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_399_foreign_interv_zaire --approved-by joe`. The code never runs it.
