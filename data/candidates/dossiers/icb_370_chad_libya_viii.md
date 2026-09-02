# Dossier icb_370_chad_libya_viii — CHAD/LIBYA VIII

```json
{
 "id": "icb_370_chad_libya_viii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:48+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 370,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=370",
  "trigdate": "1986-12-12",
  "termdate": "1987-09-11",
  "viol": 4,
  "forout": 2
 },
 "event_date": "1986-12-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
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
  "query": "Chad Libya Viii 1986",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+Viii+1986&within=documents",
  "search_status": 200,
  "window": [
   "1986-11-12",
   "1987-10-11"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:48+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 370 **CHAD/LIBYA VIII**: trigdate 1986-12-12, termdate 1987-09-11, viol 4, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=370

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.libya:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chad Libya Viii 1986` (https://history.state.gov/search?q=Chad+Libya+Viii+1986&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-11-12..1987-10-11.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_370_chad_libya_viii --approved-by joe`. The code never runs it.
