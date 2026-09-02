# Dossier icb_409_optn_accountability — OPTN. ACCOUNTABILITY

```json
{
 "id": "icb_409_optn_accountability",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 409,
  "source": "icb",
  "source_id": "409",
  "detail": "OPTN. ACCOUNTABILITY 1993-07-10..1993-07-28 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=409",
  "trigdate": "1993-07-10",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1993-07-10",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.lebanon",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Optn  Accountability 1993",
  "search_url": "https://history.state.gov/search?q=Optn++Accountability+1993&within=documents",
  "search_status": 200,
  "window": [
   "1993-06-10",
   "1993-08-09"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:23+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 409 **OPTN. ACCOUNTABILITY**: OPTN. ACCOUNTABILITY 1993-07-10..1993-07-28 viol 2.0 trigdate 1993-07-10, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=409

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 660: country.lebanon (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.lebanon:unknown, country.israel:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Optn  Accountability 1993` (https://history.state.gov/search?q=Optn++Accountability+1993&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1993-06-10..1993-08-09. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_409_optn_accountability --approved-by joe`. The code never runs it.
