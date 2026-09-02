# Dossier icb_152_suez_natn_war — SUEZ NATN.-WAR

```json
{
 "id": "icb_152_suez_natn_war",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:02+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 152,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=152",
  "trigdate": "1956-07-26",
  "termdate": "1957-03-12",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1956-07-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.gbr",
   "role": "target"
  },
  {
   "entity": "country.fra",
   "role": "target"
  },
  {
   "entity": "country.russia",
   "role": "target"
  },
  {
   "entity": "country.egypt",
   "role": "actor"
  },
  {
   "entity": "country.israel",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Suez Natn War 1956",
  "search_url": "https://history.state.gov/search?q=Suez+Natn+War+1956&within=documents",
  "search_status": 200,
  "window": [
   "1956-06-26",
   "1957-04-11"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:02+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 152 **SUEZ NATN.-WAR**: trigdate 1956-07-26, termdate 1957-03-12, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=152

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 365: country.russia (registered state set)
- 651: country.egypt (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.gbr:target, country.fra:target, country.russia:target, country.egypt:actor, country.israel:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Suez Natn War 1956` (https://history.state.gov/search?q=Suez+Natn+War+1956&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1956-06-26..1957-04-11.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_152_suez_natn_war --approved-by joe`. The code never runs it.
