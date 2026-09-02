# Dossier icb_313_operation_smokeshell — OPERATION SMOKESHELL

```json
{
 "id": "icb_313_operation_smokeshell",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:38+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 313,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=313",
  "trigdate": "1980-06-07",
  "termdate": "1980-07-02",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1980-06-07",
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
  "query": "Operation Smokeshell 1980",
  "search_url": "https://history.state.gov/search?q=Operation+Smokeshell+1980&within=documents",
  "search_status": 200,
  "window": [
   "1980-05-08",
   "1980-08-01"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:18:38+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 313 **OPERATION SMOKESHELL**: trigdate 1980-06-07, termdate 1980-07-02, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=313

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.ago:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Operation Smokeshell 1980` (https://history.state.gov/search?q=Operation+Smokeshell+1980&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1980-05-08..1980-08-01.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_313_operation_smokeshell --approved-by joe`. The code never runs it.
