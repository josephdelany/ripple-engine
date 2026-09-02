# Dossier icb_187_west_irian_ii — WEST IRIAN II

```json
{
 "id": "icb_187_west_irian_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:55+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 187,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=187",
  "trigdate": "1961-09-26",
  "termdate": "1962-08-15",
  "viol": 2,
  "forout": 1
 },
 "event_date": "1961-09-26",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.indonesia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  210
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1961-63v08/d69",
  "title": "69. Summary of President Kennedy\u2019s Remarks to the 496th Meeting of the National Security Council (1961\u20131963, Volume VIII, National Security Policy)",
  "date": "1962-01-18",
  "window": [
   "1961-08-27",
   "1962-09-14"
  ],
  "query": "West Irian Ii 1961",
  "search_url": "https://history.state.gov/search?q=West+Irian+Ii+1961&within=documents",
  "retrieved_at": "2026-09-02T19:14:55+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v23/d291",
    "title": "291. Memorandum From the Under Secretary of State (Ball) to President Kennedy (1961\u20131963, Volume XXIII, Southeast Asia)",
    "page_date": "1962-10-10",
    "retrieved_at": "2026-09-02T19:14:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v23/d169",
    "title": "169. Memorandum From Robert H. Johnson of the National Security Council Staff to the President\u2019s Deputy Special Assistant for National Security Affairs (Rostow) (1961\u20131963, Volume XXIII, Southeast Asi",
    "page_date": "1961-04-21",
    "retrieved_at": "2026-09-02T19:14:53+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v23/d175",
    "title": "175. Memorandum From the Deputy Under Secretary of State for Political Affairs (Johnson) to Secretary of State Rusk (1961\u20131963, Volume XXIII, Southeast Asia)",
    "page_date": "1961-05-23",
    "retrieved_at": "2026-09-02T19:14:54+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1961-63v08/d69",
    "title": "69. Summary of President Kennedy\u2019s Remarks to the 496th Meeting of the National Security Council (1961\u20131963, Volume VIII, National Security Policy)",
    "page_date": "1962-01-18",
    "retrieved_at": "2026-09-02T19:14:55+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 187 **WEST IRIAN II**: trigdate 1961-09-26, termdate 1962-08-15, viol 2, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=187

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 210: UNMAPPED
- 850: country.indonesia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.indonesia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:14:55+00:00: **69. Summary of President Kennedy’s Remarks to the 496th Meeting of the National Security Council (1961–1963, Volume VIII, National Security Policy)** — page date 1962-01-18 (window 1961-08-27..1962-09-14)
  https://history.state.gov/historicaldocuments/frus1961-63v08/d69
- search: https://history.state.gov/search?q=West+Irian+Ii+1961&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_187_west_irian_ii --approved-by joe`. The code never runs it.
