# Dossier icb_402_egypt_sudan_bdr_ii — EGYPT/SUDAN BDR. II

```json
{
 "id": "icb_402_egypt_sudan_bdr_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 402,
  "source": "icb",
  "source_id": "402",
  "detail": "EGYPT/SUDAN BDR. II 1992-01-28..1992-06-28 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=402",
  "trigdate": "1992-01-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-01-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.sudan",
   "role": "unknown"
  },
  {
   "entity": "country.egypt",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Egypt Sudan Bdr  Ii 1992",
  "search_url": "https://history.state.gov/search?q=Egypt+Sudan+Bdr++Ii+1992&within=documents",
  "search_status": 200,
  "window": [
   "1991-12-29",
   "1992-02-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:55+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 402 **EGYPT/SUDAN BDR. II**: EGYPT/SUDAN BDR. II 1992-01-28..1992-06-28 viol 2.0 trigdate 1992-01-28, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=402

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 625: country.sudan
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.sudan:unknown, country.egypt:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Egypt Sudan Bdr  Ii 1992` (https://history.state.gov/search?q=Egypt+Sudan+Bdr++Ii+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1991-12-29..1992-02-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_402_egypt_sudan_bdr_ii --approved-by joe`. The code never runs it.
