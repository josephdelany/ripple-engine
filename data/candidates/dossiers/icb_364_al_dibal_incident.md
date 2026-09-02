# Dossier icb_364_al_dibal_incident — AL-DIBAL INCIDENT

```json
{
 "id": "icb_364_al_dibal_incident",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:47+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 364,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=364",
  "trigdate": "1986-04-26",
  "termdate": "1986-06-15",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1986-04-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.bhr",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Al Dibal Incident 1986",
  "search_url": "https://history.state.gov/search?q=Al+Dibal+Incident+1986&within=documents",
  "search_status": 200,
  "window": [
   "1986-03-27",
   "1986-07-15"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:47+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 364 **AL-DIBAL INCIDENT**: trigdate 1986-04-26, termdate 1986-06-15, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=364

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 692: country.bhr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.bhr:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Al Dibal Incident 1986` (https://history.state.gov/search?q=Al+Dibal+Incident+1986&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1986-03-27..1986-07-15.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_364_al_dibal_incident --approved-by joe`. The code never runs it.
