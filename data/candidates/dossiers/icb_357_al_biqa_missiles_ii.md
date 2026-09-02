# Dossier icb_357_al_biqa_missiles_ii — AL-BIQA MISSILES II

```json
{
 "id": "icb_357_al_biqa_missiles_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:41+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 357,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=357",
  "trigdate": "1985-11-19",
  "termdate": "1986-01-15",
  "viol": 2,
  "forout": 3
 },
 "event_date": "1985-11-19",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.syr",
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
  "query": "Al Biqa Missiles Ii 1985",
  "search_url": "https://history.state.gov/search?q=Al+Biqa+Missiles+Ii+1985&within=documents",
  "search_status": 200,
  "window": [
   "1985-10-20",
   "1986-02-14"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:19:40+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 357 **AL-BIQA MISSILES II**: trigdate 1985-11-19, termdate 1986-01-15, viol 2, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=357

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 652: country.syr (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.syr:target, country.israel:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Al Biqa Missiles Ii 1985` (https://history.state.gov/search?q=Al+Biqa+Missiles+Ii+1985&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1985-10-20..1986-02-14.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_357_al_biqa_missiles_ii --approved-by joe`. The code never runs it.
