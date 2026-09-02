# Dossier icb_325_essequibo_ii — ESSEQUIBO II

```json
{
 "id": "icb_325_essequibo_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:02+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 325,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=325",
  "trigdate": "1981-04-04",
  "termdate": "1983-03-01",
  "viol": 1,
  "forout": 2
 },
 "event_date": "1981-04-04",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.venezuela",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  110
 ],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Essequibo Ii 1981",
  "search_url": "https://history.state.gov/search?q=Essequibo+Ii+1981&within=documents",
  "search_status": 200,
  "window": [
   "1981-03-05",
   "1983-03-31"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:01+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 325 **ESSEQUIBO II**: trigdate 1981-04-04, termdate 1983-03-01, viol 1, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=325

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 101: country.venezuela (registered state set)
- 110: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.venezuela:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Essequibo Ii 1981` (https://history.state.gov/search?q=Essequibo+Ii+1981&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1981-03-05..1983-03-31.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_325_essequibo_ii --approved-by joe`. The code never runs it.
