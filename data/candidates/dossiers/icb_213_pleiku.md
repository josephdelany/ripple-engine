# Dossier icb_213_pleiku — PLEIKU

```json
{
 "id": "icb_213_pleiku",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:41+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 213,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=213",
  "trigdate": "1965-02-07",
  "termdate": "1965-03-28",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1965-02-07",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
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
 "unmapped_ccodes": [
  817
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v02/d83",
  "title": "83. Editorial Note (1964\u20131968, Volume II, Vietnam, January\u2013June 1965)",
  "date": "1965-02-08",
  "window": [
   "1965-01-08",
   "1965-04-27"
  ],
  "query": "Pleiku 1965",
  "search_url": "https://history.state.gov/search?q=Pleiku+1965&within=documents",
  "retrieved_at": "2026-09-02T19:15:41+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v02/d83",
    "title": "83. Editorial Note (1964\u20131968, Volume II, Vietnam, January\u2013June 1965)",
    "page_date": "1965-02-08",
    "retrieved_at": "2026-09-02T19:15:41+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 213 **PLEIKU**: trigdate 1965-02-07, termdate 1965-03-28, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=213

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 816: country.vietnam
- 817: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.vietnam:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:41+00:00: **83. Editorial Note (1964–1968, Volume II, Vietnam, January–June 1965)** — page date 1965-02-08 (window 1965-01-08..1965-04-27)
  https://history.state.gov/historicaldocuments/frus1964-68v02/d83
- search: https://history.state.gov/search?q=Pleiku+1965&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_213_pleiku --approved-by joe`. The code never runs it.
