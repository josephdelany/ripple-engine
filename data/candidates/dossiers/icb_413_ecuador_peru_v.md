# Dossier icb_413_ecuador_peru_v — ECUADOR/PERU V

```json
{
 "id": "icb_413_ecuador_peru_v",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 413,
  "source": "icb",
  "source_id": "413",
  "detail": "ECUADOR/PERU V 1995-01-09..1995-03-01 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=413",
  "trigdate": "1995-01-09",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1995-01-09",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ecuador",
   "role": "unknown"
  },
  {
   "entity": "country.peru",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Ecuador Peru V 1995",
  "search_url": "https://history.state.gov/search?q=Ecuador+Peru+V+1995&within=documents",
  "search_status": 200,
  "window": [
   "1994-12-10",
   "1995-02-08"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:55+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 413 **ECUADOR/PERU V**: ECUADOR/PERU V 1995-01-09..1995-03-01 viol 3.0 trigdate 1995-01-09, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=413

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 130: country.ecuador (registered state set)
- 135: country.peru

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.ecuador:unknown, country.peru:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Ecuador Peru V 1995` (https://history.state.gov/search?q=Ecuador+Peru+V+1995&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1994-12-10..1995-02-08. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_413_ecuador_peru_v --approved-by joe`. The code never runs it.
