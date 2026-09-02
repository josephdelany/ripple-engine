# Dossier icb_374_syrian_int_lebanon — SYRIAN INT./LEBANON

```json
{
 "id": "icb_374_syrian_int_lebanon",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 374,
  "source": "icb",
  "source_id": "374",
  "detail": "SYRIAN INT./LEBANON 1987-02-15..1987-04-06 viol 3.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=374",
  "trigdate": "1987-02-15",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-02-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.syr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Syrian Int Lebanon 1987",
  "search_url": "https://history.state.gov/search?q=Syrian+Int+Lebanon+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-01-16",
   "1987-03-17"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:21+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 374 **SYRIAN INT./LEBANON**: SYRIAN INT./LEBANON 1987-02-15..1987-04-06 viol 3.0 trigdate 1987-02-15, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=374

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 652: country.syr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.syr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Syrian Int Lebanon 1987` (https://history.state.gov/search?q=Syrian+Int+Lebanon+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-01-16..1987-03-17. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_374_syrian_int_lebanon --approved-by joe`. The code never runs it.
