# Dossier icb_362_chad_libya_vii — CHAD/LIBYA VII

```json
{
 "id": "icb_362_chad_libya_vii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:45+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 362,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=362",
  "trigdate": "1986-02-10",
  "termdate": "1986-03-28",
  "viol": 3,
  "forout": 7
 },
 "event_date": "1986-02-10",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "target"
  },
  {
   "entity": "country.libya",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Chad Libya Vii 1986",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+Vii+1986&within=documents",
  "search_status": 200,
  "window": [
   "1986-01-11",
   "1986-04-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:44+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 362 **CHAD/LIBYA VII**: trigdate 1986-02-10, termdate 1986-03-28, viol 3, forout 7. Page: https://www.icb.umd.edu/dataviewer/?crisno=362

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.fra:target, country.libya:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chad Libya Vii 1986` (https://history.state.gov/search?q=Chad+Libya+Vii+1986&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-01-11..1986-04-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_362_chad_libya_vii --approved-by joe`. The code never runs it.
