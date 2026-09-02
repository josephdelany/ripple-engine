# Dossier icb_222_six_day_war — SIX DAY WAR

```json
{
 "id": "icb_222_six_day_war",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:54+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 222,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=222",
  "trigdate": "1967-05-17",
  "termdate": "1967-06-11",
  "viol": 4,
  "forout": 5
 },
 "event_date": "1967-05-17",
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
   "entity": "country.russia",
   "role": "target"
  },
  {
   "entity": "country.egypt",
   "role": "actor"
  },
  {
   "entity": "country.syr",
   "role": "target"
  },
  {
   "entity": "country.jor",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v21/d21",
  "title": "21. Editorial Note (1964\u20131968, Volume XXI, Near East Region; Arabian Peninsula)",
  "date": "1967-06-05",
  "window": [
   "1967-04-17",
   "1967-07-11"
  ],
  "query": "Six Day War 1967",
  "search_url": "https://history.state.gov/search?q=Six+Day+War+1967&within=documents",
  "retrieved_at": "2026-09-02T19:15:53+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v21/d21",
    "title": "21. Editorial Note (1964\u20131968, Volume XXI, Near East Region; Arabian Peninsula)",
    "page_date": "1967-06-05",
    "retrieved_at": "2026-09-02T19:15:53+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 222 **SIX DAY WAR**: trigdate 1967-05-17, termdate 1967-06-11, viol 4, forout 5. Page: https://www.icb.umd.edu/dataviewer/?crisno=222

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 365: country.russia (registered state set)
- 651: country.egypt (registered state set)
- 652: country.syr (registered state set)
- 663: country.jor (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.russia:target, country.egypt:actor, country.syr:target, country.jor:target, country.israel:target

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:53+00:00: **21. Editorial Note (1964–1968, Volume XXI, Near East Region; Arabian Peninsula)** — page date 1967-06-05 (window 1967-04-17..1967-07-11)
  https://history.state.gov/historicaldocuments/frus1964-68v21/d21
- search: https://history.state.gov/search?q=Six+Day+War+1967&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_222_six_day_war --approved-by joe`. The code never runs it.
