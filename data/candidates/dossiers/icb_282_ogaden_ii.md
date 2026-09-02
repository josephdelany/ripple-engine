# Dossier icb_282_ogaden_ii — OGADEN II

```json
{
 "id": "icb_282_ogaden_ii",
 "built_by": "session A",
 "built_at": "2026-09-02T19:17:45+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 282,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=282",
  "trigdate": "1977-07-22",
  "termdate": "1978-03-14",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1977-07-22",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  520,
  530
 ],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p1/d33",
  "title": "33. Memorandum From the Vice President\u2019s Assistant for National Security Affairs (Clift) to Vice President Mondale (1977\u20131980, Volume XVII, Part 1, Horn of Africa)",
  "date": "1977-10-27",
  "window": [
   "1977-06-22",
   "1978-04-13"
  ],
  "query": "Ogaden Ii 1977",
  "search_url": "https://history.state.gov/search?q=Ogaden+Ii+1977&within=documents",
  "retrieved_at": "2026-09-02T19:17:45+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v17p1/d33",
    "title": "33. Memorandum From the Vice President\u2019s Assistant for National Security Affairs (Clift) to Vice President Mondale (1977\u20131980, Volume XVII, Part 1, Horn of Africa)",
    "page_date": "1977-10-27",
    "retrieved_at": "2026-09-02T19:17:45+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 282 **OGADEN II**: trigdate 1977-07-22, termdate 1978-03-14, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=282

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 520: UNMAPPED (registered state set)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:17:45+00:00: **33. Memorandum From the Vice President’s Assistant for National Security Affairs (Clift) to Vice President Mondale (1977–1980, Volume XVII, Part 1, Horn of Africa)** — page date 1977-10-27 (window 1977-06-22..1978-04-13)
  https://history.state.gov/historicaldocuments/frus1977-80v17p1/d33
- search: https://history.state.gov/search?q=Ogaden+Ii+1977&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_282_ogaden_ii --approved-by joe`. The code never runs it.
