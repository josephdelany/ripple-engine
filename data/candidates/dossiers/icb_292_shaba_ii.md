# Dossier icb_292_shaba_ii — SHABA II

```json
{
 "id": "icb_292_shaba_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:01+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 292,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=292",
  "trigdate": "1978-05-11",
  "termdate": "1978-07-28",
  "viol": 3,
  "forout": 1
 },
 "event_date": "1978-05-11",
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
   "entity": "country.fra",
   "role": "unknown"
  },
  {
   "entity": "country.congo_drc",
   "role": "unknown"
  },
  {
   "entity": "country.ago",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  211
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d13",
  "title": "13. Telegram From the Mission to the United Nations to the Department of State (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
  "date": "1978-06-14",
  "window": [
   "1978-04-11",
   "1978-08-27"
  ],
  "query": "Shaba Ii 1978",
  "search_url": "https://history.state.gov/search?q=Shaba+Ii+1978&within=documents",
  "retrieved_at": "2026-09-02T19:18:00+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d116",
    "title": "116. Memorandum From the Assistant Secretary of Defense for International Security Affairs (McGiffert) to the Deputy Secretary of Defense (Duncan) (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
    "page_date": "1978-12-28",
    "retrieved_at": "2026-09-02T19:18:00+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d13",
    "title": "13. Telegram From the Mission to the United Nations to the Department of State (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
    "page_date": "1978-06-14",
    "retrieved_at": "2026-09-02T19:18:00+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 292 **SHABA II**: trigdate 1978-05-11, termdate 1978-07-28, viol 3, forout 1. Page: https://www.icb.umd.edu/dataviewer/?crisno=292

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 211: UNMAPPED
- 220: country.fra (registered state set)
- 490: country.congo_drc
- 540: country.ago (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.fra:unknown, country.congo_drc:unknown, country.ago:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:18:00+00:00: **13. Telegram From the Mission to the United Nations to the Department of State (1977–1980, Volume XVII, Part 2, Sub-Saharan Africa)** — page date 1978-06-14 (window 1978-04-11..1978-08-27)
  https://history.state.gov/historicaldocuments/frus1977-80v17p2/d13
- search: https://history.state.gov/search?q=Shaba+Ii+1978&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_292_shaba_ii --approved-by joe`. The code never runs it.
