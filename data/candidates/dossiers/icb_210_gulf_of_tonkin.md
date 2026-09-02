# Dossier icb_210_gulf_of_tonkin — GULF OF TONKIN

```json
{
 "id": "icb_210_gulf_of_tonkin",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:32+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 210,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=210",
  "trigdate": "1964-07-28",
  "termdate": "1964-08-28",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1964-07-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.vietnam",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1917-72PubDipv07/d26",
  "title": "26. Editorial Note (1917\u20131972, Volume VII, Public Diplomacy, 1964\u20131968)",
  "date": "1964-08-05",
  "window": [
   "1964-06-28",
   "1964-09-27"
  ],
  "query": "Gulf Of Tonkin 1964",
  "search_url": "https://history.state.gov/search?q=Gulf+Of+Tonkin+1964&within=documents",
  "retrieved_at": "2026-09-02T19:15:31+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v06/d79",
    "title": "79. Editorial Note (1964\u20131968, Volume VI, Vietnam, January\u2013August 1968)",
    "page_date": "1968-02-20",
    "retrieved_at": "2026-09-02T19:15:30+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v14/d41",
    "title": "41. Editorial Note (1964\u20131968, Volume XIV, Soviet Union)",
    "page_date": "1964-10-15",
    "retrieved_at": "2026-09-02T19:15:31+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1917-72PubDipv07/d26",
    "title": "26. Editorial Note (1917\u20131972, Volume VII, Public Diplomacy, 1964\u20131968)",
    "page_date": "1964-08-05",
    "retrieved_at": "2026-09-02T19:15:31+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 210 **GULF OF TONKIN**: trigdate 1964-07-28, termdate 1964-08-28, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=210

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 816: country.vietnam

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.vietnam:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:31+00:00: **26. Editorial Note (1917–1972, Volume VII, Public Diplomacy, 1964–1968)** — page date 1964-08-05 (window 1964-06-28..1964-09-27)
  https://history.state.gov/historicaldocuments/frus1917-72PubDipv07/d26
- search: https://history.state.gov/search?q=Gulf+Of+Tonkin+1964&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_210_gulf_of_tonkin --approved-by joe`. The code never runs it.
