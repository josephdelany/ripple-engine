# Dossier icb_255_october_yom_kippur_war — OCTOBER-YOM KIPPUR WAR

```json
{
 "id": "icb_255_october_yom_kippur_war",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:02+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 255,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=255",
  "trigdate": "1973-10-05",
  "termdate": "1974-05-28",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1973-10-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  },
  {
   "entity": "country.egypt",
   "role": "unknown"
  },
  {
   "entity": "country.syr",
   "role": "unknown"
  },
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1969-76v36/d209",
  "title": "209. Editorial Note (1969\u20131976, Volume XXXVI, Energy Crisis, 1969\u20131974)",
  "date": "1973-10-06",
  "window": [
   "1973-09-05",
   "1974-06-27"
  ],
  "query": "October Yom Kippur War 1973",
  "search_url": "https://history.state.gov/search?q=October+Yom+Kippur+War+1973&within=documents",
  "retrieved_at": "2026-09-02T19:17:02+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1969-76v36/d209",
    "title": "209. Editorial Note (1969\u20131976, Volume XXXVI, Energy Crisis, 1969\u20131974)",
    "page_date": "1973-10-06",
    "retrieved_at": "2026-09-02T19:17:02+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 255 **OCTOBER-YOM KIPPUR WAR**: trigdate 1973-10-05, termdate 1974-05-28, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=255

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 365: country.russia (registered state set)
- 651: country.egypt (registered state set)
- 652: country.syr (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.russia:unknown, country.egypt:unknown, country.syr:unknown, country.israel:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:02+00:00: **209. Editorial Note (1969–1976, Volume XXXVI, Energy Crisis, 1969–1974)** — page date 1973-10-06 (window 1973-09-05..1974-06-27)
  https://history.state.gov/historicaldocuments/frus1969-76v36/d209
- search: https://history.state.gov/search?q=October+Yom+Kippur+War+1973&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_255_october_yom_kippur_war --approved-by joe`. The code never runs it.
