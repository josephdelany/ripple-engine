# Dossier icb_379_mecca_pilgrimage — MECCA PILGRIMAGE

```json
{
 "id": "icb_379_mecca_pilgrimage",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 379,
  "source": "icb",
  "source_id": "379",
  "detail": "MECCA PILGRIMAGE 1987-07-28..1987-10-01 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=379",
  "trigdate": "1987-07-28",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-07-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.iran",
   "role": "unknown"
  },
  {
   "entity": "country.saudi_arabia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Mecca Pilgrimage 1987",
  "search_url": "https://history.state.gov/search?q=Mecca+Pilgrimage+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-06-28",
   "1987-08-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:35+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 379 **MECCA PILGRIMAGE**: MECCA PILGRIMAGE 1987-07-28..1987-10-01 viol 3.0 trigdate 1987-07-28, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=379

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 630: country.iran (registered state set)
- 670: country.saudi_arabia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.iran:unknown, country.saudi_arabia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Mecca Pilgrimage 1987` (https://history.state.gov/search?q=Mecca+Pilgrimage+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-06-28..1987-08-27. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_379_mecca_pilgrimage --approved-by joe`. The code never runs it.
