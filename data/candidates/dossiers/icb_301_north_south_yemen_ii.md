# Dossier icb_301_north_south_yemen_ii — NORTH/SOUTH YEMEN II

```json
{
 "id": "icb_301_north_south_yemen_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 301,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=301",
  "trigdate": "1979-02-24",
  "termdate": "1979-03-28",
  "viol": 4,
  "forout": 1
 },
 "event_date": "1979-02-24",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.yemen",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  680
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v27/d114",
  "title": "114. Memorandum of Conversation (1977\u20131980, Volume XXVII, Western Europe)",
  "date": "1979-03-06",
  "window": [
   "1979-01-25",
   "1979-04-27"
  ],
  "query": "North South Yemen Ii 1979",
  "search_url": "https://history.state.gov/search?q=North+South+Yemen+Ii+1979&within=documents",
  "retrieved_at": "2026-09-02T19:18:22+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v18/d290",
    "title": "290. Message From the United States Commander in Chief European Command to AIG (1977\u20131980, Volume XVIII, Middle East Region; Arabian Peninsula)",
    "page_date": "1979-10-30",
    "retrieved_at": "2026-09-02T19:18:20+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v18/d40",
    "title": "40. Summary of Conclusions of a Special Coordination Committee Meeting (1977\u20131980, Volume XVIII, Middle East Region; Arabian Peninsula)",
    "page_date": "1980-01-14",
    "retrieved_at": "2026-09-02T19:18:21+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v18/d51",
    "title": "51. Memorandum From the President\u2019s Assistant for National Security Affairs (Brzezinski) to President Carter (1977\u20131980, Volume XVIII, Middle East Region; Arabian Peninsula)",
    "page_date": "1980-01-30",
    "retrieved_at": "2026-09-02T19:18:21+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v27/d114",
    "title": "114. Memorandum of Conversation (1977\u20131980, Volume XXVII, Western Europe)",
    "page_date": "1979-03-06",
    "retrieved_at": "2026-09-02T19:18:22+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 301 **NORTH/SOUTH YEMEN II**: trigdate 1979-02-24, termdate 1979-03-28, viol 4, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=301

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 678: country.yemen (registered state set)
- 680: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.yemen:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:22+00:00: **114. Memorandum of Conversation (1977–1980, Volume XXVII, Western Europe)** — page date 1979-03-06 (window 1979-01-25..1979-04-27)
  https://history.state.gov/historicaldocuments/frus1977-80v27/d114
- search: https://history.state.gov/search?q=North+South+Yemen+Ii+1979&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_301_north_south_yemen_ii --approved-by joe`. The code never runs it.
