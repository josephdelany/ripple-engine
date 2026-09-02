# Dossier icb_347_operation_askari — OPERATION ASKARI

```json
{
 "id": "icb_347_operation_askari",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:32+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 347,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=347",
  "trigdate": "1983-12-06",
  "termdate": "1984-02-16",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1983-12-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ago",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Operation Askari 1983",
  "search_url": "https://history.state.gov/search?q=Operation+Askari+1983&within=documents",
  "search_status": 200,
  "window": [
   "1983-11-06",
   "1984-03-17"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:32+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 347 **OPERATION ASKARI**: trigdate 1983-12-06, termdate 1984-02-16, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=347

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.ago:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Operation Askari 1983` (https://history.state.gov/search?q=Operation+Askari+1983&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1983-11-06..1984-03-17.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_347_operation_askari --approved-by joe`. The code never runs it.
