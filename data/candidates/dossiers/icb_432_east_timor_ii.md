# Dossier icb_432_east_timor_ii — EAST TIMOR II

```json
{
 "id": "icb_432_east_timor_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 432,
  "source": "icb",
  "source_id": "432",
  "detail": "EAST TIMOR II 1999-09-04..1999-10-19 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=432",
  "trigdate": "1999-09-04",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1999-09-04",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.indonesia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  900
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "East Timor Ii 1999",
  "search_url": "https://history.state.gov/search?q=East+Timor+Ii+1999&within=documents",
  "search_status": 200,
  "window": [
   "1999-08-05",
   "1999-10-04"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:56:08+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 432 **EAST TIMOR II**: EAST TIMOR II 1999-09-04..1999-10-19 viol 2.0 trigdate 1999-09-04, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=432

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 850: country.indonesia (registered state set)
- 900: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.indonesia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `East Timor Ii 1999` (https://history.state.gov/search?q=East+Timor+Ii+1999&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1999-08-05..1999-10-04. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_432_east_timor_ii --approved-by joe`. The code never runs it.
