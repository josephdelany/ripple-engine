# Dossier icb_196_cuban_missiles — CUBAN MISSILES

```json
{
 "id": "icb_196_cuban_missiles",
 "built_by": "session A",
 "built_at": "2026-09-02T19:15:09+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 196,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=196",
  "trigdate": "1962-10-16",
  "termdate": "1962-11-20",
  "viol": 2,
  "forout": 2
 },
 "event_date": "1962-10-16",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "target"
  },
  {
   "entity": "country.russia",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  40
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v11/d49",
  "title": "49. Editorial Note (1961\u20131963, Volume XI, Cuban Missile Crisis and Aftermath)",
  "date": "1962-10-23",
  "window": [
   "1962-09-16",
   "1962-12-20"
  ],
  "query": "Cuban Missiles 1962",
  "search_url": "https://history.state.gov/search?q=Cuban+Missiles+1962&within=documents",
  "retrieved_at": "2026-09-02T19:15:09+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v23/d77",
    "title": "77. Memorandum of Conversation (1977\u20131980, Volume XXIII, Mexico, Cuba, and the Caribbean)",
    "page_date": "1979-09-24",
    "retrieved_at": "2026-09-02T19:15:08+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v11/d49",
    "title": "49. Editorial Note (1961\u20131963, Volume XI, Cuban Missile Crisis and Aftermath)",
    "page_date": "1962-10-23",
    "retrieved_at": "2026-09-02T19:15:09+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 196 **CUBAN MISSILES**: trigdate 1962-10-16, termdate 1962-11-20, viol 2, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=196

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 40: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.usa:target, country.russia:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:15:09+00:00: **49. Editorial Note (1961–1963, Volume XI, Cuban Missile Crisis and Aftermath)** — page date 1962-10-23 (window 1962-09-16..1962-12-20)
  https://history.state.gov/historicaldocuments/frus1961-63v11/d49
- search: https://history.state.gov/search?q=Cuban+Missiles+1962&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_196_cuban_missiles --approved-by joe`. The code never runs it.
