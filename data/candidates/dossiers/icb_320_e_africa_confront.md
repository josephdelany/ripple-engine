# Dossier icb_320_e_africa_confront — E. AFRICA CONFRONT.

```json
{
 "id": "icb_320_e_africa_confront",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:55+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 320,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=320",
  "trigdate": "1980-12-05",
  "termdate": "1981-06-28",
  "viol": 1,
  "forout": 1
 },
 "event_date": "1980-12-05",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  501,
  520,
  530
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d17",
  "title": "17. Report Prepared by the Department of State Transition Team (1981\u20131988, Volume I, Foundations of Foreign Policy)",
  "date": "1980-12-22",
  "window": [
   "1980-11-05",
   "1981-07-28"
  ],
  "query": "E  Africa Confront 1980",
  "search_url": "https://history.state.gov/search?q=E++Africa+Confront+1980&within=documents",
  "retrieved_at": "2026-09-02T19:18:54+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p1/d36",
    "title": "36. Memorandum From the Assistant Secretary of Defense for International Security Affairs (McGiffert) to Secretary of Defense Brown (1977\u20131980, Volume XVII, Part 1, Horn of Africa)",
    "page_date": "1977-12-20",
    "retrieved_at": "2026-09-02T19:18:51+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v18/d84",
    "title": "84. Summary of Conclusions of a Special Coordination Committee Meeting (1977\u20131980, Volume XVIII, Middle East Region; Arabian Peninsula)",
    "page_date": "1980-06-09",
    "retrieved_at": "2026-09-02T19:18:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v01/d26",
    "title": "26. Memorandum From the President\u2019s Assistant for National Security Affairs (Brzezinski) to President Carter (1977\u20131980, Volume I, Foundations of Foreign Policy)",
    "page_date": "1977-03-05",
    "retrieved_at": "2026-09-02T19:18:52+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v18/d41",
    "title": "41. Memorandum From Jasper Welch and Fritz Ermarth of the National Security Council Staff to the President\u2019s Assistant for National Security Affairs (Brzezinski) (1977\u20131980, Volume XVIII, Middle East ",
    "page_date": "1980-01-16",
    "retrieved_at": "2026-09-02T19:18:53+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d70",
    "title": "70. Memorandum From Henry Nau of the National Security Council Staff to Members of the National Security Council Staff (1981\u20131988, Volume I, Foundations of Foreign Policy)",
    "page_date": "1981-11-25",
    "retrieved_at": "2026-09-02T19:18:54+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v01/d17",
    "title": "17. Report Prepared by the Department of State Transition Team (1981\u20131988, Volume I, Foundations of Foreign Policy)",
    "page_date": "1980-12-22",
    "retrieved_at": "2026-09-02T19:18:54+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 320 **E. AFRICA CONFRONT.**: trigdate 1980-12-05, termdate 1981-06-28, viol 1, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=320

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 501: UNMAPPED
- 520: UNMAPPED (registered state set)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:54+00:00: **17. Report Prepared by the Department of State Transition Team (1981–1988, Volume I, Foundations of Foreign Policy)** — page date 1980-12-22 (window 1980-11-05..1981-07-28)
  https://history.state.gov/historicaldocuments/frus1981-88v01/d17
- search: https://history.state.gov/search?q=E++Africa+Confront+1980&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_320_e_africa_confront --approved-by joe`. The code never runs it.
