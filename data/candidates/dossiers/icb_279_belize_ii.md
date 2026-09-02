# Dossier icb_279_belize_ii — BELIZE II

```json
{
 "id": "icb_279_belize_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:40+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 279,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=279",
  "trigdate": "1977-06-25",
  "termdate": "1977-07-28",
  "viol": 1,
  "forout": 2
 },
 "event_date": "1977-06-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d333",
  "title": "333. Telegram From Secretary of State Vance\u2019s Delegation to the Department of State (1977\u20131980, Volume XXIV, South America; Latin America Region)",
  "date": "1977-06-19",
  "window": [
   "1977-05-26",
   "1977-08-27"
  ],
  "query": "Belize Ii 1977",
  "search_url": "https://history.state.gov/search?q=Belize+Ii+1977&within=documents",
  "retrieved_at": "2026-09-02T19:17:40+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v23/d351",
    "title": "351. Memorandum From the President\u2019s Assistant for National Security Affairs (Brzezinski) to Secretary of State Vance (1977\u20131980, Volume XXIII, Mexico, Cuba, and the Caribbean)",
    "page_date": "1977-09-07",
    "retrieved_at": "2026-09-02T19:17:37+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v15/d42",
    "title": "42. Strategy Paper on Guatemala Prepared in the Department of State (1977\u20131980, Volume XV, Central America)",
    "page_date": "1980-07-14",
    "retrieved_at": "2026-09-02T19:17:38+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v15/d1",
    "title": "1. Telegram From the Embassy in Guatemala to the Department of State (1977\u20131980, Volume XV, Central America)",
    "page_date": "1977-03-11",
    "retrieved_at": "2026-09-02T19:17:39+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d31",
    "title": "31. Memorandum of Conversation (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
    "page_date": "1977-10-12",
    "retrieved_at": "2026-09-02T19:17:39+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v24/d333",
    "title": "333. Telegram From Secretary of State Vance\u2019s Delegation to the Department of State (1977\u20131980, Volume XXIV, South America; Latin America Region)",
    "page_date": "1977-06-19",
    "retrieved_at": "2026-09-02T19:17:40+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 279 **BELIZE II**: trigdate 1977-06-25, termdate 1977-07-28, viol 1, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=279

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.gbr:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:40+00:00: **333. Telegram From Secretary of State Vance’s Delegation to the Department of State (1977–1980, Volume XXIV, South America; Latin America Region)** — page date 1977-06-19 (window 1977-05-26..1977-08-27)
  https://history.state.gov/historicaldocuments/frus1977-80v24/d333
- search: https://history.state.gov/search?q=Belize+Ii+1977&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_279_belize_ii --approved-by joe`. The code never runs it.
