# Dossier icb_315_solidarity — SOLIDARITY

```json
{
 "id": "icb_315_solidarity",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:47+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 315,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=315",
  "trigdate": "1980-08-14",
  "termdate": "1981-12-13",
  "viol": 1,
  "forout": 4
 },
 "event_date": "1980-08-14",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  265,
  290,
  315
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v03/d124",
  "title": "124. Information Memorandum From the Assistant Secretary of State for European Affairs (Eagleburger) to Secretary of State Haig (1981\u20131988, Volume III, Soviet Union, January 1981\u2013January 1983)",
  "date": "1982-01-04",
  "window": [
   "1980-07-15",
   "1982-01-12"
  ],
  "query": "Solidarity 1980",
  "search_url": "https://history.state.gov/search?q=Solidarity+1980&within=documents",
  "retrieved_at": "2026-09-02T19:18:47+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v06/d309",
    "title": "309. Editorial Note (1977\u20131980, Volume VI, Soviet Union)",
    "page_date": "1977-01-20",
    "retrieved_at": "2026-09-02T19:18:45+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v12/d229",
    "title": "229. Memorandum From the President\u2019s Assistant for National Security Affairs (Brzezinski) to Secretary of State Vance (1977\u20131980, Volume XII, Afghanistan)",
    "page_date": "1980-03-08",
    "retrieved_at": "2026-09-02T19:18:45+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v20/d42",
    "title": "42. Editorial Note (1977\u20131980, Volume XX, Eastern Europe)",
    "page_date": "1980-01-28",
    "retrieved_at": "2026-09-02T19:18:46+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v03/d124",
    "title": "124. Information Memorandum From the Assistant Secretary of State for European Affairs (Eagleburger) to Secretary of State Haig (1981\u20131988, Volume III, Soviet Union, January 1981\u2013January 1983)",
    "page_date": "1982-01-04",
    "retrieved_at": "2026-09-02T19:18:47+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 315 **SOLIDARITY**: trigdate 1980-08-14, termdate 1981-12-13, viol 1, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=315

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 265: UNMAPPED
- 290: UNMAPPED
- 315: UNMAPPED
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:47+00:00: **124. Information Memorandum From the Assistant Secretary of State for European Affairs (Eagleburger) to Secretary of State Haig (1981–1988, Volume III, Soviet Union, January 1981–January 1983)** — page date 1982-01-04 (window 1980-07-15..1982-01-12)
  https://history.state.gov/historicaldocuments/frus1981-88v03/d124
- search: https://history.state.gov/search?q=Solidarity+1980&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_315_solidarity --approved-by joe`. The code never runs it.
