# Dossier icb_110_communism_in_poland — COMMUNISM IN POLAND

```json
{
 "id": "icb_110_communism_in_poland",
 "built_by": "session A",
 "built_at": "2026-09-02T19:12:56+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 110,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=110",
  "trigdate": "1946-06-28",
  "termdate": "1947-01-19",
  "viol": 1,
  "forout": 6
 },
 "event_date": "1946-06-28",
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
 "unmapped_ccodes": [],
 "second_source": {
  "found": true,
  "route": "FRUS",
  "url": "https://history.state.gov/historicaldocuments/frus1946v06/d523",
  "title": "Memorandum by the Assistant Chief of the Division of Eastern European Affairs (Stevens) (1946, Volume VI, Eastern Europe, The Soviet Union)",
  "date": "1946-07-26",
  "window": [
   "1946-05-29",
   "1947-02-18"
  ],
  "query": "Communism In Poland 1946",
  "search_url": "https://history.state.gov/search?q=Communism+In+Poland+1946&within=documents",
  "retrieved_at": "2026-09-02T19:10:57+00:00",
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1949v05/d307",
    "title": "Department of State Policy Statement (1949, Volume V, Eastern Europe; The Soviet Union)",
    "page_date": "1949-06-25",
    "retrieved_at": "2026-09-02T19:10:56+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1946v06/d523",
    "title": "Memorandum by the Assistant Chief of the Division of Eastern European Affairs (Stevens) (1946, Volume VI, Eastern Europe, The Soviet Union)",
    "page_date": "1946-07-26",
    "retrieved_at": "2026-09-02T19:10:57+00:00"
   }
  ]
 },
 "admissible": true,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 110 **COMMUNISM IN POLAND**: trigdate 1946-06-28, termdate 1947-01-19, viol 1, forout 6. Page: https://www.icb.umd.edu/dataviewer/?crisno=110

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol 1); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- FRUS document opened 2026-09-02T19:10:57+00:00: **Memorandum by the Assistant Chief of the Division of Eastern European Affairs (Stevens) (1946, Volume VI, Eastern Europe, The Soviet Union)** — page date 1946-07-26 (window 1946-05-29..1947-02-18)
  https://history.state.gov/historicaldocuments/frus1946v06/d523
- search: https://history.state.gov/search?q=Communism+In+Poland+1946&within=documents

## Admissible: **yes**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_110_communism_in_poland --approved-by joe`. The code never runs it.
