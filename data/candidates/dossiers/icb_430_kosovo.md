# Dossier icb_430_kosovo — KOSOVO

```json
{
 "id": "icb_430_kosovo",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 430,
  "source": "icb",
  "source_id": "430",
  "detail": "KOSOVO 1999-02-20..1999-06-10 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=430",
  "trigdate": "1999-02-20",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1999-02-20",
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
   "entity": "country.canada",
   "role": "unknown"
  },
  {
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.serbia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210,
  211,
  230,
  235,
  260,
  325,
  339
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Kosovo 1999",
  "search_url": "https://history.state.gov/search?q=Kosovo+1999&within=documents",
  "search_status": 200,
  "window": [
   "1999-01-21",
   "1999-03-22"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:54+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 430 **KOSOVO**: KOSOVO 1999-02-20..1999-06-10 viol 3.0 trigdate 1999-02-20, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=430

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 20: country.canada (registered state set)
- 200: country.gbr (registered state set)
- 210: UNMAPPED
- 211: UNMAPPED
- 220: country.fra (registered state set)
- 230: UNMAPPED
- 235: UNMAPPED
- 260: UNMAPPED (registered state set)
- 325: UNMAPPED (registered state set)
- 339: UNMAPPED
- 345: country.serbia

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.canada:unknown, country.gbr:unknown, country.fra:unknown, country.serbia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Kosovo 1999` (https://history.state.gov/search?q=Kosovo+1999&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1999-01-21..1999-03-22. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_430_kosovo --approved-by joe`. The code never runs it.
