# Dossier icb_291_cassinga_incident — CASSINGA INCIDENT

```json
{
 "id": "icb_291_cassinga_incident",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:58+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 291,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=291",
  "trigdate": "1978-05-03",
  "termdate": "1978-05-17",
  "viol": 3,
  "forout": 2
 },
 "event_date": "1978-05-03",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ago",
   "role": "unknown"
  },
  {
   "entity": "country.south_africa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Cassinga Incident 1978",
  "search_url": "https://history.state.gov/search?q=Cassinga+Incident+1978&within=documents",
  "search_status": 200,
  "window": [
   "1978-04-03",
   "1978-06-16"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:17:58+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 291 **CASSINGA INCIDENT**: trigdate 1978-05-03, termdate 1978-05-17, viol 3, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=291

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 540: country.ago (registered state set)
- 560: country.south_africa

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.ago:unknown, country.south_africa:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Cassinga Incident 1978` (https://history.state.gov/search?q=Cassinga+Incident+1978&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1978-04-03..1978-06-16.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_291_cassinga_incident --approved-by joe`. The code never runs it.
