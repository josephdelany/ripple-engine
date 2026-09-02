# Dossier icb_304_chad_libya_iv — CHAD/LIBYA IV

```json
{
 "id": "icb_304_chad_libya_iv",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:27+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 304,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=304",
  "trigdate": "1979-04-12",
  "termdate": "1979-11-10",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1979-04-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.libya",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Chad Libya Iv 1979",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+Iv+1979&within=documents",
  "search_status": 200,
  "window": [
   "1979-03-13",
   "1979-12-10"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:18:26+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 304 **CHAD/LIBYA IV**: trigdate 1979-04-12, termdate 1979-11-10, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=304

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.fra:unknown, country.libya:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chad Libya Iv 1979` (https://history.state.gov/search?q=Chad+Libya+Iv+1979&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1979-03-13..1979-12-10.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_304_chad_libya_iv --approved-by joe`. The code never runs it.
