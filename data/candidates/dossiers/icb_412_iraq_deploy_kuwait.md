# Dossier icb_412_iraq_deploy_kuwait — IRAQ DEPLOY./KUWAIT

```json
{
 "id": "icb_412_iraq_deploy_kuwait",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 412,
  "source": "icb",
  "source_id": "412",
  "detail": "IRAQ DEPLOY./KUWAIT 1994-10-07..1994-11-10 viol 1.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=412",
  "trigdate": "1994-10-07",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1994-10-07",
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
  },
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  },
  {
   "entity": "country.kuwait",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Iraq Deploy Kuwait 1994",
  "search_url": "https://history.state.gov/search?q=Iraq+Deploy+Kuwait+1994&within=documents",
  "search_status": 200,
  "window": [
   "1994-09-07",
   "1994-11-06"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:46+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 412 **IRAQ DEPLOY./KUWAIT**: IRAQ DEPLOY./KUWAIT 1994-10-07..1994-11-10 viol 1.0 trigdate 1994-10-07, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=412

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 645: country.iraq (registered state set)
- 670: country.saudi_arabia (registered state set)
- 690: country.kuwait (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.iraq:unknown, country.saudi_arabia:unknown, country.kuwait:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Iraq Deploy Kuwait 1994` (https://history.state.gov/search?q=Iraq+Deploy+Kuwait+1994&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1994-09-07..1994-11-06. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_412_iraq_deploy_kuwait --approved-by joe`. The code never runs it.
