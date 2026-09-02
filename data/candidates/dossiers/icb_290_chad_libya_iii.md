# Dossier icb_290_chad_libya_iii — CHAD/LIBYA III

```json
{
 "id": "icb_290_chad_libya_iii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:57+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 290,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=290",
  "trigdate": "1978-04-15",
  "termdate": "1978-08-28",
  "viol": 4,
  "forout": 2
 },
 "event_date": "1978-04-15",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "target"
  },
  {
   "entity": "country.libya",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d35",
  "title": "35. Memorandum of Conversation (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
  "date": "1978-06-08",
  "window": [
   "1978-03-16",
   "1978-09-27"
  ],
  "query": "Chad Libya Iii 1978",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+Iii+1978&within=documents",
  "retrieved_at": "2026-09-02T19:17:52+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p2/d35",
    "title": "35. Memorandum of Conversation (1977\u20131980, Volume XVII, Part 2, Sub-Saharan Africa)",
    "page_date": "1978-06-08",
    "retrieved_at": "2026-09-02T19:17:52+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 290 **CHAD/LIBYA III**: trigdate 1978-04-15, termdate 1978-08-28, viol 4, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=290

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.fra:target, country.libya:actor

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:52+00:00: **35. Memorandum of Conversation (1977–1980, Volume XVII, Part 2, Sub-Saharan Africa)** — page date 1978-06-08 (window 1978-03-16..1978-09-27)
  https://history.state.gov/historicaldocuments/frus1977-80v17p2/d35
- search: https://history.state.gov/search?q=Chad+Libya+Iii+1978&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_290_chad_libya_iii --approved-by joe`. The code never runs it.
