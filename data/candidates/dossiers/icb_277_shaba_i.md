# Dossier icb_277_shaba_i — SHABA I

```json
{
 "id": "icb_277_shaba_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:36+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 277,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=277",
  "trigdate": "1977-03-08",
  "termdate": "1977-05-26",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1977-03-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.congo_drc",
   "role": "unknown"
  },
  {
   "entity": "country.ago",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d73",
  "title": "73. Memorandum From Secretary of State Vance to President Carter (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
  "date": "1977-03-10",
  "window": [
   "1977-02-06",
   "1977-06-25"
  ],
  "query": "Shaba I 1977",
  "search_url": "https://history.state.gov/search?q=Shaba+I+1977&within=documents",
  "retrieved_at": "2026-09-02T19:17:35+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d73",
    "title": "73. Memorandum From Secretary of State Vance to President Carter (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
    "page_date": "1977-03-10",
    "retrieved_at": "2026-09-02T19:17:35+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 277 **SHABA I**: trigdate 1977-03-08, termdate 1977-05-26, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=277

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 490: country.congo_drc
- 540: country.ago (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.congo_drc:unknown, country.ago:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:35+00:00: **73. Memorandum From Secretary of State Vance to President Carter (1977–1980, Volume XVII, Part 2, Sub-Saharan Africa)** — page date 1977-03-10 (window 1977-02-06..1977-06-25)
  https://history.state.gov/historicaldocuments/frus1977-80v17p2/d73
- search: https://history.state.gov/search?q=Shaba+I+1977&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_277_shaba_i --approved-by joe`. The code never runs it.
