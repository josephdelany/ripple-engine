# Dossier icb_422_unscom_i — UNSCOM I

```json
{
 "id": "icb_422_unscom_i",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 422,
  "source": "icb",
  "source_id": "422",
  "detail": "UNSCOM I 1997-11-13..1998-02-23 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=422",
  "trigdate": "1997-11-13",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1997-11-13",
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
   "entity": "country.iraq",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Unscom I 1997",
  "search_url": "https://history.state.gov/search?q=Unscom+I+1997&within=documents",
  "search_status": 200,
  "window": [
   "1997-10-14",
   "1997-12-13"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:38+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 422 **UNSCOM I**: UNSCOM I 1997-11-13..1998-02-23 viol 1.0 trigdate 1997-11-13, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=422

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 645: country.iraq (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.iraq:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Unscom I 1997` (https://history.state.gov/search?q=Unscom+I+1997&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1997-10-14..1997-12-13. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_422_unscom_i --approved-by joe`. The code never runs it.
