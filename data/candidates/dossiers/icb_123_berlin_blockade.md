# Dossier icb_123_berlin_blockade — BERLIN BLOCKADE

```json
{
 "id": "icb_123_berlin_blockade",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:11+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 123,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=123",
  "trigdate": "1948-06-07",
  "termdate": "1949-05-12",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1948-06-07",
 "date_precision": "day",
 "proposed_class": "chokepoint_disruption",
 "proposed_severity": 3,
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
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1949v03/d408",
  "title": "Report to the National Security Council by the Acting Secretary of Defense (1949, Volume III, Council of Foreign Ministers; Germany and Austria)",
  "date": "1949-06-01",
  "window": [
   "1948-05-08",
   "1949-06-11"
  ],
  "query": "Berlin Blockade 1948",
  "search_url": "https://history.state.gov/search?q=Berlin+Blockade+1948&within=documents",
  "retrieved_at": "2026-09-02T19:13:10+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v02/d516",
    "title": "Editorial Note (1948, Volume II, Germany and Austria)",
    "page_date": "1945-07-01",
    "retrieved_at": "2026-09-02T19:13:09+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1950v04/d475",
    "title": "Editorial Note (1950, Volume IV, Central and Eastern Europe; The Soviet Union)",
    "page_date": "1950-02-21",
    "retrieved_at": "2026-09-02T19:13:10+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1949v03/d408",
    "title": "Report to the National Security Council by the Acting Secretary of Defense (1949, Volume III, Council of Foreign Ministers; Germany and Austria)",
    "page_date": "1949-06-01",
    "retrieved_at": "2026-09-02T19:13:10+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 123 **BERLIN BLOCKADE**: trigdate 1948-06-07, termdate 1949-05-12, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=123

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `chokepoint_disruption`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.gbr:target, country.fra:target, country.russia:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:10+00:00: **Report to the National Security Council by the Acting Secretary of Defense (1949, Volume III, Council of Foreign Ministers; Germany and Austria)** — page date 1949-06-01 (window 1948-05-08..1949-06-11)
  https://history.state.gov/historicaldocuments/frus1949v03/d408
- search: https://history.state.gov/search?q=Berlin+Blockade+1948&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_123_berlin_blockade --approved-by joe`. The code never runs it.
