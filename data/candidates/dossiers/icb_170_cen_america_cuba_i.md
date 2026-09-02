# Dossier icb_170_cen_america_cuba_i — CEN. AMERICA/CUBA I

```json
{
 "id": "icb_170_cen_america_cuba_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:24+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 170,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=170",
  "trigdate": "1959-04-25",
  "termdate": "1959-12-28",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1959-04-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.panama",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  41,
  42,
  93
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Cen  America Cuba I 1959",
  "search_url": "https://history.state.gov/search?q=Cen++America+Cuba+I+1959&within=documents",
  "search_status": 200,
  "window": [
   "1959-03-26",
   "1960-01-27"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:24+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 170 **CEN. AMERICA/CUBA I**: trigdate 1959-04-25, termdate 1959-12-28, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=170

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 41: UNMAPPED
- 42: UNMAPPED
- 93: UNMAPPED
- 95: country.panama (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.panama:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cen  America Cuba I 1959` (https://history.state.gov/search?q=Cen++America+Cuba+I+1959&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1959-03-26..1960-01-27.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_170_cen_america_cuba_i --approved-by joe`. The code never runs it.
