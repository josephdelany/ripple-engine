# Dossier icb_373_todghere_incident — TODGHERE INCIDENT

```json
{
 "id": "icb_373_todghere_incident",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 373,
  "source": "icb",
  "source_id": "373",
  "detail": "TODGHERE INCIDENT 1987-02-12..1987-04-28 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=373",
  "trigdate": "1987-02-12",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-02-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  520
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Todghere Incident 1987",
  "search_url": "https://history.state.gov/search?q=Todghere+Incident+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-01-13",
   "1987-03-14"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:20+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 373 **TODGHERE INCIDENT**: TODGHERE INCIDENT 1987-02-12..1987-04-28 viol 3.0 trigdate 1987-02-12, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=373

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 520: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Todghere Incident 1987` (https://history.state.gov/search?q=Todghere+Incident+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-01-13..1987-03-14. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_373_todghere_incident --approved-by joe`. The code never runs it.
