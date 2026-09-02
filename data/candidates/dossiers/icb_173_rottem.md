# Dossier icb_173_rottem — ROTTEM

```json
{
 "id": "icb_173_rottem",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:31+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 173,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=173",
  "trigdate": "1960-02-15",
  "termdate": "1960-03-08",
  "viol": 1,
  "forout": 3
 },
 "event_date": "1960-02-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.egypt",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Rottem 1960",
  "search_url": "https://history.state.gov/search?q=Rottem+1960&within=documents",
  "search_status": 200,
  "window": [
   "1960-01-16",
   "1960-04-07"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:30+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 173 **ROTTEM**: trigdate 1960-02-15, termdate 1960-03-08, viol 1, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=173

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 651: country.egypt (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.egypt:target, country.israel:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Rottem 1960` (https://history.state.gov/search?q=Rottem+1960&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1960-01-16..1960-04-07.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_173_rottem --approved-by joe`. The code never runs it.
