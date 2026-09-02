# Dossier icb_225_tet_offensive — TET OFFENSIVE

```json
{
 "id": "icb_225_tet_offensive",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:59+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 225,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=225",
  "trigdate": "1968-01-28",
  "termdate": "1968-03-28",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1968-01-28",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  817
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1964-68v06/d32",
  "title": "32. Editorial Note (1964\u20131968, Volume VI, Vietnam, January\u2013August 1968)",
  "date": "1968-04-08",
  "window": [
   "1967-12-29",
   "1968-04-27"
  ],
  "query": "Tet Offensive 1968",
  "search_url": "https://history.state.gov/search?q=Tet+Offensive+1968&within=documents",
  "retrieved_at": "2026-09-02T19:15:59+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v06/d32",
    "title": "32. Editorial Note (1964\u20131968, Volume VI, Vietnam, January\u2013August 1968)",
    "page_date": "1968-04-08",
    "retrieved_at": "2026-09-02T19:15:59+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 225 **TET OFFENSIVE**: trigdate 1968-01-28, termdate 1968-03-28, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=225

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 817: UNMAPPED

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:59+00:00: **32. Editorial Note (1964–1968, Volume VI, Vietnam, January–August 1968)** — page date 1968-04-08 (window 1967-12-29..1968-04-27)
  https://history.state.gov/historicaldocuments/frus1964-68v06/d32
- search: https://history.state.gov/search?q=Tet+Offensive+1968&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_225_tet_offensive --approved-by joe`. The code never runs it.
