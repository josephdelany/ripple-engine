# Dossier icb_116_indonesia_indep_ii — INDONESIA INDEP. II

```json
{
 "id": "icb_116_indonesia_indep_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:01+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 116,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=116",
  "trigdate": "1947-07-21",
  "termdate": "1948-01-17",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1947-07-21",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.indonesia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Indonesia Indep  Ii 1947",
  "search_url": "https://history.state.gov/search?q=Indonesia+Indep++Ii+1947&within=documents",
  "search_status": 200,
  "window": [
   "1947-06-21",
   "1948-02-16"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:13:00+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 116 **INDONESIA INDEP. II**: trigdate 1947-07-21, termdate 1948-01-17, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=116

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 210: UNMAPPED
- 850: country.indonesia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.indonesia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Indonesia Indep  Ii 1947` (https://history.state.gov/search?q=Indonesia+Indep++Ii+1947&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1947-06-21..1948-02-16.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_116_indonesia_indep_ii --approved-by joe`. The code never runs it.
