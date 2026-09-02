# Dossier icb_118_junagadh — JUNAGADH

```json
{
 "id": "icb_118_junagadh",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:02+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 118,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=118",
  "trigdate": "1947-08-17",
  "termdate": "1948-02-24",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1947-08-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  },
  {
   "entity": "country.pak",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1948v05p1/d205",
  "title": "The Charg\u00e9 in Pakistan (Lewis) to the Secretary of State (1948, Volume V, Part 1, The Near East, South Asia, and Africa)",
  "date": "1948-01-01",
  "window": [
   "1947-07-18",
   "1948-03-25"
  ],
  "query": "Junagadh 1947",
  "search_url": "https://history.state.gov/search?q=Junagadh+1947&within=documents",
  "retrieved_at": "2026-09-02T19:13:02+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v05p1/d205",
    "title": "The Charg\u00e9 in Pakistan (Lewis) to the Secretary of State (1948, Volume V, Part 1, The Near East, South Asia, and Africa)",
    "page_date": "1948-01-01",
    "retrieved_at": "2026-09-02T19:13:02+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 118 **JUNAGADH**: trigdate 1947-08-17, termdate 1948-02-24, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=118

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)
- 770: country.pak

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.india:unknown, country.pak:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:13:02+00:00: **The Chargé in Pakistan (Lewis) to the Secretary of State (1948, Volume V, Part 1, The Near East, South Asia, and Africa)** — page date 1948-01-01 (window 1947-07-18..1948-03-25)
  https://history.state.gov/historicaldocuments/frus1948v05p1/d205
- search: https://history.state.gov/search?q=Junagadh+1947&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_118_junagadh --approved-by joe`. The code never runs it.
