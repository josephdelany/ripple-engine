# Dossier icb_424_ethiopia_eritrea_i — ETHIOPIA-ERITREA I

```json
{
 "id": "icb_424_ethiopia_eritrea_i",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 424,
  "source": "icb",
  "source_id": "424",
  "detail": "ETHIOPIA-ERITREA I 1998-05-06..2000-12-12 viol 4.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=424",
  "trigdate": "1998-05-06",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-05-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  530,
  531
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Ethiopia Eritrea I 1998",
  "search_url": "https://history.state.gov/search?q=Ethiopia+Eritrea+I+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-04-06",
   "1998-06-05"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:40+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 424 **ETHIOPIA-ERITREA I**: ETHIOPIA-ERITREA I 1998-05-06..2000-12-12 viol 4.0 trigdate 1998-05-06, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=424

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)
- 531: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ethiopia Eritrea I 1998` (https://history.state.gov/search?q=Ethiopia+Eritrea+I+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-04-06..1998-06-05. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_424_ethiopia_eritrea_i --approved-by joe`. The code never runs it.
