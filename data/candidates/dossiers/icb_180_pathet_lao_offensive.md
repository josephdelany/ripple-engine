# Dossier icb_180_pathet_lao_offensive — PATHET LAO OFFENSIVE

```json
{
 "id": "icb_180_pathet_lao_offensive",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:41+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 180,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=180",
  "trigdate": "1961-03-09",
  "termdate": "1961-05-16",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1961-03-09",
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
   "entity": "country.thailand",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v24/d42",
  "title": "42. Telegram From Secretary of State Rusk to the Department of State (1961\u20131963, Volume XXIV, Laos Crisis)",
  "date": "1961-03-27",
  "window": [
   "1961-02-07",
   "1961-06-15"
  ],
  "query": "Pathet Lao Offensive 1961",
  "search_url": "https://history.state.gov/search?q=Pathet+Lao+Offensive+1961&within=documents",
  "retrieved_at": "2026-09-02T19:14:40+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1964-68v28/d246",
    "title": "246. Report by the Chief of the Far East Division, Directorate for Plans, Central Intelligence Agency (Colby) to Director of Central Intelligence Helms (1964\u20131968, Volume XXVIII, Laos)",
    "page_date": "1966-08-16",
    "retrieved_at": "2026-09-02T19:14:39+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v24/d177",
    "title": "177. Memorandum From the Executive Secretary of the Department of State (Battle) to the President\u2019s Special Assistant for National Security Affairs (Bundy) (1961\u20131963, Volume XXIV, Laos Crisis)",
    "page_date": "1961-09-08",
    "retrieved_at": "2026-09-02T19:14:39+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v24/d42",
    "title": "42. Telegram From Secretary of State Rusk to the Department of State (1961\u20131963, Volume XXIV, Laos Crisis)",
    "page_date": "1961-03-27",
    "retrieved_at": "2026-09-02T19:14:40+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 180 **PATHET LAO OFFENSIVE**: trigdate 1961-03-09, termdate 1961-05-16, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=180

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 800: country.thailand

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.thailand:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:40+00:00: **42. Telegram From Secretary of State Rusk to the Department of State (1961–1963, Volume XXIV, Laos Crisis)** — page date 1961-03-27 (window 1961-02-07..1961-06-15)
  https://history.state.gov/historicaldocuments/frus1961-63v24/d42
- search: https://history.state.gov/search?q=Pathet+Lao+Offensive+1961&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_180_pathet_lao_offensive --approved-by joe`. The code never runs it.
