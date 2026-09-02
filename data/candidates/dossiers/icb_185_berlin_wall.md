# Dossier icb_185_berlin_wall — BERLIN WALL

```json
{
 "id": "icb_185_berlin_wall",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:49+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 185,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=185",
  "trigdate": "1961-08-28",
  "termdate": "1961-10-28",
  "viol": 1,
  "forout": 3
 },
 "event_date": "1961-08-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.gbr",
   "role": "unknown"
  },
  {
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  260,
  265
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v14/d104",
  "title": "104. Editorial Note (1961\u20131963, Volume XIV, Berlin Crisis, 1961\u20131962)",
  "date": "1961-08-13",
  "window": [
   "1961-07-29",
   "1961-11-27"
  ],
  "query": "Berlin Wall 1961",
  "search_url": "https://history.state.gov/search?q=Berlin+Wall+1961&within=documents",
  "retrieved_at": "2026-09-02T19:14:49+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v14/d311",
    "title": "311. Telegram From the Department of State to the Mission at Berlin (1961\u20131963, Volume XIV, Berlin Crisis, 1961\u20131962)",
    "page_date": "1962-03-03",
    "retrieved_at": "2026-09-02T19:14:47+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v10/d289",
    "title": "289. Telegram From the Mission in West Berlin to the Department of State and the Embassy in the Federal Republic of Germany (1981\u20131988, Volume X, Eastern Europe)",
    "page_date": "1986-08-12",
    "retrieved_at": "2026-09-02T19:14:47+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v10/d288",
    "title": "288. Telegram From the Mission in West Berlin to the Department of State and the Embassy in the Federal Republic of Germany (1981\u20131988, Volume X, Eastern Europe)",
    "page_date": "1986-08-12",
    "retrieved_at": "2026-09-02T19:14:48+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v14/d104",
    "title": "104. Editorial Note (1961\u20131963, Volume XIV, Berlin Crisis, 1961\u20131962)",
    "page_date": "1961-08-13",
    "retrieved_at": "2026-09-02T19:14:49+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 185 **BERLIN WALL**: trigdate 1961-08-28, termdate 1961-10-28, viol 1, forout 3. Page: https://www.icb.umd.edu/dataviewer/?crisno=185

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 200: country.gbr (registered state set)
- 220: country.fra (registered state set)
- 260: UNMAPPED (registered state set)
- 265: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.gbr:unknown, country.fra:unknown, country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:49+00:00: **104. Editorial Note (1961–1963, Volume XIV, Berlin Crisis, 1961–1962)** — page date 1961-08-13 (window 1961-07-29..1961-11-27)
  https://history.state.gov/historicaldocuments/frus1961-63v14/d104
- search: https://history.state.gov/search?q=Berlin+Wall+1961&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_185_berlin_wall --approved-by joe`. The code never runs it.
