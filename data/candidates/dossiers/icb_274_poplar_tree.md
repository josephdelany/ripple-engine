# Dossier icb_274_poplar_tree — POPLAR TREE

```json
{
 "id": "icb_274_poplar_tree",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:31+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 274,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=274",
  "trigdate": "1976-08-17",
  "termdate": "1976-09-16",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1976-08-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  731
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Poplar Tree 1976",
  "search_url": "https://history.state.gov/search?q=Poplar+Tree+1976&within=documents",
  "search_status": 200,
  "window": [
   "1976-07-18",
   "1976-10-16"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:17:31+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 274 **POPLAR TREE**: trigdate 1976-08-17, termdate 1976-09-16, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=274

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 731: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Poplar Tree 1976` (https://history.state.gov/search?q=Poplar+Tree+1976&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1976-07-18..1976-10-16.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_274_poplar_tree --approved-by joe`. The code never runs it.
