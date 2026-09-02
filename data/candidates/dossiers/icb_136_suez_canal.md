# Dossier icb_136_suez_canal — SUEZ CANAL

```json
{
 "id": "icb_136_suez_canal",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:31+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 136,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=136",
  "trigdate": "1951-07-28",
  "termdate": "1952-01-28",
  "viol": 3,
  "forout": 2
 },
 "event_date": "1951-07-28",
 "date_precision": "day",
 "proposed_class": "chokepoint_disruption",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "actor"
  },
  {
   "entity": "country.egypt",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1951v05/d464",
  "title": "The Ambassador in Egypt (Caffery) to the Department of State (1951, Volume V, The Near East and Africa)",
  "date": "1951-08-13",
  "window": [
   "1951-06-28",
   "1952-02-27"
  ],
  "query": "Suez Canal 1951",
  "search_url": "https://history.state.gov/search?q=Suez+Canal+1951&within=documents",
  "retrieved_at": "2026-09-02T19:13:31+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1951v05/d464",
    "title": "The Ambassador in Egypt (Caffery) to the Department of State (1951, Volume V, The Near East and Africa)",
    "page_date": "1951-08-13",
    "retrieved_at": "2026-09-02T19:13:31+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 136 **SUEZ CANAL**: trigdate 1951-07-28, termdate 1952-01-28, viol 3, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=136

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `chokepoint_disruption`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.gbr:actor, country.egypt:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:31+00:00: **The Ambassador in Egypt (Caffery) to the Department of State (1951, Volume V, The Near East and Africa)** — page date 1951-08-13 (window 1951-06-28..1952-02-27)
  https://history.state.gov/historicaldocuments/frus1951v05/d464
- search: https://history.state.gov/search?q=Suez+Canal+1951&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_136_suez_canal --approved-by joe`. The code never runs it.
